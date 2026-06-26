"""
ZDAT 负面预警检查脚本 v1.0
统计负面关键词出现次数，触发预警推送
"""
import json, sys, os, yaml, datetime
from pathlib import Path

WORKDIR = Path(os.getenv("WORKDIR", os.path.expanduser("~/.molili/workspaces/default")))
CONFIG_PATH = WORKDIR / "skill_config" / "zd_keyword.yaml"
SCHEDULE_PATH = WORKDIR / "skill_config" / "zd_crawl_schedule.yaml"

def check_alerts():
    with open(SCHEDULE_PATH, "r", encoding="utf-8") as f:
        sched = yaml.safe_load(f)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        kw = yaml.safe_load(f)
    
    threshold = sched.get("alert", {}).get("negative_threshold", {}).get("count", 15)
    risk_kw = kw.get("risk_keywords", [])
    
    print(f"\n🔴 ZDAT 负面预警检查 — {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"   阈值: 单日≥{threshold}条\n")
    
    for rkw in risk_kw:
        count = 0  # TODO: 实际统计当日出现次数
        if count >= threshold:
            print(f"  ⚠️ 触发预警: [{rkw}] 出现 {count} 次")
        else:
            print(f"  ✅ [{rkw}] {count} 次（正常）")

if __name__ == "__main__":
    check_alerts()
