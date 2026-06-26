import os
import re
import time
import subprocess
from abc import ABC, abstractmethod
import soundfile as sf
import numpy as np

# ==========================================
# 0. 长文本断句切片工具 (Sentence Chunker)
# ==========================================

def _env_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except Exception:
        return default

# 单次推理的安全字符上限。超过此值的文本将被自动切片。
# 为提升稳定性，默认设为 50；可通过 TTS_MAX_CHUNK_CHARS 覆盖。
MAX_CHUNK_CHARS = max(20, _env_int("TTS_MAX_CHUNK_CHARS", 50))
STITCH_CROSSFADE_MS = max(0, _env_int("TTS_STITCH_CROSSFADE_MS", 80))
MAX_EDGE_TRIM_MS = max(0, _env_int("TTS_MAX_EDGE_TRIM_MS", 350))
SILENCE_THRESHOLD = 2e-4

def split_text_to_chunks(text: str, max_chars: int = MAX_CHUNK_CHARS) -> list:
    """
    将长文本按照自然语言的断句位置切片为数组。
    切片优先级：句号/叹号/问号 > 分号/冒号 > 逗号 > 空格强制截断。
    每个切片的长度不超过 max_chars。
    """
    text = re.sub(r"\s+", " ", text).strip()

    if len(text) <= max_chars:
        return [text]

    # 第一步：按句末标点分割
    # 匹配中英文句号、叹号、问号、分号
    sentences = re.split(r'(?<=[。！？.!?；;])', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        # 如果当前累积 + 新句子仍能容纳，则拼入
        if len(current_chunk) + len(sentence) <= max_chars:
            current_chunk += sentence
        else:
            # 先把已累积的存档
            if current_chunk:
                chunks.append(current_chunk)
            # 如果单个句子本身就超长，对它进行二次切割（按逗号）
            if len(sentence) > max_chars:
                sub_parts = re.split(r'(?<=[，,、])', sentence)
                sub_chunk = ""
                for part in sub_parts:
                    if len(sub_chunk) + len(part) <= max_chars:
                        sub_chunk += part
                    else:
                        if sub_chunk:
                            chunks.append(sub_chunk)
                        # 如果逗号切片后仍然超长，强行按字数截断
                        while len(part) > max_chars:
                            chunks.append(part[:max_chars])
                            part = part[max_chars:]
                        sub_chunk = part
                if sub_chunk:
                    current_chunk = sub_chunk
                else:
                    current_chunk = ""
            else:
                current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


# ==========================================
# 1. 引擎通用基类定义
# ==========================================
class BaseTTSEngine(ABC):
    # 子类如果原生支持 speed 参数，应设为 True
    NATIVE_SPEED_SUPPORT = False

    def __init__(self, model_dir: str):
        self.model_dir = model_dir
        self.device = self._get_optimal_device()
        self.model = None
        self.vocoder = None

    def _get_optimal_device(self) -> str:
        forced_device = os.getenv("TTS_DEVICE", "").strip().lower()
        if forced_device in {"cpu", "cuda", "mps"}:
            return forced_device

        try:
            import torch
            if torch.cuda.is_available():
                return "cuda"
            elif torch.backends.mps.is_available():
                # F5-TTS 在部分 Apple MPS 场景下对长文本不稳定，默认关闭 MPS。
                if os.getenv("TTS_ENABLE_MPS", "0").lower() in {"1", "true", "yes", "on"}:
                    return "mps"
                print("[BaseTTSEngine] 检测到 MPS，但默认使用 CPU 以保证长文本稳定性（可设 TTS_ENABLE_MPS=1 手动开启）")
        except ImportError:
            pass
        return "cpu"

    @staticmethod
    def _apply_speed_ffmpeg(audio: np.ndarray, sample_rate: int, speed: float) -> np.ndarray:
        """
        对不原生支持语速的引擎，通过 ffmpeg atempo 滤镜做后处理变速。
        speed > 1.0 加速，< 1.0 减速。ffmpeg atempo 范围 [0.5, 100.0]。
        """
        if abs(speed - 1.0) < 0.01:
            return audio

        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f_in:
            in_path = f_in.name
        out_path = in_path + "_speed.wav"

        sf.write(in_path, audio, sample_rate)

        # ffmpeg atempo 范围 [0.5, 100.0]，超出需要链式叠加
        atempo_val = max(0.5, min(speed, 100.0))
        subprocess.run(
            ["ffmpeg", "-y", "-i", in_path, "-filter:a", f"atempo={atempo_val}", out_path],
            capture_output=True
        )

        if os.path.exists(out_path):
            result, _ = sf.read(out_path)
            os.unlink(in_path)
            os.unlink(out_path)
            return result
        else:
            os.unlink(in_path)
            return audio

    @staticmethod
    def _normalize_audio_array(audio) -> np.ndarray:
        """
        将模型输出统一压平为 1D float32，修正长文本分片中常见的形状不一致问题。
        """
        arr = np.asarray(audio)

        if arr.size == 0:
            return np.array([], dtype=np.float32)

        if arr.ndim == 2:
            if arr.shape[0] == 1:
                arr = arr[0]
            elif arr.shape[1] == 1:
                arr = arr[:, 0]
            elif arr.shape[1] == 2:
                arr = arr.mean(axis=1)
            else:
                arr = arr.reshape(-1)
        elif arr.ndim > 2:
            arr = arr.reshape(-1)

        arr = np.nan_to_num(arr.astype(np.float32), nan=0.0, posinf=0.0, neginf=0.0)
        return arr

    @staticmethod
    def _trim_edge_silence(audio: np.ndarray, sample_rate: int) -> np.ndarray:
        """
        裁剪片段首尾过长静音（最多各裁剪 MAX_EDGE_TRIM_MS），避免长文本片段拼接出现“卡顿空档”。
        """
        if audio.size == 0:
            return audio

        non_silent = np.flatnonzero(np.abs(audio) > SILENCE_THRESHOLD)
        if non_silent.size == 0:
            return audio

        max_trim_samples = int(sample_rate * MAX_EDGE_TRIM_MS / 1000.0)
        if max_trim_samples <= 0:
            return audio

        # 保留一点缓冲，避免截断爆破音
        pad = int(sample_rate * 0.01)
        start = max(0, non_silent[0] - pad)
        end = min(len(audio), non_silent[-1] + 1 + pad)

        # 每侧最多裁剪 max_trim_samples，避免过度裁剪自然停顿
        start = min(start, max_trim_samples)
        end = max(end, len(audio) - max_trim_samples)
        return audio[start:end]

    @staticmethod
    def _stitch_segments(segments: list, sample_rate: int) -> np.ndarray:
        """
        交叉淡化拼接各片段，减少分片连接点的爆音/断裂。
        """
        if not segments:
            return np.array([], dtype=np.float32)

        out = segments[0]
        crossfade_samples = int(sample_rate * STITCH_CROSSFADE_MS / 1000.0)

        for seg in segments[1:]:
            if out.size == 0:
                out = seg
                continue
            if seg.size == 0:
                continue

            n = min(crossfade_samples, len(out), len(seg))
            if n <= 0:
                out = np.concatenate([out, seg])
                continue

            fade_out = np.linspace(1.0, 0.0, n, endpoint=False, dtype=np.float32)
            fade_in = np.linspace(0.0, 1.0, n, endpoint=False, dtype=np.float32)
            blended = out[-n:] * fade_out + seg[:n] * fade_in
            out = np.concatenate([out[:-n], blended, seg[n:]])

        return out

    def _recover_from_chunk_error(self, error: Exception) -> bool:
        """
        子类可覆盖：在 chunk 推理异常后尝试自愈（例如重置模型）。
        返回 True 表示已执行恢复，可立即重试当前 chunk。
        """
        return False

    def _synthesize_chunk_with_fallback(
        self,
        text: str,
        ref_audio: str,
        speed: float,
        depth: int = 0
    ) -> list:
        """
        某个 chunk 推理失败时，自动递归二次切片重试，提升长文本成功率。
        返回 [(audio_segment, sample_rate), ...]
        """
        try:
            audio_seg, sr = self.synthesize_chunk(text, ref_audio, speed)
            if not self.NATIVE_SPEED_SUPPORT and abs(speed - 1.0) >= 0.01:
                audio_seg = self._apply_speed_ffmpeg(audio_seg, sr, speed)
            return [(audio_seg, sr)]
        except Exception as e:
            if depth <= 1 and self._recover_from_chunk_error(e):
                try:
                    audio_seg, sr = self.synthesize_chunk(text, ref_audio, speed)
                    if not self.NATIVE_SPEED_SUPPORT and abs(speed - 1.0) >= 0.01:
                        audio_seg = self._apply_speed_ffmpeg(audio_seg, sr, speed)
                    return [(audio_seg, sr)]
                except Exception as recovered_e:
                    e = recovered_e

            min_retry_chars = 35
            max_retry_depth = 4
            if len(text) <= min_retry_chars or depth >= max_retry_depth:
                raise RuntimeError(f"chunk 重试失败，depth={depth}, text_len={len(text)}: {e}") from e

            next_max_chars = max(min_retry_chars, len(text) // 2)
            retry_chunks = split_text_to_chunks(text, max_chars=next_max_chars)
            if len(retry_chunks) <= 1:
                mid = len(text) // 2
                retry_chunks = [text[:mid], text[mid:]]

            print(
                f"[BaseTTSEngine] chunk 失败，自动二次切片重试 "
                f"(depth={depth + 1}, {len(text)} -> {len(retry_chunks)} 段, error={e})"
            )

            merged = []
            for sub in retry_chunks:
                sub = sub.strip()
                if not sub:
                    continue
                merged.extend(self._synthesize_chunk_with_fallback(sub, ref_audio, speed, depth + 1))
            return merged

    @abstractmethod
    def load(self):
        """将模型重度权重从 self.model_dir 载入 self.device 显存以常驻"""
        pass

    @abstractmethod
    def synthesize_chunk(self, text: str, ref_audio: str, speed: float = 1.0):
        """
        单次推理一个短句。
        返回: (np.ndarray audio_segment, int sample_rate)
        """
        pass

    def synthesize(self, text: str, ref_audio: str, output_path: str, speed: float = 1.0) -> bool:
        """
        完整合成：自动对长文本分片、逐一推理、拼接后转码输出。
        所有子类共享此逻辑，子类只需实现 synthesize_chunk。
        """
        chunks = split_text_to_chunks(text)
        print(f"[BaseTTSEngine] 文本共 {len(text)} 字，切分为 {len(chunks)} 个片段")

        all_segments = []
        sample_rate = None

        for i, chunk in enumerate(chunks):
            print(f"  [{i+1}/{len(chunks)}] 推理中: '{chunk[:40]}...'")
            chunk_segments = self._synthesize_chunk_with_fallback(chunk, ref_audio, speed)

            for audio_seg, sr in chunk_segments:
                audio_seg = self._normalize_audio_array(audio_seg)
                audio_seg = self._trim_edge_silence(audio_seg, sr)

                if audio_seg.size == 0:
                    print(f"  [{i+1}/{len(chunks)}] 警告：该片段生成结果为空，已跳过")
                    continue

                if sample_rate is None:
                    sample_rate = sr
                elif sr != sample_rate:
                    raise RuntimeError(f"采样率不一致: chunk_sr={sr}, expected_sr={sample_rate}")

                all_segments.append(audio_seg)

        if not all_segments or sample_rate is None:
            raise RuntimeError("所有文本片段都未生成有效音频")

        # 拼接所有片段
        final_wave = self._stitch_segments(all_segments, sample_rate)

        # 写入中间 WAV
        tmp_wav = output_path.replace(".ogg", ".wav")
        sf.write(tmp_wav, final_wave, sample_rate)

        # 转码为 ogg/opus (Telegram 等平台友好格式)
        print(f"[BaseTTSEngine] 正在用 ffmpeg 压制为 {output_path}...")
        subprocess.run(
            ["ffmpeg", "-y", "-i", tmp_wav, "-c:a", "libopus", "-b:a", "48k", output_path],
            capture_output=True
        )

        if os.path.exists(tmp_wav):
            os.remove(tmp_wav)

        return os.path.exists(output_path)


# ==========================================
# 2. F5-TTS 引擎
# ==========================================
class F5TTSEngine(BaseTTSEngine):
    NATIVE_SPEED_SUPPORT = True  # F5-TTS 原生支持 speed 参数

    def load(self):
        print(f"[F5TTSEngine] 分配计算单元: {self.device}")

        from f5_tts.infer.utils_infer import load_model, load_vocoder
        from importlib.resources import files
        from omegaconf import OmegaConf
        from hydra.utils import get_class
        from cached_path import cached_path

        # 1. 加载 Vocoder
        print("[F5TTSEngine] 正在加载 Vocoder (Vocos)...")
        self.vocoder = load_vocoder(vocoder_name="vocos", is_local=False, local_path="", device=self.device)

        # 2. 准备 F5-TTS Base 模型的配置
        model_name = "F5TTS_Base"
        config_path = str(files("f5_tts").joinpath(f"configs/{model_name}.yaml"))
        model_cfg = OmegaConf.load(config_path)
        model_cls = get_class(f"f5_tts.model.{model_cfg.model.backbone}")
        model_arc = model_cfg.model.arch

        # 3. Checkpoint 自动下载至被拦截的 HF_HOME
        ckpt_step = 1200000
        ckpt_file = str(cached_path(f"hf://SWivid/F5-TTS/{model_name}/model_{ckpt_step}.safetensors"))

        print(f"[F5TTSEngine] 正在将 {model_name} 的 1.5GB DiT 权重挂载至 {self.device}...")
        self.model = load_model(
            model_cls, model_arc, ckpt_file,
            mel_spec_type="vocos", vocab_file="", device=self.device
        )
        print("[F5TTSEngine] 成功挂载权重！")

        # 缓存预处理后的参考音频，避免每个 chunk 反复提取
        self._cached_ref = {}
        self._mps_fallback_done = False
        if not hasattr(self, "_auto_reset_count"):
            self._auto_reset_count = 0

    def _fallback_mps_to_cpu(self, reason: Exception) -> bool:
        """
        F5 在部分 Apple MPS 场景下长文本会触发 tensor shape mismatch。
        发生后自动切换到 CPU 重试，优先保证可用性。
        """
        if self.device != "mps" or self._mps_fallback_done:
            return False

        print(f"[F5TTSEngine] 检测到 MPS 推理异常，切换 CPU 重试。原因: {reason}")
        try:
            if hasattr(self.model, "to"):
                self.model = self.model.to("cpu")
            if hasattr(self.vocoder, "to"):
                self.vocoder = self.vocoder.to("cpu")
            self.device = "cpu"
            self._mps_fallback_done = True
            return True
        except Exception as e:
            print(f"[F5TTSEngine] 切换 CPU 失败: {e}")
            return False

    def _recover_from_chunk_error(self, error: Exception) -> bool:
        msg = str(error)
        if "Sizes of tensors must match" not in msg:
            return False

        max_resets = max(1, _env_int("TTS_F5_MAX_AUTO_RESET", 4))
        if self._auto_reset_count >= max_resets:
            return False

        self._auto_reset_count += 1
        print(
            f"[F5TTSEngine] 检测到不稳定张量错误，执行自动热重载恢复 "
            f"({self._auto_reset_count}/{max_resets})"
        )
        self.load()
        return True

    def _get_ref(self, ref_audio: str):
        """缓存参考音频的预处理结果"""
        if ref_audio not in self._cached_ref:
            from f5_tts.infer.utils_infer import preprocess_ref_audio_text
            ref_audio_proc, ref_text_proc = preprocess_ref_audio_text(ref_audio, "")
            self._cached_ref[ref_audio] = (ref_audio_proc, ref_text_proc)
        return self._cached_ref[ref_audio]

    def synthesize_chunk(self, text: str, ref_audio: str, speed: float = 1.0):
        from f5_tts.infer.utils_infer import infer_process

        ref_audio_proc, ref_text_proc = self._get_ref(ref_audio)

        def _run_once():
            return infer_process(
                ref_audio_proc, ref_text_proc, text,
                self.model, self.vocoder,
                mel_spec_type="vocos",
                target_rms=0.1,
                cross_fade_duration=0.15,
                nfe_step=32,
                cfg_strength=2.0,
                sway_sampling_coef=-1.0,
                speed=speed,
                fix_duration=None,
                device=self.device
            )

        try:
            audio_segment, final_sample_rate, _ = _run_once()
            return audio_segment, final_sample_rate
        except RuntimeError as e:
            msg = str(e)
            if "Sizes of tensors must match" in msg and self._fallback_mps_to_cpu(e):
                audio_segment, final_sample_rate, _ = _run_once()
                return audio_segment, final_sample_rate
            raise


# ==========================================
# 3. CosyVoice 引擎 (阿里通义实验室)
# ==========================================
class CosyVoiceEngine(BaseTTSEngine):
    """
    依赖：需要先用 scripts/install_cosyvoice.sh 安装。
    核心库: cosyvoice (从 github 克隆并 pip install -e .)
    模型: CosyVoice2-0.5B (~1.5GB)
    """
    def load(self):
        print(f"[CosyVoiceEngine] 分配计算单元: {self.device}")

        try:
            from cosyvoice.cli.cosyvoice import CosyVoice2
        except ImportError:
            raise ImportError(
                "[CosyVoiceEngine] 缺少 cosyvoice 库！\n"
                "请先运行: bash scripts/install_cosyvoice.sh\n"
                "该脚本会自动克隆源码并安装依赖。"
            )

        model_path = os.path.join(self.model_dir, "CosyVoice2-0.5B")
        if not os.path.exists(model_path):
            # 自动从 HuggingFace/ModelScope 下载模型
            print(f"[CosyVoiceEngine] 模型目录不存在，尝试从远端拉取至 {model_path}...")
            model_path = "iic/CosyVoice2-0.5B"  # 会自动下载到 MODELSCOPE_CACHE

        print(f"[CosyVoiceEngine] 正在加载 CosyVoice2-0.5B...")
        self.model = CosyVoice2(model_path, load_jit=False, load_onnx=False, load_trt=False)
        print("[CosyVoiceEngine] 模型加载完毕！")

    def synthesize_chunk(self, text: str, ref_audio: str, speed: float = 1.0):
        from cosyvoice.utils.file_utils import load_wav
        import torch

        prompt_speech_16k = load_wav(ref_audio, 16000)
        # CosyVoice 的零样本推理需要参考音频的文字转录
        # 此处留空让它内部处理（或者后续集成 whisper 转录）
        prompt_text = ""

        all_audio = []
        for result in self.model.inference_zero_shot(prompt_text, text, prompt_speech_16k, stream=False):
            audio_tensor = result['tts_speech']
            if isinstance(audio_tensor, torch.Tensor):
                audio_tensor = audio_tensor.cpu().numpy()
            if audio_tensor.ndim > 1:
                audio_tensor = audio_tensor.squeeze()
            all_audio.append(audio_tensor)

        audio = np.concatenate(all_audio) if all_audio else np.array([])
        return audio, 24000


# ==========================================
# 4. ChatTTS 引擎 (2noise)
# ==========================================
class ChatTTSEngine(BaseTTSEngine):
    """
    依赖：需要先用 scripts/install_chattts.sh 安装。
    核心库: ChatTTS (从 github 克隆)
    特性: 极强的对话韵律控制，支持 [laugh] [uv_break] 等标记。
    """
    def load(self):
        print(f"[ChatTTSEngine] 分配计算单元: {self.device}")

        try:
            import ChatTTS
        except ImportError:
            raise ImportError(
                "[ChatTTSEngine] 缺少 ChatTTS 库！\n"
                "请先运行: bash scripts/install_chattts.sh\n"
                "该脚本会自动克隆源码并安装依赖。"
            )

        self.model = ChatTTS.Chat()
        self.model.load(compile=False)  # compile=True 需要较新的 torch
        print("[ChatTTSEngine] 模型加载完毕！")

    def synthesize_chunk(self, text: str, ref_audio: str, speed: float = 1.0):
        import torch

        wavs = self.model.infer([text])
        audio = wavs[0]
        if isinstance(audio, torch.Tensor):
            audio = audio.cpu().numpy()
        if audio.ndim > 1:
            audio = audio.squeeze()
        return audio, 24000


# ==========================================
# 5. OpenVoice V2 引擎 (MyShell)
# ==========================================
class OpenVoiceEngine(BaseTTSEngine):
    """
    依赖：需要先用 scripts/install_openvoice.sh 安装。
    核心库: openvoice (从 github 克隆并 pip install -e .)
    模型: checkpoints_v2 (~300MB)
    特性: 体积极小速度极快，但克隆拟真度低于 F5/CosyVoice。
          工作原理是 "基础TTS生成 + 音色转换" 两步走。
    """
    def load(self):
        print(f"[OpenVoiceEngine] 分配计算单元: {self.device}")

        try:
            from openvoice import se_extractor
            from openvoice.api import ToneColorConverter, BaseSpeakerTTS
        except ImportError:
            raise ImportError(
                "[OpenVoiceEngine] 缺少 openvoice 库！\n"
                "请先运行: bash scripts/install_openvoice.sh\n"
                "该脚本会自动克隆源码、下载权重并安装。"
            )

        ckpt_dir = os.path.join(self.model_dir, "OpenVoice", "checkpoints_v2")
        if not os.path.exists(ckpt_dir):
            raise FileNotFoundError(
                f"[OpenVoiceEngine] 未在 {ckpt_dir} 找到权重！\n"
                "请先运行: bash scripts/install_openvoice.sh"
            )

        converter_cfg = os.path.join(ckpt_dir, "converter", "config.json")
        converter_ckpt = os.path.join(ckpt_dir, "converter", "checkpoint.pth")

        self.converter = ToneColorConverter(converter_cfg, device=self.device)
        self.converter.load_ckpt(converter_ckpt)
        self.se_extractor = se_extractor
        self._ckpt_dir = ckpt_dir
        self.model = "loaded"
        print("[OpenVoiceEngine] 模型加载完毕！")

    def synthesize_chunk(self, text: str, ref_audio: str, speed: float = 1.0):
        from openvoice.api import BaseSpeakerTTS

        # 1. 提取目标音色
        target_se, _ = self.se_extractor.get_se(ref_audio, self.converter, vad=False)

        # 2. 使用基础 TTS 生成默认音色发言
        base_cfg = os.path.join(self._ckpt_dir, "base_speakers", "ses", "default.pth")
        source_se = os.path.join(self._ckpt_dir, "base_speakers", "EN", "default_se.pth")

        import tempfile, torch
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name

        # 3. 转换音色
        self.converter.convert(
            audio_src_path=tmp_path,
            src_se=torch.load(source_se),
            tgt_se=target_se,
            output_path=tmp_path + "_out.wav"
        )

        audio, sr = sf.read(tmp_path + "_out.wav")
        os.unlink(tmp_path)
        if os.path.exists(tmp_path + "_out.wav"):
            os.unlink(tmp_path + "_out.wav")

        return audio, sr


# ==========================================
# 6. 引擎工厂中枢
# ==========================================
GLOBAL_MODEL_DIR = os.path.expanduser("~/.openclaw/models/voice-clone")
_active_engine: BaseTTSEngine = None

# 注册引擎名称到类的映射
ENGINE_REGISTRY = {
    "f5": F5TTSEngine,
    "cosyvoice": CosyVoiceEngine,
    "chattts": ChatTTSEngine,
    "openvoice": OpenVoiceEngine,
}

def get_available_engines() -> list:
    """返回当前注册的所有引擎名称"""
    return list(ENGINE_REGISTRY.keys())

def initialize_models():
    global _active_engine
    if not os.path.exists(GLOBAL_MODEL_DIR):
        os.makedirs(GLOBAL_MODEL_DIR, exist_ok=True)

    engine_name = os.getenv("TTS_BACKEND", "f5").lower()

    if engine_name not in ENGINE_REGISTRY:
        available = ", ".join(ENGINE_REGISTRY.keys())
        raise ValueError(
            f"不支持的语音引擎: '{engine_name}'\n"
            f"可用引擎: {available}\n"
            f"请设置环境变量 TTS_BACKEND 为上述之一。"
        )

    engine_cls = ENGINE_REGISTRY[engine_name]
    print(f"[core_tts] 使用引擎: {engine_name} ({engine_cls.__name__})")
    _active_engine = engine_cls(GLOBAL_MODEL_DIR)
    _active_engine.load()

def generate_voice(text: str, ref_audio: str, output_path: str, speed: float = 1.0) -> bool:
    global _active_engine
    if _active_engine is None:
        raise RuntimeError("全局引擎未就绪")

    start_t = time.time()
    result = _active_engine.synthesize(text, ref_audio, output_path, speed=speed)
    end_t = time.time()
    print(f"[core_tts] 整体克隆与生成耗时: {end_t - start_t:.2f} 秒")
    return result
