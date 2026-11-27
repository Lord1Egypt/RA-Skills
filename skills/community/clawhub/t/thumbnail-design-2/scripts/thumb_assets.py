#!/usr/bin/env python3
"""Asset helpers for thumbnails (Pillow required; no other dependency).

Commands
  search      "query" --out DIR [--source auto|pexels|pixabay] [--count 6]  free stock photos + attribution.json
  cutout      IMAGE [--out PNG] [--engine rembg|removebg]                   transparent PNG of the subject
  ai-image    "prompt" --out PNG [--model NAME] [--size 1536x1024]          OpenAI Image API (paid, optional)
  prompt      --subject ".." [--emotion ..] [--setting ..] [--style ..]    build a prompt for any image generator
  upscale     IMAGE --factor 2 [--out PATH]                                 Lanczos + gentle sharpen (not AI upscaling)
  competitors IDS_OR_FILES... --out DIR                                     download/analyse other thumbnails FOR STUDY

Keys (environment variables only; never printed): PEXELS_API_KEY, PIXABAY_API_KEY, REMOVEBG_API_KEY, OPENAI_API_KEY.
For ai-image the model name comes from --model or THUMB_IMAGE_MODEL: model names change, check the provider's docs.
"""
import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

try:
    from PIL import Image, ImageFilter
except ImportError:
    sys.exit("Pillow is required: pip install pillow")

sys.path.insert(0, str(Path(__file__).resolve().parent))
UA = "thumbnail-design-skill/1.0"


class Fail(RuntimeError):
    pass


