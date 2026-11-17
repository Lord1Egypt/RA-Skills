# weekend-self-check skill

## 用途
每周六 10:00 执行码虫周末全面自检，覆盖系统状态/Cron任务/技能体系/数据驱动层/已知问题，输出完整自检报告并发送飞书。

## 触发
- 时间：`0 10 * * 6`（周六 10:00）
- 超时：`timeoutSeconds=600`（command payload 显式超时，HOT-20260515 高风险 10 分钟）
- SIGTERM 真正可中断（v1.4）：脚本内置 signal handler + async Popen，主循环 0.5s 内检测中断，kill 子进程 + 发飞书告警 + exit 130

## 执行流程

### 第一步：系统状态核查
```bash
bash CODIS-DATA/sync.sh
python3 CODIS-DATA/read_data.py all
openclaw cron list
ls -la skills/ | tail -5 && ls skills/ | wc -l
ls memory/ && ls memory/tasks/ | wc -l && ls memory/daily-reports/ | wc -l
```

### 第二步：Cron任务状态分析
- 统计：total / ok / error / idle 数量
- 列出所有 error 状态任务
- 列出 idle 超7天的任务
- 检查重复/冲突的 cron 任务

### 第三步：技能体系全面核查
- 检查 `CODIS-DATA/state/skills-stats.json`
- 找出有反馈但无评分的技能
- 检查最近7天/超过30天未更新的技能

### 第四步：数据驱动层状态
- `case-stats.json` — 案例数/有效率
- `efficiency-stats.json` — entries数量
- `corrections-summary.json` — corrections状态
- `hot-rules.json` — HOT rules
- `data-registry.json` — registry_version

### 第五步：已知问题深度检查
- `.learnings/ERRORS.md` — 错误记录
- `.learnings/LEARNINGS.md` — 学习记录
- `corrections-summary.json` — pending状态

## 输出格式

```markdown
## 🛠 码虫周末全面自检 · YYYY-MM-DD [v1.2]

### 📊 系统状态总览
| 指标 | 数值 |
|------|------|
| 总技能数 | X |
| Cron任务(total/ok/error/idle) | X/X/X/X |
| 案例总数 | X |
| 数据Registry版本 | vXX |

### 📊 Cron任务状态
（表格：任务名/Job ID/状态/最后执行/备注）

🔴 问题任务（需要修复）：...
🟡 长时间未执行：...

### 🛠 技能体系状态
| 指标 | 数值 |
|------|------|
| 有反馈技能 | X |
| 有评分技能 | X |
| 无反馈技能 | X |
| 最近7天更新 | X |
| 超过30天未更新 | X |

⚠️ 有反馈无评分技能：...

### 📊 数据驱动层状态
（数据源/数值/状态表格）

### 📋 已知问题检查
- ERRORS.md 最新记录：...
- LEARNINGS.md 最新记录：...
- corrections 状态：total/new/active

### 🐛 下周行动项
1. ...
2. ...

---
📌 整理：码虫 🐛
🤖 模型：minimax/MiniMax-M3
📡 来源：系统状态/Cron任务/技能体系/数据驱动层
📅 日期：YYYY-MM-DD
---
🛠 技能：weekend-self-check
```

## 依赖
- `CODIS-DATA/sync.sh`
- `CODIS-DATA/read_data.py`
- `CODIS-DATA/send_feishu_report.py`
- `openclaw cron list`（系统命令）

## 版本
- v1.2：标准化尾部信息 + 五步骤结构化自检
- v1.3 (2026-07-11)：SIGTERM-safe + 真实状态解析器（ERR-20260711-001 闭环 v1）
  - 解析器：旧版依赖 ● ✓ ✗ 字符 → v1.3 按 status: 字段 fixed-width 匹配（OpenClaw 6.x 兼容）
  - SIGTERM handler：捕获系统信号 → 打诊断 + 发飞书中断告警（best-effort 5s）
  - --dry-run：验证流程，不发飞书
  - --no-send：CI 模式，跑流程不发飞书
  - 系统健康采集：内存/CPU/最近 OOM/gateway 状态全部进报告
- v1.4 (2026-07-11)：SIGTERM 真正可中断 + 异步 sync（ERR-20260711-001 闭环 v2）
  - **v1.3 缺陷**：handler 只设置 flag，主流程在 subprocess.run 同步阻塞期间 flag 无效 → 11:31 SIGTERM 时脚本 4.2s 内被外层 SIGKILL
  - **v1.4 修复**：
    - `safe_run_interruptible()`：Popen 启动子进程 + 主循环 0.5s poll `_INTERRUPTED`，检测到立即 SIGTERM 子进程 → 2s → SIGKILL
    - `_check_interrupt(label)`：统一中断检查函数，每个 step 完成后调用
    - sync.sh 改成异步调用，主循环每 0.5s 检测中断标志
    - 加 `--skip-sync`：调试用，跳过 sync 步骤
  - **cron timeoutSeconds: 540 → 600**（HOT-20260515 高风险 10 分钟对齐 SKILL.md）
  - 验证：实测 SIGTERM 后 0.5s 内响应 + 退出码 130 + 子进程无残留

## 验证命令
```bash
# 1. 语法检查
python3 -c "import ast; ast.parse(open('skills/weekend-self-check/weekend-self-check.py').read())"

# 2. Dry-run 完整流程
python3 skills/weekend-self-check/weekend-self-check.py --dry-run

# 3. SIGTERM 模拟（验证 v1.4 可中断）
(python3 -u skills/weekend-self-check/weekend-self-check.py --dry-run > /tmp/wsc.log 2>&1) &
WSC_PID=$!
sleep 0.5
kill -TERM $WSC_PID
wait $WSC_PID; echo "退出码=$?"  # 应输出 130
cat /tmp/wsc.log

# 4. 真发送（手动触发，谨慎）
python3 skills/weekend-self-check/weekend-self-check.py
```