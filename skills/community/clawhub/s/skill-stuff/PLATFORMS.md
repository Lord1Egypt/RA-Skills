# Platform Specifications

*Referenced from thought-leader SKILL.md*

## Platform specifications

### Substack

**Format:** Long-form essay. 600-2000 words depending on the idea.
**Voice:** The most personal version. First-person narrative. Can be meandering in good ways.
**Structure:**
- Opening: a scene, a moment, a specific thing — not an abstract claim
- Development: the argument unfolds with stories and evidence interwoven
- Ending: earns the read — leaves the reader with something to sit with

**Hook (subject line + first line):**
Subject: specific enough to be interesting, not clickbait
First line: the most interesting version of the first thing — not preamble

**OG Image spec for Substack:**
- 1200x630px
- Editorial aesthetic — think magazine cover energy
- Large readable title text
- Minimal design — the title does the work
- Color: pull from user's Substack brand colors (ask once, store in voice.md)
- No stock photos. Typography-led or abstract.

---

### LinkedIn

**Format:** 150-600 words. White space. Short paragraphs.
**Voice:** Professional but human. The most polished version of the voice profile.
**Structure:**
- First line: the hook. The reason to click "see more."
- No preamble. The interesting thing first.
- Short paragraphs — max 3 lines each
- Ending: a genuine thought, not a CTA

**Banned from LinkedIn posts:**
"Excited to share" / "Humbled and grateful" / "Unpopular opinion:" / "I've been thinking about this"
(see linkedin-voice skill for full list)

**OG Image spec for LinkedIn:**
- 1200x627px
- Clean, professional
- The core claim as large text — one sentence max
- Minimal branding — name or logo, small
- Background: solid color or simple gradient — nothing busy
- Font: bold, readable at thumbnail size

---

### Twitter/X

**Format:** Either a single tweet (under 280 chars) or a thread (3-8 tweets).
**Decision rule:** Can the core claim be made in one tweet? Then do that.
If it needs development: thread.
**Voice:** Sharpest version. The least hedged. The most direct.

**Single tweet format:**
The claim. Nothing else. No setup. No "thread 🧵".
The interesting version of the idea in under 280 characters.

**Thread format:**
Tweet 1: The hook. The most interesting version of the claim.
Tweets 2-7: The development. One point per tweet. No filler.
Final tweet: The landing. Not a summary. The thing worth remembering.

**OG Image spec for Twitter/X:**
- 1200x675px (landscape) or 1080x1080px (square)
- Punchy — bold text, high contrast
- The core claim as a pull quote
- Works at thumbnail size (it will be small in most feeds)

---

### Instagram

**Format:** Caption + visual concept.
**Voice:** Most accessible version. Can be warmer than other platforms.
**Caption structure:**
- First line: the hook (visible before "more")
- 2-4 short paragraphs
- Ending: genuine — can include a question if it's real

**Carousel option:** If the idea has a natural structure (steps, contrasts, a list), suggest carousel format. Provide text for each slide.

**OG Image spec for Instagram:**
- 1080x1080px (square, feed) or 1080x1920px (story/reel cover)
- More visual than other platforms — can use color more boldly
- For carousel: each slide has one point, consistent visual template
- For single post: the core claim, visually treated

**Instagram note:** This platform is the most visual-first.
The image needs to work without the caption. The caption supports the image.
Not the other way round.

---

### Reddit

**Format:** This is the most different. Reddit is a community, not an audience.
**The rule:** Post as if you're genuinely sharing something with the community, not publishing for them.

**Reddit-specific approach:**
- Find the right subreddit first. The subreddit determines everything.
- Read the community norms before suggesting a post angle.
- The post should add value to that community specifically — not just be a version of the LinkedIn post.
- Self-promotion is detected immediately. The post should not feel like content — it should feel like a contribution.

**Format options:**
- Text post: the full argument, written for Reddit's culture (more casual, open to being wrong)
- Link post with comment: share the Substack link with a genuine comment adding context
- Discussion starter: pose the idea as a question to the community

**Reddit-specific voice:**
- Admit uncertainty where it exists
- Invite disagreement — Reddit communities respect intellectual honesty
- Don't lecture. Contribute.

**OG Image spec for Reddit:**
- Text posts don't need an image
- Link posts use the Substack OG image
- If image is used: 1200x628px, community-appropriate style

**Reddit caution flag:**
Before writing a Reddit post, the skill assesses:
- Is this idea genuinely useful to [subreddit] or is it primarily promotional?
- Does it pass the "would I post this if I had nothing to sell?" test?

If it doesn't pass: flag it. Suggest either a different angle or skipping Reddit for this piece.

---

## OG image generation

After platform drafts are written, generate OG images using `image_generate`.

For each platform, write a precise image prompt:

