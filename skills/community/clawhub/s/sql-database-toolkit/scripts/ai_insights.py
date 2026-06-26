"""
AI 自动洞察生成模块 - 纯统计分析，无需外部 API
基于 pandas + numpy + scipy 的数据智能分析引擎
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum
import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime
import json


class InsightType(Enum):
    """洞察类型枚举"""
    ANOMALY = "anomaly"
    TREND = "trend"
    CORRELATION = "correlation"
    TOP_N = "top_n"
    DISTRIBUTION = "distribution"
    SEASONALITY = "seasonality"
    COMPARISON = "comparison"


class SeverityLevel(Enum):
    """严重程度枚举"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class Insight:
    """单个洞察对象"""
    type: str
    severity: str
    title: str
    description: str
    metric: str
    value: Any
    confidence: float
    
    def to_dict(self) -> dict:
        """转换为字典（确保 JSON 可序列化）"""
        def make_serializable(val):
            if isinstance(val, (np.integer, np.int64, np.int32)):
                return int(val)
            elif isinstance(val, (np.floating, np.float64, np.float32)):
                return float(val)
            elif isinstance(val, np.ndarray):
                return val.tolist()
            return val
        
        return {
            "type": make_serializable(self.type),
            "severity": make_serializable(self.severity),
            "title": make_serializable(self.title),
            "description": make_serializable(self.description),
            "metric": make_serializable(self.metric),
            "value": make_serializable(self.value),
            "confidence": make_serializable(self.confidence)
        }


