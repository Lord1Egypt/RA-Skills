---
name: volcengine-doubao-image-gen
description: 豆包图像与视频生成。使用火山引擎 API 生成图片或短视频，支持 Seedream 文生图/图生图/组图，以及 Seedance 文生视频。触发词：豆包图片、doubao、生成图片、火山引擎、字节跳动图片生成、豆包视频、Seedance、生成视频。
---

# 豆包图像与视频生成

使用火山引擎豆包 API 生成图片与短视频。

- **默认图片模型：** `doubao-seedream-5-0-260128`
- **默认视频模型：** `doubao-seedance-1-5-pro-251215`

## 环境要求

### 必需凭证
- `ARK_API_KEY`：火山引擎豆包 API Key（必填）

### 可选环境变量
- `DOUBAO_MODEL`：覆盖默认图片模型版本（可选）
- `DOUBAO_VIDEO_MODEL`：覆盖默认视频模型版本（可选）

## 快速开始

```bash
# 设置 API Key
export ARK_API_KEY="your-api-key"

# 文生图
python3 scripts/generate_image.py --prompt "一只可爱的猫咪" --filename "cat.png"
```

## 图片脚本参数说明

| 参数 | 说明 | 默认值 |
|-----|------|--------|
| `--prompt` / `-p` | 图片描述（必填） | - |
| `--filename` / `-f` | 输出文件名 | 自动生成 |
| `--size` / `-s` | 图片尺寸 (1K/2K/4K) | 2K |
| `--no-watermark` | 不添加水印 | 默认有水印 |
| `--model` / `-m` | 图片模型名称 | doubao-seedream-5-0-260128 |
| `--image` / `-i` | 参考图 URL（可多次，图生图） | 无 |
| `--sequential` | 是否生成组图 (`disabled`/`auto`) | disabled |
| `--max-images` | 组图最大数量 | 无限制 |
| `--stream` | 流式输出 | false |

> 安全提示：不要通过命令行传递 API Key，请使用环境变量 `ARK_API_KEY`。

## 使用示例

### 文生图（默认走 Seedream 5.0）

```bash
python3 scripts/generate_image.py \
  --prompt "星空下的城市夜景，赛博朋克风格" \
  --filename "city.png"
```

### 指定 Seedream 5.0

```bash
python3 scripts/generate_image.py \
  --prompt "未来感产品海报，极简高级，金属质感" \
  --model doubao-seedream-5-0-260128 \
  --filename "seedream5.png"
```

### 图生图

```bash
python3 scripts/generate_image.py \
  --prompt "参考这个 LOGO，做一套户外运动品牌视觉设计，品牌名称为 GREEN" \
  --image "https://example.com/logo.png" \
  --sequential auto \
  --max-images 5 \
  --filename "brand_"
```

### 多图参考

```bash
python3 scripts/generate_image.py \
  --prompt "将图 1 的服装换为图 2 的服装" \
  --image "https://example.com/look1.png" \
  --image "https://example.com/look2.png" \
  --filename "outfit_swap.png"
```

## 视频生成

使用 `scripts/generate_video.py` 调用 Seedance 视频生成接口。

### 视频脚本参数说明

| 参数 | 说明 | 默认值 |
|-----|------|--------|
| `--prompt` / `-p` | 视频描述（必填） | - |
| `--filename` / `-f` | 输出视频文件名 | 自动生成 |
| `--model` / `-m` | 视频模型名称 | doubao-seedance-1-5-pro-251215 |
| `--duration` | 视频时长（秒） | 5 |
| `--resolution` | 分辨率 | 720p |
| `--ratio` | 画幅比例 | 16:9 |
| `--camera-fixed` | 固定机位 | false |
| `--no-audio` | 不生成音频 | false |
| `--watermark` | 添加水印 | false |
| `--poll-interval` | 轮询间隔秒数 | 5 |
| `--timeout` | 最大等待秒数 | 300 |

### 生成一个简单视频

```bash
python3 scripts/generate_video.py \
  --prompt "一只红色小龙虾在白色桌面上缓慢挥动钳子，极简插画风格，镜头稳定" \
  --duration 5 \
  --resolution 720p \
  --ratio 16:9 \
  --filename "seedance-demo.mp4"
```

## API Key 获取

1. 访问火山引擎控制台：https://console.volcengine.com/ark
2. 创建或选择一个接入点
3. 获取 API Key

## 提示词技巧

建议按以下结构编写：

1. 主体描述（是什么）
2. 场景/环境（在哪里）
3. 风格（赛博朋克、水彩、油画等）
4. 光影效果
5. 氛围/情绪

## 注意事项

1. 图片尺寸越大，生成时间越长
2. 默认添加水印，使用 `--no-watermark` 可去除
3. 组图使用 `--sequential auto` 和 `--max-images`
4. 图生图可通过多次 `--image` 传入多张参考图
5. 输出文件名现在会自动做安全清洗，避免提示词里的 `/` 等字符造成异常路径
6. 图片下载链接会做基础校验：要求 `https` 且响应内容必须是图片
7. 视频下载链接也会做基础校验：要求 `https` 且响应内容必须是视频
8. `Seedance` 不走图片接口，需使用 `generate_video.py`

## 故障排查

**错误：No API key provided**
- 设置环境变量：`export ARK_API_KEY="your-key"`

**错误：API Error 401**
- API Key 无效或过期

**错误：API Error 429**
- 请求频率超限，稍后重试

**错误：Network Error**
- 检查网络连接或代理设置

## 模型版本

| 模型 | 说明 | 状态 |
|------|------|------|
| `doubao-seedream-5-0-260128` | Seedream 5.0，文生图/图生图，适合默认图片调用 | 当前默认图片模型 |
| `doubao-seedream-4-5-251128` | Seedream 4.5，文生图/图生图，兼容旧工作流 | 兼容保留 |
| `doubao-seedance-1-5-pro-251215` | Seedance 1.5 Pro，文生视频，走 content generation tasks 接口 | 当前默认视频模型 |
