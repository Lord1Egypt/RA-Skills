"""播客流水线 — 整合说话人分离 + 章节切片 + 金句提取，输出 Podcasting 2.0 标准"""

import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from ..logger import get_logger
from .highlight_extractor import HighlightExtractor

logger = get_logger(__name__)


class PodcastPipeline:
    """
    播客模式整合流水线。

    输入：音频文件 + ASR 转写结果
    输出：
    1. 逐说话人时间线 (speaker_timeline)
    2. Podcasting 2.0 标准章节标记 (chapters.json)
    3. 金句列表 (highlights)

    所有输出带时间戳，可直接导入播客平台。
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def run(
        self,
        audio_path: str,
        transcript: Dict[str, Any],
        output_dir: str,
        n_speakers: Optional[int] = None,
        diarize_profile: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        执行播客流水线。
        
        Args:
            audio_path: 音频文件路径
            transcript: ASR 转写结果（含 segments）
            output_dir: 输出目录
            n_speakers: 说话人数量（可选）
            diarize_profile: 分离预设 (interview/meeting/phone)
            
        Returns:
            {
                "speaker_timeline": [...],
                "chapters": {...},
                "highlights": [...],
                "output_files": {...},
            }
        """
        os.makedirs(output_dir, exist_ok=True)
        segments = transcript.get("segments", [])

        if not segments:
            logger.warning("无语音段数据，跳过播客流水线")
            return self._empty_result()

        logger.info(f"🎙️ 播客流水线开始: {len(segments)} 个语音段")

        # 1. 说话人分离
        from ..speaker_diarization import SpeakerDiarization
        diarizer = SpeakerDiarization(self.config)
        diarize_result = diarizer.diarize(audio_path, segments, n_speakers=n_speakers)
        n_speakers_detected = diarize_result.get("n_speakers", 1)

        # 2. 生成 Podcasting 2.0 章节标记
        chapters = self._generate_chapters(diarize_result, output_dir)

        # 3. 金句提取
        extractor = HighlightExtractor(self.config)
        highlight_result = extractor.extract(segments)
        highlights = highlight_result.get("highlights", [])

        # 4. 说话人时间线
        speaker_timeline = self._generate_speaker_timeline(diarize_result)

        # 5. 写入输出文件
        output_files = {}
        try:
            chapters_path = os.path.join(output_dir, "chapters.json")
            with open(chapters_path, "w", encoding="utf-8") as f:
                json.dump(chapters, f, ensure_ascii=False, indent=2)
            output_files["chapters"] = chapters_path
            logger.info(f"   ✅ chapters.json: {chapters_path}")
        except Exception as e:
            logger.warning(f"写入 chapters.json 失败: {e}")

        try:
            highlights_path = os.path.join(output_dir, "highlights.json")
            with open(highlights_path, "w", encoding="utf-8") as f:
                json.dump(highlights, f, ensure_ascii=False, indent=2)
            output_files["highlights"] = highlights_path
            logger.info(f"   ✅ highlights.json: {highlights_path}")
        except Exception as e:
            logger.warning(f"写入 highlights.json 失败: {e}")

        try:
            timeline_path = os.path.join(output_dir, "speaker_timeline.json")
            with open(timeline_path, "w", encoding="utf-8") as f:
                json.dump(speaker_timeline, f, ensure_ascii=False, indent=2)
            output_files["timeline"] = timeline_path
            logger.info(f"   ✅ speaker_timeline.json: {timeline_path}")
        except Exception as e:
            logger.warning(f"写入 speaker_timeline.json 失败: {e}")

        logger.info(
            f"✅ 播客流水线完成: {n_speakers_detected} 说话人, "
            f"{chapters.get('total_chapters', 0)} 章节, {len(highlights)} 金句"
        )

        return {
            "speaker_timeline": speaker_timeline,
            "chapters": chapters,
            "highlights": highlights,
            "output_files": output_files,
        }

    def _generate_chapters(
        self,
        diarize_result: Dict[str, Any],
        output_dir: str,
    ) -> Dict[str, Any]:
        """
        生成 Podcasting 2.0 标准 chapters.json。
        
        Podcasting 2.0 标准字段：
        - version: 版本号
        - chapters: [{startTime, title, img, url, toc, ...}]
        
        这里用说话人切换作为章节边界。
        """
        segments = diarize_result.get("segments", [])
        speaker_map = diarize_result.get("speaker_map", {})

        chapters = []
        current_chapter = None
        chapter_index = 0

        for seg in segments:
            speaker = seg.get("speaker", "unknown")
            start = seg.get("start", 0)
            text = seg.get("text", "").strip()

            if not text:
                continue

            # 说话人切换时创建新章节
            if current_chapter is None or current_chapter.get("speaker") != speaker:
                if current_chapter is not None:
                    chapters.append(current_chapter)

                chapter_index += 1
                speaker_name = speaker_map.get(speaker, {}).get("name", speaker)
                current_chapter = {
                    "index": chapter_index,
                    "startTime": start,
                    "title": f"【{speaker_name}】{text[:30]}...",
                    "speaker": speaker,
                    "speaker_name": speaker_name,
                    "sentences": [text],
                    "endTime": seg.get("end", 0),
                }
            else:
                current_chapter["sentences"].append(text)
                current_chapter["endTime"] = seg.get("end", 0)

        if current_chapter is not None:
            chapters.append(current_chapter)

        # 转为 Podcasting 2.0 格式
        podcasting_chapters = {
            "version": "1.2.0",
            "type": "Podcast",
            "chapters": [
                {
                    "startTime": ch["startTime"],
                    "title": ch["title"],
                    "speaker": ch.get("speaker_name", ""),
                    "toc": True,
                }
                for ch in chapters
            ],
            "total_chapters": len(chapters),
        }

        logger.info(f"   生成 {len(chapters)} 个章节")
        return podcasting_chapters

    def _generate_speaker_timeline(
        self,
        diarize_result: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        生成逐说话人时间线。
        
        Returns:
            [
                {
                    "speaker": "speaker_A",
                    "speaker_name": "说话人A",
                    "start": 0.0,
                    "end": 15.3,
                    "duration": 15.3,
                    "text": "...",
                }
            ]
        """
        segments = diarize_result.get("segments", [])
        speaker_map = diarize_result.get("speaker_map", {})

        timeline = []
        current = None

        for seg in segments:
            speaker = seg.get("speaker", "unknown")
            start = seg.get("start", 0)
            end = seg.get("end", 0)
            text = seg.get("text", "").strip()

            if not text:
                continue

            if current is None or current["speaker"] != speaker:
                if current is not None:
                    timeline.append(current)

                speaker_name = speaker_map.get(speaker, {}).get("name", speaker)
                current = {
                    "speaker": speaker,
                    "speaker_name": speaker_name,
                    "start": start,
                    "end": end,
                    "duration": round(end - start, 2),
                    "text": text,
                }
            else:
                current["end"] = end
                current["duration"] = round(end - current["start"], 2)
                current["text"] += text

        if current is not None:
            timeline.append(current)

        return timeline

    def _empty_result(self) -> Dict[str, Any]:
        return {
            "speaker_timeline": [],
            "chapters": {"version": "1.2.0", "type": "Podcast", "chapters": [], "total_chapters": 0},
            "highlights": [],
            "output_files": {},
        }
