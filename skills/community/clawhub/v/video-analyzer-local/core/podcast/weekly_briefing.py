"""听后简报引擎 — 周聚合视图：本周处理列表/时长分布/金句 Top10"""

import os
import sqlite3
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from ..logger import get_logger

logger = get_logger(__name__)


class WeeklyBriefing:
    """
    听后简报生成器。
    
    复用 queue_manager 的 SQLite 队列，按周聚合生成 HTML 简报。
    内容：本周处理列表 / 时长分布 / 金句 Top10。
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.briefing_config = config.get("weekly_briefing", {})
        self.cache_dir = config.get("processing", {}).get("cache_dir", ".cache")
        self.db_path = self.briefing_config.get("db_path", os.path.join(self.cache_dir, "queue.db"))
        self.output_dir = self.briefing_config.get("output_dir", os.path.join(self.cache_dir, "briefings"))

    def generate(
        self,
        week_start: Optional[datetime] = None,
        output_path: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        生成周简报。
        
        Args:
            week_start: 周起始日期（默认本周一）
            output_path: 输出 HTML 路径（默认自动生成）
            
        Returns:
            {
                "output_path": "path/to/briefing.html",
                "week_range": "2026-10-27 ~ 2026-11-02",
                "stats": {...},
            }
        """
        os.makedirs(self.output_dir, exist_ok=True)
        
        if week_start is None:
            today = datetime.now()
            week_start = today - timedelta(days=today.weekday())
        
        week_end = week_start + timedelta(days=7)
        
        # 查询本周完成的任务
        tasks = self._query_week_tasks(week_start, week_end)
        
        # 聚合统计
        stats = self._aggregate_stats(tasks)
        
        # 获取金句 Top10
        highlights = self._get_top_highlights(tasks, top_n=10)
        
        # 生成 HTML
        html = self._render_html(stats, highlights, week_start, week_end)
        
        if output_path is None:
            filename = f"briefing_{week_start.strftime('%Y%m%d')}.html"
            output_path = os.path.join(self.output_dir, filename)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        
        logger.info(f"✅ 周简报已生成: {output_path}")
        logger.info(f"   本周处理: {stats['total_tasks']} 个文件, {stats['total_duration']:.0f} 秒")
        
        return {
            "output_path": output_path,
            "week_range": f"{week_start.strftime('%Y-%m-%d')} ~ {week_end.strftime('%Y-%m-%d')}",
            "stats": stats,
        }

    def _query_week_tasks(
        self,
        week_start: datetime,
        week_end: datetime,
    ) -> List[Dict[str, Any]]:
        """查询本周完成的任务"""
        if not os.path.exists(self.db_path):
            logger.warning(f"队列数据库不存在: {self.db_path}")
            return []
        
        start_ts = week_start.timestamp()
        end_ts = week_end.timestamp()
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(
                    "SELECT * FROM tasks WHERE status = 'done' "
                    "AND completed_at >= ? AND completed_at < ? "
                    "ORDER BY completed_at ASC",
                    (start_ts, end_ts),
                )
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.warning(f"查询队列失败: {e}")
            return []

    def _aggregate_stats(self, tasks: List[Dict]) -> Dict[str, Any]:
        """聚合统计"""
        total_duration = 0
        total_tasks = len(tasks)
        daily_counts = {}
        
        for task in tasks:
            # 解析 artifact_paths 获取时长
            artifact_paths = task.get("artifact_paths", "")
            if artifact_paths:
                try:
                    import json
                    paths = json.loads(artifact_paths)
                    if isinstance(paths, dict):
                        # 尝试获取摘要中的时长
                        summary_path = paths.get("timestamped_summary", "")
                        if summary_path and os.path.exists(summary_path):
                            with open(summary_path, "r", encoding="utf-8") as f:
                                content = f.read()
                                import re
                                duration_match = re.search(r"总时长[：:]\s*([\d:]+)", content)
                                if duration_match:
                                    dur_str = duration_match.group(1)
                                    parts = dur_str.split(":")
                                    if len(parts) == 3:
                                        total_duration += int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
                                    elif len(parts) == 2:
                                        total_duration += int(parts[0]) * 60 + int(parts[1])
                except Exception:
                    pass
            
            # 按天统计
            completed = task.get("completed_at", 0)
            if completed:
                day = datetime.fromtimestamp(completed).strftime("%Y-%m-%d")
                daily_counts[day] = daily_counts.get(day, 0) + 1
        
        return {
            "total_tasks": total_tasks,
            "total_duration": total_duration,
            "daily_counts": daily_counts,
            "avg_duration": total_duration / total_tasks if total_tasks > 0 else 0,
        }

    def _get_top_highlights(
        self,
        tasks: List[Dict],
        top_n: int = 10,
    ) -> List[Dict[str, Any]]:
        """获取金句 Top N"""
        all_highlights = []
        
        for task in tasks:
            artifact_paths = task.get("artifact_paths", "")
            if not artifact_paths:
                continue
            
            try:
                import json
                paths = json.loads(artifact_paths)
                highlights_path = paths.get("highlights", "")
                if highlights_path and os.path.exists(highlights_path):
                    with open(highlights_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            for h in data:
                                h["source_file"] = os.path.basename(task.get("input_path", ""))
                            all_highlights.extend(data)
            except Exception:
                continue
        
        # 按置信度排序
        all_highlights.sort(key=lambda x: x.get("confidence", 0), reverse=True)
        return all_highlights[:top_n]

    def _render_html(
        self,
        stats: Dict[str, Any],
        highlights: List[Dict],
        week_start: datetime,
        week_end: datetime,
    ) -> str:
        """渲染 HTML 简报"""
        daily_rows = ""
        for day, count in sorted(stats.get("daily_counts", {}).items()):
            daily_rows += f"<tr><td>{day}</td><td>{count} 个</td></tr>\n"
        
        highlight_rows = ""
        for i, h in enumerate(highlights, 1):
            text = h.get("text", "")[:80]
            confidence = h.get("confidence", 0)
            source = h.get("source_file", "")
            highlight_rows += f"<tr><td>{i}</td><td>{text}...</td><td>{confidence:.0%}</td><td>{source}</td></tr>\n"
        
        total_min = stats["total_duration"] / 60
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>听后简报 — {week_start.strftime('%Y-%m-%d')}</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; color: #333; }}
h1 {{ color: #1a1a1a; border-bottom: 2px solid #0F6E56; padding-bottom: 10px; }}
h2 {{ color: #0F6E56; margin-top: 30px; }}
.stats {{ display: flex; gap: 20px; margin: 20px 0; }}
.stat-box {{ background: #f5f5f5; padding: 15px 25px; border-radius: 8px; text-align: center; }}
.stat-box .number {{ font-size: 28px; font-weight: bold; color: #0F6E56; }}
.stat-box .label {{ font-size: 12px; color: #666; margin-top: 4px; }}
table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
th, td {{ padding: 8px 12px; text-align: left; border-bottom: 1px solid #eee; }}
th {{ background: #f0f0f0; font-size: 13px; }}
td {{ font-size: 13px; }}
</style>
</head>
<body>
<h1>📊 听后简报</h1>
<p style="color: #666;">{week_start.strftime('%Y年%m月%d日')} ~ {week_end.strftime('%Y年%m月%d日')}</p>

<div class="stats">
  <div class="stat-box">
    <div class="number">{stats['total_tasks']}</div>
    <div class="label">处理文件</div>
  </div>
  <div class="stat-box">
    <div class="number">{total_min:.0f}</div>
    <div class="label">总时长(分)</div>
  </div>
  <div class="stat-box">
    <div class="number">{len(highlights)}</div>
    <div class="label">金句数</div>
  </div>
</div>

<h2>📅 每日处理</h2>
<table>
<tr><th>日期</th><th>处理数</th></tr>
{daily_rows if daily_rows else '<tr><td colspan="2" style="color:#999">本周暂无处理记录</td></tr>'}
</table>

<h2>🌟 金句 Top10</h2>
<table>
<tr><th>#</th><th>内容</th><th>置信度</th><th>来源</th></tr>
{highlight_rows if highlight_rows else '<tr><td colspan="4" style="color:#999">暂无金句记录</td></tr>'}
</table>

<p style="margin-top:40px;color:#999;font-size:12px;text-align:center;">由 video-analyzer v4.6.0 自动生成</p>
</body>
</html>"""
        return html
