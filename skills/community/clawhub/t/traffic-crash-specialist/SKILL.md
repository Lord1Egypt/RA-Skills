---
name: traffic-crash-specialist
description: 交通事故视频分析与检测专用技能。使用当需要：(1) 分析交通事故视频，(2) 事故识别、因果推理、预防分析，(3) 交通场景时空理解与对象定位，(4) 查询交通事故检测相关模型/数据集/论文，(5) 使用 CrashChat 或 Traffix VideoQA 进行视频问答，(6) 训练或评估交通视频分析模型。触发词：traffic crash、accident detection、crash analysis、交通事故、video QA。
---

# Traffic Crash Analysis

交通事故视频理解领域的模型、数据集与工具整合。

## 核心项目

### 1. CrashChat

**论文**: [CrashChat: A Multimodal Large Language Model for Multitask Traffic Crash Video Analysis](https://arxiv.org/abs/2512.18878) (2025)

**GitHub**: https://github.com/Liangkd/CrashChat

**HuggingFace**: 
- 模型: https://huggingface.co/KDliang/crashchat
- 数据集: https://huggingface.co/datasets/KDliang/CrashChat

**核心特性**:
- 基于 VideoLLaMA-3 7B 的多模态大语言模型
- 支持 **6 大任务**:
  1. Crash recognition（事故识别）
  2. Crash description（事故描述）
  3. Causal reasoning（因果推理）
  4. Prevention reasoning（预防推理）
  5. Pre-crash localization（事故前定位）
  6. Crash localization（事故定位）
- 数据规模: 18,385 视频，96,184 video-QA 对
- 训练策略: 独立单任务 / 同质多任务 / 异质多任务

**任务分类**:
- **Linguistic-centric**: crash recognition, crash description, causal reasoning, prevention reasoning
- **Perception-centric**: pre-crash localization, crash localization

### 2. Traffix VideoQA (TUMTraf)

**论文**: A Benchmark for Unified Spatio-Temporal Video Understanding in Traffic Scenes

**主页**: https://traffix-videoqa.github.io/

**核心特性**:
- 交通场景时空视频理解基准
- 数据规模: 1,000 视频，85,000 多选 QA 对
- 支持 **3 大任务**:
  1. Multiple-choice video QA
  2. Referred object captioning（2,300 标注）
  3. Spatio-temporal object grounding（5,700 标注）
- 特色: tuple-based 时空对象表达，恶劣天气场景
- 基线模型: TraffiX-Qwen（视觉 token 采样策略）

---

## 模型对比

| 特性 | CrashChat | Traffix VideoQA |
|------|-----------|-----------------|
| 骨干模型 | VideoLLaMA-3 7B | TraffiX-Qwen |
| 数据规模 | 18,385 视频 | 1,000 视频 |
| 任务数 | 6 | 3 |
| 特色 | 多任务学习、因果推理 | 时空定位、恶劣天气 |
| 开源程度 | 权重+数据+代码 | 数据集+基准 |

---

## 使用场景

### CrashChat 适用场景
- 事故原因分析（为什么会发生碰撞？）
- 预防措施建议（如何避免类似事故？）
- 事故时间定位（碰撞发生在第几秒？）
- 事故描述生成（详细描述事故过程）

### Traffix VideoQA 适用场景
- 交通监控视频问答
- 特定对象定位（找到红色轿车）
- 时空关系理解（两车何时相遇？）
- 恶劣条件下的场景理解

---

## 快速开始

### CrashChat 安装

```bash
# 克隆仓库
git clone https://github.com/Liangkd/CrashChat.git
cd CrashChat

# 创建环境
conda create -n crashchat python=3.10 -y
conda activate crashchat

# 安装依赖
pip install torch==2.4.0 torchvision==0.19.0 --extra-index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
pip install flash_attn-2.7.3+cu11torch2.4cxx11abiFALSE-cp310-cp310-linux_x86_64.whl --no-deps
conda install -c conda-forge ffmpeg -y
```

### 模型权重下载

从 HuggingFace 下载预训练权重:
```bash
# 基线模型
huggingface-cli download KDliang/crashchat --local-dir ./ckpt

# 或按任务下载
# ckpt/videollama3_baseline
# ckpt/heterogeneous_multitask (推荐：全任务版本)
```

---

## 训练与评估

### 训练命令

```bash
# 单 GPU
CUDA_VISIBLE_DEVICES=0 bash scripts/train/Independent_monotask_models_causal_reasoning.sh 1

# 多 GPU
CUDA_VISIBLE_DEVICES=1,2 bash scripts/train/Independent_monotask_models_causal_reasoning.sh 2
```

### 评估流程

```bash
# 1. 转换权重
python tool/merge_and_convert_videollama3_lora.py

# 2. 运行评估
CUDA_VISIBLE_DEVICES=0 bash scripts/eval/eval_video_causal_reasoning.sh

# 3. 计算指标
python scripts/eval/compute_causal_reasoning_metrics.py
```

---

## 资源导航

### 数据集
- CrashChat Dataset: https://huggingface.co/datasets/KDliang/CrashChat
- TUMTraf VideoQA: https://traffix-videoqa.github.io/

### 论文
- CrashChat: https://arxiv.org/abs/2512.18878
- Traffix VideoQA: 见项目主页

### 模型权重
- CrashChat-7B: https://huggingface.co/KDliang/crashchat/tree/main/ckpt
- VideoLLaMA-3 原版: https://huggingface.co/KDliang/crashchat/tree/main/videollama3_original_model

---

## References

详细文档见 `references/` 目录:
- `models.md` - 模型架构与训练策略详解
- `datasets.md` - 数据集格式与标注说明
- `tasks.md` - 六大任务定义与评估方法