# wechat-report

`wechat-report` 是公众号主题对比 skill。它会围绕一个主题收集多篇公众号文章，抽正文、互动指标、结构特征和爆款写法，最后生成一份本地对比报告。

## 这个 skill 能做什么

- 围绕一个主题收集多篇公众号文章
- 生成本地 `wechat-report.md`
- 保存结构化 raw JSON
- 产出文章总表、互动对比表、内容结构表
- 补充标题 / 开头 / 结尾 / 转发钩子的写法拆解
- 为后续 `feishu-bitable-sync` 提供标准输入

## 安装

### 基础依赖

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

### Node 依赖

公众号抽取和浏览器兜底依赖 Node 与 Playwright。首次建议执行：

```bash
cd skills/wechat-article-extractor-skill
npm install

cd ../wechat-studio/frontend
npm install
npx playwright install chromium
```

## 输入和输出

**输入**

- 一个带 frontmatter 的请求文件
- 常用字段：`topic`、`max_articles`、`seed_urls`、`collect_engagement`、`discovery_mode`

**输出**

- `content-production/inbox/YYYYMMDD-<slug>-wechat-report.md`
- `content-production/inbox/raw/wechat-report/YYYY-MM-DD/<slug>.json`

## 使用方法

### 单独运行

```bash
.venv/bin/python -m skill_runtime.cli run-skill wechat-report \
  --input content-production/inbox/20260407-harness-engineering-wechat-report-request.md
```

### 常见下游

- 用户先阅读本地报告
- 确认后再运行 `feishu-user-auth`
- 最后运行 `feishu-bitable-sync`

## 什么时候用

- 你想知道某个主题下，公众号同行都怎么写
- 你需要做“公众号选题调研”而不是只看一篇文章
- 你希望把结果沉淀到飞书做后续管理

## 注意事项

- 本 skill 不会自动发飞书
- 微信页面可能触发验证码或参数错误页，浏览器兜底只负责尽量拿到 HTML
- 互动数字并不总能从公开页直接拿到，报告里会明确标注采集状态

## 相关文件

- [SKILL.md](./SKILL.md)
- [runtime.py](./runtime.py)
- [collect_engagement.js](./scripts/collect_engagement.js)
- [fetch_article_html.js](./scripts/fetch_article_html.js)
