#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
火山引擎豆包语音播客生成器
基于 PodcastTTS API，输入主题文本自动生成双人对话播客音频。
"""

import asyncio
import json
import logging
import math
import os
import struct
import sys
import time
import uuid
from pathlib import Path
from typing import Optional

import websockets

# 加载 protocols
sys.path.insert(0, str(Path(__file__).parent))
from protocols import (
    EventType,
    MsgType,
    finish_connection,
    finish_session,
    receive_message,
    start_connection,
    start_session,
    wait_for_event,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("PodcastTTS")

ENDPOINT = "wss://openspeech.bytedance.com/api/v3/sami/podcasttts"
DEFAULT_RESOURCE_ID = "volc.service_type.10050"
DEFAULT_ENCODING = "mp3"
DEFAULT_SAMPLE_RATE = 24000


class PodcastError(Exception):
    """播客生成错误基类"""
    def __init__(self, message: str, error_code: Optional[str] = None, details: Optional[dict] = None):
        super().__init__(message)
        self.error_code = error_code
        self.details = details or {}


class AuthenticationError(PodcastError):
    """认证错误"""
    pass


class RateLimitError(PodcastError):
    """速率限制错误"""
    pass


class ContentSafetyError(PodcastError):
    """内容安全错误"""
    pass


class AudioProcessor:
    """音频后处理器"""

    @staticmethod
    def normalize_pcm(audio_bytes: bytearray, sample_rate: int = 24000, bits: int = 16) -> bytearray:
        """PCM 音量归一化到 -1dB peak"""
        if bits == 16:
            fmt = "<h"
            max_val = 32767
        elif bits == 24:
            # 24-bit 需要特殊处理
            return audio_bytes
        else:
            return audio_bytes

        samples = []
        peak = 0
        for i in range(0, len(audio_bytes), 2):
            if i + 1 < len(audio_bytes):
                val = struct.unpack(fmt, audio_bytes[i:i+2])[0]
                samples.append(val)
                peak = max(peak, abs(val))

        if peak == 0:
            return audio_bytes

        # 归一化到 -1dB (约 0.8913)
        target_peak = int(max_val * 0.8913)
        gain = target_peak / peak

        normalized = bytearray()
        for val in samples:
            new_val = int(val * gain)
            new_val = max(-max_val, min(max_val, new_val))
            normalized.extend(struct.pack(fmt, new_val))

        return normalized

    @staticmethod
    def fade_in_out_pcm(audio_bytes: bytearray, sample_rate: int = 24000, fade_ms: int = 500, bits: int = 16) -> bytearray:
        """添加淡入淡出效果"""
        if bits != 16:
            return audio_bytes

        fmt = "<h"
        samples = []
        for i in range(0, len(audio_bytes), 2):
            if i + 1 < len(audio_bytes):
                samples.append(struct.unpack(fmt, audio_bytes[i:i+2])[0])

        fade_samples = int(sample_rate * fade_ms / 1000)
        total = len(samples)

        # 淡入
        for i in range(min(fade_samples, total)):
            samples[i] = int(samples[i] * (i / fade_samples))

        # 淡出
        for i in range(max(0, total - fade_samples), total):
            samples[i] = int(samples[i] * ((total - i) / fade_samples))

        result = bytearray()
        for val in samples:
            result.extend(struct.pack(fmt, val))
        return result

    @staticmethod
    def process_mp3(audio_bytes: bytearray, normalize: bool = False, fade: bool = False) -> bytearray:
        """处理 MP3 音频（需要 pydub）"""
        try:
            from pydub import AudioSegment
            audio = AudioSegment(data=bytes(audio_bytes))

            if normalize:
                # 归一化到 -1dB
                peak = audio.max_dBFS
                if peak < 0:
                    audio = audio.apply_gain(-1.0 - peak)

            if fade:
                audio = audio.fade_in(500).fade_out(500)

            # 导出
            import io
            buf = io.BytesIO()
            audio.export(buf, format="mp3")
            return bytearray(buf.getvalue())
        except ImportError:
            logger.warning("pydub 未安装，跳过 MP3 后处理。安装: pip install pydub")
            return audio_bytes
        except Exception as e:
            logger.warning(f"MP3 后处理失败: {e}")
            return audio_bytes


class PodcastGenerator:
    """火山引擎播客语音合成客户端"""

    def __init__(
        self,
        appid: str,
        access_token: str,
        app_key: str = "aGjiRDfUWi",
        resource_id: str = DEFAULT_RESOURCE_ID,
        endpoint: str = ENDPOINT,
    ):
        self.appid = appid
        self.access_token = access_token
        self.app_key = app_key
        self.resource_id = resource_id
        self.endpoint = endpoint

    def _parse_error(self, error_msg: str) -> PodcastError:
        """解析错误信息，返回具体错误类型"""
        error_lower = error_msg.lower()

        if any(k in error_lower for k in ["auth", "unauthorized", "token", "access"]):
            return AuthenticationError(error_msg, "AUTH_ERROR")
        elif any(k in error_lower for k in ["rate limit", "too many", "throttle"]):
            return RateLimitError(error_msg, "RATE_LIMIT")
        elif any(k in error_lower for k in ["safety", "content", "harmful", "risk"]):
            return ContentSafetyError(error_msg, "SAFETY_ERROR")
        else:
            return PodcastError(error_msg, "UNKNOWN")

    async def generate(
        self,
        text: str,
        output_dir: str = "output",
        encoding: str = DEFAULT_ENCODING,
        use_head_music: bool = True,
        use_tail_music: bool = False,
        only_nlp_text: bool = False,
        return_audio_url: bool = False,
        speaker_info: dict = None,
        speech_rate: int = 0,
        skip_round_audio_save: bool = False,
        voice_type: Optional[str] = None,
        normalize_audio: bool = False,
        fade_in_out: bool = False,
    ) -> dict:
        """
        生成播客音频

        Args:
            text: 输入主题文本
            output_dir: 输出目录
            encoding: 音频格式 mp3 / wav / pcm
            use_head_music: 是否加片头音乐
            use_tail_music: 是否加片尾音乐
            only_nlp_text: 只返回文本不生成音频
            return_audio_url: 返回音频 URL 而非流式下发
            speaker_info: 说话人配置，如 {"random_order": false}
            speech_rate: 语速，默认 0
            skip_round_audio_save: 跳过分段保存
            voice_type: 音色类型: zh_male / zh_female / multi / None
            normalize_audio: 是否对音频进行音量归一化
            fade_in_out: 是否添加淡入淡出效果

        Returns:
            dict: 包含 output_files, duration, texts, usage 等信息
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        headers = {
            "X-Api-App-Id": self.appid,
            "X-Api-App-Key": self.app_key,
            "X-Api-Access-Key": self.access_token,
            "X-Api-Resource-Id": self.resource_id,
            "X-Api-Connect-Id": str(uuid.uuid4()),
        }

        req_params = {
            "input_id": f"podcast_{int(time.time())}",
            "input_text": text,
            "nlp_texts": None,
            "prompt_text": "",
            "action": 0,
            "use_head_music": use_head_music,
            "use_tail_music": use_tail_music,
            "input_info": {
                "input_url": "",
                "return_audio_url": return_audio_url,
                "only_nlp_text": only_nlp_text,
            },
            "speaker_info": speaker_info or {"random_order": False},
            "audio_config": {
                "format": encoding,
                "sample_rate": DEFAULT_SAMPLE_RATE,
                "speech_rate": speech_rate,
            }
        }

        # 添加音色类型配置
        if voice_type:
            valid_types = ["zh_male", "zh_female", "multi"]
            if voice_type not in valid_types:
                logger.warning(f"未知音色类型 {voice_type}，有效值: {valid_types}")
            else:
                req_params["voice_type"] = voice_type
                logger.info(f"使用音色类型: {voice_type}")

        is_podcast_round_end = True
        audio_received = False
        last_round_id = -1
        task_id = ""
        websocket = None
        retry_num = 5
        podcast_audio = bytearray()
        audio = bytearray()
        voice = ""
        current_round = 0
        podcast_texts = []
        output_files = []
        total_duration = 0.0
        usage_total = {"input_text_tokens": 0, "output_audio_tokens": 0, "total_tokens": 0}

        try:
            while retry_num > 0:
                logger.info(f"连接服务器: {self.endpoint}")
                websocket = await websockets.connect(
                    self.endpoint,
                    additional_headers=headers
                )
                logger.info("WebSocket 连接成功")

                if not is_podcast_round_end:
                    req_params["retry_info"] = {
                        "retry_task_id": task_id,
                        "last_finished_round_id": last_round_id
                    }

                await start_connection(websocket)
                await wait_for_event(websocket, MsgType.FullServerResponse, EventType.ConnectionStarted)

                session_id = str(uuid.uuid4())
                if not task_id:
                    task_id = session_id

                await start_session(websocket, json.dumps(req_params).encode(), session_id)
                await wait_for_event(websocket, MsgType.FullServerResponse, EventType.SessionStarted)
                await finish_session(websocket, session_id)

                while True:
                    msg = await receive_message(websocket)

                    if msg.type == MsgType.AudioOnlyServer and msg.event == EventType.PodcastRoundResponse:
                        if not audio_received and audio:
                            audio_received = True
                        audio.extend(msg.payload)
                        logger.debug(f"音频数据接收: {len(msg.payload)} 字节")

                    elif msg.type == MsgType.Error:
                        error_msg = msg.payload.decode() if msg.payload else "未知服务器错误"
                        error_obj = self._parse_error(error_msg)
                        if isinstance(error_obj, AuthenticationError):
                            logger.error(f"认证失败: {error_msg}")
                        elif isinstance(error_obj, RateLimitError):
                            logger.error(f"速率限制: {error_msg}")
                        elif isinstance(error_obj, ContentSafetyError):
                            logger.error(f"内容安全拦截: {error_msg}")
                        raise error_obj

                    elif msg.type == MsgType.FullServerResponse:
                        if msg.event == EventType.PodcastRoundStart:
                            data = json.loads(msg.payload.decode())
                            if data.get("text"):
                                filtered = {"text": data.get("text"), "speaker": data.get("speaker")}
                                podcast_texts.append(filtered)
                            voice = data.get("speaker", "")
                            current_round = data.get("round_id", -1)
                            if current_round == -1:
                                voice = "head_music"
                            if current_round == 9999:
                                voice = "tail_music"
                            is_podcast_round_end = False
                            logger.info(f"轮次开始 [{current_round}] {voice}: {data.get('text', '')[:50]}...")

                        elif msg.event == EventType.PodcastRoundEnd:
                            data = json.loads(msg.payload.decode())
                            if data.get("is_error"):
                                logger.error(f"轮次错误: {data}")
                                break
                            is_podcast_round_end = True
                            last_round_id = current_round
                            duration = data.get("audio_duration", 0)
                            total_duration += duration
                            if audio:
                                filename = f"{voice}_{current_round}.{encoding}"
                                filepath = output_path / filename
                                if not skip_round_audio_save:
                                    with open(filepath, "wb") as f:
                                        f.write(audio)
                                    output_files.append(str(filepath))
                                    logger.info(f"分段音频已保存: {filepath} ({duration:.2f}s)")
                                podcast_audio.extend(audio)
                                audio.clear()

                        elif msg.event == EventType.PodcastEnd:
                            data = json.loads(msg.payload.decode())
                            logger.info(f"播客全部生成完毕")

                        elif msg.event == EventType.UsageResponse:
                            data = json.loads(msg.payload.decode())
                            usage = data.get("usage", {})
                            for k in usage_total:
                                usage_total[k] += usage.get(k, 0)

                    if msg.event == EventType.SessionFinished:
                        break

                if not audio_received and not only_nlp_text:
                    raise RuntimeError("未收到任何音频数据")

                await finish_connection(websocket)
                await wait_for_event(websocket, MsgType.FullServerResponse, EventType.ConnectionFinished)

                if is_podcast_round_end:
                    final_files = []
                    if podcast_audio and not only_nlp_text:
                        # 音频后处理
                        if encoding == "pcm" and (normalize_audio or fade_in_out):
                            if normalize_audio:
                                podcast_audio = AudioProcessor.normalize_pcm(podcast_audio)
                                logger.info("PCM 音量归一化完成")
                            if fade_in_out:
                                podcast_audio = AudioProcessor.fade_in_out_pcm(podcast_audio)
                                logger.info("PCM 淡入淡出效果已添加")
                        elif encoding == "mp3" and (normalize_audio or fade_in_out):
                            podcast_audio = AudioProcessor.process_mp3(
                                podcast_audio, normalize=normalize_audio, fade=fade_in_out
                            )

                        final_name = f"podcast_final_{int(time.time())}.{encoding}"
                        final_path = output_path / final_name
                        with open(final_path, "wb") as f:
                            f.write(podcast_audio)
                        final_files.append(str(final_path))
                        logger.info(f"✅ 最终完整音频已保存: {final_path}")

                    if only_nlp_text and podcast_texts:
                        text_path = output_path / "podcast_texts.json"
                        with open(text_path, "w", encoding="utf-8") as f:
                            json.dump(podcast_texts, f, ensure_ascii=False, indent=2)
                        final_files.append(str(text_path))
                        logger.info(f"文本已保存: {text_path}")

                    return {
                        "success": True,
                        "output_dir": str(output_path.absolute()),
                        "segment_files": output_files,
                        "final_files": final_files,
                        "duration": round(total_duration, 2),
                        "texts": podcast_texts,
                        "usage": usage_total,
                    }
                else:
                    logger.warning(f"播客未完成，从轮次 {last_round_id} 继续重试...")
                    retry_num -= 1
                    await asyncio.sleep(1)
                    if websocket:
                        await websocket.close()
        finally:
            if websocket:
                await websocket.close()

        return {"success": False, "error": "重试次数耗尽，播客生成失败"}


