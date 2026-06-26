#!/usr/bin/env python3
"""
逆向合规检查器 - Level 2
Reverse Compliance Auditor

功能：
- audit: 逆向合规检查（数据采集/使用/存储/跨境传输4维）
- prioritize: 合规修复优先级
- report: 合规差距报告

Author: Reverse Compliance Team
Version: 1.0.0
"""

import sys
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class ComplianceLevel(Enum):
    """合规等级"""
    FULL = "完全合规"
    SUBSTANTIAL = "基本合规"
    PARTIAL = "部分合规"
    MINIMAL = "勉强合规"
    NON_COMPLIANT = "不合规"


@dataclass
class ComplianceDimension:
    """合规维度"""
    name: str
    current_score: float  # 0-100
    target_score: float
    gaps: List[str] = field(default_factory=list)
    requirements: List[str] = field(default_factory=list)
    evidence_needed: List[str] = field(default_factory=list)
    estimated_effort: str = "medium"  # low, medium, high


@dataclass
class ComplianceIssue:
    """合规问题"""
    id: str
    dimension: str
    severity: str  # critical, high, medium, low
    title: str
    description: str
    regulation: str  # 相关法规
    penalty_risk: str
    fix_suggestion: str
    priority: int
    estimated_cost: float  # 修复成本（万元）
    estimated_time: str  # 修复时间


@dataclass
class ComplianceReport:
    """合规报告"""
    overall_score: float
    overall_level: ComplianceLevel
    dimensions: List[ComplianceDimension]
    issues: List[ComplianceIssue]
    priority_matrix: List[Dict[str, Any]]
    roadmap: List[Dict[str, str]]


