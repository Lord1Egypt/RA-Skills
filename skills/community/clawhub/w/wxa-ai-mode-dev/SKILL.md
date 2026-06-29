---
name: wxa-ai-mode-dev
description: 微信小程序 AI 开发模式（beta）完整开发指南。当开发者需要将小程序改造为 AI 开发模式、封装 SKILL、编写原子接口/原子组件、编写 SKILL.md 或 mcp.json 时触发。覆盖接入流程、项目结构、Schema 设计、content 文本写法、组件约束、最佳实践、常见反例的全部规范。
metadata:
  author: TencentCloudBase
  version: '0.1.0'
compatibility: [微信小程序基础库 ≥3.16.1, iOS 微信 ≥8.0.74]
---

# wxa-ai-mode-dev — 小程序 AI 开发模式（beta）开发指南

小程序 AI 开发模式（以下简称此模式）提供了一套智能化的运行环境和开发框架。开发者将小程序功能抽象为**原子接口（API）**和**原子组件（Component）**，封装成 **SKILL**，供小程序 AI 调用。

当用户通过小程序 AI 发起对话时，小程序 AI 通过**小程序 MCP 协议**选择合适的原子接口和原子组件，完成数据处理和任务执行，最终以 GUI 卡片展示结果。用户身份与原小程序保持一致（可通过 storage 共享登录凭证）。

> **当前处于内测阶段**，暂未开放代码提审。仅支持 iOS（微信 ≥8.0.74），基础库 ≥3.16.1。**请勿将 AI 模式代码合入正式版本提交审核。**

## 职责边界

- ✅ 提供 AI 开发模式的完整技术规范参考
- ✅ 定义原子接口/组件的设计规范、最佳实践和禁令
- ✅ 定义 content 文本写法、description 三段式模板、注意力权重原则
- ✅ 提供接入配置、调试流程、FAQ 的完整指引
- ❌ 不生成业务原子接口/组件代码（交给 `wxa-skills-generate`）
- ❌ 不执行校验和修复（交给 `wxa-skills-validate`）
- ❌ 不进行端到端评测（交给 `wxa-skills-eval`）
- ❌ 不创建新小程序项目（交给 `wxa-create-ai-miniprogram`）
- 📦 交付：参考文档 + 规范说明

## 术语约定

| 概念 | 说明 |
|------|------|
| **小程序 MCP** | 向小程序 AI 暴露可调用能力的协议，与标准 MCP 不同，适配小程序开发特点 |
| **原子接口（API）** | 最小执行单元，封装单一业务功能，标准化输入/输出，运行在微信客户端**独立 JS 环境** |
| **原子组件（Component）** | 原子接口的可视化展示单元，将结构化数据渲染为 **GUI 卡片**展示在对话流中 |
| **SKILL** | 完成特定场景任务的完整能力封装，包含 `SKILL.md`、`mcp.json`、原子接口实现、原子组件实现 |

## 参考资料索引

| 来源 | 用途 | 加载时机 |
|------|------|---------|
| `references/ARCHITECTURE.md` | 三层架构与数据传递（上下文隔离、LLM 可见性） | 首次阅读架构时 |
| `references/CONFIGURATION.md` | app.json 配置、SKILL 目录结构、page-meta.json | 接入配置时 |
| `references/API_SPEC.md` | 原子接口/组件实现规范、mcp.json Schema、wx.modelContext API 速查 | 编写代码时 |
| `references/COMPONENT_CONSTRAINTS.md` | 原子组件硬性约束、WXSS 范围、内置组件支持 | 设计组件时 |
| `references/BEST_PRACTICES.md` | 注意力权重、内容分工、三段式模板、content 写法、禁令集、SOP 写法 | 编写 content/description 时 |
| `references/DEBUGGING.md` | 调试与评测指引、FAQ 速查 | 调试/排查问题时 |
| `wxa-skills-generate/SKILL.md` | 代码生成器的工作流 | 需要生成代码时 |
| `wxa-skills-validate/SKILL.md` | 校验器的工作流和修复流程 | 需要校验时 |
| `wxa-skills-eval/SKILL.md` | 评测引擎的使用方式 | 需要评测时 |

## 硬性约束

### A. 接入前置条件

| 条件 | 说明 |
|------|------|
| 微信小程序基础库 ≥3.16.1 | 否则无法使用 wx.modelContext API |
| iOS 微信 ≥8.0.74 | 安卓/鸿蒙暂不支持真机 |
| 已在公众平台申请 AI 开发模式 | 在「基础功能 - AI 能力」申请 |
| SKILL 必须在独立分包中 | `subPackages[].independent: true` |
| 必须开启 `lazyCodeLoading: "requiredComponents"` | 否则独立分包加载异常 |

### B. 平台限制

| 限制项 | 说明 |
|--------|------|
| 最多 30 个 SKILL | app.json 中 agent.skills 数组上限 |
| 一个 SKILL 只能在一个分包中 | 不可跨分包引用 |
| 原子接口超时上限 300s | 含中间件链的总耗时 |
| SKILL.md ≤16000 字节 | 固定文件名，大小限制 |
| mcp.json ≤24000 字符 | 不计 outputSchema 的体积 |
| page-meta.json ≤8000 字节 | 文字链元数据体积限制 |

### C. 阻断规则（立即停止）

