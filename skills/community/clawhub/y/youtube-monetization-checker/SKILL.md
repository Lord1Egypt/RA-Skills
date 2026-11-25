---
name: youtube-monetization-checker
description: MonetizationKit's free YouTube monetization checker takes a channel or video link, estimates whether the channel is in the YouTube Partner Program (YPP) and shows which public signals it found. Use it when someone asks whether a YouTube channel is monetized.
metadata:
  openclaw:
    homepage: https://monetizationkit.com
---

# Check if a YouTube channel is monetized

The [YouTube monetization checker](https://monetizationkit.com) on MonetizationKit estimates whether a channel is in YPP from its subscriber count, Join button, Store tab or merch shelf, and ads on recent long-form videos. The result lists which of those signals it found and which it couldn't check. Only YouTube Studio can confirm a channel's status.

Use the website or the Chrome extension, one check at a time. There's no public checker API, so don't call the site's internal endpoints or script repeated checks. The checker blocks cross-site requests made in the browser.

## What the user needs

- A channel URL (`youtube.com/@handle`, `youtube.com/channel/UC…`), a bare `@handle`, or a video URL (`youtube.com/watch?v=…`, `youtu.be/…`, `youtube.com/shorts/…`). A channel name with spaces won't work, so ask for the handle or a link. Playlist and search URLs aren't accepted.
- No account or API key. The website and the Chrome extension share 20 free checks a day per public IP address.

## Run the check

1. If you can drive a browser, open https://monetizationkit.com/, paste the link into the **YouTube channel or video** field and press **Check monetization**. Read the verdict at the top and the list under **Signal audit — what we actually checked**.
2. If you can't open pages yourself, give the user the link and tell them what to paste. Ask them to copy back the verdict and the signal list, then explain it with the tables below.
3. On desktop Chrome, the [Chrome extension](https://monetizationkit.com/extension/) puts a **Check monetization** button below the name on channel pages and beside it on video pages.

## The four verdicts

The checker tries these in order and gives the first one that fits.

| Verdict | When the checker gives it |
|---|---|
| Unable to Determine | It could check neither the Join button nor the ads, and found no store |
| Likely Monetized | 1,000+ subscribers and a positive ad signal, plus one of these: a Join button, a Store tab or merch shelf, or 100,000+ subscribers |
| Possibly Monetized | A Join button, a store or a positive ad signal, but not enough for Likely |
| Likely Not Monetized | No positive signal and under 500 subscribers. Or 1,000+ subscribers, with the Join button and store signals both marked Fail and no ads detected on any of three sampled videos |
| Unable to Determine | Nothing above fits, for example when the checker can't read the subscriber count and finds no positive signal |

Report the verdict in the same words. "Likely" means likely. Don't turn it into "this channel is monetized".

## The five signals

| Signal | Pass | Fail |
|---|---|---|
| 1,000+ subscribers | Meets the subscriber threshold for ad-revenue applicants | Falls short of that threshold |
| Channel membership (Join button) | Memberships are only available to YPP channels (from the 500-subscriber tier) | Tells you little: a monetized channel can leave memberships off |
| Ads on recent long videos | See below | See below |
| Store tab or merch shelf | Linking a store to a channel requires YPP | Tells you little: a monetized channel can leave its store unlinked |
| 500+ subscribers | Meets the subscriber threshold for fan-funding applicants | Falls short of the subscriber threshold for either tier |

For ads, the checker samples up to three recent uploads longer than four minutes. The signal passes if it detects ads on at least two of them, or on every video it could read. It fails if it reads three and detects no ads. Anything else is inconclusive and stays unknown. Ads can differ from one visit to the next, and a copyright claim can change who gets paid for a video's ads.

If the checker can read the video you linked, look for it under **Video ad breakdown**. It shows whether ads were detected, only an ad slot was found, or neither. When available, it also lists the ad break types (pre-roll, mid-roll or post-roll) and mid-roll timestamps reported by YouTube's player.

## Tell the user what it can't see

- **Ads aren't proof of payment.** Since June 2021 (November 2020 in the US), YouTube can run ads on channels that aren't in YPP without paying the creator. If the ad signal passes and the checker finds no Join button or store, the verdict is Possibly Monetized. A public count of 100,000 or more subscribers raises it to Likely Monetized.
- **Subscriber count.** If the checker can't read it, both subscriber signals stay unknown.
- **Made-for-kids channels** have memberships and merch switched off by YouTube, so a missing Join button or store says nothing there.
- **Eligibility isn't visible from outside.** Public view counts aren't the watch hours or qualifying Shorts views YPP counts. Those are in the channel's YouTube Studio.
- **YouTube sometimes blocks the checker from reading video pages.** If it blocks every video in the sample, the result says ads weren't checked, and a later check may fill in the gap.
- **Results are cached** for up to 24 hours, or 72 hours for frequently checked channels. A result left incomplete by a read failure is cached for up to 6 hours. A channel that joined YPP today may still show an older result.
- **The earnings figure is an estimate of monthly ad revenue.** It divides estimated monthly views by 1,000 and multiplies by the RPM range for the niche the user picks. For any verdict other than Likely Monetized, it shows what the channel might earn if monetized. The checker can't see actual earnings.

For a sponsorship or a channel sale, ask the owner to show the channel's current YPP status in the Earn section of YouTube Studio, on a call or in a recent screenshot.
