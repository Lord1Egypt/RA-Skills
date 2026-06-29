#!/usr/bin/env python3
"""
x-skill-updater upgrade.py — 执行 skill 升级
用法: python3 upgrade.py <slug>
      python3 upgrade.py --all   # 升级所有可升级的（仅 skillhub + clawhub 自动升级）

安全：
- slug 必须通过安全验证（仅允许字母、数字、连字符、下划线）
- shell=False，使用列表传参
- custom 来源不自动升级（需手动处理）
"""
import subprocess, sys, json, re
from pathlib import Path

# 相对于本脚本所在位置定位 OpenClaw 根目录
SKILL_DIR     = Path(__file__).parent.parent
OPENCLAW_HOME = SKILL_DIR.parent.parent

SOURCES_FILE = SKILL_DIR / "data" / "skill-sources.json"

SLUG_PATTERN = re.compile(r'^[a-zA-Z0-9][-a-zA-Z0-9_]*$')

# ============ 工具 ============

def validate_slug(slug: str) -> bool:
    return bool(SLUG_PATTERN.match(slug))


def load_sources():
    if SOURCES_FILE.exists():
        return json.loads(SOURCES_FILE.read_text())
    return {}


def skill_dir(slug):
    """返回 skill 在本地的实际路径"""
    return OPENCLAW_HOME / "skills" / slug


# ============ 升级来源分发 ============

def upgrade_skillhub(slug):
    """通过 skillhub CLI 升级 skillhub 来源的 skill"""
    dest = skill_dir(slug)
    print(f"[skillhub] 升级 {slug} → {dest}")
    try:
        result = subprocess.run(
            ["skillhub", "install", slug],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            print(f"  ✅ 升级成功\n{result.stdout}")
        else:
            print(f"  ❌ 升级失败\n{result.stderr}")
    except FileNotFoundError:
        print("  ❌ skillhub CLI 未找到，请先安装：npm install -g skillhub")
    except subprocess.TimeoutExpired:
        print("  ❌ 升级超时（120s）")
    except Exception as e:
        print(f"  ❌ 升级异常: {e}")


def upgrade_clawhub(slug):
    """通过 clawhub CLI 升级 clawhub 来源的 skill"""
    print(f"[clawhub] 升级 {slug}")
    try:
        result = subprocess.run(
            ["clawhub", "install", slug],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            print(f"  ✅ 升级成功\n{result.stdout}")
        else:
            print(f"  ❌ 升级失败\n{result.stderr}")
    except FileNotFoundError:
        print("  ❌ clawhub CLI 未找到，请先安装：npm install -g clawhub")
    except subprocess.TimeoutExpired:
        print("  ❌ 升级超时（120s）")
    except Exception as e:
        print(f"  ❌ 升级异常: {e}")


def upgrade_custom(slug, entry):
    """custom 来源不自动升级，提示手动处理"""
    note = entry.get("note", "")
    print(f"[custom] {slug} 跳过自动升级（{note}）")
    print(f"  请手动处理：https://clawhub.ai/skills/{slug}")


# ============ 主逻辑 ============

def main():
    args = sys.argv[1:]
    if not args:
        print("用法: python3 upgrade.py <slug>")
        print("      python3 upgrade.py --all")
        sys.exit(1)

    sources = load_sources()

    safe_slugs = []
    for arg in args:
        if arg == "--all":
            safe_slugs.append(arg)
        elif validate_slug(arg):
            safe_slugs.append(arg)
        else:
            print(f"[安全警告] 忽略不安全的 slug: {arg}")

    if not safe_slugs:
        print("[错误] 没有有效的 slug")
        sys.exit(1)

    # --all 模式：遍历 skill-sources.json，升级所有可升级的
    if "--all" in safe_slugs:
        if not sources:
            print("[错误] skill-sources.json 为空或不存在，请先运行 check.py")
            sys.exit(1)

        skillhub_count = 0
        clawhub_count  = 0
        skipped = []

        for slug, entry in sources.items():
            src = entry.get("source", "unknown")
            if src == "skillhub":
                upgrade_skillhub(slug)
                skillhub_count += 1
            elif src == "clawhub":
                upgrade_clawhub(slug)
                clawhub_count += 1
            else:
                skipped.append((slug, src))

        print(f"\n✅ --all 完成：skillhub {skillhub_count} 个，clawhub {clawhub_count} 个")
        if skipped:
            print(f"⏭️ 跳过（custom/unknown）：{', '.join(s for s, _ in skipped)}")

    else:
        # 单个升级
        for slug in safe_slugs:
            entry = sources.get(slug, {})
            src   = entry.get("source", "unknown")

            if src == "skillhub":
                upgrade_skillhub(slug)
            elif src == "clawhub":
                upgrade_clawhub(slug)
            elif src == "custom":
                upgrade_custom(slug, entry)
            else:
                print(f"[{slug}] 来源未知（{src}），请先在 skill-sources.json 中补充来源")


if __name__ == "__main__":
    main()
