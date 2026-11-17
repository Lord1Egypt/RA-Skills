# Semantic evaluation: invented cases

These cases test the host analyst, not a keyword matcher. They are entirely invented and contain no real user accounts, quotations or market evidence. Run them when changing the analysis instructions or adapting to a new field. Do not call a paid model or network API merely to execute an evaluation.

## Procedure

Give the host the case text and ask for: speaker, task, statement type, warranted claim, unsupported inference, counterexample and next test. Have an independent reviewer compare the answer with the expected boundary below. If a second reviewer is unavailable, label the result a self-review.

Record case ID, answer, reviewer, pass/fail per required boundary, and correction. Passing unit tests does not count as passing these cases. Do not count a case as successful without an actual evaluated response.

| ID | Invented evidence | Expected boundary |
| --- | --- | --- |
| P1 | Editor: “I spend 60% of my own editing time checking transcript versions.” | Personal time share. One speaker. Not 60% of editors and not a market prevalence estimate. |
| P2 | Viewer: “You could build an automatic revision checker. I have never used one.” | Suggestion, with explicit non-use. No actual adoption, effectiveness or payment. |
| P3 | Operator: “Our studio pays 18 dollars a month. I use the app but I do not choose or pay for it.” | Reported employer payment. Operator and payer differ; buyer is not identified. No independently verified transaction. |
| P4 | Solo creator: “The labels in my editor are enough. I would not pay for another app.” | Explicit sufficient alternative/nonpayment counterexample. Narrow by solo-workflow context, not all editors. |
| B1 | Mechanic: “I wish customers could see the approved parts list before I order.” | Explicit wish and task. No evidence the mechanic implemented it or will pay. A question/wish is still valid research input. |
| B2 | Viewer: “You could attach a QR code to every bike; I have not tried that system in a workshop.” | Advice by a different speaker. Must not become the mechanic's actual workaround. |
| B3 | Builder: “I built a repair sheet, then stopped updating it during busy shifts. An old status caused an unnecessary call.” | Actual self-build followed by abandonment and harm. A detailed tracking feature may fail through update burden; preserve the adverse outcome. |
| B4 | Small shop: “A whiteboard is enough for four bikes at a time.” | Sufficient existing solution for the stated scale. Do not discard it for lacking payment or a complaint. |
| C1 | Parent: “The public demo uses mock orders.” Reply: “It worked for me.” | Parent changes meaning. No evidence of production use, real orders, or a purchase. |
| C2 | Two records share one platform and one author; a third platform has the same handle. | First two are one known platform-scoped author. The cross-platform handle is not a confirmed identity match. Unknown authors are not additional known people. |
| C3 | A current reply points to a six-month-old account of abandoning a tool. | Historical evidence can be context, but not automatically current behavior. Seek follow-up before claiming they still abandoned it. |
| C4 | Ten transcripts from one tutorial creator promote a tool. Two customer discussions report a different workflow. | Transcript segments and views do not create independent customers. Source volume must not silence the customer cases. |
| C5 | The transcript fetch succeeded with empty text, or a comment crawl stopped at a page cap. | Transport success is separate from useful text and collection completeness. A source gap is unknown, not zero demand. |
| C6 | The final report has correct quotes but drops B3 and P4 from its product recommendation. | Fail the synthesis: important contrary findings were lost. Require explicit destination or justified deferral. |

## Review outcomes

Critical failures: wrong speaker or project; wish/advice presented as behavior; personal percentage presented as a group rate; fabricated quote or payment; missing parent changes meaning; false full-reading claim; omitted contrary evidence changes the decision.

Useful correct answers remain decisive: name the best supported target/task, explain what is still uncertain, and propose a concrete test. An answer that only adds generic caveats without advancing the decision also needs revision.

The offline test suite deliberately includes a semantically wrong `reported_behavior` label with an exact quote that passes structural validation. That test records the validator's limit, not approval of the label.
