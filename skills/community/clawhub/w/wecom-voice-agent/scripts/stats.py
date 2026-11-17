#!/usr/bin/env python3
"""
企业微信语音助手 — 通话记录看板 v2.0

功能：
1. 统计本月通话数据：总次数、总时长、平均时长、外呼/来电比例
2. 分析意图分布：哪些意图最常用
3. 统计接听率 / 挂断原因分布
4. 绘制每日趋势图（ASCII 字符画）

特性：
- 纯 Python 标准库 + rich（可选，无 rich 时降级为纯文本）
- 支持 --period week/month/year 时间范围
- 支持 --userid 按用户筛选
- 支持 --export 导出 JSON

更新日志：
| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v2.0 | 2026-07-15 | 初始发布：统计看板、ASCII 趋势图、JSON 导出 |
| v2.0.1 | 2026-07-15 | 中文化日志、安全性增强、错误提示优化 |

联系信息：njskills@agent.qq.com

使用方法：
    python scripts/stats.py                        # 本月看板
    python scripts/stats.py --period month         # 本月（默认）
    python scripts/stats.py --period week           # 本周
    python scripts/stats.py --period year           # 本年度
    python scripts/stats.py --userid zhangsan       # 按用户筛选
    python scripts/stats.py --export stats.json     # 导出 JSON
"""

import json
import logging
import os
import sys
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# ==========================================
# 配置
# ==========================================

DB_PATH = os.path.join(os.path.expanduser("~"), ".wecom_voice", "call_records.db")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("Stats")

# 尝试导入 rich（可选）
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    logger.info("rich 库未安装，使用纯文本输出。安装命令: pip install rich")


# ==========================================
# 统计生成器
# ==========================================

