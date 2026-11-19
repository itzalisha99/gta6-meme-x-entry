"""Build the GTA 6 poor-man meme (v2): composite the real make.fun ghost onto
the realistic coin-counting scene — the ghost sits on the bench beside the
poor man, holding out its star coin — then add the caption. Output: meme.png
(1024x1024). Caption concept from Gemini's best pick, wording adapted here."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

sys.path.insert(0, str(Path(__file__).parent))
from composite_meme import extract_ghost  # noqa: E402

ENTRY = "/home/hatch/workspace/makefun/gta6-meme-x-01-entry"
SCENE = ENTRY + "/assets/media-generation-gta6-poor-man-scene-0-bc6cfd9a-7253-4c9c-8f6f-d9f2eba5826f.png"
MARK = ENTRY + "/assets/mark-1024.png"
OUT = ENTRY + "/meme.png"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def outlined_text(draw, cx, y, text, font, fill=(255, 255, 255), stroke=(0, 0, 0), sw=8):
    tw = draw.textlength(text, font=font)
    draw.text((cx - tw / 2, y), text, font=font, fill=fill,
              stroke_width=sw, stroke_fill=stroke)


def main():
    scene = Image.open(SCENE).convert("RGB")
    # The generated scene is 1920x1280 landscape: crop it to a square first
    # (offset 300 keeps the man whole on the left and the bench on the right).
    w, h = scene.size
    side = min(w, h)
    scene = scene.crop((300, 0, 300 + side, side))
    S = scene.size[0]
    ghost = extract_ghost(MARK)
    # Ghost sits on the wooden bench to the man's right, leaning in a little,
    # holding its magenta star coin out toward the jar — like it is chipping in.
    gw = int(S * 0.26)
    gh = int(ghost.size[1] * gw / ghost.size[0])
    ghost = ghost.resize((gw, gh), Image.LANCZOS).rotate(-3, expand=True, resample=Image.BICUBIC)
    shadow = Image.new("RGBA", scene.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse([int(S * 0.66), int(S * 0.635), int(S * 0.90), int(S * 0.665)], fill=(0, 0, 0, 110))
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))
    scene = Image.alpha_composite(scene.convert("RGBA"), shadow)
    gx = int(S * 0.78) - ghost.size[0] // 2
    gy = int(S * 0.66) - ghost.size[1]
    scene.paste(ghost, (gx, gy), ghost)

    draw = ImageDraw.Draw(scene)
    top_font = ImageFont.truetype(FONT, int(S * 0.068))
    bot_font = ImageFont.truetype(FONT, int(S * 0.070))
    outlined_text(draw, S // 2, int(S * 0.018), "GRINDING BOUNTIES", top_font)
    outlined_text(draw, S // 2, int(S * 0.018) + int(S * 0.082), "ON MAKE.FUN", top_font)
    outlined_text(draw, S // 2, int(S * 0.905), "SO I CAN AFFORD GTA 6", bot_font)

    final = scene.convert("RGB").resize((1024, 1024), Image.LANCZOS)
    final.save(OUT, "PNG")
    print("saved", OUT, final.size)


if __name__ == "__main__":
    main()
