"""
Video Merger 使用示例
"""
from src.video_merger import VideoMerger

def main():
    # 初始化视频拼接器
    merger = VideoMerger()

    try:
        # 基础用法：保持原始分辨率拼接
        print("=== 基础拼接示例 ===")
        merger.merge(
            input_dir="./segments",
            output_path="./output/basic_merge.mp4"
        )

        # 自定义参数示例
        print("\n=== 自定义参数拼接示例 ===")
        merger.merge(
            input_dir="./segments",
            output_path="./output/custom_merge.mp4",
            resolution="1080x1920",  # 输出1080P竖屏
            transition_duration=1.0,  # 1秒转场
            crf=18,  # 更高质量
            preset="slow"  # 更好的压缩率
        )

        # 批量处理多个目录示例
        print("\n=== 批量处理示例 ===")
        episodes = ["./ep1", "./ep2", "./ep3"]
        for i, episode_dir in enumerate(episodes, 1):
            output_path = f"./output/episode_{i}.mp4"
            print(f"正在处理第{i}集: {episode_dir}")
            merger.merge(
                input_dir=episode_dir,
                output_path=output_path
            )

    except Exception as e:
        print(f"处理失败: {str(e)}")

if __name__ == "__main__":
    main()
