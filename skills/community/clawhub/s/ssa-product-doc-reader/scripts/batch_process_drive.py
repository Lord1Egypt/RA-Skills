#!/usr/bin/env python3
"""
批量处理 Google Drive 中的产品图纸，提取信息并归档到知识库

用法：
  python3 batch_process_drive.py --drive-folder-id <folder_id> --output-dir <knowledge_base_path>
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# 配置
WORKSPACE = os.getenv("WORKSPACE", Path(__file__).parent.parent.parent)
TEMP_DIR = Path(WORKSPACE) / "temp/599-batch"
KB_DIR = Path(WORKSPACE) / "obsidian-vault/Farreach 知识库/02-产品目录/599 系列"

# 599 系列所有 PDF 文件 ID（共 58 个）
PDF_FILES = {
    "599-001": "file_id_here",
    "599-002": "file_id_here",
    # ... 需要完整的 58 个文件 ID
}

def get_drive_files(folder_id: str) -> dict:
    """从 Google Drive 获取文件夹中的所有 PDF 文件"""
    cmd = ["gog", "drive", "ls", "--parent", folder_id]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    files = {}
    for line in result.stdout.split('\n'):
        if '.pdf' in line.lower():
            parts = line.split()
            if len(parts) >= 2:
                file_id = parts[0]
                file_name = parts[1]
                if file_name.endswith('.pdf'):
                    drawing_no = file_name.replace('.pdf', '')
                    files[drawing_no] = file_id
    
    return files

def download_file(file_id: str, output_path: Path) -> bool:
    """下载单个文件"""
    cmd = ["gog", "drive", "download", file_id]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    for line in result.stdout.split('\n'):
        if line.startswith('path'):
            downloaded_path = line.split('\t')[1].strip()
            subprocess.run(["mv", downloaded_path, str(output_path)], check=True)
            return True
    return False

def extract_drawing_info(pdf_path: Path) -> dict:
    """用 product-doc-reader 提取图纸信息"""
    script_path = Path(WORKSPACE + "/skills/product-doc-reader/scripts/extract_hybrid.py")
    
    cmd = [
        "python3", str(script_path),
        str(pdf_path),
        "--stdout", "-f", "json"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    try:
        # 解析 JSON（跳过 stderr）
        json_str = result.stdout.strip()
        if json_str.startswith('{'):
            return json.loads(json_str)
    except Exception as e:
        print(f"  ⚠️ JSON 解析失败：{e}")
    
    return {}

def create_kb_entry(drawing_data: dict, output_dir: Path) -> Path:
    """创建知识库条目"""
    drawing_no = drawing_data.get("drawing_no", "unknown")
    product_name = drawing_data.get("product_name", "未知产品")
    model_no = drawing_data.get("model_no", "")
    
    # 创建 Markdown 文档
    md_content = f"""# {drawing_no} - {product_name}

> 📅 **提取日期：** {datetime.now().strftime('%Y-%m-%d')}  
> 📐 **模具编号 (Model No.)：** {model_no or '未标注'}  
> 📋 **Drawing No.：** {drawing_no}  
> 🏭 **公司：** {drawing_data.get('company', '珠海福睿电子 FARREACH')}

---

## 📊 基本信息

| 项目 | 内容 |
|------|------|
| **客人品名** | {product_name} |
| **模具编号** | {model_no or '—'} |
| **Drawing No.** | {drawing_no} |
| **包装规范** | {drawing_data.get('packaging_spec', '—')} |
| **长度 (mm)** | {drawing_data.get('length_mm', '—')} |

---

## 🔧 BOM 物料清单

| NO. | 部件名称 | 规格 | 用量 |
|-----|----------|------|------|
"""
    
    # 添加 BOM 行
    for row in drawing_data.get("bom", [])[:20]:  # 限制 20 行
        md_content += f"| {row.get('no', '')} | {row.get('part_name', '')} | {row.get('spec', '')} | {row.get('quantity', '')} |\n"
    
    # 添加测试要求
    tests = drawing_data.get("test_requirements", {})
    if tests:
        md_content += f"""
---

## 🧪 测试要求

"""
        test_table = tests.get("table", [])
        if test_table:
            md_content += "| 长度范围 | 导通阻抗 | 绝缘阻抗 | DC V/S |\n|----------|----------|----------|--------|\n"
            for t in test_table:
                md_content += f"| {t.get('length_range', '')} | {t.get('resistance', '')} | {t.get('insulation', '')} | {t.get('dc_vs', '')} |\n"
        
        other_tests = tests.get("other_tests", [])
        if other_tests:
            for t in other_tests:
                md_content += f"- {t}\n"
    
    # 添加模具信息
    mold_info = drawing_data.get("mold_info", "")
    if mold_info:
        md_content += f"""
---

## 🏗️ 模具信息

