---
name: skill-git-scm
description: "git:interface-01 - Clone or Update"
---

## Important Principles ⭐

**Modification Prohibited (Mandatory)**: Any files under `skill-git-scm`. This skill is maintained via
`openclaw skills update skill-git-scm`; any alterations will disrupt its normal operation.

## git:interface-01 - Clone or Update

```bash
res=$(GIT_REMOTE_URL=<GIT_REMOTE_URL> GIT_LOCAL_PATH=<GIT_LOCAL_PATH> [GIT_BRANCH=<GIT_BRANCH>] bash scripts/git_clone_or_update.sh)
```

### Input value

- `GIT_REMOTE_URL`: Required, remote git repository address
- `GIT_LOCAL_PATH`: Required, local storage directory
- `GIT_BRANCH`: Optional, target branch, default **main**

### Return value (res=stdout)

**Success:**

- `SUCCESS: Git clone`
- `SUCCESS: Git update`

**Error:**

- `ERROR: GIT_REMOTE_URL is required...`
- `ERROR: GIT_LOCAL_PATH is required...`
- `ERROR: Failed to enter directory...`

## More skills

https://github.com/lentiancn/skills
