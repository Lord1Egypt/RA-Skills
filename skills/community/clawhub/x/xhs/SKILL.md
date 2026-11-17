---
name: xhs
description: Use this skill when publishing or managing posts on Xiaohongshu (小红书 / RED / xiaohongshu) via the official Creator Center. Triggers on requests to draft, save, or publish a note; generate titles, captions, or topic chips; reply to comments or DMs; or check creator dashboard metrics. The skill follows the language of the user's input (Chinese, English, or any locale the user supplies) — no locale is forced. Workflow is browser-automation-based; final publish always requires explicit user confirmation.
metadata:
  author: mebusw
---

# 小红书（Xiaohongshu）发布技能

通过浏览器自动化操作官方创作者中心完成全流程。

## 必读

- 主入口：`https://creator.xiaohongshu.com`
- 发布页：`https://creator.xiaohongshu.com/publish/publish?from=menu&target=image`
- 若用户未登录，请暂停并提示用户完成短信登录。
- 严禁绕过验证码、短信或风控。
- 在当前对话轮中未获得明确确认前，绝不发布。

## 语言与本地化（强制规则）

**绝不强制使用任何特定语言。** 本技能默认跟随用户在当轮对话中实际使用的语言：
- 用户写中文 → 笔记文案、标题、话题标签都用中文。
- 用户写英文 → 全部用英文，包括 chip 搜索关键词。
- 用户写其他语言 → 跟随用户的语言；如需话题标签，用该语言原文搜索。

模板与示例仅供参考语言风格参考，不应被理解为"必须用中文"或"必须用某种语言"。
若用户在多轮中切换语言，跟随用户最近一轮的语言。

## 支持的任务

- 创建笔记草稿（可带图或纯文字）
- 立即发布（仅在获得明确确认后执行）
- 保存为草稿
- 回复评论/私信
- 查看仪表盘数据（可见范围内的 7 天/30 天指标）

## 发布流程（已验证,2026-06-06）

1. 确认输入：
   - 标题（必须 ≤ 20 字）
   - 正文
   - 图片路径（图文笔记推荐;若需触发自动话题推荐则必须有图）
   - 模式：`publish_now` 或 `draft_only`
2. 打开创作者中心页面,并验证已登录的账号名。
3. 进入发布页：
   - **带图（推荐）**：选择 `target=image`,通过隐藏的 `<input type="file" multiple accept=".jpg,.jpeg,.png,.webp">` 上传。
   - **不带图**：使用 写长文 或 新的创作（注意：该模式下不会触发自动话题推荐,详见下方"话题标签格式化"一节）
4. 通过 `act:click` + `act:type` 填写标题/正文（`act:type` 必须提供 ref,不能盲打）
5. **话题标签格式化** —— 见下方专门章节
6. 提交前校验：
   - 标题非空
   - 正文非空
   - 至少格式化 1 个标签 chip（推荐,非强制）
7. 若 `draft_only`：点击保存/暂存并报告成功。
   - **注意：**"暂存离开"/"发布" 按钮由 `<xhs-publish-btn>` 自定义元素渲染，实际位于 `closed Shadow DOM` 内。外部 DOM 查询通常只能看到空的 `<xhs-publish-btn>`，无法直接定位内部的 `button.ce-btn.bg-red`。
   - 外层组件通常位于 `(x:248, y:853, w:680, h:90)`；内部两个按钮依次为“暂存离开”和“发布”，宽度约 120px，中间间距约 24px。不要固定使用旧坐标；先读取外层组件 bounding box。红色按钮中心可按公式计算：`x = host.x + (host.width - 264) / 2 + 204`，`y = host.y + 45`。确认 `submit-disabled="false"` 后，使用真实鼠标移动/按下/抬起或坐标点击该中心位置。
8. 若 `publish_now`：进行最后一轮 是/否 确认,然后发布。
9. 返回结果摘要,包含账号、标题、模式、状态。

## 话题标签格式化（已验证机制,2026-06-06）

**核心事实（取代已过时的"光标后移"建议,该建议无效）：**

1. **什么是 "chip"？** 编辑器 DOM 中已格式化的话题标签,渲染为：
   ```html
   <a class="tiptap-topic" data-topic='{"name":"xxx","id":"xxx"}' contenteditable="false">
     #xxx<span class="content-hide">[话题]#</span>
   </a>
   ```
   与真实话题 ID 绑定。在已发布笔记中点击该 chip → 跳转到话题页。

2. **chip 候选从何而来？** 小红书会在编辑器下方根据"标题 + 正文 + 图片"的语义自动生成 4-5 个"推荐话题" chip。**不会**因输入 `#`、移动光标或按方向键触发。用户正文中输入的 `#XXX` 文本仅以蓝色高亮文本形式存在,**不会**被自动格式化。

3. **触发条件：** 编辑器中同时填好标题 + 正文 + 至少一张图片后,小红书才会渲染推荐行。**写长文（无图）模式下该行不会出现。** 若需要 chip,请始终使用 图文 模式。

4. **如何等待 chip 出现：** 在最后一次 `act:type` 后,执行 `act:evaluate` 运行 `await new Promise(r => setTimeout(r, 1500))`（1.5 秒）,然后 `act:snapshot`。若在行容器（通常为 `e211`）内看到形如 `[ref=e212] "#xxx"` 的子元素,说明 chip 行已就绪。不要轮询 —— 1.5 秒足够,小红书内部已有防抖。

