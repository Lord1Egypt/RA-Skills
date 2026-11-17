# Plugin package release

Use this path for sources intended for `clawhub package publish`, including code plugins and bundle plugins. The installed CLI and current manifest schema are authoritative.

## Local review

- Require a valid `openclaw.plugin.json` when the package type needs it and a valid `package.json` for Node-distributed code.
- Check that package identity, version, entrypoints, exports, files, compatibility metadata, and license agree across manifests.
- Confirm every declared entrypoint and bundled skill exists with exact case.
- Review build output and source maps for secrets, local paths, oversized dependencies, and undeclared generated files.
- Inspect install/build/publish lifecycle scripts. Do not execute them during review without approval.
- Reject missing declared entrypoints and reconcile identity, version, exports, `files`, and bundled-skill paths across manifests before dry-run.
- Review non-registry and mutable Git dependencies, executable/native files, archives, and source maps explicitly.
- For bundles, verify each included skill independently and ensure the bundle does not shadow unrelated names.
- For code plugins, identify native binaries, postinstall behavior, network access, subprocesses, filesystem writes, and host permissions in the release report.

Do not classify code versus bundle from directory names. If manifests do not state it clearly, keep the result as `plugin-package` and let the current CLI dry-run provide the decisive validation.

## Command construction

Consult `clawhub package publish --help` before use. A typical current shape is:

```bash
clawhub package publish <source> --dry-run
```

Some CLI versions may take version, metadata, or artifact options from manifests rather than flags. Do not copy Skill-only flags onto package publishing commands.

Run the exact same source through dry-run and final publication. If a build is required, record its command, tool versions, resulting file list, and digest; any rebuild invalidates prior confirmation. Immediately before publication, repeat the dry-run and require the source digest, account, target, version, and remote baseline to match the confirmed plan.

## Verification

Confirm the immutable version, artifact digest when exposed, manifest metadata, compatibility range, package type, included skills or entrypoints, tags, and scan state. Installation or activation is a separate mutation and requires its own authorization.
