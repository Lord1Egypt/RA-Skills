# wxpublic-fetch

公众号获取技能skill —— 从微信公众号抓取文章，转换为 Markdown，图片下载到本地。<br/>
技能官网：<a href="https://wxpub.aibana.art/">https://wxpub.aibana.art</a>

## 安装

在 Claude Code 中安装 `.skill` 文件：

```bash
claude skill install wxpublic-fetch.skill
```

## 使用

```
/wxpublic-fetch <公众号名称> [startDate] [endDate] [--output 目录] [--app-id <AppID>] [--secret <SecretKey>]
```

### 示例

```
/wxpublic-fetch 拆神
/wxpublic-fetch 拆神 2026-04-15 2026-04-21
/wxpublic-fetch 拆神 2026-04-01 2026-04-21 --output ~/articles
/wxpublic-fetch 拆神 --app-id ak_xxx --secret abc123
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `公众号名称` | 必填，要抓取的公众号名称 | — |
| `startDate` | 开始日期，格式 `yyyy-MM-dd` | 今天往前 7 天 |
| `endDate` | 结束日期，格式 `yyyy-MM-dd` | 今天 |
| `--output` | 文章保存目录 | `~/wxpublic_articles/<名称>` |
| `--app-id` | 平台 AppID | 环境变量 `WXPUBLIC_APP_ID` |
| `--secret` | 平台 SecretKey | 环境变量 `WXPUBLIC_SECURE_KEY` |

## AppID 和 SecretKey

使用本 Skill 需要有效的 AppID 和 SecretKey。

- 通过参数传入：`--app-id <AppID> --secret <SecretKey>`
- 或设置环境变量：

  ```bash
  export WXPUBLIC_APP_ID=ak_xxx
  export WXPUBLIC_SECURE_KEY=abc123
  ```

如果尚未拥有 AppID 和 SecretKey，请前往 [https://wxpub.aibana.art](https://wxpub.aibana.art) 注册并生成。

## 输出结果

抓取完成后，Markdown 文件保存至指定目录，图片统一下载到 `<目录>/images/`。

```
✓ 已保存 3 篇文章到 ~/wxpublic_articles/拆神

保存的文件：
1. ~/wxpublic_articles/拆神/文章标题一.md
2. ~/wxpublic_articles/拆神/文章标题二.md
3. ~/wxpublic_articles/拆神/文章标题三.md
```

抓取完成后可直接在 Claude Code 中提问：

```
帮我总结这些文章
这些文章的主要观点是什么？
```
