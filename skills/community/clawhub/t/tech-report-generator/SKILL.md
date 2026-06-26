---
name: tech-report-generator
description: >
  面向新人培训的深度技术报告生成器。输入任意技术点（如 FlashAttention、MoE、LoRA、RLHF 等），
  自动产出结构化技术报告（Markdown + HTML），包含丰富的 SVG 可视化图示，
  并自动同步至 IMA 知识库和腾讯文档。适用于：生成技术报告、创建培训材料、产出技术分享文档、
  写技术 Tutorial、制作 Onboarding 文档。
  Use when the user asks to: generate tech reports, create training materials, write tutorials,
  make onboarding docs, or explain technical concepts in depth with visualizations.
  触发场景：技术报告、生成报告、写技术文档、技术分享、培训材料、Tutorial、Onboarding文档、
  深度技术解读、原理讲解、技术科普。
license: MIT-0
---

# 深度技术报告生成器

> 输入任意技术点，自动产出高质量结构化技术报告（含 SVG 可视化），并同步到 IMA 知识库和腾讯文档。

## 设计理念

- **面向新人友好**：由浅入深，先建立直觉再深入细节
- **图文并茂**：每个核心概念配 SVG 可视化图示，降低理解门槛
- **双格式产出**：Markdown（便于版本管理）+ HTML（便于分享阅读）
- **自动分发**：一键同步至 IMA 知识库和腾讯文档

## 报告生成流程

### Phase 1：需求分析

收到用户的技术主题后，确认以下信息：

1. **技术主题**：明确要讲解的技术点
2. **目标受众**：新人培训 / 团队分享 / 技术备忘（默认：新人培训）
3. **深度级别**：入门科普 / 原理详解 / 源码级（默认：原理详解）
4. **额外要求**：是否需要对比分析、版本演进、适用场景扩展等

### Phase 2：报告结构设计

按以下通用模板组织章节（根据具体技术灵活调整）：

```
1. 背景与动机
   - 解决什么问题？为什么现有方案不够好？
   - 直觉建立：用类比/对比让读者快速理解核心矛盾

2. 核心思想
   - 一句话总结（核心 insight）
   - 关键技术拆解（2-3 个核心技术点）
   - 对比表格：旧方案 vs 新方案

3. 关键技巧 / 数学原理
   - 核心公式推导（保持简洁，逐步展开）
   - 为什么这样设计（直觉解释）

4. 完整算法 / 系统流程
   - 伪代码或流程图
   - 前向 + 反向（如适用）

5. 性能分析
   - 复杂度对比表格
   - 实验数据 / Benchmark 结果
   - 加速效果图

6. 适用范围与变体
   - 支持哪些场景/变体
   - 对比表格（各变体支持情况）
   - 限制条件

7. 版本演进（如适用）
   - 时间线图
   - 各版本关键改进

8. 一页总结
   - 核心要点浓缩
   - 推荐阅读资源
```

### Phase 3：SVG 可视化图示设计

**核心原则：每个关键概念至少配一张图**

#### 必备图示类型（按优先级）

| 优先级 | 图示类型 | 适用场景 | 示例 |
|--------|---------|---------|------|
| P0 | 架构对比图 | 新旧方案对比 | 标准 Attention vs FlashAttention |
| P0 | 流程图/流水线 | 算法步骤展示 | 前向计算流程 |
| P1 | 原理示意图 | 数学/物理直觉 | Online Softmax 增量更新 |
| P1 | 层级/结构图 | 系统架构 | GPU 内存层级 |
| P2 | 趋势图/性能图 | 性能对比 | IO 复杂度随 N 变化 |
| P2 | 全景图 | 生态/变体总览 | Attention 变体支持矩阵 |
| P3 | 时间线图 | 版本演进 | v1 → v2 → v3 |

#### SVG 设计规范

```
画布尺寸：viewBox="0 0 800 [高度按内容]"
配色方案：
  - 主色：#6C5CE7（紫色系，用于标题/强调）
  - 辅色：#00B894（绿色系，用于正面/改进）
  - 对比色：#E17055（橙红系，用于问题/瓶颈）
  - 中性色：#636E72（灰色系，用于说明文字）
  - 背景：#F8F9FA（浅灰）或 #FFFFFF（白色）

字体：font-family="system-ui, -apple-system, sans-serif"
圆角：rx="8" ry="8"（所有矩形统一）
阴影：使用 <filter> 添加微阴影提升层次感
动画：适当使用 CSS animation 增加交互感（可选）
```

#### SVG 图示数量指引

