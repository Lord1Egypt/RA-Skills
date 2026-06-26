# Query Planner — 完整用例

本文档提供 3 个端到端示例，展示从输入到输出的完整过程。

---

## 用例 1：战略分析场景

**任务**：评估中国半导体产业政策的效果与挑战

### 输入

```json
{
  "primary_task": "评估中国半导体产业政策的效果与挑战，重点关注自给率提升和国际竞争力",
  "primary_subject": "中国半导体产业",
  "canonical_time_frame": "2020-2025",
  "goal_mode": "evaluate",
  "target_variable": "芯片自给率"
}
```

### 输出

```json
{
  "task_id": "QP-a3f7c2e1",
  "primary_subject": "中国半导体产业",
  "time_frame": "2020-2025",
  "goal_mode": "evaluate",
  "target_variable": "芯片自给率",
  "identity_queries": [
    "中国半导体产业 规模 分类 核心企业 产业链分布",
    "中国芯片 自给率 计算口径 定义 国际标准",
    "中国半导体大基金一期二期三期 投资规模 重点方向",
    "中国半导体 28nm及以上成熟制程 能力水平"
  ],
  "event_queries": [
    "中国芯片自给率 2020-2025 变化趋势 实际数据",
    "中国半导体 2020-2025 重大突破 里程碑事件",
    "美国对华芯片出口管制 2020-2025 政策演进 时间线",
    "中国半导体进口额 2020-2025 年度统计",
    "中国芯片设计 制造 封测 产值分布 2024",
    "华为麒麟芯片 2020-2024 迭代历程 性能对比",
    "中国半导体设备材料 国产化率 2020-2025 数据"
  ],
  "action_queries": [
    "中国半导体产业 国家政策 税收优惠 补贴措施 2020-2025",
    "芯片自给率 提升措施 行动计划 具体路径",
    "CHIPS Act 对中国半导体 影响 对冲措施",
    "日本韩国对华半导体限制 2023-2024 应对策略",
    "中国半导体企业 海外布局 投资建厂 东南亚中东",
    "成熟制程扩产 中芯国际 华虹 积塔 计划产能"
  ],
  "counter_queries": [
    "中国芯片自给率 数据口径 争议 质疑 统计方法",
    "半导体产业补贴 效果高估 国际反面案例 日本韩国经验教训",
    "中国半导体 人才缺口 核心技术瓶颈 短板分析",
    "成熟制程产能过剩 风险 价格战 毛利率下降"
  ]
}
```

### 解读

- **identity** (4条)：定义产业全貌、自给率口径、资金工具、技术水平基准线
- **event** (7条)：时间线覆盖5年，变量"自给率"渗透进第1条和第7条
- **action** (6条)：覆盖国内政策、对冲策略、海外布局、产能规划
- **counter** (4条)：覆盖数据质疑、政策效果质疑、技术瓶颈、产能过剩风险
- **时间绑定**：event 7条中有6条含年份 ✅，action 6条中有4条含年份 ✅
- **变量渗透**：event含2条、action含1条关于"自给率" ✅

---

## 用例 2：新闻/政策研究场景

**任务**：分析 TikTok 在美国被强制出售或禁用的政策影响

### 输入

```json
{
  "primary_task": "分析美国对TikTok强制出售或禁令的政策背景、影响范围及各方反应",
  "primary_subject": "TikTok美国禁令",
  "canonical_time_frame": "2024-2025",
  "goal_mode": "investigate",
  "target_variable": null
}
```

### 输出

```json
{
  "task_id": "QP-b8d4f1a9",
  "primary_subject": "TikTok美国禁令",
  "time_frame": "2024-2025",
  "goal_mode": "investigate",
  "target_variable": null,
  "identity_queries": [
    "TikTok 美国用户规模 日活月活 市场份额 2024",
    "TikTok 母公司字节跳动 股权结构 数据安全架构",
    "Protecting Americans from Foreign Adversary Controlled Applications Act 法案内容 全文",
    "CFIUS 美国外国投资委员会 TikTok 国家安全审查 历史"
  ],
  "event_queries": [
    "TikTok美国禁令 2024-2025 立法时间线 关键节点",
    "TikTok 禁令 司法挑战 法院裁决 上诉进展 2024-2025",
    "TikTok 禁令 对美国创作者 经济影响 数据估算",
    "TikTok 禁令 对Meta Google YouTube 竞争影响 受益分析",
    "ByteDance TikTok出售谈判 潜在买家 估值 时间线",
    "其他国家 TikTok限制禁令 印度欧盟 2024-2025"
  ],
  "action_queries": [
    "TikTok 禁令 合规方案 数据本地化 Texas Project",
    "美国国会 TikTok听证会 关键议员 立场 投票记录 2024-2025",
    "TikTok 诉讼策略 第一修正案 法律团队",
    "Meta YouTube Reels Shorts 短视频替代市场策略",
    "TikTok 用户迁移 备选平台 小红书 Lemon8"
  ],
  "counter_queries": [
    "TikTok 国家安全威胁 实际证据 数据泄露案例 争议",
    "TikTok禁令 宪法第一修正案 违宪 质疑 法学观点",
    "TikTok禁令 对中小企业创作者 负面影响 实证数据",
    "美国本土社交平台 数据隐私问题 Meta Google 安全争议 对比"
  ]
}
```

