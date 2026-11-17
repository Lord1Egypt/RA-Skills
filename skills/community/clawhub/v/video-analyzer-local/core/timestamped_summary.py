"""带时间戳视频摘要 — 生成点击可跳转的精华摘要列表"""

import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from .logger import get_logger

logger = get_logger(__name__)


class TimestampedSummary:
    """
    带时间戳的视频摘要生成器。
    
    特性：
    - 每个摘要含时间戳 [MM:SS]
    - HTML 报告点击可跳转到对应视频位置
    - 支持导出 JSON/MD 格式
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    def generate(
        self,
        highlights: Dict,
        fused_data: Dict,
        output_dir: str,
    ) -> Dict[str, Any]:
        """
        生成带时间戳的摘要报告。
        
        Args:
            highlights: HighlightExtractor 的输出
            fused_data: 融合分析数据
            output_dir: 输出目录
            
        Returns:
            摘要结果
        """
        os.makedirs(output_dir, exist_ok=True)
        
        highlights_list = highlights.get("highlights", []) if isinstance(highlights, dict) else []
        enriched_scenes = fused_data.get("scenes", [])
        
        if not highlights_list and enriched_scenes:
            # 如果没有 highlights，从 scenes 衍生摘要
            highlights_list = self._derive_highlights_from_scenes(enriched_scenes)
        
        # 生成各格式输出
        result = {
            "timestamped_items": highlights_list,
            "total_items": len(highlights_list),
        }
        
        # 生成带时间戳的 Markdown 摘要
        md_path = self._generate_markdown(highlights_list, output_dir)
        result["markdown_path"] = md_path
        
        # 生成 JSON 格式
        json_path = self._generate_json(highlights_list, output_dir)
        result["json_path"] = json_path
        
        logger.info(f"时间戳摘要完成: {len(highlights_list)} 个精华项")
        return result
    
    def _derive_highlights_from_scenes(self, scenes: List[Dict]) -> List[Dict]:
        """从场景数据中推导摘要"""
        items = []
        
        for scene in scenes:
            time_range = scene.get("time_range", {})
            start = time_range.get("start", 0)
            duration = time_range.get("duration", 0)
            content = scene.get("content", {})
            metrics = scene.get("metrics", {})
            
            # 跳过无声/太短场景
            if content.get("is_silent") or duration < 3:
                continue
            
            # 取场景内对话的前 80 字符作为摘要
            text = content.get("dialog", "")
            preview = text[:80].strip()
            
            if not preview:
                # 无声但有视觉信息
                objects = content.get("objects", [])
                ocr = content.get("ocr_text", "")
                scene_types = content.get("scene_types", [])
                if objects:
                    preview = f"画面中出现的物体: {', '.join(o['name'] for o in objects[:5])}"
                elif ocr:
                    preview = f"画面文字: {ocr[:60]}"
                elif scene_types:
                    preview = f"场景类型: {', '.join(scene_types)}"
                else:
                    continue
            
            scores = scene.get("highlight_score", metrics.get("dialog_coverage", 0.5) * 100)
            
            items.append({
                "start_time": round(start, 2),
                "end_time": round(start + duration, 2),
                "duration": round(duration, 2),
                "text_preview": preview,
                "score": round(scores, 1),
                "tags": scene.get("semantic_tags", [])[:3],
                "scene_index": scene.get("index"),
            })
        
        # 按得分排序，取前 20 个
        items.sort(key=lambda x: x.get("score", 0), reverse=True)
        items = items[:20]
        # 再按时间排序
        items.sort(key=lambda x: x.get("start_time", 0))
        
        return items
    
    def _generate_markdown(self, items: List[Dict], output_dir: str) -> str:
        """生成带时间戳的 Markdown 摘要"""
        lines = [
            "# 📋 视频精华摘要（带时间戳）",
            "",
            f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"> 共提取 {len(items)} 个精华片段",
            "",
            "## 摘要列表",
            "",
            "| 时间戳 | 精华内容 | 标签 |",
            "|--------|----------|------|",
        ]
        
        for item in items:
            ts = self._format_timestamp(item.get("start_time", 0))
            preview = item.get("text_preview", "")
            # 替换竖线避免破坏表格
            preview = preview.replace("|", "/").replace("\n", " ")
            tags = ", ".join(item.get("tags", [])[:3])
            lines.append(f"| [{ts}] | {preview} | {tags} |")
        
        lines.extend([
            "",
            "## 详细内容",
            "",
        ])
        
        for item in items:
            ts = self._format_timestamp(item.get("start_time", 0))
            end_ts = self._format_timestamp(item.get("end_time", 0))
            score = item.get("score", 0)
            
            lines.extend([
                f"### [{ts}] {item.get('text_preview', '')[:60]}",
                "",
                f"- 时间段: {ts} ~ {end_ts}",
                f"- 持续: {item.get('duration', 0):.1f}秒",
                f"- 精华评分: {score}",
                f"- 标签: {', '.join(item.get('tags', []))}",
                "",
            ])
        
        md_content = "\n".join(lines)
        md_path = os.path.join(output_dir, "timestamped_summary.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        
        return md_path
    
    def _generate_json(self, items: List[Dict], output_dir: str) -> str:
        """生成 JSON 格式的时间戳摘要"""
        data = {
            "generated_at": datetime.now().isoformat(),
            "total_items": len(items),
            "items": [
                {
                    "start_time": item.get("start_time"),
                    "end_time": item.get("end_time"),
                    "duration": item.get("duration"),
                    "timestamp_formatted": self._format_timestamp(item.get("start_time", 0)),
                    "text_preview": item.get("text_preview"),
                    "score": item.get("score"),
                    "tags": item.get("tags"),
                }
                for item in items
            ]
        }
        
        json_path = os.path.join(output_dir, "timestamped_summary.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return json_path
    
    @staticmethod
    def _format_timestamp(seconds: float) -> str:
        """格式化为 MM:SS 或 H:MM:SS"""
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        
        if h > 0:
            return f"{h}:{m:02d}:{s:02d}"
        return f"{m:02d}:{s:02d}"
