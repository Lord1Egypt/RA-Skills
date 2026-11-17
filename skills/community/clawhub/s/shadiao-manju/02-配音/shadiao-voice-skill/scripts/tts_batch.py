#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""沙雕配音批量合成（v0.1）

用法：
  python3 tts_batch.py --project 周一打工人 --season 1 --episode 1 --engine edge
  python3 tts_batch.py --project 周一打工人 --season 1 --episode 1 --engine clone --clone-consent
  python3 tts_batch.py --project 周一打工人 --season 1 --episode 1 --engine edge --only 3,7,9

输入：99-项目/<剧名>/第NN季/01-剧本/剧本.json
输出：99-项目/<剧名>/第NN季/02-配音/第NN集/S001.mp3 ...
      99-项目/<剧名>/第NN季/02-配音/第NN集/配音表.json

引擎：
  edge   edge-tts（秒级、免费、联网）
  clone  IndexTTS-2.5（本地、零样本、带情绪；M1 非实时）
  say    macOS say（离线兜底）
"""

import argparse
import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

# 工具链路径（含 $SHADIAO_TOOLCHAIN）只在 toolchain.py 里读
from toolchain import DEFAULT_CLONE, DOUYIN_DIR, MAKE_EMOTION

SKILL_ROOT = Path(__file__).resolve().parents[3]
PROJECTS_ROOT = SKILL_ROOT / "99-项目"
VOICE_DIR = Path(__file__).resolve().parents[1]
VOICES_PATH = VOICE_DIR / "voices.json"

# 抖音参考音频来源未登记授权，默认不许进入克隆合成
UNVERIFIED_REF_ROOT = DOUYIN_DIR

NARRATION_SPEAKERS = {"旁白", "叙述", "解说"}

# 沙雕扩展情绪 → 基础情绪（IndexTTS 原生）
EMOTION_ALIAS = {
    "得意": "开心",
    "无语": "无奈",
    "崩溃": "惊恐",
    "尴尬": "无奈",
    "心虚": "害怕",
    "震惊": "惊讶",
    "委屈": "悲伤",
    "嫌弃": "厌恶",
    "敷衍": "慵懒",
    "抓狂": "暴怒",
    "社死": "惊恐",
    "摆烂": "慵懒",
}

# macOS say 中文音色
SAY_VOICES = {
    "female": "Tingting",
    "male": "Tingting",
}


def run_cmd(cmd, **kwargs):
    """跑外部命令的唯一入口：一律列表传参、不经过 shell。

    这样「哪些外部程序会被调用」只有一处，也顺手统一了错误输出。
    """
    kwargs.setdefault("capture_output", True)
    kwargs.setdefault("text", True)
    return subprocess.run(list(cmd), **kwargs)


def die(msg, code=1):
    print(f"✗ {msg}", file=sys.stderr)
    sys.exit(code)


def load_voices():
    if not VOICES_PATH.is_file():
        die(f"找不到音色预设：{VOICES_PATH}")
    return json.loads(VOICES_PATH.read_text(encoding="utf-8"))


SAFE_NAME_RE = re.compile(r'^[^\\/:*?"<>|\x00-\x1f]{1,64}$')


def safe_name(name, what="剧名"):
    """剧名会拼进路径：不许带分隔符，不许是 . / .."""
    s = str(name or "").strip()
    if not s or not SAFE_NAME_RE.match(s) or s in (".", ".."):
        die(f"{what}不合法：{name!r}（不能含 / \\ : * ? \" < > |，不能是 . 或 ..）")
    return s


def season_dir(project, season):
    if not isinstance(season, int) or not (1 <= season <= 99):
        die(f"--season 必须是 1–99 的整数，实际是 {season}")
    return PROJECTS_ROOT / safe_name(project) / f"第{season:02d}季"


def resolve_voice(voice_name, characters, speaker, voices, allow_fallback=False):
    presets = voices["voices"]
    aliases = voices.get("aliases", {})

    candidates = []
    if voice_name:
        candidates.append(voice_name)
    if voice_name and voice_name in aliases:
        candidates.append(aliases[voice_name])
    if not voice_name:
        # 旁白 → 旁白预设
        if speaker in NARRATION_SPEAKERS:
            candidates.append("旁白-死鱼眼")
        else:
            for c in characters:
                if c.get("name") == speaker and c.get("voice"):
                    candidates.append(c["voice"])
                    if c["voice"] in aliases:
                        candidates.append(aliases[c["voice"]])
                    break

    for name in candidates:
        if name in presets:
            return name, presets[name]

    # 兜底：按性别
    gender = "male"
    for c in characters:
        if c.get("name") == speaker:
            gender = c.get("gender", "male")
            break
    fallback = "晓晓-暖调女声" if gender == "female" else "云希-清亮少年"
    if speaker in NARRATION_SPEAKERS:
        fallback = "旁白-死鱼眼"

    # 剧本里点名了音色却查不到：默认停下来，让用户自己决定，不要悄悄换人
    if name_wanted := (voice_name or "").strip():
        if not allow_fallback:
            die(
                f"音色「{name_wanted}」不在 voices.json 里（角色：{speaker}）。\n"
                f"  可选预设：{'、'.join(sorted(presets)[:12])} ……\n"
                "  改剧本里的 voice 字段，或加 --allow-voice-fallback 按性别兜底。"
            )
        print(f"  ! 音色「{name_wanted}」查不到，按 --allow-voice-fallback 兜底为 {fallback}", file=sys.stderr)
    else:
        print(f"  ! 角色「{speaker}」没指定音色，按性别兜底为 {fallback}", file=sys.stderr)
    return fallback, presets[fallback]


def combine_rate(base, boost):
    def pct(v):
        return int(str(v).strip().replace("%", "").replace("+", "") or 0)
    return f"{pct(base) + pct(boost):+d}%"


def edge_synthesize(text, preset, out_path, rate_boost="+0%"):
    if not shutil.which("edge-tts"):
        die("找不到 edge-tts。先安装：pip install -U edge-tts")
    rate = combine_rate(preset.get("rate", "+0%"), rate_boost)
    cmd = [
        "edge-tts",
        "--voice", preset["voice"],
        f"--rate={rate}",
        f"--pitch={preset.get('pitch', '+0Hz')}",
        "--text", text,
        "--write-media", str(out_path),
    ]
    r = run_cmd(cmd)
    if r.returncode != 0 or not out_path.exists() or out_path.stat().st_size == 0:
        raise RuntimeError(f"edge-tts 失败：{r.stderr.strip() or r.stdout.strip()}")


def say_synthesize(text, preset, out_path):
    voice = SAY_VOICES.get(preset.get("gender", "male"), "Tingting")
    with tempfile.NamedTemporaryFile(suffix=".aiff", delete=False) as f:
        tmp = Path(f.name)
    try:
        # 台词走 stdin：避免以 "-f" 之类开头时被 say 当成选项去读本地文件
        r = run_cmd(["say", "-v", voice, "-o", str(tmp)], input=text)
        if r.returncode != 0:
            raise RuntimeError(f"say 失败：{r.stderr.strip()}")
        r = run_cmd(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp),
             "-codec:a", "libmp3lame", "-q:a", "4", str(out_path)]
        )
        if r.returncode != 0:
            raise RuntimeError(f"ffmpeg 失败：{r.stderr.strip()}")
    finally:
        tmp.unlink(missing_ok=True)


def probe_duration_ms(path):
    r = run_cmd(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)]
    )
    if r.returncode != 0:
        raise RuntimeError(f"ffprobe 失败：{r.stderr.strip()}")
    try:
        return int(round(float(r.stdout.strip()) * 1000))
    except ValueError:
        raise RuntimeError(f"ffprobe 返回无法解析：{r.stdout!r}")


def sha1_short(text):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]


def build_lines(script, voices, allow_fallback=False):
    characters = script.get("characters", [])
    scenes = {s.get("id"): s for s in script.get("scenes", [])}
    out = []
    used_voice = {}
    for line in script.get("lines", []):
        seq = line.get("seq")
        speaker = (line.get("speaker") or "").strip().rstrip("：:")
        text = (line.get("text") or "").strip()
        if not text:
            continue
        scene_id = line.get("scene", "")
        scene = scenes.get(scene_id, {})
        # 角色表里的音色
        voice_name = ""
        for c in characters:
            if c.get("name") == speaker:
                voice_name = c.get("voice", "")
                break
        if speaker in NARRATION_SPEAKERS and not voice_name:
            voice_name = "旁白-死鱼眼"
        preset_name, preset = resolve_voice(voice_name, characters, speaker, voices, allow_fallback)
        used_voice[speaker or "旁白"] = preset_name

        out.append({
            "seq": seq,
            "speaker": speaker or "旁白",
            "type": line.get("type") or ("narration" if speaker in NARRATION_SPEAKERS else "dialogue"),
            "text": text,
            "emotion": line.get("emotion", "平静"),
            "sfx": line.get("sfx", ""),
            "scene": scene_id,
            "sceneTitle": scene.get("title", ""),
            "voice": preset_name,
            "preset": preset,
            "hash": sha1_short(f"{text}|{preset_name}"),
        })
    return out, used_voice


def run_edge(lines, out_dir, overwrite=False, rate_boost="+0%"):
    for item in lines:
        out = out_dir / f"S{item['seq']:03d}.mp3"
        if out.exists() and not overwrite and out.stat().st_size > 0:
            continue
        edge_synthesize(item["text"], item["preset"], out, rate_boost)


def run_say(lines, out_dir, overwrite=False):
    for item in lines:
        out = out_dir / f"S{item['seq']:03d}.mp3"
        if out.exists() and not overwrite and out.stat().st_size > 0:
            continue
        say_synthesize(item["text"], item["preset"], out)


def resolve_clone_ref(preset):
    """返回 (可用参考音频路径 | None, voices.json 里写的原始相对路径)。

    cloneRef 来自 voices.json，不能让它指到仓库外（绝对路径或 ../../）。
    """
    ref = str(preset.get("cloneRef", "") or "").strip()
    if not ref:
        return None, ""
    if os.path.isabs(ref):
        print(f"  ! cloneRef 不能用绝对路径，已忽略：{ref}", file=sys.stderr)
        return None, ref
    p = (SKILL_ROOT / ref).resolve()
    try:
        p.relative_to(SKILL_ROOT.resolve())
    except ValueError:
        print(f"  ! cloneRef 越界（跑出 skill 目录），已忽略：{ref}", file=sys.stderr)
        return None, ref
    return (p if p.is_file() else None), ref


def is_unverified_ref(path):
    """抖音参考目录下的音频视为「未登记授权」。"""
    try:
        path.resolve().relative_to(UNVERIFIED_REF_ROOT.resolve())
    except (ValueError, OSError):
        return False
    return True


def gate_clone(lines, consent, allow_unverified):
    """clone 引擎的前置闸门：没有授权确认就不合成，未登记授权的参考默认拒绝。"""
    if not consent:
        die(
            "clone 引擎需要先确认声音授权：\n"
            "  1) 确认参考音频的声音权利人已书面同意用于本片（自录 / 采购 / 数据集授权均可）；\n"
            "  2) 确认后加 --clone-consent 重跑。\n"
            "  没授权就用 --engine edge；不要克隆可识别的真人声音。"
        )

    unverified = {}
    for item in lines:
        path, raw = resolve_clone_ref(item["preset"])
        if path and is_unverified_ref(path):
            unverified.setdefault(raw, []).append(item["voice"])

    if not unverified:
        return

    print("⚠ 以下音色用的是未登记授权的抖音参考音频：", file=sys.stderr)
    for raw, voices in unverified.items():
        names = "、".join(sorted(set(voices)))
        print(f"    {raw}  ← {names}", file=sys.stderr)
    print("  这类参考只适合内部听感测试，对外发布前必须换成有授权的参考音频。", file=sys.stderr)

    if not allow_unverified:
        die(
            "已拦截：未登记授权的参考音频不允许用于克隆合成。\n"
            "  换成有授权的参考音频，或在确认仅做内部测试时加 --allow-unverified。"
        )
    print("  ! 已加 --allow-unverified，继续合成；产物不得对外发布。", file=sys.stderr)


def run_clone(lines, out_dir, alpha, overwrite=False, dry_run=False):
    if not MAKE_EMOTION.is_file():
        die(f"找不到 IndexTTS 入口：{MAKE_EMOTION}")
    wav_dir = out_dir / "_wav"
    if not dry_run:
        wav_dir.mkdir(parents=True, exist_ok=True)

    table = out_dir / "_clone_table.csv"
    with open(table, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["角色", "台词", "情绪", "强度", "语速", "音色参考", "输出"])
        for item in lines:
            emotion = EMOTION_ALIAS.get(item["emotion"], item["emotion"])
            ref = item["preset"].get("cloneRef", "")
            ref_path = ""
            if ref:
                resolved, _ = resolve_clone_ref(item["preset"])
                if resolved:
                    ref_path = str(resolved)
            if not ref_path and DEFAULT_CLONE.is_file():
                ref_path = str(DEFAULT_CLONE)
            w.writerow([
                item["speaker"], item["text"], emotion, str(alpha), "1.0",
                ref_path, f"S{item['seq']:03d}",
            ])

    print(f">> 调 IndexTTS：{MAKE_EMOTION}")
    print(f">> 标注表：{table}")
    if dry_run:
        r = run_cmd(
            [sys.executable, str(MAKE_EMOTION), "--table", str(table),
             "--outdir", str(wav_dir), "--dry-run"],
            capture_output=False,
        )
        return r.returncode
    print(">> 首次加载模型约 30 秒；之后每句 RTF 约 3–4（M1）")
    r = run_cmd(
        [sys.executable, str(MAKE_EMOTION), "--table", str(table),
         "--outdir", str(wav_dir), "--alpha", str(alpha)],
        capture_output=False,
    )
    if r.returncode != 0:
        die("IndexTTS 合成失败，看上面的报错")

    for item in lines:
        wav = wav_dir / f"S{item['seq']:03d}.wav"
        mp3 = out_dir / f"S{item['seq']:03d}.mp3"
        if not wav.is_file():
            print(f"  ! 缺 {wav.name}", file=sys.stderr)
            continue
        if mp3.exists() and not overwrite:
            continue
        rr = run_cmd(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav),
             "-codec:a", "libmp3lame", "-q:a", "2", str(mp3)]
        )
        if rr.returncode != 0:
            raise RuntimeError(f"ffmpeg 转 mp3 失败：{rr.stderr.strip()}")


def main():
    ap = argparse.ArgumentParser(description="沙雕配音批量合成")
    ap.add_argument("--project", required=True, help="剧名（99-项目 下的目录名）")
    ap.add_argument("--season", type=int, default=1)
    ap.add_argument("--episode", type=int, default=1)
    ap.add_argument("--engine", choices=["edge", "clone", "say"], default="edge")
    ap.add_argument("--script", help="剧本 JSON 路径（默认 01-剧本/剧本.json）")
    ap.add_argument("--outdir", help="输出目录（默认 02-配音/第NN集）")
    ap.add_argument("--alpha", type=float, default=0.6, help="IndexTTS 情绪强度（0.5–0.6 推荐）")
    ap.add_argument("--rate-boost", default="+0%", help="edge 全局语速加成，如 +18%（沙雕默认建议 +15%~+20%）")
    ap.add_argument("--only", help="只跑指定序号，逗号分隔，如 3,7,9")
    ap.add_argument("--force", action="store_true", help="覆盖已存在的音频")
    ap.add_argument(
        "--allow-voice-fallback",
        action="store_true",
        help="剧本里点名的音色查不到时，按性别兜底，而不是报错退出",
    )
    ap.add_argument("--dry-run", action="store_true", help="只打印计划，不合成")
    ap.add_argument(
        "--clone-consent",
        action="store_true",
        help="确认已获得参考音频声音权利人的授权（clone 引擎必需）",
    )
    ap.add_argument(
        "--allow-unverified",
        action="store_true",
        help="允许使用未登记授权的参考音频（抖音参考），仅限内部测试，产物不得发布",
    )
    args = ap.parse_args()

    sd = season_dir(args.project, args.season)
    if not sd.is_dir():
        die(f"季目录不存在：{sd}")
    script_path = Path(args.script) if args.script else sd / "01-剧本" / "剧本.json"
    if not script_path.is_file():
        die(f"找不到剧本 JSON：{script_path}\n先跑 01-剧本，产出 剧本.json")

    script = json.loads(script_path.read_text(encoding="utf-8-sig"))
    voices = load_voices()
    lines, used_voice = build_lines(script, voices, args.allow_voice_fallback)

    if args.only:
        wanted = {int(x.strip()) for x in args.only.split(",") if x.strip()}
        lines = [l for l in lines if l["seq"] in wanted]
        if not lines:
            die(f"--only {args.only} 没匹配到任何一行")

    # clone 是唯一有授权风险的引擎，闸门放在建目录之前
    if args.engine == "clone":
        sys.stdout.flush()
        gate_clone(lines, args.clone_consent, args.allow_unverified)

    out_dir = Path(args.outdir) if args.outdir else sd / "02-配音" / f"第{args.episode:02d}集"
    out_dir = out_dir.resolve()
    # 配音表里的 audio 字段是相对季目录写的，outdir 跑到季目录外会算不出相对路径
    try:
        out_dir.relative_to(sd.resolve())
    except ValueError:
        die(f"--outdir 必须在季目录内：{sd}\n  实际给了：{out_dir}")
    if not args.dry_run:
        out_dir.mkdir(parents=True, exist_ok=True)

    print(f">> 项目：{args.project} · 第{args.season:02d}季 · 第{args.episode:02d}集")
    print(f">> 剧本：{script_path}")
    print(f">> 引擎：{args.engine}")
    print(f">> 输出：{out_dir}")
    print(f">> 台词：{len(lines)} 行")
    print(">> 角色音色：")
    for role, v in used_voice.items():
        print(f"   - {role}: {v}")

    if args.dry_run:
        if args.engine == "clone":
            # 只打印计划：不建目录、不写 _clone_table.csv、不调 IndexTTS
            print(">> [dry-run] 不落盘；正式跑会写 _clone_table.csv 和 _wav/")
            for item in lines:
                print(f"   {item['seq']:>3} [{item['preset'].get('voice', '?')}] {item['emotion']}  {item['text']}")
            return 0
        for item in lines:
            print(f"   {item['seq']:>3} [{item['voice']}] {item['emotion']}  {item['text']}")
        return 0

    try:
        if args.engine == "edge":
            run_edge(lines, out_dir, overwrite=args.force, rate_boost=args.rate_boost)
        elif args.engine == "say":
            run_say(lines, out_dir, overwrite=args.force)
        else:
            run_clone(lines, out_dir, args.alpha, overwrite=args.force)
    except Exception as e:
        die(str(e))

    manifest_lines = []
    total_ms = 0
    missing = []
    for item in lines:
        mp3 = out_dir / f"S{item['seq']:03d}.mp3"
        if not mp3.is_file() or mp3.stat().st_size == 0:
            missing.append(item["seq"])
            duration = 0
        else:
            duration = probe_duration_ms(mp3)
        total_ms += duration

        if args.engine != "clone":
            license_tag, license_note = "ok", ""
        else:
            ref_path, raw_ref = resolve_clone_ref(item["preset"])
            if raw_ref and ref_path and is_unverified_ref(ref_path):
                license_tag = "unverified"
                license_note = "抖音参考未登记授权，对外发布前必须替换"
            elif raw_ref and ref_path:
                license_tag = "user-provided"
                license_note = "参考音频由使用者提供，发布前需自行确认授权"
            elif raw_ref:
                license_tag = "dataset"
                license_note = f"参考音频不存在（{raw_ref}），回落 aishell3 公开数据集音色"
            else:
                license_tag = "dataset"
                license_note = "未指定参考音频，回落 aishell3 公开数据集音色"

        manifest_lines.append({
            "seq": item["seq"],
            "speaker": item["speaker"],
            "type": item["type"],
            "text": item["text"],
            "emotion": item["emotion"],
            "sfx": item["sfx"],
            "scene": item["scene"],
            "sceneTitle": item["sceneTitle"],
            "voice": item["voice"],
            "audio": str((out_dir / f"S{item['seq']:03d}.mp3").relative_to(sd)),
            "duration": duration,
            "hash": item["hash"],
            "license": license_tag,
            "licenseNote": license_note,
        })

    manifest = {
        "project": args.project,
        "season": args.season,
        "episode": args.episode,
        "engine": args.engine,
        "generatedAt": datetime.now().isoformat(timespec="seconds"),
        "totalDuration": round(total_ms / 1000, 2),
        "lines": manifest_lines,
    }
    manifest_path = out_dir / "配音表.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print()
    print(f">> 完成：{len(lines) - len(missing)}/{len(lines)} 条；总时长 {manifest['totalDuration']}s")
    if missing:
        print(f"  ! 缺失：{missing}", file=sys.stderr)
        print(f"  ! 重跑：--only {','.join(map(str, missing))} --force", file=sys.stderr)
    print(f">> 配音表：{manifest_path}")

    target = script.get("durationTarget")
    if target and manifest["totalDuration"] > target * 1.25:
        print(f"  ! 配音 {manifest['totalDuration']}s 超过目标 {target}s 的 125%，建议删减台词", file=sys.stderr)
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
