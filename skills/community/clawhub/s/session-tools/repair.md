# Session Repair

Detects and repairs structural issues in session JSONL files.

## Quick Start

```bash
/session repair                          # Select session, then validate and repair
/session repair <session_id>             # Repair a specific session
/session repair --dry-run                # Preview only, no changes
/session repair --check-only             # Validate only (no repair)
```

## Detectable Issues

### 1. Broken Chain

Treated as a broken chain if any of the following conditions apply:

1. A message with `isSidechain: false` is **missing the `parentUuid` field entirely**
2. A message has `saved_hook_context` (abnormal session termination)
3. A message has a `stop` field (forced session interruption)

**Important**: `parentUuid: null` is normal (e.g., first message). Only missing fields are problematic.

**Symptoms**: Session load failure, missing conversation history

```
msg1 (uuid: aaa, parentUuid: null)      ← Normal (null value)
msg2 (uuid: bbb, parentUuid: aaa)       ← Normal
msg3 (uuid: ccc)                        ← Problem! parentUuid field missing
msg4 (uuid: ddd, saved_hook_context: {})← Problem! Abnormal termination trace
msg5 (uuid: eee, stop: true)            ← Problem! Forced interruption trace
```

### 2. Orphan Tool Result

The `tool_use_id` in a `tool_result` block does not match any `tool_use` block in a previous message.

**Symptoms**: API Error 400
```
messages.N.content.0: unexpected tool_use_id found in tool_result blocks: toolu_xxx.
Each tool_result block must have a corresponding tool_use block in the previous message.
```

**Causes**: Message ordering issues, missing intermediate messages, or sync errors

### 3. Duplicate UUIDs

Multiple messages with the same `uuid`.

**Symptoms**: Chain tracking errors, unexpected branching

### 4. Duplicate Messages (same message.id, different UUID)

The same API response recorded multiple times with different UUIDs due to **Syncthing sync conflicts**.

**Symptoms**: Abnormally large session file, repeated identical messages

**Detection method**:
```bash
# Check duplicates by message.id
grep -o '"id":"msg_[^"]*"' session.jsonl | sort | uniq -c | sort -rn | head -10
```

**Characteristics**:
- `uuid` is different but `message.id` is identical
- `requestId` is often also identical
- progress type entries can repeat thousands of times with identical content

## Instructions

### 1. Determine Target Session

If session ID is not provided:
1. Call `mcp__claude-sessions-mcp__list_projects`
2. Ask user to select a project
3. Call `mcp__claude-sessions-mcp__list_sessions`
4. Ask user to select a session

### 2. Session File Path

```bash
~/.claude/projects/{project_name}/{session_id}.jsonl
```

### 3. Detection Order (all must be run)

1. **Detect duplicate message.id** (Syncthing conflict) — `grep -o '"id":"msg_[^"]*"' session.jsonl | sort | uniq -c | sort -rn | head -10`
2. **Detect broken chains** — jq query
3. **Detect orphan tool_results** — jq query
4. **Detect duplicate UUIDs** — jq query

**Important**: If duplicate message.ids are found, **run dedup first** before the remaining checks. Other check results are unreliable while duplicates are present.

### 4. Repair Logic

#### Remove Duplicate Messages (by message.id)

Duplicates caused by Syncthing sync conflicts:

```bash
# Preview
python scripts/dedup-session.py session.jsonl --dry-run

# Execute (creates .dedup file)
python scripts/dedup-session.py session.jsonl
```

Script: [scripts/dedup-session.py](./scripts/dedup-session.py)

**When running from Claude Code**: Reference `scripts/dedup-session.py` relative to the skill base directory

#### Repair Broken Chain

Set the `parentUuid` of the damaged message to the `uuid` of the immediately preceding message.

#### Repair Orphan Tool Result

Options:
1. **Delete**: Remove the tool_result message
2. **Attempt matching**: Find a nearby tool_use block and link them (risky)

Deletion is the safer choice in most cases.

