#!/usr/bin/env python3
"""
批量处理 599 系列图纸（58 个完整），提取信息并归档到知识库
"""

import json
import os
import subprocess
from pathlib import Path
from datetime import datetime

# 配置
WORKSPACE = os.getenv("WORKSPACE", Path(__file__).parent.parent.parent)
TEMP_DIR = Path(WORKSPACE) / "temp/599-batch"
KB_DIR = Path(WORKSPACE) / "obsidian-vault/Farreach 知识库/02-产品目录/599 系列"

# 599 系列 PDF 文件 ID（58 个完整）
PDF_FILES = {
    "599-001": "1Y_G4OH4iIOH4GHkyB3F07g471VBfpc3A",
    "599-002": "1122b4zvB6HVZoHejQvJ4pakAKpt7DYyO",
    "599-003": "1mHfdapDWKjVGlYPoZO7GpOqqBZK4yP_0",
    "599-004": "1ChulZI-MXO54lKEmb3ikZNXw3MRFmk4e",
    "599-005": "1evzwnZWZlu6RJN_oHXckPq-0Zj-PXwtc",
    "599-006": "1sTzDRydvUwQPitB-eAxv_2hBbMsqbS7a",
    "599-007": "19wZEYl2QdYOiKos_ohzoJJncoDEyehcL",
    "599-008": "1HH0p16AT9fC3JdxHSYEpJVWuNvNfHkj7",
    "599-009": "19_zCzHt_qdWbiFYSuv4bONzJv3HllcRn",
    "599-010": "1UTuU33FqK8ATrRTnwFORxyso6lNWMbca",
    "599-011": "1ibb8Pxn1QV7vnWoJiLggZ7wEpFjRZQ6S",
    "599-012": "1EaUa86FuthhXo19Xdjh_cfKSn3k_-rDK",
    "599-013": "1auZVPUyvcOA4cox5i31-y4meqi3mhakd",
    "599-014": "1FhdQheJtkYOSmLZbh3HdgmmoF-NtaSOt",
    "599-015": "1ttmP5e19LfuJi_wH4j2hyGjmvRR_GEvr",
    "599-016": "1T15NxwPLm8RdN9YpRH_76LvOVMTo3NVI",
    "599-017": "1FYGJC7l-EbEmlDBTQDgQwe2CW_adqxCz",
    "599-018": "12zObmOBKCEX5jvN_BD6XWdUToCrQcHVZ",
    "599-019": "128F9cCc_RY2QJWBOX9kiD-okRDJANFNm",
    "599-020": "1Ijlk6Bw9MgSU_Kb8I0lIaMTZNF9xu9fz",
    "599-021": "1eNhn6VBD7jdZ41ZN8QTdXoerVnqQ8FVn",
    "599-022": "1OfnItTgMP3JqHgz_drIY9esO2xsZaImg",
    "599-023": "1LE8f9u68jDeZdvPoeX-KeDOBV7eJHSXv",
    "599-024": "1GGKlfbCdqKUK4m9hstpyhBgAGGS9DmTs",
    "599-025": "1OjLJQq0Pk7R_TxOLB2KW8zFAGFRnRN87",
    "599-026": "13pxuaYdOzf93vJcvzUXah2LQbQpfJ0LJ",
    "599-027": "1dMsIUXuq0IrhUSwFDc0xpweQGdeqI7LO",
    "599-028": "1W7bLQft7Q6wm156vMGVXruUHkPE4fJ3i",
    "599-029": "1anugs_Vi0DCg_FzU1L8WNmDty-u-PvNh",
    "599-030": "1exRU04OteixrxVQCIIsUr-s_SDe1EVLZ",
    "599-031": "1YvbTBDrCGv3ur7VWlOwL7SmPeHwH1Enc",
    "599-032": "18_D_1hqrkaPCvxkxvmofQG1e8DQliRxs",
    "599-033": "1D05ttPJAd7UvK2nNE1d49lb-6oRTL_ya",
    "599-034": "1sbHlDRf22vAA7wECD3Mch-fB3cG6_o0y",
    "599-035": "1i9TfdjVOzdc4666OAAya9EjInJrK3cE1",
    "599-036": "14mJJr1R1fQ6dR3kVwi81crxm4hZzWHEL",
    "599-037": "1hFsF9hK4PEp-Mtu9YSutYXfTb4th0c5p",
    "599-038": "12PTguhqFoGhP5K1d8yRASuv955dzBn9V",
    "599-039": "1CBjhNcZnI62EJknnQBBAMrYwDYPNbuYZ",
    "599-040": "1790VoUHuqhPnjvrOPYMKgSo64PSetgsT",
    "599-041": "1CQHGCquLXVCwGhnnxbZKacAr1snJu18F",
    "599-042": "1_jBNYa2cTxOs1mk2idVEjLs8HGp-TG03",
    "599-043": "1qsOr_6TRd-jrhorhlKjK3RXKvD97bGLj",
    "599-044": "1OOc_p17xnwcjVmQ9BArYnA1z49vSgf-j",
    "599-045": "1ZYJ6ev_siIBj4hBy-4YzVw8mCys8RbkZ",
    "599-046": "1dp5NJ1vvmRXgGWub1Tc9wp6hsbUVNO_0",
    "599-047": "18KseYwiC9moa8kv4HhtYSpaB6jvwHK8R",
    "599-048": "1JK33YqldmQJr4uCkgm-ZW40Mnkf-LqPJ",
    "599-049": "1NT__8jbcQEZ1hIwSyz5KdNr3n-sax8g1",
    "599-050": "1K57qg9TrvhdG-4BwtInygLB03a0VE0vL",
    "599-051": "18VgKexF-l8uP-JtuL08AEpFffG9UjE-_",
    "599-052": "1o7JhrmuyK4K2kiwd1SiBkqpoYsgknoXN",
    "599-053": "1of0LD_2nZlfMLfHl-Un_EQkPY5fPmOaF",
    "599-054": "1c3xUISBmBirDqKaTuEx2u5AQMSzRH13F",
    "599-055": "1Lh6-MjRI4NfM-HPgVSdx8QuRD08WRixR",
    "599-056": "1fjc2eu5-0yEQfCnJGJmmdZQBkBYR9K2b",
    "599-057": "1LC970qPP5oP7j5l8SIewSeTxjkcRdLbB",
    "599-058": "1qmlHXCTncPasokVsNCDnMZwJYzFWek2C",
}

