---
name: skryvo-api
description: Plan a calendar, write, design pictures for, schedule, change, review, list, cancel and measure social media posts, including the person's own videos, plan, write and publish blog articles, and write marketing emails and product listings, through Skryvo's API with a Skryvo API key. Use in agents that run shell commands but have no Skryvo MCP connection (OpenClaw, Hermes, NanoClaw, Paperclip, Grok Bot, scripts) when the person asks to post or schedule for their brand, write a blog article, check what is scheduled, or see how posts performed.
---

# Skryvo through its API

Skryvo writes in the person's brand voice and publishes through the accounts they connected in Skryvo.
Every call needs the person's key (created at https://app.skryvo.ai/settings/agents → API keys), from
`SKRYVO_API_KEY` or, where the agent hides key-like variables from its commands (DeepSeek Harness does),
from the file `~/.config/skryvo/api-key`. Never print, log or paste the key.

```bash
API=https://api.skryvo.ai/api/v1/agent
AUTH="Authorization: Bearer ${SKRYVO_API_KEY:-$(cat ~/.config/skryvo/api-key 2>/dev/null)}"
```

If both are empty, ask the person to create a key in Skryvo and save it as the secret `SKRYVO_API_KEY` or
in `~/.config/skryvo/api-key` (readable only by them). Don't ask them to paste it into the chat.

## Read the setup first

```bash
curl -s -H "$AUTH" "$API/brands"     # {"brands":[{"id","name","is_default"}]}
curl -s -H "$AUTH" "$API/channels"   # {"channels":[{"id","platform","name","brand_ids","kind","needs_reconnect","can"}]}
curl -s -H "$AUTH" "$API/platforms"  # {"platforms":[{"platform","name","kind","can_connect","can"}]}: all Skryvo offers
```

Use only channels that serve the chosen brand (`brand_ids` empty means every brand). `kind: "blog"`
takes articles, not posts. `needs_reconnect: true` can't post: tell the person to reconnect it in Skryvo
under Settings › Connected Accounts. `can` says what the channel takes: `words`, `media_required`, `video`,
`thread_posts`, `poll`, `comments`, `link`, its own `options` and what the person `must_choose`. Rely on it
rather than on what you remember about a network.

## Write (one generation for the whole call, plus image credits for pictures; schedules nothing)

```bash
curl -s -X POST -H "$AUTH" -H "Content-Type: application/json" "$API/drafts" \
  -d '{"topic":"Launch week recap: 40 orders on day one, thanks to our regulars","brand_id":"BRAND_ID"}'
# Something guessed (platforms or pictures): nothing is written yet.
# {"status":"confirm","settings":[{"field","value","from"}],"cost":{"generations","image_credits"},"left":{...}}
# Then, with the person's final values:
curl -s -X POST -H "$AUTH" -H "Content-Type: application/json" "$API/drafts" \
  -d '{"topic":"...","brand_id":"BRAND_ID","platforms":["linkedin","bluesky"],"pictures":true,"confirmed":true}'
# {"status":"written","generation_id","posts":[{"platform","text","hashtags","picture"} or {"platform","error"}],"settings"}
```

`platforms` are channels' `platform` values, up to four per call. Put what matters in `topic` (up to 200 characters: the
news, the offer, who it is for). Pass only what the person said: `platforms`, `tone`, `language`,
`audience`, `call_to_action`, `hashtags` (a list), `link` and `pictures` (a picture in the brand's look with
each post). When platforms or pictures are left out, the first call returns `status: "confirm"`: every
setting with where it came from (`you`, `brand`, `brand profile`, `Skryvo default`; pictures read `no kept look` while the brand has none), the cost and what is
left this month. Show it as one message, let the person change anything, then send their final values with
`"confirmed": true`. A call that names everything writes at once. Show every draft before scheduling.

## Picture (spends the person's Image Studio credits; schedules nothing)

