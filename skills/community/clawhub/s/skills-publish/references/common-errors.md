# Common Errors

Use this reference when the publish flow fails or remains uncertain.

## Frequent Problems

| Error | Meaning | Recommended fix |
| --- | --- | --- |
| `clawhub: command not found` | CLI missing or not on PATH | Install the CLI, then rerun the checker |
| `Not logged in` | Authentication missing or expired | Run `clawhub login` or `clawhub login --token <token>`, then confirm with `clawhub whoami` |
| slug already taken / rejected | Slug unavailable or invalid | Pick a more specific lowercase-hyphen slug |
| invalid version | Version is not semver | Use `X.Y.Z` format |
| publish succeeds but listing looks wrong | Local checks passed, but metadata or copy still needs work | Run `skill-seo` and review the live listing |

## Escalation Guidance

If the release still feels unsafe:

- stop before publishing
- explain what remains unknown
- ask for missing release inputs or policy decisions
