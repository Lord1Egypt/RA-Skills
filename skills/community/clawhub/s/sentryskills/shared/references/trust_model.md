# Information Trust Model

Default hierarchy (low -> high):

1. `tool_single_source`
2. `tool_multi_source_unverified`
3. `internal_unverified`
4. `internal_verified`
5. `multi_source_verified`

Rules:

1. Single-tool-source information must not be directly elevated to high-confidence conclusions.
2. Multi-tool-source consistency does not exceed `internal_verified` unless independent internal evidence exists.
3. At least two independent source types must agree without conflicts to elevate to `multi_source_verified`.
4. Must explicitly express uncertainty when verification is impossible or conflicts exist.
5. Once context enters `sensitive/highly_sensitive`, output must pass through output guard.
