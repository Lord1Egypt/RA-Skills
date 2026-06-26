# skill-perf 测试方案 v2 — Subagent 架构 Spec

**版本**: v2.0  
**状态**: 草稿  
**背景**: 解决 isolated Cron session 无法读取自身 sessions.json 数据导致报告 totalTokens=0 的根本问题

---

## 1. 根因分析

### 1.1 核心约束（OpenClaw 机制）

```
sessions.json 写入时机：
  - 主 session（agent:main:main）：每次 LLM call 完成后增量写入
  - isolated Cron session：仅在 session 完全结束后，一次性写入
  - subagent session：subagent 完成后，立即写入父 agent 的 sessions.json
```

**关键结论**：Cron isolated session 在自身运行过程中，永远无法从 sessions.json 读到自己的 `totalTokens`。

### 1.2 旧方案的问题链

```
Cron session 内 → snapshot.py report --session agent:main:cron:perf-test-rN
  └─ _read_full_session("agent:main:cron:perf-test-rN")
       └─ 读 sessions.json → key 不存在 or totalTokens=0
            └─ 报告显示 net=0（错误）
```

### 1.3 底噪标定误读问题

`snapshot.py sessions | head -3` 按 totalTokens **降序**排列，front-3 不一定是 skill-calibration session，导致 Agent 拿到错误的 calib_totalTokens（如 746），计算出负数底噪（-137）。

---

## 2. v2 架构设计

### 2.1 核心思路

**把"被测行为"放进 subagent，parent 读 subagent 的已完成 session**。

- subagent 完成 → 它的 session 立即写入 sessions.json（因为从 parent 视角它是一个完成的 external session）
- parent 仍在运行 → parent 可以自由读取任何其他已完成的 session
- 结果：parent 读 subagent session key → `totalTokens` 正常 ✅

### 2.2 三阶段流程

```
┌─────────────────────────────────────────────────────────────────┐
│  Cron isolated session (parent) — agent:main:cron:perf-test-rN  │
│                                                                  │
│  ① 底噪标定                                                      │
│     └─ 调用 skill-calibration（子任务）                           │
│     └─ sessions | grep "skill-calibration" → 精确获取 calib_total│
│     └─ calibrate.py save --total <calib_total> --runs 1          │
│     └─ 本轮底噪 = calib_total - CALIB_SKILL_TOKENS(344)          │
│                                                                  │
│  ② 投屏测试（spawn subagent）                                     │
│     └─ subagent 任务: mirror.sh start + stop ONLY                │
│     └─ 等待 subagent 完成（输出 MIRROR_TEST_DONE）                │
│                                                                  │
│  ③ 生成报告                                                       │
│     └─ sessions --latest-subagent → subagent session key         │
│     └─ report --session <subagent_key> --noise <本轮底噪>         │
│          └─ subagent session 已完成 → totalTokens 正常 ✅         │
└─────────────────────────────────────────────────────────────────┘
```

### 2.3 Session Key 格式（已确认）

| Session 类型 | Key 格式 |
|---|---|
| Cron isolated | `agent:main:cron:perf-test-device-mirror-r12` |
| subagent | `agent:main:subagent:<uuid>` |
| 主 session | `agent:main:main` |

---

## 3. 各组件详细设计

### 3.1 Cron 消息模板（三阶段）

```
【skill-perf测试 device-mirror rN - subagent架构 v2】

## 阶段一：底噪标定

调用 skill-calibration 技能，严格只输出 PERF_CALIBRATION_OK。

标定完成后，精确获取标定 session 的 totalTokens：
```
python3 ~/.openclaw/skills/skill-perf/scripts/snapshot.py sessions 2>&1 \
  | grep 'skill-calibration' \
  | grep -v ':run:' \
  | head -1
```
取第二列数字作为 calib_totalTokens，执行：
```
python3 ~/.openclaw/skills/skill-perf/scripts/calibrate.py save \
  --total <calib_totalTokens> --runs 1 --agent main
```
记录本轮底噪值（= calib_totalTokens - 344）。

## 阶段二：通过 subagent 执行投屏测试

创建 subagent，任务：
```
只执行以下操作，完成后立即输出 MIRROR_TEST_DONE，不做其他任何事情：
1. bash ~/.openclaw/skills/device-mirror/scripts/mirror.sh start --android
2. 等待 5 秒
3. bash ~/.openclaw/skills/device-mirror/scripts/mirror.sh stop --android
输出：MIRROR_TEST_DONE
```
等待 subagent 完成，确认输出了 MIRROR_TEST_DONE。

## 阶段三：parent 生成报告

```
SUBAGENT_KEY=$(python3 ~/.openclaw/skills/skill-perf/scripts/snapshot.py \
  sessions --latest-subagent 2>&1)
