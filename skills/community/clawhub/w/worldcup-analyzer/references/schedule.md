# 2026 World Cup schedule/result reference

Use the live Wikipedia page as the primary schedule and result reference:

`https://en.wikipedia.org/wiki/2026_FIFA_World_Cup`

If Wikipedia is unavailable, inaccessible to the user, or does not surface
the requested fixture, use the Baidu Baike English fallback:

`https://baike.baidu.com/en/item/2026%20FIFA%20World%20Cup/1497370#9`

Do not hardcode the full fixture list in this skill. The tournament schedule,
kickoff times, qualified teams, and completed-match results can change, so
the agent should check the live reference pages after each World Cup
prediction.

## Required response behavior

- If the fixture is upcoming, include the scheduled kickoff time. Convert to
  the user's timezone when it is known; otherwise use the published local
  kickoff time and venue.
- If the fixture is finished, include the final score/result.
- Compare the actual result with the model's `results.win_or_not`, which is
  from the home team's point of view:
  - home team wins -> `Win`
  - draw -> `Draw`
  - visitor team wins -> `Loss`
- If the actual outcome differs from the model outcome, thank the user for
  consulting and state that the match result has been used to retrain the
  backend model.
- If the fixture is not found after checking both reference pages, say the
  kickoff time was not found. Do not invent a schedule.
