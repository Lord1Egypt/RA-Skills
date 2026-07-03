#!/usr/bin/env python3
"""
Web应用生成脚本 - 生成完整的可部署Web应用
集成所有组件和脚本，创建可直接部署的应用包
"""

import os
import sys
import json
import argparse
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime


class WebAppGenerator:
    """Web应用生成器"""

    def __init__(self, content_data: Dict[str, Any], template: str = 'default'):
        self.content = content_data
        self.template = template
        self.output_dir = None

    def generate_html(self) -> str:
        """生成HTML文件"""
        title = self.content.get('metadata', {}).get('title', '教材虚拟仿真系统')

        html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="基于教材的虚拟仿真系统">
    <title>{title} - 虚拟仿真系统</title>

    <!-- CSS -->
    <link rel="stylesheet" href="css/styles.css">

    <!-- 字体 -->
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet">

    <!-- 图标 -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">

    <!-- Three.js Import Map -->
    <script type="importmap">
    {{
        "imports": {{
            "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
            "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"
        }}
    }}
    </script>
</head>
<body>
    <div id="app">
        <!-- 导航栏 -->
        <header class="navbar">
            <div class="container">
                <div class="navbar-brand">
                    <i class="fas fa-atom"></i>
                    <h1>{title}</h1>
                </div>
                <nav class="navbar-nav">
                    <ul>
                        <li><a href="#scene" class="active"><i class="fas fa-cube"></i> 3D场景</a></li>
                        <li><a href="#quiz"><i class="fas fa-question-circle"></i> 测验</a></li>
                        <li><a href="#progress"><i class="fas fa-chart-line"></i> 进度</a></li>
                        <li><a href="#analytics"><i class="fas fa-chart-bar"></i> 数据分析</a></li>
                    </ul>
                </nav>
                <div class="navbar-toggle">
                    <button id="mobile-menu-btn">
                        <i class="fas fa-bars"></i>
                    </button>
                </div>
            </div>
        </header>

        <!-- 主内容区 -->
        <main class="main-content">
            <!-- 3D场景区域 -->
            <section id="scene-section" class="scene-section">
                <div class="scene-container" id="scene-container">
                    <!-- 3D场景渲染区域 -->
                </div>
                <div class="scene-controls">
                    <button id="reset-camera" title="重置视角">
                        <i class="fas fa-sync-alt"></i>
                    </button>
                    <button id="toggle-fullscreen" title="全屏模式">
                        <i class="fas fa-expand"></i>
                    </button>
                    <button id="screenshot" title="截图">
                        <i class="fas fa-camera"></i>
                    </button>
                </div>
            </section>

            <!-- 信息面板 -->
            <section id="info-panel" class="info-panel">
                <div class="panel-content">
                    <h2><i class="fas fa-info-circle"></i> 当前操作</h2>
                    <div id="current-action">
                        <p>选择一个对象开始操作</p>
                    </div>
                    <div id="step-guide">
                        <!-- 步骤指导 -->
                    </div>
                </div>
            </section>

            <!-- 测验区域 -->
            <section id="quiz-section" class="quiz-section">
                <div class="quiz-container">
                    <h2><i class="fas fa-clipboard-check"></i> 知识测验</h2>
                    <div id="quiz-content">
                        <!-- 测验内容 -->
                    </div>
                    <div class="quiz-controls">
                        <button id="prev-question"><i class="fas fa-arrow-left"></i> 上一题</button>
                        <button id="next-question">下一题 <i class="fas fa-arrow-right"></i></button>
                        <button id="submit-quiz">提交答案</button>
                    </div>
                </div>
            </section>

            <!-- 进度追踪 -->
            <section id="progress-section" class="progress-section">
                <div class="progress-container">
                    <h2><i class="fas fa-tasks"></i> 学习进度</h2>
                    <div class="progress-overview">
                        <div class="progress-item">
                            <span class="progress-label">完成度</span>
                            <div class="progress-bar">
                                <div class="progress-fill" id="completion-progress" style="width: 0%"></div>
                            </div>
                            <span class="progress-value" id="completion-value">0%</span>
                        </div>
                        <div class="progress-item">
                            <span class="progress-label">正确率</span>
                            <div class="progress-bar">
                                <div class="progress-fill" id="accuracy-progress" style="width: 0%"></div>
                            </div>
                            <span class="progress-value" id="accuracy-value">0%</span>
                        </div>
                    </div>
                    <div class="progress-details">
                        <canvas id="progress-chart"></canvas>
                    </div>
                </div>
            </section>

            <!-- 数据分析 -->
            <section id="analytics-section" class="analytics-section">
                <div class="analytics-container">
                    <h2><i class="fas fa-chart-bar"></i> 数据分析</h2>
                    <div class="analytics-dashboard">
                        <div class="analytics-card">
                            <h3>学习时长</h3>
                            <div id="time-spent">0分钟</div>
                        </div>
                        <div class="analytics-card">
                            <h3>操作次数</h3>
                            <div id="action-count">0次</div>
                        </div>
                        <div class="analytics-card">
                            <h3>得分统计</h3>
                            <div id="score-stats">0分</div>
                        </div>
                        <div class="analytics-card">
                            <h3>学习效率</h3>
                            <div id="efficiency-rating">--</div>
                        </div>
                    </div>
                    <div class="analytics-charts">
                        <canvas id="analytics-chart"></canvas>
                    </div>
                </div>
            </section>
        </main>

        <!-- 页脚 -->
        <footer class="footer">
            <div class="container">
                <p>&copy; 2024 {title} | 由WorkBuddy生成</p>
            </div>
        </footer>
    </div>

    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <!-- JavaScript -->
    <script type="module" src="js/main.js"></script>
