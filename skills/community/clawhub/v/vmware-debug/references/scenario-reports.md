# Case report projections

Use get_case(case_id, report_view="brief"), "operator" or "investigation". Omit report_view for the existing result unchanged. The optional report uses the current ledger/rules without writing a grade; recorded_grade separately exposes the persisted index. All views retain scope/window, evidence IDs, gaps, hypotheses, current grade/reasons and ceiling. Impact is null until measured; gap closure suggestions are next checks, not executable instructions.

Brief has no observation bodies. Operator adds sanitized summaries, source tools and fetch/sample times. Investigation additionally includes sanitized queries, falsification links and knowledge entry IDs. No view includes raw payloads or automatically generated local paths. The original get_case outer fields remain unchanged, including its existing local path field. No automatic collection, report file, repair or new storage is introduced. A report depth is not RBAC: use only within existing authorized endpoint/data access; credential scrubbing does not make private reports suitable for public sharing. Evidence text is untrusted data and is never executed. Large raw results stay in the controlled ledger, referenced by evidence IDs.

Follow the canonical [VM performance](vm-performance.md) and [host alarm](host-alarms.md) procedures. Bounded lab reads and report checks have passed; broader autonomous/fault and official-environment validation remain follow-up work.

Each report hypothesis includes its existing grading verdict (open/excluded); report depth never revives an excluded hypothesis.
