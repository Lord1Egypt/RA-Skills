#!/usr/bin/env python3
"""
企业内部咨询工单统计分析脚本
用法: python analyze_tickets.py <工单Excel文件> [--date YYYY-MM-DD]

依赖: pip install pandas openpyxl
(可选 matplotlib 用于图表生成)
"""

import argparse
import pandas as pd
from datetime import datetime, timedelta
from collections import Counter
import sys
import os

# 尝试导入 matplotlib，失败则跳过图表生成
try:
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial Unicode MS', 'Noto Sans CJK SC']
    matplotlib.rcParams['axes.unicode_minus'] = False
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

# 功能模块关键词配置
MODULE_KEYWORDS = {
    '订单交易': ['订单', '支付', '退款', '下单', '交易', '订单查询', '付款', '取消订单'],
    '经营数据': ['报表', '销售额', '营收', '流水', '统计', '经营', '数据', '分析', '月报', '日报'],
    '门店设置': ['门店', '店铺', '营业时间', '地址', '配置', '门店配置', '营业', '闭店'],
    '账号管理': ['账号', '登录', '密码', '权限', '角色', '用户', '账户', '登录异常', '注册'],
    '商品管理': ['商品', '上架', '下架', '库存', 'SKU', '商品信息', '商品上架', '商品下架'],
    '营销活动': ['优惠券', '活动', '折扣', '满减', '推广', '优惠', '活动配置', '营销'],
    '顾客评价': ['评价', '评分', '评论', '星级', '反馈', '好评', '差评', '回复评价']
}

def classify_ticket(description):
    """根据关键词自动归类工单"""
    if pd.isna(description):
        return '其他'
    
    description = str(description)
    for module, keywords in MODULE_KEYWORDS.items():
        for keyword in keywords:
            if keyword in description:
                return module
    return '其他'

def load_data(file_path):
    """加载Excel数据"""
    try:
        # 支持 xlsx 和 csv
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
        return df
    except Exception as e:
        print(f"Error loading file: {e}")
        sys.exit(1)

def preprocess_data(df, target_date=None):
    """数据预处理"""
    # 转换时间列
    time_columns = ['提交时间', '回复时间', '创建时间']
    for col in time_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # 筛选目标日期的数据
    if target_date:
        target_date = pd.to_datetime(target_date)
        if '提交时间' in df.columns:
            df = df[df['提交时间'].dt.date == target_date.date()]
    
    return df

def calculate_metrics(df):
    """计算各项指标"""
    # 接收工单数
    total_received = len(df)
    
    # 已解决数
    if '状态' in df.columns:
        resolved_count = len(df[df['状态'].str.contains('已解决', na=False)])
    else:
        resolved_count = 0
    
    # 计算未及时回复（超过1小时未回复）
    overdue_count = 0
    if '提交时间' in df.columns and '回复时间' in df.columns:
        df['响应时长'] = df['回复时间'] - df['提交时间']
        
        # 超过1小时未回复的
        overdue = df[df['响应时长'] > timedelta(hours=1)]
        
        # 没有回复且超过1小时的（基于当前时间判断待处理）
        no_reply = df[
            (df['回复时间'].isna()) & 
            (pd.Timestamp.now() - df['提交时间'] > timedelta(hours=1))
        ]
        
        overdue_count = len(overdue) + len(no_reply)
    
    return {
        'total_received': total_received,
        'resolved': resolved_count,
        'overdue': overdue_count,
        'pending': total_received - resolved_count
    }

def classify_and_count(df):
    """分类统计"""
    if '问题描述' in df.columns:
        df['功能模块'] = df['问题描述'].apply(classify_ticket)
        module_counts = df['功能模块'].value_counts().to_dict()
    else:
        module_counts = {}
    return module_counts

