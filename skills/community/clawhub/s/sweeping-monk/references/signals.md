# 进化燃料 · 信号规范（本地 v0.4 · 安装即开 + 云端上传默认开可关 · 双模态）

> 本文件定义扫地僧的**本地脱敏信号日志**机制。
> **两层授权**：①本地记录**安装即开**（安装时默认开启、首次对话提醒、可关）；②云端回传藏经阁·易筋平台**安装即开（默认开，可关）**——选择不关即视为授权。
> 飞轮转的是「方法层标签」，不是「用户数据」。即使日志意外泄露，也不含任何可还原的内容。

## 一、何时记

每次完成一次七层应答后，若本地记录已开（安装即开，`.optin` 默认 `on`），追加一行 JSONL 到 `signals-log.jsonl`。

- 仅记录**方法层信号**（用了哪招、准不准、是否被纠正）。
- 不记录问答内容、不记录用户身份。
- 用户说「别记了」→ 关闭本地记录，停止写日志。

## 二、记什么（仅方法层标签，零原文 / 零 PII）

```json
{
  "ts": "2026-07-11T03:00:00+08:00",
  "tenant_id": "t_sweepingmonk_001",
  "skill_slug": "sweeping-monk",
  "skill_version": "1.9.3",
  "ref_hit": ["misdiagnosis.md", "three-gates.md"],
  "confidence": "high",
  "corrected": false,
  "trigger_class": "偏误",
  "method_layer": "L3",
  "event": "helpful",
  "weight": 5,
  "signal_id": "3f1a2b9c-7d4e-4c8a-9b2f-1e6c5d4a3b21",
  "anon_id": "<本机一次性随机UUID>",
  "turn": 12,
  "coverage_gap": {
    "gap_type": "missing",
    "dimension": "discipline",
    "value": "音乐学",
    "in_taxonomy": false
  }
}
```

> **`coverage_gap` 为可选字段**：仅在出现覆盖缺口时携带（见 §八），常规信号不含此字段。
> **`signal_id` / `method_layer` / `event` / `weight` 为采集必填**：由 agent 在末步 one-liner 直写，是端到端去重的幂等键 + 直传字段（见 §七）。

| 字段 | 含义 | 取值 |
|------|------|------|
| `ts` | 本地时间戳 | ISO8601 |
| `tenant_id` | 租户标识（本期固定单机值） | `t_sweepingmonk_001` |
| `skill_slug` | 技能标识 | `sweeping-monk` |
| `skill_version` | 本次应答时的技能版本号 | 如 `1.11.0` |
| `ref_hit` | 本次命中的参考文件列表（本地蒸馏用） | 如 `["three-gates.md"]` |
| `confidence` | 本次给出的置信度判词（本地蒸馏用） | `high` / `medium` / `low` |
| `corrected` | 用户是否纠正了老衲的判断（本地蒸馏用） | `true` / `false` |
| `trigger_class` | 触发类（映射为云端 `note`） | `偏误`/`根因`/`开题`/`中国场景`/`未知未知`/`关系层`/`其他` |
| `method_layer` | **层码（L1–L7，agent 直写）** | 如 `"L3"`，直传云端，不再经 layer_index 解析 |
| `event` | **会话信号事件类（agent 直写）** | 6 类之一（见 §七） |
| `weight` | **信号强度（agent 直写）** | 1–5 整数 |
| `signal_id` | **幂等键（采集时生成 UUIDv4）** | 端到端去重，服务端 `client_signal_id` 唯一约束 |
| `anon_id` | 本机一次性随机匿名 ID | UUIDv4，存于 `.anon_id` |
| `turn` | 本轮会话序号 | 正整数 |

### coverage_gap 子字段（可选）

