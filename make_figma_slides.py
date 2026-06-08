import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

W, H = 1360, 768
out_dir = "C:/Users/ABOU SERVICE/Downloads/portfolio-aboubakar/figma_export"
bg_base = "C:/Users/ABOU SERVICE/Downloads/portfolio-aboubakar/screenshots"
os.makedirs(out_dir, exist_ok=True)

# Load user's cosmic images
bg_files = [
    os.path.join(bg_base, "OIP (1).png"),
    os.path.join(bg_base, "telecharger (1).png"),
    os.path.join(bg_base, "telecharger (2).png"),
    os.path.join(bg_base, "telecharger.png"),
]
# Check if they exist with the actual filenames (may have special chars)
import glob
all_pngs = glob.glob(os.path.join(bg_base, "*.png"))
print("Available PNGs:", all_pngs)

# Use the 1920x1080 ones
bgs = []
for p in all_pngs:
    if "cosmic" not in p and "caisse" not in p and "connectpro" not in p and "dbeaver" not in p and "matplotlib" not in p and "sfa" not in p and "vibetodev" not in p and "basket" not in p:
        img = Image.open(p).resize((W, H))
        print(f"  Using bg: {p} ({img.size})")
        bgs.append(img)

if len(bgs) < 7:
    # Duplicate to fill 7 slides
    while len(bgs) < 7:
        bgs.append(bgs[len(bgs) % len(bgs)])

try:
    title_font = ImageFont.truetype("arial.ttf", 52)
    subtitle_font = ImageFont.truetype("arial.ttf", 28)
    heading_font = ImageFont.truetype("arial.ttf", 36)
    body_font = ImageFont.truetype("arial.ttf", 20)
    small_font = ImageFont.truetype("arial.ttf", 16)
except:
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()
    heading_font = ImageFont.load_default()
    body_font = ImageFont.load_default()
    small_font = ImageFont.load_default()

def overlay_gradient(img):
    """Add dark gradient overlay for readability"""
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 100))
    return Image.alpha_composite(img.convert('RGBA'), overlay)

def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def make_slide(label, draw_func, bg_idx=0):
    img = bgs[bg_idx % len(bgs)].copy()
    img = overlay_gradient(img)
    draw = ImageDraw.Draw(img)
    # Top bar
    draw_rounded_rect(draw, (0, 0, W, 44), 8, (30, 30, 50, 200))
    draw.text((20, 12), "Figma — Portfolio Cosmique", fill=(180, 180, 200), font=small_font)
    draw.text((W-180, 12), label, fill=(232, 184, 75), font=small_font)
    # Call the draw function
    draw_func(draw, img)
    path = os.path.join(out_dir, f"{label.replace(' ','_').lower()}.png")
    img.save(path)
    print(f"  OK: {path}")

