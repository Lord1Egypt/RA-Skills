"""剪映 draft.json 导出器 — 6.0 schema 适配 + 失败降级 SRT+EDL + EDL 导入指南"""

import json
import os
import re
from datetime import datetime
from typing import Any, Dict, List, Optional

from ..logger import get_logger

logger = get_logger(__name__)


class JianyingExporter:
    """
    剪映 draft.json 格式导出器。

    v4.4.0 升级：
    - 对齐剪映 6.0 新 schema (materials/tracks/segments)
    - 失败自动降级为 SRT + EDL
    - 输出 Premiere Pro / DaVinci / Final Cut EDL 导入指南文档
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.editing_config = config.get("editing", {})
        self.jianying_config = self.editing_config.get("jianying", {})
        self.fps = self.jianying_config.get("fps", 30)
        self.resolution = self.jianying_config.get("resolution", {"width": 1920, "height": 1080})

    def export(
        self,
        timeline: Dict,
        transcript: Dict = None,
        video_path: str = None,
        output_path: str = "draft.json",
        version: str = "6.0",
    ) -> Optional[str]:
        """
        导出剪映 draft.json 文件。

        Args:
            timeline: 剪辑时间线
            transcript: 语音识别结果（用于字幕）
            video_path: 原始视频路径
            output_path: 输出文件路径
            version: 剪映版本 (6.0/5.0/4.0)

        Returns:
            输出文件路径，失败返回 None
        """
        try:
            # 尝试构建 draft.json
            draft = self._build_draft(timeline, transcript, video_path, version)

            if draft is None:
                # 降级为 SRT + EDL
                logger.warning(f"剪映 draft.json 构建失败，降级为 SRT + EDL")
                return self._fallback_to_srt_edl(timeline, transcript, video_path, output_path)

            os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(draft, f, ensure_ascii=False, indent=2)

            logger.info(f"剪映 draft.json 已导出: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"剪映导出失败: {e}")
            # 降级为 SRT + EDL
            return self._fallback_to_srt_edl(timeline, transcript, video_path, output_path)

    def export_with_guide(
        self,
        timeline: Dict,
        transcript: Dict = None,
        video_path: str = None,
        output_dir: str = "output/jianying",
    ) -> Dict[str, Any]:
        """
        导出剪映 draft.json + EDL 导入指南。

        Args:
            timeline: 剪辑时间线
            transcript: 语音识别结果
            video_path: 原始视频路径
            output_dir: 输出目录

        Returns:
            {
                "draft_path": "draft.json路径",
                "edl_path": "EDL路径",
                "guide_path": "指南文档路径",
                "srt_path": "SRT路径",
                "format": "draft/edl_srt",
            }
        """
        result = {
            "draft_path": None,
            "edl_path": None,
            "guide_path": None,
            "srt_path": None,
            "format": "draft",
        }

        os.makedirs(output_dir, exist_ok=True)

        draft_path = os.path.join(output_dir, "draft.json")
        srt_path = os.path.join(output_dir, "subtitles.srt")
        edl_path = os.path.join(output_dir, "timeline.edl")
        guide_path = os.path.join(output_dir, "EDL_IMPORT_GUIDE.md")

        # 导出 draft.json
        draft_result = self.export(timeline, transcript, video_path, draft_path)
        if draft_result:
            result["draft_path"] = draft_path
            result["format"] = "draft"

        # 导出 SRT
        if transcript:
            srt_result = self._export_srt(transcript, srt_path)
            if srt_result:
                result["srt_path"] = srt_path

        # 导出 EDL
        edl_result = self._export_edl(timeline, edl_path)
        if edl_result:
            result["edl_path"] = edl_path
            result["format"] = "edl_srt" if not draft_result else "draft"

        # 生成 EDL 导入指南
        guide_result = self._generate_import_guide(guide_path)
        if guide_result:
            result["guide_path"] = guide_path

        return result

    def _build_draft(
        self,
        timeline: Dict,
        transcript: Dict = None,
        video_path: str = None,
        version: str = "6.0",
    ) -> Optional[Dict]:
        """构建完整的 draft.json 结构（6.0 schema）"""
        try:
            # 基础信息
            draft = {
                "version": "6.0.0" if version == "6.0" else "5.0.0",
                "type": "draft",
                "created_at": datetime.now().isoformat(),
                "title": "video-analyzer 导出",
                "fps": self.fps,
                "resolution": self.resolution,
            }

            # 素材信息
            materials = self._build_materials(video_path, transcript)
            if materials is None:
                return None
            draft["materials"] = materials

            # 轨道信息
            draft["tracks"] = self._build_tracks(timeline, video_path, transcript)

            # 片段信息
            draft["segments"] = self._build_segments(timeline, video_path)

            # 字幕文本
            if transcript:
                draft["texts"] = self._build_texts(transcript)

            # 特效/转场
            draft["effects"] = self._build_effects(timeline)

            # 验证 schema
            if not self._validate_schema(draft):
                return None

            return draft

        except Exception as e:
            logger.error(f"构建 draft.json 失败: {e}")
            return None

    def _validate_schema(self, draft: Dict) -> bool:
        """验证 draft.json schema 完整性"""
        required_keys = ["version", "materials", "tracks", "segments"]
        for key in required_keys:
            if key not in draft:
                logger.warning(f"draft.json 缺少必要字段: {key}")
                return False

        # 验证 tracks 结构
        tracks = draft.get("tracks", [])
        if not tracks:
            logger.warning("draft.json tracks 为空")
            return False

        for track in tracks:
            if "id" not in track or "type" not in track:
                logger.warning("track 缺少 id 或 type")
                return False

        return True

    def _build_materials(
        self,
        video_path: str = None,
        transcript: Dict = None,
    ) -> Optional[Dict]:
        """构建素材信息"""
        try:
            materials = {
                "videos": [],
                "audios": [],
                "texts": [],
                "effects": [],
            }

            if video_path:
                materials["videos"].append({
                    "id": "video_001",
                    "path": video_path,
                    "name": os.path.basename(video_path),
                    "duration": 0,
                    "width": self.resolution["width"],
                    "height": self.resolution["height"],
                    "fps": self.fps,
                })

            return materials
        except Exception as e:
            logger.error(f"构建 materials 失败: {e}")
            return None

    def _build_tracks(
        self,
        timeline: Dict,
        video_path: str = None,
        transcript: Dict = None,
    ) -> List[Dict]:
        """构建轨道列表"""
        tracks = []

        if video_path:
            tracks.append({
                "id": "track_video_001",
                "type": "video",
                "name": "视频轨道 1",
                "flag": 1,
                "segments": self._build_video_segments(timeline),
            })

            tracks.append({
                "id": "track_audio_001",
                "type": "audio",
                "name": "音频轨道 1",
                "flag": 1,
                "segments": self._build_audio_segments(timeline),
            })

        if transcript:
            tracks.append({
                "id": "track_text_001",
                "type": "text",
                "name": "字幕轨道 1",
                "flag": 0,
                "segments": self._build_text_segments(transcript),
            })

        return tracks

    def _build_video_segments(self, timeline: Dict) -> List[Dict]:
        """构建视频片段"""
        segments = []
        clips = timeline.get("clips", [])

        for i, clip in enumerate(clips):
            segments.append({
                "id": f"seg_video_{i:03d}",
                "material_id": "video_001",
                "source_time": [
                    int(clip.get("source_start", 0) * 1000),
                    int(clip.get("source_end", 0) * 1000),
                ],
                "target_time": [
                    int(clip.get("output_start", 0) * 1000),
                    int(clip.get("output_end", 0) * 1000),
                ],
                "speed": 1.0,
            })

        return segments

    def _build_audio_segments(self, timeline: Dict) -> List[Dict]:
        """构建音频片段"""
        segments = []
        clips = timeline.get("clips", [])

        for i, clip in enumerate(clips):
            segments.append({
                "id": f"seg_audio_{i:03d}",
                "material_id": "video_001",
                "source_time": [
                    int(clip.get("source_start", 0) * 1000),
                    int(clip.get("source_end", 0) * 1000),
                ],
                "target_time": [
                    int(clip.get("output_start", 0) * 1000),
                    int(clip.get("output_end", 0) * 1000),
                ],
                "speed": 1.0,
            })

        return segments

    def _build_text_segments(self, transcript: Dict) -> List[Dict]:
        """构建字幕片段"""
        segments = []
        segs = transcript.get("segments", [])

        for i, seg in enumerate(segs):
            start_ms = int(seg.get("start", 0) * 1000)
            end_ms = int(seg.get("end", 0) * 1000)
            text = seg.get("text", "").strip()

            if text:
                segments.append({
                    "id": f"seg_text_{i:03d}",
                    "text": text,
                    "start": start_ms,
                    "duration": end_ms - start_ms,
                    "style": self._get_text_style(),
                })

        return segments

    def _build_segments(self, timeline: Dict, video_path: str = None) -> List[Dict]:
        """构建片段列表"""
        segments = []
        clips = timeline.get("clips", [])

        for i, clip in enumerate(clips):
            segments.append({
                "id": f"segment_{i:03d}",
                "track_id": "track_video_001",
                "material_id": "video_001" if video_path else None,
                "source_range": [
                    int(clip.get("source_start", 0) * 1000),
                    int(clip.get("source_end", 0) * 1000),
                ],
                "target_range": [
                    int(clip.get("output_start", 0) * 1000),
                    int(clip.get("output_end", 0) * 1000),
                ],
            })

        return segments

    def _build_texts(self, transcript: Dict) -> List[Dict]:
        """构建文本列表"""
        texts = []
        segs = transcript.get("segments", [])

        for i, seg in enumerate(segs):
            text = seg.get("text", "").strip()
            if text:
                texts.append({
                    "id": f"text_{i:03d}",
                    "content": text,
                    "start": int(seg.get("start", 0) * 1000),
                    "duration": int((seg.get("end", 0) - seg.get("start", 0)) * 1000),
                })

        return texts

    def _build_effects(self, timeline: Dict) -> List[Dict]:
        """构建转场/特效列表"""
        effects = []
        clips = timeline.get("clips", [])

        for i in range(len(clips) - 1):
            effects.append({
                "id": f"effect_{i:03d}",
                "type": "transition",
                "name": "淡入淡出",
                "duration": 500,
                "target_segment": f"segment_{i:03d}",
                "next_segment": f"segment_{i+1:03d}",
            })

        return effects

    def _get_text_style(self) -> Dict:
        """获取默认字幕样式"""
        return {
            "font": "Microsoft YaHei",
            "size": 48,
            "color": "#FFFFFF",
            "background": "#000000",
            "background_alpha": 0.5,
            "position": "bottom_center",
            "alignment": "center",
        }

    def _fallback_to_srt_edl(
        self,
        timeline: Dict,
        transcript: Dict = None,
        video_path: str = None,
        output_path: str = "output",
    ) -> str:
        """降级为 SRT + EDL 格式"""
        output_dir = os.path.dirname(output_dir) if os.path.isfile(output_dir) else output_path
        os.makedirs(output_dir, exist_ok=True)

        # 导出 SRT
        if transcript:
            srt_path = os.path.join(output_dir, "subtitles.srt")
            self._export_srt(transcript, srt_path)

        # 导出 EDL
        edl_path = os.path.join(output_dir, "timeline.edl")
        self._export_edl(timeline, edl_path)

        # 生成导入指南
        guide_path = os.path.join(output_dir, "EDL_IMPORT_GUIDE.md")
        self._generate_import_guide(guide_path)

        return output_dir

    def _export_srt(self, transcript: Dict, output_path: str) -> bool:
        """导出 SRT 字幕"""
        try:
            segs = transcript.get("segments", [])
            with open(output_path, "w", encoding="utf-8") as f:
                for i, seg in enumerate(segs, 1):
                    start = self._seconds_to_srt_time(seg.get("start", 0))
                    end = self._seconds_to_srt_time(seg.get("end", 0))
                    text = seg.get("text", "").strip()
                    if text:
                        f.write(f"{i}\n{start} --> {end}\n{text}\n\n")
            return True
        except Exception as e:
            logger.error(f"导出 SRT 失败: {e}")
            return False

    def _export_edl(self, timeline: Dict, output_path: str) -> bool:
        """导出 EDL 时间线"""
        try:
            clips = timeline.get("clips", [])
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("TITLE: video-analyzer export\n")
                f.write("FCM: NON-DROP FRAME\n\n")

                for i, clip in enumerate(clips, 1):
                    event_num = f"{i:03d}"
                    src_start = self._seconds_to_edl_time(clip.get("source_start", 0))
                    src_end = self._seconds_to_edl_time(clip.get("source_end", 0))
                    rec_start = self._seconds_to_edl_time(clip.get("output_start", 0))
                    rec_end = self._seconds_to_edl_time(clip.get("output_end", 0))

                    f.write(f"{event_num}  AX       V     C        {src_start} {src_end} {rec_start} {rec_end}\n")
                    f.write(f"* FROM CLIP NAME: {clip.get('name', 'segment')}\n\n")

            return True
        except Exception as e:
            logger.error(f"导出 EDL 失败: {e}")
            return False

    def _generate_import_guide(self, output_path: str) -> bool:
        """生成 EDL 导入指南文档"""
        try:
            guide = """# EDL 导入指南

