---
name: Skills Audit
version: 1.5.3
description: 面向 OpenClaw Skills 的安全审计 + 追加写日志 + 变更监控推送（含文件级 diff、基线审核、SHA-256 校验）。
---

# Skills Audit（skills-audit）

`skills-audit` 是一个偏安全与可观测性的 skill，帮助你更安全地管理 OpenClaw 的 skills。该包**包含可执行的 Python 脚本**（并非只有指令文本），核心包含六项能力：

1）**威胁扫描分析能力（静态）**
2）**日志记录功能（自动生成并本地保存）**
3）**Skills 监控与变更提醒（可选推送）**
4）**文件级 diff + content diff（git 快照）**
5）**基线审核机制（已审核 skill 不重复报）**
6）**大模型语义检测（危险函数 + 功能分析）**

> 本 skill 对**被审计的 skill**只做静态分析，**不会执行被审计 skill 本身的代码**。但审计工具自身会执行**本地受控命令/子进程**，例如 `git`、Python 辅助脚本，以及用于快照、diff、通知生成的受控本地进程调用。

---

## 环境要求

- **Python ≥ 3.9**，无第三方依赖（仅使用标准库）
- **git**（必需，用于 content diff 快照与本地历史比对）
- 具备正常本地 shell / 进程执行环境，供审计工具自身执行受控子进程
- 依赖声明见 `scripts/requirements.txt`

---

## 核心能力

### 1）威胁扫描分析能力（网络/危险命令/可疑文件）
通过 `skills_audit.py` 对安装后的 skill 目录做静态扫描，提取风险信号；如已配置奇安信 token，则会额外基于**整个 `workspace/skills` 稳定压缩包 MD5** 查询奇安信 SafeSkill 情报（不再上传压缩包内容）：

- **网络扫描/指标**：从文本中提取 URL/域名，并识别 `curl/wget/requests` 等外联线索
- **危险命令扫描**：`curl|sh`、`wget|bash`、`eval`、动态执行、base64 解码管道等
- **可疑文件/行为扫描**：持久化（cron/systemd 等）、敏感路径访问（`~/.ssh`、`~/.aws`、`/etc` 等）
- **奇安信情报查询（可选）**：对整个 `workspace/skills` 计算稳定 MD5，通过用户自填 token 查询奇安信 SafeSkill 情报

风险输出：
- `risk.level`：`low | medium | high | extreme`
- `risk.decision`：`allow | allow_with_caution | require_sandbox | deny`
- `risk.risk_signals[]`：证据（文件 + snippet）
- `risk.network.domains[]`：提取到的域名列表
- `risk.source`：`local` 或 `qianxin-md5`

奇安信配置说明：
- 配置文件：`config/intelligent.json`
- 默认 `enabled: false`（关闭）
- `token` 默认留空
- 用户下载后如需启用，自行填写 token 并将 `enabled` 改为 `true`
- 若关闭、token 为空、查询失败或接口不可用：自动回退到本地静态扫描

### 2）日志记录功能（Append-only NDJSON）
将每一次检测结果以 NDJSON（每行一个 JSON）追加写入本地：

- 日志：`~/.openclaw/skills-audit/logs.ndjson`（append-only）
- 状态：`~/.openclaw/skills-audit/state.json`（用于 diff：新增/变更/删除）

日志结构以 `skills-audit/log-template.json` 为准，关键点：
- 顶层包含 `sha256`（skill 目录内 `SKILL.md` 的 SHA-256，用于完整性校验）
- `observed.install_path` 是安装路径的唯一来源
- **不包含** `source`、`approval` 字段（减少冗余/敏感信息采集范围）

### 3）Skills 监控与变更提醒（可选推送）
对 `workspace/skills` 做周期性监控，发现 **新增/变更/删除** 时生成提醒消息并推送。

- 无变化：不推送
- 有变化：推送一条消息（避免重复与噪音）
- 已审核（baseline approved）且未变更的 skill 不会出现在通知中

通知模板见 `templates/notify.txt`，详细说明见 `templates/README.md`。

组件：
- `skills_watch_and_notify.py`：从模板生成通知文本（无变化则无输出）
- `openclaw cron add / edit`：由 OpenClaw 负责创建/更新定时任务与消息投递

