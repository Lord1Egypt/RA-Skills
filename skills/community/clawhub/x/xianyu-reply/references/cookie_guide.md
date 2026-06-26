# 闲鱼 Cookie 获取指南

## 什么是 Cookie？

Cookie 是浏览器保存的登录凭证。我们需要用它来让程序以你的身份连接闲鱼消息系统。

## 获取步骤

### Chrome / Edge 浏览器

1. **打开闲鱼网页版**
   - 访问 https://www.goofish.com
   - 如果没登录，先用支付宝/淘宝账号登录

2. **打开开发者工具**
   - 按键盘 `F12`（Windows/Linux）
   - 或按 `Cmd + Option + I`（Mac）

3. **切换到网络标签**
   - 点击顶部的「网络」或「Network」标签页
   - 如果列表是空的，按 `F5` 刷新一下页面

4. **找到 Cookie**
   - 在请求列表中随便点一个请求（优先选 `.json` 或 `XHR` 类型）
   - 在右侧找到「请求标头 / Request Headers」部分
   - 找到 `Cookie:` 这一行
   - 它的值是一长串文本，格式类似：`key1=value1; key2=value2; key3=value3`

5. **复制 Cookie**
   - 双击 Cookie 值全选，然后 `Ctrl+C`（或 `Cmd+C`）复制
   - 粘贴发给 AI 助手即可

### Safari 浏览器（Mac）

1. 先在 Safari 菜单 → 偏好设置 → 高级 → 勾选「在菜单栏中显示开发菜单」
2. 访问 https://www.goofish.com 并登录
3. 菜单栏 → 开发 → 显示 Web 检查器
4. 切到「网络」标签，刷新页面
5. 点击任意请求，找到 Cookie 字段并复制

## Cookie 格式示例

正确的 Cookie 看起来像这样（非常长的一行文本）：

```
cna=abc123; _m_h5_tk=xxx_1234567890; unb=1234567890; cookie2=abcdef; ...
```

关键字段说明：
- `unb` — 你的用户 ID（必须有）
- `_m_h5_tk` — API 认证 Token（必须有）
- `cookie2` — Session 标识
- `cna` — 设备标识

## 常见问题

### Cookie 复制了但不完整？
确保复制的是完整的一行，不要遗漏末尾部分。可以在复制前先按 `Ctrl+A` 全选 Cookie 值。

### Cookie 多久失效？
通常几天到几周不等。失效后服务会报错提示，届时重新获取即可。

### 触发了风控/滑块验证？
1. 在浏览器打开 https://www.goofish.com
2. 点击「消息」页面
3. 如果弹出滑块验证，手动完成
4. 完成后重新获取 Cookie

### 为什么需要 Cookie？
Cookie 是你的登录凭证，程序用它来：
- 连接闲鱼的 WebSocket 消息系统
- 获取商品信息
- 以你的身份发送回复

Cookie 只保存在你本地的 `~/.xianyu-agent/config.json` 文件中，不会上传到任何服务器。