</body>
</html>
'''

        return html_content

    def generate_css(self) -> str:
        """生成CSS样式"""
        return '''/* 教材虚拟仿真系统 - 主样式文件 */
/* 生成时间: 自动生成 */

:root {
    /* 颜色系统 */
    --primary-color: #3498db;
    --primary-dark: #2980b9;
    --primary-light: #5dade2;
    --secondary-color: #2ecc71;
    --accent-color: #e74c3c;
    --warning-color: #f39c12;
    --success-color: #27ae60;
    --info-color: #16a085;

    /* 中性色 */
    --background-color: #f5f7fa;
    --surface-color: #ffffff;
    --text-primary: #2c3e50;
    --text-secondary: #7f8c8d;
    --border-color: #ecf0f1;

    /* 间距系统 */
    --spacing-xs: 0.5rem;
    --spacing-sm: 1rem;
    --spacing-md: 2rem;
    --spacing-lg: 3rem;
    --spacing-xl: 4rem;

    /* 阴影 */
    --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.1);
    --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 20px rgba(0, 0, 0, 0.15);

    /* 圆角 */
    --radius-sm: 4px;
    --radius-md: 8px;
    --radius-lg: 12px;
    --radius-full: 9999px;

    /* 过渡 */
    --transition-fast: 0.15s ease;
    --transition-base: 0.3s ease;
    --transition-slow: 0.5s ease;
}

/* 基础重置 */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    line-height: 1.6;
    color: var(--text-primary);
    background-color: var(--background-color);
    overflow-x: hidden;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 var(--spacing-sm);
}

/* 导航栏样式 */
.navbar {
    background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
    color: white;
    padding: var(--spacing-sm) var(--spacing-md);
    box-shadow: var(--shadow-md);
    position: sticky;
    top: 0;
    z-index: 1000;
}

.navbar .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1200px;
    margin: 0 auto;
}

.navbar-brand {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
}

.navbar-brand i {
    font-size: 1.5rem;
}

.navbar-brand h1 {
    font-size: 1.25rem;
    font-weight: 700;
}

.navbar-nav ul {
    display: flex;
    list-style: none;
    gap: var(--spacing-md);
}

.navbar-nav a {
    color: white;
    text-decoration: none;
    padding: var(--spacing-xs) var(--spacing-sm);
    border-radius: var(--radius-sm);
    transition: var(--transition-fast);
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.navbar-nav a:hover,
.navbar-nav a.active {
    background: rgba(255, 255, 255, 0.2);
}

.navbar-toggle {
    display: none;
}

.navbar-toggle button {
    background: transparent;
    border: none;
    color: white;
    font-size: 1.5rem;
    cursor: pointer;
    padding: var(--spacing-xs);
}

/* 主内容区 */
.main-content {
    min-height: calc(100vh - 200px);
    padding: var(--spacing-md) 0;
}

/* 3D场景样式 */
.scene-section {
    margin: var(--spacing-md) auto;
    max-width: 1200px;
}

.scene-container {
    width: 100%;
    height: 60vh;
    background: #000;
    border-radius: var(--radius-lg);
    overflow: hidden;
    box-shadow: var(--shadow-lg);
    position: relative;
}

.scene-controls {
    position: absolute;
    bottom: var(--spacing-sm);
    right: var(--spacing-sm);
    display: flex;
    gap: var(--spacing-xs);
    z-index: 10;
}

.scene-controls button {
    background: rgba(255, 255, 255, 0.9);
    border: none;
    border-radius: var(--radius-sm);
    padding: var(--spacing-xs);
    cursor: pointer;
    transition: var(--transition-fast);
    box-shadow: var(--shadow-sm);
    font-size: 1rem;
}

.scene-controls button:hover {
    background: white;
    transform: translateY(-2px);
}

/* 信息面板样式 */
.info-panel {
    margin: var(--spacing-md) auto;
    max-width: 1200px;
}

.panel-content {
    background: var(--surface-color);
    padding: var(--spacing-md);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-md);
}

