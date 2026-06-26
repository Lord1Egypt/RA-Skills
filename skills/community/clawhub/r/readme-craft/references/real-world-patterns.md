# 实战模式

从 OMC (oh-my-claudecode)、ECC (Everything Claude Code) 等成功开源项目的 README 中提取的模式。

## OMC — 500 行，极简主义

### 模式：3 步 Quick Start

```
1. /plugin marketplace add REGISTRY_URL
2. /plugin install oh-my-claudecode
3. /setup
```

然后一个示例命令：`autopilot: build a REST API`。从零到跑通，60 秒。

**为什么有效：** 「Don't learn Claude Code. Just use OMC.」——一句话建立信任。读者不需要理解架构就能体验价值。

### 模式：Magic Keywords 表格

用表格展示触发词和行为，而非散文描述。每个关键词一行，示例命令一列。创造了「咒语般」的记忆感。

### 模式：特性对比表

用表格对比不同编排模式（Team Mode vs tmux CLI），而非在文字中解释区别。

### 模式：角色自动生成

`<!-- OMC:FEATURED-CONTRIBUTORS:START -->` 标记——Contributors 列表由脚本自动更新，不用手动维护。

### 模式：品牌角色形象

Quick Start 后放一张居中的角色图片（`.omc-character.jpg`），作为视觉分隔符和品牌元素。

---

## ECC — 1,388 行，百科全书式

### 模式：三栏图片导航

```
| Guide 1 | Guide 2 | Guide 3 |
```

三张并排图片链接到外部详细指南。创造了「课程体系」的感觉。README 保持文字为主，视觉入口引到外部。

### 模式：带注释的目录树

```
examples/          # Example projects
  gan-harness/     # GAN-style code generation
skills/            # 150+ reusable skills
  coding/          # Language-specific helpers
```

目录树不仅是文件列表，每行都有注释说明用途。既是 TOC 也是架构图。

### 模式：跨平台对比表

| Feature | Claude Code | Cursor | Codex | OpenCode |
|---------|:-:|:-:|:-:|:-:|

功能支持矩阵，一目了然。适合多平台/多环境项目。

### 模式：折叠 FAQ

```html
<details>
<summary>如何自定义 Agent？</summary>
详细回答...
</details>
```

用 `<details>/<summary>` 实现渐进式披露。FAQ 不占篇幅但随时可展开。

### 模式：Token 优化建议

README 中直接给出具体的 JSON 配置片段和成本降低百分比（「~60% cost reduction」）。把可操作的配置和量化收益放在一起。

### 模式：个人故事

「Background」节讲创作者的个人经历。增加真实感和可信度。

---

## GAN Harness — 127 行，纯技术文档

### 模式：成本估算表

| Project Type | Recommended Settings | Estimated Cost |
|-------------|---------------------|----------------|
| CLI tool | iterations=3, max_tokens=8000 | $15-30 |
| Full-stack app | iterations=5, max_tokens=16000 | $100-200 |

在 README 中公开成本信息，极其罕见但极有价值。让用户在使用前就能做预算。

### 模式：环境变量驱动

所有配置通过环境变量，Quick Start 直接展示四种 `GAN_*` 变量组合。零配置文件需求。

### 模式：零装饰

无 badges、无图片、无 shields。每个代码块都可直接复制粘贴执行。纯信息密度最大化。适合面向高级用户的内部工具。

---

## ClawHub Top Skills — 蒸馏来源

### adewale/good-readme

- 100 分制 6 维评分（22 项检查）
- 15 个反模式目录（带修复建议）
- 生态感知：npm / Rust / Python / Go 各有安装约定
- Create + Improve 双模式

### weiliu1031/writing-readme

- 7 步强制执行序列，带 `<HARD-GATE>` 断言
- 完成前 bash 验证（检查文件是否真的生成了）
- 双语输出（EN + CN）
- GIF demo 自动生成（vhs 自动安装 + 录制）
- SVG logo 自动生成（支持 dark/light mode `<picture>` 标签）
- 自打分循环：生成后跑评分，低于 90 分重来

### hidai25/readme-roast

- 基准对标：拿你的 README 和 116 个顶级 repo（480 万 star 合计）对比
- 6 分类权重：Hero(25%) + Visuals(20%) + Install(15%) + Trust(15%) + Structure(15%) + Differentiation(10%)
- 按项目类别（CLI/AI/Web/Testing/DevOps/Library）自动选择对标集

---

## 模式适用矩阵

| 模式 | 适合项目规模 | 适合受众 | 风险 |
|------|-------------|---------|------|
| 3 步 Quick Start | 任何 | 任何 | 过度简化复杂项目 |
| Magic Keywords 表 | 中大型 CLI | 高级用户 | 新手可能困惑 |
| 带注释目录树 | 大型/Monorepo | 贡献者 | 占篇幅，需保持更新 |
| 折叠 FAQ | 任何 | 混合受众 | GitHub Mobile 渲染可能有问题 |
| 成本估算 | 付费/资源密集 | 决策者 | 价格变动时必须更新 |
| 跨平台对比表 | 多平台工具 | 选型用户 | 维护负担重 |
| 品牌角色 | 社区驱动项目 | 大众用户 | 不适合严肃企业项目 |
| 个人故事 | 个人项目 | 潜在贡献者 | 企业项目避免 |
