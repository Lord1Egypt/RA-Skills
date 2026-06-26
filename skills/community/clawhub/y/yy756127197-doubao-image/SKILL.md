---
name: doubao-image
description: 使用字节跳动豆包 Doubao SeeDream 模型生成高质量图片。支持文生图、AI 绘图、插画创作等功能。
metadata: {"clawdbot": {"emoji": "🎨", "category": "AI 工具", "version": "2.0.0"}}
---

# 豆包文生图（Doubao SeeDream）Skill

基于字节跳动火山引擎 ARK API，调用豆包 SeeDream 5.0 模型进行 AI 文生图创作。

## 📋 目录

- [功能特性](#功能特性)
- [前置条件](#前置条件)
- [安装方式](#安装方式)
- [使用方法](#使用方法)
- [API 参数详解](#api-参数详解)
- [触发条件](#触发条件)
- [工作流](#工作流)
- [错误处理](#错误处理)
- [最佳实践](#最佳实践)
- [常见问题](#常见问题)
- [技术实现](#技术实现)
- [版本历史](#版本历史)

## ✨ 功能特性

- 🎨 **高质量图像生成** - 基于豆包 SeeDream 5.0 模型，支持 2K/1080P/720P 分辨率
- 🔧 **灵活参数配置** - 支持尺寸、水印、格式等多种参数自定义
- 📦 **双脚本实现** - 提供 Bash 和 Python 两种实现方式，适应不同环境
- 🛡️ **完善的错误处理** - 详细的错误提示和日志记录
- 💾 **自动保存管理** - 智能图片下载和本地保存
- 🚀 **快速响应** - 优化的 API 调用流程，减少等待时间

## 🔐 前置条件

### 环境变量配置

必须设置火山引擎 ARK API Key：

```bash
export ARK_API_KEY="your_ark_api_key"
```

**获取 API Key 步骤：**

1. 访问 [火山引擎控制台](https://console.volcengine.com/ark)
2. 登录/注册账号
3. 进入「应用管理」→「创建应用」
4. 选择「图像生成」服务
5. 复制生成的 API Key

### 系统依赖

**Bash 脚本依赖：**
- Bash 4.0+
- curl 7.0+
- Python 3.6+（用于 JSON 处理）

**Python 脚本依赖：**
- Python 3.8+
- requests 库（可选，已内置 fallback 方案）

### 环境检查脚本

```bash
#!/bin/bash
# 检查运行环境
check_environment() {
  local errors=0
  
  # 检查 ARK_API_KEY
  if [ -z "$ARK_API_KEY" ]; then
    echo "❌ 错误：缺少 ARK_API_KEY 环境变量"
    echo "   请执行：export ARK_API_KEY=your_key"
    errors=$((errors + 1))
  else
    echo "✅ ARK_API_KEY 已配置"
  fi
  
  # 检查 curl
  if ! command -v curl &> /dev/null; then
    echo "❌ 错误：缺少 curl 命令"
    errors=$((errors + 1))
  else
    echo "✅ curl 已安装 ($(curl --version | head -n1))"
  fi
  
  # 检查 Python
  if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：缺少 Python 3"
    errors=$((errors + 1))
  else
    echo "✅ Python 已安装 ($(python3 --version))"
  fi
  
  return $errors
}

check_environment
```

## 📦 安装方式

### 方式一：通过 Clawhub 安装（推荐）

```bash
# 在 WorkBuddy 中执行
skill install doubao-image
```

### 方式二：手动安装

```bash
# 1. 克隆或下载技能到本地
git clone https://github.com/your-username/doubao-image-skill.git ~/.workbuddy/skills/doubao-image

# 2. 设置执行权限
chmod +x ~/.workbuddy/skills/doubao-image/scripts/*.sh

# 3. 配置环境变量
echo 'export ARK_API_KEY="your_key"' >> ~/.bashrc
source ~/.bashrc
```

### 方式三：直接复制

将 `doubao-image` 文件夹复制到 `~/.workbuddy/skills/` 目录即可。

## 🚀 使用方法

### 基础用法

```bash
# 使用默认参数生成图片
./scripts/doubao-image-generate.sh "一只在月光下的白色小猫"

# 指定分辨率（2K/1080P/720P）
./scripts/doubao-image-generate.sh "赛博朋克风格的城市夜景" "1080P"

# 关闭水印
./scripts/doubao-image-generate.sh "山水画" "2K" "false"
```

### Python 脚本用法

```bash
# 基础用法
python3 scripts/doubao-image-generate.py \
  --prompt "一只在月光下的白色小猫"

# 完整参数
python3 scripts/doubao-image-generate.py \
  --prompt "赛博朋克风格的城市夜景" \
  --size "1080P" \
  --watermark false \
  --output-dir "./my-images" \
  --verbose
```

### 在 WorkBuddy 中使用

当用户说以下话语时自动触发：
- "生成一张...的图片"
- "帮我画一个..."
- "AI 绘图：..."
- "文生图..."

## 📊 API 参数详解

### 核心参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `prompt` | string | ✅ 是 | - | 图片描述文本，支持中英文 |
| `model` | string | ❌ 否 | `doubao-seedream-5-0-260128` | 固定使用 SeeDream 5.0 |
| `size` | string | ❌ 否 | `2K` | 输出分辨率 |
| `watermark` | boolean | ❌ 否 | `true` | 是否添加水印 |
| `response_format` | string | ❌ 否 | `url` | 返回格式（url/base64） |
| `stream` | boolean | ❌ 否 | `false` | 是否流式输出 |

### 尺寸参数说明

| 值 | 分辨率 | 适用场景 |
|----|--------|----------|
| `2K` | 2048×2048 | 高质量输出、印刷用途 |
| `1080P` | 1920×1080 | 社交媒体、网页展示 |
| `720P` | 1280×720 | 快速预览、移动端 |

### 高级参数（通过环境变量配置）

| 环境变量 | 说明 | 默认值 |
|----------|------|--------|
| `DOUBAO_API_TIMEOUT` | API 超时时间（秒） | `60` |
| `DOUBAO_RETRY_COUNT` | 失败重试次数 | `3` |
| `DOUBAO_OUTPUT_DIR` | 默认输出目录 | `generated-images` |

## 🎯 触发条件

### 主要触发词

```
生成图片、生成图像、创建图片
AI 绘图、文生图、画一张
帮我画、画一个、生成一张...的图
doubao image、豆包生图
```

### 触发示例

```
用户：帮我画一只可爱的猫咪
用户：生成一张赛博朋克风格的城市夜景图
用户：AI 绘图：夕阳下的海滩
用户：文生图 - 中国风山水画
```

## 🔄 工作流

### 1. 需求解析

```
用户输入 → 提取 prompt → 解析参数 → 验证完整性
```

**解析逻辑：**
- 提取引号内或冒号后的描述文本作为 prompt
- 识别尺寸关键词（2K/1080P/720P）
- 检测水印相关表述（"不要水印"/"去水印"）

### 2. 参数验证

```bash
验证流程：
├─ 检查 ARK_API_KEY 是否存在
├─ 检查 prompt 是否非空
├─ 验证 size 参数合法性
├─ 检查网络连接状态
└─ 准备 API 调用
```

### 3. API 调用

```bash
curl -X POST "https://ark.cn-beijing.volces.com/api/v3/images/generations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ARK_API_KEY" \
  -d '{
    "model": "doubao-seedream-5-0-260128",
    "prompt": "用户描述",
    "size": "2K",
    "watermark": true,
    "response_format": "url",
    "stream": false,
    "sequential_image_generation": "disabled"
  }'
```

### 4. 响应处理

**成功响应：**
```json
{
  "data": [{
    "url": "https://example.com/image.png",
    "content": "base64_encoded_string"
  }],
  "usage": {
    "prompt_tokens": 50,
    "total_tokens": 50
  }
}
```

**处理流程：**
1. 解析 JSON 响应
2. 提取图片 URL
3. 下载图片到本地
4. 生成唯一文件名（带时间戳）
5. 通过 `open_result_view` 展示

### 5. 图片保存

```bash
# 保存路径规则
generated-images/
├── doubao-20260409-233045-abc123.png
├── doubao-20260409-233122-def456.png
└── ...
```

**文件名格式：** `doubao-YYYYMMDD-HHMMSS-random.png`

## ⚠️ 错误处理

### 错误码对照表

| 错误类型 | HTTP 状态码 | 处理方式 |
|----------|-------------|----------|
| 未授权 | 401 | 提示检查 API Key |
| 余额不足 | 402 | 提示充值 |
| 请求超限 | 429 | 自动重试（指数退避） |
| 服务器错误 | 500/503 | 重试 3 次后报错 |
| 超时 | 504 | 延长超时时间重试 |
| 内容违规 | 400 | 提示修改 prompt |

### 错误处理脚本

```bash
handle_error() {
  local status_code=$1
  local error_msg=$2
  
  case $status_code in
    401)
      echo "❌ 认证失败：API Key 无效或已过期"
      echo "   请重新获取：https://console.volcengine.com/ark"
      ;;
    402)
      echo "❌ 账户余额不足，请充值后重试"
      ;;
    429)
      echo "⚠️  请求频率超限，等待 ${retry_after}秒后重试..."
      sleep $retry_after
      ;;
    500|503)
      echo "⚠️  服务器繁忙，正在重试（第 $retry_count 次）..."
      ;;
    400)
      echo "❌ 请求被拒绝：${error_msg}"
      echo "   可能包含敏感词汇，请修改描述后重试"
      ;;
    *)
      echo "❌ 未知错误：${error_msg}"
      ;;
  esac
}
```

## 🎨 最佳实践

### Prompt 编写技巧

**优质 Prompt 公式：**
```
主体描述 + 环境氛围 + 艺术风格 + 技术参数
```

**示例：**
```
✅ 好的 Prompt：
"一只白色波斯猫，坐在古老的图书馆窗台上，
午后阳光透过彩色玻璃，写实风格，4K 超精细细节，
景深效果，温暖色调"

❌ 差的 Prompt：
"一只猫"
```

### 风格关键词库

```
【艺术风格】
写实、油画、水彩、素描、动漫、赛博朋克、蒸汽朋克、
极简、抽象、印象派、超现实主义

【画面质量】
4K、8K、超高清、电影大片、精致细节、杰作

【光影效果】
光线追踪、全局光照、体积光、丁达尔效应、黄金时刻

【构图方式】
对称构图、三分法、引导线、框架构图、鸟瞰视角
```

### 性能优化

1. **批量生成**：避免并发请求，串行处理更稳定
2. **缓存策略**：相同 prompt 可复用历史结果
3. **超时设置**：建议设置 60 秒超时
4. **重试机制**：指数退避重试（1s, 2s, 4s, 8s）

## ❓ 常见问题

### Q1: 生成的图片质量不佳？

**解决方案：**
- 使用更详细的 prompt 描述
- 添加质量关键词（4K、超精细、杰作）
- 选择 2K 分辨率
- 指定具体艺术风格

### Q2: API 调用失败？

**排查步骤：**
1. 检查 `ARK_API_KEY` 是否正确
2. 验证网络连接
3. 查看账户余额
4. 检查是否触发频率限制

### Q3: 图片下载失败？

**解决方案：**
```bash
# 手动下载
curl -L "图片 URL" -o "output.png"

# 检查输出目录权限
chmod 755 generated-images/
```

### Q4: 如何批量生成？

**脚本示例：**
```bash
#!/bin/bash
prompts=(
  "春日樱花"
  "夏日海滩"
  "秋日枫叶"
  "冬日雪景"
)

for prompt in "${prompts[@]}"; do
  ./scripts/doubao-image-generate.sh "$prompt"
  sleep 2  # 避免频率限制
done
```

## 🛠️ 技术实现

### 目录结构

```
doubao-image/
├── SKILL.md                 # Skill 定义文件
├── README.md                # 详细文档
├── CHANGELOG.md             # 版本历史
├── LICENSE                  # 开源协议
├── scripts/
│   ├── doubao-image-generate.sh    # Bash 实现
│   ├── doubao-image-generate.py    # Python 实现
│   └── check-env.sh                # 环境检查
├── examples/
│   └── prompts.md                  # Prompt 示例
└── tests/
    └── test-api.sh                 # API 测试
```

### 核心代码流程

```
┌─────────────┐
│  用户输入   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  解析参数   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  验证环境   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  构建请求   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  调用 API   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  处理响应   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  下载图片   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  展示结果   │
└─────────────┘
```

### 安全考虑

1. **API Key 保护**：仅从环境变量读取，不硬编码
2. **输入验证**：严格过滤 prompt 内容
3. **错误隔离**：异常不会泄露敏感信息
4. **权限控制**：脚本执行权限限制

## 📝 版本历史

### v2.0.0 (2026-04-09) - Clawhub 发布版
- ✨ 重构代码结构，符合 Clawhub 标准
- ✨ 新增 Python 实现版本
- ✨ 完善错误处理和日志记录
- ✨ 添加详细使用文档
- 🐛 修复 JSON 转义问题
- 🐛 优化超时重试机制

### v1.0.0 (2026-01-15) - 初始版本
- ✨ 基础 Bash 脚本实现
- ✨ 支持基本文生图功能
- ✨ 简单的错误处理

## 📄 许可证

MIT License - 详见 LICENSE 文件

## 🔗 相关链接

- [火山引擎 ARK 文档](https://www.volcengine.com/docs/82379)
- [豆包 SeeDream 介绍](https://www.volcengine.com/product/doubao)
- [Clawhub 技能开发指南](https://clawhub.cn/docs)
- [GitHub 仓库](https://github.com/your-username/doubao-image-skill)

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

```bash
# Fork 项目
# 创建功能分支
git checkout -b feature/your-feature

# 提交更改
git commit -m "feat: add your feature"

# 推送到分支
git push origin feature/your-feature

# 创建 Pull Request
```

## 📧 联系方式

- 作者：YangYang
- Email: your-email@example.com
- 问题反馈：GitHub Issues

---

**最后更新：** 2026-04-09  
**当前版本：** 2.0.0  
**维护状态：** 活跃维护中
