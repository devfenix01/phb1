#!/usr/bin/env python3
"""Empacota o site em um único arquivo HTML (CSS e JS embutidos).

Uso:  python3 build.py
Saída: dist/SIGAE.html
"""
import pathlib, re

RAIZ = pathlib.Path(__file__).parent
SITE = RAIZ
SAIDA = RAIZ / "dist" / "SIGAE.html"

html = (SITE / "index.html").read_text(encoding="utf-8")
css = (SITE / "assets" / "styles.css").read_text(encoding="utf-8")
vendedores = [
    (SITE / "vendor" / "qrcode.min.js").read_text(encoding="utf-8"),
    (SITE / "vendor" / "jsqr.js").read_text(encoding="utf-8"),
]
modulos = [
    (SITE / "assets" / "nucleo.js").read_text(encoding="utf-8"),
    (SITE / "assets" / "ui.js").read_text(encoding="utf-8"),
    (SITE / "assets" / "gestor.js").read_text(encoding="utf-8"),
    (SITE / "assets" / "app.js").read_text(encoding="utf-8"),
]

html = html.replace(
    '<link rel="stylesheet" href="assets/styles.css" />',
    "<style>\n" + css + "\n</style>",
)
scripts = "\n".join(f"<script>\n{js}\n</script>" for js in vendedores + modulos)
html = re.sub(
    r'\s*<script src="vendor/qrcode\.min\.js"></script>.*?<script src="assets/app\.js"></script>',
    lambda _m: "\n  " + scripts,
    html,
    flags=re.S,
)

# marca de arquivo único (útil para depuração)
html = html.replace("<head>", "<head>\n  <!-- arquivo único gerado por build.py -->")

SAIDA.parent.mkdir(exist_ok=True)
SAIDA.write_text(html, encoding="utf-8")
print(f"{SAIDA} · {len(html)/1024:.0f} KB")
