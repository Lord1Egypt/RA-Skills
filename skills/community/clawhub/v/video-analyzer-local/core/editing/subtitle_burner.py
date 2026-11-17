"""字幕烧录器 v4.7.0 — ffmpeg 硬字幕压制一条命令封装

把样式包直连 ffmpeg subtitles filter 的 force_style 参数，用户无需手写 filter_complex。
- ASS 双语文件内嵌 Orig/Trans 样式，libass 直接渲染；force_style 仅覆盖 Default 兜底
- SRT/VTT 无样式，用样式包生成的 force_style 上样式
- 复用硬件探测选择编码档位，避免拖累用户设备（死规则10）
"""

import os
import subprocess
from typing import Any, Dict, Optional

from ..logger import get_logger

logger = get_logger(__name__)


class SubtitleBurner:
    """ffmpeg 硬字幕烧录器"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.burn_cfg = config.get("burn", {}) or config.get("auto_editor", {})
        self.ffmpeg = self.burn_cfg.get("ffmpeg_path", "ffmpeg")
        self.codec = self.burn_cfg.get("codec", "libx264")
        self.preset = self.burn_cfg.get("preset", "veryfast")
        self.crf = self.burn_cfg.get("crf", 23)
        self.output_dir = self.burn_cfg.get("output_dir", "output")

    # ---------- force_style 生成 ----------

    @staticmethod
    def build_force_style(pack: Dict[str, Any], track: str = "default") -> str:
        """把样式包的 ASS 字段转成 libass force_style 字符串"""
        ass = pack.get("ass", {}) if track == "default" else pack.get("bilingual", {}).get(track, {})
        if not ass:
            ass = pack.get("ass", {})

        field_map = [
            ("FontName", "font"), ("FontSize", "size"),
            ("PrimaryColour", "primary"), ("SecondaryColour", "secondary"),
            ("OutlineColour", "outline"), ("BackColour", "back"),
            ("Bold", "bold"), ("Italic", "italic"),
            ("BorderStyle", "border_style"), ("Outline", "outline_width"),
            ("Shadow", "shadow"), ("Alignment", "alignment"),
            ("MarginL", "margin_l"), ("MarginR", "margin_r"), ("MarginV", "margin_v"),
        ]
        parts = [f"{fs}={ass[ak]}" for fs, ak in field_map if ak in ass]
        return ",".join(parts)

    @staticmethod
    def _escape_filter_path(path: str) -> str:
        """转义 subtitles filter 中的路径（Windows 冒号/反斜杠/单引号）"""
        p = os.path.abspath(path).replace("\\", "/")
        p = p.replace(":", "\\:")
        p = p.replace("'", "\\'")
        return p

    # ---------- 硬件档位（死规则10） ----------

    def _resolve_preset(self, hardware_tier: Optional[str] = None) -> str:
        """按硬件档位选编码 preset，低配用更快的档位"""
        if hardware_tier == "low":
            return "ultrafast"
        if hardware_tier == "high" and self.preset == "veryfast":
            return "medium"
        return self.preset

    # ---------- 主入口 ----------

    def burn(
        self,
        video_path: str,
        subtitle_path: str,
        output_path: Optional[str] = None,
        style_pack: Optional[Dict[str, Any]] = None,
        force_style: Optional[str] = None,
        hardware_tier: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        烧录硬字幕。

        Args:
            video_path: 源视频
            subtitle_path: 字幕文件（SRT/ASS/VTT）
            output_path: 输出视频路径（缺省自动置于 output_dir）
            style_pack: 样式包（用于生成 force_style）
            force_style: 直接指定 force_style（优先级高于 style_pack）
            hardware_tier: 硬件档位 low/mid/high

        Returns:
            {"success", "output_path", "command", "error"}
        """
        result: Dict[str, Any] = {
            "success": False, "output_path": None, "command": None, "error": None,
        }

        if not video_path or not os.path.exists(video_path):
            result["error"] = f"视频文件不存在: {video_path}"
            return result
        if not subtitle_path or not os.path.exists(subtitle_path):
            result["error"] = f"字幕文件不存在: {subtitle_path}"
            return result

        # 生成 force_style
        fs = force_style
        if fs is None and style_pack:
            fs = self.build_force_style(style_pack)

        sub_escaped = self._escape_filter_path(subtitle_path)

        if output_path is None:
            os.makedirs(self.output_dir, exist_ok=True)
            base = os.path.splitext(os.path.basename(video_path))[0]
            output_path = os.path.join(self.output_dir, f"{base}_subtitled.mp4")
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        preset = self._resolve_preset(hardware_tier)
        if fs:
            vf = f"subtitles='{sub_escaped}':force_style='{fs}'"
        else:
            vf = f"subtitles='{sub_escaped}'"

        cmd = [
            self.ffmpeg, "-y", "-i", video_path,
            "-vf", vf,
            "-c:v", self.codec, "-preset", preset, "-crf", str(self.crf),
            "-c:a", "copy",
            output_path,
        ]
        result["command"] = " ".join(cmd)

        try:
            logger.info(f"字幕烧录: {os.path.basename(video_path)} -> {os.path.basename(output_path)}")
            proc = subprocess.run(
                cmd, capture_output=True, text=True, timeout=3600,
            )
            if proc.returncode == 0 and os.path.exists(output_path):
                result["success"] = True
                result["output_path"] = output_path
                logger.info(f"烧录完成: {output_path}")
            else:
                err = (proc.stderr or "").strip().splitlines()
                result["error"] = err[-1] if err else f"ffmpeg 退出码 {proc.returncode}"
                logger.warning(f"烧录失败: {result['error']}")
        except FileNotFoundError:
            result["error"] = "未找到 ffmpeg，请安装并确保在 PATH 中"
        except subprocess.TimeoutExpired:
            result["error"] = "烧录超时（超过 1 小时）"
        except Exception as e:
            result["error"] = f"烧录异常: {e}"

        return result
