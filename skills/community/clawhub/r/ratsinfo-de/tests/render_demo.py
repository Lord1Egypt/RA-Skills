#!/usr/bin/env python3
"""Render a real terminal session into an MP4.

Reads a session transcript produced by capturing actual command output,
draws it as a terminal with a typewriter effect, and hands the frames to
ffmpeg. Nothing here is staged: the text on screen is the text the
commands printed.

    python3 tests/capture_demo.py        # records the session
    python3 tests/render_demo.py         # renders demo.mp4
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 900
FPS = 30
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_SIZE = 22
LINE_H = 30
PAD_X, PAD_Y = 40, 78

BG = (13, 17, 23)
BAR = (22, 27, 34)
BAR_TEXT = (139, 148, 158)
PROMPT = (86, 211, 100)
CMD = (230, 237, 243)
OUT = (173, 186, 199)
ERR = (255, 166, 87)
OK = (86, 211, 100)
DIM = (110, 118, 129)

PROMPT_TEXT = "alpha-quadrat ~/ratsinfo-de $ "
TITLE = "ratsinfo-de   OParl client for German council information systems"

CHAR_FRAMES = 1      # frames per typed character
LINE_FRAMES = 3      # frames per printed output line
PAUSE_AFTER_CMD = 12
HOLD_END = 60

CAPTIONS = {
    "en": [
        "1. health check first. the public registry is full of dead endpoints",
        "2. search the council papers, filtered on the client side",
        "3. what became of it. the paper's route through the committees",
        "4. watch asks only for what changed since the last run",
        "5. an endpoint that exists and is switched off",
        "6. robots.txt disallows the API path",
        "7. a file:// url from a server response is refused, not followed",
        "8. and across a whole region at once, not one town",
        "9. the document that comes out at the end",
        "10. the offline test suite. no network, no municipality touched",
    ],
    "de": [
        "1. zuerst der Gesundheitscheck. Das Verzeichnis ist voller toter Endpunkte",
        "2. die Vorlagen durchsuchen, clientseitig gefiltert",
        "3. was daraus geworden ist. Der Weg der Vorlage durch die Ausschuesse",
        "4. watch fragt nur nach dem, was sich seit dem letzten Lauf geaendert hat",
        "5. ein Endpunkt, den es gibt und der abgeschaltet ist",
        "6. die robots-Datei sperrt den Schnittstellenpfad",
        "7. eine file-Adresse aus einer Serverantwort wird abgelehnt",
        "8. und ueber eine ganze Region hinweg, nicht eine Kommune",
        "9. das Dokument, das am Ende herauskommt",
        "10. die Testsuite ohne Netz. Keine Kommune wird angefasst",
    ],
}
INTRO = {
    "en": "real output, recorded, not reconstructed",
    "de": "echte Ausgabe, aufgezeichnet, nicht nachgebaut",
}
OUTRO = {
    "en": "MIT-0   no dependencies   python standard library only",
    "de": "MIT-0   ohne Abhaengigkeiten   nur die Python-Standardbibliothek",
}

MAX_ROWS = (H - PAD_Y - 30) // LINE_H
MAX_COLS = 112


def wrap(line: str) -> list[str]:
    """Wrap like a terminal would, with a hanging indent so it stays readable."""
    if len(line) <= MAX_COLS:
        return [line]
    indent = " " * (len(line) - len(line.lstrip()) + 2)
    out, current = [], line
    width = MAX_COLS
    while len(current) > width:
        cut = current.rfind(" ", 0, width)
        if cut <= len(indent):
            cut = width
        out.append(current[:cut].rstrip())
        current = indent + current[cut:].lstrip()
        width = MAX_COLS
    out.append(current)
    return out


def colour_for(line: str) -> tuple:
    stripped = line.lstrip()
    if stripped.startswith("ok "):
        return OK
    if stripped.startswith("error:") or "passed," in line and "0 failed" not in line:
        return ERR
    if stripped.startswith("$"):
        return PROMPT
    return OUT


def draw(rows: list[tuple[str, tuple]], caption: str) -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    font = draw.font
    d.rectangle([0, 0, W, 52], fill=BAR)
    for i, colour in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([22 + i * 26, 19, 36 + i * 26, 33], fill=colour)
    d.text((120, 17), TITLE, font=font, fill=BAR_TEXT)

    visible = rows[-MAX_ROWS:]
    y = PAD_Y
    for text, colour in visible:
        d.text((PAD_X, y), text, font=font, fill=colour)
        y += LINE_H

    if caption:
        d.text((PAD_X, H - 34), caption, font=font, fill=DIM)
    d.text((W - 300, 17), "alpha-quadrat.de", font=font, fill=DIM)
    return img


def main() -> int:
    if not shutil.which("ffmpeg"):
        print("ffmpeg not found", file=sys.stderr)
        return 1
    lang = sys.argv[1] if len(sys.argv) > 1 else "en"
    target = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
    out_name = sys.argv[3] if len(sys.argv) > 3 else f"demo-{lang}.mp4"
    session = json.load(open("/tmp/session.json", encoding="utf-8"))
    draw.font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    tmp = tempfile.mkdtemp(prefix="ratsinfo-demo-")
    rows = []
    frame = 0
    shots = 0
    timeline = []

    def emit(caption: str = "", times: int = 1) -> None:
        """Write one picture and note how long it stays up.

        Saving the same frame thirty times is what made this slow. ffmpeg
        takes a concat list with durations instead.
        """
        nonlocal frame, shots
        path = os.path.join(tmp, f"{shots:05d}.png")
        draw(rows, caption).save(path)
        shots += 1
        frame += times
        timeline.append((path, times / FPS))

    captions = CAPTIONS[lang]

    # Distribute whatever time is left as pauses between blocks, so the
    # picture lands exactly on the narration.
    typed_chars = sum(len(b["cmd"].replace("python3 scripts/", "")) for b in session)
    output_lines = sum(len(b["out"].splitlines()) for b in session)
    fixed = (
        FPS * 2
        + typed_chars * CHAR_FRAMES
        + output_lines * LINE_FRAMES
        + len(session) * PAUSE_AFTER_CMD
        + HOLD_END
    )
    wanted = int(target * FPS) if target else fixed + len(session) * 26
    pause_after_block = max(10, (wanted - fixed) // max(1, len(session)))

    emit(INTRO[lang], FPS * 2)

    for block, caption in zip(session, captions):
        rows.append(("", OUT))
        typed = ""
        for char in block["cmd"].replace("python3 scripts/", ""):
            typed += char
            rows[-1] = (PROMPT_TEXT + typed, CMD)
            emit(caption, CHAR_FRAMES)
        emit(caption, PAUSE_AFTER_CMD)

        for line in block["out"].splitlines():
            colour = colour_for(line)
            for piece in wrap(line):
                rows.append((piece, colour))
            emit(caption, LINE_FRAMES)
        emit(caption, pause_after_block)

    # the payoff: show the PDF that the last command produced
    shot = os.environ.get("RATSINFO_PDF_PNG")
    if shot and os.path.exists(shot):
        page = Image.open(shot).convert("RGB")
        scale = (H - 120) / page.height
        page = page.resize(
            (int(page.width * scale), int(page.height * scale)), Image.LANCZOS
        )
        canvas = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(canvas)
        d.rectangle([0, 0, W, 52], fill=BAR)
        d.text((120, 17), TITLE, font=draw.font, fill=BAR_TEXT)
        d.text((W - 300, 17), "alpha-quadrat.de", font=draw.font, fill=DIM)
        canvas.paste(page, ((W - page.width) // 2, 70))
        d.text((PAD_X, H - 34), OUTRO[lang], font=draw.font, fill=DIM)
        path = os.path.join(tmp, f"{shots:05d}.png")
        canvas.save(path)
        shots += 1
        timeline.append((path, 6.0))
        frame += int(6.0 * FPS)
    else:
        emit(OUTRO[lang], HOLD_END)

    out = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), out_name
    )
    concat = os.path.join(tmp, "list.txt")
    with open(concat, "w", encoding="utf-8") as handle:
        for path, seconds in timeline:
            handle.write(f"file '{path}'\nduration {seconds:.4f}\n")
        handle.write(f"file '{timeline[-1][0]}'\n")  # concat needs a last frame

    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-f", "concat", "-safe", "0", "-i", concat,
            "-fps_mode", "cfr", "-r", str(FPS),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
            "-movflags", "+faststart",
            out,
        ],
        check=True,
    )
    shutil.rmtree(tmp)
    print(f"{out}  {frame} frames  {frame / FPS:.1f} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