5. **如何点击 chip：**
   - `act:click` 某个 chip 的 ref（如 `e212`）→ chip 会被插入到正文末尾,成为格式化的 `<a class="tiptap-topic">`。
   - **每点击一次,推荐列表会刷新。** 已点击的 chip 会被新推荐替换（不是追加）。同一个 ref 不能重复使用。
   - 循环：snapshot → click → snapshot → click → ... 重复 3-5 次以累积多个 chip。
   - 每次点击都会基于新上下文（标题 + 正文 + 已点击的 chip）重新计算推荐。
   - 若用户要求更多可点击 chip，建议连续点击 4-5 个推荐话题。每次点击后必须重新 snapshot，再使用新的推荐 ref；不要复用旧 ref。
   - 可用 `document.querySelectorAll('a.tiptap-topic')` 验证结果。编辑器和右侧预览通常各渲染一份，因此 DOM 数量可能是实际 chip 数的 2 倍；检查 `innerText` 中带 `[话题]#` 的节点可统计编辑器内实际 chip。

6. **若用户想要指定 #XXX 标签（不在小红书推荐中）怎么办？**
   - 点击编辑器下方的 "话题" / "添加话题" 按钮（`e223`）→ 打开搜索弹窗。
   - 按精确名称搜索 → 小红书调用 `GET /api/store/search/topic?keyword=XXX` → 返回话题信息。
   - 选择匹配的话题 → 插入为真实 chip。
   - 这是格式化用户指定但未被自动推荐的标签的唯一可靠方式。

7. **标签推荐命中率（教练培训领域观察,2026-06-06）：**
   | 标签 | 命中？ | 原因 |
   |---|---|---|
   | `#敏捷转型` | ✅ | 纯中文组合,训练充分 |
   | `#教练对话` | ✅ | 纯中文组合,训练充分 |
   | `#Scrum教练` | ❌ | 中英混排;训练数据稀缺 |
   | **经验法则** | — | 纯中文组合 → 高命中率。中英混排 → 必须通过 "添加话题" 手动搜索。 |

8. **常见坑 —— chip 元素的 `contenteditable=false`。** 一旦插入,Backspace 在编辑器中无法删除。如需移除误点的 chip,使用 `act:evaluate` 精准地从 DOM 中移除 `<a class="tiptap-topic">` 节点,或保留并继续追加。

## 必需的发布确认

发布操作要求用户给出明确的确认意图,例如：
- "立即发布"
- "确认发布"
- "继续发布"

若用户含糊其辞（"随便"、"你看着办"）,默认进入"仅草稿"模式并说明原因。

## 失败处理

- **登录失效：** 提示用户登录,然后从当前页面继续。
- **UI 变化导致控件缺失：** 重新 snapshot,切换到功能最接近的替代按钮。
- **`<xhs-publish-btn>` 使用 closed Shadow DOM：** 元素本身可能显示 `children=0`、`innerHTML` 为空、`shadowRoot` 不可访问，但内部按钮实际存在。不要继续查找 `button.ce-btn.bg-red`，因为 closed Shadow DOM 会使选择器返回 0 个元素；也不要把外层组件中心 `(x:588, y:898)` 当作发布按钮，它可能落在两个按钮之间。应点击红色按钮中心约 `(x:660, y:898)`，点击后等待页面跳转到 `/publish/success` 并核验“发布成功”。
- **浏览器标签在操作之间被重置为 about:blank：** OpenClaw 浏览器工具偶尔会在多次工具调用之间丢失状态。规避方式：使用 `act:evaluate` 执行原子操作（在同一调用中合并 click + wait + snapshot）,而不是分开的 `act:click` + `act:snapshot`。
- **发布按钮不可用：** 保留草稿,并清晰报告需手动操作的步骤。

## 工具链说明（已验证）

- **图片生成：** 使用任何已有的文生图SKILL，或 `image_generate`工具, 或图像模（默认 MiniMax 图像模型）。。
- **图片上传路径限制：** `browser.upload` 仅接受 `/Users/jacky/.openclaw/media/inbound/` 下的文件。生成在 `/Users/jacky/.openclaw/media/tool-image-generation/...` 的图片需先 `cp` 到 inbound/ 目录。
- **`act:type` 必须提供 ref 或 selector。** 盲打（无 ref）会失败并报 `type requires ref or selector`。
- **`act:press` 配合 ref 是稳定的。** 不带 ref 偶尔会触发标签页重置。
- **`<xhs-publish-btn>` 的发布按钮位于 closed Shadow DOM：** 无法通过普通 DOM 选择器访问内部按钮；使用外层组件坐标定位红色“发布”按钮，并在点击后核验 `/publish/success` 和“发布成功”。

## 输出模板

- 动作：draft | publish | reply | metrics
- 账号：<name>
- 标题：<title>
- 模式：publish_now | draft_only
- 结果：success | partial | failed
- 详情：
  - 已插入 chip 数：<N>
  - 已格式化的用户指定标签：<list> / <未格式化 —— 需手动操作>
  - 草稿已保存：yes | no（按钮不可用,需用户手动点击）
- 下一步：
  - ...

## 参考资料

可复用的文案模板见 `references/post-templates.md`。
