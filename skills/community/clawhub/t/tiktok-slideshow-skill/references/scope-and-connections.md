# Scope

## This skill does

- Plan TikTok photo-mode slideshows that market an app, SaaS or product: format, 3 hooks,
  slide text, caption and hashtags.
- Render the slides locally (1080x1920 JPEG for TikTok, 1080x1350 for Instagram) with
  `scripts/render_slides.py` in TikTok's own font and text styles, from the user's photos,
  free stock photos, AI images or screenshots.
- Check the slides against the safe zone and an honesty gate.
- Post through WoopSocial after explicit confirmation: TikTok photo posts (draft or direct),
  Instagram posts, scheduled or immediate, to one or many accounts with a variant per account.
- Read post metrics back from WoopSocial and keep a hook log that decides the next tests.

## This skill does not

- Make videos. It makes photo posts only.
- Generate images by itself. It uses the agent's own image model when there is one, or the
  user's screenshots and photos.
- Promise reach, views, downloads or revenue, or estimate them.
- Write fake reviews, testimonials, user counts or comparisons with apps the user didn't try.
- Post identical content to many accounts, buy engagement, or reuse other creators' content.
- Post anything without a clear yes from the user.
- Read comments or DMs (WoopSocial returns comment counts, not comments).

## Needs

- Any AI agent. With a shell or code sandbox it renders and uploads; without one it writes the
  slide plan and the caption for the user to build by hand.
- Python 3.8+ and Pillow for rendering (`pip install pillow`). The upload helper uses only the
  standard library.
- A WoopSocial account (free plan, 2 social accounts) to post and read results. Without it the
  skill hands over the finished files.
