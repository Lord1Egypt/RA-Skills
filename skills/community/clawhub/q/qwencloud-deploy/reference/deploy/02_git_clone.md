# Git Clone (Step 2)

Execute this step only when the user input is a Git URL. Skip for local projects.

---

## Invocation

```bash
git clone [--branch <ref>] --depth 1 <url> /tmp/qwencloud-clone-$(date +%s)
```

---

## URL Format

Supports `url#branch` suffix for branch/tag:

| Input | Parsed Result |
|-------|---------------|
| `https://github.com/user/repo` | Clone default branch |
| `https://github.com/user/repo#develop` | `--branch develop` |
| `https://github.com/user/repo#v1.2.0` | `--branch v1.2.0` |

---

## Error Handling

| Error | Detection | Action |
|-------|-----------|--------|
| Network unreachable | `Could not resolve host` | Suggest checking network |
| Repo not found | `Repository not found` / 404 | Suggest checking URL |
| Auth required | `Authentication failed` / 401 / 403 | Tell user to configure Git credentials (SSH key or token). **Never collect tokens in chat** |
| Branch/tag not found | `Remote branch <ref> not found` | Show available branches, ask user to confirm |

---

## Output

- Local project directory path (passed to step 3)

---

## Notes

- Use `--depth 1` shallow clone to reduce download size
- Private repos: only suggest configuring credentials, never collect tokens/passwords in chat
- After successful clone, proceed to step 3 (project analysis)
