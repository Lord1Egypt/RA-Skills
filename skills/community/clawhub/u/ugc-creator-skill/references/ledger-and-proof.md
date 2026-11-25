# Ledger and proof: what went out, what it earned, what it cost you

One ledger for every campaign: `~/.ugc-creator/ledger.json` (`UGC_CREATOR_HOME` moves the folder,
`UGC_CREATOR_LEDGER` or `--ledger` names another file), with `proof.csv` next to it. `plan.py` adds
every post that goes out with its file's fingerprint; `ledger.py` adds what happens after.

## Right after posting

1. `plan.py job.json --status status.json <postId>` reads each post's link and live time, and writes
   `submit.md`: per post the clock time its 30 minutes run out and the steps in order (Instagram's
   paid partnership label or YouTube's paid promotion box first, then submit, then the proof the
   brief wants at submission), plus any open problem recorded with the post. `deadlines.ics` next
   to it puts the campaign deadline and each post's proof screenshot times in your calendar.
   A post that went out is always recorded, even when the job changed after the check; a request
   checked and then not sent is cleared with `plan.py job.json --not-sent requests/<name>.json
   --checked`.
2. The user pastes each link into the campaign (the skill never submits and never drives their
   logged-in browser), then: `ledger.py --submitted <url> --campaign <id> [--submission-id ID]`.
   A link already submitted, or made for another campaign, is refused: one post goes into one
   campaign, once, ever. A late submission is recorded with a warning. A campaign id the ledger
   doesn't know (a typo) is refused; `--campaign-file campaign.json` adds a new one.

## While it runs

- `ledger.py --proof analytics.json`: the saved `social_account_posts_list_analytics` reply, one
  reading of each post's views per day into `proof.csv` (source "WoopSocial analytics"). It reads
  views and nothing else; the campaign's own count decides what is paid.
- `ledger.py --views <url> 12400 --source "TikTok analytics, 72h screenshot" [--geo-share 0.42]`: a
  number the user read in the app or the campaign dashboard. A number without a source is refused.
- Screenshots at the times `submit.md` lists, in `proof/<post>/`. Campaigns ask for them when a
  payout or a rejection is checked.

## What the campaign decides

- `ledger.py --status <url> approved|rejected|pending|paid [--reason "..."]`: a rejection needs the
  campaign's reason, in its words.
- `ledger.py --appeal-draft <url> [--dir .]`: writes `appeal-<post>.md`, a short appeal that quotes
  the rejection reason, says where the video meets the rule (the second the disclosure is said, the
  caption, the talking points) and lists the proof files to attach. You send it yourself.
- `ledger.py --appeal <url> --note "what you sent, where"`: only for a rejected post.
- `ledger.py --paid <url> 19.80`: what actually reached you. Each run adds a payment (campaigns pay
  as views come in), and `paid` is the sum. Paid after a rejection that was never appealed is
  flagged, in case the payout went to another post.
- `ledger.py --paid-campaign <id> 54.00`: a payout for the whole campaign, split over its videos
  that aren't rejected, in proportion to their last saved views (evenly without them). Run it again
  for each payout.
- `ledger.py --hours <campaign> 2.5 --note "filming"`: time spent, in one go.

## The report

`ledger.py --report [--min-hourly 15]` per campaign: each post's views (with where the number came
from), its status, what was paid, the open estimate after the fee against the minimum and the cap,
the days left in the counting window, the rejection rate and reasons, the hours, earnings per hour
received and if every open estimate pays, and "drop this campaign?" when most decided videos were
rejected, when it pays under your hourly floor, when no video reached the payout minimum in a week,
or when the budget is gone.

The verdict waits for the views: until 60% of the newest video's counting window has passed, the
report says the numbers are still counting instead of "drop". It splits the open estimate into
settled (window closed) and still counting, and shows hours per video. Each post's line names its
hook, and when the videos opened differently a "hooks" line puts each hook next to its views (on
different platforms, so read it with care). `ledger.py --report --week`
gives the last 7 days across every campaign: posts, submissions, decisions, paid, hours.

The math: views / 1,000 x rate, capped at the cap, nothing under the minimum payout (or the view
minimum), less the marketplace fee. `$2` per 1K, 18,400 views: $36.80 gross, $33.12 after 10%.
Estimates only: the campaign's own count decides, Instagram counts times shown, and many videos earn
little. The report never invents a number: a post with no saved reading shows 0 views.