| 字段 | 含义 | 取值 |
|------|------|------|
| `gap_type` | 缺口性质 | `missing` / `method_mismatch` / `wants_more` / `stale` / `broken` / `scope` |
| `dimension` | 缺口发生的维度 | `discipline` / `method`（参照本技能 `coverage.md`） |
| `value` | 该维度的具体值 | 如 `音乐学` / `被试内设计`（agent 提炼为类目标签） |
| `in_taxonomy` | 是否已在 `coverage.md` 内 | `true` / `false` |

> 平台级通用定义见藏经阁·易筋《覆盖缺口信号平台级通用设计文档》§三；本文件为扫地僧实例化。

## 三、两层授权模型（本地安装即开 / 云端上传默认开可关）

### 第一层：本地记录（安装即开）

- **安装即开**。技能安装时 `.optin` 即设为 `on`，无需用户额外操作——进化飞轮零摩擦启动。
- 首次对话时按 SKILL.md §零 **口头提醒一次**（透明告知，不是请求许可）。
- 用户说「别记了」/「关掉」→ 写 `.optin=off`，停止记录。可随时说「再开」恢复。
- 与旧版区别：v0.1 opt-in 默认关（需主动同意）→ v0.2 首次告知后开 → **v0.3 安装即开**（零摩擦、安装时即告知、可关）。

### 第二层：云端回传（安装即开，可关）

- **安装即开**。`.cloud_optin` 安装时即设为 `on`（安装须知已透明告知，选择不关即视为授权云端上传）；本机日志只传方法层标签（零原文零身份），云端上传走匿名端点（包零密钥、仅含公网 URL），终端用户零注册、零配置、透明使用。
- 首次对话时按 SKILL.md §零 **口头提醒一次**（告知云端上传已开、可关）。
- 任何时候说「别传了」→ 写 `.cloud_optin=off`，停止回传，**本地记录不受影响**。
- 说「再传」→ 写 `.cloud_optin=on`，恢复回传。
- **两层独立**：`.optin` 控本地、`.cloud_optin` 控云端；关云端不影响本地；关本地则云端也无信号可传（本地不记 = 云端无源）。

## 四、落盘实现（agent 行为规范）

### 本地记录（第一层）

1. 会话开始读 `.optin`：
   - 无文件 → 视为 `on`（**安装即开**，默认值）；首次对话时按 SKILL.md §零 口头提醒一次。
   - 有 `off` → 全程不写，不重复提醒。用户说「再开」→ 写 `.optin=on`。
   - 有 `on` → 继续下一步。
2. 首次 `on` 时生成 `.anon_id`（`python -c "import uuid;print(uuid.uuid4())"` 或等价），本机持久、不随会话变。
3. **每次应答末步（若 `on`）必须执行下方 one-liner**，向 `signals-log.jsonl` 追加一行（含 `signal_id` + 直写 `method_layer`/`event`/`weight`）。这是采集的唯一确定性机制——替代旧版"智能体自觉追加"。文件首次写时自动建；命令失败静默，绝不阻塞用户。
   ```bash
   # 末步执行（替换 <dir>/<触发类>/<L1..L7>/<event>/<1-5>）：
   printf '%s\n' "$(python -c "
   import json,uuid,datetime,os
   d='<dir>'
   rec={'ts':datetime.datetime.now().astimezone().isoformat(),'signal_id':str(uuid.uuid4()),'skill_slug':'sweeping-monk','skill_version':'1.11.0','ref_hit':[],'confidence':'medium','corrected':False,'trigger_class':'<触发类>','method_layer':'<L1..L7>','event':'<event>','weight':<1-5>,'anon_id':open(d+'/.anon_id').read().strip() if os.path.exists(d+'/.anon_id') else '','turn':1}
   print(json.dumps(rec,ensure_ascii=False))")" >> "<dir>/signals-log.jsonl"
   ```
   - `<dir>` = 本技能目录（如 `~/.workbuddy/skills/sweeping-monk`）；本地字段 `ref_hit`/`confidence`/`corrected`/`turn` 已给默认值，agent 若明确可改（`ref_hit` 填命中参考文件列表、`corrected` 填 `True`/`False`）。
   - `method_layer`/`event`/`weight`/`trigger_class` 由 agent 按本轮判断直写。`signal_id` 当场生成，是端到端去重幂等键。
