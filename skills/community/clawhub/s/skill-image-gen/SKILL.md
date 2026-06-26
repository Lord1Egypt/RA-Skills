---
name: skill-image-gen
description: 免费AI图片生成工具，使用Gitee AI API生成图片，支持本地保存和腾讯云COS上传。适用于需要免费图片生成的场景。
---

# Free Image Gen - 免费AI图片生成工具

基于 Gitee AI API 的免费图片生成技能，支持多种模型，可将生成的图片保存到本地或上传到腾讯云 COS。

## 功能特点

- 🆓 **完全免费** - 使用 Gitee AI API，无需付费
- 🎨 **多模型支持** - 支持 Kolors 等多种图片生成模型
- ☁️ **云端存储** - 可选上传到腾讯云 COS
- 📁 **本地保存** - 支持保存到本地目录
- 🔧 **灵活配置** - 配置参数可抽取到配置文件

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置说明

### 方法一：首次使用交互式配置（推荐）

**首次运行脚本时**，如果检测到配置不存在，会自动进入交互式配置模式：

```bash
python scripts/main.py --prompt "一只可爱的小狗"
```

系统会提示：
```
============================================================
  Free Image Gen - 首次使用配置
============================================================

检测到这是首次使用，需要配置 Gitee AI API Key

获取 API Key 的方法：
1. 访问 https://ai.gitee.com/
2. 注册/登录账号
3. 进入控制台获取 API Key

------------------------------------------------------------

请输入你的 Gitee AI API Key: [用户输入API Key]
```

配置完成后，配置文件会自动保存到：`~/.openclaw/skills/skill-image-gen/config.json`

### 方法二：通过对话配置（AI Agent 使用）

如果你是 AI Agent，可以通过对话获取用户的参数，然后使用 `update_config()` 方法更新配置：

```python
from config import Config

# 创建配置对象（禁用交互式配置）
config = Config(interactive=False)

# 通过对话获取用户的 API Key
# user_api_key = ... (从对话中获取)

# 更新配置
config.update_config('gitee.api_key', user_api_key)

# 现在可以使用配置了
api_key = config.get('gitee.api_key')
```

### 方法三：环境变量

在 `.env` 文件中配置：

```env
# Gitee AI API 配置
GITEE_API_KEY=your_gitee_api_key

# 腾讯云 COS 配置（可选）
COS_SECRET_ID=your_secret_id
COS_SECRET_KEY=your_secret_key
COS_REGION=ap-guangzhou
COS_BUCKET=your-bucket-name

# 输出目录
IMAGE_OUTPUT_PATH=./output
```

### 方法四：手动创建配置文件

复制配置模板并修改：

```bash
cp config.example.json ~/.openclaw/skills/skill-image-gen/config.json
```

### 配置文件查找优先级

脚本会按以下优先级查找配置文件：

1. **环境变量**：`SKILL_IMAGE_GEN_CONFIG`（最高优先级）
2. **技能安装目录**：`~/.openclaw/skills/skill-image-gen/config.json`（优先）
3. **独立技能配置目录**：`~/.openclaw/skills/config/skill-image-gen/config.json`（备选，卸载技能不影响配置）
4. **当前工作目录**：
   - `./skills/skill-image-gen/config.json`
   - `./.skill-image-gen/config.json`
5. **旧版全局配置**：`~/.openclaw/skill/skill-image-gen/config.json`（向后兼容）
6. **技能目录**：`config.json`

找到第一个存在的配置文件就会加载，后续的路径会被忽略。

> **注意**：推荐将配置文件放在 `~/.openclaw/skills/config/` 目录下，独立于技能安装目录，卸载重装技能不会丢失配置。

### 配置文件示例

配置文件内容示例：

```json
{
  "gitee": {
    "api_key": "your_gitee_api_key",
    "model": "Kolors",
    "base_url": "https://ai.gitee.com/v1"
  },
  "cos": {
    "enabled": false,
    "secret_id": "",
    "secret_key": "",
    "region": "ap-guangzhou",
    "bucket": ""
  },
  "output": {
    "path": "./output",
    "format": "png"
  }
}
```

## 使用方法

### 基本用法

```bash
# 生成图片并保存到本地
python scripts/main.py --prompt "一只可爱的小猫在阳光下睡觉"

# 指定输出路径
python scripts/main.py --prompt "海边日落" --output ./images/sunset.png

# 生成多张图片
python scripts/main.py --prompt "山水画" --count 3

# 上传到 COS
python scripts/main.py --prompt "城市夜景" --upload-cos
```

### 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--prompt`, `-p` | 图片生成提示词（必需） | - |
| `--output`, `-o` | 输出文件路径 | 自动生成 |
| `--model`, `-m` | 使用的模型 | Kolors |
| `--count`, `-n` | 生成图片数量 | 1 |
| `--upload-cos` | 上传到腾讯云 COS | False |
| `--config`, `-c` | 配置文件路径 | None（自动查找） |
| `--size`, `-s` | 图片尺寸 | 1024x1024 |
| `--json` | JSON 格式输出 | False |

### 作为模块使用

```python
from scripts.gitee_api import GiteeImageGenerator

# 初始化
generator = GiteeImageGenerator(api_key="your_api_key")

# 生成图片
result = generator.generate("一只可爱的小狗")
print(result["image_url"])

# 生成并上传
result = generator.generate(
    prompt="山水画",
    upload_to_cos=True,
    output_dir="./images"
)
```

## 获取 API Key

1. 访问 [Gitee AI](https://ai.gitee.com/)
2. 注册/登录账号
3. 进入控制台获取 API Key

## 支持的模型

| 模型 | 说明 | 推荐场景 |
|------|------|----------|
| Kolors | 快文生图模型 | 通用图片生成 |
| flux-schnell | 快速生成 | 简单场景 |
| stable-diffusion | 经典模型 | 艺术风格 |

## 目录结构

```
skill-image-gen/
├── SKILL.md              # 本说明文件
├── config.example.json   # 配置示例文件
├── scripts/
│   ├── main.py           # 主入口脚本
│   ├── config.py         # 配置管理
│   ├── gitee_api.py      # Gitee API 封装
│   ├── cos_uploader.py   # COS 上传模块
│   └── utils.py          # 工具函数
└── requirements.txt      # Python 依赖
```

**用户配置文件位置**：`~/.openclaw/skills/skill-image-gen/config.json`（推荐）

## 常见问题

### Q: API Key 无效？
A: 请确认 API Key 是否正确，是否已激活。

### Q: 图片生成失败？
A: 检查网络连接，确认 Gitee AI 服务是否正常。

### Q: COS 上传失败？
A: 检查 COS 配置是否正确，Bucket 是否存在，权限是否正确。

## 注意事项

1. Gitee AI API 有调用频率限制，请合理使用
2. 生成的图片默认保存为 PNG 格式
3. COS 上传需要提前创建 Bucket 并配置权限

## 更新日志

- v1.0.0 - 初始版本，支持基本的图片生成功能
