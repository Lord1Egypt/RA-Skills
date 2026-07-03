#!/usr/bin/env python3
"""
交互式组件构建脚本 - 创建教育仿真交互组件
支持测验、进度追踪、控制面板等组件
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime


class InteractiveBuilder:
    """交互式组件构建器"""

    def __init__(self, content_data: Dict[str, Any]):
        self.content = content_data
        self.components = set()

    def build_quiz_component(self) -> str:
        """构建测验组件"""
        quiz_data = self._extract_quiz_data()

        quiz_code = f'''// 测验组件
// 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

class QuizComponent {{
    constructor(questions = []) {{
        this.questions = questions.length > 0 ? questions : this._defaultQuestions();
        this.currentQuestion = 0;
        this.score = 0;
        this.userAnswers = [];
        this.correctAnswers = 0;
        this.container = null;
    }}

    _defaultQuestions() {{
        // 默认测验问题
        return {json.dumps(quiz_data, ensure_ascii=False, indent=12)};
    }}

    render(container) {{
        this.container = container;
        this._createQuizUI();
        this._showQuestion(this.currentQuestion);
    }}

    _createQuizUI() {{
        // 创建测验界面
        this.container.innerHTML = `
            <div class="quiz-container">
                <div class="quiz-header">
                    <h2>知识测验</h2>
                    <div class="quiz-progress">
                        <span class="question-counter">题目: <span id="current-question">1</span> / <span id="total-questions">${{this.questions.length}}</span></span>
                        <span class="score-counter">得分: <span id="current-score">0</span></span>
                    </div>
                </div>
                <div class="quiz-content" id="quiz-content"></div>
                <div class="quiz-controls">
                    <button id="prev-question" disabled>上一题</button>
                    <button id="submit-answer">提交答案</button>
                    <button id="next-question" disabled>下一题</button>
                </div>
                <div class="quiz-result" id="quiz-result" style="display: none;"></div>
            </div>
        `;

        // 绑定事件
        this._bindEvents();
    }}

    _showQuestion(index) {{
        if (index < 0 || index >= this.questions.length) return;

        const question = this.questions[index];
        const contentDiv = document.getElementById('quiz-content');

        // 生成题目HTML
        let html = `<div class="question-item">
            <h3>${{index + 1}}. ${{question.question}}</h3>`;

        if (question.type === 'multiple_choice') {{
            html += '<div class="options">';
            question.options.forEach((option, i) => {{
                html += `<label class="option-item">
                    <input type="radio" name="answer" value="${{i}}">
                    <span>${{option}}</span>
                </label>`;
            }});
            html += '</div>';
        }} else if (question.type === 'true_false') {{
            html += '<div class="options">
                <label class="option-item">
                    <input type="radio" name="answer" value="true">
                    <span>正确</span>
                </label>
                <label class="option-item">
                    <input type="radio" name="answer" value="false">
                    <span>错误</span>
                </label>
            </div>';
        }} else if (question.type === 'fill_blank') {{
            html += `<input type="text" class="fill-blank-input" placeholder="请输入答案">`;
        }}

        html += '<div class="feedback" id="feedback"></div></div>';
        contentDiv.innerHTML = html;

        // 更新进度显示
        document.getElementById('current-question').textContent = index + 1;

        // 更新按钮状态
        document.getElementById('prev-question').disabled = index === 0;
        document.getElementById('next-question').disabled = index === this.questions.length - 1;

        this.currentQuestion = index;
    }}

    _bindEvents() {{
        // 上一题按钮
        document.getElementById('prev-question').addEventListener('click', () => {{
            this._showQuestion(this.currentQuestion - 1);
        }});

        // 下一题按钮
        document.getElementById('next-question').addEventListener('click', () => {{
            this._showQuestion(this.currentQuestion + 1);
        }});

        // 提交答案按钮
        document.getElementById('submit-answer').addEventListener('click', () => {{
            this._checkAnswer();
        }});
    }}

    _checkAnswer() {{
        const question = this.questions[this.currentQuestion];
        let userAnswer;

        if (question.type === 'multiple_choice' || question.type === 'true_false') {{
            const selected = document.querySelector('input[name="answer"]:checked');
            if (selected) {{
                userAnswer = selected.value;
            }}
        }} else if (question.type === 'fill_blank') {{
            const input = document.querySelector('.fill-blank-input');
            if (input) {{
                userAnswer = input.value.trim();
            }}
        }}

        if (!userAnswer) {{
            this._showFeedback('请先选择或输入答案', 'warning');
            return;
        }}

        // 检查答案
        let isCorrect = false;
        if (question.type === 'multiple_choice' || question.type === 'true_false') {{
            isCorrect = userAnswer === question.correct_answer.toString();
        }} else if (question.type === 'fill_blank') {{
            isCorrect = userAnswer.toLowerCase() === question.correct_answer.toLowerCase();
        }}

        // 更新统计
        if (isCorrect) {{
            this.correctAnswers++;
            this.score += question.points || 1;
            this._showFeedback('✓ 正确！', 'success');
        }} else {{
            this._showFeedback('✗ 错误。正确答案是: ' + this._formatCorrectAnswer(question), 'error');
        }}

        // 更新显示
        document.getElementById('current-score').textContent = this.score;

        // 保存用户答案
        this.userAnswers[this.currentQuestion] = {{
            question: question.question,
            userAnswer: userAnswer,
            isCorrect: isCorrect,
            correctAnswer: question.correct_answer
        }};

        // 触发自定义事件
        this._dispatchEvent('answerSubmitted', {{
            questionIndex: this.currentQuestion,
            isCorrect: isCorrect,
            score: this.score
        }});
    }}

    _formatCorrectAnswer(question) {{
        if (question.type === 'multiple_choice') {{
            return question.options[question.correct_answer];
        }} else if (question.type === 'true_false') {{
            return question.correct_answer ? '正确' : '错误';
        }} else {{
            return question.correct_answer;
        }}
    }}

    _showFeedback(message, type) {{
        const feedbackDiv = document.getElementById('feedback');
        feedbackDiv.textContent = message;
        feedbackDiv.className = 'feedback ' + type;
    }}

    showResults() {{
        // 显示最终结果
        const resultDiv = document.getElementById('quiz-result');
        const percentage = (this.correctAnswers / this.questions.length * 100).toFixed(1);

        resultDiv.innerHTML = `
            <h3>测验结果</h3>
            <div class="result-summary">
                <div class="result-item">
                    <span class="result-label">总题数</span>
                    <span class="result-value">${{this.questions.length}}</span>
                </div>
                <div class="result-item">
                    <span class="result-label">正确数</span>
                    <span class="result-value">${{this.correctAnswers}}</span>
                </div>
                <div class="result-item">
                    <span class="result-label">正确率</span>
                    <span class="result-value">${{percentage}}%</span>
                </div>
                <div class="result-item">
                    <span class="result-label">得分</span>
                    <span class="result-value">${{this.score}}</span>
                </div>
            </div>
            <div class="result-message">${{this._getResultMessage(percentage)}}</div>
            <button id="restart-quiz">重新开始</button>
        `;

        resultDiv.style.display = 'block';
        document.querySelector('.quiz-content').style.display = 'none';
        document.querySelector('.quiz-controls').style.display = 'none';

        // 绑定重新开始按钮
        document.getElementById('restart-quiz').addEventListener('click', () => {{
            this.restart();
        }});

        // 触发完成事件
        this._dispatchEvent('quizCompleted', {{
            score: this.score,
            correctAnswers: this.correctAnswers,
            percentage: percentage
        }});
    }}

    _getResultMessage(percentage) {{
        if (percentage >= 90) return '太棒了！你的表现非常出色！';
        if (percentage >= 70) return '很好！继续保持！';
        if (percentage >= 60) return '及格了，继续努力！';
        return '需要加油，建议重新学习相关内容！';
    }}

    restart() {{
        // 重新开始测验
        this.currentQuestion = 0;
        this.score = 0;
        this.userAnswers = [];
        this.correctAnswers = 0;

        document.getElementById('quiz-result').style.display = 'none';
        document.querySelector('.quiz-content').style.display = 'block';
        document.querySelector('.quiz-controls').style.display = 'block';

        this._showQuestion(0);
        document.getElementById('current-score').textContent = '0';
    }}

    _dispatchEvent(eventName, data) {{
        const event = new CustomEvent(eventName, {{ detail: data }});
        this.container.dispatchEvent(event);
    }}

    // 公共方法
    getCurrentProgress() {{
        return {{
            currentQuestion: this.currentQuestion,
            totalQuestions: this.questions.length,
            score: this.score,
            correctAnswers: this.correctAnswers
        }};
    }}

    getDetailedResults() {{
        return {{
            totalQuestions: this.questions.length,
            correctAnswers: this.correctAnswers,
            userAnswers: this.userAnswers,
            score: this.score,
            percentage: (this.correctAnswers / this.questions.length * 100).toFixed(1)
        }};
    }}
}}

export default QuizComponent;
'''

        return quiz_code

    def _extract_quiz_data(self) -> List[Dict[str, Any]]:
        """从教材内容中提取测验数据"""
        quiz_data = []

        # 从实验内容中生成问题
        if 'content' in self.content and 'experiments' in self.content['content']:
            for exp in self.content['content']['experiments']:
                quiz_data.append({
                    "question": exp.get('name', '实验相关问题'),
                    "type": "multiple_choice",
                    "options": [
                        "选项A",
                        "选项B",
                        "选项C",
                        "选项D"
                    ],
                    "correct_answer": 0,
                    "points": 1
                })

        # 如果没有测验数据，添加默认问题
        if not quiz_data:
            quiz_data = [
                {
                    "question": "以下哪个是正确的实验步骤？",
                    "type": "multiple_choice",
                    "options": [
                        "步骤一",
                        "步骤二",
                        "步骤三",
                        "步骤四"
                    ],
                    "correct_answer": 0,
                    "points": 1
                },
                {
                    "question": "实验中的安全注意事项是什么？",
                    "type": "multiple_choice",
                    "options": [
                        "注意A",
                        "注意B",
                        "注意C",
                        "注意D"
                    ],
                    "correct_answer": 1,
                    "points": 1
                },
                {
                    "question": "这个说法正确吗？",
                    "type": "true_false",
                    "correct_answer": True,
                    "points": 1
                }
            ]

        return quiz_data

    def build_progress_tracker(self) -> str:
        """构建进度追踪组件"""
        return '''// 进度追踪组件

class ProgressTracker {
    constructor(totalSteps = 10) {
        this.totalSteps = totalSteps;
        this.currentStep = 0;
        this.startTime = Date.now();
        this.milestones = [];
        this.savedProgress = null;
        this.autoSave = true;
        this.autoSaveInterval = 30000; // 30秒自动保存
        this.timer = null;

        this._loadSavedProgress();
        this._startAutoSave();
    }

    updateProgress(step) {
        if (step >= 0 && step <= this.totalSteps) {
            this.currentStep = step;
            this._saveProgress();
            this._dispatchEvent('progressUpdated', {
                currentStep: this.currentStep,
                totalSteps: this.totalSteps,
                percentage: (this.currentStep / this.totalSteps * 100).toFixed(1)
            });
        }
    }

    incrementProgress() {
        if (this.currentStep < this.totalSteps) {
            this.updateProgress(this.currentStep + 1);
        }
    }

    decrementProgress() {
        if (this.currentStep > 0) {
            this.updateProgress(this.currentStep - 1);
        }
    }

    addMilestone(name, description = '') {
        const milestone = {
            name: name,
            description: description,
            timestamp: Date.now(),
            step: this.currentStep
        };
        this.milestones.push(milestone);
        this._saveProgress();
        this._dispatchEvent('milestoneAdded', milestone);
    }

    getTimeSpent() {
        return Date.now() - this.startTime;
    }

    getProgress() {
        return {
            currentStep: this.currentStep,
            totalSteps: this.totalSteps,
            percentage: (this.currentStep / this.totalSteps * 100).toFixed(1),
            timeSpent: this.getTimeSpent(),
            milestones: this.milestones,
            isComplete: this.currentStep >= this.totalSteps
        };
    }

    reset() {
        this.currentStep = 0;
        this.startTime = Date.now();
        this.milestones = [];
        this._clearSavedProgress();
        this._saveProgress();
        this._dispatchEvent('progressReset', {});
    }

    _saveProgress() {
        if (!this.autoSave) return;

        const progressData = {
            currentStep: this.currentStep,
            totalSteps: this.totalSteps,
            startTime: this.startTime,
            milestones: this.milestones,
            timestamp: Date.now()
        };

        localStorage.setItem('simulationProgress', JSON.stringify(progressData));
    }

    _loadSavedProgress() {
        try {
            const saved = localStorage.getItem('simulationProgress');
            if (saved) {
                this.savedProgress = JSON.parse(saved);
                // 恢复进度（可选）
                // this.currentStep = this.savedProgress.currentStep;
                // this.milestones = this.savedProgress.milestones;
            }
        } catch (error) {
            console.error('加载保存的进度失败:', error);
        }
    }

    _clearSavedProgress() {
        localStorage.removeItem('simulationProgress');
    }

    _startAutoSave() {
        if (this.timer) {
            clearInterval(this.timer);
        }
        this.timer = setInterval(() => {
            this._saveProgress();
        }, this.autoSaveInterval);
    }

    _stopAutoSave() {
        if (this.timer) {
            clearInterval(this.timer);
            this.timer = null;
        }
    }

    _dispatchEvent(eventName, data) {
        const event = new CustomEvent(eventName, { detail: data });
        window.dispatchEvent(event);
    }

    render(container) {
        const progress = this.getProgress();
        container.innerHTML = `
            <div class="progress-tracker">
                <h3>学习进度</h3>
                <div class="progress-overview">
                    <div class="progress-item">
                        <span class="progress-label">当前步骤</span>
                        <span class="progress-value">${progress.currentStep} / ${progress.totalSteps}</span>
                    </div>
                    <div class="progress-bar-container">
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: ${progress.percentage}%"></div>
                        </div>
                        <span class="progress-percentage">${progress.percentage}%</span>
                    </div>
                    <div class="progress-item">
                        <span class="progress-label">学习时长</span>
                        <span class="progress-value">${this._formatTime(progress.timeSpent)}</span>
                    </div>
                </div>
                <div class="progress-milestones" id="milestones">
                    <h4>里程碑</h4>
                    <ul>
                        ${this.milestones.length > 0 ? this.milestones.map(m => `
                            <li>
                                <strong>${m.name}</strong>
                                <span class="milestone-time">${new Date(m.timestamp).toLocaleTimeString()}</span>
                            </li>
                        `).join('') : '<li class="no-milestones">暂无里程碑</li>'}
                    </ul>
                </div>
                <div class="progress-controls">
                    <button id="save-progress">保存进度</button>
                    <button id="reset-progress">重置进度</button>
                </div>
            </div>
        `;

        // 绑定事件
        document.getElementById('save-progress').addEventListener('click', () => {
            this._saveProgress();
            alert('进度已保存！');
        });

        document.getElementById('reset-progress').addEventListener('click', () => {
            if (confirm('确定要重置进度吗？')) {
                this.reset();
                this.render(container);
            }
        });
    }

    _formatTime(ms) {
        const seconds = Math.floor(ms / 1000);
        const minutes = Math.floor(seconds / 60);
        const hours = Math.floor(minutes / 60);

        if (hours > 0) {
            return `${hours}小时${minutes % 60}分钟`;
        } else if (minutes > 0) {
            return `${minutes}分钟${seconds % 60}秒`;
        } else {
            return `${seconds}秒`;
        }
    }

    dispose() {
        this._stopAutoSave();
    }
}

export default ProgressTracker;
'''

    def build_control_panel(self) -> str:
        """构建控制面板组件"""
        return '''// 控制面板组件

class ControlPanel {
    constructor(scene = null) {
        this.scene = scene;
        this.controls = {
            reset: () => this.resetScene(),
            pause: () => this.pauseSimulation(),
            hint: () => this.showHint(),
            help: () => this.showHelp(),
            fullscreen: () => this.toggleFullscreen()
        };
        this.isPaused = false;
    }

    render(container) {
        container.innerHTML = `
            <div class="control-panel">
                <h3>控制面板</h3>
                <div class="control-groups">
                    <div class="control-group">
                        <h4>场景控制</h4>
                        <button class="control-btn" data-action="reset">
                            <i class="fas fa-redo"></i>
                            重置场景
                        </button>
                        <button class="control-btn" data-action="fullscreen">
                            <i class="fas fa-expand"></i>
                            全屏
                        </button>
                    </div>
                    <div class="control-group">
                        <h4>仿真控制</h4>
                        <button class="control-btn" data-action="pause">
                            <i class="fas fa-pause"></i>
                            <span id="pause-text">暂停</span>
                        </button>
                    </div>
                    <div class="control-group">
                        <h4>帮助</h4>
                        <button class="control-btn" data-action="hint">
                            <i class="fas fa-lightbulb"></i>
                            提示
                        </button>
                        <button class="control-btn" data-action="help">
                            <i class="fas fa-question-circle"></i>
                            帮助
                        </button>
                    </div>
                </div>
            </div>
        `;

        this._bindEvents();
    }

    _bindEvents() {
        const buttons = document.querySelectorAll('.control-btn');
        buttons.forEach(button => {
            button.addEventListener('click', () => {
                const action = button.dataset.action;
                if (this.controls[action]) {
                    this.controls[action]();
                }
            });
        });
    }

    resetScene() {
        if (this.scene && this.scene.resetCamera) {
            this.scene.resetCamera();
        }
        this._dispatchEvent('sceneReset', {});
    }

    pauseSimulation() {
        this.isPaused = !this.isPaused;
        const pauseBtn = document.querySelector('[data-action="pause"]');
        const pauseText = document.getElementById('pause-text');

        if (this.isPaused) {
            pauseText.textContent = '继续';
            pauseBtn.classList.add('active');
        } else {
            pauseText.textContent = '暂停';
            pauseBtn.classList.remove('active');
        }

        this._dispatchEvent('simulationToggled', { isPaused: this.isPaused });
    }

    showHint() {
        const hint = this._getCurrentHint();
        alert('提示: ' + hint);
        this._dispatchEvent('hintRequested', { hint: hint });
    }

    _getCurrentHint() {
        // 返回当前场景的提示
        const hints = [
            '尝试点击3D对象来查看详细信息',
            '使用鼠标拖动来旋转视角',
            '滚轮可以缩放场景',
            '注意观察场景中的交互提示'
        ];
        return hints[Math.floor(Math.random() * hints.length)];
    }

    showHelp() {
        alert(`
使用说明：
1. 鼠标左键拖动：旋转视角
2. 鼠标右键拖动：平移视角
3. 滚轮：缩放场景
4. 点击对象：查看详情
5. 使用控制面板：管理仿真
        `);
        this._dispatchEvent('helpRequested', {});
    }

    toggleFullscreen() {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen();
        } else {
            document.exitFullscreen();
        }
    }

    _dispatchEvent(eventName, data) {
        const event = new CustomEvent(eventName, { detail: data });
        window.dispatchEvent(event);
    }

    addCustomControl(name, icon, action) {
        this.controls[name] = action;

        const controlGroup = document.querySelector('.control-group');
        const button = document.createElement('button');
        button.className = 'control-btn';
        button.dataset.action = name;
        button.innerHTML = `<i class="fas ${icon}"></i> ${name}`;
        button.addEventListener('click', action);
        controlGroup.appendChild(button);
    }
}

export default ControlPanel;
'''

    def build_step_by_step_guide(self) -> str:
        """构建步骤指导组件"""
        # 从教材内容中提取步骤
        steps_data = []
        if 'content' in self.content and 'experiments' in self.content['content']:
            for exp in self.content['content']['experiments']:
                if 'steps' in exp:
                    for step in exp['steps']:
                        steps_data.append({
                            "instruction": step,
                            "completed": False
                        })

        # 如果没有步骤数据，添加默认步骤
        if not steps_data:
            steps_data = [
                {"instruction": "步骤一：准备实验材料", "completed": False},
                {"instruction": "步骤二：设置实验环境", "completed": False},
                {"instruction": "步骤三：执行实验操作", "completed": False},
                {"instruction": "步骤四：观察实验结果", "completed": False}
            ]

        return f'''// 步骤指导组件

class StepGuide {{
    constructor(steps = []) {{
        this.steps = steps.length > 0 ? steps : {json.dumps(steps_data, ensure_ascii=False)};
        this.currentStep = 0;
        this.container = null;
    }}

    render(container) {{
        this.container = container;
        this._createGuideUI();
        this._updateStepDisplay();
    }}

    _createGuideUI() {{
        this.container.innerHTML = `
            <div class="step-guide">
                <h3>操作指导</h3>
                <div class="step-content" id="step-content">
                    <div class="current-step">
                        <div class="step-number">步骤 ${ this.currentStep + 1 } / ${ this.steps.length }</div>
                        <div class="step-instruction" id="current-instruction"></div>
                    </div>
                </div>
                <div class="step-controls">
                    <button id="prev-step" disabled>上一步</button>
                    <button id="complete-step">完成</button>
                    <button id="next-step" disabled>下一步</button>
                </div>
                <div class="step-overview">
                    <h4>步骤概览</h4>
                    <ul id="step-list"></ul>
                </div>
            </div>
        `;

        this._bindEvents();
        this._renderStepList();
    }}

    _updateStepDisplay() {{
        const step = this.steps[this.currentStep];
        document.getElementById('current-instruction').textContent = step.instruction;

        // 更新按钮状态
        document.getElementById('prev-step').disabled = this.currentStep === 0;
        document.getElementById('next-step').disabled = this.currentStep === this.steps.length - 1;
        document.getElementById('complete-step').disabled = step.completed;

        // 更新步骤列表高亮
        this._highlightCurrentStep();
    }}

    _renderStepList() {{
        const stepList = document.getElementById('step-list');
        stepList.innerHTML = this.steps.map((step, index) => `
            <li class="step-item ${ step.completed ? 'completed' : '' }} ${ index === this.currentStep ? 'active' : '' }}">
                <span class="step-status">${ step.completed ? '✓' : (index + 1) }}</span>
                <span class="step-text">${ step.instruction }}</span>
            </li>
        `).join('');
    }}

    _highlightCurrentStep() {{
        const items = document.querySelectorAll('.step-item');
        items.forEach((item, index) => {{
            item.classList.remove('active');
            if (index === this.currentStep) {{
                item.classList.add('active');
                item.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
            }}
        }});
    }}

    _bindEvents() {{
        document.getElementById('prev-step').addEventListener('click', () => {{
            this.previousStep();
        }});

        document.getElementById('next-step').addEventListener('click', () => {{
            this.nextStep();
        }});

        document.getElementById('complete-step').addEventListener('click', () => {{
            this.completeCurrentStep();
        }});
    }}

    showStep(index) {{
        if (index >= 0 && index < this.steps.length) {{
            this.currentStep = index;
            this._updateStepDisplay();
            this._renderStepList();
        }}
    }}

    nextStep() {{
        if (this.currentStep < this.steps.length - 1) {{
            this.showStep(this.currentStep + 1);
        }}
    }}

    previousStep() {{
        if (this.currentStep > 0) {{
            this.showStep(this.currentStep - 1);
        }}
    }}

    completeCurrentStep() {{
        this.steps[this.currentStep].completed = true;
        this._updateStepDisplay();
        this._renderStepList();
        this._dispatchEvent('stepCompleted', {{
            stepIndex: this.currentStep,
            step: this.steps[this.currentStep]
        }});

        // 自动进入下一步
        if (this.currentStep < this.steps.length - 1) {{
            setTimeout(() => this.nextStep(), 500);
        }}
    }}

    reset() {{
        this.currentStep = 0;
        this.steps.forEach(step => {{
            step.completed = false;
        }});
        this._updateStepDisplay();
        this._renderStepList();
    }}

    getProgress() {{
        const completedSteps = this.steps.filter(step => step.completed).length;
        return {{
            currentStep: this.currentStep,
            totalSteps: this.steps.length,
            completedSteps: completedSteps,
            percentage: (completedSteps / this.steps.length * 100).toFixed(1)
        }};
    }}

    _dispatchEvent(eventName, data) {{
        const event = new CustomEvent(eventName, {{ detail: data }});
        window.dispatchEvent(event);
    }}
}}

export default StepGuide;
'''

    def integrate_components(self) -> str:
        """集成所有组件"""
        return '''// 组件集成脚本

class ComponentIntegrator {
    constructor(contentData) {
        this.contentData = contentData;
        this.quiz = null;
        this.progress = null;
        this.controls = null;
        this.guide = null;
        this.analytics = null;
    }

    async initialize(container) {
        // 初始化所有组件
        await Promise.all([
            this._initQuiz(container),
            this._initProgress(container),
            this._initControls(container),
            this._initGuide(container),
            this._initAnalytics(container)
        ]);

        // 建立组件间通信
        this._setupComponentCommunication();
    }

    async _initQuiz(container) {
        const quizContainer = document.getElementById('quiz-container');
        if (quizContainer) {
            this.quiz = new QuizComponent(this.contentData.quizQuestions || []);
            this.quiz.render(quizContainer);
        }
    }

    async _initProgress(container) {
        const progressContainer = document.getElementById('progress-container');
        if (progressContainer) {
            this.progress = new ProgressTracker(this.contentData.totalSteps || 10);
            this.progress.render(progressContainer);
        }
    }

    async _initControls(container) {
        const controlsContainer = document.getElementById('controls-container');
        if (controlsContainer) {
            this.controls = new ControlPanel();
            this.controls.render(controlsContainer);
        }
    }

    async _initGuide(container) {
        const guideContainer = document.getElementById('guide-container');
        if (guideContainer) {
            this.guide = new StepGuide(this.contentData.steps || []);
            this.guide.render(guideContainer);
        }
    }

    async _initAnalytics(container) {
        const analyticsContainer = document.getElementById('analytics-container');
        if (analyticsContainer) {
            this.analytics = new DataAnalyzer();
            this.analytics.render(analyticsContainer);
        }
    }

    _setupComponentCommunication() {
        // 测验组件 → 进度组件
        if (this.quiz && this.progress) {
            this.quiz.container.addEventListener('answerSubmitted', (e) => {
                this.progress.addMilestone(`答题: 第${e.detail.questionIndex + 1}题`, `答案${e.detail.isCorrect ? '正确' : '错误'}`);
            });

            this.quiz.container.addEventListener('quizCompleted', (e) => {
                this.progress.addMilestone('测验完成', `得分: ${e.detail.score}, 正确率: ${e.detail.percentage}%`);
            });
        }

        // 步骤指导 → 进度组件
        if (this.guide && this.progress) {
            window.addEventListener('stepCompleted', (e) => {
                this.progress.incrementProgress();
            });
        }

        // 所有组件 → 数据分析组件
        if (this.analytics) {
            window.addEventListener('answerSubmitted', (e) => {
                this.analytics.recordAction('quiz_answer', e.detail);
            });

            window.addEventListener('stepCompleted', (e) => {
                this.analytics.recordAction('step_complete', e.detail);
            });

            window.addEventListener('milestoneAdded', (e) => {
                this.analytics.recordAction('milestone', e.detail);
            });
        }
    }

    // 公共方法
    getAllComponents() {
        return {
            quiz: this.quiz,
            progress: this.progress,
            controls: this.controls,
            guide: this.guide,
            analytics: this.analytics
        };
    }

    getOverallProgress() {
        return {
            quiz: this.quiz ? this.quiz.getCurrentProgress() : null,
            progress: this.progress ? this.progress.getProgress() : null,
            guide: this.guide ? this.guide.getProgress() : null,
            analytics: this.analytics ? this.analytics.getReport() : null
        };
    }

    resetAll() {
        if (this.quiz) this.quiz.restart();
        if (this.progress) this.progress.reset();
        if (this.guide) this.guide.reset();
    }
}

export default ComponentIntegrator;
'''

    def save_component(self, component_name: str, component_code: str, output_dir: str) -> bool:
        """保存组件代码"""
        try:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)

            file_path = output_path / f"{component_name}.js"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(component_code)

            return True
        except Exception as e:
            self.error = f"保存失败: {str(e)}"
            return False


def main():
    parser = argparse.ArgumentParser(
        description='交互式组件构建脚本 - 创建教育仿真交互组件',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 interactive_builder.py content.json --components quiz --output components/
  python3 interactive_builder.py content.json --components quiz,progress,control --output components/
  python3 interactive_builder.py content.json --integrate --output components/
        """
    )

    parser.add_argument('content_file', help='教材内容JSON文件')
    parser.add_argument('--components', nargs='+',
                        choices=['quiz', 'progress', 'control', 'guide', 'all'],
                        help='要生成的组件类型')
    parser.add_argument('--integrate', action='store_true',
                        help='生成组件集成代码')
    parser.add_argument('--output', required=True, help='输出目录路径')

    args = parser.parse_args()

    # 读取教材内容
    try:
        with open(args.content_file, 'r', encoding='utf-8') as f:
            content_data = json.load(f)
    except Exception as e:
        print(f"❌ 读取文件失败: {str(e)}", file=sys.stderr)
        sys.exit(1)

    # 创建组件构建器
    print(f"正在构建交互式组件...")
    builder = InteractiveBuilder(content_data)

    # 生成组件
    components_to_generate = args.components
    if 'all' in components_to_generate or not components_to_generate:
        components_to_generate = ['quiz', 'progress', 'control', 'guide']

    success_count = 0
    for component in components_to_generate:
        print(f"  生成 {component} 组件...")

        if component == 'quiz':
            code = builder.build_quiz_component()
            if builder.save_component('quiz', code, args.output):
                success_count += 1
                print(f"    ✅ {component} 组件已生成")
            else:
                print(f"    ❌ {component} 组件生成失败")

        elif component == 'progress':
            code = builder.build_progress_tracker()
            if builder.save_component('progress', code, args.output):
                success_count += 1
                print(f"    ✅ {component} 组件已生成")
            else:
                print(f"    ❌ {component} 组件生成失败")

        elif component == 'control':
            code = builder.build_control_panel()
            if builder.save_component('control', code, args.output):
                success_count += 1
                print(f"    ✅ {component} 组件已生成")
            else:
                print(f"    ❌ {component} 组件生成失败")

        elif component == 'guide':
            code = builder.build_step_by_step_guide()
            if builder.save_component('guide', code, args.output):
                success_count += 1
                print(f"    ✅ {component} 组件已生成")
            else:
                print(f"    ❌ {component} 组件生成失败")

    # 生成集成代码（如果需要）
    if args.integrate:
        print(f"  生成组件集成代码...")
        integration_code = builder.integrate_components()
        if builder.save_component('integration', integration_code, args.output):
            success_count += 1
            print(f"    ✅ 组件集成代码已生成")
        else:
            print(f"    ❌ 组件集成代码生成失败")

    # 显示摘要
    print(f"\n📊 组件生成摘要:")
    print(f"  生成组件数: {success_count} / {len(components_to_generate) + (1 if args.integrate else 0)}")
    print(f"  输出目录: {args.output}")

    if success_count > 0:
        print(f"✅ 组件生成成功！")
    else:
        print(f"❌ 组件生成失败！")
        sys.exit(1)


if __name__ == '__main__':
    main()