# 图片生成指南

## 支持的模型

### 文生图模型
- **nano-banana** - 标准图片生成模型（推荐）
- **nano-banana-hd** - 4K 高清版本
- **gemini-2.5-flash-image-preview** - Gemini 官方模型

### 图生图模型
- **nano-banana-edit** - 图片编辑模型

## 图片比例选项

- `4:3` - 横屏比例（推荐）
- `3:4` - 竖屏比例
- `16:9` - 宽屏比例
- `9:16` - 手机屏比例
- `2:3` - 竖屏比例
- `3:2` - 横屏比例

## 使用流程

### 文生图

1. **选择模型** - 根据需求选择合适的模型
2. **输入提示词** - 详细描述您想要的图片内容
3. **选择比例** - 根据用途选择合适的长宽比
4. **生成图片** - 等待 AI 处理完成

### 图生图

1. **上传参考图片** - 选择一张参考图片
2. **输入提示词** - 描述您想要的修改或效果
3. **生成图片** - 等待 AI 处理完成

## 提示词技巧

### 描述主体
- 人物、动物、物体等主要元素

### 添加风格
- 写实、卡通、油画、水彩、科幻等

### 指定场景
- 室内、户外、特定地点、背景环境

### 描述光线
- 明亮、昏暗、夕阳、月光、自然光等

### 添加情感
- 快乐、神秘、温馨、科幻、浪漫等

## 示例

### 文生图示例

```bash
python3 {baseDir}/scripts/wangyi-banana.py \
  --task text-to-image \
  --prompt "一只可爱的橘猫坐在窗台上，阳光透过窗户洒在它身上，写实风格，4K高清" \
  --model nano-banana \
  --aspect-ratio 4:3 \
  -o /tmp/openclaw/wangyi-output/cat.png
```

### 图生图示例

```bash
python3 {baseDir}/scripts/wangyi-banana.py \
  --task image-to-image \
  --prompt "将背景改为夜晚，添加星空" \
  --image /path/to/image.png \
  --model nano-banana-edit \
  -o /tmp/openclaw/wangyi-output/edited.png
```

## 注意事项

- 图片生成通常需要 10-30 秒
- 高清模型生成时间可能更长
- 提示词越详细，生成效果越好
- 支持多种图片格式输出（PNG, JPG 等）
