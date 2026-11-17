# Changes and dependency invalidation

Maintain project state, not a growing transcript. Use the lightest evidence-preserving operation.

| Operation | Meaning |
| --- | --- |
| Insert/refine | New fact or precise evidence, with scope and provenance |
| Supersede | Accepted replacement; link old/new records |
| Contradict | Unresolved disagreement; preserve alternatives |
| Consolidate | Same fact/entity/scope/valid interval; preserve sources/exclusions |
| Link | `depends_on`, `derived_from`, `verified_by`, `affects`, `supersedes`, `contradicts` |
| Recheck | Changed dependency invalidates current reliance |
| Retire | Expired state leaves active retrieval; no inferred completion |
| Forget | Authorized content removal including owned derivatives |

## Stable facts, events, precise records

Consolidate stable descriptions sparingly. For events retain what happened, when, outcome and scope. For precise records retain span/version and numbers, units, tags and verbatim fields. Do not change table rows/order through summarization.

Separate `recorded_at` from `valid_from` / `valid_to`; leave unknown dates unknown. A correction to a mistaken historical label applies to its relevant period; do not invent a physical equipment change on the correction date.

## Propagate changed dependencies

1. Identify changed source/old-new revision or reversed decision.
2. Follow `depends_on` / `derived_from` to direct and transitive dependents. Use a visited set in programmatic traversal.
3. Mark affected current findings, acceptance statements and deliverables `needs_recheck`. Keep historical checks attached to their old revision. An old pass never validates a new artifact.
4. Inspect unrecorded dependencies when material: no graph edge does not prove independence.
5. Revalidate affected scope, bind evidence to exact inputs, then restore current status. Pending recheck is not a failed test. Do not repeat unaffected checks without cause.

Never transfer pinouts, settings or proofs across similar order codes, project names or revisions.

## Lessons

Keep isolated failures as scoped episodes. Promote procedures only with repeated or sufficiently strong direct validation. Repeated assistant summaries count as one origin. Do not edit unrelated skills or publish procedures outside authorized scope.
