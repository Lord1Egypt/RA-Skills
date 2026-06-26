# LDM Dev Tools Jobs

Shell scripts that power the LDM Dev Tools.app scheduled automation. These are the same scripts bundled inside the `.app` at `Contents/Resources/jobs/`. Committed here so the logic is fully readable and auditable without installing the app.

## Jobs

### backup.sh

Daily backup. Delegates to Lesa's backup script.

### branch-protect.sh

Audits all repos in the `wipcomputer` GitHub org. Enforces branch protection on any repo missing it. Reports results.

### visibility-audit.sh

Audits all public repos in the `wipcomputer` GitHub org for missing `-private` counterparts. Uses `wip-repo-permissions-hook` CLI.

### setup-shell.sh

One-time shell environment setup for new machines. Configures:
- **tmux mouse scrolling** ... `set -g mouse on` in `~/.tmux.conf`. Trackpad scrolling works inside tmux sessions.

Idempotent. Safe to re-run.

## Usage

These scripts can be run standalone (no `.app` required):

```bash
bash tools/ldm-jobs/backup.sh
bash tools/ldm-jobs/branch-protect.sh
bash tools/ldm-jobs/visibility-audit.sh
```

Or via the macOS app wrapper (which provides Full Disk Access for scripts that need it):

```bash
open -W ~/Applications/LDMDevTools.app --args backup
open -W ~/Applications/LDMDevTools.app --args branch-protect
open -W ~/Applications/LDMDevTools.app --args visibility-audit
```

## App Source

The LDM Dev Tools.app is a minimal native macOS launcher that runs these shell scripts with Full Disk Access permissions. The app binary source is not yet committed. The automation logic lives entirely in these `.sh` files.
