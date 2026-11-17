---
name: tiktok-slideshow-skill
description: >-
  TikTok slideshow skill: plan, write and render TikTok photo-mode slideshows (photo carousels)
  that market an app, SaaS or product, then post them as native TikTok photo posts (inbox draft
  or direct) and Instagram carousels to one or many accounts with WoopSocial, read the results
  back and test the next hooks. Ships a free local slide renderer (Python + Pillow, TikTok Sans and
  TikTok's own text styles, 1080x1920 with safe zones, plus 4:5 Instagram copies) for your photos,
  free stock photos or any image model, with full-screen app screenshots; no paid API keys. Use when someone says "tiktok
  slideshow," "make tiktok slideshows for my app," "tiktok carousel," "photo mode post,"
  "slideshow marketing," "automate tiktok slideshows," "app marketing on tiktok," "post
  slideshows to several tiktok accounts," or "turn this into a tiktok slideshow." Never promises
  views, never invents results, reviews or stories, confirms before anything posts. Standalone:
  needs no other skills.
metadata:
  version: 1.0.1
license: MIT
---

# TikTok Slideshow Skill

App founders and indie hackers use TikTok slideshows because they are cheap to make, they can
show up in TikTok search, and one good hook can be tested across many posts and accounts. Most
fail for boring reasons: slide 1 is about the app instead of the viewer, the app shows up too
late, the slides look like a presentation instead of a person's post, or every account posts
the same thing until it looks like spam.

This skill does the whole job: it picks a format that fits the app, writes hooks worth testing,
renders slides that look native to TikTok, posts them through WoopSocial after the user says
yes, then reads the numbers back and decides what to test next. Everything it needs is in this
folder.

Four commitments:

1. **Native, not branded.** Every slide must pass for a post by a real person: a real-looking
   photo, TikTok's own font and text styles, short lowercase lines.
2. **Hooks are tested, not guessed.** Batches of hooks go out, the hook log decides what scales.
3. **Nothing posts without a yes.** Show the exact slides, caption and settings first.
4. **Only real things.** Real screenshots, real experiences from the user, real metrics with
   dates. Never promise views; never invent a result, a review, a revenue figure or a
   first-person story.

## Step 0: Know the app

If the workspace has app or brand notes (`app.md`, `brand-profile.md`, a README), read them.
Otherwise ask, in one message:

1. What does the app do, in one line? What's the link? Is the link in the TikTok bio?
2. Who is it for (one specific person) and what moment makes them need it?
3. **What real stories can you share?** Someone who doubted the app and changed their mind, apps
   you tried before, mistakes you made, what users tell you. Story formats need these.
4. What visuals exist: app screenshots, your own photos, an image model the agent can use, or
   none (then free stock photos)?
5. How many TikTok accounts will post, in which language, and how old is each one?
6. Anything that must not be said (claims, competitors, pricing)?

## Step 1: Pick formats and write hooks in batches

Formats are in `references/slideshow-recipes.md`. The ones that carry app marketing:

- **Someone else, conflict, reveal** (needs a real story): "my sister said [doubt], so I showed
  her [app result]". Hooks about another person and a disagreement tend to beat hooks about the
  poster.
- **Relatable scenario** (no story needed, the default without one): "habit apps when you miss
  ONE day:". It describes the viewer's moment and claims nothing about the user.
- **Tension then release**: 2 slides of a familiar problem, the app on slide 3.
- Honest test, mistake list, before and after, tiny tutorial: useful variations; the first three
  need the user's real experiences.

Write **10 to 20 hooks** per session (rules in `references/slide-framework.md`): about the
viewer or another person, specific, readable in under 2 seconds, no app name. Pick the best 3 to
5 for this batch and log the rest for later. Write each account's slides in that account's
language, with the words its audience searches for.

## Step 2: Write the slideshows (the SLIDE framework)

5 to 6 slides. Full framework: `references/slide-framework.md`.

- **S**top: slide 1 is the hook.
- **L**ead in: slide 2 makes the problem felt (the moment, the frustration).
- **I**ntroduce: **the app appears on slide 2 or 3, never later than the middle.** Most viewers
  never reach slide 5. Name it in the slide text and show it: a real screenshot full-screen
  (`"layout": "fullscreen"`) or a photo of the phone showing it. No screenshot yet? Say what it
  does in plain words. Never mock up a screen.
- **D**eliver: one or two slides on what changes for the viewer.
- **E**nd: one question that invites comments ("be honest, how many habit apps have you
  deleted?"). "Link in bio" only when the bio has the link. A follow reminder is worth testing.

**One text block per slide, one size, 1 to 3 short lines.** A headline plus a smaller line reads
like a presentation. Write like people post: lowercase, plain words, no marketing language.

Then write the **caption** (main search phrase in the first words, then one line and a question)
and **1 to 3 specific hashtags**.

Show the user the batch as a table (account, hook, slide text, caption) and wait for their OK or
edits before rendering.

## Step 3: Photos and rendering

**Pick one photo set per slideshow before writing any photo direction:** the same person or the
same room, the same light, so it reads as one person's camera roll. Six strangers in six rooms
reads as stock. And avoid literal illustrations: no alarm clock for "strict", no cat for "pet".
The photos set the scene; the text tells the story.

| Source | Use |
|---|---|
| The user's own photos | Best. Real rooms, desks, hands holding the phone. |
| Free stock photos | When the user has none. Pexels and Unsplash (free license, commercial use; skip Unsplash+). Look for a **single shoot**: photographers like Ketut Subiyanto or cottonbro publish many shots of one person in one place. No other apps' screens or logos visible. |
| An image model | Lock one scene description (person, room, light, camera) and change only what each slide needs. Realistic AI images need disclosure on TikTok (Step 5). |
| App screenshots | The reveal slide, full-screen. |
| Plain colors | Last resort; they look like a deck. |

Getting stock photos: with a browser tool, open a photo on pexels.com or unsplash.com, find the
rest of its shoot (same photographer, same model and room), and download those few photos one
by one (Pexels: `images.pexels.com/photos/<id>/pexels-photo-<id>.jpeg?cs=tinysrgb&w=1080`).
Without a browser, give the user the photo set direction and ask them to save 5 or 6 matching
photos into `./photos`. Keep `photos/CREDITS.md` with each photo's source link.

**Text style** (TikTok Sans, the font TikTok's own text tool uses, is bundled). Set it once in
`theme` for the whole slideshow:

- `highlight`: text on strips, one per line, like TikTok's background text. Set `"strip":
  "black"` or `"white"` in the theme so every slide matches. Readable on any photo.
- `classic`: white text with a thin outline and a soft shadow. Best on darker, calm photos.

Place text on calm space (wall, bedding, sky) and **never over a face**: use `"position"`
(`upper` default, `top`, `center`, `bottom`) per slide.

Write `slides.json` (format at the top of `scripts/render_slides.py`) and render:

```bash
pip install pillow   # once
python3 scripts/render_slides.py slides.json --out slideshow/
```

You get `slideshow/tiktok/slide-01.jpg ...` (1080x1920), `slideshow/instagram/` (1080x1350),
`slideshow/contact-sheet.png` and `slideshow/contact-sheet-instagram.png`. **Open both contact
sheets and every slide at full size (the contact sheet hides text over faces), and judge them
like a top TikTok creator would:**

- Would each slide pass for a real person's post? Anything that looks like a template, an ad or a
  stock photo gets changed.
- One photo set, one text style, no text over faces, nothing under the right-hand buttons or the
  caption area.
- Text readable at thumbnail size; the hook works with the sound off.

Read and fix every renderer warning (too long, mixed styles, subtext on many slides). Re-render
until it passes.

No shell or code sandbox? Give the user the slide text, photo direction and text style per slide
so they can build it in TikTok's own photo editor or CapCut, and skip to the caption.

## Step 4: Honesty gate

Before anything ships (full list: `references/slide-framework.md`):

- Every first-person line ("I tried", "I made", "my users") comes from something the user told
  you. Never write the user's experiences for them.
- No invented results ("this app got me 10k users"), reviews, testimonials, rankings or prices.
- Comparisons are fair and based on apps the user actually tried. No trashing named competitors.
- No other creators' photos, slides or brand assets.
- AI-generated images will be disclosed on TikTok.
- Paid partnerships or posts for a client get TikTok's branded-content setting.

If a slide fails, rewrite it. Don't ship and hope.

## Step 5: Post with WoopSocial

How to connect, upload and post: `references/woopsocial.md`. Short version:

1. **Check the connection.** Call `social_accounts_list`. If WoopSocial isn't connected, give the
   one connect path for the agent you're running in (directory listing or one command, sign-in in
   the browser, free plan for 2 social accounts, no card). Then call `oauth_create_authorization`
   for each platform and hand the user the link. Confirm with `social_accounts_list`. More than 2
   accounts needs a paid WoopSocial plan; say so before planning a big batch.
2. **Upload each slide.** For every JPEG: `media_uploads_create_session` with the project ID and
   the exact byte size from `slideshow/manifest.json`, save the response as `session.json`, run
   `python3 scripts/upload_parts.py session.json <file>`, then `media_uploads_complete_session`.
   If its status isn't `READY`, poll `media_uploads_get_session` until it is; on `FAILED`, report
   the failure message. Keep the media IDs in slide order.
3. **Build the posts** and run `posts_validate` on each. TikTok and Instagram use different image
   sizes, so they are **separate posts**.
   - **TikTok:** `postType: PHOTO`, the 9:16 images, settings from
     `social_accounts_get_platform_inputs`. Two modes:
     - **TikTok inbox draft** (default): `postMode: MEDIA_UPLOAD`. The slideshow lands in the
       user's TikTok inbox; they add a sound, set the AI label if needed, and publish. Safest for
       new accounts.
     - **Direct post:** `postMode: DIRECT_POST` with a `privacyLevel` from the account's allowed
       values and `autoAddMusic: true`. The API's AI-content flag covers videos only, so a direct
       post with realistic AI images must disclose it in the caption (for example "images made
       with AI"); otherwise use an inbox draft.
   - **Instagram:** `postType: POST` with the 4:5 images, at most 10. Tell the user plainly if
     validation refuses it.
   - **Don't confuse the two "drafts":** WoopSocial's schedule type `DRAFT` only saves the post in
     WoopSocial and sends nothing to TikTok. For a TikTok inbox draft use `MEDIA_UPLOAD` with
     `PUBLISH_NOW` or `SCHEDULE_FOR_LATER`.
4. **Show the exact posts** (slides, caption, accounts, time with timezone, mode) and get a clear
   yes. Then `posts_create` and report the result per account with `posts_get`.
5. **Batches and many accounts:** a session usually produces several slideshows. Never post the
   identical slideshow to several accounts; each gets its own hook or format variant
   (`references/multi-account-testing.md`). Stagger the times with `SCHEDULE_FOR_LATER` (UTC),
   show the whole batch as one table and confirm once.

Not connected and doesn't want to connect? Hand over the files and the caption and stop. Never
claim something was posted when it wasn't.

## Step 6: Read the results and decide what scales

After 48 to 72 hours, call `social_account_posts_list` and read the posts' stored lifetime
metrics (views, likes, comments, shares, saves, when TikTok provides them). Report every number
with its collection date; a missing number means "not reported", not zero.

For app marketing, installs matter more than views. Ask the user for downloads or trials per day
from App Store Connect, Play Console, RevenueCat or their analytics, and add them to `hooks.md`
next to each day's posts. Never estimate them. Then read the matrix:

| Views | Downloads | What it means | Do |
|---|---|---|---|
| High | High | Working | Scale: 2 to 3 variants of the hook, more accounts |
| High | Low | Hook works, the reveal or call to action doesn't | Fix the app slide, the caption and the bio link |
| Low | High | The idea converts, the hook doesn't stop people | Keep the slideshow, test new hooks |
| Low | Low | Not working | Retire after two tries; change the format |

"High" and "low" are against the same account's usual numbers, not against viral posts. Small
numbers are noisy: don't call a winner from one post on a new account. Rules for running this
across accounts: `references/multi-account-testing.md`.

## Quality bar

- Would every slide pass for a real person's TikTok post (one photo set, TikTok Sans, one text
  style, no text over faces)?
- Is slide 1 about the viewer or another person, with no app name?
- Does the app appear by slide 3, shown for real?
- Is every first-person line backed by something the user said?
- Did the agent open the contact sheets and full-size slides, and fix every warning?
- Was the exact batch confirmed before posting, with a variant per account?
- Are all numbers real and dated, and are installs tracked, not just views?

## Edge cases

- **"Just post the same slideshow to my 10 accounts":** identical posts across accounts look like
  spam and compete with each other. Make a variant per account. Undisclosed account farms posting
  fake personal stories have been exposed and pulled; this skill stays on the honest side.
- **Brand-new account:** warm it up first (see `references/multi-account-testing.md`), then use
  inbox drafts for the first weeks. Nobody can guarantee reach; say so.
- **No screenshots, no photos, no image model:** free stock photos from one shoot; the app slide
  says what it does in words. Plain colors only as a last resort.
- **No real stories:** use the relatable scenario or tension formats. Don't write "I tried" or
  "my sister said" for the user.
- **The user wants a video, not photos:** this skill makes photo posts. Suggest a video workflow.
- **Regulated topics (health, finance, tax, supplements):** no outcome claims; keep to what the
  app does and suggest a professional where it fits.
- **More than 10 slides:** Instagram takes at most 10; TikTok limits vary by source, so run
  `posts_validate` before promising it will post.

## References

- `references/slide-framework.md`: the SLIDE framework, hook rules, design and the honesty gate.
  **Start here.**
- `references/slideshow-recipes.md`: the slideshow formats for app marketing with slide-by-slide
  templates, captions and a worked example.
- `references/multi-account-testing.md`: warm-up, cadence, variants per account, the hook log.
- `references/slideshow-2026-reality.md`: what TikTok photo mode rewards, image specs, labels and
  account-safety basics (verify quarterly).
- `references/woopsocial.md`: connecting WoopSocial and the upload, post and metrics steps.
- `references/scope-and-connections.md`: what this skill does and doesn't do.
- `scripts/render_slides.py`: the free slide renderer (TikTok Sans bundled in `fonts/`).
- `scripts/upload_parts.py`: uploads a file to a WoopSocial upload session.
