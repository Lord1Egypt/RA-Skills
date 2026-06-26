# 技术方案书自动写作 - 快速参考卡

**一页掌握核心要点**

## 🚀 5分钟快速上手

### 必需配置

```bash
# 1. 智能体（至少4个）
~/.openclaw/agents/{milo,josh,dev,marketing}/IDENTITY.md

# 2. 技能文件
~/.openclaw/workspace/skills/tech-proposal-autopilot/
├── SKILL.md              # 主文档（必读）
├── MIGRATION.md          # 迁移指南
├── trigger-continue.js   # 续作触发器
└── continue-executor.js  # 续作执行器

# 3. 自动续作（二选一）
# 方式A：Cron（推荐）
# 方式B：心跳检查
```

### 启动项目

```
请使用技术方案书自动写作技能，为"XXX项目"生成技术方案书。

要求：
- 规模：约30万字，18个章节
- 参考资料：[附上路径或URL]

章节大纲：
1. 项目概述与发展背景
2. 政策环境与市场分析
...
```

---

## 📊 核心流程

```
Phase 0: 初始化
  ├─ 提取参考资料关键点 → reference-keypoints.md
  └─ 生成大纲 → outline.md

Phase 1-N: 章节生成（每章独立会话）
  └─ spawn 智能体 → 生成 → 保存 → 更新进度

自动续作（无需人工干预）
  ├─ 上下文>70% → 创建触发文件
  └─ Cron/心跳检测 → spawn 续作会话 → 继续

Phase Final: 合并输出
  └─ 所有章节 → final.md
```

---

## 🔄 自动续作三重触发

| 触发方式 | 频率 | 条件 |
|---------|------|------|
| **心跳检查** | 用户交互时 | 用户发消息 |
| **Cron 定时** | 每5分钟 | 定时触发 |
| **主动请求** | 即时 | 上下文>70% |

**关键文件**：
- `.trigger-continue` - 触发信号
- `CONTINUE.md` - 续作指令
- `progress.json` - 进度追踪

---

## 👥 智能体分工

| 智能体 | 擅长 | 适合章节 |
|--------|------|---------|
| **milo** | 架构、AI | 系统架构、核心技术 |
| **josh** | 政策、安全 | 政策环境、安全保障 |
| **dev** | 实现、集成 | 平台开发、接口设计 |
| **marketing** | 商业、投资 | 投资估算、效益分析 |

---

## 📝 写作规范

**段落优先原则**：
- 标题最多 `###`，禁止 `####`
- 每个标题后至少1段（100-200字）
- 列表占比 < 30%

**System Prompt 片段**：
```
采用论述式写作，段落优先。标题层级不超过三级（###），每个标题后必须有实质内容段落。列表占比不超过30%。
```

---

## 📈 进度管理

**progress.json 结构**：

```json
{
  "project": "项目名称",
  "totalChapters": 18,
  "completed": ["chapter-01", "chapter-02"],
  "current": "chapter-03",
  "agents": { "chapter-03": "milo" },
  "status": "in_progress",
  "autoContinue": true,
  "lastUpdate": "2026-03-23T02:30:00Z"
}
```

---

## 🔧 常用命令

```bash
# 查看进度
查看当前技术方案书项目进度

# 手动续作
继续执行技术方案书项目

# 测试续作执行器
node ~/.openclaw/workspace/skills/tech-proposal-autopilot/continue-executor.js --dry-run

# 查看日志
tail -f ~/.openclaw/logs/tech-proposal-monitor.log
```

---

## 🚨 常见问题

| 问题 | 解决 |
|------|------|
| 上下文超限 | 自动续作接管（无需操作） |
| 智能体无响应 | 自动重试3次 |
| Cron未触发 | 检查配置 `openclaw cron list` |
| 缺少智能体 | 创建 IDENTITY.md 文件 |

---

## 📚 完整文档

- **主文档**：`skills/tech-proposal-autopilot/SKILL.md`
- **迁移指南**：`skills/tech-proposal-autopilot/MIGRATION.md`
- **本参考卡**：`skills/tech-proposal-autopilot/QUICKREF.md`

---

**阅读顺序**：本参考卡 → MIGRATION.md → SKILL.md

**迁移步骤**：复制技能文件 → 配置智能体 → 配置Cron/心跳 → 验证
