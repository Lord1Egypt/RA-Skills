# x-post-fetcher

X (Twitter) 帖子自动获取工具 - 使用浏览器自动化抓取指定用户的推文并生成汇总报告。

## 触发方式

当用户说：
- "获取XXX的推文"
- "抓取X帖子"
- "生成XXX推文汇总"
- "XXX过去24小时推文"
- "XXX一周帖子汇总"
- 类似表达需要获取 X 用户帖子内容的场景

---

## 🔧 完整使用流程

### Step 1: 启动浏览器

使用 `browser start` 命令启动一个全新的 Chrome 浏览器：

```json
{
  "action": "start",
  "profile": "openclaw",
  "cdp": true,
  "headless": false
}
```

**返回结果示例**：
```json
{
  "ok": true,
  "targetId": "1A5FCBFF48B350CF5113674CB22B7A45",
  "pid": 6472,
  "cdpUrl": "ws://127.0.0.1:28800"
}
```

**关键返回字段**：
- `targetId`：会话ID，后续所有操作都需要用到它
- `pid`：浏览器进程ID
- `cdpUrl`：Chrome DevTools Protocol 连接地址

---

### Step 2: 打开 X 网站

使用 navigation 命令打开 x.com：

```json
{
  "action": "navigate",
  "targetId": "1A5FCBFF48B350CF5113674CB22B7A45",
  "url": "https://x.com"
}
```

**此时状态**：
- 如果未登录，会显示 X 注册/登录页面
- 如果已登录（之前使用过），会直接显示首页

---

### Step 3: 检查登录状态

获取页面快照检查是否已登录：

```json
{
  "action": "snapshot"
}
```

**已登录状态特征**：
- 页面右上角显示用户头像和用户名
- 有 "Post" 按钮可以发推

**未登录状态特征**：
- 显示 "Sign up" / "Log in" 按钮
- 页面是注册/登录表单

---

### Step 4: 手动登录（如果是首次使用）

如果未登录，需要手动完成以下步骤：

#### 4.1 点击登录按钮
```json
{
  "action": "act",
  "targetId": "1A5FCBFF48B350CF5113674CB22B7A45",
  "request": {
    "kind": "click",
    "ref": "登录按钮的ref"
  }
}
```

#### 4.2 输入用户名/邮箱
```json
{
  "action": "act",
  "request": {
    "kind": "type",
    "ref": "输入框ref",
    "text": "your_email_or_username"
  }
}
```

#### 4.3 点击下一步，然后输入密码
```json
{
  "action": "act",
  "request": {
    "kind": "type",
    "ref": "密码框ref",
    "text": "your_password"
  }
}
```

#### 4.4 可能需要验证
- X 可能会要求邮箱验证或手机验证码
- 用户需要在弹出的窗口中手动输入验证码
- 等待几秒钟让系统完成验证

**重要**：
- 由于 X 的登录流程经常变化（验证码、滑动验证等），建议让用户手动完成登录
- 登录一次后，cookie 会保存在浏览器配置中
- 后续使用无需再登录

---

### Step 5: 登录成功后，开始抓取帖子

登录状态确认后，就可以开始抓取目标用户的帖子了：

1. 导航到目标用户主页：`https://x.com/{username}`
2. 按 End 键滚动加载更多内容
3. 使用 snapshot 获取页面内容
4. 解析推文数据
5. 生成报告并保存

（详见下文"核心流程"部分）

---

## 核心流程

### Step 1: 导航到目标用户主页

使用 browser 工具导航：
```json
{
  "action": "navigate",
  "url": "https://x.com/{username}"
}
```

**注意**：username 不带 @ 符号

### Step 2: 加载更多推文

由于 X 页面默认只显示部分推文，需要滚动加载更多：

1. **按 End 键** - 跳到页面底部触发加载
   ```json
   {
     "action": "act",
     "request": {"key": "End", "kind": "press"}
   }
   ```

2. **重复多次** - 每次按 End 后 snapshot 检查是否加载新内容
   - 一般需要 3-5 次滚动才能获取足够数据

3. **检查时间范围** - 对比推文时间是否符合用户需求（如"过去24小时"）

### Step 3: 抓取页面内容

使用 snapshot 获取当前可见的所有推文：
```json
{
  "action": "snapshot"
}
```

### Step 4: 解析推文数据

从 snapshot 结果中提取每条推文的：
- **时间**：如 "9 hours ago", "Apr 11", "Mar 25"
- **内容**：推文文本内容
- **类型**：原创 vs 转推 (reposted)
- **互动数据**：
  - replies（回复数）
  - reposts（转推数）
  - likes（点赞数）
  - views（阅读量）- 可能在 analytics 链接中

### Step 5: 生成汇总报告

按指定格式生成 Markdown 报告：

```markdown
# {用户名} 推文汇总 ({时间范围})

> 数据来源：x.com/{username} | 采集时间：{时间}

---

## 📊 统计概览

| 类型 | 数量 |
|------|------|
| 原创推文 | X |
| 转推 | X |
| 总计 | X |

---

## 🐦 推文详情（按发布时间）

### 1️⃣ {时间} - {类型}
> {内容摘要}

📈 {回复}回复 | {转推}转推 | {赞}赞 | {阅读}阅读

---

## 📈 话题标签

#{话题1} #{话题2} ...

---

## 💡 总结

{关键洞察}
```

