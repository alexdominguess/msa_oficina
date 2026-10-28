"""Verificação rápida do index.html: âncoras, arquivos referenciados e links externos.
Uso (na raiz do projeto):  python tools/check-site.py
"""
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
html = (ROOT / "index.html").read_text(encoding="utf-8")
bad = 0

ids = set(re.findall(r'id="([^"]+)"', html))
for a in sorted(set(re.findall(r'href="#([^"]+)"', html))):
    ok = a in ids
    bad += not ok
    print(f"âncora #{a}: {'OK' if ok else 'FALTANDO'}")

files = set(re.findall(r'(?:src|href)="(assets/[^"]+)"', html))
for srcset in re.findall(r'(?:srcset|imagesrcset)="([^"]+)"', html):
    files |= {p.strip().split()[0] for p in srcset.split(",")}
for f in sorted(files):
    ok = (ROOT / f).exists()
    bad += not ok
    print(f"arquivo {f}: {'OK' if ok else 'FALTANDO'}")

blank = re.findall(r"<a [^>]*target=\"_blank\"[^>]*>", html)
no_rel = [b for b in blank if "noopener" not in b]
print(f"links externos: {len(blank)}, sem noopener: {len(no_rel)}")
bad += len(no_rel)

phones = {p for p in re.findall(r"phone=(\d+)", html)}
print("números de WhatsApp usados:", phones)
bad += phones != {"5519974206964"}

for img in re.findall(r"<img [^>]*>", html):
    if "alt=" not in img:
        print("img sem alt:", img[:80])
        bad += 1

print("PROBLEMAS:", bad)
