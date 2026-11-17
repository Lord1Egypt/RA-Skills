# VC Output Format Specification

## 1. VC 块结构（强制）

每条 VC **必须**是一个独立的二级标题块，从 `## VC-` 开始，到下一个 `## VC-`
（或文件末尾）结束。**禁止**把多条 VC 放进一个分组标题（如 `## 1. 过充保护`）
或塞进一张大表（如 `## VC Table`）。

### 1.1 标准模板

每条 VC 严格使用以下结构（变量用 `{...}` 表示）：

```markdown
## VC-{REQ-ID} — {简短标题}

| VC ID | Linked Requirement | Verification Method | Test Conditions | Measurement Target | Pass/Fail Criterion |
|-------|-------------------|---------------------|-----------------|--------------------|---------------------|
| VC-{REQ-ID} | {REQ-ID} | {Method} | {conditions<br>换行} | {target} | {criterion<br>换行} |

**SMARTR-OC**: **{X}/8**
> ✗ {dim}: {1-line reason}   ← 仅当 <8/8 时出现，每行 ≤80 chars；8/8 时不输出此行

**Source Depth**:
- {value} [{tag}: {content}]
- {value} [{tag}: {content}]

```

### 1.2 完整示例

```markdown
## VC-BMS-0127 — 单体过充二级保护

| VC ID | Linked Requirement | Verification Method | Test Conditions | Measurement Target | Pass/Fail Criterion |
|-------|-------------------|---------------------|-----------------|--------------------|---------------------|
| VC-BMS-0127 | BMS-0127 | Test | Rig: BMS HIL + 电压模拟器<br>Temp: -40°C, +25°C, +85°C<br>Fault: Vcell 4.15V→4.25V 阶跃 | 过充检测到充电禁止指令的时间 | T(Vcell≥4.20V→禁止指令) ≤ 1s<br>N=100 fault injections, 触发率=100%<br>N=100 normal (4.15V), 误触发率=0% |

**SMARTR-OC**: **8/8** ✅

**Source Depth**:
- 4.20V [R: BMS-0127]
- ≤1s [R: BMS-0127]
- N=100 [S: vc-safety-patterns §Double-100]
- -40°C/+25°C/+85°C [S: ISO 16750-4]

```

---

## 2. 格式硬规则（违反即格式不合格）

| # | 规则 | ✅ 正确 | ❌ 错误 |
|---|------|--------|--------|
| F1 | 每条 VC 必须有独立 `## VC-{ID} — {title}` 二级标题 | `## VC-BMS-0001 — 电压采集` | 多条 VC 放进 `## 1. 过充保护` 分组下；或全部塞进一张 `## VC Table` 大表 |
| F2 | SMARTR-OC 必须独占一行：`**SMARTR-OC**: **X/8**` | `**SMARTR-OC**: **7/8**` | 作为表格列 `\| 7/8 \|`；写成 `SMARTR-OC: 7` |
| F3 | 多条件用 `<br>` 分隔 | `条件A<br>条件B<br>条件C` | `条件A, 条件B`；`条件A; 条件B` |
| F4 | Source Depth 标签**必须含具体内容** | `4.10V [R: BMS-0126]` | `[R]`（无 ID）；`[E]`（空） |
| F5 | `[E]` 无法说出具体惯例或依据 → 自动降级为 `[A]`（标准同 `vc-source-depth.md` Quick Decision Flow："能说出是哪个惯例吗？不能 → 降级为 [A]"） | `N=100 [E: binomial 95% conf → <3% → N=100]` | `N=100 [E: 行业惯例]` → 降级为 `[A]` |
| F6 | `[R]` 不带 REQ-ID → M 维度 = ✗ | `≤5mV [R: BMS-0001]` | `≤5mV [R]` |
| F7 | 8/8 时只写 `**SMARTR-OC**: **8/8** ✅`，**不输出维度行** | `**SMARTR-OC**: **8/8** ✅` | 8/8 却列出 8 个维度表格 |
| F8 | <8/8 时每行一个 `> ✗ {dim}: {reason}`，≤80 chars | `> ✗ A: 阈值待标定确认` | 输出完整 8 维评分表 |
| F9 | 文件末尾**必须**输出 Assumption Log 表（如有任何 `[A]`） | 见 §4 模板 | 有 `[A]` 但无 Assumption Log |
| F10 | **禁止输出全量 SMARTR-OC 汇总表**（把每条 VC 的 8 维展开成 `S\|M\|A\|R\|T\|R\|O\|C\|Score\|Disposition` 列，逐条列出全部 VC） | 仅在 CHECKPOINT/报告处列出 <8/8 的问题 VC；全 8/8 时一句 `全部 N 条 8/8 ✅` | 文件末尾或 CHECKPOINT 处输出 30+ 行的 8 列展开汇总表 |
| F11 | **子 Agent 最终回复只传 `{output_file_path}` + 统计摘要**；禁止回传 VC 全文 | 只返回路径 + 需求数/ID 范围/VC-BLOCKED 清单/均分/来源值数；主 Agent 自行 `read_file` 加载全文 | 子 Agent 把写入文件的 VC 正文复制一份到 `runSubagent`（`agentName: "bms-system-engineer"`）返回值 |

### 2.1 Source Depth 标签格式速查

