#!/usr/bin/env python3
"""
钢材价格查询交互助手
提供地区和品种选择提示
"""

# 支持的地区列表
SUPPORTED_REGIONS = {
    "华北": ["唐山", "北京", "天津", "邯郸", "石家庄"],
    "华东": ["上海", "杭州", "南京", "无锡", "济南", "青岛"],
    "华南": ["广州", "深圳", "乐从"],
    "华中": ["武汉", "长沙"],
    "西南": ["重庆", "成都"],
    "西北": ["西安", "兰州"],
    "东北": ["沈阳", "长春", "哈尔滨"]
}

# 支持的品种列表
SUPPORTED_TYPES = {
    "建筑钢材": ["螺纹钢", "线材", "盘螺", "高线"],
    "板材": ["热轧板卷", "冷轧板卷", "中厚板", "镀锌板卷", "花纹板"],
    "型钢": ["H型钢", "角钢", "槽钢", "工字钢", "扁钢", "圆钢", "方钢"],
    "管材": ["焊管", "无缝管", "镀锌管", "方管", "矩形管"]
}

# 常见规格示例
SPEC_EXAMPLES = {
    "螺纹钢": ["Φ12-14 HRB400E", "Φ16-25 HRB400E", "Φ28-32 HRB400E"],
    "线材": ["Φ6.5 HPB300", "Φ8 HPB300", "Φ10 HPB300"],
    "高线": ["Φ6.5 HPB300", "Φ8 HPB300", "Φ10 HPB300"],
    "盘螺": ["Φ6 HRB400E", "Φ8 HRB400E", "Φ10 HRB400E"],
    "热轧板卷": ["4.75*1500*C Q235B", "3.0*1250*C Q235B", "5.75*1500*C Q355B"],
    "冷轧板卷": ["1.0*1250*C SPCC", "2.0*1250*C DC01", "0.8*1000*C SPCC"],
    "中厚板": ["20mm Q235B", "30mm Q345B", "40mm Q355B", "10mm Q235B"],
    "镀锌板卷": ["1.0*1250*C DX51D+Z", "2.0*1250*C SGCC"],
    "花纹板": ["3.0*1250*C Q235B", "4.0*1500*C Q235B"],
    "H型钢": ["200*100 Q235B", "300*150 Q235B", "400*200 Q355B", "100*100 Q235B"],
    "角钢": ["50*5 Q235B", "63*6 Q235B", "75*8 Q355B", "40*4 Q235B"],
    "槽钢": ["16# Q235B", "20# Q235B", "25# Q355B", "10# Q235B"],
    "工字钢": ["20# Q235B", "25# Q235B", "32# Q355B", "16# Q235B"],
    "扁钢": ["40*4 Q235B", "50*5 Q235B", "60*6 Q355B"],
    "圆钢": ["Φ20 Q235B", "Φ25 45#", "Φ30 Q355B"],
    "方钢": ["20*20 Q235B", "30*30 45#", "40*40 Q355B"],
    "焊管": ["Φ48*3.5 Q235B", "Φ89*4 Q235B", "Φ114*4 Q355B"],
    "无缝管": ["Φ89*4 20#", "Φ108*4.5 20#", "Φ133*5 Q355B"],
    "镀锌管": ["Φ48*3.5 Q235B", "Φ89*4 Q235B", "DN100 Q235B"],
    "方管": ["50*50*3 Q235B", "100*100*4 Q235B", "80*80*4 Q355B"],
    "矩形管": ["60*40*3 Q235B", "80*40*3 Q235B", "100*50*4 Q355B"]
}


def get_help_text() -> str:
    """获取帮助提示文本"""
    lines = []
    lines.append("📍 请告诉我您要查询的钢材信息：")
    lines.append("")
    lines.append("【地区】如：唐山、上海、广州、北京...")
    lines.append("【品种】如：螺纹钢、热轧板卷、冷轧板卷...")
    lines.append("【规格】（可选）如：Φ12-14 HRB400E")
    lines.append("")
    lines.append("示例：")
    lines.append("  • 唐山螺纹钢")
    lines.append("  • 上海热轧板卷 4.75*1500*C")
    lines.append("  • 查一下广州冷轧板卷价格")
    lines.append("")
    lines.append('回复"列表"查看所有支持的地区和品种')
    
    return "\n".join(lines)


def get_region_list() -> str:
    """获取地区列表"""
    lines = []
    lines.append("📍 支持的地区：")
    lines.append("")
    
    for region, cities in SUPPORTED_REGIONS.items():
        lines.append(f"【{region}】")
        lines.append(f"  {', '.join(cities)}")
    
    return "\n".join(lines)


def get_type_list() -> str:
    """获取品种列表"""
    lines = []
    lines.append("🔩 支持的钢材品种：")
    lines.append("")
    
    for category, types in SUPPORTED_TYPES.items():
        lines.append(f"【{category}】")
        lines.append(f"  {', '.join(types)}")
    
    return "\n".join(lines)


def get_spec_examples(steel_type: str) -> str:
    """获取规格示例"""
    specs = SPEC_EXAMPLES.get(steel_type)
    if specs:
        return f"【{steel_type}】常见规格：{', '.join(specs)}"
    return f"【{steel_type}】规格请咨询具体钢贸商"


def parse_query(text: str) -> dict:
    """
    解析用户查询文本
    
    返回：
    {
        "region": 地区,
        "type": 品种,
        "spec": 规格（可选）
    }
    """
    import re
    
    result = {"region": None, "type": None, "spec": None}
    
    # 提取地区（先匹配完整的）
    all_regions = []
    for cities in SUPPORTED_REGIONS.values():
        all_regions.extend(cities)
    
    for region in all_regions:
        if region in text:
            result["region"] = region
            break
    
    # 提取品种
    all_types = []
    for types in SUPPORTED_TYPES.values():
        all_types.extend(types)
    
    for steel_type in all_types:
        if steel_type in text:
            result["type"] = steel_type
            break
    
    # 尝试提取规格（支持希腊字母Φ和普通字符）
    spec_patterns = [
        r'[Φφ][\d\-]+(?:\.\d+)?[^\s,，]*',  # Φ12-14 HRB400E
        r'\d+\.?\d*\*\d+[^\s,，]*',  # 4.75*1500*C
        r'\d+mm[^\s,，]*',  # 20mm Q235B
        r'\d+#',  # 20#
    ]
    
    for pattern in spec_patterns:
        match = re.search(pattern, text)
        if match:
            result["spec"] = match.group(0)
            break
    
    return result


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="价格查询助手")
    parser.add_argument("--regions", action="store_true", help="显示地区列表")
    parser.add_argument("--types", action="store_true", help="显示品种列表")
    parser.add_argument("--spec", help="显示某品种的规格示例")
    parser.add_argument("--parse", help="解析查询文本")
    
    args = parser.parse_args()
    
    if args.regions:
        print(get_region_list())
    elif args.types:
        print(get_type_list())
    elif args.spec:
        print(get_spec_examples(args.spec))
    elif args.parse:
        result = parse_query(args.parse)
        print(f"解析结果: {result}")
    else:
        print(get_help_text())


if __name__ == "__main__":
    main()
