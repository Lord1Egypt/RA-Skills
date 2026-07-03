# Web应用模板设计指南

## 概述

本指南详细说明了教材虚拟仿真系统Web应用的模板设计，包括HTML结构、CSS样式、JavaScript架构以及响应式设计原则。

## 基础模板结构

### 目录结构

```
web-template/
├── index.html           # 主HTML文件
├── css/
│   ├── styles.css      # 主样式文件
│   ├── responsive.css  # 响应式样式
│   └── themes.css      # 主题样式
├── js/
│   ├── main.js         # 主JavaScript文件
│   ├── scene.js        # 3D场景代码
│   ├── utils.js        # 工具函数
│   └── config.js       # 配置文件
├── assets/
│   ├── images/         # 图片资源
│   ├── models/         # 3D模型
│   ├── textures/       # 纹理文件
│   └── sounds/         # 音频文件
└── lib/                # 第三方库
```

---

## HTML模板设计

### 基础HTML结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="基于教材的虚拟仿真系统">
    <meta name="keywords" content="教育,仿真,3D,交互式学习">
    <meta name="author" content="WorkBuddy">

    <title>教材虚拟仿真系统</title>

    <!-- CSS -->
    <link rel="stylesheet" href="css/styles.css">
    <link rel="stylesheet" href="css/responsive.css">

    <!-- 字体 -->
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet">

    <!-- 图标 -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">

    <!-- Three.js Import Map -->
    <script type="importmap">
    {
        "imports": {
            "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
            "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"
        }
    }
    </script>
</head>
<body>
    <div id="app">
        <!-- 导航栏 -->
        <header class="navbar">
            <div class="container">
                <div class="navbar-brand">
                    <i class="fas fa-atom"></i>
                    <h1>虚拟仿真系统</h1>
                </div>
                <nav class="navbar-nav">
                    <ul>
                        <li><a href="#scene" class="active"><i class="fas fa-cube"></i> 3D场景</a></li>
                        <li><a href="#quiz"><i class="fas fa-question-circle"></i> 测验</a></li>
                        <li><a href="#progress"><i class="fas fa-chart-line"></i> 进度</a></li>
                        <li><a href="#help"><i class="fas fa-question"></i> 帮助</a></li>
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
                <p>&copy; 2024 虚拟仿真系统 | 由WorkBuddy生成</p>
            </div>
        </footer>
    </div>

    <!-- 第三方库 -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <!-- JavaScript -->
    <script type="module" src="js/main.js"></script>
</body>
</html>
```

---

## CSS样式设计

### 主样式文件 (styles.css)

```css
/* 全局变量 */
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
```

### 响应式样式 (responsive.css)

```css
/* 平板设备 */
@media (max-width: 1024px) {
    .navbar-nav ul {
        gap: var(--spacing-sm);
    }

    .scene-container {
        height: 50vh;
    }

    .analytics-dashboard {
        grid-template-columns: repeat(2, 1fr);
    }
}

/* 移动设备 */
@media (max-width: 768px) {
    .navbar-nav {
        display: none;
    }

    .navbar-toggle {
        display: block;
    }

    .scene-container {
        height: 40vh;
    }

    section {
        padding: var(--spacing-sm);
        margin: var(--spacing-sm);
    }

    .quiz-controls {
        flex-direction: column;
        gap: var(--spacing-sm);
    }

    .quiz-controls button {
        width: 100%;
    }

    .analytics-dashboard {
        grid-template-columns: 1fr;
    }

    .progress-overview {
        gap: var(--spacing-xs);
    }

    .progress-item {
        flex-direction: column;
        align-items: flex-start;
    }
}

/* 小屏移动设备 */
@media (max-width: 480px) {
    .navbar-brand h1 {
        font-size: 1rem;
    }

    .scene-container {
        height: 35vh;
    }

    .scene-controls button {
        padding: 0.5rem;
    }

    .analytics-card {
        padding: var(--spacing-sm);
    }
}

/* 横屏模式 */
@media (orientation: landscape) and (max-height: 600px) {
    .scene-container {
        height: 70vh;
    }

    .navbar {
        padding: 0.5rem var(--spacing-sm);
    }

    section {
        margin: var(--spacing-xs) auto;
    }
}
```

### 主题样式 (themes.css)

```css
/* 暗色主题 */
[data-theme="dark"] {
    --background-color: #1a1a2e;
    --surface-color: #16213e;
    --text-primary: #eaeaea;
    --text-secondary: #a0a0a0;
    --border-color: #2d3a4a;

    --primary-color: #3498db;
    --primary-dark: #2980b9;
}

/* 高对比度主题 */
[data-theme="high-contrast"] {
    --background-color: #ffffff;
    --surface-color: #ffffff;
    --text-primary: #000000;
    --text-secondary: #333333;
    --border-color: #000000;

    --primary-color: #0066cc;
    --primary-dark: #0044aa;
}

/* 护眼模式 */
[data-theme="eye-care"] {
    --background-color: #f5f5dc;
    --surface-color: #fffaf0;
    --text-primary: #5d4037;
    --text-secondary: #8d6e63;
    --border-color: #d7ccc8;
}
```

---

## JavaScript架构设计

### 主应用文件 (main.js)

```javascript
// 配置文件
import { CONFIG } from './config.js';

// 工具函数
import * as Utils from './utils.js';

// 场景模块
import SimulationScene from './scene.js';

// 应用主类
class App {
    constructor() {
        this.scene = null;
        this.quiz = null;
        this.progress = null;
        this.analytics = null;
        this.initialized = false;
    }

