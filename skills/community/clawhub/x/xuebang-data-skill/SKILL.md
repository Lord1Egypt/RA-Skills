---
name: xuebang-data-skill
description: |
  查看学邦数据。用于登录学邦后台并读取首页今日经营数据与待办数据。
  Use this skill when the user wants to:
  - 查看学邦今日数据
  - 查看学邦数据
  - 学邦今日数据
  - 学邦数据
  - 查看校区今日经营数据
  Triggers: 学邦, 今日数据，经营数据，待办数据，校区数据
version: 1.0.1
author: local
allowed-tools:
  - browser
---

# 学邦 EDU.BOSS 今日数据查看

## 目标
登录 `https://boss.xuebangsoft.net/eduboss/`，读取首页"今日数据预览"和待办区块，并整理成简洁汇总返回。

## 凭据管理
- 这是一个可发布技能，`SKILL.md` 中不得包含任何真实账号、密码、Cookie、Token 或其他敏感信息。
- 首次使用时，如果本地未保存学邦凭据，先向用户索取：
  - 登录账号
  - 登录密码
- 获取后，将凭据写入本地私有笔记 `workspace/TOOLS.md`。
- 后续执行时，优先从 `workspace/TOOLS.md` 读取凭据；只有在缺失或用户要求更新时才再次询问。
- 如果用户明确要求"不保存"，则仅本次使用，任务结束后不在任何文件中落盘。

## 执行时机
当用户表达以下意图时直接使用本技能：
- 查看学邦今日数据
- 查看学邦今日经营数据
- 看下学邦今天数据
- 查学邦待办
- 查 EDU.BOSS 今日概览

## 站点信息
- 登录页：`https://boss.xuebangsoft.net/eduboss/`

## Browser Act 调用格式（重要！）
使用 `browser act` 时必须使用 **`request` 对象格式**：

```json
{
  "kind": "type",
  "ref": "<输入框 ref>",
  "text": "<要输入的内容>"
}
```

**常见错误和注意事项**：
- ❌ 不要使用 `type="type"` 或 `type="fill"` 作为独立参数
- ❌ 不要使用 `inputRef` 参数
- ✅ 必须使用 `request` 对象，且 `kind` 为 "type"（填写）或 "click"（点击）
- ✅ `ref` 参数在 `request` 对象内部，不是浏览器 act 的顶级参数

## 执行步骤

1. **启动浏览器**
   ```
   browser action="start"
   ```

2. **打开登录页**
   ```
   browser action="open" targetUrl="https://boss.xuebangsoft.net/eduboss/"
   ```

3. **获取页面快照**
   ```
   browser action="snapshot"
   ```
   找到以下元素的 ref：
   - 账号输入框：文本为 "请输入您的手机号码或账号"
   - 密码输入框：文本为 "请输入您的密码"
   - 登录按钮：文本为 "登 录"

4. **直接填写账号密码（关键步骤）**
   ```
   browser action="act" request={"kind": "type", "ref": "<账号输入框 ref>", "text": "{账号}"}
   browser action="act" request={"kind": "type", "ref": "<密码输入框 ref>", "text": "{密码}"}
   ```

5. **点击登录**
   ```
   browser action="act" request={"kind": "click", "ref": "<登录按钮 ref>"}
   ```

6. **等待页面跳转**
   ```
   browser action="act" request={"kind": "wait", "timeMs": 3000}
   ```

7. **处理浏览器连接中断（重要！）**
   如果看到错误提示 "gateway closed (1006 abnormal closure)"，说明浏览器连接断了：
   - 需要重启浏览器：`browser action="start"`
   - 然后重新 `snapshot` 确认页面状态
   - 如果已登录到首页，继续下一步；如果回到登录页，重新执行步骤 4-6

8. **确认首页加载**
   ```
   browser action="snapshot"
   ```
   确认页面已跳转到首页，看到左侧导航栏（前台、营销、招生等）

9. **提取今日数据**
   从快照中查找"数据预览"区块，提取：

10. **提取待办事项**
    从快照中查找待办相关区块，提取：

## 输出要求

按下面结构返回，缺失字段写"未读取到"，不要编造：

```
## 📊 今日数据预览（YYYY-MM-DD）

| 指标 | 今日 | 昨日 |
|------|------|------|
| 🧑 新增客户 | **X** | Y |
| ...

## 📋 待处理事项
| 事项 | 数量 |
|------|------|
| ...

## 📌 小结
...
```

## 约束
- 不要因为个别字段缺失就中止，先返回已拿到的数据。
- 如果登录失败，明确说明失败步骤和页面提示。
- 如果浏览器工具异常，说明是工具不可用，不要伪造结果。
- 不要在响应中复述完整密码。
- **浏览器连接中断是常见情况，需要优雅地重启并继续，不要报错退出。**

## 常见问题排查

### 浏览器连接中断（gateway closed）
- **原因**：点击登录导致页面跳转，有时会中断 CDP 连接
- **解决**：立即执行 `browser action="start"` 重启浏览器，然后 `snapshot` 确认状态

### 填写账号密码失败
- **原因**：使用了错误的参数格式
- **解决**：确保使用 `request` 对象格式，`kind` 为 "type"，`ref` 在对象内部

### 找不到输入框
- **原因**：页面结构变化或 ref 过期
- **解决**：重新执行 `snapshot` 获取最新 ref

---