echo "subagent session: $SUBAGENT_KEY"

python3 ~/.openclaw/skills/skill-perf/scripts/snapshot.py report \
  --session "$SUBAGENT_KEY" \
  --noise <本轮底噪> \
  --skill-name device-mirror \
  --html
```

输出报告链接，然后输出：ANNOUNCE_SKIP
```

### 3.2 `snapshot.py sessions --latest-subagent`（已实现）

```python
def cmd_sessions(latest_subagent: bool = False):
    # ...
    if latest_subagent:
        subagents = [s for s in all_sessions
                     if ":subagent:" in s["key"] and ":run:" not in s["key"]
                     and s["total_tokens"] > 0]
        subagents.sort(key=lambda x: x["updated_at_ms"], reverse=True)
        print(subagents[0]["key"] if subagents else "")
        return
```

**潜在问题**：`--latest-subagent` 按时间取最新，但 parent Cron session 启动前可能已有历史 subagent session。需要确保时间窗口内只有本次 subagent。

**风险缓解**：
- 测试 Cron job 之间间隔 ≥ 5 分钟（subagent archiveAfterMinutes=5）
- 或者：在阶段二之前记录当前时间，`--latest-subagent` 只取 N 分钟内的 subagent

### 3.3 `calibrate.py save` 精确读取

**旧写法（有 bug）**：
```bash
snapshot.py sessions 2>&1 | head -3
# ❌ head -3 拿的是 totalTokens 最大的 3 条，不一定是 skill-calibration
```

**新写法**：
```bash
snapshot.py sessions 2>&1 | grep 'skill-calibration' | grep -v ':run:' | head -1
# ✅ 精确过滤，只取 skill-calibration session
```

Session 输出格式（列：key, total, input, output, updated_time）：
```
agent:main:cron:skill-calibration-xxx   18,256    9,128    1,598   14:51:00
```
取第二列（`awk '{print $2}'` 或 Agent 手动解析）。

### 3.4 `cmd_report` 简化（已回退 pending/defer 机制）

```python
def cmd_report(session_key, html=False, skill_name="", noise_override=None):
    raw = _read_full_session(session_key)
    if not raw:
        print({"error": f"未找到 session: {session_key}"})
        return 1
    if raw.get("totalTokens", 0) == 0:
        print("  ⚠️  totalTokens=0，session 数据未就绪。")
        print("  💡 建议：在 Cron 消息中用 subagent 执行测试，parent 读 subagent session key 生成报告。")
        return 1
    # ... 正常生成报告
```

---

## 4. 关键问题与边界情况

### 4.1 subagent archiveAfterMinutes=5

**问题**：subagent 5 分钟后被 archive，`sessions --latest-subagent` 是否还能找到它？

**待确认**：archived subagent 的 session key 是否仍保留在 sessions.json 中？

**验证方法**：
```bash
# 在 subagent 完成 6 分钟后执行
python3 snapshot.py sessions | grep subagent
# 看是否还有该条目
```

**若消失**：需要在 subagent 完成后立即（阶段三）生成报告，不能有延迟。目前三阶段是连续的，应该 OK。

### 4.2 `--latest-subagent` 时间窗口问题

**问题**：如果 parent 在阶段三执行前有历史 subagent（上次测试残留），`--latest-subagent` 可能返回错误 key。

**解决方案 A（推荐）**：在 Cron 消息阶段二前，让 Agent 记录当前时间戳，阶段三时传给 `--after-ts` 参数：
```bash
TS_BEFORE=$(python3 -c "import time; print(int(time.time()*1000))")
# ... spawn subagent ...
python3 snapshot.py sessions --latest-subagent --after-ts $TS_BEFORE
```

**解决方案 B（简单）**：测试 Cron job 的 schedule 间隔 ≥ 10 分钟，保证 archive 后再触发下次。

**解决方案 C（更robust）**：让 subagent 在最后一步执行 `snapshot.py sessions | grep subagent | head -1` 并把自己的 key 输出给 parent，parent 直接从 subagent 的返回值解析 key。

> **推荐 C**：最可靠，不依赖时间假设。

### 4.3 subagent 执行失败

**场景**：subagent 崩溃或超时，mirror.sh 没有正常执行。

**处理**：
- Cron 消息显式要求 subagent 输出 `MIRROR_TEST_DONE` 作为完成标志
- 若 parent 未收到 `MIRROR_TEST_DONE`，不进入阶段三，输出 `PERF_TEST_FAILED`
- parent 的 delivery=announce 会把错误信息推送给用户

### 4.4 subagent 额外开销

