# TikTok Slideshow Marketing Automation

Automate high-quality educational TikTok slideshows for any app or product. Generates AI images via a user-chosen image generation method, uploads via AutomateClips API, and tracks performance over time.

---

## SETUP — Run Once When First Invoked

Work through setup conversationally. Ask one section at a time. Wait for answers before moving on.

---

### STEP 1 — App Info

Ask:
1. What app or product are we promoting? (name, what it does, who it is for)
2. What is the App Store / Google Play / product link?
3. What is the core value proposition — what problem does it solve and why would someone download/buy it today?
4. What are the main brand colors?

After collecting answers, confirm back a one-sentence pitch for the product and ask the user to approve it. This becomes the north star for all content.

---

### STEP 2 — Image Generation Method

Ask the user which image generation method they want to use. Present these options clearly:

**Option A — `nano-banana-2` via Replicate (Recommended)**
- Model: `google/nano-banana-2`
- Strengths: excellent text rendering, consistent character/mascot continuity when passing reference images, strong at dark cinematic styles
- Requires: Replicate account + API token (`r8_...`)
- Cost: pay-per-generation via Replicate

**Option B — OpenAI / DALL-E**
- Model: `gpt-image-1` or `dall-e-3`
- Strengths: widely available, good general quality, easy API access
- Requires: OpenAI API key
- Limitation: no native image-input support for reference images in all versions — character consistency is harder

**Option C — Google Gemini (imagen)**
- Model: `imagen-3.0-generate-002` or similar via Google AI Studio
- Strengths: high quality, Google ecosystem
- Requires: Google AI Studio API key
- Limitation: image-input for reference consistency varies by model version

**Option D — Something else**
- User pastes their own generation command or API details
- Ask: "Paste the command or describe the tool you want to use. I will adapt the workflow to fit."

After the user chooses, configure the generation step accordingly. If they choose Option A, create `nano_banana-2.py` (see STEP 5). If they choose another option, adapt the generation commands throughout the workflow to use their chosen tool instead.

---

### STEP 2b — AutomateClips Credentials

Ask for:
1. **AutomateClips API key** — format: `ac_sk_...`. Set as env variable: `export AUTOMATECLIPS_API_KEY="ac_sk_..."`. Never hardcode.
2. **AutomateClips TikTok Account ID** — a number visible in the AutomateClips dashboard URL or account settings.

Tell the user to set credentials as environment variables before each session. Example for Option A (Replicate):
```bash
export REPLICATE_API_TOKEN="your_token_here"
export AUTOMATECLIPS_API_KEY="your_key_here"
```

Adjust which env variables are needed based on the image generation method chosen in STEP 2.

---

### STEP 3 — Style Discovery (Conversation First, Assets After)

Do NOT ask for files yet. Have a real conversation first.

Ask one by one, waiting for answers:

1. **Niche and content type**: What topic will these slideshows cover? What kind of content performs well in this niche? (Educational tips, workout plans, myth-busting, product demos, before/after, rankings, etc.)

2. **Target audience**: Who is watching? Age range, interests, pain points, what they hope to get from this content.

3. **Visual identity**: Does the brand have a mascot, character, or recurring visual element? Or will slides be text-and-photo driven? Both work — some of the best-performing slideshows use no mascot at all.

4. **Tone**: Serious and expert? Playful and mocking? Motivational? Clinical? This affects both copy and visual style.

5. **Art style inspiration**: Ask the user to describe 1–3 TikTok accounts or visual references they like — or describe the look in their own words. Suggest if they're stuck: bold text on dark background like a movie poster, clean infographic style, realistic illustration, flat cartoon character, lifestyle photography.

6. **Background preference**: Dark and cinematic, clean white/minimal, or something else?

7. **Color palette**: Beyond brand colors, what accent colors feel right for labels, highlights, callouts?

After collecting answers, synthesize into a **Visual Style Guide** — 5–6 bullet points describing the look. Present it and ask: "Does this capture your vision, or should we adjust anything before I build the prompting system?"

---

### STEP 4 — Asset Collection

Based on style decisions, ask only for relevant assets:

