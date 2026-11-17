---
name: send-doc-to-feishu
description: |
  将本地文档（Word/Excel/PDF 等）发送给飞书用户或群聊。处理飞书 IM 消息发送的完整流程、权限卡点排查与降级方案。
  当用户说"发给我""发到飞书""通过飞书发送""发给某人/某群"时触发。
---

# 飞书文档发送工作流

## 核心结论（ upfront ）

当前工具链\u003cb\u003e缺少「IM 文件上传」工具\u003c/b\u003e，导致：
- ✅ 能生成本地文件
- ✅ 能上传到\u003cb\u003e飞书云盘\u003c/b\u003e（个人空间）
- ❌ \u003cb\u003e不能直接以 IM 附件（file 消息）发送给用户\u003c/b\u003e（会报 Bot is NOT the owner of the resource）

因此，发送本地文件时必须使用\u003cb\u003e链接降级方案\u003c/b\u003e；若需纯消息内送达，优先使用「飞书云文档」（docx/sheet/bitable）。

---

## 一、完整发送流程（按文档类型）

### 类型 A：Markdown / 结构化内容
最佳路径：创建「飞书云文档」→ 发送 doc_url

```
1. 用 feishu_create_doc 创建 docx（支持全彩色 Lark Markdown）
   → 得到 doc_url
2. 用 feishu_im_user_message (text 类型) 发送 doc_url 给用户
```

优点：在线查看、可编辑、可打印、可直接改文字颜色。
缺点：无法直接以传统 Word 文件形式下载（可导出）。

---

### 类型 B：本地文件（docx / xlsx / pdf / 图片等）
次优路径：上传到飞书云盘 → 发送 Drive 文件直链

```
1. 生成本地文件（python-docx / openpyxl / reportlab 等）
2. 用 feishu_drive_file action=upload 上传到用户云盘
   → 得到 file_token 和 url（如 https://my.feishu.cn/file/xxx）
3. 用 feishu_im_user_message (text/post 类型) 发送文件直链
```

注意：
- file_token 是\u003cb\u003e云盘文件 token\u003c/b\u003e，不能用于 IM file 消息。
- 用户点击链接即可预览/下载，体验接近附件。
- 若用户反馈"只看到链接文字"，告知其「复制链接到浏览器打开」或「长按链接选择打开」。

---

### 类型 C：IM 原生文件附件（理论上最优，但当前不可行）

```
1. 生成本地文件
2. 调用「IM 文件上传接口」(im/v1/files) 上传临时文件
   → 得到 IM file_key
3. 用 feishu_im_user_message (msg_type=file) 发送
   → file_key=上一步的 key
```

\u003cb\u003e当前缺少步骤 2 的工具。\u003c/b\u003e 若未来添加 `feishu_im_file_upload` 工具，此路径即可打通。

---

## 二、权限与报错速查

| 报错信息 | 原因 | 处理 |
|---|---|---|
| Bot is NOT the owner of the resource | 试图用云盘 file_token 发 IM file 消息 | 改用发送链接，或改用云文档 |
| awaiting_authorization | 用户未授权或授权过期 | 提示用户点击授权卡片，重新授权后再执行 |
| invalid container_id | chat_id 格式不对 | 私聊用 open_id，群聊用 chat_id |

---

## 三、实战发送话术模板

### 发送云文档
```
彩色版文档已经生成！直接点开就能看：
https://www.feishu.cn/docx/xxxx
可在线编辑、打印，所有文字都是彩色的。
```

### 发送本地文件链接
```
Word 文件已上传到你的飞书云盘，点击下载：
https://my.feishu.cn/file/xxxx
如果显示为纯文字，请复制链接到浏览器打开即可下载。
```

### 发送群聊
```
用 feishu_im_user_message，receive_id_type=chat_id，
receive_id=oc_xxx（群 ID）即可。
```

---

## 四、待补齐的能力清单

1. **feishu_im_file_upload 工具**
   - 作用：把本地文件上传到飞书 IM 临时文件空间
   - 解决：打通「本地文件 → IM 附件」的最后一公里
   - 优先级：高

2. **feishu_doc_export 工具**
   - 作用：把云文档导出为 docx/pdf
   - 解决：让用户既能在线看，也能下载本地文件
   - 优先级：中

3. **文件转卡片消息支持**
   - 作用：用 interactive/post 消息渲染带缩略图的可点击卡片
   - 解决：提升链接形式的美观度
   - 优先级：中

---

## 五、决策树：这文件怎么发？

```
用户要求发送文件？
├─ 内容是文字/表格/结构化数据？
│  └─ YES → 创建飞书云文档（docx/sheet）→ 发 URL
│
└─ 内容是已生成的本地文件（docx/pdf/图片）？
   ├─ 用户能点开链接？
   │  └─ YES → 上传飞书云盘 → 发 drive 链接
   │
   └─ 用户要求必须像聊天附件一样直接打开？
      └─ YES → 说明当前缺少 IM 上传工具，
                建议先用云盘链接或云文档替代
```
