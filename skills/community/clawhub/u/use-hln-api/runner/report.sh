#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: ./runner/report.sh <benchmark.json>" >&2
}

if [[ $# -ne 1 ]]; then
  usage
  exit 1
fi

BENCHMARK="$1"

if [[ ! -f "$BENCHMARK" ]]; then
  echo "ERROR: benchmark file not found: $BENCHMARK" >&2
  exit 1
fi

timestamp="$(jq -r '.timestamp' "$BENCHMARK")"
skill="$(jq -r '.skill' "$BENCHMARK")"
model="$(jq -r '.model' "$BENCHMARK")"
judge_model="$(jq -r '.judge_model' "$BENCHMARK")"
base_url="$(jq -r '.base_url' "$BENCHMARK")"
baseline_enabled="$(jq -r '.baseline_enabled' "$BENCHMARK")"
total="$(jq -r '.summary.total' "$BENCHMARK")"
with_pass="$(jq -r '.summary.with_skill.pass' "$BENCHMARK")"
with_partial="$(jq -r '.summary.with_skill.partial' "$BENCHMARK")"
with_fail="$(jq -r '.summary.with_skill.fail' "$BENCHMARK")"
with_errors="$(jq -r '.summary.with_skill.errors' "$BENCHMARK")"
with_rate="$(jq -r '.summary.with_skill.rate_percent' "$BENCHMARK")"
base_pass="$(jq -r '.summary.without_skill.pass' "$BENCHMARK")"
base_partial="$(jq -r '.summary.without_skill.partial' "$BENCHMARK")"
base_fail="$(jq -r '.summary.without_skill.fail' "$BENCHMARK")"
base_errors="$(jq -r '.summary.without_skill.errors' "$BENCHMARK")"
base_rate="$(jq -r '.summary.without_skill.rate_percent' "$BENCHMARK")"
uplift="$(jq -r '.summary.uplift_percent' "$BENCHMARK")"
errors="$(jq -r '.summary.errors' "$BENCHMARK")"

cat <<EOF
# $skill eval results

## Run metadata

- Timestamp: \`$timestamp\`
- Model: \`$model\`
- Judge: \`$judge_model\`
- HLN base URL: \`$base_url\`
- Total evals: \`$total\`
- Errors: \`$errors\`

## Summary

- With skill: \`$with_rate%\` pass rate (\`$with_pass\` pass, \`$with_partial\` partial, \`$with_fail\` fail, \`$with_errors\` error)
EOF

if [[ "$baseline_enabled" == "true" ]]; then
  cat <<EOF
- Without skill: \`$base_rate%\` pass rate (\`$base_pass\` pass, \`$base_partial\` partial, \`$base_fail\` fail, \`$base_errors\` error)
- Uplift: \`$uplift%\`
EOF
fi

cat <<'EOF'

## Per-eval results

| Eval | Type | With skill | Without skill |
| --- | --- | --- | --- |
EOF

jq -r '
  .results[]
  | [
      .eval_id,
      .type,
      (.verdict // "ERROR"),
      (if (.baseline_verdict // "") == "" then "-" else .baseline_verdict end)
    ]
  | "| " + join(" | ") + " |"
' "$BENCHMARK"

cat <<'EOF'

## Error details
EOF

jq -r '
  .results[]
  | select((.with_error // "") != "" or (.baseline_error // "") != "")
  | "### " + .eval_id,
    (if (.with_error // "") != "" then "- With skill error: `" + .with_error + "`" else empty end),
    (if (.baseline_error // "") != "" then "- Without skill error: `" + .baseline_error + "`" else empty end),
    ""
' "$BENCHMARK"
