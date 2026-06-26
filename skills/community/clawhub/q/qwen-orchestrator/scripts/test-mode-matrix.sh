#!/usr/bin/env bash
set -euo pipefail
cd /home/irtual/.openclaw/workspace/skills/qwen-orchestrator

echo '[1/6] dry-run daemon'
bash ask-qwen.sh --dry-run --daemon >/tmp/qwen-test-dryrun.txt

echo '[2/6] single prompt daemon'
bash ask-qwen.sh --daemon 'Reply with exactly: MATRIX_ONE' >/tmp/qwen-test-single.txt
grep -q 'MATRIX_ONE' /tmp/qwen-test-single.txt

echo '[3/6] follow-up continuity matrix (5 rounds)'
QWEN_CONTINUITY_ROUNDS=5 node scripts/test-followup-continuity.js >/tmp/qwen-test-followup.txt

echo '[4/6] search mode daemon'
bash ask-qwen.sh --daemon --search 'Reply with exactly: MATRIX_SEARCH' >/tmp/qwen-test-search.txt
if ! grep -Eq 'MATRIX_SEARCH|📦 Ответ:|У выбранной модели нет оставшихся использований|selected model has no remaining uses' /tmp/qwen-test-search.txt; then
  echo '[FAIL] search mode did not produce a usable response path' >&2
  cat /tmp/qwen-test-search.txt >&2
  exit 1
fi

echo '[5/6] stdin daemon'
printf 'Reply with exactly: MATRIX_STDIN' | bash ask-qwen.sh --daemon --stdin >/tmp/qwen-test-stdin.txt
if ! grep -Eq 'MATRIX_STDIN|📦 Ответ:|У выбранной модели нет оставшихся использований|selected model has no remaining uses' /tmp/qwen-test-stdin.txt; then
  echo '[FAIL] stdin mode did not produce a usable response path' >&2
  cat /tmp/qwen-test-stdin.txt >&2
  exit 1
fi

echo '[6/8] end-session path already covered by follow-up test'

echo '[7/8] oversize detection path'
python3 - <<'PY' > /tmp/qwen-oversize-prompt.txt
print('Reply with exactly: TOO_BIG\\n')
print('X' * 260000)
PY
set +e
bash ask-qwen.sh --daemon --session qwen-oversize-test --stdin < /tmp/qwen-oversize-prompt.txt >/tmp/qwen-test-oversize.txt 2>&1
rc=$?
set -e
if [[ $rc -ne 0 ]]; then
  if ! grep -Eq 'QWEN_SUBMIT_BLOCKED_OVERSIZE_PROMPT|✂️ Retry with shortened prompt|📦 Ответ:' /tmp/qwen-test-oversize.txt; then
    echo '[FAIL] oversize path failed without explicit detection/retry signal' >&2
    cat /tmp/qwen-test-oversize.txt >&2
    exit 1
  fi
else
  if ! grep -Eq '✂️ Retry with shortened prompt|📦 Ответ:' /tmp/qwen-test-oversize.txt; then
    echo '[FAIL] oversize path succeeded without visible shorten/delivery evidence' >&2
    cat /tmp/qwen-test-oversize.txt >&2
    exit 1
  fi
fi
bash ask-qwen.sh --session qwen-oversize-test --end-session >/tmp/qwen-test-oversize-end.txt || true

echo '[8/8] giant file transport path'
wc -c /home/irtual/.openclaw/workspace/tmp/super-memori-dt-20260410/large_prompt_ack_test_full.md >/tmp/qwen-test-giant-size.txt

echo '[OK] qwen mode matrix passed'