- **If using a mascot/character**: Ask for `reference_mascot.png` — a clean image of the character on a simple background. Passed to the image model on every generation call for character consistency.
- **If using organic phone CTA slides**: Ask for `appstore.jpg` — a screenshot of the App Store or Google Play listing.
- **If text-and-photo / infographic style**: No mascot needed. Confirm the visual rules.
- **Other brand assets**: Logo, existing slide examples, competitor screenshots to reference.

Tell the user exactly where to drop files:
```
/your-project-folder/
├── reference_mascot.png    ← if using a character
├── appstore.jpg            ← if using phone CTA slides
└── any other assets...
```

---

### STEP 5 — Environment Setup

Once assets are ready:

**Create project directory structure:**
```bash
mkdir -p /your-project-folder/slideshows
```

**If the user chose Option A (nano-banana-2 / Replicate):**

Install the dependency:
```bash
pip install replicate
```

Create `nano_banana-2.py` in the project folder with this exact content:

```python
#!/usr/bin/env python3
"""Call the Replicate google/nano-banana-2 model with local images."""

import argparse
import base64
import mimetypes
import sys
from pathlib import Path

import replicate


def file_to_data_uri(filepath: str) -> str:
    path = Path(filepath)
    if not path.exists():
        sys.exit(f"Error: file not found: {filepath}")
    mime_type = mimetypes.guess_type(filepath)[0] or "application/octet-stream"
    data = path.read_bytes()
    b64 = base64.b64encode(data).decode("utf-8")
    return f"data:{mime_type};base64,{b64}"


def main():
    parser = argparse.ArgumentParser(description="Run google/nano-banana-2 on Replicate")
    parser.add_argument("--prompt", "-p", required=True, help="Text prompt")
    parser.add_argument("--aspect-ratio", "-a", default="9:16",
                        help="Aspect ratio (default: 9:16)")
    parser.add_argument("--output", "-o", default="output.jpg",
                        help="Output file path (default: output.jpg)")
    parser.add_argument("--output-format", "-f", default="jpg",
                        choices=["jpg", "png", "webp"],
                        help="Output format (default: jpg)")
    parser.add_argument("images", nargs="*", help="Input image file paths (optional)")
    args = parser.parse_args()

    model_input = {
        "prompt": args.prompt,
        "aspect_ratio": args.aspect_ratio,
        "output_format": args.output_format,
    }

    if args.images:
        model_input["image_input"] = [file_to_data_uri(img) for img in args.images]

    output = replicate.run("google/nano-banana-2", input=model_input)

    with open(args.output, "wb") as f:
        f.write(output.read())
    print(f"Saved to {args.output}")


if __name__ == "__main__":
    main()
```

**If the user chose Option B (OpenAI / DALL-E):**

Install the dependency:
```bash
pip install openai
```

Use this generation pattern per slide (adapt to their chosen model):
```python
from openai import OpenAI
import base64

client = OpenAI()  # reads OPENAI_API_KEY from env

result = client.images.generate(
    model="gpt-image-1",  # or dall-e-3
    prompt="YOUR PROMPT HERE",
    size="1024x1792",  # closest to 9:16
    n=1,
)

# Save image
img_data = base64.b64decode(result.data[0].b64_json)
with open("slideshows/XX_topic/slide1.jpg", "wb") as f:
    f.write(img_data)
```

Note: DALL-E does not support reference image input natively. For character consistency, describe the character in full detail in every prompt instead of passing a reference file.

---

**If the user chose Option C (Google Gemini / Imagen):**

Install the dependency:
```bash
pip install google-genai
```

Use this generation pattern per slide:
```python
from google import genai
from google.genai import types

client = genai.Client()  # reads GOOGLE_API_KEY from env

response = client.models.generate_image(
    model="imagen-3.0-generate-002",
    prompt="YOUR PROMPT HERE",
    config=types.GenerateImageConfig(
        number_of_images=1,
        aspect_ratio="9:16",
        output_mime_type="image/jpeg",
    ),
)

with open("slideshows/XX_topic/slide1.jpg", "wb") as f:
    f.write(response.generated_images[0].image.image_bytes)
```

Note: Check whether your chosen Imagen model version supports image input for reference consistency. If not, describe the character fully in every prompt.

