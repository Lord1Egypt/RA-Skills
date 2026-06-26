# WeChat Articles Fetcher

抓取微信公众号文章并转换为Markdown格式的OpenClaw Skill。

## 功能

- 使用Playwright无头浏览器抓取微信文章
- 提取标题、公众号名称、正文内容
- 自动转换为干净的Markdown格式
- 支持图片处理（可选下载）
- 保存为`.md`文件，包含YAML前置信息

## 依赖要求

```bash
# 安装Python依赖
pip3 install playwright beautifulsoup4

# 安装Chromium浏览器
python3 -m playwright install chromium
```

## 安装方法

### 方法1：手动安装

将整个 `wechat-articles-skill` 目录复制到OpenClaw的skills目录：

```bash
cp -r wechat-articles-skill ~/.nvm/versions/node/v24.14.0/lib/node_modules/openclaw/skills/wechat-articles/
```

### 方法2：从GitHub安装

```bash
cd ~/.nvm/versions/node/v24.14.0/lib/node_modules/openclaw/skills/
git clone https://github.com/YOUR_USERNAME/wechat-articles-skill.git wechat-articles
```

## 使用方法

在OpenClaw聊天中发送微信文章链接：

```
https://mp.weixin.qq.com/s/xxxxxx
```

Agent会自动：
1. 识别微信文章链接
2. 调用抓取脚本
3. 转换为Markdown
4. 保存文件并发送给你

## 目录结构

```
wechat-articles/
├── SKILL.md              # Skill定义文件
├── README.md             # 本说明文档
├── scripts/
│   └── fetch_article.py  # 抓取脚本
└── references/           # 参考文档
```

## 输出示例

```markdown
---
title: 文章标题
author: 公众号名称
url: https://mp.weixin.qq.com/s/xxxxx
fetched: 2024-01-15T10:30:00Z
---

# 文章标题

> 作者：公众号名称

正文内容...
```

## 注意事项

- 微信文章可能有防爬机制，首次访问可能需要等待
- 部分付费文章或私密文章无法完整抓取
- 建议在合规范围内使用，尊重原作者版权

## License

MIT
