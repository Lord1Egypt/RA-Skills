"""
Token决策 v2.0 — 使用统计面板（含累计节省）
用法: python stats.py
"""
import sqlite3
import os
from collections import Counter
from datetime import datetime, date, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), "benchmark.db")


def show_stats():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS usage_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        prompt TEXT, task_type TEXT, task_confidence INTEGER DEFAULT 0,
        recommended_model TEXT, mode TEXT, quality REAL, cost REAL, logged_at TEXT
    )""")
    cur.execute("PRAGMA table_info(usage_log)")
    cols = [r[1] for r in cur.fetchall()]
    if "task_confidence" not in cols:
        try:
            cur.execute("ALTER TABLE usage_log ADD COLUMN task_confidence INTEGER DEFAULT 0")
        except:
            pass

    cur.execute("SELECT COUNT(*), COUNT(DISTINCT date(logged_at)) FROM usage_log")
    total, days = cur.fetchone()
    if total == 0:
        print("\n尚无使用数据。每次用 /token决策 都会自动记录。")
        conn.close()
        return

    today = date.today().isoformat()
    week_start = (date.today() - timedelta(days=date.today().weekday())).isoformat()

    cur.execute("SELECT COUNT(*), COALESCE(SUM(cost),0) FROM usage_log WHERE logged_at LIKE ?", (f"{today}%",))
    today_count, today_cost = cur.fetchone()

    cur.execute("SELECT COUNT(*), COALESCE(SUM(cost),0) FROM usage_log WHERE logged_at >= ?", (week_start,))
    week_count, week_cost = cur.fetchone()

    cur.execute("SELECT COUNT(*), COALESCE(SUM(cost),0) FROM usage_log")
    total_count, total_cost = cur.fetchone()

    print()
    print("=" * 50)
    print("  Token决策 v2.0 — 使用统计")
    print("=" * 50)
    print(f"  {'':<16} {'调用次数':>8} {'消耗¥':>12}")
    print(f"  {'今日':<16} {today_count:>8} {today_cost or 0:>12.6f}")
    print(f"  {'本周':<16} {week_count:>8} {week_cost or 0:>12.6f}")
    print(f"  {'累计 (全渠道)':<16} {total_count:>8} {total_cost or 0:>12.6f}")
    print(f"  📅 活跃天数: {days} 天")
    print()

    # 模式分布
    cur.execute("SELECT mode, COUNT(*), COALESCE(SUM(cost),0) FROM usage_log GROUP BY mode ORDER BY COUNT(*) DESC")
    print(f"  📋 模式分布:")
    for r in cur.fetchall():
        bar = "█" * min(r[1], 30)
        print(f"     {r[0]:<10} {r[1]:>4}次 ¥{r[2]:.6f} {bar}")

    # 推荐模型排行
    cur.execute("SELECT recommended_model, COUNT(*), COALESCE(SUM(cost),0) FROM usage_log GROUP BY recommended_model ORDER BY COUNT(*) DESC")
    print(f"\n  🎯 推荐模型排行:")
    for r in cur.fetchall():
        print(f"     {r[0]:<22} {r[1]:>4}次 ¥{r[2]:.6f}")

    # 任务类型分布
    cur.execute("SELECT task_type, COUNT(*), COALESCE(SUM(cost),0) FROM usage_log GROUP BY task_type ORDER BY COUNT(*) DESC")
    print(f"\n  🏷️  任务类型分布:")
    for r in cur.fetchall():
        print(f"     {r[0]:<8} {r[1]:>4}次 ¥{r[2]:.6f}")

    # 累计节省：你的推荐 vs 全局平均成本对比
    cur.execute("SELECT AVG(cost) FROM usage_log")
    avg_cost = cur.fetchone()[0] or 0
    cur.execute("SELECT AVG(total_cost) FROM runs WHERE total_cost > 0")
    avg_db_cost = cur.fetchone()[0] or 0
    if avg_db_cost > avg_cost and avg_cost > 0:
        est_savings = (avg_db_cost - avg_cost) * total_count
        print(f"\n  💰 累计节省（估算）: ¥{est_savings:.4f}")
        print(f"     (你的推荐 vs 全局平均成本 × {total_count}次调用)")

    # 最近 10 条
    cur.execute("""SELECT logged_at, task_type, task_confidence, recommended_model, mode, ROUND(quality,1), ROUND(cost,6)
        FROM usage_log ORDER BY id DESC LIMIT 10""")
    print(f"\n  🕐 最近调用:")
    for r in cur.fetchall():
        time_str = r[0][11:19] if 'T' in r[0] else r[0][:19][-8:]
        conf_tag = f"[信{r[2]}]" if r[2] is not None else ""
        print(f"     {time_str}  {r[1]:<8} {conf_tag} → {r[3]:<20} [{r[4]}] {r[5]:.1f}分 ¥{r[6]:.6f}")

    # 全量调用
    try:
        import urllib.request, json
        resp = urllib.request.urlopen("https://api.countapi.xyz/get/token-decision/total-calls", timeout=5)
        data = json.loads(resp.read())
        global_calls = data.get("value", 0)
        print(f"\n  🌍 全量调用: {global_calls} 次（所有用户累计）")
    except:
        pass

    # 分类置信度统计
    cur.execute("""
        SELECT task_confidence, COUNT(*) FROM usage_log
        WHERE task_confidence IS NOT NULL
        GROUP BY task_confidence ORDER BY task_confidence
    """)
    conf_rows = cur.fetchall()
    if conf_rows:
        print(f"\n  🔍 分类置信度分布:")
        for conf, cnt in conf_rows:
            label = {0: "未知(已fallback)", 1: "低", 2: "中", 3: "高"}.get(conf, "超高")
            bar = "█" * cnt
            print(f"     {label:<16} {cnt:>4} {bar}")

    print()
    conn.close()


if __name__ == "__main__":
    show_stats()
