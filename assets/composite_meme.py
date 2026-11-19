"""Build the GTA 6 sick-day meme: composite the real make.fun ghost (cut out of
the press-kit mark) onto the AI-made living-room scene as Player 2 on the couch,
then add big meme captions with PIL. Output: meme.png (1024x1024)."""
from collections import deque
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ENTRY = "/home/hatch/workspace/makefun/gta6-meme-x-01-entry"
SCENE = ENTRY + "/assets/media-generation-gta6-sick-day-scene-0-2ac7c66d-b8c8-49f7-9170-9f58b4c95179.png"
MARK = ENTRY + "/assets/mark-1024.png"
OUT = ENTRY + "/meme.png"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def extract_ghost(path):
    """Cut the white ghost + its star coin out of the magenta-disc mark."""
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(int)
    h, w, _ = a.shape
    white = (a[:, :, 0] > 235) & (a[:, :, 1] > 235) & (a[:, :, 2] > 235)
    black = (a[:, :, 0] < 70) & (a[:, :, 1] < 70) & (a[:, :, 2] < 70)
    walk = white | black
    # Flood-fill from a seed inside the ghost body (white) through white/black.
    mask = np.zeros((h, w), dtype=bool)
    seed = (450, 450)
    q = deque([seed])
    mask[seed] = True
    while q:
        y, x = q.popleft()
        for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
            if 0 <= ny < h and 0 <= nx < w and not mask[ny, nx] and walk[ny, nx]:
                mask[ny, nx] = True
                q.append((ny, nx))
    # Add the magenta star coin: a disc around its centre (the coin's black ring
    # touches the ghost outline, the magenta interior + white star do not).
    yy, xx = np.mgrid[0:h, 0:w]
    coin = (xx - 745) ** 2 + (yy - 478) ** 2 <= 138 ** 2
    mask |= coin
    # Soft edge: blur the alpha a touch.
    alpha = Image.fromarray((mask * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(1.2))
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.paste(im.convert("RGBA"), (0, 0), alpha)
    # Trim transparent borders.
    bbox = out.getbbox()
    return out.crop(bbox)


def outlined_text(draw, cx, y, text, font, fill=(255, 255, 255), stroke=(0, 0, 0), sw=8):
    tw = draw.textlength(text, font=font)
    draw.text((cx - tw / 2, y), text, font=font, fill=fill,
              stroke_width=sw, stroke_fill=stroke)


def main():
    scene = Image.open(SCENE).convert("RGB")  # 1600x1600
    S = scene.size[0]
    ghost = extract_ghost(MARK)
    # Scale ghost to ~30% of the frame width and lean it slightly, like it is
    # sitting back on the couch cushion next to the man.
    gw = int(S * 0.30)
    gh = int(ghost.size[1] * gw / ghost.size[0])
    ghost = ghost.resize((gw, gh), Image.LANCZOS).rotate(-4, expand=True, resample=Image.BICUBIC)
    # Soft shadow on the cushion under the ghost.
    shadow = Image.new("RGBA", scene.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse([int(S * 0.56), int(S * 0.755), int(S * 0.86), int(S * 0.795)], fill=(0, 0, 0, 110))
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))
    scene = Image.alpha_composite(scene.convert("RGBA"), shadow)
    # Paste ghost: bottom of the ghost sits on the right cushion (~78% down).
    gx = int(S * 0.71) - ghost.size[0] // 2
    gy = int(S * 0.785) - ghost.size[1]
    scene.paste(ghost, (gx, gy), ghost)

    draw = ImageDraw.Draw(scene)
    top_font = ImageFont.truetype(FONT, int(S * 0.068))
    bot_font = ImageFont.truetype(FONT, int(S * 0.074))
    outlined_text(draw, S // 2, int(S * 0.018), "ME CALLING IN SICK", top_font)
    outlined_text(draw, S // 2, int(S * 0.018) + int(S * 0.082), "ON GTA 6 LAUNCH DAY", top_font)
    outlined_text(draw, S // 2, int(S * 0.905), "IT'S VICE CITY FLU", bot_font)

    final = scene.convert("RGB").resize((1024, 1024), Image.LANCZOS)
    final.save(OUT, "PNG")
    print("saved", OUT, final.size)


if __name__ == "__main__":
    main()
