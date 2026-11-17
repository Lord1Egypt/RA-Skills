# 报告一致性与重分析追溯

有机器摘要或已有报告需要复算时读取。普通摸底仍可只交付Markdown，不要求为运行检查器补齐整套新字段。

## 1. 两个可选检查器

在Skill目录执行，均只依赖Python标准库，读取UTF-8 JSON，不解析YAML、不读取外部证据或连接被测系统：

```text
python scripts/check-report.py report.json
python scripts/check-consistency.py report.json
python scripts/check-consistency.py report.json --checks metrics inventory reanalysis
```

- `check-report.py`保留原行为：只检查否证记录完整性。
- `check-consistency.py`默认只检查`metrics`。通过`--checks`选择适用部分，不要求一次包含三个部分；输出列出未选的检查，不声称全部核验。
- 两者退出0分别表示对应记录齐备/声明内部未发现矛盾，1表示记录缺口或矛盾，2表示输入格式、文件或运行所需资源错误；均不代表业务验收。输入上限2 MiB。
- `business_verdict`始终为`not_evaluated`。填写来源、判据或哈希不证明其真实、独立或适用；否证有效性、底线、统计区间及业务正确性仍须审核。任一工具通过都不能替代另一工具。

## 2. 按需补充的字段

### metrics：编号、比例和分母声明

- `expected_metric_ids`：本轮已选、应报告的指标编号清单，来自任务要求。缺证据项仍留一行，`value/n/numerator=null`、`verdict=insufficient_evidence`并填`caveat`，不能直接删掉。
- `metrics[].id`：只接受本包指标表的46个注册编号。行为分层、辅助计数放附录，不发明`E4-03a-behavior`等注册指标。每个编号一行，分层放附录。
- 对29项简单计数比例，填写整数`numerator`、分母`n`、`value`、`unit`及`denominator_source: {kind, reference}`。`unit=ratio`时值为0～1，`percent`时为0～100。使用未舍入值供复算（容差1e-9），展示层可另行舍入。`n=0`时`value=null`，不得写0或判满足。
- `E3-01a`分母来源类型仅接受`plan`或`admission`，须指向独立完整的计划/受理清单。将输出日志改名为plan不能使它合格；工具只核对声明，真实性与完整性需人工核查。其他来源类型可用`truth`、`audit`等明确名称。
- 其余17项涉及耗时、人时、计数、成本、配对差值或多分项，工具只要求已测值写明单位，**不自动校验单位含义、聚合或数值**，输出人工审核提示；不把资源向量压成单分。
- `verdict=satisfied`须有非空`criterion`，写明具体判据与来源；检查器只确认字段存在，不证明门槛合理，也不推导满足判定。计算成功、程序退出0或某项不变量满足均不自动成为业务达标依据。

### inventory：应检清单与实际输出

`check_inventory`包含`source_ref`、`expected_unit_ids`、`observations`；每行观察含`unit_id/status`，状态归一为PASS、FAIL、UNKNOWN、NOT_APPLICABLE，原始状态映射在报告说明。单位可以是对象×检查项×计划槽，具体粒度随任务固定。

检查器核对缺失、重复和清单外输出，分别计数四种状态；缺输出保留在预期清单内。NOT_APPLICABLE须填`reason`，UNKNOWN和N/A均不变成PASS。可选声明`all_checks_passed=true`只有在非空清单的全部预期输出均为PASS时才不矛盾。

**输出状态不等于检查正确性。** 独立期望为UNKNOWN时，输出UNKNOWN可以计E1-07a正确；仍不属于“所有输出均PASS”。FAIL状态也可能是准确发现真实异常。`all_expected_outputs_pass`只是输出状态汇总，不能解释成正确率或业务健康证明。少数工作负载检查PASS也不支持Service或整个业务健康的更大声明。

### reanalysis：原执行与修订分析分别保留

`analysis_lineage`记录同一次执行的原始分析和新分析，字段见下例：

- 固定`run_id/run_status`、被测对象引用及摘要、原始工件引用及摘要。摘要可对应已封存的manifest，报告说明它覆盖哪些二进制、组件、配置和输入；长运行应记录起止身份与变化，不能凭浮动文件名声称对象未变。
- `original/current`分别保留分析引用、分析版本和当时记录的状态；引用与版本均须不同，记录`change_reason`。原分析只读保留，不用新结果覆盖。
- 原始执行记录FAILED、修订分析PASS可以同时成立。报告写成“原执行记录FAILED，修订分析v2满足所列检查”，不能自动改写为重新执行成功或整体业务达标。
- 工具只检查字段、摘要格式和引用/版本是否分立，不读取这些引用，不验证文件保留、哈希、版本依赖或原状态。报告方须实际核对；无原工件时列追溯缺口，不补造哈希。

## 3. 可复算的合成结构示例

以下是虚构的元数据示例，无真实运行或独立验收含义。复制JSON后可用三个一致性检查一起核对；它未提供否证记录，原`check-report.py`仍会报告缺口。

```json
{
  "selfcheck": {
    "expected_metric_ids": ["E1-03b"],
    "metrics": [{
      "id": "E1-03b", "numerator": 1, "n": 2, "value": 0.5,
      "unit": "ratio", "verdict": "insufficient_evidence",
      "denominator_source": {"kind": "truth", "reference": "synthetic-truth-v1"},
      "caveat": "仅演示1/2复算，无总体达标判据"
    }],
    "check_inventory": {
      "source_ref": "synthetic-plan-v1",
      "expected_unit_ids": ["A", "B"],
      "observations": [
        {"unit_id": "A", "status": "PASS"},
        {"unit_id": "B", "status": "UNKNOWN"}
      ],
      "all_checks_passed": false
    },
    "analysis_lineage": {
      "run_id": "synthetic-run", "run_status": "FAILED",
      "subject_ref": "synthetic-subject-manifest",
      "subject_sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "raw_artifact_ref": "synthetic-raw-manifest",
      "raw_artifact_sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
      "original": {"analysis_ref": "analysis-v1.json", "analysis_version": "v1", "recorded_status": "FAILED"},
      "current": {"analysis_ref": "analysis-v2.json", "analysis_version": "v2", "recorded_status": "PASS"},
      "change_reason": "修订分析假设，仅示范结构，不代表重新执行"
    }
  }
}
```

## 4. 三个应用判例（不新增rc1裁决）

| 情形 | 正确处理 | 反例应如何变化 |
|---|---|---|
| 检出耗时51.2秒被标为E1-03b | 秒数作为辅助描述；E1-03b仍按时命中事件数/应检事件数 | 将示例比例单位改为seconds，检查器应报单位冲突 |
| FAIL=0，但有UNKNOWN、N/A或缺输出 | 同报四态与缺失清单，不宣称全部PASS；独立期望另行判检查正确性 | 将示例`all_checks_passed`改true，或删除B输出，应报声明冲突或缺失 |
| 原分析失败，修订分析通过 | 两版并列，固定原工件和被测对象身份，说明变化原因 | 把current指回original同一引用/版本，应报追溯矛盾 |
