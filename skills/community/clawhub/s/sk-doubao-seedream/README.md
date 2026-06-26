# Doubao Seedream Skill

🎨 火山方舟 Seedream 文生图 Skill for WorkBuddy/OpenClaw

## 功能特性

- 📝 **文生图**: 根据文字描述生成精美图片
- 🎨 **多版本支持**: Seedream 5.0 / 4.5 / 4.0 / 3.0
- ⚙️ **灵活配置**: 支持自定义尺寸、模型选择

## 支持的模型

| 模型 ID | 名称 | 尺寸要求 |
|---------|------|----------|
| `doubao-seedream-5-0-260128` | Seedream 5.0 | 1920x1928 |
| `doubao-seedream-4-5-251128` | Seedream 4.5 | 1920x1928 |
| `doubao-seedream-4-0-250828` | Seedream 4.0 | 1024x1024 等 |
| `doubao-seedream-3-0-t2i-250415` | Seedream 3.0 | 1024x1024 等 |

## 安装

```bash
# 使用 ClawHub 安装
npx clawhub@latest install sk-doubao-seedream

# 或手动安装到 ~/.workbuddy/skills/
```

## 使用方法

### 命令行模式

```bash
# 查看模型列表
python scripts/generate.py list

# 文生图
python scripts/generate.py generate -p "一只可爱的猫咪" -o output.png

# 指定模型
python scripts/generate.py generate -p "未来城市" -m "doubao-seedream-5-0-260128" -s "1920x1928" -o output.png
```

### 交互模式

```bash
python scripts/generate.py
```

## 配置

首次使用需要设置 API Key：

```bash
python scripts/generate.py config
```

或编辑 `config.json`：

```json
{
    "api_key": "your-volcengine-api-key",
    "default_model": "doubao-seedream-4-0-250828",
    "output_dir": "./generated-images"
}
```

## 获取 API Key

1. 访问 [火山方舟控制台](https://console.volcengine.com/ark)
2. 创建 API Key
3. 确保开通图片生成模型权限

## 技术信息

- **API**: 火山方舟 Ark Service
- **端点**: `https://ark.cn-beijing.volces.com/api/v3/images/generations`
- **兼容性**: WorkBuddy, OpenClaw

## License

MIT
