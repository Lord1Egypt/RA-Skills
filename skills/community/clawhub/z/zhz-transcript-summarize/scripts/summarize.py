#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""读取缓存转录稿，准备摘要输入：术语表纠错、时间轴骨架、字幕导出、上下文文件。

用法:
    python summarize.py <文件路径> [--focus ...] [--audience ...] [--format ...] [--lang ...]
                          [--glossary glossary.txt] [--timeline auto] [--format-sub srt]
                          [--out-dir DIR] [--model base] [--cache DIR] [--cache-json FILE]

本脚本只做确定性准备，不做摘要生成；最终摘要由当前代理会话的模型生成并写入 out-dir/summary.md。
换角度重新总结时只需重跑本脚本（修改 --focus 等参数），完全跳过转录阶段。
"""

import argparse
import hashlib
import json
import logging
import sys
from pathlib import Path

LOG = logging.getLogger("zhz-summarize")

CACHE_ROOT = Path.home() / ".cache" / "zhz-transcript"
BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES = {
    "meeting": "meeting.md",
    "key_summary": "key_summary.md",
    "analysis": "analysis.md",
}

LENGTH_HINT = {
    "short": "简洁：中文约 300 字以内 / 英文约 150 词以内，只保留最关键结论",
    "medium": "适中：中文约 800 字 / 英文约 400 词，覆盖主要观点",
    "detailed": "详细：中文 1500 字以上 / 英文 800 词以上，尽量完整、分点展开",
}


def _setup_logging():
    if LOG.handlers:
        return
    LOG.setLevel(logging.INFO)
    h_out = logging.StreamHandler(sys.stdout)
    h_out.setLevel(logging.INFO)
    h_out.addFilter(lambda r: r.levelno < logging.ERROR)
    h_err = logging.StreamHandler(sys.stderr)
    h_err.setLevel(logging.ERROR)
    h_err.setFormatter(logging.Formatter("[错误] %(message)s"))
    LOG.addHandler(h_out)
    LOG.addHandler(h_err)


def _reconfigure_stdout():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def fatal(msg):
    LOG.error(msg)
    sys.exit(1)


def file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_glossary(path):
    terms = []
    # utf-8-sig 容忍 BOM（记事本/Set-Content -Encoding utf8 常见）
    for raw in Path(path).read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        sep = None
        for s in ("\t", "->", "=>", "→", "=", "："):
            if s in line:
                sep = s
                break
        if sep is None:
            LOG.warning(f"跳过无法解析的术语行: {raw}")
            continue
        wrong, right = line.split(sep, 1)
        wrong, right = wrong.strip(), right.strip()
        if wrong and right and wrong != right:
            terms.append((wrong, right))
    return terms


def apply_glossary(text, terms):
    changes = []
    for wrong, right in terms:
        n = text.count(wrong)
        if n > 0:
            text = text.replace(wrong, right)
            changes.append({"wrong": wrong, "right": right, "count": n})
    return text, changes


def build_timeline(segments, window=300):
    buckets = {}
    for seg in segments:
        idx = int(seg["start"] // window)
        buckets.setdefault(idx, []).append(seg)
    out = []
    for idx in sorted(buckets):
        segs = buckets[idx]
        out.append({
            "start": round(segs[0]["start"], 1),
            "end": round(segs[-1]["end"], 1),
            "text": " ".join(s["text"] for s in segs).strip(),
        })
    return out


def _fmt_dur(seconds):
    s = int(seconds)
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    if h:
        return f"{h}:{m:02d}:{sec:02d}"
    return f"{m}:{sec:02d}"


def _srt_ts(seconds):
    ms = int(round((seconds - int(seconds)) * 1000))
    s = int(seconds)
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    base = f"{h:02d}:{m:02d}:{sec:02d}" if h else f"{m:02d}:{sec:02d}"
    return f"{base},{ms:03d}"


def _vtt_ts(seconds):
    ms = int(round((seconds - int(seconds)) * 1000))
    s = int(seconds)
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    base = f"{h:02d}:{m:02d}:{sec:02d}" if h else f"{m:02d}:{sec:02d}"
    return f"{base}.{ms:03d}"


def write_srt(segments, path):
    lines = []
    for i, seg in enumerate(segments, 1):
        lines.append(str(i))
        lines.append(f"{_srt_ts(seg['start'])} --> {_srt_ts(seg['end'])}")
        lines.append(seg["text"].strip())
        lines.append("")
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def write_vtt(segments, path):
    lines = ["WEBVTT", ""]
    for i, seg in enumerate(segments, 1):
        lines.append(str(i))
        lines.append(f"{_vtt_ts(seg['start'])} --> {_vtt_ts(seg['end'])}")
        lines.append(seg["text"].strip())
        lines.append("")
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def find_cache(src, model, cache_root):
    content_hash = file_sha256(src)
    json_path = cache_root / f"{content_hash}-{model}.json"
    if not json_path.is_file():
        cands = sorted(cache_root.glob(f"{content_hash}-*.json"))
        if cands:
            LOG.warning(f"未找到 {model} 模型的缓存，回退到: {cands[0].name}")
            json_path = cands[0]
        else:
            return None, content_hash
    return json_path, content_hash


def main():
    _reconfigure_stdout()
    _setup_logging()
    ap = argparse.ArgumentParser(description="读取缓存转录稿，准备摘要输入")
    ap.add_argument("path", help="原始音视频文件路径（用于定位缓存）")
    ap.add_argument("--cache-json", default=None, help="直接指定转录稿 JSON 路径（跳过内容哈希）")
    ap.add_argument("--model", default="base", help="缓存所用的 Whisper 模型")
    ap.add_argument("--cache-dir", default=None, help="缓存目录（默认 ~/.cache/zhz-transcript）")
    ap.add_argument("--focus", default="", help="总结焦点，如：云原生架构选型理由与踩坑经验")
    ap.add_argument("--audience", default="通用读者", help="目标受众")
    ap.add_argument("--format", dest="fmt", default="key_summary",
                    choices=["meeting", "key_summary", "analysis", "custom"],
                    help="摘要模板")
    ap.add_argument("--template", default=None, help="自定义模板文件（--format custom 时使用）")
    ap.add_argument("--length", default="medium", choices=["short", "medium", "detailed"])
    ap.add_argument("--lang", default="zh", help="输出语言 (zh/en)")
    ap.add_argument("--glossary", default=None, help="术语表 glossary.txt")
    ap.add_argument("--timeline", default="auto", choices=["auto", "on", "off"])
    ap.add_argument("--format-sub", dest="format_sub", default=None, choices=["srt", "vtt"],
                    help="导出字幕（基于原始转录稿，不含术语纠错）")
    ap.add_argument("--out-dir", default=None, help="输出目录（默认 summaries/<name>/）")
    args = ap.parse_args()

    cache_root = Path(args.cache_dir).expanduser() if args.cache_dir else CACHE_ROOT
    src = Path(args.path).expanduser().resolve()
    if not src.is_file():
        fatal(f"文件不存在: {src}")

    if args.cache_json:
        json_path = Path(args.cache_json).expanduser().resolve()
        if not json_path.is_file():
            fatal(f"转录稿不存在: {json_path}")
    else:
        json_path, _ = find_cache(src, args.model, cache_root)
        if json_path is None:
            fatal(
                "未找到转录稿缓存。请先运行: "
                f'python "{BASE_DIR / "scripts" / "transcribe.py"}" "{src}"'
            )

    data = json.loads(json_path.read_text(encoding="utf-8"))
    text = data.get("text", "")
    segments = data.get("segments", [])
    duration = data.get("duration", 0)
    language = data.get("language", "?")
    n_seg = len(segments)

    if args.out_dir:
        out_dir = Path(args.out_dir).expanduser()
    else:
        out_dir = Path.cwd() / "summaries" / src.stem
    out_dir.mkdir(parents=True, exist_ok=True)

    # 术语表纠错（只作用于摘要用的文本，不改缓存里的原始转录稿）
    changes = []
    if args.glossary:
        gp = Path(args.glossary).expanduser().resolve()
        if not gp.is_file():
            fatal(f"术语表不存在: {gp}")
        terms = load_glossary(gp)
        text, changes = apply_glossary(text, terms)
        LOG.info(f"术语表: 加载 {len(terms)} 条，命中 {len(changes)} 条")

    # 时间轴（>20 分钟自动生成）
    do_timeline = args.timeline == "on" or (args.timeline == "auto" and duration > 1200)
    timeline = build_timeline(segments) if do_timeline else []
    if do_timeline:
        LOG.info(f"内容时长 >20 分钟（{duration:.0f}s），生成时间轴骨架")

    # 字幕导出（原始转录稿）
    if args.format_sub == "srt":
        write_srt(segments, out_dir / "subtitles.srt")
        LOG.info("已导出字幕: subtitles.srt（原始转录稿）")
    elif args.format_sub == "vtt":
        write_vtt(segments, out_dir / "subtitles.vtt")
        LOG.info("已导出字幕: subtitles.vtt（原始转录稿）")

    # 上下文文件
    meta_lines = [
        "# 转录上下文",
        "",
        f"- 来源: {src.name}",
        f"- 时长: {_fmt_dur(duration)}",
        f"- 语言: {language}",
        f"- 段落: {n_seg}",
    ]
    if changes:
        meta_lines.append(f"- 术语更正: {len(changes)} 条（详见 glossary_changes.md）")
    meta_lines += ["", "## 转录稿（已按术语表更正）", ""]
    (out_dir / "context.md").write_text(
        "\n".join(meta_lines) + text + "\n", encoding="utf-8"
    )

    if changes:
        gl_lines = ["# 术语更正记录", "", "| 原词 | 更正为 | 出现次数 |", "|------|--------|---------|"]
        for c in changes:
            gl_lines.append(f"| {c['wrong']} | {c['right']} | {c['count']} |")
        gl_lines.append("")
        (out_dir / "glossary_changes.md").write_text("\n".join(gl_lines), encoding="utf-8")

    if timeline:
        tl_lines = ["# 时间轴骨架（请为每段补一句要点）", ""]
        for t in timeline:
            tl_lines.append(f"## [{_fmt_dur(t['start'])} – {_fmt_dur(t['end'])}]")
            tl_lines.append("")
            tl_lines.append(t["text"])
            tl_lines.append("")
        (out_dir / "timeline.md").write_text("\n".join(tl_lines), encoding="utf-8")

    # 模板
    if args.fmt == "custom":
        if not args.template:
            fatal("--format custom 需要 --template <模板文件>")
        tpl_path = Path(args.template).expanduser().resolve()
        if not tpl_path.is_file():
            fatal(f"模板文件不存在: {tpl_path}")
        template_text = tpl_path.read_text(encoding="utf-8-sig")
    else:
        tpl_path = BASE_DIR / "templates" / TEMPLATES[args.fmt]
        template_text = tpl_path.read_text(encoding="utf-8")

    params = [
        "",
        "",
        "## 本次总结参数",
        f"- 焦点: {args.focus or '（未指定，全面总结）'}",
        f"- 受众: {args.audience}",
        f"- 长度: {LENGTH_HINT[args.length]}",
        f"- 语言: {args.lang}",
    ]
    prompt_text = template_text + "\n".join(params) + "\n"
    (out_dir / "summary_prompt.md").write_text(prompt_text, encoding="utf-8")

    # 打印指引
    print()
    print("=" * 64)
    print("输入已就绪，请由代理会话的模型生成摘要：")
    print(f"  1. 读取转录稿:   {out_dir / 'context.md'}")
    if changes:
        print(f"  2. 术语更正记录: {out_dir / 'glossary_changes.md'}")
    if timeline:
        print(f"  3. 时间轴骨架:   {out_dir / 'timeline.md'}")
    print(f"  - 模板与参数:    {out_dir / 'summary_prompt.md'}")
    print(f"  - 请将最终摘要写入: {out_dir / 'summary.md'}")
    print("=" * 64)
    print()

    LOG.info("完成。输出目录: %s", out_dir)


if __name__ == "__main__":
    main()
