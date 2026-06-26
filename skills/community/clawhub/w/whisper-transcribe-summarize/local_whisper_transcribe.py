import argparse
import os

import whisper


def default_output_path(input_path: str) -> str:
    abs_path = os.path.abspath(os.path.expanduser(input_path))
    directory = os.path.dirname(abs_path)
    stem = os.path.splitext(os.path.basename(abs_path))[0]
    return os.path.join(directory, f"{stem}_whisper.txt")


def detect_device(requested_device: str) -> str:
    if requested_device != "auto":
        return requested_device

    try:
        import torch

        if torch.cuda.is_available():
            return "cuda"
    except Exception:
        pass

    return "cpu"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="使用本地 Whisper 转写本地音频或视频，默认输出为同目录下 *_whisper.txt",
    )
    parser.add_argument("media_path", help="本地音频或视频路径")
    parser.add_argument("--model", default="medium", help="模型名，如 tiny/base/small/medium/large")
    parser.add_argument("--output", default=None, help="输出 txt 路径")
    parser.add_argument("--language", default=None, help="语言代码，例如 zh、en；留空则自动识别")
    parser.add_argument("--task", default="transcribe", choices=["transcribe", "translate"], help="Whisper 任务类型")
    parser.add_argument("--device", default="auto", help="auto/cpu/cuda/mps")
    parser.add_argument("--download-dir", default=None, help="可选：指定 Whisper 模型下载目录")
    args = parser.parse_args()

    media_path = os.path.abspath(os.path.expanduser(args.media_path))
    if not os.path.isfile(media_path):
        raise SystemExit(f"找不到文件: {args.media_path}")

    output_path = args.output or default_output_path(media_path)
    device = detect_device(args.device)
    model = whisper.load_model(args.model, device=device, download_root=args.download_dir)

    transcribe_kwargs = {"task": args.task}
    if args.language:
        transcribe_kwargs["language"] = args.language
    if device != "cuda":
        transcribe_kwargs["fp16"] = False

    result = model.transcribe(media_path, **transcribe_kwargs)
    text = (result.get("text") or "").strip()

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text + ("\n" if text else ""))

    print("完成")
    print("模型:", args.model)
    print("设备:", device)
    print("输入:", media_path)
    print("文本输出:", output_path)


if __name__ == "__main__":
    main()