---

**If the user chose Option D (custom tool):**

Ask the user to describe or paste the generation command they want to use. Adapt the workflow to use their command in place of the generation step. Document the adapted command here for use throughout the session.

---

**Create `slideshows/slideshows_tracking.json`:**
```json
{
  "slideshows": []
}
```

**Dry run — generate slide 1 only:**
Design the first slideshow topic, generate only the hook slide, show it to the user. If the style looks right, proceed to generate the remaining 6 slides, upload, and confirm the `publish_id` is returned. If style is off, iterate with specific changes before generating more.

**After successful dry run, ask if they want a cron job set up** (see STEP 9).

---

## ONGOING WORKFLOW — Run Every Session

Every time a new slideshow is requested, follow this exact sequence:

### 1. Fetch Analytics
```bash
curl https://app.automateclips.com/api/v1/tiktok_accounts/{ACCOUNT_ID}/analytics \
  -H "Authorization: Bearer $AUTOMATECLIPS_API_KEY"
```
Skip on first run if no data yet.

### 2. Analyze
Identify top performers by views/saves/likes. Understand what worked: hook style, visual treatment, CTA placement, content angle. Cross-reference with `slideshows_tracking.json`.

### 3. Decide
Double down on the winning formula, or test exactly one variable at a time (never change multiple things at once — isolates what caused improvement or decline).

### 4. Design the Slideshow
- Choose topic and hook style
- Write the full 7-slide plan (see Slideshow Structure below)
- Write all 7 image generation prompts
- Write a **title**: punchy, search-optimized, no emojis — reads like an expert, not clickbait
- Write a **description**: 300–500 words, no emojis, expert-tone. Cover exercises/tips/topics, the problem solved, why this approach works. TikTok indexes descriptions as a search engine — depth = better discoverability.

### 5. Generate Slides

Use whichever generation method was configured in STEP 2. Reference patterns below — adapt the command to the chosen tool.

**If using nano-banana-2 (Option A):**

Slide 1 (hook — character only):
```bash
python3 nano_banana-2.py -p "PROMPT" -o slideshows/XX_topic/slide1.jpg reference_mascot.png
```

Slide 2 (phone CTA — character + appstore reference):
```bash
python3 nano_banana-2.py -p "PROMPT" -o slideshows/XX_topic/slide2.jpg reference_mascot.png appstore.jpg
```

Slides 3–7 (character + hook slide for style consistency):
```bash
python3 nano_banana-2.py -p "PROMPT" -o slideshows/XX_topic/slide3.jpg reference_mascot.png slideshows/XX_topic/slide1.jpg
```

If no mascot (text/photo style), omit image arguments. If no phone CTA slide, skip appstore.jpg.

**If using DALL-E, Gemini, or a custom tool (Options B/C/D):**

Run the generation script/command configured in STEP 5 for each slide. Since these tools may not support reference image input, ensure character consistency by including a full, detailed character description in every prompt. Describe the character's appearance, colors, pose, and style in the same wording across all slides.

### 6. Upload to AutomateClips
```bash
curl -X POST https://app.automateclips.com/api/v1/tiktok_accounts/{ACCOUNT_ID}/photos \
  -H "Authorization: Bearer $AUTOMATECLIPS_API_KEY" \
  -F "title=SLIDESHOW TITLE" \
  -F "description=LONG EXPERT DESCRIPTION (300-500 words, no emojis)" \
  -F "images[]=@slideshows/XX_topic/slide1.jpg" \
  -F "images[]=@slideshows/XX_topic/slide2.jpg" \
  -F "images[]=@slideshows/XX_topic/slide3.jpg" \
  -F "images[]=@slideshows/XX_topic/slide4.jpg" \
  -F "images[]=@slideshows/XX_topic/slide5.jpg" \
  -F "images[]=@slideshows/XX_topic/slide6.jpg" \
  -F "images[]=@slideshows/XX_topic/slide7.jpg"
```

