# 微信消息发送示例

## 示例 1：发送简单消息给好友

**场景**: 给好友张三发送问候消息

**命令**:
```bash
osascript scripts/wechat_automation_script.applescript "张三" "你好，今天有空吗？"
```

**预期结果**:
- 微信窗口自动激活
- 搜索并打开张三的聊天窗口
- 发送消息"你好，今天有空吗？"
- 微信窗口自动隐藏
- 终端输出: `微信消息发送完成`

---

## 示例 2：发送消息到群组

**场景**: 在工作群发送通知

**命令**:
```bash
osascript scripts/wechat_automation_script.applescript "工作群" "大家好！今天下午3点开会"
```

**预期结果**:
- 消息成功发送到"工作群"
- 群成员可以看到该消息

---

## 示例 3：发送中英文混合消息

**场景**: 给好友 Yatocala 发送中英混合消息

**命令**:
```bash
osascript scripts/wechat_automation_script.applescript "Yatocala" "hello你好"
```

**预期结果**:
- 消息"hello你好"成功发送

---

## 示例 4：发送多行消息

**场景**: 发送格式化的多行文本

**命令**:
```bash
osascript scripts/wechat_automation_script.applescript "张三" "会议通知：

时间：下午3点
地点：会议室A
主题：项目进度讨论"
```

**预期结果**:
- 消息以多行格式发送

---

## 示例 5：包含 @ 提及的群消息

**场景**: 在群里 @ 特定人员

**命令**:
```bash
osascript scripts/wechat_automation_script.applescript "项目组" "@张三 请查看最新的文档"
```

**预期结果**:
- 群消息发送成功，张三收到 @ 提醒

---

## 示例 6：发送本地图片

**场景**: 给好友发送一张截图

**命令**:
```bash
osascript scripts/wechat_automation_script.applescript "张三" "" "/Users/me/Desktop/screenshot.png"
```

**带说明文字**:
```bash
osascript scripts/wechat_automation_script.applescript "张三" "请看截图" "/Users/me/Desktop/screenshot.png"
```

**预期结果**:
- 图片通过剪贴板粘贴到聊天框并发送
- 若同时提供文字，先发送文字再发送图片

---

## 执行时间参考

| 步骤 | 延时 |
|------|------|
| 激活微信 | 2秒 |
| 打开搜索框 | 1.5秒 |
| 搜索联系人 | 2秒 |
| 选择联系人 | 1.5秒 |
| 定位输入框 | 1.3秒 |
| 粘贴消息 | 2秒 |
| 确认焦点 | 1秒 |
| 发送消息 | 1秒 |
| 确认发送 | 1秒 |
| 隐藏窗口 | 3秒 |
| **总计** | **约15秒** |
