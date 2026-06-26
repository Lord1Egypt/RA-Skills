#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志分析系统 - 纯本地版本
Log Analysis System - Standalone Version
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict, Counter
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==================== 3个核心功能 ====================

CORE_FUNCTIONS = {
    "数据摄取诊断": {
        "icon": "📥",
        "description": "直接分析日志文件，检查数据采集和索引问题",
        "file_patterns": ["*.log", "*.txt"],
        "analysis": ["log_stats", "duplicate_check", "time_distribution"]
    },
    "索引性能优化": {
        "icon": "⚡",
        "description": "分析日志数据量、索引效率和查询性能",
        "file_patterns": ["*.log", "*.txt"],
        "analysis": ["volume_analysis", "indexing_efficiency", "storage_optimization"]
    },
    "错误与异常监控": {
        "icon": "🚨",
        "description": "识别错误模式、异常事件和问题趋势",
        "file_patterns": ["*.log", "*.txt", "*.csv"],
        "analysis": ["error_detection", "anomaly_detection", "trend_analysis"]
    }
}

# ==================== 日志解析器 ====================

class LogParser:
    """日志解析器"""
    
    @staticmethod
    def parse_line(line):
        """解析单行日志"""
        if not line.strip():
            return None
        
        # 通用日志模式匹配
        patterns = [
            r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]',  # 时间戳
            r'\[(ERROR|WARN|INFO|DEBUG|CRITICAL|FATAL)\]',  # 日志级别
            r'\[(?:DB_|APP_|NETWORK_|AUTH_|TIMEOUT_)ERROR\]',  # 错误类型
            r'IP:(\d+\.\d+\.\d+\.\d+)',  # IP 地址
            r'(?:SQL_INJECTION|XSS|BRUTE_FORCE|PATH_TRAVERSAL)',  # 攻击类型
            r'(?:CRITICAL|FATAL|ERROR)',  # 关键词
        ]
        
        parsed = {
            "timestamp": None,
            "level": None,
            "error_type": None,
            "ip": None,
            "attack_type": None,
            "is_critical": False,
            "raw": line
        }
        
        # 匹配模式
        for pattern in patterns:
            match = re.search(pattern, line)
            if not match:
                continue
            
            if "timestamp" in pattern:
                parsed["timestamp"] = match.group(1)
            elif "ERROR|WARN|INFO|DEBUG|CRITICAL|FATAL" in pattern:
                parsed["level"] = match.group(1)
            elif "DB_|APP_|NETWORK_|AUTH_|TIMEOUT_" in pattern:
                parsed["error_type"] = match.group(1)
            elif "IP:" in pattern:
                parsed["ip"] = match.group(1)
            elif "SQL_INJECTION|XSS|BRUTE_FORCE|PATH_TRAVERSAL" in pattern:
                parsed["attack_type"] = match.group(1)
            
            if "CRITICAL" in pattern or "FATAL" in pattern:
                parsed["is_critical"] = True
        
        return parsed

# ==================== 日志分析器 ====================