### 7. Save to Tracking JSON
Append to `slideshows/slideshows_tracking.json`:
```json
{
  "publish_id": "p_inbox_url~v2.XXXX",
  "slideshow_number": 1,
  "title": "SLIDESHOW TITLE",
  "hook_style": "Aspirational / Curiosity gap / Fear / Myth-bust / Ranking / etc.",
  "visual_style": "Description of what was tested",
  "folder": "slideshows/01_topic_name",
  "created_at": "YYYY-MM-DD",
  "views": null,
  "likes": null,
  "saves": null,
  "comments": null
}
```

---

## SLIDESHOW STRUCTURE

### v2 Format (Proven Winning Structure)
Front-loads the app plug (high viewership = more downloads) and ends with a share driver (algorithm boost).

| Slide | Role | Notes |
|-------|------|-------|
| 1 | Hook | Bold text, dramatic visual, no subtitle — let the image speak |
| 2 | Organic phone CTA | Casual photo of someone using the app. High viewership here. |
| 3 | Content slide 1 | Educational content with clear labels and structure |
| 4 | Content slide 2 | Same format |
| 5 | Content slide 3 | Same format |
| 6 | Content slide 4 | Same format |
| 7 | Mocking share CTA | Funny/mocking share prompt ("Send this to your friend who...") + character |

### v3 Format (Pain-First — Use When Downloads Are The Goal)
Use when v2 is getting views but zero conversions. Leads with pain instead of value.

| Slide | Role | Notes |
|-------|------|-------|
| 1 | Hook | Pain statement. Character looks frustrated/defeated. |
| 2 | Pain 1 | Agitate problem. No plan / random approach. |
| 3 | Pain 2 | Agitate problem. No progression. Body stopped responding. |
| 4 | Pain 3 | Agitate problem. Imbalances. Doing it wrong. |
| 5 | Pain 4 | Agitate problem. Inconsistency. Starts and stops. |
| 6 | The Fix | Character now looks confident. Solution positioned as obvious. |
| 7 | CTA | Direct. "Get your FREE personalized plan." Explicit download directive. |

Key differences from v2: no phone CTA at slide 2, no mocking share, character emotional arc (frustrated → confident), CTA must use "FREE" and explicit download language.

---

## HOOK PATTERNS (Ranked by Engagement)

1. **Curiosity gap / incomplete statement** — "Your [X] Don't Work Because..." → forces swipe to find out
2. **Aspirational build** — "Build The Perfect [X]" → viewers save for reference
3. **Bold provocative negative** — "The Worst [X] You're Doing" → fear of doing it wrong
4. **Contrarian / myth-bust** — "You Don't Need [assumption] To [desired outcome]" → challenges belief
5. **Ranking / tier list** — "Every [X] Ranked From D to S Tier" → completion loop
6. **Smarter alternative** — "Smarter [X] For Better [outcome]" → promises optimization
7. **Identity-targeted** — "[Specific person], This Is Why [X]" → personal relevance
8. **Time-based** — "[N]-Minute [X] That Does [impressive result]" → low barrier

---

## PROMPT WRITING RULES

**DO:**
- Use natural language full sentences — brief the model like a human artist
- Put desired on-screen text in "quotation marks" in your prompt
- If using a character: always pass `reference_mascot.png` as the first input image
- Pass the hook slide (slide1.jpg) as second input from slide 3 onward
- Pass `appstore.jpg` only for phone CTA slides
- Keep all text and visuals within the center 70% of the frame
- Max 3 bullet points per slide
- Number content items ("1. Item Name") rather than decorative badge icons
- Include this in every prompt: *"Keep all text and important visuals centered, leaving generous margins on all edges — especially bottom and right. No text in the outer 15% of any edge."*

**DO NOT:**
- Never mention "TikTok" in any prompt — causes TikTok UI overlay artifacts
- Never use keyword-stuffed tag lists — use descriptive sentences
- Never put more than 3 bullet points on a slide
- Never overload a single slide with multiple sections of copy

**Prompt template (character-based):**
```
"[Niche] educational slide with [dark/light] background. [Top section: hook text in quotes].
In the center, [CHARACTER DESCRIPTION] — keep the character exactly the same as Image 1 —
[pose/action description]. [Visual details: anatomy highlights, labels with thin lines pointing to
specific areas, props]. [Bottom section: content text in quotes]. Clean bold graphic design,
all text and visuals centered well within the frame leaving generous margins on all edges."
```

