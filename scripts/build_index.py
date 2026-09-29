#!/usr/bin/env python3
"""Regenera el index.html de la raíz con un enlace a cada carpeta que tenga su propio index.html.

El texto de cada enlace sale del <title> de la política de esa carpeta
(sin los prefijos/sufijos "Privacy Policy"). Si no hay <title>, usa el nombre de la carpeta.
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXCLUDED = {"scripts"}

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Privacy Policies</title>
    <style>
        :root {
            --text: #1f2933;
            --muted: #616e7c;
            --heading: #12263f;
            --accent: #1f5f99;
            --border: #d9dee3;
            --bg: #f4f6f8;
            --page: #ffffff;
        }
        * { box-sizing: border-box; }
        body {
            margin: 0;
            padding: 32px 16px;
            background: var(--bg);
            color: var(--text);
            font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, Roboto, "Helvetica Neue", Arial, sans-serif;
            font-size: 16px;
            line-height: 1.7;
        }
        main {
            max-width: 820px;
            margin: 0 auto;
            padding: 48px 56px;
            background: var(--page);
            border: 1px solid var(--border);
            border-radius: 6px;
        }
        h1 {
            margin: 0 0 8px;
            padding-bottom: 16px;
            color: var(--heading);
            font-size: 2rem;
            line-height: 1.3;
            border-bottom: 3px solid var(--accent);
        }
        p { margin: 0 0 1rem; }
        .intro { color: var(--muted); }
        ul { margin: 0 0 1rem; padding-left: 1.5rem; }
        li { margin-bottom: 0.4rem; }
        a { color: var(--accent); text-decoration: underline; }
        a:hover { text-decoration: none; }
        @media (max-width: 600px) {
            body { padding: 0; }
            main { padding: 28px 20px; border: none; border-radius: 0; }
            h1 { font-size: 1.6rem; }
        }
    </style>
</head>
<body>
<main>
<h1>Privacy Policies</h1>
<p class="intro">Privacy policies for the apps published by Zanaxú Apps.</p>
<ul>
{items}
</ul>
</main>
</body>
</html>
"""


def display_name(folder: Path) -> str:
    text = (folder / "index.html").read_text(encoding="utf-8", errors="replace")
    match = re.search(r"<title>(.*?)</title>", text, re.S | re.I)
    if not match:
        return folder.name
    title = html.unescape(match.group(1)).strip()
    title = re.sub(r"^\s*Privacy Policy\s*[-–—:]\s*", "", title, flags=re.I)
    title = re.sub(r"\s*[-–—:]\s*Privacy Policy\s*$", "", title, flags=re.I)
    return title.strip() or folder.name


def main() -> None:
    folders = sorted(
        (d for d in ROOT.iterdir()
         if d.is_dir() and not d.name.startswith(".") and d.name not in EXCLUDED
         and (d / "index.html").is_file()),
        key=lambda d: d.name.lower(),
    )
    items = "\n".join(
        f'<li><a href="{html.escape(d.name)}/">{html.escape(display_name(d), quote=False)}</a></li>'
        for d in folders
    )
    content = PAGE.replace("{items}", items)
    target = ROOT / "index.html"
    if target.exists() and target.read_text(encoding="utf-8") == content:
        print("index.html ya está actualizado.")
        return
    target.write_text(content, encoding="utf-8", newline="\n")
    print(f"index.html regenerado con {len(folders)} política(s).")


if __name__ == "__main__":
    main()
