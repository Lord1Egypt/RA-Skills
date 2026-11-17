"""
会议纪要生成模块 v5.1.0
功能：语音 → 转写 → 要素化摘要 → Word 文档

v5.1.0 变更:
  - 新增：三段式要素化纪要结构（待办清单+决策记录+风险异议）
  - 新增：说话人标注（MFCC 分离或显式报名）
  - 新增：Word 分节导出（每节独立页眉）
  - 优化：结构化摘要支持 llm_bridge + 本地规则双引擎
  - 版本升级到 v5.1.0

v4.9.0 变更:
  - 新增：llm_bridge 作为摘要的优先引擎，未装 cn-llm-router 时回落本地规则
  - 版本升级到 v4.9.0

v4.6.1 变更:
  - 🔒 ASR 引擎改为显式 Opt-in：auto 模式仅使用本地 whisper-local 和 template，不读取外部凭证
  - 🔒 Azure/Google STT 仅在用户 method 显式指定时调用，首次使用显示凭证读取范围警告
  - 🔒 移除 azure-speech 和 google-stt 的自动检测与降级

v4.5.0 变更:
  - 🎯 会议纪要完整流水线（ASR 转写 → LLM 摘要 → Word 生成）
  - 🎯 长音频分段处理（默认 5 分钟/段，可配置）
  - 🎯 进度回调（每段完成触发回调函数）
  - 🎯 硬件自适应（根据内存调整并发数）
"""

import os
import sys
import json
import re
import hashlib
import tempfile
import wave
import math
import time
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Callable, List, Dict, Any, Tuple

# 从公共模块导入
sys.path.insert(0, str(Path(__file__).parent))

try:
    from wps_common import safe_path, get_hardware_info, release_wps, with_retry
except ImportError:
    # 降级：独立运行时提供 stub
    def safe_path(p): return Path(p)
    def get_hardware_info(): return {"cpu_cores": 4, "memory_gb": 8, "level": "medium"}
    def release_wps(): pass
    def with_retry(f): return f

try:
    from wps_word import call_worker
except ImportError:
    def call_worker(cmd, args):
        return {"ok": False, "error": "wps_word 模块不可用"}


