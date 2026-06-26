"""
按指定顺序自动发布视频：B站 → 抖音 → 快手 → 小红书
完全自动化，无需人工干预
"""

import sys
import os
import time
from pathlib import Path
from datetime import datetime

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from auto_publish import VideoPublisher, get_latest_video, generate_content, PLATFORMS

# 配置日志
import logging
BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

log_file = LOG_DIR / f"publish_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def main():
    logging.info("=" * 60)
    logging.info("视频自动发布工具 - 按顺序发布 (完全自动化)")
    logging.info("发布顺序: B站 → 抖音 → 小红书")
    logging.info("=" * 60)

    start_time = datetime.now()

    # 获取最新视频
    video_path = get_latest_video()
    if not video_path:
        logging.error("错误: 未找到视频文件")
        return False

    logging.info(f"\n找到视频: {video_path}")
    logging.info(f"文件大小: {video_path.stat().st_size / 1024 / 1024:.2f} MB")

    # 生成内容
    title, description, tags = generate_content(video_path)

    logging.info(f"\n标题: {title}")
    logging.info(f"描述: {description[:100]}...")
    logging.info(f"标签: {', '.join(tags)}")

    # 按指定顺序发布（去掉快手）
    platforms_order = ["bilibili", "douyin", "xiaohongshu"]

    results = {}
    for platform in platforms_order:
        logging.info(f"\n{'=' * 60}")
        logging.info(f"正在发布到 {PLATFORMS[platform]['name']}")
        logging.info(f"{'=' * 60}")

        try:
            with VideoPublisher(platform, headless=False) as publisher:  # B站使用非 headless 模式
                success = publisher.publish(video_path, title, description, tags)
                results[platform] = success

                if success:
                    logging.info(f"✅ {PLATFORMS[platform]['name']} 发布成功")
                else:
                    logging.warning(f"❌ {PLATFORMS[platform]['name']} 发布失败")

                # 平台之间等待一段时间，避免过快
                if platform != platforms_order[-1]:  # 不是最后一个平台
                    logging.info(f"\n等待 10 秒后继续下一个平台...")
                    time.sleep(10)

        except Exception as e:
            logging.error(f"❌ {PLATFORMS[platform]['name']} 发布出错: {e}", exc_info=True)
            results[platform] = False
            # 即使失败也继续下一个平台
            time.sleep(5)

    # 显示结果
    logging.info("\n" + "=" * 60)
    logging.info("发布结果汇总")
    logging.info("=" * 60)
    for platform in platforms_order:
        status = "✅ 成功" if results.get(platform, False) else "❌ 失败"
        logging.info(f"{PLATFORMS[platform]['name']}: {status}")

    # 统计
    success_count = sum(1 for v in results.values() if v)
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    logging.info(f"\n总计: {success_count}/{len(platforms_order)} 个平台发布成功")
    logging.info(f"总耗时: {duration:.1f} 秒")
    logging.info(f"日志文件: {log_file}")

    return success_count > 0


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        logging.error(f"程序异常退出: {e}", exc_info=True)
        sys.exit(1)
