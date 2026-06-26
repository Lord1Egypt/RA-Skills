# 详细工作流程

本文档提供 web-fixing 技能的详细工作流程，补充 SKILL.md 中的核心内容。

## 完整修复流程

### 步骤 0：准备环境

在开始修复前，确保：
- 安装必要的浏览器开发工具
- 配置 Playwright 测试环境
- 准备测试设备或模拟器
- 开启浏览器自动刷新

### 步骤 1：问题收集与分类

#### 1.1 收集用户报告

**必需信息：**
- 问题描述（用户看到的症状）
- 复现步骤（如何触发问题）
- 预期行为（应该发生什么）
- 实际行为（实际发生了什么）
- 环境信息（浏览器、设备、操作系统）

**信息收集模板：**
```
问题：[简洁描述]
复现步骤：
1.
2.
3.
预期：
实际：
环境：
- 浏览器：
- 设备：
- 屏幕尺寸：
```

#### 1.2 问题分类

根据症状分类问题：

**类别 A：样式问题**
- 布局错位
- 颜色/字体错误
- 间距问题
- 视觉不一致

**类别 B：功能问题**
- JavaScript 错误
- 交互失效
- 表单问题
- 数据加载失败

**类别 C：性能问题**
- 加载缓慢
- 动画卡顿
- 内存泄漏
- 高 CPU 使用

**类别 D：兼容性问题**
- 特定浏览器异常
- 移动端显示错误
- 触摸交互问题

### 步骤 2：初步诊断（2026 增强版）

#### 2.1 快速视觉检查

**打开页面并观察：**
- 页面是否完整渲染
- 布局是否明显错乱
- 是否有明显的样式冲突
- 控制台是否有红色错误

**使用浏览器工具：**
1. 右键 → 检查元素
2. 查看元素面板
3. 检查样式面板
4. 观察控制台

**2026 新增：AI 辅助诊断**
- 使用 Chrome DevTools AI 功能分析问题
- 让 AI 解释复杂的错误堆栈
- 请求 AI 生成可能的修复建议
- 使用 AI 分析样式冲突

#### 2.2 控制台分析（增强）

**错误级别：**
- **红色错误（Error）**：阻止执行，优先修复
- **黄色警告（Warning）**：潜在问题，调查影响
- **蓝色信息（Info）**：调试信息，了解上下文

**常见错误模式：**
```
Uncaught TypeError: Cannot read property 'X' of undefined
→ 检查对象是否正确初始化

Uncaught ReferenceError: X is not defined
→ 检查变量名拼写和作用域

404 Not Found: /path/to/resource
→ 检查资源路径是否正确

CORS policy: No 'Access-Control-Allow-Origin' header
→ 检查跨域配置
```

#### 2.3 网络请求检查（增强）

**Network 面板分析：**
1. 打开 Network 面板
2. 刷新页面
3. 检查所有请求的状态码
4. 查看请求和响应详情

**关键检查点：**
- 所有资源是否成功加载（200 状态码）
- 是否有失败的请求（红色）
- 加载时间是否过长
- API 响应是否正确

**2026 新增：高级网络分析**
- **请求重放**：在控制台重新发送 XHR 请求测试
- **请求拦截**：使用 Local Overrides 测试本地修复
- **网络节流**：模拟不同网络条件（3G、4G、离线）
- **CORS 调试**：详细分析跨域请求问题

### 步骤 3：深度根因分析

#### 3.1 元素级分析

**检查 HTML 结构：**
```html
<!-- 确认 DOM 结构 -->
<div class="container">
  <div class="item">内容</div>
</div>
```

**验证 CSS 选择器：**
```css
/* 检查选择器是否匹配 */
.container .item {
  /* 样式是否生效 */
}
```

**检查计算样式：**
- 浏览器开发工具 → Computed
- 查看最终应用的样式值
- 识别样式覆盖问题

#### 3.2 JavaScript 执行追踪（2026 增强）

