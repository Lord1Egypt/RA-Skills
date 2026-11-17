# Findings JSON

The host AI reads the packets and writes this document. The Python validator checks identities, exact snippets, selected arithmetic and reference links between findings. It does **not** decide whether a claim follows from a quote, verify a claimed review, or open raw files to check their hashes.

Complete invented examples are under `assets/demo/` relative to the skill root, or `../assets/demo/` relative to this document. Use their shape, not their findings, for real research.

## Document shape

```json
{
  "schema_version": "1.0",
  "reviewed_evidence_ids": ["reddit:t3_example"],
  "findings": [
    {
      "id": "F01",
      "title": "A concrete task problem",
      "claim": "A narrowly supported conclusion, in the user's language.",
      "status": "accepted",
      "review_status": "reviewed",
      "disposition": "include",
      "evidence": [
        {
          "evidence_id": "reddit:t3_example",
          "quote": "Paste an exact, nonempty snippet from that record here.",
          "role": "support",
          "interpretation": "reported_behavior"
        }
      ],
      "counterevidence": [],
      "counterevidence_search": "What opposing cases you actually checked.",
      "context_review": "complete",
      "context_limitations": null,
      "question_ids": ["Q03", "Q08"],
      "segment": null,
      "task": "The observed task",
      "consequence": null,
      "workaround": null,
      "buyer": null,
      "payer": null,
      "uncertainty": "What these records cannot establish.",
      "next_test": "A concrete way to test the interpretation."
    }
  ],
  "question_answers": {
    "Q03": {
      "status": "partial",
      "answer": "An answer supported by F01.",
      "finding_ids": ["F01"],
      "gap": "Which people, tasks or contrary evidence remain unexamined."
    }
  },
  "key_findings": [
    {
      "id": "K01",
      "title": "A key case to preserve in synthesis",
      "disposition": "include",
      "finding_ids": ["F01"],
      "reason": "How it affects the decision."
    }
  ]
}
```

This skeleton's quote is a placeholder; validation must fail until it is replaced by real text from the specified evidence record.

## Evidence and review

- `reviewed_evidence_ids` is the exact set actually read, including necessary parents. Omit it only when reading coverage is unknown. An empty array means zero declared reviewed records and cannot accompany citations.
- `quote` must be an exact substring of that record's `text`. Translation or paraphrase belongs in `claim` or citation `note`; retain the original quote too. Do not splice distant fragments into one supposedly verbatim quote.
- `role`: `support`, `counter`, or `context`. Context never increases supporting-author counts. Entries in `counterevidence` use `counter`.
- `interpretation`: `reported_behavior`, `wish`, `suggestion`, `question`, `reported_outcome`, `reported_payment`, `praise`, `complaint`, `secondhand`, `promotion`, or `unknown`. This is an analyst judgment; the program validates the vocabulary, not its meaning.
- A citation may include `author_id`, `platform`, `native_id`, `url`, `conversation_id`, or `parent_id`; if present these must exactly match the source record. Prefer leaving them to the renderer when redundant.
- `status`: `accepted`, `hypothesis`, `rejected`, `needs_context`, or `inconclusive`. Accepted findings require host-declared `review_status: reviewed`. Record who reviewed and how in optional `review_note`; the software cannot establish independence.
- If cited records lack parents, set `context_review: limited` and explain `context_limitations`. Do not accept a context-dependent claim until necessary context is read. A standalone account can support a narrower conclusion with a disclosed limitation.
- `disposition`: `include`, `defer`, `reject`, or `needs_evidence`. Other than `include`, supply `disposition_reason`. All findings remain visible in the destination table; rejected ideas are not silently deleted.
- Document the search for counterexamples. An empty list means none supplied, not proof that none exist.

## Statistics and quantities

`counts` is optional and only asserts deterministic values: `evidence_records`, `known_authors`, `unknown_author_records`, `conversations`, `platforms`, `counterevidence_records`. Counts refer to distinct cited supporting records, not the full market. Authors are distinct only within their platform; unknown authors are records with missing identity, not known independent people.

Use `quantities` when a number matters to the conclusion. Each entry includes the usual `evidence_id`, `quote` and `interpretation` fields:

| Kind | Required boundary |
| --- | --- |
| `personal_share` | `value` in percent, `scope: individual`, `denominator_description`; this speaker's time/budget share is not a share of users |
| `sample_fraction` | `scope: observed_sample`, `unit: records` or `known_authors`, `numerator_ids`, `denominator_ids`, `value` in percent; IDs explicitly define the observed denominator |
| `reported_cost` | Value and unit plus whose cost, time period, payer and whether self-reported |
| `reported_time` | Value and unit plus whose task and observation boundary |
| `reported_count` | Value and unit plus what was counted and in which project |

The program checks fraction arithmetic but cannot certify the semantic selection of the numerator. Every denominator member must actually have been assessed for the question before you call it a reviewed-sample fraction. Do not compute rates from a handpicked list of positive examples.

`null` means unknown. Do not replace missing role, cost, payment or score with `0`, `false`, or “no.” Use exact source quantities only when the quote supports them; the validator does not parse arbitrary language to prove numeric entailment.

## Optional scorecard

```json
{
  "dimensions": [
    {
      "name": "consequence",
      "value": 4,
      "weight": 2,
      "rationale": "Explain this human judgment and the chosen weight.",
      "evidence_ids": ["reddit:t3_example"]
    },
    {"name": "solution_feasibility", "value": null, "weight": 1}
  ],
  "total": null
}
```

Put this object in a finding's `scorecard`. Values use a 0–5 scale; positive finite weights are analyst choices. A known value needs a reason and evidence IDs. When every dimension is known, the total is the weighted mean. Any unknown dimension makes the total unknown. The score neither ranks markets automatically nor establishes willingness to pay.

## Fourteen questions and missing destinations

Use Q01–Q14 for `question_ids` and `question_answers`. Answer status is `answered`, `partial`, or `unknown`. Answered/partial entries require text and existing `finding_ids`. Unspecified questions render as unknown with a gap. Config `questions` can replace the question wording by ID, while retaining all fourteen slots.

Optional `key_findings` tracks important observations discovered before synthesis. An included entry must link to at least one existing finding; a deferred/rejected entry needs a reason. Review this inventory against the report so useful opposing evidence cannot disappear merely because it complicates a recommendation.