def center_text(draw, y, text, font=title_font, color=(255,255,255)):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    draw.text(((W-w)//2, y), text, fill=color, font=font)

# ── SLIDE 1: Cover ──
def cover(d, img):
    d.ellipse([W//2-180, 120, W//2+180, 480], fill=(232, 184, 75, 20), outline=(232, 184, 75, 60), width=2)
    center_text(d, 220, "ABOUBAKAR", title_font)
    center_text(d, 280, "MOHAMAN", title_font, (232, 184, 75))
    center_text(d, 350, "Etudiant en Genie Informatique", subtitle_font, (200, 200, 220))
    center_text(d, 400, "IUT de Douala", subtitle_font, (160, 170, 190))
    draw_rounded_rect(d, (W//2-120, 470, W//2+10, 520), 25, (232, 184, 75))
    d.text((W//2-85, 485), "Decouvrir", fill=(10, 10, 30), font=body_font)
    draw_rounded_rect(d, (W//2+30, 470, W//2+160, 520), 25, None, (232, 184, 75, 150), 2)
    d.text((W//2+55, 485), "CV", fill=(232, 184, 75), font=body_font)
    d.text((W-80, H-30), "1/7 ▶", fill=(232, 184, 75, 120), font=small_font)
make_slide("Cover", cover, 0)

# ── SLIDE 2: About ──
def about(d, img):
    d.text((60, 70), "A PROPOS", fill=(232, 184, 75), font=small_font)
    d.text((60, 95), "Qui suis-je ?", fill=(255, 255, 255), font=heading_font)
    d.rectangle([60, 150, 140, 156], fill=(232, 184, 75))
    texts = [
        "Aboubakar Mohaman, 1re annee Genie Informatique a l'IUT de Douala.",
        "Sur le papier je suis etudiant, dans les faits je prefere coder",
        "un projet que de recopier un cours.",
        "",
        "Ma zone de confort ? Python, les bases de donnees, et tout ce qui",
        "touche a la Data Science et au Machine Learning.",
    ]
    y = 180
    for t in texts:
        d.text((60, y), t, fill=(220, 220, 240), font=body_font)
        y += 32
    for i, (num, lbl) in enumerate([("3", "Projets"), ("5", "Certificats"), ("1", "Package PyPI")]):
        x = 80 + i * 200
        draw_rounded_rect(d, (x, 360, x+150, 430), 12, (20, 20, 50, 180), (232, 184, 75, 40), 1)
        d.text((x+50, 375), num, fill=(232, 184, 75), font=title_font)
        bbox = d.textbbox((0, 0), lbl, font=small_font)
        lw = bbox[2] - bbox[0]
        d.text((x+75-lw//2, 420), lbl, fill=(200, 200, 220), font=small_font)
    d.text((W-80, H-30), "2/7 ▶", fill=(232, 184, 75, 120), font=small_font)
make_slide("About", about, 1)

# ── SLIDE 3: Skills ──
def skills(d, img):
    d.text((60, 70), "COMPETENCES", fill=(232, 184, 75), font=small_font)
    d.text((60, 95), "Ma stack technique", fill=(255, 255, 255), font=heading_font)
    d.rectangle([60, 150, 140, 156], fill=(232, 184, 75))
    colors = [(55, 118, 171), (51, 103, 145), (232, 184, 75), (108, 99, 255)]
    cards = [
        ("Python & Data Science", "Mon royaume. Flask, Pandas,\nNumPy, scikit-learn."),
        ("Bases de donnees", "PostgreSQL, SQLite,\nNeon.tech, DBeaver."),
        ("Frontend", "React, PWA, Jinja2.\nL'IA gere pour moi."),
        ("Outils", "Git, Vercel, PyCharm,\nObsidian, PyPI."),
    ]
    for i, (title, desc) in enumerate(cards):
        x = 60 + (i % 2) * 340
        y = 180 + (i // 2) * 200
        draw_rounded_rect(d, (x, y, x+300, y+170), 14, (20, 20, 50, 200), colors[i], 2)
        d.rectangle([x+4, y, x+8, y+170], fill=colors[i])
        d.text((x+20, y+15), title, fill=(255, 255, 255), font=subtitle_font)
        d.text((x+20, y+60), desc, fill=(210, 210, 230), font=body_font)
    d.text((W-80, H-30), "3/7 ▶", fill=(232, 184, 75, 120), font=small_font)
make_slide("Skills", skills, 2)

# ── SLIDE 4: Projects ──
def projects(d, img):
    d.text((60, 70), "PROJETS", fill=(232, 184, 75), font=small_font)
    d.text((60, 95), "Ce que j'ai construit", fill=(255, 255, 255), font=heading_font)
    d.rectangle([60, 150, 140, 156], fill=(232, 184, 75))
    projs = [
        ("STIMULATION CAISSE", "Full Stack", "Systeme de gestion de caisse — Flask,\ndouble backend SQLite/PostgreSQL."),
        ("CONNECT-PRO", "Full Stack", "Matching startups-investisseurs —\nTF-IDF, cosine similarity, React PWA."),
        ("vibetodev", "Open Source", "Package PyPI transformant un projet\nen parcours d'apprentissage."),
    ]
    for i, (name, badge, desc) in enumerate(projs):
        y = 180 + i * 170
        draw_rounded_rect(d, (60, y, W-60, y+150), 14, (20, 20, 50, 200), (232, 184, 75, 50), 1)
        draw_rounded_rect(d, (W-180, y+12, W-80, y+38), 12, (232, 184, 75))
        bbox = d.textbbox((0, 0), badge, font=small_font)
        bw = bbox[2] - bbox[0]
        d.text((W-130-bw//2, y+15), badge, fill=(10, 10, 30), font=small_font)
        d.text((80, y+15), name, fill=(255, 255, 255), font=subtitle_font)
        d.text((80, y+55), desc, fill=(210, 210, 230), font=body_font)
    d.text((W-80, H-30), "4/7 ▶", fill=(232, 184, 75, 120), font=small_font)
make_slide("Projects", projects, 3)

# ── SLIDE 5: Interests ──
def interests(d, img):
    d.text((60, 70), "CENTRES D'INTERET", fill=(232, 184, 75), font=small_font)
    d.text((60, 95), "Ce qui me definit", fill=(255, 255, 255), font=heading_font)
    d.rectangle([60, 150, 140, 156], fill=(232, 184, 75))
    icons = ["\U0001f3c0", "\U0001f40d", "\U0001f4ca", "\U0001f527"]
    items = [
        ("Basketball", "1m65, shifty, un poison\npour les defenses."),
        ("Python mon amour", "Si ca peut se faire en\nPython, je le fais."),
        ("Data Science & ML", "Faire parler les donnees,\nentrainer des modeles."),
        ("Veille techno", "GitHub trending, Hacker\nNews, Reddit."),
    ]
    for i, (title, desc) in enumerate(items):
        x = 60 + (i % 2) * 350
        y = 180 + (i // 2) * 220
        draw_rounded_rect(d, (x, y, x+300, y+180), 14, (20, 20, 50, 200), (232, 184, 75, 30), 1)
        d.text((x+130, y+15), icons[i], fill=(255, 255, 255), font=subtitle_font)
        d.text((x+20, y+60), title, fill=(255, 255, 255), font=subtitle_font)
        d.text((x+20, y+100), desc, fill=(210, 210, 230), font=body_font)
    d.text((W-80, H-30), "5/7 ▶", fill=(232, 184, 75, 120), font=small_font)
make_slide("Interests", interests, 4)

# ── SLIDE 6: Contact ──
def contact(d, img):
    d.text((60, 70), "CONTACT", fill=(232, 184, 75), font=small_font)
    d.text((60, 95), "Parlons-en", fill=(255, 255, 255), font=heading_font)
    d.rectangle([60, 150, 140, 156], fill=(232, 184, 75))
    info = [
        "\u2709\ufe0f  aboubakar.mohaman@sfaedu.org",
        "\U0001f4ac  +237 681 369 973",
        "\U0001f419  github.com/AB-cloud-cyber",
        "\U0001f4e6  pypi.org/project/vibetodev",
        "\U0001f4cd  Douala, Cameroun",
    ]
    for i, line in enumerate(info):
        d.text((60, 200 + i*40), line, fill=(220, 220, 240), font=body_font)
    draw_rounded_rect(d, (600, 180, W-60, 400), 14, (20, 20, 50, 200), (232, 184, 75, 30), 1)
    d.text((620, 195), "Formulaire de contact", fill=(255, 255, 255), font=body_font)
    for fx, fy, fx2, fy2 in [(620, 230, 780, 265), (620, 280, 780, 315), (620, 330, 860, 390)]:
        draw_rounded_rect(d, (fx, fy, fx2, fy2), 8, (35, 35, 65, 180), (232, 184, 75, 30), 1)
    draw_rounded_rect(d, (620, 410, 770, 455), 25, (232, 184, 75))
    d.text((655, 425), "Envoyer", fill=(10, 10, 30), font=body_font)
    d.text((W-80, H-30), "6/7 ▶", fill=(232, 184, 75, 120), font=small_font)
make_slide("Contact", contact, 5)

# ── SLIDE 7: Thanks ──
def thanks(d, img):
    d.ellipse([W//2-150, 180, W//2+150, 480], fill=(232, 184, 75, 15), outline=(232, 184, 75, 40), width=1)
    center_text(d, 300, "Merci !", title_font, (232, 184, 75))
    center_text(d, 370, "aboubakar.mohaman@sfaedu.org", subtitle_font, (220, 220, 240))
    center_text(d, 410, "Disponible pour un stage en IA et Data", body_font, (180, 190, 210))
    d.text((W-80, H-30), "7/7", fill=(232, 184, 75, 120), font=small_font)
make_slide("Thanks", thanks, 6)

print("\nDone! 7 slides with your cosmic backgrounds.")
