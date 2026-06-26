# ComfyUI Generator

## 概述

提供可靠的 ComfyUI 图像生成功能，内置错误预防机制。

## 核心约束

### 1. 提示词字段强制验证

- ✅ **必须使用 `inputs['text']`**
- ❌ **禁止使用 `inputs['prompt']`**
- ✅ **自动检查节点类型为 `CLIPTextEncode`**

### 2. 避免重复生成

- ✅ **不使用 `spawn` 执行生成任务**
- ✅ **同步执行，确保任务完成**
- ✅ **任务失败时重试机制**

### 3. 工作流验证

- ✅ **加载时检查文件存在性**
- ✅ **验证必需节点存在**
- ✅ **自动跳过负面提示词节点**

## 使用方法

### 基础生成

```python
from skills.comfyui_generator import generate

# 生成图片
result = generate(
    prompt="古代剑客，黑色短发，眼神坚毅，正面特写",
    workflow_path="/path/to/workflow.json",
    output_path="/home/node/projects/demo/characters/hero/front.png"
)

if result['success']:
    print(f"✓ 生成成功: {result['file_path']}")
else:
    print(f"✗ 生成失败: {result['error']}")
```

### 高级选项

```python
result = generate(
    prompt="古代剑客，正面特写",
    workflow_path="/path/to/workflow.json",
    output_path="/output.png",
    filename_prefix="sword_hero_front",
    node_id="45",  # 指定修改哪个节点
    negative_prompt_node_id="7",  # 跳过负面提示词节点
    timeout=300,  # 超时时间（秒）
    retry=2  # 重试次数
)
```

## 返回结果

```python
{
    'success': True/False,
    'file_path': '/path/to/output.png',
    'file_size_mb': 2.47,
    'prompt_id': 'uuid',
    'duration_seconds': 45,
    'error': None  # 失败时包含错误信息
}
```

## 工作流要求

工作流必须包含以下节点：

- **CLIPTextEncode**: 提示词编码节点（必须有）
- **SaveImage**: 保存图片节点（必须有一个）

## 错误处理

内置错误处理机制：

| 错误类型 | 处理方式 |
|----------|----------|
| 工作流文件不存在 | 立即失败，返回错误 |
| 找不到 CLIPTextEncode | 立即失败，返回错误 |
| 字段名错误 | 自动修正，使用 `text` |
| ComfyUI 连接失败 | 重试 3 次 |
| 生成超时 | 放弃并返回错误 |
| 下载失败 | 重试 2 次 |

## 常见错误预防

### 错误 1: 字段名错误

```python
# ❌ 错误方式（历史错误）
node['inputs']['prompt'] = new_prompt  # 字段不存在

# ✅ Skill 自动使用正确方式
node['inputs']['text'] = new_prompt  # 正确
```

### 错误 2: 重复生成

```python
# ❌ 错误方式（历史错误）
spawn("generate_image", ...)  # 可能重复执行

# ✅ Skill 不使用 spawn
result = generate_image(...)  # 同步执行
```

### 错误 3: 没有检查节点类型

```python
# ❌ 错误方式（历史错误）
for node_id, node in workflow.items():
    node['inputs']['text'] = new_prompt  # 可能修改错误节点

# ✅ Skill 自动检查
if node.get('class_type') == 'CLIPTextEncode':
    node['inputs']['text'] = new_prompt
```

## 测试

```bash
# 测试 ComfyUI 连接
python -c "from skills.comfyui_generator import test_connection; test_connection()"

# 测试生成一张图片
python << 'EOF'
from skills.comfyui_generator import generate

result = generate(
    prompt="古代剑客，黑色短发，眼神坚毅，正面特写",
    workflow_path="/mnt/share2win/comfyui_work/comfyui_workflows/image_z_image_turbo（可用 写实）.json",
    output_path="/tmp/test_output.png"
)

print(result)
EOF
```

## 配置

### 默认服务器地址

```python
COMFYUI_SERVER = "http://192.168.18.15:8188"
```

### 默认工作流路径

```python
DEFAULT_WORKFLOW = "/mnt/share2win/comfyui_work/comfyui_workflows/image_z_image_turbo（可用 写实）.json"
```

## 历史错误记录

以下错误已通过本 skill 预防：

1. **提示词字段错误** (2026-03-16 12:05)
   - 问题: 代码使用 `inputs['prompt']` 但实际字段是 `inputs['text']`
   - 影响: 提示词修改失败，生成默认图片
   - 预防: Skill 强制使用 `inputs['text']`

2. **重复生成问题** (2026-03-16 11:46)
   - 问题: 使用 spawn 子 agent 导致重复执行
   - 影响: 生成多个相同文件
   - 预防: Skill 不使用 spawn，同步执行

3. **负面提示词被修改**
   - 问题: 修改了所有 CLIPTextEncode 节点
   - 影响: 风格提示词被破坏
   - 预防: Skill 自动识别并跳过负面提示词节点