| 报告规模 | 建议图示数量 | 说明 |
|---------|------------|------|
| 入门科普（2-3页）| 3-4 张 | 核心概念+对比+流程 |
| 原理详解（5-8页）| 5-7 张 | 覆盖所有关键章节 |
| 源码级深入（8+页）| 8-10 张 | 每个细节都有图示支撑 |

### Phase 4：双格式产出

#### Markdown 版本

- 清晰的目录结构（带锚点链接）
- 表格化对比信息
- 代码块包裹公式和伪代码
- 图示位置用 `【图示：描述】` 占位标注
- 文件命名：`{技术主题}技术报告.md`

#### HTML 版本（核心交付物）

- 将所有 SVG 图示内联嵌入对应章节位置
- 响应式布局（max-width: 920px 居中）
- 统一设计语言：
  ```css
  body { font-family: system-ui; line-height: 1.8; background: #f8f8f6; }
  .container { max-width: 920px; background: #fff; border-radius: 12px; padding: 3rem; }
  h2 { border-bottom: 2px solid #EEEDFE; }
  table { border-collapse: collapse; width: 100%; }
  th { background: #6C5CE7; color: white; }
  .highlight-box { background: #f0efff; border-left: 4px solid #6C5CE7; padding: 1rem; }
  ```
- 文件命名：`{技术主题}技术报告.html`

#### 元信息标注（必须）

在报告头部包含：

```markdown
**面向新人培训** | {日期}
**报告生成模型**：AI 智能编程助手
**目标**：{一句话描述报告目标}
```

### Phase 5：自动同步分发

#### 5.1 同步至 IMA 知识库

目标知识库：「龙虾-模型ScalingUp」(kb_id: `6peD1tTQj2UYi41MTaDgLpfVnbCegcA-sjzZLJ0zVPA=`)

流程：
1. 调用 `ima-skills` 的 preflight-check 验证连接
2. 调用 check_repeated_names 避免重复
3. 调用 create_media 获取上传凭证
4. 使用 curl PUT 上传文件到 COS
5. 调用 add_knowledge 完成入库

上传文件：Markdown 版本（便于知识库索引检索）

#### 5.2 同步至腾讯文档

使用 `mcp__tencent-docs__create_smartcanvas_by_mdx` 工具：
- content_format: "markdown"
- title: 报告标题
- mdx: Markdown 正文内容

注意：腾讯文档对 Markdown 的渲染有限，SVG 图示主要在 HTML 版呈现。

### Phase 6：质量检查清单

生成完毕后逐条检查：

- [ ] 章节结构完整，由浅入深
- [ ] 每个核心概念有对应 SVG 图示
- [ ] 所有表格格式正确，信息对齐
- [ ] 公式推导步骤完整且有直觉解释
- [ ] HTML 中 SVG 正确内联且渲染正常
- [ ] 元信息（日期、模型版本）已标注
- [ ] 已同步至 IMA 知识库
- [ ] 已同步至腾讯文档
- [ ] 无未完成的占位符

## 适配指南

### 不同技术主题的章节调整

| 技术类型 | 重点章节 | 可选省略 |
|---------|---------|---------|
| 算法/模型（FlashAttention, MoE）| 数学原理 + 性能分析 | — |
| 系统架构（vLLM, TensorRT）| 系统流程 + 性能对比 | 数学推导可简化 |
| 训练方法（RLHF, DPO）| 核心思想 + 对比分析 | 版本演进 |
| 工具/框架（DeepSpeed, Megatron）| 使用流程 + 配置项 | 数学推导 |

### 图示风格统一规范

所有 SVG 图示必须遵循统一设计语言，确保系列报告的视觉一致性：
- 标题字号：18-20px，加粗
- 正文字号：13-14px
- 矩形圆角统一 rx="8"
- 颜色不超过 5 种主色
- 留白充足，避免拥挤

## 前置依赖

### 必须安装的 Skill

- **ima-skills**（或 **腾讯ima**）— 用于上传到 IMA 知识库

### 可选但推荐的 Skill

- **腾讯文档** — 用于同步到腾讯文档

## 示例用法

```
用户: 帮我生成一份 MoE (Mixture of Experts) 的技术报告，面向新人培训

Agent 执行:
1. 确认主题和深度 → MoE，原理详解级
2. 设计 7 章结构 → 稀疏激活背景/门控机制/负载均衡/训练策略/性能分析/变体对比/应用案例
3. 设计 6 张 SVG → 密集vs稀疏对比图/门控路由示意/负载均衡策略/训练流程/扩展性曲线/MoE变体全景
4. 产出 Markdown + HTML
5. 同步至 IMA + 腾讯文档
6. 质量检查 → 交付
```