    async init() {
        if (this.initialized) return;

        try {
            console.log('正在初始化应用...');

            // 初始化场景
            await this.initScene();

            // 初始化组件
            await this.initComponents();

            // 绑定事件
            await this.bindEvents();

            this.initialized = true;
            console.log('应用初始化完成！');

        } catch (error) {
            console.error('应用初始化失败:', error);
            Utils.showError('应用初始化失败，请刷新页面重试。');
        }
    }

    async initScene() {
        const container = document.getElementById('scene-container');
        if (!container) {
            throw new Error('场景容器不存在');
        }

        this.scene = new SimulationScene(container);
        await Utils.wait(100);
    }

    async initComponents() {
        // 初始化各个组件
        // ...
    }

    async bindEvents() {
        // 绑定事件
        // ...
    }

    dispose() {
        // 清理资源
        if (this.scene) {
            this.scene.dispose();
        }
    }
}

// 启动应用
document.addEventListener('DOMContentLoaded', async () => {
    const app = new App();
    await app.init();
    window.app = app;
});

export default App;
```

### 配置文件 (config.js)

```javascript
// 应用配置
export const CONFIG = {
    app: {
        name: '教材虚拟仿真系统',
        version: '1.0.0',
        debug: true
    },
    scene: {
        backgroundColor: 0x000000,
        cameraPosition: { x: 0, y: 5, z: 10 },
        enableShadows: true,
        antialias: true
    },
    ui: {
        theme: 'default',
        language: 'zh-CN',
        animations: true
    },
    analytics: {
        enabled: true,
        trackActions: true,
        saveProgress: true
    },
    performance: {
        targetFPS: 60,
        enableLOD: true,
        enableObjectPool: true
    }
};

// 导出配置
export default CONFIG;
```

### 工具函数文件 (utils.js)

```javascript
// 工具函数集合

// 防抖函数
export function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// 节流函数
export function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// 等待函数
export function wait(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// 格式化时间
export function formatTime(ms) {
    const seconds = Math.floor(ms / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);

    return `${hours.toString().padStart(2, '0')}:${(minutes % 60).toString().padStart(2, '0')}:${(seconds % 60).toString().padStart(2, '0')}`;
}

// 显示错误
export function showError(message) {
    console.error(message);
    alert(message);
}

// 显示消息
export function showMessage(message, type = 'info') {
    console.log(message);
}
```

---

## 组件模板

### 3D场景组件模板

```javascript
// 3D场景组件模板
class SceneComponent {
    constructor(container) {
        this.container = container;
        this.scene = null;
        this.camera = null;
        this.renderer = null;
    }

    init() {
        // 初始化场景
        this.createScene();
        this.createCamera();
        this.createRenderer();
        this.addObjects();
        this.animate();
    }

    createScene() {
        // 创建场景
    }

    createCamera() {
        // 创建相机
    }

    createRenderer() {
        // 创建渲染器
    }

    addObjects() {
        // 添加对象
    }

    animate() {
        // 动画循环
        requestAnimationFrame(() => this.animate());
        this.renderer.render(this.scene, this.camera);
    }

    dispose() {
        // 清理资源
    }
}

export default SceneComponent;
```

### 测验组件模板

```javascript
// 测验组件模板
class QuizComponent {
    constructor(questions) {
        this.questions = questions;
        this.currentQuestion = 0;
        this.score = 0;
    }

    render(container) {
        // 渲染测验界面
    }

    checkAnswer(answer) {
        // 检查答案
    }

    showResults() {
        // 显示结果
    }

    nextQuestion() {
        // 下一题
    }

    reset() {
        // 重置测验
    }
}

export default QuizComponent;
```

---

## 响应式设计

### 断点系统

```css
/* 断点系统 */
:root {
    --breakpoint-xs: 480px;
    --breakpoint-sm: 576px;
    --breakpoint-md: 768px;
    --breakpoint-lg: 992px;
    --breakpoint-xl: 1200px;
    --breakpoint-xxl: 1400px;
}
```

### 响应式布局策略

1. **移动优先**：从移动端开始设计，逐步增强
2. **流式布局**：使用百分比和flex布局
3. **媒体查询**：针对不同设备优化
4. **触摸优化**：优化触摸交互

---

## 性能优化

### CSS优化

1. **减少重排重绘**：合理使用transform和opacity
2. **CSS压缩**：生产环境压缩CSS
3. **按需加载**：按需加载CSS文件
4. **避免过度嵌套**：减少CSS选择器复杂度

### JavaScript优化

1. **代码分割**：使用ES6模块按需加载
2. **懒加载**：延迟加载非关键代码
3. **防抖节流**：优化事件处理
4. **内存管理**：及时清理不再使用的对象

---

## 可访问性

### 语义化HTML

1. 使用正确的HTML标签
2. 提供替代文本
3. 使用ARIA属性
4. 键盘导航支持

### 颜色对比度

1. 确保文本和背景对比度符合WCAG标准
2. 支持高对比度模式
3. 避免仅依赖颜色传达信息

---

## 总结

本指南提供了完整的Web应用模板设计，包括HTML结构、CSS样式、JavaScript架构以及响应式设计原则。遵循这些模板和原则，可以创建出美观、响应式、高性能的虚拟仿真系统Web应用。

模板设计注重：
- **用户体验**：直观易用的界面
- **性能**：优化的加载和渲染性能
- **可维护性**：清晰的代码结构
- **可扩展性**：易于添加新功能
- **可访问性**：支持各种用户需求