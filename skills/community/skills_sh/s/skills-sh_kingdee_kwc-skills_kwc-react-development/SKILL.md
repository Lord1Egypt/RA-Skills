---
name: kwc-react-development
description: 【由 kwc-project-scaffold 调度】仅负责 React 组件代码编写，不直接承接用户需求，不创建文件。所有 KWC 需求和文件创建必须先经 kwc-project-scaffold。
---

# KWC React 开发专家

当项目确认使用 React 框架后，本 Skill 负责该框架下的代码编写规范与组件使用指导。

## 重要：使用前置条件

**必须同时满足以下条件才能使用本 Skill：**
1. 当前目录已存在 `.kd/config.json` 文件
2. 配置文件中 `framework` 字段值为 `react`
3. 工程已通过 `kwc-project-scaffold` 完成初始化

**以下场景禁止使用本 Skill，必须交由 `kwc-project-scaffold`：**
- 工程初始化（`kd project init`）
- 创建组件或页面（`kd project create`）
- 生成或修改 `.js-meta.kwc` 组件元数据
- 生成或修改 `.page-meta.kwp` 页面元数据
- 环境配置（`kd env` 相关命令）
- 部署操作（`kd project deploy`）
- 调试操作（`kd debug`）— 调试由 kwc-project-scaffold 负责，须以后台模式运行（`is_background: true`），详见其调试约定

若当前不满足上述前置条件，请立即停止并切换到 `kwc-project-scaffold` Skill。

## 核心职责
你负责指导用户进行 KWC React 组件的开发、修改和维护。
**重要**：你必须严格遵守**本 Skill 目录下的** `rule.md` 文件中定义的硬性约束。在开始任何代码编写前，请务必阅读并理解这些规则。

## 1. 环境上下文确认
- **项目根目录**：包含 `.kd` 文件夹和 `app/kwc` 目录。
- **配置环境**：`.kd/config.json` 中 `framework` 为 `react`。
- **重要**：若当前环境**不满足**上述条件，**必须立即停止**使用本 Skill 的所有约束，转而按**通用 React Web 项目**标准协助用户。

## 2. 标准工作流 (Workflow)

1. **新建组件**：
   - **必须**使用 CLI 工具，严禁手工创建文件：
     ```bash
     kd project create [组件名] --type kwc
     ```
   - 组件命名遵循 `PascalCase`。

2. **代码实现与修改**：
   - **学习**：优先参考 `app/kwc/exampleComponent` 和 **本 Skill 目录下的**`rule.md` 中的开发范例。
   - **严格合规**：代码必须符合**本 Skill 目录下的** `rule.md` 中的所有约束（React Wrapper 导入、onSl* 事件等）。
   - **Shoelace 集成**：涉及 Shoelace 组件时，确保正确使用 React Wrapper 和类型导入。

3. **验证与交付**：
   - 按项目入口更新 `app/kwc/main*` 引用。
   - 运行 `npm run dev` 进行验证。

## 3. 关键约束摘要 (详细请见本 Skill 目录下的 rule.md)
- **导入**：`import SlInput from '@kdcloudjs/shoelace/dist/react/input/index.js';`
- **业务组件导入**：`import SlLookup from '@kdcloudjs/shoelace-biz/dist/react/lookup/index.js';`（注意包名为 `shoelace-biz`）
- **类型**：`import type SlInputElement from '@kdcloudjs/shoelace/dist/components/input/input.js';`
- **JSX**：`<SlInput onSlChange={handleChange} />`
- **事件**：必须映射为 `onSl*`，且使用 `CustomEvent` 类型断言
- **CSS**：样式必须使用 Shoelace Design Token（`var(--sl-color-*)`、`var(--sl-spacing-*)`、`var(--sl-font-size-*)`、`var(--sl-border-radius-*)`），禁止硬编码 hex 色值和 px 数值。详见 `./reference/css-design-tokens.md`。

## 4. 常用资源
- **扩展组件文档**（位于本 Skill 的 `reference/` 目录下）：
  - **基础扩展组件**（`@kdcloudjs/shoelace`）：
  - Table: `reference/table/index.md`
  - DatePicker: `reference/datepicker/index.md`
  - TimePicker: `reference/sl-timepicker.md`
  - Pagination: `reference/sl-pagination.md`
  - Daterangepicker: `reference/sl-daterangepicker.md`
  - ThoughtChain: `reference/sl-thought-chain.md`
  - Nav: `reference/sl-nav.md`
  - XMarkdown: `reference/sl-xmarkdown.md`
  - Think: `reference/sl-think.md`
  - TreeSelect: `reference/sl-tree-select.md`
  - Cascader: `reference/sl-cascader.md`
  - FloatButton: `reference/sl-float-button.md`
  - FloatButtonGroup: `reference/sl-float-button.md`
  - Sender: `reference/sender/index.md`
  - SenderHeader: `reference/sender/index.md`
  - SenderSwitch: `reference/sender/index.md`
  - Steps: `reference/sl-steps.md`
  - Grid: `reference/sl-grid.md`
  - Notification: `reference/sl-notification.md`
  - RadioGroup: `reference/sl-radio-group.md`
  - Space: `reference/sl-space.md`
  - Upload: `reference/upload/index.md`
  - Segmented: `reference/sl-segmented.md`
  - Transfer: `reference/sl-transfer.md`
  - Popconfirm: `reference/sl-popconfirm.md`
  - Bubble: `reference/sl-bubble.md`
  - **业务组件**（`@kdcloudjs/shoelace-biz`，导入路径为 `@kdcloudjs/shoelace-biz/dist/react/...`）：
  - Lookup (F7): `reference/sl-lookup.md`
  - **使用前必须阅读相应文档**。
- **标准组件文档**：[https://shoelace.style/](https://shoelace.style/)

## 5. 输出检查清单
提交代码前，请自查：
- [ ] 新建组件使用了 `kd project create [组件名] --type kwc`
- [ ] 导入路径包含 `/index.js` (组件) 和 `/[component]/[component].js` (类型，如 `button/button.js`)
- [ ] 事件命名使用 `onSl*` 前缀
- [ ] 针对 Event Target 进行了正确的类型断言
- [ ] 严格参考了 `rule.md` 中的 Strict Template
- [ ] **未运行**任何 ESLint/Prettier 修复命令
