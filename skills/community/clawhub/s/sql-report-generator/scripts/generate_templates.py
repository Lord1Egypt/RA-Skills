# -*- coding: utf-8 -*-
"""
generate_templates.py
从 dashboard_templates.py 读取模板，生成 .md 预设模板文件到 templates/ 目录

用法：
    python generate_templates.py              # 生成所有模板
    python generate_templates.py --dry-run    # 仅预览，不生成
    python generate_templates.py --industry 医疗  # 仅生成指定行业
"""

import os
import json
import argparse
from pathlib import Path

# 导入模板库
from dashboard_templates import DASHBOARD_LIBRARY, DashboardGenerator

# 脚本目录
SCRIPT_DIR = Path(__file__).parent
TEMPLATES_DIR = SCRIPT_DIR.parent / "templates"


def sanitize_filename(name: str) -> str:
    """将模板名称转换为合法的文件名"""
    # 替换特殊字符为空格，然后去除空格
    name = name.replace("&", "_")
    name = name.replace("/", "-")
    name = name.replace("\\", "-")
    name = name.replace("*", "")
    name = name.replace("?", "")
    name = name.replace(":", "-")
    name = name.replace("\"", "")
    name = name.replace("<", "")
    name = name.replace(">", "")
    name = name.replace("|", "")
    name = name.replace(" ", "_")
    # 去除连续的下划线
    while "__" in name:
        name = name.replace("__", "_")
    return name.lower()


def template_to_markdown(template) -> str:
    """将模板转换为 Markdown 格式"""
    
    md = f"""# {template.template_name}

**行业**: {template.industry}  
**模板ID**: {template.template_id}  
**描述**: {template.description}

---

## 核心指标

{', '.join(template.kpis)}

---

## 图表组合

"""

    for i, chart in enumerate(template.charts, 1):
        md += f"""### {i}. {chart.title}

**图表类型**: `{chart.chart_type}`

**简洁解读**: {chart.description}

**数据格式示例**:
```json
{json.dumps(chart.data_format, ensure_ascii=False, indent=2)}
```

**深度洞察**: {chart.insights}

---

"""

    md += f"""## 综合洞察

{template.insights}

---

## 运营建议

{template.recommendations}

---

*本模板由 sql-report-generator skill 自动生成*
"""

    return md


def generate_template_file(industry: str, template_id: str, template, dry_run: bool = False) -> tuple:
    """生成单个模板文件"""
    
    # 生成文件名
    filename = f"{sanitize_filename(template.template_id)}.md"
    filepath = TEMPLATES_DIR / filename
    
    if dry_run:
        status = "预览" if filepath.exists() else "新建"
        return (industry, template.template_name, filename, status, "")
    
    # 生成 Markdown 内容
    content = template_to_markdown(template)
    
    # 检查是否已存在
    if filepath.exists():
        # 读取现有内容，检查是否有自动生成标记
        with open(filepath, 'r', encoding='utf-8') as f:
            existing = f.read()
        
        # 如果有自动生成标记，则覆盖
        if "*本模板由 sql-report-generator skill 自动生成*" in existing:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return (industry, template.template_name, filename, "覆盖", "")
        else:
            return (industry, template.template_name, filename, "跳过(已存在)", "")
    else:
        # 新建文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return (industry, template.template_name, filename, "新建", "")


def main():
    parser = argparse.ArgumentParser(description='生成预设模板文件')
    parser.add_argument('--dry-run', action='store_true', help='仅预览，不生成文件')
    parser.add_argument('--industry', type=str, help='仅生成指定行业模板')
    parser.add_argument('--template-id', type=str, help='仅生成指定模板')
    args = parser.parse_args()
    
    print("=" * 70)
    print("sql-report-generator 预设模板生成器")
    print("=" * 70)
    print()
    
    if args.dry_run:
        print("[预览模式] 仅显示将要执行的操作，不会生成或修改文件")
        print()
    
    # 确保 templates 目录存在
    if not args.dry_run:
        TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
    
    # 统计
    results = []
    total = 0
    skipped = 0
    
    # 遍历所有行业
    industry_list = list(DASHBOARD_LIBRARY.items())
    
    if args.industry:
        industry_list = [(k, v) for k, v in industry_list if args.industry in k]
        if not industry_list:
            print(f"[错误] 未找到行业 '{args.industry}'")
            return
    
    for industry, templates in industry_list:
        print(f"[DIR] {industry}")
        
        for template_id, template in templates.items():
            total += 1
            
            # 如果指定了模板ID，则跳过其他模板
            if args.template_id and template_id != args.template_id:
                continue
            
            result = generate_template_file(
                industry, template_id, template, 
                dry_run=args.dry_run
            )
            results.append(result)
            
            status_icon = {
                "新建": "[NEW]",
                "覆盖": "[UPD]",
                "跳过(已存在)": "[SKIP]",
                "预览": "[VIEW]"
            }.get(result[3], "[???]")
            
            print(f"    {status_icon} {template.template_name}")
            
            if result[3] == "跳过(已存在)":
                skipped += 1
    
    # 输出统计
    print()
    print("=" * 70)
    print("生成完成")
    print("=" * 70)
    print(f"总计: {total} 个模板")
    print(f"新建: {sum(1 for r in results if r[3] == '新建')}")
    print(f"覆盖: {sum(1 for r in results if r[3] == '覆盖')}")
    print(f"跳过: {skipped}")
    print()
    print(f"生成目录: {TEMPLATES_DIR}")
    
    # 列出已有文件
    existing_files = list(TEMPLATES_DIR.glob("*.md"))
    print(f"已有模板文件: {len(existing_files)} 个")


if __name__ == '__main__':
    main()
