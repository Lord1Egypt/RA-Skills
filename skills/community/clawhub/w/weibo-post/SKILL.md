---
name: weibo-post
description: 发微博（新浪微博）。当用户说"发微博"、"发条微博"、"发到微博"、"发一条微博"、"帮我发微博"、"发到微博"时触发。使用浏览器自动发微博。
---

# 微博发布 Skill

## 工作流程

1. **打开微博**
   ```
   browser(action=navigate, profile="openclaw", url="https://weibo.com")
   ```

2. **等待页面加载，获取快照**
   ```
   browser(action=snapshot, profile="openclaw", compact=true)
   ```
   找到发微博的文本框 `ref=e35`，以及发送按钮（初始 disabled，填入内容后变为可点击）

3. **填入微博内容**
   ```
   browser(action=act, profile="openclaw", targetId=<targetId>, ref="e35", kind="type", text=<微博内容>)
   ```
   ⚠️ 内容中换行用 `\n`，不要用真正的换行符

4. **重新获取快照，确认发送按钮可用**
   ```
   browser(action=snapshot, profile="opencloak", compact=true)
   ```
   找到发送按钮 `ref=e36`

5. **点击发送**
   ```
   browser(action=act, profile="openclaw", targetId=<targetId>, ref="e36", kind="click")
   ```

6. **验证发送成功**
   ```
   browser(action=snapshot, profile="openclaw", compact=true)
   ```
   看到"刚刚"发布的新微博即表示成功

## ⚠️ 重要：话题标签格式

**必须是 `#标签#`（前后各一个 #），不是 #标签**

✅ 正确：`#黄仁勋# #英伟达# #太空数据中心#`
❌ 错误：`#黄仁勋 #英伟达 #太空数据中心` （少了右边的 #）

## 注意事项

- 微博内容支持 emoji、话题标签
- 不支持 Markdown 格式（**粗体**等会被当作普通文本发出）
- 发之前确认内容无误，微博发出后无法编辑删除
- 如果发送按钮仍为 `disabled`，再等待一下或重新 snapshot 确认