**断点调试（高级技巧）：**
1. 打开 Sources 面板
2. 在可疑行设置断点
3. 触发问题
4. 检查变量值和调用栈

**2026 新增断点类型：**
- **条件断点**：`x > 100` 或 `element.classList.contains('error')`
- **DOM 断点**：监听元素移除、属性修改、子树变化
- **事件监听器断点**：拦截特定事件（如 click、load）
- **异常断点**：在所有未捕获异常处暂停
- **日志断点**：不暂停执行，只输出表达式值

**console.log 调试（增强）：**
```javascript
// 记录关键变量
console.log('当前状态：', state);
console.log('元素位置：', element.getBoundingClientRect());

// 2026 新增：表格输出
console.table([
  { name: 'Item 1', value: 100 },
  { name: 'Item 2', value: 200 }
]);

// 分组输出
console.group('调试信息');
console.log('状态 1:', data1);
console.log('状态 2:', data2);
console.groupEnd();

// 性能测量
console.time('operation');
// ... 操作
console.timeEnd('operation');
```

**性能分析（增强）：**
- Performance 面板 → 录制
- 执行问题操作
- 分析火焰图
- 识别性能瓶颈
- **2026 新增**：Performance Observer API 自动监控
  ```javascript
  const observer = new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      console.log(entry.name, entry.duration);
    }
  });
  observer.observe({ entryTypes: ['measure', 'navigation'] });
  ```

#### 3.3 样式优先级分析

**CSS 特异性计算：**
```
内联样式 (1000) > ID (100) > 类/属性/伪类 (10) > 元素/伪元素 (1)

示例：
#nav .item (100 + 10 = 110)
.nav .item (10 + 10 = 20)
```

**检查样式覆盖：**
- 开发工具 → Styles 面板
- 查看被划掉的样式
- 识别更高优先级规则

### 步骤 4：形成假设

#### 4.1 假设模板

**格式化假设陈述：**
```
假设：[根本原因]
证据：[观察到的现象]
测试：[如何验证假设]
预期结果：[如果假设正确，应该看到什么]
```

**示例：**
```
假设：移动端导航栏溢出是由于固定宽度导致
证据：
- 在桌面浏览器缩小时出现溢出
- 计算样式显示 nav-width: 1200px
测试：将宽度改为 100%
预期结果：导航栏适应屏幕宽度
```

#### 4.2 假设优先级

**优先处理：**
1. 导致功能完全失效的问题
2. 影响所有用户的问题
3. 安全相关问题
4. 性能严重下降

**延后处理：**
1. 视觉微调
2. 边缘情况
3. 浏览器特定小问题

### 步骤 5：最小化测试

#### 5.1 创建隔离测试

**HTML 测试文件：**
```html
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <!-- 只包含问题元素 -->
  <div class="problematic-element">测试</div>

  <script>
    // 最小化复现代码
  </script>
</body>
</html>
```

**CSS 测试：**
```css
/* 只应用相关样式 */
.problematic-element {
  /* 复制原始样式 */
}
```

#### 5.2 二分测试

**逐步排除法：**
1. 禁用所有 CSS
2. 逐个启用样式规则
3. 识别导致问题的规则
4. 进一步缩小范围

**使用注释：**
```css
/* 禁用一半规则 */
/*
.rule1 { }
.rule2 { }
*/
.rule3 { }  <!-- 测试这部分 -->
```

### 步骤 6：实施修复

#### 6.1 修复优先级

**立即修复：**
- 阻止核心功能
- 安全漏洞
- 数据丢失风险

**计划修复：**
- 非关键 UI 问题
- 性能优化
- 兼容性改进

**记录延后：**
- 边缘情况
- 低优先级改进

#### 6.2 修复模式

**样式修复：**
```css
/* 修复前 */
.element {
  width: 100%;
  float: left;
}

/* 修复后 - 使用现代布局 */
.element {
  width: 100%;
  display: flex;
  flex-wrap: wrap;
}
```

