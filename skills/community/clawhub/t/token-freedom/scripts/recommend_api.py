"""
AI API 平台推荐工具
用法: python recommend_api.py "<需求描述>"
      python recommend_api.py --model <模型名>
      python recommend_api.py --free (只看免费)
      python recommend_api.py --list (全部平台)
"""
import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
DB_PATH = SKILL_DIR / "references" / "platforms.json"
DEFAULT_CONFIG = SKILL_DIR / "references" / "default_config.json"
USER_CONFIG = Path.home() / ".qclaw" / "affiliate-config.json"


def load_affiliate_config():
    """加载联盟配置"""
    config = {}
    if DEFAULT_CONFIG.exists():
        with open(DEFAULT_CONFIG, "r", encoding="utf-8") as f:
            config.update(json.load(f))
    if USER_CONFIG.exists():
        with open(USER_CONFIG, "r", encoding="utf-8") as f:
            config.update(json.load(f))
    return config


def resolve_link(link, config):
    """替换链接中的 {AFF_CODE} 占位符"""
    for key, value in config.items():
        if value:
            link = link.replace(f"{{{key}}}", value)
            link = link.replace(f"{{{key.upper()}}}", value)
    return link


def load_platforms():
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)["platforms"]


def search_platforms(platforms, query):
    """搜索包含关键词的平台"""
    q = query.lower()
    results = []
    for p in platforms:
        score = 0
        # 名称匹配
        if q in p["name"].lower():
            score += 10
        # 描述匹配
        for h in p.get("highlights", []):
            if q in h.lower():
                score += 5
        # 适用场景匹配
        for b in p.get("best_for", []):
            if q in b.lower():
                score += 8
        # 模型名匹配
        for model in p.get("pricing", {}):
            if q in model.lower():
                score += 15
        # 免费模型匹配
        for fm in p.get("free_models", []):
            if q in fm.lower():
                score += 12
        if score > 0:
            results.append((score, p))
    results.sort(key=lambda x: x[0], reverse=True)
    return [r[1] for r in results]


def recommend_by_model(platforms, model_name):
    """按模型名推荐最佳平台"""
    q = model_name.lower()
    candidates = []
    for p in platforms:
        for model, price in p.get("pricing", {}).items():
            if q in model.lower():
                candidates.append((p, model, price))
        for fm in p.get("free_models", []):
            if q in fm.lower():
                candidates.append((p, fm, "免费"))
    return candidates


def get_free_platforms(platforms):
    """列出有免费模型或免费额度的平台"""
    results = []
    for p in platforms:
        has_free = len(p.get("free_models", [])) > 0 or p.get("free_new_user")
        if has_free:
            results.append(p)
    return results


def format_platform(p, index=None, show_pricing=False):
    """格式化输出一个平台"""
    prefix = f"{index}. " if index else ""
    lines = [f"{prefix}🏢 {p['name']}"]
    lines.append(f"   🔗 {p['url']}")

    if p.get("has_referral") and p.get("referral_reward"):
        lines.append(f"   🎁 推荐奖励: {p['referral_reward']}")
    if p.get("free_new_user"):
        lines.append(f"   🆓 新用户: {p['free_new_user']}")

    if show_pricing:
        lines.append("   💰 定价:")
        for model, price in p.get("pricing", {}).items():
            lines.append(f"      {model}: {price}")

    if p.get("free_models"):
        lines.append(f"   🆓 免费模型: {', '.join(p['free_models'])}")

    lines.append(f"   ✨ {' · '.join(p.get('highlights', []))}")
    lines.append(f"   🎯 适合: {' / '.join(p.get('best_for', []))}")
    lines.append("")
    return "\n".join(lines)


def main():
    platforms = load_platforms()
    config = load_affiliate_config()

    if len(sys.argv) < 2:
        print("用法: python recommend_api.py <需求关键词>")
        print("      python recommend_api.py --model <模型名>")
        print("      python recommend_api.py --free")
        print("      python recommend_api.py --list")
        print("\n示例:")
        print("  python recommend_api.py 免费")
        print("  python recommend_api.py --model deepseek")
        print("  python recommend_api.py 国内高速")
        return

    arg = sys.argv[1]

    if arg == "--list":
        for i, p in enumerate(platforms, 1):
            print(format_platform(p, i, show_pricing=True))
        return

    if arg == "--free":
        results = get_free_platforms(platforms)
        print(f"🎉 有免费额度/模型的平台（共{len(results)}个）:\n")
        for i, p in enumerate(results, 1):
            print(format_platform(p, i))

        print("💡 推荐: 硅基流动 + 智谱GLM-4.7-Flash 组合，一个高质量一个免费调用")
        return

    if arg == "--model":
        if len(sys.argv) < 3:
            print("请指定模型名，如: python recommend_api.py --model deepseek")
            return
        model = sys.argv[2]
        results = recommend_by_model(platforms, model)

        if not results:
            print(f"未找到支持 '{model}' 的平台。试试其他关键词？")
            return

        print(f"🔍 支持 '{model}' 的平台:\n")
        seen = set()
        for i, (p, model_name, price) in enumerate(results, 1):
            if p["name"] not in seen:
                seen.add(p["name"])
                print(format_platform(p))
            print(f"   📌 匹配模型: {model_name} → {price}\n")

        # 推荐最佳
        best = None
        for p, _, _ in results:
            if p.get("has_referral") and p.get("referral_unlimited"):
                best = p
                break
        if best:
            print(f"🏆 最佳推荐: {best['name']}")
            print(f"   理由: 有推荐返利 + {best['referral_reward']}")
            if best.get("referral_url"):
                resolved = resolve_link(best['referral_url'], config)
                print(f"   注册链接: {resolved}")
        return

    # 关键词搜索
    query = " ".join(sys.argv[1:])
    results = search_platforms(platforms, query)

    if not results:
        print(f"未找到与 '{query}' 匹配的平台。")
        print("试试: 免费、deepseek、国内、海外、qwen、glm")
        return

    print(f"🔍 与 '{query}' 相关的平台（共{len(results)}个）:\n")
    for i, p in enumerate(results[:5], 1):
        print(format_platform(p, i))


if __name__ == "__main__":
    main()