def http(url, headers=None, data=None, timeout=60, method=None):
    host = urllib.parse.urlsplit(url).netloc
    req = urllib.request.Request(url, data=data, headers={"User-Agent": UA, **(headers or {})}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8", "replace")[:300]
        except OSError:
            pass
        if e.code == 429:
            raise Fail(f"{host}: HTTP 429, rate limit reached; wait and retry.") from None
        if e.code in (401, 403):
            raise Fail(f"{host}: HTTP {e.code}, access refused. Check the API key and plan. {body}") from None
        raise Fail(f"{host}: HTTP {e.code}. {body}") from None
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        raise Fail(f"Cannot reach {host} ({getattr(e, 'reason', e)}). Outbound access may be blocked here; "
                   "run this on your own machine.") from None


def need_key(name):
    v = os.environ.get(name, "").strip()
    if not v:
        raise Fail(f"Set {name} in your environment.")
    return v


# ---- search -----------------------------------------------------------------
def cmd_search(a):
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    items = []
    if a.source == "auto":  # use whichever free key exists (Pexels paused new keys at times)
        a.source = "pexels" if os.environ.get("PEXELS_API_KEY", "").strip() else "pixabay"
    if a.source == "pexels":
        url = "https://api.pexels.com/v1/search?" + urllib.parse.urlencode(
            {"query": a.query, "orientation": "landscape", "per_page": a.count})
        data = json.loads(http(url, {"Authorization": need_key("PEXELS_API_KEY")}))
        for p in data.get("photos", []):
            src = p.get("src") or {}
            link = src.get("large2x") or src.get("original")
            if link:
                items.append({"id": p["id"], "url": link, "page": p.get("url", ""), "creator": p.get("photographer", ""),
                              "license": "Pexels License", "source": "Pexels"})
    else:
        url = "https://pixabay.com/api/?" + urllib.parse.urlencode(
            {"key": need_key("PIXABAY_API_KEY"), "q": a.query[:100], "image_type": "photo", "orientation": "horizontal",
             "per_page": max(3, a.count), "safesearch": "true"})
        data = json.loads(http(url))
        for p in data.get("hits", [])[:a.count]:
            if p.get("largeImageURL"):
                items.append({"id": p["id"], "url": p["largeImageURL"], "page": p.get("pageURL", ""),
                              "creator": p.get("user", ""), "license": "Pixabay Content License", "source": "Pixabay"})
    if not items:
        print("No results; try simpler, more concrete words.")
        return
    att = out / "attribution.json"
    log = json.loads(att.read_text(encoding="utf-8")) if att.exists() else []
    saved, failed = 0, []
    for it in items:
        dest = out / f"{a.source}_{it['id']}.jpg"
        if not dest.exists():
            try:
                data = http(it["url"], timeout=120)
            except Fail as e:  # keep going: one slow file must not lose the others or their credits
                failed.append(f"{it['id']}: {e}")
                continue
            tmp = dest.with_name(dest.name + ".part")
            tmp.write_bytes(data)
            tmp.replace(dest)
        it["file"] = dest.name
        if not any(x.get("file") == dest.name for x in log):
            log.append({k: it[k] for k in ("file", "source", "creator", "page", "license")})
            att.write_text(json.dumps(log, indent=2), encoding="utf-8")  # credit written with each file
        saved += 1
        try:
            w, h = Image.open(dest).size
        except OSError:
            w = h = 0
        print(f"{dest.name}  {w}x{h}  by {it['creator']}  {it['page']}")
    att.write_text(json.dumps(log, indent=2), encoding="utf-8")
    for f in failed:
        print(f"  ! not downloaded: {f}", file=sys.stderr)
    print(f"Saved {saved} of {len(items)} image(s) and attribution.json to {out}."
          + (" Pixabay photos top out near 1280 px wide." if a.source == "pixabay" else ""))
    if failed and not saved:
        raise Fail("No image could be downloaded.")


# ---- cutout -----------------------------------------------------------------
def multipart(fields, files):
    b = uuid.uuid4().hex
    body = b""
    for k, v in fields.items():
        body += f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
    for k, (name, content) in files.items():
        body += (f'--{b}\r\nContent-Disposition: form-data; name="{k}"; filename="{name}"\r\n'
                 f"Content-Type: application/octet-stream\r\n\r\n").encode() + content + b"\r\n"
    return body + f"--{b}--\r\n".encode(), f"multipart/form-data; boundary={b}"


def cmd_cutout(a):
    src = Path(a.image)
    if not src.exists():
        raise Fail(f"{src} not found.")
    out = Path(a.out) if a.out else src.with_name(src.stem + "_cutout.png")
    engine = a.engine
    if engine == "auto":
        try:
            import rembg  # noqa: F401
            engine = "rembg"
        except ImportError:
            engine = "removebg" if os.environ.get("REMOVEBG_API_KEY") else ""
    if engine == "rembg":
        try:
            from rembg import remove
        except ImportError:
            raise Fail("rembg is not installed: pip install \"rembg[cpu]\" (free, runs locally; downloads a model on first use).") from None
        out.write_bytes(remove(src.read_bytes()))
    elif engine == "removebg":
        key = need_key("REMOVEBG_API_KEY")
        body, ctype = multipart({"size": "auto", "format": "png"}, {"image_file": (src.name, src.read_bytes())})
        out.write_bytes(http("https://api.remove.bg/v1.0/removebg", {"X-Api-Key": key, "Content-Type": ctype}, data=body,
                             timeout=120, method="POST"))
        print("Note: remove.bg announced that its standalone website closes on 1 Dec 2026 and background removal moves to "
              "Canva and Leonardo.ai; check remove.bg's notice for what that means for the API.")
    else:
        raise Fail("No cutout engine. Install rembg (pip install \"rembg[cpu]\"), set REMOVEBG_API_KEY, or cut the "
                   "subject out by hand in Photopea/GIMP and save a PNG with transparency.")
    im = Image.open(out).convert("RGBA")
    lo, hi = im.getchannel("A").getextrema()
    print(f"Wrote {out}. Zoom in on hair and edges, and fix any rough spots by hand if needed."
          + ("" if lo < 255 else " WARNING: the result has no transparent pixels."))


# ---- AI image ---------------------------------------------------------------
def cmd_ai_image(a):
    key = need_key("OPENAI_API_KEY")
    model = a.model or os.environ.get("THUMB_IMAGE_MODEL", "")
    if not model:
        raise Fail("Give --model or set THUMB_IMAGE_MODEL (model names change; see the provider's image-generation guide).")
    body = json.dumps({"model": model, "prompt": a.prompt, "size": a.size, "n": 1}).encode()
    raw = http("https://api.openai.com/v1/images/generations",
               {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}, data=body, timeout=300,
               method="POST")
    try:
        b64 = json.loads(raw)["data"][0]["b64_json"]
    except (ValueError, KeyError, IndexError):
        raise Fail("Unexpected response from the image API (no b64_json). Check the model name and the account's access; "
                   "some image models require organization verification.") from None
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(base64.b64decode(b64))
    w, h = Image.open(out).size
    print(f"Wrote {out} ({w}x{h}). Each call is billed; AI-drawn text is often wrong, so add text with thumb_compose.py.")


def cmd_prompt(a):
    parts = [f"Subject: {a.subject}."]
    if a.emotion:
        parts.append(f"Emotion/expression: {a.emotion}.")
    parts.append(f"Setting: {a.setting or 'simple, uncluttered background that supports the subject'}.")
    parts.append(f"Style: {a.style or 'high-contrast, sharp, saturated, cinematic photo'}.")
    parts.append(f"Lighting: {a.lighting or 'strong rim light, clear separation between subject and background'}.")
    if a.palette:
        parts.append(f"Colour palette: {a.palette}.")
    parts.append(f"Composition: {a.composition or 'subject on the right third, left third left empty for headline text, one clear focal point'}.")
    parts.append("16:9 landscape. No text, no letters, no logos, no watermark, no UI elements.")
    print(" ".join(parts))
    print("\nNegative/avoid (for tools with a negative-prompt field): text, watermark, logo, extra fingers, distorted face, clutter, low resolution.")


# ---- upscale ----------------------------------------------------------------
def cmd_upscale(a):
    src = Path(a.image)
    im = Image.open(src)
    f = max(1.0, min(a.factor, 4.0))
    out = Path(a.out) if a.out else src.with_name(f"{src.stem}_x{f:g}{src.suffix}")
    big = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB").resize(
        (round(im.width * f), round(im.height * f)), Image.LANCZOS)
    big = big.filter(ImageFilter.UnsharpMask(radius=1.6, percent=60, threshold=3))
    big.save(out)
    print(f"Wrote {out} ({big.width}x{big.height}). This is classic resampling; it adds size, not real detail. "
          "For heavy upscaling use a dedicated AI upscaler (Magnific, Real-ESRGAN) if licensed for your use.")


