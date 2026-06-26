> 🔴 元规则：禁止伪造结果 | 禁止连段执行(本段结束必须⏸️) | 禁止抛选择题
> 🔴 V3.5.2禁止行为：禁止直接写gate/output/state文件 | 禁止import orchestrator | 禁止跳过orchestrator
> 📋 来源：SKILL.md 段落4 | 版本 V4.9.0

## 前置依赖
- 段落3已完成：P0+P1+P2全部通过，P0P1报告已发送
- Gate: P2 gate pass必须存在
- P5使用代码自动合并，Agent只需执行一条命令

---

**🔴 段内规则**: P3和P4在段落4内部并行执行（不需逐个等用户确认），段落4的确认点在P5自动合并完成后（见下方⏸️标记）。段落边界才需要用户回复「继续」。

用户确认后执行:

**🔴 段间验证:**
```
exec: python3 "$ORCH" --action status
```
确认P2的gate pass存在。

**⚡ P3和P4互不依赖,必须并行执行(同时进行,省3-4分钟):**

并行分支1 - **执行P3(风险识别):**
```
exec: python3 "$ORCH" --action prep_prompt --step P3
```
→ 读取P3 prompt → 生成JSON → write到p3_agent_output.json
```
exec: python3 "$ORCH" --action step_run --step P3
```

并行分支2 - **执行P4(PCI识别):**
```
exec: python3 "$ORCH" --action prep_prompt --step P4
```
→ 读取P4 prompt → 生成JSON → write到p4_agent_output.json
```
exec: python3 "$ORCH" --action step_run --step P4
```

❗ **并行要求**:P3和P4的4条命令(2条prep_prompt + 2条step_run)必须同时发起,不等其中一个完成再执行另一个。若任一步骤失败,立即停止,不执行P5合并。

**⚡ V4.1.1 并行失败处理机制:**

也可使用一条命令执行P3+P4并行(推荐,内置完整失败处理):
```
exec: python3 "$ORCH" --action p3_p4_parallel
```

失败处理规则:
1. **任一失败→立即停止**: P3或P4任一步骤失败,另一个立即标记为"跳过",不进入P5合并
2. **失败日志聚合**: 输出包含失败步骤名、失败阶段(prep_prompt/step_run/timeout)、失败原因、耗时
3. **资源自动释放**: 无论成功失败,finally块自动清理所有.tmp.json临时文件
4. **重试指引**: 失败时输出`restart_from P3`重试命令

失败时输出示例:
```json
{"status":"failed","failure_log":[{"step":"P3","status":"failed","reason":"..."}],"can_proceed_to_p5":false}
```

**⚡ P3+P4完成后自动执行P5合并(无需用户确认):**

**🔴 段间验证:**
```
exec: python3 "$ORCH" --action status
```
确认P2/P3/P4的gate pass存在。

**🔴🔴🔴 P5由代码自动合并,Agent绝对不参与!**
- Agent不生成P5 JSON,不写p5_agent_output.json
- Agent不调用step_run --step P5(代码层会直接拒绝)
- Agent只执行下面这一条命令,然后等结果:

```
exec: python3 "$ORCH" --action p5_code_merge
```
→ orchestrator自动读P2+P3+P4→代码合并→写入P5→gate pass
→ 🔴 **"P5自动"仅指执行P5不需要用户确认，不等于段落4→段落5自动过渡。段落边界必须等待用户回复「继续」。**

**❌ 以下操作全部禁止(代码层硬控,会被拒绝):**
```
# 禁止!会被orchestrator直接拒绝
exec: python3 "$ORCH" --action step_run --step P5
# 禁止!Agent不能自己写P5
write: p5_agent_output.json
write: p5_output.json
# 禁止!Agent不能用Python脚本生成P5
exec: python3 -c "..."
# 禁止!Agent不能伪造gate pass(V3.2.6 HMAC验签会拒绝)
write: gates/P5.pass.json
```

**🔴🔴🔴 段落4段末验证（P5自动完成后逐项检查，全部通过才输出收尾）:**
→ exec: python3 "$ORCH" --action status
  确认 step0/P0/P1 gate pass 存在
→ exec: python3 -c "import json; d=json.load(open('{data_dir}/p3_output.json')); assert d.get('risk_points'), 'risk_points缺失'"
  确认 p3_output.json 包含 risk_points
→ exec: python3 -c "import json; d=json.load(open('{data_dir}/p4_output.json')); assert d.get('pci_list'), 'pci_list缺失'"
  确认 p4_output.json 包含 pci_list
→ exec: test -f "{data_dir}/gates/P5.pass.json" && echo "P5.pass.json exists" || (echo "P5.pass.json missing" && exit 1)
  确认 gates/P5.pass.json 存在
→ 如任一检查失败,必须重新执行对应步骤,禁止跳过进入段落5

**段落4收尾输出（P5自动完成后展示）:**
```
[自动] P3+P4完成 | 风险:Y条 | PCI:Z条
[自动] P5测试点合并完成(代码自动执行)
📋 请回复「继续」进入用例生成
```

⏸️ **段落4完成。必须等待用户回复「继续」后，才能进入段落5。禁止自动跨段。**
---
🔴🔴🔴 本段执行完毕 → ⏸️ 停止 → 等待用户回复「继续」
🔴 禁止继续读取 rules/paragraph_5.md 或 SKILL.md 后续内容
