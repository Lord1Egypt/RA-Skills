---
name: weekly-report-pro
description: 周报生成器Pro v1.2——自动收集素材再成稿,支持周报+月报。当用户说"写周报""生成周报""周报""本周工作总结""写月报""月度总结"等需要产出工作汇报时使用本技能。自动从本机 Git 提交记录收集工作素材(含代码统计),自动识别角色,可读取 Markdown 计划清单统计完成率,结合用户提供的待办清单、口述要点,生成结果导向、可量化的结构化汇报。支持程序员/运营/销售/管理者四种角色模板,支持钉钉/飞书/邮件三种排版风格。全程本地运行,不上传任何数据。
---

# 周报生成器 Pro v1.2 (Weekly Report Pro)

自动收集素材 → 结构化成稿。拒绝流水账,写出让领导看得见价值的周报/月报。

## 使用步骤

### 第一步:收集素材(能自动的都自动)

1. **Git 提交记录**(如用户是开发者或本机有代码仓库):

```bash
python3 {baseDir}/scripts/collect_git.py --dirs <用户的代码目录> --days 7
```

   可选参数:
   - `--days 30` 或 `--mode monthly` — 月报模式,回溯30天
   - `--include-merges` — 包含 merge commits(默认排除)
   - `--with-stats` — 附带每个仓库的增删行数+文件数统计
   - `--author <名字>` — 按作者过滤
   - `--role auto|developer|ops|sales|manager` — 自动识别或手动指定角色
   - `--plan-file <路径>` — 只读解析 Markdown 任务清单中的完成率
   - `--language auto|zh|en` — 选择模板语言元数据
   - 输出 JSON:各仓库提交记录+可选代码统计

2. **询问用户补充素材**(一次问齐,别挤牙膏):
   - 本周/本月完成的非代码工作(会议/文档/沟通/上线)?
   - 有没有可量化的数字(处理量、增长、耗时、营收)?
   - 遇到的阻塞和需要的支持?
   - 下周期/下月计划?
   - 也接受:待办清单文件、聊天记录导出文件、口述一段话

### 第二步:自动检测角色与风格

优先使用脚本输出的 `role` 字段;也可用 `--role` 覆盖。根据 Git 仓库语言和提交内容自动判断:
- **仓库语言为代码** → 默认「程序员」角色
- **提交消息多含"运营/数据/转化"** → 建议「运营」角色
- **用户为团队 Lead/管理者** → 建议「管理者」角色

若不确定,二选一确认:
- **角色**:程序员 / 运营 / 销售 / 管理者
- **风格**:钉钉简洁版(短句+emoji) / 飞书文档版(层级标题) / 邮件正式版(无emoji)

脚本输出的 `dashboard` 包含仓库数、提交数、代码增删行数和变更文件数。
如果提供 `--plan-file`,使用 `goal_tracking.completion_rate` 写出“上周计划完成率”;计划文件只读,不存在或无法读取时如实说明。
`language` 为 `zh` 时使用中文模板,为 `en` 时使用英文模板; `auto` 会根据提交信息中的中文字符选择。

### 第三步:成稿(写作铁律)

1. **结果导向**:每条以动词开头,写"做成了什么",不写"做了什么"
   - ❌ 参与了支付模块开发
   - ✅ 完成支付模块退款链路开发,联调通过,预计下周二上线
2. **能量化就量化**:提交数、代码增删行数、解决问题数、覆盖率、转化率、金额
3. **合并同类项**:同一项目多条提交合并为一条成果
4. **诚实**:素材里没有的事不编造;阻塞项如实写
5. 篇幅:周报 200-400 字,月报 400-800 字;用户可要求调整

### 周报模板

```markdown
# 周报 · {姓名} · {MM.DD-MM.DD}

## ✅ 本周成果
1. (成果+量化数据+状态)
2. ...

## 📊 本周数据(如有 --with-stats)
- {仓库A}: {commit_count} 提交, +{lines_added}/-{lines_deleted} 行, {files_changed} 文件
- 总计: {dashboard.repo_count} 个仓库, {dashboard.total_commits} 提交, +{dashboard.lines_added}/-{dashboard.lines_deleted} 行, {dashboard.files_changed} 文件

## 🎯 计划完成率(如有 --plan-file)
- {goal_tracking.completed}/{goal_tracking.total} 项已完成 ({goal_tracking.completion_rate}%)

## 🚧 进行中
- (事项+当前进度+预计完成时间)

## ⚠️ 风险与求助
- (阻塞点+需要谁的什么支持;无则写"无")

## 📋 下周计划
1. (具体+可验收)
```

### 月报模板

```markdown
# 月报 · {姓名} · {YYYY年MM月}

## 📈 本月关键成果
1. (重大里程碑+量化数据)
2. ...

## 📊 本月数据汇总
- 总提交: {total_commits} 次 · 代码: +{lines_added}/-{lines_deleted} 行 · 涉及 {files_changed} 文件

## 🎯 目标完成情况
(对比月初目标,逐项说明)

## 🚧 进行中
- (跨月事项+进度)

## ⚠️ 风险与求助
- (阻塞点;无则写"无")

## 📋 下月计划
1. (大目标+可验收里程碑)
```

### English template (when `language` is `en`)

```markdown
# Weekly Report · {name} · {MM.DD-MM.DD}

## Key Outcomes
1. (outcome + metric + status)

## Metrics
- {dashboard.repo_count} repositories, {dashboard.total_commits} commits, +{dashboard.lines_added}/-{dashboard.lines_deleted} lines, {dashboard.files_changed} files

## Plan Completion
- {goal_tracking.completed}/{goal_tracking.total} items complete ({goal_tracking.completion_rate}%)

## In Progress / Risks / Next Period
- (facts only; do not invent missing details)
```

## 隐私说明

Git 记录仅在本机读取分析;所有素材(待办/口述/聊天)仅在当前会话使用;本技能不上传任何数据。
