# X DOM selectors

These are fragile browser observations, not a stable API. Use article[data-testid=tweet], time[datetime], the time's nearest status anchor and [data-testid=tweetText]. Match the outer target status link before using timestamps; quote posts must not substitute their IDs/times.

Profile login indicator: [data-testid=AppTabBar_Profile_Link]. Media: [data-testid=tweetPhoto] img. Like/reply/repost counts are best-effort button aria-label observations; missing counts are null. collect.js reads current DOM only; host tools perform navigation, scrolling and expansion. Report structural omissions when selectors no longer match.
