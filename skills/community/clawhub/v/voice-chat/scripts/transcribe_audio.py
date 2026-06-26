#!/usr/bin/env python3
"""
音频转写模块：支持 Sherpa-ONNX（首选）和 Vosk（备份）双引擎。
支持格式：OGG/Opus, WAV, MP3 等 (需 ffmpeg 支持)
模型：
- Sherpa-ONNX: sherpa-onnx-sense-voice-zh-en-ja-ko-small-with-hotwords (中英文混合，int8 量化)
- Vosk: vosk-model-small-cn-0.22 (中文小模型，备份方案)
"""

import argparse
import json
import logging
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional

from utils import ensure_file

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 配置
TEMP_DIR = os.path.join("/tmp", "voice-chat")
os.makedirs(TEMP_DIR, exist_ok=True)

from config import get_settings
_settings = get_settings()
STT_ENGINE = _settings.STT_ENGINE
SHERPA_MODEL_DIR = _settings.SHERPA_MODEL_DIR
SHERPA_MODEL_NAME = _settings.SHERPA_MODEL_NAME
SHERPA_NUM_THREADS = _settings.SHERPA_NUM_THREADS
VENV_PY = _settings.VOSK_PYTHON
VOSK_MODEL_DIR = _settings.VOSK_MODEL_DIR
TEMP_WAV_PREFIX = 'transcribe_'
TEMP_WAV_SUFFIX = '.wav'


class TranscriptionError(Exception):
    """转写过程中的自定义异常"""
    pass


def transcribe_with_sherpa(src_audio: str) -> str:
    """
    使用 Sherpa-ONNX 模型转写音频（首选引擎）。

    Args:
        src_audio: 输入音频文件路径

    Returns:
        转写后的文本内容

    Raises:
        TranscriptionError: Sherpa-ONNX 转写失败
    """
    try:
        import sherpa_onnx

        logger.info(f"使用 Sherpa-ONNX 转写音频：{src_audio}")

        # 模型路径
        model_dir = os.path.join(SHERPA_MODEL_DIR, SHERPA_MODEL_NAME)
        model_path = os.path.join(model_dir, "model.onnx")
        tokens_path = os.path.join(model_dir, "tokens.txt")

        # 检查模型文件
        if not os.path.exists(model_path):
            raise TranscriptionError(
                f"模型文件不存在：{model_path}\n"
                f"请下载模型：\n"
                f"wget https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17.tar.bz2\n"
                f"tar -xjf sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17.tar.bz2 -C {SHERPA_MODEL_DIR}"
            )
        if not os.path.exists(tokens_path):
            raise TranscriptionError(f"Token 文件不存在：{tokens_path}")

        # 初始化识别器
        recognizer = sherpa_onnx.OfflineRecognizer.from_sense_voice(
            model=model_path,
            tokens=tokens_path,
            num_threads=SHERPA_NUM_THREADS,
            language="auto",  # 自动检测语言
            use_itn=False,  # 先关闭 ITN 测试
        )

        # 先使用 ffmpeg 转换为 16kHz 单声道 WAV
        with tempfile.NamedTemporaryFile(
            suffix=TEMP_WAV_SUFFIX,
            prefix=TEMP_WAV_PREFIX,
            dir=TEMP_DIR,
            delete=False
        ) as tmp_wav:
            wav_path = tmp_wav.name

        try:
            # 转换音频格式
            ffmpeg_cmd = [
                'ffmpeg', '-y',
                '-i', str(src_audio),
                '-ar', '16000',
                '-ac', '1',
                '-f', 'wav',
                wav_path
            ]
            subprocess.run(
                ffmpeg_cmd,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                timeout=60
            )

            # 使用 numpy 正确读取并归一化音频数据
            import numpy as np
            with open(wav_path, 'rb') as f:
                # 跳过 WAV 头，读取 PCM 数据
                import wave
                wf = wave.open(f, 'rb')
                sample_rate = wf.getframerate()
                raw_bytes = wf.readframes(wf.getnframes())
                wf.close()

                # 关键：转为 float32 且缩放到 [-1, 1] 之间
                samples = np.frombuffer(raw_bytes, dtype=np.int16).astype(np.float32) / 32768.0

            # 创建流并识别
            stream = recognizer.create_stream()
            stream.accept_waveform(sample_rate, samples)
            recognizer.decode_stream(stream)

            result_text = stream.result.text
            logger.info(f"Sherpa-ONNX 转写完成：{result_text}")
            return result_text
        finally:
            # 清理临时 WAV 文件
            if os.path.exists(wav_path):
                try:
                    os.remove(wav_path)
                except OSError:
                    pass

    except ImportError as e:
        logger.error(f"Sherpa-ONNX 依赖未安装：{e}")
        raise TranscriptionError(f"Sherpa-ONNX 依赖未安装，请运行：pip install sherpa-onnx")
    except Exception as e:
        logger.error(f"Sherpa-ONNX 转写失败：{e}")
        raise TranscriptionError(f"Sherpa-ONNX 转写失败：{e}")


