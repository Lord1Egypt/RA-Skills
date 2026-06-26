#!/usr/bin/env python3
"""
视频自动发布 Skill - ClawHub 格式
自动发布视频到 B站、抖音、小红书
"""

import sys
import os
import argparse
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from auto_publish import VideoPublisher, get_latest_video, generate_content, PLATFORMS
import logging
from datetime import datetime

# 配置日志
BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

log_file = LOG_DIR / f"skill_publish_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='自动发布视频到中国三大平台（B站、抖音、小红书）'
    )

    parser.add_argument(
        '--video',
        type=str,
        help='视频文件路径（可选，默认使用最新视频）'
    )

    parser.add_argument(
        '--title',
        type=str,
        help='视频标题（可选，默认自动生成）'
    )

    parser.add_argument(
        '--description',
        type=str,
        help='视频描述（可选，默认自动生成）'
    )

    parser.add_argument(
        '--tags',
        type=str,
        help='标签列表，逗号分隔（可选，默认自动生成）'
    )

    parser.add_argument(
        '--platforms',
        type=str,
        default='bilibili,douyin,xiaohongshu',
        help='目标平台，逗号分隔（默认: bilibili,douyin,xiaohongshu）'
    )

    parser.add_argument(
        '--headless',
        action='store_true',
        help='使用无头模式（默认: False）'
    )

    return parser.parse_args()


def main():
    """主函数"""
    args = parse_arguments()

    logging.info("=" * 60)
    logging.info("视频自动发布 Skill - ClawHub")
    logging.info("=" * 60)

    start_time = datetime.now()

    # 获取视频文件
    if args.video:
        video_path = Path(args.video)
        if not video_path.exists():
            logging.error(f"错误: 视频文件不存在: {video_path}")
            return False
    else:
        video_path = get_latest_video()
        if not video_path:
            logging.error("错误: 未找到视频文件")
            return False

    logging.info(f"\n找到视频: {video_path}")
    logging.info(f"文件大小: {video_path.stat().st_size / 1024 / 1024:.2f} MB")

    # 生成或使用提供的内容
    if args.title or args.description or args.tags:
        title = args.title or video_path.stem
        description = args.description or f"视频: {video_path.stem}"
        tags = args.tags.split(',') if args.tags else []
    else:
        title, description, tags = generate_content(video_path)

    logging.info(f"\n标题: {title}")
    logging.info(f"描述: {description[:100]}...")
    logging.info(f"标签: {', '.join(tags)}")

    # 解析目标平台
    target_platforms = [p.strip() for p in args.platforms.split(',')]

    # 验证平台名称
    invalid_platforms = [p for p in target_platforms if p not in PLATFORMS]
    if invalid_platforms:
        logging.error(f"错误: 无效的平台名称: {', '.join(invalid_platforms)}")
        logging.error(f"可用平台: {', '.join(PLATFORMS.keys())}")
        return False

    logging.info(f"\n目标平台: {', '.join([PLATFORMS[p]['name'] for p in target_platforms])}")

    # 按顺序发布到各平台
    results = {}
    for platform in target_platforms:
        logging.info(f"\n{'=' * 60}")
        logging.info(f"正在发布到 {PLATFORMS[platform]['name']}")
        logging.info(f"{'=' * 60}")

        try:
            with VideoPublisher(platform, headless=args.headless) as publisher:
                success = publisher.publish(video_path, title, description, tags)
                results[platform] = success

                if success:
                    logging.info(f"✅ {PLATFORMS[platform]['name']} 发布成功")
                else:
                    logging.warning(f"❌ {PLATFORMS[platform]['name']} 发布失败")

                # 平台之间等待一段时间
                if platform != target_platforms[-1]:
                    logging.info(f"\n等待 10 秒后继续下一个平台...")
                    import time
                    time.sleep(10)

        except Exception as e:
            logging.error(f"❌ {PLATFORMS[platform]['name']} 发布出错: {e}", exc_info=True)
            results[platform] = False
            import time
            time.sleep(5)

    # 显示结果
    logging.info("\n" + "=" * 60)
    logging.info("发布结果汇总")
    logging.info("=" * 60)
    for platform in target_platforms:
        status = "✅ 成功" if results.get(platform, False) else "❌ 失败"
        logging.info(f"{PLATFORMS[platform]['name']}: {status}")

    # 统计
    success_count = sum(1 for v in results.values() if v)
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    logging.info(f"\n总计: {success_count}/{len(target_platforms)} 个平台发布成功")
    logging.info(f"总耗时: {duration:.1f} 秒")
    logging.info(f"日志文件: {log_file}")

    return success_count > 0


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logging.info("\n用户中断")
        sys.exit(1)
    except Exception as e:
        logging.error(f"程序异常退出: {e}", exc_info=True)
        sys.exit(1)
