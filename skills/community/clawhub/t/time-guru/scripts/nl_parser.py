"""
Natural language time parser for time-guru.
Parses activity descriptions to extract time ranges, durations, categories, and projects.
"""
import re
import logging
from typing import Dict, Optional, List, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


# Time patterns (Chinese)
TIME_PATTERNS_CN = {
    "exact_range": [
        r'(?:从)?(\d{1,2})[点时:：](\d{0,2})[分]*\s*(?:到|至|~|－|—|—)\s*(\d{1,2})[点时:：](\d{0,2})[分]*',
        r'(\d{1,2}):(\d{2})\s*(?:到|至|~|－|—)\s*(\d{1,2}):(\d{2})',
    ],
    "duration": [
        r'(\d+)\s*个?\s*(?:小时|h|hr)',
        r'(\d+)\s*个?\s*(?:分钟|min|m)(?:钟)?',
        r'(\d+)\s*个?\s*(?:半小时|半)[小]时?',
    ],
    "fuzzy_time": [
        r'(早上|上午|中午|下午|晚上|清晨|半夜|凌晨)',
        r'(刚才|刚刚|现在|之前在|正在)',
        r'(昨天|前天|今天|明天)',
    ],
    "activity": [
        r'(?:在|做了|写了|搞了|搞|弄了|做了个|写了些|看了|听了|复习|学习|练习|研究)',
    ],
}

# Time period definitions
FUZZY_TIME_MAP = {
    "早上": (6, 9),
    "上午": (9, 12),
    "中午": (12, 14),
    "下午": (14, 18),
    "晚上": (18, 22),
    "凌晨": (0, 6),
    "清晨": (5, 8),
    "半夜": (23, 1),
}


def parse_time_expression(text: str, now: Optional[datetime] = None) -> List[Dict]:
    """
    Parse a natural language time expression into structured entries.
    
    Examples:
    - "9点到11点写代码" → {"start": "09:00", "end": "11:00", "activity": "写代码"}
    - "下午开了2小时的会" → {"start": "14:00", "end": "16:00", "activity": "开会"}
    - "刚才一直在写代码" → {"start": now-1h, "duration_min": 60, "activity": "写代码"}
    
    Args:
        text: Natural language description.
        now: Current datetime (default: datetime.now()).
        
    Returns:
        List of parsed activity dicts.
    """
    if now is None:
        now = datetime.now()
    
    entries = []
    
    # Split by common delimiters for multi-activity descriptions
    parts = re.split(r'[,，、。;；\n]+', text)
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
        
        entry = _parse_single_expression(part, now)
        if entry:
            entries.append(entry)
    
    return entries


