"""Stage 2 - acquire audio and put the original and the instrumental on ONE timeline.

Strategy
--------
* Download the original song and a karaoke instrumental from Bilibili (dash audio).
* Find the constant time offset between them with chroma cross-correlation.
* Re-emit both at SR so that t=0 is the same instant (the instrumental gets a
  head pad of |offset|), which means LRC timestamps apply to both directly.

Outputs in <run-dir>/02:
  orig.wav        original mix, SR mono
  inst.wav        instrumental, same length/timeline as orig
  audio.json      {origin:{bv,cid,stream}, duration, offset, tempo, beats}
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import time
from pathlib import Path

from common import SR, ffmpeg_exe, load_mono, save_json, save_wav

UA = {"User-Agent": "Mozilla/5.0", "Referer": ""}


def bili_search(term: str, limit: int = 12):
    import requests
    s = requests.Session()
    s.headers["User-Agent"] = UA["User-Agent"]
    s.get("https://www.bilibili.com", timeout=20)      # cookie for the playback api
    r = s.get("https://api.bilibili.com/x/web-interface/search/type",
              params={"search_type": "video", "keyword": term, "page": 1},
              headers={"Referer": "https://www.bilibili.com/"}, timeout=25)
    out = []
    for v in (r.json().get("data", {}).get("result") or [])[:limit]:
        out.append({"bvid": v["bvid"], "title": re.sub(r"<[^>]+>", "", v["title"]),
                    "duration": v.get("duration", ""), "author": v.get("author", "")})
    return s, out


def bili_audio(bv: str, dest: Path, sess=None):
    """Download the highest-bitrate dash audio track of `bv` as `.m4s`."""
    import requests
    s = sess or requests.Session()
    s.headers["User-Agent"] = UA["User-Agent"]
    if not s.cookies:
        s.get("https://www.bilibili.com", timeout=20)
    v = s.get("https://api.bilibili.com/x/web-interface/view",
              params={"bvid": bv}, headers={"Referer": "https://www.bilibili.com/"},
              timeout=25).json()
    if v.get("code") != 0:
        raise SystemExit(f"view failed for {bv}: {v.get('message')}")
    d = v["data"]
    cid = d["pages"][0]["cid"]
    pu = s.get("https://api.bilibili.com/x/player/playurl",
               params={"bvid": bv, "cid": cid, "fnval": 16, "fourk": 1},
               headers={"Referer": f"https://www.bilibili.com/video/{bv}"},
               timeout=25).json()
    if pu.get("code") != 0:
        raise SystemExit(f"playurl failed for {bv}: {pu.get('message')}")
    audio = pu["data"].get("dash", {}).get("audio") or []
    if not audio:
        raise SystemExit(f"no dash audio for {bv}")
    best = max(audio, key=lambda a: a.get("bandwidth", 0))
    r = s.get(best["baseUrl"], headers={"Referer": f"https://www.bilibili.com/video/{bv}",
                                        "User-Agent": UA["User-Agent"]}, timeout=600)
    r.raise_for_status()
    dest.write_bytes(r.content)
    return {"bv": bv, "title": d.get("title"), "cid": cid,
            "stream": best.get("id"), "bandwidth": best.get("bandwidth"),
            "bytes": len(r.content)}


def to_wav(src: Path, dst: Path):
    cmd = [ffmpeg_exe(), "-hide_banner", "-loglevel", "error", "-y",
           "-i", str(src), "-ac", "1", "-ar", str(SR), "-vn", str(dst)]
    subprocess.run(cmd, check=True)


def find_offset(a_wav: Path, b_wav: Path, hop: int = 2048) -> tuple[float, float]:
    """Return (offset_seconds, score) where a[off + t] ~= b[t].

    A positive offset means b's content happens earlier than a's content, so
    b needs `offset` seconds of silence prepended to share a's timeline.
    """
    import librosa
    import numpy as np
    a, _ = librosa.load(str(a_wav), sr=SR, mono=True)
    b, _ = librosa.load(str(b_wav), sr=SR, mono=True)
    ca = librosa.feature.chroma_cqt(y=librosa.effects.harmonic(a), sr=SR, hop_length=hop)
    cb = librosa.feature.chroma_cqt(y=librosa.effects.harmonic(b), sr=SR, hop_length=hop)

    def score(lag):
        if lag >= 0:
            x, y = ca[:, : ca.shape[1] - lag], cb[:, lag:]
        else:
            x, y = ca[:, -lag:], cb[:, : cb.shape[1] + lag]
        n = min(x.shape[1], y.shape[1])
        if n < 100:
            return -1.0
        x, y = x[:, :n], y[:, :n]
        return float(np.mean(np.sum(x * y, 0)
                             / (np.linalg.norm(x, axis=0) * np.linalg.norm(y, axis=0) + 1e-8)))

    fps = SR / hop
    best = (-9.0, 0)
    for lag in range(-120, 121, 2):
        s = score(lag)
        if s > best[0]:
            best = (s, lag)
    for lag in range(best[1] - 4, best[1] + 5):
        s = score(lag)
        if s > best[0]:
            best = (s, lag)
    return best[1] / fps, best[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--orig-bv", default="BV1Rs4y1X7RY", help="or --orig-file")
    ap.add_argument("--inst-bv", default="BV1ZecrzPEQ2", help="or --inst-file")
    ap.add_argument("--orig-file")
    ap.add_argument("--inst-file")
    ap.add_argument("--search", help="list Bilibili candidates for a query and exit")
    a = ap.parse_args()

    if a.search:
        _, hits = bili_search(a.search)
        for h in hits:
            print(f"{h['bvid']}  {h['duration']:>7}  {h['title'][:60]}  [{h['author']}]")
        return

    run = Path(a.run_dir)
    out = run / "02"
    out.mkdir(parents=True, exist_ok=True)
    cache = run.parent.parent / "cache"
    cache.mkdir(parents=True, exist_ok=True)

    meta = {}

    def resolve(kind, bv, local):
        if local:
            return Path(local)
        raw = cache / f"{kind}_{bv}.m4s"
        if not raw.exists() or raw.stat().st_size < 100_000:
            t0 = time.time()
            meta[kind] = bili_audio(bv, raw)
            meta[kind]["download_s"] = round(time.time() - t0, 1)
        else:
            meta.setdefault(kind, {"bv": bv, "cached": True})
        wav = out / f"{kind}_raw.wav"
        if not wav.exists() or raw.stat().st_mtime > wav.stat().st_mtime:
            to_wav(raw, wav)
        return wav

    ow = resolve("orig", a.orig_bv, a.orig_file)
    iw = resolve("inst", a.inst_bv, a.inst_file)

    off, score = find_offset(ow, iw)
    print(f"offset {off:+.2f}s (score {score:.3f}): the instrumental's content is "
          f"{abs(off):.2f}s {'earlier' if off < 0 else 'later'} than the original's")

    import numpy as np
    o = load_mono(ow)
    i = load_mono(iw)
    pad = int(round(abs(off) * SR))
    if off < 0:          # instrumental is early -> prepend silence to it
        i = np.concatenate([np.zeros(pad, dtype=i.dtype), i])
    elif off > 0:        # original is early -> prepend silence to it
        o = np.concatenate([np.zeros(pad, dtype=o.dtype), o])
    n = min(len(o), len(i))
    o, i = o[:n], i[:n]

    save_wav(out / "orig.wav", o)
    save_wav(out / "inst.wav", i)

    import librosa
    tempo, beats = librosa.beat.beat_track(y=i, sr=SR, hop_length=512, units="time")
    meta["offset_s"] = round(off, 3)
    meta["offset_score"] = round(score, 3)
    meta["duration_s"] = round(n / SR, 3)
    meta["tempo"] = round(float(np.atleast_1d(tempo)[0]), 2)
    meta["beats"] = [round(float(b), 3) for b in beats]
    save_json(out / "audio.json", meta)
    print(f"duration {n / SR:.2f}s, tempo {meta['tempo']}, {len(beats)} beats")


if __name__ == "__main__":
    main()