> 推送目标不写死，通过当前会话上下文获取 channel / to 参数。

### 4）文件级 diff + content diff（git 快照）

每次 scan 完成后，自动将 skills 目录快照到本地 git repo（`~/.openclaw/skills-audit/snapshots/`）：

- 每次 scan = 一次 git commit
- 变更检测 = `git diff HEAD~1 HEAD`
- 通知中展示文件级变更摘要（+N -N 行）
- 用户可随时查看完整 diff

分层展示规则：
- 变更文件 ≤ 5：全部列出
- 6~20：前 3 个 + 省略
- \> 20：前 3 个 + 省略 + ⚠️ 大规模变更警告
- 变更 skill 数 > 8：高风险展开，低风险压缩

查看 content diff：
```bash
git -C ~/.openclaw/skills-audit/snapshots diff HEAD~1 HEAD
git -C ~/.openclaw/skills-audit/snapshots diff HEAD~1 HEAD -- skills/<skill-name>/
git -C ~/.openclaw/skills-audit/snapshots log --oneline
```

### 6）大模型语义检测（危险函数 + 功能分析）

每次扫描时，会额外生成一份“语义检测”结果，并写入日志字段 `semantic_analysis`：

- **危险函数分析**：识别 `eval`、`exec`、`os.system`、`subprocess + shell=True`、`curl|sh`、`wget|bash` 等高风险模式
- **功能分析**：识别该 skill 是否具备网络访问、文件系统修改、进程执行、定时任务、git 操作、配置处理等能力
- **综合结果**：将“执行能力风险”和“恶意意图风险”分开评估，并以“语义意图”作为更重要的主判维度，再给出 `level / decision / reason`

说明：
- 当前实现为**本地大模型风格语义启发式分析**，不依赖外部模型 API
- 这是 **硬性规则**：凡是新增或变更的 skill，在 `skills_audit.py scan` 流程中都必须执行语义检测
- 若 `semantic_analysis` 缺失、为空或无法生成结果，则该次扫描应视为失败，而不是静默跳过
- 为减少审计器自检误报，规则文件、日志模板、技能文档，以及 `config/semantic-patterns.json` 这类模式配置文件，不会参与高权重危险函数评分
- 风险规则扫描已区分命中上下文：`real_execution / rule_sample / doc_example / config_sample`
- 对 `skills_audit.py` 本身，语义检测与规则扫描都会优先识别真实执行路径，而不是把模式字符串表本身当作高危执行行为
- 语义检测会区分“有执行能力”与“有恶意意图”：前者不等于恶意，避免审计工具因具备正常工程能力而被过度打高
- 对 `subprocess.run([...], shell=False)`、固定 argv、本地受控命令调用会按“工程能力”处理，而不是直接判成高恶意倾向
- 结果会作为日志模板中的独立字段保存，便于后续接入真正的大模型服务或做前端展示

### 5）基线审核机制

通过 `baseline.json`（`~/.openclaw/skills-audit/baseline.json`）管理已审核 skill：

- 审核后的 skill（tree_sha256 匹配）不再重复报风险
- 任何文件变动自动打破基线，重新触发风险检测
- 支持单个审核、批量审核、查看列表、撤销审核

```bash
# 审核单个 skill
python3 {baseDir}/scripts/skills_audit.py approve --skill weather --workspace <workspace>

# 批量审核所有
python3 {baseDir}/scripts/skills_audit.py approve --all --workspace <workspace>

# 查看已审核列表
python3 {baseDir}/scripts/skills_audit.py baseline --list

# 撤销审核
python3 {baseDir}/scripts/skills_audit.py baseline --revoke --skill weather
```

---

## 初始化与手动创建监控（Agent 指令）

当 Agent 首次加载本 skill 时，可以自动做**本地初始化**，但**不要自动创建 cron**，必须改为引导用户手动创建：

1. 检查 `~/.openclaw/skills-audit/state.json` 是否存在
2. 若不存在，执行初始化：
   ```bash
   python3 {baseDir}/scripts/skills_audit.py init --workspace <workspace>
   ```
