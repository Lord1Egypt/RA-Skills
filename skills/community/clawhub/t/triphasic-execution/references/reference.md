# reference.md — CLI 命令速查、进度文件、问题记录、数据目录、安装

> 本文件包含 triphasic-execution 的完整命令参考和配置说明，供需要时加载。

---

## 临时进度文件机制

> **[MANDATORY]** 违反 F-03/F-07/F-09 属于严重违规。

### 核心原理

```
任务规划确认
  └─→ [MANDATORY] 创建临时进度文件（init）
         │
         ├─ 步骤1 ADVANCE 后 → [MANDATORY] 更新文件（update）
         ├─ 步骤2 ADVANCE 后 → [MANDATORY] 更新文件（update）
         │   ...
         └─ 任务完成 → [MANDATORY] 删除进度文件（complete）
             中断/异常 → 保留文件，下次 resume 恢复
```

### AI 调用时机（[MANDATORY]）

| 时机 | 必须调用的命令 |
|------|----------------|
| 任务规划确认后 | `init` |
| 每个步骤 ADVANCE 后 | `update --step N --status success/failed --review "..." --advance "..."` |
| 任务全部完成后 | `complete` |
| 用户说"继续"、"恢复" | `resume` |
| 用户说"取消任务"、"停止" | `abort --reason "..."` |

### 命令速查

```bash
# [MANDATORY] 初始化（任务规划确认后立即调用）
python {SKILL_DIR}/scripts/task_progress.py init \
  --task "任务名" \
  --purpose "任务目的" \
  --requirements "具体要求" \
  --risks "潜在风险" \
  --steps '[{"description":"步骤描述","purpose":"步骤目的","tool":"工具名"}]'

# [MANDATORY] 更新步骤状态（每步 ADVANCE 后调用）
python {SKILL_DIR}/scripts/task_progress.py update \
  --task "任务名" \
  --step 1 \
  --status success \
  --review "审查结论" \
  --advance "推进决策"

# 恢复中断任务
python {SKILL_DIR}/scripts/task_progress.py resume --task "任务名"

# [MANDATORY] 完成任务（删除进度文件）
python {SKILL_DIR}/scripts/task_progress.py complete --task "任务名"

# 中止任务
python {SKILL_DIR}/scripts/task_progress.py abort --task "任务名" --reason "原因"

# 列出活跃任务
python {SKILL_DIR}/scripts/task_progress.py list

# 清理已完成/中止文件
python {SKILL_DIR}/scripts/task_progress.py clean
```

---

## 问题、风险、经验记录

### [MANDATORY] 强制记录规则

> 每次任务执行完成后，**[MANDATORY]** AI 必须执行以下步骤（除非用户明确选择"2.跳过记录"）：
> 1. 回顾执行过程，识别问题 → 调用 `add`
> 2. 回顾执行过程，识别风险 → 调用 `add-risk`
> 3. 执行完成后 → 调用 `merge-to-lessons`

### 问题记录

```bash
python {SKILL_DIR}/scripts/problem_logger.py add \
  --scene "API 测试" \
  --symptom "HTTP 503" \
  --cause "服务端限流" \
  --solution "增加重试机制" \
  --task "用户头像接口"
```

### 风险记录

```bash
python {SKILL_DIR}/scripts/problem_logger.py add-risk \
  --description "网络不稳定可能导致 API 调用失败" \
  --impact "用户体验下降" \
  --mitigation "增加重试机制和降级策略" \
  --task "用户头像接口"
```

### 经验积累

```bash
python {SKILL_DIR}/scripts/problem_logger.py merge-to-lessons
```

---

## 配置界面

安装技能后首次运行 `install.py` 时，会自动弹出 HTML 配置界面（系统默认浏览器），引导用户完成初始配置。

| 配置项 | 选项 | 说明 |
|---|---|---|
| **默认调用方式** | 调用模式（按需） / 全局模式 | 控制技能激活方式 |
| **记录文件路径** | TRIPHASIC_HOME 等 | 未自定义时使用默认值 |
| **任务规划确认** | 询问确认后再执行 / 直接执行 | 控制 Agent 是否请求确认 |

**当前配置**：
> **调用方式**：🟢 按需调用模式（默认）
> **数据目录**：`skills/.standardization/triphasic-execution/data/`
> **任务规划确认**：询问确认后再执行

呼出配置界面：向 Agent 发送"打开 triphasic 配置"，或运行 `python {SKILL_DIR}/scripts/settings.py`

---

## 双模式设计

