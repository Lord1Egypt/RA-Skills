# Release Notes: wip-ai-devops-toolbox v1.9.64

Closes #295

## Branch guard: allow extension cleanup

The branch guard blocked `rm` on deployed extension directories (`~/.openclaw/extensions/` and `~/.ldm/extensions/`) because those paths live inside git repos. But deployed extensions are managed by `ldm install`, not by hand. When a stale `-private` extension needed to be removed (e.g. `wip-xai-grok-private` replaced by the public `wip-xai-grok`), the agent couldn't clean it up without asking the user to run the command manually.

Added an allowlist pattern for `rm` targeting `.openclaw/extensions/` and `.ldm/extensions/` paths. Same approach as the existing `.ldm/state/` allowlist. The guard still blocks `rm` on actual repo source files.
