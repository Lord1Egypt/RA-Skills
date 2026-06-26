"""
ZDAT 评论巡检与回复脚本 v1.0
按平台巡检新评论，匹配话术库自动回复
"""
import sys, os, yaml, datetime
from pathlib import Path

WORKDIR = Path(os.getenv("WORKDIR", os.path.expanduser("~/.molili/workspaces/default")))
REPLY_CONFIG = WORKDIR / "skill_config" / "zd_reply_words.yaml"
KEYWORD_CONFIG = WORKDIR / "skill_config" / "zd_keyword.yaml"

def load_replies():
    with open(REPLY_CONFIG, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def match_scene(comment_text, keywords):
    """匹配场景"""
    kw = keywords.get("risk_keywords", [])
    for rk in kw:
        if rk in comment_text:
            return "negative_controversial"
    
    intent_kw = keywords.get("intent_keywords", [])
    for ik in intent_kw:
        if ik in comment_text:
            return "high_intent"
    
    basic_kw = ["什么是零缺陷", "什么是PONC", "零缺陷是什么", "PONC是什么"]
    for bk in basic_kw:
        if bk in comment_text:
            return "basic_question"
    
    return "praise_thank"

def reply_to_comments(platform="all"):
    with open(KEYWORD_CONFIG, "r", encoding="utf-8") as f:
        keywords = yaml.safe_load(f)
    
    replies = load_replies()
    
    print(f"\n💬 ZDAT 评论巡检 — {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"   平台: {platform}\n")
    
    # TODO: 实际接入各平台评论API
    # 模拟流程
    sample_comments = [
        ("感谢分享，讲得很好", "praise_thank"),
        ("什么是零缺陷？", "basic_question"),
        ("我们工厂想导入零缺陷，有课件吗", "high_intent"),
    ]
    
    for text, scene in sample_comments:
        scene_config = replies.get("scenes", {}).get(scene, {})
        action = scene_config.get("action", "reply")
        
        if action == "skip_auto_reply":
            print(f"  ⚠️ 跳过自动回复（人工审核）: {text[:30]}")
        else:
            reply_list = scene_config.get("replies", ["感谢留言～"])
            reply = reply_list[0]
            print(f"  ✅ [{scene}] {text[:30]}...")
            print(f"     ↳ {reply[:50]}...")
        
        if scene == "high_intent":
            print(f"     📝 写入线索台账 【高意向客户】")

if __name__ == "__main__":
    platform = sys.argv[2] if len(sys.argv) > 2 else "all"
    reply_to_comments(platform)