.panel-content h2 {
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
    margin-bottom: var(--spacing-md);
    color: var(--primary-color);
}

/* 测验区域样式 */
.quiz-section {
    margin: var(--spacing-md) auto;
    max-width: 1200px;
}

.quiz-container {
    background: var(--surface-color);
    padding: var(--spacing-md);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-md);
}

.quiz-container h2 {
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
    margin-bottom: var(--spacing-md);
    color: var(--primary-color);
}

.quiz-controls {
    display: flex;
    justify-content: center;
    gap: var(--spacing-md);
    margin-top: var(--spacing-md);
}

.quiz-controls button {
    padding: var(--spacing-sm) var(--spacing-md);
    border: none;
    border-radius: var(--radius-md);
    background: var(--primary-color);
    color: white;
    cursor: pointer;
    transition: var(--transition-fast);
    font-size: 1rem;
}

.quiz-controls button:hover {
    background: var(--primary-dark);
    transform: translateY(-2px);
}

.quiz-controls button:disabled {
    background: var(--text-secondary);
    cursor: not-allowed;
    transform: none;
}

/* 进度区域样式 */
.progress-section {
    margin: var(--spacing-md) auto;
    max-width: 1200px;
}

.progress-container {
    background: var(--surface-color);
    padding: var(--spacing-md);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-md);
}

.progress-container h2 {
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
    margin-bottom: var(--spacing-md);
    color: var(--primary-color);
}

.progress-overview {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-sm);
}

.progress-item {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
}

.progress-label {
    min-width: 100px;
    font-weight: 500;
}

.progress-bar {
    flex: 1;
    height: 24px;
    background: var(--border-color);
    border-radius: var(--radius-full);
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
    transition: width var(--transition-slow);
    border-radius: var(--radius-full);
}

.progress-value {
    min-width: 50px;
    text-align: right;
    font-weight: 700;
    color: var(--primary-color);
}

/* 数据分析样式 */
.analytics-section {
    margin: var(--spacing-md) auto;
    max-width: 1200px;
}

.analytics-container {
    background: var(--surface-color);
    padding: var(--spacing-md);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-md);
}

.analytics-container h2 {
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
    margin-bottom: var(--spacing-md);
    color: var(--primary-color);
}

.analytics-dashboard {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: var(--spacing-md);
    margin-bottom: var(--spacing-md);
}

.analytics-card {
    background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
    color: white;
    padding: var(--spacing-md);
    border-radius: var(--radius-md);
    text-align: center;
    box-shadow: var(--shadow-sm);
}

.analytics-card h3 {
    font-size: 0.9rem;
    margin-bottom: var(--spacing-xs);
    opacity: 0.9;
}

.analytics-card div {
    font-size: 2rem;
    font-weight: 700;
}

/* 页脚样式 */
.footer {
    background: var(--text-primary);
    color: white;
    padding: var(--spacing-md) var(--spacing-lg);
    margin-top: var(--spacing-xl);
    text-align: center;
}

.footer .container {
    max-width: 1200px;
    margin: 0 auto;
}

/* 响应式设计 */
@media (max-width: 768px) {
    .navbar-nav {
        display: none;
    }

    .navbar-toggle {
        display: block;
    }

    .scene-container {
        height: 50vh;
    }

    .analytics-dashboard {
        grid-template-columns: 1fr;
    }

    section {
        padding: var(--spacing-sm);
        margin: var(--spacing-sm);
    }
}

/* 动画效果 */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.scene-section,
.quiz-section,
.progress-section,
.analytics-section {
    animation: fadeIn 0.6s ease-out;
}

/* 交互反馈 */
.scene-container:active {
    cursor: grabbing;
}

button:active {
    transform: scale(0.95);
}

/* 加载动画 */
@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}

.loading {
    display: inline-block;
    width: 20px;
    height: 20px;
    border: 2px solid var(--border-color);
    border-top-color: var(--primary-color);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

/* 测验组件样式 */
.quiz-container {
    background: var(--surface-color);
    border-radius: var(--radius-lg);
    padding: var(--spacing-md);
    box-shadow: var(--shadow-md);
}

.question-item {
    margin-bottom: var(--spacing-md);
}

.question-item h3 {
    margin-bottom: var(--spacing-sm);
    color: var(--text-primary);
}

.options {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-xs);
}

