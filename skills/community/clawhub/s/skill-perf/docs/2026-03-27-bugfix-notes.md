# skill-perf 优化记录 — 2026-03-27

> 基于 r1~r10 共 10 轮 html-extractor 实测，发现并修复了多个 edge case。

---

## 一、问题与修复清单

### 1. `--html` 参数需要手动传，agent 容易遗漏

**现象**：生成报告时只有控制台文字输出，本地没有 HTML 文件。  
**根因**：`snapshot.py report --html` 是可选参数，agent 生成命令时经常漏掉。  
**修复**：`--html` 改为**默认开启**，新增 `--no-html` 用于禁用。

---

### 2. `--calib-key` 参数完全没有生效

**现象**：传了 `--calib-key` 但代码里完全忽略，仍走 `_find_calib_companion` 自动识别。  
**根因**：`cmd_report` 里接收了参数但没有任何使用逻辑。  
**修复**：实现了 `--calib-key` 优先路径——直接用传入的 calib session key 精确读取底噪，失败才回退自动识别。

---

### 3. `--calib-key` 传入的 key 末尾被截断

**现象**：`agent:main:subagent:7a3a3337-...-de90c0`（末尾 6 字符丢失），导致精确匹配失败回退自动识别。  
**根因**：agent 在生成命令文本时对 session key 做了截断。  
**修复**：`_read_full_session` 精确匹配失败时，自动尝试**前缀模糊匹配**（传入 key 为某条目前缀，或某条目为传入 key 前缀），命中时打印提示。

---

### 4. `sessions.json` 里 `totalTokens` 写入异常（OpenClaw 已知 bug）

**现象**：`totalTokens=297`，但 `inputTokens=18,610`，实际计费值应为 18,380（来自 `.jsonl`）。  
**根因**：OpenClaw 的 `sessions.json` 是事件驱动**覆盖写入**，最后一次 usage 事件的 delta 值（297）覆盖了之前的正确累计值。  
**修复**：
- `_read_full_session`：始终读取对应 `.jsonl` 文件，取 `max(sessions.json, .jsonl)`——两者取大，以 `.jsonl` 流水账为准。
- `wait_and_report.sh`：轮询读到的 `totalTokens < inputTokens * 0.5` 时，回退读 `.jsonl`。

---

### 5. calib session 在 `sessions.json` 被清走后无法找到

**现象**：报告生成时 calib session 已从 `sessions.json` 消失（OpenClaw 约 5 分钟后清除），`_find_calib_companion` 返回空。  
**根因**：原逻辑只搜 `sessions.json`，不查历史文件。  
**修复**：扩展 `_find_calib_companion` 同时搜索 `{sessionId}.jsonl.deleted.*` 文件，策略：时间窗口 + 排除 test 自身 + 取 `totalTokens` 更小的那个作为 calib。

---

### 6. `sessions.json` 找不到 session，且 `fallback_session_id` 未传

**现象**：test session 已清走，直接调 `snapshot.py report --session <key>` 无法恢复数据。  
**根因**：fallback 路径要求传 `--session-id`（sessionId UUID），但 agent 有时不传。  
**修复**：`_read_full_session` 的 fallback 路径会自动从 `session_key`（格式 `agent:x:subagent:{uuid}`）里提取 UUID 作为 fallback，无需 agent 显式传 `--session-id`。

---

### 7. 旧版 `wait_and_report.sh` 用 `--noise` 参数（已废弃）

**现象**：脚本用 `--noise "$calib_t"` 传底噪，但 `--noise` 已从 `snapshot.py` 删除。  
**修复**：改为 `--calib-key "$CALIB_KEY"`，同时脚本在启动时就保存两个 subagent 的精确 session key。

---

## 二、数据可信度提升效果

| 场景 | 修复前 | 修复后 |
|------|--------|--------|
| sessions.json 写入 bug | 报告用错误值（如 297），报告失败或数据错误 | 自动从 .jsonl 修正，打印提示 |
| session 被清走 | 报告生成失败 | 从 .deleted 文件恢复，正常生成 |
| calib key 截断 | 回退自动识别，可能匹配错 calib | 前缀模糊匹配，正确找到 session |
| 忘传 --html | 只有控制台输出，无 HTML 文件 | 默认总是生成 HTML |
| 忘传 --session-id | fallback 失效，报告失败 | 自动从 session_key 提取 UUID |

---

## 三、核心文件变更

| 文件 | 改动摘要 |
|------|---------|
| `scripts/snapshot.py` | `_read_full_session`：前缀模糊匹配 + .jsonl 对比取大值；`--calib-key` 真正生效；`--html` 默认开启；fallback 自动提取 UUID |
| `scripts/wait_and_report.sh` | `--noise` → `--calib-key`；totalTokens 合理性校验 |
| `SKILL.md` | Step 3 示例更新（`--calib-key`，删除 `--html`，说明默认行为） |

---

## 四、后续关注点

- **calib 底噪偏低（r10 出现 14,331 vs 正常 ~18k）**：原因为 calib subagent 那次运行的 bootstrap context 和 test 有差异，导致底噪不具可比性。下次测试若仍偏低，需排查 calib task 描述是否触发了不同的 skill 加载路径。
- **单次测量置信度**：net 消耗 < 5% 时建议多轮（≥3次）取中位数排除底噪抖动。