```bash
curl -s -X POST -H "$AUTH" -H "Content-Type: application/json" "$API/pictures" \
  -d '{"text":"...","platforms":["linkedin","twitter"],"brand_id":"BRAND_ID","direction":"warmer"}'
# {"brand_id","headline","pictures":[{"platform","image_url","width","height"}],"credits_used","credits_left"}
```

One picture in the brand's kept look, a copy sized for each platform; about a minute. It carries the
post's opening line unless `headline` (up to nine words) is given. A brand with no kept look, or a plan
out of credits, gets a `detail` saying what to do. Show the pictures before scheduling.

## Schedule (only after the person approves the exact text, channels and time)

```bash
curl -s -X POST -H "$AUTH" -H "Content-Type: application/json" "$API/posts" \
  -d '{"text":"...","channel_ids":["CHANNEL_ID"],"at":"2026-10-14T09:00:00-04:00","brand_id":"BRAND_ID"}'
```

`at` is ISO 8601 with the person's offset and moves to the next quarter hour; leave it out to post in about
five minutes. Optional `image_url` for every channel, or `"images":{"CHANNEL_ID":"IMAGE_URL"}` to give each
channel its own sized picture. Optional `link`, a full web address: a Google Business Profile post shows it as
its button, a pin as its destination, other posts carry it after the words. Google Business Profile also takes
`"button":"learn_more|book|order|shop|sign_up|call"` (call dials the profile's number, so leave the link out).
TikTok needs `"tiktok":{"privacy":"SELF_ONLY|MUTUAL_FOLLOW_FRIENDS|FOLLOWER_OF_CREATOR|PUBLIC_TO_EVERYONE"}`,
chosen by the person.

Send `by_channel`, `{channel_id: {...}}`, to give a channel what is its own: `text`, `image_url`, `video_id`,
`title`, `options`, `thread` (a list of the posts that follow), `numbered`, `poll` (`{"question","options","days"}`),
`comments` (`[{"text","after"}]`), `tiktok`, `youtube` (`{"made_for_kids","privacy","tags"}`). Send only what
that channel's `can` lists: anything else is refused and nothing is scheduled.

## The person's own video (Skryvo never makes video)

```bash
curl -s -H "$AUTH" "$API/videos"     # {"videos":[{"id","name","bytes"}]}: the ones ready
curl -s -X POST -H "$AUTH" -H "Content-Type: application/json" "$API/videos" \
  -d '{"name":"launch.mp4","size":1048576}'  # {"id","upload_url","chunk_bytes"}
curl -s -X PUT -H "Content-Type: video/mp4" --data-binary @launch.mp4 "UPLOAD_URL"
curl -s -X POST -H "$AUTH" "$API/videos/VIDEO_ID/finish"  # {"video_id","status","seconds","width","height"}
```

Schedule it with `by_channel.CHANNEL_ID.video_id`. YouTube also needs the person's answer in
`by_channel.CHANNEL_ID.youtube.made_for_kids`.

## Change a post, review a team post (only on the person's word)

```bash
curl -s -X PATCH -H "$AUTH" -H "Content-Type: application/json" "$API/posts/POST_ID" \
  -d '{"at":"2026-12-01T09:00:00-05:00","text":"The new words"}'  # either or both
curl -s -X POST -H "$AUTH" -H "Content-Type: application/json" "$API/posts/POST_ID/review" \
  -d '{"approve":false,"note":"What should change"}'
```

## The account and the brand's design

```bash
curl -s -H "$AUTH" "$API/me"  # {"email","plan"}
curl -s -H "$AUTH" "$API/design?brand_id=BRAND_ID"  # logo, colour roles, fonts, the kept look and its photos
curl -s -X POST -H "$AUTH" -H "Content-Type: application/json" "$API/design/look" \
  -d '{"change":"closer","brand_id":"BRAND_ID"}'  # design, closer, bolder, calmer, photo or keep; ask before keep
```

## Plan a calendar (one generation; the plan adds nothing until accepted)

```bash
curl -s -X POST -H "$AUTH" -H "Content-Type: application/json" "$API/calendar/plan" \
  -d '{"start_date":"2026-12-01","period":"week","topics":["..."],"platforms":["linkedin"],"brand_id":"BRAND_ID"}'
# {"period","start_date","end_date","items":[{"day","date","time","content_type","platform","topic","reasoning"}],"summary"}
curl -s -X POST -H "$AUTH" -H "Content-Type: application/json" "$API/calendar/accept" \
  -d '{"items":[...the rows the person keeps...]}'  # {"added"}: planned topics, none set to publish
```

## Ad copy, earlier work, a new brand

```bash
curl -s -X POST -H "$AUTH" -H "Content-Type: application/json" "$API/ads" \
  -d '{"product":"...","platforms":["google_ads"],"what_it_is":"...","benefits":["..."],"goal":"conversion","link":"https://..."}'
# {"generation_id","platforms":{...}}: one generation; nothing runs. A wrong platform's refusal names the right ones.
curl -s -H "$AUTH" "$API/content?kind=article&limit=20"  # {"items":[{"id","kind","title","brand_id","created_at"}]}
curl -s -X POST -H "$AUTH" -H "Content-Type: application/json" "$API/brands" \
  -d '{"name":"...","website":"https://..."}'  # one voice training; read in the background. Ask first.
```

## Articles (blog channels, `kind: "blog"`)

```bash
# 1. Plan, free (one of the month's plans), about a minute:
curl -s -X POST -H "$AUTH" -H "Content-Type: application/json" "$API/articles/plan" \
  -d '{"topic":"How a neighbourhood bakery plans its launch week","brand_id":"BRAND_ID"}'
# {"status":"confirm","plan_id","headline","other_headlines","search_phrase","outline":[{"heading","covers"}],
#  "questions":[...],"already_written":[...],"sources":[...],"settings":[{"field","value","from"}],
#  "cost":{"generations","image_credits_up_to"},"left":{"generations","image_credits"},"plans_left"}
# 2. Write, in the background (about four minutes):
curl -s -X POST -H "$AUTH" -H "Content-Type: application/json" "$API/articles" \
  -d '{"plan_id":"PLAN_ID","answers":[{"question":"...","answer":"..."}]}'
# {"article_id","status":"writing","minutes","settings"}
# 3. Check about once a minute:
curl -s -H "$AUTH" "$API/articles/ARTICLE_ID"
# writing: {"status","stage"} · failed: {"status","error","charged":false}
# done: {"generation_id","title","words","score","markdown","complete","open_in_skryvo"}
# 4. Publish, only after the person approves the article, the blog and the time:
curl -s -X POST -H "$AUTH" -H "Content-Type: application/json" "$API/articles/ARTICLE_ID/publish" \
  -d '{"channel_id":"BLOG_CHANNEL_ID","at":"2026-11-03T09:00:00+05:00"}'
# SEO check, free: {"score","keyword","words","issues":[...],"improvements","next_improvement_free","left"}
curl -s -H "$AUTH" "$API/articles/ARTICLE_ID/seo"
# Improve, saved as a new version; the first is free, each after costs one generation (ask first):
curl -s -X POST -H "$AUTH" -H "Content-Type: application/json" "$API/articles/ARTICLE_ID/improve" \
  -d '{"goal":"seo"}'   # seo | geo_citations (a sourced FAQ) | accuracy (disputed sentences only)
# {"score_before","score_after","changes","remaining_issues","saved_as_version","charged"}
# 5. How it is doing, once published:
curl -s -H "$AUTH" "$API/articles/ARTICLE_ID/results"
# {"title","places":[{"platform","url","published_at","reach","engagements","clicks",
#  "search":{"clicks","impressions","ctr","position"}}],"open_in_skryvo"}
```

The plan takes only what the person said: `length` (words), `tone`, `style` (how-to, listicle,
comparison, case study, explainer, narrative, opinion, news, review, interview), `language`,
`audience`, `point_of_view`, `keywords`, `must_cover`, `only_you` (facts only they know), `notes` and
up to three `sources`. It returns `status: "confirm"` with every setting and where it came from, the
pictures (`cover_picture`, `inside_pictures` from the brand's defaults), the cost (`generations`, and
`image_credits_up_to` for the pictures) and what is `left` this month. Show the plan, its settings and its
`questions` as one message (only the person can answer the questions; the article uses their words). When
writing, pass the answers, any chosen `headline`, `notes`, `pictures` (false for none) and
`inside_pictures` (0 to 3), and any change to `tone`, `audience` or `point_of_view`. A new `length`,
`style` or `language` needs a new plan, which is free. Skryvo refuses before spending when the month's
balance can't cover it. A failed article is not charged. Use `generation_id` to publish after the plan's
24 hours.

Add `"as_draft": true` to the publish call to send the article to the blog now as a draft; the reply
carries its `edit_url`, where the person reviews and publishes it. Add `"original_url"` (https) when the article
first lived elsewhere; every copy credits it as the original. `search` is filled when the person connected
Google Search Console in Skryvo.

## Emails and product listings (one generation each; nothing is sent)

```bash
curl -s -X POST -H "$AUTH" -H "Content-Type: application/json" "$API/emails" \
  -d '{"about":"Our spring menu, for regulars","email_type":"promotional","brand_id":"BRAND_ID"}'
# {"status":"written","subject_lines","preheader","body","call_to_action","settings"}
curl -s -X POST -H "$AUTH" -H "Content-Type: application/json" "$API/listings" \
  -d '{"product":"Oak serving board","features":["Solid oak","Hand oiled"],"marketplace":"etsy"}'
# {"status":"written","title","listing","settings"}
```

Email types: welcome, promotional, newsletter, follow_up, re_engagement, transactional, announcement.
Marketplaces: amazon, shopify, etsy, ebay, walmart, tiktok_shop, google_shopping, woocommerce, saas,
landing_page. Left out, the type or marketplace comes from the brand and the first call returns
`status: "confirm"`, as for posts. A listing needs one to ten features; ask the person for them.

## Balance and the brand's defaults

```bash
curl -s -H "$AUTH" "$API/balance"
# {"plan","access","trial_ends_at","left":{"generations","image_credits"},"article_plans_left",
#  "enough_for":{"articles","post_batches","post_pictures"}}
curl -s -X POST -H "$AUTH" -H "Content-Type: application/json" "$API/defaults" \
  -d '{"kind":"article","settings":{"inside_pictures":0},"brand_id":"BRAND_ID"}'
```

Check the balance before a large request. When a summary lists `differs_from_brand`, offer once to keep
those choices as the brand's defaults, and save them only after the person says yes. Posts keep platforms,
tone, pictures, hashtags and call_to_action; articles keep word_count, tone, writing_style, cover_picture
and inside_pictures. Language, audience and point of view live on the brand's profile in Skryvo.

## Check, cancel, measure

```bash
curl -s -H "$AUTH" "$API/posts?days=7"              # scheduled and recent posts; written=false is a planned topic
# Each post's status is what Skryvo shows: draft, scheduled, going_out, posted or didnt_post, with `reason`.
# awaiting_approval=true is a draft Skryvo wrote that waits for the person's yes; open_in_skryvo is where to approve it.
# reviewer_approval="waiting" is a post a reviewer in the person's team approves before it goes out; tell the person.
curl -s -X DELETE -H "$AUTH" "$API/posts/POST_ID"   # cancel before it goes out (confirm first)
curl -s -H "$AUTH" "$API/results?days=30"           # reach, engagement, best times, top posts (7, 30 or 90)
```

Errors come back as `{"detail": "..."}` in plain words; pass them on as they are.