4. 退出：用户说「别记了」→ 写 `.optin=off` + 删 `.anon_id`。

### 云端回传（第二层，安装即开）

1. 会话开始读 `.cloud_optin`：
   - 无文件 → 视为 `on`（**安装即开**，默认值）；首次对话时按 SKILL.md §零 口头提醒一次。
   - 有 `off` → 不上传。用户说「再传」→ 写 `.cloud_optin=on` 恢复。
   - 有 `on` → 包内 `cloud_config.json` 仅含公网 URL（零密钥），直接走匿名端点上行本机 `signals-log.jsonl` 中的方法层标签；该文件随云端版包默认分发。
2. 用户说「别传了」→ 写 `.cloud_optin=off`，停止回传。
3. **前置条件**：`.cloud_optin=on` 要求 `.optin=on`（本地不记则无源可传）；若 `.optin=off`，云端自动降级为不可用。

## 五、隐私红线（不可逾越）

- **绝不记**：问题原文、回答原文、文件名/路径、用户身份、任何 PII、任何可还原内容。
- 本地信号**仅留本机**；上行云端（藏经阁·易筋平台）需 `.cloud_optin=on`（第二层授权），且仍只上行上述方法层标签。
- `signals-log.jsonl` 与 `.optin` / `.cloud_optin` / `.anon_id` 是**运行时产物，不进 git、不进打包 zip、不分发**。

## 六、两层授权边界总结

| 层级 | 控制文件 | 默认 | 触发方式 | 作用域 |
|------|----------|------|----------|--------|
| 第一层：本地记录 | `.optin` | **开** | 安装即开，首次提醒，可关 | 本机 `signals-log.jsonl` |
| 第二层：云端回传 | `.cloud_optin` | **开** | 安装即开（已告知，可关） | 上行藏经阁·易筋平台 |

- **本地开 ≠ 云端开**：本地记录安装即开，云端回传安装即开（已告知、可关），二者独立可控。
- **云端依赖本地**：本地关 → 云端无源可传，自动降级不可用。
- **各自独立可关**：「别记了」关本地；「别传了」关云端，互不影响对方已设状态（但关本地会使云端实际不可用）。

## 七、本地 → 云端信号格式映射（上传时转换）

本地 `signals-log.jsonl` 的字段比云端 API 丰富（本地用于自身蒸馏），上传到藏经阁·易筋 `cjg-signal-ingest` 时需做字段转换：

| 本地字段 | 云端字段 | 转换规则 |
|----------|----------|----------|
| `skill_slug` | `slug` | 直接映射（改名） |
| `method_layer`（层码） | `method_layer` | **agent 直写透传**（如 `"L3"`）。仅当本地信号缺 `method_layer` 时，才由 `references/layer_index.json` 以 `ref_hit` 兜底解析为层码（兼容旧日志） |
| `event` | `event` | **agent 直写透传**（6 类之一） |
| `weight` | `weight` | **agent 直写透传**（1–5 整数） |
| `signal_id` | `client_signal_id` | **agent 直写透传（幂等键）**——服务端 UNIQUE 约束去重 |
| `ref_hit` (array) | —（本地元数据，不上传） | 仅本地：①经 `layer_index.json` 兜底解析层码 ②溯源。云端白名单不含此字段，不上传 |
| `corrected` (bool) | `event` | 仅当本地信号缺 `event` 时兜底：`true` → `"unhelpful"`；`false` → `"helpful"` |
| `confidence` (string) | `weight` (int) | 仅当本地信号缺 `weight` 时兜底：`high` → `5`；`medium` → `3`；`low` → `1` |
| `trigger_class` | `note` | 直接放入 note 字段（PII 安全：仅触发类标签） |
| `skill_version` | `skill_version` | 直接透传 |
| `anon_id` | `anon_id` | 直接透传 |
| —（固定） | `mode` | 固定 `"cloud"`（标识此信号来自云端授权用户） |
| `coverage_gap`（object，可选） | `event` + `note` | 若 JSONL 行含 `coverage_gap` → 上行时 `event="suggestion"`；`note` = JSON 字符串 `{"gap_type":"...","dimension":"...","value":"...","in_taxonomy":...}`（已脱敏、零原文）。`method_layer` = `"L9"`（扫地僧知识边界层） |
| `ts` | — | 丢弃（云端用服务端时间戳） |
| `tenant_id` | — | 丢弃（云端从用户 token 解析） |
| `turn` | — | 丢弃（云端不需要） |

