#!/usr/bin/env python3
"""
采购需求发布与搜索模块
"""

import json
import argparse
import re
import uuid
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# 数据目录
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# 采购需求文件
PURCHASE_REQUESTS_FILE = DATA_DIR / "purchase_requests.json"

# 导入语音库存解析器（复用逻辑）
import sys
sys.path.insert(0, str(Path(__file__).parent))
from voice_inventory import VoiceInventoryParser


# ====== 数据结构定义 ======

class PurchaseRequestParser:
    """采购需求解析器"""
    
    MATERIAL_KEYWORDS = ["Q235B", "Q235", "Q355B", "Q355", "Q345B", "Q345", 
                         "HRB400E", "HRB400", "HPB300", "20#", "45#", 
                         "SPCC", "DC01", "SGCC", "DX51D+Z"]
    
    @staticmethod
    def parse_text(text: str, buyer_name: str = "") -> Optional[Dict]:
        """解析采购需求文本"""
        text_lower = text.lower().replace(' ', '')
        
        # 识别采购商
        if not buyer_name:
            match = re.search(r'我是(.{2,10})[厂公司]?', text)
            if match:
                buyer_name = match.group(1)
        
        # 识别品种
        vp = VoiceInventoryParser()
        steel_type = vp._extract_type(text)
        if not steel_type:
            return None
        
        # 识别规格
        spec = vp._extract_spec(text, steel_type)
        
        # 识别材质
        material = PurchaseRequestParser._extract_material(text) or "Q235B"
        
        # 识别数量
        quantity = PurchaseRequestParser._extract_quantity(text)
        
        # 识别价格
        price_info = PurchaseRequestParser._extract_price(text)
        
        # 识别地址
        address = PurchaseRequestParser._extract_address(text)
        
        # 识别紧急程度
        urgency = PurchaseRequestParser._extract_urgency(text)
        
        # 识别时间要求
        deadline = PurchaseRequestParser._extract_deadline(text)
        
        # 验证必需字段
        if not all([steel_type, quantity, price_info["max_price"], address]):
            return None
        
        return {
            "id": "",
            "buyer": buyer_name or "采购商",
            "type": steel_type,
            "spec": spec,
            "material": material,
            "quantity": quantity,
            "max_price": price_info["max_price"],
            "min_price": price_info.get("min_price"),
            "delivery_address": address,
            "contact": "待确认",
            "phone": "待确认",
            "urgency": urgency,
            "deadline": deadline,
            "status": "采购中",
            "publish_time": ""
        }
    
    @staticmethod
    def _extract_type(text: str) -> Optional[str]:
        vp = VoiceInventoryParser()
        return vp._extract_type(text)
    
    @staticmethod
    def _extract_spec(text: str, steel_type: str) -> str:
        vp = VoiceInventoryParser()
        return vp._extract_spec(text, steel_type)
    
    @staticmethod
    def _extract_material(text: str) -> Optional[str]:
        for material in PurchaseRequestParser.MATERIAL_KEYWORDS:
            if material in text:
                return material
        return None
    
    @staticmethod
    def _extract_quantity(text: str) -> Optional[float]:
        patterns = [
            r'买(\d+\.?\d*)\s*吨',
            r'需要(\d+\.?\d*)\s*吨',
            r'要(\d+\.?\d*)\s*吨',
            r'(\d+\.?\d*)\s*吨',
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return float(match.group(1))
        return None
    
    @staticmethod
    def _extract_price(text: str) -> Dict:
        result = {"max_price": None, "min_price": None}
        
        # 匹配各种价格表达
        patterns = [
            r'[不]*[要]*[超]*过(\d{3,5})',  # 不超过、不要超过、超过
            r'(\d{3,5})以内',  # X以内
            r'(\d{3,5})以下',  # X以下
            r'预算(\d{3,5})',  # 预算X
            r'最高(\d{3,5})',  # 最高X
            r'限价(\d{3,5})',  # 限价X
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                result["max_price"] = float(match.group(1))
                break
        
        # 匹配价格范围 "3000-4000" 或 "3000到4000"
        match = re.search(r'(\d{3,5})[-~到至](\d{3,5})', text)
        if match:
            result["min_price"] = float(match.group(1))
            result["max_price"] = float(match.group(2))
        
        # 匹配"要X元"或"要X块"
        match = re.search(r'要(\d{3,5})[的块元]', text)
        if match:
            result["max_price"] = float(match.group(1))
        
        return result
    
    @staticmethod
    def _extract_address(text: str) -> str:
        regions = ["唐山", "天津", "北京", "上海", "广州", "乐从",
                   "无锡", "杭州", "武汉", "重庆", "成都", "西安",
                   "石家庄", "邯郸", "济南", "青岛", "南京", "深圳"]
        
        for region in regions:
            if region in text:
                return region
        
        match = re.search(r'送(到|往|至)(.{2,10})', text)
        if match:
            return match.group(2)
        
        return ""
    
    @staticmethod
    def _extract_urgency(text: str) -> str:
        if "急" in text or "紧急" in text or "今天" in text:
            return "紧急"
        return "普通"
    
    @staticmethod
    def _extract_deadline(text: str) -> str:
        if "今天" in text:
            return "今天"
        elif "明天" in text:
            return "明天"
        return ""


# ====== 发布器 ======

def publish_request(request: Dict) -> bool:
    """发布采购需求"""
    try:
        request["id"] = str(uuid.uuid4())[:8]
        request["publish_time"] = datetime.now().isoformat()
        
        requests_list = _load_requests()
        requests_list.append(request)
        
        with open(PURCHASE_REQUESTS_FILE, "w", encoding="utf-8") as f:
            json.dump(requests_list, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        print(f"发布失败: {e}")
        return False


def _load_requests() -> List[Dict]:
    """加载采购需求"""
    if PURCHASE_REQUESTS_FILE.exists():
        with open(PURCHASE_REQUESTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def _search_requests(type_filter: str = "", region_filter: str = "",
                     max_budget: float = None, urgency: str = "") -> List[Dict]:
    """搜索采购需求"""
    requests_list = _load_requests()
    results = []
    
    for req in requests_list:
        # 状态筛选
        if req.get("status") != "采购中":
            continue
        
        # 品种筛选
        if type_filter and type_filter not in req.get("type", ""):
            continue
        
        # 地区筛选
        if region_filter and region_filter not in req.get("delivery_address", ""):
            continue
        
        # 预算筛选
        if max_budget is not None and req.get("max_price", 0) > max_budget:
            continue
        
        # 紧急程度筛选
        if urgency and urgency not in req.get("urgency", ""):
            continue
        
        results.append(req)
    
    # 按紧急程度和发布时间排序
    results.sort(key=lambda x: (
        x.get("urgency") != "普通",
        x.get("publish_time", "")
    ), reverse=True)
    
    return results


def _format_requests(requests: List[Dict]) -> str:
    """格式化采购需求列表"""
    if not requests:
        return "🔍 暂无采购需求\n\n💡 您可以发布采购需求，钢贸商会主动联系您！"
    
    lines = []
    lines.append(f"🔍 找到 {len(requests)} 条采购需求：")
    lines.append("")
    
    for i, req in enumerate(requests[:10], 1):
        urgency_emoji = "🔴" if req.get("urgency") == "紧急" else "🔵"
        
        lines.append(f"{urgency_emoji}【{i}】{req['type']} {req['spec']} {req['material']}")
        lines.append(f"    💰 预算：≤{req['max_price']} 元/吨")
        if req.get("min_price"):
            lines.append(f"    预算范围：{req['min_price']} ~ {req['max_price']} 元/吨")
        lines.append(f"    📦 数量：{req['quantity']} 吨")
        lines.append(f"    📍 送货：{req['delivery_address']}")
        
        if req.get("deadline"):
            lines.append(f"    ⏰ 要求：{req['deadline']}")
        lines.append(f"    🏢 采购商：{req['buyer']}")
        
        if req.get("phone") and req["phone"] != "待确认":
            phone_display = req["phone"][:3] + "****" + req["phone"][-4:] if len(req["phone"]) > 7 else req["phone"]
            lines.append(f"    📞 电话：{phone_display}")
        
        lines.append("")
    
    if len(requests) > 10:
        lines.append(f"... 还有 {len(requests) - 10} 条，请细化搜索条件查看")
    
    lines.append("💡 回复【响应+序号】联系采购商")
    lines.append("💡 回复【发布需求】发布您的采购需求")
    
    return "\n".join(lines)


# ====== 主程序 ======

def main():
    parser = argparse.ArgumentParser(description="采购需求管理")
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # publish 子命令
    publish_parser = subparsers.add_parser("publish", help="发布需求")
    publish_parser.add_argument("--text", required=True, help="需求文本")
    publish_parser.add_argument("--buyer", default="采购商", help="采购商名称")
    
    # search 子命令
    search_parser = subparsers.add_parser("search", help="搜索需求")
    search_parser.add_argument("--type", help="品种")
    search_parser.add_argument("--region", help="地区")
    search_parser.add_argument("--max-budget", type=float, help="最高预算")
    search_parser.add_argument("--urgency", help="紧急程度")
    
    # stats 子命令
    subparsers.add_parser("stats", help="需求统计")
    
    # my 子命令
    my_parser = subparsers.add_parser("my", help="我的需求")
    my_parser.add_argument("--buyer", required=True, help="采购商名称")
    
    args = parser.parse_args()
    
    if args.command == "publish":
        result = PurchaseRequestParser.parse_text(args.text, args.buyer)
        
        if result:
            if publish_request(result):
                print("✅ 采购需求已发布！")
                print(f"\n📋 需求信息：")
                print(f"品种：{result['type']} {result['spec']} {result['material']}")
                print(f"数量：{result['quantity']} 吨")
                print(f"预算：≤{result['max_price']} 元/吨")
                print(f"送货：{result['delivery_address']}")
                print(f"紧急：{result['urgency']}")
            else:
                print("❌ 发布失败")
        else:
            print("❌ 需求解析失败，请提供：")
            print("• 钢材品种")
            print("• 规格")
            print("• 数量")
            print("• 预算")
            print("• 送货地址")
    
    elif args.command == "search":
        results = _search_requests(
            type_filter=args.type or "",
            region_filter=args.region or "",
            max_budget=args.max_budget,
            urgency=args.urgency or ""
        )
        print(_format_requests(results))
    
    elif args.command == "stats":
        requests_list = _load_requests()
        
        total = len(requests_list)
        active = len([r for r in requests_list if r.get("status") == "采购中"])
        
        type_stats = {}
        for req in requests_list:
            t = req.get("type", "未知")
            type_stats[t] = type_stats.get(t, 0) + 1
        
        region_stats = {}
        for req in requests_list:
            r = req.get("delivery_address", "未知")
            region_stats[r] = region_stats.get(r, 0) + 1
        
        print("📊 采购需求统计")
        print(f"总需求数：{total}")
        print(f"采购中：{active}")
        print("\n按品种分布：")
        for t, count in sorted(type_stats.items(), key=lambda x: -x[1]):
            print(f"  {t}: {count}条")
        print("\n按地区分布：")
        for r, count in sorted(region_stats.items(), key=lambda x: -x[1]):
            print(f"  {r}: {count}条")
    
    elif args.command == "my":
        results = [r for r in _load_requests() 
                   if r.get("buyer", "") == args.buyer and r.get("status") == "采购中"]
        results.sort(key=lambda x: x.get("publish_time", ""), reverse=True)
        print(f"🏢 {args.buyer} 的采购需求（{len(results)}条）")
        print(_format_requests(results))
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
