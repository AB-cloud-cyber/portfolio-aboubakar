from PIL import Image
import os, glob

src = "C:/Users/ABOU SERVICE/Downloads/portfolio-aboubakar/screenshots"
out = "C:/Users/ABOU SERVICE/Downloads/portfolio-aboubakar/figma_export"

# Convert webp to png and find the best cosmic bg
webps = glob.glob(os.path.join(src, "*.webp"))
print(f"Found {len(webps)} webp images:")
bg_images = []
for w in webps:
    name = os.path.basename(w)
    img = Image.open(w).convert("RGBA")
    png_path = os.path.join(src, name.replace(".webp", ".png"))
    # Resize if too small
    if img.size[0] < 200 or img.size[1] < 200:
        # Tile to make larger
        w2, h2 = img.size
        new = Image.new('RGBA', (max(1920, w2*4), max(1080, h2*4)))
        for x in range(0, new.width, w2):
            for y in range(0, new.height, h2):
                new.paste(img, (x, y))
        img = new
    img.save(png_path)
    bg_images.append(png_path)
    print(f"  {name} -> {png_path} ({img.size})")

print(f"\n✅ {len(bg_images)} backgrounds ready")
print(f"\nUse these in figma_export:")
for b in bg_images:
    print(f"  {b}")
