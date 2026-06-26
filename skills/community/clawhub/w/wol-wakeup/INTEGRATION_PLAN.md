# 工作流引擎集成方案

## 任务信息
- **任务 ID**: JJC-20260323-003
- **需求**: 将工作流引擎集成到 OpenClaw 消息处理流程，实现微信消息自动触发工作流

## 现状分析

### 已有代码
工作流引擎代码已完整实现在 `/root/.openclaw/workspace-zhongshu/skills/wol-wakeup/scripts/`:
- `workflow_engine.py` - 工作流引擎核心（支持多轮对话、状态保持、流程锁定、超时处理）
- `state_manager.py` - 状态管理器（会话状态存储、检索、超时检查）
- `wol_workflow.py` - WoL 工作流定义（添加/删除设备工作流）
- `message_handler.py` - 消息处理器（已实现微信消息处理逻辑）
- `wol_manager.py` - WoL 设备管理（添加、删除、列表、唤醒设备）

### OpenClaw 消息处理流程
微信消息处理链路：
```
monitor.ts (长轮询) → process-message.ts → dispatchReplyFromConfig → Agent 处理
```

关键集成点：`process-message.ts` 中的 `processOneMessage` 函数

## 集成方案

### 方案 A：Internal Hooks 集成（推荐）

OpenClaw 支持 internal hooks，可在消息到达 Agent 之前拦截处理。

**实现步骤：**

1. **创建 Hook 处理器** (`/root/.openclaw/workspace-zhongshu/skills/wol-wakeup/scripts/openclaw_hook.py`)
   - 实现 HTTP webhook 接口，接收 OpenClaw inbound 消息
   - 调用 `message_handler.py` 的 `handle_message` 函数
   - 返回处理结果（如有工作流响应则直接返回，否则返回 None 让消息继续流转）

2. **配置 OpenClaw Hooks** (修改 `/root/.openclaw/openclaw.json`)
   ```json
   {
     "hooks": {
       "enabled": true,
       "token": "<随机生成的安全 token>",
       "internal": {
         "enabled": true,
         "endpoint": "http://localhost:8765/hook"
       }
     }
   }
   ```

3. **启动 Hook 服务**
   ```bash
   python3 /root/.openclaw/workspace-zhongshu/skills/wol-wakeup/scripts/openclaw_hook.py
   ```

### 方案 B：Skill 消息预处理（备选）

在 skill 的 metadata 中声明 `requires` 和 `tools`，通过 `message` 工具接收消息后优先处理。

**优点：**
- 无需修改 OpenClaw 核心配置
- 利用现有 skill 机制

**缺点：**
- 依赖 Agent 主动调用，非完全自动
- 响应延迟较高

### 方案 C：微信插件内嵌（深度集成）

修改微信插件源码，在 `process-message.ts` 中直接调用 Python 工作流引擎。

**实现：**
```typescript
// 在 process-message.ts 的 processOneMessage 函数开头添加
const workflowResponse = await callWorkflowEngine({
  text: textBody,
  sessionId: full.from_user_id,
});

if (workflowResponse) {
  // 工作流已处理，直接回复，跳过 AI  pipeline
  await sendMessageWeixin({ to: full.from_user_id, text: workflowResponse, ... });
  return;
}
```

**优点：**
- 零延迟，原生集成
- 不依赖外部服务

**缺点：**
- 需要修改插件源码
- 需要 TypeScript/Python 互调用机制

## 推荐实施方案：方案 A（Internal Hooks）

### 理由：
1. **非侵入式** - 不修改 OpenClaw 核心代码
2. **松耦合** - 工作流引擎独立运行，易于维护
3. **低延迟** - HTTP 本地调用，响应迅速
4. **可扩展** - 支持多技能、多工作流类型

### 实施计划：

#### 第一步：创建 Hook 服务脚本
文件：`/root/.openclaw/workspace-zhongshu/skills/wol-wakeup/scripts/openclaw_hook.py`
- Flask/FastAPI HTTP 服务
- 监听 `POST /hook` 端点
- 接收 inbound 消息 JSON
- 调用 `handle_message` 处理
- 返回响应（或空响应让消息继续）

#### 第二步：配置 OpenClaw
- 生成安全 token
- 在 `openclaw.json` 中添加 hooks 配置
- 重启 OpenClaw Gateway

#### 第三步：测试验证
1. 启动 Hook 服务
2. 发送测试消息到微信
3. 验证工作流触发
4. 验证多轮对话状态保持
5. 验证非工作流消息正常流转给 Agent

#### 第四步：部署自动化
- 创建 systemd 服务或 cron 任务
- 确保 Hook 服务随 OpenClaw 启动

## 技术细节

### Hook 接口设计
```python
# OpenClaw → Hook (inbound)
POST /hook
Content-Type: application/json
Authorization: Bearer <token>

{
  "event": "inbound_message",
  "channel": "openclaw-weixin",
  "from": "user@im.wechat",
  "to": "bot@im.wechat",
  "text": "添加网络唤醒",
  "timestamp": 1234567890,
  "context_token": "xxx"
}

# Hook → OpenClaw (response)
{
  "handled": true,  # true=已处理，false=继续流转
  "response": "📝 第一步：请输入设备名称..."  # 回复文本（handled=true 时必需）
}
```

### 状态持久化
- 会话状态保存在 `~/.openclaw/wol/workflows/sessions.json`
- 设备配置保存在 `~/.openclaw/wol/devices.json`
- 支持多用户并发会话

### 超时处理
- 默认会话超时 60 秒
- 定期调用 `check_timeouts()` 清理过期会话
- 超时后自动发送提示消息

## 预期效果

用户发送消息后的处理流程：
```
用户：添加网络唤醒
  ↓
微信 → OpenClaw → Hook 服务
  ↓
工作流引擎检测到"添加网络唤醒"关键词
  ↓
启动 wol_add_device 工作流
  ↓
返回："📝 第一步：请输入设备名称..."
  ↓
Hook 返回 handled=true，OpenClaw 直接发送回复（不经过 AI）
```

多轮对话：
```
用户：书房电脑          → 工作流保存名称，返回 MAC 输入提示
用户：00:11:22:33:44:55 → 工作流保存 MAC，返回备注输入提示
用户：我的台式机        → 工作流完成，调用 add_device，返回成功消息
```

## 风险与缓解

| 风险 | 缓解措施 |
|------|----------|
| Hook 服务宕机 | 配置健康检查 + 自动重启 |
| 消息重复处理 | Hook 返回 handled=false 时消息才流转给 AI |
| 状态丢失 | 状态文件实时持久化 + 定期备份 |
| 安全漏洞 | 使用强 token 认证 + 仅监听 localhost |

## 下一步行动

1. ✅ 分析现有代码和 OpenClaw 架构（已完成）
2. ⏳ 创建 Hook 服务脚本
3. ⏳ 配置 OpenClaw hooks
4. ⏳ 测试完整流程
5. ⏳ 部署自动化

---

**方案选择**: 推荐方案 A（Internal Hooks），兼顾非侵入性和自动化程度。
**预计耗时**: 30-60 分钟完成实施和测试。