| 维度 | 按需调用模式（默认） | 全局自动模式（可选） |
|---|---|---|
| **触发条件** | 用户主动加载技能 | 配置 `mode: global` + 启动 daemon |
| **记录行为** | 调用时才记录三步框架 | 所有任务自动应用三步框架 |
| **后台守护** | 不启动 daemon | `problem_daemon.py` 持续监控 |
| **适用场景** | 日常简单任务、跨平台协作 | 复杂多步骤项目、长期维护 |

---

## 数据目录

`TRIPHASIC_HOME` 默认指向 `skills/.standardization/triphasic-execution/`。

| 路径 | 说明 | 规范分类 |
|------|------|---------|
| `TRIPHASIC_HOME/config.json` | 用户配置 | 根目录 |
| `TRIPHASIC_HOME/default_config.json` | 默认配置模板 | 根目录 |
| `TRIPHASIC_HOME/data/active/` | 活跃进度文件 | data/ |
| `TRIPHASIC_HOME/data/completed/` | 已完成归档 | data/ |
| `TRIPHASIC_HOME/output/PROBLEMS.md` | 问题清单 | output/ |
| `TRIPHASIC_HOME/output/RISKS.md` | 风险手册 | output/ |
| `TRIPHASIC_HOME/output/LESSONS_REGISTER.md` | 经验教训登记册 | output/ |
| `TRIPHASIC_HOME/logs/problems.jsonl` | 问题日志 | logs/ |
| `TRIPHASIC_HOME/logs/risks.jsonl` | 风险日志 | logs/ |
| `TRIPHASIC_HOME/temp/` | 临时文件 | temp/ |
| `TRIPHASIC_HOME/backup/` | 操作备份 | backup/ |
| `TRIPHASIC_HOME/cache/` | 缓存 | cache/ |
| `TRIPHASIC_HOME/state/` | 状态文件 | state/ |
| `TRIPHASIC_HOME/.exec_output_pipe.txt` | exec 输出管道 | 根目录（运行期标志） |

---

## 安装

```bash
python install.py                           # 基础安装
python install.py --mode global            # 全局自动模式
python install.py --target ~/.workbuddy/skills/  # 指定安装路径
python install.py --home ~/.myagent/triphasic/   # 指定数据目录
python install.py --uninstall              # 卸载
```

---

## 脚本清单

| 脚本 | 功能 |
|------|------|
| `install.py` | 安装/卸载 |
| `settings.py` | HTML 配置界面 |
| `problem_logger.py` | 问题/风险 CRUD + 合并登记册 |
| `exec_wrapper.py` | 命令执行拦截器 |
| `problem_daemon.py` | 后台监控守护进程（仅全局模式） |
| `lessons_register.py` | 登记册管理 |
| `cron_helper.py` | 定时任务钩子 |
| `task_progress.py` | 临时进度文件管理（init/update/resume/complete/abort/clean） |

所有脚本零外部依赖，仅使用 Python 标准库。跨平台支持 Windows/Linux/macOS。

---

## 权限权重说明（R-16）

本技能各操作的权限权重评估如下（由 `skill-standardization/scripts/permission_checker.py` 计算）：

| 脚本 | 操作类型 | 权限权重 | 风险等级 | 说明 |
|------|---------|---------|---------|------|
| `task_progress.py` | 读写 `.active_tasks/*.json` | 中低 | 🟡 | 仅读写本地进度文件，无外部命令调用 |
| `problem_logger.py` | 读写 `.problem_logs/*.jsonl`、合并登记册 | 中 | 🟡 | 本地日志文件写入，无网络/外部命令 |
| `settings.py` | 读/写 `config.json`，启动 HTTP 服务 | 中 | 🟡 | 本地配置读写，HTTP 仅本地 `localhost` |
| `install.py` | 创建目录、写配置文件、注册守护进程 | 中高 | 🟠 | 涉及目录创建和配置写入，无系统级操作 |
| `problem_daemon.py` | 后台守护进程，监控任务执行 | 中 | 🟡 | 仅本地监控，无外部访问 |
| `exec_wrapper.py` | 拦截命令执行，记录问题 | 中高 | 🟠 | 涉及命令执行拦截，但仅记录不更新 |
| `lessons_register.py` | 读写 `LESSONS_REGISTER.md` | 低 | 🟢 | 仅本地文件读写 |
| `cron_helper.py` | 定时任务钩子 | 中低 | 🟡 | 仅本地定时任务管理 |

**合计权限权重**：中（所有脚本均无高风险操作）
**敏感信息访问**：无（仅本地文件读写）
**关键位置写入**：否（仅写入技能自身 `data/` 和 `.active_tasks/` 目录）
**高权限操作**：无（无需授权）

> 本技能整体风险等级：**低至中等**。所有写入操作仅限于本地用户目录，不涉及系统目录、敏感位置或网络传输。命令行拦截器（`exec_wrapper.py`）仅做记录和监控，不更新原始命令。