async def main():
    import argparse

    parser = argparse.ArgumentParser(description="火山引擎豆包语音播客生成器")
    parser.add_argument("text", help="输入主题文本")
    parser.add_argument("-o", "--output", default="output", help="输出目录 (默认: output)")
    parser.add_argument("-f", "--format", default="mp3", choices=["mp3", "wav", "pcm"], help="音频格式")
    parser.add_argument("--no-head-music", action="store_true", help="不加片头音乐")
    parser.add_argument("--tail-music", action="store_true", help="加片尾音乐")
    parser.add_argument("--only-text", action="store_true", help="只生成文本不生成音频")
    parser.add_argument("--voice-type", choices=["zh_male", "zh_female", "multi"], help="音色类型")
    parser.add_argument("--normalize", action="store_true", help="音量归一化")
    parser.add_argument("--fade", action="store_true", help="淡入淡出效果")
    parser.add_argument("--appid", default=os.getenv("VOLC_APPID"), help="App ID (或环境变量 VOLC_APPID)")
    parser.add_argument("--token", default=os.getenv("VOLC_ACCESS_TOKEN"), help="Access Token (或环境变量 VOLC_ACCESS_TOKEN)")
    parser.add_argument("--app-key", default=os.getenv("VOLC_APP_KEY", "aGjiRDfUWi"), help="App Key")
    parser.add_argument("-v", "--verbose", action="store_true", help="详细日志")

    args = parser.parse_args()

    if not args.appid or not args.token:
        print("错误: 必须提供 --appid 和 --token，或通过环境变量 VOLC_APPID / VOLC_ACCESS_TOKEN 设置")
        sys.exit(1)

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    gen = PodcastGenerator(
        appid=args.appid,
        access_token=args.token,
        app_key=args.app_key,
    )

    result = await gen.generate(
        text=args.text,
        output_dir=args.output,
        encoding=args.format,
        use_head_music=not args.no_head_music,
        use_tail_music=args.tail_music,
        only_nlp_text=args.only_text,
        voice_type=args.voice_type,
        normalize_audio=args.normalize,
        fade_in_out=args.fade,
    )

    if result["success"]:
        print(f"\n✅ 播客生成成功！")
        print(f"   时长: {result['duration']} 秒")
        print(f"   输出目录: {result['output_dir']}")
        print(f"   最终文件: {', '.join(result['final_files'])}")
        print(f"   Token 消耗: {result['usage']}")
    else:
        print(f"\n❌ 生成失败: {result.get('error', '未知错误')}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
