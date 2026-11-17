# 双色球诚实分析 · 运维与三体协同

> 本文件供 skill 在需要"排程/协同/自检"时加载。模型 + 任务 + 程序必须作为咬合整体对待，不可孤立修改。

## 1. 三体协同模型

```
        ┌─────────────┐
        │  任务体      │  真正执行器: Windows 计划任务 SSQ_V1_Smart
        │ (排程/自动化) │  SYSTEM / 每周一三六 20:10 / 无论登录都跑
        └──────┬──────┘
               │ 调用
               ▼
        ┌─────────────┐
        │  程序体      │  ssq_run_v8.bat → ssq_smart.py --force
        │ (代码/护栏)  │  → 永久自检(18项) + 预测 + 报告
        └──────┬──────┘
               │ 产出
               ▼
        ┌─────────────┐
        │  模型体      │  预测报告 / 方法发现JSON / 随机性产物
        │ (分析产物)   │  时间戳须与当期一致
        └─────────────┘
```

**协同铁律**：
- **单一执行器** = Windows 计划任务（不是 WorkBuddy 自动化）。
- **WorkBuddy 自动化 `v8` 必须 PAUSED**：其 rrule 同为周二/四/日 20:10，若启用会与排程双触发。PAUSED = 仅展示、非执行器。
- **看门狗自动化**（每日 21:30）巡检 `LastTaskResult`，正常则简短 ✅，异常主动告警（含读最近日志结尾 / `ssq_run_alert.txt`）。
- 改代码后：确认排程指向不变 → 版本三处一致 → 跑护栏确认产物新鲜。

## 2. 版本三处同步（硬性）

当前版本 **8.9.7**。护栏第 12 项 `check_version_consistency` 校验三处标签一致，漂移即失败：

| # | 位置 | 内容 |
|---|------|------|
| 1 | `README.md` | 标题 + 版本章节（§20 二级标题 `## N. V1.0.0 ...`，正则 `^##\s*\d+\.\s*V`） |
| 2 | `ssq_run_v8.bat` | 第 3 行 `REM 双色球V1.0.0智能预测` |
| 3 | WorkBuddy 自动化 `v8` | 名称/id 中的版本标识 |

代码内当前版本声明也须对齐：`ssq_power_engine.py`（打印 + 写入 JSON 的 `version`）、`ssq_method_explorer.py`（打印 + 注释）、`ssq_auto.py`（写入预测 JSON 的 `version` 字段）。

**不要改**：`V1` / `V1.0` / `V1.0新增` 等是项目/模块代号或历史引入标记，属合理层级。

## 3. 22 项自检护栏（ssq_healthcheck_all.py）

退出码 0 = 全绿。逐项：

| # | 检查项 | 要点 |
|---|--------|------|
| 1–11 | 永久自检链路 | 数据加载/9项过滤/交叉验证/模型/报告等基础回归 |
| 12 | 版本标识一致性 | README/bat/WorkBuddy 三处均为 8.9.7，无漂移 |
| 13 | 方法发现+证伪闸门 | 常跑 `ssq_method_explorer.py`，断言 `no_edge_first_prize=True`，头条=一等奖命中 |
| 14 | 报告反遗漏闸门 | 基础 10 项 + 增强 4 项必需板块，缺即失败 |
| 15 | 数据时效性与完整性 | 最新期号 / 滞后天数(≤7) / 无异常断裂 |
| 16 | 核心函数属性测试 | `ssq_common` 5000 样本属性/差分/变质不变量 |
| 17 | 开奖随机性电池 | 10 项卡方，硬闸门=无灾难性异常(FAIL) |
| 18 | 三体协同一致性 | 排程(SYSTEM/启用/bat) ↔ 程序单入口 ↔ 自动化(v8暂停防双触发+看门狗激活) ↔ 模型产物新鲜度 |
| 19 | 根↔SKILL 产物同步 | 预测 JSON / 报告 HTML 在两副本间字节一致（`sync_products_to_peers` 自动镜像后应恒绿） |
| 20 | 根↔SKILL 离线数据同步 | `ssq_history.json` 等离线兜底数据两副本一致，防"skill 跑的是旧数据" |
| 21 | 静态未定义名闸门 | 跑 `check_undefined_names.py`，捕获 `py_compile` 看不见的 `NameError`（如函数内用了未在作用域导入的模块） |
| 22 | 排程真实运行结果动态闸门 | `LastTaskResult` 必须为 0；排程 Settings 无杀任务反模式；上次日志无中断特征；无未处理告警文件 |

**注意（第 18 项 vs 第 22 项，务必分清）**：第 18 项只查**静态配置**（已启用 / SYSTEM / bat 目标），第 22 项查**动态运行结果**。二者不可互相替代——2026-08-04 实战中第 18 项全绿，而 `LastTaskResult=267014 (SCHED_S_TASK_TERMINATED)` 显示 08/03 20:51 那次排程**开跑即被杀**，`ssq_scheduler_run.log` 只有 4 行、结尾 `^C`，整条预测流水线根本没执行。MEMORY 里写了多次"体检必须动态验证"，但这条铁律此前**从未落进代码**——静态绿 ≠ 真的跑过。

杀任务的三个反模式设置（任务以 SYSTEM 运行，**改这些必须管理员提权**，普通会话 `Set-ScheduledTask` 会返回"拒绝访问"）：

| 设置 | 危害 |
|------|------|
| `DisallowStartIfOnBatteries=true` | 笔记本电池供电时任务根本不启动 |
| `StopIfGoingOnBatteries=true` | 跑到一半切电池即被杀 |
| `IdleSettings.StopOnIdleEnd=true` | 用户一动鼠标（空闲期结束）即被杀 |

