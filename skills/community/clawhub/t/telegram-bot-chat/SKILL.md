# Telegram Bot间群聊通信技能
**创建时间**: 2026-02-20 11:03 UTC+8
**技能版本**: 1.0.0
**适用场景**: Telegram群聊中多agent协同通信

name: telegram-bot-chat
version: 1.0.0
description: Telegram群聊中实现多agent之间互相通信的技术，促进协同工作效率提升
homepage: https://telegram.org
metadata: {"category":"communication","platform":"telegram","use_case":"multi_agent_coordination"}

# Telegram Bot群聊通信

实现多agent在Telegram群聊中的高效协同通信，促进协同工作效率的提升

## Skill Files

| File | URL |
|------|-----|
| **SKILL.md** (this file) | Current file |
| **SKILL.md** | Skill documentation |

**Install locally:**
```bash
# 安装到工作空间skills目录
cp -r telegram-bot-chat /root/.openclaw/workspace/skills/
```

**然后主agent需要手动执行多bot部署：**
```bash
# 主agent执行：复制skill到每个bot的工作空间
WORKSPACE_SKILLS="/root/.openclaw/workspace/skills"

# 复制workspace中所有skills到每个bot的workspace目录
for skill_dir in $WORKSPACE_SKILLS/*/; do
    if [ -d "$skill_dir" ]; then
        skill_name=$(basename "$skill_dir")
        echo "复制技能 $skill_name 到每个bot的工作空间"
        
        # 复制到workspace-2, workspace-3, workspace-4等
        for workspace_dir in /root/.openclaw/workspace*; do
            if [ "$workspace_dir" != "$WORKSPACE_SKILLS" ]; then
                mkdir -p "$workspace_dir/skills"
                cp -r "$skill_dir" "$workspace_dir/skills/"
                echo "已部署技能 $skill_name 到 $workspace_dir"
            fi
        done
    fi
done
```

**Or just read from this file!**

---

⚠️ **IMPORTANT:** 
- 确保所有bot都有完整的telegram配置
- 正确使用sessions_send和message工具参数
- 测试bot间通信是否正常工作

🔒 **关键要点:**
- 必须在正确的sessionKey格式中使用telegram和group类型
- message工具必须指定accountId使用自己的bot配置
- sessionKey必须包含bot名称、channel类型和群ID

**适用性检查:** 所有agent都可使用此技能进行多agent协同通信

## 核心问题

Telegram Bot API不会把bot发的消息投递给其他bot，所以：
- ❌ 在群里@其他bot，他们收不到消息
- ❌ bot直接艾特bot没有效果

## 解决方案：sessions_send + 正确配置

### 发送消息到其他bot

当需要与其他bot对话时，使用：

```javascript
sessions_send(
    sessionKey="agent:bot2:telegram:group:群ID",  // 正确的sessionKey
    message="群聊对话。来自:main。内容：想要bot2回复的内容..."
)
```

### 接收消息并回复

当收到其他bot通过sessions_send发来的消息时：

1. **解析消息内容**：识别这是群聊场景和消息来源
2. **使用message工具回复**：
```javascript
message(
    action="send",
    channel="telegram",
    accountId="自己的bot accountId",        // 使用自己的bot accountId
    target="群ID", // 群ID
    message="你的回复内容"
)
```

### sessionKey格式详解

```
agent:[bot名称]:telegram:group:群ID
```

示例：
- bot2在群聊：`agent:bot2:telegram:group:群ID`
- bot3在群聊：`agent:bot3:telegram:group:群ID`
- bot4在群聊：`agent:bot4:telegram:group:群ID`

### 完整工作流程

```
botA → sessions_send → botB收到 → botB回复 → OpenClaw announce → 群聊显示
```

## 关键技术要点

### 1. sessionKey必须包含
- bot名称（bot2, bot3, bot4等）
- channel类型（telegram）
- group类型和群ID

### 2. message工具必须指定
- `accountId`：使用自己的bot accountId
- `channel`：固定为"telegram"
- `target`：群ID

### 3. 配置要求
每个bot必须在`channels.telegram.accounts`中有完整配置：
- botToken
- 群聊权限
- 正确的accountId

## 实际使用示例

### 场景1：bot2叫bot3
```javascript
// 错误的做法
// @bot3 在群里（bot3收不到）

// 正确的做法
sessions_send(
    sessionKey="agent:bot3:telegram:group:群ID",
    message="bot2在群里说：bot3，过来帮忙！"
)
```

### 场景2：bot3收到并回复
```javascript
// bot3收到sessions_send后
message(
    action="send",
    channel="telegram",
    accountId="自己的bot accountId",         // 使用自己的bot accountId
    target="群ID",
    message="来了，什么事？"
)
```

## 常见错误

### ❌ 错误1：sessionKey格式不对
```javascript
// 错误的sessionKey
agent:bot2:main  // 没有channel和群信息

// 正确的sessionKey
agent:bot2:telegram:group:群ID
```

### ❌ 错误2：忘记指定accountId
```javascript
// 错误：没有accountId
message(action="send", channel="telegram", target="群ID")

// 正确：包含accountId
message(action="send", channel="telegram", accountId="自己的bot accountId", target="群ID")
```

### ❌ 错误3：没有telegram配置
- bot需要在channels.telegram.accounts中有完整配置
- 需要有对应的botToken和权限

## 部署指南

**第1步：安装到主agent工作空间**
```bash
# 安装到工作空间skills目录
cp -r telegram-bot-chat /root/.openclaw/workspace/skills/
```

**第2步：主agent手动执行多bot部署**
```bash
# 复制skill到每个bot的工作空间（主agent执行）
WORKSPACE_SKILLS="/root/.openclaw/workspace/skills"

# 复制workspace中所有skills到每个bot的workspace目录
for skill_dir in $WORKSPACE_SKILLS/*/; do
    if [ -d "$skill_dir" ]; then
        skill_name=$(basename "$skill_dir")
        echo "复制技能 $skill_name 到每个bot的工作空间"
        
        # 复制到workspace-2, workspace-3, workspace-4等
        for workspace_dir in /root/.openclaw/workspace*; do
            if [ "$workspace_dir" != "$WORKSPACE_SKILLS" ]; then
                mkdir -p "$workspace_dir/skills"
                cp -r "$skill_dir" "$workspace_dir/skills/"
                echo "已部署技能 $skill_name 到 $workspace_dir"
            fi
        done
    fi
done
```

**第3步：验证部署**
1. 确保每个bot的channels.telegram.accounts配置完整
2. 测试bot之间的通信是否正常

**多bot部署说明：**
- skill安装时只部署到主agent工作空间
- 主agent需要手动执行复制脚本
- 复制脚本会自动检测所有非main bot目录
- 复制完成后所有bot都可使用此技能进行协同通信

## 总结

通过这个技能，多个agent可以在Telegram群聊中实现高效协同通信，促进协同工作效率的提升。关键是要使用正确的sessionKey格式和message工具参数。

**检查更新:** 随时重新阅读此文件查看新功能！
