---
name: test-case-design
description: 这项技能应在为特定场景或者功能生成测试用例、编写测试用例、设计测试用例、补充异常场景和边界值、设计复杂交互测试用例、输出标准化测试用例，比如：功能测试、兼容性测试、适应性测试、API 测试、UI 可视化测试、移动端/应用/小程序/H5/桌面/PC 网页测试、AI agent测试、联动测试或路由测试等场景中使用。仅专注于编写测试用例，不涉及测试计划、测试策略或自动化脚本。
---

## 执行流程

1. **识别用例类型**：
   - 含"接口测试"/"API 测试" → 接口测试用例
   - 含"AI agent测试"/"Agent 测试"/"Agent"/"智能体" → Agent 测试用例
   - 默认 → 功能测试用例
2. **加载能力文件**：始终加载 `references/templates/common-rules.md`（规则），能力文件按类型选择：
   - 接口测试 → `references/core-capabilities/api-testing.md`
   - Agent 测试 → `references/core-capabilities/agent-testing.md`+ `references/core-capabilities/functional-testing.md中的第一部分：测试用例设计方法+第二部分：测试用例质量标准` 
   - 功能测试 → `references/core-capabilities/functional-testing.md`
3. **加载平台专项**（接口测试跳过此步骤）：
   - 匹配平台关键词 → 加载 `references/platform/{平台}.md`
4. **生成用例**：按加载的能力文件以及平台专项生成测试用例
5. **自查**：
   - 接口测试 → `references/checklists/api-checklist.md`
   - Agent 测试 → `references/checklists/agent-checklist.md` + `references/checklists/common-checklist.md中的一、功能测试检查清单`
   -  Agent 测试+平台 → `references/checklists/agent-checklist.md` + `references/checklists/common-checklist.md中的一、功能测试检查清单`+  `references/checklists/{平台}-checklist.md`
   - 功能测试+平台 → `references/checklists/common-checklist.md`+ `references/checklists/{平台}-checklist.md` 
   - 功能测试无平台 → `references/checklists/common-checklist.md`
6. **输出**：按 `references/examples/format-spec.md` 规定的表格格式，Markdown 表格输出

## 能力边界
✅ 可生成：功能测试、接口测试、AI agent测试（含 Agent 安全与边界）、平台专项测试
❌ 不可生成：测试方案、测试策略、测试计划、渗透测试执行、漏洞扫描、性能压测（并发/压力/负载）、自动化脚本

## 指令映射表

> 规则文件始终加载 `references/templates/common-rules.md`。能力文件按用例类型选择，平台文件按需叠加。

### 能力文件

| 关键词触发 | 加载 | 说明 |
|-----------|------|------|
| "接口测试"、"API 测试" | `references/core-capabilities/api-testing.md` | 独立使用，不叠加平台 |
| "Agent 测试"、"Agent"、"智能体" | `references/core-capabilities/agent-testing.md`+`references/core-capabilities/functional-testing.md中的第一部分：测试用例设计方法+第二部分：测试用例质量标准` | 可叠加任意平台 |
| 默认 | `references/core-capabilities/functional-testing.md` | 功能测试 |

### 平台文件（叠加到能力文件之上，接口测试除外）

| 关键词触发 | 加载 | 说明 |
|-----------|------|------|
| "移动端测试"、"App 测试" | `references/platform/mobile-app.md` | 手势/中断/网络/权限/推送/兼容/性能 |
| "小程序测试" | `references/platform/mini-program.md` | 生命周期/授权/分享/支付/跳转/订阅 |
| "移动 Web 测试"、"H5 测试" | `references/platform/mobile-web.md` | 响应式/触摸/浏览器/视口/H5/SEO |
| "桌面端测试"、"桌面应用测试" | `references/platform/desktop.md` | 窗口/快捷键/文件/系统集成/多显示器 |
| "PC Web 测试"、"Web 端测试" | `references/platform/pc-web.md` | 浏览器/布局/键盘/表单/会话/路由/拖拽 |