### 解读

- **identity** (4条)：建立用户规模、公司结构、法案定义、历史审查基础
- **event** (6条)：覆盖立法进程、司法挑战、经济影响、竞争影响、出售谈判、国际对比
- **action** (5条)：覆盖合规方案、立法立场、诉讼策略、竞品动作、用户迁移
- **counter** (4条)：质疑安全证据、质疑违宪、关注负面影响、本土平台对比
- **无 target_variable**：变量渗透规则不适用 ✅
- **时间绑定**：event 6条全含年份 ✅，action 5条中3条含年份 ✅

---

## 用例 3：技术调研场景

**任务**：对比 Transformer 与 Mamba 两种模型架构的优劣

### 输入

```json
{
  "primary_task": "对比Transformer和Mamba两种LLM架构的原理、性能和适用场景",
  "primary_subject": "Transformer vs Mamba架构",
  "canonical_time_frame": null,
  "goal_mode": "compare",
  "target_variable": "推理速度"
}
```

### 输出

```json
{
  "task_id": "QP-c1e5a8f3",
  "primary_subject": "Transformer vs Mamba架构",
  "time_frame": null,
  "goal_mode": "compare",
  "target_variable": "推理速度",
  "identity_queries": [
    "Transformer架构 自注意力机制 原理 核心组件",
    "Mamba架构 SSM状态空间模型 选择性机制 原理",
    "Transformer vs Mamba 计算复杂度 时间复杂度 空间复杂度 对比",
    "Mamba论文 Selective State Spaces 原始论文 核心贡献"
  ],
  "event_queries": [
    "Mamba架构 最新进展 Mamba-2 Jamba 2024-2025",
    "Transformer vs Mamba 推理速度 benchmark 对比评测",
    "Mamba架构 实际部署 案例 生产环境 应用",
    "Transformer 长上下文处理 注意力瓶颈 FlashAttention优化",
    "Mamba 架构 在不同任务上的表现 NLU生成代码数学 benchmark",
    "Transformer替代架构 SSM RWKV Hyena 研究进展 2024-2025"
  ],
  "action_queries": [
    "Mamba架构 优化策略 训练技巧 实践经验",
    "企业选择 模型架构 决策因素 成本性能trade-off",
    "Mamba 推理速度优化 GPU部署 CUDA实现",
    "Mamba vs Transformer 长文本任务 选择建议 最佳实践"
  ],
  "counter_queries": [
    "Mamba架构 局限性 缺点 不适用场景",
    "Mamba性能评测 公平性质疑 cherry-picking 实验条件",
    "Transformer替代 极早期失败案例 注意力机制不可替代的证据",
    "Mamba架构 生态不成熟 缺乏预训练模型 第三方支持不足"
  ]
}
```

### 解读

- **identity** (4条)：双架构原理、复杂度对比、原始论文
- **event** (6条)：最新进展、速度 benchmark、部署案例、长上下文处理、多任务表现、替代架构
- **action** (4条)：优化策略、决策框架、部署方案、选择建议
- **counter** (4条)：Mamba 局限性、评测公平性质疑、替代失败案例、生态成熟度
- **变量渗透**：event含1条、action含1条关于"推理速度" ✅
- **无 time_frame**：时间绑定规则不适用 ✅

---

## 用例速查表

| 用例 | 场景 | identity | event | action | counter | 总计 |
|------|------|----------|-------|--------|---------|------|
| 1 | 战略分析(半导体) | 4 | 7 | 6 | 4 | 21 |
| 2 | 政策研究(TikTok) | 4 | 6 | 5 | 4 | 19 |
| 3 | 技术调研(架构对比) | 4 | 6 | 4 | 4 | 18 |
