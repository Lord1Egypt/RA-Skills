#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
需求真实性验证器 v1.1.0 - 完整版
实现六维度完整验证
"""

import sys
import json
import csv
import argparse
import yaml
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from pathlib import Path

class RequirementValidator:
    """需求真实性验证器 - 完整版"""
    
    def __init__(self, config_path: str = None):
        """
        初始化验证器
        
        Args:
            config_path: 配置文件路径
        """
        # 默认权重
        self.weights = {
            'consistency': 0.30,      # 用户一致性
            'frequency': 0.20,        # 需求频次
            'impact': 0.15,           # 影响面
            'competitor': 0.10,       # 竞品覆盖
            'alternative': 0.15,      # 替代方案
            'roi': 0.10              # ROI
        }
        
        # 加载配置
        if config_path and Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                if config and 'weights' in config:
                    self.weights.update(config['weights'])
    
    def validate(
        self,
        feedback_data: List[Dict],
        behavior_data: List[Dict] = None,
        requirement_keywords: List[str] = None,
        competitor_data: Dict = None
    ) -> Dict[str, Any]:
        """
        完整验证需求
        
        Args:
            feedback_data: 用户反馈数据
            behavior_data: 用户行为数据（可选）
            requirement_keywords: 需求关键词
            competitor_data: 竞品数据（可选）
            
        Returns:
            完整验证结果
        """
        if not requirement_keywords:
            requirement_keywords = []
        
        # 1. 筛选相关反馈
        relevant_feedbacks = self._filter_relevant_feedbacks(
            feedback_data, 
            requirement_keywords
        )
        
        # 2. 计算各维度得分
        dimensions = {}
        
        # 用户一致性验证
        if behavior_data:
            dimensions['consistency'] = self._validate_consistency(
                relevant_feedbacks, 
                behavior_data
            )
        else:
            # 如果没有行为数据，基于反馈质量推断
            dimensions['consistency'] = self._infer_consistency(relevant_feedbacks)
        
        # 需求频次验证
        dimensions['frequency'] = self._validate_frequency(relevant_feedbacks)
        
        # 影响面验证
        dimensions['impact'] = self._validate_impact(relevant_feedbacks)
        
        # 竞品覆盖验证
        if competitor_data:
            dimensions['competitor'] = self._validate_competitor(competitor_data)
        else:
            dimensions['competitor'] = 50.0  # 默认中等
        
        # 替代方案验证（基于反馈内容分析）
        dimensions['alternative'] = self._validate_alternative(relevant_feedbacks)
        
        # ROI评估
        dimensions['roi'] = self._validate_roi(relevant_feedbacks)
        
        # 3. 综合评分
        total_score = sum(
            score * self.weights[dim] 
            for dim, score in dimensions.items()
        )
        
        # 4. 生成详细分析
        analysis = self._generate_analysis(
            dimensions,
            relevant_feedbacks,
            behavior_data,
            competitor_data
        )
        
        return {
            'score': total_score,
            'level': self._get_level(total_score),
            'dimensions': dimensions,
            'feedback_count': len(relevant_feedbacks),
            'total_feedback': len(feedback_data),
            'analysis': analysis,
            'recommendation': self._get_recommendation(total_score, dimensions)
        }
    
    def _filter_relevant_feedbacks(
        self,
        feedback_data: List[Dict],
        keywords: List[str]
    ) -> List[Dict]:
        """筛选相关反馈"""
        if not keywords:
            return feedback_data
        
        relevant = []
        for feedback in feedback_data:
            content = feedback.get('content', '')
            if any(kw.lower() in content.lower() for kw in keywords):
                relevant.append(feedback)
        
        return relevant
    
    def _validate_consistency(
        self,
        feedbacks: List[Dict],
        behaviors: List[Dict]
    ) -> float:
        """
        验证用户一致性
        对比用户说的和实际做的
        """
        if not feedbacks or not behaviors:
            return 50.0
        
        # 提取反馈用户
        feedback_users = set()
        for f in feedbacks:
            user_id = f.get('user_id') or f.get('userId') or f.get('user')
            if user_id:
                feedback_users.add(str(user_id))
        
        # 提取行为用户
        behavior_users = set()
        for b in behaviors:
            user_id = b.get('user_id') or b.get('userId') or b.get('user')
            if user_id:
                behavior_users.add(str(user_id))
        
        # 计算一致性
        if feedback_users:
            consistent_users = feedback_users & behavior_users
            consistency_rate = len(consistent_users) / len(feedback_users)
            return consistency_rate * 100
        
        return 50.0
    
    def _infer_consistency(self, feedbacks: List[Dict]) -> float:
        """
        基于反馈质量推断一致性
        当没有行为数据时使用
        """
        if not feedbacks:
            return 50.0
        
        # 分析反馈质量
        high_quality_count = 0
        for feedback in feedbacks:
            content = feedback.get('content', '')
            # 高质量反馈的特征：具体、详细、有场景描述
            if len(content) > 50 and any(word in content for word in ['场景', '使用', '需要', '希望']):
                high_quality_count += 1
        
        quality_rate = high_quality_count / len(feedbacks)
        return 50 + quality_rate * 30  # 50-80分范围
    
    def _validate_frequency(self, feedbacks: List[Dict]) -> float:
        """验证需求频次"""
        count = len(feedbacks)
        
        if count >= 100:
            return 95.0
        elif count >= 50:
            return 85.0
        elif count >= 20:
            return 75.0
        elif count >= 10:
            return 65.0
        elif count >= 5:
            return 55.0
        elif count >= 2:
            return 45.0
        else:
            return 30.0
    
    def _validate_impact(self, feedbacks: List[Dict]) -> float:
        """验证影响面"""
        if not feedbacks:
            return 0.0
        
        # 统计用户数
        users = set()
        for f in feedbacks:
            user_id = f.get('user_id') or f.get('userId') or f.get('user')
            if user_id:
                users.add(str(user_id))
        
        user_count = len(users)
        
        # 影响面评分
        if user_count >= 100:
            return 90.0
        elif user_count >= 50:
            return 80.0
        elif user_count >= 20:
            return 70.0
        elif user_count >= 10:
            return 60.0
        elif user_count >= 5:
            return 50.0
        else:
            return 40.0
    
    def _validate_competitor(self, competitor_data: Dict) -> float:
        """验证竞品覆盖"""
        if not competitor_data or 'competitors' not in competitor_data:
            return 50.0
        
        competitors = competitor_data['competitors']
        if not competitors:
            return 50.0
        
        # 计算覆盖率
        has_feature_count = sum(
            1 for c in competitors 
            if c.get('has_feature') or c.get('hasFeature')
        )
        
        coverage_rate = has_feature_count / len(competitors)
        
        # 覆盖率高说明是标准功能
        if coverage_rate >= 0.8:
            return 85.0
        elif coverage_rate >= 0.6:
            return 75.0
        elif coverage_rate >= 0.4:
            return 65.0
        else:
            return 55.0
    
    def _validate_alternative(self, feedbacks: List[Dict]) -> float:
        """
        验证替代方案
        分析反馈中是否提到现有替代方案
        """
        if not feedbacks:
            return 50.0
        
        # 检测是否提到替代方案
        alternative_keywords = [
            '暂时', '目前', '现在', '用', '代替', '替代',
            '已经', '可以', '能够', '勉强'
        ]
        
        has_alternative_count = 0
        for feedback in feedbacks:
            content = feedback.get('content', '')
            if any(kw in content for kw in alternative_keywords):
                has_alternative_count += 1
        
        # 如果很多用户提到替代方案，说明需求紧迫性降低
        alternative_rate = has_alternative_count / len(feedbacks)
        
        if alternative_rate > 0.5:
            return 50.0  # 有替代方案，紧迫性低
        elif alternative_rate > 0.2:
            return 65.0  # 部分有替代方案
        else:
            return 80.0  # 没有替代方案，需求真实
    
    def _validate_roi(self, feedbacks: List[Dict]) -> float:
        """
        验证ROI
        基于反馈强度和用户价值推断
        """
        if not feedbacks:
            return 30.0
        
        # 分析反馈强度
        strong_keywords = ['强烈', '迫切', '必须', '刚需', '核心', '重要']
        strong_count = 0
        
        for feedback in feedbacks:
            content = feedback.get('content', '')
            if any(kw in content for kw in strong_keywords):
                strong_count += 1
        
        # 计算ROI得分
        if strong_count > 0:
            strength_rate = strong_count / len(feedbacks)
            return 50 + strength_rate * 40  # 50-90分范围
        
        return 55.0
    
    def _generate_analysis(
        self,
        dimensions: Dict[str, float],
        feedbacks: List[Dict],
        behaviors: List[Dict],
        competitors: Dict
    ) -> Dict[str, Any]:
        """生成详细分析"""
        analysis = {}
        
        # 一致性分析
        consistency = dimensions['consistency']
        if consistency >= 70:
            analysis['consistency'] = "用户反馈与实际行为高度一致，需求真实可靠"
        elif consistency >= 50:
            analysis['consistency'] = "用户反馈与实际行为基本一致，需求较为真实"
        else:
            analysis['consistency'] = "用户反馈与实际行为存在差异，需要进一步验证"
        
        # 频次分析
        frequency = dimensions['frequency']
        count = len(feedbacks)
        if frequency >= 75:
            analysis['frequency'] = f"反馈人数较多({count}人)，需求具有普遍性"
        elif frequency >= 55:
            analysis['frequency'] = f"反馈人数适中({count}人)，需求具有一定代表性"
        else:
            analysis['frequency'] = f"反馈人数较少({count}人)，需求可能只是个别需求"
        
        # 影响面分析
        impact = dimensions['impact']
        if impact >= 70:
            analysis['impact'] = "影响面较广，涉及较多核心用户"
        elif impact >= 50:
            analysis['impact'] = "影响面适中，需要评估优先级"
        else:
            analysis['impact'] = "影响面较小，优先级可适当降低"
        
        return analysis
    
    def _get_level(self, score: float) -> str:
        """获取等级"""
        if score >= 80:
            return 'high'
        elif score >= 60:
            return 'medium_high'
        elif score >= 40:
            return 'medium'
        elif score >= 20:
            return 'low'
        else:
            return 'fake'
    
    def _get_recommendation(self, score: float, dimensions: Dict) -> str:
        """生成建议"""
        recommendations = []
        
        # 总体建议
        if score >= 80:
            recommendations.append("✅ 高真实需求，强烈建议实现")
        elif score >= 60:
            recommendations.append("⚠️ 中高真实需求，建议实现")
        elif score >= 40:
            recommendations.append("⚠️ 中等真实需求，需要更多验证")
        elif score >= 20:
            recommendations.append("⚠️ 低真实需求，暂不推荐")
        else:
            recommendations.append("❌ 伪需求，不建议实现")
        
        # 具体建议
        if dimensions.get('consistency', 0) < 50:
            recommendations.append("💡 用户一致性较低，建议访谈验证实际需求")
        
        if dimensions.get('frequency', 0) < 50:
            recommendations.append("💡 反馈人数较少，建议扩大调研范围")
        
        if dimensions.get('alternative', 0) < 60:
            recommendations.append("💡 存在替代方案，建议先优化现有功能")
        
        return '\n'.join(recommendations)
    
    def generate_report(self, result: Dict, requirement: str) -> str:
        """生成完整验证报告"""
        dims = result['dimensions']
        
        report = f"""# 需求验证报告

