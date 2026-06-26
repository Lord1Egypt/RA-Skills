# 豆包文生图（Doubao SeeDream）Skill

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/your-username/doubao-image-skill)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Bash](https://img.shields.io/badge/bash-4.0+-blue.svg)](https://www.gnu.org/software/bash/)

基于字节跳动火山引擎 ARK API 的 AI 文生图工具，通过豆包 SeeDream 5.0 模型生成高质量图片。

## 📖 目录

- [功能特性](#-功能特性)
- [快速开始](#-快速开始)
- [安装指南](#-安装指南)
- [使用方法](#-使用方法)
- [API 参考](#-api-参考)
- [配置选项](#-配置选项)
- [最佳实践](#-最佳实践)
- [故障排除](#-故障排除)
- [开发指南](#-开发指南)
- [贡献指南](#-贡献指南)
- [常见问题](#-常见问题)
- [更新日志](#-更新日志)

## ✨ 功能特性

### 核心功能

- 🎨 **AI 图像生成** - 基于豆包 SeeDream 5.0 模型，支持多种艺术风格
- 📐 **多分辨率支持** - 2K/1080P/720P 三种尺寸可选
- 💧 **水印控制** - 灵活选择是否添加平台水印
- 🔄 **自动重试** - 智能错误处理和指数退避重试机制
- 📦 **双实现方案** - Bash 和 Python 两种脚本，适应不同环境
- 🛡️ **完善的错误处理** - 详细的错误提示和日志记录
- 💾 **智能文件管理** - 自动生成唯一文件名，避免冲突

### 技术特性

- ✅ 支持环境变量配置
- ✅ 详细的运行日志
- ✅ 优雅的错误处理
- ✅ 跨平台兼容（macOS/Linux）
- ✅ 无需额外依赖（Python 脚本支持 fallback 到标准库）

## 🚀 快速开始

### 1. 获取 API Key

访问 [火山引擎控制台](https://console.volcengine.com/ark) 创建应用并获取 ARK API Key。

### 2. 设置环境变量

```bash
export ARK_API_KEY="your_ark_api_key_here"
```

### 3. 生成第一张图片

**使用 Bash 脚本：**
```bash
./scripts/doubao-image-generate.sh "一只在月光下的白色小猫"
```

**使用 Python 脚本：**
```bash
python3 scripts/doubao-image-generate.py --prompt "一只在月光下的白色小猫"
```

### 4. 查看生成的图片

图片将保存在 `generated-images/` 目录下，使用图片查看器打开即可。

## 📦 安装指南

### 方式一：通过 Clawhub 安装（推荐）

```bash
# 在 WorkBuddy 中执行
skill install doubao-image
```

### 方式二：Git 克隆

```bash
# 克隆仓库
git clone https://github.com/your-username/doubao-image-skill.git \
  ~/.workbuddy/skills/doubao-image

# 设置执行权限
chmod +x ~/.workbuddy/skills/doubao-image/scripts/*.sh \
  ~/.workbuddy/skills/doubao-image/scripts/*.py

# 验证安装
~/.workbuddy/skills/doubao-image/scripts/doubao-image-generate.sh --help
```

### 方式三：手动复制

1. 下载或复制整个 `doubao-image` 文件夹
2. 移动到 `~/.workbuddy/skills/` 目录
3. 设置脚本执行权限

```bash
chmod +x scripts/*.sh scripts/*.py
```

### 环境检查

运行环境检查脚本：

```bash
# Bash 版本
bash scripts/check-env.sh

# 或手动检查
echo $ARK_API_KEY  # 应显示你的 API Key
curl --version     # 应显示 curl 版本信息
python3 --version  # 应显示 Python 3.x.x
```

## 📖 使用方法

### 命令行用法

#### Bash 脚本

```bash
# 基础用法
./scripts/doubao-image-generate.sh "图片描述"

# 指定分辨率
./scripts/doubao-image-generate.sh "图片描述" "1080P"

# 关闭水印
./scripts/doubao-image-generate.sh "图片描述" "2K" "false"

# 指定输出目录
./scripts/doubao-image-generate.sh "图片描述" "2K" "true" "./my-images"

# 查看帮助
./scripts/doubao-image-generate.sh --help

# 查看版本
./scripts/doubao-image-generate.sh --version
```

#### Python 脚本

```bash
# 基础用法
python3 scripts/doubao-image-generate.py --prompt "图片描述"

# 指定分辨率
python3 scripts/doubao-image-generate.py \
  --prompt "图片描述" \
  --size "1080P"

# 关闭水印
python3 scripts/doubao-image-generate.py \
  --prompt "图片描述" \
  --no-watermark

# 指定输出目录
python3 scripts/doubao-image-generate.py \
  --prompt "图片描述" \
  --output-dir "./my-images"

# 启用详细日志
python3 scripts/doubao-image-generate.py \
  --prompt "图片描述" \
  --verbose

# 自定义超时和重试
python3 scripts/doubao-image-generate.py \
  --prompt "图片描述" \
  --timeout 120 \
  --retry 5

# 查看帮助
python3 scripts/doubao-image-generate.py --help
```

### 在 WorkBuddy 中使用

当用户输入包含以下关键词时，会自动触发文生图功能：

- "生成图片"
- "生成图像"
- "创建图片"
- "AI 绘图"
- "文生图"
- "画一张"
- "帮我画"

**示例对话：**
```
用户：帮我画一只可爱的猫咪，赛博朋克风格
助手：正在为您生成图片...
助手：图片生成完成！已保存到 generated-images/doubao-20260409-233045-abc123.png
```

### 编程调用

```python
from scripts.doubao_image_generate import DoubaoImageGenerator

# 创建生成器实例
generator = DoubaoImageGenerator(
    api_key="your_api_key",  # 或从环境变量读取
    timeout=60,
    retry_count=3,
    output_dir="generated-images",
    verbose=True
)

# 生成图片
output_path = generator.generate(
    prompt="一只在月光下的白色小猫",
    size="2K",
    watermark=True
)

print(f"图片已保存到：{output_path}")
```

## 📊 API 参考

### API 端点

```
POST https://ark.cn-beijing.volces.com/api/v3/images/generations
```

### 请求头

```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer YOUR_ARK_API_KEY",
  "User-Agent": "doubao-image-skill/2.0.0"
}
```

### 请求体

```json
{
  "model": "doubao-seedream-5-0-260128",
  "prompt": "一只在月光下的白色小猫，写实风格，4K 超精细细节",
  "sequential_image_generation": "disabled",
  "response_format": "url",
  "size": "2K",
  "stream": false,
  "watermark": true
}
```

### 响应示例

**成功响应：**
```json
{
  "data": [
    {
      "url": "https://example.com/images/abc123.png",
      "content": "base64_encoded_string"
    }
  ],
  "usage": {
    "prompt_tokens": 50,
    "total_tokens": 50
  }
}
```

**错误响应：**
```json
{
  "error": {
    "code": "invalid_api_key",
    "message": "API Key 无效或已过期",
    "type": "authentication_error"
  }
}
```

### 错误码

| HTTP 状态码 | 错误类型 | 说明 | 解决方案 |
|-------------|---------|------|----------|
| 200 | - | 请求成功 | - |
| 400 | Bad Request | 请求参数错误 | 检查 prompt 是否包含敏感词 |
| 401 | Unauthorized | API Key 无效 | 重新获取 API Key |
| 402 | Payment Required | 账户余额不足 | 充值账户 |
| 429 | Too Many Requests | 请求频率超限 | 等待后重试 |
| 500 | Internal Server Error | 服务器内部错误 | 稍后重试 |
| 503 | Service Unavailable | 服务不可用 | 稍后重试 |
| 504 | Gateway Timeout | 网关超时 | 增加超时时间 |

## ⚙️ 配置选项

### 环境变量

| 变量名 | 说明 | 默认值 | 示例 |
|--------|------|--------|------|
| `ARK_API_KEY` | 火山引擎 ARK API Key（必需） | - | `your_api_key` |
| `DOUBAO_API_TIMEOUT` | API 超时时间（秒） | `60` | `120` |
| `DOUBAO_RETRY_COUNT` | 失败重试次数 | `3` | `5` |
| `DOUBAO_OUTPUT_DIR` | 默认输出目录 | `generated-images` | `./my-images` |
| `DOUBAO_VERBOSE` | 启用详细日志 | `false` | `true` |

### 配置文件（可选）

创建 `.env` 文件在项目根目录：

```bash
# .env
ARK_API_KEY=your_api_key_here
DOUBAO_API_TIMEOUT=120
DOUBAO_RETRY_COUNT=5
DOUBAO_OUTPUT_DIR=./generated-images
DOUBAO_VERBOSE=true
```

加载环境变量：

```bash
# Bash
source .env

# 或使用 direnv
direnv allow
```

### 参数说明

#### prompt（必需）

图片描述文本，支持中英文。建议包含：
- 主体描述
- 环境氛围
- 艺术风格
- 技术参数

**示例：**
```
✅ 好的 prompt：
"一只白色波斯猫，坐在古老的图书馆窗台上，
午后阳光透过彩色玻璃，写实风格，4K 超精细细节，
景深效果，温暖色调"

❌ 差的 prompt：
"一只猫"
```

#### size（可选）

输出分辨率，可选值：
- `2K`（默认）- 2048×2048，高质量输出
- `1080P` - 1920×1080，社交媒体适用
- `720P` - 1280×720，快速预览

#### watermark（可选）

是否添加平台水印：
- `true`（默认）- 添加水印
- `false` - 不添加水印

## 🎨 最佳实践

### Prompt 编写技巧

#### 基本公式

```
主体描述 + 环境氛围 + 艺术风格 + 技术参数
```

#### 风格关键词库

**艺术风格：**
```
写实、油画、水彩、素描、动漫、赛博朋克、
蒸汽朋克、极简、抽象、印象派、超现实主义
```

**画面质量：**
```
4K、8K、超高清、电影大片、精致细节、杰作、 masterpiece
```

**光影效果：**
```
光线追踪、全局光照、体积光、丁达尔效应、
黄金时刻、蓝色时刻、霓虹灯光
```

**构图方式：**
```
对称构图、三分法、引导线、框架构图、
鸟瞰视角、鱼眼镜头、微距特写
```

#### 示例对比

```bash
# ❌ 过于简单
./doubao-image-generate.sh "一只猫"

# ✅ 详细描述
./doubao-image-generate.sh \
  "一只白色波斯猫，坐在古老的图书馆窗台上，
   午后阳光透过彩色玻璃，写实风格，
   4K 超精细细节，景深效果，温暖色调"

# ✅ 指定风格
./doubao-image-generate.sh \
  "赛博朋克风格的城市夜景，霓虹灯闪烁，
   雨后街道反射着五彩光芒，电影级构图，
   广角镜头，高对比度"
```

### 性能优化

1. **避免并发请求**
   ```bash
   # ❌ 不推荐：并发请求可能触发频率限制
   for prompt in "${prompts[@]}"; do
     ./doubao-image-generate.sh "$prompt" &
   done
   
   # ✅ 推荐：串行处理
   for prompt in "${prompts[@]}"; do
     ./doubao-image-generate.sh "$prompt"
     sleep 2  # 避免频率限制
   done
   ```

2. **批量生成脚本**
   ```bash
   #!/bin/bash
   prompts=(
     "春日樱花盛开"
     "夏日海滩日落"
     "秋日枫叶满山"
     "冬日雪景森林"
   )
   
   for prompt in "${prompts[@]}"; do
     echo "生成：$prompt"
     ./doubao-image-generate.sh "$prompt" "1080P"
     sleep 2
   done
   ```

3. **缓存策略**
   ```python
   import hashlib
   import json
   from pathlib import Path
   
   class CachedGenerator:
       def __init__(self, cache_dir=".cache"):
           self.cache_dir = Path(cache_dir)
           self.cache_dir.mkdir(exist_ok=True)
       
       def _get_cache_key(self, prompt, size):
           key = f"{prompt}:{size}"
           return hashlib.md5(key.encode()).hexdigest()
       
       def generate(self, prompt, size="2K"):
           cache_key = self._get_cache_key(prompt, size)
           cache_file = self.cache_dir / f"{cache_key}.json"
           
           # 检查缓存
           if cache_file.exists():
               with open(cache_file) as f:
                   data = json.load(f)
                   print(f"使用缓存：{data['path']}")
                   return Path(data['path'])
           
           # 生成新图片
           generator = DoubaoImageGenerator()
           path = generator.generate(prompt, size)
           
           # 保存缓存
           with open(cache_file, 'w') as f:
               json.dump({"path": str(path)}, f)
           
           return path
   ```

## 🔧 故障排除

### 常见问题

#### 1. 缺少 ARK_API_KEY

**错误信息：**
```
ERROR: 缺少 ARK_API_KEY 环境变量
```

**解决方案：**
```bash
# 临时设置（当前终端会话）
export ARK_API_KEY="your_api_key"

# 永久设置（添加到 shell 配置文件）
echo 'export ARK_API_KEY="your_api_key"' >> ~/.bashrc
source ~/.bashrc
```

#### 2. API 调用失败

**错误信息：**
```
API 错误：认证失败：API Key 无效或已过期
```

**解决方案：**
1. 检查 API Key 是否正确复制
2. 访问 [火山引擎控制台](https://console.volcengine.com/ark) 重新生成
3. 确认账户余额充足

#### 3. 图片下载失败

**错误信息：**
```
下载错误：图片下载失败：Connection timeout
```

**解决方案：**
```bash
# 增加超时时间
python3 scripts/doubao-image-generate.py \
  --prompt "图片描述" \
  --timeout 120

# 检查网络连接
curl -I https://ark.cn-beijing.volces.com
```

#### 4. 请求频率超限

**错误信息：**
```
API 错误：请求频率超限，等待 5 秒后重试...
```

**解决方案：**
- 增加请求间隔（建议 2-5 秒）
- 减少并发请求数量
- 使用指数退避策略

#### 5. 内容被安全策略拦截

**错误信息：**
```
API 错误：请求被拒绝：可能包含敏感词汇
```

**解决方案：**
- 修改 prompt，避免敏感词汇
- 使用更委婉的描述方式
- 参考平台内容规范

### 日志分析

启用详细日志：

```bash
# Bash 脚本
export DOUBAO_VERBOSE=true
./scripts/doubao-image-generate.sh "prompt"

# Python 脚本
python3 scripts/doubao-image-generate.py --prompt "prompt" --verbose
```

### 调试技巧

1. **测试 API 连接**
   ```bash
   curl -X POST "https://ark.cn-beijing.volces.com/api/v3/images/generations" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $ARK_API_KEY" \
     -d '{"model":"doubao-seedream-5-0-260128","prompt":"test","size":"2K"}'
   ```

2. **检查环境变量**
   ```bash
   echo "ARK_API_KEY: ${ARK_API_KEY:0:10}..."  # 显示前 10 个字符
   echo "Timeout: $DOUBAO_API_TIMEOUT"
   echo "Retry Count: $DOUBAO_RETRY_COUNT"
   ```

3. **验证 Python 环境**
   ```bash
   python3 -c "import sys; print(sys.version)"
   python3 -c "import requests; print(requests.__version__)" 2>/dev/null || echo "requests 未安装"
   ```

## 🛠️ 开发指南

### 项目结构

```
doubao-image/
├── SKILL.md                    # Skill 定义文件
├── README.md                   # 本文件
├── CHANGELOG.md                # 版本历史
├── LICENSE                     # 开源协议
├── .gitignore                  # Git 忽略文件
├── scripts/
│   ├── doubao-image-generate.sh    # Bash 实现
│   ├── doubao-image-generate.py    # Python 实现
│   └── check-env.sh                # 环境检查脚本
├── examples/
│   └── prompts.md                  # Prompt 示例
└── tests/
    └── test-api.sh                 # API 测试脚本
```

### 本地开发

```bash
# 1. Fork 并克隆项目
git clone https://github.com/your-username/doubao-image-skill.git
cd doubao-image-skill

# 2. 创建虚拟环境（Python 开发）
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# 3. 安装开发依赖
pip install -r requirements-dev.txt  # 如果有的话

# 4. 运行测试
bash tests/test-api.sh
```

### 测试脚本

```bash
#!/bin/bash
# tests/test-api.sh

set -e

echo "运行 API 测试..."

# 测试 1：基本生成
echo "测试 1：基本生成"
./scripts/doubao-image-generate.sh "测试图片" "720P" "false"

# 测试 2：不同尺寸
echo "测试 2：不同尺寸"
for size in 2K 1080P 720P; do
  echo "  测试尺寸：$size"
  ./scripts/doubao-image-generate.sh "测试 $size" "$size" "false"
done

# 测试 3：Python 脚本
echo "测试 3：Python 脚本"
python3 scripts/doubao-image-generate.py --prompt "Python 测试" --size 720P

echo "所有测试通过！"
```

## 🤝 贡献指南

### 提交代码

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: add AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 提交规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

- `feat:` 新功能
- `fix:` 修复 bug
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建/工具相关

### 报告问题

在 GitHub Issues 中创建 Issue，包含：
- 问题描述
- 复现步骤
- 预期行为
- 实际行为
- 环境信息（系统版本、Python 版本等）
- 日志输出

## ❓ 常见问题

### Q1: 生成的图片质量不佳？

**A:** 尝试以下方法：
- 使用更详细的 prompt 描述
- 添加质量关键词（4K、超精细、杰作）
- 选择 2K 分辨率
- 指定具体艺术风格

### Q2: 如何批量生成图片？

**A:** 使用循环脚本：
```bash
prompts=("描述 1" "描述 2" "描述 3")
for prompt in "${prompts[@]}"; do
  ./doubao-image-generate.sh "$prompt"
  sleep 2
done
```

### Q3: 图片版权如何？

**A:** 根据火山引擎平台协议，生成的图片版权归平台所有。请遵守平台使用规范，仅用于合法用途。

### Q4: 支持哪些图片格式？

**A:** 目前仅支持 PNG 格式输出。

### Q5: 可以一次生成多张图片吗？

**A:** API 目前仅支持单次生成一张图片。如需多张，请循环调用并设置适当间隔。

### Q6: 生成的图片可以商用吗？

**A:** 请查阅火山引擎平台的商业使用条款。建议联系官方确认具体使用场景。

### Q7: 如何节省 API 调用成本？

**A:** 
- 使用较低分辨率（720P）进行测试
- 优化 prompt 减少重试次数
- 实现本地缓存避免重复生成
- 监控账户余额和使用情况

## 📝 更新日志

详细更新日志请查看 [CHANGELOG.md](CHANGELOG.md)。

### v2.0.0 (2026-04-09)
- ✨ 重构代码结构，符合 Clawhub 标准
- ✨ 新增 Python 实现版本
- ✨ 完善错误处理和日志记录
- ✨ 添加详细使用文档
- 🐛 修复 JSON 转义问题
- 🐛 优化超时重试机制

### v1.0.0 (2026-01-15)
- ✨ 初始版本发布
- ✨ 基础 Bash 脚本实现
- ✨ 支持基本文生图功能

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🔗 相关链接

- [火山引擎 ARK 官方文档](https://www.volcengine.com/docs/82379)
- [豆包 SeeDream 产品介绍](https://www.volcengine.com/product/doubao)
- [Clawhub 技能开发指南](https://clawhub.cn/docs)
- [GitHub 仓库](https://github.com/your-username/doubao-image-skill)
- [问题反馈](https://github.com/your-username/doubao-image-skill/issues)

## 📧 联系方式

- **作者：** YangYang
- **Email:** your-email@example.com
- **问题反馈：** [GitHub Issues](https://github.com/your-username/doubao-image-skill/issues)

---

**最后更新：** 2026-04-09  
**当前版本：** 2.0.0  
**维护状态：** 活跃维护中

**⭐ 如果这个项目对你有帮助，请给个 Star 支持一下！**
