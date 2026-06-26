#!/usr/bin/env python3
"""
库存搜索模块 - 通过OpenClaw飞书工具访问
数据存储在飞书多维表格中
"""

import json
import argparse
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict

# 飞书多维表格配置
BITABLE_APP_TOKEN = "A27gbl3lDaheavs4sFhcO1K4ngg"
BITABLE_TABLE_ID = "tblOpHmJjdqqr3aD"


def extract_text_value(value) -> str:
    """从飞书字段提取文本值"""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        if value and isinstance(value[0], dict):
            return value[0].get("text", "")
        return str(value[0]) if value else ""
    if isinstance(value, dict):
        return value.get("text", "")
    return str(value)


class FeishuBitableConnector:
    """飞书多维表格连接器 - 通过OpenClaw工具调用"""
    
    # 存储待处理的查询参数
    pending_queries = []
    
    @classmethod
    def set_query_params(cls, app_token: str, table_id: str):
        cls.pending_queries.append({
            "app_token": app_token,
            "table_id": table_id
        })
    
    @classmethod
    def get_config(cls):
        """返回飞书多维表格配置（供外部工具调用）"""
        return {
            "app_token": BITABLE_APP_TOKEN,
            "table_id": BITABLE_TABLE_ID
        }


class InventorySearcher:
    """库存搜索器"""
    
    @staticmethod
    def search(
        type_filter: str = "",
        region_filter: str = "",
        status: str = "在售"
    ) -> List[Dict]:
        """
        搜索库存 - 返回配置信息，实际查询由OpenClaw工具执行
        
        返回搜索参数，供外部调用飞书API
        """
        config = FeishuBitableConnector.get_config()
        return {
            "config": config,
            "filters": {
                "status_filter": status,
                "type_filter": type_filter,
                "region_filter": region_filter
            }
        }
    
    @staticmethod
    def get_statistics() -> Dict:
        """获取库存统计信息"""
        return {
            "message": "请使用 'feishu_bitable_app_table_record' 工具获取完整数据后统计"
        }


def format_search_results(items: List[Dict]) -> str:
    """格式化搜索结果"""
    if not items:
        return "🔍 暂无符合条件的库存\n\n建议您：\n• 放宽搜索条件\n• 换个品种或地区试试\n• 过段时间再查（库存实时更新）"
    
    lines = []
    lines.append(f"🔍 找到 {len(items)} 条库存：")
    lines.append("")
    
    for i, item in enumerate(items[:10], 1):
        item_type = item.get("type", "-")
        item_spec = item.get("spec", "-")
        item_material = item.get("material", "")
        item_price = item.get("price", 0)
        item_quantity = item.get("quantity", 0)
        item_warehouse = item.get("warehouse", "-")
        item_supplier = item.get("supplier", "-")
        item_phone = item.get("phone", "")
        
        lines.append(f"【{i}】{item_type} {item_spec} {item_material}")
        lines.append(f"    💰 价格：{item_price} 元/吨")
        lines.append(f"    📦 数量：{item_quantity} 吨")
        lines.append(f"    📍 仓库：{item_warehouse}")
        lines.append(f"    🏢 供应商：{item_supplier}")
        
        if item_phone:
            phone_display = item_phone[:3] + "****" + item_phone[-4:] if len(item_phone) > 7 else item_phone
            lines.append(f"    📞 电话：{phone_display}")
        
        lines.append("")
    
    if len(items) > 10:
        lines.append(f"... 还有 {len(items) - 10} 条，请细化搜索条件查看")
    
    lines.append("💡 回复【查看详情+序号】获取完整联系信息")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="库存搜索配置")
    parser.add_argument("--type", help="品种")
    parser.add_argument("--region", help="地区")
    
    args = parser.parse_args()
    
    result = InventorySearcher.search(
        type_filter=args.type or "",
        region_filter=args.region or ""
    )
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