| 阻断情况 | 处理方式 |
|---------|---------|
| 用户描述的场景在现有社区 Skill 中已存在 | 建议 `wxa-find-skills` 搜索安装，不重复创建 |
| 基础库版本低于 3.16.1 | 提示升级基础库 |
| 用户未在公众平台申请 AI 模式 | 引导先去申请 |
| 用户需要生成业务代码 | 转 `wxa-skills-generate` |

## 工作流

### Step 0 — 环境检查

确认以下条件是否满足：

- 微信小程序基础库 ≥3.16.1
- iOS 微信 ≥8.0.74（真机）
- 已在公众平台「基础功能 - AI 能力」申请开发模式
- 开发者工具已安装 Nightly 版本

如不满足，告知用户需要准备的条件。

### Step 1 — 了解需求

与用户对话，明确当前需要 AI 开发模式的哪方面帮助：

| 用户诉求 | 加载内容 |
|---------|---------|
| 了解整体架构 | `references/ARCHITECTURE.md` |
| 配置接入 | `references/CONFIGURATION.md` |
| 编写原子接口/组件 | `references/API_SPEC.md` + `references/COMPONENT_CONSTRAINTS.md` |
| 编写 content/description | `references/BEST_PRACTICES.md` |
| 调试排查 | `references/DEBUGGING.md` |
| 需要生成代码 | 转 `wxa-skills-generate` |

### Step 2 — 提供规范参考

根据 Step 1 的诉求，加载对应的 references 文件，向用户提供规范说明。

### Step 3 — 交棒

根据用户下一步动作交棒到对应工具：

- 需要生成代码 → `wxa-skills-generate`
- 需要校验 → `wxa-skills-validate`
- 需要评测 → `wxa-skills-eval`
- 需要创建新项目 → `wxa-create-ai-miniprogram`
- 需要搜索社区 Skill → `wxa-find-skills`
- 需要创建自定义 Skill → `wxa-create-mp-skill`

---

## 核心规范（完整内容）

以下为 AI 开发模式的核心规范。详细内容按主题拆分到 `references/` 目录下，此处提供摘要速查。

### 三层架构与数据传递

```
[原子接口上下文 A] ──── 返回值(content/structuredContent/_meta) ────→ [小程序 AI 后台]
[原子组件上下文 B] ─┐
[实时动态组件上下文 C]┘ 三个上下文全局变量不共享，数据只能通过返回值传递
[半屏页面] ───────── 与小程序运行环境一致，部分接口受限
```

| 返回值字段 | LLM 可见 | 用途 |
|-----------|---------|------|
| `content` | ✅ | LLM 决策的上下文和指令（TextContent[]，≤200KB） |
| `structuredContent` | ✅ | LLM 理解屏幕展示内容的结构化数据（≤200KB） |
| `_meta` | ❌ | 纯渲染数据，如图片 URL，对 LLM 不可见（≤200KB） |

### 注意力权重原则（核心方法论）

| 优先级 | 信息源 | 作用 |
|--------|--------|------|
| ★★★★★ | 原子接口返回的 `content` | 离决策点最近，LLM 当"事实承接 + 直接指令"理解 |
| ★★★★ | `mcp.json` 的 `description` | 首句决定接口选择准确率 |
| ★★★★ | `inputSchema` 字段 `description` | 参数填充的核心参考 |
| ★★★ | `SKILL.md` | 业务流程编排、跨接口规则、意图分流 |

多处约束冲突时，LLM 遵循高权重位置的指令。核心约束不应全依赖 `SKILL.md`，硬约束应通过 `content` 或 `description` 字段说明。

### 字段 description 三段式模板

```
<字段语义（一句话）>。
取值来源：<用户原话 / 上游接口 X 返回的 Y 字段 / 枚举集合>。
【禁止编造】<用户未提供 / 上下文无来源 / 越界> 时，<反问用户『…』 / 改走接口 Z / 留空>。
```

三段缺一不可：前两段决定模型能不能填对，第三段决定模型不会"硬填"。

### 常见禁令

- 禁止裸指令：所有成功返回的接口（`isError=false`）且绑定组件的，**必须展示卡片**
- 禁止 ID 编造：`drinkId` / `orderId` / `itemId` 等必须来自上游接口返回的原值
- 禁止并发调用支付类接口：`payOrder` / `createOrder` 须等上一笔结束后再发起
- 禁止在 `structuredContent` 中放图片 URL
- 动作类接口必须先调成功（`isError=false`）再向用户宣布结果
- 枚举值必须使用英文枚举，禁止中文 label

### content 文本写法

✅ 正确：事实陈述 + 业务动作两段式

```
"已查到该 orderId 的机票订单数据。请把本次接口返回的卡片数据展示给用户，并用简短一句话引导用户查看。"
```

❌ 反例：裸指令

```
"接下来请务必为用户展示订单确认卡片"
```

---

## 相关链接

- [微信官方文档](https://developers.weixin.qq.com/miniprogram/dev/ai/guide.html)
- [官方 demo](https://github.com/wechat-miniprogram/ai-mode-demo)
- [微信开放社区 - 小程序 AI 能力专区](https://developers.weixin.qq.com/community/minihome/mixflow/4547794673309990912)
- [mp-skills 工具](https://github.com/TencentCloudBase/mp-skills)
