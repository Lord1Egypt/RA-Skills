# authorize — 媒体账号 OAuth 授权

> 为尚未绑定或 Token 已失效的媒体账号发起 OAuth 授权，在浏览器中完成授权后自动跳回账号管理页。

---

## 用法

```bash
siluzan-cso authorize --media-type YouTube
siluzan-cso authorize --media-type TikTokBusinessAccount   # TikTok（注意不是 TikTok）
siluzan-cso authorize --media-type Instagram
siluzan-cso authorize --media-type Facebook
siluzan-cso authorize --media-type LinkedIn
siluzan-cso authorize --media-type Twitter    # X（推特）
```

命令执行后 CLI 会打印授权链接，并尝试在系统默认浏览器中打开授权页面；用户在浏览器完成授权后会自动跳转回账号管理页。

**当前若运行在受限的 API/工具环境（如沙箱、容器、远程 Agent 等无法自动唤起本地浏览器的场景），必须将 CLI 输出的完整授权链接展示给用户，由其手动复制到浏览器打开**

> ⚠️ 链接显示规范（必须遵守，否则可能会出现 URL 溢出容器、被强制折行、排版错乱）：
>
> - **必须**使用独立的围栏代码块（三个反引号 ` ``` `）展示链接，并指定语言为 `text`，让链接独占一整块、可横向滚动；
> - **不要**使用单反引号的行内代码（` `...` `）包裹长 URL —— 行内代码不会横向滚动，会被强制折行；
> - **不要**使用 Markdown 链接语法 `[文本](https://...)` —— 用户复制时容易漏掉字符；
> - 链接前后各保留一行空行，避免与正文挤在一起。
>
> ✅ 正确示例（向用户呈现的内容）：
>
> 请在浏览器中打开下面的授权链接完成授权：
>
> ```text
> https://accounts.google.com/o/oauth2/auth?access_type=offline&state=...&client_id=...&redirect_uri=...&scope=...&prompt=consent
> ```

---

## 支持的平台

| 用户说法                         | `--media-type` 参数值   | 备注                                                           |
| -------------------------------- | ----------------------- | -------------------------------------------------------------- |
| YouTube                          | `YouTube`               |                                                                |
| TikTok                           | `TikTokBusinessAccount` | ⚠️ 必须用这个值，传 `TikTok` 会跳到错误的授权页                |
| Instagram / IG                   | `Instagram`             |                                                                |
| Facebook / FB                    | `Facebook`              |                                                                |
| LinkedIn                         | `LinkedIn`              |                                                                |
| Twitter（即 X / 推特，同一平台） | `Twitter`               | Twitter 已更名为 X，前端显示为"X"，但 API 参数固定为 `Twitter` |

---

## 何时需要重新授权

以下情况需要对账号重新执行 `authorize`：

- `list-accounts --json-out` 落盘数据中 `invalidOAuthToken: true`
- `list-accounts` 显示账号状态为"异常"或"已过期"
- 发布任务失败，错误原因为 Token 失效

---

## 交叉引用

- 查看账号 Token 状态 → 参见 `references/list-accounts.md`
- 重新发布失败的任务项 → 参见 `references/task.md`