# ---- competitors ------------------------------------------------------------
def video_id(s):
    s = s.strip()
    if "youtu" in s:
        u = urllib.parse.urlsplit(s)
        if u.netloc.endswith("youtu.be"):
            return u.path.strip("/")
        return urllib.parse.parse_qs(u.query).get("v", [""])[0]
    return s


def pix(im):
    return list(im.get_flattened_data() if hasattr(im, "get_flattened_data") else im.getdata())


def analyse(path):
    im = Image.open(path).convert("RGB")
    small = im.resize((160, round(160 * im.height / im.width)))
    q = small.quantize(5, method=Image.MEDIANCUT).convert("RGB")
    colors = sorted(q.getcolors(), reverse=True)
    pal = ["#%02X%02X%02X" % c for _, c in colors[:4]]
    px = pix(small.convert("L"))
    mean = sum(px) / len(px)
    edges = small.convert("L").filter(ImageFilter.FIND_EDGES)
    w = edges.width
    left = sum(pix(edges.crop((0, 0, w // 2, edges.height))))
    right = sum(pix(edges.crop((w // 2, 0, w, edges.height))))
    r, g, b = [sum(pix(c)) / len(px) for c in small.split()]
    tone = "warm" if r > b + 12 else "cool" if b > r + 12 else "neutral"
    return {"palette": pal, "brightness": round(mean), "tone": tone,
            "detail_side": "left" if left > right * 1.15 else "right" if right > left * 1.15 else "balanced"}


def cmd_competitors(a):
    from thumb_compose import sheet
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    files, rows = [], []
    for item in a.items:
        p = Path(item)
        if p.exists():
            files.append(p)
            continue
        vid = video_id(item)
        if not vid:
            print(f"Skipping {item!r}: not a video id, URL or file.", file=sys.stderr)
            continue
        dest = out / f"{vid}.jpg"
        if not dest.exists():
            for name in ("maxresdefault", "hqdefault"):
                try:
                    dest.write_bytes(http(f"https://i.ytimg.com/vi/{vid}/{name}.jpg"))
                    break
                except Fail as e:
                    err = e
            else:
                print(f"! {vid}: {err}", file=sys.stderr)
                continue
        files.append(dest)
    if not files:
        raise Fail("No thumbnails to analyse.")
    for f in files:
        info = analyse(f)
        info["file"] = str(f)
        rows.append(info)
        print(f"{f.name}: brightness {info['brightness']}, {info['tone']}, detail {info['detail_side']}, palette {' '.join(info['palette'])}")
    sheet([str(f) for f in files], out / "competitor_sheet.jpg")
    tones = {t: sum(1 for r in rows if r["tone"] == t) for t in ("warm", "cool", "neutral")}
    avg = sum(r["brightness"] for r in rows) / len(rows)
    print(f"\n{len(rows)} thumbnails: tones {tones}, average brightness {avg:.0f}/255. Sheet: {out / 'competitor_sheet.jpg'}")
    print("For study only: note patterns (colours, face size, text length, layout) and choose a different, own direction. "
          "Do not copy, trace or lightly edit another creator's thumbnail.")
    (out / "analysis.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search")
    s.add_argument("query")
    s.add_argument("--out", required=True)
    s.add_argument("--source", choices=["auto", "pexels", "pixabay"], default="auto",
                   help="auto: Pexels if PEXELS_API_KEY is set, else Pixabay")
    s.add_argument("--count", type=int, default=6)
    s.set_defaults(fn=cmd_search)
    c = sub.add_parser("cutout")
    c.add_argument("image")
    c.add_argument("--out")
    c.add_argument("--engine", choices=["auto", "rembg", "removebg"], default="auto")
    c.set_defaults(fn=cmd_cutout)
    g = sub.add_parser("ai-image")
    g.add_argument("prompt")
    g.add_argument("--out", required=True)
    g.add_argument("--model")
    g.add_argument("--size", default="1536x1024")
    g.set_defaults(fn=cmd_ai_image)
    r = sub.add_parser("prompt")
    for k in ("subject", "emotion", "setting", "style", "lighting", "palette", "composition"):
        r.add_argument(f"--{k}", required=(k == "subject"))
    r.set_defaults(fn=cmd_prompt)
    u = sub.add_parser("upscale")
    u.add_argument("image")
    u.add_argument("--factor", type=float, default=2.0)
    u.add_argument("--out")
    u.set_defaults(fn=cmd_upscale)
    k = sub.add_parser("competitors")
    k.add_argument("items", nargs="+")
    k.add_argument("--out", required=True)
    k.set_defaults(fn=cmd_competitors)
    a = p.parse_args(argv)
    try:
        a.fn(a)
        return 0
    except Fail as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    except (OSError, ValueError) as e:
        print(f"error: {type(e).__name__}: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
