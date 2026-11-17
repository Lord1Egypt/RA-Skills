# Local impact layer

Keep this record outside the public skill when it contains hostnames, private
services, installed paths, account names, or internal project links. Prefer the
workspace's existing operations or project documentation over creating another
tracker.

## Include an entry only when

- the behavior is live on this installation;
- an OpenClaw update can overwrite, invalidate, or quietly break it;
- native update status and native post-update verification do not already prove it;
- a bounded compatibility or smoke test already exists; and
- a canonical owner or recovery source is known.

Do not use the ledger as update history, a wishlist, a release-note copy, or a
generic inventory of everything attached to OpenClaw.

## Entry shape

```markdown
### <short impact name>

- State: live | temporary | blocked
- Owner: <canonical project, plugin, or procedure>
- Native coverage gap: <what the updater cannot observe>
- Affected seam: <package path, API boundary, external service, or behavior>
- Relevant when: <target/component condition>
- Pre-update gate: <smallest read-only compatibility proof>
- Post-update proof: <smallest observable behavior check>
- Recovery source: <canonical patch, project, or verified backup>
- Retire when: <upstreamed, removed, or natively covered>
- Last tested: <OpenClaw version/build and result>
```

Use placeholders in shared templates. Put real private values only in the local
record that owns them.

## Maintenance

Before an update, select entries by changed component or explicit warning rather
than running every check. After verification, update the tested baseline, keep a
specific unresolved obligation, or remove the entry. If an entry repeatedly
cannot name a bounded proof or recovery source, it is not ready to protect a
production deviation.
