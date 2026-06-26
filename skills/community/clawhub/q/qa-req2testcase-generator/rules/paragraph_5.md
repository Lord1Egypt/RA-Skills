> 🔴 元规则：禁止伪造结果 | 禁止连段执行(本段结束必须⏸️) | 禁止抛选择题
> 📋 来源：SKILL.md 段落5 | 版本 V4.11.0

## 前置依赖
- 段落4已完成：P3+P4+P5全部通过
- Gate: P5 gate pass必须存在
- P6使用**逐条生成流程**，Agent作为LLM每条独立生成

---

**🔴 核心约束:**
- ⛔ **禁止抛选择题**：任何失败后自动处理
- ⛔ **禁止子Agent执行P6**：代码层已检测，子Agent直接exit
- ⛔ **禁止跳过p6_generate_one**：每条必须走 generate_one → Agent生成 → generate_one --save
- ⛔ **禁止中途停止**：必须执行完全部TP后才 p6_merge
- ⛔ **禁止手写脚本绕过流程**：禁止直接写 tp_*.json 文件

**🚨 P6 三大红线:**

| # | 红线 | 正确做法 |
|---|------|----------|
| ⓵ | **禁止子Agent执行P6** | 主会话直接执行 |
| ⓶ | **禁止跳过LLM prompt直接套模板** | 必须走 p6_tp_list → p6_generate_one → **Agent完整阅读prompt并生成JSON** → p6_generate_one --save |
| ⓷ | **禁止手工forge gate文件** | gate只能由p6_merge自动生成，手工伪造会被HMAC验签拒绝 |

---

**🔴 段间验证:**
```
exec: python3 "$ORCH" --action status
```
确认P5的gate pass存在。

---

## 🔴 前置动作（必须先执行，禁止跳过）V4.12.2新增

**执行P6生成前，必须完成以下3步，缺一不可：**

```
Step ① 读取P6 prompt规则:
  read prompts/P6_testcase_generation.md
  → 理解步骤具体性要求、禁止词清单、期望结果量化规则

Step ② 读取P5测试点数据:
  read {DATA_DIR}/p5_output.json
  → 提取每个TP的description/related_rules/ui_elements等结构化信息

Step ③ 确认 --agent-output 参数的正确用法:
  ⛔ 禁止：传入成品用例JSON（如模板占位符"进入功能页面执行测试点"）
  ✅ 正确：让Agent作为LLM阅读prompt后生成JSON，
           --agent-output传入的是LLM基于prompt理解生成的用例
```

**🚨 --agent-output 不是"直接注入成品用例"，而是"Agent=LLM阅读prompt后的生成结果"。**
任何包含"进入功能页面执行测试点"/"验证操作结果"/"页面或数据发生相应变化"等模板短语的agent-output，
代码层会直接reject（V4.12.2占位符检测）。

---

## V4.12.1 逐条生成流程

**🔴 前置依赖：已完成上述「前置动作」3步（已读P6 prompt + P5数据 + 理解参数用法）**

```
exec: python3 "$ORCH" --action p6_tp_list
```
→ 获得 tp_list、total、model_tier、estimated_minutes

**对每个 tp_index=0,1,...,total-1 执行:**

```
Step ① 获取prompt:
  exec: python3 "$ORCH" --action p6_generate_one --tp-index {N}
  → stdout输出完整prompt（含页面路径/操作链路/UI元素/业务规则等11章节）
  → 🔴 Agent必须完整阅读prompt，不得跳过

Step ② 作为LLM生成用例JSON:
  → 基于prompt中的P5结构化信息（ui_elements/field_checklist/related_rules等）
  → 🔴 Agent即被prompt的LLM，完整阅读并生成5核心字段

Step ③ 保存:
  exec: python3 "$ORCH" --action p6_generate_one --tp-index {N} --save --agent-output '...'
  → 代码自动补全其余19列字段
  → 执行G1+G1.5+G5-intra快速检查 + V4.12.2占位符检测

Step ④ 进度报告（每5条）:
  输出"[进度] {N+1}/{total}条完成"
```

**🔴 重试规则:**
- quality_rejected时，读取issues+fix_hints → 修复 → 重新 --save
- 自动重试最多3次，不得向用户报告过程
- 连续3次失败 → remarks标注 `[GATE_ISSUE]`，继续下一条，不阻塞

**🔴 全部TP完成后必须执行:**
```
exec: python3 "$ORCH" --action p6_merge
```
→ 合并所有 tp_*.json → p6_output.json（兼容旧batch格式）

---

**🔴🔴🔴 段落5完成前强制检查:**

```
exec: python3 -c "import json; d=json.load(open('{data_dir}/p6_output.json')); assert d.get('testcases'); assert len(d['testcases'])>0"
```
→ 确认 p6_output.json 存在且非空

```
exec: python3 -c "import json; d=json.load(open('{data_dir}/p6_output.json')); smokes=[c for c in d.get('testcases',[]) if c.get('isSmoke')]; assert len(smokes)>0, '无冒烟用例'"
```
→ 确认冒烟用例 isSmoke 字段已标注

```
exec: test -f "{data_dir}/gates/P6.pass.json" && echo "P6.pass.json exists" || exit 1
```
→ 确认 gates/P6.pass.json 存在

---

检查全部通过后:
```
✅ 段落5完成 | 用例:N条 | 冒烟:M条
📋 请回复「继续」进入段落6（P7+Excel）
```

⏸️ **段落5完成。必须等待用户回复「继续」**
🔴 所有TP的p6_generate_one通过后才算本段结束
🔴 禁止继续读取 rules/paragraph_6.md
