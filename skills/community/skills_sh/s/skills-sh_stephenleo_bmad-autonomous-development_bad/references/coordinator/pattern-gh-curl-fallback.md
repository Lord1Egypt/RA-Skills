# gh → curl Fallback Pattern

If any `gh` command fails for any reason (TLS error, sandbox restriction, spending limit, etc.), use the curl equivalents below.

## Setup

```bash
TOKEN=$(gh auth token 2>/dev/null)
REMOTE=$(git remote get-url origin)
OWNER=$(echo "$REMOTE" | sed 's|.*github\.com[:/]\([^/]*\)/.*|\1|')
REPO=$(echo "$REMOTE" | sed 's|.*github\.com[:/][^/]*/\([^.]*\).*|\1|')
```

---

## Read operations

### gh pr list

```bash
# gh pr list --search "story-{number}" --state all --json number,title,state,mergedAt
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.github.com/repos/$OWNER/$REPO/pulls?state=all&per_page=100" | \
  python3 -c "
import sys, json
for p in json.load(sys.stdin):
    if 'story-{number}' in p['head']['ref']:
        print(p['number'], p['title'], p['state'], p.get('merged_at') or '')
"
```

### gh pr view

```bash
# gh pr view {pr_number} --json number,title,mergeable,mergeStateStatus,state,mergedAt
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.github.com/repos/$OWNER/$REPO/pulls/{pr_number}" | \
  python3 -c "
import sys, json; p = json.load(sys.stdin)
print('number:', p['number'])
print('state:', p['state'])
print('mergeable:', p.get('mergeable'))
print('mergeStateStatus:', p.get('merge_state_status'))
print('mergedAt:', p.get('merged_at'))
"
```

### gh pr checks

```bash
# gh pr checks {pr_number}
SHA=$(curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.github.com/repos/$OWNER/$REPO/pulls/{pr_number}" | \
  python3 -c "import sys,json; print(json.load(sys.stdin)['head']['sha'])")

curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.github.com/repos/$OWNER/$REPO/commits/$SHA/check-runs" | \
  python3 -c "
import sys, json
for r in json.load(sys.stdin).get('check_runs', []):
    print(r['name'], r['status'], r.get('conclusion') or 'pending')
"
```

For polling (replacing `gh pr checks --watch`): call the above in a 30-second sleep loop until all `status` values are `completed`.

### gh issue list

```bash
# gh issue list --search "Story {n}:" --json number,title,state
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.github.com/repos/$OWNER/$REPO/issues?state=all&per_page=100" | \
  python3 -c "
import sys, json
for i in json.load(sys.stdin):
    if 'Story {n}:' in i['title']:
        print(i['number'], i['title'], i['state'])
"
```

### gh run view

```bash
# Get latest workflow run for current branch
BRANCH=$(git branch --show-current)
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.github.com/repos/$OWNER/$REPO/actions/runs?branch=$BRANCH&per_page=5" | \
  python3 -c "
import sys, json
runs = json.load(sys.stdin).get('workflow_runs', [])
if runs:
    r = runs[0]
    print('status:', r['status'])
    print('conclusion:', r.get('conclusion') or 'pending')
"
```

---

## Write operations

`gh pr merge` has no safe curl equivalent (requires a GraphQL mutation). If `gh` is unavailable for the merge step, report the failure and ask the user to merge manually.
