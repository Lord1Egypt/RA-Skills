---
name: wan-t2i
description: |
  阿里云DashScope Wan2.6文生图工具。使用阿里云百炼平台的Wan2.6-t2i模型生成图片。
  当用户需要：AI生成图片、文生图、从文字生成图像时触发。
  需要DASHSCOPE_API_KEY环境变量（已在系统中配置）。
---

# Wan2.6 文生图

使用阿里云DashScope的Wan2.6-t2i模型进行文生图。

## 环境要求

- DASHSCOPE_API_KEY：已配置在系统中
- curl：系统自带

## 使用方式

### 脚本调用

```bash
# 基本用法
bash ~/.openclaw/workspace/skills/wan-t2i/scripts/t2i.sh "你的提示词"

# 指定反向提示词
bash ~/.openclaw/workspace/skills/wan-t2i/scripts/t2i.sh "提示词" "不想出现的内容"

# 指定图片尺寸（支持：1280*1280, 720*1280, 1280*720）
bash ~/.openclaw/workspace/skills/wan-t2i/scripts/t2i.sh "提示词" "" "1280*720"
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| 第1个 | 正向提示词（中文效果更好） | 必填 |
| 第2个 | 反向提示词（不想出现的元素） | 空 |
| 第3个 | 尺寸（宽*高） | 1280*1280 |

## API详情

- **模型**：wan2.6-t2i
- **Endpoint**：https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
- **特点**：支持prompt_extend自动优化提示词

## 示例

```bash
# 生成一张风景图
bash ~/.openclaw/workspace/skills/wan-t2i/scripts/t2i.sh "日落时的海滩，海浪轻拍沙滩"

# 生成人物图
bash ~/.openclaw/workspace/skills/wan-t2i/scripts/t2i.sh "一位穿着汉服的少女" "" "720*1280"
```

## 注意事项

1. API响应是JSON格式，包含base64编码的图片或图片URL
2. 实际使用中可能需要解析JSON获取图片
3. 建议使用中文提示词，效果更好