**Substack prompt template:**
```
Editorial magazine cover style. Large bold typography reading "[TITLE]". 
Minimal design. [USER'S BRAND COLOR] background or [complementary palette]. 
Clean, sophisticated. No photography. No stock imagery. 
Font weight: heavy for title, light for byline "[AUTHOR NAME]".
1200x630px layout.
```

**LinkedIn prompt template:**
```
Clean professional design. White or light background.
Bold sans-serif text: "[CORE CLAIM — one sentence]".
Small "[AUTHOR NAME]" credit bottom right.
No decorative elements. Typography-first.
High contrast for thumbnail readability. 1200x627px.
```

**Twitter/X prompt template:**
```
High contrast. Bold typography. "[PULL QUOTE from piece]".
Simple background — solid or minimal texture.
Punchy, immediate. Readable at small size.
[User's brand color or neutral] palette. 1200x675px.
```

**Instagram prompt template:**
```
[More visual — use what's appropriate to the topic].
[Color palette from voice.md if set].
"[First line of caption]" as overlay text if appropriate.
Visual-first design. 1080x1080px.
```

Store generated images in `images/[slug]-[platform].png`.

---

## The approval package

When all drafts and images are ready, present the full package:

```
📦 CONTENT PACKAGE: "[PIECE TITLE]"

Ready for approval:

✅ Substack — [word count] — [read time]
✅ LinkedIn — [word count]
✅ Twitter/X — [tweet / thread of N]
✅ Instagram — [word count + carousel/single]
✅ Reddit — [subreddit] — [post type]

Images generated: [5 images ready]

Review each:
/tl review substack
/tl review linkedin
/tl review twitter
/tl review instagram
/tl review reddit

Approve all and deploy: /tl approve all
Approve individual: /tl approve [platform]
Edit before approving: /tl edit [platform]
```

---

## Approval and deployment

### Manual approval (default)

User reviews each piece and explicitly approves:
`/tl approve [platform]` — approves one platform
`/tl approve all` — approves everything

Approved pieces are passed to `content-publisher` for deployment.

### Auto-post option (per platform)

User can enable auto-post for specific platforms they trust:
`/tl autopost [platform] on`

With auto-post on: piece deploys immediately on approval, no additional confirmation.
With auto-post off: piece is queued for manual posting via content-publisher.

30-minute cancel window is always available regardless of mode:
`/tl cancel [platform]` — cancels deployment within 30 minutes of approval

---

## Revision flow

Between outline agreement and final approval, the user can request revisions at any stage.

`/tl revise [platform] [instruction]`
`/tl revise all [instruction]`
`/tl revise substack [make the opening more personal]`
`/tl revise linkedin [shorter, cut the second section]`

The skill revises and presents the updated version.

---

## Management commands

- `/tl [idea]` — start the ideation flow
- `/tl setup voice` — set up or update voice profile
- `/tl outline` — view current outline
- `/tl review [platform]` — review a specific platform draft
- `/tl revise [platform] [instruction]` — revise a draft
- `/tl approve [platform]` — approve for publishing
- `/tl approve all` — approve all platforms
- `/tl cancel [platform]` — cancel deployment (within 30 min)
- `/tl drafts` — list all in-progress pieces
- `/tl published` — list all published pieces
- `/tl autopost [platform] on/off` — toggle auto-post per platform
- `/tl voice` — view current voice profile
- `/tl image [platform]` — view OG image for a platform
- `/tl regenerate image [platform]` — regenerate an OG image
- `/tl insights` — show performance patterns from content-dashboard
- `/tl insights [topic]` — what's worked for a specific topic
- `/tl insights [platform]` — what's worked on a specific platform
- `/tl suggest` — suggest new piece ideas based on what's resonated

---

## What makes it good

The agreement step before writing anything.
Most tools skip this. They take the raw idea and immediately produce content.
The problem: the raw idea is often not the real idea.
The conversation about structure surfaces the actual argument.
This step is where the skill earns its place.

The native-to-platform writing.
A Substack essay and a LinkedIn post about the same idea should not look like
a long version and a short version of the same thing.
They should feel like they were written for their destination.

The Reddit honesty check.
Reddit will destroy promotional content. The skill knows this and flags it.
Better to skip Reddit for a piece than to damage a reputation with a post that reads as content.

The voice profile per platform.
One voice doesn't mean one register.
The user sounds like themselves everywhere while adapting to platform norms.
That's the difference between authentic and generic.

The feedback loop.
Every published piece feeds the next one.
The outline conversation after 10 pieces is different from after 1 piece —
not because the skill changed, but because it has evidence.
A recommendation backed by "your last 3 posts on this topic averaged 6.2 resonance"
is more useful than a recommendation backed by instinct alone.

The loop closes the system.
Idea → content → publish → performance → next idea.
All within the same skill stack, all building on each other.