.option-item {
    display: flex;
    align-items: center;
    padding: var(--spacing-xs) var(--spacing-sm);
    border: 2px solid var(--border-color);
    border-radius: var(--radius-sm);
    cursor: pointer;
    transition: var(--transition-fast);
}

.option-item:hover {
    border-color: var(--primary-color);
    background: rgba(52, 152, 219, 0.05);
}

.option-item input[type="radio"] {
    margin-right: var(--spacing-sm);
}

.option-item input[type="radio"]:checked + span {
    color: var(--primary-color);
    font-weight: 500;
}

.feedback {
    margin-top: var(--spacing-sm);
    padding: var(--spacing-sm);
    border-radius: var(--radius-sm);
    font-weight: 500;
}

.feedback.success {
    background: rgba(39, 174, 96, 0.1);
    color: var(--success-color);
}

.feedback.error {
    background: rgba(231, 76, 60, 0.1);
    color: var(--accent-color);
}

.feedback.warning {
    background: rgba(243, 156, 18, 0.1);
    color: var(--warning-color);
}

/* 进度追踪样式 */
.progress-tracker {
    background: var(--surface-color);
    border-radius: var(--radius-lg);
    padding: var(--spacing-md);
    box-shadow: var(--shadow-md);
}

.progress-bar-container {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
}

.progress-percentage {
    min-width: 50px;
    text-align: right;
    font-weight: 700;
    color: var(--primary-color);
}

.progress-milestones {
    margin-top: var(--spacing-md);
}

.progress-milestones ul {
    list-style: none;
    max-height: 200px;
    overflow-y: auto;
}

.progress-milestones li {
    padding: var(--spacing-xs);
    border-bottom: 1px solid var(--border-color);
}

.progress-milestones li:last-child {
    border-bottom: none;
}

.milestone-time {
    font-size: 0.85rem;
    color: var(--text-secondary);
}

/* 控制面板样式 */
.control-panel {
    background: var(--surface-color);
    border-radius: var(--radius-lg);
    padding: var(--spacing-md);
    box-shadow: var(--shadow-md);
}

.control-groups {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-md);
}

.control-group {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-sm);
}

.control-group h4 {
    color: var(--text-secondary);
    font-size: 0.9rem;
    margin-bottom: var(--spacing-xs);
}

.control-btn {
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
    padding: var(--spacing-sm) var(--spacing-md);
    border: 2px solid var(--border-color);
    border-radius: var(--radius-md);
    background: white;
    cursor: pointer;
    transition: var(--transition-fast);
    font-size: 1rem;
}

.control-btn:hover {
    border-color: var(--primary-color);
    color: var(--primary-color);
}

.control-btn.active {
    background: var(--primary-color);
    border-color: var(--primary-color);
    color: white;
}

/* 步骤指导样式 */
.step-guide {
    background: var(--surface-color);
    border-radius: var(--radius-lg);
    padding: var(--spacing-md);
    box-shadow: var(--shadow-md);
}

.step-content {
    margin-bottom: var(--spacing-md);
}

.current-step {
    padding: var(--spacing-md);
    background: rgba(52, 152, 219, 0.05);
    border-radius: var(--radius-md);
    border-left: 4px solid var(--primary-color);
}

.step-number {
    font-size: 0.85rem;
    color: var(--text-secondary);
    margin-bottom: var(--spacing-xs);
}

.step-instruction {
    font-size: 1.1rem;
    font-weight: 500;
    color: var(--text-primary);
}

.step-overview {
    margin-top: var(--spacing-md);
}

.step-overview h4 {
    margin-bottom: var(--spacing-sm);
    color: var(--text-secondary);
}

.step-overview ul {
    list-style: none;
    max-height: 150px;
    overflow-y: auto;
}

.step-item {
    padding: var(--spacing-xs);
    border-radius: var(--radius-sm);
    cursor: pointer;
    transition: var(--transition-fast);
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
}

.step-item:hover {
    background: rgba(52, 152, 219, 0.05);
}

.step-item.active {
    background: rgba(52, 152, 219, 0.1);
    border-left: 3px solid var(--primary-color);
}

.step-item.completed {
    color: var(--success-color);
}

.step-status {
    min-width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--border-color);
    border-radius: 50%;
    font-size: 0.85rem;
}

.step-item.completed .step-status {
    background: var(--success-color);
    color: white;
}

/* 数据分析面板样式 */
.analytics-dashboard {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: var(--spacing-md);
    margin-bottom: var(--spacing-md);
}

.analytics-card {
    background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
    color: white;
    padding: var(--spacing-md);
    border-radius: var(--radius-md);
    text-align: center;
    box-shadow: var(--shadow-sm);
}

