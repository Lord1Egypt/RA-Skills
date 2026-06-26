# 机器人领域经典论文索引

## 目录

1. [模仿学习](#模仿学习)
2. [视觉-语言-动作模型 (VLA)](#视觉-语言-动作模型-vla)
3. [扩散策略](#扩散策略)
4. [世界模型与规划](#世界模型与规划)
5. [强化学习](#强化学习)
6. [操作与抓取](#操作与抓取)
7. [具身智能基础](#具身智能基础)

---

## 模仿学习

### ACT: Action Chunking with Transformers (Stanford, 2023)

**论文**：Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware

**核心贡献**：
- 提出 Action Chunking Transformer (ACT)，一次预测 30 步动作
- 引入条件解码机制，动态调整动作
- 在精细操作任务（拉拉链、扣扣子）上取得突破

**关键指标**：
- 双臂操作任务成功率：80%+
- 训练数据：约 1 小时演示

**论文链接**：https://arxiv.org/abs/2304.13705

**代码**：https://github.com/tonyzhaozh/act

---

### ALOHA: A Low-cost Open-source Hardware (Stanford, 2023)

**论文**：Learning Bimanual Manipulation with Low-Cost Hardware

**核心贡献**：
- 开源低成本双臂机器人平台（约 $20,000）
- 遥操作系统，支持高效数据采集
- 与 ACT 配合，实现精细操作

**影响力**：推动了社区低成本机器人研究

**论文链接**：https://arxiv.org/abs/2304.13705

**代码**：https://github.com/tonyzhaozh/aloha

---

### Diffusion Policy (UC Berkeley, 2023)

**论文**：Diffusion Policy: Visuomotor Policy Learning via Action Diffusion

**核心贡献**：
- 首次将扩散模型用于机器人动作生成
- 通过去噪过程生成多样化动作
- 在多个基准上达到 SOTA

**关键指标**：
- Push-T 任务：95.6%
- Cup Arrangement：97.5%
- UCLA Coffee：95.7%

**论文链接**：https://arxiv.org/abs/2303.04137

**代码**：https://github.com/real-stanford/diffusion_policy

---

## 视觉-语言-动作模型 (VLA)

### RT-1: Robotics Transformer (Google DeepMind, 2022)

**论文**：RT-1: Robotics Transformer for Real-World Control at Scale

**核心贡献**：
- 首个大规模机器人多任务 Transformer
- 在 700+ 任务上训练，展示多任务学习
- 提出机器人数据集构建方法

**关键指标**：
- 未见任务零样本成功率：32%
- 已见任务成功率：76%

**论文链接**：https://arxiv.org/abs/2212.06817

---

### RT-2: Vision-Language-Action Models (Google DeepMind, 2023)

**论文**：RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control

**核心贡献**：
- 将视觉-语言模型（VLM）知识迁移到机器人
- 支持语义理解（如"拿起看起来像草莓的东西"）
- 证明大规模预训练对机器人有益

**关键指标**：
- 语义指令成功率：62%
- 零样本泛化能力显著提升

**论文链接**：https://arxiv.org/abs/2307.15818

---

### RT-X: Cross-Embodiment Robot Learning (Google DeepMind, 2023)

**论文**：Open X-Embodiment: Robotic Learning Datasets and RT-X Models

**核心贡献**：
- 最大规模跨机构机器人数据集（百万级轨迹）
- 跨平台、跨机器人统一模型
- 证明数据规模效应

**数据规模**：
- 22 种机器人
- 527 种技能
- 160,266 个任务

**论文链接**：https://arxiv.org/abs/2310.08864

**数据集**：https://robotics-transformer-x.github.io/

---

### OpenVLA (Stanford, 2024)

**论文**：OpenVLA: An Open-Source Vision-Language-Action Model

**核心贡献**：
- 首个开源 VLA 模型
- 基于 Llama 2，7B 参数
- 在多个基准上媲美 RT-2

**关键特性**：
- 可本地部署
- 支持微调
- 开源权重

**论文链接**：https://arxiv.org/abs/2406.09246

**代码**：https://github.com/stanford-vila/openvla

---

### π0 (Physical Intelligence, 2024)

**论文**：π0: A Vision-Language-Action Flow Model

**核心贡献**：
- 引入 Flow Matching 替代 Diffusion
- 超大规模数据训练
- 刷新多项 SOTA

**关键创新**：
- 更快的推理速度
- 更稳定的动作生成
- 更好的泛化能力

**论文链接**：https://arxiv.org/abs/2410.24164

---

## 扩散策略

### 3D Diffusion Policy (Columbia, 2024)

**论文**：3D Diffusion Policy: Generalizable Visuomotor Policy Learning via Simple 3D Representations

**核心贡献**：
- 引入 3D 点云表示
- 提升跨场景泛化能力
- 减少对相机视角的敏感度

**论文链接**：https://arxiv.org/abs/2403.03954

---

### IDP3: Improved 3D Diffusion Policy (2024)

**论文**：IDP3: Improved 3D Diffusion Policy

**核心贡献**：
- 改进 3D 表示学习
- 更高效的数据利用
- 更好的泛化性能

**论文链接**：https://arxiv.org/abs/2410.02547

---

## 世界模型与规划

### Dreamer (DeepMind, 2020)

**论文**：Dream to Control: Learning Behaviors by Latent Imagination

**核心贡献**：
- 学习环境的世界模型
- 在潜在空间中规划
- 高效的样本利用率

**关键指标**：
- Atari 100k：人类水平
- DeepMind Control：SOTA

**论文链接**：https://arxiv.org/abs/1912.01603

**代码**：https://github.com/danijar/dreamer

---

### Dreamer V3 (DeepMind, 2023)

**论文**：Mastering Diverse Domains through World Models

**核心贡献**：
- 通用世界模型架构
- 无需超参数调整
- 在多个领域达到 SOTA

**关键突破**：
- Minecraft 钻石收集：首次从零学习
- Atari 200M：人类水平

**论文链接**：https://arxiv.org/abs/2301.04104

---

### DayDreamer (UC Berkeley, 2022)

**论文**：DayDreamer: World Models for Physical Robot Learning

**核心贡献**：
- 将世界模型应用于真实机器人
- 在线学习，无需仿真
- 高效的现实世界训练

**关键成果**：
- 4 个机器人任务，1 小时训练
- 样本效率提升 10x+

**论文链接**：https://arxiv.org/abs/2206.14176

---

## 强化学习

### Decision Transformer (UC Berkeley, 2021)

**论文**：Decision Transformer: Reinforcement Learning via Sequence Modeling

**核心贡献**：
- 将强化学习建模为序列预测
- 用 Transformer 替代传统 RL
- 无需价值函数

**影响力**：开启了"RL as Sequence Modeling"范式

**论文链接**：https://arxiv.org/abs/2106.01345

**代码**：https://github.com/kzl/decision-transformer

---

### Gato (DeepMind, 2022)

**论文**：A Generalist Agent

**核心贡献**：
- 单一模型处理 600+ 任务
- 统一的游戏、机器人、NLP 模型
- 证明通才智能体可行性

**模型规模**：1.2B 参数

**论文链接**：https://arxiv.org/abs/2205.06175

---

### Q-Transformer (DeepMind, 2023)

**论文**：Q-Transformer: Scalable Offline Reinforcement Learning via Autoregressive Q-Functions

**核心贡献**：
- 将 Q-learning 与 Transformer 结合
- 适用于离线强化学习
- 高效利用演示数据

**论文链接**：https://arxiv.org/abs/2309.10150

---

## 操作与抓取

### CLIPort (MIT, 2022)

**论文**：CLIPort: What and Where Pathways for Robotic Manipulation

**核心贡献**：
- 语言引导的 2D 规划
- 简化 3D 规划问题
- 高效的语义理解

**关键指标**：
- 语义任务成功率：88%
- 零样本泛化能力

**论文链接**：https://arxiv.org/abs/2109.12098

**代码**：https://github.com/cliport/cliport

---

### AnyGrasp (CUHK, 2023)

**论文**：AnyGrasp: Robust and Efficient Grasp Perception in Spatial and Temporal Domains

**核心贡献**：
- 通用抓取检测
- 处理遮挡和复杂场景
- 实时推理

**关键指标**：
- 抓取成功率：93.4%
- 推理速度：10 FPS

**论文链接**：https://arxiv.org/abs/2212.08333

---

### DexGraspNet (Stanford, 2023)

**论文**：DexGraspNet: A Large-Scale Benchmark for Generalizable Dexterous Grasping

**核心贡献**：
- 大规模灵巧手抓取数据集
- 5355 个物体，130 万抓取姿态
- 推动灵巧操作研究

**论文链接**：https://arxiv.org/abs/2304.03817

---

## 具身智能基础

### Embodied AI Survey (2024)

**论文**：Embodied Artificial Intelligence: A Survey

**核心贡献**：
- 系统梳理具身智能研究
- 涵盖感知、学习、控制
- 未来发展方向预测

**论文链接**：https://arxiv.org/abs/2404.09169

---

### Robot Learning Survey (2023)

**论文**：A Survey on Robot Learning

**核心贡献**：
- 全面覆盖机器人学习方法
- 模仿学习、强化学习、世界模型
- 数据集和基准介绍

**论文链接**：https://arxiv.org/abs/2304.08359

---

## 使用说明

1. **撰写推文时**：根据论文主题，查阅相应类别的经典论文作为背景知识
2. **技术溯源时**：识别论文所属技术流派，引用相关工作
3. **对比分析时**：参考经典论文的关键指标进行对比

## 更新计划

本索引将定期更新，收录最新的突破性工作。建议每季度回顾一次。
