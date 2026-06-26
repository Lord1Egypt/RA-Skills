#!/usr/bin/env python3
"""
库存共享与搜索模块
支持钢贸商发布库存，采购商搜索库存
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict

# 数据目录
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# 公开库存文件（所有用户可访问）
PUBLIC_INVENTORY_FILE = DATA_DIR / "inventory_public.json"

@dataclass
class PublicInventoryItem:
    """公开库存条目"""
    id: str                   # 唯一ID
    type: str                 # 品种
    spec: str                 # 规格
    material: str             # 材质
    quantity: float           # 数量
    price: float              # 单价
    warehouse: str            # 仓库/地区
    supplier: str             # 供应商名称
    contact: str              # 联系人
    phone: str                # 电话
    wechat: str = ""          # 微信号
    status: str = "在售"       # 状态：在售/已售/下架
    publish_time: str = ""     # 发布时间
    update_time: str = ""      # 更新时间
    view_count: int = 0        # 浏览次数
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> "PublicInventoryItem":
        return cls(**data)


class InventoryPublisher:
    """库存发布器"""
    
    @staticmethod
    def publish(item: PublicInventoryItem) -> bool:
        """发布库存到公共平台"""
        try:
            # 生成ID
            import uuid
            item.id = str(uuid.uuid4())[:8]
            item.publish_time = datetime.now().isoformat()
            item.update_time = item.publish_time
            
            # 加载现有库存
            inventory = InventoryPublisher._load_public_inventory()
            
            # 添加新库存
            inventory.append(item.to_dict())
            
            # 保存
            with open(PUBLIC_INVENTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(inventory, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"发布失败: {e}")
            return False
    
    @staticmethod
    def update(item_id: str, updates: Dict) -> bool:
        """更新库存信息"""
        try:
            inventory = InventoryPublisher._load_public_inventory()
            
            for item in inventory:
                if item.get("id") == item_id:
                    item.update(updates)
                    item["update_time"] = datetime.now().isoformat()
                    break
            
            with open(PUBLIC_INVENTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(inventory, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"更新失败: {e}")
            return False
    
    @staticmethod
    def delete(item_id: str) -> bool:
        """删除库存"""
        try:
            inventory = InventoryPublisher._load_public_inventory()
            inventory = [item for item in inventory if item.get("id") != item_id]
            
            with open(PUBLIC_INVENTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(inventory, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"删除失败: {e}")
            return False
    
    @staticmethod
    def _load_public_inventory() -> List[Dict]:
        """加载公开库存"""
        if PUBLIC_INVENTORY_FILE.exists():
            with open(PUBLIC_INVENTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []


class InventorySearcher:
    """库存搜索器"""
    
    @staticmethod
    def search(
        type_filter: str = "",
        spec_filter: str = "",
        material_filter: str = "",
        region_filter: str = "",
        supplier_filter: str = "",
        max_price: float = None,
        min_quantity: float = None,
        status: str = "在售"
    ) -> List[PublicInventoryItem]:
        """
        搜索库存
        
        Args:
            type_filter: 品种筛选
            spec_filter: 规格筛选
            material_filter: 材质筛选
            region_filter: 地区筛选
            supplier_filter: 供应商筛选
            max_price: 最高价格
            min_quantity: 最小数量
            status: 状态筛选
        """
        inventory = InventoryPublisher._load_public_inventory()
        results = []
        
        for item_data in inventory:
            item = PublicInventoryItem.from_dict(item_data)
            
            # 状态筛选
            if status and item.status != status:
                continue
            
            # 品种筛选
            if type_filter and type_filter not in item.type:
                continue
            
            # 规格筛选（模糊匹配）
            if spec_filter and spec_filter not in item.spec:
                continue
            
            # 材质筛选
            if material_filter and material_filter.upper() not in item.material.upper():
                continue
            
            # 地区筛选
            if region_filter and region_filter not in item.warehouse:
                continue
            
            # 供应商筛选
            if supplier_filter and supplier_filter not in item.supplier:
                continue
            
            # 价格筛选
            if max_price is not None and item.price > max_price:
                continue
            
            # 数量筛选
            if min_quantity is not None and item.quantity < min_quantity:
                continue
            
            results.append(item)
        
        # 按发布时间倒序
        results.sort(key=lambda x: x.publish_time, reverse=True)
        
        return results
    
    @staticmethod
    def get_by_id(item_id: str) -> Optional[PublicInventoryItem]:
        """根据ID获取库存详情"""
        inventory = InventoryPublisher._load_public_inventory()
        
        for item_data in inventory:
            if item_data.get("id") == item_id:
                # 增加浏览次数
                item_data["view_count"] = item_data.get("view_count", 0) + 1
                with open(PUBLIC_INVENTORY_FILE, "w", encoding="utf-8") as f:
                    json.dump(inventory, f, ensure_ascii=False, indent=2)
                
                return PublicInventoryItem.from_dict(item_data)
        
        return None
    
    @staticmethod
    def get_by_supplier(supplier: str) -> List[PublicInventoryItem]:
        """获取某供应商的所有库存"""
        return InventorySearcher.search(supplier_filter=supplier)
    
    @staticmethod
    def get_statistics() -> Dict:
        """获取库存统计信息"""
        inventory = InventoryPublisher._load_public_inventory()
        
        total_count = len(inventory)
        on_sale_count = len([i for i in inventory if i.get("status") == "在售"])
        
        # 按品种统计
        type_stats = {}
        for item in inventory:
            t = item.get("type", "未知")
            type_stats[t] = type_stats.get(t, 0) + 1
        
        # 按地区统计
        region_stats = {}
        for item in inventory:
            r = item.get("warehouse", "未知")
            region_stats[r] = region_stats.get(r, 0) + 1
        
        return {
            "total": total_count,
            "on_sale": on_sale_count,
            "by_type": type_stats,
            "by_region": region_stats
        }


def format_search_results(items: List[PublicInventoryItem]) -> str:
    """格式化搜索结果"""
    if not items:
        return "🔍 暂无符合条件的库存\n\n建议您：\n• 放宽搜索条件\n• 换个品种或地区试试\n• 过段时间再查（库存实时更新）"
    
    lines = []
    lines.append(f"🔍 找到 {len(items)} 条库存：")
    lines.append("")
    
    for i, item in enumerate(items[:10], 1):  # 最多显示10条
        lines.append(f"【{i}】{item.type} {item.spec} {item.material}")
        lines.append(f"    💰 价格：{item.price} 元/吨")
        lines.append(f"    📦 数量：{item.quantity} 吨")
        lines.append(f"    📍 仓库：{item.warehouse}")
        lines.append(f"    🏢 供应商：{item.supplier}")
        
        if item.phone:
            # 隐藏部分号码
            phone_display = item.phone[:3] + "****" + item.phone[-4:] if len(item.phone) > 7 else item.phone
            lines.append(f"    📞 电话：{phone_display}")
        
        # 计算发布时间
        if item.publish_time:
            try:
                pub_time = datetime.fromisoformat(item.publish_time)
                days_ago = (datetime.now() - pub_time).days
                if days_ago == 0:
                    time_str = "今天"
                elif days_ago == 1:
                    time_str = "昨天"
                else:
                    time_str = f"{days_ago}天前"
                lines.append(f"    🕐 发布：{time_str}")
            except:
                pass
        
        lines.append("")
    
    if len(items) > 10:
        lines.append(f"... 还有 {len(items) - 10} 条，请细化搜索条件查看")
    
    lines.append("💡 回复【查看详情+序号】获取完整联系信息")
    lines.append("💡 回复【搜索+条件】继续搜索")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="库存共享与搜索")
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # search 子命令
    search_parser = subparsers.add_parser("search", help="搜索库存")
    search_parser.add_argument("--type", help="品种")
    search_parser.add_argument("--spec", help="规格")
    search_parser.add_argument("--material", help="材质")
    search_parser.add_argument("--region", help="地区")
    search_parser.add_argument("--max-price", type=float, help="最高价格")
    search_parser.add_argument("--min-qty", type=float, help="最小数量")
    
    # stats 子命令
    subparsers.add_parser("stats", help="库存统计")
    
    # my 子命令
    my_parser = subparsers.add_parser("my", help="我的库存")
    my_parser.add_argument("--supplier", required=True, help="供应商名称")
    
    args = parser.parse_args()
    
    if args.command == "search":
        results = InventorySearcher.search(
            type_filter=args.type or "",
            spec_filter=args.spec or "",
            material_filter=args.material or "",
            region_filter=args.region or "",
            max_price=args.max_price,
            min_quantity=args.min_qty
        )
        print(format_search_results(results))
    
    elif args.command == "stats":
        stats = InventorySearcher.get_statistics()
        print("📊 平台库存统计")
        print(f"总库存数：{stats['total']}")
        print(f"在售库存：{stats['on_sale']}")
        print("\n按品种分布：")
        for t, count in sorted(stats['by_type'].items(), key=lambda x: -x[1]):
            print(f"  {t}: {count}条")
        print("\n按地区分布：")
        for r, count in sorted(stats['by_region'].items(), key=lambda x: -x[1]):
            print(f"  {r}: {count}条")
    
    elif args.command == "my":
        results = InventorySearcher.get_by_supplier(args.supplier)
        print(f"🏢 {args.supplier} 的库存（{len(results)}条）")
        print(format_search_results(results))
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