def transcribe_with_vosk(src_audio: str) -> str:
    """
    使用 Vosk 模型转写音频（备份引擎）。

    Args:
        src_audio: 输入音频文件路径

    Returns:
        转写后的文本内容

    Raises:
        TranscriptionError: Vosk 转写失败
    """
    if not os.path.isdir(VOSK_MODEL_DIR):
        raise RuntimeError(f"Vosk 模型目录不存在：{VOSK_MODEL_DIR}")

    logger.info(f"使用 Vosk 转写音频：{src_audio}")

    # 创建临时 WAV 文件
    with tempfile.NamedTemporaryFile(
        suffix=TEMP_WAV_SUFFIX,
        prefix=TEMP_WAV_PREFIX,
        dir=TEMP_DIR,
        delete=False
    ) as tmp_wav:
        wav_path = tmp_wav.name

    try:
        # 使用 ffmpeg 转换为 16kHz 单声道 WAV (Vosk 要求格式)
        logger.info("正在转换音频格式...")
        ffmpeg_cmd = [
            'ffmpeg', '-y',
            '-i', str(src_audio),
            '-ar', '16000',
            '-ac', '1',
            '-f', 'wav',
            wav_path
        ]
        result = subprocess.run(
            ffmpeg_cmd,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            timeout=60
        )

        if not os.path.exists(wav_path) or os.path.getsize(wav_path) == 0:
            raise TranscriptionError("ffmpeg 转换生成的 WAV 文件为空")

        logger.info("音频格式转换完成，开始 Vosk 转写...")

        # 执行 Vosk 转写
        code = f'''
import json
import wave
from vosk import Model, KaldiRecognizer

wav_path = {repr(wav_path)}
model_dir = {repr(VOSK_MODEL_DIR)}

wf = wave.open(wav_path, 'rb')
model = Model(model_dir)
rec = KaldiRecognizer(model, wf.getframerate())

texts = []
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())
        text = result.get('text', '')
        if text:
            texts.append(text)

# 处理最终结果
final_result = json.loads(rec.FinalResult())
final_text = final_result.get('text', '')
if final_text:
    texts.append(final_text)

print(' '.join(texts).strip())
'''
        output = subprocess.check_output(
            [VENV_PY, '-c', code],
            text=True,
            timeout=120,
            stderr=subprocess.PIPE
        )
        result_text = output.strip()
        logger.info(f"Vosk 转写完成：{result_text}")
        return result_text

    except subprocess.TimeoutExpired:
        logger.error("Vosk 转写过程超时")
        raise TranscriptionError("Vosk 转写过程超时")
    except subprocess.CalledProcessError as e:
        # Python 3.13+ 中 stderr 已经是 str，不需要 decode
        stderr_msg = e.stderr if isinstance(e.stderr, str) else e.stderr.decode('utf-8', errors='ignore') if e.stderr else '未知错误'
        logger.error(f"Vosk 转写失败：{stderr_msg}")
        raise TranscriptionError(f"Vosk 转写失败：{stderr_msg}")
    finally:
        # 清理临时 WAV 文件
        if os.path.exists(wav_path):
            try:
                os.remove(wav_path)
                logger.debug(f"已清理临时文件：{wav_path}")
            except OSError as e:
                logger.warning(f"无法删除临时文件 {wav_path}: {e}")