def download_file(file_id: str, output_path: Path) -> bool:
    """下载文件"""
    cmd = ["gog", "drive", "download", file_id]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    for line in result.stdout.split('\n'):
        if line.startswith('path'):
            downloaded_path = line.split('\t')[1].strip()
            subprocess.run(["mv", downloaded_path, str(output_path)], check=True)
            return True
    return False

def extract_drawing_info(pdf_path: Path) -> dict:
    """提取图纸信息"""
    script_path = Path(WORKSPACE + "/skills/product-doc-reader/scripts/extract_hybrid.py")
    
    cmd = ["python3", str(script_path), str(pdf_path), "--stdout", "-f", "json"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    try:
        json_str = result.stdout.strip()
        if json_str.startswith('{'):
            return json.loads(json_str)
    except:
        pass
    return {}

def create_kb_entry(data: dict, output_dir: Path) -> Path:
    """创建知识库条目"""
    drawing_no = data.get("drawing_no", "unknown")
    product_name = data.get("product_name", "未知产品")
    model_no = data.get("model_no", "")
    
    products = data.get("products", [])
    
    md = f"""# {drawing_no} - {product_name[:50]}

> 📅 **提取日期：** {datetime.now().strftime('%Y-%m-%d')}  
> 📐 **模具编号 (Model No.)：** `{model_no or '未标注'}`  
> 📋 **Drawing No.：** {drawing_no}  
> 🏭 **公司：** {data.get('company', '珠海福睿电子 FARREACH')}

---

## 📊 产品信息

| 项目 | 内容 |
|------|------|
"""
    
    if len(products) > 1:
        md += "| 客人品名 | 长度 (mm) | 包装规范 |\n|----------|----------|----------|\n"
        for p in products:
            md += f"| {p.get('customer_item', '')} | {p.get('length_mm', '')} | {p.get('packaging_spec', '')} |\n"
    else:
        md += f"| **客人品名** | {product_name} |\n"
        md += f"| **模具编号** | {model_no or '—'} |\n"
        md += f"| **包装规范** | {data.get('packaging_spec', '—')} |\n"
        md += f"| **长度 (mm)** | {data.get('length_mm', '—')} |\n"
    
    md += f"\n---\n\n## 🔧 BOM 物料清单\n\n"
    md += "| NO. | 部件名称 | 规格 | 用量 |\n|-----|----------|------|------|\n"
    
    for row in data.get("bom", [])[:15]:
        spec = row.get('spec', '')[:80]
        md += f"| {row.get('no', '')} | {row.get('part_name', '')} | {spec} | {row.get('quantity', '')} |\n"
    
    tests = data.get("test_requirements", {})
    if tests:
        md += f"\n---\n\n## 🧪 测试要求\n\n"
        for t in tests.get("other_tests", []):
            md += f"- {t}\n"
    
    mold = data.get("mold_info", "")
    if mold:
        md += f"\n---\n\n## 🏗️ 模具信息\n\n```\n{mold}\n```\n"
    
    notes = data.get("notes", [])
    if notes:
        md += f"\n---\n\n## ⚠️ 注意事项\n\n"
        for n in notes:
            md += f"- {n}\n"
    
    md += f"\n---\n\n*由 Product Doc Reader v4.0 自动提取*\n"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    md_path = output_dir / f"{drawing_no}.md"
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md)
    
    return md_path

