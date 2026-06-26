# 多 Agent 协作机制

## 适用场景

当多个 Agent 需要共享知识和协作时（如团队开发、多角色协作）。

---

## 一、共享记忆架构

### 方案 A：中心化共享（推荐）

```
workspace-shared/          # 共享知识库
├── TEAM_PROTOCOL.md      # 团队协议
├── COMMON_RULES.md       # 通用规则
├── memory/
│   ├── hot.md           # 团队共享 HOT 记忆
│   └── projects/        # 项目知识库
└── tasks/               # 任务看板

workspace-agent1/         # Agent 1 个人空间
├── IDENTITY.md
├── memory/hot.md        # 个人 HOT 记忆
└── ...

workspace-agent2/         # Agent 2 个人空间
├── IDENTITY.md
├── memory/hot.md
└── ...
```

**启动流程：**
```markdown
1. 读取个人 IDENTITY.md
2. 读取个人 memory/hot.md
3. 读取共享 workspace-shared/COMMON_RULES.md
4. 如果任务涉及协作，读取 workspace-shared/TEAM_PROTOCOL.md
```

---

## 二、冲突避免机制

### 问题：多个 Agent 同时写同一文件

**解决方案：文件锁 + 重试**

```bash
# scripts/safe_write.sh
LOCK_FILE="$1.lock"
MAX_RETRY=5
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRY ]; do
    if mkdir "$LOCK_FILE" 2>/dev/null; then
        # 获得锁，执行写入
        cat > "$1"
        rmdir "$LOCK_FILE"
        exit 0
    else
        # 锁被占用，等待
        sleep 1
        RETRY_COUNT=$((RETRY_COUNT + 1))
    fi
done

echo "❌ 无法获取文件锁: $1"
exit 1
```

---

## 三、Task Brief 协作格式

### 单 Agent 任务

```markdown
## 任务 ID: TB-2026-03-27-001
## Owner: Ethon
## 目标: 实现登录功能
## 标准: 
  - [ ] 支持手机号登录
  - [ ] 支持验证码验证
## 交付物: LoginViewController.m
```

### 多 Agent 协作任务

```markdown
## 任务 ID: TB-2026-03-27-002
## Owner: 组长
## 协作者: Ethon, Lily, 小明
## 目标: 实现支付功能
## 子任务:
  - [ ] Ethon: 实现支付 UI (2h)
  - [ ] Ethon: 对接支付 API (3h)
  - [ ] Lily: 测试支付流程 (1h)
  - [ ] 小明: 设计支付成功页 (1h)
## 依赖关系:
  - 小明设计 → Ethon 实现 UI
  - Ethon 实现完成 → Lily 测试
## 交付物: PaymentViewController.m + 测试报告
```

---

## 四、通信协议

### 方式 1：通过共享任务看板

```
Agent A 完成任务 → 更新 workspace-shared/tasks/TB-XXX.md
→ Agent B 定期检查 → 发现状态变化 → 开始下一步
```

### 方式 2：通过消息通道（OpenClaw）

```
Agent A: sessions_send(sessionKey="agent:ethon:main", message="登录功能已完成")
→ Agent B 收到通知 → 开始测试
```

### 方式 3：通过日志文件

```
Agent A 写入: workspace-shared/logs/2026/03/27.md
## 14:30 - Ethon 完成登录功能
- 文件: LoginViewController.m
- 状态: ✅ 已完成
- 下一步: @Lily 开始测试

Agent B 定期扫描日志 → 发现 @Lily → 开始执行
```

---

## 五、知识同步规则

| 知识类型 | 存放位置 | 同步方式 |
|---------|---------|---------|
| 团队规范 | workspace-shared/COMMON_RULES.md | 手动更新，所有 Agent 启动时读取 |
| 项目知识 | workspace-shared/memory/projects/*.md | 按需读取 |
| 个人经验 | workspace-agentX/memory/hot.md | 不同步，各自维护 |
| 任务状态 | workspace-shared/tasks/*.md | 实时更新 |

---

## 六、示例：三人协作开发支付功能

### 第一步：组长创建任务

```bash
# workspace-shared/tasks/TB-2026-03-27-002.md
## 任务 ID: TB-2026-03-27-002
## Owner: 组长
## 协作者: Ethon, Lily, 小明
## 目标: 实现支付功能
## 子任务:
  - [ ] 小明: 设计支付页面 (1h)
  - [ ] Ethon: 实现支付 UI (2h)
  - [ ] Ethon: 对接支付 API (3h)
  - [ ] Lily: 测试支付流程 (1h)
```

### 第二步：小明完成设计

```bash
# 小明更新任务状态
  - [x] 小明: 设计支付页面 (1h) ✅ 已完成
  
# 小明通知 Ethon
sessions_send(sessionKey="agent:ethon:main", 
              message="支付页面设计已完成，可以开始开发了")
```

### 第三步：Ethon 开始开发

```bash
# Ethon 收到通知 → 读取设计稿 → 开始开发
# 完成后更新任务状态
  - [x] Ethon: 实现支付 UI (2h) ✅ 已完成
  - [x] Ethon: 对接支付 API (3h) ✅ 已完成
  
# Ethon 通知 Lily
sessions_send(sessionKey="agent:lily:main", 
              message="支付功能已完成，可以开始测试了")
```

### 第四步：Lily 测试

```bash
# Lily 收到通知 → 开始测试 → 发现问题 → 通知 Ethon
sessions_send(sessionKey="agent:ethon:main", 
              message="支付测试发现问题：金额输入框没有限制小数位")

# Ethon 修复 → 通知 Lily 复测
# Lily 复测通过 → 更新任务状态
  - [x] Lily: 测试支付流程 (1h) ✅ 已完成
```

### 第五步：组长汇总

```bash
# 组长检查所有子任务完成 → 汇报用户
所有子任务已完成 ✅
- 小明设计 ✅
- Ethon 开发 ✅
- Lily 测试 ✅
```

---

## 七、最佳实践

1. **明确 Owner** — 每个任务必须有明确的负责人
2. **及时通知** — 完成后立即通知下一个协作者
3. **状态透明** — 任务状态实时更新到共享看板
4. **避免冲突** — 不同 Agent 操作不同文件，减少锁竞争
5. **定期同步** — 每天同步一次共享知识库

---

## 八、故障处理

| 问题 | 解决方案 |
|------|---------|
| Agent A 卡住 | 组长检测超时 → 重新分配任务 |
| 文件锁死锁 | 超时自动释放锁（5分钟） |
| 通信失败 | 降级到日志文件通信 |
| 知识冲突 | 以最新时间戳为准 |
