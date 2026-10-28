"""
Gera as imagens otimizadas do site a partir dos arquivos originais da raiz do projeto.
Uso (na raiz do projeto):  python tools/build-images.py
Requer: Pillow (pip install pillow)
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "img"
OUT.mkdir(parents=True, exist_ok=True)


def load(name):
    return Image.open(ROOT / name).convert("RGB")


def save_webp(img, name, widths, quality=78):
    """Salva a imagem em WebP nas larguras pedidas (nunca amplia)."""
    for w in widths:
        w = min(w, img.width)
        h = round(img.height * w / img.width)
        im = img if w == img.width else img.resize((w, h), Image.LANCZOS)
        im.save(OUT / f"{name}-{w}.webp", "WEBP", quality=quality, method=6)
        print(f"{name}-{w}.webp  {w}x{h}")


# --- Fotos -----------------------------------------------------------------
alinhamento = load("Alinhamento.png")
save_webp(alinhamento, "hero-alinhamento", [520, 855], quality=80)
save_webp(alinhamento.crop((150, 0, 800, 489)), "servico-alinhamento", [420, 650])

save_webp(load("Troca de oleo.png"), "servico-troca-oleo", [420, 847])

cambio = load("Troca de oleo do cambio.png")
save_webp(cambio.crop((0, 0, 847, 470)), "servico-cambio", [520, 847])

save_webp(load("Scanner.png"), "servico-scanner", [420, 845])

revisao = load("Revisão.png")
save_webp(revisao, "servico-revisao", [420, 843])

save_webp(load("Maquina de cartão.png"), "parcelamento", [520, 850])

# Equipamento CAT 501S (círculo recortado da arte original da MSA)
cat = cambio.crop((14, 474, 242, 702)).resize((228, 228), Image.LANCZOS)
mask = Image.new("L", (228 * 4, 228 * 4), 0)
ImageDraw.Draw(mask).ellipse((8, 8, 228 * 4 - 8, 228 * 4 - 8), fill=255)
mask = mask.resize((228, 228), Image.LANCZOS)
cat_rgba = cat.convert("RGBA")
cat_rgba.putalpha(mask)
cat_rgba.resize((160, 160), Image.LANCZOS).save(OUT / "cat-501s.webp", "WEBP", quality=85)
print("cat-501s.webp")

# --- Logo com fundo transparente ------------------------------------------
logo = Image.open(ROOT / "Logo.png").convert("RGB")
gray = ImageOps.grayscale(logo)
BG = 14
alpha = gray.point(lambda v: 0 if v <= BG + 6 else min(255, round((v - BG) * 255 / (255 - BG))))
white = Image.new("RGBA", logo.size, (255, 255, 255, 0))
white.putalpha(alpha)
bbox = alpha.point(lambda v: 255 if v > 40 else 0).getbbox()
logo_t = white.crop(bbox)
logo_t.save(OUT / "logo-msa.png", optimize=True)
print("logo-msa.png", logo_t.size)

# Separa o símbolo (três faixas) do texto para o favicon
logo_a = logo_t.getchannel("A")
rows = [any(logo_a.getpixel((x, y)) > 40 for x in range(logo_t.width)) for y in range(logo_t.height)]
gap = next(y for y in range(5, len(rows)) if not rows[y])
symbol = logo_t.crop((0, 0, logo_t.width, gap))
symbol = symbol.crop(symbol.getbbox())

def favicon(size, name, pad=0.16):
    canvas = Image.new("RGBA", (size, size), (17, 17, 17, 255))
    inner = round(size * (1 - pad * 2))
    s = symbol.copy()
    s.thumbnail((inner, inner), Image.LANCZOS)
    canvas.alpha_composite(s, ((size - s.width) // 2, (size - s.height) // 2))
    canvas.convert("RGB").save(OUT / name, optimize=True)
    print(name)

favicon(32, "favicon-32.png", pad=0.08)
favicon(180, "apple-touch-icon.png")

# --- Imagem de compartilhamento (Open Graph) ------------------------------
W, H = 1200, 630
og = Image.new("RGB", (W, H), (17, 17, 17))
photo = alinhamento.resize((round(alinhamento.width * H / alinhamento.height), H), Image.LANCZOS)
fade = Image.linear_gradient("L").rotate(90).resize(photo.size)  # 0 à esquerda -> 255 à direita
fade = fade.point(lambda v: min(255, v * 2))
og.paste(photo, (W - photo.width, 0), fade)
d = ImageDraw.Draw(og)
font_dir = Path("C:/Windows/Fonts")
f_title = ImageFont.truetype(str(font_dir / "segoeuib.ttf"), 64)
f_small = ImageFont.truetype(str(font_dir / "segoeuib.ttf"), 24)
og_logo = logo_t.copy()
og_logo.thumbnail((240, 240), Image.LANCZOS)
og.paste(og_logo, (72, 70), og_logo)
d.text((72, 300), "Seu carro merece", font=f_title, fill=(255, 255, 255))
d.text((72, 372), "cuidado de quem", font=f_title, fill=(255, 255, 255))
d.text((72, 444), "entende.", font=f_title, fill=(237, 28, 36))
d.text((74, 540), "DESDE 1992  •  PAULÍNIA/SP", font=f_small, fill=(184, 184, 184))
og.save(OUT / "og-image.jpg", "JPEG", quality=84, optimize=True, progressive=True)
print("og-image.jpg")
