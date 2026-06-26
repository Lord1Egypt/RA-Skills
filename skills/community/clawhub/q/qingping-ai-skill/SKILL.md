---
name: qingping-ai-skill
description: "青萍 AI 图片生成工具。通过 API 生成高质量图片并自动下载到本地。使用场景：(1) 用户需要生成 AI 图片，(2) 提到"青萍"、"qingping"、"生成图片"、"AI生图"等关键词，(3) 需要快速生成设计素材或创意图片。支持多种模型、尺寸和比例配置，默认生成 16:9 比例图片。"
version: "1.0.4"
homepage: "https://claw.lusyoe.com"
repository: "https://github.com/lusyoe/qingping-ai-skill.git"
authors: ["lusyoe"]
license: "MIT"

requirements:
  environment_variables:
    - QINGPING_API_KEY

credentials:
  QINGPING_API_KEY:
    description: "青萍 AI 平台的 API Key"
    required: true
    source: "environment_variable"
---

# 青萍 AI 图片生成

通过青萍 AI API 生成高质量图片并自动下载到本地 `qingping-ai` 目录。

## 认证方式

配置 `QINGPING_API_KEY` 环境变量：

```bash
# 临时配置（当前终端会话）
export QINGPING_API_KEY='your-api-key-here'

# 永久配置（添加到 shell 配置文件）
echo 'export QINGPING_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

**获取 API Key**：
1. 登录青萍AI平台：https://auth.lusyoe.com/profile
2. 在个人信息页面，滚动到最下面
3. 点击生成或查看 API Key

## 快速开始

使用脚本生成图片：

```bash
# 基础用法（使用默认模型 nano-banana）
python scripts/generate_image.py "一只可爱的金鱼"

# 指定模型
python scripts/generate_image.py "一只可爱的金鱼" nano-banana-2

# 完整参数
python scripts/generate_image.py "提示词" [模型] [数量] [比例] [尺寸]

# 示例
python scripts/generate_image.py "一只可爱的小狗" nano-banana-2 1 1:1 1K
python scripts/generate_image.py "夕阳下的海滩" nano-banana-pro 1 16:9 2K
```

## 工作流程

1. **认证检查**：检查 `QINGPING_API_KEY` 环境变量
2. **提交任务**：POST 请求创建生成任务，获取 `task_id`
3. **轮询状态**：每 5 秒查询一次任务状态，直到完成或失败
4. **下载图片**：任务完成后，自动下载生成的图片到 `qingping-ai/` 目录

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| prompt | 必填 | 图片描述提示词 |
| model | `nano-banana` | 模型名称（见下方模型列表） |
| count | `1` | 生成数量 |
| ratio | `16:9` | 图片比例（见下方比例列表） |
| size | `1K` | 图片尺寸（见下方尺寸列表） |
| category | `青萍 Claw` | 分类标签 |
| tags | `[""]` | 自定义标签 |

## 支持的模型

| 模型名称 | 说明 |
|---------|------|
| `nano-banana` | 默认模型，快速生成 |
| `nano-banana-2` | 增强版本，更高质量 |
| `nano-banana-pro` | 专业版本，最佳质量 |

## 支持的比例

| 比例 | 说明 |
|------|------|
| `1:1` | 正方形 |
| `16:9` | 默认，横屏，适合封面 |
| `9:16` | 竖屏，适合手机壁纸 |

## 支持的尺寸

| 尺寸 | 说明 |
|------|------|
| `1K` | 默认，1024px |
| `2K` | 2048px，更高质量 |
| `4K` | 4096px，最高质量 |

**使用示例**：

```bash
# 使用默认参数（nano-banana, 16:9, 1K）
python scripts/generate_image.py "一只可爱的金鱼"

# 指定模型
python scripts/generate_image.py "一只可爱的金鱼" nano-banana-2

# 指定模型和比例
python scripts/generate_image.py "夕阳下的海滩" nano-banana-pro 1 16:9

# 完整参数
python scripts/generate_image.py "手机壁纸" nano-banana 1 9:16 4K
```

## API 端点

- **创建任务**: `POST https://video.lusyoe.com/api/img/generations`
- **查询状态**: `GET https://video.lusyoe.com/api/img/generations/{task_id}/status`

## 输出示例

```
📤 提交生成任务...
   提示词: 一只可爱的金鱼
   模型: nano-banana
   尺寸: 1K, 比例: 16:9
✅ 任务已提交
   任务ID: e5e363b6-78ed-441f-88ed-73cfeca0971f

⏳ 开始轮询任务状态...
   [1] 状态: pending, 等待中...
   [2] 状态: processing, 等待中...
   [3] 状态: processing, 等待中...
   [4] 状态: processing, 等待中...

✅ 任务完成! (轮询 4 次)

📥 下载图片...
   URL: https://img-cdn.lusyoe.cn/images/...
   保存到: qingping-ai/zc0d3kgp3bfw.png
✅ 下载完成!

🎉 完成! 共下载 1 张图片到 /path/to/qingping-ai/
```

## 错误处理

- **未配置认证信息**: 提示 API Key 配置步骤
- **不支持的模型**: 显示支持的模型列表
- **不支持的比例**: 显示支持的比例列表
- **不支持的尺寸**: 显示支持的尺寸列表
- **API 请求失败**: 显示详细错误信息
- **任务失败**: 显示错误原因
- **下载失败**: 显示下载错误详情

## 更新日志

### v1.0.4

- 移除云端托管环境认证支持，统一使用 API Key 认证
- 修改默认图片比例为 16:9（适合封面）
- 优化认证错误提示信息
- 简化代码逻辑和参数

### v1.0.3

- 添加完整的 Registry 元数据声明（version, homepage, repository, authors, license）
- 添加 `requirements` 和 `credentials` 配置
- 明确 `QINGPING_API_KEY` 为必需凭证
