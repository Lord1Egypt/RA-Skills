---
name: question-explanation
description: Generate a complete HTML tutorial that explains one or more problems with clear reasoning and embedded SVG or Canvas visuals. Use this skill whenever the user shares a question image, screenshot, worksheet, exam problem, homework problem, or pasted problem text and wants it explained, solved, broken down, or turned into a teachable walkthrough, even if they do not explicitly ask for HTML.
---

# Question Explanation Tutorial Generator

## Goal
Use this skill to produce a deep, systematic, visual, and easy-to-understand tutorial for one or more questions, delivered as a complete HTML page.

Core capabilities:
- Extract and recognize question content from an uploaded image or from text
- Handle multiple questions in one input
- Generate idea guidance for each question, including entry points and core knowledge
- Generate a detailed step-by-step solution walkthrough for each question
- Embed visual teaching material throughout the explanation
- Output a complete, directly viewable HTML file

Use this skill when:
- The user uploads an image of a question
- The user provides the question as text
- The user asks to explain, analyze, or teach a specific question

## Preparation
No special dependencies or manual setup are required. Rely on the agent's multimodal and reasoning abilities.

## Output Rules
- Generate silently: do not print progress, intermediate notes, summaries, or narration while working
- Create a real file: write the complete HTML into an actual `.html` file instead of only describing it in the conversation
- Save the final deliverable as a complete HTML file and send that HTML file to the user
- Respond only once after the file is saved
- Use visual material aggressively wherever it improves understanding
- Use only SVG and Canvas for visuals; do not use image formats such as PNG or JPEG
- Generate the final HTML in one pass: the file must already contain all final text, SVG, Canvas, CSS, and JavaScript with no placeholders, no staged assembly, and no follow-up completion step
- Sending the `.html` file to the user is required

Use this exact final response after the file is saved and sent:

`The tutorial has been generated. I have sent the HTML file to you.`

## Visual Material Rules

### Allowed formats
This skill supports only two visual formats:

1. **SVG** for static diagrams, geometric figures, formula illustrations, and flowcharts
 - Vector-based and lossless when scaled
 - Can include CSS styling and light animation
 - Must be embedded as complete `<svg>...</svg>` markup directly in the HTML

2. **Canvas** for dynamic interaction, animation, or more complex visual demonstrations
 - Supports interaction such as dragging, zooming, and animation
 - Suitable for physics processes, chemistry demonstrations, and dynamic geometry
 - Must include both the `<canvas>` element and the corresponding JavaScript needed to render and run it

Do not use:
- `<img>` tags for generated teaching graphics
- External image assets as substitutes for SVG or Canvas

### Quality requirements

**For SVG**
- Choose a sensible size based on content complexity, usually in the 400x300 to 800x600 range
- Use clear, high-contrast colors
- Label text, symbols, values, and formulas accurately
- Prevent labels from covering important shapes
- Use clear line widths, usually around 2px to 3px
- Highlight important elements with color or line style
- Add grids or axes when they improve comprehension
- Use `viewBox` so the graphic scales well
- Group elements logically so the structure remains clear

**For Canvas**
- Choose a sensible size for the interaction
- Use `requestAnimationFrame` for animations
- Keep animation smooth and avoid wasteful redraws
- Provide clear interaction cues
- Show important state or values during interaction when helpful
- Support pointer and touch interaction when practical
- Use clear variable names and avoid repeated heavy computation

### Standard visual patterns
- **Geometry**: show a suitable coordinate layout, label vertices, side lengths, and angles, and add helper lines when useful
- **Function graphs**: draw clear axes and ticks, mark key points such as vertices, intercepts, and extrema, and sample curves densely enough to stay smooth
- **Physics diagrams**: use standard arrows for forces and vectors, label force names, magnitudes, and directions, and define a clear reference frame
- **Chemistry structures or setups**: use standard chemical notation, label symbols and formulas clearly, and keep proportions balanced
- **Flowcharts and relation diagrams**: use recognizable symbols, keep arrow direction unambiguous, and avoid cluttered crossings

### Selection guidance
- Use SVG for static graphics such as geometry diagrams, theorem illustrations, or formula explanations
- Use Canvas for dynamic demonstrations such as motion, experiments, or interactive geometric transformations
- For formulas or mathematical relationships, use whichever of SVG or Canvas communicates the idea more clearly

### Naming guidance
- Use descriptive English identifiers such as `pythagorean-theorem`, `force-analysis`, or `motion-trajectory`
- Avoid names that start with numbers, contain unnecessary special characters, or become excessively long

## HTML Structure

### Base structure
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Question Explanation Tutorial</title>
  <style>
  </style>
</head>
<body>
</body>
</html>
```

### Content organization
The page should usually contain:
1. A question section showing the original question content from the image or text
2. A structure overview showing the number of questions, their types, and the knowledge involved
3. A dedicated explanation section for each question, including:
 - idea guidance
 - detailed solution walkthrough
 - embedded visuals exactly where they improve understanding

### Styling requirements
- Use responsive layout so the page works across screen sizes
- Keep visual hierarchy clear across titles, subtitles, body text, formulas, and callouts
- Use balanced colors and readable font sizes
- Center or otherwise place visuals cleanly with enough whitespace

## Working Method

### 1. Recognize and extract the question content
Extract the complete question content from the user's input. Identify known conditions, targets, and constraints.

### 2. Handle multiple questions coherently
If the input contains multiple questions:
- Identify and number them
- Give each question a brief overview including type, knowledge area, and difficulty
- If the user already specified a target question, focus on that one
- Otherwise explain all recognized questions in an orderly way instead of pausing for confirmation, unless the user's request explicitly requires narrowing the scope

### 3. Generate the complete final HTML directly
Create one complete HTML document that already contains:
- the full question text
- the question structure overview
- idea guidance for each question
- the detailed solution walkthrough for each question
- all required SVG and Canvas content embedded in its final location
- all CSS and JavaScript needed for correct display and interaction

Do not use placeholder comments, staged generation, incremental visual insertion, or any partial HTML draft.

## Content Quality Standards

### Idea guidance
- Each question needs its own idea guidance
- Entry points must be clear, concrete, and genuinely helpful
- Core knowledge points must be complete and accurate
- Important concepts, theorems, formulas, and relationships should be visualized whenever useful

### Solution walkthrough
- Each question needs a detailed walkthrough
- Steps should be clearly ordered and logically connected
- Every major step should explain both what to do and why it is valid
- Important transformations, relationships, and structural changes should be visualized whenever useful

### Visual standard
- Core knowledge should be visualized whenever it benefits understanding
- Key steps should be visualized whenever figures, changes, relationships, or mechanisms matter
- Use only SVG and Canvas
- SVG should be clear, well-labeled, and scalable
- Canvas should be smooth, readable, and interaction-friendly when interaction is used
- The visuals and text should reinforce each other tightly

### HTML standard
- Use semantic HTML structure
- Keep CSS organized and visually effective
- Make the page responsive
- Ensure embedded visuals render correctly
- Make the page self-contained and independently viewable, without unnecessary external dependencies

## Important Notes
- Never output progress text such as "recognizing", "generating", or "saving"
- The final artifact must be a real HTML file saved in the working directory
- Use the environment-compatible file writing method available in the session to create or overwrite the `.html` file
- After saving the file, send the actual `.html` file to the user in the final response
- Prefer generating visuals whenever they can improve understanding
- Restrict all generated teaching visuals to SVG and Canvas only
- Fully use image recognition, content generation, and reasoning ability to keep the tutorial accurate, systematic, and richly illustrated
