# YouTube SEO rules

What the scripts check and why. Facts were checked against YouTube's own pages on 2026-10-31;
YouTube changes these, so re-check the links each quarter. Where YouTube publishes no number,
it says so.

## How YouTube decides what to show

YouTube's search weighs three things: **relevance** ("how well the title, tags, description, and
video content match your search query"), **engagement** (such as the watch time of a video for a
query) and **quality** (channels that show expertise and trustworthiness on the topic).
[How YouTube Search works](https://www.youtube.com/howyoutubeworks/product-features/search/)

So the package has two jobs: say clearly what the video is (relevance), and earn the click from
the right viewer, who then keeps watching (engagement). A title that wins clicks the video
doesn't pay off loses on the second job, and breaks the spam policy below.

## Limits (hard)

| Field | Limit | Source |
|---|---|---|
| Title | 100 characters, no `<` or `>` | [Data API](https://developers.google.com/youtube/v3/docs/videos), [Help](https://support.google.com/youtube/answer/57407) |
| Description | 5,000 bytes as the API counts (emoji and accents use more than one), no `<` or `>` | Data API |
| Tags | 500 characters for the whole list; commas count, a tag with a space counts 2 more for its quotes | Data API |
| Hashtags | more than 60 and YouTube ignores all of them; up to 3 show above the title | [Hashtags](https://support.google.com/youtube/answer/6390658) |
| Chapters | first at 0:00, at least 3, ascending, each at least 10 seconds | [Chapters](https://support.google.com/youtube/answer/9884579) |
| Thumbnail | recommended 3840x2160 (2160x3840 for Shorts), at least 640 wide, JPG or PNG, 2 MB from a phone, 50 MB from a computer, verified channel | [Thumbnails](https://support.google.com/youtube/answer/72431) |
| Short | up to 3 minutes, square or vertical | [Shorts](https://support.google.com/youtube/answer/12779649) |

## Titles

- YouTube: name "1-2 main words that describe your video" and use them in both the title and
  the description. Title, thumbnail and description matter more for discovery than tags.
  ([Tips for descriptions](https://support.google.com/youtube/answer/12948449),
  [Tags](https://support.google.com/youtube/answer/146402))
- **How much shows:** YouTube publishes no number. Phones often show about 40 characters on a
  line, and titles past about 60 to 70 are commonly cut. So the main phrase goes early and the
  title stays under 70. (Rule of thumb, not a YouTube figure.)
- **Specific beats broad.** A new video rarely ranks for "saturn"; it can rank for "is saturn
  losing its rings in 2025" if it answers exactly that.
- **A reason to click** that the video keeps: the question it answers, a number, the result, a
  tension, a mistake to avoid.
- **Misleading titles and thumbnails** are "malicious clickbait" under YouTube's
  [Spam Policy](https://support.google.com/youtube/answer/2801973): removal, strikes or loss of
  monetisation.
- **Test & Compare** can A/B test up to 3 titles, 3 thumbnails, or both, judged on watch time
  share, within two weeks. Desktop Studio only, advanced features on; not for Shorts, made-for-
  kids, mature or private videos.
  ([A/B test titles & thumbnails](https://support.google.com/youtube/answer/13861714))

## Descriptions

- YouTube splits the description into what shows before "...more" and the rest, and advises
  "using the first few lines of your description to describe your video". It publishes no
  character count; about 100 to 150 characters is typical, so the script checks the phrase in
  the first 150.
- Each video gets a **unique** description written from its own transcript. A short, shared
  channel footer (links, socials) is fine.
- **No tag lists** in the description: "Adding excessive tags to your video description is against
  our policies".
- Links: only to safe pages; YouTube may remove links it can't verify, and content made only to
  send people off YouTube is spam.
  ([External links](https://support.google.com/youtube/answer/9054257))

## Chapters

- Written as timestamps in the description (first `0:00`, 3 or more, 10 seconds each). Manual
  chapters override YouTube's automatic ones.
- Named for what the viewer gets. Chapters show in the player and can show in Google's results,
  so a chapter named with a related search phrase (where it's true) earns a second way in.
- The script moves each start to the beginning of the sentence it falls in.

## Tags

"Tags can be useful if the content of your video is commonly misspelled. Otherwise, tags play a
minimal role in your video's discovery." 5 to 10 specific tags: the main phrase, spelling
variants, names. What happens past 500 characters isn't documented; stay under.

## Hashtags

Up to 3 show above the title: YouTube picks the "most engaging" of those in the description.
No spaces, related to the video, nothing offensive. 3 specific hashtags beat 15 generic ones.

## Thumbnails

- Rendered from the video's own frames, so the thumbnail shows what the video shows.
- **2 to 5 words** that add to the title, not repeat it. Big enough to read in the small
  "up next" card (the script warns below about 80 px at 1280 wide).
- **Keep the bottom-right corner clear**: the duration badge covers it.
- **One clear subject:** a face with a readable expression, the object, the result. Faces aren't
  required; a clear subject is.
- Not allowed: shocking or graphic imagery, sexual imagery, and anything that "misleads viewers to
  think they're about to view something that's not in the video".
  ([Thumbnails policy](https://support.google.com/youtube/answer/9229980))
- Under 720p, Test & Compare shows thumbnails at 480p.

## Captions

Upload `captions.srt` (plain UTF-8, no styling) in Studio. Captions open the video to deaf and
hard-of-hearing viewers and to viewers in other languages.
([Subtitle formats](https://support.google.com/youtube/answer/2734698)) Whether uploaded captions
help ranking isn't stated by YouTube; their value is the audience they add.

## Settings with legal or policy weight

- **Made for kids:** required for every video under an agreement with the US FTC (COPPA).
  Made-for-kids videos lose personalised ads, comments and notifications. Ask; never guess.
  ([Made for kids](https://support.google.com/youtube/answer/9528076))
- **AI use** (altered or synthetic content): required when the video makes a real person appear
  to say or do something they didn't, alters footage of a real event or place, or shows a
  realistic scene that didn't happen. Not needed for clearly unrealistic content or edits like
  colour fixes and captions. Set in Studio under "AI use"; WoopSocial doesn't set it.
  ([Disclosure](https://support.google.com/youtube/answer/14328491))
- **Mass production:** the Spam Policy bans "using automated tools or AI to churn out high
  volumes of similar content with minimal changes", and the Partner Program's "inauthentic
  content" policy (renamed in July 2025) excludes templated, mass-produced videos from
  monetisation. ([Monetisation policies](https://support.google.com/youtube/answer/1311392))
  This skill writes every package from the video's own transcript; don't use it to flood a
  channel with near-identical uploads.

## Shorts

Vertical or square and up to 3 minutes. No chapters, no Test & Compare. A custom thumbnail
(9:16) is added in desktop Studio. YouTube doesn't say `#shorts` is needed; the length and shape
decide.

## Search phrases

- `suggest.py` reads YouTube's public autocomplete: what people type, in YouTube's order, with no
  volumes. It has no official API, so it's used lightly and can stop working without notice.
- With the user's own free YouTube Data API key, `--top` reads the 10 videos ranking now.
  Default quota (October 2026): 100 searches a day, plus 10,000 units for other calls.
  ([Quota](https://developers.google.com/youtube/v3/determine_quota_cost))
- YouTube's own Research tab in Studio Analytics shows what the channel's viewers search; ask
  the user to check it for established channels.