## 支持软件

| 软件 | 导入方式 | 备注 |
|------|---------|------|
| Adobe Premiere Pro | 文件 → 导入 → 选择 .edl | 需先导入素材 |
| DaVinci Resolve | 文件 → 导入时间线 → 导入 EDL | 支持 CMX3600 |
| Final Cut Pro | 文件 → 导入 → EDL | 需 XML 转换 |
| Avid Media Composer | File → Import → EDL | 原生支持 |

## 导入步骤

### Premiere Pro
1. 打开 Premiere Pro
2. 文件 → 导入 → 选择 `timeline.edl`
3. 在项目面板中找到导入的序列
4. 将素材拖入时间线即可开始编辑

### DaVinci Resolve
1. 打开 DaVinci Resolve
2. 文件 → 导入时间线 → 导入 EDL
3. 选择 `timeline.edl`
4. 确认时间线设置后导入

### Final Cut Pro
1. Final Cut Pro 不直接支持 EDL
2. 使用第三方工具将 EDL 转换为 XML（如 XtoCC）
3. 导入 XML 到 Final Cut Pro

## 注意事项

- EDL 仅包含时间码信息，不包含实际素材
- 导入前请确保素材文件在正确路径
- 如时间码不匹配，请检查帧率设置（默认 30fps）
- 字幕文件 `subtitles.srt` 可单独导入

## 故障排除

| 问题 | 解决方案 |
|------|---------|
| 时间码偏移 | 检查源视频帧率是否匹配 |
| 素材离线 | 重新链接素材文件路径 |
| 字幕乱码 | 确保 SRT 文件为 UTF-8 编码 |
| EDL 导入失败 | 检查 EDL 格式是否为 CMX3600 |

---
*由 video-analyzer 自动生成*
"""
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(guide)
            return True
        except Exception as e:
            logger.error(f"生成导入指南失败: {e}")
            return False

    def _seconds_to_srt_time(self, seconds: float) -> str:
        """秒转 SRT 时间码"""
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        ms = int((seconds % 1) * 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    def _seconds_to_edl_time(self, seconds: float) -> str:
        """秒转 EDL 时间码 (HH:MM:SS:FF)"""
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        ff = int((seconds % 1) * self.fps)
        return f"{h:02d}:{m:02d}:{s:02d}:{ff:02d}"
