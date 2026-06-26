"""
衣橱分析模块
生成衣橱诊断报告
"""

import json
from typing import Dict, List, Any
from collections import Counter

class WardrobeAnalyzer:
    """衣橱分析器"""
    
    def __init__(self, database):
        self.db = database
    
    def generate_report(self) -> str:
        """生成衣橱诊断报告"""
        stats = self.db.get_stats()
        items = self.db.get_all_items()
        
        if not items:
            return "👗 衣橱还是空的，先添加一些单品再来分析吧！"
        
        report = []
        report.append("🌸 衣橱诊断报告")
        report.append("")
        report.append(f"📊 基础数据")
        report.append(f"   总单品数：{stats['total_items']} 件")
        report.append(f"   穿搭记录：{stats['total_outfits']} 天")
        
        # 类别分析
        report.append("")
        report.append("📦 类别分布")
        by_cat = stats.get('by_category', {})
        cat_names = {"outer": "外套", "top": "上衣", "bottom": "下装", "shoes": "鞋子", "accessory": "配饰"}
        
        for cat, name in cat_names.items():
            count = by_cat.get(cat, 0)
            bar = "█" * count + "░" * (10 - min(count, 10))
            report.append(f"   {name}：{bar} {count}件")
        
        # 平衡性诊断
        report.append("")
        report.append("💡 衣橱健康度")
        health_issues = self._check_balance(by_cat)
        if health_issues:
            for issue in health_issues:
                report.append(f"   ⚠️ {issue}")
        else:
            report.append("   ✅ 类别比例均衡")
        
        # 颜色分析
        report.append("")
        report.append("🎨 色彩分析")
        by_color = stats.get('by_color', {})
        if by_color:
            top_colors = sorted(by_color.items(), key=lambda x: x[1], reverse=True)[:5]
            for color, count in top_colors:
                report.append(f"   {color}系：{count} 件")
            
            # 颜色建议
            color_advice = self._analyze_colors(by_color)
            if color_advice:
                report.append(f"   💡 {color_advice}")
        
        # 搭配建议
        report.append("")
        report.append("👗 搭配建议")
        advice = self._generate_advice(by_cat, by_color)
        for tip in advice:
            report.append(f"   • {tip}")
        
        return "\n".join(report)
    
    def _check_balance(self, by_cat: Dict[str, int]) -> List[str]:
        """检查衣橱平衡性"""
        issues = []
        
        outer = by_cat.get('outer', 0)
        top = by_cat.get('top', 0)
        bottom = by_cat.get('bottom', 0)
        shoes = by_cat.get('shoes', 0)
        
        total = outer + top + bottom + shoes
        
        if total == 0:
            return ["衣橱空空如也，快去买衣服吧！"]
        
        # 检查比例
        if top / total < 0.3:
            issues.append("上衣偏少，建议多添置基础款")
        
        if bottom / total < 0.2:
            issues.append("下装不足，搭配选择受限")
        
        if shoes < 3:
            issues.append("鞋子太少，不同场合需要不同鞋款")
        
        if outer < 2:
            issues.append("外套不足，换季搭配受限")
        
        # 检查是否能组成完整搭配
        if top > 0 and bottom > 0 and shoes > 0:
            pass  # 能组成搭配
        else:
            issues.append("缺少核心单品，无法组成完整搭配")
        
        return issues
    
    def _analyze_colors(self, by_color: Dict[str, int]) -> str:
        """分析颜色搭配"""
        total = sum(by_color.values())
        if total == 0:
            return ""
        
        # 基础色比例
        basic_colors = ["黑色", "白色", "灰色", "米色", "卡其色"]
        basic_count = sum(by_color.get(c, 0) for c in basic_colors)
        basic_ratio = basic_count / total
        
        if basic_ratio < 0.4:
            return "基础色（黑白灰米卡其）偏少，建议多添置基础款，更易搭配"
        elif basic_ratio > 0.8:
            return "基础色充足，可以尝试添加一些彩色单品增加活力"
        
        return "颜色搭配合理，基础色与彩色比例适中"
    
    def _generate_advice(self, by_cat: Dict[str, int], by_color: Dict[str, int]) -> List[str]:
        """生成搭配建议"""
        advice = []
        
        outer = by_cat.get('outer', 0)
        top = by_cat.get('top', 0)
        bottom = by_cat.get('bottom', 0)
        
        # 基础建议
        if top >= 5 and bottom >= 3:
            advice.append("基础单品充足，可以尝试更多风格搭配")
        
        if outer >= 3:
            advice.append("外套选择丰富，适合多层叠穿")
        
        # 进阶建议
        if top + bottom >= 10:
            advice.append("单品数量充足，建议尝试'胶囊衣橱'理念，提高单品利用率")
        
        if by_cat.get('accessory', 0) < 2:
            advice.append("配饰较少，适当添加围巾、包包能提升搭配精致度")
        
        if not advice:
            advice.append("继续丰富衣橱，尝试不同风格的单品")
        
        return advice
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """获取使用统计"""
        outfits = self.db.get_outfits(limit=1000)
        
        if not outfits:
            return {"message": "还没有穿搭记录"}
        
        # 统计最爱单品
        item_counter = Counter()
        occasion_counter = Counter()
        
        for outfit in outfits:
            items = outfit.get('items', [])
            if isinstance(items, str):
                try:
                    items = json.loads(items)
                except:
                    items = []
            
            for item in items:
                item_counter[item] += 1
            
            occasion = outfit.get('occasion', '日常')
            occasion_counter[occasion] += 1
        
        return {
            "total_outfits": len(outfits),
            "most_worn": item_counter.most_common(5),
            "occasions": dict(occasion_counter.most_common())
        }
