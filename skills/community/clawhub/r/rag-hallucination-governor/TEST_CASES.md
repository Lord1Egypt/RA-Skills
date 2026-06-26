# Test Cases

Synthetic cases only. Do not use real customer names, corpus snippets, prices, contracts, or incident details.

## TC1: Top1 Pollution

Input:

```bash
node src/generator.js --symptom "Top1相似度很高但答案经常错" --scenario "客服知识库" --quick
```

Expected:

- risk type is `Top1 pollution`;
- output mentions Top1/Top2 conflict or evidence consistency;
- output includes a reject/refuse/handoff condition.

## TC2: Citation Coverage Gap

Input:

```bash
node src/generator.js --symptom "引用了错误政策但看起来有出处" --scenario "企业制度问答" --quick
```

Expected:

- risk type is `Citation coverage gap`;
- output mentions sentence-level or key-claim citation coverage;
- output refuses or hands off when key facts cannot be bound to evidence.

## TC3: Query Rewrite Drift

Input:

```bash
node src/generator.js --symptom "query rewrite 后把门店退款问题扩成了通用财务制度" --scenario "零售门店问答" --quick
```

Expected:

- risk type is `Query rewrite drift`;
- output mentions rewrite drift or pre/post rewrite retrieval comparison;
- output asks for clarification or routes away from direct answer when scope changes.

## TC4: Permission Or Scope Mismatch

Input:

```bash
node src/generator.js --symptom "不同租户知识库串了，回答引用了别的部门资料" --scenario "企业内部知识助手" --quick
```

Expected:

- risk type is `Permission or scope mismatch`;
- output mentions tenant, department, ACL, or scope guard;
- output treats this as a refusal/handoff condition, not a normal low-confidence answer.

## TC5: Evidence Version Conflict

Input:

```bash
node src/generator.js --symptom "同一个政策新旧版本冲突，模型把两个版本混在一起回答" --scenario "企业制度问答" --quick
```

Expected:

- risk type is `Evidence conflict`;
- output mentions version, scope, or conflict resolution;
- output asks for clarification or human routing when conflict cannot be resolved.

## TC6: Low-Confidence Hard Answer

Input:

```bash
node src/generator.js --symptom "召回分数低且证据分散，但系统还是硬答" --scenario "销售知识助手" --quick
```

Expected:

- risk type is `Low-confidence hard answer`;
- output mentions answer, clarify, or refuse bands;
- output routes to human when evidence is below threshold or unrelated.