class StatsGenerator:
    """
    通话统计生成器

    使用方式：
        gen = StatsGenerator()
        stats = gen.generate(period="month")
        print(gen.render(stats))
    """

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def generate(self, period: str = "month", userid: str = None) -> Dict:
        """
        生成统计数据

        Args:
            period: week / month / year
            userid: 按用户筛选（None 表示全部）

        Returns:
            统计数据 dict
        """
        start_date, end_date = self._get_date_range(period)

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row

            # 基础过滤条件
            where_clause = "WHERE start_time >= ? AND start_time <= ?"
            params = [start_date, end_date]
            if userid:
                where_clause += " AND (caller = ? OR callee = ?)"
                params.extend([userid, userid])

            # 总次数
            row = conn.execute(
                f"SELECT COUNT(*) FROM call_records {where_clause}", params
            ).fetchone()
            total_calls = row[0]

            if total_calls == 0:
                return {
                    "period": period,
                    "date_range": f"{start_date} ~ {end_date}",
                    "total_calls": 0,
                    "message": "该时间段内暂无通话记录",
                }

            # 总时长
            row = conn.execute(
                f"SELECT COALESCE(SUM(duration_seconds), 0) FROM call_records {where_clause}", params
            ).fetchone()
            total_duration = row[0]

            # 平均时长
            avg_duration = total_duration / total_calls

            # 外呼/来电比例
            rows = conn.execute(
                f"SELECT direction, COUNT(*) as cnt FROM call_records {where_clause} GROUP BY direction", params
            ).fetchall()
            direction_counts = {r["direction"]: r["cnt"] for r in rows}
            outbound = direction_counts.get("outbound", 0)
            inbound = direction_counts.get("inbound", 0)

            # 意图分布
            rows = conn.execute(
                f"SELECT intent, COUNT(*) as cnt FROM call_records {where_clause} GROUP BY intent ORDER BY cnt DESC", params
            ).fetchall()
            intent_counts = {r["intent"]: r["cnt"] for r in rows}

            # 挂断原因分布
            rows = conn.execute(
                f"SELECT hangup_reason, COUNT(*) as cnt FROM call_records {where_clause} GROUP BY hangup_reason", params
            ).fetchall()
            hangup_reasons = {r["hangup_reason"]: r["cnt"] for r in rows}

            # 每日趋势（按日期分组）
            rows = conn.execute(
                f"""
                SELECT DATE(start_time) as day, COUNT(*) as cnt,
                       SUM(duration_seconds) as total_dur
                FROM call_records {where_clause}
                GROUP BY day ORDER BY day
                """, params
            ).fetchall()
            daily_trend = [{"date": r["day"], "calls": r["cnt"], "duration": r["total_dur"]} for r in rows]

            # 最长通话
            row = conn.execute(
                f"SELECT call_id, duration_seconds FROM call_records {where_clause} ORDER BY duration_seconds DESC LIMIT 1", params
            ).fetchone()
            longest_call = {"call_id": row["call_id"], "duration": row["duration_seconds"]} if row else None

            # 录音比例
            row = conn.execute(
                f"SELECT COUNT(*) FROM call_records {where_clause} AND has_recording = 1", params
            ).fetchone()
            recorded_calls = row[0]
            recording_rate = recorded_calls / total_calls if total_calls > 0 else 0

            # 接听率（简化：正常挂断视为已接听）
            normal_hangup = hangup_reasons.get("normal", 0)
            answered_rate = normal_hangup / total_calls if total_calls > 0 else 0

        return {
            "period": period,
            "date_range": f"{start_date} ~ {end_date}",
            "total_calls": total_calls,
            "total_duration": total_duration,
            "avg_duration": avg_duration,
            "total_hours": total_duration / 3600,
            "outbound": outbound,
            "inbound": inbound,
            "outbound_ratio": outbound / total_calls if total_calls > 0 else 0,
            "intent_counts": intent_counts,
            "hangup_reasons": hangup_reasons,
            "daily_trend": daily_trend,
            "longest_call": longest_call,
            "recorded_calls": recorded_calls,
            "recording_rate": recording_rate,
            "answered_rate": answered_rate,
        }

    def render(self, stats: Dict) -> str:
        """渲染统计为可读字符串"""
        if stats["total_calls"] == 0:
            return f"\n📊 {stats['date_range']}: 暂无通话记录\n"

        if HAS_RICH:
            return self._render_rich(stats)
        else:
            return self._render_plain(stats)

    def _render_rich(self, stats: Dict) -> str:
        """使用 rich 渲染表格"""
        console = Console(record=True)

        # 主统计表格
        main_table = Table(title="📊 通话统计看板", show_header=True)
        main_table.add_column("指标", style="bold cyan", width=20)
        main_table.add_column("数值", style="bold green")

        main_table.add_row("时间范围", stats["date_range"])
        main_table.add_row("总通话次数", f"{stats['total_calls']} 次")
        main_table.add_row("总通话时长", f"{stats['total_hours']:.1f} 小时 ({stats['total_duration']:.0f} 秒)")
        main_table.add_row("平均通话时长", f"{stats['avg_duration']:.1f} 秒")
        main_table.add_row("外呼次数", f"{stats['outbound']} 次 ({stats['outbound_ratio']*100:.0f}%)")
        main_table.add_row("来电次数", f"{stats['inbound']} 次 ({(1-stats['outbound_ratio'])*100:.0f}%)")
        main_table.add_row("已接听率", f"{stats['answered_rate']*100:.1f}%")
        main_table.add_row("录音覆盖率", f"{stats['recording_rate']*100:.1f}%")

        if stats["longest_call"]:
            main_table.add_row("最长通话", f"{stats['longest_call']['call_id']} ({stats['longest_call']['duration']:.0f}秒)")

        console.print(main_table)

        # 意图分布表
        intent_table = Table(title="🎯 意图分布", show_header=True)
        intent_table.add_column("意图", style="bold")
        intent_table.add_column("次数", style="bold")
        intent_table.add_column("占比", style="bold")
        for intent, count in stats["intent_counts"].items():
            pct = count / stats["total_calls"] * 100
            intent_table.add_row(intent, str(count), f"{pct:.1f}%")
        console.print(intent_table)

        # 挂断原因表
        hangup_table = Table(title="📴 挂断原因分布", show_header=True)
        hangup_table.add_column("原因", style="bold")
        hangup_table.add_column("次数", style="bold")
        hangup_table.add_column("占比", style="bold")
        for reason, count in stats["hangup_reasons"].items():
            pct = count / stats["total_calls"] * 100
            hangup_table.add_row(reason, str(count), f"{pct:.1f}%")
        console.print(hangup_table)

        # 每日趋势 ASCII 图
        if stats["daily_trend"]:
            trend_text = self._render_trend_ascii(stats["daily_trend"])
            console.print(Panel(trend_text, title="📈 每日趋势", expand=False))

        return console.export_text()

    def _render_plain(self, stats: Dict) -> str:
        """纯文本渲染"""
        lines = [
            "",
            "=" * 60,
            "📊 通话统计看板",
            "=" * 60,
            f"时间范围: {stats['date_range']}",
            f"总通话次数: {stats['total_calls']} 次",
            f"总通话时长: {stats['total_hours']:.1f} 小时 ({stats['total_duration']:.0f} 秒)",
            f"平均通话时长: {stats['avg_duration']:.1f} 秒",
            f"外呼次数: {stats['outbound']} 次 ({stats['outbound_ratio']*100:.0f}%)",
            f"来电次数: {stats['inbound']} 次 ({(1-stats['outbound_ratio'])*100:.0f}%)",
            f"已接听率: {stats['answered_rate']*100:.1f}%",
            f"录音覆盖率: {stats['recording_rate']*100:.1f}%",
            "",
        ]

        if stats["longest_call"]:
            lines.append(f"最长通话: {stats['longest_call']['call_id']} ({stats['longest_call']['duration']:.0f}秒)")
            lines.append("")

        lines.append("🎯 意图分布:")
        for intent, count in stats["intent_counts"].items():
            pct = count / stats["total_calls"] * 100
            lines.append(f"  {intent}: {count} 次 ({pct:.1f}%)")
        lines.append("")

        lines.append("📴 挂断原因:")
        for reason, count in stats["hangup_reasons"].items():
            pct = count / stats["total_calls"] * 100
            lines.append(f"  {reason}: {count} 次 ({pct:.1f}%)")
        lines.append("")

        if stats["daily_trend"]:
            lines.append("📈 每日趋势:")
            lines.append(self._render_trend_ascii(stats["daily_trend"]))

        lines.append("=" * 60)
        return "\n".join(lines)

    def _render_trend_ascii(self, daily_trend: List[Dict]) -> str:
        """渲染 ASCII 趋势图"""
        if not daily_trend:
            return "(无数据)"

        max_calls = max(d["calls"] for d in daily_trend) if daily_trend else 1
        if max_calls == 0:
            max_calls = 1

        lines = []
        lines.append(f"  最大: {max_calls} 次/天")
        lines.append("")

        for day in daily_trend:
            bar_len = int((day["calls"] / max_calls) * 20)
            bar = "█" * bar_len + "░" * (20 - bar_len)
            lines.append(f"  {day['date']} │{bar}│ {day['calls']}次 ({day['duration']:.0f}s)")

        return "\n".join(lines)

    def _get_date_range(self, period: str) -> tuple:
        """获取日期范围"""
        now = datetime.now()
        end_date = now.strftime("%Y-%m-%d %H:%M:%S")

        if period == "week":
            start = now - timedelta(days=7)
        elif period == "year":
            start = now.replace(month=1, day=1, hour=0, minute=0, second=0)
        elif period == "month":
            start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            raise ValueError(f"不支持的时间范围: {period}（支持: week/month/year）")

        start_date = start.strftime("%Y-%m-%d %H:%M:%S")
        return start_date, end_date

    def export_json(self, stats: Dict, filepath: str) -> bool:
        """导出统计为 JSON"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(stats, f, ensure_ascii=False, indent=2)
            logger.info(f"已导出: {filepath}")
            return True
        except Exception as e:
            logger.error(f"导出失败: {e}")
            return False


# ==========================================
# 命令行入口
# ==========================================

def main():
    import argparse

    parser = argparse.ArgumentParser(description="通话记录看板")
    parser.add_argument("--period", choices=["week", "month", "year"], default="month",
                        help="时间范围（默认 month）")
    parser.add_argument("--userid", type=str, default=None, help="按用户ID筛选")
    parser.add_argument("--export", type=str, default=None, help="导出 JSON 文件路径")
    parser.add_argument("--no-rich", action="store_true", help="禁用 rich 输出")

    args = parser.parse_args()

    # 禁用 rich
    global HAS_RICH
    if args.no_rich:
        HAS_RICH = False

    gen = StatsGenerator()
    stats = gen.generate(period=args.period, userid=args.userid)
    output = gen.render(stats)
    print(output)

    if args.export:
        gen.export_json(stats, args.export)


# ==========================================
# 自测
# ==========================================

def run_self_test():
    """运行看板自测"""
    print("=" * 60)
    print("通话记录看板 — 自测模式")
    print("=" * 60)

    # 使用模拟数据（先创建临时数据库）
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        temp_db = f.name

    conn = None
    try:
        # 插入模拟数据
        conn = sqlite3.connect(temp_db)
        conn.execute("""
            CREATE TABLE call_records (
                call_id TEXT PRIMARY KEY,
                caller TEXT, callee TEXT, direction TEXT,
                start_time TEXT, duration_seconds REAL,
                intent TEXT, hangup_reason TEXT,
                has_recording INTEGER DEFAULT 0
            )
        """)

        now = datetime.now()
        for i in range(15):
            day = (now - timedelta(days=i % 7)).strftime("%Y-%m-%d")
            direction = "outbound" if i % 3 != 0 else "inbound"
            intent = ["query_weather", "schedule", "customer_service", "appointment"][i % 4]
            reason = "normal" if i % 5 != 0 else "timeout"
            conn.execute(
                "INSERT INTO call_records VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (f"call_{i}", f"1380000000{i}", f"1390000000{i}", direction,
                 f"{day} 10:00:00", 60 + i * 10, intent, reason, 1 if i % 2 == 0 else 0)
            )
        conn.commit()
        conn.close()

        # 生成统计
        gen = StatsGenerator(db_path=temp_db)
        stats = gen.generate(period="month")

        assert stats["total_calls"] == 15
        assert stats["outbound"] > 0
        assert stats["inbound"] > 0
        assert len(stats["intent_counts"]) > 0
        assert len(stats["daily_trend"]) > 0

        print(f"  总通话: {stats['total_calls']} 次")
        print(f"  外呼: {stats['outbound']} / 来电: {stats['inbound']}")
        print(f"  意图: {stats['intent_counts']}")
        print(f"  每日趋势: {len(stats['daily_trend'])} 天")
        print("✅ 统计生成通过")

        # 渲染输出
        output = gen.render(stats)
        assert len(output) > 100
        print("✅ 渲染输出通过")

        # 导出
        export_path = temp_db.replace(".db", "_export.json")
        gen.export_json(stats, export_path)
        assert os.path.exists(export_path)
        os.remove(export_path)
        print("✅ JSON 导出通过")

    finally:
        try:
            conn.close()
        except Exception:
            pass
        import time as _time
        for _ in range(3):
            try:
                os.unlink(temp_db)
                break
            except PermissionError:
                _time.sleep(0.1)

    print(f"\n{'='*60}")
    print("所有自测通过 ✓")
    print('='*60)


if __name__ == "__main__":
    run_self_test()