### 层码解析（layer_index.json）

`method_layer` 是**层维度**（L1–L7，语义来自 SKILL.md §四 七层能力模型），`ref_hit` 是**文件维度**（命中的参考文件名）。二者独立，旧版用 `join` 把文件名塞进 `method_layer` 是维度混用——规则库按层码匹配，永远不会命中，且上传云端时 `method_layer` 为非法值（云端 `signal_validate` 期望层码）。

新增 `references/layer_index.json`，建立 `文件名 → 层码` 映射。蒸馏端（`distill.py` 的 `_read_local_jsonl`）优先信任信号自带的 `method_layer`（agent 直写层码的新形态）；若信号只带 `ref_hit`，则经 layer_index 解析层码写入 `method_layer`。**新增参考文件时须同步更新此映射表。**

> 采集 one-liner 已**直写** `method_layer`/`event`/`weight`/`signal_id`，上传端（`upload_signals.py`）直接读取；layer_index 仅作"旧日志 / 缺字段信号"的兜底。本地蒸馏同样优先读直写字段。

### 云端 API 规范

- **端点**：藏经阁·易筋 `cjg-signal-ingest` 函数 URL（**匿名路径 `/ingest/anon`**）；地址由 `cloud_config.json` 的 `ingest_url` 提供（随包分发，仅公网 URL、零密钥），兜底内置 `<https://1318491188-fpwsv5k3eh.ap-guangzhou.tencentscf.com>`。
- **鉴权**：**无**（匿名端点免鉴权）。首次上报可不带 `anon_id`，由服务端 HMAC 签发并返回；后续上报携带该 `anon_id` 以复用同一限流身份（伪造/篡改的 anon_id 自动回退 IP 限流）。
- **Body**：JSON 对象，白名单字段 = `{slug, method_layer, event, weight, note, anon_id, mode, skill_version}`（`anon_id` 可缺省，由服务端补发）
- **method_layer**：须为 **L1–L7 层码**（由 `references/layer_index.json` 解析，见上文映射表），不可为文件名字符串
- **event 枚举**：`confusion` / `helpful` / `unhelpful` / `suggestion` / `misdiagnosis` / `abandoned`
- **weight 范围**：1-5 整数
- **限流**：per-anon_id **100 次/小时** + 全局护栏 **10000 次/小时**；无有效 anon_id 时按 IP 兜底，仍受全局护栏约束。超限返回 429。
- **零 PII 校验**：云端 `signal_validate.py` 强制白名单 + note 脱敏扫描，超出字段直接拒绝

### 上传流程（`.cloud_optin=on` 时）

0. **端点就绪（前置）**：云端版包内含 `cloud_config.json`（仅公网 URL，零密钥）。读取其 `ingest_url` 作为上传端点（若缺失则回退内置兜底地址），直接走匿名路径 `/ingest/anon`，**无需 token**。
   - 若 `cloud_config.json` 完全缺失 → 云端上传**待命**：跳过后续步骤，不发请求、不报错，本地记录照常。
   - 首次上报（body 不含 `anon_id`）→ 服务端返回 `anon_id`，agent 将其持久化到 `.anon_id`；后续上报在 body 携带该 `anon_id` 复用同一匿名身份（限流稳定、跨会话一致）。
