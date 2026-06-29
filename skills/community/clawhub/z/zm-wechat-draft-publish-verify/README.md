# wechat-publisher

微信公众号草稿推送执行层，负责把**已经准备好的公众号稿**稳定推入草稿箱，并在汇报成功前完成微信后台核验。

## 它解决什么问题

过去最容易踩的坑有三个：

1. 把 `preview` / `convert` 当成真正进草稿箱
2. 把 `media_id` 当成最终成功证明
3. 把 `CONVERT_AI_REQUEST_READY` 当成 AI 排版完成

这个 skill 的目标，就是把正式发布链收成一条稳定标准链：

```text
文章 HTML / Markdown
→ 封面上传
→ create_draft
→ draft/get 核验
→ 再汇报成功
```

## 标准执行方式

```bash
cd <openclaw-home>/workspace/skills/zm-wechat-draft-publish-verify
./scripts/publish.sh /path/to/article.html /path/to/cover.png "标题" "野哥" "摘要"
```

也支持 Markdown 输入：

```bash
./scripts/publish.sh /path/to/article.md /path/to/cover.png "标题" "野哥" "摘要"
```

## 脚本自动做的事

- `md2wechat config validate --json`
- 若输入是 Markdown：
  - `inspect`
  - `preview`
  - `convert`
- 上传封面图
- 生成 `draft.json`
- 执行 `md2wechat create_draft`
- 调微信官方 `draft/get` 做独立核验
- 生成最终核验证据文件

## 环境要求

需要：

- `md2wechat`
- `python3`

配置文件：

```text
~/.config/md2wechat/config.yaml
```

至少包含：

```yaml
wechat:
  appid: "公众号 AppID"
  secret: "公众号 AppSecret"
```

另外必须保证当前机器公网 IP 已在公众号后台白名单。

## 成功口径

只有下面两件事同时成立，才算真的“推草稿成功”：

1. `md2wechat create_draft` 返回成功
2. `*.md2wechat-create-draft-verify.json` 核验通过，且后台草稿真实存在

否则只能算：

- 已提交待核验
- 核验失败
- 发布阻塞

## 注意

- `test-draft` 只用于链路验证，不作为正式发布方式
- `preview` / `convert` / `media_id` 都不能单独当成功依据
- `convert --mode ai` 返回 `CONVERT_AI_REQUEST_READY` 时，表示“还要继续生成 HTML”，不是成功
- 正式执行默认优先跑 `scripts/publish.sh`

## 输出文件

脚本会在文章目录旁生成：

```text
*.md2wechat-inspect.json
*.md2wechat-preview.json
*.md2wechat-convert.json
*.md2wechat-cover-upload.json
*.md2wechat-create-draft.json
*.md2wechat-create-draft-result.json
*.md2wechat-create-draft-verify.json
```

其中最终证据是：

```text
*.md2wechat-create-draft-verify.json
```

## 相关文件

- `SKILL.md`：标准 skill 说明
- `references/troubleshooting.md`：故障排查
- `references/themes.md`：发布相关补充
- `scripts/publish.sh`：正式执行脚本
- `scripts/setup.sh`：安装/准备脚本
