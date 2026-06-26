#!/usr/bin/env python3
"""
腾讯云 MPS 语音合成与音色复刻脚本

功能：
  基于 AI 语音模型，支持声音复刻、语音合成能力，适用于有声书、播客、音视频创作等多种场景。
  支持中、英、日、韩等 40+ 语种，提供丰富的系统音色，音色复刻还原度高。

  运行模式（通过 --mode 指定）：

  ● clone        音色复刻（同步）
                 传入克隆音频，返回音色 ID（VoiceId）。
                 建议音频时长 10~20 秒，仅包含单人清晰语音。

  ● tts          短文本语音合成（同步）
                 传入文本 + 音色 ID，返回合成音频（WAV）。
                 文本不超过 2000 字符时使用同步接口；超过 2000 字符时自动切换为
                 异步接口（async-tts），无需手动指定。

  ● async-tts    长文本转语音（异步，TextToSpeech）
                 通过 ProcessMedia 接口提交异步任务，支持超长文本合成，输出音频到 COS。

  ● async-sts    语音转语音（异步，SpeechToSpeech）
                 通过 ProcessMedia 接口提交异步任务，对输入音视频进行音色替换，输出到 COS。

COS 存储约定：
  通过环境变量 TENCENTCLOUD_COS_BUCKET 指定 COS Bucket 名称。
  - 输出文件默认路径：{TENCENTCLOUD_COS_BUCKET}/output/dubbing/

用法：
  # 音色复刻（传入本地音频文件）
  python mps_dubbing.py --mode clone --audio-file /path/to/voice.wav

  # 音色复刻（传入音频 URL）
  python mps_dubbing.py --mode clone --audio-url https://example.com/voice.mp4

  # 短文本语音合成（指定音色 ID）
  python mps_dubbing.py --mode tts --text "您好，欢迎使用腾讯云语音合成" --voice-id s1_2GSzVAf00hl

  # 短文本语音合成（指定音色 ID，保存到文件）
  python mps_dubbing.py --mode tts --text "Hello, welcome!" --voice-id s1_xxx --output /tmp/output.wav

  # 音色复刻 + 语音合成（先用 clone 拿到 VoiceId，再用 tts 合成）
  python mps_dubbing.py --mode clone --audio-file /path/to/voice.wav
  python mps_dubbing.py --mode tts --text "您好" --voice-id <上一步返回的 VoiceId>

  # 长文本转语音（异步，指定音色 ID）
  python mps_dubbing.py --mode async-tts \\
      --text "这是一段很长的文本..." --voice-id clone_v1_Q03FBduA

  # 长文本转语音（异步，传入克隆视频 URL）
  python mps_dubbing.py --mode async-tts \\
      --text "这是一段很长的文本..." \\
      --clone-video-url https://example.com/train.mp4

  # 语音转语音（异步，替换音色）
  python mps_dubbing.py --mode async-sts \\
      --url https://example.com/video.mp4 \\
      --clone-video-url https://example.com/train.mp4

  # 语音转语音（异步，使用系统音色 ID）
  python mps_dubbing.py --mode async-sts \\
      --url https://example.com/video.mp4 --voice-id s1_2GSzVAf00hl

  # Dry Run（仅打印请求参数，不实际调用 API）
  python mps_dubbing.py --mode tts --text "您好" --voice-id s1_xxx --dry-run

环境变量：
  TENCENTCLOUD_SECRET_ID   - 腾讯云 SecretId
  TENCENTCLOUD_SECRET_KEY  - 腾讯云 SecretKey
  TENCENTCLOUD_COS_BUCKET  - COS Bucket 名称（异步模式必需）
  TENCENTCLOUD_COS_REGION  - COS Bucket 区域（异步模式必需）
"""

import argparse
import base64
import json
import os
import sys
from mps_auto_upgrade import check_sdk_version
import time
import urllib.request

# 同目录辅助模块
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SCRIPT_DIR)

try:
    from mps_load_env import ensure_env_loaded as _ensure_env_loaded
    _LOAD_ENV_AVAILABLE = True
except ImportError:
    _LOAD_ENV_AVAILABLE = False

try:
    from mps_poll_task import poll_video_task, auto_download_outputs
    _POLL_AVAILABLE = True
except ImportError:
    _POLL_AVAILABLE = False

check_sdk_version()
try:
    from tencentcloud.common import credential
    from tencentcloud.common.profile.client_profile import ClientProfile
    from tencentcloud.common.profile.http_profile import HttpProfile
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
    from tencentcloud.mps.v20190612 import mps_client, models
except ImportError:
    print("错误：请先安装腾讯云 SDK：pip install tencentcloud-sdk-python", file=sys.stderr)
    sys.exit(1)


# =============================================================================
# 常量
# =============================================================================

# SyncDubbing 接口端点（国际站设置 TENCENTCLOUD_MPS_ENDPOINT=mps.intl.tencentcloudapi.com）
MPS_ENDPOINT = os.environ.get("TENCENTCLOUD_MPS_ENDPOINT", "mps.tencentcloudapi.com")

# 语音合成 / 语音转语音预设模板 ID（TextToSpeech / SpeechToSpeech）
ASYNC_DUBBING_DEFINITION = 36

