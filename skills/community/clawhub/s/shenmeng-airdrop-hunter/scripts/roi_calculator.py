#!/usr/bin/env python3
"""
空投ROI计算器
计算空投活动的时间成本和预期收益
"""

from dataclasses import dataclass
from typing import List, Dict
import json

@dataclass
class AirdropInvestment:
    """空投投资记录"""
    project_name: str
    time_hours: float  # 投入时间（小时）
    gas_cost_usd: float  # Gas费用
    other_costs_usd: float = 0  # 其他成本
    expected_value_usd: float = 0  # 预期收益
    probability: float = 0.5  # 获得空投概率

@dataclass
class ROICalculation:
    """ROI计算结果"""
    project_name: str
    total_cost_usd: float
    expected_return_usd: float
    roi_ratio: float  # ROI比率
    hourly_rate: float  # 每小时收益
    risk_adjusted_roi: float  # 风险调整ROI

class AirdropROICalculator:
    """空投ROI计算器"""
    
    def __init__(self, hourly_wage: float = 10.0):
        """
        Args:
            hourly_wage: 时薪（美元），用于计算时间成本
        """
        self.hourly_wage = hourly_wage
        self.investments: List[AirdropInvestment] = []
    
    def add_project(self, investment: AirdropInvestment):
        """添加项目投资"""
        self.investments.append(investment)
    
    def calculate_single_roi(self, inv: AirdropInvestment) -> ROICalculation:
        """计算单个项目的ROI"""
        # 时间成本
        time_cost = inv.time_hours * self.hourly_wage
        
        # 总成本
        total_cost = time_cost + inv.gas_cost_usd + inv.other_costs_usd
        
        # 预期收益（考虑获得概率）
        expected_return = inv.expected_value_usd * inv.probability
        
        # ROI比率
        roi_ratio = (expected_return - total_cost) / total_cost if total_cost > 0 else 0
        
        # 每小时收益
        hourly_rate = expected_return / inv.time_hours if inv.time_hours > 0 else 0
        
        # 风险调整ROI（概率权重）
        risk_adjusted_roi = roi_ratio * inv.probability
        
        return ROICalculation(
            project_name=inv.project_name,
            total_cost_usd=total_cost,
            expected_return_usd=expected_return,
            roi_ratio=roi_ratio,
            hourly_rate=hourly_rate,
            risk_adjusted_roi=risk_adjusted_roi
        )
    
    def calculate_portfolio(self) -> Dict:
        """计算投资组合总体ROI"""
        if not self.investments:
            return {}
        
        total_cost = 0
        total_expected = 0
        total_time = 0
        
        results = []
        for inv in self.investments:
            roi = self.calculate_single_roi(inv)
            results.append(roi)
            
            total_cost += roi.total_cost_usd
            total_expected += roi.expected_return_usd
            total_time += inv.time_hours
        
        portfolio_roi = (total_expected - total_cost) / total_cost if total_cost > 0 else 0
        
        return {
            "projects": results,
            "summary": {
                "total_projects": len(self.investments),
                "total_cost_usd": round(total_cost, 2),
                "total_expected_return_usd": round(total_expected, 2),
                "total_time_hours": round(total_time, 2),
                "portfolio_roi": round(portfolio_roi, 2),
                "avg_hourly_rate": round(total_expected / total_time, 2) if total_time > 0 else 0,
            }
        }
    
    def print_report(self, project_name: str = None):
        """打印ROI报告"""
        if project_name:
            # 单个项目报告
            inv = next((i for i in self.investments if i.project_name == project_name), None)
            if not inv:
                print(f"未找到项目: {project_name}")
                return
            
            roi = self.calculate_single_roi(inv)
            self._print_single_report(roi, inv)
        else:
            # 组合报告
            portfolio = self.calculate_portfolio()
            self._print_portfolio_report(portfolio)
    
    def _print_single_report(self, roi: ROICalculation, inv: AirdropInvestment):
        """打印单个项目报告"""
        print(f"\n{'='*60}")
        print(f"📊 {roi.project_name} ROI分析报告")
        print(f"{'='*60}")
        
        print(f"\n💰 成本分析:")
        print(f"   投入时间: {inv.time_hours} 小时")
        print(f"   时间成本: ${inv.time_hours * self.hourly_wage:.2f} (@${self.hourly_wage}/h)")
        print(f"   Gas费用: ${inv.gas_cost_usd:.2f}")
        print(f"   其他成本: ${inv.other_costs_usd:.2f}")
        print(f"   总成本: ${roi.total_cost_usd:.2f}")
        
        print(f"\n📈 收益分析:")
        print(f"   预期空投价值: ${inv.expected_value_usd:.2f}")
        print(f"   获得概率: {inv.probability*100:.0f}%")
        print(f"   预期收益(风险调整): ${roi.expected_return_usd:.2f}")
        
        print(f"\n🎯 ROI指标:")
        print(f"   ROI比率: {roi.roi_ratio*100:.1f}%")
        print(f"   风险调整ROI: {roi.risk_adjusted_roi*100:.1f}%")
        print(f"   每小时收益: ${roi.hourly_rate:.2f}")
        
        # 评级
        if roi.risk_adjusted_roi > 2:
            rating = "🟢 优秀"
        elif roi.risk_adjusted_roi > 0.5:
            rating = "🟡 良好"
        elif roi.risk_adjusted_roi > 0:
            rating = "🟠 一般"
        else:
            rating = "🔴 不建议"
        
        print(f"\n🏆 综合评级: {rating}")
        print(f"{'='*60}\n")
    
    def _print_portfolio_report(self, portfolio: Dict):
        """打印组合报告"""
        print(f"\n{'='*70}")
        print(f"📊 空投投资组合ROI报告")
        print(f"{'='*70}")
        
        print(f"\n📋 各项目详情:")
        print("-" * 70)
        print(f"{'项目':<20} {'成本':>10} {'预期':>10} {'ROI':>8} {'评级':>6}")
        print("-" * 70)
        
        for roi in portfolio["projects"]:
            # 评级
            if roi.risk_adjusted_roi > 2:
                rating = "🟢"
            elif roi.risk_adjusted_roi > 0.5:
                rating = "🟡"
            elif roi.risk_adjusted_roi > 0:
                rating = "🟠"
            else:
                rating = "🔴"
            
            print(f"{roi.project_name:<20} ${roi.total_cost_usd:>9.2f} ${roi.expected_return_usd:>9.2f} {roi.roi_ratio*100:>7.1f}% {rating:>6}")
        
        print("-" * 70)
        
        summary = portfolio["summary"]
        print(f"\n📈 组合总览:")
        print(f"   项目数量: {summary['total_projects']}")
        print(f"   总投入成本: ${summary['total_cost_usd']}")
        print(f"   总预期收益: ${summary['total_expected_return_usd']}")
        print(f"   总投入时间: {summary['total_time_hours']} 小时")
        print(f"   组合ROI: {summary['portfolio_roi']*100:.1f}%")
        print(f"   平均时薪: ${summary['avg_hourly_rate']}/小时")
        
        # 建议
        if summary['portfolio_roi'] > 1:
            advice = "✅ 投资组合表现优秀，继续执行"
        elif summary['portfolio_roi'] > 0:
            advice = "🟡 投资组合略有盈利，可优化项目选择"
        else:
            advice = "⚠️ 投资组合预期亏损，建议重新评估项目"
        
        print(f"\n💡 建议: {advice}")
        print(f"{'='*70}\n")
    
    def export_to_json(self, filename: str):
        """导出到JSON"""
        portfolio = self.calculate_portfolio()
        
        # 转换为可序列化格式
        data = {
            "projects": [
                {
                    "name": r.project_name,
                    "total_cost": r.total_cost_usd,
                    "expected_return": r.expected_return_usd,
                    "roi_ratio": r.roi_ratio,
                    "hourly_rate": r.hourly_rate,
                    "risk_adjusted_roi": r.risk_adjusted_roi
                }
                for r in portfolio["projects"]
            ],
            "summary": portfolio["summary"]
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"报告已导出到: {filename}")