class LogAnalyzer:
    """日志分析器"""
    
    @staticmethod
    def get_log_files(directory, patterns):
        """获取日志文件列表"""
        log_files = []
        dir_path = Path(directory)
        
        if not dir_path.exists():
            return []
        
        for pattern in patterns:
            log_files.extend(dir_path.glob(pattern))
        
        return log_files
    
    @staticmethod
    def analyze_log_stats(log_files):
        """分析日志统计"""
        stats = {
            "total_files": len(log_files),
            "total_lines": 0,
            "file_sizes": [],
            "line_lengths": [],
            "time_distribution": {}
        }
        
        for log_file in log_files:
            try:
                file_size = log_file.stat().st_size
                stats["file_sizes"].append(file_size)
                
                with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                    line_count = 0
                    for line in f:
                        line_count += 1
                        
                        # 解析时间分布（按小时）
                        parsed = LogParser.parse_line(line)
                        if parsed and parsed["timestamp"]:
                            hour = parsed["timestamp"][:13]  # YYYY-MM-DD HH
                            stats["time_distribution"][hour] += 1
                        
                        stats["line_lengths"].append(len(line))
                
                stats["total_lines"] += line_count
            except Exception as e:
                continue
        
        return stats
    
    @staticmethod
    def check_duplicates(log_files):
        """检查重复日志"""
        duplicates = defaultdict(int)
        total_lines = 0
        
        for log_file in log_files:
            try:
                with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        total_lines += 1
                        line_hash = hash(line.strip())
                        duplicates[line_hash] += 1
            except Exception:
                continue
        
        # 找出重复次数最多的日志
        sorted_duplicates = sorted(duplicates.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "total_lines": total_lines,
            "unique_lines": len(duplicates),
            "duplicate_ratio": (total_lines - len(duplicates)) / total_lines if total_lines > 0 else 0,
            "top_duplicates": sorted_duplicates[:10]
        }
    
    @staticmethod
    def detect_errors(log_files):
        """检测错误"""
        errors = []
        error_stats = defaultdict(lambda: {
            "count": 0,
            "timestamps": []
        })
        
        for log_file in log_files:
            try:
                with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        parsed = LogParser.parse_line(line)
                        if parsed and parsed["level"] in ["ERROR", "CRITICAL", "FATAL"]:
                            errors.append({
                                "timestamp": parsed["timestamp"],
                                "level": parsed["level"],
                                "error_type": parsed["error_type"],
                                "ip": parsed["ip"],
                                "is_critical": parsed["is_critical"],
                                "raw": parsed["raw"]
                            })
                            
                            if parsed["error_type"]:
                                error_stats[parsed["error_type"]]["count"] += 1
                                if parsed["timestamp"]:
                                    error_stats[parsed["error_type"]]["timestamps"].append(parsed["timestamp"])
            except Exception:
                continue
        
        return {
            "total_errors": len(errors),
            "error_stats": error_stats,
            "recent_errors": errors[-100:]  # 最近100个错误
        }
    
    @staticmethod
    def detect_anomalies(log_files):
        """检测异常"""
        # 基于时间戳分析异常
        timestamps = []
        
        for log_file in log_files:
            try:
                with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        parsed = LogParser.parse_line(line)
                        if parsed and parsed["timestamp"]:
                            timestamps.append(parsed["timestamp"])
            except Exception:
                continue
        
        # 按小时统计事件数量
        hourly_counts = defaultdict(int)
        for ts in timestamps:
            hour = ts[:13]  # YYYY-MM-DD HH
            hourly_counts[hour] += 1
        
        # 找出异常（偏离平均值超过2个标准差）
        if hourly_counts:
            counts = list(hourly_counts.values())
            if len(counts) > 1:
                avg_count = sum(counts) / len(counts)
                if len(counts) > 2:
                    std_dev = (sum([(c - avg_count) ** 2 for c in counts]) / len(counts)) ** 0.5
                    anomalies = []
                    
                    for hour, count in hourly_counts.items():
                        if abs(count - avg_count) > 2 * std_dev:
                            anomalies.append({
                                "hour": hour,
                                "count": count,
                                "deviation": count - avg_count
                            })
                    
                    return anomalies
        
        return []

# ==================== 结果展示器 ====================