### Step 6: 保存文件

使用 write 工具保存报告到工作目录。

## 关键技巧

### 1. 登录状态检查

本技能使用**独立浏览器会话**，不访问用户现有 Chrome profile：

```json
{
  "action": "start",
  "profile": "openclaw",
  "cdp": true,
  "headless": false
}
```

**安全设计**：
- 使用隔离的浏览器实例，与用户日常 Chrome 完全分离
- 用户需要在独立浏览器中手动登录 X/Twitter
- 登录后 cookie 保存在隔离环境中，可复用于后续操作

这种方式确保技能无法访问用户现有浏览器中的任何数据。

### 2. 滚动加载策略
- X 是懒加载，每次滚动大约加载 5-10 条推文
- 需要获取"过去24小时"或"一周"数据时要滚动更多次
- 可通过时间筛选判断是否需要继续滚动

### 3. 时间识别
- X 时间格式：`X hours ago`（今天）, `Apr XX`（今年其他月份）, `Mar XX`（更早）
- 需要计算是否符合用户要求的时间范围

### 4. 互动数据提取
- 数字可能简化显示：如 "1.2K", "6.2M"
- 需要还原为实际数字

### 5. 浏览器会话保持
- targetId 会在多次操作中保持
- 无需每次都重新登录

## 依赖工具

- `browser` - 浏览器控制（navigate, snapshot, act）
- `write` - 文件写入

## 注意事项

1. **隐私合规**：只抓取公开可见的推文
2. **频率限制**：避免短时间内大量请求
3. **登录必要**：未登录只能看到部分内容
4. **动态内容**：X 页面是动态加载，需要等待加载完成

---

## ⚠️ 安全说明 / Security Notice

本技能使用浏览器自动化访问公开可见的 X/Twitter 内容。

This skill uses browser automation to access publicly visible X/Twitter content.

### 浏览器隔离 / Browser Isolation

本技能**强制使用独立浏览器实例**（`profile="openclaw"`），与用户日常 Chrome 完全隔离：

This skill **uses an isolated browser instance** (`profile="openclaw"`), completely separated from user's daily Chrome:

- ✅ 独立的浏览器进程和用户数据目录 / Independent browser process and user data directory
- ✅ 无法访问用户现有 Chrome 中的任何数据 / Cannot access any data from user's existing Chrome
- ✅ 用户需要在隔离环境中手动登录 X / User must manually login to X in the isolated environment
- ✅ 所有 cookies 和会话数据仅存在于隔离环境中 / All cookies and session data exist only in the isolated environment

### 隐私合规 / Privacy Compliance

- 只抓取**公开可见**的推文 / Only fetches **publicly visible** tweets
- 不访问私密账户或受保护内容 / Does not access private accounts or protected content
- 不绕过 X 的访问限制 / Does not bypass X's access restrictions
- 符合 X 平台服务条款 / Complies with X platform Terms of Service

### 数据存储 / Data Storage

- 生成的报告保存在用户本地工作目录 / Generated reports saved to user's local workspace
- 不上传到任何外部服务器 / Not uploaded to any external server
- 用户完全控制数据的去向 / User has full control over data destination

### 用户责任 / User Responsibility

使用本技能前，用户应：
- 了解浏览器自动化会访问 X.com
- 在隔离环境中完成 X 登录
- 审查生成的报告内容再分享

Before using this skill, users should:
- Understand that browser automation will access X.com
- Complete X login in the isolated environment
- Review generated report content before sharing

### 技术实现 / Technical Implementation

```
用户请求 → 启动隔离浏览器 → 访问 x.com → 手动登录 → 滚动加载 → 解析内容 → 保存本地 → 完成
              ↓
    独立浏览器实例，无法访问用户现有 Chrome 数据
```

## 示例对话

**用户**：帮我抓取 Elon Musk 最近24小时的推文

**执行**：
1. `navigate` → x.com/elonmusk
2. `act(End)` → 滚动加载
3. `snapshot` → 获取内容
4. 解析推文数据
5. 生成报告
6. 保存文件并展示

---

**Skill 版本**：1.0.2  
**创建时间**：2026-04-14  
**更新时间**：2026-04-15  
**作者**：qq虾 🦐

## 📝 更新日志 / Changelog

### v1.0.2 (2026-04-15)
- 🔒 修复安全扫描问题：改用隔离浏览器实例
- 🛡️ 移除 `profile="user"` 推荐，避免安全担忧
- 📝 修改安全声明为可验证的设计
- ✅ 通过 ClawHub 安全扫描

### v1.0.1 (2026-04-15)
- 🔒 添加完整安全说明和隐私合规声明
- 🌐 添加中英双语文档
- 📋 明确凭证要求和数据存储策略
- ✅ 声明不会执行的危险操作

### v1.0.0 (2026-04-14)
- 🎉 初始版本发布
- ✨ 支持自动抓取指定 X 用户的推文
- 📊 生成 Markdown 格式汇总报告