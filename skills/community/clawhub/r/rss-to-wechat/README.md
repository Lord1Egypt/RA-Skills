# RSS to WeChat | RSS 转微信公众号

中文 | [English](README.en.md)

OpenClaw skill，用于将 RSS 文章转换为微信公众号格式。

## 特性

- ✅ 解析 RSS 订阅和网页文章
- ✅ 生成微信兼容的 HTML 格式
- ✅ 可配置品牌和样式
- ✅ 可选封面图生成
- ✅ 可选自动发布

## 安装

### 方式 1：通过 ClawHub 安装（推荐）

```bash
# 安装
clawhub install rss-to-wechat

# 配置
cd rss-to-wechat
cp references/config.example.sh config.local.sh
nano config.local.sh  # 编辑配置
```

### 方式 2：手动安装

```bash
# 克隆仓库
git clone https://github.com/huangbaixun/rss-to-wechat.git
cd rss-to-wechat

# 配置
cp references/config.example.sh config.local.sh
nano config.local.sh  # 编辑配置
```

## 快速开始

### 1. 配置

```bash
# 复制配置示例
cp references/config.example.sh config.local.sh

# 编辑配置文件
nano config.local.sh
```

最小配置：

```bash
# 微信公众号配置（必需）
WECHAT_APPID="你的AppID"
WECHAT_APPSECRET="你的AppSecret"

# 品牌配置
BRAND_NAME="你的公众号名称"
BRAND_SLOGAN="你的 Slogan"
```

### 2. 检查配置

```bash
bash scripts/rss-to-wechat.sh --check
```

### 3. 使用

```bash
# 处理指定文章
bash scripts/rss-to-wechat.sh --url "https://example.com/article"

# 自动选择最新文章（需要 blogwatcher）
bash scripts/rss-to-wechat.sh --auto
```

## 工作流程

1. **数据准备**（自动）
   - 脚本获取并解析文章
   - 提取标题、作者、内容
   - 保存为 JSON

2. **HTML 生成**（AI 辅助）
   - AI 助手生成微信兼容的 HTML
   - 使用你的品牌配置
   - 遵循严格的格式要求

3. **封面生成**（可选）
   - 如果配置了 `COVER_SKILL`
   - 生成 1283×383 封面图

4. **发布**（可选）
   - 如果配置了微信凭证
   - 通过 API 上传到草稿箱

## 微信 HTML 格式要求

微信公众号 API 对 HTML 格式有严格要求：

**必须使用：**
- `<section>` 和 `<p>` 标签（不用 `<div>`）
- 内联样式 `style="..."`
- `<strong>` 和 `<em>` 标签
- 完整 URL（不用相对链接）

**禁止使用：**
- `class` 或 `id` 属性
- 外部 CSS
- JavaScript
- 相对链接

详见 `references/html-template.md` 查看完整模板和示例。

## 文档

- **[SKILL.md](SKILL.md)** - Skill 主文档（英文）
- **[用户指南](references/USER_GUIDE.md)** - 完整使用指南（英文）
- **[HTML 模板](references/html-template.md)** - 微信 HTML 格式参考（英文）
- **[配置示例](references/config.example.sh)** - 配置选项说明

## 依赖

**必需：**
- `curl` - HTTP 请求
- `jq` - JSON 处理
- `pandoc` - 格式转换

**可选：**
- `blogwatcher` - RSS 订阅管理（用于 --auto 模式）
- 自定义封面生成脚本
- 自定义发布脚本

## 目录结构

```
rss-to-wechat/
├── SKILL.md              # Skill 主文档
├── README.md             # 英文说明
├── README.zh-CN.md       # 中文说明（本文件）
├── scripts/              # 可执行脚本
│   ├── rss-to-wechat.sh # 主入口
│   ├── parse-article.sh # 文章解析器
│   └── config.sh        # 默认配置
├── references/           # 文档
│   ├── USER_GUIDE.md    # 完整指南
│   ├── html-template.md # HTML 格式参考
│   └── config.example.sh# 配置示例
└── assets/              # 输出资源（空）
```

## 配置选项

查看 `references/config.example.sh` 了解所有可用选项：

- RSS 源和过滤条件
- 品牌定制（名称、标语、颜色）
- 路径配置
- 外部工具集成
- 关键词过滤

## 故障排除

**错误 45166（invalid content）**
- 检查 HTML 格式是否符合要求
- 确保所有样式都是内联的
- 移除 class/id 属性
- 参考成功案例

**文章解析失败**
- 检查 URL 是否可访问
- 确认没有反爬虫措施
- 尝试手动提取内容

**配置问题**
- 运行 `bash scripts/rss-to-wechat.sh --check`
- 确认所有必需工具已安装
- 检查微信凭证

## OpenClaw 集成

### Skill 触发条件

当你在 OpenClaw 中提到以下内容时，此 skill 会自动激活：

- "RSS 转微信"
- "发布文章到公众号"
- "微信公众号格式"
- "从 RSS 获取文章"
- "WeChat Official Account"

### 使用示例

在 OpenClaw 中，你可以直接说：

```
"帮我把这篇文章转换为微信公众号格式：https://example.com/article"

"从 RSS 订阅中选择最新文章发布到公众号"

"生成一篇微信公众号文章，内容来自 Simon Willison 的博客"
```

AI 助手会自动：
1. 加载此 skill
2. 解析文章内容
3. 生成微信格式 HTML
4. 创建封面图
5. 上传到草稿箱

## 许可证

MIT License - 查看 [LICENSE](LICENSE)

## 贡献

欢迎提交 Issue 和 Pull Request！

## 相关项目

- [OpenClaw](https://openclaw.ai) - AI 助手框架
- [ClawHub](https://clawhub.com) - OpenClaw Skill 市场

## 作者

黄百训 ([@huangbaixun](https://github.com/huangbaixun))

## 致谢

感谢 OpenClaw 社区的支持和反馈。