### 5. Output Results

**Dry-run/Check-only mode**:
```
## Session Repair Preview

Session: {session_id}

| Check Item | Result |
|------------|--------|
| Duplicate message.id | 0 |
| Broken chains | 2 (1 first message = normal) |
| Orphan tool_results | 1 |
| Duplicate UUIDs | 0 |
| Total messages | 150 |

### Broken Chains (needs fix: 1)
| Line | UUID | Type | Fix |
|------|------|------|-----|
| 5 | a129f842 | assistant | → 270fe00a |

### Orphan Tool Results (needs deletion: 1)
| Line | UUID | orphan_ids |
|------|------|------------|
| 23 | 747d9a2d | toolu_01HEm... |

### Duplicate UUIDs (needs deletion: 3)
| Line | UUID | Type |
|------|------|------|
| 45 | a129f842 | assistant |
| 78 | a129f842 | assistant |
| 120 | b234c567 | user |

Run without --dry-run to apply fixes.
```

**Note**: The first user message (Line 2) in a broken chain is excluded because `parentUuid: null` is normal.

**Execute mode**:
```
## Session Repair Complete

- Backup: {session_id}.jsonl.bak
- Fixed chains: 2
- Removed orphan tool_results: 1
- Removed duplicate UUIDs: 3
- Total messages: 150 → 146
```

## Diagnostic Queries

### Quick Status Check

```bash
# File size and line count
ls -lh session.jsonl && wc -l < session.jsonl

# Distribution by type
jq -r '.type // "null"' session.jsonl | sort | uniq -c | sort -rn

# Duplicate message.id (top 10)
grep -o '"id":"msg_[^"]*"' session.jsonl | sort | uniq -c | sort -rn | head -10

# Count of duplicate message.ids
grep -o '"id":"msg_[^"]*"' session.jsonl | sort | uniq -d | wc -l
```

## jq Queries

### Broken Chain Detection

**Important**: `parentUuid: null` is normal. Detect if any of the following conditions apply:
1. The `parentUuid` field is entirely absent
2. `saved_hook_context` is present (abnormal termination)
3. The `stop` field is present (forced interruption)

```bash
# Note: after to_entries, apply has() to .value
jq -c --slurp '
  . as $all |
  to_entries |
  map(select(
    .value.isSidechain == false and
    (.value.type | test("file-history-snapshot") | not) and
    .key > 0 and
    (
      (.value | has("parentUuid") | not) or
      (.value | has("saved_hook_context")) or
      (.value | has("stop"))
    )
  )) |
  map({
    line: (.key + 1),
    uuid: .value.uuid[0:8],
    type: .value.type,
    reason: (
      if (.value | has("saved_hook_context")) then "saved_hook_context"
      elif (.value | has("stop")) then "stop"
      else "missing_parentUuid"
      end
    ),
    fix: $all[.key - 1].uuid[0:8]
  })
' session.jsonl
```

### Orphan Tool Result Detection

**Important**: Must check whether the corresponding tool_use exists anywhere in the entire file (checking only previous messages will miss matches).

```bash
# Collect all tool_use ids from the entire file, then find tool_results with no match
# Note: use type check instead of select(.value.message.content != null) (shell escape issue)
jq -c --slurp '
  [.[] | .message.content? // [] | if type == "array" then .[] else empty end | select(.type == "tool_use") | .id] as $all_tool_uses |
  to_entries |
  map(
    select(.value.message.content | type == "array") |
    select([.value.message.content[] | select(type == "object" and .type == "tool_result")] | length > 0) |
    {
      line: (.key + 1),
      tool_use_ids: [.value.message.content[] | select(.type == "tool_result") | .tool_use_id],
      uuid: .value.uuid[0:8]
    } |
    select(([.tool_use_ids[] | select(. as $id | $all_tool_uses | index($id) | not)] | length) > 0) |
    {
      line: .line,
      uuid: .uuid,
      orphan_ids: [.tool_use_ids[] | select(. as $id | $all_tool_uses | index($id) | not) | .[0:20]]
    }
  )
' session.jsonl
```

