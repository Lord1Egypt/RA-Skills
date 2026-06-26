# 微信公众号自动发布工具

一个强大的微信公众号文章发布工具，支持多种主题模板、自动上传图片、保存到草稿箱等功能。

## ✨ 功能特性

- 🎨 **16种精美主题模板** - 橙心、墨黑、姹紫、嫩青、绿意、红绯等
- 📝 **多种内容来源** - 支持AI写作、本地文件、爬虫伪原创
- 🖼️ **自动上传图片** - 自动处理文章中的本地图片
- 💾 **草稿箱管理** - 自动保存到公众号草稿箱
- 🔧 **CLI命令行工具** - 方便快捷的命令行操作

## 📦 安装

### 前置要求

- Python 3.8+
- 微信公众号开发者账号

### 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/your-username/wechat-mp-skills.git
cd wechat-mp-skills
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的微信公众号 AppID 和 AppSecret
```

## 🚀 快速开始

### 1. 配置微信公众号

#### 方式一：使用加密配置（推荐）

本项目支持 AES 加密存储凭证，保护你的 App ID 和 App Secret。

```bash
# 加密你的凭证
python scripts/encrypt_credentials.py encrypt

# 查看加密状态
python scripts/encrypt_credentials.py status
```

详细使用说明请查看 [ENCRYPTION.md](ENCRYPTION.md)。

#### 方式二：使用明文配置

编辑 `config.json` 文件：

```json
{
  "app_id": "你的AppID",
  "app_secret": "你的AppSecret",
  "base_dir": "你的文章目录"
}
```

#### 方式三：使用环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件
WECHAT_APP_ID=你的AppID
WECHAT_APP_SECRET=你的AppSecret
```

### 2. 使用命令行工具

```bash
# 获取帮助
python scripts/cli.py --help

# 保存文章到草稿箱
python scripts/cli.py save-draft --topic "AI技术进展" --app-id "xxx" --app-secret "xxx"

# 上传图片
python scripts/cli.py upload-image --image-path "photo.jpg" --app-id "xxx" --app-secret "xxx"

# 获取 AccessToken
python scripts/cli.py get-token --app-id "xxx" --app-secret "xxx"
```

### 3. 作为 OpenClaw Skill 使用

这个项目可以作为 OpenClaw 的技能插件使用：

1. 将项目放置在 OpenClaw 的 skills 目录下
2. 重启 OpenClaw
3. 使用命令："发布文章到公众号"

## 🎨 主题模板

支持16种精美主题：

1. 橙心
2. 墨黑
3. 姹紫
4. 嫩青
5. 绿意
6. 红绯
7. WeChat-Format
8. 科技蓝
9. 兰青
10. 山吹
11. 前端之巅
12. 极客黑
13. 简（默认）
14. 蔷薇紫
15. 萌绿
16. 全栈蓝

## 📁 项目结构

```
wechat-mp-skills/
├── scripts/
│   ├── wechat/
│   │   ├── api_client.py      # 微信公众号 API 客户端
│   │   ├── content_generator.py # 内容生成器
│   │   └── theme.py           # 主题样式
│   └── cli.py                 # 命令行工具
├── config.json                # 配置文件
├── image_mapping.json         # 图片路径映射
├── SKILL.md                   # OpenClaw Skill 定义
└── README.md                  # 项目文档
```

## 🔧 API 使用

### 获取 AccessToken

```python
from scripts.wechat.api_client import WeChatMPClient

client = WeChatMPClient(app_id, app_secret)
token = client.get_access_token()
```

### 上传图片

```python
# 上传文章内图片
result = client.upload_article_image(image_path="path/to/image.png")

# 上传永久素材图片
result = client.upload_permanent_image_from_url(image_url="https://...")
```

### 保存草稿

```python
result = client.save_draft(
    title="文章标题",
    content="<p>文章内容</p>",
    author="作者",
    cover_image_path="cover.png"
)
```

## 📝 配置说明

### config.json

```json
{
  "app_id": "微信公众号AppID",
  "app_secret": "微信公众号AppSecret",
  "base_dir": "文章基础目录"
}
```

### image_mapping.json

用于映射 Markdown 中的图片路径到实际文件路径：

```json
{
  "images/1.png": "/actual/path/to/images/1.png",
  "images/2.png": "/actual/path/to/images/2.png"
}
```

## 🔐 安全建议

### 基本安全措施

1. **使用加密存储** - 使用 AES 加密存储 App ID 和 App Secret（推荐）
2. **不要提交敏感信息** - 确保 `.secret_key` 和 `.env` 文件不被提交到版本控制
3. **使用环境变量** - 推荐使用 `.env` 文件管理敏感凭证
4. **定期更换密钥** - 定期在微信公众平台重置 AppSecret
5. **文件权限** - 设置配置文件权限为 600（仅所有者可读写）

### 高级安全特性

本项目包含以下安全功能：

- ✅ **凭证加密** - AES 加密存储 App ID 和 App Secret
- ✅ **路径验证** - 防止路径遍历攻击
- ✅ **URL 验证** - 防止 SSRF 攻击
- ✅ **输入清理** - 防止 XSS 攻击
- ✅ **文件类型验证** - 只允许上传图片文件
- ✅ **文件大小限制** - 限制上传文件大小为 10MB

### 安全最佳实践

```bash
# 1. 加密凭证（推荐）
python scripts/encrypt_credentials.py encrypt --use-password

# 2. 设置文件权限
chmod 600 .env config.json .secret_key

# 3. 使用环境变量
export WECHAT_APP_ID="your_app_id"
export WECHAT_APP_SECRET="your_app_secret"

# 4. 定期检查依赖漏洞
pip install pip-audit
pip-audit

# 5. 使用虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 6. 定期更换加密密钥
rm .secret_key
python scripts/encrypt_credentials.py encrypt
```

### 凭证加密说明

本项目支持 AES 加密存储凭证，提供企业级安全保护：

- **加密算法**: AES (Fernet)
- **密钥管理**: 自动生成或密码派生
- **双重保护**: 可选密码加密
- **透明解密**: 代码中自动处理

详细使用说明请查看 [ENCRYPTION.md](ENCRYPTION.md)。

### 安全报告

如果你发现安全漏洞，请负责任地披露。详见 [SECURITY.md](SECURITY.md) 文件。

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📮 联系方式

如有问题或建议，请提交 Issue。

## 🙏 致谢

感谢所有贡献者的支持！
