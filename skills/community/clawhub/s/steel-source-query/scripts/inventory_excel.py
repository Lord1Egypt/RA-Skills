#!/usr/bin/env python3
"""
Excel库存导入脚本
支持多个钢贸商上传库存Excel文件
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Optional
import uuid
from datetime import datetime

try:
    import pandas as pd
    from openpyxl import load_workbook
    EXCEL_SUPPORT = True
except ImportError:
    EXCEL_SUPPORT = False
    print("警告: 未安装pandas/openpyxl，Excel功能不可用", file=sys.stderr)
    print("请运行: pip install -r scripts/requirements.txt", file=sys.stderr)

# 数据目录
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# 库存文件
INVENTORY_FILE = DATA_DIR / "inventory.json"

# 支持的Excel列名映射（支持多种列名格式）
COLUMN_MAPPINGS = {
    "品种": ["品种", "钢材品种", "产品名称", "名称", "品名", "type", "steel_type"],
    "规格": ["规格", "规格型号", "型号", "spec", "specification"],
    "价格": ["价格", "单价", "售价", "price", "price_per_ton"],
    "数量": ["数量", "库存量", "库存", "quantity", "stock", "amount"],
    "供应商": ["供应商", "钢贸商", "商家", "公司", "supplier", "vendor", "company"],
    "联系人": ["联系人", "联系人姓名", "姓名", "contact", "contact_person"],
    "电话": ["电话", "联系电话", "手机", "手机号", "phone", "tel", "mobile"],
    "地区": ["地区", "城市", "省份", "region", "city", "province", "area"],
    "备注": ["备注", "说明", "备注信息", "remark", "note", "notes"]
}


def find_column(df_columns, target_names):
    """在DataFrame列中查找匹配的列名"""
    cols_lower = {c.lower().strip(): c for c in df_columns}
    for name in target_names:
        if name.lower() in cols_lower:
            return cols_lower[name.lower()]
    return None


def detect_columns(df):
    """自动检测Excel列对应关系"""
    column_map = {}
    df_columns = list(df.columns)
    
    for standard_name, possible_names in COLUMN_MAPPINGS.items():
        found = find_column(df_columns, possible_names)
        if found:
            column_map[standard_name] = found
    
    return column_map


def validate_data(df, column_map):
    """验证数据有效性"""
    errors = []
    
    # 必需字段检查
    required = ["品种", "规格", "价格"]
    for field in required:
        if field not in column_map:
            errors.append(f"缺少必需字段: {field}")
    
    if errors:
        return errors
    
    # 数据类型检查
    price_col = column_map.get("价格")
    if price_col:
        non_numeric = df[price_col].apply(lambda x: not is_numeric(x))
        if non_numeric.any():
            rows = df[non_numeric].index.tolist()
            errors.append(f"价格列包含非数字值，行号: {[r+2 for r in rows]}")
    
    return errors


def is_numeric(value):
    """检查值是否为数字"""
    if pd.isna(value):
        return True
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False


def load_inventory() -> List[Dict]:
    """读取现有库存"""
    if INVENTORY_FILE.exists():
        with open(INVENTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_inventory(data: List[Dict]):
    """保存库存"""
    with open(INVENTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def import_from_excel(file_path: str, default_supplier: Optional[str] = None, 
                      replace_existing: bool = False) -> Dict:
    """
    从Excel导入库存
    
    Args:
        file_path: Excel文件路径
        default_supplier: 默认供应商名称（如果Excel中没有供应商列）
        replace_existing: 是否替换该供应商的现有库存
    
    Returns:
        导入结果统计
    """
    if not EXCEL_SUPPORT:
        return {"success": False, "error": "Excel支持未安装"}
    
    file_path = Path(file_path)
    if not file_path.exists():
        return {"success": False, "error": f"文件不存在: {file_path}"}
    
    # 读取Excel
    try:
        df = pd.read_excel(file_path)
        df = df.dropna(how='all')  # 删除空行
    except Exception as e:
        return {"success": False, "error": f"读取Excel失败: {e}"}
    
    if df.empty:
        return {"success": False, "error": "Excel文件为空"}
    
    # 检测列映射
    column_map = detect_columns(df)
    
    # 验证数据
    errors = validate_data(df, column_map)
    if errors:
        return {"success": False, "error": "数据验证失败", "details": errors}
    
    # 获取现有库存
    inventory = load_inventory()
    
    # 如果需要替换该供应商的库存
    supplier_col = column_map.get("供应商")
    if replace_existing and supplier_col:
        suppliers_in_file = df[supplier_col].dropna().unique().tolist()
        if default_supplier:
            suppliers_in_file.append(default_supplier)
        inventory = [r for r in inventory if r.get("supplier") not in suppliers_in_file]
    elif replace_existing and default_supplier:
        inventory = [r for r in inventory if r.get("supplier") != default_supplier]
    
    # 导入记录
    imported = 0
    skipped = 0
    
    for _, row in df.iterrows():
        # 获取供应商
        if supplier_col and pd.notna(row[supplier_col]):
            supplier = str(row[supplier_col]).strip()
        else:
            supplier = default_supplier or ""
        
        # 跳过空行
        if pd.isna(row[column_map["品种"]]) or pd.isna(row[column_map["规格"]]):
            skipped += 1
            continue
        
        # 构建记录
        record = {
            "id": str(uuid.uuid4())[:8],
            "type": str(row[column_map["品种"]]).strip(),
            "spec": str(row[column_map["规格"]]).strip(),
            "price": float(row[column_map["price"]]) if pd.notna(row[column_map["price"]]) else 0,
            "supplier": supplier,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # 可选字段
        if "数量" in column_map and pd.notna(row[column_map["数量"]]):
            try:
                record["quantity"] = float(row[column_map["数量"]])
            except:
                pass
        
        if "联系人" in column_map and pd.notna(row[column_map["联系人"]]):
            record["contact"] = str(row[column_map["联系人"]]).strip()
        
        if "电话" in column_map and pd.notna(row[column_map["电话"]]):
            record["phone"] = str(row[column_map["电话"]]).strip()
        
        if "地区" in column_map and pd.notna(row[column_map["地区"]]):
            record["region"] = str(row[column_map["地区"]]).strip()
        
        if "备注" in column_map and pd.notna(row[column_map["备注"]]):
            record["remark"] = str(row[column_map["备注"]]).strip()
        
        inventory.append(record)
        imported += 1
    
    # 保存
    save_inventory(inventory)
    
    return {
        "success": True,
        "imported": imported,
        "skipped": skipped,
        "total": len(df),
        "supplier": default_supplier or "多个供应商"
    }


def export_template(output_path: str):
    """导出Excel模板"""
    if not EXCEL_SUPPORT:
        print("错误: Excel支持未安装", file=sys.stderr)
        return False
    
    # 创建示例数据
    sample_data = {
        "品种": ["螺纹钢", "热轧板卷"],
        "规格": ["Φ12-14 HRB400E", "4.75*1500*C Q235B"],
        "价格": [3850, 3650],
        "数量": [50, 30],
        "供应商": ["示例钢贸A", "示例钢贸B"],
        "联系人": ["张经理", "李经理"],
        "电话": ["13800138000", "13900139000"],
        "地区": ["唐山", "天津"],
        "备注": ["可议价", ""]
    }
    
    df = pd.DataFrame(sample_data)
    df.to_excel(output_path, index=False, engine='openpyxl')
    
    print(f"模板已导出: {output_path}")
    return True


def list_suppliers() -> List[str]:
    """列出所有供应商"""
    inventory = load_inventory()
    suppliers = set()
    for r in inventory:
        if r.get("supplier"):
            suppliers.add(r["supplier"])
    return sorted(list(suppliers))


def clear_supplier(supplier: str) -> int:
    """清空某供应商的所有库存"""
    inventory = load_inventory()
    original_count = len(inventory)
    inventory = [r for r in inventory if r.get("supplier") != supplier]
    save_inventory(inventory)
    return original_count - len(inventory)


def main():
    parser = argparse.ArgumentParser(description="Excel库存导入工具")
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # import 子命令
    import_parser = subparsers.add_parser("import", help="导入Excel")
    import_parser.add_argument("file", help="Excel文件路径")
    import_parser.add_argument("--supplier", help="默认供应商名称")
    import_parser.add_argument("--replace", action="store_true", help="替换该供应商的现有库存")
    
    # template 子命令
    template_parser = subparsers.add_parser("template", help="导出Excel模板")
    template_parser.add_argument("--output", default="库存模板.xlsx", help="输出路径")
    
    # suppliers 子命令
    subparsers.add_parser("suppliers", help="列出所有供应商")
    
    # clear 子命令
    clear_parser = subparsers.add_parser("clear", help="清空某供应商库存")
    clear_parser.add_argument("supplier", help="供应商名称")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if not EXCEL_SUPPORT:
        print("错误: 请先安装依赖: pip install -r scripts/requirements.txt", file=sys.stderr)
        sys.exit(1)
    
    if args.command == "import":
        result = import_from_excel(args.file, args.supplier, args.replace)
        if result["success"]:
            print(f"✓ 导入成功")
            print(f"  导入: {result['imported']} 条")
            print(f"  跳过: {result['skipped']} 条")
            print(f"  总计: {result['total']} 条")
            print(f"  供应商: {result['supplier']}")
        else:
            print(f"✗ 导入失败: {result['error']}")
            if "details" in result:
                for detail in result["details"]:
                    print(f"  - {detail}")
            sys.exit(1)
    
    elif args.command == "template":
        export_template(args.output)
    
    elif args.command == "suppliers":
        suppliers = list_suppliers()
        if suppliers:
            print("已录入的供应商:")
            for s in suppliers:
                print(f"  - {s}")
        else:
            print("暂无供应商数据")
    
    elif args.command == "clear":
        count = clear_supplier(args.supplier)
        print(f"✓ 已清空供应商 [{args.supplier}] 的 {count} 条库存记录")


if __name__ == "__main__":
    main()
