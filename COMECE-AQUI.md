# SIGAE · projeto para VS Code

Sistema de Gestão de Alimentação Estudantil — IFSC Câmpus Palhoça Bilíngue.
HTML + CSS + JavaScript puro (sem build obrigatório, sem dependências de CDN), ligado ao
Supabase do projeto **`sigae`** (`akvlrotxvjuvfvigymiq`).

---

## 1. Abrir no VS Code

1. Descompacte esta pasta (por exemplo em `~/projetos/sigae`).
2. VS Code → **Arquivo → Abrir Pasta…** → escolha a pasta `sigae`.
3. Instale as extensões recomendadas (o VS Code pergunta automaticamente; são só duas):
   - **Live Server** (`ritwickdey.LiveServer`) — *necessária*
   - **Prettier** (`esbenp.prettier-vscode`) — opcional, formatação

## 2. Rodar

**Opção A — Live Server (recomendada)**

Clique com o botão direito em `index.html` → **Open with Live Server**.
Abre em `http://localhost:5173/index.html` (porta já configurada em `.vscode/settings.json`).

**Opção B — terminal / tarefa**

```bash
python3 serve.py          # http://localhost:5173
```
ou `Ctrl+Shift+B` → *SIGAE: gerar arquivo único* e `Ctrl+Shift+P` → *Tasks: Run Task* → *SIGAE: servir local*.

**Opção C — sem servidor**

Abrir `index.html` direto no navegador também funciona (tudo é local). Servidor só é
necessário para testar o retorno do OAuth real com redirect.

## 3. Gerar o arquivo único (para entregar/publicar)

```bash
python3 build.py      # gera dist/SIGAE.html (CSS e JS embutidos, ~500 KB)
```

O `dist/SIGAE.html` roda sozinho — inclusive por `file://` — e é o arquivo que você pode
enviar por e-mail, subir no Drive ou hospedar como página estática.

## 4. Estrutura

```
.
├── index.html                 página e configuração do Supabase (URL, chave, trava do Google)
├── assets/
│   ├── nucleo.js              núcleo: estado, persistência, regras, sessão, Supabase REST, OAuth
│   ├── ui.js                  componentes: ícones, toasts, modais, telas do estudante
│   ├── gestor.js              telas da gestão (painel, acesso, reservas, relatórios, parâmetros)
│   ├── app.js                 rotas #/rota, handlers, fluxo do login Google, câmera/QR
│   └── styles.css             design system (claro/escuro, acessibilidade)
├── vendor/                    bibliotecas locais (QR Code e leitor de QR) — nada de CDN
├── supabase/migrations/       SQL versionado do banco (schema + contas de demonstração)
├── build.py                   empacota tudo em dist/SIGAE.html
├── serve.py                   servidor local (porta 5173)
├── .vscode/                   settings, tasks, launch e extensões recomendadas
└── README.md                  documentação funcional completa
```

## 5. Onde mexer

| Quero… | Arquivo |
| --- | --- |
| mudar cores, tipografia, espaçamentos | `assets/styles.css` (variáveis CSS no topo) |
| mudar regras de reserva/cardápio/QR | `assets/nucleo.js` |
| mudar telas do estudante | `assets/ui.js` |
| mudar telas da gestão | `assets/gestor.js` |
| adicionar rota ou comportamento | `assets/app.js` (`ROTAS`, `tratarClique`, `tratarEnvio`) |
| trocar chaves/URL do Supabase | `index.html` (bloco `<script>` do topo) |

## 6. Supabase já configurado

`index.html` já vem com:

```html
window.SUPABASE_URL = "https://akvlrotxvjuvfvigymiq.supabase.co";
window.SUPABASE_ANON_KEY = "sb_publishable_...";   // chave pública — pode ficar no código
window.SIGAE_GOOGLE_ATIVO = true;                  // liga o OAuth quando o provedor existir
```

- O estado do app é gravado em `public.sigae_estado` (o selo **“Banco conectado”** confirma).
- O vínculo conta Google → matrícula/login fica em `public.sigae_contas` (RLS: cada um só vê o próprio e-mail).
- **Falta apenas** habilitar o provedor Google no Supabase (Client ID + Secret do Google Cloud):
  *Authentication → Providers → Google*. Enquanto isso, o app avisa e usa o login Google
  simulado — nada quebra. Passo a passo em `README.md`.

Para recriar o banco do zero em outro projeto: rode
`supabase/migrations/0001_sigae_schema_inicial.sql` e depois `0002_sigae_contas_demo.sql`
no SQL Editor.

## 7. Acessos de demonstração

| Perfil | Como entrar |
| --- | --- |
| Estudante | Google simulado → `ana.c@aluno.ifsc.edu.br` (Ana Carolina, restrição lactose) |
| Estudante | matrícula `202610704213` (José Gustavo) |
| Gestão | Google simulado → `gustavo@ifsc.edu.br`, ou login `ADM20261234` |
| Gestão inativa | `ADM20265521` (mostra a recusa de acesso) |

Base: 124 estudantes, 2 bloqueados, 17 com restrição alimentar.

## 8. Dicas de VS Code

- `Ctrl+Shift+P` → *Tasks: Run Task* → **SIGAE: servir local (porta 5173)** deixa o servidor no painel.
- `F5` → **Abrir SIGAE no Chrome** (configuração pronta em `.vscode/launch.json`).
- Antes de publicar, rode `python3 build.py` e teste `dist/SIGAE.html` por `file://`.
- Se o navegador reclamar de cache, o `serve.py` já envia `Cache-Control: no-store`.
