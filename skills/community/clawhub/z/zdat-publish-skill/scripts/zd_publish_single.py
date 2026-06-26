"""
ZDAT 单平台发布脚本 v1.0
调用 zdat-mpg-multi-publish 引擎进行单平台发布
"""
import sys, os, subprocess, yaml
from pathlib import Path

WORKDIR = Path(os.getenv("WORKDIR", os.path.expanduser("~/.molili/workspaces/default")))
PUBLISH_ENGINE = WORKDIR / "active_skills" / "zdat-mpg-multi-publish"
PUBLISH_RULE = WORKDIR / "skill_config" / "zd_publish_rule.yaml"

def get_platform_config(platform):
    with open(PUBLISH_RULE, "r", encoding="utf-8") as f:
        rules = yaml.safe_load(f)
    platform_map = {
        "toutiao": "weibo",           # 头条号没有独立配置，复用通用
        "weixin": "wechat_public",
        "zhihu": "zhihu",
        "xiaohongshu": "xiaohongshu",
        "weibo": "weibo",
    }
    key = platform_map.get(platform, platform)
    return rules.get("platforms", {}).get(key, {})

def publish(platform, title, content):
    """调用发布引擎"""
    print(f"\n📤 ZDAT 发布 — 平台: {platform}")
    config = get_platform_config(platform)
    print(f"   规格: {config.get('word_count', '默认')}字")
    print(f"   标签: {config.get('tags', [])}")
    print(f"   标题: {title[:40]}..." if len(title) > 40 else f"   标题: {title}")
    
    # 调用 v5 发布引擎
    script = str(WORKDIR / "zd_auto_publish_v5.py")
    if os.path.exists(script):
        result = subprocess.run(
            ["python", script, "--platform", platform, "--title", title, "--content", content],
            capture_output=True, text=True, timeout=120
        )
        print(f"   结果: {'✅ 成功' if result.returncode == 0 else '❌ 失败'}")
        if result.returncode != 0:
            print(f"   错误: {result.stderr[:200]}")
    else:
        print(f"   ⚠️ 发布引擎未找到: {script}")
        print(f"   请先确认 zdat-mpg-multi-publish 已就绪")

if __name__ == "__main__":
    platform = sys.argv[2] if len(sys.argv) > 2 else "zhihu"
    title = sys.argv[4] if len(sys.argv) > 4 else "默认标题"
    content = sys.argv[6] if len(sys.argv) > 6 else "默认正文"
    publish(platform, title, content)
