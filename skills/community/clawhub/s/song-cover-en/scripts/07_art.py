"""Generate the song-art images with local ComfyUI (Z-Image-Turbo).

Each prompt is tied to an image cluster in the lyrics, so the lyric video can cut
to a picture that matches what is being sung. Wide 16:9 because these become the
background plate of the video.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from _env import LIBS, RUNS

sys.path.insert(0, str(LIBS))


from comfy_client import generate  # noqa: E402

# key, prompt  -- one picture per lyrical movement
SCENES = [
    ("title", "cinematic wide shot, lone figure on a vast misty plain under a "
              "pale moon, ancient Chinese wuxia mood, indigo and slate blue, fog, "
              "negative space for text, painterly, no text"),
    ("blade", "extreme close-up of a polished ancient Chinese jian sword blade "
              "catching cold blue light, rain droplets on steel, dark background, "
              "cinematic rim light, shallow depth of field, no text"),
    ("bloom", "Chinese plum blossoms opening in falling snow, soft pink petals "
              "against jade green haze, shallow depth of field, ink-wash painting "
              "atmosphere, cinematic, no text"),
    ("lantern", "rows of blood-red paper lanterns glowing in a narrow ancient "
                "Chinese street at night, warm red light on wet stone, rain, "
                "cinematic, deep shadows, no text"),
    ("gate", "moonlit stone gate of an ancient Chinese estate, a small boy "
             "silhouetted in the doorway, drifting snow, cyan moonlight, "
             "cinematic wide shot, no text"),
    ("stars", "the Milky Way turning over a Chinese mountain ridge, a lone "
              "figure looking up, deep blue and silver, long exposure look, "
              "cinematic, no text"),
    ("isle", "a lonely snow-covered island in a grey frozen sea, swirling snow "
             "and rain, distant waves, desaturated, cinematic wide shot, no text"),
    ("valley", "a deep mossy valley with ancient stone coffins half-buried, "
               "shafts of pale light, mist, dark green and grey, cinematic, no text"),
    ("jianghu", "abstract ink-wash mountains dissolving into blood-red mist, "
                "calligraphic energy, dark, cinematic, plenty of negative space, no text"),
]

# 1152x648 is the largest 16:9 size this VAE decodes cleanly (1344x768 faults)
W, H = 1152, 648


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(RUNS / "sudi" / "07" / "art"))
    ap.add_argument("--only", default=None, help="comma separated scene keys")
    ap.add_argument("--steps", type=int, default=8)
    ap.add_argument("--seed", type=int, default=20261107)
    a = ap.parse_args()

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    want = set(a.only.split(",")) if a.only else None

    made = {}
    for i, (key, prompt) in enumerate(SCENES):
        if want and key not in want:
            continue
        dst = out / f"{i:02d}_{key}.png"
        if dst.exists():
            print(f"skip {key} (exists)", flush=True)
            made[key] = str(dst)
            continue
        t = time.time()
        got = generate(prompt, negative="text, watermark, signature, letters, "
                                         "low quality, blurry, deformed",
                       width=W, height=H, steps=a.steps, seed=a.seed + i * 7919,
                       out_dir=str(out))
        # generate() returns (paths, meta); an empty path list means the server
        # reported an execution error even though the HTTP call succeeded
        paths = got[0] if isinstance(got, tuple) else got
        if not paths:
            print(f"!! {key}: generation failed, skipping", flush=True)
            continue
        src = Path(paths[0])
        if src.exists() and src.resolve() != dst.resolve():
            src.replace(dst)
        made[key] = str(dst)
        print(f"made {key} in {time.time()-t:.1f}s -> {dst.name}", flush=True)

    (out / "art.json").write_text(json.dumps(made, ensure_ascii=False, indent=2),
                                  encoding="utf-8")
    print(f"wrote {out/'art.json'} ({len(made)} images)", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
