#!/usr/bin/env python3
"""
心跳机制测试示例
"""
from client import CameraClient
import time

if __name__ == "__main__":
    client = CameraClient(base_url="http://localhost:27793")

    try:
        print("🎬 准备录制 5 秒的 MP4 视频...")

        # 便捷方法：录制指定时长的视频
        result = client.record_video(
            duration=5,              # 录制 5 秒
            task_name="my_video",    # 任务名称
            output_format="mp4"      # 输出格式为 MP4
        )

        print("✅ 录制完成！")
        print(f"   视频路径: {result['video_path']}")
        print(f"   文件大小: {result['file_size_bytes'] / 1024 / 1024:.2f} MB")
        print(f"   格式: {result['format']}")

    except Exception as e:
        print(f"❌ 录制失败: {e}")
    finally:
        client.session.close()