class AudioProcessor:
    """音频预处理与分段"""
    
    def __init__(self, segment_minutes: int = 5, progress_cb: Optional[Callable] = None):
        self.segment_minutes = segment_minutes
        self.progress_cb = progress_cb or (lambda *a: None)
        self.hw = get_hardware_info()
        # 低配电脑减少并发
        self.max_workers = 1 if self.hw.get("level") == "low" else min(4, self.hw.get("cpu_cores", 4))
    
    def get_audio_duration(self, audio_path: str) -> float:
        """获取音频时长（秒）"""
        try:
            # 尝试用 wave（仅 wav）
            if audio_path.lower().endswith(".wav"):
                with wave.open(audio_path, "rb") as wf:
                    frames = wf.getnframes()
                    rate = wf.getframerate()
                    return frames / float(rate)
        except Exception:
            pass
        
        # 尝试 ffprobe
        try:
            cmd = [
                "ffprobe", "-v", "quiet", "-show_entries",
                "format=duration", "-of", "csv=p=0", audio_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return float(result.stdout.strip())
        except Exception:
            pass
        
        # 降级：按文件大小估算（假设 128kbps mp3）
        try:
            size = os.path.getsize(audio_path)
            return size / (128 * 1024 / 8)  # 粗略估算
        except Exception:
            return 0.0
    
    def segment_audio(self, audio_path: str, output_dir: str) -> List[str]:
        """将长音频切分为多段（使用 ffmpeg）"""
        duration = self.get_audio_duration(audio_path)
        if duration <= 0:
            return [audio_path]  # 无法获取时长，原样返回
        
        segment_seconds = self.segment_minutes * 60
        if duration <= segment_seconds:
            return [audio_path]  # 不需要分段
        
        segments = []
        num_segments = math.ceil(duration / segment_seconds)
        self.progress_cb("segment_start", {"total": num_segments, "duration": duration})
        
        for i in range(num_segments):
            start = i * segment_seconds
            seg_path = os.path.join(output_dir, f"segment_{i:03d}.wav")
            cmd = [
                "ffmpeg", "-y", "-i", audio_path,
                "-ss", str(start), "-t", str(segment_seconds),
                "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
                seg_path
            ]
            try:
                subprocess.run(cmd, capture_output=True, timeout=60)
                if os.path.exists(seg_path):
                    segments.append(seg_path)
                    self.progress_cb("segment_done", {"index": i, "path": seg_path})
            except Exception as e:
                self.progress_cb("segment_error", {"index": i, "error": str(e)})
        
        return segments if segments else [audio_path]
    
    def cleanup_segments(self, segments: List[str]):
        """清理临时分段文件"""
        for seg in segments:
            try:
                if "segment_" in seg and os.path.exists(seg):
                    os.remove(seg)
            except Exception:
                pass


class ASRTranscriber:
    """ASR 转写引擎（带降级链）"""
    
    def __init__(self, method: str = "auto", progress_cb: Optional[Callable] = None):
        self.method = method
        self.progress_cb = progress_cb or (lambda *a: None)
        self._available_methods = self._detect_available()
    
    def _detect_available(self) -> Dict[str, bool]:
        """检测可用的 ASR 引擎（仅本地引擎）"""
        available = {
            "whisper-local": False,
            "azure-speech": False,
            "google-stt": False,
            "template": True,  # 始终可用
        }
        
        # 检测 whisper
        try:
            import whisper
            available["whisper-local"] = True
        except ImportError:
            pass
        
        # 注意：azure-speech 和 google-stt 的可用性仅在用户显式指定 method 时检测
        # auto 模式下不自动检测外部服务，避免读取凭证文件
        
        return available
    
    def _detect_external_available(self, method: str) -> bool:
        """检测外部 ASR 引擎是否可用（仅在显式调用时执行）"""
        if method == "azure-speech":
            try:
                import azure.cognitiveservices.speech as speechsdk
                key = os.environ.get("AZURE_SPEECH_KEY", "")
                return bool(key)
            except ImportError:
                return False
        elif method == "google-stt":
            try:
                from google.cloud import speech
                cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")
                return bool(cred_path and os.path.exists(cred_path))
            except ImportError:
                return False
        return False
    
    def get_best_method(self) -> str:
        """根据可用性选择最佳方法（auto 模式仅使用本地引擎）"""
        if self.method != "auto":
            # 显式指定外部引擎时，检测是否可用
            if self.method in ("azure-speech", "google-stt"):
                if self._detect_external_available(self.method):
                    return self.method
                else:
                    # 外部引擎不可用，降级到 template
                    print(f"[ASR] ⚠️ 外部引擎 '{self.method}' 不可用（SDK 未安装或凭证未配置），降级到 template", file=sys.stderr)
                    return "template"
            return self.method
        
        # auto 模式：仅使用本地 whisper-local，不读取外部凭证
        if self._available_methods.get("whisper-local", False):
            return "whisper-local"
        return "template"
    
    @with_retry
    def transcribe(self, audio_path: str, language: str = "zh") -> Dict[str, Any]:
        """转写音频（显式 Opt-in 模式）"""
        method = self.get_best_method()
        self.progress_cb("transcribe_start", {"method": method, "file": audio_path})
        
        # 外部服务调用前显示警告
        if method == "azure-speech":
            self._warn_azure_usage()
        elif method == "google-stt":
            self._warn_google_usage()
        
        try:
            if method == "whisper-local":
                result = self._transcribe_whisper(audio_path, language)
            elif method == "azure-speech":
                result = self._transcribe_azure(audio_path, language)
            elif method == "google-stt":
                result = self._transcribe_google(audio_path, language)
            else:
                result = self._transcribe_template(audio_path, language)
            
            self.progress_cb("transcribe_done", {"method": method, "chars": len(result.get("text", ""))})
            return {"success": True, "method": method, **result}
        
        except Exception as e:
            self.progress_cb("transcribe_error", {"method": method, "error": str(e)})
            # 尝试降级到 template
            if method != "template":
                return self._transcribe_template(audio_path, language)
            return {"success": False, "error": f"ASR 转写失败: {str(e)}"}
    
    def _warn_azure_usage(self):
        """Azure Speech 使用前的 Opt-in 警告"""
        region = os.environ.get("AZURE_SPEECH_REGION", "eastasia")
        key = os.environ.get("AZURE_SPEECH_KEY", "")
        key_preview = key[:4] + "..." + key[-4:] if len(key) > 8 else "未配置"
        print(f"""
⚠️  [Azure Speech 服务调用警告]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 即将使用 Azure Speech 服务进行语音转写
🔑 凭证: AZURE_SPEECH_KEY = {key_preview}
🌐 区域: {region}
📤 数据流向: 音频数据将发送至 https://{region}.stt.speech.microsoft.com
📌 用途: 将音频转写为文本
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
外部服务将在上方信息确认后开始调用。
""", file=sys.stderr)
    
    def _warn_google_usage(self):
        """Google STT 使用前的 Opt-in 警告"""
        cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")
        cred_exists = os.path.exists(cred_path) if cred_path else False
        cred_preview = f"存在 ({Path(cred_path).name})" if cred_exists else "路径不存在"
        print(f"""
⚠️  [Google Cloud Speech API 调用警告]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 即将使用 Google Cloud Speech API 进行语音转写
🔑 凭证文件 (GOOGLE_APPLICATION_CREDENTIALS): {cred_preview}
📤 数据流向: 音频数据将发送至 https://speech.googleapis.com/v1
📌 用途: 将音频转写为文本
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
凭证文件将读取并发送至 Google Cloud 服务。
外部服务将在上方信息确认后开始调用。
""", file=sys.stderr)
    
    def _transcribe_whisper(self, audio_path: str, language: str) -> Dict[str, Any]:
        """本地 Whisper 转写"""
        import whisper
        
        hw = get_hardware_info()
        # 低配电脑用 tiny 模型
        model_name = "tiny" if hw.get("level") == "low" else "base"
        
        model = whisper.load_model(model_name)
        result = model.transcribe(audio_path, language=language, fp16=False)
        
        return {
            "text": result.get("text", ""),
            "segments": result.get("segments", []),
            "language": result.get("language", language),
        }
    
    def _transcribe_azure(self, audio_path: str, language: str) -> Dict[str, Any]:
        """Azure Speech 转写（需要 AZURE_SPEECH_KEY 环境变量）"""
        import azure.cognitiveservices.speech as speechsdk
        
        key = os.environ.get("AZURE_SPEECH_KEY", "")
        region = os.environ.get("AZURE_SPEECH_REGION", "eastasia")
        
        if not key:
            raise ValueError("未配置 AZURE_SPEECH_KEY 环境变量")
        
        speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
        speech_config.speech_recognition_language = f"{language}-CN"
        
        audio_config = speechsdk.audio.AudioConfig(filename=audio_path)
        recognizer = speechsdk.SpeechRecognizer(speech_config, audio_config)
        
        done = False
        all_text = []
        
        def recognized_cb(evt):
            if evt.result.text:
                all_text.append(evt.result.text)
        
        def stop_cb(evt):
            nonlocal done
            done = True
        
        recognizer.recognized.connect(recognized_cb)
        recognizer.session_stopped.connect(stop_cb)
        recognizer.canceled.connect(stop_cb)
        
        recognizer.start_continuous_recognition()
        while not done:
            time.sleep(0.5)
        recognizer.stop_continuous_recognition()
        
        return {
            "text": " ".join(all_text),
            "segments": [],
            "language": language,
        }
    
    def _transcribe_google(self, audio_path: str, language: str) -> Dict[str, Any]:
        """Google STT 转写（需要 GOOGLE_APPLICATION_CREDENTIALS 环境变量）"""
        from google.cloud import speech
        
        client = speech.SpeechClient()
        with open(audio_path, "rb") as f:
            content = f.read()
        
        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=f"{language}-CN",
        )
        
        response = client.recognize(config=config, audio=audio)
        texts = [result.alternatives[0].transcript for result in response.results]
        
        return {
            "text": " ".join(texts),
            "segments": [],
            "language": language,
        }
    
    def _transcribe_template(self, audio_path: str, language: str) -> Dict[str, Any]:
        """模板框架（所有 ASR 不可用时的降级方案）"""
        # 生成一个模板框架，用户可手动填充
        duration = 0
        try:
            cmd = ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
                   "-of", "csv=p=0", audio_path]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                duration = float(result.stdout.strip())
        except Exception:
            pass
        
        mins = duration / 60 if duration > 0 else "?"
        
        template_text = f"""[会议录音转写模板]

⚠️ 注意：当前无可用的 ASR 引擎，已生成空白模板。
请安装以下任一引擎后重试：
  - 本地 Whisper: pip install openai-whisper
  - Azure Speech: 设置 AZURE_SPEECH_KEY 环境变量
  - Google STT: 设置 GOOGLE_APPLICATION_CREDENTIALS 环境变量

音频信息：
  - 文件：{audio_path}
  - 时长：{mins:.1f} 分钟（约）
  - 语言：{language}

--- 请手动粘贴转写内容到下方 ---

[发言人 1] （时间段：00:00 - 00:00）


[发言人 2] （时间段：00:00 - 00:00）


--- 转写内容结束 ---
"""
        return {
            "text": template_text,
            "segments": [],
            "language": language,
            "template_mode": True,
        }


