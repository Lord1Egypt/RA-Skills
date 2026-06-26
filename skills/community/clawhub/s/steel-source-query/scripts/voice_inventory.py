#!/usr/bin/env python3
"""
钢贸商库存语音录入模块
支持语音转文字后自动解析库存信息
"""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

@dataclass
class InventoryItem:
    """库存条目"""
    type: str           # 品种
    spec: str           # 规格
    material: str       # 材质（如 Q235B, Q355B）
    quantity: float     # 数量（吨）
    price: float        # 单价（元/吨）
    warehouse: str      # 仓库/地区
    supplier: str       # 供应商名称
    contact: str = ""   # 联系人
    phone: str = ""     # 电话
    status: str = "在售" # 状态：在售/已售/预留


class VoiceInventoryParser:
    """语音库存解析器"""
    
    # 品种关键词映射
    TYPE_KEYWORDS = {
        "螺纹钢": ["螺纹钢", "螺纹", "钢筋"],
        "角钢": ["角钢", "角铁"],
        "槽钢": ["槽钢", "槽铁"],
        "工字钢": ["工字钢", "工字", "工钢"],
        "H型钢": ["H型钢", "H钢", "h型钢"],
        "扁钢": ["扁钢", "扁铁"],
        "圆钢": ["圆钢", "圆铁"],
        "方钢": ["方钢"],
        "热轧板卷": ["热轧板卷", "热轧卷", "热卷"],
        "冷轧板卷": ["冷轧板卷", "冷轧卷", "冷卷"],
        "中厚板": ["中厚板", "中板", "厚板"],
        "镀锌板卷": ["镀锌板卷", "镀锌卷", "镀锌板"],
        "花纹板": ["花纹板", "花纹卷"],
        "高线": ["高线", "线材", "盘条"],
        "盘螺": ["盘螺"],
        "焊管": ["焊管", "焊接钢管"],
        "无缝管": ["无缝管", "无缝钢管"],
        "镀锌管": ["镀锌管", "镀锌钢管"],
        "方管": ["方管", "方钢管"],
        "矩形管": ["矩形管", "矩管"],
    }
    
    # 材质关键词
    MATERIAL_KEYWORDS = ["Q235B", "Q235", "Q355B", "Q355", "Q345B", "Q345", 
                         "HRB400E", "HRB400", "HPB300", "20#", "45#", 
                         "SPCC", "DC01", "SGCC", "DX51D+Z"]
    
    # 材质别名映射（语音中可能出现的变体）
    MATERIAL_ALIASES = {
        "q235b": "Q235B",
        "q235": "Q235B",
        "q355b": "Q355B",
        "q355": "Q355B",
        "hrb400e": "HRB400E",
        "hrb400": "HRB400",
        "hpb300": "HPB300",
    }
    
    # 规格模式
    SPEC_PATTERNS = [
        r'(Φ|φ)?(\d+)(-|~)(\d+)',  # Φ12-14 或 12-14
        r'(\d+\.?\d*)\*(\d+\.?\d*)\*C',  # 4.75*1500*C
        r'(\d+\.?\d*)\*(\d+\.?\d*)\*(\d+\.?\d*)',  # 50*50*3
        r'(\d+)#',  # 20#
        r'(\d+)mm',  # 20mm
    ]
    
    @staticmethod
    def parse_voice_text(text: str, supplier_name: str = "") -> Optional[InventoryItem]:
        """
        解析语音转文字后的库存信息
        
        示例输入：
        - "我这有角钢50乘5的Q235B，有50吨，今天卖3850"
        - "槽钢20号Q235B，30吨，价格3900"
        - "螺纹钢12到14的HRB400E，100吨，3850一吨"
        
        Returns:
            InventoryItem 或 None
        """
        text = text.lower().replace(' ', '')
        
        # 1. 识别品种
        steel_type = VoiceInventoryParser._extract_type(text)
        if not steel_type:
            return None
        
        # 2. 识别材质
        material = VoiceInventoryParser._extract_material(text) or "Q235B"
        
        # 3. 识别规格
        spec = VoiceInventoryParser._extract_spec(text, steel_type)
        
        # 4. 识别数量（吨）
        quantity = VoiceInventoryParser._extract_quantity(text)
        
        # 5. 识别价格
        price = VoiceInventoryParser._extract_price(text)
        
        # 6. 识别地区/仓库
        warehouse = VoiceInventoryParser._extract_warehouse(text)
        
        if not all([steel_type, spec, quantity, price]):
            return None
        
        return InventoryItem(
            type=steel_type,
            spec=spec,
            material=material,
            quantity=quantity,
            price=price,
            warehouse=warehouse,
            supplier=supplier_name
        )
    
    @staticmethod
    def _extract_type(text: str) -> Optional[str]:
        """提取品种"""
        for type_name, keywords in VoiceInventoryParser.TYPE_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text:
                    return type_name
        return None
    
    @staticmethod
    def _extract_material(text: str) -> Optional[str]:
        """提取材质"""
        text_lower = text.lower()
        
        # 先检查别名映射
        for alias, standard in VoiceInventoryParser.MATERIAL_ALIASES.items():
            if alias in text_lower:
                return standard
        
        # 再检查标准关键词
        for material in VoiceInventoryParser.MATERIAL_KEYWORDS:
            if material.lower() in text_lower:
                return material
        return None
    
    @staticmethod
    def _extract_spec(text: str, steel_type: str) -> str:
        """提取规格"""
        # 根据品种类型提取不同格式的规格
        
        # 螺纹钢/线材：Φ12-14 或 12到14
        if steel_type in ["螺纹钢", "线材", "高线", "盘螺", "圆钢"]:
            # 支持 - ~ 到 至
            match = re.search(r'(Φ|φ)?(\d+)[\-~到至](\d+)', text)
            if match:
                return f"Φ{match.group(2)}-{match.group(3)}"
            match = re.search(r'(Φ|φ)(\d+)', text)
            if match:
                return f"Φ{match.group(2)}"
        
        # 角钢/扁钢：50*5 或 50乘5
        if steel_type in ["角钢", "扁钢"]:
            # 匹配 * x X 乘 乘以
            match = re.search(r'(\d+)[\*xX乘](\d+)', text)
            if match:
                return f"{match.group(1)}*{match.group(2)}"
        
        # 槽钢/工字钢：20#
        if steel_type in ["槽钢", "工字钢"]:
            match = re.search(r'(\d+)\s*号', text)
            if match:
                return f"{match.group(1)}#"
            match = re.search(r'(\d+)#', text)
            if match:
                return f"{match.group(1)}#"
        
        # H型钢：200*100 或 200乘100
        if steel_type == "H型钢":
            match = re.search(r'(\d+)[\*xX乘](\d+)', text)
            if match:
                return f"{match.group(1)}*{match.group(2)}"
        
        # 板卷：4.75*1500*C 或 4.75乘1500乘C 或 4.75乘1500
        if "板卷" in steel_type or "板" in steel_type:
            # 尝试匹配带C的格式
            match = re.search(r'(\d+\.?\d*)[\*xX乘](\d+\.?\d*)[\*xX乘]?C', text)
            if match:
                return f"{match.group(1)}*{match.group(2)}*C"
            # 尝试匹配不带C的格式（如"4.75乘1500"）
            match = re.search(r'(\d+\.?\d*)[\*xX乘](\d+\.?\d*)', text)
            if match:
                return f"{match.group(1)}*{match.group(2)}*C"
        
        # 中厚板：20mm
        if steel_type == "中厚板":
            match = re.search(r'(\d+)mm', text)
            if match:
                return f"{match.group(1)}mm"
        
        # 管材：Φ48*3.5 或 50*50*3
        if "管" in steel_type:
            match = re.search(r'(Φ|φ)?(\d+\.?\d*)[\*xX](\d+\.?\d*)', text)
            if match:
                if match.group(1):
                    return f"Φ{match.group(2)}*{match.group(3)}"
                else:
                    return f"{match.group(2)}*{match.group(3)}"
        
        # 方钢：20*20
        if steel_type == "方钢":
            match = re.search(r'(\d+)[\*xX乘](\d+)', text)
            if match:
                return f"{match.group(1)}*{match.group(2)}"
        
        # 圆钢：Φ20
        if steel_type == "圆钢":
            match = re.search(r'(Φ|φ)(\d+)', text)
            if match:
                return f"Φ{match.group(2)}"
        
        return ""
    
    @staticmethod
    def _extract_quantity(text: str) -> Optional[float]:
        """提取数量"""
        # 匹配 "50吨"、"100吨左右"、"大概200吨"
        patterns = [
            r'(\d+\.?\d*)\s*吨',
            r'(\d+\.?\d*)\s*t',
            r'库存(\d+\.?\d*)',
            r'有(\d+\.?\d*)',
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return float(match.group(1))
        return None
    
    @staticmethod
    def _extract_price(text: str) -> Optional[float]:
        """提取价格"""
        # 匹配各种价格表达方式
        patterns = [
            r'(?:价格|卖|报|单价)?[:：\s]*(\d{3,5})(?:元|块)?(?:一吨|每吨|/吨)?',
            r'(\d{3,5})\s*(?:元|块)?\s*(?:一吨|每吨|/吨)',
            r'今天[:：\s]*(\d{3,5})',
            r'(?:卖|报|价格)[:：\s]*(\d{3,5})',
            r'(\d{3,5})(?:元|块)?$',  # 结尾的数字
        ]
        
        # 先尝试找明确的"元"或价格关键词附近的数字
        match = re.search(r'(\d{3,5})(?:元|块)', text)
        if match:
            price = int(match.group(1))
            if 2000 <= price <= 10000:
                return price
        
        # 找"卖"、"报"后面的数字
        match = re.search(r'(?:卖|报|价格)[:：]?\s*(\d{3,5})', text)
        if match:
            price = int(match.group(1))
            if 2000 <= price <= 10000:
                return price
        
        # 找"元"或"块"前面的数字（明确的价格标识）
        match = re.search(r'(\d{3,5})(?:元|块)', text)
        if match:
            price = int(match.group(1))
            if 2000 <= price <= 10000:
                return price
        
        # 找"一吨"前面的数字（如"3850一吨"）
        match = re.search(r'(\d{3,5})一吨', text)
        if match:
            price = int(match.group(1))
            if 2000 <= price <= 10000:
                return price
        
        # 找结尾的数字（可能是价格）
        match = re.search(r'(\d{3,5})(?:元|块)?$', text)
        if match:
            price = int(match.group(1))
            if 2000 <= price <= 10000:
                return price
        
        return None
    
    @staticmethod
    def _extract_warehouse(text: str) -> str:
        """提取仓库/地区"""
        # 常见地区关键词
        regions = ["唐山", "天津", "北京", "上海", "广州", "乐从", 
                   "无锡", "杭州", "武汉", "重庆", "成都", "西安"]
        for region in regions:
            if region in text:
                return region
        
        # 匹配 "在唐山"、"仓库在"、"现货在"
        match = re.search(r'(?:在|仓库|现货|存放)[\s于]?([\u4e00-\u9fa5]{2,4})', text)
        if match:
            return match.group(1)
        
        return ""


class InventorySearch:
    """库存搜索器"""
    
    @staticmethod
    def search(inventory_list: List[InventoryItem], 
               type_filter: str = "",
               spec_filter: str = "",
               region_filter: str = "",
               max_price: float = None) -> List[InventoryItem]:
        """搜索库存"""
        results = inventory_list
        
        if type_filter:
            results = [item for item in results if type_filter in item.type]
        
        if spec_filter:
            results = [item for item in results if spec_filter in item.spec]
        
        if region_filter:
            results = [item for item in results if region_filter in item.warehouse]
        
        if max_price:
            results = [item for item in results if item.price <= max_price]
        
        return results
    
    @staticmethod
    def format_results(items: List[InventoryItem]) -> str:
        """格式化搜索结果"""
        if not items:
            return "暂无符合条件的库存"
        
        lines = []
        lines.append(f"找到 {len(items)} 条库存：")
        lines.append("")
        
        for item in items:
            lines.append(f"【{item.type} {item.spec} {item.material}】")
            lines.append(f"  价格：{item.price} 元/吨")
            lines.append(f"  数量：{item.quantity} 吨")
            lines.append(f"  仓库：{item.warehouse}")
            lines.append(f"  供应商：{item.supplier}")
            if item.contact:
                lines.append(f"  联系人：{item.contact}")
            if item.phone:
                lines.append(f"  电话：{item.phone}")
            lines.append("")
        
        return "\n".join(lines)


# 测试
if __name__ == "__main__":
    parser = VoiceInventoryParser()
    
    test_cases = [
        "我这有角钢50乘5的Q235B，有50吨，今天卖3850",
        "槽钢20号Q235B，30吨，价格3900",
        "螺纹钢12到14的HRB400E，100吨，3850一吨",
        "热轧板卷4.75乘1500的Q235B，200吨，3650",
        "H型钢200乘100的Q235B，80吨，3750",
    ]
    
    print("语音库存解析测试：\n")
    for text in test_cases:
        print(f"输入: {text}")
        result = parser.parse_voice_text(text, supplier_name="测试钢贸商")
        if result:
            print(f"✓ 解析成功: {result.type} {result.spec} {result.material}, "
                  f"{result.quantity}吨, {result.price}元/吨, 仓库:{result.warehouse}")
        else:
            print("✗ 解析失败")
        print()
