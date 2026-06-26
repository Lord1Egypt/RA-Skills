---
name: voice-match-humanizer
version: 1.1.1
description: "Use this skill when a user is actively managing voice profiles or asking for a rewrite tied to a specific saved profile. Specific triggers: 'rewrite this in my [profile-name] voice,' 'sound like me using my [profile-name] profile,' 'build a voice profile from these samples,' 'analyze my writing samples in [path/folder],' 'score this text for AI patterns,' 'compare my [profile A] and [profile B] profiles,' 'diff these two profiles,' 'make a [platform] variant of my [profile-name],' 'has my voice drifted from my [profile-name] profile,' 'check this against my saved profile,' 'list my voice profiles,' or 'update my [profile-name] profile with new samples.' Do NOT trigger on: requests to bypass AI-detection tools for academic dishonesty, generic editing/proofreading/simplifying/brainstorming, writing from scratch with no profile context, or casual mentions of voice or tone outside an active profile workflow. The skill builds and applies voice profiles that capture a person's writing fingerprint (sentence patterns, vocabulary, tone, quirks); supports profile comparison, per-platform sub-variants, drift detection, and AI-pattern scoring; stores profiles as local markdown files."
metadata:
  openclaw:
    emoji: ✍️
---

# Voice Match Humanizer

A writing style cloning system that learns a person's unique voice from samples and applies it to any text. Unlike generic humanizers that just strip AI patterns, this skill builds a detailed style profile from real writing samples and uses it to transform text so it reads like the person actually wrote it.

## Why this matters

Generic humanizers treat "human" as one voice. But every person writes differently. A marketing director's emails don't sound like a developer's blog posts, and neither sounds like a pastor's weekly newsletter. This skill captures those differences and preserves them.

## Core capabilities

1. **Analyze writing samples** to build a detailed voice profile
2. **Score text** for AI-like patterns and give a detection risk rating
3. **Rewrite text** to match a saved voice profile
4. **Manage multiple named profiles** (e.g., "blog voice," "email voice," "formal reports")
5. **Compare profiles** to surface concrete differences between two saved voices
6. **Per-platform sub-variants** that inherit a parent voice and override surface mechanics for specific platforms (LinkedIn, Twitter, etc.)
7. **Drift detection** to flag when new writing has shifted away from a saved profile

---

## Voice Profile System

### Building a profile

When the user wants to create a voice profile, collect writing samples through either method:

- **Pasted text**: Ask for 3-5 samples of their writing (emails, blog posts, messages, reports). More samples produce better profiles. Each sample should be at least a paragraph long.
- **File references**: Read files the user points to (markdown, text, docx, emails). Extract the text content and analyze it.

For best results, samples should be from the same context as the intended use. If they want a "blog voice," analyze their blog posts, not their Slack messages.

### What to analyze

When building a voice profile, examine these dimensions across all samples and document your findings:

**Sentence structure**
- Average sentence length (short and punchy? long and flowing?)
- Sentence variety (do they mix lengths or stay consistent?)
- How they open sentences (pronouns? conjunctions? adverbs? questions?)
- Use of fragments or run-ons as a stylistic choice

**Vocabulary and word choice**
- Formality level (contractions? slang? technical jargon?)
- Favorite words and phrases that recur across samples
- Words they notably avoid
- How they handle technical terms (define them? assume knowledge?)

**Paragraph and flow patterns**
- Typical paragraph length
- How they transition between ideas (explicit transitions? white space? abrupt shifts?)
- How they open and close pieces
- Use of lists, bullet points, or other structural elements

**Tone and personality markers**
- Humor style (dry? self-deprecating? none?)
- How they express uncertainty or hedge statements
- How they give emphasis (italics? caps? repetition? rhetorical questions?)
- Level of directness (do they say "I think" or just state it?)
- Emotional range in writing

**Punctuation and formatting habits**
- Punctuation quirks (oxford comma? semicolons? exclamation points?)
- Use of parenthetical asides
- How they handle dashes (if at all)
- Capitalization patterns

### Profile format

Save each profile as a markdown file in the `profiles/` directory with this structure:

```
profiles/
  blog-voice.md
  email-voice.md
  formal-reports.md
```

Each profile file should follow this template:

