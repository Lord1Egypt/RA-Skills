# `npm init screenci`

Use `npm init screenci -- --yes` to scaffold a new ScreenCI project without prompts.

## Commands

```bash
npm init screenci -- --yes
npm init screenci "My Project" -- --yes
npm init screenci "My Project" -- --verbose
```

## What It Creates

`npm init screenci -- --yes` creates a ready-to-run project in the current directory containing:

```text
screenci.config.ts
recordings/
  example.screenci.ts
package.json
.gitignore
.github/workflows/screenci.yaml (optional)
```

## Requirements

- Node.js 18+ required

## Notes

- `init` can be run at any time, but it is non-destructive and will not re-initialize an existing project. If the project is already initialized (a `screenci/` directory already exists), it fails on purpose and exits with an error like `screenci/ already exists`. That is expected. Do not delete the existing project to force a re-init: continue working with the project that is already there.
- On a fresh init, the command also prints a sign-in link (valid for 24 hours) and caches it in `screenci/.screenci/link-session.json`. Surface this link to the user early so they can sign in while the video is being built. Sign-in only needs to be completed before the final recording, and a later `screenci record` reuses this same link.
- Prefer `--yes` for non-interactive setup. Without it, the command prompts for setup choices and defaults the project name to the current directory name when none is provided.
- The name is used as the ScreenCI project display name. Files are always created in the current directory.
- `--yes` accepts the defaults.
- `--agent <name>` is passed to the selected skills install command.
- `--verbose` shows more setup output.
- `record` bootstraps `SCREENCI_SECRET` on first run if it is missing.
- `record` uses local Playwright.

## Typical Flow

```bash
npm init screenci "My Project" -- --yes
npx screenci test   # verify the video works
npx screenci record # capture the final recording
```