.analytics-card h3 {
    font-size: 0.9rem;
    margin-bottom: var(--spacing-xs);
    opacity: 0.9;
}

.analytics-card div {
    font-size: 2rem;
    font-weight: 700;
}

.analytics-charts {
    margin-top: var(--spacing-md);
}

.chart-container {
    background: var(--surface-color);
    padding: var(--spacing-md);
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-sm);
}

.chart-container h4 {
    margin-bottom: var(--spacing-md);
    color: var(--text-secondary);
}

/* 反馈消息样式 */
.feedback-message {
    position: fixed;
    top: 20px;
    right: 20px;
    padding: var(--spacing-md);
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-lg);
    z-index: 9999;
    animation: slideIn 0.3s ease-out;
    max-width: 400px;
}

@keyframes slideIn {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

.feedback-message.success {
    background: var(--success-color);
    color: white;
}

.feedback-message.error {
    background: var(--accent-color);
    color: white;
}

.feedback-message.warning {
    background: var(--warning-color);
    color: white;
}

.feedback-content {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
}

.feedback-icon {
    font-size: 1.5rem;
}

.feedback-suggestions {
    margin-top: var(--spacing-sm);
    padding-top: var(--spacing-sm);
    border-top: 1px solid rgba(255, 255, 255, 0.2);
}

.feedback-suggestions li {
    font-size: 0.9rem;
    padding: var(--spacing-xs) 0;
}

/* 完成对话框样式 */
.completion-dialog {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 10000;
}

.completion-content {
    background: white;
    padding: var(--spacing-lg);
    border-radius: var(--radius-lg);
    text-align: center;
    max-width: 400px;
    box-shadow: var(--shadow-lg);
}

.completion-content h2 {
    color: var(--primary-color);
    margin-bottom: var(--spacing-md);
}

.completion-content button {
    background: var(--primary-color);
    color: white;
    border: none;
    padding: var(--spacing-sm) var(--spacing-md);
    border-radius: var(--radius-md);
    cursor: pointer;
    font-size: 1rem;
    margin-top: var(--spacing-md);
}

.completion-content button:hover {
    background: var(--primary-dark);
}
'''

    def generate_javascript(self) -> str:
        """生成JavaScript代码"""
        title = self.content.get('metadata', {}).get('title', '教材虚拟仿真系统')

        js_content = f'''// 教材虚拟仿真系统 - 主应用文件
// 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
// 系统名称: {title}

import SimulationScene from './scene.js';
import QuizComponent from './quiz.js';
import ProgressTracker from './progress.js';
import DataAnalyzer from './analytics.js';

class App {{
    constructor() {{
        this.scene = null;
        this.quiz = null;
        this.progress = null;
        this.analytics = null;
        this.contentData = {json.dumps(self.content, ensure_ascii=False)};
        this.initialized = false;
    }}

    async init() {{
        if (this.initialized) return;

        try {{
            console.log('正在初始化虚拟仿真系统...');

            // 初始化场景
            await this.initScene();

            // 初始化组件
            await this.initComponents();

            // 绑定事件
            await this.bindEvents();

            // 显示欢迎消息
            this.showWelcomeMessage();

            this.initialized = true;
            console.log('系统初始化完成！');

        }} catch (error) {{
            console.error('系统初始化失败:', error);
            this.showError('系统初始化失败，请刷新页面重试。');
        }}
    }}

    async initScene() {{
        const container = document.getElementById('scene-container');
        if (!container) {{
            console.error('场景容器不存在');
            return;
        }}

        try {{
            // 创建场景实例
            this.scene = new SimulationScene(container);

            // 等待场景加载完成
            await new Promise((resolve) => {{
                setTimeout(resolve, 100);
            }});

            console.log('3D场景初始化完成');

        }} catch (error) {{
            console.error('场景初始化失败:', error);
            throw error;
        }}
    }}

    async initComponents() {{
        try {{
            // 初始化测验组件
            const quizContainer = document.getElementById('quiz-content');
            if (quizContainer) {{
                this.quiz = new QuizComponent(this.contentData.quizQuestions || []);
                this.quiz.render(quizContainer);
                console.log('测验组件初始化完成');
            }}

            // 初始化进度追踪
            const progressContainer = document.getElementById('progress-container');
            if (progressContainer) {{
                this.progress = new ProgressTracker(this.contentData.totalSteps || 10);
                this.progress.render(progressContainer);
                console.log('进度追踪初始化完成');
            }}

            // 初始化数据分析
            const analyticsContainer = document.getElementById('analytics-container');
            if (analyticsContainer) {{
                this.analytics = new DataAnalyzer(this.contentData);
                this.analytics.render(analyticsContainer.id);
                console.log('数据分析初始化完成');
            }}

        }} catch (error) {{
            console.error('组件初始化失败:', error);
            throw error;
        }}
    }}

    async bindEvents() {{
        try {{
            // 绑定场景控制事件
            this.bindSceneControls();

            // 绑定导航事件
            this.bindNavigation();

            // 绑定窗口事件
            this.bindWindowEvents();

            // 绑定组件间通信
            this.bindComponentCommunication();

            console.log('事件绑定完成');

        }} catch (error) {{
            console.error('事件绑定失败:', error);
            throw error;
        }}
    }}

    bindSceneControls() {{
        // 重置相机
        const resetBtn = document.getElementById('reset-camera');
        if (resetBtn && this.scene) {{
            resetBtn.addEventListener('click', () => {{
                this.scene.resetCamera();
            }});
        }}

        // 全屏切换
        const fullscreenBtn = document.getElementById('toggle-fullscreen');
        if (fullscreenBtn && this.scene) {{
            fullscreenBtn.addEventListener('click', () => {{
                this.scene.toggleFullscreen();
            }});
        }}

        // 截图
        const screenshotBtn = document.getElementById('screenshot');
        if (screenshotBtn && this.scene) {{
            screenshotBtn.addEventListener('click', () => {{
                this.takeScreenshot();
            }});
        }}
    }}

    bindNavigation() {{
        // 平滑滚动到锚点
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{
                        behavior: 'smooth',
                        block: 'start'
                    }});

                    // 更新活动链接
                    document.querySelectorAll('.navbar-nav a').forEach(a => {{
                        a.classList.remove('active');
                    }});
                    this.classList.add('active');
                }}
            }});
        }});

        // 移动端菜单切换
        const mobileMenuBtn = document.getElementById('mobile-menu-btn');
        if (mobileMenuBtn) {{
            mobileMenuBtn.addEventListener('click', () => {{
                this.toggleMobileMenu();
            }});
        }}
    }}

    bindWindowEvents() {{
        // 窗口大小变化
        window.addEventListener('resize', () => {{
            if (this.scene) {{
                this.scene.onWindowResize();
            }}
        }});

        // 页面卸载前保存状态
        window.addEventListener('beforeunload', () => {{
            this.saveState();
        }});

        // 键盘快捷键
        window.addEventListener('keydown', (e) => {{
            this.handleKeyboard(e);
        }});
    }}

    bindComponentCommunication() {{
        // 测验完成 → 进度更新
        if (this.quiz && this.progress) {{
            this.quiz.container.addEventListener('quizCompleted', (e) => {{
                this.progress.addMilestone('测验完成', `得分: ${{e.detail.score}}, 正确率: ${{e.detail.percentage}}%`);
            }});
        }}

        // 答题记录 → 数据分析
        if (this.analytics) {{
            window.addEventListener('answerSubmitted', (e) => {{
                this.analytics.recordAction('quiz_answer', e.detail);
            }});
        }}

        // 步骤完成 → 进度更新
        if (this.progress) {{
            window.addEventListener('stepCompleted', (e) => {{
                this.progress.incrementProgress();
            }});
        }}
    }}

    showWelcomeMessage() {{
        const message = `
欢迎来到{title}！

本系统提供以下功能：
- 3D交互式场景
- 知识测验
- 学习进度追踪
- 数据分析

开始探索吧！
        `;

        this.showMessage(message, 'info');
    }}

    takeScreenshot() {{
        if (!this.scene || !this.scene.renderer) {{
            this.showMessage('场景未初始化，无法截图', 'error');
            return;
        }}

        try {{
            const canvas = this.scene.renderer.domElement;
            const link = document.createElement('a');
            link.download = `screenshot-${{Date.now()}}.png`;
            link.href = canvas.toDataURL('image/png');
            link.click();

            this.showMessage('截图已保存', 'success');
        }} catch (error) {{
            console.error('截图失败:', error);
            this.showMessage('截图失败', 'error');
        }}
    }}

    toggleMobileMenu() {{
        const nav = document.querySelector('.navbar-nav');
        nav.style.display = nav.style.display === 'flex' ? 'none' : 'flex';
    }}

    handleKeyboard(e) {{
        // ESC键退出全屏
        if (e.key === 'Escape') {{
            if (document.fullscreenElement) {{
                document.exitFullscreen();
            }}
        }}

        // Ctrl+R 重置场景
        if (e.ctrlKey && e.key === 'r') {{
            e.preventDefault();
            if (this.scene) {{
                this.scene.resetCamera();
            }}
        }}

        // Ctrl+S 保存状态
        if (e.ctrlKey && e.key === 's') {{
            e.preventDefault();
            this.saveState();
            this.showMessage('状态已保存', 'success');
        }}
    }}

    saveState() {{
        const state = {{
            timestamp: Date.now(),
            progress: this.progress ? this.progress.getProgress() : null,
            quiz: this.quiz ? this.quiz.getCurrentProgress() : null,
            analytics: this.analytics ? this.analytics.getReport() : null
        }};

        try {{
            localStorage.setItem('appState', JSON.stringify(state));
        }} catch (error) {{
            console.error('保存状态失败:', error);
        }}
    }}

    loadState() {{
        try {{
            const saved = localStorage.getItem('appState');
            if (saved) {{
                const state = JSON.parse(saved);
                console.log('加载保存的状态:', state);
                return state;
            }}
        }} catch (error) {{
            console.error('加载状态失败:', error);
        }}
        return null;
    }}

    showMessage(text, type = 'info') {{
        // 创建消息元素
        const message = document.createElement('div');
        message.className = `feedback-message ${{type}}`;
        message.innerHTML = `
            <div class="feedback-content">
                <span class="feedback-text">${{text}}</span>
                <button onclick="this.parentElement.parentElement.remove()">✕</button>
            </div>
        `;

        document.body.appendChild(message);

        // 自动消失
        setTimeout(() => {{
            message.remove();
        }}, 5000);
    }}

    showError(text) {{
        this.showMessage(text, 'error');
    }}

    getSystemInfo() {{
        return {{
            name: '{title}',
            version: '1.0.0',
            initialized: this.initialized,
            components: {{
                scene: !!this.scene,
                quiz: !!this.quiz,
                progress: !!this.progress,
                analytics: !!this.analytics
            }},
            state: this.loadState()
        }};
    }}

    dispose() {{
        console.log('正在清理资源...');

        // 清理场景
        if (this.scene) {{
            this.scene.dispose();
        }}

        // 清理组件
        if (this.progress) {{
            this.progress.dispose();
        }}

        // 清理分析器
        if (this.analytics) {{
            this.analytics.dispose();
        }}

        console.log('资源清理完成');
    }}
}}

