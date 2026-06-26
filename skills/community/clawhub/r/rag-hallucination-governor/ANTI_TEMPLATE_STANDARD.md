# Anti-Template Standard

This Skill exists to govern hallucination risk in production RAG systems. It must produce operational judgment, not generic RAG education.

## Do Not Produce

- 泛泛 RAG 科普：不要解释“什么是 RAG”“向量库是什么”“Embedding 原理”这类入门内容，除非用户明确要求。
- 空洞模板：不要输出只有标题、口号、占位符的治理方案；每条建议必须能落到阈值、路由、召回、重排、转人工或观测指标之一。
- 客户隐私数据：不要引用、复述或硬编码具体客户名、项目报价、合同条款、真实工单、真实知识库片段、私有指标。
- 伪精确结论：不要在没有输入证据时给出“准确率提升 37%”“幻觉率下降到 1%”之类数字。
- 单点万能解：不要把所有问题都归因于模型、Prompt、向量库或某一个阈值。

## Required Output Standard

Every recommendation should answer:

1. What signal triggered the risk?
2. What production failure may happen?
3. Which control should be changed?
4. What metric should be watched after the change?
5. When should the answer be refused or routed to a human?

## Privacy Boundary

The rule source may abstract from 10+ production RAG engagements, but must stay at pattern level:

- Allowed: "high-similarity wrong Top1 often suppresses correct lower-ranked evidence."
- Not allowed: "Client X had quote Y and knowledge item Z causing issue W."
- Allowed: synthetic test cases and anonymized retrieval shapes.
- Not allowed: real customer corpus snippets, named incidents, pricing, account strategy, or implementation secrets.

## Production Bias

Prefer controls that can be tested in logs:

- threshold tuning with reject bands;
- Top1 pollution detection;
- dual-hit conflict checks;
- intent-aware retrieval routing;
- low-confidence human handoff;
- answer grounding and citation coverage checks.

## ToB Experience Source Mix

This skill is worth building only if the output is driven mainly by field patterns, not generic RAG knowledge.

Current source mix target:

- Field patterns: 70%
  - high-similarity wrong Top1 suppressing correct lower-ranked evidence;
  - citation-looking answers where key claims are not actually covered by cited chunks;
  - multiple policy or SOP versions retrieved together and blended into a synthetic answer;
  - query rewrite expanding a narrow business question into the wrong scope;
  - permission or tenant scope mismatch producing answers from the wrong knowledge slice;
  - low-confidence answers that should have been refused or handed off.
- General model knowledge: 30%
  - common RAG vocabulary;
  - generic threshold/retrieval/rerank terminology;
  - common observability terms.

If future rules cannot be traced to a field failure pattern, keep them out of the main rule set or mark them as generic background.

## Required Control Types

Every rule should map to at least one concrete control:

- retrieval threshold or reject band;
- rerank or evidence consistency check;
- citation coverage check;
- routing or intent classification change;
- permission/scope/version guard;
- refusal, clarification, or human handoff;
- metric or log field to observe.
