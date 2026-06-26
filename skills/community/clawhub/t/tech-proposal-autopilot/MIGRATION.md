# 技术方案书自动写作技能 - 迁移指南

**版本**: 1.0.0  
**适用**: OpenClaw v0.8+

## 快速迁移（5分钟）

### 第一步：复制技能文件

```bash
# 从源实例复制到目标实例
SOURCE=~/.openclaw/workspace/skills/tech-proposal-autopilot
TARGET=/path/to/other-openclaw/workspace/skills/tech-proposal-autopilot

cp -r "$SOURCE" "$TARGET"
```

### 第二步：配置智能体

复制或创建以下智能体配置：

```bash
# 智能体目录
AGENTS_DIR=~/.openclaw/agents

# 需要的智能体
- milo   # 架构设计、技术深度
- josh   # 政策分析、安全保障
- dev    # 技术实现、系统集成
- marketing  # 商业分析、投资估算
```

**最小配置**（如果没有这些智能体）：

```bash
# 创建 milo 智能体
mkdir -p ~/.openclaw/agents/milo
cat > ~/.openclaw/agents/milo/IDENTITY.md << 'EOF'
# Milo - 架构设计师
擅长：系统架构设计、技术方案深度分析、AI系统设计
EOF

# 其他智能体类似创建...
```

### 第三步：配置自动续作

**方式 A：Cron 定时检查（推荐）**

在 OpenClaw 配置中添加 Cron 任务：

```json
{
  "name": "tech-proposal-auto-continue",
  "schedule": { "kind": "every", "everyMs": 300000 },
  "payload": {
    "kind": "agentTurn",
    "message": "检查未完成的技术方案书项目并自动续作。详见技能文档：skills/tech-proposal-autopilot/SKILL.md"
  },
  "sessionTarget": "isolated"
}
```

**方式 B：心跳检查**

在 HEARTBEAT.md 中添加：

```markdown
- [x] **技术方案书项目检查**
  - 扫描 projects/*/progress.json
  - 检查 status="in_progress" 且 autoContinue=true
  - 自动续作未完成项目
```

### 第四步：验证安装

```bash
# 运行续作执行器（测试模式）
node ~/.openclaw/workspace/skills/tech-proposal-autopilot/continue-executor.js --dry-run

# 应该输出：检查完成，无需续作的项目
```

---

## 完整迁移检查清单

### ✅ 必需文件

| 文件 | 位置 | 用途 |
|------|------|------|
| SKILL.md | skills/tech-proposal-autopilot/ | 主技能文档 |
| trigger-continue.js | skills/tech-proposal-autopilot/ | 续作触发器 |
| continue-executor.js | skills/tech-proposal-autopilot/ | 续作执行器 |
| MIGRATION.md | skills/tech-proposal-autopilot/ | 本迁移指南 |

### ✅ 必需配置

| 配置项 | 位置 | 说明 |
|--------|------|------|
| 4个智能体 | ~/.openclaw/agents/ | milo, josh, dev, marketing |
| projects 目录 | workspace/projects/ | 存放项目文件 |
| Cron 或心跳 | 配置文件 | 自动续作触发 |

### ✅ 可选配置

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| 续作检查间隔 | 5分钟 | Cron everyMs |
| 超时阈值 | 30分钟 | 无更新视为超时 |
| 上下文警告阈值 | 70% | 触发续作准备 |

### ✅ 模型要求

| 要求 | 说明 |
|------|------|
| 长上下文支持 | 建议 50K+ tokens |
| 推荐 | GLM-5、Gemini 2.5、DeepSeek |

---

## 核心文件结构

迁移完成后，目标实例应有以下结构：

```
~/.openclaw/
├── agents/
│   ├── milo/
│   │   └── IDENTITY.md
│   ├── josh/
│   │   └── IDENTITY.md
│   ├── dev/
│   │   └── IDENTITY.md
│   └── marketing/
│       └── IDENTITY.md
│
├── workspace/
│   ├── skills/
│   │   └── tech-proposal-autopilot/
│   │       ├── SKILL.md
│   │       ├── trigger-continue.js
│   │       ├── continue-executor.js
│   │       └── MIGRATION.md
│   │
│   ├── projects/
│   │   └── (项目目录)
│   │
│   └── HEARTBEAT.md (已更新)
│
└── (配置文件已包含 Cron 任务)
```

---

## 使用方法

### 启动新项目

在 OpenClaw 中输入：