**Phone CTA prompt template:**
```
"A casual photograph taken with a second phone, showing someone holding their iPhone with the
[APP NAME] app open on screen. [Relevant screen content visible on the phone].
Background is a [realistic everyday setting relevant to the app's context].
Natural lighting, authentic unplanned feel. No text overlays."
```

---


## TIKTOK SAFE ZONES

| Zone | Coverage | What's There |
|------|----------|--------------|
| Top ~15% | "Following / For You" tabs, search icon | Never put key content here |
| Bottom ~25% | Caption, music ticker, comment bar | Never put key content here |
| Right edge ~12% | Like / Comment / Share / Bookmark / Profile | Never put key content here |
| Left edge | Generally safe | OK to use |

Always design for the center 70% of the frame.

---

## MOCKING SHARE CTA EXAMPLES

Shares are the #1 algorithm signal on TikTok. Mocking humor creates social proof and makes people tag friends = free reach. Adapt to the niche:

- "Send this to your friend who [ironic relevant behavior]"
- "Tag someone who needs to see this"
- "Share this with someone who's been [doing it wrong]"
- "Your [friend/partner/colleague] needs this more than you do"

Place on the last slide with the character looking amused/smug.

---

## CONTENT PILLAR FRAMEWORK

Adapt these to the niche during setup:

1. **Mistake/Fix** — "Stop doing X, do Y instead" — speaks to frustration of wasted effort
2. **Workout/Action Plan** — "The Perfect [X] for [outcome]" with numbered steps — saves = algorithm gold
3. **Myth Busting** — "You don't need [assumption] to [outcome]" — challenges limiting beliefs
4. **Curiosity Gap** — "Your [X] doesn't work because..." — forces completion
5. **Ranking / Best-Of** — "Every [X] Ranked" or "The Best [X] For [outcome]" — high share rate
6. **Time/Constraint Removal** — "[N] minutes / No equipment / No [barrier]" — lowers resistance

---

## SCHEDULED AUTOMATION (Optional — Ask After Successful Dry Run)

Use the `/schedule` skill to set up recurring automated runs. The `/schedule` skill will guide the user through the configuration — just provide it a clear agent prompt.

**Suggested agent prompt for `/schedule`:**
```
You are a TikTok slideshow marketing agent for [APP NAME].

Your job:
1. Fetch analytics from AutomateClips (account ID: [ACCOUNT_ID], API key in env as AUTOMATECLIPS_API_KEY)
2. Read slideshows/slideshows_tracking.json to see what has been posted and what performed best
3. Pick the next best topic — avoid repeating recent ones, double down on what is working
4. Design a 7-slide v2 slideshow: hook → phone CTA → 4 content slides → mocking share CTA
5. Generate all 7 slides using nano_banana-2.py (Replicate API key in env as REPLICATE_API_TOKEN)
6. Upload to AutomateClips with a punchy title and 300-500 word expert description
7. Save the returned publish_id and metadata to slideshows/slideshows_tracking.json

Prompt writing rules: never say "TikTok" in image prompts, keep all visuals in center 70% of frame, max 3 bullet points per slide, always pass reference_mascot.png as first image input.
```

**Suggested schedules:**
- 2x per week: `0 9 * * 1,4` — Monday and Thursday at 9am UTC
- 3x per week: `0 9 * * 1,3,5` — Monday, Wednesday, Friday at 9am UTC
- Daily: `0 10 * * *` — Every day at 10am UTC

To view or manage scheduled triggers: check your openclaw.ai dashboard.

---

## ITERATION PRINCIPLES

- **Test one variable at a time** — hook style, art style, CTA placement, content angle. Never change multiple things at once.
- **Double down on winners** — if one hook style or visual treatment outperforms, make the next 2–3 slideshows in that exact format before testing something new.
- **Track the right metrics** — saves indicate content value (people want to return), shares indicate social spread (algorithm boost), views indicate hook effectiveness. Optimize for all three, in that order.
- **Refresh content pillars** — if perfmance plateaus across 3+ slideshows, try a completely new content pillar or hook pattern rather than minor tweaks.