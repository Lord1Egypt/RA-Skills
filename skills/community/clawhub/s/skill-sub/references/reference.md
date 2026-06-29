# skill-sub 参考手册

> 本文档是 SKILL.md 的渐进式补充，包含完整 CLI 速查、脚本 API、存储格式。

---

## CLI 速查

```bash
# 初始化数据目录
python {SKILL_DIR}/scripts/chain_manager.py init

# 配置
python {SKILL_DIR}/scripts/settings.py                          # 交互式配置（打开浏览器）
python {SKILL_DIR}/scripts/settings.py --serve-only             # Agent 模式
python {SKILL_DIR}/scripts/settings.py --get-config             # 查看配置
python {SKILL_DIR}/scripts/settings.py --save-config '<json>'   # 保存配置
python {SKILL_DIR}/scripts/chain_manager.py config              # 查看配置

# 创建调用链
python {SKILL_DIR}/scripts/chain_manager.py create --name "链名" --description "描述" --purpose "目的" --steps '[...]'

# 查询
python {SKILL_DIR}/scripts/chain_manager.py list [--tag "标签"]
python {SKILL_DIR}/scripts/chain_manager.py show --name "链名"

# 执行
python {SKILL_DIR}/scripts/chain_executor.py plan --name "链名" [-v] [--json]
python {SKILL_DIR}/scripts/chain_executor.py quick --steps '[...]' --name "临时"
python {SKILL_DIR}/scripts/chain_executor.py validate --name "链名"

# 调整
python {SKILL_DIR}/scripts/chain_manager.py add-step --name "链名" ...
python {SKILL_DIR}/scripts/chain_manager.py remove-step --name "链名" --step N
python {SKILL_DIR}/scripts/chain_manager.py update-step --name "链名" --step N [--action ...] [--milestone] [--retry-max N]
python {SKILL_DIR}/scripts/chain_manager.py rename --name "旧名" --new-name "新名"

# 删除
python {SKILL_DIR}/scripts/chain_manager.py delete --name "链名" --force
```

---

## 脚本清单

| 脚本 | 功能 |
|------|------|
| `chain_manager.py` | 调用链 CRUD（init/create/list/show/run/add-step/remove-step/update-step/rename/delete/config） |
| `chain_executor.py` | 执行引擎（plan/quick/validate）+ 里程碑分类 + 配置集成 |
| `skill_extractor.py` | 从 SKILL.md 提取关键步骤和指令名称（extract/scan） |
| `settings.py` | HTML 配置界面 + CLI 配置管理 |

---

## 存储机制

### 数据目录

```
~/.workbuddy/skills/.standardization/skill-sub/
├── config.json           # 用户配置（配置界面写入）
└── chains/               # 调用链数据
    ├── index.json        # 调用链索引
    ├── 发布流水线.json    # 每条链一个文件
    └── ...
```

### 调用链 JSON 格式

```json
{
  "name": "发布流水线",
  "description": "技能发布完整流程",
  "purpose": "一键发布技能到 SkillHub/ClawHub",
  "user_intent": "帮我打包发布这个技能",
  "tags": ["发布", "技能管理"],
  "created_at": "2026-05-21T15:00:00",
  "updated_at": "2026-05-21T19:00:00",
  "exec_count": 5,
  "steps": [
    {
      "index": 1,
      "skill_name": "skills-security-check",
      "step_name": "安全审计",
      "action": "对技能目录执行安全审计，检查敏感信息泄露",
      "skill_instruction": "security-audit",
      "depends_on": [],
      "retry_policy": {"max_retries": 3},
      "failure_mode": {"on_exhaust": "abort", "is_milestone": true}
    },
    {
      "index": 2,
      "skill_name": "(内置)",
      "step_name": "打包",
      "action": "按规范打包为 ZIP（仅含 SKILL.md、_meta.json、scripts/*.py）",
      "depends_on": [1],
      "retry_policy": {"max_retries": 3},
      "failure_mode": {"on_exhaust": "ask", "is_milestone": false}
    },
    {
      "index": 3,
      "skill_name": "git-sync",
      "step_name": "推送代码",
      "action": "推送到 Gitee 和 GitHub 仓库",
      "depends_on": [2],
      "retry_policy": {"max_retries": 3, "error_types": ["network_error", "timeout"]},
      "failure_mode": {"on_exhaust": "ask", "is_milestone": false}
    }
  ]
}
```

---

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `SKILL_SUB_HOME` / `SKILL_CHAIN_HOME` | 数据目录 | `~/.workbuddy/skills/.standardization/skill-sub/` |
| `WORKBUDDY_SKILLS_DIR` | 技能安装目录 | `~/.workbuddy/skills/` |

---

## 完整流程图

```
用户触发创建
  │
  ├─ 分析意图 → 确定需要哪些技能
  │
  ├─ 读取技能信息（skill_extractor.py scan）
  │   └─ [配置: 记忆参考=是] → 额外读取 MEMORY.md + 日志
  │
  ├─ 规划步骤（提取关键步骤 → 排列顺序 → 配置依赖）
  │
  ├─ 里程碑判断（classify_milestones 自动判断）
  │   ├─ 关键词匹配
  │   ├─ 瓶颈点检测
  │   └─ 最后一步标记
  │   └─ 展示判断依据 → 用户确认调整
  │
  ├─ 展示完整调用链 → 用户确认
  │
  └─ 命名保存
      ├─ [配置: naming_mode=auto] → AI 自动命名
      └─ [配置: naming_mode=manual] → 询问用户
```

```
用户触发执行
  │
  ├─ 生成执行计划（chain_executor.py plan）
  │
  ├─ 逐步骤执行
  │   ├─ 第一层：用 action 直接执行
  │   ├─ 失败 → 分级重试（最多 N 次，N 从配置读取）
  │   ├─ 仍失败 → 按 on_exhaust 处理
  │   │   ├─ ask → 询问用户
  │   │   ├─ skip → 跳过，继续下一步
  │   │   └─ abort → 中止整条链
  │   │
  │   └─ 里程碑步骤失败 → 强制中止（无论 on_exhaust）
  │
  └─ 汇报结果
```

---

## 权限权重说明（R-16）

> 本节说明 `skill-sub` 各操作的权限权重，便于审查时评估风险。

### 脚本权限分析

| 脚本 | 敏感信息访问 | 关键位置写入 | 网络访问 | 文件删除 | Subprocess 调用 | 权重 |
|------|--------------|--------------|----------|----------|-------------------|------|
| `chain_manager.py` | 低（读 SKILL.md） | 中（写 `chains/` 目录） | 无 | 无 | 无 | **中** |
| `chain_executor.py` | 低（读调用链） | 低（执行日志） | 无 | 无 | 中（调用其他 skill） | **中** |
| `settings.py` | 低（读配置） | 低（写 `config.json`） | 无 | 无 | 无 | **低** |
| `skill_extractor.py` | 低（读 SKILL.md） | 无 | 无 | 无 | 无 | **低** |

### 授权方式

- **低权重操作**（如查看调用链列表）：静默执行，无需授权
- **中权重操作**（如创建/更新调用链）：统一授权（批量展示风险列表）
- **高权重操作**（如删除调用链）：即时授权（执行前单独确认）

### 风险缓解

- 调用链数据存储在 `~/.workbuddy/skills/.standardization/skill-sub/chains/`，非技能核心目录
- `chain_executor.py` 调用其他 skill 时，通过标准 `Skill` 工具调用，不执行任意命令
- 配置文件中不含敏感信息（仅用户偏好配置）