// 启动应用
document.addEventListener('DOMContentLoaded', async () => {{
    const app = new App();
    await app.init();

    // 将app实例暴露到全局，便于调试
    window.app = app;

    console.log('应用已启动！');
    console.log('系统信息:', app.getSystemInfo());
}});

export default App;
'''

        return js_content

    def create_package_structure(self, output_dir: str) -> bool:
        """创建打包结构"""
        try:
            self.output_dir = Path(output_dir)
            self.output_dir.mkdir(parents=True, exist_ok=True)

            # 创建目录结构
            dirs = [
                'css',
                'js',
                'assets',
                'assets/models',
                'assets/textures'
            ]

            for dir_name in dirs:
                (self.output_dir / dir_name).mkdir(exist_ok=True)

            return True
        except Exception as e:
            self.error = f"创建目录结构失败: {str(e)}"
            return False

    def generate_deployment_config(self) -> Dict[str, Any]:
        """生成部署配置"""
        return {
            "name": self.content.get('metadata', {}).get('title', '教材虚拟仿真系统'),
            "version": "1.0.0",
            "description": "基于教材的虚拟仿真系统",
            "main": "index.html",
            "scripts": {
                "start": "python -m http.server 8000",
                "build": "echo 'Build complete'",
                "preview": "python -m http.server 8000"
            },
            "dependencies": {},
            "devDependencies": {},
            "keywords": [
                "education",
                "simulation",
                "3d",
                "web",
                "interactive"
            ],
            "author": "WorkBuddy",
            "license": "MIT"
        }

    def save_webapp(self, output_dir: str) -> bool:
        """保存完整的Web应用"""
        try:
            # 创建目录结构
            if not self.create_package_structure(output_dir):
                return False

            # 生成并保存文件
            files = {
                'index.html': self.generate_html(),
                'css/styles.css': self.generate_css(),
                'js/main.js': self.generate_javascript(),
                'package.json': json.dumps(self.generate_deployment_config(), indent=2),
                'README.md': self.generate_readme()
            }

            for file_path, content in files.items():
                full_path = self.output_dir / file_path
                full_path.parent.mkdir(parents=True, exist_ok=True)
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)

            return True
        except Exception as e:
            self.error = f"保存Web应用失败: {str(e)}"
            return False

    def generate_readme(self) -> str:
        """生成README文件"""
        title = self.content.get('metadata', {}).get('title', '教材虚拟仿真系统')
        return f'''# {title}

