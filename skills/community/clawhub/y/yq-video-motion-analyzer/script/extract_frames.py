import cv2
import os
import sys

def extract_frames(video_path, output_dir, interval=1):
    """
    从视频中提取关键帧

    Args:
        video_path: 视频文件路径
        output_dir: 输出目录
        interval: 提取间隔（秒）
    """
    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"无法打开视频文件: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * interval)

    frame_count = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            timestamp = frame_count / fps
            output_path = os.path.join(output_dir, f"frame_{saved_count:04d}_{timestamp:.2f}s.jpg")
            cv2.imwrite(output_path, frame)
            saved_count += 1

        frame_count += 1

    cap.release()
    return saved_count

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_frames.py <video_path> [output_dir] [interval]")
        sys.exit(1)

    video_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "output/frames"
    interval = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0

    try:
        count = extract_frames(video_path, output_dir, interval)
        print(f"成功提取 {count} 帧到 {output_dir}")
    except Exception as e:
        print(f"提取失败: {str(e)}")
        sys.exit(1)
