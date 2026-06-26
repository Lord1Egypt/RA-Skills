# WoL 工作流引擎使用指南

## 📋 概述

本工作流引擎为 WoL（Wake-on-LAN）技能提供多轮对话支持，解决传统单行命令格式复杂的问题。

### 核心功能

1. **状态保持** - 记录每个会话的当前对话步骤
2. **流程锁定** - 工作流进行期间不响应其他无关消息
3. **退出机制** - 用户输入 "q" 随时退出当前流程
4. **超时处理** - 60 秒无操作自动退出并清理状态
5. **上下文记忆** - 记住上一步输入的内容（如 MAC 地址、备注等）

---

## 🚀 快速开始

### 传统模式 vs 工作流模式

#### 传统模式（单行命令）
```
用户：添加网络唤醒|00:11:22:33:44:55|书房电脑
助手：已添加设备：书房电脑 (00:11:22:33:44:55)
```

#### 工作流模式（多轮对话）
```
用户：添加网络唤醒
助手：📝 第一步：请输入设备名称（如：书房电脑）
      （输入 q 退出）

用户：书房电脑
助手：📝 第二步：请输入 MAC 地址
      格式：00:11:22:33:44:55
      （输入 q 退出）

用户：00:11:22:33:44:55
助手：📝 第三步：请输入备注信息（可选）
      直接回车可跳过
      （输入 q 退出）

用户：台式机
助手：✅ 设备添加成功！
      名称：书房电脑
      MAC: 00:11:22:33:44:55
      备注：台式机
```

---

## 📖 支持的命令

### 启动工作流

| 命令 | 说明 |
|------|------|
| `添加网络唤醒` | 启动添加设备工作流 |
| `添加设备` | 启动添加设备工作流（别名） |
| `新增设备` | 启动添加设备工作流（别名） |
| `删除设备` | 启动删除设备工作流 |
| `移除设备` | 启动删除设备工作流（别名） |

### 工作流中

| 输入 | 说明 |
|------|------|
| `q` | 退出当前工作流 |
| `quit` | 退出当前工作流（英文） |
| `退出` | 退出当前工作流（中文） |
| `取消` | 退出当前工作流 |
| 任意其他文本 | 作为当前步骤的输入 |

### 传统命令（仍然支持）

| 命令 | 说明 |
|------|------|
| `帮我开机` / `开机` | 列出设备 |
| `开机 - 设备名` | 唤醒设备 |
| `添加网络唤醒\|MAC\|备注` | 单行添加设备 |
| `列表` | 显示设备列表 |
| `删除 - 设备名` | 删除设备 |

---

## 🔧 技术架构

### 文件结构

```
wol-wakeup/
├── scripts/
│   ├── workflow_engine.py    # 工作流引擎核心
│   ├── state_manager.py      # 状态管理器
│   ├── wol_workflow.py       # WoL 工作流定义
│   ├── message_handler.py    # 消息处理器（已整合工作流）
│   ├── wol_manager.py        # WoL 设备管理
│   └── test_wol.py           # 测试脚本
├── WORKFLOW.md               # 本文档
└── SKILL.md                  # 技能说明
```

### 核心组件

#### 1. StateManager（状态管理器）
- 会话状态存储（JSON 文件）
- 超时检查
- 状态持久化

位置：`~/.openclaw/wol/workflows/sessions.json`

#### 2. WorkflowEngine（工作流引擎）
- 工作流注册
- 消息路由
- 步骤验证
- 完成回调

#### 3. WorkflowDefinition（工作流定义）
- 步骤序列
- 验证器
- 退出关键词
- 完成回调

---

## 💻 集成到 OpenClaw

### 在 OpenClaw 中使用

```python
from message_handler import handle_openclaw_message

# 处理微信消息
message_data = {
    'sender_id': 'user123',
    'text': '添加网络唤醒'
}

response = handle_openclaw_message(message_data)
print(response)
```

### 在 message 工具中调用

```bash
# 通过 OpenClaw message 工具接收消息后
python3 /path/to/wol-wakeup/scripts/message_handler.py "添加网络唤醒" "user123"
```

### 定时清理超时会话

建议设置定时任务（cron）每分钟检查超时：

```bash
# 添加到 crontab
* * * * * python3 /path/to/wol-wakeup/scripts/message_handler.py check-timeouts
```

或在消息处理时惰性检查（已内置）。

---

## 🧪 测试

### 命令行测试

```bash
# 测试添加设备工作流
cd /root/.openclaw/workspace-zhongshu/skills/wol-wakeup/scripts
python3 wol_workflow.py test-add

# 交互式测试
python3 wol_workflow.py interactive-add

# 查看活跃会话
python3 wol_workflow.py list-sessions

# 查看会话信息
python3 wol_workflow.py session-info <session_id>

# 检查超时
python3 wol_workflow.py check-timeouts
```

### 单元测试

```bash
# 测试状态管理器
python3 state_manager.py list
python3 state_manager.py info <session_id>
python3 state_manager.py clear <session_id>

# 测试工作流引擎
python3 workflow_engine.py
```

---

## 📊 状态文件示例

```json
{
  "user123": {
    "session_id": "user123",
    "workflow_type": "wol_add_device",
    "current_step": 1,
    "step_data": {
      "step_1": "书房电脑"
    },
    "created_at": 1711180800.123,
    "updated_at": 1711180810.456,
    "timeout_seconds": 60,
    "active": true
  }
}
```

---

## 🔐 安全考虑

1. **会话隔离** - 每个用户独立的会话 ID
2. **超时保护** - 防止会话永久占用
3. **输入验证** - MAC 地址格式验证
4. **退出机制** - 用户可随时中断流程

---

## 🐛 故障排除

### 问题：工作流不响应

**检查：**
1. 会话 ID 是否正确
2. 会话是否已超时
3. 工作流是否已注册

```bash
python3 wol_workflow.py list-sessions
python3 wol_workflow.py check-timeouts
```

### 问题：状态文件损坏

**解决：**
```bash
# 删除状态文件（会丢失所有活跃会话）
rm ~/.openclaw/wol/workflows/sessions.json
```

### 问题：MAC 地址验证失败

**检查格式：**
- 正确：`00:11:22:33:44:55`
- 正确：`001122334455`
- 错误：`00-11-22-33-44-5G`（包含非十六进制字符）

---

## 📝 扩展工作流

### 添加新的工作流类型

```python
from workflow_engine import WorkflowDefinition, WorkflowStep, engine

def create_custom_workflow():
    def on_complete(step_data):
        # 处理完成逻辑
        return "完成！"
    
    return WorkflowDefinition(
        workflow_type="custom_workflow",
        name="自定义工作流",
        description="描述",
        steps=[
            WorkflowStep(
                step_id=1,
                prompt="第一步提示",
                validator=lambda x: (True, x)
            ),
            # 更多步骤...
        ]
    )

engine.register_workflow(create_custom_workflow())
```

---

## 📞 支持

如有问题，请查看：
- SKILL.md - 技能总体说明
- USAGE.md - 使用示例
- 或联系开发者
