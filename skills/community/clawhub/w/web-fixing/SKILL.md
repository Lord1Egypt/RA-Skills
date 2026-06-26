---
name: web-fixing
description: 修复网页和前端界面问题。当用户要求修复网页、调试前端、解决UI问题、修复样式、响应式布局错误、移动端显示异常、CSS问题、JavaScript报错、交互功能失效、生成网页后检查并修复时使用此技能。
---

## 快速概览

系统化修复网页和前端界面问题，四阶段调试方法论高效定位根本原因。

**核心铁律**：修复根因而非表面 → 每次只改一个问题 → 修复后必须验证

## 阶段 0：工具检测（可选）

开始修复前，根据项目需要检测可用工具：

- **内置**：Chrome DevTools（F12）、Lighthouse
- **可安装**：`npx playwright install --with-deps`（端到端测试）、`npm i -D web-vitals`（性能监控）
- **OpenClaw 工具**：browser snapshot/screenshot、web_fetch、read/edit/write

## 阶段 1：根因分析

在尝试任何修复之前，必须完成以下步骤：

**1.1 理解问题**
- 阅读错误信息和控制台输出
- 确认具体症状：样式错误 / 功能失效 / 性能问题 / 兼容性问题

**1.2 可视化检查**
- DevTools 检查元素 → Computed Styles → Box Model → DOM 结构

**1.3 控制台诊断**
- 错误信息、网络请求失败、JS 执行顺序、资源加载状态

**1.4 交叉验证**
- 多浏览器（Chrome/Firefox/Safari/Edge）+ 多设备尺寸（桌面/平板/手机）

## 阶段 2：模式识别

- 定位同代码库中正常工作的类似代码，对比差异
- 查阅文档（MDN、W3C）验证 API 和语法正确性
- 列出所有差异：HTML 结构、CSS 选择器、JS 逻辑、资源加载顺序

## 阶段 3：假设与测试

- 形成单一假设："我认为 X 是根因，因为 Y"
- 做最小更改验证，一次只改一个变量
- 有效 → 阶段 4；无效 → 新假设，不在失败修复上叠加

## 阶段 4：实施修复

- 创建最简复现案例，截图记录
- 实施单一修复，不做"顺带"改进
- 全面验证：修复生效？无新问题？跨浏览器？响应式正常？
- **3 次失败后停止**，质疑架构设计，考虑重构

## 前端修复策略

**布局**：Flexbox/Grid > 浮动；检查 box-sizing、overflow、position
**样式不生效**：验证选择器优先级、CSS 加载顺序、!important 滥用
**JavaScript**：读堆栈跟踪，检查作用域/闭包/事件绑定/DOM 加载时机
**响应式**：移动优先，用相对单位（rem/em/%），触摸目标 ≥44px
**兼容性**：查 Can I Use，CSS 前缀，Polyfill，多浏览器测试

**HTML 特殊字符转义**（高频踩坑点）：
生成包含代码片段的 HTML 时，必须用 escapeHTML() 转义 `< > & ' "`，动态内容优先用 textContent 而非 innerHTML。

**CSS 2026 新特性注意：**
- CSS Nesting 原生支持（Chrome 112+），DevTools 显示嵌套层级
- `:has()` 父选择器（Chrome 105+），注意性能避免过度嵌套
- `@layer` 级联层控制优先级，DevTools 可查看规则所属层级
- Container Queries 按容器尺寸响应，检查 container-type 定义

**Core Web Vitals（2024+ 标准）：**
- LCP < 2.5s、INP < 200ms（取代 FID）、CLS < 0.1

**构建工具调试：**
- Vite：`--debug --force`，检查 source map 和 HMR
- Next.js 15+ Turbopack：`next dev --turbo`，增量构建

## 反模式 vs 正确做法

| ❌ 错误 | ✅ 正确 |
|---------|---------|
| 跳过分析直接改代码 | 先理解问题再修复 |
| 同时改多个地方 | 一次只改一个 |
| 假设而非验证 | 形成假设并测试 |
| 修复症状非根因 | 追溯源头 |
| 忽略跨浏览器测试 | 多浏览器验证 |
| 不测响应式 | 多设备尺寸验证 |

## 修复检查清单

- [ ] 根本原因已识别并修复
- [ ] 原问题已解决，无新问题
- [ ] 多浏览器 + 多设备尺寸测试
- [ ] 控制台无错误/警告
- [ ] 动态内容已转义（HTML 特殊字符）
- [ ] Core Web Vitals 达标（LCP/INP/CLS）
- [ ] 代码可读性良好

## 详细参考

- `references/workflows.md` — 详细工作流程
- `references/checklist.md` — 完整检查清单
- `references/examples.md` — 真实修复案例
