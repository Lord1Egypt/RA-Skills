# wip-release v1.9.76

Force-deploy of the 1.9.75 stderr-capture fix.

The 1.9.75 publish landed on npm correctly, but the ldm install deploy to `~/.ldm/extensions/wip-release/` skipped the file copy because `deployExtension`'s version check (`cmp <= 0` on source vs installed) saw the deployed `package.json` already at 1.9.75 and short-circuited. Net effect: deployed `package.json` reported 1.9.75, but deployed `core.mjs` was still the old 1.9.74 content (no `runNpmPublish`, no `spawnSync`). File checksums differed.

This is a latent installer bug (versions equal doesn't mean content equal), tracked separately. For now, bumping wip-release to 1.9.76 forces the version-check to trigger an actual file re-copy on the next `ldm install`.

No code change. Just `package.json` version bump and this release notes file.
