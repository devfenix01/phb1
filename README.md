# SIGAE · IFSC Câmpus Palhoça Bilíngue

Sistema de Gestão da Alimentação Estudantil — site completo (front-end estático, sem build e sem dependências externas).

```
sigae/
├── index.html            página única (SPA com rotas em #/) + configuração do Supabase
├── assets/
│   ├── styles.css        design system (claro/escuro, responsivo)
│   ├── nucleo.js         estado, persistência, contas Google, regras do refeitório
│   ├── ui.js             ícones, componentes, shell, login, telas do estudante
│   ├── gestor.js         telas da gestão
│   └── app.js            rotas, eventos, fluxo de login, câmera/QR, formulários
├── vendor/
│   ├── qrcode.min.js     geração de QR (local, offline)
│   └── jsqr.js           leitura de QR (câmera e foto)
└── supabase/
    └── migrations/       SQL do banco (schema + contas de demonstração)
```

> **Abrindo no VS Code?** Comece por [`COMECE-AQUI.md`](COMECE-AQUI.md) — instalação, Live Server,
> estrutura de pastas e onde mexer em cada arquivo.

## Como abrir

- **Direto:** abra `index.html` no navegador (funciona em `file://`).
- **Servidor local:** `python3 serve.py` → http://localhost:5173 (ou Live Server do VS Code)
- A câmera do leitor de QR exige `https://` ou `localhost`; em `file://` use “Enviar foto do QR Code” ou a matrícula manual.

---

## Login e cadastro com conta Google

O SIGAE entra **com conta Google** e cria o vínculo com a matrícula no primeiro acesso.

**Fluxo do estudante**

1. **Entrar com conta Google** → janela no estilo do Google com as contas já vinculadas + “Usar outra conta”.
2. Conta **nova** → passo “Concluir cadastro”: informar a **matrícula (12 dígitos)**, nome, curso e restrição alimentar.
   - Se a matrícula já existir na base, o vínculo é feito nesse cadastro (nada é duplicado e a tela mostra o nome encontrado).
   - Se não existir, o cadastro é criado já ativo.
3. Conta **já vinculada** → tela de confirmação com perfil/identificador/curso e botão **Entrar** (um toque).
4. Dali em diante, a tela de acesso mostra sua conta no topo: **“Ana Carolina Silva · ana.c@aluno.ifsc.edu.br · Entrar”**.
5. O **perfil** tem a seção *Conta Google* para vincular outra conta ou desvincular.
   - Também é possível gerenciar vínculo pela gestão: a lista de estudantes mostra o e-mail Google de cada aluno.

**Fluxo da gestão:** no passo de cadastro, escolher **Gestão** e informar o identificador `ADM` + 8 dígitos. Gestor desativado é recusado com aviso.

**Acessos já vinculados na demonstração**

| Conta Google | Perfil | Identificador |
|---|---|---|
| `ana.c@aluno.ifsc.edu.br` | Estudante (lactose) | `202610704214` |
| `gustavo@ifsc.edu.br` | Gestão (coordenação) | `ADM20261234` |

Também continuam disponíveis: “Ver como estudante/gestor” (demonstração em 1 clique) e “Entrar com matrícula (sem conta Google)”.

### Modo simulação × OAuth real

O app funciona nos dois modos, sem mudar código:

- **Demonstração (hoje):** o banco está ligado e o estado é gravado no Supabase (selo **“Banco conectado”**). O login Google ainda usa a lista de contas simulada, porque o provedor Google não está habilitado no projeto.
- **OAuth real (a um clique):** a página já tem `SUPABASE_URL`, `SUPABASE_ANON_KEY` e `SIGAE_GOOGLE_ATIVO = true`. Antes de redirecionar, o app consulta `/auth/v1/settings`; se o Google estiver desligado no Supabase, ele **não** manda o usuário para um erro 400 — avisa e abre o modo demonstração. Assim que o provedor for habilitado, o mesmo botão passa a abrir a tela de contas do Google, e o retorno (`#access_token=…`) cria a sessão e grava o vínculo em `sigae_contas`. Nada precisa ser refeito.

#### Estado do projeto Supabase (`sigae`) — já feito

| Item | Situação |
| --- | --- |
| Projeto | `sigae` · ref `akvlrotxvjuvfvigymiq` · us-west-2 · Postgres 17.11 · **ACTIVE_HEALTHY** |
| URL | `https://akvlrotxvjuvfvigymiq.supabase.co` |
| Migration | `sigae_schema_inicial` aplicada (`sigae_estado` + `sigae_contas`) |
| RLS | estado: leitura/escrita pela chave anon; contas: cada e-mail vê/escreve só a própria linha |
| Dados | estado `id=1` com `{"versao":1,"origem":"supabase"}`; contas semeadas: `ana.c@aluno.ifsc.edu.br` → 202610704214 e `gustavo@ifsc.edu.br` → ADM20261234 |
| Auth URLs | *Site URL* `http://localhost:8080`; *Redirect URLs*: `localhost:8080`, `127.0.0.1:8080`, `localhost:3000`, `https://*.e2b.app/**`, `https://*.lovable.app/**` |
| Provedor Google | **desligado** (`external_google_enabled: false`) — é o único item que falta |

#### Para ligar o OAuth real (o que falta — só depende das credenciais Google)

