#!/usr/bin/env python3
"""
本地库存管理脚本
支持本地JSON文件或飞书多维表格存储
"""

import argparse
import json
import sys
import uuid
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

# 数据目录
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# 库存文件（本地存储模式）
INVENTORY_FILE = DATA_DIR / "inventory.json"

# 配置文件路径
CONFIG_FILE = Path(__file__).parent.parent / "references" / "config.json"


def load_config() -> Dict:
    """加载配置"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"storage": "local"}


def get_local_inventory() -> List[Dict]:
    """读取本地库存"""
    if INVENTORY_FILE.exists():
        with open(INVENTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_local_inventory(data: List[Dict]):
    """保存本地库存"""
    with open(INVENTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_bitable_inventory(config: Dict) -> List[Dict]:
    """
    从飞书多维表格读取库存
    注：需要安装飞书相关依赖并配置token
    """
    # 这里预留飞书API调用接口
    # 实际实现需要使用feishu_bitable相关工具
    print("飞书多维表格模式待实现，请确保已配置飞书token", file=sys.stderr)
    return []


def add_bitable_inventory(config: Dict, record: Dict) -> bool:
    """添加库存到飞书多维表格"""
    print("飞书多维表格模式待实现，请确保已配置飞书token", file=sys.stderr)
    return False


def delete_bitable_inventory(config: Dict, record_id: str) -> bool:
    """从飞书多维表格删除库存"""
    print("飞书多维表格模式待实现，请确保已配置飞书token", file=sys.stderr)
    return False


def list_inventory(config: Dict, steel_type: Optional[str] = None, 
                   spec: Optional[str] = None) -> List[Dict]:
    """列出库存"""
    storage = config.get("storage", "local")
    
    if storage == "bitable":
        inventory = get_bitable_inventory(config)
    else:
        inventory = get_local_inventory()
    
    # 过滤
    if steel_type:
        inventory = [r for r in inventory if steel_type in r.get("type", "")]
    if spec:
        inventory = [r for r in inventory if spec in r.get("spec", "")]
    
    return inventory


def add_inventory(config: Dict, steel_type: str, spec: str, price: float, 
                  quantity: Optional[float] = None, supplier: Optional[str] = None,
                  contact: Optional[str] = None, region: Optional[str] = None) -> bool:
    """添加库存记录"""
    storage = config.get("storage", "local")
    
    record = {
        "id": str(uuid.uuid4())[:8],
        "type": steel_type,
        "spec": spec,
        "price": price,
        "quantity": quantity,
        "supplier": supplier or "",
        "contact": contact or "",
        "region": region or "",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    if storage == "bitable":
        return add_bitable_inventory(config, record)
    else:
        inventory = get_local_inventory()
        inventory.append(record)
        save_local_inventory(inventory)
        return True


def delete_inventory(config: Dict, record_id: str) -> bool:
    """删除库存记录"""
    storage = config.get("storage", "local")
    
    if storage == "bitable":
        return delete_bitable_inventory(config, record_id)
    else:
        inventory = get_local_inventory()
        original_len = len(inventory)
        inventory = [r for r in inventory if r.get("id") != record_id]
        
        if len(inventory) < original_len:
            save_local_inventory(inventory)
            return True
        return False


def update_inventory(config: Dict, record_id: str, **kwargs) -> bool:
    """更新库存记录"""
    storage = config.get("storage", "local")
    
    if storage == "bitable":
        # 飞书模式待实现
        print("飞书多维表格更新功能待实现", file=sys.stderr)
        return False
    else:
        inventory = get_local_inventory()
        for r in inventory:
            if r.get("id") == record_id:
                for key, value in kwargs.items():
                    if value is not None:
                        r[key] = value
                r["updated_at"] = datetime.now().isoformat()
                save_local_inventory(inventory)
                return True
        return False


def format_inventory_output(inventory: List[Dict]) -> str:
    """格式化库存输出"""
    if not inventory:
        return "暂无库存记录"
    
    lines = []
    lines.append(f"{'ID':<10} {'品种':<10} {'规格':<12} {'价格':<10} {'数量':<8} {'地区':<8} {'更新日期':<20}")
    lines.append("-" * 90)
    
    for r in inventory:
        lines.append(
            f"{r.get('id', '-'):<10} "
            f"{r.get('type', '-'):<10} "
            f"{r.get('spec', '-'):<12} "
            f"{r.get('price', '-'):<10} "
            f"{r.get('quantity', '-'):<8} "
            f"{r.get('region', '-'):<8} "
            f"{r.get('updated_at', '-')[:19]:<20}"
        )
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="本地库存管理")
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # list 子命令
    list_parser = subparsers.add_parser("list", help="列出库存")
    list_parser.add_argument("--type", help="按品种筛选")
    list_parser.add_argument("--spec", help="按规格筛选")
    list_parser.add_argument("--json", action="store_true", help="JSON格式输出")
    
    # add 子命令
    add_parser = subparsers.add_parser("add", help="添加库存")
    add_parser.add_argument("--type", required=True, help="品种")
    add_parser.add_argument("--spec", required=True, help="规格")
    add_parser.add_argument("--price", type=float, required=True, help="价格(元/吨)")
    add_parser.add_argument("--quantity", type=float, help="数量(吨)")
    add_parser.add_argument("--supplier", help="供应商")
    add_parser.add_argument("--contact", help="联系方式")
    add_parser.add_argument("--region", help="地区")
    
    # remove 子命令
    remove_parser = subparsers.add_parser("remove", help="删除库存")
    remove_parser.add_argument("--id", required=True, help="记录ID")
    
    # update 子命令
    update_parser = subparsers.add_parser("update", help="更新库存")
    update_parser.add_argument("--id", required=True, help="记录ID")
    update_parser.add_argument("--price", type=float, help="新价格")
    update_parser.add_argument("--quantity", type=float, help="新数量")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    config = load_config()
    
    if args.command == "list":
        inventory = list_inventory(config, args.type, args.spec)
        if args.json:
            print(json.dumps(inventory, ensure_ascii=False, indent=2))
        else:
            print(format_inventory_output(inventory))
    
    elif args.command == "add":
        success = add_inventory(
            config,
            steel_type=args.type,
            spec=args.spec,
            price=args.price,
            quantity=args.quantity,
            supplier=args.supplier,
            contact=args.contact,
            region=args.region
        )
        if success:
            print(f"✓ 已添加库存记录: {args.type} {args.spec} {args.price}元/吨")
        else:
            print("✗ 添加失败", file=sys.stderr)
            sys.exit(1)
    
    elif args.command == "remove":
        success = delete_inventory(config, args.id)
        if success:
            print(f"✓ 已删除库存记录: {args.id}")
        else:
            print("✗ 删除失败，请检查ID是否正确", file=sys.stderr)
            sys.exit(1)
    
    elif args.command == "update":
        success = update_inventory(
            config, args.id,
            price=args.price,
            quantity=args.quantity
        )
        if success:
            print(f"✓ 已更新库存记录: {args.id}")
        else:
            print("✗ 更新失败，请检查ID是否正确", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