**Repair method**: Delete lines containing orphan tool_results (starting from the highest line number!)
```bash
cp session.jsonl session.jsonl.bak
# Delete from the highest line number to avoid shifting line numbers
sed -i '' '40d' session.jsonl
sed -i '' '13d' session.jsonl
```

### Duplicate UUID Detection

```bash
# Use has() — != null causes shell escape issues
jq -s '
  [.[] | select(has("uuid")) | .uuid] |
  group_by(.) |
  map(select(length > 1) | {uuid: .[0][0:8], count: length})
' session.jsonl
```

### Remove Duplicate UUIDs

**Principle**: Among identical UUIDs, **keep only the first**, delete the rest.

```bash
# 1. Backup
cp session.jsonl session.jsonl.bak

# 2. Remove duplicates (keep first)
jq -c --slurp '
  reduce .[] as $item (
    {seen: {}, result: []};
    if $item.uuid == null then
      .result += [$item]
    elif .seen[$item.uuid] then
      .  # already seen — skip
    else
      .seen[$item.uuid] = true |
      .result += [$item]
    end
  ) | .result[]
' session.jsonl.bak > session.jsonl
```

**Detailed detection** (including line numbers to delete):
```bash
jq -c --slurp '
  reduce to_entries[] as $e (
    {seen: {}, dups: []};
    if $e.value.uuid == null then .
    elif .seen[$e.value.uuid] then
      .dups += [{line: ($e.key + 1), uuid: $e.value.uuid[0:8], type: $e.value.type}]
    else
      .seen[$e.value.uuid] = true
    end
  ) | .dups
' session.jsonl
```

### Repair Broken Chain

**Important**: `parentUuid: null` is normal — do not touch. Only add the field when it is missing entirely.

```bash
# 1. Backup
cp session.jsonl session.jsonl.bak

# 2. Apply repair (only when parentUuid field is missing)
jq -c --slurp '
  . as $all |
  to_entries |
  map(
    if (.value.isSidechain == false and
        (.value | has("parentUuid") | not) and
        (.value.type | test("file-history-snapshot") | not) and
        .key > 0)
    then .value + {parentUuid: $all[.key - 1].uuid}
    else .value
    end
  ) | .[]
' session.jsonl.bak > session.jsonl
```

### Remove Orphan Tool Results

```bash
# Get the list of line numbers containing orphan tool_results, then remove them
# Complex — running the skill is recommended
```

## Repair Incorrect Split

If messages ended up in the wrong session after `split_session`, recover by direct file manipulation.

### Scenario: Move the last N messages of a session to another session

```python
# uv run python - <<'EOF'
import json, shutil
from pathlib import Path

# ~ paths must be expanded with expanduser() (Python open() does not auto-expand ~)
SRC = Path('~/.claude/projects/{project}/{wrong_session}.jsonl').expanduser()
DST = Path('~/.claude/projects/{project}/{target_session}.jsonl').expanduser()
SPLIT_IDX = 309  # starting line to move (0-indexed)

# 1. Backup
shutil.copy2(SRC, str(SRC) + '.bak')
shutil.copy2(DST, str(DST) + '.bak')

# 2. Read SRC
with open(SRC, encoding='utf-8') as f:
    src_lines = f.readlines()

keep = src_lines[:SPLIT_IDX]
move = src_lines[SPLIT_IDX:]

# 3. Find last UUID in DST (new parentUuid)
with open(DST, encoding='utf-8') as f:
    dst_lines = f.readlines()

new_parent = next(
    json.loads(l)['uuid'] for l in reversed(dst_lines)
    if json.loads(l).get('uuid')
)

# 4. Messages to move: update parentUuid + sessionId
dst_session_id = DST.stem  # remove .jsonl
modified = []
for i, line in enumerate(move):
    obj = json.loads(line)
    if i == 0:
        obj['parentUuid'] = new_parent
    if 'sessionId' in obj:
        obj['sessionId'] = dst_session_id
    modified.append(json.dumps(obj, ensure_ascii=False) + '\n')

# 5. Append to DST, shrink SRC
with open(DST, 'a', encoding='utf-8') as f:
    f.writelines(modified)
with open(SRC, 'w', encoding='utf-8') as f:
    f.writelines(keep)
# EOF
```

