---
name: "visual-html-presentations"
description: "Create attractive, self-contained HTML slide decks for browser use."
license: "MIT-0"
---

# Visual HTML Presentations

Use this skill when a user asks to create, improve, or convert content into a presentation, deck, slides, slideshow, pitch deck, class, workshop, training, explainer, or browser-ready visual presentation.

Trigger examples:

- "Make a presentation"
- "Create a deck"
- "Turn this into slides"
- "Make this visual"
- "Prepare slides"
- "Improve this presentation"
- "Create an HTML presentation"

Use a dedicated design tool instead when the user explicitly wants an editable design file, a branded template workflow, collaboration in a design app, or a specific export format the local HTML deck cannot provide.

## Purpose

Create polished, self-contained HTML presentations that can be opened locally in a browser, shown in meetings, recorded in videos, or used as a starting point for later design work.

## Output Standard

The final presentation should be:

- A single HTML file unless assets are explicitly requested.
- Visually attractive and easy to read.
- Responsive enough for common laptop and desktop screens.
- Navigable with keyboard arrows and visible controls.
- Free of external dependencies unless there is a clear reason.
- Stored locally by default unless the user asks for another destination.

## When To Ask Before Building

Ask a short clarification if any of these are unclear and materially affect the result:

- Audience.
- Objective.
- Slide count or duration.
- Brand/style requirements.
- Whether the output must be editable in another tool or exported to a specific format.

If missing details are minor, assume reasonably and state the assumptions in the summary.

## Workflow

1. Read the input fully: idea, notes, outline, document, transcript, markdown, report, or existing deck content.
2. Extract:
   - Topic and objective.
   - Audience.
   - Key message.
   - Required facts or sources.
   - Desired tone and use case.
   - Approximate slide count.
3. Build a slide narrative:
   - Opening / title.
   - Context or problem.
   - Main ideas.
   - Examples, evidence, or process.
   - Implications or recommendations.
   - Closing / call to action when relevant.
4. Choose a visual style suited to the topic and audience.
5. Design varied slide layouts.
6. Generate the HTML, CSS, and JavaScript.
7. Validate that text fits, slides are navigable, and the presentation is not visually broken.
8. Report the local result path or inline HTML according to the user's requested delivery style.

## Design Rules

- One main idea per slide.
- Clear hierarchy: title, short support text, visual structure.
- Avoid long paragraphs.
- Use strong spacing and alignment.
- Keep body text legible.
- Use restrained color palettes suited to the subject.
- Vary layouts across slides.
- Avoid nested cards and card-heavy marketing layouts unless cards are truly useful.
- Avoid decorative blobs, generic gradient backgrounds, and stock-like filler visuals.
- Use icons, numbers, timelines, diagrams, comparison blocks, and process flows when they clarify the idea.
- Do not invent data, citations, logos, brand claims, or source references.

## Layout Patterns

Use a mix of appropriate patterns:

- Title slide with strong subject signal.
- Two-column concept/explanation.
- Large number or key metric slide.
- Timeline or roadmap.
- Step-by-step process.
- Comparison slide.
- Quote or principle slide.
- Diagram or architecture slide.
- Problem/solution slide.
- Final summary or CTA.

## Technical Requirements

Default to a single HTML file with:

- `<!DOCTYPE html>`.
- Embedded CSS in `<style>`.
- Embedded JS for slide navigation.
- Keyboard support for left/right arrows.
- Visible previous/next controls or slide dots.
- Print/export-friendly CSS when practical.
- Responsive constraints so text does not overflow.

Use local assets only when needed. Do not rely on remote images or fonts unless the user explicitly wants that and the tradeoff is acceptable.

## Video Presentation Mode

If the slides are for video, reels, screen recording, or narration:

- Use fewer words per slide.
- Make visual rhythm stronger.
- Use large type and clear contrast.
- Prefer one sentence or one idea per slide.
- Avoid dense bullet lists.
- Consider 16:9 layout unless otherwise requested.

## Meeting or Training Mode

If the slides are for a meeting, class, workshop, or training:

- Prioritize clarity over spectacle.
- Include slide numbers.
- Allow slightly more detail per slide.
- Use summary slides and section breaks.
- Include speaker notes only if requested.

## Brand or Project Mode

When the user provides a brand, project, product, or organization context:

- Follow the provided style guidance.
- Avoid unsupported claims or invented references.
- Keep tone appropriate to the audience.
- Recommend a factual claim check for public, investor-facing, medical, legal, financial, or high-stakes decks.
- Do not publish, upload, or share the presentation externally without explicit user approval.

## Output Format

When returning the result, include:

```markdown
**Summary**
[objective, audience assumption, style chosen]

**Structure**
- Slide 1: [title]
- Slide 2: [title]

**Result**
[local file created or HTML if the user asked for inline code]

**Verification**
[what was checked]

**Remaining**
[missing assets, sources, brand details, or optional improvements]
```

For large decks, do not paste the full HTML into chat unless asked. Create the local file.

## Verification

When feasible, run a local browser or screenshot check to confirm:

- Slides render.
- Text fits containers.
- Navigation works.
- Layout is not blank or overlapping.
- Mobile or narrow viewport does not break badly.

If visual verification cannot be run, say so.

## Safety

This skill creates local presentation files only. It does not upload, publish, share, or send the result through external services unless the user explicitly requests and approves that action.
