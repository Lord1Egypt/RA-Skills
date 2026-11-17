"""字幕样式生成器 v4.7.0 — 样式包加载器（JSON 化样式 + SRT/ASS 双格式 + 双语同轴）

样式包从 templates/subtitle_styles/*.json 加载，加载失败时用内置兜底模板（死规则9降级）。
双语模式：原文轨 / 译文轨独立开关，ASS 下用 Orig / Trans 两个样式错位显示。
旧样式名（douyin/bilibili/movie/minimal）通过别名映射到新样式包，保持向后兼容。
"""

import json
import os
from typing import Any, Dict, List, Optional

from ..logger import get_logger

logger = get_logger(__name__)

# 包内样式包目录（相对 skill 根目录）
STYLE_PACK_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "templates", "subtitle_styles",
)

# 旧样式名 -> 新样式包 id（向后兼容）
STYLE_ALIASES = {
    "douyin": "variety",
    "bilibili": "variety",
    "movie": "interview",
    "minimal": "minimal",
}

# 内置兜底样式（JSON 缺失时使用，保证零依赖可运行）
BUILTIN_PACKS: Dict[str, Dict[str, Any]] = {
    "variety": {
        "id": "variety", "name": "综艺",
        "ass": {"font": "Microsoft YaHei", "size": 54, "primary": "&H0000FFFF",
                "secondary": "&H000000FF", "outline": "&H00000000", "back": "&H80000000",
                "bold": -1, "italic": 0, "border_style": 1, "outline_width": 4,
                "shadow": 1, "alignment": 2, "margin_l": 100, "margin_r": 100,
                "margin_v": 60, "encoding": 1},
        "bilingual": {
            "orig": {"primary": "&H00FFFFFF", "size": 42, "margin_v": 150, "alignment": 2, "outline_width": 3},
            "trans": {"primary": "&H0000FFFF", "size": 52, "margin_v": 55, "alignment": 2, "outline_width": 4},
        },
    },
    "interview": {
        "id": "interview", "name": "访谈",
        "ass": {"font": "Microsoft YaHei", "size": 46, "primary": "&H00FFFFFF",
                "secondary": "&H000000FF", "outline": "&H00000000", "back": "&H80000000",
                "bold": 0, "italic": 0, "border_style": 1, "outline_width": 2,
                "shadow": 1, "alignment": 2, "margin_l": 100, "margin_r": 100,
                "margin_v": 55, "encoding": 1},
        "bilingual": {
            "orig": {"primary": "&H00B0B0B0", "size": 36, "margin_v": 135, "alignment": 2, "outline_width": 2},
            "trans": {"primary": "&H00FFFFFF", "size": 46, "margin_v": 50, "alignment": 2, "outline_width": 2},
        },
    },
    "course": {
        "id": "course", "name": "课程",
        "ass": {"font": "Microsoft YaHei", "size": 48, "primary": "&H00FFFFFF",
                "secondary": "&H000000FF", "outline": "&H00000000", "back": "&H9A000000",
                "bold": 0, "italic": 0, "border_style": 3, "outline_width": 2,
                "shadow": 0, "alignment": 2, "margin_l": 120, "margin_r": 120,
                "margin_v": 70, "encoding": 1},
        "bilingual": {
            "orig": {"primary": "&H00D0D0D0", "size": 38, "margin_v": 160, "alignment": 2, "outline_width": 2},
            "trans": {"primary": "&H00FFFFFF", "size": 48, "margin_v": 65, "alignment": 2, "outline_width": 2},
        },
    },
    "minimal": {
        "id": "minimal", "name": "极简",
        "ass": {"font": "Microsoft YaHei", "size": 44, "primary": "&H00FFFFFF",
                "secondary": "&H000000FF", "outline": "&H00000000", "back": "&H80000000",
                "bold": 0, "italic": 0, "border_style": 1, "outline_width": 1,
                "shadow": 0, "alignment": 2, "margin_l": 100, "margin_r": 100,
                "margin_v": 50, "encoding": 1},
        "bilingual": {
            "orig": {"primary": "&H00C8C8C8", "size": 36, "margin_v": 125, "alignment": 2, "outline_width": 1},
            "trans": {"primary": "&H00FFFFFF", "size": 44, "margin_v": 48, "alignment": 2, "outline_width": 1},
        },
    },
    "vertical": {
        "id": "vertical", "name": "竖屏",
        "ass": {"font": "Microsoft YaHei", "size": 44, "primary": "&H00FFFFFF",
                "secondary": "&H000000FF", "outline": "&H00000000", "back": "&H80000000",
                "bold": -1, "italic": 0, "border_style": 1, "outline_width": 3,
                "shadow": 1, "alignment": 2, "margin_l": 60, "margin_r": 60,
                "margin_v": 220, "encoding": 1},
        "bilingual": {
            "orig": {"primary": "&H00E0E0E0", "size": 36, "margin_v": 330, "alignment": 2, "outline_width": 2},
            "trans": {"primary": "&H00FFFFFF", "size": 44, "margin_v": 215, "alignment": 2, "outline_width": 3},
        },
    },
}