基于教材的虚拟仿真系统，由 WorkBuddy 自动生成。

## 功能特性

- 3D交互式场景
- 知识测验系统
- 学习进度追踪
- 数据分析与可视化
- 响应式设计

## 快速开始

### 本地运行

1. 使用 Python 服务器：
   ```bash
   python -m http.server 8000
   ```

2. 或使用 Node.js 服务器：
   ```bash
   npx http-server -p 8000
   ```

3. 在浏览器中访问：
   ```
   http://localhost:8000
   ```

### 部署

可以直接部署到任何静态网站托管服务：
- GitHub Pages
- Netlify
- Vercel
- 或其他 Web 服务器

## 系统要求

- 现代浏览器（Chrome, Firefox, Safari, Edge）
- WebGL 支持
- JavaScript 启用

## 技术栈

- **3D渲染**: Three.js
- **动画**: GSAP
- **数据可视化**: Chart.js
- **样式**: CSS3
- **脚本**: JavaScript (ES6+)

## 使用说明

1. **3D场景**: 使用鼠标拖动旋转视角，滚轮缩放
2. **知识测验**: 回答问题检查学习效果
3. **进度追踪**: 实时查看学习进度
4. **数据分析**: 查看学习数据和分析报告

## 快捷键

- `ESC`: 退出全屏
- `Ctrl+R`: 重置场景
- `Ctrl+S`: 保存状态

