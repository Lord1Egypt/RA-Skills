"""
Content analyzer for identifying video segments and highlights
"""
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class SegmentType(Enum):
    """Types of video segments"""
    INTRODUCTION = "introduction"
    HIGHLIGHT = "highlight"
    EXPLANATION = "explanation"
    EXAMPLE = "example"
    SUMMARY = "summary"
    TRANSITION = "transition"
    OTHER = "other"


@dataclass
class VideoSegment:
    """A identified video segment"""
    start: float          # Start time in seconds
    end: float            # End time in seconds
    text: str             # Associated text
    segment_type: SegmentType
    importance: float     # Importance score (0-1)
    keywords: List[str]   # Key topics/words
    summary: str          # Brief summary


@dataclass
class AnalysisResult:
    """Result of content analysis"""
    success: bool
    segments: List[VideoSegment]
    total_duration: float
    topics: List[str]
    error: Optional[str] = None


class ContentAnalyzer:
    """Analyze transcribed content to identify edit-worthy segments"""
    
    def __init__(
        self,
        min_length: int = 5,
        max_length: int = 60,
        silence_threshold: float = 0.15
    ):
        """
        Initialize analyzer
        
        Args:
            min_length: Minimum segment length in seconds
            max_length: Maximum segment length in seconds
            silence_threshold: Threshold for detecting pauses
        """
        self.min_length = min_length
        self.max_length = max_length
        self.silence_threshold = silence_threshold
        
        # Keywords for segment type detection (Chinese + English)
        self.intro_keywords = ["首先", "开始", "介绍", "今天", "我们来", "大家好", 
                               "first", "start", "intro", "today", "welcome", "let's", "hey guys"]
        self.summary_keywords = ["总结", "最后", "总之", "综上所述", "回顾", "要点",
                                 "summary", "finally", "conclusion", "wrap up", "review", "key points"]
        self.example_keywords = ["例如", "比如", "举例", "实例", "就像",
                                 "for example", "like", "such as", "instance"]
        self.highlight_keywords = ["重要", "关键", "注意", "记住", "重点", "核心",
                                   "important", "key", "notice", "remember", "highlight", "main"]
    
    def analyze(
        self,
        transcription_path: Path,
        video_duration: Optional[float] = None
    ) -> AnalysisResult:
        """
        Analyze transcription to identify segments
        
        Args:
            transcription_path: Path to transcription JSON file
            video_duration: Total video duration (optional)
        
        Returns:
            AnalysisResult with identified segments
        """
        try:
            print(f"🔍 Analyzing content...")
            
            # Load transcription
            import json
            with open(transcription_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            segments_data = data.get("segments", [])
            if not segments_data:
                return AnalysisResult(
                    success=False,
                    segments=[],
                    total_duration=0,
                    topics=[],
                    error="No segments found in transcription"
                )
            
            # Convert to transcription segments
            from modules.transcriber import TranscriptionSegment
            trans_segments = [
                TranscriptionSegment(**seg)
                for seg in segments_data
            ]
            
            # Get duration
            duration = video_duration or data.get("duration", 0)
            
            # Identify segments
            video_segments = self._identify_segments(trans_segments, duration)
            
            # Extract topics
            topics = self._extract_topics(trans_segments)
            
            print(f"✅ Analysis complete: {len(video_segments)} segments identified")
            
            return AnalysisResult(
                success=True,
                segments=video_segments,
                total_duration=duration,
                topics=topics
            )
            
        except Exception as e:
            return AnalysisResult(
                success=False,
                segments=[],
                total_duration=0,
                topics=[],
                error=str(e)
            )
    
    def _identify_segments(
        self,
        segments: List,
        duration: float
    ) -> List[VideoSegment]:
        """Identify meaningful segments from transcription"""
        video_segments = []
        
        # Group segments into logical chunks
        chunks = self._group_segments(segments)
        
        for chunk in chunks:
            if not chunk:
                continue
            
            start = chunk[0].start
            end = chunk[-1].end
            text = " ".join([seg.text for seg in chunk])
            
            # Skip too short or too long segments
            seg_length = end - start
            if seg_length < self.min_length or seg_length > self.max_length:
                continue
            
            # Determine segment type
            seg_type = self._classify_segment(text)
            
            # Calculate importance
            importance = self._calculate_importance(text, seg_type)
            
            # Extract keywords
            keywords = self._extract_keywords(text)
            
            # Generate summary
            summary = self._generate_summary(text)
            
            video_segment = VideoSegment(
                start=start,
                end=end,
                text=text,
                segment_type=seg_type,
                importance=importance,
                keywords=keywords,
                summary=summary
            )
            
            video_segments.append(video_segment)
        
        # Sort by importance
        video_segments.sort(key=lambda x: x.importance, reverse=True)
        
        return video_segments
    
    def _group_segments(
        self,
        segments: List,
        max_gap: float = 2.0
    ) -> List[List]:
        """Group consecutive segments into chunks"""
        if not segments:
            return []
        
        chunks = []
        current_chunk = [segments[0]]
        
        for i in range(1, len(segments)):
            prev = segments[i - 1]
            curr = segments[i]
            
            # Check gap between segments
            gap = curr.start - prev.end
            
            if gap > max_gap:
                # Start new chunk
                chunks.append(current_chunk)
                current_chunk = [curr]
            else:
                current_chunk.append(curr)
        
        # Add last chunk
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    def _classify_segment(self, text: str) -> SegmentType:
        """Classify segment type based on content"""
        text_lower = text.lower()
        
        # Check for introduction
        if any(kw in text_lower for kw in self.intro_keywords):
            return SegmentType.INTRODUCTION
        
        # Check for summary
        if any(kw in text_lower for kw in self.summary_keywords):
            return SegmentType.SUMMARY
        
        # Check for examples
        if any(kw in text_lower for kw in self.example_keywords):
            return SegmentType.EXAMPLE
        
        # Check for highlights
        if any(kw in text_lower for kw in self.highlight_keywords):
            return SegmentType.HIGHLIGHT
        
        # Default to explanation
        return SegmentType.EXPLANATION
    
    def _calculate_importance(
        self,
        text: str,
        segment_type: SegmentType
    ) -> float:
        """Calculate importance score for segment"""
        score = 0.5  # Base score
        
        # Type-based scoring
        type_scores = {
            SegmentType.HIGHLIGHT: 0.3,
            SegmentType.EXAMPLE: 0.2,
            SegmentType.EXPLANATION: 0.1,
            SegmentType.INTRODUCTION: 0.0,
            SegmentType.SUMMARY: 0.15,
            SegmentType.TRANSITION: -0.1,
            SegmentType.OTHER: 0.0,
        }
        score += type_scores.get(segment_type, 0)
        
        # Length bonus (prefer medium-length segments)
        word_count = len(text.split())
        if 20 <= word_count <= 100:
            score += 0.1
        
        # Keyword density bonus
        important_words = ["为什么", "如何", "怎样", "方法", "技巧", "秘密"]
        for word in important_words:
            if word in text:
                score += 0.05
        
        return min(1.0, max(0.0, score))
    
    def _extract_keywords(self, text: str, max_keywords: int = 5) -> List[str]:
        """Extract key topics/words from text"""
        # Simple keyword extraction
        # Remove common words
        stop_words = {
            "的", "了", "是", "在", "我", "有", "和", "就", "不", "人",
            "都", "一", "一个", "上", "也", "很", "到", "说", "要", "去",
            "你", "会", "着", "没有", "看", "好", "自己", "这", "那", "他"
        }
        
        # Split into words (simple approach for Chinese)
        words = re.findall(r'[\w\u4e00-\u9fff]+', text)
        
        # Filter and count
        word_freq = {}
        for word in words:
            if word not in stop_words and len(word) > 1:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency
        sorted_words = sorted(
            word_freq.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [word for word, _ in sorted_words[:max_keywords]]
    
    def _generate_summary(self, text: str, max_length: int = 50) -> str:
        """Generate brief summary of segment"""
        # Simple extractive summary - take first sentence
        sentences = re.split(r'[。！？.!?]', text)
        
        if sentences and sentences[0].strip():
            summary = sentences[0].strip()
            if len(summary) > max_length:
                summary = summary[:max_length] + "..."
            return summary
        
        # Fallback: truncate text
        if len(text) > max_length:
            return text[:max_length] + "..."
        
        return text
    
    def save_analysis(self, result: AnalysisResult, output_path: Path):
        """Save analysis results to JSON"""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            "success": result.success,
            "total_duration": result.total_duration,
            "topics": result.topics,
            "segments": [
                {
                    "start": seg.start,
                    "end": seg.end,
                    "text": seg.text,
                    "segment_type": seg.segment_type.value,
                    "importance": seg.importance,
                    "keywords": seg.keywords,
                    "summary": seg.summary
                }
                for seg in result.segments
            ]
        }
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Saved analysis: {output_path}")
    
    def filter_segments(
        self,
        segments: List[VideoSegment],
        min_importance: float = 0.5,
        max_segments: int = 10
    ) -> List[VideoSegment]:
        """Filter segments by importance and limit count"""
        filtered = [
            seg for seg in segments
            if seg.importance >= min_importance
        ]
        
        return filtered[:max_segments]


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        analyzer = ContentAnalyzer()
        result = analyzer.analyze(Path(sys.argv[1]))
        print(f"Success: {result.success}")
        print(f"Segments: {len(result.segments)}")
        print(f"Topics: {result.topics}")
        for seg in result.segments[:3]:
            print(f"  [{seg.start:.1f}-{seg.end:.1f}s] {seg.summary}")