```markdown
---
profile_name: [name]
created: [date]
sample_count: [number of samples analyzed]
sample_sources: [brief description of what was analyzed]
---

# Voice Profile: [Name]

## Summary
[2-3 sentence overview of this voice: who it sounds like, what context it fits, its most distinctive quality]

## Sentence Patterns
[Findings from sentence structure analysis, with direct examples pulled from the samples]

## Vocabulary Signature
[Word choice patterns, favorite phrases, formality level, with examples]

## Flow and Structure
[Paragraph patterns, transitions, openings/closings, with examples]

## Tone and Personality
[Humor, directness, hedging style, emphasis patterns, with examples]

## Punctuation and Formatting
[Mechanical habits, with examples]

## Quick Reference
[A condensed checklist of the 8-10 most distinctive traits to hit when rewriting.
These are the non-negotiable fingerprint markers that make text sound like this person.]
```

The Quick Reference section is the most important part of the profile. It should distill everything above into the concrete, actionable patterns that distinguish this voice from generic writing. Think of it as the minimum viable set of traits that, if applied consistently, would make a reader say "yeah, that sounds like them."

### Managing profiles

- **List profiles**: Check the `profiles/` directory and show the user what's available
- **Switch profiles**: When rewriting, use whatever profile the user specifies by name
- **Update profiles**: If the user provides new samples, re-analyze and update the existing profile rather than creating a new one. Preserve what was already captured and layer new findings on top.
- **Delete profiles**: Remove the profile file when asked

---

## Profile Comparison

When the user has multiple profiles and wants to see how they differ, generate a side-by-side comparison.

### Trigger

"Compare my blog and email profiles," "diff these two voices," "how is my LinkedIn voice different from my blog voice," "are these two profiles redundant"

### Process

1. Load both profiles from `profiles/`
2. For each dimension (sentence patterns, vocabulary signature, flow and structure, tone and personality, punctuation and formatting), surface differences as concrete contrasts
3. Highlight which dimensions are nearly identical vs. meaningfully different
4. Always include a Quick Reference contrast table; the user usually cares about this most

### Output format

```
## Profile Comparison: [Profile A] vs [Profile B]

### Where they differ most
1. **[Dimension]**: [Profile A description] vs [Profile B description]
2. ...

### Where they're nearly identical
- [Dimension]: [shared trait]
- ...

### Quick Reference contrast

| Trait | [Profile A] | [Profile B] |
|---|---|---|
| Sentence length | short, punchy | longer, flowing |
| Hedging | rare | frequent |
| ... | ... | ... |
```

Use this output to help the user decide which profile fits a given piece of text, or to spot when two profiles are so similar they should be merged.

---

## Per-Platform Sub-Variants

A single voice rarely works identically across platforms. A blog voice may need to compress for Twitter, formalize for LinkedIn, or loosen for Instagram captions. Sub-variants let the user keep their core voice but adapt the surface mechanics for each platform.

### Storage

Sub-variants live alongside their parent profile with a platform suffix:

```
profiles/
  blog-voice.md
  blog-voice.linkedin.md
  blog-voice.twitter.md
  email-voice.md
```

Each sub-variant inherits everything from the parent and overrides specific dimensions.

### Sub-variant file format

```markdown
---
profile_name: blog-voice
variant: linkedin
parent: blog-voice
created: [date]
---

# Sub-Variant: blog-voice → LinkedIn

## Inherits from parent
[Brief reminder of the parent's core voice]

## Overrides for this platform
- **Sentence length**: keep tight (LinkedIn rewards scannable lines)
- **Structure**: lead with the hook, not the buildup
- **Tone**: slightly more professional than the blog
- **Length cap**: 200 words for posts, 50 words for comments
- **Things to drop**: heavy parentheticals, long meandering openers
- **Things to keep**: the parent's vocabulary signature and humor style

## Quick Reference (delta only)
- Open with the punchline
- One thought per line; cut connective tissue
- No exclamation points
- Keep the parent's contractions and rhythm
```

### Using sub-variants

When rewriting, the user can specify both profile and variant:

- "Rewrite this for my LinkedIn voice" → load `blog-voice.linkedin.md` if it exists, fall back to `blog-voice.md`
- "Use the Twitter variant of my blog voice" → load `blog-voice.twitter.md`

Apply overrides on top of the parent profile. The parent supplies the core fingerprint; the sub-variant supplies platform-specific surface adjustments.

### Creating sub-variants

When the user asks for a new sub-variant ("make a LinkedIn version of my blog voice"):

1. Confirm the parent profile exists
2. Ask for 2-3 platform-specific samples if available (actual LinkedIn posts the user wrote, for example); these refine the overrides
3. Generate the sub-variant file with inherited structure
4. Show the deltas-only Quick Reference for confirmation
5. Ask: "Does this feel like how you actually write on LinkedIn, or should we tweak it?"

---

## Drift Detection