**问题**：subagent 的 `totalTokens` 包含了 subagent 自身的 overhead（agent 启动、系统 prompt 等），这部分不是 device-mirror skill 的真实开销。

**影响分析**：
- subagent 的系统 prompt 开销 ≈ agent 启动的 bootstrap tokens
- 与 parent 共享相同的 model 和 system prompt
- 理论上 subagent overhead ≈ calibration noise（相同 baseline）
- 因此 `net = subagent.totalTokens - parent_calibration_noise` 依然合理

**验证**：对比 subagent 的 `totalTokens` 与直接在 parent 运行同样任务的 `totalTokens`，差异若 < 5% 则可接受。

### 4.5 底噪误差来源

**历史问题**：calibration.json 里出现了几条 noise=34,827 的异常值，是因为标定 Cron session 的消息本身太长，把额外 tokens 计入了 calibration total。

**新方案缓解**：
- 标定在 parent 完成（parent 消息是固定的 Cron payload，token 数稳定）
- `calibrate.py save --runs 1` 只记录本次，不混历史均值
- 异常检测：若 calib_totalTokens < 15,000 or > 25,000，输出警告并跳过保存

---

## 5. 需要的代码改动

### 5.1 `snapshot.py sessions --latest-subagent`（已实现 ✅）

现状：按 `updatedAt` 降序返回最新 subagent session key。

待增强（可选）：
```python
p_sessions.add_argument("--after-ts", type=int, default=0,
    help="只返回 updatedAt > after-ts 的 subagent session（毫秒时间戳）")
```

### 5.2 `calibrate.py save` 异常范围检测（建议新增）

```python
if not (15000 <= total_tokens <= 25000):
    print(f"  ⚠️  calib_totalTokens={total_tokens} 超出合理范围 [15000, 25000]，跳过保存")
    return 1
```

### 5.3 `snapshot.py report` 支持 subagent session（现已支持 ✅）

`_read_full_session` 读取任意 `agent:main:subagent:<uuid>` key，功能不变。

唯一注意：`job_name` 字段从 Cron jobs.json 读取，subagent session 没有对应 job，会显示空。可以通过 `--skill-name` 传入覆盖。

### 5.4 Cron 消息模板规范化（新建文档）

建议在 `skills/skill-perf/` 下维护一个 `CRON_TEMPLATE.md`，存放标准 Cron 消息模板，避免每次手写时出错。

---

## 6. 测试验证计划

### 6.1 单元验证

| 验证点 | 命令 | 预期 |
|---|---|---|
| `--latest-subagent` 返回正确 key | `snapshot.py sessions --latest-subagent` | 返回 `agent:main:subagent:<uuid>` |
| subagent session totalTokens | `snapshot.py report --session <key>` | totalTokens > 0，net > 0 |
| calibration grep 精确性 | `snapshot.py sessions \| grep skill-calibration \| grep -v :run:` | 只返回 calibration session |

### 6.2 端到端验证（r11 / r12）

- 触发 Cron 测试 job（r11 @ 11:24）
- 确认 announce 收到报告
- 确认报告 totalTokens ≠ 0
- 确认 net 在合理范围（4,000 ~ 10,000）

### 6.3 多轮一致性验证

- 连续跑 3 轮（r12/r13/r14），同条件（热 cache）
- net 值标准差 < 20%
- 若标准差大，排查 subagent overhead 稳定性

---

## 7. 方案对比总结

| 维度 | v1（直接 report） | v1.5（延迟报告） | **v2（subagent）** |
|---|---|---|---|
| totalTokens=0 根因 | ❌ session 自读 | ⚠️ 后台进程可能失败 | ✅ 读已完成 subagent |
| 底噪误读 | ❌ head -3 容易拿错 | ❌ 同上 | ✅ 精确 grep |
| 实现复杂度 | 低 | 高（pending + 后台进程） | 中（消息模板改造） |
| 依赖外部机制 | 无 | 后台 Python 进程 | subagent（平台原生） |
| 可靠性 | 差 | 一般 | 好 |
| 报告延迟 | 即时（但错误） | ~30s | 即时（subagent 完成后） |

---

## 8. 遗留问题

- [ ] **subagent archive 后 sessions.json 是否保留**：需实测。若 5 分钟后 key 消失，需在 subagent 完成后立即生成报告（当前设计已是如此）。
- [ ] **解决方案 C（subagent 自报 key）**：更可靠但需要 subagent 消息里运行 `snapshot.py sessions`，增加 subagent 的 token 消耗（约 +2,000 tokens）。权衡后可选择是否启用。
- [ ] **CRON_TEMPLATE.md 维护**：避免每次手写消息时出错。
- [ ] **calibrate.py 异常范围检测**：防止坏数据写入 calibration.json。