class ReverseComplianceAuditor:
    """逆向合规审计器"""
    
    # 法规标准库（简化版）
    REGULATIONS = {
        "GDPR": {
            "name": "欧盟通用数据保护条例",
            "jurisdiction": "欧盟",
            "data_采集": ["合法依据", "隐私告知", "同意机制"],
            "data_使用": ["目的限制", "最小化原则", "自动化决策"],
            "data_存储": ["存储限制", "安全保障", "数据删除"],
            "跨境传输": ["充分性决定", "标准合同条款", "约束性公司规则"]
        },
        "CCPA": {
            "name": "加州消费者隐私法",
            "jurisdiction": "美国加州",
            "data_采集": ["知情权", "选择退出权"],
            "data_使用": ["使用限制", "不歧视"],
            "data_存储": ["安全措施", "数据删除"],
            "跨境传输": ["国内传输限制"]
        },
        "PIPL": {
            "name": "中国个人信息保护法",
            "jurisdiction": "中国",
            "data_采集": ["告知同意", "最小必要"],
            "data_使用": ["目的限制", "处理限制"],
            "data_存储": ["存储期限", "境内存储"],
            "跨境传输": ["安全评估", "标准合同"]
        },
        "PDPA": {
            "name": "泰国个人数据保护法",
            "jurisdiction": "泰国",
            "data_采集": ["同意要求", "目的明确"],
            "data_使用": ["使用限制", "准确性"],
            "data_存储": ["存储期限", "安全措施"],
            "跨境传输": ["充分保护"]
        }
    }
    
    def __init__(self):
        self.current_report: Optional[ComplianceReport] = None
    
    def audit(self, data_handling: Dict[str, Any], 
              regulations: List[str] = None) -> ComplianceReport:
        """
        执行逆向合规审计
        
        Args:
            data_handling: 数据处理现状
            regulations: 需要满足的法规列表
        
        Returns:
            合规审计报告
        """
        if regulations is None:
            regulations = ["GDPR", "CCPA", "PIPL"]
        
        dimensions = []
        all_issues = []
        
        # 评估各维度
        dim_configs = [
            ("data_采集", "数据采集", 25),
            ("data_使用", "数据使用", 25),
            ("data_存储", "数据存储", 25),
            ("跨境传输", "跨境传输", 25)
        ]
        
        for dim_key, dim_name, weight in dim_configs:
            current_data = data_handling.get(dim_key, {})
            dim_result = self._assess_dimension(
                dim_key, dim_name, current_data, regulations
            )
            dimensions.append(dim_result)
            
            for issue in dim_result.get("issues", []):
                issue["dimension"] = dim_name
                all_issues.append(issue)
        
        # 计算综合评分
        overall_score = sum(d["score"] * 0.25 for d in dimensions)
        
        # 确定合规等级
        overall_level = self._get_compliance_level(overall_score)
        
        # 生成优先级矩阵
        priority_matrix = self._generate_priority_matrix(all_issues)
        
        # 生成实施路线图
        roadmap = self._generate_roadmap(overall_score, all_issues)
        
        self.current_report = ComplianceReport(
            overall_score=round(overall_score, 1),
            overall_level=overall_level,
            dimensions=self._format_dimensions(dimensions),
            issues=self._format_issues(all_issues),
            priority_matrix=priority_matrix,
            roadmap=roadmap
        )
        
        return self.current_report
    
    def _assess_dimension(self, dim_key: str, dim_name: str,
                          current_data: Dict, 
                          regulations: List[str]) -> Dict:
        """评估单个维度"""
        requirements = []
        gaps = []
        issues = []
        score = 100
        
        # 收集各法规要求
        for reg in regulations:
            if reg in self.REGULATIONS:
                reqs = self.REGULATIONS[reg].get(dim_key, [])
                requirements.extend(reqs)
        
        # 去重
        requirements = list(set(requirements))
        
        # 检查当前状态与要求的差距
        current_state = current_data.get("status", "unknown")
        
        if current_state == "compliant":
            score = 90
        elif current_state == "partial":
            score = 60
            gaps.append("部分要求尚未完全满足")
            issues.append({
                "id": f"{dim_key}-001",
                "severity": "medium",
                "title": f"{dim_name}部分不合规",
                "description": "存在部分要求未满足",
                "regulation": ", ".join(regulations),
                "penalty_risk": "中",
                "fix_suggestion": "完善相关流程和文档",
                "priority": 3,
                "estimated_cost": 5.0,
                "estimated_time": "2-4周"
            })
        elif current_state == "non_compliant":
            score = 30
            gaps.append("严重不合规项存在")
            issues.append({
                "id": f"{dim_key}-001",
                "severity": "critical",
                "title": f"{dim_name}严重不合规",
                "description": "存在关键合规要求未满足",
                "regulation": ", ".join(regulations),
                "penalty_risk": "高",
                "fix_suggestion": "紧急修复，必要时暂停相关业务",
                "priority": 1,
                "estimated_cost": 20.0,
                "estimated_time": "1-2周"
            })
        else:
            score = 50
            gaps.append("状态未知，需要评估")
        
        return {
            "name": dim_name,
            "score": score,
            "target_score": 80,
            "gaps": gaps,
            "requirements": requirements[:5],
            "issues": issues,
            "estimated_effort": "high" if score < 50 else "medium" if score < 75 else "low"
        }
    
    def _get_compliance_level(self, score: float) -> ComplianceLevel:
        """确定合规等级"""
        if score >= 90:
            return ComplianceLevel.FULL
        elif score >= 75:
            return ComplianceLevel.SUBSTANTIAL
        elif score >= 60:
            return ComplianceLevel.PARTIAL
        elif score >= 40:
            return ComplianceLevel.MINIMAL
        else:
            return ComplianceLevel.NON_COMPLIANT
    
    def _format_dimensions(self, dimensions: List[Dict]) -> List[ComplianceDimension]:
        """格式化维度列表"""
        return [
            ComplianceDimension(
                name=d["name"],
                current_score=d["score"],
                target_score=d["target_score"],
                gaps=d["gaps"],
                requirements=d["requirements"],
                evidence_needed=self._get_evidence_needed(d["name"]),
                estimated_effort=d["estimated_effort"]
            )
            for d in dimensions
        ]
    
    def _get_evidence_needed(self, dim_name: str) -> List[str]:
        """获取需要的证据"""
        evidence_map = {
            "数据采集": ["隐私政策", "用户同意记录", "Cookie同意机制"],
            "数据使用": ["处理记录", "日志审计", "访问控制策略"],
            "数据存储": ["加密配置", "备份记录", "存储期限文档"],
            "跨境传输": ["传输协议", "安全评估报告", "数据地图"]
        }
        return evidence_map.get(dim_name, [])
    
    def _format_issues(self, issues: List[Dict]) -> List[ComplianceIssue]:
        """格式化问题列表"""
        return [
            ComplianceIssue(
                id=i["id"],
                dimension=i.get("dimension", "未知"),
                severity=i["severity"],
                title=i["title"],
                description=i["description"],
                regulation=i["regulation"],
                penalty_risk=i["penalty_risk"],
                fix_suggestion=i["fix_suggestion"],
                priority=i["priority"],
                estimated_cost=i["estimated_cost"],
                estimated_time=i["estimated_time"]
            )
            for i in issues
        ]
    
    def _generate_priority_matrix(self, issues: List[Dict]) -> List[Dict[str, Any]]:
        """生成优先级矩阵"""
        # 按严重程度和成本分组
        matrix = {
            "quick_wins": [],      # 高优先级，低成本
            "major_projects": [],  # 高优先级，高成本
            "fill_ins": [],        # 低优先级，低成本
            "consider_later": []   # 低优先级，高成本
        }
        
        for issue in issues:
            severity_score = {"critical": 4, "high": 3, "medium": 2, "low": 1}.get(issue["severity"], 2)
            cost = issue["estimated_cost"]
            
            if severity_score >= 3 and cost < 10:
                matrix["quick_wins"].append(issue)
            elif severity_score >= 3:
                matrix["major_projects"].append(issue)
            elif cost < 5:
                matrix["fill_ins"].append(issue)
            else:
                matrix["consider_later"].append(issue)
        
        return matrix
    
    def _generate_roadmap(self, overall_score: float, 
                          issues: List[Dict]) -> List[Dict[str, str]]:
        """生成实施路线图"""
        if overall_score >= 80:
            return [
                {"phase": "1-2周", "focus": "持续关注", "milestone": "保持合规状态"},
                {"phase": "月度", "focus": "定期审计", "milestone": "发现问题时快速响应"},
                {"phase": "年度", "focus": "全面复审", "milestone": "符合监管要求"}
            ]
        
        critical_issues = [i for i in issues if i["severity"] == "critical"]
        high_issues = [i for i in issues if i["severity"] == "high"]
        
        roadmap = []
        
        if critical_issues:
            roadmap.append({
                "phase": "第1-2周",
                "focus": "紧急修复",
                "milestone": "解决critical级别问题"
            })
        
        if high_issues:
            roadmap.append({
                "phase": "第3-6周",
                "focus": "重点整改",
                "milestone": "解决high级别问题"
            })
        
        roadmap.extend([
            {"phase": "第2-3月", "focus": "体系完善", "milestone": "建立合规管理体系"},
            {"phase": "第4-6月", "focus": "持续优化", "milestone": "达到基本合规"}
        ])
        
        return roadmap
    
    def prioritize_fixes(self, issues: List[Dict] = None) -> List[Dict]:
        """
        修复优先级排序
        
        Returns:
            优先级排序的修复计划
        """
        if issues is None and self.current_report:
            issues = [
                {"id": i.id, "severity": i.severity, "estimated_cost": i.estimated_cost,
                 "dimension": i.dimension, "title": i.title}
                for i in self.current_report.issues
            ]
        
        if not issues:
            return []
        
        # 按优先级和成本排序
        def priority_key(item):
            severity_weight = {"critical": 100, "high": 50, "medium": 20, "low": 5}
            sw = severity_weight.get(item["severity"], 10)
            cost_factor = 1 / (item["estimated_cost"] + 1)
            return sw * cost_factor
        
        sorted_issues = sorted(issues, key=priority_key, reverse=True)
        
        result = []
        total_cost = 0
        
        for i, issue in enumerate(sorted_issues, 1):
            result.append({
                "rank": i,
                "id": issue["id"],
                "title": issue["title"],
                "dimension": issue.get("dimension", ""),
                "severity": issue["severity"],
                "estimated_cost": f"{issue['estimated_cost']}万元",
                "reason": self._get_priority_reason(issue)
            })
            total_cost += issue["estimated_cost"]
        
        result.append({
            "rank": "合计",
            "id": "-",
            "title": f"共{len(issues)}项",
            "severity": "-",
            "estimated_cost": f"{total_cost}万元",
            "reason": "总预算"
        })
        
        return result
    
    def _get_priority_reason(self, issue: Dict) -> str:
        """获取优先级原因"""
        if issue["severity"] == "critical":
            return "紧急，需立即处理"
        elif issue["severity"] == "high":
            return "重要，应优先处理"
        elif issue["estimated_cost"] < 5:
            return "成本低，建议尽快处理"
        else:
            return "可安排在后续阶段"
    
    def generate_report(self) -> str:
        """生成合规报告"""
        if not self.current_report:
            return "请先执行合规审计"
        
        report = self.current_report
        output = []
        
        output.append("=" * 70)
        output.append("逆向合规审计报告")
        output.append("=" * 70)
        output.append(f"\n【综合合规评分】{report.overall_score}分")
        output.append(f"【合规等级】{report.overall_level.value}")
        
        output.append(f"\n【各维度评分】")
        for dim in report.dimensions:
            gap = dim.target_score - dim.current_score
            gap_str = f"(差距: {gap:.1f}分)" if gap > 0 else "(已达标)"
            output.append(f"\n  ▶ {dim.name}: {dim.current_score}分 {gap_str}")
            if dim.gaps:
                output.append(f"    差距: {', '.join(dim.gaps[:2])}")
            if dim.estimated_effort == "high":
                output.append(f"    ⚠ 修复难度: 高")
        
        output.append(f"\n【问题汇总】")
        output.append(f"  总计: {len(report.issues)}项")
        
        severity_counts = {}
        for issue in report.issues:
            severity_counts[issue.severity] = severity_counts.get(issue.severity, 0) + 1
        
        for sev, count in sorted(severity_counts.items(), 
                                 key=lambda x: ["critical", "high", "medium", "low"].index(x[0])):
            output.append(f"    {sev.upper()}: {count}项")
        
        output.append(f"\n【优先级矩阵】")
        pm = report.priority_matrix
        
        if pm.get("quick_wins"):
            output.append(f"\n  🔥 速赢项 (高优先级，低成本):")
            for item in pm["quick_wins"]:
                output.append(f"    • {item['title']}")
        
        if pm.get("major_projects"):
            output.append(f"\n  📋 重点项目 (高优先级，高成本):")
            for item in pm["major_projects"]:
                output.append(f"    • {item['title']}")
        
        output.append(f"\n【实施路线图】")
        for phase in report.roadmap:
            output.append(f"\n  {phase['phase']}: {phase['focus']}")
            output.append(f"    里程碑: {phase['milestone']}")
        
        output.append("\n" + "=" * 70)
        return "\n".join(output)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python reverse-auditor.py <command> [args]")
        print("命令:")
        print("  audit       - 执行合规审计")
        print("  prioritize - 生成修复优先级")
        print("  report     - 生成合规报告")
        return
    
    command = sys.argv[1]
    auditor = ReverseComplianceAuditor()
    
    if command == "audit":
        # 模拟数据处理现状
        sample_data = {
            "data_采集": {"status": "partial"},
            "data_使用": {"status": "compliant"},
            "data_存储": {"status": "partial"},
            "跨境传输": {"status": "non_compliant"}
        }
        
        report = auditor.audit(sample_data, ["GDPR", "PIPL"])
        print(auditor.generate_report())
        
    elif command == "prioritize":
        # 先生成审计报告
        sample_data = {
            "data_采集": {"status": "partial"},
            "data_使用": {"status": "partial"},
            "data_存储": {"status": "partial"},
            "跨境传输": {"status": "non_compliant"}
        }
        auditor.audit(sample_data)
        
        priorities = auditor.prioritize_fixes()
        
        print("=" * 70)
        print("修复优先级排序")
        print("=" * 70)
        
        for item in priorities:
            if item["rank"] == "合计":
                print(f"\n{'='*50}")
            print(f"\n#{item['rank']} {item['title']}")
            print(f"   维度: {item['dimension']}")
            print(f"   严重程度: {item['severity']}")
            print(f"   预估成本: {item['estimated_cost']}")
            print(f"   原因: {item['reason']}")
        
    elif command == "report":
        if not auditor.current_report:
            sample_data = {
                "data_采集": {"status": "partial"},
                "data_使用": {"status": "compliant"},
                "data_存储": {"status": "partial"},
                "跨境传输": {"status": "non_compliant"}
            }
            auditor.audit(sample_data)
        
        print(auditor.generate_report())
    
    else:
        print(f"未知命令: {command}")


if __name__ == "__main__":
    main()
