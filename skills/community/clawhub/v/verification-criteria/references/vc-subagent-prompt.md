
## 完整 Prompt 模板

复制以下内容作为 `runSubagent` 的 `prompt` 参数值，替换 `{变量}` 后发送（调用时固定 `agentName = "bms-system-engineer"`）：

```
You are generating Verification Criteria (VC) for a subset of system requirements.

## 你的任务

为主Agent分派给你的那批需求逐条生成 Verification Criteria (VC)。这批需求
存放在一个独立文件中（由主Agent预先用 `scripts/split_req.py` 拆分得到），
**你需要先 `read_file` 把它读进来**，再执行 VC-First 循环。**不要等待主Agent在
prompt 里内联需求全文**——prompt 只携带文件路径。

你需要：
1. **第一步（MANDATORY）**：`read_file {requirements_file_path}` 加载本批次需求
   - 该文件顶部有自动生成的元信息行（`> Source:` / `> Domain:` / `> IDs:` / `> ID range:`），
     据此核对本批次覆盖的 ID 范围是否与下方 "本批次概览" 一致；不一致立即标注
     `⚠️ degraded: 拆分文件 ID 范围与 prompt 不符` 并以**文件内容**为准继续工作。
2. 用 `read_file` 加载下方 📁 参考文件（方法论与模板）
3. 对每条需求执行 VC-First 循环（选择模板 → 填写5元素 → Source Depth标注 → SMARTR-OC自检）
4. 将所有结果写入文件 `{output_file_path}`

## 本批次概览（主Agent预填，详细内容在文件中）

- **需求文件路径**: `{requirements_file_path}` ← **必须 read_file 此路径**
- 功能域: {functional_domain_name}
- 需求数量: {N} 条  |  ID 范围: {id_range}（如 `BMS-016..BMS-030`）

> ⚠️ 跨需求引用：若某条需求引用了**本批次之外**的 ID（如 `参见 BMS-050`），
> 不要去读原需求全文，按字面信息处理并在该 VC 的 Source Depth 标 `[A]` +
> 注明 `cross-ref to {ID} outside batch`。

## 领域上下文

- 功能域: {functional_domain_name}
- 行业: {industry_context}
- 惯例: {conventions}

## � 必须加载的参考文件（用 read_file）

按以下顺序加载，加载失败则标注 `⚠️ degraded: 缺少 {filename}` 继续工作。
其中前 5 个为**强制加载**，其余按主Agent标注选择性加载：

1. `{skill_base_path}/references/vc-output-format.md` — **输出格式契约（唯一真理源：F1-F11 硬规则 + VC 块结构 + Gate Checklist + Assumption Log + 自检清单）**（强制）
2. `{skill_base_path}/references/vc-smartr-oc.md` — SMARTR-OC 8维评分标准（强制）
3. `{skill_base_path}/references/vc-source-depth.md` — Source Depth 标注规则（强制）
4. `{skill_base_path}/assets/vc-template.md` — VC 表格模板 + 4种类型模板（强制）
5. `{skill_base_path}/references/vc-hard-gates.md` — 11条硬门控 + 全部规则（强制，**Gates 不在此 prompt 中内联，需从文件完整加载**）
6. `{skill_base_path}/references/vc-safety-patterns.md` — **仅当本批次含 ASIL/安全需求时加载**（主Agent会在下方标注 `📌 REQUIRED: vc-safety-patterns.md` 或 `⏭️ SKIP: vc-safety-patterns.md — 本批次无ASIL需求`）
7. `{skill_base_path}/references/vc-sequence-guide.md` — **仅当本批次含多场景/因果链需求时加载**（主Agent标注）
8. `{skill_base_path}/references/vc-exceptions.md` — 遇异常时加载

{reference_file_hints}

## Hard Gates & 质量标准

所有 Gates 和评分规则从 `vc-hard-gates.md` 和 `vc-smartr-oc.md` 完整加载，不在此内联。必须逐条对照执行。

## 输出格式

写入文件 `{output_file_path}`。**格式契约完全遵循 `vc-output-format.md`**（已在上方强制加载），
不在此重复——以该文件为准：§1 VC 块结构 + §2 F1-F11 硬规则 + §3 Gate Checklist + §4 Assumption Log + §5 自检清单。

**子 Agent 特有约束（F11 回传契约）**：
- ⛔ 最终回复**禁止回传 VC 全文**（反例#12），只回传 `{output_file_path}` + 统计摘要（见下方「最终输出」）
- 主 Agent 自行 `read_file {output_file_path}` 加载全文

## 行为约束

- ⛔ **禁止等待用户确认** — 一次性输出完整结果，不设 CHECKPOINT
- VC-BLOCKED → 标记 🔴 + 阻塞原因，继续下一条（不暂停、不等待）

## 最终输出

完成后，将完整的 VC 文档写入 `{output_file_path}`，并在你的最终回复中返回：
1. **输出文件路径** `{output_file_path}`（主 Agent 会自行 `read_file` 加载全文）
2. 已处理的需求数量和 ID 范围
3. VC-BLOCKED 清单（如有）
4. 平均 SMARTR-OC 分数
5. `[S]`/`[E]`/`[A]` 来源值总数（对应 Source Depth 显示条目数）

> ⛔ F11 回传契约的完整理由见 `vc-output-format.md` §2 F11。**例外**：单个
> VC-BLOCKED 的阻塞原因可内联（1 行文字），但**不是 VC 正文**。
```

