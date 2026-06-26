# Session Guardian 架构说明

## Session存储架构（符合OpenClaw设计理念）

### 核心原则
- **Workspace和Sessions分离**：符合OpenClaw官方设计
- **每个agent独立session目录**：便于管理和备份
- **集中备份到King的workspace**：便于统一管理

### 实际存储位置

#### 1. Session文件（对话记录）
```
~/.openclaw/agents/
├── main/sessions/              # King的对话记录
├── dev-lead/sessions/          # 开发团长
├── dev-ui-designer/sessions/   # UI设计师
├── dev-fullstack/sessions/     # 全栈开发
├── finance-lead/sessions/      # 金融团长
├── finance-strategist/sessions/  # 金融策略研究员
├── finance-data/sessions/      # 金融数据分析师
├── finance-risk/sessions/      # 金融风控专员
├── finance-executor/sessions/  # 金融执行专员
├── strategic-lead/sessions/    # 战略团长
├── strategy-financing/sessions/  # 融资策略师
├── strategy-product/sessions/  # 产品策略师
├── strategy-marketing/sessions/  # 市场策略师
├── strategy-business-model/sessions/  # 商业模式设计师
├── media-lead/sessions/        # 运营团长
└── track-lead/sessions/        # 安防团长
```

#### 2. 备份位置（集中管理）
```
~/.openclaw/workspace/Assets/SessionBackups/
├── incremental/              # 增量备份（每5分钟）
│   └── YYYYMMDD_HHMMSS/
├── hourly/                   # 快照（每小时）
│   └── YYYYMMDD_HH/
├── daily/                    # 智能总结（每日）
│   └── YYYY-MM-DD.md
├── collaboration/            # 协作链路记录（v2.0）
│   └── YYYY-MM-DD/
│       └── task-chains.json
└── Knowledge/                # 知识库沉淀（v2.0）
    ├── dev-lead/
    │   ├── best-practices.txt
    │   └── common-issues.txt
    └── ...
```

#### 3. Workspace（工作目录）
```
~/.openclaw/workspace/                    # King的workspace
~/.openclaw/agents/dev-lead/workspace/    # 开发团长的workspace
~/.openclaw/agents/finance-lead/workspace/  # 金融团长的workspace
...
```

### 为什么这样设计？

1. **符合OpenClaw理念**
   - Sessions不在workspace里（官方推荐）
   - Workspace用于存储"记忆"（AGENTS.md、memory/等）
   - Sessions是对话记录，单独管理

2. **便于备份管理**
   - 集中备份到King的workspace
   - 只需备份一个workspace就包含所有备份
   - 便于协作分析和知识沉淀

3. **安全性**
   - Workspace可以git备份（私有仓库）
   - Sessions备份不提交git（.gitignore排除）
   - 敏感数据隔离

## 所有agent的认知状态

### ✅ King（赛博阿昕）
- 知道Session Guardian的存在和位置
- 知道所有agent的session位置
- 知道备份系统的功能
- 可以使用所有Session Guardian命令

### ✅ 五大团长
- dev-lead（开发团长）✅
- finance-lead（金融团长）✅
- strategic-lead（战略团长）✅
- media-lead（运营团长）✅
- track-lead（安防团长）✅

**他们都知道**：
- 自己的session位置
- Session Guardian会自动备份
- 知识会自动沉淀
- 协作链路会被追踪

### ✅ TOOLS.md
- 记录了所有agent的session位置
- 记录了备份位置
- 记录了常用命令

## Session Guardian v2.0 功能

### 1. 五层防护
- 增量备份（每5分钟）
- 快照（每小时）
- 智能总结（每日）
- 健康检查（每6小时）
- 项目管理（按需）

### 2. v2.0新功能
- 协作链路追踪：追踪 King → 团长 → 成员
- 智能备份策略：固定agent（5MB）vs 临时subagent（1MB）
- 知识库沉淀：自动提取最佳实践和常见问题
- 协作健康度：量化评估协作质量（0-100分）

### 3. 自动运行
通过OpenClaw cron自动运行，无需手动干预。

## 验证清单

- [x] Sessions在正确位置（`~/.openclaw/agents/*/sessions/`）
- [x] 备份到King的workspace（`~/.openclaw/workspace/Assets/SessionBackups/`）
- [x] King知道Session Guardian
- [x] 所有团长知道session位置和备份系统
- [x] TOOLS.md记录了架构信息
- [x] .gitignore排除敏感备份
- [x] 所有v2.0功能正常工作

## 总结

✅ **架构完全符合你的军团设计**
✅ **所有agent都知道session位置和备份系统**
✅ **Session Guardian已准备就绪，可以发布**

---

创建时间：2026-03-05
版本：v2.0.0