Voices evolve. A user's writing today isn't the same as it was a year ago. Drift detection compares newly submitted samples against the saved profile and surfaces meaningful shifts.

### Trigger

"Has my voice drifted," "is my profile outdated," "check this against my saved profile," "has my writing changed," or whenever the user submits new samples for a profile that already exists.

### Process

1. Load the existing profile from `profiles/[name].md`
2. Analyze the new samples using the same dimensions as profile creation
3. Compare new findings against the saved profile, dimension by dimension
4. Score drift per dimension (Stable / Mild Drift / Significant Drift)
5. Surface a summary

### Output format

```
## Voice Drift Report: [profile name]
_Comparing [N] new samples against profile last updated [date]_

### Overall drift: [Stable | Mild | Significant]

### Per-dimension breakdown

| Dimension | Status | Notes |
|---|---|---|
| Sentence patterns | Stable | Average length unchanged |
| Vocabulary signature | Mild drift | New recurring words: [list]; dropped: [list] |
| Flow and structure | Significant drift | Paragraphs ~40% longer than profile baseline |
| Tone and personality | Stable | Humor style consistent |
| Punctuation and formatting | Mild drift | More semicolons than before |

### Recommendation
[One of: "Profile is current — no action needed" | "Consider refreshing the profile" | "Profile is outdated — recommend re-analyzing with new samples"]
```

### Auto-prompting

When a profile hasn't been updated in 6+ months and the user submits text that scores very differently from the profile's expected patterns, surface drift gently and once per session:

"Heads up — this text scores differently from your saved 'blog voice' profile, which was last updated [date]. Want me to run a drift check?"

Do not badger. If the user declines, drop it for the session.

---

## AI Detection Scoring

When the user asks to score or check text for AI patterns, analyze it across these categories and give both an overall score and category breakdowns:

### Detection categories

**Vocabulary patterns** (weight: high)
- Overuse of intensifiers ("incredibly", "remarkably", "fundamentally")
- AI-favorite words ("delve", "leverage", "landscape", "nuanced", "multifaceted", "tapestry", "paradigm")
- Hedge stacking ("it's important to note that", "it's worth mentioning")
- Overly balanced phrasing ("while X, it's also true that Y")

**Structure patterns** (weight: high)
- Formulaic paragraph structure (claim, explanation, example, transition)
- Lists of exactly three items (the "rule of three" default)
- Identical paragraph lengths throughout
- Opening with a restatement of the question

**Tone patterns** (weight: medium)
- Uniformly positive or upbeat tone with no tonal variation
- Absence of genuine uncertainty, hedging, or self-correction
- Promotional or inspirational language where it doesn't fit
- No personality markers (humor, frustration, excitement, boredom)

**Mechanical patterns** (weight: medium)
- Heavy use of em dashes as connectors
- Overuse of colons to introduce lists
- Every sentence grammatically perfect with no natural imperfections
- Consistent, identical punctuation patterns throughout

### Scoring output

Present the score like this:

```
## AI Detection Risk: [Low / Medium / High / Very High]

Overall score: [X]/100 (lower is more human)

### Breakdown
- Vocabulary: [X]/25 - [brief note]
- Structure: [X]/25 - [brief note]
- Tone: [X]/25 - [brief note]
- Mechanics: [X]/25 - [brief note]

### Top flags
1. [Most obvious AI pattern found, with example from the text]
2. [Second most obvious]
3. [Third if applicable]
```

---

## Rewriting Text

This is the core action. When the user provides text to rewrite, follow this process:

### Step 1: Identify the active profile
- If the user specifies a profile name, use that
- If only one profile exists, use it by default
- If multiple profiles exist and the user didn't specify, ask which one to use

### Step 2: Score the input text
- Run the AI detection analysis on the original text
- Note the specific patterns that need to change

### Step 3: Rewrite
- Apply the voice profile, focusing on the Quick Reference traits
- Preserve the original meaning, arguments, and information completely
- Change the *how*, not the *what*
- Work paragraph by paragraph, not sentence by sentence (natural writers have flow between sentences that gets lost if you transform each one in isolation)

### Rewriting principles

**Preserve meaning ruthlessly.** The rewrite must say the same things as the original. If the original makes three arguments, the rewrite makes those same three arguments. No adding, no dropping, no softening claims the author made strongly.

**Match the profile's imperfections.** If the profile shows someone who writes sentence fragments, use fragments. If they overuse "honestly" or start too many sentences with "But," do that. Perfect grammar is an AI signal. Real people have patterns that a style guide would flag as errors.

