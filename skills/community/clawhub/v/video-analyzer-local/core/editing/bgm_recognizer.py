"""BGM 识别器 — 可选依赖 chromaprint/fpcalc 计算音频指纹，匹配本地参考库"""

import hashlib
import json
import os
import subprocess
import tempfile
from typing import Any, Dict, List, Optional

from ..logger import get_logger

logger = get_logger(__name__)


class BGMRecognizer:
    """
    BGM 识别器。

    可选依赖 chromaprint/fpcalc 计算音频指纹，
    匹配本地小参考库（用户提交常见 BGM 样本），
    输出版权风险提示（未知 BGM 标记商业风险）。

    无依赖时隐藏该功能，不阻塞主流程。
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.editing_config = config.get("editing", {})
        self.bgm_config = self.editing_config.get("bgm", {})

        # 配置参数
        self.fpcalc_path = self.bgm_config.get("fpcalc_path", "fpcalc")
        self.chromaprint_path = self.bgm_config.get("chromaprint_path", "fpcalc")
        self.library_path = self.bgm_config.get("library_path", None)
        self.temp_dir = self.bgm_config.get("temp_dir", ".temp/bgm")
        self.match_threshold = self.bgm_config.get("match_threshold", 0.7)

        # 确保目录存在
        os.makedirs(self.temp_dir, exist_ok=True)

        # 加载本地参考库
        self.library = self._load_library()

    def recognize(
        self, video_path: str, extract_audio: bool = True
    ) -> Dict[str, Any]:
        """
        识别视频中的 BGM。

        Args:
            video_path: 视频文件路径
            extract_audio: 是否先提取音频

        Returns:
            {
                "identified": True/False,
                "bgm_name": "BGM名称",
                "confidence": 置信度,
                "copyright_risk": "low/medium/high",
                "risk_reason": "风险原因",
                "library_match": True/False,
                "fingerprint": "指纹摘要",
                "warnings": ["警告"],
            }
        """
        result = {
            "identified": False,
            "bgm_name": None,
            "confidence": 0.0,
            "copyright_risk": "unknown",
            "risk_reason": None,
            "library_match": False,
            "fingerprint": None,
            "warnings": [],
        }

        if not video_path or not os.path.exists(video_path):
            result["warnings"].append("视频文件不存在")
            return result

        # 检查依赖是否可用
        if not self._check_dependency():
            result["warnings"].append(
                "未找到 chromaprint/fpcalc，BGM 识别功能已禁用。"
                "请安装 chromaprint 后重试。"
            )
            result["copyright_risk"] = "unknown"
            return result

        try:
            # 提取音频
            if extract_audio:
                audio_path = self._extract_audio(video_path)
                if not audio_path:
                    result["warnings"].append("音频提取失败")
                    return result
            else:
                audio_path = video_path

            # 计算指纹
            fingerprint = self._compute_fingerprint(audio_path)
            if not fingerprint:
                result["warnings"].append("指纹计算失败")
                return result

            result["fingerprint"] = fingerprint[:16] + "..."  # 摘要

            # 匹配参考库
            match_result = self._match_library(fingerprint)
            if match_result:
                result["identified"] = True
                result["bgm_name"] = match_result["name"]
                result["confidence"] = match_result["confidence"]
                result["library_match"] = True
                result["copyright_risk"] = match_result.get("risk", "unknown")
                result["risk_reason"] = match_result.get("reason", "参考库匹配成功")
            else:
                # 未匹配到：标记为未知 BGM
                result["identified"] = False
                result["copyright_risk"] = "high"
                result["risk_reason"] = "未知 BGM，无法确认版权状态，商业使用存在风险"

            # 清理临时文件
            if extract_audio and audio_path != video_path:
                try:
                    os.remove(audio_path)
                except OSError:
                    pass

        except Exception as e:
            logger.error(f"BGM 识别失败: {e}")
            result["warnings"].append(f"识别异常: {str(e)}")

        return result

    def _check_dependency(self) -> bool:
        """检查 chromaprint/fpcalc 是否可用"""
        for cmd in [self.fpcalc_path, self.chromaprint_path, "fpcalc"]:
            try:
                result = subprocess.run(
                    [cmd, "-version"],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    self.fpcalc_path = cmd
                    return True
            except (FileNotFoundError, OSError):
                continue
        return False

    def _extract_audio(self, video_path: str) -> Optional[str]:
        """从视频中提取音频"""
        try:
            audio_path = os.path.join(
                self.temp_dir,
                f"bgm_audio_{os.getpid()}.wav",
            )
            cmd = [
                "ffmpeg", "-y",
                "-i", video_path,
                "-vn",  # 无视频
                "-acodec", "pcm_s16le",
                "-ar", "44100",
                "-ac", "2",
                audio_path,
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if result.returncode == 0 and os.path.exists(audio_path):
                return audio_path
        except Exception as e:
            logger.error(f"音频提取失败: {e}")
        return None

    def _compute_fingerprint(self, audio_path: str) -> Optional[str]:
        """计算音频指纹"""
        try:
            cmd = [self.fpcalc, "-raw", "-length", "120", audio_path]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                # fpcalc 输出格式: FINGERPRINT=xxxxx
                for line in result.stdout.split("\n"):
                    if line.startswith("FINGERPRINT="):
                        return line.split("=", 1)[1].strip()
        except Exception as e:
            logger.error(f"指纹计算失败: {e}")
        return None

    def _match_library(self, fingerprint: str) -> Optional[Dict]:
        """匹配本地参考库"""
        if not self.library:
            return None

        best_match = None
        best_score = 0.0

        for entry in self.library:
            lib_fp = entry.get("fingerprint", "")
            if not lib_fp:
                continue

            # 简单相似度：共同子串比例
            similarity = self._compute_similarity(fingerprint, lib_fp)
            if similarity > best_score and similarity >= self.match_threshold:
                best_score = similarity
                best_match = {
                    "name": entry.get("name", "未知"),
                    "confidence": round(similarity, 3),
                    "risk": entry.get("risk", "unknown"),
                    "reason": entry.get("reason", "参考库匹配"),
                }

        return best_match

    def _compute_similarity(self, fp1: str, fp2: str) -> float:
        """计算两个指纹的相似度（简化版）"""
        if not fp1 or not fp2:
            return 0.0

        # 使用编辑距离比例
        len1, len2 = len(fp1), len(fp2)
        if len1 == 0 or len2 == 0:
            return 0.0

        # 取较短长度
        min_len = min(len1, len2)
        matches = sum(1 for i in range(min_len) if fp1[i] == fp2[i])

        return matches / max(len1, len2)

    def _load_library(self) -> List[Dict]:
        """加载本地 BGM 参考库"""
        library = []

        # 默认库路径
        default_paths = [
            self.library_path,
            os.path.join(os.path.dirname(__file__), "bgm_library.json"),
            "D:/skill/video-analyzer/core/editing/bgm_library.json",
        ]

        for path in default_paths:
            if path and os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            library = data
                        elif isinstance(data, dict) and "tracks" in data:
                            library = data["tracks"]
                    logger.info(f"加载 BGM 参考库: {path} ({len(library)} 条)")
                    break
                except Exception as e:
                    logger.warning(f"加载 BGM 参考库失败: {e}")

        return library

    def add_to_library(
        self,
        audio_path: str,
        name: str,
        risk: str = "unknown",
        reason: str = "",
    ) -> bool:
        """添加 BGM 到本地参考库"""
        try:
            fingerprint = self._compute_fingerprint(audio_path)
            if not fingerprint:
                return False

            entry = {
                "name": name,
                "fingerprint": fingerprint,
                "risk": risk,
                "reason": reason,
            }

            self.library.append(entry)

            # 保存到文件
            library_path = self.library_path or os.path.join(
                os.path.dirname(__file__), "bgm_library.json"
            )
            with open(library_path, "w", encoding="utf-8") as f:
                json.dump(self.library, f, ensure_ascii=False, indent=2)

            return True

        except Exception as e:
            logger.error(f"添加 BGM 到参考库失败: {e}")
            return False

    @staticmethod
    def get_dependency_instructions() -> str:
        """获取依赖安装指引"""
        return (
            "BGM 识别需要 chromaprint/fpcalc。\n"
            "安装方法：\n"
            "  Windows: choco install chromaprint\n"
            "  macOS: brew install chromaprint\n"
            "  Linux: sudo apt install chromaprint-fpcalc\n"
            "安装后重试即可启用 BGM 识别功能。"
        )
