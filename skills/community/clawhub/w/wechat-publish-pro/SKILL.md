# wechat-publish-pro Skill

微信公众号文章发布工具，完全独立实现，不依赖任何外部 CLI 工具。

## 功能特性

- **纯 Python 实现**: 不依赖 wenyan-cli 或其他外部工具
- **Markdown 转换**: 内置 Markdown → HTML 转换，参考 wenyan-cli 排版风格
- **多主题支持**: 多种精美主题（green、blue、purple、orange、default、simple）
- **代码高亮**: Mac 风格代码块，语法高亮
- **封面生成**: 自动处理封面图，支持本地/网络图片
- **直接发布**: 一键发布到微信公众号草稿箱

## 触发条件

当用户需要以下操作时自动触发：
- 将 Markdown 或 HTML 文章发布到微信公众号草稿箱
- 转换 Markdown 为公众号格式 HTML
- 使用特定主题发布公众号文章
- 测试微信连接

## 安装

```bash
# 从 GitHub 安装
pip install git+https://github.com/yuesf/wechat-publish-pro.git
```

## 配置

### 第一步：获取微信公众号凭证

1. 登录 [https://developers.weixin.qq.com/](https://developers.weixin.qq.com/) 公众号平台
2. 获取 **AppID** 和 **AppSecret**

### 第二步：配置凭证

#### 环境变量

```bash
export WECHAT_APP_ID=your_wechat_app_id
export WECHAT_APP_SECRET=your_wechat_app_secret
```

#### 配置文件

```bash
# 初始化配置
wechat-publish-pro config init

# 设置配置
wechat-publish-pro config set wechat.app_id <AppID>
wechat-publish-pro config set wechat.app_secret <AppSecret>
```

### 第三步：设置 IP 白名单

把运行机器的 IP 添加到微信公众号后台白名单：
1. 登录 https://mp.weixin.qq.com/
2. 设置与开发 → 基本配置 → IP白名单

## 使用方式

### 通过 OpenClaw 直接发送

在 OpenClaw 对话中直接说：
- "把这篇文章发到公众号"
- "用蓝色主题发布"
- "帮我发布到微信，测试一下"

### 命令行方式

#### Markdown 转换

```bash
# 基本转换（默认绿色主题）
wechat-publish-pro convert article.md

# 指定蓝色主题
wechat-publish-pro convert article.md --theme blue

# 指定输出文件
wechat-publish-pro convert article.md -o output.html
```

#### 发布到微信

```bash
# 发布 HTML 文件到草稿箱（需要指定账号，否则会卡在交互提示）
wechat-publish-pro publish article.html --account <账号标识>

# 指定标题和封面
wechat-publish-pro publish article.html --title "文章标题" --cover cover.jpg --account <账号标识>
```

**常见问题：**
- **发布命令卡住不动**：确保使用 `--account` 参数指定账号，避免交互式选择
- **封面上传失败**：确认封面图片路径存在，不存在时省略 `--cover` 参数

#### 一站式：Markdown → 转换 → 发布

```bash
# 转换后直接发布
wechat-publish-pro convert article.md --theme blue -o /tmp/article.html
wechat-publish-pro publish /tmp/article.html --title "文章标题"
```

#### 测试连接

```bash
wechat-publish-pro test
```

#### 上传图片

```bash
wechat-publish-pro upload-image image.jpg
```

## Markdown 格式

文件顶部可以包含 frontmatter（建议只用 cover，不用 title，避免重复）：

```markdown
<!--
title: 文章标题
---
cover: ./assets/cover.jpg
---

你的内容...
```

**重要注意事项**：

- **不要在正文使用 `#` 大标题**——标题由命令行 `-t` 参数提供，正文里的 `#` 标题会导致标题重复输出
- **不要使用 `---` 作为章节分隔线**——wenyan-cli 会将其误解析为列表项 `• --`，用空行替代 `---`
- **frontmatter 的 `title` 会被输出到正文**——如果同时在正文写了 `#` 标题，会导致两个标题重复；建议 frontmatter 的 title 用 `<!-- -->` 包裹，或完全不用 frontmatter 的 title，改由命令行 `-t` 提供标题

**推荐格式**：

```markdown
<!--
title: 文章标题（可选，用命令行 -t 更稳定）
cover: ./assets/cover.jpg
---

第一段内容（直接开始，不要用 `#` 标题）

## 章节标题（使用 ## ，不是 #）

内容...

（章节之间用空行分隔，不要用 ---）
```

## 可用主题

| 主题 | 风格 |
|------|------|
| green | 清新自然（绿色，默认） |
| blue | 清新专业（蓝色） |
| purple | 优雅神秘（紫色） |
| orange | 温暖活力（橙色） |
| default | 简洁清爽 |
| simple | 极简风格 |

## 故障排查

### 错误：45166 (IP地址不在白名单中)
- 原因：运行机器的 IP 未添加到微信白名单
- 解决：登录公众号后台添加 IP 到白名单

### 发布成功但看不到文章？
- 原因：文章在草稿箱，需要审核发布
- 解决：草稿箱 → 选中文章 → 发布

## 架构说明

```
wechat-publish-pro/
├── src/wechat_publish_pro/
│   ├── cli.py         # CLI 入口
│   ├── config.py      # 配置管理
│   ├── converter/     # Markdown 转换模块
│   │   ├── wechat_style.py   # 微信公众号样式转换器
│   │   ├── themes.py          # 主题配置
│   │   └── theme_types.py     # 主题数据类型
│   └── platforms/     # 平台适配器
│       └── wechat.py # 微信公众号 API
└── pyproject.toml
```

## 设计参考

本项目参考了以下优秀项目的设计思路：
- **wenyan-cli**: Markdown 转微信 HTML 的排版思路
- **multi-writing-skills**: 转换器和主题系统的实现

但本项目是完全独立实现的，不依赖任何外部代码。

## 作者

yuesf

## 许可证

MIT
