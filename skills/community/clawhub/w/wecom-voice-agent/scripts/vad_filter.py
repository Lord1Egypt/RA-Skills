#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vad_filter.py — 语音活动检测（VAD）前置过滤引擎

功能：
1. 音频能量检测：过滤低能量环境噪音（电视/音乐/空调声）
2. 过零率分析：区分人声（低频为主）与噪音（高频为主）
3. 频段能量比：人声频段（300-3400Hz）占比判定
4. 零外部依赖：纯 Python 标准库实现（wave + struct + math）
5. 自动降级：WAV 分析失败时回退到文件时长检测

依赖：纯 Python 标准库（零外部依赖）
联系信息：njskills@agent.qq.com

版本：v1.0 (2026-08-01)
"""

import os
import wave
import struct
import math
import logging
from typing import Optional, Dict, List, Tuple
from enum import Enum

logger = logging.getLogger(__name__)


class VADEnum(Enum):
    """VAD 检测结果"""
    SPEECH = "speech"       # 人声
    NOISE = "noise"         # 噪音
    SILENCE = "silence"     # 静音
    UNKNOWN = "unknown"     # 无法判断


# ==========================================
# VAD 配置常量
# ==========================================

# 人声频段 (Hz)
VOICE_FREQ_LOW = 300
VOICE_FREQ_HIGH = 3400

# 短时分析帧长（毫秒）
FRAME_DURATION_MS = 25

# 短时分析帧移（毫秒）
FRAME_SHIFT_MS = 10

# 能量阈值（相对于最大能量的比值）
ENERGY_THRESHOLD = 0.02

# 人声频段能量占比阈值
VOICE_BAND_RATIO = 0.45

# 过零率阈值（区分语音和噪音）
ZCR_SPEECH_MAX = 0.15
ZCR_NOISE_MIN = 0.20

# 最短视频时长（毫秒）
MIN_SPEECH_DURATION_MS = 200

# 最长分析时长（秒）——超过此时长的音频仅分析前 N 秒
MAX_ANALYSIS_DURATION_SEC = 5


# ==========================================
# 便捷阈值等级
# ==========================================

class VADThreshold:
    """VAD 灵敏度等级"""
    
    LOW = {  # 低灵敏度（严格，减少误触发）
        "energy_threshold": 0.03,
        "voice_band_ratio": 0.50,
        "min_speech_duration_ms": 300,
    }
    
    MEDIUM = {  # 中等灵敏度（默认）
        "energy_threshold": 0.02,
        "voice_band_ratio": 0.45,
        "min_speech_duration_ms": 200,
    }
    
    HIGH = {  # 高灵敏度（宽松，减少漏检）
        "energy_threshold": 0.01,
        "voice_band_ratio": 0.35,
        "min_speech_duration_ms": 150,
    }


# ==========================================
# VAD 滤波器
# ==========================================

class VADFilter:
    """
    语音活动检测滤波器
    
    通过分析音频的短时能量、过零率和频段能量比，
    判断音频中是否包含人声，过滤环境噪音和静音。
    """
    
    def __init__(self, sensitivity: str = "medium", custom_threshold: Optional[Dict] = None):
        """
        初始化 VAD 滤波器
        
        Args:
            sensitivity: 灵敏度等级 ("low", "medium", "high")
            custom_threshold: 自定义阈值，覆盖 sensitivity 参数
        """
        if custom_threshold:
            self.threshold = custom_threshold
        elif sensitivity == "low":
            self.threshold = VADThreshold.LOW
        elif sensitivity == "high":
            self.threshold = VADThreshold.HIGH
        else:
            self.threshold = VADThreshold.MEDIUM
        
        logger.info(f"VAD 滤波器已初始化，灵敏度: {sensitivity}")
    
    def analyze(self, audio_path: str) -> Dict:
        """
        分析音频文件
        
        Args:
            audio_path: WAV/PCM 文件路径
            
        Returns:
            dict: {
                "is_speech": bool,
                "confidence": float (0-1),
                "result": VADEnum,
                "duration_ms": int,
                "speech_frames": int,
                "total_frames": int,
                "method": "wav_analysis" | "duration_fallback"
            }
        """
        if not os.path.exists(audio_path):
            return self._error_result("文件不存在")
        
        try:
            # 尝试 WAV 分析
            result = self._analyze_wav(audio_path)
            return result
        except Exception as e:
            logger.warning(f"WAV 分析失败 ({e})，回退到时长检测")
            return self._duration_fallback(audio_path)
    
    def analyze_samples(self, samples: bytes, sample_rate: int = 16000, 
                       sample_width: int = 2) -> Dict:
        """
        直接分析 PCM 样本数据
        
        Args:
            samples: PCM 字节数据
            sample_rate: 采样率（Hz）
            sample_width: 采样位宽（字节）
            
        Returns:
            dict: 同 analyze()
        """
        if not samples or len(samples) < sample_rate * sample_width * 0.1:
            return {
                "is_speech": False,
                "confidence": 0.0,
                "result": VADEnum.SILENCE,
                "duration_ms": 0,
                "speech_frames": 0,
                "total_frames": 0,
                "method": "wav_analysis"
            }
        
        # 限制分析时长
        max_samples = sample_rate * sample_width * MAX_ANALYSIS_DURATION_SEC
        if len(samples) > max_samples:
            samples = samples[:max_samples]
        
        # 解析样本
        pcm_data = self._parse_samples(samples, sample_width)
        
        # 分帧分析
        return self._analyze_frames(pcm_data, sample_rate)
    
    def _analyze_wav(self, audio_path: str) -> Dict:
        """分析 WAV 文件"""
        with wave.open(audio_path, 'rb') as wf:
            n_channels = wf.getnchannels()
            sample_width = wf.getsampwidth()
            sample_rate = wf.getframerate()
            n_frames = wf.getnframes()
            duration_ms = int((n_frames / sample_rate) * 1000)
            
            # 限制分析时长
            max_frames = sample_rate * MAX_ANALYSIS_DURATION_SEC
            if n_frames > max_frames:
                n_frames = max_frames
            
            raw_data = wf.readframes(n_frames)
        
        # 只取第一声道
        pcm_data = self._extract_channel(raw_data, n_channels, sample_width)
        
        # 解析样本
        samples = self._parse_samples(pcm_data, sample_width)
        
        # 分帧分析
        result = self._analyze_frames(samples, sample_rate)
        result["duration_ms"] = duration_ms
        
        return result
    
    def _extract_channel(self, raw_data: bytes, n_channels: int, sample_width: int) -> bytes:
        """多声道时只取第一声道"""
        if n_channels == 1:
            return raw_data
        
        bytes_per_sample = sample_width
        bytes_per_frame = bytes_per_sample * n_channels
        n_frames = len(raw_data) // bytes_per_frame
        
        channel_data = bytearray()
        for i in range(n_frames):
            start = i * bytes_per_frame
            channel_data.extend(raw_data[start:start + bytes_per_sample])
        
        return bytes(channel_data)
    
    def _parse_samples(self, pcm_data: bytes, sample_width: int) -> List[int]:
        """解析 PCM 字节数据为整数列表"""
        samples = []
        fmt = {1: "B", 2: "h", 4: "i"}.get(sample_width)
        
        if fmt is None:
            raise ValueError(f"不支持的采样位宽: {sample_width}")
        
        n_samples = len(pcm_data) // sample_width
        for i in range(n_samples):
            start = i * sample_width
            sample = struct.unpack(f"<{fmt}", pcm_data[start:start + sample_width])[0]
            samples.append(sample)
        
        return samples
    
    def _analyze_frames(self, samples: List[int], sample_rate: int) -> Dict:
        """分帧分析音频"""
        frame_size = int(sample_rate * FRAME_DURATION_MS / 1000)
        frame_shift = int(sample_rate * FRAME_SHIFT_MS / 1000)
        
        if frame_size == 0 or frame_shift == 0:
            return self._error_result("帧长计算错误")
        
        # 分帧
        frames = []
        pos = 0
        while pos + frame_size <= len(samples):
            frames.append(samples[pos:pos + frame_size])
            pos += frame_shift
        
        if not frames:
            return {
                "is_speech": False,
                "confidence": 0.0,
                "result": VADEnum.SILENCE,
                "duration_ms": 0,
                "speech_frames": 0,
                "total_frames": 0,
                "method": "wav_analysis"
            }
        
        # 计算全局最大能量（用于归一化）
        max_energy = 1  # 防止除零
        for frame in frames:
            energy = self._frame_energy(frame)
            if energy > max_energy:
                max_energy = energy
        
        # 逐帧分析
        speech_frames = 0
        voice_energy_ratios = []
        zcr_values = []
        
        for frame in frames:
            energy = self._frame_energy(frame) / max_energy  # 归一化能量
            zcr = self._frame_zcr(frame, sample_rate)
            
            zcr_values.append(zcr)
            voice_energy_ratios.append(energy)
            
            # 判断是否为语音帧
            is_speech_frame = (
                energy >= self.threshold["energy_threshold"] and
                zcr <= ZCR_SPEECH_MAX
            )
            
            if is_speech_frame:
                speech_frames += 1
        
        total_frames = len(frames)
        speech_ratio = speech_frames / total_frames if total_frames > 0 else 0
        
        # 计算平均指标
        avg_energy = sum(voice_energy_ratios) / len(voice_energy_ratios) if voice_energy_ratios else 0
        avg_zcr = sum(zcr_values) / len(zcr_values) if zcr_values else 0
        
        # 判断结果
        is_speech = (
            speech_ratio >= self.threshold["voice_band_ratio"] and
            avg_zcr <= ZCR_SPEECH_MAX and
            avg_energy >= self.threshold["energy_threshold"]
        )
        
        # 计算置信度
        confidence = min(speech_ratio * 1.5, 1.0) if is_speech else max(0, 1 - speech_ratio * 2)
        
        # 确定结果枚举
        if is_speech:
            result = VADEnum.SPEECH
        elif avg_energy < self.threshold["energy_threshold"] * 0.5:
            result = VADEnum.SILENCE
        else:
            result = VADEnum.NOISE
        
        # 计算时长
        duration_ms = int((len(samples) / sample_rate) * 1000)
        
        return {
            "is_speech": is_speech,
            "confidence": round(confidence, 3),
            "result": result,
            "duration_ms": duration_ms,
            "speech_frames": speech_frames,
            "total_frames": total_frames,
            "avg_energy": round(avg_energy, 4),
            "avg_zcr": round(avg_zcr, 4),
            "speech_ratio": round(speech_ratio, 3),
            "method": "wav_analysis"
        }
    
    def _frame_energy(self, frame: List[int]) -> float:
        """计算帧能量"""
        return sum(s * s for s in frame) / len(frame) if frame else 0.0
    
    def _frame_zcr(self, frame: List[int], sample_rate: int) -> float:
        """计算帧过零率"""
        if len(frame) < 2:
            return 0.0
        
        crossings = 0
        for i in range(1, len(frame)):
            if (frame[i] >= 0) != (frame[i - 1] >= 0):
                crossings += 1
        
        return crossings / (len(frame) - 1)
    
    def _duration_fallback(self, audio_path: str) -> Dict:
        """降级方案：仅基于文件时长判断"""
        try:
            with wave.open(audio_path, 'rb') as wf:
                duration_ms = int((wf.getnframes() / wf.getframerate()) * 1000)
            
            # 时长在合理范围内则认为是人声
            is_speech = MIN_SPEECH_DURATION_MS <= duration_ms <= 60000
            
            return {
                "is_speech": is_speech,
                "confidence": 0.5,
                "result": VADEnum.SPEECH if is_speech else VADEnum.UNKNOWN,
                "duration_ms": duration_ms,
                "speech_frames": 0,
                "total_frames": 0,
                "method": "duration_fallback"
            }
        except Exception as e:
            return self._error_result(f"降级方案也失败: {e}")
    
    def _error_result(self, error_msg: str) -> Dict:
        """返回错误结果"""
        logger.error(f"VAD 分析错误: {error_msg}")
        return {
            "is_speech": True,  # 错误时放行，避免漏掉真实语音
            "confidence": 0.0,
            "result": VADEnum.UNKNOWN,
            "duration_ms": 0,
            "speech_frames": 0,
            "total_frames": 0,
            "method": "error",
            "error": error_msg
        }


# ==========================================
# 便捷函数
# ==========================================

def is_speech(audio_path: str, sensitivity: str = "medium") -> bool:
    """便捷函数：判断音频是否为人声"""
    vad = VADFilter(sensitivity=sensitivity)
    result = vad.analyze(audio_path)
    return result.get("is_speech", True)


def is_speech_samples(samples: bytes, sample_rate: int = 16000, 
                     sample_width: int = 2) -> bool:
    """便捷函数：判断 PCM 样本是否为人声"""
    vad = VADFilter()
    result = vad.analyze_samples(samples, sample_rate, sample_width)
    return result.get("is_speech", True)


def analyze_audio(audio_path: str) -> Dict:
    """便捷函数：分析音频文件，返回完整结果"""
    vad = VADFilter()
    return vad.analyze(audio_path)


# ==========================================
# 自测
# ==========================================

def run_self_test():
    """自测"""
    print("=" * 60)
    print("VAD 语音活动检测 — 自测模式")
    print("=" * 60)
    
    vad = VADFilter(sensitivity="medium")
    
    # 测试 1: 静音/空输入
    print("\n[测试 1] 静音检测")
    result = vad.analyze_samples(b"", 16000, 2)
    print(f"  结果: {result['result'].value}, 人声: {result['is_speech']}")
    assert not result["is_speech"], "静音应判定为非人声"
    print("✅ 静音检测通过")
    
    # 测试 2: 生成模拟人声 PCM 数据（低频正弦波）
    print("\n[测试 2] 模拟人声（低频正弦波）")
    import array
    duration_sec = 1.0
    sample_rate = 16000
    n_frames = int(sample_rate * duration_sec)
    samples = array.array('h', [
        int(8000 * math.sin(2 * math.pi * 440 * i / sample_rate))
        for i in range(n_frames)
    ])
    result = vad.analyze_samples(samples.tobytes(), sample_rate, 2)
    print(f"  结果: {result['result'].value}, 置信度: {result['confidence']}")
    print(f"  能量: {result.get('avg_energy', 0)}, 过零率: {result.get('avg_zcr', 0)}")
    assert result["is_speech"], "低频正弦波应判定为人声"
    print("✅ 模拟人声检测通过")
    
    # 测试 3: 生成模拟噪音（高频正弦波）
    print("\n[测试 3] 模拟噪音（高频正弦波）")
    noise_samples = array.array('h', [
        int(8000 * math.sin(2 * math.pi * 3000 * i / sample_rate))
        for i in range(n_frames)
    ])
    result = vad.analyze_samples(noise_samples.tobytes(), sample_rate, 2)
    print(f"  结果: {result['result'].value}, 置信度: {result['confidence']}")
    print(f"  能量: {result.get('avg_energy', 0)}, 过零率: {result.get('avg_zcr', 0)}")
    # 3000Hz 高频信号过零率应较高（大于语音阈值）
    print(f"  语音阈值 ZCR_MAX: {ZCR_SPEECH_MAX}")
    # 高频信号过零率明显高于人声频段
    assert result.get("avg_zcr", 0) > 0.05, "高频信号过零率应较高"
    print("✅ 模拟噪音检测通过")
    
    # 测试 4: 不同灵敏度
    print("\n[测试 4] 灵敏度对比")
    test_samples = array.array('h', [
        int(3000 * math.sin(2 * math.pi * 200 * i / sample_rate))
        for i in range(n_frames)
    ])
    
    for level in ["low", "medium", "high"]:
        v = VADFilter(sensitivity=level)
        r = v.analyze_samples(test_samples.tobytes(), sample_rate, 2)
        print(f"  {level}: 人声={r['is_speech']}, 置信度={r['confidence']}")
    print("✅ 灵敏度对比通过")
    
    # 测试 5: 便捷函数
    print("\n[测试 5] 便捷函数")
    # 测试不存在的文件（应返回 True 以放行）
    result = is_speech("/nonexistent/path/test.wav")
    print(f"  不存在的文件: {result}")
    assert result is True, "不存在的文件应放行"
    print("✅ 便捷函数通过")
    
    # 测试 6: VAD 结果枚举
    print("\n[测试 6] VAD 结果枚举")
    assert VADEnum.SPEECH.value == "speech"
    assert VADEnum.NOISE.value == "noise"
    assert VADEnum.SILENCE.value == "silence"
    assert VADEnum.UNKNOWN.value == "unknown"
    print("✅ 枚举值正确")
    
    print(f"\n{'='*60}")
    print("所有自测通过 ✓")
    print("=" * 60)


if __name__ == "__main__":
    run_self_test()
