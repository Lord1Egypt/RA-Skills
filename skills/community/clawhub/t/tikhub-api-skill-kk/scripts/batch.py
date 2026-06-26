"""
TikHub 批量任务脚本

用法:
  python batch.py download --aweme-ids 7618502770185833766,7618502770185833767
  python batch.py comments --aweme-id 7618502770185833766 --max 100
  python batch.py pipeline --urls urls.txt
  python batch.py balance
"""

import argparse
import json
import time
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from tikhub import (
    download_video,
    batch_download,
    get_video_info,
    get_all_comments,
    get_user_videos,
    full_pipeline_douyin_to_text,
    check_balance,
    set_api_key,
)


def read_urls(path: str) -> list:
    with open(path) as f:
        return [line.strip() for line in f if line.strip()]


def main():
    parser = argparse.ArgumentParser(description="TikHub 批量任务")
    parser.add_argument("--api-key", help="API Key（也可在代码中设置）")
    parser.add_argument("--mode", required=True,
                        choices=["download", "comments", "user-videos", "pipeline", "balance"],
                        help="任务模式")
    parser.add_argument("--aweme-ids", help="aweme_id 列表，逗号分隔")
    parser.add_argument("--aweme-id", help="单个 aweme_id")
    parser.add_argument("--urls", help="URL 列表文件路径（pipeline 模式用）")
    parser.add_argument("--unique-id", help="抖音号（查用户视频用）")
    parser.add_argument("--output-dir", default="./downloads", help="输出目录")
    parser.add_argument("--max", type=int, default=50, help="最大数量")
    parser.add_argument("--delay", type=float, default=2.0, help="请求间隔（秒）")
    parser.add_argument("--use-gpu", action="store_true", help="转写时使用 Apple GPU（mlx-whisper，默认开启）")
    parser.add_argument("--no-gpu", action="store_true", help="禁用 GPU，使用 CPU 转写（慢）")
    args = parser.parse_args()

    # API Key 设置
    if args.api_key:
        set_api_key(args.api_key)

    if args.mode == "balance":
        print("=== 查询余额 ===")
        info = check_balance()
        balance = info.get("user_data", {}).get("balance", "?")
        free = info.get("user_data", {}).get("free_credit", "?")
        print(f"余额: ${balance}")
        print(f"免费额度: ${free}")

    elif args.mode == "download":
        ids = args.aweme_ids.split(",") if args.aweme_ids else []
        if not ids:
            print("❌ 需要 --aweme-ids 参数")
            return
        print(f"📥 批量下载 {len(ids)} 个视频...")
        results = batch_download(ids, output_dir=args.output_dir, delay=args.delay)
        success = len([r for r in results if r["status"] == "success"])
        print(f"\n✅ 完成: {success}/{len(ids)}")

    elif args.mode == "comments":
        if not args.aweme_id:
            print("❌ 需要 --aweme-id 参数")
            return
        print(f"📝 采集评论: {args.aweme_id}")
        comments = get_all_comments(args.aweme_id, max_count=args.max)
        out_file = f"comments_{args.aweme_id}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(comments, f, ensure_ascii=False, indent=2)
        print(f"✅ 采集 {len(comments)} 条评论，保存到 {out_file}")

    elif args.mode == "user-videos":
        if not args.unique_id:
            print("❌ 需要 --unique-id 参数（抖音号）")
            return
        print(f"👤 获取用户视频列表: {args.unique_id}")
        data = get_user_videos(args.unique_id, max_count=args.max)
        out_file = f"user_videos_{args.unique_id}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ 保存到 {out_file}")

    elif args.mode == "pipeline":
        if not args.urls:
            print("❌ 需要 --urls 参数指定 URL 文件")
            return

        # GPU 逻辑：默认开启，--no-gpu 可禁用
        use_gpu = not args.no_gpu

        urls = read_urls(args.urls)
        # 从 URL 解析 aweme_id
        # 支持: https://v.douyin.com/xxx (短链) / https://www.douyin.com/video/xxx (长链接)
        aweme_ids = []
        for url in urls:
            from tikhub import parse_aweme_id
            aid = parse_aweme_id(url)
            # 短链无法直接解析，尝试用 API 解析
            if aid.startswith("https://v.douyin.com") or "v.douyin.com" in aid:
                from tikhub import get_video_info_by_url
                try:
                    info = get_video_info_by_url(url)
                    aid = info.get("data", {}).get("aweme_detail", {}).get("aweme_id", "")
                    print(f"  🔗 短链接解析: {url} → {aid}")
                except Exception as e:
                    print(f"  ⚠️ 短链接解析失败: {url}，跳过 ({e})")
                    continue
            aweme_ids.append(aid)

        print(f"🚀 完整 pipeline（下载→音频→转写）共 {len(aweme_ids)} 个...")
        if use_gpu:
            print("🎮 使用 mlx-whisper（Apple GPU 加速）")
        else:
            print("🔧 使用 openai-whisper（CPU）")

        results = []
        for i, aid in enumerate(aweme_ids):
            print(f"\n[{i+1}/{len(aweme_ids)}] 处理: {aid}")
            try:
                result = full_pipeline_douyin_to_text(
                    aid,
                    output_dir=args.output_dir,
                    use_gpu=use_gpu,
                    whisper_model="small"
                )
                if use_gpu:
                    # GPU 模式返回文字内容
                    text_path = result
                    results.append({"aweme_id": aid, "status": "success", "text_length": len(result), "path": text_path})
                    print(f"  ✅ {len(result)}字")
                else:
                    # CPU 模式返回路径（后台运行）
                    results.append({"aweme_id": aid, "status": "success", "path": result})
                    print(f"  ✅ 文字稿路径: {result}")
            except Exception as e:
                print(f"  ❌ 失败: {e}")
                results.append({"aweme_id": aid, "status": "error", "error": str(e)})
            time.sleep(args.delay)

        out_file = "pipeline_results.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        success = len([r for r in results if r["status"] == "success"])
        print(f"\n✅ 完成: {success}/{len(aweme_ids)}，结果保存到 {out_file}")
        if not use_gpu:
            print("💡 注意：Whisper 转写在后台运行，可通过 tail -f /tmp/whisper_*.log 查看进度")


if __name__ == "__main__":
    main()