| 标签 | 格式要求 | ✅ 正确示例 | ❌ 错误示例 |
|------|---------|------------|-----------|
| `[R]` | `[R: BMS-XXXX]` 含具体需求 ID | `4.10V [R: BMS-0126]` | `4.10V [R]` |
| `[D]` | `[D: derivation logic]` 含推导逻辑 | `BOL/MOL/EOL [D: BMS-039 "全生命周期"]` | `[D]`（空） |
| `[S]` | `[S: standard name, §clause]` 含标准名称+条款 | `FTTI [S: ISO 26262-4 §6.4.2.3]` | `[S: ISO 26262]` |
| `[E]` | `[E: convention + basis]` 含具体惯例名称和依据，**禁止仅写"行业惯例"**（标准见 `vc-source-depth.md`） | `N=100 [E: binomial 95% conf → <3% failure → N=100]` | `N=100 [E: 行业惯例]` |
| `[A]` | `[A: assumption, resolution plan]` 含假设描述+解决方案 | `100ms [A: 待整车FTTI分配确认, 暂取典型安全断开时间]` | `100ms [A: 待确认]` |

---

## 3. Gate Compliance Checklist（仅列出未通过的 Gate）

### 3.1 规则

- ⛔ **只输出未通过的 Gate**（⚠️ 或 ✗）
- 若全部通过 → 写 **一行**：`All 11 Gates: ✅ PASS`
- 禁止输出完整的 11 Gate 表格

### 3.2 模板

全部通过时：

```markdown
All 11 Gates: ✅ PASS
```

有未通过时：

```markdown
## 🔍 Gate Compliance Checklist（仅列出 ⚠️ / ✗）

| Gate | Status | Issue |
|------|--------|-------|
| Gate 4 | ⚠️ | Double-100 未满足, N=50 |
```

> 11 条硬门控的完整定义在 `vc-hard-gates.md` 中，本文件不重复。

---

## 4. Assumption Log（文件末尾，如有任何 `[A]`）

### 4.1 规则

- 文件中只要出现任何 `[A]` 标签，**文件末尾必须**输出 Assumption Log 表
- 若无任何 `[A]`，则不输出此表

### 4.2 模板

```markdown

## Assumption Log

| VC ID | Field | Assumed Value | Rationale | Resolution | Owner | Due Date |
|-------|-------|---------------|-----------|------------|-------|----------|
| VC-BMS-0126 | 充电限流精度 | ±10% | 待 BMS 标定规范定义 | 获取标定规范后更新 | SW Eng | TBD |
| VC-BMS-0128 | FTTI 裕量 | ≤100ms | 基于 BMS-0192 交叉引用 | 整车级安全概念确认后更新 | Safety Eng | TBD |
```

---

## 5. 子 Agent 输出前自检清单

输出全部 VC 后，逐条核对以下检查项。**全部通过**才能提交。

### 5.1 结构自检

- [ ] 每条 VC 都有独立的 `## VC-{ID} — {title}` 二级标题？
- [ ] **没有**用分组标题（如 `## 1. 过充保护`）替代 VC 标题？
- [ ] **没有**把多条 VC 塞进一张大表（如 `## VC Table`）？
- [ ] VC 总数 = 需求数？（一一对应，无跳过/合并）

### 5.2 SMARTR-OC 自检

- [ ] SMARTR-OC 独占一行，格式为 `**SMARTR-OC**: **X/8**`？
- [ ] 8/8 时**没有**输出维度表格？
- [ ] <8/8 时每行一个 `> ✗ {dim}: {reason}`（≤80 chars）？

### 5.3 Source Depth 自检

- [ ] 每个 `[R]` 都带具体 REQ-ID（如 `[R: BMS-0126]`）？
- [ ] 没有**空的** `[D]` / `[E]`（必须有推导逻辑/推导链）？
- [ ] `[E]` 有具体惯例名称和依据（不是仅写"行业惯例"）？无法说出具体惯例的已降级为 `[A]`？
- [ ] 每个 `[S]` 都带标准名称+条款（如 `[S: ISO 26262-4 §6.4.2.3]`）？
- [ ] 每个 `[A]` 都有假设描述+解决方案？

### 5.4 Gate Checklist 自检

- [ ] 全部通过的写了一行 `All 11 Gates: ✅ PASS`？
- [ ] 没有输出完整的 11 Gate 表格？

### 5.5 Assumption Log 自检

- [ ] 如有 `[A]`，文件末尾有 Assumption Log 表？
- [ ] 每条 `[A]` 在 Log 表中都有对应记录？

### 5.6 格式细节自检

- [ ] 多条件用 `<br>` 分隔（不是逗号/分号）？
- [ ] 没有使用主观模糊词（`良好`/`合理`/`足够`/`适当`）？

### 5.7 汇总输出自检（F10）

- [ ] **没有**在文件末尾或 CHECKPOINT 处输出全量 SMARTR-OC 汇总表（`S|M|A|R|T|R|O|C|Score|Disposition` 8 列展开，逐条列出全部 VC）？
- [ ] 汇总/CHECKPOINT 处只列出 <8/8 或非 Ready 的问题 VC；全 8/8 时仅一句 `全部 N 条 8/8 ✅`？

### 5.8 子 Agent 回传自检（F11）

- [ ] 最终回复**只包含**：`{output_file_path}` + 需求数/ID 范围/VC-BLOCKED 清单/均分/来源值数？
- [ ] **没有**在最终回复中复制 VC 正文（表格/Source Depth/Gate Checklist 等）？主 Agent 会自行 `read_file` 加载。
