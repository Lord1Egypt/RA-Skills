# agentToAgent 配置指南（双向白名单）

> 本文档沉淀自真实踩坑经验（2026-08-29：跨 agent 通道首次开启时，
> allow 只加接收方被拒，源码校验 `isAllowed = matchesAllow(requester) && matchesAllow(target)`）。

## 1. 三层配置（缺一不可）

```json5
{
  tools: {
    sessions: {
      // "self" | "tree" | "agent" | "all"
      // 默认 "tree"：只含当前会话 + 本会话 spawn 的子会话
      visibility: "all",        // ← 跨 agent 必须 all
    },
    agentToAgent: {
      enabled: true,            // ← 默认 false，必须显式开启
      allow: ["tiantong", "xiaoguang"],  // ← 双向：发送方 + 接收方都在内
    },
  },
}
```

## 2. 核心坑：allow 必须双向

**源码校验**：`isAllowed = matchesAllow(requester) && matchesAllow(target)`

- 只把「接收方」加入 allow → 请求方不在 → **报 denied by tools.agentToAgent.allow**
- 只把「发送方」加入 allow → 目标不在 → 同样 denied
- **必须同时包含收发双方**

示例：天桐（tiantong）要编排小光（xiaoguang）：
```json5
allow: ["tiantong", "xiaoguang"]   // ✅ 双方都在
```

## 3. 最小权限原则

- allow 列表只放需要协作的 agent，不放全部（多 agent 家庭建议最小权限）
- 扩新 agent 协作时，把新 agent id 加入 allow（仍是双向）
- 配置修改用 config.patch（见 references/config_patch.md），**禁止 config.apply**

## 4. 常见错误排查

| 症状 | 原因 | 修复 |
|------|------|------|
| `Session send visibility is restricted` | visibility 默认 tree | 设 `tools.sessions.visibility = "all"` |
| `denied by tools.agentToAgent.allow` | allow 缺发送方或接收方 | 双向补齐 |
| `agentToAgent not enabled` | enabled 默认 false | 设 `enabled: true` |
| 配置改了没生效 | 未重启网关 | 改完重启 ~10s 生效；期间新任务报 GatewayDrainingError 属正常 |

## 5. 验证方法

改完配置重启后，先小成本验证再正式编排：
1. `sessions_list` 确认能看到目标 agent 的会话
2. 发一条简单测试消息确认能送达并收到回复
3. 再进入正式编排流程

## 6. 安全提示

- 跨 agent 消息 = 把内容暴露给另一个 agent 的会话 → 分发前确认用户意图（三档触发）
- 白名单是硬边界：未授权的 agent 无法被 send，技能不会绕过