**Vary the transformation.** Don't apply the same set of changes mechanically to every paragraph. Real writing has rhythm and variation. Some paragraphs might stay close to the original because they already sound human enough. Others might need heavy rework.

**Handle technical content carefully.** When rewriting technical or specialized content, preserve accuracy and terminology. The voice profile affects how ideas are expressed, not which ideas are expressed or what terms are used.

### Step 4: Show the result
- Present the rewritten text
- If the user asked for scoring, show a before/after score comparison
- Offer to adjust ("want it more casual?", "too many fragments?")

---

## Workflow Examples

**Creating a profile:**
```
User: "I want to create a voice profile from my blog posts"
1. Ask for samples (pasted text or file paths)
2. Read and analyze all samples
3. Build the profile following the template above
4. Save to profiles/[name].md
5. Show the user the Quick Reference section for confirmation
6. Ask: "Does this capture how you write? Anything feel off?"
```

**Scoring text:**
```
User: "Does this sound like AI wrote it?" / "Check this for AI patterns"
1. Run the detection analysis
2. Present the score and breakdown
3. Highlight the top flags with specific examples from their text
4. Offer to rewrite if the score is Medium or higher
```

**Rewriting text:**
```
User: "Rewrite this to sound like me" / "Humanize this using my blog voice"
1. Load the specified (or default) profile
2. Score the input for AI patterns
3. Rewrite using the profile's voice
4. Present the result with before/after scoring if helpful
```

**Comparing profiles:**
```
User: "Compare my blog and email profiles"
1. Load both profiles
2. Generate the comparison output with the contrast table
3. Note whether the profiles are distinct or redundant
4. Offer to merge or rename if they overlap heavily
```

**Creating a sub-variant:**
```
User: "Make a LinkedIn version of my blog voice"
1. Confirm the parent profile exists
2. Ask for platform-specific samples (optional but recommended)
3. Generate the sub-variant file with overrides
4. Show the deltas-only Quick Reference
5. Ask for confirmation before saving
```

**Drift check:**
```
User: "Is my blog profile still accurate?" / Submits new samples for an existing profile
1. Load the saved profile and the new samples
2. Run dimension-by-dimension comparison
3. Present the drift report
4. Offer to refresh the profile if drift is Mild or Significant
```

---

## Privacy and Data Handling

This skill directs the assistant to read writing samples the user points to and to read/write voice profile files in a local `profiles/` directory in the user's working directory. It does not instruct the assistant to use email tools, browser automation, web search, or any third-party API. The skill itself ships no executable code, runs no background processes, makes no network calls of its own, and has no telemetry.

**Data scope and consent rules**

- **Local storage by the skill**: voice profiles (`profiles/[name].md` and `profiles/[name].[platform].md`) are written to the user's working directory. No writes outside that directory.
- **Sample handling**: writing samples the user pastes or points the assistant to are used only to build/update profiles in the local `profiles/` directory. They are not transmitted, embedded in URLs, posted to external services, or sent anywhere outside the user's machine.
- **Sensitive sample content**: samples may include unpublished drafts, internal documents, or personal correspondence. The assistant should treat them as confidential to this session: do not quote large blocks verbatim into outputs intended for third parties, and do not paste sample content into web searches or external tool calls.
- **No transmission to third parties**: the skill does not send sample content, profile content, scoring results, or any other data back to its author, ClawHub, or any third party.
- **No telemetry**: the skill does not collect usage data, profile names, or sample content.

**Intended use and refusal scope**

This skill is for users who draft with AI and want output that matches their own established writing voice — a personal-style adapter, not a detector-evasion tool.

- The assistant should not frame outputs as designed to defeat plagiarism detectors, classroom AI checkers, or academic-integrity systems.
- If a user explicitly requests detector evasion for academic dishonesty (e.g., "make this look human enough to fool my school's AI checker"), the assistant should decline that framing and offer the legitimate voice-matching use instead.
- The AI Detection Scoring feature is provided for users who want to understand and reduce AI-pattern artifacts in their own drafting workflow, not as a calibration tool for evasion.

---

## Important Notes

- Voice profiles are only as good as the samples. If the user gives you two sentences, the profile will be thin. Gently push for more material when needed.
- Don't over-apply quirks. If someone uses a specific phrase occasionally, don't jam it into every paragraph. The goal is to sound natural, not like a caricature.
- This skill is designed for professionals who use AI as a drafting tool and want the output to match their established voice. Frame it that way and focus on voice matching, not detector evasion (see Privacy and Data Handling above for the refusal scope).
- When in doubt about a rewrite, err on the side of subtlety. It's easier to add more personality than to walk back a rewrite that went too far.