# 支持的语种列表
SUPPORTED_LANGS = {
    "zh": "中文 (Chinese)",
    "en": "英语 (English)",
    "ja": "日语 (Japanese)",
    "de": "德语 (German)",
    "fr": "法语 (French)",
    "ko": "韩语 (Korean)",
    "ru": "俄语 (Russian)",
    "uk": "乌克兰语 (Ukrainian)",
    "pt": "葡萄牙语 (Portuguese)",
    "it": "意大利语 (Italian)",
    "es": "西班牙语 (Spanish)",
    "id": "印度尼西亚语 (Indonesian)",
    "nl": "荷兰语 (Dutch)",
    "tr": "土耳其语 (Turkish)",
    "fil": "菲律宾语 (Filipino)",
    "ms": "马来语 (Malay)",
    "el": "希腊语 (Greek)",
    "fi": "芬兰语 (Finnish)",
    "hr": "克罗地亚语 (Croatian)",
    "sk": "斯洛伐克语 (Slovak)",
    "pl": "波兰语 (Polish)",
    "sv": "瑞典语 (Swedish)",
    "hi": "印地语 (Hindi)",
    "bg": "保加利亚语 (Bulgarian)",
    "ro": "罗马尼亚语 (Romanian)",
    "ar": "阿拉伯语 (Arabic)",
    "cs": "捷克语 (Czech)",
    "da": "丹麦语 (Danish)",
    "ta": "泰米尔语 (Tamil)",
    "hun": "匈牙利语 (Hungarian)",
    "vi": "越南语 (Vietnamese)",
    "no": "挪威语 (Norwegian)",
    "yue": "粤语 (Cantonese)",
    "th": "泰语 (Thai)",
    "he": "希伯来语 (Hebrew)",
    "ca": "加泰罗尼亚语 (Catalan)",
    "nn": "尼诺斯克语 (Nynorsk)",
    "af": "阿非利卡语 (Afrikaans)",
    "fa": "波斯语 (Persian)",
    "sl": "斯洛文尼亚语 (Slovenian)",
}

# 支持的采样率
SUPPORTED_SAMPLE_RATES = [8000, 16000, 22050, 32000, 44100]

# 运行模式说明
MODES = {
    "clone":     "音色复刻（同步）—— 传入克隆音频，返回音色 ID",
    "tts":       "短文本语音合成（同步）—— 传入文本 + 音色 ID，返回合成音频",
    "async-tts": "长文本转语音（异步 TextToSpeech）—— 传入长文本，异步合成输出到 COS",
    "async-sts": "语音转语音（异步 SpeechToSpeech）—— 对输入音视频做音色替换，异步输出到 COS",
}

# 同步接口文本长度上限（超出后自动切换为异步模式）
TTS_SYNC_MAX_CHARS = 2000


# =============================================================================
# 工具函数
# =============================================================================

def get_cos_bucket():
    """从环境变量获取 COS Bucket 名称。"""
    return os.environ.get("TENCENTCLOUD_COS_BUCKET", "")


def get_cos_region():
    """从环境变量获取 COS Bucket 区域。"""
    return os.environ.get("TENCENTCLOUD_COS_REGION", "")


def get_credentials():
    """从环境变量获取腾讯云凭证。"""
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
    if not secret_id or not secret_key:
        print("❌ 未找到 TENCENTCLOUD_SECRET_ID / TENCENTCLOUD_SECRET_KEY 环境变量", file=sys.stderr)
        print("   请在 ~/.env 或 <SKILL_DIR>/.env 中配置后重试", file=sys.stderr)
        if _LOAD_ENV_AVAILABLE:
            from mps_load_env import _print_setup_hint
            _print_setup_hint(["TENCENTCLOUD_SECRET_ID", "TENCENTCLOUD_SECRET_KEY"])
        sys.exit(1)
    return credential.Credential(secret_id, secret_key)


def create_mps_client(cred, region):
    """创建 MPS 客户端。"""
    http_profile = HttpProfile()
    http_profile.endpoint = MPS_ENDPOINT
    http_profile.reqMethod = "POST"

    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile

    return mps_client.MpsClient(cred, region or "", client_profile)