```
请使用技术方案书自动写作技能，为"XXX项目"生成技术方案书。

要求：
- 规模：约30万字，18个章节
- 参考资料：[附上参考资料]

章节大纲：
1. 项目概述与发展背景
2. 政策环境与市场分析
...
```

### 监控进度

```
查看当前技术方案书项目进度
```

### 手动续作（如需要）

```
继续执行技术方案书项目
```

---

## 验证步骤

### 1. 文件检查

```bash
# 检查技能文件
ls ~/.openclaw/workspace/skills/tech-proposal-autopilot/
# 应该看到：SKILL.md, trigger-continue.js, continue-executor.js, MIGRATION.md

# 检查智能体
ls ~/.openclaw/agents/
# 应该看到：milo, josh, dev, marketing (至少)
```

### 2. Cron 检查

```bash
# 检查 Cron 任务
openclaw cron list
# 应该看到 tech-proposal-auto-continue 任务
```

### 3. 测试续作执行器

```bash
node ~/.openclaw/workspace/skills/tech-proposal-autopilot/continue-executor.js --dry-run
# 应该输出：检查完成，无需续作的项目
```

### 4. 创建测试项目

```
创建一个测试技术方案书项目：
- 项目名：测试项目
- 规模：3章，约5000字
- 大纲：
  1. 项目概述
  2. 技术方案
  3. 实施计划
```

检查是否正常生成章节。

---

## 常见问题

### Q: 没有智能体配置怎么办？

**A**: 可以使用最小配置，创建简单的 IDENTITY.md 文件：

```bash
mkdir -p ~/.openclaw/agents/{milo,josh,dev,marketing}

echo "擅长架构设计和AI系统" > ~/.openclaw/agents/milo/IDENTITY.md
echo "擅长政策分析和安全保障" > ~/.openclaw/agents/josh/IDENTITY.md
echo "擅长技术实现和系统集成" > ~/.openclaw/agents/dev/IDENTITY.md
echo "擅长商业分析和投资估算" > ~/.openclaw/agents/marketing/IDENTITY.md
```

### Q: 只有一个智能体怎么办？

**A**: 可以让所有章节都使用主会话生成。修改自动分配逻辑：

```javascript
// 所有章节都用主会话
function assignAgent(chapter) {
  return 'main';  // 或当前智能体名称
}
```

### Q: 不想用 Cron 怎么办？

**A**: 可以只用心跳检查。在 HEARTBEAT.md 中添加检查逻辑，每次用户交互时都会检查。

### Q: 上下文超限后还是需要手动续作？

**A**: 检查以下配置：

1. Cron 任务是否正确配置
2. trigger-continue.js 是否可执行
3. 项目 progress.json 中 autoContinue 是否为 true

### Q: 如何调整续作检查频率？

**A**: 修改 Cron 配置：

```json
{
  "schedule": { 
    "kind": "every", 
    "everyMs": 60000  // 改为1分钟检查一次
  }
}
```

### Q: 模型不支持长上下文怎么办？

**A**: 减少每章目标字数，增加章节数：

```
原来：10章，每章3万字
改为：15章，每章2万字
```

---

## 升级指南

### 从旧版本升级

如果之前有 `tech-proposal-writer` 技能：

```bash
# 备份旧技能
mv ~/.openclaw/workspace/skills/tech-proposal-writer \
   ~/.openclaw/workspace/skills/tech-proposal-writer.bak

# 复制新技能
cp -r /path/to/tech-proposal-autopilot \
      ~/.openclaw/workspace/skills/
```

### 版本兼容性

| 技能版本 | OpenClaw 版本 | Node 版本 |
|---------|--------------|----------|
| 1.0.0 | v0.8+ | v18+ |

---

## 技术支持

### 文档位置

- 主技能文档：`skills/tech-proposal-autopilot/SKILL.md`
- 本迁移指南：`skills/tech-proposal-autopilot/MIGRATION.md`
- OpenClaw 文档：https://docs.openclaw.ai

### 日志位置

```
~/.openclaw/logs/tech-proposal-monitor.log
projects/{project-name}/logs/
```

### 调试命令

```bash
# 查看续作日志
tail -f ~/.openclaw/logs/tech-proposal-monitor.log

# 测试续作执行器
node ~/.openclaw/workspace/skills/tech-proposal-autopilot/continue-executor.js --dry-run

# 手动触发续作
node ~/.openclaw/workspace/skills/tech-proposal-autopilot/trigger-continue.js \
     ~/.openclaw/workspace/projects/{project-name}
```

---

**迁移完成后，即可使用本技能实现技术方案书全自动写作！**
