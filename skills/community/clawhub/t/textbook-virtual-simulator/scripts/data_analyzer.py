#!/usr/bin/env python3
"""
数据分析脚本 - 实现学习数据分析功能
支持用户操作追踪、学习指标计算、数据可视化
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime


class DataAnalyzer:
    """数据分析器"""

    def __init__(self, content_data: Dict[str, Any]):
        self.content = content_data
        self.actions = []
        self.metrics = {}
        self.startTime = datetime.now()

    def track_user_actions(self) -> str:
        """追踪用户操作"""
        return '''// 用户操作追踪

class ActionTracker {
    constructor() {
        this.actions = [];
        this.sessionStartTime = Date.now();
        this.sessionId = this.generateSessionId();
        this.maxActions = 1000; // 最大存储操作数

        // 恢复之前的会话（如果有）
        this._loadSession();
    }

    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    getSessionId() {
        return this.sessionId;
    }

    logAction(actionType, details = {}) {
        const action = {
            type: actionType,
            timestamp: Date.now(),
            details: details,
            sessionId: this.sessionId,
            page: window.location.pathname
        };

        this.actions.push(action);

        // 限制存储的操作数量
        if (this.actions.length > this.maxActions) {
            this.actions.shift();
        }

        // 保存到本地存储
        this.saveToLocalStorage();

        // 触发事件
        this._dispatchEvent('actionLogged', action);
    }

    getActionsByType(actionType) {
        return this.actions.filter(action => action.type === actionType);
    }

    getActionsInTimeRange(startTime, endTime) {
        return this.actions.filter(action =>
            action.timestamp >= startTime && action.timestamp <= endTime
        );
    }

    getRecentActions(count = 10) {
        return this.actions.slice(-count);
    }

    saveToLocalStorage() {
        try {
            const data = {
                sessionId: this.sessionId,
                sessionStartTime: this.sessionStartTime,
                actions: this.actions
            };
            localStorage.setItem('userActions', JSON.stringify(data));
        } catch (error) {
            console.error('保存用户操作失败:', error);
        }
    }

    _loadSession() {
        try {
            const saved = localStorage.getItem('userActions');
            if (saved) {
                const data = JSON.parse(saved);
                // 如果会话时间在24小时内，恢复会话
                if (Date.now() - data.sessionStartTime < 24 * 60 * 60 * 1000) {
                    this.sessionId = data.sessionId;
                    this.sessionStartTime = data.sessionStartTime;
                    this.actions = data.actions || [];
                }
            }
        } catch (error) {
            console.error('加载会话失败:', error);
        }
    }

    clearSession() {
        this.actions = [];
        this.sessionStartTime = Date.now();
        this.sessionId = this.generateSessionId();
        localStorage.removeItem('userActions');
    }

    exportData(format = 'json') {
        const data = {
            sessionId: this.sessionId,
            sessionStartTime: this.sessionStartTime,
            exportTime: Date.now(),
            totalActions: this.actions.length,
            actions: this.actions
        };

        if (format === 'json') {
            return JSON.stringify(data, null, 2);
        } else if (format === 'csv') {
            return this._convertToCSV(data);
        }
    }

    _convertToCSV(data) {
        if (data.actions.length === 0) return '';

        const headers = ['Type', 'Timestamp', 'Details', 'SessionId', 'Page'];
        const rows = data.actions.map(action => [
            action.type,
            new Date(action.timestamp).toISOString(),
            JSON.stringify(action.details),
            action.sessionId,
            action.page
        ]);

        return [headers, ...rows].map(row => row.join(',')).join('\\n');
    }

    getAnalyticsReport() {
        const actionTypes = this._getActionTypesSummary();
        const timeDistribution = this._getTimeDistribution();
        const errorRate = this._calculateErrorRate();

        return {
            sessionId: this.sessionId,
            totalActions: this.actions.length,
            sessionDuration: Date.now() - this.sessionStartTime,
            actionTypes: actionTypes,
            timeDistribution: timeDistribution,
            errorRate: errorRate,
            recentActions: this.getRecentActions(5)
        };
    }

    _getActionTypesSummary() {
        const summary = {};
        this.actions.forEach(action => {
            if (!summary[action.type]) {
                summary[action.type] = {
                    count: 0,
                    percentage: 0
                };
            }
            summary[action.type].count++;
        });

        // 计算百分比
        Object.keys(summary).forEach(type => {
            summary[type].percentage = (
                (summary[type].count / this.actions.length) * 100
            ).toFixed(2);
        });

        return summary;
    }

    _getTimeDistribution() {
        const distribution = {
            first_hour: 0,
            first_10_minutes: 0,
            last_10_minutes: 0
        };

        const sessionDuration = Date.now() - this.sessionStartTime;

        this.actions.forEach(action => {
            const actionTime = action.timestamp - this.sessionStartTime;
            if (actionTime < 60 * 60 * 1000) { // 1小时内
                distribution.first_hour++;
            }
            if (actionTime < 10 * 60 * 1000) { // 前10分钟
                distribution.first_10_minutes++;
            }
            if (actionTime > sessionDuration - 10 * 60 * 1000) { // 最后10分钟
                distribution.last_10_minutes++;
            }
        });

        return distribution;
    }

    _calculateErrorRate() {
        const errorActions = this.actions.filter(action =>
            action.details && action.details.error
        );
        return (errorActions.length / this.actions.length * 100).toFixed(2);
    }

    _dispatchEvent(eventName, data) {
        const event = new CustomEvent(eventName, { detail: data });
        window.dispatchEvent(event);
    }
}

export default ActionTracker;
'''

    def calculate_learning_metrics(self) -> str:
        """计算学习指标"""
        return '''// 学习指标计算

class LearningMetrics {
    constructor(actionTracker) {
        this.tracker = actionTracker;
        this.quizResults = [];
        this.stepProgress = [];
    }

    addQuizResult(result) {
        this.quizResults.push({
            timestamp: Date.now(),
            ...result
        });
        this._saveMetrics();
    }

    addStepProgress(progress) {
        this.stepProgress.push({
            timestamp: Date.now(),
            ...progress
        });
        this._saveMetrics();
    }

    calculateAccuracy() {
        if (this.quizResults.length === 0) return 0;

        const totalCorrect = this.quizResults.reduce((sum, result) => {
            return sum + (result.isCorrect ? 1 : 0);
        }, 0);

        const totalQuestions = this.quizResults.reduce((sum, result) => {
            return sum + (result.totalQuestions || 1);
        }, 0);

        return (totalCorrect / totalQuestions * 100).toFixed(2);
    }

    calculateCompletionRate() {
        if (this.stepProgress.length === 0) return 0;

        const latestProgress = this.stepProgress[this.stepProgress.length - 1];
        const percentage = latestProgress.percentage || latestProgress.completedSteps / latestProgress.totalSteps * 100;

        return parseFloat(percentage).toFixed(2);
    }

    calculateEngagementScore() {
        // 计算参与度评分
        const actions = this.tracker.getAnalyticsReport();
        const actionDensity = actions.totalActions / (actions.sessionDuration / 1000 / 60); // 每分钟操作数

        let engagementScore = 0;

        // 操作密度评分 (0-30分)
        if (actionDensity > 5) engagementScore += 30;
        else if (actionDensity > 2) engagementScore += 20;
        else if (actionDensity > 1) engagementScore += 10;

        // 准确率评分 (0-30分)
        const accuracy = parseFloat(this.calculateAccuracy());
        engagementScore += accuracy * 0.3;

        // 完成率评分 (0-30分)
        const completion = parseFloat(this.calculateCompletionRate());
        engagementScore += completion * 0.3;

        // 持续时间评分 (0-10分)
        const durationHours = actions.sessionDuration / 1000 / 60 / 60;
        if (durationHours > 1) engagementScore += 10;
        else if (durationHours > 0.5) engagementScore += 7;
        else if (durationHours > 0.25) engagementScore += 5;

        return Math.min(100, Math.max(0, engagementScore)).toFixed(2);
    }

    calculateEfficiency() {
        if (this.quizResults.length === 0) return 0;

        // 计算效率：正确答案所需时间
        const correctActions = this.tracker.getActionsByType('quiz_answer').filter(
            action => action.details.isCorrect
        );

        const totalTime = this.tracker.getAnalyticsReport().sessionDuration;
        const efficiency = correctActions.length / (totalTime / 1000 / 60); // 每分钟正确答案数

        return efficiency.toFixed(2);
    }

    calculateImprovementTrend() {
        if (this.quizResults.length < 2) return {
            trend: 'insufficient_data',
            improvement: 0
        };

        // 计算前半段和后半段的准确率
        const midPoint = Math.floor(this.quizResults.length / 2);
        const firstHalf = this.quizResults.slice(0, midPoint);
        const secondHalf = this.quizResults.slice(midPoint);

        const firstHalfAccuracy = this._calculateBatchAccuracy(firstHalf);
        const secondHalfAccuracy = this._calculateBatchAccuracy(secondHalf);

        const improvement = secondHalfAccuracy - firstHalfAccuracy;

        return {
            trend: improvement > 0 ? 'improving' : 'declining',
            improvement: improvement.toFixed(2),
            firstHalfAccuracy: firstHalfAccuracy.toFixed(2),
            secondHalfAccuracy: secondHalfAccuracy.toFixed(2)
        };
    }

    _calculateBatchAccuracy(results) {
        const totalCorrect = results.reduce((sum, result) => {
            return sum + (result.isCorrect ? 1 : 0);
        }, 0);

        const totalQuestions = results.reduce((sum, result) => {
            return sum + (result.totalQuestions || 1);
        }, 0);

        return totalCorrect / totalQuestions * 100;
    }

    generateLearningReport() {
        return {
            timestamp: Date.now(),
            sessionId: this.tracker.getSessionId(),

            accuracy: this.calculateAccuracy(),
            completionRate: this.calculateCompletionRate(),
            engagementScore: this.calculateEngagementScore(),
            efficiency: this.calculateEfficiency(),

            improvementTrend: this.calculateImprovementTrend(),

            timeSpent: this.tracker.getAnalyticsReport().sessionDuration,
            totalActions: this.tracker.getAnalyticsReport().totalActions,

            quizResults: this.quizResults,
            stepProgress: this.stepProgress,

            recommendations: this.generateRecommendations()
        };
    }

    generateRecommendations() {
        const recommendations = [];

        // 基于准确率的建议
        const accuracy = parseFloat(this.calculateAccuracy());
        if (accuracy < 60) {
            recommendations.push({
                type: 'accuracy',
                priority: 'high',
                message: '准确率较低，建议重新学习基础知识点'
            });
        } else if (accuracy < 80) {
            recommendations.push({
                type: 'accuracy',
                priority: 'medium',
                message: '准确率良好，建议加强薄弱环节'
            });
        }

        // 基于完成率的建议
        const completion = parseFloat(this.calculateCompletionRate());
        if (completion < 50) {
            recommendations.push({
                type: 'completion',
                priority: 'high',
                message: '完成度较低，建议集中时间完成学习'
            });
        }

        // 基于参与度的建议
        const engagement = parseFloat(this.calculateEngagementScore());
        if (engagement < 50) {
            recommendations.push({
                type: 'engagement',
                priority: 'medium',
                message: '参与度较低，建议增加互动和练习'
            });
        }

        // 基于改进趋势的建议
        const trend = this.calculateImprovementTrend();
        if (trend.trend === 'declining') {
            recommendations.push({
                type: 'trend',
                priority: 'high',
                message: '学习效果有所下降，建议调整学习方法'
            });
        } else if (trend.trend === 'improving') {
            recommendations.push({
                type: 'trend',
                priority: 'low',
                message: '学习效果持续提升，继续保持！'
            });
        }

        return recommendations;
    }

    _saveMetrics() {
        try {
            const data = {
                quizResults: this.quizResults,
                stepProgress: this.stepProgress
            };
            localStorage.setItem('learningMetrics', JSON.stringify(data));
        } catch (error) {
            console.error('保存学习指标失败:', error);
        }
    }

    _loadMetrics() {
        try {
            const saved = localStorage.getItem('learningMetrics');
            if (saved) {
                const data = JSON.parse(saved);
                this.quizResults = data.quizResults || [];
                this.stepProgress = data.stepProgress || [];
            }
        } catch (error) {
            console.error('加载学习指标失败:', error);
        }
    }

    exportMetrics(format = 'json') {
        const report = this.generateLearningReport();

        if (format === 'json') {
            return JSON.stringify(report, null, 2);
        } else if (format === 'csv') {
            return this._convertReportToCSV(report);
        }
    }

    _convertReportToCSV(report) {
        const headers = ['Metric', 'Value'];
        const rows = [
            ['Accuracy', report.accuracy + '%'],
            ['Completion Rate', report.completionRate + '%'],
            ['Engagement Score', report.engagementScore],
            ['Efficiency', report.efficiency],
            ['Time Spent (seconds)', Math.floor(report.timeSpent / 1000)],
            ['Total Actions', report.totalActions]
        ];

        return [headers, ...rows].map(row => row.join(',')).join('\\n');
    }

    reset() {
        this.quizResults = [];
        this.stepProgress = [];
        localStorage.removeItem('learningMetrics');
    }
}

export default LearningMetrics;
'''

    def create_visualization(self) -> str:
        """创建数据可视化"""
        return '''// 数据可视化组件

class DataVisualization {
    constructor(data) {
        this.data = data;
        this.charts = {};
    }

    render(containerId) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error('容器不存在:', containerId);
            return;
        }

        container.innerHTML = `
            <div class="analytics-dashboard">
                <h3>数据分析</h3>
                <div class="analytics-cards">
                    <div class="analytics-card">
                        <h4>学习时长</h4>
                        <div class="card-value" id="time-spent">0分钟</div>
                    </div>
                    <div class="analytics-card">
                        <h4>操作次数</h4>
                        <div class="card-value" id="action-count">0次</div>
                    </div>
                    <div class="analytics-card">
                        <h4>准确率</h4>
                        <div class="card-value" id="accuracy">0%</div>
                    </div>
                    <div class="analytics-card">
                        <h4>完成率</h4>
                        <div class="card-value" id="completion">0%</div>
                    </div>
                </div>
                <div class="analytics-charts">
                    <div class="chart-container">
                        <h4>进度变化趋势</h4>
                        <canvas id="progress-chart"></canvas>
                    </div>
                    <div class="chart-container">
                        <h4>操作类型分布</h4>
                        <canvas id="action-distribution"></canvas>
                    </div>
                </div>
                <div class="analytics-recommendations">
                    <h4>学习建议</h4>
                    <ul id="recommendations"></ul>
                </div>
            </div>
        `;

        this.updateDashboard();
    }

    updateDashboard(data = null) {
        if (data) {
            this.data = data;
        }

        this._updateCards();
        this._createProgressChart();
        this._createActionDistributionChart();
        this._showRecommendations();
    }

    _updateCards() {
        // 学习时长
        const timeSpent = Math.floor(this.data.timeSpent / 1000 / 60);
        document.getElementById('time-spent').textContent = timeSpent + '分钟';

        // 操作次数
        document.getElementById('action-count').textContent = this.data.totalActions + '次';

        // 准确率
        document.getElementById('accuracy').textContent = this.data.accuracy + '%';

        // 完成率
        document.getElementById('completion').textContent = this.data.completionRate + '%';
    }

    _createProgressChart() {
        const canvas = document.getElementById('progress-chart');
        if (!canvas) return;

        // 模拟进度数据
        const progressData = this._generateProgressData();

        // 创建图表
        const chart = new Chart(canvas, {
            type: 'line',
            data: {
                labels: progressData.labels,
                datasets: [{
                    label: '完成进度',
                    data: progressData.values,
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    tension: 0.1,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                }
            }
        });

        this.charts.progress = chart;
    }

    _generateProgressData() {
        // 根据实际数据生成进度变化
        const data = {
            labels: [],
            values: []
        };

        if (this.data.stepProgress && this.data.stepProgress.length > 0) {
            this.data.stepProgress.forEach((progress, index) => {
                const time = new Date(progress.timestamp);
                data.labels.push(`${time.getHours()}:${time.getMinutes()}`);
                data.values.push(parseFloat(progress.percentage));
            });
        } else {
            // 生成示例数据
            for (let i = 0; i <= 10; i++) {
                data.labels.push(`步骤${i + 1}`);
                data.values.push(i * 10);
            }
        }

        return data;
    }

    _createActionDistributionChart() {
        const canvas = document.getElementById('action-distribution');
        if (!canvas) return;

        // 获取操作类型分布
        const distributionData = this._getActionDistribution();

        // 创建饼图
        const chart = new Chart(canvas, {
            type: 'doughnut',
            data: {
                labels: distributionData.labels,
                datasets: [{
                    data: distributionData.values,
                    backgroundColor: [
                        'rgb(255, 99, 132)',
                        'rgb(54, 162, 235)',
                        'rgb(255, 205, 86)',
                        'rgb(75, 192, 192)',
                        'rgb(153, 102, 255)'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'right'
                    }
                }
            }
        });

        this.charts.distribution = chart;
    }

    _getActionDistribution() {
        const distribution = {
            labels: [],
            values: []
        };

        if (this.data.actionTypes) {
            Object.keys(this.data.actionTypes).forEach(type => {
                distribution.labels.push(type);
                distribution.values.push(this.data.actionTypes[type].count);
            });
        } else {
            // 生成示例数据
            distribution.labels = ['点击', '拖拽', '答题', '导航', '其他'];
            distribution.values = [30, 20, 25, 15, 10];
        }

        return distribution;
    }

    _showRecommendations() {
        const recommendationsContainer = document.getElementById('recommendations');
        if (!recommendationsContainer) return;

        const recommendations = this.data.recommendations || [];

        if (recommendations.length === 0) {
            recommendationsContainer.innerHTML = '<li class="no-recommendations">暂无建议</li>';
            return;
        }

        recommendationsContainer.innerHTML = recommendations.map(rec => `
            <li class="recommendation-item ${rec.priority}">
                <span class="priority-badge">${rec.priority}</span>
                <span class="recommendation-text">${rec.message}</span>
            </li>
        `).join('');
    }

    exportReport(format = 'pdf') {
        const report = this._generateReportText();

        if (format === 'pdf') {
            // 简化的PDF导出（实际应用中可以使用jsPDF等库）
            this._downloadTextFile(report, 'analytics-report.txt');
        } else if (format === 'json') {
            const jsonData = JSON.stringify(this.data, null, 2);
            this._downloadTextFile(jsonData, 'analytics-data.json');
        }
    }

    _generateReportText() {
        return `
学习分析报告
=====================

生成时间: ${new Date().toLocaleString()}
会话ID: ${this.data.sessionId}

学习指标
--------
准确率: ${this.data.accuracy}%
完成率: ${this.data.completionRate}%
参与度: ${this.data.engagementScore}
效率: ${this.data.efficiency}

时间统计
--------
学习时长: ${Math.floor(this.data.timeSpent / 1000 / 60)}分钟
操作次数: ${this.data.totalActions}次

改进趋势
--------
趋势: ${this.data.improvementTrend.trend}
改进幅度: ${this.data.improvementTrend.improvement}%

学习建议
--------
${this.data.recommendations.map(rec => `- ${rec.message}`).join('\\n')}
        `;
    }

    _downloadTextFile(content, filename) {
        const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    }

    dispose() {
        // 清理图表
        Object.values(this.charts).forEach(chart => {
            if (chart.destroy) {
                chart.destroy();
            }
        });
        this.charts = {};
    }
}

export default DataVisualization;
'''

    def implement_feedback_system(self) -> str:
        """实现反馈系统"""
        return '''// 反馈系统

class FeedbackSystem {
    constructor() {
        this.feedbackRules = this._loadFeedbackRules();
        this.feedbackHistory = [];
        this.feedbackQueue = [];
    }

    _loadFeedbackRules() {
        return {
            // 正确答案反馈
            correct: [
                "很好！",
                "正确！",
                "继续保持！",
                "做得好！",
                "太棒了！"
            ],

            // 错误答案反馈
            incorrect: [
                "再试一次",
                "仔细思考一下",
                "不对，请重新考虑",
                "还需要努力"
            ],

            // 提示消息
            hints: [
                "想想相关的理论知识",
                "回顾一下前面的内容",
                "注意题目中的关键词",
                "试试用不同的思路"
            ],

            // 完成任务反馈
            completion: [
                "恭喜完成任务！",
                "练习完成！",
                "做得很好！"
            ]
        };
    }

    provideFeedback(userAction, expectedAction, context = {}) {
        let feedback = {
            type: 'info',
            message: '',
            suggestions: [],
            timestamp: Date.now(),
            context: context
        };

        if (userAction === expectedAction) {
            feedback.type = 'success';
            feedback.message = this._getRandomFeedback('correct');
            feedback.suggestions = this._generateSuccessSuggestions(context);
        } else {
            feedback.type = 'error';
            feedback.message = this._getCorrectiveFeedback(userAction, expectedAction);
            feedback.suggestions = this._generateErrorSuggestions(userAction, expectedAction, context);
        }

        this.feedbackHistory.push(feedback);
        this._showFeedback(feedback);

        return feedback;
    }

    _getRandomFeedback(type) {
        const messages = this.feedbackRules[type] || [];
        return messages[Math.floor(Math.random() * messages.length)];
    }

    _getCorrectiveFeedback(userAction, expectedAction) {
        if (typeof expectedAction === 'string') {
            return `应该是 "${expectedAction}" 而不是 "${userAction}"`;
        } else {
            return `操作不正确，请重试`;
        }
    }

    _generateSuccessSuggestions(context) {
        const suggestions = [];

        if (context.difficulty === 'easy') {
            suggestions.push("可以尝试更难的题目");
        } else if (context.difficulty === 'hard') {
            suggestions.push("你做得很好！");
        }

        if (context.timeSpent < 5000) {
            suggestions.push("回答很快！继续保持");
        }

        return suggestions;
    }

    _generateErrorSuggestions(userAction, expectedAction, context) {
        const suggestions = [];
        suggestions.push(this._getRandomFeedback('hints'));

        if (context.attempts > 3) {
            suggestions.push("需要帮助吗？可以查看提示");
        }

        if (context.hintsAvailable > 0) {
            suggestions.push("可以查看提示获取帮助");
        }

        return suggestions;
    }

    adaptiveHint(currentStep, errorCount, context = {}) {
        let hintLevel = 'basic';

        if (errorCount > 5) {
            hintLevel = 'detailed';
        } else if (errorCount > 2) {
            hintLevel = 'moderate';
        }

        return this._getHintByLevel(currentStep, hintLevel, context);
    }

    _getHintByLevel(step, level, context) {
        const hints = {
            basic: "再仔细想一想",
            moderate: this._getRandomFeedback('hints'),
            detailed: this._generateDetailedHint(step, context)
        };

        return hints[level];
    }

    _generateDetailedHint(step, context) {
        // 根据具体步骤和上下文生成详细提示
        if (context.relatedConcepts && context.relatedConcepts.length > 0) {
            return `提示：回顾一下 ${context.relatedConcepts[0]} 的相关内容`;
        }

        return "提示：参考示例和理论知识";
    }

    _showFeedback(feedback) {
        // 创建反馈元素
        const feedbackElement = document.createElement('div');
        feedbackElement.className = `feedback-message ${feedback.type}`;
        feedbackElement.innerHTML = `
            <div class="feedback-content">
                <span class="feedback-icon">${feedback.type === 'success' ? '✓' : '✗'}</span>
                <span class="feedback-text">${feedback.message}</span>
            </div>
        `;

        // 如果有建议，添加建议列表
        if (feedback.suggestions.length > 0) {
            const suggestionsList = document.createElement('ul');
            suggestionsList.className = 'feedback-suggestions';
            feedback.suggestions.forEach(suggestion => {
                const li = document.createElement('li');
                li.textContent = suggestion;
                suggestionsList.appendChild(li);
            });
            feedbackElement.appendChild(suggestionsList);
        }

        // 显示反馈
        this._displayFeedback(feedbackElement);
    }

    _displayFeedback(element) {
        // 找到合适的显示位置
        const container = document.querySelector('.feedback-container') || document.body;

        // 添加到队列
        this.feedbackQueue.push(element);

        // 如果当前没有显示反馈，显示下一个
        if (this.feedbackQueue.length === 1) {
            this._showNextFeedback(container);
        }
    }

    _showNextFeedback(container) {
        if (this.feedbackQueue.length === 0) return;

        const feedback = this.feedbackQueue[0];
        container.appendChild(feedback);

        // 自动消失
        setTimeout(() => {
            this._removeFeedback(feedback, container);
        }, 3000);
    }

    _removeFeedback(element, container) {
        element.remove();

        // 从队列中移除
        this.feedbackQueue.shift();

        // 显示下一个反馈
        if (this.feedbackQueue.length > 0) {
            this._showNextFeedback(container);
        }
    }

    showCompletionFeedback(taskName, score, context = {}) {
        const feedback = {
            type: 'completion',
            message: this._getRandomFeedback('completion'),
            score: score,
            taskName: taskName,
            timestamp: Date.now(),
            context: context
        };

        this.feedbackHistory.push(feedback);
        this._showCompletionDialog(feedback);
    }

    _showCompletionDialog(feedback) {
        const dialog = document.createElement('div');
        dialog.className = 'completion-dialog';
        dialog.innerHTML = `
            <div class="completion-content">
                <h2>${feedback.message}</h2>
                <p>任务: ${feedback.taskName}</p>
                <p>得分: ${feedback.score}</p>
                <button id="close-completion">继续</button>
            </div>
        `;

        document.body.appendChild(dialog);

        document.getElementById('close-completion').addEventListener('click', () => {
            dialog.remove();
        });
    }

    getFeedbackHistory() {
        return this.feedbackHistory;
    }

    clearHistory() {
        this.feedbackHistory = [];
    }

    exportFeedbackReport() {
        const report = {
            timestamp: Date.now(),
            totalFeedback: this.feedbackHistory.length,
            feedbackByType: this._getFeedbackByType(),
            recentFeedback: this.feedbackHistory.slice(-10)
        };

        return JSON.stringify(report, null, 2);
    }

    _getFeedbackByType() {
        const byType = {
            success: 0,
            error: 0,
            info: 0,
            completion: 0
        };

        this.feedbackHistory.forEach(feedback => {
            byType[feedback.type]++;
        });

        return byType;
    }
}

export default FeedbackSystem;
'''

    def save_analytics_script(self, output_path: str) -> bool:
        """保存分析脚本"""
        try:
            # 合并所有分析组件
            full_code = f'''// 数据分析脚本 - 完整版本
// 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{self.track_user_actions()}

{self.calculate_learning_metrics()}

{self.create_visualization()}

{self.implement_feedback_system()}

// 导出所有组件
export {{
    ActionTracker,
    LearningMetrics,
    DataVisualization,
    FeedbackSystem
}};

// 创建默认实例
export default {{
    ActionTracker,
    LearningMetrics,
    DataVisualization,
    FeedbackSystem
}};
'''

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(full_code)
            return True
        except Exception as e:
            self.error = f"保存失败: {str(e)}"
            return False


def main():
    parser = argparse.ArgumentParser(
        description='数据分析脚本 - 实现学习数据分析功能',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 data_analyzer.py content.json --metrics tracking --output analytics.js
  python3 data_analyzer.py content.json --metrics tracking,metrics,visualization --output analytics.js
  python3 data_analyzer.py content.json --export-report --format pdf
        """
    )

    parser.add_argument('content_file', help='教材内容JSON文件')
    parser.add_argument('--metrics', nargs='+',
                        choices=['tracking', 'metrics', 'visualization', 'feedback', 'all'],
                        default=['all'],
                        help='要生成的分析模块')
    parser.add_argument('--export-report', action='store_true',
                        help='导出分析报告')
    parser.add_argument('--format', choices=['json', 'pdf', 'csv'],
                        default='json',
                        help='报告格式')
    parser.add_argument('--output', required=True, help='输出文件路径')

    args = parser.parse_args()

    # 读取教材内容
    try:
        with open(args.content_file, 'r', encoding='utf-8') as f:
            content_data = json.load(f)
    except Exception as e:
        print(f"❌ 读取文件失败: {str(e)}", file=sys.stderr)
        sys.exit(1)

    # 创建数据分析器
    print(f"正在生成数据分析脚本...")
    analyzer = DataAnalyzer(content_data)

    # 保存分析脚本
    print(f"正在保存分析脚本到: {args.output}")
    if analyzer.save_analytics_script(args.output):
        print(f"✅ 数据分析脚本生成成功！")
        print(f"  输出文件: {args.output}")

        # 显示摘要
        print(f"\n📊 分析模块摘要:")
        print(f"  操作追踪: {'✅' if 'tracking' in args.metrics or 'all' in args.metrics else '❌'}")
        print(f"  学习指标: {'✅' if 'metrics' in args.metrics or 'all' in args.metrics else '❌'}")
        print(f"  数据可视化: {'✅' if 'visualization' in args.metrics or 'all' in args.metrics else '❌'}")
        print(f"  反馈系统: {'✅' if 'feedback' in args.metrics or 'all' in args.metrics else '❌'}")

        if args.export_report:
            print(f"\n📋 报告导出:")
            print(f"  格式: {args.format}")
            print(f"  状态: 报告导出功能将在运行时提供")
    else:
        print(f"❌ 保存失败: {analyzer.error}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()