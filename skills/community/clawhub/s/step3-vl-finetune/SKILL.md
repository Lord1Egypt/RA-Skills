---
name: step3-vl-finetune
description: Step3-VL-10B 多模态模型微调指南。用于在 GPU 服务器上进行 Step3-VL 模型的 LoRA/全量微调。包含配置、训练、推理完整流程。
metadata:
  clawdbot:
    emoji: "🎯"
    requires:
      anyBins: ["python3"]
      env: ["CUDA_VISIBLE_DEVICES"]
    os: ["linux"]
---

# Step3-VL-10B 微调指南

Step3-VL-10B 是一个多模态视觉语言模型，支持图像理解和文本生成。本指南涵盖模型架构、微调配置、训练流程和推理方法。

## 模型架构

| 组件 | 配置 |
|------|------|
| **LLM** | Qwen3 (4096 hidden, 36 layers, GQA) |
| **Vision** | 自定义 ViT (728 size, 1536 width, 47 layers) |
| **Projector** | Linear (vision_width×4 → hidden_size) |
| **参数量** | ~10B |

## 项目位置

- **服务器**: `wphu@gpu506.aibee.cn`
- **容器**: `step3vl-finetune`
- **项目目录**: `/app/` (容器内)
- **模型路径**: `/data/algorithm/tracking/Checkpoints/Step3-VL-10B`
- **硬件**: 8× RTX 4090D 48GB

## 核心技术问题与解决方案

### 1. 模型兼容性问题 ⚠️

**问题**: Step3-VL 使用自定义模型架构，`forward()` 方法期望 `patch_pixel_values`，但 HuggingFace processor 只输出 `pixel_values`。

**解决方案**: 使用 monkey patch 重写 forward 函数，跳过多模态特征，仅使用语言模型部分训练。

```python
def patched_forward(
    self,
    input_ids: torch.Tensor,
    attention_mask: torch.Tensor,
    position_ids: torch.Tensor = None,
    **kwargs
):
    # 跳过 vision encoder，直接使用语言模型
    inputs_embeds = self.model.language_model.get_input_embeddings()(input_ids)
    outputs = self.model.language_model(
        inputs_embeds=inputs_embeds,
        attention_mask=attention_mask,
        position_ids=position_ids,
        return_dict=True,
        use_cache=False
    )
    logits = self.model.language_model.lm_head(outputs.last_hidden_state)
    return CausalLMOutputWithPast(logits=logits, loss=None)
```

### 2. PEFT 保存错误 ⚠️

**问题**: PEFT 库检查 `vocab_size`，但 StepRoboticsConfig 没有这个属性。

**解决方案**: 重写 `_save()` 方法，直接保存 adapter 权重到 bin 文件。

```python
def save_adapter(model, output_dir):
    """绕过 PEFT 的 vocab_size 检查，直接保存 adapter 权重"""
    adapter_weights = {}
    for name, param in model.named_parameters():
        if param.requires_grad:
            adapter_weights[name] = param.data.cpu()
    
    os.makedirs(output_dir, exist_ok=True)
    torch.save(adapter_weights, os.path.join(output_dir, "adapter_model.bin"))
    
    config = {
        "r": 16,
        "lora_alpha": 32,
        "target_modules": ["q_proj", "v_proj", "k_proj", "o_proj"]
    }
    with open(os.path.join(output_dir, "adapter_config.json"), "w") as f:
        json.dump(config, f)
```

### 3. Loss 设备不一致 ⚠️

**问题**: 计算出的 loss 在 CPU，模型在 GPU。

**解决方案**: 显式将 loss 移到 GPU。

```python
loss = loss_fn(logits.view(-1, vocab_size), labels.view(-1))
loss = loss.to("cuda:0")  # 显式移到 GPU
```

## 标准项目结构

```
/app/
├── dataset.py           # 数据集加载
├── model_utils.py       # 模型加载 + LoRA
├── inference.py         # 推理脚本
├── processor_simple.py  # 简化版 processor
└── output/final/        # 输出目录
    ├── adapter_model.bin
    └── adapter_config.json
```

## GPU 环境配置（RTX 40 系列）

**必须设置以下环境变量：**

```bash
export NCCL_P2P_DISABLE=1
export NCCL_IB_DISABLE=1
export CUDA_VISIBLE_DEVICES=2  # 单卡训练
```

> RTX 40 系列显卡的 NCCL 通信有兼容问题，禁用 P2P 和 IB 后才能正常训练。

## 数据格式

### 训练数据 (train.jsonl)

```json
{
  "id": "sample_001",
  "image": "images/example.jpg",
  "conversations": [
    {"role": "user", "content": "描述这张图片的内容"},
    {"role": "assistant", "content": "这张图片展示了一个..."}
  ]
}
```

## 训练结果示例

| 指标 | 值 |
|------|-----|
| 模型参数 | 10.17B |
| LoRA 可训练参数 | 174.59M (1.69%) |
| 训练时间 | 13.58秒 (3 samples, 3 epochs) |
| Loss | 32.20 |
| Adapter 大小 | 698MB (504 个参数) |

## 推理

```bash
# 基本推理
python inference.py --model_path /path/to/model --image test.jpg --prompt "描述图片"

# 使用 LoRA 微调后的模型
python inference.py --model_path /path/to/base_model --lora_path output/final --image test.jpg --prompt "描述图片"
```

## 加载微调后的模型

```python
from model_utils import load_model_and_processor

model, processor = load_model_and_processor(
    model_path="/data/algorithm/tracking/Checkpoints/Step3-VL-10B",
    lora_path="/app/output/final",
    device="cuda"
)

# 推理
inputs = processor(images=image, text=prompt, return_tensors="pt")
outputs = model.generate(**inputs.to(device))
result = processor.decode(outputs[0], skip_special_tokens=True)
```

## 常见问题

### 1. NCCL 通信错误

```
RuntimeError: NCCL error in: /path/to/nccl.cpp
```

**解决**: 设置 `NCCL_P2P_DISABLE=1` 和 `NCCL_IB_DISABLE=1`

### 2. vocab_size 属性缺失

```
AttributeError: 'StepRoboticsConfig' object has no attribute 'vocab_size'
```

**解决**: 使用自定义的 `save_adapter()` 函数，绕过 PEFT 检查

### 3. forward 参数不匹配

```
TypeError: forward() got an unexpected keyword argument 'pixel_values'
```

**解决**: 使用 monkey patch 重写 forward 方法

### 4. 显存不足

**解决方案**:
- 减小 `per_device_train_batch_size`
- 增加 `gradient_accumulation_steps`
- 使用 DeepSpeed ZeRO-2/3
- 启用梯度检查点

### 5. 多模态数据加载慢

**优化方案**:
- 预处理图像到固定尺寸
- 使用 WebDataset 格式
- 增加数据加载线程数

## 下一步工作

1. **验证推理**: 加载 adapter 测试生成效果
2. **真实数据**: 替换测试数据为实际业务数据
3. **多模态训练**: 实现完整的 vision + language 联合训练（需要解决 processor 兼容性）
4. **参数调优**: 调整 learning rate、epochs 等超参数

## 相关资源

- vLLM 推理服务: `http://172.18.10.103:8600/v1`
- Docker 镜像: `harbor.aibee.cn/auto_car/preference-align:v1.1`
- 系统设计文档: `memory/reports/2026-03-25-rlhf-system-design.md`