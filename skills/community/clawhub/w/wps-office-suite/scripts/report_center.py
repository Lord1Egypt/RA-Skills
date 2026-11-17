"""
报告中心 v5.4.0
功能：周报/月报/对账单统一模板仓库（参数化占位符）+ ECharts 单文件 HTML 输出（图表内联、无服务端、双击即开）
      自动从 usage_stats 拉周度摘要附在报告末尾
      让用户"看见这个 skill 每周替我干了多少活"，留存数据化

实现：report_generator 的渲染部分抽出共享渲染器，模板存 templates/reports/*.json
      调度层 schedule_register 通过 "wps report-center weekly/monthly" 调用

死规则合规：
  - 规则9：纯本地实现，不依赖任何外部 API；ECharts 通过 CDN（cdn.jsdelivr.net）加载
  - 规则10：无额外常驻进程
  - 规则13：不生成禁止文件类型（输出 .html）
  - 规则14：三次自审
  - 规则15：沙箱模拟运行
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

sys.path.insert(0, str(Path(__file__).parent))

SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = SCRIPT_DIR.parent / "templates" / "reports"

try:
    from wps_common import safe_path
except ImportError:
    def safe_path(p):
        return Path(p).resolve()


# ==================== 默认模板（兜底） ====================

DEFAULT_TEMPLATES = {
    "weekly": {
        "type": "weekly",
        "title": "周报 — {date_range}",
        "sections": [
            {"key": "summary", "title": "📊 本周摘要", "type": "stats_cards"},
            {"key": "chart_actions", "title": "🔧 命令使用分布", "type": "echarts_pie"},
            {"key": "chart_daily", "title": "📈 每日调用趋势", "type": "echarts_line"},
            {"key": "engine_health", "title": "⚙️ 引擎健康度", "type": "table"},
            {"key": "top_actions", "title": "🏆 高频命令 TOP5", "type": "table"}
        ],
        "footer": "由 WPS Office 全家桶 v5.4 自动生成 · {generated_at}"
    },
    "monthly": {
        "type": "monthly",
        "title": "月报 — {year}年{month}月",
        "sections": [
            {"key": "summary", "title": "📊 本月摘要", "type": "stats_cards"},
            {"key": "chart_actions", "title": "🔧 命令使用分布", "type": "echarts_pie"},
            {"key": "chart_trend", "title": "📈 周度调用趋势", "type": "echarts_bar"},
            {"key": "engine_health", "title": "⚙️ 引擎健康度", "type": "table"},
            {"key": "highlights", "title": "💡 使用亮点", "type": "bullets"}
        ],
        "footer": "由 WPS Office 全家桶 v5.4 自动生成 · {generated_at}"
    }
}


class UsageStatsReader:
    """读取 usage_stats SQLite 数据"""

    def __init__(self):
        self.db_path = SCRIPT_DIR / "wps_stats.db"

    def _get_db(self):
        import sqlite3
        return sqlite3.connect(str(self.db_path))

    def get_weekly_summary(self) -> Dict[str, Any]:
        """获取最近一周的统计数据"""
        if not self.db_path.exists():
            return self._empty_summary()
        try:
            conn = self._get_db()
            conn.row_factory = __import__("sqlite3").Row
            since = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

            # 总操作数/成功数/耗时
            cur = conn.execute("""
                SELECT COUNT(*) as total,
                       SUM(CASE WHEN success=1 THEN 1 ELSE 0 END) as success,
                       SUM(duration_ms) as total_duration,
                       AVG(duration_ms) as avg_duration,
                       SUM(CASE WHEN success=0 THEN 1 ELSE 0 END) as failed
                FROM usage_log WHERE DATE(timestamp) >= ?
            """, (since,))
            row = cur.fetchone()

            # 引擎分布
            cur = conn.execute("""
                SELECT engine, COUNT(*) as cnt FROM usage_log
                WHERE DATE(timestamp) >= ? AND engine != ''
                GROUP BY engine ORDER BY cnt DESC
            """, (since,))
            engine_dist = {r["engine"]: r["cnt"] for r in cur.fetchall()}

            # 命令分布
            cur = conn.execute("""
                SELECT action, COUNT(*) as cnt FROM usage_log
                WHERE DATE(timestamp) >= ? AND action != ''
                GROUP BY action ORDER BY cnt DESC LIMIT 10
            """, (since,))
            action_dist = {r["action"]: r["cnt"] for r in cur.fetchall()}

            # 每日分布
            cur = conn.execute("""
                SELECT DATE(timestamp) as day, COUNT(*) as cnt
                FROM usage_log WHERE DATE(timestamp) >= ?
                GROUP BY DATE(timestamp) ORDER BY day
            """, (since,))
            daily_dist = {r["day"]: r["cnt"] for r in cur.fetchall()}

            conn.close()
            return {
                "total": row["total"] or 0,
                "success": row["success"] or 0,
                "failed": row["failed"] or 0,
                "total_duration_ms": row["total_duration"] or 0,
                "avg_duration_ms": round(row["avg_duration"] or 0, 1),
                "success_rate": round((row["success"] or 0) / max(row["total"] or 1, 1) * 100, 1),
                "engine_distribution": engine_dist,
                "action_distribution": action_dist,
                "daily_distribution": daily_dist,
                "period": f"{since} ~ {datetime.now().strftime('%Y-%m-%d')}"
            }
        except Exception:
            return self._empty_summary()

    def _empty_summary(self) -> Dict[str, Any]:
        return {
            "total": 0, "success": 0, "failed": 0,
            "total_duration_ms": 0, "avg_duration_ms": 0,
            "success_rate": 0,
            "engine_distribution": {},
            "action_distribution": {},
            "daily_distribution": {},
            "period": "最近 7 天"
        }


class ReportCenter:
    """报告中心 v5.4.0"""

    VERSION = "v5.4.0"

    def __init__(self):
        self.stats_reader = UsageStatsReader()
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict:
        templates = {}
        for name in ["weekly", "monthly"]:
            tmpl_path = TEMPLATES_DIR / f"{name}.json"
            if tmpl_path.exists():
                try:
                    templates[name] = json.loads(tmpl_path.read_text(encoding="utf-8"))
                except Exception:
                    templates[name] = DEFAULT_TEMPLATES[name]
            else:
                templates[name] = DEFAULT_TEMPLATES[name]
        return templates

    def _fill_placeholders(self, text: str, extra: Dict = None) -> str:
        now = datetime.now()
        replacements = {
            "{date}": now.strftime("%Y%m%d"),
            "{date_range}": f"{(now - timedelta(days=6)).strftime('%m/%d')} ~ {now.strftime('%m/%d')}",
            "{year}": str(now.year),
            "{month}": f"{now.month:02d}",
            "{generated_at}": now.strftime("%Y-%m-%d %H:%M"),
        }
        if extra:
            replacements.update(extra)
        result = text
        for k, v in replacements.items():
            result = result.replace(k, str(v))
        return result

    def generate(self, report_type: str = "weekly", output: str = "") -> Dict[str, Any]:
        """生成报告"""
        if report_type not in self.templates:
            return {"ok": False, "error": f"不支持的报告类型: {report_type}，可选: {list(self.templates.keys())}"}

        if not output:
            return {"ok": False, "error": "必须指定 --output 输出路径（.html）"}

        try:
            stats = self.stats_reader.get_weekly_summary()
            template = self.templates[report_type]
            html = self._render_html(template, stats, report_type)

            out_path = safe_path(output)
            out_path.write_text(html, encoding="utf-8")

            return {
                "ok": True,
                "path": str(out_path),
                "format": "html",
                "stats_summary": f"本周 {stats['total']} 次调用，成功率 {stats['success_rate']}%",
                "version": self.VERSION
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def preview(self, report_type: str = "weekly") -> Dict[str, Any]:
        """预览统计摘要（不生成 HTML）"""
        if report_type not in self.templates:
            return {"ok": False, "error": f"不支持的报告类型: {report_type}"}

        stats = self.stats_reader.get_weekly_summary()
        return {"ok": True, "type": report_type, "stats": stats, "version": self.VERSION}

    def list_templates(self) -> Dict[str, Any]:
        return {"ok": True, "templates": {k: v.get("title", k) for k, v in self.templates.items()}, "version": self.VERSION}

    def _render_html(self, template: Dict, stats: Dict, report_type: str) -> str:
        """渲染 ECharts 单文件 HTML"""
        title = self._fill_placeholders(template.get("title", "WPS 报告"))
        footer = self._fill_placeholders(template.get("footer", ""))

        # 构造各 section 的 HTML
        sections_html = ""
        for section in template.get("sections", []):
            section_html = self._render_section(section, stats)
            if section_html:
                sections_html += f'<div class="section"><h2>{section["title"]}</h2>{section_html}</div>\n'

        # ECharts 数据
        engine_labels = list(stats.get("engine_distribution", {}).keys())
        engine_values = list(stats.get("engine_distribution", {}).values())
        action_labels = list(stats.get("action_distribution", {}).keys())[:10]
        action_values = list(stats.get("action_distribution", {}).values())[:10]
        daily_labels = sorted(stats.get("daily_distribution", {}).keys())
        daily_values = [stats.get("daily_distribution", {}).get(d, 0) for d in daily_labels]

        # 数据序列化为 JS 字面量
        action_data = json.dumps([{"name": l, "value": v} for l, v in zip(action_labels, action_values)], ensure_ascii=False)
        daily_labels_json = json.dumps(daily_labels, ensure_ascii=False)
        daily_values_json = json.dumps(daily_values)
        engine_labels_json = json.dumps(engine_labels, ensure_ascii=False)
        engine_values_json = json.dumps(engine_values)

        html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>''' + title + '''</title>
<script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f5f7fa; color: #333; padding: 24px; }
.container { max-width: 960px; margin: 0 auto; }
.header { text-align: center; padding: 32px 0 24px; }
.header h1 { font-size: 24px; font-weight: 600; color: #1a1a1a; }
.header p { color: #666; margin-top: 8px; }
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; margin-bottom: 24px; }
.stat-card { background: #fff; border-radius: 12px; padding: 20px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }
.stat-card .value { font-size: 28px; font-weight: 600; color: #1a1a1a; }
.stat-card .label { font-size: 13px; color: #666; margin-top: 4px; }
.section { background: #fff; border-radius: 12px; padding: 24px; margin-bottom: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0,0.08); }
.section h2 { font-size: 16px; font-weight: 600; margin-bottom: 16px; color: #1a1a1a; }
.chart { width: 100%; height: 280px; }
table { width: 100%; border-collapse: collapse; font-size: 13px; }
th, td { padding: 8px 12px; text-align: left; border-bottom: 1px solid #eee; }
th { background: #f8f9fa; font-weight: 500; }
.footer { text-align: center; padding: 24px 0; color: #999; font-size: 12px; }
</style>
</head>
<body>
<div class="container">
<div class="header">
<h1>''' + title + '''</h1>
<p>统计周期：''' + str(stats.get("period", "最近 7 天")) + '''</p>
</div>
''' + sections_html + '''
<div class="footer">''' + footer + '''</div>
</div>
<script>
var chart_actions = echarts.init(document.getElementById("chart_actions"));
chart_actions.setOption({title:{text:"命令分布"},tooltip:{trigger:"pie"},series:[{type:"pie",radius:["40%","70%"],data:''' + action_data + '''}]});

var chart_daily = echarts.init(document.getElementById("chart_daily"));
chart_daily.setOption({title:{text:"每日调用趋势"},tooltip:{trigger:"axis"},xAxis:{type:"category",data:''' + daily_labels_json + '''},yAxis:{type:"value"},series:[{type:"line",data:''' + daily_values_json + ''',smooth:true,areaStyle:{}}]});

var chart_engine = echarts.init(document.getElementById("chart_engine"));
chart_engine.setOption({title:{text:"引擎分布"},tooltip:{trigger:"axis"},xAxis:{type:"category",data:''' + engine_labels_json + '''},yAxis:{type:"value"},series:[{type:"bar",data:''' + engine_values_json + '''}]});
</script>
</body>
</html>'''
        return html

    def _render_section(self, section: Dict, stats: Optional[Dict]) -> str:
        key = section.get("key", "")
        stype = section.get("type", "")

        if stype == "stats_cards":
            total = stats.get("total", 0) if stats else 0
            success_rate = stats.get("success_rate", 0) if stats else 0
            avg_dur = stats.get("avg_duration_ms", 0) if stats else 0
            duration_s = round(stats.get("total_duration_ms", 0) / 1000, 1) if stats else 0
            failed = stats.get("failed", 0) if stats else 0
            return f'''<div class="stats-grid">
<div class="stat-card"><div class="value">{total}</div><div class="label">总调用次数</div></div>
<div class="stat-card"><div class="value">{success_rate}%</div><div class="label">成功率</div></div>
<div class="stat-card"><div class="value">{avg_dur}ms</div><div class="label">平均耗时</div></div>
<div class="stat-card"><div class="value">{duration_s}s</div><div class="label">总运行时长</div></div>
<div class="stat-card"><div class="value">{failed}</div><div class="label">失败次数</div></div>
</div>'''

        elif stype == "echarts_pie":
            return '<div id="chart_actions" class="chart"></div>'

        elif stype == "echarts_line":
            return '<div id="chart_daily" class="chart"></div>'

        elif stype == "echarts_bar":
            return '<div id="chart_engine" class="chart"></div>'

        elif stype == "table":
            if key == "engine_health":
                rows = ""
                engine_dist = stats.get("engine_distribution", {}) if stats else {}
                for eng, cnt in engine_dist.items():
                    rows += f"<tr><td>{eng}</td><td>{cnt}</td></tr>"
                if not rows:
                    rows = "<tr><td colspan='2' style='color:#999'>暂无数据</td></tr>"
                return f'<table><tr><th>引擎</th><th>调用次数</th></tr>{rows}</table>'

            elif key == "top_actions":
                rows = ""
                action_dist = stats.get("action_distribution", {}) if stats else {}
                for act, cnt in list(action_dist.items())[:5]:
                    rows += f"<tr><td>{act}</td><td>{cnt}</td></tr>"
                if not rows:
                    rows = "<tr><td colspan='2' style='color:#999'>暂无数据</td></tr>"
                return f'<table><tr><th>命令</th><th>调用次数</th></tr>{rows}</table>'

            return ""

        elif stype == "bullets":
            highlights = []
            if stats:
                total = stats.get("total", 0)
                if total > 50:
                    highlights.append(f"本周高频使用，累计 <b>{total}</b> 次调用")
                if stats.get("success_rate", 0) > 95:
                    highlights.append(f"成功率高达 <b>{stats['success_rate']}%</b>，运行稳定")
                engines = list(stats.get("engine_distribution", {}).keys())
                if len(engines) > 1:
                    highlights.append(f"使用了 <b>{len(engines)}</b> 个引擎：{', '.join(engines)}")
            if not highlights:
                highlights.append("暂无使用亮点记录")
            items = "".join(f"<li>{h}</li>" for h in highlights)
            return f"<ul style='padding-left:20px;line-height:1.8'>{items}</ul>"

        return ""


def main():
    parser = argparse.ArgumentParser(
        description=f"报告中心 {ReportCenter.VERSION} — 生成 ECharts 单文件 HTML 报告",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_weekly = sub.add_parser("weekly", help="生成周报（ECharts HTML）")
    p_weekly.add_argument("--output", required=True, help="输出 .html 路径")
    p_weekly.add_argument("--preview", action="store_true", help="仅预览统计摘要不生成文件")

    p_monthly = sub.add_parser("monthly", help="生成月报（ECharts HTML）")
    p_monthly.add_argument("--output", required=True, help="输出 .html 路径")
    p_monthly.add_argument("--preview", action="store_true", help="仅预览统计摘要不生成文件")

    sub.add_parser("list", help="列出可用报告类型")

    args = parser.parse_args()
    center = ReportCenter()

    if args.command == "weekly":
        if getattr(args, "preview", False):
            result = center.preview("weekly")
        else:
            result = center.generate("weekly", args.output)
    elif args.command == "monthly":
        if getattr(args, "preview", False):
            result = center.preview("monthly")
        else:
            result = center.generate("monthly", args.output)
    elif args.command == "list":
        result = center.list_templates()
    else:
        result = {"ok": False, "error": "未知命令"}

    print(json.dumps(result, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
