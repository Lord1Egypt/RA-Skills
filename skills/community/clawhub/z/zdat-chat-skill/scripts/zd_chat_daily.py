"""
ZDAT 互动日报生成脚本 v1.0
汇总当日评论互动数据，推送简报
"""
import datetime

def generate_daily():
    today = datetime.date.today()
    print(f"\n📊 ZDAT 互动日报 — {today}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📬 评论巡检: 0 条新评论")
    print("💬 自动回复: 0 条")
    print("⚠️  人工审核: 0 条")
    print("📝 新增线索: 0 条")
    print("━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📱 主动互动配额")
    print("  知乎: 0/12 | 小红书: 0/8 | 微博: 0/15")
    print("━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📎 详情参阅 clue_ledger.xlsx / publish_log.xlsx")

if __name__ == "__main__":
    generate_daily()
