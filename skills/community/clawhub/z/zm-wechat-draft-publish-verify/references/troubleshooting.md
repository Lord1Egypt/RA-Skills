# 故障排查（wechat-publisher 正式链路）

## 正式链路

```text
HTML / Markdown
→ md2wechat config validate
→ inspect / preview / convert（如需要）
→ md2wechat upload_image cover.*
→ 生成 draft.json
→ md2wechat create_draft draft.json
→ 微信 draft/get 核验
```

## 先判断你卡在哪一层

1. **环境层**：`md2wechat` / `python3` / 配置文件是否可用
2. **凭证层**：AppID / AppSecret 是否正确
3. **网络白名单层**：当前公网 IP 是否在公众号后台白名单
4. **输入产物层**：HTML / Markdown / cover 是否存在且格式对
5. **提交层**：`create_draft` 是否真的返回成功
6. **核验层**：`draft/get` 是否真的查到草稿并字段一致

不要一上来就说“平台抽风”。先分层定位。

## 常见错误

### 1）IP 白名单错误

报错：

```text
errcode=40164 invalid ip ... not in whitelist
```

处理：

- 查询当前机器公网 IP
- 加入微信公众号后台 IP 白名单
- 重新执行发布

### 2）AppSecret 错误

报错：

```text
errcode=40125 invalid appsecret
```

处理：修正：

```text
~/.config/md2wechat/config.yaml
```

中的：

```yaml
wechat:
  appid: "..."
  secret: "..."
```

### 3）AI 模式只返回请求，没有成稿

返回：

```json
{
  "code": "CONVERT_AI_REQUEST_READY",
  "status": "action_required"
}
```

这不是失败，也不是成功。它只是说明：AI 排版请求准备好了。

正确处理：

```text
根据 prompt 继续生成公众号兼容 HTML
→ 落盘 HTML
→ upload_image
→ create_draft
→ draft/get 核验
```

### 4）create_draft 缺字段

最小 `draft.json` 至少需要：

```json
{
  "articles": [
    {
      "title": "标题",
      "content": "<section>正文 HTML</section>"
    }
  ]
}
```

正式流程还应补齐：

```json
{
  "author": "野哥",
  "digest": "摘要",
  "thumb_media_id": "封面 media_id",
  "show_cover_pic": 0
}
```

### 5）命令成功，但不能算正式完成

`create_draft` 返回成功后，还必须做 `draft/get` 核验：

- 草稿真实存在
- 标题正确
- 作者正确
- 封面存在
- 正文存在
- 无本地路径泄漏
- 正文图片真实可见
- 若输入是 Markdown，要确认不是只生成了本地 preview / convert 产物
- 若上游走 AI 模式，要确认最终进后台的是落盘后的 HTML，而不是 request-ready 响应

核验未通过前，不得汇报“已推草稿成功”。

### 6）本地看起来正常，后台却没有

这是最危险的误判场景。

常见原因：

- 只做了 `preview`
- 只做了 `convert`
- `create_draft` 请求发了，但核验失败
- `media_id` 被误当成最终成功证明

处理原则：

- 只认 `*.md2wechat-create-draft-verify.json`
- 没有核验文件通过，就不能报成功

## 最稳执行方式

优先执行：

```bash
cd <openclaw-home>/workspace/skills/zm-wechat-draft-publish-verify
./scripts/publish.sh /path/to/article.html /path/to/cover.png "标题" "野哥" "摘要"
```

原因：

- 自动做配置校验
- Markdown 输入自动补 `inspect / preview / convert`
- 自动上传封面
- 自动生成 `draft.json`
- 自动执行 `create_draft`
- 自动调用微信 `draft/get`
- 自动生成核验证据文件

## 结果判断口径

### 可汇报“已推草稿成功”

必须同时满足：

- `create_draft` 成功
- `draft/get` 成功
- 标题 / 作者 / 正文 / 封面核验通过

### 只能汇报“已提交待核验”

适用于：

- 已拿到提交结果
- 但还没做 `draft/get`
- 或核验文件还没生成

### 应汇报“阻塞 / 失败”

适用于：

- 配置错
- 白名单错
- AI 模式未落盘 HTML
- `draft/get` 查不到草稿
- 核验字段不一致

## 经验沉淀

### 2026-05-15

这次正式沉淀的核心经验：

- 正式推草稿默认走 `scripts/publish.sh`
- `media_id` 只是回执，不是成功证明
- `CONVERT_AI_REQUEST_READY` 是“继续动作提示”，不是成功状态
- `preview / convert / test-draft` 都不能替代 `create_draft + draft/get`
- 命令成功但后台无草稿时，优先按核验失败处理，不先假设平台延迟