def main():
    print(f"=== 批量处理 599 系列图纸 (58 个完整) ===")
    print(f"文件数：{len(PDF_FILES)}")
    print(f"知识库：{KB_DIR}")
    print()
    
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    
    for i, (drawing_no, file_id) in enumerate(PDF_FILES.items(), 1):
        print(f"[{i:2d}/58] {drawing_no}")
        
        pdf_path = TEMP_DIR / f"{drawing_no}.pdf"
        if not pdf_path.exists():
            if not download_file(file_id, pdf_path):
                print(f"        ❌ 下载失败")
                continue
        
        data = extract_drawing_info(pdf_path)
        if not data:
            print(f"        ❌ 提取失败")
            continue
        
        product = data.get("product_name", "")[:40]
        model = data.get("model_no", "")
        drawing = data.get("drawing_no", drawing_no)
        
        # 如果产品名是 drawing no，说明提取有问题
        if product == drawing_no or len(product) <= 3:
            products = data.get("products", [])
            if products:
                product = products[0].get("customer_item", "")[:40]
        
        print(f"        ✅ {product} → Model: {model}")
        
        create_kb_entry(data, KB_DIR)
        results.append({
            "drawing_no": drawing_no,
            "model_no": model,
            "product": product,
        })
    
    # 生成汇总
    summary = f"""# 599 系列产品图纸汇总

> 📅 生成：{datetime.now().strftime('%Y-%m-%d %H:%M')}  
> 📊 总数：{len(results)}/58

## 模具对照表

| Drawing No. | 模具编号 | 产品 |
|-------------|---------|------|
"""
    for r in sorted(results, key=lambda x: x['drawing_no']):
        summary += f"| {r['drawing_no']} | {r['model_no']} | {r['product']} |\n"
    
    summary_path = KB_DIR / "00-599 汇总.md"
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    subprocess.run(["rm", "-rf", str(TEMP_DIR)], check=True)
    
    print(f"\n✅ 完成！")
    print(f"   成功：{len(results)}/58")
    print(f"   知识库：{KB_DIR}")
    print(f"   汇总：{summary_path}")

if __name__ == "__main__":
    main()
