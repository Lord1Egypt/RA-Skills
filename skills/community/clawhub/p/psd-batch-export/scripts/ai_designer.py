"""
模板设计器 v3.0 — 基于官方 PSD 模板的设计工作台
===================================================
三款官方 PSD 模板，涵盖日签、邀请函、招聘海报场景。
通过 batch_from_excel.py 实现数据驱动批量填充。

用法:
  python ai_designer.py --list                    # 列出所有模板
  python ai_designer.py --info morning            # 查看模板可编辑字段
  python ai_designer.py --use morning --data 名单.xlsx --output output/  # 批量生成
  python ai_designer.py --use tech --ai --prompt "AI 峰会邀请函" --data 嘉宾.xlsx
"""

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from console_utils import configure_stdio
from template_loader import TEMPLATES, get_psd_path, list_templates, show_info

configure_stdio()

# LLM 集成（可选）
try:
    from design_llm import DesignLLM
    _llm = DesignLLM()
except Exception:
    _llm = None


# ═══════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════

def main():
    p = argparse.ArgumentParser(
        description="模板设计器 v3.0 — 基于官方 PSD 模板的智能设计工作台",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""官方模板:
  morning   早安手绘风日签 (720×1280)  — 早安问候/励志日签
  tech      炫彩风科技邀请函 (720×1280) — 科技峰会/产品发布
  doodle    手绘涂鸦招聘海报 (1284×2778) — 创意招聘/设计师岗位

示例:
  %(prog)s --list
  %(prog)s --info morning
  %(prog)s --use morning --data 日签文案.xlsx --output output/
  %(prog)s --use tech --ai --prompt "AI 峰会邀请函" --data 嘉宾.xlsx
        """
    )
    p.add_argument("--list", action="store_true", help="列出所有官方模板")
    p.add_argument("--info", choices=list(TEMPLATES.keys()), help="查看模板详情")
    p.add_argument("--use", choices=list(TEMPLATES.keys()), help="选择要使用的模板")
    p.add_argument("--data", help="Excel 数据文件路径（用于批量填充）")
    p.add_argument("--output", default="output", help="输出目录")
    p.add_argument("--ai", action="store_true", help="启用 LLM 智能建议")
    p.add_argument("--prompt", default="", help="自然语言描述（LLM 模式）")
    p.add_argument("--dpi", type=int, default=300, help="输出 DPI")
    p.add_argument("--preview", action="store_true", help="干运行预览模式")

    args = p.parse_args()

    if args.list:
        print("\n📂 PSD 图层级智能引擎 — 官方模板\n")
        list_templates()
        if _llm and _llm._available:
            print(f"\n  🤖 LLM 可用 ({_llm.model}) — 使用 --ai 启用智能建议")
        else:
            print("\n  💡 设置 OPENAI_API_KEY 后可启用 --ai 智能模式")
        return

    if args.info:
        show_info(args.info)
        psd_path = get_psd_path(args.info)
        print(f"\n  📁 PSD: {psd_path}")
        print(f"\n  使用方式:")
        print(f"    python batch_from_excel.py 名单.xlsx \"{psd_path}\" output/")
        if _llm and _llm._available:
            print(f"    （可添加 --ai --prompt \"描述\" 获取 LLM 建议）")
        return

    if args.use:
        t = TEMPLATES.get(args.use)
        if not t:
            print(f"❌ 未知模板: {args.use}")
            return

        psd_path = get_psd_path(args.use)
        print(f"\n🎨 模板: {t['name']} ({t['size']})")
        print(f"📁 PSD: {psd_path}")

        if args.ai and _llm and _llm._available:
            print("🤖 LLM 增强模式")
            if args.prompt:
                result = _llm.generate_palette(args.prompt)
                if result:
                    print(f"   配色建议: {result.get('name','?')} — {result.get('reason','')}")
            copy_result = _llm.write_copy(
                "poster" if args.use == "doodle" else "invitation",
                {"scene": t['scene'], "prompt": args.prompt}
            )
            if copy_result:
                print(f"   文案建议: {json.dumps(copy_result, ensure_ascii=False)[:200]}")

        if args.data:
            print(f"\n📊 数据驱动批量生成...")
            try:
                from batch_from_excel import batch_export
                count = batch_export(
                    args.data, str(psd_path), args.output,
                    dpi=args.dpi, dry_run=args.preview,
                )
            except Exception as e:
                print(f"   ⚠ 调用失败: {e}")
                print(f"   请手动运行:")
                print(f"   python batch_from_excel.py \"{args.data}\" \"{psd_path}\" \"{args.output}\"")
        else:
            print(f"\n💡 添加 --data 名单.xlsx 进行批量生成")
        return

    p.print_help()


if __name__ == "__main__":
    main()