---

## 变量清单

- `{N}` — 本批次需求数量，e.g. `15`
- `{output_file_path}` — 子Agent输出文件路径，e.g. `output/vc-batch-01.md`
- `{requirements_file_path}` — **本批次需求拆分文件的绝对路径**，e.g.
  `c:\AI\BMS_Requirements_5000\_vc_batches\req-split-02-电池保护功能-Battery-Protection.md`。
  由主Agent在 A.1a 步骤通过 `scripts/split_req.py` 生成（见 `vc-workflow-a.md` §A.1a）。
  子Agent**必须** `read_file` 此路径获取需求全文；**禁止**把全文复制进 prompt。
- `{id_range}` — 本批次需求 ID 范围，e.g. `BMS-016..BMS-030`（用于概览校验）
- `{functional_domain_name}` — 功能域名，e.g. `电池保护`
- `{industry_context}` — 行业背景，e.g. `汽车电子`
- `{conventions}` — 领域惯例，e.g. `ISO 26262, ASPICE`
- `{skill_base_path}` — skill 根目录绝对路径，e.g. `c:\AI\.github\skills\verification-criteria`

---

## 主Agent调度规则

### 主Agent职责

- **拆分 (A.1a)**: 读取需求文档 → 运行 `scripts/split_req.py` 按功能域拆分为独立 `.md` 文件 → 核对 ID 完整性 → 构造分派映射（split_file → domain → ids → output_file）
- **分派**: 对分派映射中每条记录调用 `runSubagent`（`agentName = "bms-system-engineer"`），prompt **只填 `{requirements_file_path}`**（拆分文件路径），需求全文不内联
- **合并**: 收集所有子Agent输出 → 拼接为完整 VC 文档
- **分层复核** (两阶段门控，由 `merge_vc.py` tiered_review 自动执行):
  - 阶段一 SMARTR-OC 抽样：8/8 → 进入阶段二 / 6-7/8 → 随机抽样 20%，1 条不一致则扩至全量 / <6/8 → 全量复核
  - 阶段二 Gate 11 格式抽查（仅 8/8 候选）：独立检测 Test Conditions/Pass-Fail 列是否误用 `; ` 而非 `<br>`，命中则降级到抽样桶（不依赖子Agent 自报告，弥补纵深防御缺口）
  - 异常检测: 任一子Agent均分偏离全局 >1.0 → 全量复核该Agent
- **覆盖率审计 (A.4)**: 主Agent独立执行
- **CHECKPOINT 展示**: 合并后一次性展示批量结果（不逐条打断）

### 主Agent合并流程

所有 `runSubagent` 返回后，主Agent执行：

> **契约对称性**：入站（主→子）prompt 只传 `{requirements_file_path}`，需求全文不内联；
> 出站（子→主）回复只传 `{output_file_path}` + 统计摘要，VC 全文不回传。主 Agent 自行 `read_file`
> 加载。任一方向打破对称性 → token 爆炸 / context 挤占。

1. **读取输出文件**：对每个子Agent的 `{output_file_path}` 执行 `read_file`
2. **合并**：将所有子文件内容拼接为主 VC 文档
3. **分层复核**（两阶段门控，由 `merge_vc.py` tiered_review 自动执行）：
   - 阶段一 SMARTR-OC 抽样：8/8 子Agent批次 → 进入阶段二 / 6-7/8 → 随机抽样 20%，1 条不一致 → 全量复核 / <6/8 → 全量复核
   - 阶段二 Gate 11 格式抽查（仅 8/8 候选）：独立检测表格 Test Conditions/Pass-Fail 列是否误用 `; ` 而非 `<br>`（违反 Gate 11），命中则降级到抽样桶。此检查不依赖子Agent 自报告，弥补“8/8 被信任跳过但格式违规漏过”的缺口
   - 异常检测: 任一子Agent均分偏离全局 >1.0 → 全量复核该批次
4. **A.4 覆盖率审计**：主Agent独立执行
5. **CHECKPOINT**：向用户展示合并结果 + 覆盖率报告
