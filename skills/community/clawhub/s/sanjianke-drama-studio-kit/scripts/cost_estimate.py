#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AI 短剧创作台 —— 存储、带宽与生成成本离线测算。

纯本地计算：不联网、不写文件。用于判断成本的量级与结构，
不用于精确预算。

脚本中的单价参数均为占位示例值，务必替换为当期真实报价。

示例：
    # 30 集，每集 2 分钟，完整测算
    python cost_estimate.py --episodes 30 --minutes 2

    # 只看存储与带宽，不计生成成本
    python cost_estimate.py --episodes 30 --minutes 2 \\
        --gen-image 0 --gen-video 0 --gen-tts 0

    # 缩短中间素材保存周期
    python cost_estimate.py --episodes 30 --minutes 2 --lifecycle-days 7
"""

import argparse
import sys


def build_parser():
    p = argparse.ArgumentParser(
        description='AI 短剧创作台 —— 成本量级离线测算（不联网）',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    g = p.add_argument_group('产出规模')
    g.add_argument('--episodes', type=int, default=30, help='集数')
    g.add_argument('--minutes', type=float, default=2.0, help='单集时长（分钟）')

    g = p.add_argument_group('画质与素材比例')
    g.add_argument('--quality', type=float, default=1.0,
                   help='画质系数，1.0 约等于 1080p / 4 Mbps')
    g.add_argument('--shoot-ratio', type=float, default=1.6,
                   help='实际生成量 / 最终采用量，用于计入废片')
    g.add_argument('--intermediate-ratio', type=float, default=2.0,
                   help='中间素材相对生成量的额外占比')

    g = p.add_argument_group('存储与带宽单价（占位示例值）')
    g.add_argument('--storage-per-gb', type=float, default=0.12,
                   help='对象存储单价（元 / GB / 月）')
    g.add_argument('--egress-per-gb', type=float, default=0.50,
                   help='回源带宽单价（元 / GB）')
    g.add_argument('--preview-count', type=float, default=3.0,
                   help='每集成片平均被完整回源 / 预览的次数')
    g.add_argument('--lifecycle-days', type=int, default=30,
                   help='中间素材保留天数，用于折算留存占用')

    g = p.add_argument_group('生成单价（占位示例值）')
    g.add_argument('--gen-image', type=float, default=40.0, help='每集图片生成次数')
    g.add_argument('--gen-video', type=float, default=30.0, help='每集视频生成次数')
    g.add_argument('--gen-tts', type=float, default=30.0, help='每集配音生成次数')
    g.add_argument('--image-unit', type=float, default=0.04, help='单张图片单价（元）')
    g.add_argument('--video-unit', type=float, default=2.00, help='单段视频单价（元）')
    g.add_argument('--tts-unit', type=float, default=0.01, help='单次配音单价（元）')

    return p


def main(argv=None):
    args = build_parser().parse_args(argv)

    # ---------- 基础换算 ----------
    base_bitrate_mbps = 4.0                       # 1080p 基准码率
    bitrate_mbps = base_bitrate_mbps * args.quality
    bitrate_mb_per_min = bitrate_mbps * 60 / 8    # Mbps -> MB/分钟

    total_minutes = args.episodes * args.minutes
    final_video_mb = total_minutes * bitrate_mb_per_min
    generated_video_mb = final_video_mb * args.shoot_ratio

    image_count = args.episodes * args.gen_image
    image_mb = image_count * 2.0                  # 每张约 2 MB
    audio_mb = total_minutes * 1.0                # 每分钟约 1 MB
    intermediate_mb = (generated_video_mb + image_mb) * args.intermediate_ratio

    peak_mb = (final_video_mb + generated_video_mb + image_mb
               + audio_mb + intermediate_mb)

    lifecycle_factor = min(1.0, args.lifecycle_days / 30.0)
    retained_mb = final_video_mb + (
        (generated_video_mb + image_mb + audio_mb + intermediate_mb)
        * lifecycle_factor)

    # ---------- 带宽 ----------
    # 只有已发布的成片会被反复回源；中间素材与废片不对外分发
    egress_gb = (final_video_mb * args.preview_count) / 1024

    # ---------- 生成成本 ----------
    image_cost = image_count * args.image_unit
    video_count = args.episodes * args.gen_video
    video_cost = video_count * args.video_unit
    tts_count = args.episodes * args.gen_tts
    tts_cost = tts_count * args.tts_unit
    gen_total = image_cost + video_cost + tts_cost

    # ---------- 平台成本 ----------
    storage_monthly = (retained_mb / 1024) * args.storage_per_gb
    egress_cost = egress_gb * args.egress_per_gb

    grand_total = gen_total + storage_monthly + egress_cost
    per_episode = grand_total / args.episodes if args.episodes else 0.0
    per_minute = grand_total / total_minutes if total_minutes else 0.0

    # ---------- 合理性校验 ----------
    warnings = []
    if args.episodes < 1:
        warnings.append('集数小于 1，结果无意义。请传 --episodes 至少为 1。')
    if args.minutes <= 0:
        warnings.append('单集时长非正数，结果无意义。请传 --minutes 大于 0。')
    if args.shoot_ratio < 1.0:
        warnings.append('拍摄比 {:.2f} 小于 1.0，意味着生成量少于采用量，'
                        '不符合实际。'.format(args.shoot_ratio))
    if args.lifecycle_days < 1:
        warnings.append('生命周期小于 1 天，中间素材将全部即时清除，'
                        '请确认是否符合预期。')
    if args.preview_count > 8:
        warnings.append('每集预览次数超过 8 次，回源流量将显著高于成片体积，'
                        '请确认是否符合预期。')
    if args.gen_video > 0 and args.video_unit <= 0:
        warnings.append('视频单价为 0，生成成本将被低估，请填入真实单价。')

    # ---------- 输出 ----------
    out = []
    w = out.append
    w('')
    w('========================================')
    w(' AI 短剧创作台 · 成本量级测算')
    w('========================================')
    w('')
    w('产出规模 : {} 集 / 每集 {} 分钟 / 共 {} 分钟'.format(
        args.episodes, args.minutes, total_minutes))
    w('画质系数 : {}  →  约 {:.1f} Mbps'.format(args.quality, bitrate_mbps))
    w('拍摄比   : {}  （含废片）'.format(args.shoot_ratio))
    w('')

    w('---- 素材体积 ----')
    w('成片        : {:>10,.1f} MB'.format(final_video_mb))
    w('生成片段    : {:>10,.1f} MB'.format(generated_video_mb))
    w('图片 ({:>4.0f} 张) : {:>10,.1f} MB'.format(image_count, image_mb))
    w('音频        : {:>10,.1f} MB'.format(audio_mb))
    w('中间素材    : {:>10,.1f} MB'.format(intermediate_mb))
    w('峰值占用    : {:>10,.2f} GB'.format(peak_mb / 1024))
    w('留存占用    : {:>10,.2f} GB   （生命周期 {} 天）'.format(
        retained_mb / 1024, args.lifecycle_days))
    w('')

    w('---- 平台成本 ----')
    w('对象存储    : {:>10,.2f} 元 / 月'.format(storage_monthly))
    w('回源带宽    : {:>10,.1f} GB  →  {:>8,.2f} 元'.format(
        egress_gb, egress_cost))
    w('平台小计    : {:>10,.2f} 元'.format(storage_monthly + egress_cost))
    w('')

    w('---- 生成成本 ----')
    w('图片 {:>4.0f} 次 : {:>10,.2f} 元'.format(image_count, image_cost))
    w('视频 {:>4.0f} 次 : {:>10,.2f} 元'.format(video_count, video_cost))
    w('配音 {:>4.0f} 次 : {:>10,.2f} 元'.format(tts_count, tts_cost))
    w('生成小计    : {:>10,.2f} 元'.format(gen_total))
    w('')

    w('---- 结论 ----')
    w('合计        : {:>10,.2f} 元'.format(grand_total))
    w('单集成本    : {:>10,.2f} 元'.format(per_episode))
    w('单分钟成本  : {:>10,.2f} 元'.format(per_minute))

    if grand_total > 0:
        w('')
        w('---- 结构占比 ----')
        w('视频生成    : {:>6.1f}%'.format(video_cost / grand_total * 100))
        w('图片生成    : {:>6.1f}%'.format(image_cost / grand_total * 100))
        w('配音生成    : {:>6.1f}%'.format(tts_cost / grand_total * 100))
        w('对象存储    : {:>6.1f}%'.format(storage_monthly / grand_total * 100))
        w('回源带宽    : {:>6.1f}%'.format(egress_cost / grand_total * 100))

    w('')
    w('----------------------------------------')
    w(' 提示：以上单价均为占位示例值，请替换为')
    w(' 当期真实报价后再采信结论。本测算未计')
    w(' 入重试、失败重跑与人工返工消耗。')
    w('----------------------------------------')

    if warnings:
        w('')
        w('---- 参数提醒 ----')
        for item in warnings:
            w('  · {}'.format(item))
    w('')

    sys.stdout.write('\n'.join(out))
    return 0


if __name__ == '__main__':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    sys.exit(main())
