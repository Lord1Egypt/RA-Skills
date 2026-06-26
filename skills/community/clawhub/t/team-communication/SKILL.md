---
name: team-communication
description: 团队内部沟通技能。当需要与其他 team members（agents）沟通、协调任务、请求帮助或发送消息时使用。提供团队成员目录、sessions_send 用法和最佳实践。
---

# Team Communication

## 团队成员目录

- 🤖 **main**（小二）- 私人助理 & 团队协调
- 🎨 **designer**（美美）- 设计师
- 💻 **coder**（老张）- 资深程序员
- 🧪 **test**（玲子）- 测试专员
- 📦 **support**（小刘）- 后勤专员

## 使用 sessions_send 沟通

**基本用法：**

```bash
sessions_send(sessionKey="<session_key>", message="<你的消息>")
```

**示例：**

```bash
# 给老张发技术问题
sessions_send(sessionKey="coder", message="老张，测试发现了一个 bug，在登录页面...")

# 给小刘提需求
sessions_send(sessionKey="support", message="小刘，下周的测试环境准备好了吗？")

# 给玲子同步测试进度
sessions_send(sessionKey="test", message="玲子，新的测试用例已经写好了，请查收")
```

## 常见场景

### 1. **请求技术帮助**
```bash
sessions_send(sessionKey="coder", message="老张，我需要帮忙优化这个查询...")
```

### 2. **分配测试任务**
```bash
sessions_send(sessionKey="test", message="玲子，这个功能需要做回归测试")
```

### 3. **协调设计资源**
```bash
sessions_send(sessionKey="designer", message="美美，需要新的 UI 设计稿...")
```

### 4. **后勤支持**
```bash
sessions_send(sessionKey="support", message="小刘，需要准备一下演示环境")
```

### 5. **跨团队协调**
```bash
sessions_send(sessionKey="coder", message="老张，玲子发现的问题我看过了，需要你来修复")
sessions_send(sessionKey="test", message="玲子，老张已经在处理这个问题了")
```

## 查看在线成员

使用 `sessions_list` 查看所有在线的 sessions：

```bash
sessions_list
```

## 最佳实践

1. **明确主题** - 消息开头说明目的，例如："【紧急】Bug 修复需求"、"【同步】测试进度"
2. **提供上下文** - 包含必要的背景信息，避免来回询问
3. **使用合适的 sessionKey** - 根据任务类型选择对应的专业成员
4. **及时回复** - 收到消息后尽快回应，保持沟通流畅
5. **团队协作** - 对于需要多人参与的任务，用 sessions_send 协调各方

## 约定

- ✅ 团队内部沟通统一使用 `sessions_send`
- ✅ 不使用飞书机器人发消息给其他团队成员
- ✅ 直接通过 sessions 进行 agent 间通信
- ✅ 保持消息简洁高效

---

*这个技能确保团队成员之间的沟通高效、统一且可追溯。*