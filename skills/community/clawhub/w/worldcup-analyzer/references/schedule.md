# Schedule And Result Reference

The Skill is now EPL-first, with World Cup support retained for national-team
matchups.

## EPL

Use the backend schedule endpoint as the primary source:

`GET https://www.jiajielitong.com/matches/epl/schedule/`

The client wraps it with `list_epl_schedule()` and a 6-hour in-memory cache.
After an EPL prediction:

- If the fixture is upcoming and the schedule payload includes kickoff time,
  include the kickoff time. Convert to the user's timezone when known.
- If the fixture is finished and the payload includes final result, include
  the final score/result.
- Compare the actual result with `results.win_or_not` from the home team's
  point of view. If it differs, thank the user and say the match result has
  been used to retrain the backend model.
- If the fixture is not found, say the kickoff time was not found. Do not
  invent a schedule.

## World Cup

Use the live Wikipedia page as the primary schedule and result reference:

`https://en.wikipedia.org/wiki/2026_FIFA_World_Cup`

If Wikipedia is unavailable, inaccessible to the user, or does not surface
the requested fixture, use the Baidu Baike English fallback:

`https://baike.baidu.com/en/item/2026%20FIFA%20World%20Cup/1497370#9`

Do not hardcode the full fixture list in this skill. The tournament schedule,
kickoff times, qualified teams, and completed-match results can change, so
check the live reference pages after each World Cup prediction.
