"""Template catalog loader for official PSD templates."""

import json
from pathlib import Path

from console_utils import configure_stdio

configure_stdio()

SKILL_ROOT = Path(__file__).parent.parent
TEMPLATES_DIR = SKILL_ROOT / "templates"
TEMPLATES_JSON = SKILL_ROOT / "references" / "templates.json"


def load_templates() -> dict:
    """Load template metadata from references/templates.json."""
    if not TEMPLATES_JSON.exists():
        return {}
    return json.loads(TEMPLATES_JSON.read_text(encoding="utf-8"))


TEMPLATES = load_templates()


def get_template(slug: str) -> dict:
    """获取模板信息"""
    return TEMPLATES.get(slug)

def get_psd_path(slug: str) -> Path:
    """获取 PSD 文件绝对路径"""
    t = TEMPLATES.get(slug)
    if not t:
        return None
    return SKILL_ROOT / t["psd"]

def list_templates():
    """列出所有模板"""
    for slug, t in TEMPLATES.items():
        print(f"  [{slug:<10}] {t['name']}  {t['size']}  → {t['scene']}")

def show_info(slug: str):
    """显示模板详细信息"""
    t = TEMPLATES.get(slug)
    if not t:
        print(f"未知模板: {slug}")
        return
    print(f"\n📋 {t['name']}")
    print(f"   尺寸: {t['size']}")
    print(f"   场景: {t['scene']}")
    print(f"   PSD: {t['psd']}")
    print(f"\n   可编辑字段 ({len(t['editable'])}个):")
    print(f"   {'图层':<12} {'字段':<14} {'示例':<25} {'容量':>4}")
    print(f"   {'─'*55}")
    for e in t["editable"]:
        print(f"   {e['layer']:<12} {e['field']:<14} {e['example']:<25} {e['max_len']:>4}字")
    if t.get("fonts"):
        print(f"\n   🅰 推荐字体: {', '.join(t['fonts'][:3])}")


# ═══════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="模板加载器")
    p.add_argument("--list", action="store_true", help="列出所有模板")
    p.add_argument("--info", help="查看模板详情 (morning/tech/doodle)")
    args = p.parse_args()

    if args.list:
        print("\n📂 官方模板:\n")
        list_templates()
    elif args.info:
        show_info(args.info)
    else:
        p.print_help()
