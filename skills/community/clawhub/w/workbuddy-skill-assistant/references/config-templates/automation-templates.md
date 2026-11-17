# 自动化任务配置模板

> 复制需要的模板，按注释修改参数，用 `automation_update mode="create"` 创建。
>
> ⚠️ **必改项**：所有模板的 `cwds` 必须改为**你自己的 skill 工作区路径**（即 SKILL.md 所在目录），否则自动化会在错误目录运行、找不到文件。
> ⚠️ `rrule` 写错是最常见的"自动化不执行"原因，格式参考文末「rrule 速查」。

---

## 模板0：每日主动检查（「启用主动监护」标准配置）

本 skill 的一键监护自动化。初始化引导完成后主动询问创建，或用户说"启用主动监护 / 建每日检查"。确认后用 `automation_update` 创建（ACTIVE）：

```yaml
name: WorkBuddy 每日主动检查
scheduleType: recurring
rrule: FREQ=DAILY;INTERVAL=1;BYHOUR=11;BYMINUTE=0
prompt: 【主动态】按本 skill 安装目录（$SKILL_DIR，即 SKILL.md 所在目录）的 references/execution.md 的「主动态执行脚本」执行每日检查。一切行为/边界遵循该文件与 SKILL.md，勿自行发散。
status: ACTIVE
```

**验证**：创建后点"运行一次"立即测试，或次日 11:00 看 `reports/` 是否新增。

---

## 模板1：每日系统检查

每天上午 11:00 自动运行系统状态诊断，发现问题后入队报告。

```yaml
name: 每日系统检查
prompt: |
  执行每日系统状态检查：
  1. 运行 scripts/usage_diag.py --json 获取当前状态
  2. 对照 references/system-scan.md 的分级标准判断
  3. 若有 P0/P1 问题，记录到 reports/ 并更新 state.md 的 pending_actions
  4. 若一切正常，只更新 last_check 时间戳，静默退出
scheduleType: recurring
rrule: FREQ=DAILY;BYHOUR=11;BYMINUTE=0
cwds: <你的工作区路径>
status: ACTIVE
```

---

## 模板2：每周策略周报

每周一早 8:00 生成上周的使用效率分析报告。

```yaml
name: 每周效率周报
prompt: |
  生成本周 WorkBuddy 使用效率周报：
  1. 读 state.md 获取本周所有检查记录
  2. 运行效率建议「运行记录扫描」：检索本周对话，归类使用模式问题
  3. 运行「最佳实践达标检查」：跑 checklist 审计 + 未达标项展开 install_skill 推荐
  4. 汇总为本周周报 reports/YYYY-WW.md，含健康评分趋势图
  5. 如有 P0/P1 问题，追加到 state.md 的 pending_actions
scheduleType: recurring
rrule: FREQ=WEEKLY;BYDAY=MO;BYHOUR=8;BYMINUTE=0
cwds: <你的工作区路径>
status: ACTIVE
```

---

## 模板3：知识库同步

每晚 22:00 自动同步 Obsidian 最新笔记到知识库。

```yaml
name: 知识库同步
prompt: |
  执行每日知识库同步：
  1. 扫描 Obsidian Stock 仓库最新更新的笔记（最近 24h）
  2. 用 ontology skill 识别新实体和关系
  3. 更新实体图谱
  4. 如有新材料触发 skill 推荐，加入 pending_actions
scheduleType: recurring
rrule: FREQ=DAILY;BYHOUR=22;BYMINUTE=0
cwds: <你的工作区路径>
status: ACTIVE
```

---

## 模板4：月度清理

每月 1 日凌晨 2:00 清理过期报告和临时文件。

```yaml
name: 月度清理
prompt: |
  执行月度文件清理：
  1. 检查 reports/ 目录，归档超过 30 天的报告到 reports/archive/
  2. 检查 state.md 的 pending_actions，清理已完成超过 7 天的条目
  3. 检查 dist/ 目录，确认与源文件同步
  4. 生成清理报告 reports/cleanup-YYYY-MM.md
scheduleType: recurring
rrule: FREQ=MONTHLY;BYMONTHDAY=1;BYHOUR=2;BYMINUTE=0
cwds: <你的工作区路径>
status: ACTIVE
```

---

## 自动化调试 checklist（"不执行"排查5步法）

1. **查状态**：`automation_update mode="list"` → status 是否是 ACTIVE？
2. **查时间**：rrule 的下次触发时间是否已过？用 `date` 命令验证
3. **查范围**：validFrom/validUntil 是否覆盖当前日期？
4. **查路径**：cwds 指向的工作目录是否存在且可访问？
5. **查日志**：`automation_runs` 表是否有错误记录？

> 完整故障排查见 `references/faq.md` → 第2节「自动化任务」

---

## rrule 速查（写错 = 不执行）

| 想要 | rrule | 说明 |
|------|-------|------|
| 每天 9:00 | `FREQ=DAILY;BYHOUR=9;BYMINUTE=0` | 最常用 |
| 每周一 8:00 | `FREQ=WEEKLY;BYDAY=MO;BYHOUR=8;BYMINUTE=0` | BYDAY 用 MO/TU/WE/TH/FR/SA/SU |
| 每月 1 日 2:00 | `FREQ=MONTHLY;BYMONTHDAY=1;BYHOUR=2;BYMINUTE=0` | BYMONTHDAY=1 即每月1号 |
| 每 4 小时 | `FREQ=HOURLY;INTERVAL=4` | 高频任务用 |

> 排查口诀：**查状态（ACTIVE？）→ 查时间（rrule 对？）→ 查范围（validFrom/Until 覆盖今天？）→ 查路径（cwds 存在？）**