@dataclass
class InsightReport:
    """完整洞察报告"""
    insights: List[Insight] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    summary: str = ""
    generated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "insights": [i.to_dict() for i in self.insights],
            "recommendations": self.recommendations,
            "summary": self.summary,
            "generated_at": self.generated_at,
            "total_insights": len(self.insights)
        }
    
    def to_markdown(self) -> str:
        """转换为 Markdown 格式"""
        lines = []
        lines.append("# 数据洞察报告\n")
        lines.append(f"**生成时间**: {self.generated_at}\n")
        lines.append(f"**总洞察数**: {len(self.insights)}\n")
        
        if self.summary:
            lines.append("## 摘要\n")
            lines.append(f"{self.summary}\n")
        
        lines.append("## 洞察详情\n")
        for i, insight in enumerate(self.insights, 1):
            lines.append(f"### {i}. {insight.title}\n")
            lines.append(f"- **类型**: {insight.type}\n")
            lines.append(f"- **严重程度**: {insight.severity}\n")
            lines.append(f"- **指标**: {insight.metric}\n")
            lines.append(f"- **关键值**: {insight.value}\n")
            lines.append(f"- **置信度**: {insight.confidence:.1%}\n")
            lines.append(f"- **描述**: {insight.description}\n")
        
        if self.recommendations:
            lines.append("## 运营建议\n")
            for i, rec in enumerate(self.recommendations, 1):
                lines.append(f"{i}. {rec}\n")
        
        return "".join(lines)
    
    def to_html(self) -> str:
        """转换为 HTML 格式"""
        html_parts = []
        html_parts.append("<!DOCTYPE html>")
        html_parts.append("<html lang='zh-CN'>")
        html_parts.append("<head>")
        html_parts.append("<meta charset='UTF-8'>")
        html_parts.append("<meta name='viewport' content='width=device-width, initial-scale=1.0'>")
        html_parts.append("<title>数据洞察报告</title>")
        html_parts.append("<style>")
        html_parts.append("""
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 30px;
        }
        .header h1 {
            margin: 0 0 10px 0;
            font-size: 28px;
        }
        .meta {
            font-size: 14px;
            opacity: 0.9;
        }
        .summary {
            background-color: #e8f4f8;
            border-left: 4px solid #667eea;
            padding: 15px;
            margin-bottom: 30px;
            border-radius: 4px;
        }
        .insights-container {
            display: grid;
            gap: 20px;
            margin-bottom: 30px;
        }
        .insight-card {
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #667eea;
        }
        .insight-card.critical {
            border-left-color: #e74c3c;
        }
        .insight-card.warning {
            border-left-color: #f39c12;
        }
        .insight-card.info {
            border-left-color: #3498db;
        }
        .insight-title {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #2c3e50;
        }
        .insight-meta {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
            margin-bottom: 10px;
            font-size: 13px;
        }
        .meta-item {
            background-color: #f8f9fa;
            padding: 8px;
            border-radius: 4px;
        }
        .meta-label {
            font-weight: bold;
            color: #667eea;
        }
        .insight-description {
            color: #555;
            line-height: 1.6;
            margin-top: 10px;
        }
        .recommendations {
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .recommendations h2 {
            color: #2c3e50;
            margin-top: 0;
        }
        .recommendation-item {
            padding: 10px;
            margin-bottom: 10px;
            background-color: #f8f9fa;
            border-left: 3px solid #667eea;
            border-radius: 4px;
        }
        .severity-badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
            margin-right: 10px;
        }
        .severity-critical {
            background-color: #e74c3c;
            color: white;
        }
        .severity-warning {
            background-color: #f39c12;
            color: white;
        }
        .severity-info {
            background-color: #3498db;
            color: white;
        }
        """)
        html_parts.append("</style>")
        html_parts.append("</head>")
        html_parts.append("<body>")
        
        html_parts.append("<div class='header'>")
        html_parts.append("<h1>📊 数据洞察报告</h1>")
        html_parts.append(f"<div class='meta'>生成时间: {self.generated_at} | 总洞察数: {len(self.insights)}</div>")
        html_parts.append("</div>")
        
        if self.summary:
            html_parts.append("<div class='summary'>")
            html_parts.append(f"<strong>摘要:</strong> {self.summary}")
            html_parts.append("</div>")
        
        html_parts.append("<div class='insights-container'>")
        for insight in self.insights:
            severity_class = insight.severity.lower()
            html_parts.append(f"<div class='insight-card {severity_class}'>")
            html_parts.append(f"<div class='insight-title'>")
            html_parts.append(f"<span class='severity-badge severity-{severity_class}'>{insight.severity.upper()}</span>")
            html_parts.append(f"{insight.title}")
            html_parts.append("</div>")
            html_parts.append("<div class='insight-meta'>")
            html_parts.append(f"<div class='meta-item'><span class='meta-label'>类型:</span> {insight.type}</div>")
            html_parts.append(f"<div class='meta-item'><span class='meta-label'>指标:</span> {insight.metric}</div>")
            html_parts.append(f"<div class='meta-item'><span class='meta-label'>关键值:</span> {insight.value}</div>")
            html_parts.append(f"<div class='meta-item'><span class='meta-label'>置信度:</span> {insight.confidence:.1%}</div>")
            html_parts.append("</div>")
            html_parts.append(f"<div class='insight-description'>{insight.description}</div>")
            html_parts.append("</div>")
        html_parts.append("</div>")
        
        if self.recommendations:
            html_parts.append("<div class='recommendations'>")
            html_parts.append("<h2>💡 运营建议</h2>")
            for rec in self.recommendations:
                html_parts.append(f"<div class='recommendation-item'>{rec}</div>")
            html_parts.append("</div>")
        
        html_parts.append("</body>")
        html_parts.append("</html>")
        
        return "\n".join(html_parts)