## 基本信息
- **需求**: {requirement}
- **验证时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **真实性评分**: {result['score']:.1f}/100

## 综合评级
{self._get_level_emoji(result['score'])} {self._get_level_text(result['level'])}

---

## 验证详情

### 1️⃣ 用户一致性（权重 30%）
**得分**: {dims['consistency']:.1f}/100

{result['analysis'].get('consistency', '')}

### 2️⃣ 需求频次（权重 20%）
**得分**: {dims['frequency']:.1f}/100

{result['analysis'].get('frequency', '')}

### 3️⃣ 影响面（权重 15%）
**得分**: {dims['impact']:.1f}/100

{result['analysis'].get('impact', '')}

### 4️⃣ 竞品覆盖（权重 10%）
**得分**: {dims['competitor']:.1f}/100

### 5️⃣ 替代方案（权重 15%）
**得分**: {dims['alternative']:.1f}/100

### 6️⃣ ROI评估（权重 10%）
**得分**: {dims['roi']:.1f}/100

---

## 决策建议

{result['recommendation']}

---

## 数据统计

- 相关反馈: {result['feedback_count']} 条
- 总反馈量: {result['total_feedback']} 条
- 关键词匹配率: {result['feedback_count']/result['total_feedback']*100:.1f}%

---

*Generated by Requirement Validator v1.1.0*
"""
        return report
    
    def _get_level_emoji(self, score: float) -> str:
        """获取等级emoji"""
        if score >= 80:
            return "⭐⭐⭐⭐⭐"
        elif score >= 60:
            return "⭐⭐⭐⭐"
        elif score >= 40:
            return "⭐⭐⭐"
        elif score >= 20:
            return "⭐⭐"
        else:
            return "⭐"
    
    def _get_level_text(self, level: str) -> str:
        """获取等级文本"""
        texts = {
            'high': '高真实',
            'medium_high': '中高真实',
            'medium': '中等真实',
            'low': '低真实',
            'fake': '伪需求'
        }
        return texts.get(level, '未知')


def load_data(file_path: str) -> List[Dict]:
    """加载数据文件"""
    path = Path(file_path)
    
    if path.suffix == '.csv':
        data = []
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(dict(row))
        return data
    
    elif path.suffix == '.json':
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    else:
        raise ValueError(f"不支持的文件格式: {path.suffix}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='需求真实性验证器 v1.1.0')
    parser.add_argument('--file', required=True, help='数据文件路径（CSV/JSON）')
    parser.add_argument('--behavior', help='行为数据文件路径（可选）')
    parser.add_argument('--requirement', required=True, help='需求名称')
    parser.add_argument('--keywords', help='关键词（逗号分隔）')
    parser.add_argument('--config', help='配置文件路径')
    parser.add_argument('--output', help='输出文件路径')
    
    args = parser.parse_args()
    
    # 解析关键词
    if args.keywords:
        keywords = [kw.strip() for kw in args.keywords.split(',')]
    else:
        keywords = [args.requirement]
    
    # 加载数据
    print(f"📂 加载数据: {args.file}")
    feedback_data = load_data(args.file)
    print(f"✅ 加载 {len(feedback_data)} 条反馈数据")
    
    # 加载行为数据（可选）
    behavior_data = None
    if args.behavior:
        print(f"📂 加载行为数据: {args.behavior}")
        behavior_data = load_data(args.behavior)
        print(f"✅ 加载 {len(behavior_data)} 条行为数据")
    
    # 初始化验证器
    validator = RequirementValidator(args.config)
    
    # 验证需求
    print(f"\n🔬 开始验证: {args.requirement}")
    result = validator.validate(
        feedback_data=feedback_data,
        behavior_data=behavior_data,
        requirement_keywords=keywords
    )
    
    # 生成报告
    report = validator.generate_report(result, args.requirement)
    
    # 输出
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n✅ 验证完成！")
        print(f"📄 报告已保存到: {args.output}")
    else:
        print("\n" + "="*60)
        print(report)
    
    print(f"\n📊 评分: {result['score']:.1f}/100")


if __name__ == '__main__':
    main()
