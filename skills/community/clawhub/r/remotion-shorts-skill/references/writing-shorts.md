# Writing a text short that people finish

Sources checked 2026-11-02. Where a number comes from a third party, it says so.

## The first second

- Frame 0 already shows the whole hook. No fade from black, no logo, no intro. The renderer sets
  the first scene fully on frame 0; only the highlight wipe and a small punch move after it.
  Frame 0 is also what the profile grid and the first paint in the feed show.
- The hook states the payoff: a number ("68.7% of fresh water is frozen"), a claim, or the
  list promise ("5 free tools that replace..."). TikTok's ads team reports that over 63% of the
  videos with the highest click-through rate put the key message in the first 3 seconds
  ([TikTok for Business](https://ads.tiktok.com/business/en-US/blog/9-creative-tips-to-drive-auction-ad-performance)).
  That's ads data and a correlation, but it matches what YouTube measures for Shorts: "viewed vs
  swiped away" ([YouTube Help](https://support.google.com/youtube/answer/12220281)).
- About 10 words or fewer. If the hook needs a comma, it's probably two scenes.

Hook patterns that work for text shorts:

| Pattern | Example |
|---|---|
| The surprising number | "Less than 1% of Earth's water is fresh water you can reach" |
| The list promise | "5 free tools that replace a $300 design stack" |
| The reversal | "Everyone says X. The numbers say Y." |
| The direct benefit | "Cut your build time in half with one flag" |
| The question they already have | "Why does your phone die faster in the cold?" |

Every hook must be true for this short. Don't promise what the scenes don't deliver.

## Reading speed and timing

The renderer times each scene for you. What it's based on:

- BBC subtitle guidance: 160 to 180 words per minute, about 0.33 to 0.375 seconds per word
  ([BBC](https://www.bbc.co.uk/accessibility/forproducts/guides/subtitles/)).
- Netflix allows adults up to 20 characters per second in subtitles
  ([Netflix](https://partnerhelp.netflixstudios.com/hc/en-us/articles/217350977-English-USA-Timed-Text-Style-Guide)).
- Silent reading of continuous text averages about 238 words per minute (Brysbaert 2019,
  meta-analysis of 190 studies).

Here the text is the whole picture, so the renderer uses 0.3 seconds per word or 17 characters
per second, whichever is longer, plus a moment for the scene to land. Typical results: a hook
about 2 to 3 seconds, a stat 2.5 to 4, a list item 2 to 3. Use `pace` only to nudge (0.9 to
1.15); if the short feels slow, cut words instead.

## Length

- 15 to 45 seconds for most text shorts. A stat short is often 12 to 20; a top-5 list 25 to 45.
- Keep it under 60 seconds. YouTube blocks Shorts longer than a minute worldwide when any
  copyright claim lands on them
  ([YouTube Help](https://support.google.com/youtube/answer/15424877)), and one music claim is
  enough.
- Third-party data: a study of 9.77 million organic Reels (January to June 2026) found 45 to 60
  seconds had the highest median views
  ([Socialinsider](https://socialinsider.io/blog/instagram-reels-length/)). Treat it as a hint;
  length follows the content.

## Endings and loops

- One action at most, in the last scene: save, follow for part 2, comment a word. Put links in the
  caption, not in the video; they aren't clickable there.
- Or end on a line that leads back into the hook, so the replay feels like a continuation.
  YouTube counts every start and replay of a Short as a view since March 2025
  ([TechCrunch](https://techcrunch.com/2025/03/26/youtube-is-changing-how-youtube-shorts-views-are-counted)).
- No "thanks for watching" end card.

## Make every short worth posting

The platforms are explicit about mass-produced text videos:

- YouTube's "inauthentic content" policy (renamed in July 2025) excludes "templated storylines,
  or scrolling text with minimal or no narrative" from monetisation, and asks that each video
  have a distinct concept and deliver value
  ([YouTube Help](https://support.google.com/youtube/answer/1311392)).
- Instagram stops recommending accounts that mostly post unoriginal or near-duplicate content to
  non-followers; when copies exist, only the original is recommended
  ([Instagram](https://creators.instagram.com/blog/rewarding-original-creators-on-instagram)).

So:

- Each short has its own idea and real information. Swapping words in the same script is not a
  new short.
- Posting to several accounts: a different version for each (a different hook, theme, order, or
  angle), never the same file.
- Don't batch dozens of near-identical shorts. Say no to that request and explain why.

## Accuracy

- Every number on screen comes from a source you can name; put it in `footer` or the caption.
- Keep the source's precision ("96.5%", not "almost all").
- Quotes: exact wording, real speaker, with a source. If you can't verify a quote, don't use it.
- Product claims in launch videos: the user's own words or their changelog, nothing invented.

## Audio

The built-in sound effects are on by default: a low hit on the hook, a whoosh on each cut, a pop
when a highlight lands and ticks under count-ups. They were made for this template (no samples),
are MIT licensed and safe on every app. Turn them off with `"sfx": false`, or lower them with
`sfxVolume` under music. If the user wants music:

- It must be a file they have the rights to use on every platform it goes to.
- No free library is safe on all three apps: some Pixabay tracks get Content ID claims even
  with a valid licence ([Pixabay FAQ](https://pixabay.com/service/faq/)); YouTube Audio Library
  tracks are cleared for YouTube; TikTok's Commercial Music Library is for TikTok only.
- API posts can't attach a trending sound. For TikTok, post with `postMode: MEDIA_UPLOAD` so the
  video lands in the user's TikTok inbox, then add the sound in the app.
- Set `bpm` when the track has a steady beat, so cuts land on it.

## Captions under the video

- TikTok and Reels: one line that adds something the video doesn't say (the source, a detail,
  a question), then 3 to 5 specific hashtags. No hashtag walls.
- YouTube Shorts: a title under 100 characters with the search phrase near the start, and a
  description with the source.
- Write each platform's text separately (`contentOverride`); WoopSocial doesn't rewrite captions.