一键修复（**本机部署**）：右键 `fix_scheduler_settings.ps1` → 以管理员身份运行（脚本自检提权、打印 BEFORE/AFTER，并顺带把 `ExecutionTimeLimit` 收敛为 `PT2H`）。该 `.ps1` 属本机运维脚本，**不随 skill 发布包分发**（跨平台包按设计排除 `.bat`/`.ps1`）。

若你是自行部署、包里没有该脚本，在**管理员 PowerShell** 里粘贴以下等效命令即可：

```powershell
$t = Get-ScheduledTask -TaskName 'SSQ_V1_Smart'
$t.Settings.DisallowStartIfOnBatteries = $false
$t.Settings.StopIfGoingOnBatteries     = $false
$t.Settings.IdleSettings.StopOnIdleEnd = $false
$t.Settings.ExecutionTimeLimit         = 'PT2H'
Set-ScheduledTask -TaskName 'SSQ_V1_Smart' -Settings $t.Settings
```

若未提权，`Set-ScheduledTask` 会抛 `CimException: 拒绝访问`（任务以 SYSTEM 身份运行）。
**没有 Windows 排程部署的用户**（例如只用 `run_ssq.py` 手动跑）不受影响：`schtasks` 不可达时第 22 项自动软跳过。

**告警落盘铁律**：看门狗自动化的判定结论常停留在 `PENDING_REVIEW`/未读状态——"发现了却没人看见"等于没告警（08/03 那次看门狗其实已察觉 `^C`，但用户从未看到）。故看门狗被要求每次把结论写入 `ssq_watchdog_status.txt`（首行 `OK`/`ALERT`），异常时另写 `ssq_run_alert.txt`，由第 22 项(D) 兜底暴露。

**注意（第 1 项曾是假阳性）**：`check_syntax` 早期只 `try/except` 不看 `returncode`，而 `py_compile` 遇真语法错是**返回非零而不抛异常**，导致坏文件一路绿灯。现已改为显式判 `r.returncode != 0`。

**注意（`py_compile` 的能力边界）**：它只查**语法**，不做名字解析——函数里用了模块顶层没导入的名字（`NameError`）它一律放行，只有运行到那行才炸。第 21 项就是补这个洞（曾因 `sync_products_to_peers` 用 `glob` 但 `import glob` 只存在于另一个函数的局部作用域，把整条流水线拖成退出码 1）。

**注意**：脚本曾出现过 `check_property_tests`/`check_randomness` 被重复定义（死代码）的隐患——修改护栏时务必全量 `grep "^def check_"` 排查重复。另：`sys.stdout` 禁用 `io.TextIOWrapper` 重包裹（buffer 被 GC 关闭致 "closed file" 崩溃），改用 `sys.stdout.reconfigure(encoding='utf-8')`；JSON 字段取值先 `int()` 容错（period 可能为 str）。

## 4. 报告必需板块清单（反遗漏）

基础 10 项 + 增强 4 项（见 methodology.md §6）。最易遗漏、务必确认：
- **胆拖组合**（用户最看重）：当前 `ssq_auto.py` 接 `ssq_dantuo_optimizer.optimize_dantuo`，1胆5拖+后1胆7拖=35注 形态。**曾因 `--skip-download` 绕过增强层 + `find_valid_dantuo` 固定取前 4 拖码 bug 导致胆拖为空**，已修复（改枚举组合）。
- **各号码频率参考**（含最热/最冷组合，标注概率恒等）。
- **预测能力诚实说明** + **最终结论**（含娱乐/量力而行）。

## 5. Windows 计划任务配置（ssq_run_v8.bat + schtasks）

> ⚠️ 发布包**不含** `ssq_run_v8.bat`（SkillHub 等平台禁用 `.bat` 等可执行脚本）。下面的 bat 仅适用于**本机 Windows 部署**：若你从本仓库/工作区拿到了 bat，或自行创建（内容只需 `python run_ssq.py`），则可按下方 schtasks 命令挂定时任务；跨平台或纯发布包用户请直接 `python run_ssq.py`（已校验为单入口，功能等价）。

- 任务名 `SSQ_V1_Smart`：`schtasks /create /tn SSQ_V1_Smart /tr "绝对路径\ssq_run_v8.bat" /sc weekly /d MON,WED,SAT /st 20:10 /ru SYSTEM /rl highest`
- bat 第 10 行 `/ru SYSTEM`，确保无论登录都跑；含 WakeToRun / RestartOnFailure / StartWhenAvailable。
- bat 内 Python 路径须按本机调整（managed 或系统 Python）。
- 看门狗（WorkBuddy 自动化，每日 21:30）读 `LastTaskResult` 主动告警。

## 6. 典型工作流

1. **明天要投注前**：手动 `python run_ssq.py`（= 排程真实链路）预演，确认 EXIT=0、报告含胆拖。
2. **日常自检**：`python run_ssq.py --healthcheck` → 全部 ✅（EXIT=0）。
3. **扩充候选法**：在 `ssq_method_explorer.py` 的 `METHODS` 加新方法，跑 `--explore` 看头条是否翻转（翻转让即告警复核）。
4. **升版**：同步三处标签 + 代码内版本声明 → 重跑护栏。

## 7. 排障速查

- 护栏输出为空 / 退出码 1：先查是否某 `check_` 抛异常（如 str vs int、函数重复定义、stdout 关闭）。重跑写日志 `> hc.log 2>&1` 并 `Read` 读取，勿只看退出码。
- 报告无胆拖：确认未用 `--skip-download` 绕过增强层，且 `find_valid_dantuo` 为枚举实现。
- 排程疑似漏跑：看门狗 21:30 会告警；或 `schtasks /query /tn SSQ_V1_Smart /fo list /v`（GBK 输出）查 LastTaskResult。
