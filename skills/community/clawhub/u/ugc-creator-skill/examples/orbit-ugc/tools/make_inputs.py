#!/usr/bin/env python3
"""Rebuild the example's two input files from NASA's own downloads (see ../CREDITS.md for the links).

    python3 tools/make_inputs.py <Artemis I launch ~medium.mp4> <Earth Views ~medium.mp4>

Writes orbit-footage.mp4 (the made-up brand's "supplied footage": 8 s of the Artemis I launch and
6 s of Earth from the ISS, no people) and takes/screen.mp4 (a mock screen recording of the made-up
"Example Orbit" app, drawn with Pillow around three Earth stills). Run it from the example folder.
Needs ffmpeg and Pillow. Nothing here is a real app or a real person.
"""
import os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = os.path.join(HERE, "..", "..", "fonts", "Poppins-Bold.ttf")


def ff(*args):
    subprocess.run(["ffmpeg", "-y", "-v", "error", *args], check=True)


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    artemis, earth = sys.argv[1], sys.argv[2]
    from PIL import Image, ImageDraw, ImageFont
    with tempfile.TemporaryDirectory() as tmp:
        vf = "fps=30,scale=640:568:force_original_aspect_ratio=increase,crop=640:568,setsar=1"
        enc = ["-c:v", "libx264", "-crf", "30", "-preset", "slow", "-pix_fmt", "yuv420p"]
        ff("-ss", "44", "-t", "8", "-i", artemis, "-an", "-vf", vf, *enc, os.path.join(tmp, "a.mp4"))
        ff("-ss", "1500", "-t", "6", "-i", earth, "-an", "-vf", vf, *enc, os.path.join(tmp, "e.mp4"))
        with open(os.path.join(tmp, "l.txt"), "w") as fh:
            fh.write("file 'a.mp4'\nfile 'e.mp4'\n")
        ff("-f", "concat", "-safe", "0", "-i", os.path.join(tmp, "l.txt"), *enc, "-movflags", "+faststart",
           "-map_metadata", "-1", os.path.join(HERE, "orbit-footage.mp4"))
        stills = []
        for t in (300, 1200, 2100):
            p = os.path.join(tmp, f"s{t}.jpg")
            ff("-ss", str(t), "-i", earth, "-frames:v", "1", "-q:v", "3", p)
            stills.append(Image.open(p).convert("RGB"))
        W, H, FPS = 540, 960, 15

        def f(s):
            return ImageFont.truetype(FONT, s)

        def card(img, w, h):
            r = max(w / img.width, h / img.height)
            im = img.resize((int(img.width * r) + 1, int(img.height * r) + 1), Image.LANCZOS)
            x, y = (im.width - w) // 2, (im.height - h) // 2
            return im.crop((x, y, x + w, y + h))
        for i in range(FPS * 12):
            t = i / FPS
            fr = Image.new("RGB", (W, H), (12, 14, 22))
            d = ImageDraw.Draw(fr)
            d.text((W // 2, 34), "9:41", font=f(22), fill=(230, 230, 235), anchor="mm")
            d.text((32, 96), "Example Orbit", font=f(34), fill=(255, 255, 255), anchor="lm")
            d.text((32, 136), "Today's space photo", font=f(22), fill=(150, 160, 185), anchor="lm")
            idx, off = (int(t // 2) % 3, (t % 2) / 2) if t < 6 else (1, 0)
            ph = card(stills[idx], W - 64, 560)
            if t < 6 and off > 0.8:
                nxt = card(stills[(idx + 1) % 3], W - 64, 560)
                sh = int((off - 0.8) / 0.2 * (W - 64))
                comb = Image.new("RGB", (W - 64, 560))
                comb.paste(ph, (-sh, 0))
                comb.paste(nxt, (W - 64 - sh, 0))
                ph = comb
            mask = Image.new("L", ph.size, 0)
            ImageDraw.Draw(mask).rounded_rectangle([0, 0, ph.width, ph.height], 28, fill=255)
            fr.paste(ph, (32, 170), mask)
            d.text((32, 760), "Earth from orbit (NASA)", font=f(22), fill=(200, 205, 220), anchor="lm")
            pressed = 7.5 <= t < 8.1
            d.rounded_rectangle([32, 810, W - 32, 880], 35, fill=(220, 180, 40) if pressed else (255, 212, 59))
            d.text((W // 2, 845), "Set as wallpaper", font=f(26), fill=(10, 10, 10), anchor="mm")
            if 7.2 <= t < 8.3:
                d.ellipse([W // 2 - 26, 819, W // 2 + 26, 871], outline=(255, 255, 255), width=4)
            if t >= 8.3:
                d.rounded_rectangle([80, 640, W - 80, 710], 20, fill=(30, 34, 46))
                d.text((W // 2, 675), "Saved as wallpaper", font=f(24), fill=(255, 255, 255), anchor="mm")
            d.text((W // 2, 930), "EXAMPLE ONLY: made-up app", font=f(16), fill=(110, 115, 130), anchor="mm")
            fr.save(os.path.join(tmp, f"f{i:04d}.png"))
        os.makedirs(os.path.join(HERE, "takes"), exist_ok=True)
        ff("-framerate", str(FPS), "-i", os.path.join(tmp, "f%04d.png"), *enc, "-r", "30", "-movflags", "+faststart",
           "-map_metadata", "-1", os.path.join(HERE, "takes", "screen.mp4"))
    print("wrote orbit-footage.mp4 and takes/screen.mp4")


if __name__ == "__main__":
    main()