def transcribe(src_audio: str, engine: Optional[str] = None) -> str:
    """
    将音频文件转写为文本（支持双引擎 fallback）。

    Args:
        src_audio: 输入音频文件路径 (支持 ogg, opus, wav, mp3 等)
        engine: 指定引擎 ("sherpa", "vosk", "auto")，默认为配置值

    Returns:
        转写后的文本内容

    Raises:
        FileNotFoundError: 音频文件不存在
        TranscriptionError: 所有引擎均失败

    Example:
        >>> text = transcribe('/tmp/audio.ogg')
        >>> print(text)
        '你好，这是一个测试'
    """
    src_audio = ensure_file(src_audio)

    if shutil.which('ffmpeg') is None:
        raise TranscriptionError("ffmpeg 未安装或不在 PATH 中")

    # 确定使用的引擎
    engine = engine or STT_ENGINE

    logger.info(f"开始转写音频：{src_audio}")
    logger.info(f"使用引擎策略：{engine}")

    # 策略 1: 仅使用 Sherpa-ONNX
    if engine == "sherpa":
        try:
            return transcribe_with_sherpa(src_audio)
        except Exception as e:
            logger.error(f"Sherpa-ONNX 转写失败：{e}")
            raise TranscriptionError(f"Sherpa-ONNX 转写失败：{e}")

    # 策略 2: 仅使用 Vosk
    elif engine == "vosk":
        try:
            return transcribe_with_vosk(src_audio)
        except Exception as e:
            logger.error(f"Vosk 转写失败：{e}")
            raise TranscriptionError(f"Vosk 转写失败：{e}")

    # 策略 3: 自动 fallback（Sherpa-ONNX 失败时切换 Vosk）
    elif engine == "auto":
        # 首选 Sherpa-ONNX
        try:
            logger.info("尝试使用 Sherpa-ONNX...")
            return transcribe_with_sherpa(src_audio)
        except Exception as e:
            logger.warning(f"Sherpa-ONNX 失败，切换到 Vosk：{e}")
            try:
                return transcribe_with_vosk(src_audio)
            except Exception as e2:
                logger.error(f"Vosk 也失败了：{e2}")
                raise TranscriptionError(f"所有引擎均失败：Sherpa-ONNX({e}), Vosk({e2})")

    else:
        raise TranscriptionError(f"未知的引擎策略：{engine}")


def main():
    """命令行入口点"""
    parser = argparse.ArgumentParser(description='将音频文件转写为文本（支持 Sherpa-ONNX 和 Vosk 双引擎）')
    parser.add_argument('audio_file', help='输入音频文件路径')
    parser.add_argument(
        '--engine', '-e',
        choices=['sherpa', 'vosk', 'auto'],
        default=None,
        help='指定转写引擎（默认：auto，即 Sherpa-ONNX 失败时自动切换 Vosk）'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='显示详细日志'
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        transcript = transcribe(args.audio_file, engine=args.engine)
        if transcript:
            print(transcript)
            sys.exit(0)
        else:
            logger.error("转写结果为空")
            print('ERROR: 转写结果为空', file=sys.stderr)
            sys.exit(2)
    except FileNotFoundError as e:
        logger.error(f"文件未找到：{e}")
        print(f'ERROR: {e}', file=sys.stderr)
        sys.exit(1)
    except TranscriptionError as e:
        logger.error(f"转写错误：{e}")
        print(f'ERROR: {e}', file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        logger.exception(f"未预期的错误：{e}")
        print(f'ERROR: 未预期的错误 - {e}', file=sys.stderr)
        sys.exit(3)


if __name__ == '__main__':
    main()
