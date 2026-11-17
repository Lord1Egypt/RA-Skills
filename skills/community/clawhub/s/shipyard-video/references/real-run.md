# Real run (advanced, Mac only)

A real run is a screen recording of something really happening, for example a coding agent fixing a bug in a small demo site and deploying it live, while a pre-recorded call plays. Use it only when the student needs that proof. Everything else is a harness (`references/footage.md`): faster, repeatable, no real accounts. Tell the student it takes a quiet hour at the computer with them signed in, plus the editing.

Read the engine's own section on real runs in `<appDir>/video/README.md` first. The tools are in `video/capture/screen-take/` (`rec.sh`, `play.sh`, `mark.sh`), `video/src/screen.tsx` (the editor) and `video/scripts/scan.mjs`.

## 1. What it needs

- **A separate demo site**, never the student's real app or real data: its own small repo and deploy (a static page with one bug and a test). Its `CLAUDE.md` holds the deploy and check steps. Its `.claude/settings.json` allows only the tools needed, so no permission question appears on camera. Add media files to `.git/info/exclude`: personal files can land in the folder during a take, and an agent might save them to GitHub. A page that reloads itself when its code changes shows the deploy landing.
- **The student at the keyboard** for what only they may do: signing in, Do Not Disturb on, Stage Manager off. You never type their passwords. When they must click something, give the exact clicks (for example Chrome's zoom from its menu: a keyboard shortcut opened Siri).
- **Pre-recorded voices** for the people in the story: `video-voice.mjs <appDir> --clips <spec>` (SKILL.md step 3), played through the speakers with `play.sh`.
- **A director: you.** Play the next clip only once the agent has done its part. Wait for the page to change with one long check instead of many small ones, check the live site until the deploy lands, and log each moment with `mark.sh`.

## 2. The take

1. Arrange the windows (AppleScript `set bounds of w to {...}`), then take a screenshot (`screencapture -x`) and look at it before recording. Hide private things: the browser's tab strip, sidebars with real data, other windows.
2. A coding agent on camera: start it with a clean environment (`env -i HOME=... PATH=... <cli>`) so it does not inherit another chat's settings; use a current version (an old one on PATH showed old models); turn off plugins and status lines that would show, in the demo folder's `.claude/settings.local.json`. Type its command into the running terminal once its tools are connected: a command given at start-up ran before they were ready.
3. `rec.sh <out.mp4>` records the whole screen until `pkill -INT -f avfoundation`. `rec.sh`, `play.sh` and `mark.sh` write the exact times to `take.log`, so the clean clip sound can be placed exactly where it was heard.
4. One take, start to end. If something goes wrong, reset the demo site and record again: never fake a step.

## 3. The edit

- Crop the menu bar off and re-encode with `-g 15 -bf 0` (exact seeks), then put the file in `video/public/capture/`.
- `src/screen.tsx`: `makeEdit(PIECES)` says which part of the recording plays when (cuts, and speed-ups that `SpeedBadge` marks "▶▶ ×N"); `Pane` shows one window of the recording in a slot of the video, with camera moves and rings. Place the clean clip sound with `<Html5Audio trimBefore trimAfter>` at `edit.outOf(piece, logged second)`.
- While an agent drives Chrome, Chrome shows a "started debugging this browser" bar that pushes the page down and comes and goes. `node scripts/scan.mjs <recording> <x,y,w,h>` (inside `video/`) prints when it appears; shift the pane with `dy`. Or keep browser automation out of the take.

## 4. Honesty

- **Show what really happened.** If the agent waited for a typed "go" instead of acting on a spoken approval, the video says "It waits for your go" and leaves out the spoken one. Never narrate something the take did not show.
- End card: "Narrated with an AI voice" and "A real run, sped up where marked".