def _parse_single_expression(text: str, now: datetime) -> Optional[Dict]:
    """Parse a single activity expression."""
    entry = {
        "raw_text": text,
        "start": None,
        "end": None,
        "duration_minutes": None,
        "activity": "",
        "parsing_confidence": "low",
    }
    
    # Try exact time range first
    for pattern in TIME_PATTERNS_CN["exact_range"]:
        match = re.search(pattern, text)
        if match:
            groups = match.groups()
            if len(groups) == 4:
                start_h, start_m, end_h, end_m = groups
                start_h, end_h = int(start_h), int(end_h)
                start_m = int(start_m) if start_m else 0
                end_m = int(end_m) if end_m else 0
            elif len(groups) == 2:
                start_h, end_h = int(groups[0]), int(groups[1])
                start_m, end_m = 0, 0
            
            # Normalize hours (12h → 24h)
            start_h = _normalize_hour(start_h, text)
            end_h = _normalize_hour(end_h, text)
            
            entry["start"] = f"{start_h:02d}:{start_m:02d}"
            entry["end"] = f"{end_h:02d}:{end_m:02d}"
            
            # Calculate duration
            start_total = start_h * 60 + start_m
            end_total = end_h * 60 + end_m
            if end_total < start_total:
                # Crosses midnight
                end_total += 24 * 60
            entry["duration_minutes"] = end_total - start_total
            entry["parsing_confidence"] = "high"
            
            # Extract activity (text after time range)
            activity = _extract_activity(text, match.group(0))
            entry["activity"] = activity
            
            return entry
    
    # Try duration-based patterns
    duration_patterns = [
        (r'(\d+)\s*个?\s*(?:小时|h|hr)', 60),
        (r'(\d+)\s*个?\s*(?:分钟|min|m)', 1),
        (r'(\d+)\.5\s*(?:小时|h)', 90),
    ]
    
    for pattern, multiplier in duration_patterns:
        match = re.search(pattern, text)
        if match:
            try:
                duration_val = float(match.group(1))
            except ValueError:
                continue
            
            entry["duration_minutes"] = int(duration_val * multiplier)
            entry["parsing_confidence"] = "medium"
            
            # Infer start/end based on fuzzy time
            fuzzy = _detect_fuzzy_time(text)
            if fuzzy:
                start_h, start_m = fuzzy
                start_total = start_h * 60 + start_m
                end_total = start_total + entry["duration_minutes"]
                end_h = end_total // 60
                end_m = end_total % 60
                if end_h >= 24:
                    end_h -= 24
                entry["start"] = f"{start_h:02d}:{start_m:02d}"
                entry["end"] = f"{end_h:02d}:{end_m:02d}"
            else:
                # Default: "刚才" → last 1-2 hours
                if any(kw in text for kw in ["刚才", "刚刚", "之前"]):
                    end = now
                    start = end - timedelta(minutes=entry["duration_minutes"])
                    entry["start"] = start.strftime("%H:%M")
                    entry["end"] = end.strftime("%H:%M")
                    entry["parsing_confidence"] = "medium"
            
            # Extract activity
            activity = _extract_activity(text, match.group(0))
            entry["activity"] = activity
            
            return entry
    
    # Try fuzzy time only (no duration, no range)
    fuzzy = _detect_fuzzy_time(text)
    if fuzzy:
        start_h, start_m = fuzzy
        entry["start"] = f"{start_h:02d}:{start_m:02d}"
        entry["parsing_confidence"] = "low"
        
        # Default duration: 1 hour
        entry["duration_minutes"] = 60
        end_total = start_h * 60 + start_m + 60
        entry["end"] = f"{end_total // 60 % 24:02d}:{end_total % 60:02d}"
        
        activity = _extract_activity(text, "")
        entry["activity"] = activity
        
        return entry
    
    # Fallback: "刚才一直在做X" / "在做X"
    activity = _extract_activity(text, "")
    if activity:
        # Assume last hour
        entry["start"] = (now - timedelta(hours=1)).strftime("%H:%M")
        entry["end"] = now.strftime("%H:%M")
        entry["duration_minutes"] = 60
        entry["activity"] = activity
        entry["parsing_confidence"] = "low"
        return entry
    
    return None


def _normalize_hour(hour: int, text: str) -> int:
    """Normalize 12-hour to 24-hour format based on context."""
    if "下午" in text or "晚上" in text or "凌晨" in text:
        if 1 <= hour <= 12:
            if "凌晨" in text:
                return hour if hour <= 5 else hour
            return hour + 12 if hour < 12 else hour
    elif "上午" in text or "早上" in text:
        return hour if hour <= 12 else hour - 12
    return hour  # Assume 24h format


def _extract_activity(text: str, time_part: str) -> str:
    """Extract the activity description, removing time-related text."""
    # Remove the matched time pattern
    activity = text.replace(time_part, "").strip()
    
    # Remove common time-related words
    time_words = ["从", "到", "至", "点", "时", "分", "分钟", "小时", "半", 
                  "上午", "下午", "晚上", "中午", "早上", "凌晨", "刚才", 
                  "之前", "在", "一直在", "一直在做"]
    for word in time_words:
        activity = activity.replace(word, "")
    
    # Remove leading punctuation and whitespace
    activity = re.sub(r'^[,，、。\s]+', '', activity).strip()
    
    return activity if activity else text[:30]


def _detect_fuzzy_time(text: str) -> Optional[Tuple[int, int]]:
    """Detect fuzzy time references and return (hour, minute)."""
    for keyword, (start_h, end_h) in FUZZY_TIME_MAP.items():
        if keyword in text:
            # Return the midpoint of the time range
            if keyword == "半夜":
                return (23, 30)
            return ((start_h + end_h) // 2, 0)
    return None


def classify_intent(text: str) -> str:
    """
    Classify the user's intent from the input text.
    
    Returns one of: "log", "start", "stop", "report", "analyze", "goal", "project", "config"
    """
    text_lower = text.lower().strip()
    
    if text_lower in ("stop", "⏹", "结束", "停止"):
        return "stop"
    if text_lower.startswith("start ") or text_lower.startswith("开始 "):
        return "start"
    
    if any(kw in text_lower for kw in ("report", "日报", "周报", "月报", "报告")):
        return "report"
    if any(kw in text_lower for kw in ("analyze", "分析", "效率")):
        return "analyze"
    if any(kw in text_lower for kw in ("goal", "目标", "计划")):
        return "goal"
    if any(kw in text_lower for kw in ("project", "项目", "客户")):
        return "project"
    
    # Default: log
    return "log"