### Chain Validation

After moving, verify the chain in the DST file is not broken:

```bash
jq -s '[.[1:] | .[] |
  select(.isSidechain == false and
         (.type | test("file-history-snapshot") | not) and
         (has("parentUuid") | not))
] | length' dst_session.jsonl
# Result should be: 0
```

## Edge Cases

### Items to Skip
- `file-history-snapshot` type: normal even without parentUuid
- `parentUuid: null` value: normal (first message, system messages, etc.)
- `isSidechain: true` messages: separate branch, different chain rules

### parentUuid Decision Criteria
- `parentUuid: null` → **Normal** (explicitly set to null)
- `parentUuid` field missing → **Problem** (field itself is absent)

### tool_result Special Cases
- Responses to multiple tool_uses can exist in a single message
- tool_use and tool_result can exist in the same message (parallel calls)

## Validation

Validate after repair:
```bash
# 1. Check duplicate message.id (Syncthing conflict)
grep -o '"id":"msg_[^"]*"' session.jsonl | sort | uniq -d | wc -l
# Result: 0

# 2. Check broken chains (only when parentUuid field is missing)
# Note: after slurp, has() can be used directly
jq -s '[.[1:] | .[] |
  select(.isSidechain == false and
         (.type | test("file-history-snapshot") | not) and
         (has("parentUuid") | not))
] | length' session.jsonl
# Result: 0

# 3. Check orphan tool_results (re-run detection query above)
# Result: []

# 4. Check duplicate UUIDs
jq -s '[.[] | select(has("uuid")) | .uuid] | group_by(.) | map(select(length > 1)) | length' session.jsonl
# Result: 0

# 5. JSON validity
jq empty session.jsonl && echo "Valid JSON"
```

## Requirements

- claude-code-sessions MCP server (for session list lookup)
- jq (for JSON parsing)
- Write permission on session files

## Notes

### jq Shell Escape Issues
- Avoid `!=` operator → use `test() | not` or `type == "array"` pattern instead
- Use `select(.field | type == "array")` or `select(has("field"))` instead of `select(.field != null)`

### has() Placement When Using to_entries
- `to_entries` transforms to `{key, value}` form
- **Wrong**: `has("parentUuid")` → applied to the entry object, always false
- **Correct**: `.value | has("parentUuid")` → applied to the original object

### Repair Order
1. Backup first (`.bak` extension)
2. **Run `dedup-session.py`** — must run before all other repairs
   - Removes duplicates based on message.id (including streaming intermediate results)
   - Auto-deletes orphan tool_results (5th pass)
   - Auto-repairs chain (6th pass)
3. **Remove 400 error lines** — lines with `isApiErrorMessage: true` + the preceding user message
4. Remove duplicate UUIDs (keep first only)
5. **Delete orphan tool_results** — manual line removal in steps 3–4 can create new orphans
6. **Repair broken chains** — line deletions in steps 3–5 break the chain; detect with jq query then repair
7. Always run validation queries after repair

### Cautions
- Deleting orphan tool_results can affect conversation flow
- `parentUuid: null` is normal (only repair when the field itself is absent)

### Syncthing Sync Conflicts
- Syncing `~/.claude/projects/` with Syncthing can cause conflicts
- The same message gets recorded multiple times with different UUIDs
- Mainly occurs in `assistant` and `progress` types with large-scale duplication
- Diagnose with: `grep -o '"id":"msg_[^"]*"' session.jsonl | sort | uniq -c | sort -rn`
- 8x or more duplicates suggest a Syncthing conflict
