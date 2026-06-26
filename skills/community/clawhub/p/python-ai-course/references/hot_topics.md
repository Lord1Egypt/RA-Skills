# AI 热门技术全景（2025-2026）

> 本文档供 AI 全栈教学导师在「专题 A：热门技术」阶段加载使用。
> 每个技术点按「是什么 → 为什么火 → 怎么学 → 能做什么」四段式展开。

---

## 一、协议层：Agent 标准化通信

### 1.1 MCP（Model Context Protocol）

**是什么**：Anthropic 2024 年底推出的开放协议，定义 AI 模型与外部工具/数据源之间的标准化交互方式。类比为「AI 的 USB-C 接口」— 一套协议让所有模型和所有工具互相连接。

**为什么火**：
- 解决了 Agent 开发的碎片化问题（之前每个平台有自己的一套工具调用方式）
- WorkBuddy、Cursor、Claude Desktop 等产品已原生支持
- 社区生态爆发：已有 1000+ MCP Server（数据库、API、文件系统等）

**怎么学**：
1. 理解 MCP 架构三要素：Client（AI 应用）→ Server（工具提供方）→ Transport（通信层）
2. 手写一个简单的 MCP Server（Python `mcp` SDK）
3. 学习 MCP Server 的 Tools、Resources、Prompts 三大原语
4. 将已有 API 封装为 MCP Server

**能做什么**：
- 让 AI 助手直接操作本地文件、数据库、第三方 API
- 构建可复用的工具生态，一次开发到处使用
- WorkBuddy 中通过 MCP 连接器接入企业内部系统

---

### 1.2 A2A（Agent-to-Agent 协议）

**是什么**：Google 2025 年推出的 Agent 间通信协议，让不同厂商的 Agent 可以互相发现、协商、协作完成任务。

**为什么火**：
- 多 Agent 系统是 2025 年最大趋势之一
- 解决了「不同框架开发的 Agent 如何通信」这一核心痛点
- Google + 50+ 合作伙伴背书（Salesforce、SAP、Cohere 等）

**怎么学**：
1. 理解 A2A 三大核心：Agent Card（能力声明）、Task（任务定义）、Artifact（产出物）
2. 用官方 Python SDK 搭建两个 Agent 的 A2A 通信
3. 对比 A2A vs MCP：MCP 解决「Agent-工具」通信，A2A 解决「Agent-Agent」通信

**能做什么**：构建异构多 Agent 系统，让 Claude Agent 调用 Gemini Agent 的能力，或让企业内部 Agent 与外部 SaaS Agent 协作。

---

## 二、多模态 AI

### 2.1 视觉语言模型（VLM）

**是什么**：能同时理解图像和文本的大模型。代表：GPT-4V/4o、Gemini 2.0 Flash、Qwen2.5-VL、Claude 3.5（视觉版）。

**为什么火**：
- 多模态是 AGI 的必经之路（人类感知世界不只靠文字）
- 成本快速下降：Qwen2.5-VL-7B 可在消费级 GPU 运行
- 应用场景极大扩展：UI 自动化、文档理解、视频分析

**怎么学**：
1. 了解 VLM 核心架构：视觉编码器（ViT/SigLIP）→ 投影层 → LLM
2. 用 HuggingFace `transformers` 加载 Qwen2.5-VL 跑本地推理
3. 学习多模态 Prompt 技巧（图片标注、区域定位）
4. 实战：用 VLM 做发票 OCR + 结构化提取

**能做什么**：智能客服（理解用户截图）、自动化测试（看懂 UI）、文档数字化、视频内容审核。

---

### 2.2 文生视频（Text-to-Video）

**是什么**：从文本描述直接生成视频的 AI 模型。代表：OpenAI Sora、快手 Kling（可灵）、Runway Gen-3、Google Veo 2。

**为什么火**：
- 2024 年 Sora 发布引发行业地震，2025 年进入可用阶段
- 国产 Kling（可灵）全球领先，支持最长 2 分钟高清生成
- 短视频/广告/教育行业需求巨大

**怎么学**：
1. 了解扩散模型（Diffusion Model）+ 时空注意力机制基本原理
2. 使用开源方案：CogVideoX（智谱开源）、Stable Video Diffusion
3. 学习 Prompt 工程：镜头描述、动作时序、风格控制
4. 后处理：视频编辑、音效合成、字幕生成

**能做什么**：教学视频生成、产品 demo 制作、社交媒体内容创作。

---

## 三、推理能力突破

### 3.1 推理模型（Reasoning Models）

**是什么**：专门针对复杂推理优化的大模型。代表：OpenAI o1/o3、DeepSeek-R1、Qwen-QwQ、Claude 3.5 Sonnet（Extended Thinking）。

**为什么火**：
- o1 在数学竞赛（AIME）和编程竞赛（Codeforces）达到人类顶尖水平
- DeepSeek-R1 开源，证明「纯强化学习」路线可行
- 推理时计算（Test-time Compute）成为新范式

**怎么学**：
1. 理解推理模型的「慢思考」机制：生成内部推理链 → 反思 → 输出
2. 学习推理模型的 Prompt 技巧（与普通模型不同：更简洁，不需要 CoT）
3. 用 DeepSeek-R1 开源权重跑本地推理
4. 对比：推理模型 vs 普通模型 在数学/编程/逻辑任务上的差异

