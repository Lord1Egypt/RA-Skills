"""
ZDAT 多平台全量分发脚本 v1.0
遍历发布规则，按平台规格逐一发布
"""
import sys, os, yaml, datetime
from pathlib import Path

WORKDIR = Path(os.getenv("WORKDIR", os.path.expanduser("~/.molili/workspaces/default")))
PUBLISH_RULE = WORKDIR / "skill_config" / "zd_publish_rule.yaml"

def publish_all(article_path=None):
    with open(PUBLISH_RULE, "r", encoding="utf-8") as f:
        rules = yaml.safe_load(f)
    
    print(f"\n📤 ZDAT 全平台分发 — {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"   文章: {article_path or '默认'}\n")
    
    platforms = rules.get("platforms", {})
    for plat, config in platforms.items():
        print(f"  📱 {plat}: {config.get('word_count', '?')}字 | {config.get('style', '')}")
    
    print(f"\n   共 {len(platforms)} 个平台待分发")
    print(f"   (实际发布请使用 zd_publish_single.py 逐平台执行)")

if __name__ == "__main__":
    article = sys.argv[2] if len(sys.argv) > 2 else None
    publish_all(article)