class InsightGenerator:
    """AI 自动洞察生成器 - 纯统计分析，无需外部 API"""
    
    def __init__(self, df: pd.DataFrame, date_col=None, value_cols=None, dimension_cols=None):
        """
        初始化洞察生成器
        
        Args:
            df: 输入数据框
            date_col: 日期列名（用于时间序列分析）
            value_cols: 数值列列表（用于分析的指标列）
            dimension_cols: 维度列列表（用于分组分析）
        """
        self.df = df.copy()
        self.date_col = date_col
        self.value_cols = value_cols or self._infer_numeric_cols()
        self.dimension_cols = dimension_cols or []
        self.insights: List[Insight] = []
        
        # 数据预处理
        if self.date_col and self.date_col in self.df.columns:
            self.df[self.date_col] = pd.to_datetime(self.df[self.date_col], errors='coerce')
    
    def _infer_numeric_cols(self) -> List[str]:
        """自动推断数值列"""
        return self.df.select_dtypes(include=[np.number]).columns.tolist()
    
    def generate_all(self) -> InsightReport:
        """生成完整洞察报告"""
        self.insights = []
        
        # 执行各类分析
        self.insights.extend(self.detect_anomalies())
        self.insights.extend(self.detect_trends())
        self.insights.extend(self.detect_correlations())
        self.insights.extend(self.detect_top_items())
        self.insights.extend(self.detect_distribution())
        
        if self.date_col:
            self.insights.extend(self.detect_seasonality())
        
        if self.dimension_cols:
            self.insights.extend(self.detect_comparison())
        
        # 生成建议
        recommendations = self.generate_recommendations(self.insights)
        
        # 生成摘要
        summary = self._generate_summary()
        
        return InsightReport(
            insights=self.insights,
            recommendations=recommendations,
            summary=summary
        )
    
    def detect_anomalies(self) -> List[Insight]:
        """异常检测：识别离群值、突变点"""
        insights = []
        
        for col in self.value_cols:
            if col not in self.df.columns:
                continue
            
            data = self.df[col].dropna()
            if len(data) < 3:
                continue
            
            # Z-score 方法
            z_scores = np.abs(stats.zscore(data))
            anomaly_mask = z_scores > 2.5
            anomaly_count = anomaly_mask.sum()
            
            if anomaly_count > 0:
                anomaly_rate = anomaly_count / len(data)
                insights.append(Insight(
                    type=InsightType.ANOMALY.value,
                    severity=SeverityLevel.WARNING.value if anomaly_rate > 0.05 else SeverityLevel.INFO.value,
                    title=f"{col} 中检测到异常值",
                    description=f"检测到 {anomaly_count} 个异常值（占比 {anomaly_rate:.1%}），可能需要进一步调查。",
                    metric=col,
                    value=anomaly_count,
                    confidence=min(0.95, 0.7 + anomaly_rate)
                ))
            
            # IQR 方法检测突变
            if len(data) > 1 and self.date_col:
                sorted_df = self.df.sort_values(self.date_col)
                values = sorted_df[col].dropna().values
                if len(values) > 1:
                    pct_change = np.abs(np.diff(values) / (np.abs(values[:-1]) + 1e-10))
                    max_change_idx = np.argmax(pct_change)
                    max_change = pct_change[max_change_idx]
                    
                    if max_change > 0.5:
                        insights.append(Insight(
                            type=InsightType.ANOMALY.value,
                            severity=SeverityLevel.CRITICAL.value if max_change > 1.0 else SeverityLevel.WARNING.value,
                            title=f"{col} 出现突变",
                            description=f"检测到 {max_change:.1%} 的环比变化，可能存在重大事件。",
                            metric=col,
                            value=f"{max_change:.1%}",
                            confidence=0.85
                        ))
        
        return insights
    
    def detect_trends(self) -> List[Insight]:
        """趋势检测：上升/下降/平稳"""
        insights = []
        
        if not self.date_col or self.date_col not in self.df.columns:
            return insights
        
        sorted_df = self.df.sort_values(self.date_col)
        
        for col in self.value_cols:
            if col not in sorted_df.columns:
                continue
            
            data = sorted_df[col].dropna()
            if len(data) < 3:
                continue
            
            # 线性回归计算趋势
            x = np.arange(len(data))
            y = data.values
            
            try:
                coeffs = np.polyfit(x, y, 1)
                slope = coeffs[0]
                mean_val = np.mean(y)
                
                # 标准化斜率
                normalized_slope = slope / (mean_val + 1e-10)
                
                if normalized_slope > 0.05:
                    trend_type = "上升"
                    severity = SeverityLevel.INFO.value
                    confidence = min(0.95, 0.6 + abs(normalized_slope))
                elif normalized_slope < -0.05:
                    trend_type = "下降"
                    severity = SeverityLevel.WARNING.value
                    confidence = min(0.95, 0.6 + abs(normalized_slope))
                else:
                    trend_type = "平稳"
                    severity = SeverityLevel.INFO.value
                    confidence = 0.7
                
                insights.append(Insight(
                    type=InsightType.TREND.value,
                    severity=severity,
                    title=f"{col} 呈现{trend_type}趋势",
                    description=f"在分析周期内，{col} 显示{trend_type}趋势，斜率为 {slope:.4f}。",
                    metric=col,
                    value=f"{normalized_slope:.1%}",
                    confidence=confidence
                ))
            except Exception:
                pass
        
        return insights
    
    def detect_correlations(self) -> List[Insight]:
        """相关性检测：列间相关性"""
        insights = []
        
        if len(self.value_cols) < 2:
            return insights
        
        numeric_df = self.df[self.value_cols].select_dtypes(include=[np.number])
        if numeric_df.shape[1] < 2:
            return insights
        
        corr_matrix = numeric_df.corr()
        
        # 找出强相关对
        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                col1 = corr_matrix.columns[i]
                col2 = corr_matrix.columns[j]
                corr_val = corr_matrix.iloc[i, j]
                
                abs_corr = abs(corr_val)
                
                if abs_corr > 0.7:
                    severity = SeverityLevel.INFO.value
                    corr_type = "正相关" if corr_val > 0 else "负相关"
                    insights.append(Insight(
                        type=InsightType.CORRELATION.value,
                        severity=severity,
                        title=f"{col1} 与 {col2} 高度{corr_type}",
                        description=f"相关系数为 {corr_val:.3f}，两个指标高度相关，可作为预测指标。",
                        metric=f"{col1} vs {col2}",
                        value=f"{corr_val:.3f}",
                        confidence=0.9
                    ))
                elif 0.4 < abs_corr < 0.7:
                    insights.append(Insight(
                        type=InsightType.CORRELATION.value,
                        severity=SeverityLevel.INFO.value,
                        title=f"{col1} 与 {col2} 中等相关",
                        description=f"相关系数为 {corr_val:.3f}，两个指标存在中等程度的相关性。",
                        metric=f"{col1} vs {col2}",
                        value=f"{corr_val:.3f}",
                        confidence=0.75
                    ))
        
        return insights
    
    def detect_top_items(self) -> List[Insight]:
        """TOP N 分析：头部集中度、长尾"""
        insights = []
        
        for col in self.value_cols:
            if col not in self.df.columns:
                continue
            
            data = self.df[col].dropna()
            if len(data) < 5:
                continue
            
            # 帕累托分析
            sorted_data = np.sort(data)[::-1]
            cumsum = np.cumsum(sorted_data)
            total = cumsum[-1]
            
            if total <= 0:
                continue
            
            # 找出占比 80% 的项数
            threshold_80 = total * 0.8
            idx_80 = np.searchsorted(cumsum, threshold_80)
            concentration_20 = (idx_80 + 1) / len(data)
            
            if concentration_20 < 0.3:
                severity = SeverityLevel.WARNING.value
                insights.append(Insight(
                    type=InsightType.TOP_N.value,
                    severity=severity,
                    title=f"{col} 集中度偏高",
                    description=f"前 {concentration_20:.0%} 的项目贡献了 80% 的价值，集中度偏高，建议分散风险。",
                    metric=col,
                    value=f"{concentration_20:.1%}",
                    confidence=0.85
                ))
            else:
                insights.append(Insight(
                    type=InsightType.TOP_N.value,
                    severity=SeverityLevel.INFO.value,
                    title=f"{col} 分布相对均衡",
                    description=f"前 {concentration_20:.0%} 的项目贡献了 80% 的价值，分布相对均衡。",
                    metric=col,
                    value=f"{concentration_20:.1%}",
                    confidence=0.8
                ))
        
        return insights
    
    def detect_distribution(self) -> List[Insight]:
        """分布检测：正态/偏态/均匀"""
        insights = []
        
        for col in self.value_cols:
            if col not in self.df.columns:
                continue
            
            data = self.df[col].dropna()
            if len(data) < 10:
                continue
            
            # 计算偏度和峰度
            skewness = stats.skew(data)
            kurtosis = stats.kurtosis(data)
            cv = np.std(data) / (np.mean(data) + 1e-10)
            
            # 判断分布类型
            if abs(skewness) < 0.5:
                dist_type = "近似正态分布"
            elif skewness > 0.5:
                dist_type = "右偏分布"
            else:
                dist_type = "左偏分布"
            
            insights.append(Insight(
                type=InsightType.DISTRIBUTION.value,
                severity=SeverityLevel.INFO.value,
                title=f"{col} 呈现{dist_type}",
                description=f"偏度: {skewness:.3f}, 峰度: {kurtosis:.3f}, 变异系数: {cv:.3f}。",
                metric=col,
                value=f"偏度={skewness:.3f}",
                confidence=0.8
            ))
        
        return insights
    
    def detect_seasonality(self) -> List[Insight]:
        """季节性检测：周期性模式"""
        insights = []
        
        if not self.date_col or self.date_col not in self.df.columns:
            return insights
        
        sorted_df = self.df.sort_values(self.date_col)
        
        for col in self.value_cols:
            if col not in sorted_df.columns:
                continue
            
            data = sorted_df[col].dropna()
            if len(data) < 14:
                continue
            
            # 简单的周期性检测：计算周间差异
            if len(data) >= 7:
                week1 = data.iloc[:7].mean()
                week2 = data.iloc[7:14].mean()
                
                if week1 > 0:
                    week_diff = abs(week2 - week1) / week1
                    
                    if week_diff > 0.2:
                        insights.append(Insight(
                            type=InsightType.SEASONALITY.value,
                            severity=SeverityLevel.INFO.value,
                            title=f"{col} 存在周期性波动",
                            description=f"检测到周间差异 {week_diff:.1%}，可能存在周期性模式。",
                            metric=col,
                            value=f"{week_diff:.1%}",
                            confidence=0.7
                        ))
        
        return insights
    
    def detect_comparison(self, group_col=None) -> List[Insight]:
        """对比分析：分组差异"""
        insights = []
        
        if not self.dimension_cols:
            return insights
        
        for dim_col in self.dimension_cols:
            if dim_col not in self.df.columns:
                continue
            
            for val_col in self.value_cols:
                if val_col not in self.df.columns:
                    continue
                
                grouped = self.df.groupby(dim_col)[val_col].agg(['mean', 'std', 'count'])
                grouped = grouped[grouped['count'] >= 2]
                
                if len(grouped) < 2:
                    continue
                
                # 计算组间差异
                max_mean = grouped['mean'].max()
                min_mean = grouped['mean'].min()
                
                if min_mean > 0:
                    diff_ratio = (max_mean - min_mean) / min_mean
                    
                    if diff_ratio > 0.3:
                        max_group = grouped['mean'].idxmax()
                        min_group = grouped['mean'].idxmin()
                        
                        insights.append(Insight(
                            type=InsightType.COMPARISON.value,
                            severity=SeverityLevel.WARNING.value if diff_ratio > 0.5 else SeverityLevel.INFO.value,
                            title=f"{dim_col} 维度下 {val_col} 差异显著",
                            description=f"{max_group} 的 {val_col} 比 {min_group} 高 {diff_ratio:.1%}，存在显著差异。",
                            metric=f"{dim_col} - {val_col}",
                            value=f"{diff_ratio:.1%}",
                            confidence=0.8
                        ))
        
        return insights
    
    def generate_recommendations(self, insights: List[Insight]) -> List[str]:
        """基于洞察生成运营建议"""
        recommendations = []
        
        for insight in insights:
            if insight.type == InsightType.TREND.value:
                if "上升" in insight.title:
                    recommendations.append(f"✅ {insight.metric} 持续增长，建议加大投入和资源配置。")
                elif "下降" in insight.title:
                    recommendations.append(f"⚠️ {insight.metric} 出现下降趋势，建议排查原因并制定改进方案。")
            
            elif insight.type == InsightType.ANOMALY.value:
                if "突变" in insight.title:
                    recommendations.append(f"🔴 {insight.metric} 出现异常突变，需要立即调查根本原因。")
                else:
                    recommendations.append(f"⚠️ {insight.metric} 中存在异常值，建议数据清洗和验证。")
            
            elif insight.type == InsightType.TOP_N.value:
                if "偏高" in insight.title:
                    recommendations.append(f"📊 {insight.metric} 集中度过高，建议优化产品组合，分散风险。")
                else:
                    recommendations.append(f"✅ {insight.metric} 分布均衡，继续保持现有策略。")
            
            elif insight.type == InsightType.CORRELATION.value:
                if "高度" in insight.title:
                    recommendations.append(f"🔗 {insight.metric} 高度相关，可作为预测指标，建议建立预测模型。")
            
            elif insight.type == InsightType.COMPARISON.value:
                if "差异显著" in insight.title:
                    recommendations.append(f"📈 {insight.metric} 存在显著差异，建议分析差异原因并复制最佳实践。")
            
            elif insight.type == InsightType.SEASONALITY.value:
                recommendations.append(f"📅 {insight.metric} 存在周期性模式，建议制定季节性运营策略。")
        
        # 去重
        recommendations = list(dict.fromkeys(recommendations))
        
        return recommendations[:10]  # 限制建议数量
    
    def _generate_summary(self) -> str:
        """生成报告摘要"""
        if not self.insights:
            return "未检测到显著洞察。"
        
        critical_count = sum(1 for i in self.insights if i.severity == SeverityLevel.CRITICAL.value)
        warning_count = sum(1 for i in self.insights if i.severity == SeverityLevel.WARNING.value)
        
        summary_parts = []
        
        if critical_count > 0:
            summary_parts.append(f"检测到 {critical_count} 个严重问题")
        
        if warning_count > 0:
            summary_parts.append(f"{warning_count} 个警告")
        
        if summary_parts:
            return "，".join(summary_parts) + "。建议立即采取行动。"
        else:
            return "数据整体表现良好，继续监控关键指标。"