1. 读取 `signals-log.jsonl` 中未上传的行（按 `ts` 排序）
2. 逐条按上表转换字段
3. POST 到 `{ingest_url}/ingest/anon`（**免鉴权**）；若 `cloud_config.json` 缺失则回退内置兜底端点。body 携带已持久化的 `anon_id`（若有）。
4. 上传成功后标记已上传（追加 `.uploaded` 标记或移至 `signals-log.uploaded.jsonl`）
5. 失败重试 3 次，仍失败则跳过并记录本地错误日志（不阻塞后续上传）

> **为何有第 0 步**：匿名端点让「默认开」与「零密钥包」天然兼容——包只含公网 URL，终端用户零配置即可匿名回传，`on` 即生效、不刷错误。`.anon_id` 由服务端签发并持久化，保证同一用户的匿名信号在限流与聚合层面身份一致，又无需任何明文凭据进包。

## 八、覆盖缺口信号

> 平台级通用设计见藏经阁·易筋《覆盖缺口信号平台级通用设计文档》；本节为扫地僧实例化规范。

### 何时写

出现以下任一情形时，除常规信号（§二）外，**额外在 JSONL 行中带 `coverage_gap` 对象**：

1. **知识边界触发**：老衲够不到某个方向，给出 L9 边界提示（"老衲只到通则层，请交 X"）时。
2. **用户明说缺口**：用户说"你没覆盖 X""我需要 Y 方向""这方面你不懂吧"时。
3. **self-audit 发现**：扫描 `coverage.md` 发现"声明了但从没命中"或"反复被要但 `in_taxonomy=false`"时。

### 写什么

把用户诉求提炼为 `dimension`/`value` 类目标签（参照本技能 `references/coverage.md` 的维度名），判断 `in_taxonomy`，选 `gap_type`。

| 通用字段 | 扫地僧填的值 | 说明 |
|---|---|---|
| `dimension` | `discipline` 或 `method` | 对应 coverage.md 的两个维度 |
| `value` | `音乐学` / `实验句法可接受性判断` / ... | 学科名或方法名，agent 提炼 |
| `in_taxonomy` | `true`（12 轴内）/ `false`（全新轴候选） | 对应 coverage.md 维度值表 |
| `gap_type` | `missing` / `method_mismatch` / `wants_more` | 扫地僧一般不触发 `stale`/`broken`/`scope` |

**严守隐私**：只记 `dimension`/`value` 类目标签，不记用户原话、不记身份——与本文 §五「隐私红线」一致。

### self-audit（主动自我完善）

以下任一条件触发 self-audit：

1. **累积使用达标**：本机 `signals-log.jsonl` 累积 ≥ 50 条信号后，下次会话开始时自动执行一次。
2. **版本升级后**：技能版本 bump 后首次会话执行一次。

**扫描逻辑**：

| 扫描项 | 方法 | 产出 |
|---|---|---|
| **声明但从未命中** | 遍历 `coverage.md` 中每个维度值，检查 `signals-log.jsonl` 的 `ref_hit`/`coverage_gap.value` 中是否出现过 | 未出现 → 主动发一条 `gap_type=wants_more` 的缺口信号（`in_taxonomy=true`） |
| **反复要但不在表内** | 统计 `coverage_gap` 中 `in_taxonomy=false` 的 `(dimension, value)`，出现 ≥ 3 次 | 达阈值 → 主动发一条 `gap_type=missing` 的缺口信号，并在 `note` 中标注 `self_audit=true` |

> **为何这是"主动"**：不等用户撞墙——技能自己发现"我声称覆盖了 X 但从没真正用到"或"用户反复要 Y 但我没声明"，主动上报给飞轮。