class ResultDisplay:
    """结果展示器"""
    
    @staticmethod
    def display_stats(stats):
        """显示统计信息"""
        st.markdown("### 📊 日志统计")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("总文件数", stats["total_files"])
        
        with col2:
            total_size_mb = sum(stats["file_sizes"]) / (1024 * 1024)
            st.metric("总大小", f"{total_size_mb:.2f} MB")
        
        with col3:
            st.metric("总行数", f"{stats['total_lines']:,}")
        
        st.markdown("---")
        
        # 时间分布
        if stats["time_distribution"]:
            st.markdown("### 📅 时间分布（按小时）")
            hours = sorted(stats["time_distribution"].keys())
            counts = [stats["time_distribution"][h] for h in hours]
            
            df_time = pd.DataFrame({
                "小时": hours,
                "日志数": counts
            })
            
            fig_time = px.bar(df_time, x="小时", y="日志数", title="日志时间分布")
            st.plotly_chart(fig_time, width='content')
    
    @staticmethod
    def display_duplicates(duplicate_info):
        """显示重复信息"""
        st.markdown("### 🔄 重复日志分析")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("总行数", f"{duplicate_info['total_lines']:,}")
        
        with col2:
            st.metric("唯一行数", f"{duplicate_info['unique_lines']:,}")
        
        with col3:
            ratio = duplicate_info["duplicate_ratio"] * 100
            st.metric("重复率", f"{ratio:.2f}%")
        
        # Top 重复日志
        if duplicate_info["top_duplicates"]:
            st.markdown("### 🔝 最重复的日志")
            
            df_dup = pd.DataFrame(duplicate_info["top_duplicates"], columns=["哈希值", "重复次数"])
            st.dataframe(df_dup, width='content', hide_index=True)
    
    @staticmethod
    def display_errors(error_info):
        """显示错误信息"""
        st.markdown(f"### ❌ 错误检测（共 {error_info['total_errors']} 个）")
        
        # 错误类型统计
        st.markdown("#### 错误类型分布")
        
        error_types = []
        counts = []
        
        for error_type, data in error_info["error_stats"].items():
            error_types.append(error_type)
            counts.append(data["count"])
        
        if error_types:
            df_errors = pd.DataFrame({
                "错误类型": error_types,
                "数量": counts
            })
            
            fig_errors = px.pie(df_errors, values="数量", names="错误类型", title="错误类型分布")
            st.plotly_chart(fig_errors, width='content')
        
        # 最近错误
        if error_info["recent_errors"]:
            st.markdown("#### 最近错误（最新20个）")
            
            df_recent = pd.DataFrame(error_info["recent_errors"][-20:])
            st.dataframe(df_recent, width='content', hide_index=True, height=400)
    
    @staticmethod
    def display_anomalies(anomalies):
        """显示异常"""
        if not anomalies:
            st.markdown("### 📉 异常检测")
            st.info("✅ 未检测到明显的时间异常")
            return
        
        st.markdown("### 📉 异常检测")
        st.markdown(f"发现 {len(anomalies)} 个时间异常：")
        
        df_anomalies = pd.DataFrame(anomalies)
        st.dataframe(df_anomalies, width='content', hide_index=True)
        
        # 异常可视化
        df_anomalies["deviation"] = df_anomalies["deviation"].abs()
        
        fig_anomalies = px.scatter(
            df_anomalies,
            x="hour",
            y="count",
            color="deviation",
            title="时间异常分布",
            size="deviation"
        )
        
        st.plotly_chart(fig_anomalies, width='content')

# ==================== 主函数 ====================