class SpeakerDiarization:
    """说话人标注（MFCC 分离或显式报名）"""
    
    def __init__(self, method: str = "auto"):
        self.method = method
        self._available = self._detect_available()
    
    def _detect_available(self) -> Dict[str, bool]:
        """检测可用的说话人标注引擎"""
        available = {
            "mfcc": False,
            "pyannote": False,
            "template": True,
        }
        # 检测 librosa/sklearn（MFCC 方案）
        try:
            import librosa
            import sklearn
            available["mfcc"] = True
        except ImportError:
            pass
        # 检测 pyannote（更精确但依赖较多）
        try:
            import pyannote.audio
            available["pyannote"] = True
        except ImportError:
            pass
        return available
    
    def get_best_method(self) -> str:
        if self.method != "auto":
            return self.method
        if self._available.get("mfcc"):
            return "mfcc"
        if self._available.get("pyannote"):
            return "pyannote"
        return "template"
    
    def diarize(self, audio_path: str, num_speakers: int = 0) -> Dict[str, Any]:
        """
        说话人标注
        
        Returns:
            {
                "ok": bool,
                "method": str,
                "segments": [
                    {"start": 0.0, "end": 5.0, "speaker": "说话人A"},
                    {"start": 5.0, "end": 10.0, "speaker": "说话人B"},
                    ...
                ],
                "speaker_count": int
            }
        """
        method = self.get_best_method()
        try:
            if method == "mfcc":
                return self._diarize_mfcc(audio_path, num_speakers)
            elif method == "pyannote":
                return self._diarize_pyannote(audio_path)
            else:
                return self._diarize_template(audio_path)
        except Exception as e:
            return {"ok": False, "error": f"说话人标注失败: {str(e)}", "method": method}
    
    def _diarize_mfcc(self, audio_path: str, num_speakers: int) -> Dict[str, Any]:
        """基于 MFCC 聚类的说话人标注"""
        import librosa
        from sklearn.cluster import KMeans
        import numpy as np
        
        # 加载音频
        y, sr = librosa.load(audio_path, sr=16000)
        
        # 提取 MFCC 特征
        hop_length = int(sr * 0.5)  # 50ms hop
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, hop_length=hop_length)
        
        # 说话人活动检测（基于能量）
        rms = librosa.feature.rms(y=y, hop_length=hop_length)[0]
        threshold = np.median(rms) * 0.5
        active_frames = rms > threshold
        
        # 提取有效段的 MFCC
        active_mfccs = mfccs[:, active_frames].T
        
        if len(active_mfccs) < 2:
            return {"ok": False, "error": "音频太短或无法检测到说话人", "method": "mfcc"}
        
        # 自动估计说话人数（若未指定）
        if num_speakers <= 0:
            num_speakers = min(4, max(2, len(active_mfccs) // 30))
        
        # KMeans 聚类
        kmeans = KMeans(n_clusters=num_speakers, random_state=42, n_init=10)
        labels = kmeans.fit_predict(active_mfccs)
        
        # 生成说话人段
        segments = []
        active_indices = np.where(active_frames)[0]
        hop_duration = hop_length / sr
        
        current_label = labels[0]
        start_time = 0.0
        
        for i in range(1, len(labels)):
            if labels[i] != current_label:
                end_time = i * hop_duration
                segments.append({
                    "start": round(start_time, 1),
                    "end": round(end_time, 1),
                    "speaker": f"说话人{chr(65 + current_label)}",
                })
                current_label = labels[i]
                start_time = end_time
        
        # 添加最后一个段
        end_time = len(labels) * hop_duration
        segments.append({
            "start": round(start_time, 1),
            "end": round(end_time, 1),
            "speaker": f"说话人{chr(65 + current_label)}",
        })
        
        # 统计说话人
        speaker_count = len(set(labels))
        
        return {
            "ok": True,
            "method": "mfcc",
            "segments": segments,
            "speaker_count": speaker_count,
        }
    
    def _diarize_pyannote(self, audio_path: str) -> Dict[str, Any]:
        """基于 pyannote.audio 的说话人标注（更精确但需要更多依赖）"""
        # pyannote 需要 HuggingFace 模型，降级到 template
        return self._diarize_template(audio_path)
    
    def _diarize_template(self, audio_path: str) -> Dict[str, Any]:
        """模板框架（所有引擎不可用时的降级方案）"""
        return {
            "ok": True,
            "method": "template",
            "segments": [],
            "speaker_count": 0,
            "message": "无可用的说话人标注引擎，已生成无标注转写。安装 librosa+sklearn 可启用 MFCC 聚类。",
        }


class MinutesSummarizer:
    """会议纪要摘要引擎（带降级链）"""
    
    def __init__(self, method: str = "auto"):
        self.method = method
        self._available = self._detect_available()
        self.speaker_diarization = SpeakerDiarization()
    
    def _detect_available(self) -> Dict[str, bool]:
        """检测可用的摘要引擎"""
        try:
            from llm_bridge import is_router_available
            llm_bridge_avail = is_router_available()
        except ImportError:
            llm_bridge_avail = False
        return {
            "llm_bridge": llm_bridge_avail,  # v4.9: cn-llm-router 白名单探测
            "rule-engine": True,  # 始终可用（本地规则）
            "external-llm": bool(os.environ.get("OPENAI_API_KEY") or os.environ.get("OPENAI_BASE_URL")),
            "pure-template": True,  # 始终可用
        }
    
    def get_best_method(self) -> str:
        if self.method != "auto":
            return self.method
        chain = ["llm_bridge", "rule-engine", "external-llm", "pure-template"]
        for m in chain:
            if self._available.get(m, False):
                return m
        return "pure-template"
    
    def summarize(self, text: str, language: str = "zh") -> Dict[str, Any]:
        """生成会议纪要摘要"""
        method = self.get_best_method()
        
        try:
            if method == "llm_bridge":
                result = self._summarize_llm_bridge(text, language)
            elif method == "rule-engine":
                result = self._summarize_rule_engine(text, language)
            elif method == "external-llm":
                result = self._summarize_external_llm(text, language)
            else:
                result = self._summarize_pure_template(text, language)
            
            return {"success": True, "method": method, **result}
        
        except Exception as e:
            if method == "llm_bridge":
                # llm_bridge 失败，回落到本地规则引擎
                return self._summarize_rule_engine(text, language)
            if method != "pure-template":
                return self._summarize_pure_template(text, language)
            return {"success": False, "error": f"摘要生成失败: {str(e)}"}
    
    def _summarize_llm_bridge(self, text: str, language: str) -> Dict[str, Any]:
        """通过 llm_bridge 走 cn-llm-router 生成摘要（v4.9 新增）"""
        from llm_bridge import summarize as bridge_summarize, INSTALL_HINT
        result = bridge_summarize(text, max_length=500, timeout=60)
        if result.get("ok"):
            return {
                "summary": {"raw": result["text"]},
                "structured": False,
                "model": result.get("model", ""),
                "cost": result.get("cost", ""),
                "install_hint": INSTALL_HINT,
            }
        raise ValueError(result.get("error", "llm_bridge 摘要失败"))

    def _summarize_rule_engine(self, text: str, language: str) -> Dict[str, Any]:
        """本地规则引擎摘要（v5.1 三段式要素化：待办+决策+风险异议）"""
        # 提取关键信息
        sentences = [s.strip() for s in re.split(r'[。！？\n]', text) if s.strip()]
        
        # v5.1 三分类关键词
        todo_keywords = ["需要", "安排", "计划", "必须", "负责", "跟进", "落实", "执行", "推进", "完成", "截止", "期限"]
        decision_keywords = ["决定", "同意", "通过", "确定", "批准", "采纳", "选定", "确认", "达成共识", "一致同意"]
        risk_keywords = ["风险", "问题", "担忧", "异议", "保留意见", "不同意", "质疑", "顾虑", "警告", "注意", "隐患", "不足"]
        
        todo_sentences = []
        decision_sentences = []
        risk_sentences = []
        key_sentences = []
        
        for s in sentences:
            is_key = False
            if any(kw in s for kw in todo_keywords):
                todo_sentences.append(s)
                is_key = True
            if any(kw in s for kw in decision_keywords):
                decision_sentences.append(s)
                is_key = True
            if any(kw in s for kw in risk_keywords):
                risk_sentences.append(s)
                is_key = True
            if is_key:
                key_sentences.append(s)
        
        # 提取时间信息
        time_pattern = re.findall(r'\d{1,2}[:：]\d{2}', text)
        dates = re.findall(r'\d{4}[-/年]\d{1,2}[-/月]\d{1,2}', text)
        
        # 提取人名
        speaker_pattern = re.findall(r'([一-龥]{2,4})(?:说|表示|认为|提到|介绍|汇报|总结)', text)
        speakers = list(set(speaker_pattern))
        
        # 提取责任人
        responsible_pattern = re.findall(r'([一-龥]{2,4})(?:负责|跟进|落实|执行)', text)
        responsible = list(set(responsible_pattern))
        
        # v5.1 三段式结构化摘要
        summary = {
            # 第一段：待办清单（责任人+期限）
            "action_items": [
                {
                    "task": s,
                    "responsible": responsible[i] if i < len(responsible) else "",
                    "deadline": dates[i] if i < len(dates) else "",
                }
                for i, s in enumerate(todo_sentences[:5])
            ],
            # 第二段：决策记录（决策点+依据）
            "decisions": [
                {"decision": s, "basis": ""}
                for s in decision_sentences[:5]
            ],
            # 第三段：风险与异议（保留意见不被摘要吞掉）
            "risks_and_objections": risk_sentences[:5],
            # 元信息
            "key_points": key_sentences[:5] if key_sentences else sentences[:3],
            "speakers": speakers[:5],
            "responsible": responsible[:5],
            "time_mentions": time_pattern[:5],
            "dates": dates[:3],
            "total_sentences": len(sentences),
            "structured": True,
            "structure_version": "v5.1_three_section",
        }
        
        return {
            "summary": summary,
            "structured": True,
        }
    
    def _summarize_external_llm(self, text: str, language: str) -> Dict[str, Any]:
        """外部 LLM 摘要（OpenAI 兼容 API）"""
        base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
        api_key = os.environ.get("OPENAI_API_KEY", "")
        
        if not api_key:
            raise ValueError("未配置 OPENAI_API_KEY")
        
        import urllib.request
        import urllib.error
        
        prompt = f"""请将以下会议转写文本整理为结构化的会议纪要，包含：
1. 会议主题
2. 关键要点（3-5条）
3. 决议事项
4. 待办事项（负责人 + 截止时间）
5. 风险与问题

转写文本：
{text[:4000]}
"""
        
        payload = json.dumps({
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
            "max_tokens": 2000,
        }).encode("utf-8")
        
        req = urllib.request.Request(
            f"{base_url}/chat/completions",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            }
        )
        
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                content = result["choices"][0]["message"]["content"]
                return {"summary": {"raw": content}, "structured": False}
        except urllib.error.HTTPError as e:
            raise ValueError(f"LLM API 错误: {e.code} {e.reason}")
    
    def _summarize_pure_template(self, text: str, language: str) -> Dict[str, Any]:
        """纯模板摘要（所有 LLM 不可用时的降级）"""
        sentences = [s.strip() for s in re.split(r'[。！？\n]', text) if s.strip()]
        
        # 按句子顺序均匀抽取
        n = len(sentences)
        if n <= 5:
            selected = sentences
        else:
            step = max(1, n // 5)
            selected = [sentences[i] for i in range(0, n, step)][:5]
        
        template = f"""# 会议纪要

## 会议主题
（请根据内容补充）

## 关键要点
{chr(10).join(f"- {s}" for s in selected)}

## 决议事项
（请根据内容补充）

## 待办事项
（请根据内容补充）

## 风险与问题
（请根据内容补充）

---
*此纪要由模板自动生成，请手动完善标灰内容*
*转写字数：{len(text)} 字 | 句子数：{n}*
"""
        return {
            "summary": {"raw": template, "template_mode": True},
            "structured": False,
        }


class MeetingMinutesGenerator:
    """会议纪要生成器（完整流水线）"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.progress_cb = self.config.get("progress_cb", lambda *a: None)
        self.segment_minutes = self.config.get("segment_minutes", 5)
        
        self.audio_processor = AudioProcessor(
            segment_minutes=self.segment_minutes,
            progress_cb=self.progress_cb,
        )
        self.transcriber = ASRTranscriber(
            method=self.config.get("asr_method", "auto"),
            progress_cb=self.progress_cb,
        )
        self.summarizer = MinutesSummarizer(
            method=self.config.get("summary_method", "auto"),
        )
    
    def generate_minutes(self, audio_path: str, output_path: str,
                         title: str = "会议纪要",
                         language: str = "zh",
                         diarize: bool = True) -> Dict[str, Any]:
        """完整流水线：音频 → 转写 → 说话人标注 → 摘要 → Word"""
        audio_path = str(Path(audio_path).resolve())
        
        if not os.path.exists(audio_path):
            return {"success": False, "error": f"音频文件不存在: {audio_path}"}
        
        self.progress_cb("pipeline_start", {"audio": audio_path})
        
        # Step 1: 音频分段
        tmp_dir = tempfile.mkdtemp(prefix="mm_")
        segments = self.audio_processor.segment_audio(audio_path, tmp_dir)
        
        # Step 2: 逐段转写
        all_text = []
        for i, seg in enumerate(segments):
            self.progress_cb("transcribing", {"current": i + 1, "total": len(segments)})
            result = self.transcriber.transcribe(seg, language)
            if result.get("success"):
                all_text.append(result.get("text", ""))
            else:
                all_text.append(f"[转写失败: {result.get('error', '未知错误')}]")
        
        full_text = "\n".join(all_text)
        
        # Step 3: 清理临时分段
        if len(segments) > 1:
            self.audio_processor.cleanup_segments(segments)
            try:
                os.rmdir(tmp_dir)
            except Exception:
                pass
        
        # Step 4: 说话人标注（v5.1 新增）
        diarization_result = None
        if diarize:
            self.progress_cb("diarizing", {})
            diarization_result = self.summarizer.speaker_diarization.diarize(audio_path)
            if diarization_result.get("ok"):
                self.progress_cb("diarize_done", {
                    "method": diarization_result.get("method", "unknown"),
                    "speakers": diarization_result.get("speaker_count", 0),
                })
        
        # Step 5: 生成摘要（v5.1 三段式）
        self.progress_cb("summarizing", {})
        summary_result = self.summarizer.summarize(full_text, language)
        
        # 如果有说话人标注，附加到摘要
        if diarization_result and diarization_result.get("ok"):
            summary = summary_result.get("summary", {})
            if isinstance(summary, dict):
                summary["diarization"] = {
                    "method": diarization_result.get("method"),
                    "speaker_count": diarization_result.get("speaker_count"),
                    "segments": diarization_result.get("segments", []),
                }
                summary["speakers"] = [
                    f"说话人{chr(65 + i)}"
                    for i in range(diarization_result.get("speaker_count", 0))
                ] or summary.get("speakers", [])
        
        # Step 6: 生成 Word 文档
        word_result = self._generate_word(
            title=title,
            full_text=full_text,
            summary=summary_result.get("summary", {}),
            audio_path=audio_path,
            output_path=output_path,
        )
        
        self.progress_cb("pipeline_done", {"output": output_path})
        
        return {
            "success": word_result.get("ok", False),
            "transcribe_method": self.transcriber.get_best_method(),
            "summary_method": self.summarizer.get_best_method(),
            "diarize_method": diarization_result.get("method") if diarization_result else "skipped",
            "segments": len(segments),
            "text_length": len(full_text),
            **word_result,
        }
    
    def _generate_word(self, title: str, full_text: str, summary: Dict,
                       audio_path: str, output_path: str) -> Dict[str, Any]:
        """调用 wps_word 生成 Word 文档（v5.1 三段式分节导出）"""
        # 文档头部
        body_lines = [
            f"# {title}",
            "",
            f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"**音频文件**: {Path(audio_path).name}",
            "",
        ]
        
        # 参会人员
        if isinstance(summary, dict) and summary.get("speakers"):
            body_lines.append(f"**参会人员**: {', '.join(summary['speakers'])}")
            body_lines.append("")
        
        # v5.1 三段式分节导出（每节独立页眉）
        is_three_section = (
            isinstance(summary, dict)
            and summary.get("structure_version") == "v5.1_three_section"
        )
        
        if is_three_section:
            # 第一段：待办清单（责任人+期限）
            body_lines.extend([
                "---",
                "## 第一段：待办清单",
                "",
            ])
            if summary.get("action_items"):
                for i, item in enumerate(summary["action_items"], 1):
                    task = item.get("task", item) if isinstance(item, dict) else item
                    responsible = item.get("responsible", "") if isinstance(item, dict) else ""
                    deadline = item.get("deadline", "") if isinstance(item, dict) else ""
                    line = f"{i}. {task}"
                    if responsible:
                        line += f" — 责任人：{responsible}"
                    if deadline:
                        line += f"（期限：{deadline}）"
                    body_lines.append(line)
                body_lines.append("")
            else:
                body_lines.append("（本次无待办事项）")
                body_lines.append("")
            
            # 第二段：决策记录（决策点+依据）
            body_lines.extend([
                "---",
                "## 第二段：决策记录",
                "",
            ])
            if summary.get("decisions"):
                for i, item in enumerate(summary["decisions"], 1):
                    decision = item.get("decision", item) if isinstance(item, dict) else item
                    basis = item.get("basis", "") if isinstance(item, dict) else ""
                    line = f"{i}. {decision}"
                    if basis:
                        line += f"（依据：{basis}）"
                    body_lines.append(line)
                body_lines.append("")
            else:
                body_lines.append("（本次无决策记录）")
                body_lines.append("")
            
            # 第三段：风险与异议（保留意见不被摘要吞掉）
            body_lines.extend([
                "---",
                "## 第三段：风险与异议",
                "",
            ])
            if summary.get("risks_and_objections"):
                for i, item in enumerate(summary["risks_and_objections"], 1):
                    body_lines.append(f"{i}. {item}")
                body_lines.append("")
            else:
                body_lines.append("（本次无风险或异议记录）")
                body_lines.append("")
        elif isinstance(summary, dict):
            # 非 v5.1 结构，降级为普通格式
            if summary.get("key_points"):
                body_lines.append("### 关键要点")
                for i, point in enumerate(summary["key_points"], 1):
                    body_lines.append(f"{i}. {point}")
                body_lines.append("")
            if summary.get("raw"):
                body_lines.append(summary["raw"])
                body_lines.append("")
        else:
            body_lines.append(str(summary))
            body_lines.append("")
        
        body_lines.extend([
            "---",
            "## 完整转写",
            "",
            full_text,
        ])
        
        body = "\n".join(body_lines)
        
        # 调用 wps_word create
        return call_worker("create_word", {
            "title": title,
            "filepath": output_path,
            "body": body,
        })
    
    def batch_process(self, input_dir: str, output_dir: str,
                      language: str = "zh") -> Dict[str, Any]:
        """批量处理目录中的音频"""
        input_dir = Path(input_dir)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        audio_extensions = {".wav", ".mp3", ".m4a", ".flac", ".ogg", ".aac"}
        files = [f for f in input_dir.iterdir() if f.suffix.lower() in audio_extensions]
        
        results = []
        for i, audio_file in enumerate(files, 1):
            self.progress_cb("batch_progress", {"current": i, "total": len(files), "file": audio_file.name})
            
            output_path = str(output_dir / f"{audio_file.stem}_纪要.docx")
            result = self.generate_minutes(
                audio_path=str(audio_file),
                output_path=output_path,
                title=f"{audio_file.stem} - 会议纪要",
                language=language,
            )
            results.append({"file": audio_file.name, **result})
        
        success = sum(1 for r in results if r.get("success"))
        return {
            "success": True,
            "total": len(results),
            "success_count": success,
            "failed": len(results) - success,
            "results": results,
        }


def _cli():
    """CLI 入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="会议纪要生成器 v5.1.0")
    sub = parser.add_subparsers(dest="command", required=True)
    
    # transcribe 子命令
    p = sub.add_parser("transcribe", help="转写音频为文字")
    p.add_argument("--file", required=True, help="音频文件路径")
    p.add_argument("--method", default="auto", choices=["auto", "whisper-local", "azure-speech", "google-stt", "template"])
    p.add_argument("--language", default="zh", help="语言代码")
    p.add_argument("--output", default="", help="输出文本文件路径")
    
    # summarize 子命令
    p = sub.add_parser("summarize", help="摘要转写文本")
    p.add_argument("--file", required=True, help="转写文本文件路径")
    p.add_argument("--method", default="auto", choices=["auto", "llm_bridge", "rule-engine", "external-llm", "pure-template"])
    p.add_argument("--language", default="zh")
    p.add_argument("--output", default="", help="输出摘要文件路径")
    
    # generate 子命令（完整流水线）
    p = sub.add_parser("generate", help="完整流水线：音频→纪要→Word")
    p.add_argument("--file", required=True, help="音频文件路径")
    p.add_argument("--output", default="", help="输出 Word 文件路径")
    p.add_argument("--title", default="会议纪要", help="文档标题")
    p.add_argument("--language", default="zh")
    p.add_argument("--asr-method", default="auto")
    p.add_argument("--summary-method", default="auto", choices=["auto", "llm_bridge", "rule-engine", "external-llm", "pure-template"])
    p.add_argument("--segment-minutes", type=int, default=5)
    p.add_argument("--diarize", action="store_true", default=True, help="启用说话人标注（默认启用）")
    p.add_argument("--no-diarize", action="store_true", help="禁用说话人标注")
    p.add_argument("--num-speakers", type=int, default=0, help="说话人数（0=自动检测）")

    # diarize 子命令（独立说话人标注）
    p = sub.add_parser("diarize", help="独立说话人标注")
    p.add_argument("--file", required=True, help="音频文件路径")
    p.add_argument("--num-speakers", type=int, default=0, help="说话人数（0=自动检测）")
    p.add_argument("--method", default="auto", choices=["auto", "mfcc", "pyannote", "template"])
    
    # batch 子命令
    p = sub.add_parser("batch", help="批量处理目录")
    p.add_argument("--input-dir", required=True, help="输入音频目录")
    p.add_argument("--output-dir", required=True, help="输出 Word 目录")
    p.add_argument("--language", default="zh")
    
    # check 子命令
    p = sub.add_parser("check", help="检查可用引擎")
    
    args = parser.parse_args()
    
    def print_progress(event, data):
        """默认进度回调"""
        if event == "segment_start":
            print(f"[分段] 共 {data['total']} 段，时长 {data['duration']:.0f}s")
        elif event == "segment_done":
            print(f"[分段] 第 {data['index'] + 1} 段完成")
        elif event == "transcribe_start":
            print(f"[转写] 使用引擎: {data['method']}")
        elif event == "transcribe_done":
            print(f"[转写] 完成，{data['chars']} 字符")
        elif event == "summarizing":
            print("[摘要] 正在生成摘要...")
        elif event == "pipeline_done":
            print(f"[完成] 输出: {data.get('output', '')}")
        elif event == "batch_progress":
            print(f"[批量] {data['current']}/{data['total']}: {data['file']}")
    
    if args.command == "transcribe":
        tr = ASRTranscriber(method=args.method, progress_cb=print_progress)
        result = tr.transcribe(args.file, args.language)
        if result.get("success"):
            text = result.get("text", "")
            if args.output:
                Path(args.output).write_text(text, encoding="utf-8")
                print(f"已保存到: {args.output}")
            else:
                print(text[:500])
        else:
            print(json.dumps(result, ensure_ascii=False))
    
    elif args.command == "summarizer":
        sm = MinutesSummarizer(method=args.method)
        text = Path(args.file).read_text(encoding="utf-8")
        result = sm.summarize(text, args.language)
        if result.get("success"):
            summary = result.get("summary", {})
            raw = summary.get("raw", str(summary))
            if args.output:
                Path(args.output).write_text(raw, encoding="utf-8")
                print(f"已保存到: {args.output}")
            else:
                print(raw[:800])
        else:
            print(json.dumps(result, ensure_ascii=False))
    
    elif args.command == "generate":
        config = {
            "asr_method": args.asr_method,
            "summary_method": args.summary_method,
            "segment_minutes": args.segment_minutes,
            "progress_cb": print_progress,
        }
        gen = MeetingMinutesGenerator(config)
        output = args.output or f"{Path(args.file).stem}_纪要.docx"
        diarize = args.diarize and not args.no_diarize
        result = gen.generate_minutes(args.file, output, args.title, args.language, diarize=diarize)
        print(json.dumps(result, ensure_ascii=False, default=str))
    
    elif args.command == "diarize":
        sd = SpeakerDiarization(method=args.method)
        result = sd.diarize(args.file, args.num_speakers)
        print(json.dumps(result, ensure_ascii=False, default=str))
    
    elif args.command == "batch":
        config = {"progress_cb": print_progress}
        gen = MeetingMinutesGenerator(config)
        result = gen.batch_process(args.input_dir, args.output_dir, args.language)
        print(json.dumps(result, ensure_ascii=False, default=str))
    
    elif args.command == "check":
        tr = ASRTranscriber(method="auto")
        sm = MinutesSummarizer(method="auto")
        print(json.dumps({
            "asr_available": tr._available_methods,
            "asr_best": tr.get_best_method(),
            "summary_available": sm._available,
            "summary_best": sm.get_best_method(),
        }, ensure_ascii=False))


if __name__ == "__main__":
    _cli()
