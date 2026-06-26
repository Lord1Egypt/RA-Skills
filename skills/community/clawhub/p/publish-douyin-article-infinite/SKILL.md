name: publish-douyin-article-infinite
description: 在抖音创作者平台发布图文文章。触发场景：发布抖音文章、抖音发文、抖音创作文章。
version: 1.0.0.0
---

# 发布抖音图文文章_无限

用于在抖音创作者平台发布图文文章，包含标题、摘要、正文、头图、话题和配乐的完整填写流程。

## 触发场景

用户说：
- "发布抖音文章"
- "发表抖音文章"
- "抖音发文"
- "发布抖音图文"
- "抖音发布文章"
- "抖音创作文章"

## 重要注意事项

⚠️ **必须先启动 OpenClaw 浏览器！**
- 所有浏览器操作前，**必须先启动 OpenClaw 托管的 Chrome**
- 使用 `browser(action=start, target="host", profile="openclaw")` 启动浏览器
- 启动后再用 `browser(action=navigate, ...)` 导航到目标 URL

⚠️ **浏览器控制核心原则：**
- `browser(action=start, target="host", profile="openclaw")` 用于启动浏览器
- `browser(action=navigate, target="host", profile="openclaw", url=...)` 用于导航页面
- **禁止使用 `profile="user"` 或 `profile="chrome-relay"`**（除非用户明确要求使用用户浏览器）
- **禁止使用 `browser(action=open, targetUrl=...)`**（会被 SSRF 策略拦截）
- **禁止硬编码 ref 值** — 每次页面加载后 ref 值会变化，必须通过快照获取当前 refs
- **使用 `type` 命令输入文本**，无需 JS evaluate

⚠️ **核心操作原则：**
- 除登录、支付、删除等核心操作外，**所有问题自己尝试解决，不指挥用户**
- 操作过程中如遇弹窗/提示，优先尝试自行关闭或确认，不凡事都问用户
- 每一步操作前先获取快照（snapshot），从快照中获取元素的 ref 值

## 操作流程

### 第零步：启动 OpenClaw 浏览器

1. 调用 `browser(action=start, target="host", profile="openclaw")` 启动浏览器
2. 若浏览器已在运行，跳过此步骤
3. 检查 `browser(action=status, target="host")` 确认状态

### 第一步：导航到发文页面

1. 导航到：`https://creator.douyin.com/creator-micro/content/upload?default-tab=5`
2. 等待页面加载完成（可使用 `loadState="networkidle"`）
3. 获取页面快照，找到并点击**"我要发文"**按钮

### 第二步：填写标题

1. 获取快照，找到标题输入框的 ref
2. 使用 `type` 命令输入文章标题

### 第三步：填写摘要

1. 从快照中找到摘要输入框的 ref
2. 使用 `type` 命令输入摘要内容（摘要由正文生成，字符数小于30）

### 第四步：填写正文

1. 从快照中找到正文输入框的 ref
2. 使用 `type` 命令输入正文内容

### 第五步：设置文章头图

1. 点击**"AI配图"**按钮，进入 AI 生成封面流程
2. 输入封面描述，点击"开始创作"
3. 等待图片生成，从生成的图片中选择一张作为文章头图

### 第六步：添加话题

1. 点击**"点击添加话题"**按钮，打开话题添加窗口
2. 在弹出的话题添加窗口中，在搜索框输入**第一个话题**名称
3. 等待下拉框弹出，点击下拉框中的**同名话题**确认选中
4. 重复上述步骤，依次添加剩余4个话题（共5个话题）
5. 5个话题全部添加完毕后，点击**"确认添加"**按钮关闭弹出窗口

### 第七步：选择配乐

1. 点击**"选择音乐"**按钮，打开音乐选择窗口
2. 在推荐音乐列表中，将鼠标移动到**第一首音乐**上
3. 点击**"使用"**按钮，确认使用该音乐

### 第八步：暂存离开

1. 找到并点击**"暂存离开"**按钮，退出任务，等待用户自己检查，等待用户自己点击“发布”按钮。
2. **⚠️ 重要：点击"暂存离开"而不是"发布"，不要点击“发布”按钮** — 这样可以将文章保存为草稿

## 关键元素参考

| 元素 | 描述 | 操作方式 |
|------|------|---------|
| 发文页面URL | https://creator.douyin.com/creator-micro/content/upload?default-tab=5 | navigate 导航 |
| 我要发文按钮 | 进入图文发布模式 | click + ref |
| 标题输入框 | 文章标题 | type 命令输入 |
| 摘要输入框 | 文章摘要（<30字） | type 命令输入 |
| 正文输入框 | 文章正文内容 | type 命令输入 |
| AI配图 | AI生成封面图 | click + ref → 生成 → 选择 |
| 点击添加话题 | 打开话题添加窗口 | click + ref |
| 话题搜索框 | 输入话题名称 | type 命令输入 |
| 确认添加 | 关闭话题窗口 | click + ref |
| 选择音乐 | 打开音乐选择窗口 | click + ref |
| 推荐音乐第一首 | 推荐列表第一首 | hover → 点击"使用" |
| 暂存离开 | 保存草稿并退出任务 | click + ref |

## 技术要点总结

1. **先启动浏览器** — 使用 `browser(action=start, target="host", profile="openclaw")`
2. **用 navigate 导航** — `browser(action=navigate, target="host", profile="openclaw", url=...)`
3. **每步先快照获取 ref** — 禁止硬编码，必须实时从快照获取
4. **type 命令输入文本** — 直接使用 type 命令在输入框中输入内容
5. **话题添加需逐个确认** — 每个话题输入后，在下拉框中点击同名话题确认，然后再添加下一个
6. **音乐选择 hover 后使用** — 鼠标悬停到推荐音乐上后点击"使用"按钮
7. **暂存离开而不是发布** — 最后点击"暂存离开"按钮保存为草稿，退出任务，由用户自行发布

## 常见失败原因

- ❌ 浏览器未启动就调用 navigate → 应先 start
- ❌ 硬编码 ref 值 → 每次页面刷新 ref 会变化，必须快照获取
- ❌ 使用 profile="user" → 应使用 profile="openclaw"
- ❌ 使用 browser(action=open) → 应使用 browser(action=navigate)
- ❌ 使用 evaluate 执行 JS → 应使用 type 命令直接输入
- ❌ 话题添加跳过下拉框确认 → 必须在下拉框中点击同名话题确认
- ❌ 点击"发布"而不是"暂存离开" → 应点击"暂存离开"保存为草稿
