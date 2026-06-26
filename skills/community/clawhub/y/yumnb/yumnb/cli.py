"""
yumnb — Yum NoteBook main CLI.

Subcommands:
  ingest <INPUT>           ingest URL / YouTube / image / text into a note folder
  summarize <FOLDER>       AI summary → summary.md (requires ai.provider != none)
  talkshow <FOLDER>        AI talk-show script → talkshow.txt (requires ai)
  deckplan <FOLDER>        AI deck plan → deck.json (requires ai)
  tts <SCRIPT> --output X  Render dual-voice MP3 from a [Speaker]-tagged script
  ppt <JSON> --output X    Render PPTX from a slide-plan JSON
  publish <FOLDER>         Write links.json, optionally notify webhook
  auto <INPUT>             Run end-to-end (ingest → summarize → talkshow → tts → deckplan → ppt → publish)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict
from urllib.parse import urlparse

from yumnb.make_ppt import build as build_pptx
from yumnb.tts import build_dual_audio
from yumnb import notify
from yumnb import deliver
from yumnb import ai_provider
from yumnb.ai_provider import AIError
from yumnb import upload as upload_mod


# ── Config loading ────────────────────────────────────────────────────────

_DEFAULT_LANGUAGE_VOICES = {
    "en": {
        "HostA": {"voice": "en-US-AndrewNeural", "rate": "+0%"},
        "HostB": {"voice": "en-US-AvaNeural",    "rate": "+0%"},
    },
    "zh": {
        "云飞": {"voice": "zh-CN-YunyangNeural",  "rate": "+10%"},
        "小晓": {"voice": "zh-CN-XiaoxiaoNeural", "rate": "+10%"},
    },
    "ja": {
        "HostA": {"voice": "ja-JP-KeitaNeural",  "rate": "+0%"},
        "HostB": {"voice": "ja-JP-NanamiNeural", "rate": "+0%"},
    },
    "es": {
        "HostA": {"voice": "es-ES-AlvaroNeural", "rate": "+0%"},
        "HostB": {"voice": "es-ES-ElviraNeural", "rate": "+0%"},
    },
    "fr": {
        "HostA": {"voice": "fr-FR-HenriNeural",   "rate": "+0%"},
        "HostB": {"voice": "fr-FR-DeniseNeural",  "rate": "+0%"},
    },
    "de": {
        "HostA": {"voice": "de-DE-ConradNeural",  "rate": "+0%"},
        "HostB": {"voice": "de-DE-KatjaNeural",   "rate": "+0%"},
    },
}

_LANGUAGE_NAMES = {
    "en": "English", "zh": "Simplified Chinese (简体中文)", "ja": "Japanese (日本語)",
    "es": "Spanish (Español)", "fr": "French (Français)", "de": "German (Deutsch)",
    "ko": "Korean (한국어)", "pt": "Portuguese", "it": "Italian", "ru": "Russian",
}

_DEFAULT_CFG = {
    "output_dir": "./notes",
    "language": "en",
    "ai": {"provider": "none"},
    "tts": {
        "enabled": True,
        "voices": {},
        "language_voices": _DEFAULT_LANGUAGE_VOICES,
        "jingle": True,
        "custom_jingle_mp3": "",
    },
    "upload": {
        "provider": "none",
        "rclone": {
            "remote": "",
            "rclone_bin": "rclone",
            "share": True,
            "per_note_subfolder": True,
            "extra_args": [],
        },
        "files": ["talkshow.mp3", "deck.pptx", "summary.md"],
    },
    "notify": {"webhook_url": None, "style": "generic"},
    "deliver": {
        "provider": "none",
        "openclaw": {
            "binary": "openclaw",
            "channel": "",
            "target": "",
            "account": "",
            "reply_to": "",
            "thread_id": "",
            "silent": False,
            "force_document": False,
            "captions": True,
            "send_text": True,
            "send_files": True,
            "dry_run": False,
            "timeout_seconds": 120,
        },
        "files": ["talkshow.mp3", "deck.pptx"],
    },
}

_HERE = Path(__file__).resolve().parent


def _resolve_language(cfg: dict, override: str = "") -> str:
    lang = (override or os.environ.get("YUMNB_LANGUAGE") or cfg.get("language") or "en")
    return str(lang).strip().lower() or "en"


def _resolve_voices(cfg: dict, language: str) -> dict:
    tts = cfg.get("tts") or {}
    if tts.get("voices"):
        return tts["voices"]
    lv = tts.get("language_voices") or {}
    if language in lv and lv[language]:
        return lv[language]
    if "en" in lv and lv["en"]:
        return lv["en"]
    return _DEFAULT_LANGUAGE_VOICES["en"]


def _deep_merge(base: dict, overlay: dict) -> dict:
    out = dict(base)
    for k, v in (overlay or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load_config(explicit_path: str = "") -> Dict[str, Any]:
    candidates = []
    if explicit_path:
        candidates.append(Path(explicit_path))
    if os.environ.get("YUMNB_CONFIG"):
        candidates.append(Path(os.environ["YUMNB_CONFIG"]))
    candidates += [
        Path.cwd() / "config.local.yaml",
        Path.cwd() / "config.yaml",
        _HERE.parent / "config.yaml",
    ]

    raw: Dict[str, Any] = {}
    for p in candidates:
        if p.is_file():
            try:
                import yaml  # type: ignore
            except ImportError:
                print(f"WARN: PyYAML not installed, ignoring {p}", file=sys.stderr)
                break
            raw = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
            print(f"yumnb: loaded config from {p}")
            break

    cfg = _deep_merge(_DEFAULT_CFG, raw)
    if os.environ.get("YUMNB_OUTPUT_DIR"):
        cfg["output_dir"] = os.environ["YUMNB_OUTPUT_DIR"]
    return cfg


def slugify(s: str, maxlen: int = 30) -> str:
    s = re.sub(r"[\\/:*?\"<>|\r\n\t]+", "", s or "").strip()
    s = re.sub(r"\s+", "-", s)
    return (s[:maxlen] or "note").strip("-")


def detect_kind(inp: str) -> str:
    low = inp.lower()
    if "youtube.com" in low or "youtu.be" in low:
        return "youtube"
    if low.startswith(("http://", "https://")):
        return "url"
    if os.path.isfile(inp):
        ext = os.path.splitext(inp)[1].lower()
        if ext in (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".avif"):
            return "image"
        return "file"
    return "text"


def make_folder(output_dir: Path, kind: str, title_hint: str) -> Path:
    date = datetime.now().strftime("%Y%m%d-%H%M")
    slug = slugify(title_hint or kind)
    folder = output_dir / f"{date}-{slug}"
    (folder / "source").mkdir(parents=True, exist_ok=True)
    return folder


def _parse_vtt(vtt_text: str) -> str:
    out, last = [], ""
    for raw in vtt_text.splitlines():
        ln = raw.strip()
        if not ln or ln.startswith(("WEBVTT", "Kind:", "Language:", "NOTE")) or "-->" in ln:
            continue
        ln = re.sub(r"<[^>]+>", "", ln).strip()
        if not ln or ln == last:
            continue
        out.append(ln)
        last = ln
    return "\n".join(out)


def _youtube_transcript_api_fallback(video_id: str, lang_order: list[str]) -> tuple[str, str, str]:
    try:
        from youtube_transcript_api import YouTubeTranscriptApi  # type: ignore
    except ImportError:
        return "", "", ""

    candidates = []
    for lang in lang_order:
        if lang not in candidates:
            candidates.append(lang)
        if "-" in lang:
            base = lang.split("-", 1)[0]
            if base not in candidates:
                candidates.append(base)
    if "en" not in candidates:
        candidates.append("en")

    try:
        fetched = YouTubeTranscriptApi().fetch(video_id, languages=candidates)
        text = "\n".join(
            (getattr(snippet, "text", "") or "").strip()
            for snippet in fetched
            if (getattr(snippet, "text", "") or "").strip()
        ).strip()
        if text:
            lang = getattr(fetched, "language_code", "") or getattr(fetched, "language", "") or ""
            return text, "youtube-transcript-api", lang
    except Exception as e:
        print(f"[subs:youtube-transcript-api] error: {e}")
    return "", "", ""


def ingest_youtube(url: str, src_dir: Path) -> dict:
    try:
        import yt_dlp  # type: ignore
    except ImportError as e:
        raise SystemExit(f"yt-dlp not installed: {e}")

    info_path = src_dir / "youtube_info.json"
    opts_meta = {
        "skip_download": True, "quiet": True, "no_warnings": True,
        "writethumbnail": True, "writeinfojson": False,
        "outtmpl": str(src_dir / "thumb.%(ext)s"),
    }
    with yt_dlp.YoutubeDL(opts_meta) as ydl:
        info = ydl.extract_info(url, download=True)

    meta = {k: info.get(k) for k in ("title", "uploader", "duration", "description", "view_count", "upload_date", "webpage_url", "id")}
    info_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    sub_base = src_dir / "sub"
    transcript_text, sub_source, sub_lang = "", "", ""
    lang_order = ["zh-Hans", "zh-CN", "zh", "en", "en-US"]
    for attempt in ("manual", "auto"):
        for lang in lang_order:
            opts_sub = {
                "skip_download": True, "quiet": True, "no_warnings": True,
                "writesubtitles": attempt == "manual",
                "writeautomaticsub": attempt == "auto",
                "subtitleslangs": [lang], "subtitlesformat": "vtt",
                "outtmpl": str(sub_base) + ".%(ext)s",
                "ignoreerrors": True,
            }
            try:
                with yt_dlp.YoutubeDL(opts_sub) as ydl:
                    ydl.extract_info(url, download=True)
            except Exception as e:
                print(f"[subs:{attempt}:{lang}] yt-dlp error: {e}")
                continue
            vtts = list(src_dir.glob(f"sub.{lang}.vtt"))
            if not vtts:
                continue
            try:
                txt = _parse_vtt(vtts[0].read_text(encoding="utf-8", errors="replace"))
                if txt.strip():
                    transcript_text, sub_source, sub_lang = txt, attempt, lang
                    break
            except Exception as e:
                print(f"[subs:{attempt}:{lang}] parse error: {e}")
        if transcript_text:
            break

    if not transcript_text.strip() and meta.get("id"):
        transcript_text, sub_source, sub_lang = _youtube_transcript_api_fallback(meta["id"], lang_order)

    if not transcript_text.strip():
        transcript_text = f"[no subtitles available — manual, auto, and transcript API all empty]\n\nDescription:\n{meta.get('description', '')}"
        sub_source = "none"

    (src_dir / "transcript.txt").write_text(transcript_text, encoding="utf-8")
    meta["transcript_source"] = sub_source
    meta["transcript_lang"] = sub_lang
    info_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    (src_dir / "raw.txt").write_text(
        f"# {meta.get('title')}\n\n"
        f"Uploader: {meta.get('uploader')}\nDuration: {meta.get('duration')}s\n"
        f"URL: {meta.get('webpage_url')}\n"
        f"Transcript source: {sub_source} ({sub_lang})\n\n"
        f"## Transcript\n\n{transcript_text}\n\n"
        f"## Description\n\n{meta.get('description', '')}",
        encoding="utf-8",
    )
    return {"kind": "youtube", "title": meta.get("title") or "youtube", "meta": meta}


def ingest_url(url: str, src_dir: Path, fetcher: str = "") -> dict:
    import requests
    html, title = "", ""
    try:
        r = requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
        if r.status_code == 200:
            html = r.text
    except Exception as e:
        html = f"<!-- fetch failed: {e} -->"

    if (not html or "<title>" not in html.lower()) and fetcher:
        try:
            out = subprocess.run(fetcher.split() + [url], capture_output=True, text=True, encoding="utf-8", timeout=60)
            if out.returncode == 0 and out.stdout:
                html = out.stdout
        except Exception as e:
            print(f"fetcher fallback failed: {e}")

    (src_dir / "page.html").write_text(html, encoding="utf-8", errors="replace")

    text = ""
    try:
        from bs4 import BeautifulSoup  # type: ignore
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "noscript", "svg"]):
            tag.decompose()
        title = (soup.title.string.strip() if soup.title and soup.title.string else "")
        text = re.sub(r"\n{3,}", "\n\n", soup.get_text("\n")).strip()
    except ImportError:
        try:
            from html.parser import HTMLParser
            class _T(HTMLParser):
                def __init__(self):
                    super().__init__()
                    self.parts = []
                    self.skip = 0
                    self.in_title = False
                    self.title = ""
                def handle_starttag(self, tag, attrs):
                    if tag in ("script", "style", "noscript", "svg"):
                        self.skip += 1
                    if tag == "title":
                        self.in_title = True
                def handle_endtag(self, tag):
                    if tag in ("script", "style", "noscript", "svg") and self.skip > 0:
                        self.skip -= 1
                    if tag == "title":
                        self.in_title = False
                    if tag in ("p", "br", "div", "li", "h1", "h2", "h3", "h4", "tr"):
                        self.parts.append("\n")
                def handle_data(self, data):
                    if self.skip == 0:
                        self.parts.append(data)
                    if self.in_title:
                        self.title += data
            p = _T()
            p.feed(html)
            text = re.sub(r"\n{3,}", "\n\n", "".join(p.parts)).strip()
            title = p.title.strip()
        except Exception as e:
            text = f"[parse failed: {e}]"

    (src_dir / "raw.txt").write_text(f"# {title or url}\n\nURL: {url}\n\n{text}", encoding="utf-8")
    (src_dir / "meta.json").write_text(json.dumps({"url": url, "title": title, "fetched_at": datetime.now().isoformat()}, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"kind": "url", "title": title or urlparse(url).netloc, "meta": {"url": url, "title": title}}


def ingest_image(path: str, src_dir: Path) -> dict:
    fname = os.path.basename(path)
    dst = src_dir / fname
    shutil.copy2(path, dst)
    (src_dir / "raw.txt").write_text(
        f"# Image: {fname}\n\nLocal source: {path}\nSaved as: {dst}\n\n(See image file for content; multi-modal summarization should view it.)",
        encoding="utf-8",
    )
    return {"kind": "image", "title": os.path.splitext(fname)[0], "meta": {"image_path": str(dst)}}


def ingest_text(text: str, src_dir: Path) -> dict:
    (src_dir / "raw.txt").write_text(text, encoding="utf-8")
    title = text.strip().splitlines()[0][:30] if text.strip() else "note"
    return {"kind": "text", "title": title, "meta": {}}


def cmd_ingest(args, cfg):
    inp = args.input
    kind = detect_kind(inp)
    out_dir = Path(cfg["output_dir"]).expanduser().resolve()
    folder = make_folder(out_dir, kind, args.title or "")
    src_dir = folder / "source"

    if kind == "youtube":
        result = ingest_youtube(inp, src_dir)
    elif kind == "url":
        result = ingest_url(inp, src_dir, fetcher=args.fetcher)
    elif kind == "image":
        result = ingest_image(inp, src_dir)
    else:
        result = ingest_text(inp, src_dir)

    if not args.title and result.get("title"):
        new_slug = slugify(result["title"])
        prefix = folder.name.split("-")[0] + "-" + folder.name.split("-")[1]
        if new_slug:
            new_folder = folder.parent / f"{prefix}-{new_slug}"
            try:
                if new_folder != folder:
                    folder.rename(new_folder)
                    folder = new_folder
            except OSError:
                pass

    info = {"kind": result["kind"], "title": result.get("title"), "input": inp, "folder": str(folder), "created_at": datetime.now().isoformat(), "meta": result.get("meta", {})}
    (folder / "info.json").write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"FOLDER: {folder}")
    print(f"KIND:   {result['kind']}")
    print(f"TITLE:  {result.get('title')}")
    return folder


_SUMMARY_SYS = (
    "You are a careful study-note writer. Given source material, produce a Markdown summary following exactly this structure (keep section headings verbatim, including emojis):\n\n"
    "# <title>\n\n"
    "> **Source**: ...\n"
    "> **Type**: ...\n"
    "> **Length**: ...\n\n"
    "## 🎯 One-line summary\n\n"
    "## 📌 Key points\n\n"
    "## 🔑 Facts / data\n\n"
    "## 💡 Takeaways\n\n"
    "## 🤔 Open questions\n\n"
    "Be concise but information-dense."
)

_TALKSHOW_SYS = (
    "Write a short, lively two-host talk-show script discussing the source. Keep it informative, not cheesy. Return only the script with [Speaker] tags, no stage directions, no markdown fences."
)

_DECK_SYS = (
    "Create a compact slide-plan as strict JSON matching this schema: "
    "{title, subtitle, slides:[{type,title,subtitle,bullets,headers,rows,steps,image_path,caption,left,text}]}. "
    "Use 5-10 slides max. Prefer concrete bullets and tables over fluff. Return ONLY JSON."
)


def _read_source(folder: Path) -> str:
    raw = folder / "source" / "raw.txt"
    if raw.exists():
        return raw.read_text(encoding="utf-8", errors="replace")
    raise FileNotFoundError(f"Missing source/raw.txt in {folder}")


def _find_image_files(folder: Path):
    exts = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif"}
    src = folder / "source"
    return [str(p.resolve()) for p in src.iterdir() if p.is_file() and p.suffix.lower() in exts]


def _lang_directive(language: str) -> str:
    name = _LANGUAGE_NAMES.get(language, language)
    return (f"\n\nIMPORTANT: Write ALL output (including section headings' non-emoji text, body text, bullets, table cells, captions) in {name}. Keep proper nouns, code identifiers, and technical terms verbatim in their original form.")


def cmd_summarize(args, cfg):
    folder = Path(args.folder).resolve()
    provider = ai_provider.get_provider(cfg["ai"])
    language = _resolve_language(cfg, getattr(args, "language", "") or "")
    src = _read_source(folder)
    info = json.loads((folder / "info.json").read_text(encoding="utf-8"))
    user = f"Source type: {info.get('kind')}\nTitle hint: {info.get('title')}\nInput: {info.get('input')}\n\n=== SOURCE START ===\n{src[:60000]}\n=== SOURCE END ==="
    md = provider.complete(_SUMMARY_SYS + _lang_directive(language), user)
    (folder / "summary.md").write_text(md, encoding="utf-8")
    print(f"summary.md: {len(md)} chars (lang={language})")


def cmd_talkshow(args, cfg):
    folder = Path(args.folder).resolve()
    provider = ai_provider.get_provider(cfg["ai"])
    language = _resolve_language(cfg, getattr(args, "language", "") or "")
    voices = _resolve_voices(cfg, language)
    if not voices:
        raise SystemExit("tts.voices is empty in config — add at least two speakers.")
    tags = list(voices.keys())
    summary_md = (folder / "summary.md").read_text(encoding="utf-8") if (folder / "summary.md").exists() else _read_source(folder)
    user = f"Two hosts: {', '.join(tags)}.\nUse lines like [{tags[0]}] … and [{tags[1]}] … (only these tags).\nMaterial to discuss:\n\n{summary_md[:30000]}"
    script = provider.complete(_TALKSHOW_SYS + _lang_directive(language), user)
    (folder / "talkshow.txt").write_text(script, encoding="utf-8")
    print(f"talkshow.txt: {len(script)} chars (lang={language}, hosts={tags})")


def cmd_deckplan(args, cfg):
    folder = Path(args.folder).resolve()
    provider = ai_provider.get_provider(cfg["ai"])
    language = _resolve_language(cfg, getattr(args, "language", "") or "")
    summary_md = (folder / "summary.md").read_text(encoding="utf-8") if (folder / "summary.md").exists() else _read_source(folder)
    image_files = _find_image_files(folder)
    user = (
        f"Available local images you may reuse in image/image+text slides:\n" +
        "\n".join(image_files[:10]) +
        f"\n\nWrite slide JSON for this material:\n\n{summary_md[:30000]}"
    )
    obj = ai_provider.complete_json(provider, _DECK_SYS + _lang_directive(language), user)
    if not isinstance(obj, dict) or "slides" not in obj:
        raise SystemExit("Model returned invalid deck JSON")
    if image_files:
        for slide in obj.get("slides", []):
            if slide.get("type") in {"image", "two_column"} and not slide.get("image_path"):
                slide["image_path"] = image_files[0]
    (folder / "deck.json").write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"deck.json: {len(obj.get('slides', []))} slides (lang={language})")


def cmd_tts(args, cfg):
    language = _resolve_language(cfg, getattr(args, "language", "") or "")
    voices_cfg = _resolve_voices(cfg, language)
    voices = {k: (v.get("voice"), v.get("rate", "+0%")) for k, v in voices_cfg.items() if v.get("voice")}
    if not voices:
        raise SystemExit("tts.voices is empty in config — add at least one speaker.")
    text = Path(args.script).read_text(encoding="utf-8")
    build_dual_audio(text, args.output, voices, use_jingle=cfg["tts"].get("jingle", True), custom_jingle_mp3=cfg["tts"].get("custom_jingle_mp3", ""))


def cmd_ppt(args, cfg):
    build_pptx(args.json, args.output)


def cmd_publish(args, cfg):
    folder = Path(args.folder).resolve()
    info = json.loads((folder / "info.json").read_text(encoding="utf-8")) if (folder / "info.json").exists() else {}
    slug = folder.name

    one_liner = ""
    sm = folder / "summary.md"
    title = info.get("title") or slug
    if sm.exists():
        md = sm.read_text(encoding="utf-8")
        m = re.search(r"##\s*🎯[^\n]*\n+([^\n#]+)", md)
        if m:
            one_liner = m.group(1).strip()
        else:
            for ln in md.splitlines():
                s = ln.strip()
                if s and not s.startswith("#") and not s.startswith(">"):
                    one_liner = s
                    break

    links: Dict[str, str] = {}
    local_links: Dict[str, str] = {}
    for label, fname in [("🎧 Listen", "talkshow.mp3"), ("📊 Slides", "deck.pptx"), ("📝 Summary", "summary.md")]:
        fp = folder / fname
        if fp.exists():
            local_links[label] = fp.as_uri()

    upload_cfg = cfg.get("upload") or {}
    cloud_links: Dict[str, str] = {}
    try:
        cloud_links = upload_mod.upload_folder(folder, upload_cfg)
    except Exception as e:
        print(f"WARN upload failed: {e}")

    for label, uri in local_links.items():
        links[label] = cloud_links.get(label) or uri

    (folder / "links.json").write_text(json.dumps({"title": title, "slug": slug, "summary": one_liner, "links": links, "local_links": local_links, "cloud_links": cloud_links}, ensure_ascii=False, indent=2), encoding="utf-8")

    n = cfg.get("notify") or {}
    try:
        notify.post(n.get("webhook_url"), n.get("style", "generic"), title, one_liner, links)
    except Exception as e:
        print(f"WARN notify failed: {e}")

    deliver_results = []
    d = cfg.get("deliver") or {}
    try:
        deliver_results = deliver.deliver_folder(folder, d, title, one_liner, links)
    except Exception as e:
        print(f"WARN deliver failed: {e}")

    publish_meta = {
        "title": title,
        "slug": slug,
        "summary": one_liner,
        "links": links,
        "local_links": local_links,
        "cloud_links": cloud_links,
        "deliver_results": deliver_results,
    }
    (folder / "links.json").write_text(json.dumps(publish_meta, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"PUBLISH DONE — {folder}")
    print(json.dumps(links, ensure_ascii=False, indent=2))


def cmd_auto(args, cfg):
    folder = cmd_ingest(args, cfg)
    provider_name = cfg["ai"].get("provider", "none")
    if provider_name == "none":
        print("ai.provider is 'none' — stopping after ingest.")
        return

    try:
        ai_provider.get_provider(cfg["ai"])
    except AIError as e:
        raise SystemExit(
            f"auto mode cannot continue because AI provider '{provider_name}' is not ready.\n"
            f"Reason: {e}\n\n"
            "Fix one of these and retry:\n"
            "- install the matching SDK inside yumnb's .venv\n"
            "- set the required API key / base URL\n"
            "- or switch ai.provider to 'none' and use step-by-step mode"
        )

    lang_override = getattr(args, "language", "") or ""

    class _Ns:
        pass

    ns = _Ns()
    ns.folder = str(folder)
    ns.language = lang_override
    cmd_summarize(ns, cfg)

    if cfg["tts"].get("enabled", True):
        cmd_talkshow(ns, cfg)
        tts_ns = _Ns()
        tts_ns.script = str(folder / "talkshow.txt")
        tts_ns.output = str(folder / "talkshow.mp3")
        tts_ns.language = lang_override
        cmd_tts(tts_ns, cfg)

    cmd_deckplan(ns, cfg)
    ppt_ns = _Ns()
    ppt_ns.json = str(folder / "deck.json")
    ppt_ns.output = str(folder / "deck.pptx")
    ppt_ns.language = lang_override
    cmd_ppt(ppt_ns, cfg)

    pub_ns = _Ns()
    pub_ns.folder = str(folder)
    pub_ns.language = lang_override
    cmd_publish(pub_ns, cfg)


def main():
    ap = argparse.ArgumentParser(prog="yumnb")
    ap.add_argument("--config", default="", help="Path to config.yaml")
    ap.add_argument("--language", default="", help="Override output language (e.g. en|zh|ja|es|fr|de). Defaults to config.language or 'en'. Selects both AI prompt language and the default TTS voice pair.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("ingest")
    p.add_argument("input"); p.add_argument("--title", default="")
    p.add_argument("--fetcher", default="", help="Optional external command (e.g. 'python my_fetch.py') used to fetch JS/auth-walled pages when plain requests gets HTML-less response.")
    p.set_defaults(func=cmd_ingest)

    p = sub.add_parser("summarize"); p.add_argument("folder"); p.set_defaults(func=cmd_summarize)
    p = sub.add_parser("talkshow"); p.add_argument("folder"); p.set_defaults(func=cmd_talkshow)
    p = sub.add_parser("deckplan"); p.add_argument("folder"); p.set_defaults(func=cmd_deckplan)

    p = sub.add_parser("tts")
    p.add_argument("script"); p.add_argument("--output", required=True)
    p.set_defaults(func=cmd_tts)

    p = sub.add_parser("ppt")
    p.add_argument("json"); p.add_argument("--output", required=True)
    p.set_defaults(func=cmd_ppt)

    p = sub.add_parser("publish"); p.add_argument("folder"); p.set_defaults(func=cmd_publish)

    p = sub.add_parser("auto")
    p.add_argument("input"); p.add_argument("--title", default="")
    p.add_argument("--fetcher", default="")
    p.set_defaults(func=cmd_auto)

    args = ap.parse_args()
    cfg = load_config(args.config)
    args.func(args, cfg)


if __name__ == "__main__":
    main()