**能做什么**：数学证明、代码审查、复杂逻辑推理、科研辅助、策略规划。

---

## 四、AI 安全与对齐

### 4.1 前沿对齐技术

**是什么**：确保 AI 系统的行为符合人类价值和意图的技术体系。

**为什么火**：
- 模型能力越强，安全问题越迫切
- 各国监管加速（EU AI Act、中国生成式 AI 管理办法）
- 企业落地 AI 的首要障碍是「不可控」

**关键方向**：
- **RLHF/DPO**：让模型学习人类偏好（DPO 比 RLHF 更稳定、更便宜）
- **Constitutional AI**：用一套原则（宪法）约束模型行为，减少人工标注
- **红队测试（Red Teaming）**：系统性地攻击模型找漏洞
- **Guardrails**：部署层的安全护栏（NeMo Guardrails、Guardrails AI）

**怎么学**：
1. 理解对齐的核心问题：奖励黑客（Reward Hacking）、目标错位（Goal Misgeneralization）
2. 用 TRL 库实践 DPO 训练（比 RLHF 入门门槛低）
3. 搭建 Guardrails 安全层（输入检查 + 输出过滤）
4. 了解 AI 安全评估基准：MMLU-Pro、HumanEval、SafetyBench

**能做什么**：确保企业 AI 应用安全可控，防止越狱攻击和有害输出。

---

## 五、推理加速

### 5.1 FlashAttention-3 & 推理优化

**是什么**：新一代注意力计算算法，大幅提升 Transformer 的推理和训练速度。

**为什么火**：
- FlashAttention-3 在 H100 上实现 1.5-2× 加速，利用率达 75%
- 推理成本是 AI 应用落地的最大瓶颈之一
- Speculative Decoding、KV Cache 量化等配套技术成熟

**关键方向**：

| 技术 | 原理 | 加速效果 |
|------|------|----------|
| FlashAttention-3 | IO-aware 注意力计算，充分利用 GPU 异步性 | 1.5-2× |
| Speculative Decoding | 小模型「起草」→ 大模型「校验」 | 2-3× |
| KV Cache 量化 | 将 Key-Value 缓存压缩为 INT4/INT8 | 内存减半 |
| vLLM v2 | PagedAttention + 连续批处理 | 吞吐量 10-20× |

**怎么学**：
1. 理解 Transformer 推理的性能瓶颈（显存带宽 vs 计算）
2. 用 vLLM 部署开源模型，对比原生 HuggingFace 的吞吐差异
3. 了解量化技术栈：GPTQ → AWQ → GGUF 的演进路线

**能做什么**：降低 AI 服务部署成本（50-70%），支持更高并发。

---

## 六、AI 工程化

### 6.1 可观测性与 LLMOps

**是什么**：监控、调试、优化 LLM 应用的全生命周期管理。

**为什么火**：
- LLM 应用从 demo 到生产的最大障碍是「不可观测」（黑盒输入输出）
- 提示词版本混乱、Token 消耗不可控、质量无法评估
- LangSmith、LangFuse、Weights & Biases 等工具趋于成熟

**怎么学**：
1. 接入 LangFuse 做 Prompt 版本管理和 A/B 测试
2. 搭建 LLM 应用的成本监控（Token 用量、延迟、错误率）
3. 学习 RAGAS 评估框架（Faithfulness、Answer Relevancy、Context Recall）
4. 构建评估数据集（Golden Dataset）自动化回归测试

**能做什么**：将 LLM 应用的可靠性从「玄学」提升到「工程可控」。

---

## 七、新兴方向

### 7.1 世界模型（World Model）

**是什么**：学习物理世界运行规律的 AI 模型，能预测环境的状态变化。代表：Sora（视频世界模型）、UniSim、Genie 2。

**为什么值得关注**：被认为是通向 AGI 的关键路径之一。Yann LeCun 力推的 JEPA 架构就是世界模型思路。

### 7.2 具身智能（Embodied AI）

**是什么**：让 AI 拥有物理身体，能在真实世界中感知和行动。代表：Figure 01/02、Tesla Optimus、智元机器人。

**为什么值得关注**：2025 年 Figure 02 已进入宝马工厂测试，具身智能是 AI 落地的终极形态之一。

### 7.3 AI for Science

**是什么**：用 AI 加速科学研究。代表：AlphaFold 3（蛋白质+DNA+小分子全预测）、GNoME（材料发现）、NeuralGCM（气象预测）。

**为什么值得关注**：2024 年诺贝尔化学奖颁给 AlphaFold 团队。AI 正在成为科学发现的「新显微镜」。

---

## 教学使用指南

当讲解热门技术时，遵循以下原则：
1. **先锚定学员水平**：L1/L2 讲概念和应用场景，L3/L4 深入原理和实现
2. **控制范围**：一次专题聚焦 2-3 个热点，不要铺开全部
3. **必讲主题**：MCP 协议（与 WorkBuddy 生态直接相关）、推理模型、AI 工程化
4. **可选主题**：多模态、安全对齐、具身智能（根据学员兴趣选讲）
5. **每个主题至少配 1 个 `show_widget` 图示**：架构图、演进时间线、技术栈对比等