def load_audio_base64(audio_file):
    """读取本地音频文件并转换为 base64 字符串。"""
    if not os.path.isfile(audio_file):
        print(f"❌ 音频文件不存在：{audio_file}", file=sys.stderr)
        sys.exit(1)
    with open(audio_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode("utf-8")


def _ensure_wav_ext(path):
    """确保文件路径以 .wav 结尾，否则追加 .wav 后缀。"""
    if not path.lower().endswith(".wav"):
        path = path + ".wav"
    return path


def _truncate_audio_data(d):
    """将字典中 AudioData 字段截断，避免 base64 内容刷屏。"""
    return {
        k: (v[:40] + "...（已截断）" if k == "AudioData" and isinstance(v, str) and len(v) > 40 else v)
        for k, v in d.items()
    }


def save_audio_output(audio_base64, output_path):
    """将 base64 编码的音频（WAV 格式）解码并保存为本地 WAV 文件。"""
    output_path = _ensure_wav_ext(output_path)
    audio_bytes = base64.b64decode(audio_base64)
    # 简单校验：WAV 文件头为 RIFF....WAVE
    if len(audio_bytes) >= 12 and audio_bytes[:4] == b"RIFF" and audio_bytes[8:12] == b"WAVE":
        fmt = "WAV"
    else:
        fmt = "unknown"
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(audio_bytes)
    size_kb = len(audio_bytes) / 1024
    print(f"✅ 音频已保存到：{output_path}  [{fmt}, {size_kb:.1f} KB]")
    return output_path


def download_audio_from_url(url, output_path):
    """从 URL 下载音频并保存为本地 WAV 文件。"""
    output_path = _ensure_wav_ext(output_path)
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    print(f"⬇️  正在从 URL 下载音频...")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "mps-syncdubbing/1.0"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            audio_bytes = resp.read()
    except Exception as e:
        print(f"❌ 下载音频失败：{e}", file=sys.stderr)
        return None
    if len(audio_bytes) >= 12 and audio_bytes[:4] == b"RIFF" and audio_bytes[8:12] == b"WAVE":
        fmt = "WAV"
    else:
        fmt = "unknown"
    with open(output_path, "wb") as f:
        f.write(audio_bytes)
    size_kb = len(audio_bytes) / 1024
    print(f"✅ 音频已保存到：{output_path}  [{fmt}, {size_kb:.1f} KB]")
    return output_path


# =============================================================================
# SyncDubbing 同步接口（clone / tts）
# =============================================================================

def build_sync_params(args):
    """
    构建 SyncDubbing 请求参数。

    两种场景：
    - clone:     仅传 AudioData/AudioUrl，复刻音色，返回 VoiceId
    - tts:       传 Text + VoiceId，语音合成，返回音频
    """
    params = {}

    mode = args.mode

    # ---- 文本参数 + 音色 ID（tts）----
    if mode == "tts":
        if not args.text:
            print(f"❌ --mode {mode} 需要指定 --text 合成文本", file=sys.stderr)
            sys.exit(1)
        params["Text"] = args.text
        if args.text_lang:
            params["TextLang"] = args.text_lang

        if not args.voice_id:
            print("❌ --mode tts 需要指定 --voice-id 音色 ID", file=sys.stderr)
            sys.exit(1)
        params["VoiceId"] = args.voice_id

    # ---- 克隆音频（clone）----
    if mode == "clone":
        if args.audio_file:
            params["AudioData"] = load_audio_base64(args.audio_file)
        elif args.audio_url:
            params["AudioUrl"] = args.audio_url
        else:
            print(f"❌ --mode {mode} 需要指定 --audio-file 或 --audio-url 克隆音频", file=sys.stderr)
            sys.exit(1)
        if args.audio_lang:
            params["AudioLang"] = args.audio_lang

    # ---- 扩展参数（synExt / cloneExt）----
    ext_param = {}
    syn_ext = {}
    clone_ext = {}

    if args.sample_rate is not None:
        if args.sample_rate not in SUPPORTED_SAMPLE_RATES:
            print(f"❌ 不支持的采样率 {args.sample_rate}，支持值：{SUPPORTED_SAMPLE_RATES}", file=sys.stderr)
            sys.exit(1)
        syn_ext["sampleRate"] = args.sample_rate

    if args.pitch is not None:
        if not (-12 <= args.pitch <= 12):
            print(f"❌ 音调取值范围为 [-12, 12]，当前值：{args.pitch}", file=sys.stderr)
            sys.exit(1)
        syn_ext["pitch"] = args.pitch

    if args.duration is not None:
        if args.duration <= 0:
            print(f"❌ 音频时长必须大于 0", file=sys.stderr)
            sys.exit(1)
        syn_ext["duration"] = args.duration

    if args.time_ranges:
        ranges = []
        for tr in args.time_ranges:
            parts = tr.split(",")
            if len(parts) != 2:
                print(f"❌ 时间范围格式错误 '{tr}'，应为 start,end（单位秒，如 5.2,20）", file=sys.stderr)
                sys.exit(1)
            try:
                start, end = float(parts[0]), float(parts[1])
            except ValueError:
                print(f"❌ 时间范围值必须为数字 '{tr}'", file=sys.stderr)
                sys.exit(1)
            ranges.append([start, end])
        clone_ext["timeRanges"] = ranges

    if syn_ext:
        ext_param["synExt"] = syn_ext
    if clone_ext:
        ext_param["cloneExt"] = clone_ext
    if ext_param:
        params["ExtParam"] = json.dumps(ext_param, ensure_ascii=False)

    # ---- 输出选项 ----
    # 默认输出 base64（不额外设置 Output），若需 URL 则设置
    if getattr(args, "output_url", False):
        params["Output"] = {"OutputType": "URL"}

    # ---- 资源 ID ----
    if getattr(args, "resource_id", None):
        params["ResourceId"] = args.resource_id

    return params


def run_sync_dubbing(args):
    """执行同步配音/克隆任务（SyncDubbing API）。"""
    region = getattr(args, "region", None) or os.environ.get("TENCENTCLOUD_API_REGION", "")

    cred = get_credentials()
    client = create_mps_client(cred, region)

    params = build_sync_params(args)

    if args.dry_run:
        print("=" * 60)
        print("【Dry Run 模式】仅打印请求参数，不实际调用 API")
        print("=" * 60)
        print(json.dumps(_truncate_audio_data(params), ensure_ascii=False, indent=2))
        return

    if args.verbose:
        print("请求参数：")
        print(json.dumps(_truncate_audio_data(params), ensure_ascii=False, indent=2))
        print()

    try:
        req = models.SyncDubbingRequest()
        req.from_json_string(json.dumps(params))

        resp = client.SyncDubbing(req)
        result = json.loads(resp.to_json_string())

        error_code = result.get("ErrorCode", -1)
        msg = result.get("Msg", "")
        request_id = result.get("RequestId", "N/A")

        if error_code != 0:
            print(f"❌ 接口返回错误 [{error_code}]: {msg}", file=sys.stderr)
            if args.verbose:
                print("完整响应：")
                print(json.dumps(result, ensure_ascii=False, indent=2))
            sys.exit(1)

        print("✅ 任务完成！")
        print(f"   RequestId: {request_id}")

        mode = args.mode

        # 输出音色 ID
        voice_id = result.get("VoiceId")
        if voice_id:
            print(f"   VoiceId: {voice_id}")

        # 输出音频时长（ExtInfo）
        ext_info_str = result.get("ExtInfo")
        if ext_info_str:
            try:
                ext_info = json.loads(ext_info_str)
                if isinstance(ext_info, dict):
                    duration = ext_info.get("duration")
                    if duration is not None:
                        print(f"   音频时长: {duration:.3f} 秒")
            except (json.JSONDecodeError, TypeError):
                pass

        # 确定本地输出路径
        output_path = getattr(args, "output", None)
        if not output_path:
            output_path = _auto_output_name(args)

        # 保存合成音频（仅语音合成模式，clone 模式不产生音频）
        if mode != "clone":
            audio_data = result.get("AudioData")
            audio_url = result.get("AudioUrl")

            if audio_data:
                # 优先使用 base64 数据直接写盘（无需网络请求）
                save_audio_output(audio_data, output_path)
            elif audio_url:
                # 接口返回 URL（使用了 --output-url 或服务端选择 URL 输出）
                print(f"   AudioUrl: {audio_url}")
                download_audio_from_url(audio_url, output_path)
            else:
                print("⚠️  响应中未包含 AudioData / AudioUrl，无法保存音频", file=sys.stderr)
        else:
            # clone 模式仅打印 AudioUrl（若有）
            audio_url = result.get("AudioUrl")
            if audio_url:
                print(f"   AudioUrl: {audio_url}")

        if args.verbose:
            print("\n完整响应：")
            print(json.dumps(_truncate_audio_data(result), ensure_ascii=False, indent=2))

        return result

    except TencentCloudSDKException as e:
        print(f"❌ 请求失败: {e}", file=sys.stderr)
        sys.exit(1)


def _auto_output_name(args):
    """根据模式自动生成输出文件名。"""
    ts = int(time.time())
    mode = args.mode
    if mode == "tts":
        name = f"tts_{ts}.wav"
    else:
        name = f"dubbing_{ts}.wav"
    return name


# =============================================================================
# 长文本异步接口（async-tts / async-sts，ProcessMedia API）
# =============================================================================

def build_async_input_info(args):
    """
    构建异步任务的输入信息。

    async-tts 模式：InputInfo 可填任意可访问的音视频链接（不统计时长计费），建议使用占位 URL。
    async-sts 模式：InputInfo 为要做音色替换的原始音视频。
    """
    mode = args.mode

    if mode == "async-tts":
        # TextToSpeech 模式 InputInfo 仅作占位，填任意可访问链接
        url = getattr(args, "url", None) or getattr(args, "placeholder_url", None)
        if not url:
            # 使用公开 COS 测试资源作占位
            url = "https://mps-1300828900.cos.ap-guangzhou.myqcloud.com/test/silent_1s.mp4"
        return {"Type": "URL", "UrlInputInfo": {"Url": url}}

    # async-sts 模式：真实输入源
    if args.url:
        return {"Type": "URL", "UrlInputInfo": {"Url": args.url}}

    cos_input_key = getattr(args, "cos_input_key", None)
    if cos_input_key:
        bucket = getattr(args, "cos_input_bucket", None) or get_cos_bucket()
        region = getattr(args, "cos_input_region", None) or get_cos_region()
        if not bucket:
            print("❌ COS 输入需要指定 Bucket。请通过 --cos-input-bucket 或 TENCENTCLOUD_COS_BUCKET 设置",
                  file=sys.stderr)
            sys.exit(1)
        return {
            "Type": "COS",
            "CosInputInfo": {
                "Bucket": bucket,
                "Region": region,
                "Object": cos_input_key if cos_input_key.startswith("/") else f"/{cos_input_key}",
            },
        }

    print("❌ async-sts 模式需要指定输入源：--url 或 --cos-input-key", file=sys.stderr)
    sys.exit(1)


def build_async_extended_param(args):
    """
    构建 ExtendedParameter JSON 字符串。

    TextToSpeech 场景：
      {"dubbing": {"dubbingType": "TextToSpeech", "text": "...", "voiceId": "...", ...}}

    SpeechToSpeech 场景：
      {"dubbing": {"dubbingType": "SpeechToSpeech", "cloneVideoUrl": "...", "voiceId": "...", ...}}
    """
    mode = args.mode
    dubbing = {}

    if mode == "async-tts":
        dubbing["dubbingType"] = "TextToSpeech"

        if not args.text:
            print("❌ --mode async-tts 需要指定 --text 合成文本", file=sys.stderr)
            sys.exit(1)
        dubbing["text"] = args.text

        if args.text_lang:
            dubbing["textLang"] = args.text_lang
        if args.voice_id:
            dubbing["voiceId"] = args.voice_id
        if getattr(args, "clone_video_url", None):
            dubbing["cloneVideoUrl"] = args.clone_video_url
        if getattr(args, "clone_video_lang", None):
            dubbing["cloneVideoLang"] = args.clone_video_lang
        if getattr(args, "output_pattern", None):
            dubbing["outputPattern"] = args.output_pattern

    elif mode == "async-sts":
        dubbing["dubbingType"] = "SpeechToSpeech"

        if not args.voice_id and not getattr(args, "clone_video_url", None):
            print("❌ --mode async-sts 需要指定 --voice-id 或 --clone-video-url", file=sys.stderr)
            sys.exit(1)

        if args.voice_id:
            dubbing["voiceId"] = args.voice_id
        if getattr(args, "clone_video_url", None):
            dubbing["cloneVideoUrl"] = args.clone_video_url
        if getattr(args, "clone_video_lang", None):
            dubbing["cloneVideoLang"] = args.clone_video_lang
        if getattr(args, "src_lang", None):
            dubbing["srcLang"] = args.src_lang
        if getattr(args, "output_pattern", None):
            dubbing["outputPattern"] = args.output_pattern

    # extraPara.synExt（两种异步模式公共部分）
    syn_ext = {}
    if args.pitch is not None:
        syn_ext["pitch"] = args.pitch
    if mode == "async-tts" and args.sample_rate is not None:
        if args.sample_rate not in SUPPORTED_SAMPLE_RATES:
            print(f"❌ 不支持的采样率 {args.sample_rate}，支持值：{SUPPORTED_SAMPLE_RATES}", file=sys.stderr)
            sys.exit(1)
        syn_ext["sampleRate"] = args.sample_rate
    if syn_ext:
        dubbing["extraPara"] = {"synExt": syn_ext}

    ext_param_obj = {"dubbing": dubbing}
    return json.dumps(ext_param_obj, ensure_ascii=False)


def build_async_output_storage(args):
    """构建异步任务输出存储。"""
    bucket = getattr(args, "output_bucket", None) or get_cos_bucket()
    region = getattr(args, "output_region", None) or get_cos_region()

    if not bucket:
        print("❌ 异步模式需要配置输出 COS Bucket（--output-bucket 或 TENCENTCLOUD_COS_BUCKET 环境变量）",
              file=sys.stderr)
        sys.exit(1)
    return {
        "Type": "COS",
        "CosOutputStorage": {
            "Bucket": bucket,
            "Region": region,
        },
    }


def build_async_request_params(args):
    """构建完整的 ProcessMedia 请求参数。"""
    params = {}

    # 输入
    params["InputInfo"] = build_async_input_info(args)

    # 输出存储
    params["OutputStorage"] = build_async_output_storage(args)

    # 输出目录（API 要求必须以 / 结尾）
    output_dir = getattr(args, "output_dir", None) or "/output/dubbing/"
    if not output_dir.endswith("/"):
        output_dir += "/"
    params["OutputDir"] = output_dir

    # AI 分析任务（语音合成，Definition=36）
    extended_param = build_async_extended_param(args)
    params["AiAnalysisTask"] = {
        "Definition": ASYNC_DUBBING_DEFINITION,
        "ExtendedParameter": extended_param,
    }

    # 回调配置
    notify_url = getattr(args, "notify_url", None)
    if notify_url:
        params["TaskNotifyConfig"] = {
            "NotifyType": "URL",
            "NotifyUrl": notify_url,
        }

    return params


def run_async_dubbing(args):
    """执行异步语音合成/语音转语音任务（ProcessMedia API）。"""
    region = getattr(args, "region", None) or os.environ.get("TENCENTCLOUD_API_REGION", "")

    cred = get_credentials()
    client = create_mps_client(cred, region)

    params = build_async_request_params(args)

    if args.dry_run:
        print("=" * 60)
        print("【Dry Run 模式】仅打印请求参数，不实际调用 API")
        print("=" * 60)
        print(json.dumps(params, ensure_ascii=False, indent=2))
        return

    if args.verbose:
        print("请求参数：")
        print(json.dumps(params, ensure_ascii=False, indent=2))
        print()

    try:
        req = models.ProcessMediaRequest()
        req.from_json_string(json.dumps(params))

        resp = client.ProcessMedia(req)
        result = json.loads(resp.to_json_string())

        task_id = result.get("TaskId", "N/A")
        print("✅ 异步任务提交成功！")
        print(f"   TaskId: {task_id}")
        print(f"   RequestId: {result.get('RequestId', 'N/A')}")

        mode = args.mode
        mode_desc = MODES.get(mode, mode)
        print(f"   模式: {mode_desc}")

        extended_param = params.get("AiAnalysisTask", {}).get("ExtendedParameter", "")
        if extended_param and args.verbose:
            print(f"   ExtendedParameter: {extended_param}")

        out_storage = params.get("OutputStorage", {}).get("CosOutputStorage", {})
        out_dir = params.get("OutputDir", "")
        if out_storage:
            print(f"   输出: COS - {out_storage.get('Bucket')}:{out_dir} "
                  f"(region: {out_storage.get('Region')})")

        if args.verbose:
            print("\n完整响应：")
            print(json.dumps(result, ensure_ascii=False, indent=2))

        # 自动轮询（除非指定 --no-wait）
        no_wait = getattr(args, "no_wait", False)
        if not no_wait and _POLL_AVAILABLE and task_id != "N/A":
            poll_interval = getattr(args, "poll_interval", 10)
            max_wait = getattr(args, "max_wait", 3600)
            task_result = poll_video_task(task_id, region=region, interval=poll_interval,
                                         max_wait=max_wait, verbose=args.verbose)
            # 自动下载
            download_dir = getattr(args, "download_dir", None)
            if download_dir and task_result and _POLL_AVAILABLE:
                auto_download_outputs(task_result, download_dir=download_dir)
        else:
            print(f"\n提示：任务在后台处理中，可使用以下命令查询进度：")
            print(f"  python scripts/mps_get_video_task.py --task-id {task_id}")

        return result

    except TencentCloudSDKException as e:
        print(f"❌ 请求失败: {e}", file=sys.stderr)
        sys.exit(1)


# =============================================================================
# 主函数
# =============================================================================

# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)
def main():
    parser = argparse.ArgumentParser(
        description="腾讯云 MPS 语音合成与音色复刻 —— 有声书/播客/音视频创作首选，支持 40+ 语种",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
运行模式（--mode）：
  clone       音色复刻（同步）—— 返回音色 ID
  tts         语音合成 —— 返回 WAV 音频（文本 ≤2000 字符用同步，超出自动切换异步）
  async-tts   长文本转语音（异步）—— TextToSpeech，输出到 COS
  async-sts   语音转语音（异步）—— SpeechToSpeech，音色替换，输出到 COS

⚡ 自动模式切换：使用 tts 模式时，若文本超过 2000 字符，会自动切换为
  async-tts 异步模式，无需手动指定 --mode async-tts。

示例：
  # 音色复刻（传入本地音频，建议 10~20 秒清晰单人语音）
  python mps_dubbing.py --mode clone --audio-file /path/to/voice.wav

  # 音色复刻（传入音频 URL）
  python mps_dubbing.py --mode clone --audio-url https://example.com/voice.mp4

  # 短文本语音合成（指定系统音色 ID）
  python mps_dubbing.py --mode tts --text "您好，欢迎使用腾讯云" --voice-id s1_2GSzVAf00hl

  # 短文本语音合成（自定义采样率 + 音调 + 输出文件）
  python mps_dubbing.py --mode tts --text "Hello!" --voice-id s1_xxx \\
      --sample-rate 44100 --pitch 2 --output /tmp/out.wav

  # 先复刻音色，再用拿到的 VoiceId 合成
  python mps_dubbing.py --mode clone --audio-file voice.wav
  python mps_dubbing.py --mode tts --text "您好" --voice-id <上一步返回的 VoiceId>

  # 长文本转语音（异步，指定音色 ID）
  python mps_dubbing.py --mode async-tts \\
      --text "这是一段超过 2000 字的长文本..." --voice-id clone_v1_Q03FBduA

  # 长文本转语音（异步，传入克隆视频 URL）
  python mps_dubbing.py --mode async-tts \\
      --text "长文本..." --clone-video-url https://example.com/train.mp4

  # 语音转语音（异步，替换音色）
  python mps_dubbing.py --mode async-sts \\
      --url https://example.com/video.mp4 \\
      --clone-video-url https://example.com/train.mp4

  # 语音转语音（异步，使用指定音色 ID）
  python mps_dubbing.py --mode async-sts \\
      --url https://example.com/video.mp4 --voice-id s1_2GSzVAf00hl

  # Dry Run
  python mps_dubbing.py --mode tts --text "您好" --voice-id s1_xxx --dry-run

支持语种（--text-lang / --audio-lang / --src-lang / --clone-video-lang）：
  zh=中文  en=英语  ja=日语  ko=韩语  de=德语  fr=法语  es=西班牙语  it=意大利语
  ru=俄语  pt=葡萄牙语  ar=阿拉伯语  hi=印地语  th=泰语  vi=越南语  ...（共 40+ 种）

环境变量：
  TENCENTCLOUD_SECRET_ID   腾讯云 SecretId
  TENCENTCLOUD_SECRET_KEY  腾讯云 SecretKey
  TENCENTCLOUD_COS_BUCKET  COS Bucket 名称（异步模式必需）
  TENCENTCLOUD_COS_REGION  COS Bucket 区域（异步模式必需）
        """
    )

    # ---- 运行模式 ----
    parser.add_argument(
        "--mode", type=str, required=True, choices=list(MODES.keys()),
        metavar="MODE",
        help=(
            "运行模式（必填）："
            "clone=音色复刻 | "
            "tts=语音合成 | "
            "async-tts=长文本转语音 | "
            "async-sts=语音转语音"
        )
    )

    # ---- 文本参数 ----
    text_group = parser.add_argument_group("文本参数（tts / async-tts 模式使用）")
    text_group.add_argument("--text", type=str,
                            help="合成文本。tts 模式：≤2000 字符走同步接口，"
                                 "超出时自动切换为异步接口（无需手动指定 async-tts）")
    text_group.add_argument(
        "--text-lang", type=str, metavar="LANG",
        choices=list(SUPPORTED_LANGS.keys()),
        help="文本语言（默认中文 zh）。如 en/ja/ko/fr/de/..."
    )

    # ---- 音色参数 ----
    voice_group = parser.add_argument_group("音色参数")
    voice_group.add_argument("--voice-id", type=str,
                             help="音色 ID（系统音色或克隆音色）。tts/async-tts/async-sts 模式使用")

    # ---- 克隆音频参数 ----
    clone_group = parser.add_argument_group("克隆音频参数（clone 同步模式使用）")
    clone_group.add_argument("--audio-file", type=str,
                             help="本地克隆音频文件路径（支持 WAV/MP3/MP4 等）。建议时长 10~20 秒，单人清晰语音")
    clone_group.add_argument("--audio-url", type=str,
                             help="克隆音频 URL（--audio-file 为空时使用）")
    clone_group.add_argument(
        "--audio-lang", type=str, metavar="LANG",
        choices=list(SUPPORTED_LANGS.keys()),
        help="克隆音频语言（默认中文 zh）"
    )
    clone_group.add_argument("--time-ranges", type=str, action="append",
                             metavar="START,END",
                             help="指定克隆音频的时间范围（单位秒，如 5.2,20）。可多次指定，默认 [[0, 20]]")

    # ---- 异步任务克隆视频 ----
    async_clone_group = parser.add_argument_group("异步模式克隆视频参数（async-tts / async-sts 使用）")
    async_clone_group.add_argument("--clone-video-url", type=str,
                                   help="克隆音色的视频/音频 URL（要求时长不小于 5 秒，单人说话人）")
    async_clone_group.add_argument(
        "--clone-video-lang", type=str, metavar="LANG",
        choices=list(SUPPORTED_LANGS.keys()),
        help="克隆视频/音频对应的语言（默认中文 zh）"
    )
    async_clone_group.add_argument(
        "--src-lang", type=str, metavar="LANG",
        choices=list(SUPPORTED_LANGS.keys()),
        help="源视频/音频对应的语言（async-sts 模式使用）"
    )

    # ---- 异步任务输入源 ----
    input_group = parser.add_argument_group("异步任务输入源（async-tts/async-sts 使用）")
    input_group.add_argument("--url", type=str,
                             help="输入视频/音频 URL。"
                                  "async-tts 模式可不填（填任意可访问链接），async-sts 模式必填")
    input_group.add_argument("--cos-input-bucket", type=str,
                             help="输入 COS Bucket 名称（与 --cos-input-key 配合使用）")
    input_group.add_argument("--cos-input-region", type=str,
                             help="输入 COS Bucket 区域")
    input_group.add_argument("--cos-input-key", type=str,
                             help="输入 COS 对象 Key（如 /input/video.mp4）")

    # ---- 音频合成质量参数 ----
    quality_group = parser.add_argument_group("音频质量参数（可选）")
    quality_group.add_argument("--sample-rate", type=int,
                               metavar="RATE",
                               choices=SUPPORTED_SAMPLE_RATES,
                               help=f"输出音频采样率，支持：{SUPPORTED_SAMPLE_RATES}（默认 16000）")
    quality_group.add_argument("--pitch", type=int,
                               metavar="[-12,12]",
                               help="音调，取值范围 [-12, 12]，默认 0（原音色输出）")
    quality_group.add_argument("--duration", type=float,
                               help="合成音频目标时长（秒，如 5.2）。仅同步模式有效")

    # ---- 异步任务输出配置 ----
    output_group = parser.add_argument_group("异步任务输出配置（async-tts / async-sts 使用）")
    output_group.add_argument("--output-bucket", type=str,
                              help="输出 COS Bucket（默认取 TENCENTCLOUD_COS_BUCKET 环境变量）")
    output_group.add_argument("--output-region", type=str,
                              help="输出 COS Bucket 区域（默认取 TENCENTCLOUD_COS_REGION 环境变量）")
    output_group.add_argument("--output-dir", type=str,
                              help="输出目录（默认 /output/dubbing/），以 / 开头和结尾")
    output_group.add_argument("--output-pattern", type=str,
                              help="输出文件名前缀，支持占位符 {taskType}、{timestamp}")

    # ---- 同步任务输出 ----
    sync_output_group = parser.add_argument_group("同步任务输出配置（clone / tts 使用）")
    sync_output_group.add_argument("--output", "-o", type=str,
                                   help="合成音频保存路径（如 /tmp/output.wav）。"
                                        "不指定时自动生成文件名保存到当前目录")
    sync_output_group.add_argument("--output-url", action="store_true",
                                   help="请求接口返回音频 URL（有效期 24 小时）而非 base64 数据")

    # ---- 其他配置 ----
    other_group = parser.add_argument_group("其他配置")
    other_group.add_argument("--region", type=str, help="MPS 服务区域（同步接口不需要 Region，异步接口建议指定）")
    other_group.add_argument("--resource-id", type=str, help="资源 ID（默认使用账号主资源 ID）")
    other_group.add_argument("--notify-url", type=str, help="异步任务完成回调 URL")
    other_group.add_argument("--no-wait", action="store_true",
                             help="仅提交异步任务，不等待结果（默认会自动轮询直到完成）")
    other_group.add_argument("--poll-interval", type=int, default=10,
                             help="轮询间隔（秒），默认 10")
    other_group.add_argument("--max-wait", type=int, default=3600,
                             help="最长等待时间（秒），默认 3600（1小时）")
    other_group.add_argument("--download-dir", type=str, default=None,
                             help="异步任务完成后自动下载结果到指定目录")
    other_group.add_argument("--verbose", "-v", action="store_true", help="输出详细信息")
    other_group.add_argument("--dry-run", action="store_true", help="仅打印请求参数，不实际调用 API")

    args = parser.parse_args()

    # 加载 .env 文件中的环境变量（如有）
    if _LOAD_ENV_AVAILABLE:
        _ensure_env_loaded()

    # ---- 参数校验 ----
    mode = args.mode

    # ---- 自动检测：根据文本长度决定同步/异步路径 ----
    # SyncDubbing 接口文本上限为 TTS_SYNC_MAX_CHARS 字符；超出时自动切换为异步模式。
    _auto_upgraded = False
    _orig_mode = None
    _text_len = None
    if mode == "tts" and args.text:
        _text_len = len(args.text)
        if _text_len > TTS_SYNC_MAX_CHARS:
            _orig_mode = mode
            _auto_upgraded = True
            mode = "async-tts"
            args.mode = mode

    # 同步模式不能使用异步专用参数
    if mode in ("clone", "tts"):
        async_only = [
            (getattr(args, "clone_video_url", None), "--clone-video-url"),
            (getattr(args, "clone_video_lang", None), "--clone-video-lang"),
            (getattr(args, "src_lang", None), "--src-lang"),
            (getattr(args, "output_bucket", None), "--output-bucket"),
            (getattr(args, "output_dir", None), "--output-dir"),
            (getattr(args, "output_pattern", None), "--output-pattern"),
            (getattr(args, "notify_url", None), "--notify-url"),
            (getattr(args, "no_wait", False) and True, "--no-wait"),
            (getattr(args, "download_dir", None), "--download-dir"),
        ]
        used = [name for val, name in async_only if val]
        if used:
            parser.error(f"参数 {', '.join(used)} 仅支持异步模式（async-tts / async-sts）")

    # async-tts 模式需要 --text
    if mode == "async-tts" and not args.text:
        parser.error("--mode async-tts 需要指定 --text 合成文本")

    # async-sts 模式需要 --voice-id 或 --clone-video-url
    if mode == "async-sts":
        if not args.voice_id and not getattr(args, "clone_video_url", None):
            parser.error("--mode async-sts 需要指定 --voice-id 或 --clone-video-url")

    # tts 模式需要 --text 和 --voice-id
    if mode == "tts" and not args.text:
        parser.error("--mode tts 需要指定 --text 合成文本")
    if mode == "tts" and not args.voice_id:
        parser.error("--mode tts 需要指定 --voice-id 音色 ID")

    # clone 模式需要 --audio-file 或 --audio-url
    if mode == "clone":
        if not args.audio_file and not args.audio_url:
            parser.error("--mode clone 需要指定 --audio-file 或 --audio-url 克隆音频")

    # 打印执行信息
    print("=" * 60)
    if _auto_upgraded:
        print(f"⚡ 自动检测：文本 {_text_len} 字符 > 同步上限 {TTS_SYNC_MAX_CHARS} 字符")
        print(f"   已自动切换：{_orig_mode}（同步）→ async-tts（异步 TextToSpeech）")
    print(f"腾讯云 MPS 语音合成与音色复刻 — {MODES.get(mode, mode)}")
    print("=" * 60)

    if mode in ("clone", "tts"):
        if mode == "tts":
            text_preview = (args.text[:30] + "...") if args.text and len(args.text) > 30 else args.text
            print(f"文本: {text_preview}")
        if args.voice_id:
            print(f"音色 ID: {args.voice_id}")
        if args.audio_file:
            print(f"克隆音频: {args.audio_file}")
        elif args.audio_url:
            print(f"克隆音频: {args.audio_url}")
    else:
        if args.url:
            print(f"输入: {args.url}")
        elif getattr(args, "cos_input_key", None):
            bucket = getattr(args, "cos_input_bucket", None) or get_cos_bucket()
            print(f"输入: COS - {bucket}:{args.cos_input_key}")
        if args.text:
            text_preview = (args.text[:50] + "...") if len(args.text) > 50 else args.text
            print(f"文本: {text_preview}")
        if args.voice_id:
            print(f"音色 ID: {args.voice_id}")
        if getattr(args, "clone_video_url", None):
            print(f"克隆视频: {args.clone_video_url}")
        out_bucket = getattr(args, "output_bucket", None) or get_cos_bucket() or "未设置"
        out_dir = getattr(args, "output_dir", None) or "/output/dubbing/"
        print(f"输出: COS - {out_bucket}:{out_dir}")

        # 异步模式检查 COS Bucket
        if not get_cos_bucket() and not getattr(args, "output_bucket", None) and not args.dry_run:
            print("❌ 未设置 TENCENTCLOUD_COS_BUCKET 环境变量，请配置后重试", file=sys.stderr)
            sys.exit(1)

    print("-" * 60)

    # ---- 执行 ----
    if mode in ("clone", "tts"):
        run_sync_dubbing(args)
    else:
        run_async_dubbing(args)


if __name__ == "__main__":
    main()