## 浏览器支持

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 许可证

MIT License

## 生成信息

- 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 生成工具: WorkBuddy
- 版本: 1.0.0

## 支持

如有问题，请检查浏览器控制台获取详细错误信息。
'''

    def generate_package(self, output_dir: str) -> bool:
        """生成部署包"""
        try:
            # 先生成所有文件
            if not self.save_webapp(output_dir):
                return False

            # 创建启动脚本
            start_script = '''@echo off
echo 启动虚拟仿真系统...
python -m http.server 8000
echo 服务器运行在 http://localhost:8000
pause
'''

            with open(self.output_dir / 'start.bat', 'w', encoding='utf-8') as f:
                f.write(start_script)

            # 创建Linux启动脚本
            start_script_linux = '''#!/bin/bash
echo "启动虚拟仿真系统..."
python3 -m http.server 8000
echo "服务器运行在 http://localhost:8000"
'''

            with open(self.output_dir / 'start.sh', 'w', encoding='utf-8') as f:
                f.write(start_script_linux)

            return True
        except Exception as e:
            self.error = f"生成部署包失败: {str(e)}"
            return False


def main():
    parser = argparse.ArgumentParser(
        description='Web应用生成脚本 - 生成完整的可部署Web应用',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 generate_webapp.py content.json --output dist/
  python3 generate_webapp.py content.json --template custom --output dist/
  python3 generate_webapp.py content.json --package --output simulation-package/
        """
    )

    parser.add_argument('content_file', help='教材内容JSON文件')
    parser.add_argument('--template', choices=['default', 'minimal', 'full'],
                        default='default',
                        help='应用模板类型')
    parser.add_argument('--package', action='store_true',
                        help='生成完整的部署包')
    parser.add_argument('--output', required=True,
                        help='输出目录路径')

    args = parser.parse_args()

    # 读取教材内容
    try:
        with open(args.content_file, 'r', encoding='utf-8') as f:
            content_data = json.load(f)
    except Exception as e:
        print(f"❌ 读取文件失败: {str(e)}", file=sys.stderr)
        sys.exit(1)

    # 创建Web应用生成器
    print(f"正在生成Web应用...")
    print(f"  模板: {args.template}")
    print(f"  部署包: {'是' if args.package else '否'}")
    generator = WebAppGenerator(content_data, args.template)

    # 生成Web应用
    print(f"正在生成应用到: {args.output}")
    if generator.generate_package(args.output):
        print(f"✅ Web应用生成成功！")
        print(f"  输出目录: {args.output}")
        print(f"  应用名称: {content_data.get('metadata', {}).get('title', '教材虚拟仿真系统')}")

        # 显示文件列表
        print(f"\n📁 生成的文件:")
        files = ['index.html', 'css/styles.css', 'js/main.js', 'package.json', 'README.md']
        if args.package:
            files.extend(['start.bat', 'start.sh'])

        for file in files:
            file_path = Path(args.output) / file
            if file_path.exists():
                size = file_path.stat().st_size
                print(f"  ✓ {file} ({size} bytes)")

        # 显示启动说明
        print(f"\n🚀 启动应用:")
        print(f"  Windows: 运行 {args.output}/start.bat")
        print(f"  Linux/Mac: 运行 {args.output}/start.sh")
        print(f"  手动: cd {args.output} && python -m http.server 8000")
        print(f"  然后访问: http://localhost:8000")
    else:
        print(f"❌ 生成失败: {generator.error}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()