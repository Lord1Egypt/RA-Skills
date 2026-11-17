# 删除 ShareOne 分享链接

当用户明确要求“删除/删掉/移除”某个已有 ShareOne 分享链接本身时读取本文件。这是 owner-only 操作，删除后公开链接立即失效（软删除）。

不要把“删除链接”和“修改设置”（水印/密码/短链/评论开关，见 `update-share-settings.md`）混淆；本流程销毁整个 share。

## 0. 删除前确认（阻塞）

执行删除命令前，必须先向用户复述要删除的目标（链接/`share_id`/slug）并获得明确确认。用户确认前不要调用 `delete_share.js`。

## 1. 凭据

删除需要 owner 的 API Key。先运行 `node scripts/ensure_credentials.js`（含义见 `workflows/environment-and-credentials.md`）。没有可用凭据时不要继续。

## 2. 获取 ref

目标可以是完整链接、`/s/<ref>` 等路径、裸 `share_id` 或自定义 slug。脚本会自行取末段并同时接受 `share_id` 与 slug；HTML/文本页和二进制文件（`/pdf/`、`/ppt/`、`/word/`）通用。

## 3. 执行删除

```bash
node scripts/delete_share.js <REF>
```

成功输出 `SHARE_DELETED:<ref>`。删除是幂等的：对已删除的链接重复执行仍返回 `SHARE_DELETED`。

### 连带失效的指针（必须转达给用户）

如果有别的 ShareOne 分享把这条链接当作内容源（remote-url **指针**），它们会**一并失效**，每条打印一行：

```
POINTER_INVALIDATED:https://s.shareone.vip/s/xxx
HINT:POINTERS_INVALIDATED:2
```

出现这些行时，**必须把每条失效链接原样列给用户**，不要只说"已删除"。指针不持有内容、只缓存源的内容，源撤了它们就没有可指的东西；但**指针可能属于别人**，用户需要知道自己刚刚让哪些链接失效了，才能去知会对方。没有这些行就表示没有任何指针受影响。

## 4. 错误处理

- `ERROR:KEY_NOT_FOUND`：没有可用凭据，先按 `environment-and-credentials.md` 配置或创建 guest key。
- `HTTP 404`：链接不存在，或不属于当前 API Key（IDOR 保护）。据此提示用户核对链接归属。
- 其他 `ERROR:*` / `AUTH_FAILED`：把服务端返回的原因反馈给用户，不要静默重试。
