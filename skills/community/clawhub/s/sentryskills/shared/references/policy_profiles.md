# Runtime Policy Profiles

The table below explains the differences between strict / balanced / permissive profiles and their recommended use cases.

| Profile | Retry Threshold (`retry_threshold_downgrade`) | Single Source Types (`single_source_types`) | High-Sensitivity Leak Handling (`block_on_highly_sensitive_leak`) | Recommended Scenarios |
|---|---:|---|---|---|
| strict | 2 | `tool_single_source`, `tool_multi_source_unverified` | true | Production high-sensitivity scenarios, strict compliance requirements |
| balanced | 3 | `tool_single_source` | true | Default recommendation, balances security and usability |
| permissive | 5 | `tool_single_source` | false | Low-sensitivity offline analysis, exploratory tasks |

## Common Rules

1. All profiles execute `preflight -> runtime -> output_guard` pipeline.
2. Explicit sensitive leakage requests may still be directly `block`ed.
3. Single-source conclusions should not provide high-confidence answers by default.

## Selection Recommendations

1. When uncertain, prioritize `balanced`.
2. If false positives are high, try `permissive` in controlled environments, but maintain audit logs.
3. Use `strict` for external production services or compliance-sensitive tasks.