def main():
    """主函数"""
    
    # ==================== 页面配置 ====================
    st.set_page_config(
        page_title="日志分析系统",
        page_icon="📊",
        layout="wide"
    )
    
    # ==================== 标题 ====================
    st.title("📊 日志分析系统")
    st.markdown("✨ 本地日志文件分析工具 - 无需外部连接")
    st.markdown("---")
    
    # ==================== 侧边栏配置 ====================
    st.sidebar.title("⚙️ 配置")
    
    # 日志目录选择
    log_dir = st.sidebar.text_input("日志目录", value="/Users/godyoung/splunk/logs")
    
    # 文件模式选择
    file_patterns = st.sidebar.multiselect(
        "文件模式",
        ["*.log", "*.txt", "*.csv"],
        default=["*.log", "*.txt"]
    )
    
    # 最大文件数
    max_files = st.sidebar.slider("最大分析文件数", min_value=1, max_value=100, value=50)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📋 分析选项")
    
    # 显示选项
    show_charts = st.sidebar.checkbox("显示图表", value=True)
    show_duplicates = st.sidebar.checkbox("显示重复分析", value=True)
    
    # ==================== 3个核心功能按钮 ====================
    st.subheader("📋 选择分析功能")
    st.markdown("点击下方按钮开始日志文件分析：")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📥 数据摄取诊断")
        st.markdown("**功能**: 日志统计、重复检测、时间分析")
        st.markdown("- 总行数统计")
        st.markdown("- 重复日志识别")
        st.markdown("- 时间分布分析")
        
        if st.button("🚀 开始分析", key="data_ingestion", type="primary", width='content'):
            st.session_state.active_function = "数据摄取诊断"
    
    with col2:
        st.markdown("### ⚡ 索引性能优化")
        st.markdown("**功能**: 错误检测、异常分析、性能评估")
        st.markdown("- 错误类型统计")
        st.markdown("- 异常模式识别")
        st.markdown("- 关键错误定位")
        
        if st.button("🚀 开始分析", key="index_performance", type="primary", width='content'):
            st.session_state.active_function = "索引性能优化"
    
    with col3:
        st.markdown("### 🚨 错误与异常监控")
        st.markdown("**功能**: 错误追踪、异常识别、趋势分析")
        st.markdown("- 错误日志提取")
        st.markdown("- 异常事件识别")
        st.markdown("- 错误趋势图")
        
        if st.button("🚀 开始分析", key="error_monitoring", type="primary", width='content'):
            st.session_state.active_function = "错误与异常监控"
    
    # ==================== 显示分析结果 ====================
    st.markdown("---")
    
    if hasattr(st.session_state, 'active_function'):
        active_function = st.session_state.active_function
        
        # 获取日志文件
        log_files = LogAnalyzer.get_log_files(log_dir, file_patterns)
        
        if not log_files:
            st.warning(f"⚠️ 在目录 `{log_dir}` 中未找到匹配的日志文件")
            return
        
        # 限制文件数量
        log_files = log_files[:max_files]
        
        st.info(f"📁 分析 {len(log_files)} 个日志文件")
        
        if active_function == "数据摄取诊断":
            st.markdown("## 📥 数据摄取诊断")
            
            # 日志统计
            stats = LogAnalyzer.analyze_log_stats(log_files)
            ResultDisplay.display_stats(stats)
            
            # 重复检测
            if show_duplicates:
                duplicate_info = LogAnalyzer.check_duplicates(log_files)
                ResultDisplay.display_duplicates(duplicate_info)
        
        elif active_function == "索引性能优化":
            st.markdown("## ⚡ 索引性能优化")
            
            # 日志统计
            stats = LogAnalyzer.analyze_log_stats(log_files)
            ResultDisplay.display_stats(stats)
            
            # 错误检测
            error_info = LogAnalyzer.detect_errors(log_files)
            ResultDisplay.display_errors(error_info)
        
        elif active_function == "错误与异常监控":
            st.markdown("## 🚨 错误与异常监控")
            
            # 错误检测
            error_info = LogAnalyzer.detect_errors(log_files)
            ResultDisplay.display_errors(error_info)
            
            # 异常检测
            anomalies = LogAnalyzer.detect_anomalies(log_files)
            ResultDisplay.display_anomalies(anomalies)
        
        else:
            st.warning("⚠️ 未找到功能配置")
    else:
        st.info("💡 请点击上方 3 个分析功能按钮之一开始分析日志文件")
        
        # 显示所有功能概览
        st.markdown("---")
        st.markdown("### 📊 所有功能概览")
        
        for function_name, function_info in CORE_FUNCTIONS.items():
            with st.expander(f"{function_info['icon']} {function_name}"):
                st.markdown(f"**功能说明**: {function_info['description']}")
                st.markdown(f"**文件模式**: {', '.join(function_info['file_patterns'])}")
                st.markdown(f"**分析类型**: {', '.join(function_info['analysis'])}")
    
    # ==================== 底部状态 ====================
    st.markdown("---")
    col_left, col_right = st.columns([3, 1])
    
    with col_left:
        st.info(f"📅 当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        st.info(f"📁 日志目录: {log_dir}")
    
    with col_right:
        st.markdown('<span style="color: green; font-weight: bold;">✅</span> 系统正常运行（纯本地模式）', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