1. **Google Cloud Console** → *APIs e serviços → Credenciais* → **ID do cliente OAuth** tipo *Aplicativo da Web*:
   - Origem JavaScript autorizada: `https://akvlrotxvjuvfvigymiq.supabase.co`
   - URI de redirecionamento autorizado: `https://akvlrotxvjuvfvigymiq.supabase.co/auth/v1/callback`
   - Copie **Client ID** e **Client Secret**.
2. **Supabase → Authentication → Providers → Google**: colar o Client ID + Secret e ativar.
   A API de gerenciamento disponível aqui **não** expõe `external_google_client_id/secret` — esse passo é clique no dashboard (ou chamada à Management API com um token pessoal).
3. Pronto: o app já está configurado (`index.html` com URL, chave e trava ligada). Se editar o `index.html`, rode `python3 build.py` para regerar o `SIGAE.html`.
4. Testar: “Entrar com conta Google” → escolher conta → volta logado (primeiro acesso cai no cadastro de vínculo). Depois sair e entrar de novo: um toque na conta.

> Enquanto o passo 2 não acontece, tanto o `SIGAE.html` quanto a prévia avisam “login Google ainda não habilitado” e seguem na demonstração. O banco, o REST, o RLS e as telas já estão prontos e testados.

---

## O que está implementado

**Estudante**
- Início: almoço do dia, ocupação do refeitório, agenda da semana, cardápio, dados e mural.
- Minhas reservas: reservar/cancelar/doar por dia, navegação entre semanas, vagas e capacidade por dia.
- Cardápio do dia (com impressão), mural de doações (resgatar refeição) e perfil (dados, restrição, conta Google, tema, som).
- QR Code pessoal (carteirinha digital) para o balcão.
- Questionário de permanência com as 16 perguntas da pesquisa, incluindo as duas condicionais (`q13` depende de `q12 = Sim`, `q15` de `q14 = Sim`), progresso e obrigatoriedade no primeiro acesso.

**Gestão**
- Painel: reservas ativas, servidas, canceladas/doadas, ocupação, gráfico de 14 dias, restrições a servir, últimas leituras.
- Controle de acesso: leitor de QR pela câmera (jsQR), leitura por foto, matrícula manual, overlay de resultado com bipe (liberado/negado) e aviso de restrição alimentar.
- Reservas do dia: filtros, servir, cancelar, exportar CSV.
- Estudantes: busca, filtros, criar/editar, bloquear, **conta Google vinculada**, exportar CSV.
- Liberações excepcionais, relatórios com agregado do questionário e histórico diário, cardápio editável e parâmetros (capacidade por dia, alerta, gestores, som, status do OAuth, manutenção).

**Regras implementadas** (portadas de `dados.ts`)
- Capacidade diária (padrão + valor próprio por dia da semana), bloqueio de novas reservas quando lotado, alerta de ocupação.
- `registrarAcesso`: não encontrado → bloqueado → já servido → reserva ativa (marca servida) → liberação excepcional (marca usada) → sem reserva (avisa se foi doada).
- Doação/resgate no mural, cancelamento, questionário obrigatório, restrições alimentares visíveis no balcão.
- Vínculo de conta única por e-mail, com validação de matrícula (`2026xxxxxxxx`) e identificador de gestão (`ADMxxxxxxxx`).

## Dados e persistência

- Amostra determinística de 124 estudantes, reservas de três semanas, histórico de 26 dias úteis e ~78 respostas do questionário, geradas de forma reprodutível (`mulberry32`).
- Estado guardado em `localStorage` com fallback em memória (não quebra em iframe de prévia com origem opaca). A base é regenerada a cada novo dia, porque as reservas são da semana corrente.
- **Banco (Supabase):** se a página receber `window.SUPABASE_URL` + `window.SUPABASE_ANON_KEY` e existir a tabela abaixo, o estado é carregado/sincronizado por REST — sem SDK:

```sql
create table if not exists public.sigae_estado (
  id int primary key,
  conteudo jsonb not null,
  atualizado_em timestamptz not null default now()
);

alter table public.sigae_estado enable row level security;

-- demonstração: leitura/escrita anônima (em produção, restrinja a usuários autenticados)
create policy "demo leitura" on public.sigae_estado for select using (true);
create policy "demo escrita" on public.sigae_estado for insert with check (true);
create policy "demo atualizacao" on public.sigae_estado for update using (true);
```

E, para o OAuth real guardar os vínculos:

```sql
create table if not exists public.sigae_contas (
  email text primary key,
  papel text not null check (papel in ('estudante','gestor')),
  matricula text,
  login text,
  nome text,
  provider text default 'Google',
  criado_em timestamptz default now()
);
alter table public.sigae_contas enable row level security;
create policy "conta do proprio email" on public.sigae_contas
  for select using (email = (auth.jwt() ->> 'email'));
```

## Privacidade e limites desta versão

- No **modo simulação** não há verificação de identidade: a conta Google é escolhida numa lista local. Serve para demonstrar o fluxo, não para autenticar de verdade.
- No **modo OAuth**, a identidade é verificada pelo Google; o vínculo com a matrícula ainda deve ser conferido pela coordenação (importação do SUAP) antes de liberar reservas em produção.
- O `anon key` do Supabase é público por natureza; as políticas RLS acima são abertas apenas para a demonstração.
- Não há back-end dedicado: a sincronização é “última escrita vence” no registro único de estado.
