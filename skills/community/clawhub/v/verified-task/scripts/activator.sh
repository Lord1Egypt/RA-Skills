#!/bin/bash
cat <<'EOF'
<verified-task-reminder>
Before execution, verify the output against the task specification.
Proceed only if the verdict is PASS.
Agents must not override FAIL or INDETERMINATE results.
Only a human operator may explicitly override.
</verified-task-reminder>
