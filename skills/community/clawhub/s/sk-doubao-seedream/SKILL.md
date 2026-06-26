# Doubao Seedream Skill

火山方舟 Seedream 文生图 Skill，支持 Doubao-Seedream 系列模型。

**API 文档**: https://www.volcengine.com/docs/82379/1541523

## 功能特性

- 📝 **文生图**: 根据文字描述生成图片
- 🖼️ **图生图**: 对已有图片进行编辑
- 🔄 **多版本支持**: Seedream 5.0 / 4.5 / 4.0 / 3.0

## 支持的模型

| 模型 ID | 名称 | 类型 |
|---------|------|------|
| `doubao-seedream-5-0-260128` | Doubao-Seedream-5.0 | 文生图 |
| `doubao-seedream-4-5-251128` | Doubao-Seedream-4.5 | 文生图 |
| `doubao-seedream-4-0-250828` | Doubao-Seedream-4.0 | 文生图 |
| `doubao-seededit-3-0-i2i-250628` | Doubao-SeedEdit-3.0-i2i | 图生图 |
| `doubao-seedream-3-0-t2i-250415` | Doubao-Seedream-3.0-t2i | 文生图 |

## 首次使用

### 1. 检查/设置 API Key

运行任何命令前，系统会检查 API Key。如果没有设置或需要更新：

```bash
# 方式1: 交互式设置
python {baseDir}/scripts/generate.py config

# 方式2: 直接编辑配置文件
# 文件位置: {baseDir}/config.json
{
    "api_key": "your-api-key",
    "default_model": "doubao-seedream-4-0-250828",
    "output_dir": "./generated-images"
}

# 方式3: 设置环境变量
set VOLCENGINE_API_KEY=your-api-key
```

### 2. 获取 API Key

1. 访问 [火山方舟控制台](https://console.volcengine.com/ark)
2. 登录后进入「API Key 管理」
3. 创建或复制你的 API Key

## 使用方法

### 1. 查看模型列表

```bash
python {baseDir}/scripts/generate.py list
```

### 2. 命令行模式

**文生图**:
```bash
python {baseDir}/scripts/generate.py generate -p "一只可爱的猫咪" -m "doubao-seedream-4-0-250828" -o "output.png"
```

**指定尺寸**:
```bash
python {baseDir}/scripts/generate.py generate -p "风景画" -s "1024x2048" -o "landscape.png"
```

**图生图**:
```bash
python {baseDir}/scripts/generate.py edit -p "把这只猫变成老虎" -i "cat.png" -o "tiger.png"
```

### 3. 交互模式

```bash
python {baseDir}/scripts/generate.py
```

会依次引导你：
1. 选择模型
2. 选择模式（文生图/图生图）
3. 输入提示词
4. 生成图片

## 参数说明

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--prompt` | `-p` | 图片描述/编辑指令 | - |
| `--model` | `-m` | 模型 ID | `doubao-seedream-4-0-250828` |
| `--output` | `-o` | 输出文件路径 | `seedream_output_{timestamp}.png` |
| `--input-image` | `-i` | 输入图片（图生图） | - |
| `--size` | `-s` | 图片尺寸 | `1024x1024` |

**支持的图片尺寸**: `512x512`, `768x768`, `1024x1024`, `1024x2048`, `2048x1024`

## 文件结构

```
sk-doubao-seedream/
├── SKILL.md           # 本文件
├── config.json        # 配置文件（API Key 等）
└── scripts/
    └── generate.py    # 主生成脚本
```

## API 端点

- **基础 URL**: `https://ark.cn-beijing.volces.com/api/v3`
- **文生图端点**: `POST /images/generations`
- **图生图端点**: `POST /chat/completions`

## 常见问题

### Q: 提示 "API Key 无效" 或 "模型不存在"
A: 确保：
1. API Key 是火山方舟 Ark 服务的（不是 Atlas Cloud）
2. API Key 有图片生成模型的访问权限
3. 在[火山方舟控制台](https://console.volcengine.com/ark)检查模型权限

### Q: 如何查看可用的模型？
A: 使用 `list` 命令查看所有支持的模型，或访问控制台的模型列表。

### Q: 图片生成需要多长时间？
A: 通常 5-30 秒，视服务器负载而定。
