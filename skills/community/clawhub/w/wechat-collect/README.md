# wechat-collect

`wechat-collect` 是当前阶段 2A 的入口 skill。它把一篇公众号文章 URL 转成可直接进入主写作链的 brief，并把原始 HTML 归档下来。

## 这个 skill 能做什么

- 读取公众号文章 URL
- 抓取正文 HTML
- 提取标题、作者、发布日期和候选正文段落
- 生成阶段 1 可复用的 brief
- 保存 raw HTML，便于后续抽取调优和复盘

## 安装

### 基础依赖

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

### 可选：浏览器兜底依赖

当公众号页面被验证码或环境校验拦住时，会尝试调用 Playwright 浏览器兜底。首次建议执行：

```bash
cd skills/wechat-studio/frontend
npm install
npx playwright install chromium
```

## 输入和输出

**输入**

- 一个文本文件，里面至少有一个公众号 URL
- 例如：`content-production/inbox/20260403-wechat-collect-url.txt`

**输出**

- `content-production/inbox/<date>-<slug>-gzh-brief.md`
- `content-production/inbox/raw/wechat/<date>-<slug>.html`

## 使用方法

### 单独运行

```bash
.venv/bin/python -m skill_runtime.cli run-skill wechat-collect \
  --input content-production/inbox/20260403-wechat-collect-url.txt
```

### 常见下游衔接

- `case-writer-hybrid`
- `generate-image`
- `wechat-formatter`
- 完整链路可直接用 `stage2-wechat-pipeline`

## 什么时候用

- 你看到一篇公众号文章，想快速转成自己的再创作素材
- 你不想手工整理正文，想直接得到规范 brief
- 你需要保留原始 HTML 方便以后排查抽取问题

## 注意事项

- 只适用于公开可访问的公众号文章链接
- 若遇到微信验证码页，先在弹出的浏览器里完成验证再重试
- 参数错误页、过期页、删除页不会生成可用 brief

## 相关文件

- [SKILL.md](./SKILL.md)
- [runtime.py](./runtime.py)
- [stage2-wechat-pipeline.json](../../workflows/stage2-wechat-pipeline.json)
