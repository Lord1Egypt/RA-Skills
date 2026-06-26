#!/usr/bin/env python3
"""
WhatsApp私域运营规划器 - Level 2
WhatsApp Private Domain Operations Planner

功能：
- score: 私域运营评分（获客/激活/留存/变现/推荐 5维）
- journey: 客户旅程设计
- templates: 消息模板建议

Author: WhatsApp Ops Team
Version: 1.0.0
"""

import sys
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class OpsLevel(Enum):
    """运营等级"""
    EXPERT = "专家级"
    ADVANCED = "进阶级"
    INTERMEDIATE = "中级"
    BEGINNER = "初级"
    STARTER = "入门级"


@dataclass
class OpsDimension:
    """运营维度"""
    dimension: str
    score: float
    metrics: Dict[str, Any] = field(default_factory=dict)
    findings: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


@dataclass
class OpsReport:
    """运营报告"""
    overall_score: float
    ops_level: OpsLevel
    dimensions: List[OpsDimension]
    journey_map: List[Dict]
    message_templates: List[Dict]
    improvement_plan: List[str]


class WhatsAppOpsPlanner:
    """WhatsApp私域运营规划器"""
    
    DIMENSIONS = [
        {"id": "acquisition", "name": "获客", "weight": 0.20},
        {"id": "activation", "name": "激活", "weight": 0.15},
        {"id": "retention", "name": "留存", "weight": 0.25},
        {"id": "monetization", "name": "变现", "weight": 0.25},
        {"id": "referral", "name": "推荐", "weight": 0.15}
    ]
    
    JOURNEY_STAGES = [
        "awareness",      # 认知
        "interest",       # 兴趣
        "consideration",  # 考虑
        "purchase",       # 购买
        "post_purchase",  # 购买后
        "advocacy"        # 推荐
    ]
    
    def __init__(self):
        self.current_report: Optional[OpsReport] = None
    
    def assess_dimension(self, dim_id: str, metrics: Dict) -> OpsDimension:
        """评估单个维度"""
        dim_config = next((d for d in self.DIMENSIONS if d["id"] == dim_id), None)
        if not dim_config:
            return OpsDimension(dimension=dim_id, score=50)
        
        dim_name = dim_config["name"]
        score = 50
        findings = []
        recommendations = []
        
        if dim_id == "acquisition":
            score, findings, recommendations = self._assess_acquisition(metrics)
        elif dim_id == "activation":
            score, findings, recommendations = self._assess_activation(metrics)
        elif dim_id == "retention":
            score, findings, recommendations = self._assess_retention(metrics)
        elif dim_id == "monetization":
            score, findings, recommendations = self._assess_monetization(metrics)
        elif dim_id == "referral":
            score, findings, recommendations = self._assess_referral(metrics)
        
        return OpsDimension(
            dimension=dim_name,
            score=round(score, 1),
            metrics=metrics,
            findings=findings[:3],
            recommendations=recommendations[:3]
        )
    
    def _assess_acquisition(self, metrics: Dict) -> tuple:
        """评估获客维度"""
        score = 50
        findings = []
        recommendations = []
        
        # 获客渠道数
        channels = metrics.get("channel_count", 0)
        if channels >= 5:
            score += 15
            findings.append(f"多渠道获客，覆盖{channels}个渠道")
        elif channels >= 3:
            score += 10
            findings.append("已建立基础获客渠道")
        else:
            recommendations.append("建议拓展更多获客渠道")
        
        # 获客成本
        cac = metrics.get("cac", 0)
        if cac and cac <= 10:
            score += 20
            findings.append(f"获客成本低，${cac}/人")
        elif cac and cac <= 30:
            score += 10
            findings.append(f"获客成本可接受，${cac}/人")
        else:
            recommendations.append("优化获客成本")
        
        # 私域导入率
        import_rate = metrics.get("private_import_rate", 0)
        if import_rate >= 0.3:
            score += 15
            findings.append(f"私域导入率高，{import_rate*100:.1f}%")
        elif import_rate >= 0.1:
            score += 5
        
        return score, findings, recommendations
    
    def _assess_activation(self, metrics: Dict) -> tuple:
        """评估激活维度"""
        score = 50
        findings = []
        recommendations = []
        
        # 首次回复率
        reply_rate = metrics.get("first_reply_rate", 0)
        if reply_rate >= 0.7:
            score += 25
            findings.append(f"首次回复率优秀，{reply_rate*100:.1f}%")
        elif reply_rate >= 0.5:
            score += 15
            findings.append(f"首次回复率良好，{reply_rate*100:.1f}%")
        else:
            recommendations.append("提升首次回复率和互动率")
        
        # 消息打开率
        open_rate = metrics.get("message_open_rate", 0)
        if open_rate >= 0.6:
            score += 15
            findings.append(f"消息打开率高，{open_rate*100:.1f}%")
        elif open_rate >= 0.4:
            score += 10
        else:
            recommendations.append("优化消息标题提升打开率")
        
        # 互动深度
        interaction_depth = metrics.get("interaction_depth", 0)
        if interaction_depth >= 3:
            score += 10
            findings.append("用户互动深度好")
        
        return score, findings, recommendations
    
    def _assess_retention(self, metrics: Dict) -> tuple:
        """评估留存维度"""
        score = 50
        findings = []
        recommendations = []
        
        # 消息送达率
        delivery_rate = metrics.get("delivery_rate", 0)
        if delivery_rate >= 0.95:
            score += 20
            findings.append(f"送达率高，{delivery_rate*100:.1f}%")
        elif delivery_rate >= 0.85:
            score += 10
        else:
            recommendations.append("排查送达率问题")
        
        # 举报率
        report_rate = metrics.get("report_rate", 1)
        if report_rate <= 0.01:
            score += 15
            findings.append("举报率极低，账号健康")
        elif report_rate <= 0.03:
            score += 5
        else:
            score -= 20
            recommendations.append("举报率偏高，需优化发送策略")
        
        # 用户流失率
        churn_rate = metrics.get("churn_rate", 1)
        if churn_rate <= 0.1:
            score += 15
            findings.append(f"用户留存好，月流失率{churn_rate*100:.1f}%")
        elif churn_rate <= 0.2:
            score += 5
        else:
            recommendations.append("关注用户流失问题")
        
        return score, findings, recommendations
    
    def _assess_monetization(self, metrics: Dict) -> tuple:
        """评估变现维度"""
        score = 50
        findings = []
        recommendations = []
        
        # 转化率
        cvr = metrics.get("conversion_rate", 0)
        if cvr >= 0.1:
            score += 25
            findings.append(f"转化率优秀，{cvr*100:.1f}%")
        elif cvr >= 0.05:
            score += 15
            findings.append(f"转化率良好，{cvr*100:.1f}%")
        else:
            recommendations.append("提升私域转化策略")
        
        # 客单价
        aov = metrics.get("average_order_value", 0)
        if aov >= 100:
            score += 15
            findings.append(f"客单价高，${aov}")
        elif aov >= 50:
            score += 10
        else:
            recommendations.append("考虑提升客单价")
        
        # 复购率
        repurchase_rate = metrics.get("repurchase_rate", 0)
        if repurchase_rate >= 0.3:
            score += 10
            findings.append(f"复购率良好，{repurchase_rate*100:.1f}%")
        
        return score, findings, recommendations
    
    def _assess_referral(self, metrics: Dict) -> tuple:
        """评估推荐维度"""
        score = 50
        findings = []
        recommendations = []
        
        # 推荐率
        referral_rate = metrics.get("referral_rate", 0)
        if referral_rate >= 0.15:
            score += 25
            findings.append(f"推荐率高，{referral_rate*100:.1f}%")
        elif referral_rate >= 0.05:
            score += 15
            findings.append(f"推荐率可接受，{referral_rate*100:.1f}%")
        else:
            recommendations.append("设计推荐奖励机制")
        
        # NPS评分
        nps = metrics.get("nps_score", 0)
        if nps >= 50:
            score += 15
            findings.append(f"NPS优秀，{nps}")
        elif nps >= 30:
            score += 10
        else:
            recommendations.append("提升客户满意度")
        
        # 口碑传播
        viral_coefficient = metrics.get("viral_coefficient", 0)
        if viral_coefficient >= 1.5:
            score += 10
            findings.append("具有口碑传播效应")
        
        return score, findings, recommendations
    
    def calculate_overall_score(self, dimensions: List[OpsDimension]) -> float:
        """计算综合评分"""
        total = 0
        for dim in dimensions:
            dim_config = next((d for d in self.DIMENSIONS if d["name"] == dim.dimension), None)
            weight = dim_config["weight"] if dim_config else 0.2
            total += dim.score * weight
        return round(total, 1)
    
    def get_ops_level(self, score: float) -> OpsLevel:
        """确定运营等级"""
        if score >= 85:
            return OpsLevel.EXPERT
        elif score >= 70:
            return OpsLevel.ADVANCED
        elif score >= 55:
            return OpsLevel.INTERMEDIATE
        elif score >= 40:
            return OpsLevel.BEGINNER
        else:
            return OpsLevel.STARTER
    
    def score(self, metrics: Dict) -> OpsReport:
        """执行完整评分"""
        dimensions = []
        
        for dim_config in self.DIMENSIONS:
            dim_metrics = metrics.get(dim_config["id"], {})
            dim = self.assess_dimension(dim_config["id"], dim_metrics)
            dimensions.append(dim)
        
        overall_score = self.calculate_overall_score(dimensions)
        ops_level = self.get_ops_level(overall_score)
        
        # 生成旅程地图
        journey_map = self.design_journey_map()
        
        # 生成消息模板
        templates = self.generate_templates()
        
        # 改进计划
        improvement_plan = self.generate_improvement_plan(dimensions)
        
        self.current_report = OpsReport(
            overall_score=overall_score,
            ops_level=ops_level,
            dimensions=dimensions,
            journey_map=journey_map,
            message_templates=templates,
            improvement_plan=improvement_plan
        )
        
        return self.current_report
    
    def design_journey_map(self) -> List[Dict]:
        """设计客户旅程"""
        return [
            {
                "stage": "awareness",
                "name": "认知阶段",
                "touchpoints": ["社交媒体", "口碑传播", "广告触达"],
                "goals": ["建立品牌认知", "引发兴趣"],
                "messages": ["欢迎介绍", "品牌故事", "核心价值"]
            },
            {
                "stage": "interest",
                "name": "兴趣阶段",
                "touchpoints": ["WhatsApp互动", "内容推送", "优惠活动"],
                "goals": ["引导关注", "收集需求"],
                "messages": ["产品介绍", "用户评价", "限时优惠"]
            },
            {
                "stage": "consideration",
                "name": "考虑阶段",
                "touchpoints": ["1v1咨询", "案例展示", "FAQ"],
                "goals": ["解答疑问", "建立信任"],
                "messages": ["专业解答", "成功案例", "服务承诺"]
            },
            {
                "stage": "purchase",
                "name": "购买阶段",
                "touchpoints": ["下单引导", "支付支持", "订单确认"],
                "goals": ["完成转化", "提升客单价"],
                "messages": ["购买确认", "促销提醒", "组合推荐"]
            },
            {
                "stage": "post_purchase",
                "name": "购买后阶段",
                "touchpoints": ["物流跟踪", "使用指导", "满意度回访"],
                "goals": ["提升体验", "引导复购"],
                "messages": ["发货通知", "使用指南", "满意度调查"]
            },
            {
                "stage": "advocacy",
                "name": "推荐阶段",
                "touchpoints": ["推荐激励", "UGC征集", "会员权益"],
                "goals": ["促进推荐", "口碑传播"],
                "messages": ["推荐奖励", "会员日通知", "新品试用"]
            }
        ]
    
    def generate_templates(self) -> List[Dict]:
        """生成消息模板"""
        return [
            {
                "type": "welcome",
                "name": "欢迎消息",
                "timing": "首次互动",
                "content": "您好！感谢您关注我们 😊\n\n我是[品牌名]的专属客服，很高兴为您服务！\n\n您有任何问题随时告诉我，我会第一时间为您解答。",
                "variables": ["品牌名", "客服名"]
            },
            {
                "type": "product_intro",
                "name": "产品介绍",
                "timing": "客户表达兴趣后",
                "content": "为您推荐我们的热门产品 🔥\n\n【产品名称】\n✨ 核心卖点：...\n💰 价格：...\n📦 发货：...\n\n如需了解更多，回复【1】获取详情~",
                "variables": ["产品名称", "卖点", "价格", "发货信息"]
            },
            {
                "type": "order_confirmation",
                "name": "订单确认",
                "timing": "下单后",
                "content": "订单确认成功！🎉\n\n订单号：{order_id}\n商品：{product_name}\n金额：{amount}\n\n预计送达：{delivery_date}\n\n如有任何问题，请随时联系我~",
                "variables": ["订单号", "商品", "金额", "送达日期"]
            },
            {
                "type": "follow_up",
                "name": "跟进消息",
                "timing": "购买后3-7天",
                "content": "您好！您的订单已签收~ 📦\n\n请问产品使用体验如何呢？\n\n如果满意，欢迎分享您的使用感受，我们会提供专属福利哦~",
                "variables": []
            },
            {
                "type": "reengagement",
                "name": "唤醒消息",
                "timing": "用户沉默30天",
                "content": "好久不见！🌟\n\n我们最近上新了[产品类型]，看到您之前对[兴趣品类]感兴趣，特意为您推荐~\n\n现在下单可享受专属折扣，点击了解：[链接]",
                "variables": ["产品类型", "兴趣品类"]
            }
        ]
    
    def generate_improvement_plan(self, dimensions: List[OpsDimension]) -> List[str]:
        """生成改进计划"""
        plan = []
        
        # 按分数排序找短板
        sorted_dims = sorted(dimensions, key=lambda x: x.score)
        
        for dim in sorted_dims[:3]:
            if dim.score < 70:
                plan.extend(dim.recommendations[:2])
        
        return plan[:6]
    
    def format_report(self, report: OpsReport) -> str:
        """格式化报告"""
        output = []
        output.append("=" * 70)
        output.append("WhatsApp私域运营评分报告")
        output.append("=" * 70)
        
        output.append(f"\n【综合评分】{report.overall_score}分 ({report.ops_level.value})")
        
        output.append(f"\n【各维度评分】")
        for dim in report.dimensions:
            bar = "█" * int(dim.score/5) + "░" * (20 - int(dim.score/5))
            output.append(f"\n  {dim.dimension}: [{bar}] {dim.score}分")
            if dim.findings:
                output.append(f"     ✓ {dim.findings[0]}")
        
        output.append("\n" + "=" * 70)
        return "\n".join(output)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python whatsapp-ops-planner.py <command> [args]")
        print("命令:")
        print("  score      - 私域评分")
        print("  journey    - 客户旅程")
        print("  templates  - 消息模板")
        return
    
    command = sys.argv[1]
    planner = WhatsAppOpsPlanner()
    
    # 示例数据
    sample_metrics = {
        "acquisition": {
            "channel_count": 4,
            "cac": 15,
            "private_import_rate": 0.25
        },
        "activation": {
            "first_reply_rate": 0.65,
            "message_open_rate": 0.55,
            "interaction_depth": 3
        },
        "retention": {
            "delivery_rate": 0.92,
            "report_rate": 0.02,
            "churn_rate": 0.12
        },
        "monetization": {
            "conversion_rate": 0.08,
            "average_order_value": 80,
            "repurchase_rate": 0.25
        },
        "referral": {
            "referral_rate": 0.08,
            "nps_score": 45,
            "viral_coefficient": 1.2
        }
    }
    
    if command == "score":
        report = planner.score(sample_metrics)
        print(planner.format_report(report))
        
    elif command == "journey":
        planner.score(sample_metrics)
        journey = planner.current_report.journey_map
        
        print("=" * 70)
        print("客户旅程地图")
        print("=" * 70)
        
        for stage in journey:
            print(f"\n📍 {stage['name']}")
            print(f"   触点: {', '.join(stage['touchpoints'])}")
            print(f"   目标: {', '.join(stage['goals'])}")
            print(f"   消息: {', '.join(stage['messages'])}")
    
    elif command == "templates":
        planner.score(sample_metrics)
        templates = planner.current_report.message_templates
        
        print("=" * 70)
        print("消息模板库")
        print("=" * 70)
        
        for tmpl in templates:
            print(f"\n📝 {tmpl['name']} ({tmpl['timing']})")
            print(f"   类型: {tmpl['type']}")
            print(f"   内容:")
            for line in tmpl['content'].split('\n'):
                print(f"     {line}")
    
    else:
        print(f"未知命令: {command}")


if __name__ == "__main__":
    main()
