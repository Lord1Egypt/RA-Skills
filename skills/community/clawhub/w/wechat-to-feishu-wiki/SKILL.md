---
name: wechat-to-feishu-wiki
description: Fetch WeChat public-article content and save it into a user-provided Feishu Wiki location. Use when user shares mp.weixin.qq.com links and asks to archive/sync to Feishu knowledge base. Always ask for target wiki link if missing.
---

# WeChat → Feishu Wiki (Generic)

将微信公众号文章入库到飞书知识库（面向通用用户，不预设固定节点）。

## 必要输入

- 公众号文章链接（一个或多个）
- 目标飞书 Wiki 链接（必须由用户提供）

如果用户未提供 Wiki 链接：先索取，不要默认写入任何固定节点。

## 先做权限检查（分步引导）

仅在“首次使用”或“出现权限错误”时引导；若用户已确认完成，则跳过重复引导。

### 检查项

1. 飞书已开通：云文档（Doc/Docx）+ 知识库（Wiki）。
2. 若目标在群空间：已建立群聊，并将 Bot 拉入群。
3. 目标知识库/文档已给 Bot 权限（至少可编辑，必要时 full access）。
4. 参考官方排障文档：
   `https://open.feishu.cn/document/faq/trouble-shooting/how-to-add-permissions-to-app?lang=zh-CN&utm_source=chatgpt.com`

### 引导话术（建议）

- 若未完成：输出“缺失项 + 下一步操作”，暂停写入。
- 若已完成：进入抓取与写入流程，不再重复教育性提示。

## Chrome 使用检查（必须）

在需要浏览器抓取（DOM）前，先做以下检查：

1. 先尝试 `web_fetch`；仅当内容不完整/被反爬时才启用浏览器。
2. 若用户明确要求“用我的 Chrome”：优先 `browser` + `profile: "user"`。
3. 若用户提到“Chrome Relay/插件/工具栏 attach tab”：改用 `profile: "chrome-relay"`，并提醒用户点亮扩展图标（badge ON）。
4. 若无法确认用户是否在场可授权浏览器附加：先询问再继续。
5. DOM 抽取前用 `snapshot` 确认页面已加载正文（标题+段落可见），避免抓到空壳页。

## 标准执行流程

1. 解析用户给的 Wiki 链接，提取 wiki `token`。
2. `feishu_wiki.get` 校验节点可访问。
3. 抽取公众号内容：
   - 优先 `web_fetch`
   - 不完整时用 `browser` DOM 抽取（遵循上面的 Chrome 使用检查）
4. 结构化内容：标题、来源、发布时间、原文链接、正文。
5. `feishu_wiki.create` 在目标节点下创建 docx 子页面。
6. `feishu_doc.write` 一次性写入内容。
7. 返回新页面链接。

## 写入模板

```markdown
# {标题}

- 来源公众号：{来源}
- 发布时间：{发布时间}
- 原文链接：{URL}
- 采集方式：{web_fetch 或 Chrome DOM}

## 正文摘录（按页面可见文本整理）

{正文}
```

## 批量导入

- 多链接按顺序串行处理。
- 每条链接独立创建子页面。
- 最终汇总：成功/失败 + 对应页面链接。

## 失败处理

- 反爬导致内容缺失：切换 DOM 抽取。
- Wiki/Doc 写入失败：明确回报权限、节点不可写或网络问题。
- 禁止“假成功”回复。