def demo():
    """演示"""
    calc = AirdropROICalculator(hourly_wage=10.0)
    
    # 添加项目
    calc.add_project(AirdropInvestment(
        project_name="Monad",
        time_hours=20,  # 20小时
        gas_cost_usd=0,  # 测试网
        other_costs_usd=0,
        expected_value_usd=5000,
        probability=0.3  # 30%获得
    ))
    
    calc.add_project(AirdropInvestment(
        project_name="Eclipse",
        time_hours=10,
        gas_cost_usd=50,  # 主网Gas
        other_costs_usd=0,
        expected_value_usd=3000,
        probability=0.25
    ))
    
    calc.add_project(AirdropInvestment(
        project_name="Sahara AI",
        time_hours=15,
        gas_cost_usd=0,
        other_costs_usd=0,
        expected_value_usd=2000,
        probability=0.1  # 白名单竞争激烈
    ))
    
    calc.add_project(AirdropInvestment(
        project_name="Polymarket",
        time_hours=5,
        gas_cost_usd=20,
        other_costs_usd=100,  # 预测投入
        expected_value_usd=1500,
        probability=0.4
    ))
    
    # 打印报告
    calc.print_report()
    
    # 导出
    # calc.export_to_json("airdrop_roi_report.json")


if __name__ == "__main__":
    demo()