DEFAULT_ASS = {
    "font": "Microsoft YaHei", "size": 48, "primary": "&H00FFFFFF",
    "secondary": "&H000000FF", "outline": "&H00000000", "back": "&H80000000",
    "bold": 0, "italic": 0, "border_style": 1, "outline_width": 2,
    "shadow": 0, "alignment": 2, "margin_l": 100, "margin_r": 100,
    "margin_v": 50, "encoding": 1,
}


class SubtitleStylist:
    """
    字幕样式包加载器（v4.7.0）。

    能力：
    - 从 templates/subtitle_styles/*.json 加载样式包，缺失时内置兜底
    - SRT / ASS / VTT 三种格式导出
    - 双语同轴：原文轨 + 译文轨独立开关（ASS 用 Orig/Trans 双样式，SRT 用双行文本）
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.editing_config = config.get("editing", {})
        self.subtitle_config = self.editing_config.get("subtitle", {})
        presets_cfg = config.get("subtitle_presets", {})

        self.default_style = presets_cfg.get("default", self.subtitle_config.get("default_style", "variety"))
        self.style_dir = presets_cfg.get("style_dir") or STYLE_PACK_DIR
        self.font_size = self.subtitle_config.get("font_size", 48)
        self.font_name = self.subtitle_config.get("font_name", "Microsoft YaHei")

    # ---------- 样式包加载 ----------

    def list_style_packs(self) -> List[str]:
        """列出可用样式包 id（JSON 文件 + 内置）"""
        ids = set(BUILTIN_PACKS.keys())
        if os.path.isdir(self.style_dir):
            for fn in os.listdir(self.style_dir):
                if fn.lower().endswith(".json"):
                    ids.add(os.path.splitext(fn)[0])
        return sorted(ids)

    def load_style_pack(self, style: Optional[str] = None) -> Dict[str, Any]:
        """加载样式包：先 JSON 文件，缺失则内置兜底"""
        style = self._resolve_style_id(style)

        if os.path.isdir(self.style_dir):
            path = os.path.join(self.style_dir, f"{style}.json")
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        pack = json.load(f)
                    return self._merge_defaults(pack)
                except Exception as e:
                    logger.warning(f"样式包 JSON 加载失败，改用内置模板: {style} - {e}")

        pack = dict(BUILTIN_PACKS.get(style, BUILTIN_PACKS["variety"]))
        return self._merge_defaults(pack)

    def _resolve_style_id(self, style: Optional[str]) -> str:
        style = style or self.default_style
        return STYLE_ALIASES.get(style, style)

    @staticmethod
    def _merge_defaults(pack: Dict[str, Any]) -> Dict[str, Any]:
        """补齐缺失字段，保证旧/简版 JSON 也能用"""
        ass = dict(DEFAULT_ASS)
        ass.update(pack.get("ass", {}) or {})
        pack = dict(pack)
        pack["ass"] = ass

        bil = pack.get("bilingual", {}) or {}
        base_orig = dict(ass)
        base_orig.update({"size": ass["size"] - 8, "margin_v": ass["margin_v"] + 90,
                          "primary": "&H00FFFFFF", "outline_width": max(1, ass["outline_width"] - 1)})
        base_trans = dict(ass)
        base_orig.update(bil.get("orig", {}) or {})
        base_trans.update(bil.get("trans", {}) or {})
        pack["bilingual"] = {"orig": base_orig, "trans": base_trans}
        return pack

    # ---------- 主入口 ----------

    def generate(
        self,
        transcript: Dict,
        output_path: str,
        style: str = None,
        format: str = "ass",
        bilingual: bool = False,
        original_track: bool = True,
        translation_track: bool = True,
        translation_segments: Optional[List[Dict]] = None,
    ) -> Optional[str]:
        """
        生成字幕文件（v4.7.0）。

        Args:
            transcript: 语音识别结果 {"segments":[{"start","end","text"}]}
            output_path: 输出文件路径
            style: 样式包 id（variety/interview/course/minimal/vertical，兼容旧名）
            format: 输出格式 srt/ass/vtt
            bilingual: 是否双语同轴
            original_track: 原文轨开关
            translation_track: 译文轨开关
            translation_segments: 译文片段，缺省时从 transcript["translated_segments"] 读取

        Returns:
            输出文件路径，失败返回 None
        """
        pack = self.load_style_pack(style)
        fmt = (format or "ass").lower()

        if bilingual and not original_track and not translation_track:
            original_track = True

        try:
            if fmt == "srt":
                return self._generate_srt(transcript, output_path, bilingual, original_track,
                                          translation_track, translation_segments)
            elif fmt == "ass":
                return self._generate_ass(transcript, output_path, pack, bilingual, original_track,
                                          translation_track, translation_segments)
            elif fmt == "vtt":
                return self._generate_vtt(transcript, output_path, bilingual, original_track,
                                          translation_track, translation_segments)
            else:
                logger.error(f"不支持的字幕格式: {format}")
                return None
        except Exception as e:
            logger.error(f"字幕生成失败: {e}")
            return None

    # ---------- 数据准备 ----------

    @staticmethod
    def _get_translation_map(
        transcript: Dict, translation_segments: Optional[List[Dict]]
    ) -> Dict[int, str]:
        segs = translation_segments
        if segs is None:
            segs = transcript.get("translated_segments") or transcript.get("translation") or []
        return {i: (s.get("text", "") or "").strip() for i, s in enumerate(segs) if s}

    # ---------- SRT ----------

    def _generate_srt(self, transcript, output_path, bilingual, orig_on, trans_on, trans_segs) -> str:
        segments = transcript.get("segments", [])
        tmap = self._get_translation_map(transcript, trans_segs) if bilingual else {}
        lines = []
        n = 0
        for i, seg in enumerate(segments):
            start = self._format_srt_time(seg.get("start", 0))
            end = self._format_srt_time(seg.get("end", 0))
            origin_text = (seg.get("text", "") or "").strip()
            trans_text = tmap.get(i, "")

            text_lines = []
            if orig_on and origin_text:
                text_lines.append(origin_text)
            if trans_on and trans_text:
                text_lines.append(trans_text)
            if not text_lines:
                continue

            n += 1
            lines.extend([str(n), f"{start} --> {end}", "\n".join(text_lines), ""])

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return output_path

    # ---------- ASS ----------

    @staticmethod
    def _ass_style_line(name: str, s: Dict[str, Any]) -> str:
        return (
            f"Style: {name},{s.get('font','Microsoft YaHei')},{s.get('size',48)},"
            f"{s.get('primary','&H00FFFFFF')},{s.get('secondary','&H000000FF')},"
            f"{s.get('outline','&H00000000')},{s.get('back','&H80000000')},"
            f"{s.get('bold',0)},{s.get('italic',0)},0,0,100,100,0,0,"
            f"{s.get('border_style',1)},{s.get('outline_width',2)},{s.get('shadow',0)},"
            f"{s.get('alignment',2)},{s.get('margin_l',100)},{s.get('margin_r',100)},"
            f"{s.get('margin_v',50)},{s.get('encoding',1)}"
        )

    def _generate_ass(self, transcript, output_path, pack, bilingual, orig_on, trans_on, trans_segs) -> str:
        segments = transcript.get("segments", [])
        tmap = self._get_translation_map(transcript, trans_segs) if bilingual else {}
        ass = pack["ass"]

        lines = [
            "[Script Info]",
            "Title: Video Analyzer Subtitles v4.7.0",
            "ScriptType: v4.00+",
            "PlayResX: 1920",
            "PlayResY: 1080",
            "ScaledBorderAndShadow: yes",
            "",
            "[V4+ Styles]",
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, "
            "BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, "
            "BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
            self._ass_style_line("Default", ass),
        ]
        if bilingual:
            if orig_on:
                lines.append(self._ass_style_line("Orig", pack["bilingual"]["orig"]))
            if trans_on:
                lines.append(self._ass_style_line("Trans", pack["bilingual"]["trans"]))

        lines.extend([
            "", "[Events]",
            "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
        ])

        for i, seg in enumerate(segments):
            start = self._format_ass_time(seg.get("start", 0))
            end = self._format_ass_time(seg.get("end", 0))
            origin_text = (seg.get("text", "") or "").strip().replace("\n", "\\N")
            trans_text = tmap.get(i, "").replace("\n", "\\N")

            if bilingual:
                if orig_on and origin_text:
                    lines.append(f"Dialogue: 0,{start},{end},Orig,,0,0,0,,{origin_text}")
                if trans_on and trans_text:
                    lines.append(f"Dialogue: 0,{start},{end},Trans,,0,0,0,,{trans_text}")
            else:
                if origin_text:
                    lines.append(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{origin_text}")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return output_path

    # ---------- VTT ----------

    def _generate_vtt(self, transcript, output_path, bilingual, orig_on, trans_on, trans_segs) -> str:
        segments = transcript.get("segments", [])
        tmap = self._get_translation_map(transcript, trans_segs) if bilingual else {}
        lines = ["WEBVTT", ""]
        for i, seg in enumerate(segments):
            start = self._format_vtt_time(seg.get("start", 0))
            end = self._format_vtt_time(seg.get("end", 0))
            origin_text = (seg.get("text", "") or "").strip()
            trans_text = tmap.get(i, "")
            text_lines = []
            if orig_on and origin_text:
                text_lines.append(origin_text)
            if trans_on and trans_text:
                text_lines.append(trans_text)
            if not text_lines:
                continue
            lines.extend([f"{start} --> {end}", "\n".join(text_lines), ""])
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return output_path

    # ---------- 时间格式化 ----------

    @staticmethod
    def _format_srt_time(seconds: float) -> str:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

    @staticmethod
    def _format_ass_time(seconds: float) -> str:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        centis = int((seconds % 1) * 100)
        return f"{hours}:{minutes:02d}:{secs:02d}.{centis:02d}"

    @staticmethod
    def _format_vtt_time(seconds: float) -> str:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"
