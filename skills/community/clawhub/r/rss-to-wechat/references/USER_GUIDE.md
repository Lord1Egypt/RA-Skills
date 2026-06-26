# RSS to WeChat Skill

将 RSS 文章转换为微信公众号格式并发布的通用工具。

## 特性

- ✅ **通用性**：支持任何 RSS 源或 URL
- ✅ **可配置**：品牌、样式、关键词完全可定制
- ✅ **模块化**：数据获取、内容生成、发布分离
- ✅ **灵活性**：AI 助手可根据内容调整结构
- ✅ **安全性**：本地配置不会被提交到 git

## 快速开始

### 1. 安装依赖

```bash
# 必需工具
brew install curl jq pandoc  # macOS
# 或
apt-get install curl jq pandoc  # Linux

# 可选工具（用于 --auto 模式）
npm install -g blogwatcher
```

### 2. 配置

```bash
# 复制配置示例
cd ~/clawd/skills/rss-to-wechat
cp config.example.sh config.local.sh

# 编辑配置
nano config.local.sh
```

最小配置：

```bash
# 微信公众号配置
WECHAT_APPID="your_appid"
WECHAT_APPSECRET="your_secret"

# 品牌配置
BRAND_NAME="你的公众号名称"
BRAND_SLOGAN="你的 Slogan"
```

### 3. 检查配置

```bash
bash rss-to-wechat.sh --check
```

### 4. 使用

```bash
# 指定文章 URL
bash rss-to-wechat.sh --url "https://example.com/article"

# 自动选择最新文章（需要 blogwatcher）
bash rss-to-wechat.sh --auto
```

## 工作流程

1. **数据准备**（自动）
   - 解析文章内容
   - 提取标题、作者、正文
   - 保存到 JSON 文件

2. **HTML 生成**（AI 助手）
   - 根据模板和指导生成微信格式 HTML
   - 使用你的品牌配置
   - 保存到草稿目录

3. **封面生成**（可选）
   - 如果配置了 `COVER_SKILL`
   - 自动生成 1283×383 封面图

4. **发布**（可选）
   - 如果配置了微信凭证
   - 自动上传到草稿箱
   - 或手动发布

## 配置选项

### 必需配置

```bash
# 微信公众号
WECHAT_APPID="your_appid"
WECHAT_APPSECRET="your_secret"

# 品牌
BRAND_NAME="你的公众号名称"
BRAND_SLOGAN="你的 Slogan"
```

### 可选配置

```bash
# RSS 订阅源
RSS_SOURCES=(
  "example.com"
  "another-blog.com"
)

# 筛选条件
MIN_VIEWS_DAILY=10000
MAX_VIEWS_DAILY=100000

# 关键词
PRIORITY_KEYWORDS=(
  "AI"
  "Technology"
)

EXCLUDE_KEYWORDS=(
  "crypto"
  "blockchain"
)

# 路径
WORKSPACE="$HOME/my-workspace"
OUTPUT_DIR="$WORKSPACE/output"
DRAFTS_DIR="$WORKSPACE/drafts"

# 外部工具
COVER_SKILL="/path/to/cover-generator.sh"
WECHAT_PUBLISH_SCRIPT="/path/to/publish-script.sh"

# 品牌样式
BRAND_COLOR="#c41e3a"

# 时区
TZ="Asia/Shanghai"

# 调试
DEBUG=1
```

## HTML 格式要求

微信公众号对 HTML 格式要求严格，必须遵循：

### 必须使用
- `<section>` 和 `<p>` 标签
- 内联样式 `style="..."`
- `<strong>` 和 `<em>` 标签
- `<br/>` 换行
- 完整 URL

### 禁止使用
- `<div>` 标签
- `class` 和 `id` 属性
- 相对链接 `<a href="/...">`
- 外部 CSS
- JavaScript

### 内容结构

1. 头部品牌 Logo（内联 SVG）
2. 日期栏
3. 标题
4. 核心观点（TL;DR）
5. 详细内容（分段落）
6. 原文链接

参考 `html-template.md` 查看完整模板。

## 文件结构

```
rss-to-wechat/
├── README.md              # 本文件
├── SKILL.md               # Skill 描述
├── config.sh              # 默认配置
├── config.example.sh      # 配置示例
├── config.local.sh        # 本地配置（不提交）
├── .gitignore             # Git 忽略规则
├── rss-to-wechat.sh       # 主脚本
├── parse-article.sh       # 文章解析
├── html-template.md       # HTML 模板
└── test.sh                # 测试脚本
```

## 示例

### 完整流程

```bash
# 1. 获取文章数据
bash rss-to-wechat.sh --url "https://simonwillison.net/..."

# 2. AI 助手生成 HTML（根据提示）
# 保存到: ~/clawd/drafts/rss-2026-03-06.html

# 3. 生成封面（如果配置了）
bash "$COVER_SKILL" \
  "文章标题" \
  ~/clawd/drafts/rss-2026-03-06-cover.png

# 4. 上传草稿（如果配置了）
bash "$WECHAT_PUBLISH_SCRIPT" \
  "文章标题" \
  ~/clawd/drafts/rss-2026-03-06.html \
  ~/clawd/drafts/rss-2026-03-06-cover.png
```

### 自动化

```bash
# 每天自动获取最新文章
0 7 * * * cd ~/clawd/skills/rss-to-wechat && bash rss-to-wechat.sh --auto
```

## 故障排除

### 错误码 45166: invalid content

检查 HTML 格式：
- 是否包含不支持的标签？
- 所有样式都是内联的吗？
- 是否有 `class`、`id` 属性？
- 参考成功案例的格式

### 文章解析失败

- 检查 URL 是否可访问
- 确认网站没有反爬虫限制
- 尝试手动复制内容

### 配置检查失败

```bash
bash rss-to-wechat.sh --check
```

查看详细错误信息。

## 进阶使用

### 自定义 HTML 模板

编辑 `html-template.md`，添加你的自定义样式和结构。

### 集成其他工具

在 `config.local.sh` 中设置：

```bash
# 自定义封面生成
COVER_SKILL="/path/to/your/cover-generator.sh"

# 自定义发布脚本
WECHAT_PUBLISH_SCRIPT="/path/to/your/publish-script.sh"
```

### 批量处理

```bash
# 处理多篇文章
for url in $(cat urls.txt); do
  bash rss-to-wechat.sh --url "$url"
done
```

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可

MIT License

## 相关 Skills

- `wechat-daily` - 日报生成
- `wechat-featured` - 精选文章
- `wechat-cover` - 封面生成
- `wechat-publish` - 草稿上传

## 支持

- 文档：查看 `SKILL.md` 和 `html-template.md`
- 配置帮助：`bash rss-to-wechat.sh --config`
- 检查配置：`bash rss-to-wechat.sh --check`