{mold_info}
"""
    
    # 添加注意事项
    notes = drawing_data.get("notes", [])
    if notes:
        md_content += f"""
---

## ⚠️ 注意事项

"""
        for note in notes:
            md_content += f"- {note}\n"
    
    # 添加变更记录
    revs = drawing_data.get("revision_history", [])
    if revs:
        md_content += f"""
---

## 📝 变更记录

| 版本 | 日期 | 内容 |
|------|------|------|
"""
        for r in revs:
            md_content += f"| {r.get('revision', '')} | {r.get('date', '')} | {r.get('description', '')} |\n"
    
    md_content += f"""
---

*本文档由 Product Doc Reader v4.0 自动提取*
"""
    
    # 保存文件
    output_dir.mkdir(parents=True, exist_ok=True)
    md_path = output_dir / f"{drawing_no}.md"
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    return md_path

def main():
    parser = argparse.ArgumentParser(description="批量处理产品图纸并归档到知识库")
    parser.add_argument("--drive-folder-id", required=True, help="Google Drive 文件夹 ID")
    parser.add_argument("--output-dir", default=str(KB_DIR), help="知识库输出目录")
    parser.add_argument("--temp-dir", default=str(TEMP_DIR), help="临时目录")
    parser.add_argument("--limit", type=int, default=0, help="限制处理数量（0=全部）")
    
    args = parser.parse_args()
    
    print(f"=== 批量处理产品图纸 ===")
    print(f"Drive 文件夹：{args.drive_folder_id}")
    print(f"知识库目录：{args.output_dir}")
    print()
    
    # 1. 获取文件列表
    print("[1/4] 获取文件列表...")
    files = get_drive_files(args.drive_folder_id)
    print(f"  找到 {len(files)} 个 PDF 文件")
    
    if args.limit > 0:
        files = dict(list(files.items())[:args.limit])
        print(f"  限制处理 {len(files)} 个")
    
    # 2. 创建目录
    temp_dir = Path(args.temp_dir)
    output_dir = Path(args.output_dir)
    temp_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 3. 批量处理
    print(f"\n[2/4] 批量处理图纸...")
    results = []
    
    for i, (drawing_no, file_id) in enumerate(files.items(), 1):
        print(f"\n[{i}/{len(files)}] {drawing_no}")
        
        # 下载
        pdf_path = temp_dir / f"{drawing_no}.pdf"
        if not pdf_path.exists():
            print(f"  下载...")
            if not download_file(file_id, pdf_path):
                print(f"  ❌ 下载失败")
                continue
        
        # 提取
        print(f"  提取信息...")
        drawing_data = extract_drawing_info(pdf_path)
        
        if not drawing_data:
            print(f"  ❌ 提取失败")
            continue
        
        # 显示关键信息
        product_name = drawing_data.get("product_name", "")
        model_no = drawing_data.get("model_no", "")
        print(f"  ✅ 产品：{product_name[:50]}")
        print(f"     模具：{model_no}")
        
        # 归档
        md_path = create_kb_entry(drawing_data, output_dir)
        print(f"  📁 已归档：{md_path.name}")
        
        results.append({
            "drawing_no": drawing_no,
            "product_name": product_name,
            "model_no": model_no,
            "md_path": str(md_path),
        })
    
    # 4. 生成汇总
    print(f"\n[3/4] 生成汇总...")
    
    summary_md = f"""# 599 系列产品图纸汇总

> 📅 生成日期：{datetime.now().strftime('%Y-%m-%d %H:%M')}  
> 📊 图纸总数：{len(results)}  
> 🏭 公司：珠海福睿电子 FARREACH

---

## 📋 模具对照表

| Drawing No. | 模具编号 (Model No.) | 产品名称 | 知识库 |
|-------------|---------------------|----------|--------|
"""
    
    for r in sorted(results, key=lambda x: x['drawing_no']):
        summary_md += f"| {r['drawing_no']} | {r['model_no']} | {r['product_name'][:50]} | [查看]({Path(r['md_path']).name}) |\n"
    
    summary_md += f"""
---

## 📊 统计

- **总图纸数：** {len(results)}
- **已归档：** {len(results)}
- **失败：** {len(files) - len(results)}

---

*由 Product Doc Reader v4.0 自动生成*
"""
    
    summary_path = output_dir / "00-599 系列汇总.md"
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(summary_md)
    
    print(f"  ✅ 汇总：{summary_path}")
    
    # 5. 清理临时文件
    print(f"\n[4/4] 清理临时文件...")
    subprocess.run(["rm", "-rf", str(temp_dir)], check=True)
    print(f"  ✅ 已清理：{temp_dir}")
    
    # 完成
    print(f"\n✅ 完成！")
    print(f"   处理：{len(results)}/{len(files)}")
    print(f"   知识库：{output_dir}")

if __name__ == "__main__":
    main()
