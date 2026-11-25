#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shrink videos to a target file size with a quality-first ladder.

Order: stream copy -> same-resolution CQ 19 -> CQ 22 -> CQ 24 -> 1080p CQ 20/24
-> 720p CQ 24. Every rung caps bitrate from the size budget, so one pass lands
close to the target instead of overshooting.

Usage:
  python video_shrink.py input.mp4 --limit-mb 28 --out out.mp4
  python video_shrink.py "clips/*.mp4" --limit-mb 28 --out-dir shrunk/
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import shutil
import subprocess
import sys

FF = shutil.which("ffmpeg") or "ffmpeg"
FP = shutil.which("ffprobe") or "ffprobe"

HDR_TRANSFERS = {"arib-std-b67", "smpte2084", "smpte428", "linear"}


def log(msg: str) -> None:
    print(msg, flush=True)


def probe(path: str) -> dict:
    p = subprocess.run(
        [FP, "-v", "error", "-print_format", "json", "-show_streams", "-show_format", path],
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        raise RuntimeError(f"ffprobe failed for {path}: {(p.stderr or '')[-200:]}")
    d = json.loads(p.stdout or "{}")
    streams = d.get("streams", [])
    v = next((s for s in streams if s.get("codec_type") == "video"), None)
    a = next((s for s in streams if s.get("codec_type") == "audio"), None)
    if not v:
        raise RuntimeError(f"no video stream in {path}")

    w, h = int(v["width"]), int(v["height"])
    rot = 0
    for sd in v.get("side_data_list", []) or []:
        if "rotation" in sd:
            try:
                rot = int(float(sd["rotation"]))
            except (TypeError, ValueError):
                rot = 0
    if abs(rot) % 180 == 90:
        w, h = h, w

    pix = (v.get("pix_fmt") or "").lower()
    trc = (v.get("color_transfer") or "").lower()
    hdr = trc in HDR_TRANSFERS or "10le" in pix or "12le" in pix
    dur = float(d.get("format", {}).get("duration") or v.get("duration") or 0)
    return {
        "w": w, "h": h, "dur": dur, "hdr": hdr, "trc": trc, "pix_fmt": pix,
        "vcodec": v.get("codec_name"), "audio": a is not None,
        "size": os.path.getsize(path),
    }


def nvenc_available(codec: str) -> bool:
    enc = "hevc_nvenc" if codec == "hevc" else "h264_nvenc"
    try:
        out = subprocess.run([FF, "-hide_banner", "-encoders"],
                             capture_output=True, text=True, timeout=30)
    except Exception:
        return False
    return enc in (out.stdout or "")


def even(n: float) -> int:
    n = int(round(n))
    return n - (n % 2)


def scale_expr(w: int, h: int, short_edge: int | None) -> str | None:
    if not short_edge or min(w, h) <= short_edge:
        return None
    return (f"scale=w='if(gte(iw,ih),-2,min({short_edge},iw))':"
            f"h='if(gte(iw,ih),min({short_edge},ih),-2)':flags=lanczos,setsar=1")


def tonemap_expr() -> str:
    return ("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,"
            "tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv")


def build_vf(info: dict, short_edge: int | None, keep_hdr: bool) -> str | None:
    parts = []
    if info["hdr"] and not keep_hdr:
        parts.append(tonemap_expr())
    se = scale_expr(info["w"], info["h"], short_edge)
    if se:
        parts.append(se)
    parts.append("format=yuv420p")
    return ",".join(parts)


def maxrate_for(limit_bytes: int, dur: float, audio_kbps: int,
                safety: float = 0.94) -> int | None:
    if dur <= 0:
        return None
    video_bits = limit_bytes * 8 * safety - audio_kbps * 1000 * dur
    video_bits = max(video_bits, limit_bytes * 8 * 0.5)
    return max(int(video_bits / dur), 700_000)


def run_ff(cmd: list) -> tuple[bool, str]:
    p = subprocess.run(cmd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=7200)
    return p.returncode == 0, (p.stderr or "")[-300:]


def shrink_one(src: str, dst: str, limit_mb: float, codec: str, keep_audio: bool,
               prefer_1080: bool, keep_hdr: bool, dry_run: bool) -> dict:
    info = probe(src)
    limit = int(limit_mb * 1024 * 1024 * 0.97)
    audio_kbps = 192 if (info["audio"] and keep_audio) else 0
    enc = ("hevc_nvenc" if codec == "hevc" else "h264_nvenc")
    hw = nvenc_available(codec)

    vcodec, preset, tune = ("hevc", "p7", "uhq") if codec == "hevc" else ("h264", "p7", "hq")
    tiers = [("copy", None, None)]
    first_edge = 1080 if prefer_1080 else None
    tiers += [
        ("cq19@orig", None, 19),
        ("cq22@orig", None, 22),
        ("cq24@orig", None, 24),
        ("cq20@1080", 1080, 20),
        ("cq24@1080", 1080, 24),
        ("cq24@720", 720, 24),
    ]
    if prefer_1080:
        tiers = [("cq19@1080", 1080, 19), ("cq21@1080", 1080, 21),
                 ("cq24@1080", 1080, 24), ("cq24@720", 720, 24)]

    work = os.path.join(os.path.dirname(os.path.abspath(dst)) or ".", ".shrink")
    os.makedirs(work, exist_ok=True)
    best = None

    for name, short_edge, cq in tiers:
        out = os.path.join(work, f"try_{name.replace('@', '_')}.mp4")
        if name == "copy" and info["vcodec"] not in ("h264", "hevc"):
            continue
        if name == "copy":
            cmd = [FF, "-y", "-hide_banner", "-loglevel", "error", "-i", src]
            cmd += ["-c", "copy"] if (info["audio"] and keep_audio) else ["-c:v", "copy", "-an"]
            cmd += ["-movflags", "+faststart", out]
        else:
            vf = build_vf(info, short_edge, keep_hdr)
            cmd = [FF, "-y", "-hide_banner", "-loglevel", "error", "-i", src]
            if vf:
                cmd += ["-vf", vf]
            mr = maxrate_for(limit, info["dur"], audio_kbps)
            if hw:
                cmd += ["-c:v", enc, "-preset", preset, "-tune", tune,
                        "-rc", "vbr", "-cq", str(cq), "-b:v", "0"]
            else:
                cmd += ["-c:v", "libx265" if codec == "hevc" else "libx264",
                        "-preset", "slow", "-crf", str(cq)]
            cmd += ["-profile:v", "main" if codec == "hevc" else "high"]
            if mr:
                cmd += ["-maxrate", str(mr), "-bufsize", str(mr * 2)]
            if info["audio"] and keep_audio:
                cmd += ["-c:a", "aac", "-b:a", "192k", "-ac", "2"]
            else:
                cmd += ["-an"]
            cmd += ["-movflags", "+faststart", out]

        ok, err = run_ff(cmd)
        if not ok and name != "copy" and hw:
            hw = False
            cmd[cmd.index(enc)] = "libx265" if codec == "hevc" else "libx264"
            ok, err = run_ff(cmd)
        if not ok:
            log(f"[SKIP] {os.path.basename(src)} {name}: {err}")
            continue

        size = os.path.getsize(out)
        if best is None or size < best[2]:
            best = (name, out, size)
        if size <= limit:
            best = (name, out, size)
            break

    if not best:
        raise RuntimeError("all tiers failed")

    name, tmp, size = best
    if not dry_run:
        shutil.copyfile(tmp, dst)
    dims = (info["w"], info["h"]) if "@orig" in name or name == "copy" else None
    if dims is None:
        p = subprocess.run([FP, "-v", "error", "-select_streams", "v:0",
                            "-show_entries", "stream=width,height", "-of", "csv=p=0", tmp],
                           capture_output=True, text=True)
        try:
            w, h = [int(x) for x in p.stdout.strip().split(",")[:2]]
        except Exception:
            w, h = info["w"], info["h"]
    else:
        w, h = dims

    res = {
        "input": src, "output": dst, "limit_mb": limit_mb,
        "input_mb": round(info["size"] / 1048576, 1),
        "output_mb": round(size / 1048576, 1),
        "tier": name, "width": w, "height": h, "duration": round(info["dur"], 1),
        "fits": size <= limit, "encoder": enc if hw else ("libx265" if codec == "hevc" else "libx264"),
        "hdr_tonemapped": bool(info["hdr"] and not keep_hdr),
    }
    return res


def main() -> None:
    ap = argparse.ArgumentParser(description="Shrink video to a target size, quality first.")
    ap.add_argument("input", help="input file or glob pattern")
    ap.add_argument("--limit-mb", type=float, default=28.0, help="max output size in MB (default 28)")
    ap.add_argument("--out", help="output file (single input only)")
    ap.add_argument("--out-dir", help="output directory (batch mode)")
    ap.add_argument("--codec", choices=["h264", "hevc"], default="h264")
    ap.add_argument("--strip-audio", action="store_true", help="remove audio track")
    ap.add_argument("--prefer-1080", action="store_true", help="start the ladder at 1080 short edge")
    ap.add_argument("--keep-hdr", action="store_true", help="do not tonemap HDR to SDR")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of text lines")
    ap.add_argument("--dry-run", action="store_true", help="encode but do not write the output file")
    args = ap.parse_args()

    files = sorted(glob.glob(args.input)) if any(c in args.input for c in "*?[") else [args.input]
    files = [f for f in files if os.path.isfile(f)]
    if not files:
        log(f"[FAIL] no input files matched {args.input}")
        sys.exit(2)
    if len(files) > 1 and not args.out_dir:
        log("[FAIL] multiple inputs require --out-dir")
        sys.exit(2)

    results, failures = [], 0
    for f in files:
        if args.out_dir:
            os.makedirs(args.out_dir, exist_ok=True)
            base, ext = os.path.splitext(os.path.basename(f))
            dst = os.path.join(args.out_dir, f"{base}_shrunk{ext or '.mp4'}")
        else:
            dst = args.out or os.path.splitext(f)[0] + "_shrunk.mp4"
        try:
            r = shrink_one(f, dst, args.limit_mb, args.codec, not args.strip_audio,
                           args.prefer_1080, args.keep_hdr, args.dry_run)
        except Exception as exc:
            log(f"[FAIL] {f}: {exc}")
            failures += 1
            continue
        results.append(r)
        if args.json:
            log(json.dumps(r, ensure_ascii=False))
        else:
            log("[SHRINK] %s %dx%d %.1fs %.1fMB -> %.1fMB tier=%s %dx%d%s" % (
                os.path.basename(f), r["width"], r["height"], r["duration"],
                r["input_mb"], r["output_mb"], r["tier"], r["width"], r["height"],
                " (HDR->SDR)" if r["hdr_tonemapped"] else ""))
        if not r["fits"]:
            failures += 1

    if not args.json:
        tin = sum(r["input_mb"] for r in results)
        tout = sum(r["output_mb"] for r in results)
        log("[SUMMARY] ok=%d over=%d total_in=%.1fMB total_out=%.1fMB" % (
            len(results) - failures, failures, tin, tout))
    sys.exit(0 if failures == 0 else 1)


if __name__ == "__main__":
    main()