3. 检查是否已有 `skills-audit-watch` cron 任务（`openclaw cron list`）
4. 若没有：
   - **不要自动创建 cron**
   - 告知用户可手动创建监控任务
   - 给出建议命令示例（请用户确认后自行执行或明确授权 Agent 执行）：
   ```bash
   openclaw cron add \
     --name "skills-audit-watch" \
     --cron "*/1 * * * *" \
     --tz "Asia/Shanghai" \
     --session isolated \
     --message "python3 {baseDir}/scripts/skills_watch_and_notify.py --workspace <workspace>" \
     --announce \
     --channel <当前渠道> \
     --to <当前用户ID>
   ```
5. 提醒用户：
   - 创建 cron 前应确认推送目标是否合适
   - 原始变更内容可能较长，必要时应先做摘要或收敛推送范围
   - **默认不要把大型原始 diff 直接推送到外部频道**，优先发送摘要，再按需查看详情

> **设计原则**：`skills-audit` 只负责扫描、日志、提醒文本生成；定时调度与消息投递应由用户明确决定，不再默认自动创建。

---

## 查看变更详情（Agent 强制流程）

> ⚠️ **强制规则**：当用户询问 skill 变更详情时（包括但不限于以下表达），Agent **必须**使用 `show` 命令获取结构化变更信息；默认应先给出**安全摘要**，而不是直接外发完整原始 diff。

**触发词**（用户可能的表达方式）：
- "具体改了什么" / "哪里变了" / "看一下变更" / "变更详情"
- "diff" / "看看 diff" / "改动内容"
- "什么文件被改了" / "改了哪些东西"
- 英文："what changed" / "show diff" / "what's different"

**执行流程（固定，不可跳过）**：

1. 如果用户提到了具体 skill 名称：
   ```bash
   python3 {baseDir}/scripts/skills_audit.py show --skill <skill-name>
   ```
2. 如果用户没指定具体 skill：
   ```bash
   python3 {baseDir}/scripts/skills_audit.py show
   ```
3. 默认仅发送 `show` 输出的**安全摘要**（文件、行数、主要改动点），避免直接外发可能包含敏感内容的完整 diff
4. 只有在用户**明确要求查看原始完整内容**时，才发送完整 `show` 输出；发送前应提醒其中可能包含敏感信息
5. 如果用户想看更早的历史，使用 `--commit-range`：
   ```bash
   python3 {baseDir}/scripts/skills_audit.py show --commit-range HEAD~3..HEAD~2
   ```

**禁止行为**：
- ❌ 自行执行 `git diff` 并绕过 `show` 的结构化输出
- ❌ 在未提醒风险的情况下，把可能包含敏感信息的完整原始 diff 默认外发到频道
- ❌ 将大段原始变更内容自动推送到外部频道
- ✅ 优先基于 `show` 结果发送安全摘要；用户明确要求时再提供完整原始内容

**输出格式（由 `show` 命令固定生成，每次一致）**：
```
📦 <skill-name>
   共变更 N 个文件，新增 X 行，删除 Y 行

   主要变更：
   • file1（+N -N）
   其他变更：
   • file2（+N -N）

────────────────────────────────────────
📝 具体改动内容：

   📄 [skill] filename
      新增内容：
        + 具体新增的代码或文字
      删除内容：
        - 具体删除的代码或文字
      修改内容：
        - 旧内容
        + 新内容
```

---

## 手动使用

### 初始化

```bash
python3 {baseDir}/scripts/skills_audit.py init --workspace /root/.openclaw/workspace
```

会创建：
- `~/.openclaw/skills-audit/logs.ndjson`
- `~/.openclaw/skills-audit/state.json`
- `~/.openclaw/skills-audit/baseline.json`
- `~/.openclaw/skills-audit/snapshots/`（git repo）

### 手动扫描

```bash
python3 {baseDir}/scripts/skills_audit.py scan --workspace /root/.openclaw/workspace --who user --channel local
```

### 监控通知（本地验证）

```bash
python3 {baseDir}/scripts/skills_watch_and_notify.py --workspace /root/.openclaw/workspace
```

---

## 注意

- 本技能只做**静态分析**，不要在审计过程中执行任何未知 skill 代码。
- 当风险等级为 `high/extreme` 时，建议要求人工确认或在隔离环境中验证。
- 推荐由 OpenClaw 的 `cron add` / `cron edit` 负责定时任务写入与消息投递。
- 完整性校验使用 **SHA-256**。