**JavaScript 修复：**
```javascript
// 修复前 - 可能报错
function handleClick() {
  const button = document.querySelector('.button');
  button.addEventListener('click', doSomething);
}

// 修复后 - 添加存在检查
function handleClick() {
  const button = document.querySelector('.button');
  if (button) {
    button.addEventListener('click', doSomething);
  }
}
```

**响应式修复：**
```css
/* 修复前 - 固定宽度 */
.container {
  width: 1200px;
}

/* 修复后 - 响应式宽度 */
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

@media (max-width: 768px) {
  .container {
    padding: 0 20px;
  }
}
```

### 步骤 7：验证与测试

#### 7.1 功能验证

**检查清单：**
- [ ] 原问题已解决
- [ ] 没有引入新问题
- [ ] 相关功能正常
- [ ] 边缘情况处理

#### 7.2 跨浏览器测试

**主要浏览器：**
- Chrome（最新版本）
- Firefox（最新版本）
- Safari（最新版本）
- Edge（最新版本）

**移动浏览器：**
- iOS Safari
- Android Chrome

#### 7.3 响应式测试

**断点测试：**
- 移动端：320px - 480px
- 平板：481px - 768px
- 桌面：769px - 1024px
- 大屏：1025px+

**测试工具：**
- 浏览器开发工具 → 设备模拟
- 真实设备测试
- Playwright 自动化测试

#### 7.4 性能验证

**Lighthouse 评分：**
- Performance: > 90
- Accessibility: > 90
- Best Practices: > 90
- SEO: > 90

**关键指标：**
- First Contentful Paint (FCP) < 1.8s
- Largest Contentful Paint (LCP) < 2.5s
- Cumulative Layout Shift (CLS) < 0.1
- First Input Delay (FID) < 100ms

### 步骤 8：文档与复盘

#### 8.1 记录修复

**修复报告模板：**
```markdown
## 问题
[问题描述]

## 根本原因
[根因分析]

## 修复方案
[实施的修复]

## 测试验证
- [ ] 功能正常
- [ ] 跨浏览器兼容
- [ ] 响应式正常
- [ ] 性能无下降

## 相关文件
- 修改的文件列表
```

#### 8.2 复盘学习

**反思问题：**
- 这个问题如何避免？
- 需要添加什么检查？
- 是否需要改进开发流程？

**预防措施：**
- 添加自动化测试
- 实施代码审查
- 更新开发规范
- 改进文档

## 高级工作流程

### 性能问题排查流程

1. **Performance 面板录制**
   - 录制页面加载和交互
   - 分析火焰图
   - 识别长任务

2. **Lighthouse 审计**
   - 运行完整审计
   - 查看建议
   - 优先处理高影响项目

3. **网络优化**
   - 检查资源大小
   - 启用压缩
   - 实施 CDN

4. **渲染优化**
   - 减少 reflow/repaint
   - 使用 transform 和 opacity
   - 实施懒加载

### 兼容性问题排查流程

1. **特性检测**
   ```javascript
   if ('IntersectionObserver' in window) {
     // 使用现代 API
   } else {
     // 提供回退方案
   }
   ```

2. **Polyfill 策略**
   - 识别缺失特性
   - 加载必要 Polyfill
   - 测试回退行为

3. **渐进增强**
   - 基础功能所有浏览器
   - 增强特性现代浏览器
   - 优雅降级旧浏览器

### 复杂问题排查流程

1. **问题分解**
   - 将大问题拆分成小问题
   - 逐个解决子问题
   - 整合解决方案

2. **对照测试**
   - 创建工作版本
   - 创建问题版本
   - 系统对比差异

3. **外部帮助**
   - 搜索类似问题
   - 查阅官方文档
   - 咨询社区

## 工作流程总结

```
问题收集 → 初步诊断 → 根因分析 → 形成假设
    ↓
最小化测试 ← 验证假设
    ↓
实施修复 → 全面验证 → 文档复盘
```

每个步骤都是必要的，跳过步骤会导致修复不彻底或引入新问题。
