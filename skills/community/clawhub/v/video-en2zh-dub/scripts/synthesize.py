#!/usr/bin/env python3
"""步骤 3：把中文字幕合成为配音，并按字幕时间轴落位。

用法：
    python scripts/synthesize.py                          # 默认 output.srt -> output.mp3
    python scripts/synthesize.py -i zh.srt -o配音.mp3
    python scripts/synthesize.py --rate "+15%"            # 语速加快 15%，缓解溢出
    python scripts/synthesize.py --sleep 10 --report      # 保守限速，并输出溢出报告

输出 MP3（192kbps），时长 = 最后一条字幕结束时间 + 500ms。
"""

from __future__ import annotations

import argparse
import asyncio
import os
import re
import shutil
import sys

DEFAULT_VOICE = "zh-CN-XiaoxiaoNeural"


def check_ffmpeg() -> None:
    if shutil.which("ffmpeg") is None:
        print("错误：未找到 ffmpeg。音频读取与导出依赖它，请先安装并加入 PATH。", file=sys.stderr)
        sys.exit(2)


def srt_time_to_ms(time_obj) -> int:
    return (time_obj.hours * 3600 + time_obj.minutes * 60 + time_obj.seconds) * 1000 + time_obj.milliseconds


def parse_srt(filepath: str) -> list[tuple[str, int, int]]:
    import pysrt

    segments: list[tuple[str, int, int]] = []
    for sub in pysrt.open(filepath, encoding="utf-8"):
        text = re.sub(r"<[^>]+>", "", sub.text.replace("\n", " ")).strip()
        if text:
            segments.append((text, srt_time_to_ms(sub.start), srt_time_to_ms(sub.end)))
    return segments


async def synth_one(text: str, voice: str, rate: str, dest: str, max_retry: int = 3) -> None:
    """合成单条。失败时按指数退避重试 —— 比固定 sleep 更省时间。"""
    import edge_tts

    kwargs = {}
    if rate and rate not in ("+0%", "0%"):
        kwargs["rate"] = rate

    for attempt in range(1, max_retry + 1):
        try:
            await edge_tts.Communicate(text, voice, **kwargs).save(dest)
            return
        except Exception as exc:  # noqa: BLE001 - 网络类错误需要重试
            if attempt == max_retry:
                raise
            wait = 2 ** attempt
            print(f"        第 {attempt} 次失败（{exc}），{wait}s 后重试...")
            await asyncio.sleep(wait)


async def main() -> int:
    parser = argparse.ArgumentParser(description="edge-tts 中文字幕转配音")
    parser.add_argument("-i", "--srt", default="output.srt", help="中文字幕（默认 output.srt）")
    parser.add_argument("-o", "--out", default="output.mp3", help="输出音频（默认 output.mp3）")
    parser.add_argument("--voice", default=DEFAULT_VOICE, help=f"音色（默认 {DEFAULT_VOICE}）")
    parser.add_argument("--rate", default="+0%", help='语速，如 "+15%"（默认 +0%%）')
    parser.add_argument("--bitrate", default="192k", help="导出码率（默认 192k）")
    parser.add_argument("--sleep", type=float, default=1.5,
                        help="每条之间的间隔秒数，用于规避限流（默认 1.5）")
    parser.add_argument("--temp-dir", default="temp_audio", help="临时片段目录（默认 temp_audio）")
    parser.add_argument("--keep-temp", action="store_true", help="保留临时片段目录")
    parser.add_argument("--limit", type=int, default=0, help="只处理前 N 条（0=全部，用于试跑）")
    parser.add_argument("--report", action="store_true", help="输出每条的时长溢出报告")
    args = parser.parse_args()

    check_ffmpeg()

    from pydub import AudioSegment  # 延迟导入，便于先给出清晰的错误提示

    if not os.path.exists(args.srt):
        print(f"错误：找不到字幕文件 {args.srt}。请先完成字幕翻译。", file=sys.stderr)
        return 2

    os.makedirs(args.temp_dir, exist_ok=True)

    segments = parse_srt(args.srt)
    if args.limit:
        segments = segments[: args.limit]
    total = len(segments)
    print(f"共解析到 {total} 条字幕")
    if total:
        est = total * (args.sleep + 1.2) / 60
        print(f"预计耗时 {est:.1f} 分钟（每条间隔 {args.sleep}s）")

    audio_segments: list[tuple] = []
    failed = 0

    for i, (text, start_ms, end_ms) in enumerate(segments):
        temp_file = os.path.join(args.temp_dir, f"seg_{i:04d}.mp3")
        print(f"  [{i + 1}/{total}] 合成: {text[:40]}...")
        try:
            await synth_one(text, args.voice, args.rate, temp_file)
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"        失败，跳过：{exc}")
            continue

        seg_audio = AudioSegment.from_mp3(temp_file)
        audio_segments.append((seg_audio, start_ms, end_ms))
        if args.report:
            slot = end_ms - start_ms
            ratio = len(seg_audio) / slot if slot else 0
            flag = "  <-- 溢出" if ratio > 1.1 else ""
            print(f"        语音 {len(seg_audio)}ms / 字幕槽 {slot}ms = {ratio:.2f}{flag}")

        if args.sleep and i < total - 1:
            await asyncio.sleep(args.sleep)

    if not audio_segments:
        print("错误：没有任何语音片段合成成功。多为网络或限流问题，请稍后重试。", file=sys.stderr)
        return 1

    last_end_ms = max(seg[2] for seg in audio_segments)
    total_duration_ms = last_end_ms + 500

    print(f"拼接音频，总时长 {total_duration_ms / 1000:.1f} 秒...")
    final_audio = AudioSegment.silent(duration=total_duration_ms)
    for seg_audio, start_ms, _ in audio_segments:
        final_audio = final_audio.overlay(seg_audio, position=start_ms)

    print(f"导出 {args.out} ...")
    final_audio.export(args.out, format="mp3", bitrate=args.bitrate)

    # 成功信息必须在清理之前打印：某些环境下清理临时目录会被安全策略拦截并终止进程，
    # 导致任务被误报为 failed —— 那只是清理失败，产物早已写盘。
    print(f"\n完成! 已生成 {args.out}")
    print(f"  音频时长: {len(final_audio) / 1000:.1f} 秒")
    print(f"  文件大小: {os.path.getsize(args.out) / 1024 / 1024:.1f} MB")
    print(f"  语音片段数: {len(audio_segments)} / {total}")
    if failed:
        print(f"  失败条数: {failed}（可对该部分单独重跑）")

    if args.report:
        ratios = sorted(
            len(a) / (e - s) for a, s, e in audio_segments if e > s
        )
        if ratios:
            mid = ratios[len(ratios) // 2]
            over = sum(1 for r in ratios if r > 1.1)
            print(f"  溢出统计: 中位占比 {mid:.2f}，超过 1.1 倍的 {over}/{len(ratios)} 条")
            if over > len(ratios) * 0.2:
                if args.rate in ("+0%", "0%", ""):
                    print('  提示：溢出偏多，建议加 --rate "+15%" 重新合成。')
                else:
                    print(f"  提示：已用 {args.rate} 加速但溢出仍偏多，")
                    print("        此时再加速会损伤音质，更有效的办法是")
                    print("        按 4.5 字/秒重做字幕翻译（见 references/sync-tuning.md）。")

    if not args.keep_temp:
        try:
            shutil.rmtree(args.temp_dir, ignore_errors=True)
        except Exception as exc:  # noqa: BLE001 - 清理失败绝不应影响产物
            print(f"  注意：清理 {args.temp_dir} 时出错（{exc}），可手动删除，不影响产物。")

    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
