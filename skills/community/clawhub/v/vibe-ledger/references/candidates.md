# How candidates are found

`start` marks places in the conversations worth reading closely. They are hints from simple rules; the ledger only records what you confirm.

## K — an error, then a change

- **Error**: a tool call that failed; command output with an error line (`Error:`, `permission denied`, `violates row-level security`, 401/403/500, CORS blocked, compile failure, a traceback); or a user saying it is broken ("报错了", "还是不行", "still not working", "blocked by CORS").
- **Window**: from the error to 20 digest records later or the end of the next user turn, whichever is earlier. Overlapping windows merge.
- **Change**: any edit, or a command that writes files or runs SQL / database tools.
- **Bypass hints** (raise priority only): `rls_disabled`, `policy_allows_all`, `cors_wildcard`, `type_check_silenced`, `verify_skipped`, `service_role_used`, `empty_catch`, `mock_data`, `commented_out`, `removed_guard` (an auth/policy/verify/check/validate/permission/require word disappeared).

## D — put off for later

User or AI text containing phrases such as for now, temporarily, placeholder, mock, hardcode, stub, in production you should, quick fix, workaround, before launch, 暂时, 先这样, 之后再, 后续再, 以后再, 临时, 写死, 模拟数据, 先跑起来, 先不管, 上线前. Code comments with TODO, FIXME, HACK, XXX, for now, temporary, mock, placeholder, hardcoded, 暂时, 临时, 写死 are listed at the end of the first pack.

## A — the AI says it did something

The last AI message of each turn when it contains phrases such as "I've added", "now protected", "is now", "已经", "已实现", "已添加", "已修复", "✅".

## What is left out

Inside each conversation, everything from the first time vibe-ledger itself runs (`vl.py start`, `check`, `render` …), or the first mention of one of its work files (`reading_pack_NN.md`, `explain_pack.md`, `*.verified.json` — what a helper writing explanations is given), onward is left out: analysing a project is not part of building it, and the analysis would otherwise show up as build history. Work done earlier in the same conversation still counts.
