# Example: Example Orbit (made up)

A complete run of the skill on a made-up campaign: a space-photo app pays creators per 1,000 views
for a split-screen or face-plus-screen video. Every file here was written by the skill's scripts,
from NASA footage with no people in it. The creator's half is a labelled placeholder: in a real run
it is your own recording.

Read them in this order:

| Step | File | Written by |
|---|---|---|
| The brief, pasted | `brief.txt` | the creator |
| The brief as data | `campaign.json` | the agent |
| GO, NO-GO or REFUSED, and the checklist | `checklist.md` | `campaign.py` |
| Hooks, lines, claim tags | `script.json` | the agent, with the creator |
| The experience line confirmed true | `confirmations.json` | `script.py --confirm` |
| The script to read and the shot list | `script.md`, `shotlist.md` | `script.py` |
| What to edit | `edit.json` | the agent |
| One video per account, each with its hook, retakes cut | `videos/` | `make_video.py --placeholder --width 540` |
| Every check | `lint-report.md` | `check_videos.py --report` |
| The plan page with its plan id | `plan.html`, `plan.md` | `plan.py` |
| The yes, bound to the files, for 3 hours | `yes.json` | `plan.py --yes` |
| The Shorts post, by hand (written after the yes) | `by-hand/orbit-shorts.md` | `plan.py --yes` |
| The uploads, each covered by the yes | `videos/uploaded.json`, `media.json` | `upload_parts.py` |
| The WoopSocial request | `requests/` | `plan.py --media media.json` |
| After posting: the submission steps in order, the calendar file, the ledger | `after-posting/` | `plan.py --posted/--status`, `ledger.py` |

`after-posting/earnings.txt` is `ledger.py --report --min-hourly 15` on numbers marked EXAMPLE ONLY:
one video paid, one pending, one rejected and appealed, four hours logged, and the hint the report
gives while the views are still counting.

The example never posts: `plan.py --check` refuses every request of a campaign marked
`example_demo`. To run it again from this folder:

```bash
python3 ../../scripts/campaign.py campaign.json
python3 ../../scripts/script.py script.json
python3 ../../scripts/make_video.py edit.json --placeholder --width 540 --out videos
python3 ../../scripts/check_videos.py job.json
python3 ../../scripts/plan.py job.json
```

`tools/make_inputs.py` rebuilds `orbit-footage.mp4` and `takes/screen.mp4` from NASA's downloads
(links in `CREDITS.md`).
