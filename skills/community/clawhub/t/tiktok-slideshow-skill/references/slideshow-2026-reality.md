# TikTok slideshows in 2026: what's true

*Platforms change these details often. Re-check every quarter.*

## Photo mode is a real format, not a guaranteed hack

TikTok photo posts (swipeable image carousels) can be shown to non-followers like videos.
Reports differ on how their reach compares with video; they tend to do well when the content
suits them (lists, comparisons, tutorials, stories told in steps) and when people swipe to the
end. Never promise views or a multiplier.

**Swiping to the end is the commonly reported signal:** how many people get past slide 1, and
how many reach the last slide. That's why slide 1 and the last slide matter most.

## Native photo posts, not video slideshows

Post the images as a **native photo post** (WoopSocial `postType: PHOTO`), not as an MP4 with
images stitched together. Native photo posts get the swipe interface and the photo-mode sound
options.

## Image specs

- **1080x1920 (9:16), JPEG.** Sources disagree on PNG support for TikTok photo posts, and JPEG is
  the safe choice for Instagram too; the renderer saves JPEG for both.
- **Under 20 MB per image.** The renderer's files are far smaller.
- **5 to 7 slides** is the common recommendation. TikTok's maximum is reported as 35, Instagram
  carousels take at most 10, so run `posts_validate` before posting more than 10.
- **Safe zone:** TikTok draws the profile and search bar at the top, the like, comment and share
  buttons on the right, and the caption at the bottom. Keep text centred and away from those
  edges. The renderer reserves roughly 230 px at the top, 470 px at the bottom (the caption can
  run several lines) and 130 px on each side, so text sits a little above the middle. Screenshots
  in the `screenshot` layout may run lower, since a caption over an image is fine.
- **Instagram:** use the 4:5 copies (1080x1350). Square leaves dead space on TikTok, and 9:16
  gets cropped in the Instagram feed.

## Text and search

- The caption and hashtags help TikTok match the post to searches, and on-slide text is widely
  reported to help too. Use the words people actually type ("habit tracker app", "study
  planner"), in the account's language.
- 1 to 3 specific hashtags. Generic ones (#fyp, #viral) say nothing about the content.
- A question in the caption or on the last slide invites comments. Asking for likes doesn't help;
  a follow reminder is worth testing.
- One text block per slide, in TikTok Sans with TikTok's own text styles, reads as native. A
  headline plus a small subline reads as a presentation.

## Sound

Sound helps photo posts too. In draft mode the user picks a sound in the TikTok app before
publishing. For direct posts, `autoAddMusic: true` lets TikTok add music.

## Labels and disclosure

- **AI-generated images:** TikTok requires realistic AI content to be disclosed, with its
  AI-generated label or in the caption. With a TikTok inbox draft the user switches the label on
  while finishing the post. The API's AI-content flag applies to videos only, so a direct photo
  post with realistic AI images says so in the caption.
- **Paid partnerships or client posts:** use the branded-content setting (`isBrandedContent`).
  Promoting your own business: `isYourBrand`.

## Account safety

- New accounts: 7 to 14 days of normal niche scrolling before the first post, inbox drafts for
  the first weeks, and some posts that aren't promotional (details in
  `multi-account-testing.md`).
- Undisclosed account farms posting fake personal stories have been exposed in the press and
  taken down. Angles are fine; invented people and stories are not.
- Many accounts posting identical content looks like spam. Each account gets its own variant.
- Don't buy followers, use engagement pods, or post other creators' content.
- Nobody can guarantee an account won't be limited. Say so instead of promising it.

## Images you may use

- The user's own screenshots and photos.
- Images generated for this post (labeled as AI where required).
- Stock images under a license that allows commercial social use.
- Never other creators' slides, photos or brand assets.