def quick_insights(df: pd.DataFrame, date_col=None, value_cols=None, dimension_cols=None) -> InsightReport:
    """一键生成洞察报告"""
    gen = InsightGenerator(df, date_col=date_col, value_cols=value_cols, dimension_cols=dimension_cols)
    return gen.generate_all()


if __name__ == "__main__":
    import sys
    import io
    
    # 设置 stdout 为 UTF-8 编码（解决 Windows 控制台编码问题）
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("=" * 80)
    print("AI Auto Insights Generator - Test Demo")
    print("=" * 80)
    
    # 创建模拟电商销售数据
    np.random.seed(42)
    dates = pd.date_range('2024-01-01', periods=60, freq='D')
    
    # 生成销售数据：基础趋势 + 周期性 + 噪声 + 异常值
    base_sales = 1000 + np.arange(60) * 5
    seasonality = 200 * np.sin(np.arange(60) * 2 * np.pi / 7)
    noise = np.random.normal(0, 50, 60)
    sales = base_sales + seasonality + noise
    
    # 添加异常值
    sales[15] = 3000
    sales[45] = 200
    
    # 创建数据框
    df = pd.DataFrame({
        'date': dates,
        'region': np.random.choice(['华东', '华北', '华南', '西部'], 60),
        'product': np.random.choice(['产品A', '产品B', '产品C'], 60),
        'sales': sales,
        'quantity': np.random.randint(10, 100, 60),
        'cost': np.random.randint(300, 800, 60)
    })
    
    # 计算利润
    df['profit'] = df['sales'] - df['cost']
    
    print("\n[样本数据] 前10行:")
    print(df.head(10).to_string())
    print(f"\n数据形状: {df.shape}")
    print(f"日期范围: {df['date'].min()} 到 {df['date'].max()}")
    
    # 生成洞察报告
    print("\n[生成洞察报告...]")
    report = quick_insights(
        df,
        date_col='date',
        value_cols=['sales', 'quantity', 'profit'],
        dimension_cols=['region', 'product']
    )
    
    print(f"\n[完成] 生成了 {len(report.insights)} 个洞察")
    print(f"[完成] 生成了 {len(report.recommendations)} 条建议")
    
    # 输出 Markdown 格式
    print("\n" + "=" * 80)
    print("Markdown 格式报告")
    print("=" * 80)
    markdown_report = report.to_markdown()
    print(markdown_report)
    
    # 输出 HTML 格式并保存
    print("\n" + "=" * 80)
    print("HTML 格式报告")
    print("=" * 80)
    html_report = report.to_html()
    
    # 保存到临时文件
    import tempfile
    import os
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
        f.write(html_report)
        temp_path = f.name
    
    print(f"[OK] HTML 报告已保存到: {temp_path}")
    print(f"[文件大小] {os.path.getsize(temp_path)} 字节")
    
    # 输出 JSON 格式
    print("\n" + "=" * 80)
    print("JSON 格式报告（摘要）")
    print("=" * 80)
    report_dict = report.to_dict()
    print(json.dumps(report_dict, ensure_ascii=False, indent=2)[:500] + "...")
    
    print("\n" + "=" * 80)
    print("[OK] 测试完成！")
    print("=" * 80)
