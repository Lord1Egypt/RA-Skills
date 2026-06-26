# Models - 模型架构详解

## CrashChat 模型架构

基于 VideoLLaMA-3 7B，采用 LoRA 微调策略。

### 架构组成
1. **视觉编码器**: SigLIP (预训练)
2. **视觉-语言投影层**: 可学习的位置线性投影
3. **语言模型**: Llama-3 7B backbone
4. **LoRA 适配器**: 低秩适应层

### 训练策略

#### 1. Independent Monotask（独立单任务）
- 每个任务单独训练一个模型
- 优点: 任务特异性强
- 缺点: 计算资源消耗大
- 适用: 特定任务优化场景

#### 2. Homogeneous Multitask（同质多任务）
- Linguistic-centric 任务联合训练
- Perception-centric 任务联合训练
- 优点: 相似任务互相增强
- 权重: `linguistic_centric_homogeneous_multitask` / `perception_centric_homogeneous_multitask`

#### 3. Heterogeneous Multitask（异质多任务）
- 所有 6 任务联合训练
- 推荐版本: `heterogeneous_multitask`
- 优点: 综合能力强，单一模型完成所有任务

### 模型选择指南

| 场景 | 推荐模型 |
|------|---------|
| 通用分析 | heterogeneous_multitask |
| 精确定位 | perception_centric_homogeneous_multitask |
| 深度推理 | linguistic_centric_homogeneous_multitask |
| 单任务优化 | corresponding independent_monotask |

---

## Traffix VideoQA - TraffiX-Qwen

基于 Qwen 视觉语言模型，专为时空视频理解设计。

### 核心创新
- **Tuple-based 时空表达**: `(时间, 空间, 对象)` 三元组
- **视觉 Token 采样策略**: 优化长视频处理效率
- **多粒度定位**: 支持帧级和区域级定位

### 与 CrashChat 的互补性
- CrashChat: 侧重事故分析与推理
- Traffix: 侧重时空定位与对象理解
- 联合使用可实现更完整的视频分析

---

## 其他相关模型

### 视频理解基线
- VideoLLaMA-2
- VideoChat
- InternVideo
- PandaGPT

### 目标检测基线
- YOLO 系列 (v8/v9/v10)
- Faster R-CNN
- DETR / DINO

### 时空理解专用
- VidT-GDRN
- ST-VQA
- Spatio-Temporal Action Detection