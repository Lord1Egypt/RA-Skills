"""说话人分离模块 — 本地离线多人对话分离 + 标注 + 三类预设（访谈/会议/电话）"""

import os
import warnings
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from .logger import get_logger

logger = get_logger(__name__)

# 忽略一些科学计算库的警告
warnings.filterwarnings("ignore", category=UserWarning)

# ==================== 说话人分离预设（v4.6 新增） ====================
DIARIZATION_PROFILES = {
    "interview": {
        "description": "访谈/播客（2-3人，对话轮换，中等间隔）",
        "threshold": 0.5,
        "window": 1.5,
        "max_speakers": 3,
        "merge_gap": 1.0,
    },
    "meeting": {
        "description": "会议/讨论（3-6人，多人交叉，短间隔）",
        "threshold": 0.6,
        "window": 2.0,
        "max_speakers": 6,
        "merge_gap": 0.8,
    },
    "phone": {
        "description": "电话/对讲（2人，一方为主，长间隔）",
        "threshold": 0.4,
        "window": 3.0,
        "max_speakers": 2,
        "merge_gap": 2.0,
    },
}


class SpeakerDiarization:
    """
    说话人分离器 — 完全离线，无需网络/API
    
    原理：
    1. 使用 VAD (语音活动检测) 切分有效语音段
    2. 提取每段的声学特征 (MFCC + 频谱特征)
    3. 使用高斯混合模型 (GMM) 聚类分人
    4. 输出带说话人标签的字幕
    """
    
    # 预设颜色对应不同说话人
    SPEAKER_COLORS = [
        "#FF6B6B",  # 红色 - 说话人A
        "#4ECDC4",  # 青色 - 说话人B
        "#FFD93D",  # 黄色 - 说话人C
        "#6C5CE7",  # 紫色 - 说话人D
        "#A8E6CF",  # 浅绿 - 说话人E
        "#FF8B94",  # 粉色 - 说话人F
    ]
    
    SPEAKER_NAMES = ["说话人A", "说话人B", "说话人C", "说话人D", "说话人E", "说话人F"]
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.min_speech_duration = 0.5  # 最短语音段（秒）
        self.eps = 1e-6
        # v46: 说话人分离预设
        self.profile_config = config.get("diarization_profiles", {})
        self.default_profile = self.profile_config.get("default", "interview")
    
    def get_profile(self, profile_name: Optional[str] = None) -> Dict[str, Any]:
        """
        获取分离预设配置。
        
        Args:
            profile_name: 预设名 (interview/meeting/phone)，None 则返回默认
            
        Returns:
            预设配置 dict
        """
        name = profile_name or self.default_profile
        profile = DIARIZATION_PROFILES.get(name, DIARIZATION_PROFILES["interview"])
        # 用户自定义覆盖
        custom = self.profile_config.get("custom", {}).get(name, {})
        merged = dict(profile)
        merged.update(custom)
        return merged
    
    def diarize(
        self,
        audio_path: str,
        segments: List[Dict],
        n_speakers: Optional[int] = None,
        profile: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        执行说话人分离。
        
        Args:
            audio_path: WAV 音频文件路径
            segments: whisper 识别结果中的语音段列表
            n_speakers: 指定说话人数量（不指定则自动检测）
            profile: 分离预设 (interview/meeting/phone, v46新增)
            
        Returns:
            带说话人标签的结果 + 质量评分（v46起自动输出）
        """
        logger.info("🎙️  开始说话人分离...")
        
        if not segments:
            return {"segments": [], "n_speakers": 0, "speaker_map": {}, "quality_score": None}
        
        # v46: 加载预设
        prof = self.get_profile(profile)
        logger.info(f"   使用预设: {prof.get('description', '默认')}")
        
        # 提取每个语音段的声学特征
        features = self._extract_segment_features(audio_path, segments)
        
        # 如果特征全为null（库不可用），则使用启发式分人
        if features is None or len(features) == 0:
            logger.warning("声学特征提取不可用，使用启发式分人")
            result = self._heuristic_diarize(segments, n_speakers, prof)
        else:
            # 自动估计说话人数量
            if n_speakers is None:
                n_speakers = self._estimate_speaker_count(features, prof)
            n_speakers = min(n_speakers, prof.get("max_speakers", 6))
            
            # 聚类分人
            speaker_labels = self._cluster_speakers(features, n_speakers)
            
            # 合并连续同一说话人段（使用预设的 merge_gap）
            merge_gap = prof.get("merge_gap", 1.0)
            merged_segments = self._merge_consecutive_speakers(segments, speaker_labels, merge_gap)
            
            # 构建说话人信息
            speaker_map = {}
            for i in range(n_speakers):
                speaker_id = f"speaker_{chr(65 + i)}"
                speaker_map[speaker_id] = {
                    "name": self.SPEAKER_NAMES[i] if i < len(self.SPEAKER_NAMES) else f"说话人{chr(65+i)}",
                    "color": self.SPEAKER_COLORS[i] if i < len(self.SPEAKER_COLORS) else "#999",
                }
            
            result = {
                "segments": merged_segments,
                "n_speakers": n_speakers,
                "speaker_map": speaker_map,
                "profile_used": profile or self.default_profile,
            }
        
        # v46: 质量评分自动输出
        from .speaker_diarization.quality_scorer import QualityScorer
        scorer = QualityScorer(self.config)
        quality_result = scorer.score(result, features, segments)
        result["quality_score"] = quality_result
        logger.info(f"   质量评分: {quality_result.get('overall_score')} 分 ({quality_result.get('level')}可信度)")
        
        logger.info(f"说话人分离完成: {result['n_speakers']} 人, {len(result['segments'])} 个对话段")
        return result
    
    def _extract_segment_features(
        self,
        audio_path: str,
        segments: List[Dict],
    ) -> Optional[np.ndarray]:
        """提取每个语音段的声学特征向量"""
        try:
            import librosa
        except ImportError:
            logger.warning("librosa 未安装，无法提取高级声学特征。请 pip install librosa")
            return None
        
        try:
            # 加载音频
            y, sr = librosa.load(audio_path, sr=16000, mono=True)
            
            feature_list = []
            for seg in segments:
                start = seg.get("start", 0)
                end = seg.get("end", 0)
                duration = end - start
                
                if duration < self.min_speech_duration:
                    feature_list.append(None)
                    continue
                
                # 提取对应音频片段
                start_sample = int(start * sr)
                end_sample = int(end * sr)
                segment_audio = y[start_sample:end_sample]
                
                if len(segment_audio) < sr * 0.3:  # 至少需要 0.3 秒
                    feature_list.append(None)
                    continue
                
                # 提取 MFCC (13维) + 一阶差分 + 二阶差分
                mfcc = librosa.feature.mfcc(y=segment_audio, sr=sr, n_mfcc=13)
                mfcc_delta = librosa.feature.delta(mfcc)
                mfcc_delta2 = librosa.feature.delta(mfcc, order=2)
                
                # 提取频谱特征
                spectral_centroid = librosa.feature.spectral_centroid(y=segment_audio, sr=sr)
                spectral_bandwidth = librosa.feature.spectral_bandwidth(y=segment_audio, sr=sr)
                spectral_rolloff = librosa.feature.spectral_rolloff(y=segment_audio, sr=sr)
                zero_crossing_rate = librosa.feature.zero_crossing_rate(segment_audio)
                
                # 基频估计 (F0) — 使用 piptrack
                try:
                    pitches, magnitudes = librosa.piptrack(y=segment_audio, sr=sr)
                    # 取每个帧的最大 pitch
                    pitch_values = []
                    for t in range(pitches.shape[1]):
                        index = magnitudes[:, t].argmax()
                        pitch = pitches[index, t]
                        if pitch > 0:
                            pitch_values.append(pitch)
                    
                    if pitch_values:
                        mean_pitch = np.mean(pitch_values)
                        std_pitch = np.std(pitch_values)
                    else:
                        mean_pitch = 0
                        std_pitch = 0
                except Exception:
                    mean_pitch = 0
                    std_pitch = 0
                
                # RMS 能量
                rms = librosa.feature.rms(y=segment_audio)
                
                # 汇总特征向量
                feat = np.concatenate([
                    np.mean(mfcc, axis=1),       # 13
                    np.std(mfcc, axis=1),        # 13
                    np.mean(mfcc_delta, axis=1), # 13
                    np.mean(spectral_centroid),   # 1
                    np.std(spectral_centroid),    # 1
                    np.mean(spectral_bandwidth),  # 1
                    np.mean(spectral_rolloff),    # 1
                    np.mean(zero_crossing_rate),  # 1
                    np.std(zero_crossing_rate),   # 1
                    [mean_pitch, std_pitch],      # 2
                    np.mean(rms),                 # 1
                    np.std(rms),                  # 1
                ])
                
                feature_list.append(feat)
            
            # 用均值填充 None
            valid_features = [f for f in feature_list if f is not None]
            if not valid_features:
                return None
            
            mean_feat = np.mean(valid_features, axis=0)
            for i in range(len(feature_list)):
                if feature_list[i] is None:
                    feature_list[i] = mean_feat
            
            return np.array(feature_list)
            
        except Exception as e:
            logger.debug(f"特征提取失败: {e}")
            return None
    
    def _estimate_speaker_count(self, features: np.ndarray, prof: Optional[Dict] = None) -> int:
        """自动估计说话人数量（使用BIC/AIC准则或轮廓系数）"""
        try:
            from sklearn.mixture import GaussianMixture
        except ImportError:
            logger.warning("scikit-learn 未安装，默认识别 2 人")
            return 2 if prof is None else prof.get("max_speakers", 2)
        
        n_samples = len(features)
        if n_samples <= 2:
            return 1
        
        # 归一化特征
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)
        
        max_k = min(prof.get("max_speakers", 6) if prof else 6, n_samples - 1)
        best_bic = float("inf")
        best_k = 2
        
        for k in range(1, max_k + 1):
            try:
                gmm = GaussianMixture(
                    n_components=k,
                    covariance_type="full",
                    max_iter=100,
                    random_state=42,
                    n_init=1,
                )
                gmm.fit(features_scaled)
                bic = gmm.bic(features_scaled)
                if bic < best_bic:
                    best_bic = bic
                    best_k = k
            except Exception:
                continue
        
        logger.info(f"自动检测说话人数量: {best_k}")
        return best_k
    
    def _cluster_speakers(self, features: np.ndarray, n_speakers: int) -> List[int]:
        """使用GMM聚类分配说话人"""
        try:
            from sklearn.mixture import GaussianMixture
            from sklearn.preprocessing import StandardScaler
        except ImportError:
            # 回退：简单均匀分配
            return [i % n_speakers for i in range(len(features))]
        
        # 归一化
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)
        
        try:
            gmm = GaussianMixture(
                n_components=n_speakers,
                covariance_type="full",
                max_iter=200,
                random_state=42,
                n_init=3,
            )
            labels = gmm.fit_predict(features_scaled)
            return labels.tolist()
        except Exception as e:
            logger.debug(f"GMM 聚类失败: {e}")
            return [i % n_speakers for i in range(len(features))]
    
    def _heuristic_diarize(
        self,
        segments: List[Dict],
        n_speakers: Optional[int] = None,
        prof: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """
        启发式分人（无 librosa/sklearn 时的回退方案）
        基于时间间隔和文本特征猜测说话人切换
        """
        if not segments:
            return {"segments": [], "n_speakers": 0, "speaker_map": {}}
        
        default_n = prof.get("max_speakers", 2) if prof else 2
        merge_gap = prof.get("merge_gap", 2.0) if prof else 2.0
        
        if n_speakers is None:
            n_speakers = default_n
        
        # 简单策略：间隔超过 merge_gap 秒，大概率换人
        current_speaker = 0
        labels = [0]
        
        for i in range(1, len(segments)):
            gap = segments[i].get("start", 0) - segments[i-1].get("end", 0)
            if gap > merge_gap:
                current_speaker = (current_speaker + 1) % n_speakers
            labels.append(current_speaker)
        
        # 构建合并后的段
        merged = self._merge_consecutive_speakers(segments, labels, merge_gap)
        
        speaker_map = {}
        for i in range(n_speakers):
            speaker_id = f"speaker_{chr(65 + i)}"
            speaker_map[speaker_id] = {
                "name": self.SPEAKER_NAMES[i] if i < len(self.SPEAKER_NAMES) else f"说话人{chr(65+i)}",
                "color": self.SPEAKER_COLORS[i] if i < len(self.SPEAKER_COLORS) else "#999",
            }
        
        return {
            "segments": merged,
            "n_speakers": n_speakers,
            "speaker_map": speaker_map,
            "profile_used": prof.get("default") if prof else "interview",
        }
    
    def _merge_consecutive_speakers(
        self,
        segments: List[Dict],
        labels: List[int],
        merge_gap: float = 1.0,
    ) -> List[Dict]:
        """合并连续同一说话人的语音段"""
        if not segments:
            return []
        
        merged = []
        current = {
            "speaker_idx": labels[0],
            "start": segments[0].get("start", 0),
            "end": segments[0].get("end", 0),
            "text": segments[0].get("text", "").strip(),
            "segments": [segments[0]],
        }
        
        for i in range(1, len(segments)):
            gap = segments[i].get("start", 0) - current["end"]
            if labels[i] == current["speaker_idx"] and gap < merge_gap:
                # 同一说话人且间隙小于 merge_gap，合并
                current["end"] = segments[i].get("end", 0)
                current["text"] += " " + segments[i].get("text", "").strip()
                current["segments"].append(segments[i])
            else:
                # 说话人变化，保存当前段
                merged.append({
                    "speaker": f"说话人{chr(65 + current['speaker_idx'])}",
                    "speaker_idx": current["speaker_idx"],
                    "start": round(current["start"], 3),
                    "end": round(current["end"], 3),
                    "duration": round(current["end"] - current["start"], 2),
                    "text": current["text"],
                    "color": self.SPEAKER_COLORS[current["speaker_idx"]] if current["speaker_idx"] < len(self.SPEAKER_COLORS) else "#999",
                })
                current = {
                    "speaker_idx": labels[i],
                    "start": segments[i].get("start", 0),
                    "end": segments[i].get("end", 0),
                    "text": segments[i].get("text", "").strip(),
                    "segments": [segments[i]],
                }
        
        # 添加最后一段
        merged.append({
            "speaker": f"说话人{chr(65 + current['speaker_idx'])}",
            "speaker_idx": current["speaker_idx"],
            "start": round(current["start"], 3),
            "end": round(current["end"], 3),
            "duration": round(current["end"] - current["start"], 2),
            "text": current["text"],
            "color": self.SPEAKER_COLORS[current["speaker_idx"]] if current["speaker_idx"] < len(self.SPEAKER_COLORS) else "#999",
        })
        
        return merged
    
    def generate_srt_with_speakers(self, diarize_result: Dict, output_path: str) -> str:
        """生成带说话人标签的SRT字幕"""
        segments = diarize_result.get("segments", [])
        
        parts = []
        for i, seg in enumerate(segments):
            start = self._format_time(seg.get("start", 0))
            end = self._format_time(seg.get("end", 0))
            speaker = seg.get("speaker", "未知")
            text = seg.get("text", "").strip()
            
            if text:
                parts.append(f"{i+1}\n{start} --> {end}\n[{speaker}] {text}\n")
        
        srt_content = "\n".join(parts)
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(srt_content)
        
        return output_path
    
    @staticmethod
    def _format_time(seconds: float) -> str:
        """格式化为 SRT 时间: HH:MM:SS,mmm"""
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        ms = int((seconds % 1) * 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
