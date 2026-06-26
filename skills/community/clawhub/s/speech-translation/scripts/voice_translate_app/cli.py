import argparse
from pathlib import Path

from .config import AppConfig
from .pipeline import run_pipeline



def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audio -> Whisper -> Translate -> Piper")
    parser.add_argument("--input", required=True, help="输入音频文件路径")
    parser.add_argument("--output-dir", required=True, help="输出目录")
    parser.add_argument("--source-lang", required=True, help="源语言，例如 zh / en")
    parser.add_argument("--target-lang", required=True, help="目标语言，例如 en / zh")
    parser.add_argument("--whisper-model", default="small", help="faster-whisper 模型名")
    parser.add_argument(
        "--transcribe-backend",
        default="faster-whisper",
        choices=["faster-whisper", "mock"],
        help="转写后端：真实 faster-whisper 或 mock",
    )
    parser.add_argument("--piper-model", required=True, help="Piper onnx 模型路径")
    parser.add_argument(
        "--tts-backend",
        default="piper",
        choices=["piper", "mock"],
        help="TTS 后端：真实 piper 或 mock",
    )
    parser.add_argument(
        "--translation-backend",
        default="llm",
        choices=["llm", "manual", "service"],
        help="翻译后端：llm=由当前代理/大模型先产出译文文件，manual=手工/文件，service=HTTP 翻译服务",
    )
    parser.add_argument("--translation-file", help="人工翻译结果文件路径；提供后将跳过终端输入")
    parser.add_argument("--translation-service-url", help="翻译服务 URL，要求返回 JSON: {\"translation\": \"...\"}")
    parser.add_argument(
        "--no-interactive-translate",
        action="store_true",
        help="关闭终端人工翻译输入；需配合 --translation-file 或 service 后端使用",
    )
    parser.add_argument("--transcript-command", help="转写完成后发送消息的命令，文本走 stdin")
    parser.add_argument("--translation-command", help="翻译完成后发送消息的命令，文本走 stdin")
    parser.add_argument("--audio-command", help="音频完成后发送消息的命令，后接音频文件路径参数")
    parser.add_argument("--piper-binary", default="piper", help="Piper 可执行文件路径")
    parser.add_argument("--device", default="auto", help="Whisper 设备，例如 auto/cpu/cuda")
    parser.add_argument("--compute-type", default="default", help="Whisper compute type")
    return parser



def main() -> None:
    args = build_parser().parse_args()
    config = AppConfig(
        input_file=Path(args.input),
        output_dir=Path(args.output_dir),
        source_lang=args.source_lang,
        target_lang=args.target_lang,
        whisper_model=args.whisper_model,
        piper_model=Path(args.piper_model),
        transcribe_backend=args.transcribe_backend,
        tts_backend=args.tts_backend,
        translation_backend=args.translation_backend,
        translation_file=Path(args.translation_file) if args.translation_file else None,
        interactive_translate=not args.no_interactive_translate,
        translation_service_url=args.translation_service_url,
        transcript_command=args.transcript_command,
        translation_command=args.translation_command,
        audio_command=args.audio_command,
        piper_binary=args.piper_binary,
        device=args.device,
        compute_type=args.compute_type,
    )
    result = run_pipeline(config)
    print("Done")
    print(f"Transcript: {result.transcript_file}")
    print(f"Translation: {result.translation_file}")
    print(f"Audio: {result.audio_file}")
    print(f"Metadata: {result.metadata_file}")


if __name__ == "__main__":
    main()
