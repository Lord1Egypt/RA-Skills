# Privacy Contract — zhuge-skill

> 简短版：**你的数据永远不会离开你的机器。作者也拿不到。**

---

## 架构级保证（不是"承诺"，是代码物理事实）

### 1. 单向消费架构 — `sync.py` 只 pull，没有 push

自 v1.0.1 起，`scripts/sync.py` **只有两个命令**：
- `pull` — 从公共 GitHub Release 拉**匿名晶体**（HTTP GET，不携带任何本地数据）
- `status` — 本地查看

`push` 函数**被移除**。这意味着：

> **本 skill 的代码里没有任何一行把你的本地数据发到网络上。**
> 不是"默认关闭"，是**根本没写**。

如果你还是担心，用 `grep` 自查：
```bash
grep -rn "requests.post\|urlopen.*POST\|upload" scripts/ core/
```
你只会看到 `core/llm.py` 里调 LLM 供应商的 POST（那是你自己配置的 API key 目标，也只送 prompt/响应，不送本地数据库）。

---

### 2. 晶体脱敏白名单

即使你未来 fork 了本 skill 并想加共享功能，请遵循 `scripts/sync.py` 里定义的 `ALLOWED_SHARED_FIELDS`：

```python
ALLOWED_SHARED_FIELDS = {
    "crystal_id",   # 匿名 hash，只由 (hexagram, yang_count, outcome) 生成
    "version",
    "trigger",      # {hexagram, yang_count} — 纯结构化特征
    "outcome",      # 如 "1x2=home" — 枚举值
    "stats",        # {matches, hits, rate, ci_95} — 纯数值
    "tags",
}
```

**不允许共享的字段**（哪怕未来添加到晶体里也会被天然排除）：
- 用户 ID / 账号名 / 机器指纹
- 原始比赛名 / 球队名
- 时间戳（防止关联到具体比赛）
- IP / 地理位置
- API key（任何供应商）
- 赔率原始值 / 投注金额
- 其它任何可识别用户的信息

---

### 3. 作者（skill 维护者）的数据可见度

| 维度 | 作者能看到吗？ |
|---|---|
| 你的预测历史 | ❌ 数据不离开你机器 |
| 你的比赛记录 | ❌ |
| 你的 API key | ❌ |
| 你用的 LLM 供应商 | ❌ |
| 你贡献到公共池的匿名晶体 | ✅ 但已脱敏，看不到 "你" |

公共晶体池（`https://github.com/yangfei222666-9/zhuge-crystals`）由作者维护，用于审核社区贡献。**但贡献流程必须是手动 Pull Request**——作者只会看到 PR 里的脱敏晶体 JSON，不会看到贡献者的原始数据。

---

### 4. 运行时网络调用清单（透明）

Skill 在运行中**可能**发起的网络请求：

| 调用 | 触发条件 | 送出的数据 |
|---|---|---|
| `sync.py pull` | 你主动跑 | **无**（纯 GET） |
| `backfill.py` | 你主动跑 | 球队名/比赛日期→数据源 API |
| LLM 孔明评语 | 你启用了 LLM 且主动跑预测 | 卦象+爻位 prompt →你配置的 LLM 供应商 |
| LLM 周报 | 你主动跑 `report.py --llm` | 统计摘要→你配置的 LLM 供应商 |

**没有任何**：
- 遥测 / 埋点 / 使用统计
- "匿名诊断" / "帮助我们改进"
- 自动上传崩溃日志
- 任何指向 `api.zhuge-skill.*` / `api.taijios.*` 之类的端点（**不存在**这些端点）

---

### 5. 如果你用 LLM 中转（relay）

Skill 支持 `relay` 供应商（`base = https://apiport.cc.cd`）。**如果你启用了 relay**：

- 你的 prompt 和 LLM 响应会经过该第三方中转服务器
- 中转方**理论上能看到**对话内容
- 这是你的选择，**不是 zhuge-skill 的选择**

生产环境建议：**直连官方 API**（DeepSeek / OpenAI / Anthropic / Gemini），**不用 relay**。

---

## 如何验证这份合约

你不需要"相信"本文档。直接审代码（2 分钟）：

```bash
# 1. 确认 sync.py 没有上传逻辑
grep -n "requests.post\|push\|upload\|POST" scripts/sync.py
#   应该只看到 docstring 里提到 "没有 push"

# 2. 确认没有遥测端点
grep -rn "telemetry\|analytics\|track" core/ scripts/
#   应该无输出

# 3. 列出所有网络出站
grep -rn "requests.get\|requests.post\|urlopen" core/ scripts/
#   应该只看到：sync.py(pull) / adapters/(数据源) / llm.py(你配的供应商)
```

代码即合约。任何与本文档不符的行为都是 bug，请开 issue。

---

## 变更历史

- **v1.0.2 (2026-04-17)** — 无代码变更；SKILL.md 同步修正，移除与本合约矛盾的旧 §晶体共享 描述
- **v1.0.1 (2026-04-17)** — 首次形成此合约；移除 `sync.py` 的 `push` 函数，固化单向消费架构
- v1.0.0 — Initial release