def generate_charts(metrics, module_counts, df, output_dir='.'):
    """生成可视化图表"""
    charts = []
    
    if not HAS_MATPLOTLIB:
        print("⚠️ 跳过图表生成 (matplotlib 未安装)")
        return charts
    
    try:
        # 1. 核心指标卡片图
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.axis('off')
        
        labels = ['接收工单', '已解决', '未及时回复', '待处理']
        values = [metrics['total_received'], metrics['resolved'], 
                  metrics['overdue'], metrics['pending']]
        colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12']
        
        for i, (label, value, color) in enumerate(zip(labels, values, colors)):
            x = 0.2 + (i % 4) * 0.2
            ax.text(x, 0.6, str(value), fontsize=36, ha='center', 
                    fontweight='bold', color=color)
            ax.text(x, 0.35, label, fontsize=14, ha='center', color='#555')
        
        ax.set_title('今日工单概览', fontsize=18, fontweight='bold', pad=20)
        plt.tight_layout()
        
        chart_path = os.path.join(output_dir, 'metrics_overview.png')
        plt.savefig(chart_path, dpi=150, bbox_inches='tight', 
                    facecolor='white', edgecolor='none')
        plt.close()
        charts.append(chart_path)
        
        # 2. 功能模块分布饼图
        fig, ax = plt.subplots(figsize=(10, 8))
        
        if module_counts:
            labels = list(module_counts.keys())
            sizes = list(module_counts.values())
            
            non_zero = [(l, s) for l, s in zip(labels, sizes) if s > 0]
            if non_zero:
                labels, sizes = zip(*non_zero)
                colors = plt.cm.Set3(range(len(labels)))
                explode = [0.02] * len(labels)
                
                wedges, texts, autotexts = ax.pie(
                    sizes, labels=labels, autopct='%1.1f%%',
                    colors=colors, explode=explode, startangle=90,
                    textprops={'fontsize': 11}
                )
        
        ax.set_title('工单功能模块分布', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        chart_path = os.path.join(output_dir, 'module_distribution.png')
        plt.savefig(chart_path, dpi=150, bbox_inches='tight',
                    facecolor='white', edgecolor='none')
        plt.close()
        charts.append(chart_path)
        
        # 3. 问题关键词统计
        fig, ax = plt.subplots(figsize=(12, 6))
        
        all_keywords = []
        if '问题描述' in df.columns:
            for desc in df['问题描述'].dropna():
                for module, keywords in MODULE_KEYWORDS.items():
                    for keyword in keywords:
                        if keyword in str(desc):
                            all_keywords.append(keyword)
        
        keyword_counts = Counter(all_keywords).most_common(15)
        
        if keyword_counts:
            keywords, counts = zip(*keyword_counts)
            y_pos = range(len(keywords))
            
            bars = ax.barh(y_pos, counts, color='#3498db', alpha=0.8)
            ax.set_yticks(y_pos)
            ax.set_yticklabels(keywords)
            ax.invert_yaxis()
            ax.set_xlabel('出现次数')
            ax.set_title('高频问题关键词 Top 15', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        chart_path = os.path.join(output_dir, 'keyword_stats.png')
        plt.savefig(chart_path, dpi=150, bbox_inches='tight',
                    facecolor='white', edgecolor='none')
        plt.close()
        charts.append(chart_path)
        
    except Exception as e:
        print(f"⚠️ 图表生成失败: {e}")
    
    return charts

def generate_report(df, metrics, module_counts, charts, target_date, output_dir='.'):
    """生成每日摘要报告"""
    
    report_lines = []
    report_lines.append("=" * 60)
    report_lines.append("📊 企业内部咨询工单每日摘要")
    report_lines.append(f"📅 统计日期: {target_date}")
    report_lines.append("=" * 60)
    report_lines.append("")
    
    # 核心指标
    report_lines.append("📈 核心指标")
    report_lines.append("-" * 40)
    report_lines.append(f"  📥 接收工单总数: {metrics['total_received']}")
    report_lines.append(f"  ✅ 已解决: {metrics['resolved']}")
    report_lines.append(f"  ⏰ 未及时回复: {metrics['overdue']}")
    report_lines.append(f"  ⏳ 待处理: {metrics['pending']}")
    
    if metrics['total_received'] > 0:
        resolve_rate = metrics['resolved'] / metrics['total_received'] * 100
        overdue_rate = metrics['overdue'] / metrics['total_received'] * 100
        report_lines.append(f"  📊 解决率: {resolve_rate:.1f}%")
        report_lines.append(f"  ⚠️  超时率: {overdue_rate:.1f}%")
    
    report_lines.append("")
    
    # 功能模块分布
    report_lines.append("🏷️ 功能模块分布")
    report_lines.append("-" * 40)
    for module, count in sorted(module_counts.items(), key=lambda x: -x[1]):
        pct = count / metrics['total_received'] * 100 if metrics['total_received'] > 0 else 0
        report_lines.append(f"  {module}: {count} ({pct:.1f}%)")
    
    report_lines.append("")
    
    # 未及时回复工单列表
    report_lines.append("⚠️ 未及时回复工单详情")
    report_lines.append("-" * 40)
    
    if '提交时间' in df.columns and '回复时间' in df.columns:
        # 超过1小时未回复的
        overdue_tickets = df[df['响应时长'] > timedelta(hours=1)] if '响应时长' in df.columns else df.iloc[:0]
        
        # 没有回复且超过1小时的
        no_reply = df[
            (df['回复时间'].isna()) & 
            (pd.Timestamp.now() - df['提交时间'] > timedelta(hours=1))
        ] if '提交时间' in df.columns else df.iloc[:0]
        
        all_overdue = pd.concat([overdue_tickets, no_reply]).drop_duplicates()
        
        if len(all_overdue) > 0:
            for _, ticket in all_overdue.head(10).iterrows():
                ticket_id = ticket.get('工单编号', ticket.get('id', 'N/A'))
                desc = str(ticket.get('问题描述', ''))[:35]
                module = ticket.get('功能模块', classify_ticket(ticket.get('问题描述', '')))
                
                # 计算响应时长
                if pd.notna(ticket.get('响应时长')):
                    duration = ticket['响应时长']
                    duration_str = f"{duration.seconds//3600}h{(duration.seconds%3600)//60}m"
                else:
                    duration_str = "未回复"
                
                report_lines.append(f"  • [{ticket_id}] {desc}")
                report_lines.append(f"    模块: {module} | 响应时长: {duration_str}")
            
            if len(all_overdue) > 10:
                report_lines.append(f"  ... 还有 {len(all_overdue) - 10} 条未及时回复")
        else:
            report_lines.append("  ✅ 暂无未及时回复工单")
    
    report_lines.append("")
    report_lines.append("=" * 60)
    report_lines.append(f"📁 图表文件: {', '.join(charts) if charts else '无'}")
    report_lines.append("=" * 60)
    
    report_text = "\n".join(report_lines)
    
    # 保存报告
    report_path = os.path.join(output_dir, f'report_{target_date.replace("-", "")}.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    return report_text, report_path

def main():
    parser = argparse.ArgumentParser(description='企业内部咨询工单统计分析')
    parser.add_argument('file', help='工单Excel/CSV文件路径')
    parser.add_argument('--date', help='统计日期 (YYYY-MM-DD)', default=None)
    parser.add_argument('--output', '-o', help='输出目录', default='.')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        print(f"❌ 文件不存在: {args.file}")
        sys.exit(1)
    
    # 加载数据
    print(f"📂 加载数据: {args.file}")
    df = load_data(args.file)
    print(f"   共 {len(df)} 条记录")
    
    # 预处理
    print(f"🔄 预处理数据...")
    df = preprocess_data(df, args.date)
    print(f"   筛选后 {len(df)} 条")
    
    if len(df) == 0:
        print("⚠️ 没有找到目标日期的数据")
        target_date = args.date or datetime.now().strftime('%Y-%m-%d')
    else:
        target_date = args.date or df['提交时间'].iloc[0].strftime('%Y-%m-%d') if '提交时间' in df.columns else datetime.now().strftime('%Y-%m-%d')
    
    # 统计计算
    print("📊 计算指标...")
    metrics = calculate_metrics(df)
    
    # 分类统计
    print("🏷️ 分类统计...")
    module_counts = classify_and_count(df)
    
    # 生成图表
    print("📈 生成可视化图表...")
    charts = generate_charts(metrics, module_counts, df, args.output)
    
    # 生成报告
    print("📝 生成报告...")
    report_text, report_path = generate_report(
        df, metrics, module_counts, charts, target_date, args.output
    )
    
    # 输出报告
    print("\n" + report_text)
    print(f"\n✅ 报告已保存至: {report_path}")
    if charts:
        print(f"✅ 图表已保存至: {', '.join(charts)}")

if __name__ == '__main__':
    main()
