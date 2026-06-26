---
name: story-writer
description: Complete story development and writing pipeline. Use when creating, planning, or writing fiction. The skill runs 5 sequential processes: Discovery (questionnaire with suggestions), Story Bible (world-building), Book Bible (detailed planning), Drafting (chapter-by-chapter writing), Review (quality check), and Export (HTML book format). Includes project manager to track progress.
---

# Story Writer

A complete end-to-end story development and writing system with project management.

---

## Project Manager

The skill tracks your project through 6 stages:

| Stage | Status | Description |
|-------|--------|-------------|
| **0. Discovery** | `discovery.json` | Questionnaire complete |
| **1. Story Bible** | `story-bible.md` | World-building documented |
| **2. Book Bible** | `book-bible.md` | Detailed chapter planning |
| **3. Drafting** | `chapters/*.md` | Writing in progress |
| **4. Review** | `review-notes.md` | Quality check complete |
| **5. Export** | `export/*.html` | Book formatted |

### Project Files

```
project-folder/
├── discovery.json           # Stage 0: All questionnaire answers
├── story-bible.md           # Stage 1: World, characters, rules
├── book-bible.md            # Stage 2: Detailed chapter outline
├── chapters/                 # Stage 3: Written chapters
│   ├── chapter-01.md
│   ├── chapter-02.md
│   └── ...
├── review-notes.md          # Stage 4: Review feedback
└── export/                   # Stage 5: Final formatted book
    └── book.html
```

---

## Process 1: Discovery (Questionnaire)

### Questions (10 suggestions each)

**Q1: Chapters**
1. 12 chapters (novella)
2. 18 chapters (short novel)
3. 24 chapters (standard)
4. 30 chapters (full novel)
5. 36 chapters (epic)
6. 40 chapters (long novel)
7. 50 chapters (saga)
8. 60 chapters (multi-part)
9. 80 chapters (epic series)
10. 100+ chapters (multi-volume)

**Q2: Word Count**
1. 5,000 words (short story)
2. 15,000 words (novelette)
3. 30,000 words (novella)
4. 50,000 words (short novel)
5. 80,000 words (standard)
6. 100,000 words (full-length)
7. 120,000 words (epic)
8. 150,000 words (fantasy/sci-fi)
9. 200,000 words (doorstopper)
10. 300,000+ words (epic saga)

**Q3: Genre & Sub-genre**
See `references/fiction-genres-encyclopedia.md` for comprehensive list. Top 10 suggestions:
1. Literary Fiction - Contemporary (character-driven, introspective)
2. Fantasy - Epic/High (world-building, quest)
3. Fantasy - Urban (magic in modern world)
4. Science Fiction - Hard (technology-focused, realistic)
5. Science Fiction - Space Opera (adventure, galaxy-spanning)
6. Mystery - Cozy (amateur detective, gentle)
7. Mystery - Thriller (suspense, high stakes)
8. Romance - Contemporary (modern love story)
9. Horror - Supernatural/Psychological (fear-based)
10. Historical Fiction (period drama)

*Reference:* `references/fiction-genres-encyclopedia.md` contains 150+ genres and subgenres.

**Q4: Time Period**
1. Ancient/Pre-Medieval (BC to 500 AD)
2. Medieval (500-1500 AD)
3. Renaissance/Victorian (1500-1900)
4. 1920s-1940s (interwar, WWII)
5. 1950s-1970s (post-war)
6. 1980s-1990s (pre-internet)
7. Present Day (2020s)
8. Near Future (10-50 years)
9. Far Future (100+ years)
10. Timeless/Ambiguous

**Q5: Locations**
1. Small Town (close community)
2. Big City (urban, diverse)
3. Rural/Countryside (isolated)
4. Coastal/Island (ocean setting)
5. Mountain/Wilderness (survival)
6. Desert/Wasteland (extreme)
7. Fantasy Kingdom (magical realm)
8. Space Station/Spaceship (confined sci-fi)
9. Multiple Worlds (portal/travel)
10. Virtual/Digital (simulation)

**Q6: Story Outline**
*(Free-form or choose a template)*

1. Hero's Journey (ordinary world → call → trials → transformation)
2. Rags to Riches (poor/weak → rich/powerful)
3. Tragedy (good → bad through flaw)
4. Quest (search for object/person/knowledge)
5. Voyage and Return (go to strange land → return changed)
6. Overcoming the Monster (threat → battle → victory)
7. Comedy (confusion → chaos → happy resolution)
8. Mystery (crime/disappearance → investigation → revelation)
9. Rebellion (oppression → resistance → freedom)
10. Coming of Age (youth → maturity through experience)

**Q7: Plot Suggestions**
*(Based on chosen outline - 10 variations within that structure)*

The skill generates 10 specific plot variations based on your chosen outline, genre, and setting.

**Q8: Atmosphere/Tone**
1. Dark/Gritty (serious, heavy themes)
2. Hopeful/Uplifting (inspiring, positive)
3. Mysterious/Enigmatic (secrets, revelations)
4. Romantic/Sensual (love-focused, emotional)
5. Adventurous/Exciting (action, thrills)
6. Melancholic/Reflective (somber, thoughtful)
7. Satirical/Humorous (comedy, wit)
8. Epic/Intimate (grand scope, personal stakes)
9. Tense/Suspenseful (page-turner)
10. Whimsical/Magical (light, fantastical)

**Q9: Story Outcome**
1. Happy Ending (conflict resolved, joy)
2. Tragic Ending (loss, sadness)
3. Bittersweet (win with cost)
4. Ambiguous/Open (reader decides)
5. Triumphant (complete victory)
6. Devastating (complete loss)
7. Circular (ends where began)
8. Twist Ending (unexpected revelation)
9. Redemptive (transformation wins)
10. Cliffhanger (setup for sequel)

**Q10: Target Audience**
1. Middle Grade (ages 8-12)
2. Young Adult (ages 13-18)
3. New Adult (ages 18-25)
4. Adult Literary (sophisticated prose)
5. Adult Commercial (mainstream)
6. Women's Fiction (female-focused)
7. Thriller/Mystery Fans
8. Sci-Fi/Fantasy Fans
9. Romance Readers
10. Crossover (multiple audiences)

### Output
- `discovery.json` - All answers saved
- Summary displayed for confirmation

---

## Process 2: Story Bible Generation

Takes `discovery.json` and generates comprehensive world-building document.

### Contents

1. **Project Overview** - All discovery answers summarized
2. **Logline** - One-sentence premise
3. **Theme Statement** - What the story is really about
4. **Character Bible**
   - Protagonist (want/need/wound/fear/lie/arc)
   - Antagonist (motivation/philosophy/connection)
   - Supporting cast (5-6 characters with roles)
5. **World Building**
   - Geography & setting details
   - Time period context
   - Social systems (politics/economics/class)
   - Culture & beliefs
   - Magic/Technology rules (if applicable)
   - Daily life
6. **Theme Exploration**
   - Core theme
   - Secondary themes
   - How theme manifests in story
7. **Risk Factors** - Common pitfalls for this genre/tone
8. **Comp Titles** - Suggested comparable books

### Output
- `story-bible.md` - Comprehensive world reference

---

## Process 3: Book Bible Generation

Takes `story-bible.md` and generates detailed chapter-by-chapter planning.

### Contents

1. **Structure Selection**
   - Three-Act, Save the Cat, Hero's Journey, or Custom
   - Based on chosen story outline

2. **Beat Breakdown**
   - Major plot beats mapped to chapters
   - Word count targets per beat

3. **Chapter Outline**
   - For each chapter:
     - Chapter number & title
     - Word count target
     - One-paragraph summary
     - Key events (bullet points)
     - Character development
     - End hook (what keeps reader reading)

4. **Scene Cards**
   - Each chapter broken into 2-4 scenes
   - Scene purpose, conflict, outcome

5. **Subplot Tracking**
   - A-story (main plot)
   - B-story (relationship/secondary)
   - C-story (tertiary)
   - Where each appears in chapters

6. **Pacing Guide**
   - Tension graph across chapters
   - Breath/relax moments
   - Climax positioning

### Output
- `book-bible.md` - Complete chapter-by-chapter plan

---

## Process 4: Drafting (Chapter Writing)

Writes the actual story text, chapter by chapter.

### Workflow

For each chapter:

1. **Review chapter plan** from book bible
2. **Check previous chapter** for continuity
3. **Write chapter content** following:
   - Opening hook
   - Scene progression
   - Character voice
   - Dialogue style
   - Sensory details
   - End hook
4. **Track progress** against word count target
5. **Save chapter** as `chapters/chapter-XX.md`

### Writing Standards

- **Show, don't tell** - Action over exposition
- **Active voice** - Strong verbs, minimal adverbs
- **Dialogue** - Natural, character-specific
- **Pacing** - Vary sentence length
- **Sensory** - All five senses
- **POV consistency** - Stay in character's head
- **End hooks** - Every chapter ends with tension

### Style Adherence

The skill maintains:
- Genre-appropriate language
- Atmosphere/tone consistency
- Audience-appropriate content
- POV/tense established in story bible

### Output
- `chapters/chapter-01.md` through `chapters/chapter-XX.md`

---

## Process 5: Review (Quality Check)

Reviews all chapters using enhanced 5-category scoring system.

### Enhanced Scoring Categories (0-10 each)

**1. Plot (Structure & Pacing)**
- **Score Factors:** 3-act structure, rising tension, climax positioning, pacing
- **What to look for:** Clear beginning-middle-end, appropriate chapter lengths, climax at ~85%
- **Common issues:** Sagging middle, rushed ending, unclear structure

**2. Story Line (Emotional Coherence)**
- **Score Factors:** Character arcs, atmosphere consistency, emotional journey
- **What to look for:** Characters develop believably, tone matches atmosphere, emotional payoff
- **Common issues:** Inconsistent character voices, tone shifts, unsatisfying arcs

**3. Dramas (Conflict & Tension)**
- **Score Factors:** External obstacles, internal conflict, stakes, tension
- **What to look for:** Medical crises, storms, threats, relationship conflicts
- **Common issues:** Low stakes, insufficient conflict, predictable obstacles

**4. Love & Sensuality (Relationships)**
- **Score Factors:** Relationship development, emotional intimacy, appropriate sensuality
- **What to look for:** Emotional connection prioritized, relationship evolves naturally
- **Common issues:** Insta-love, excessive physical focus, lack of emotional depth

**5. Humanity (Theme & Meaning)**
- **Score Factors:** Theme exploration, emotional impact, hope in bleakness
- **What to look for:** What makes us human, legacy beyond biology, meaning in survival
- **Common issues:** Superficial themes, hopeless bleakness, unclear message

### Scoring Scale
- **10/10:** Masterpiece level, publication ready
- **9/10:** Excellent, minor polishing needed
- **8/10:** Very good, some improvements possible
- **7/10:** Good, needs revision in weaker areas
- **6/10:** Adequate, significant work needed
- **<6/10:** Needs major revision

### Review Outputs
- `review-notes.md` - Basic review with issues and suggestions
- `review-notes-enhanced.md` - Enhanced review with 5-category scoring (recommended)

### Enhanced Review Features
1. **Category scoring** - 0-10 for each of 5 categories
2. **Overall composite** - Weighted average score
3. **Visual score bars** - Easy-to-read progress bars
4. **Priority recommendations** - Critical/High/Medium/Low
5. **Publication readiness** - Assessment based on score
6. **Target markets** - Suggested venues based on quality
7. **Grammar analysis** - Filter words, adverbs, passive voice
8. **Chapter statistics** - Word count distribution, pacing analysis

---

## Process 6: Export (HTML Book Format)

Converts chapters into formatted HTML book.

### HTML Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>[Book Title]</title>
  <style>
    /* Book styling */
    body { font-family: Georgia, serif; line-height: 1.6; }
    .chapter { page-break-before: always; }
    .title-page { text-align: center; padding-top: 40%; }
    /* ... more styles ... */
  </style>
</head>
<body>
  <div class="title-page">
    <h1>[Title]</h1>
    <h2>[Subtitle]</h2>
    <p>by [Author]</p>
  </div>
  
  <div class="toc">
    <h2>Table of Contents</h2>
    <!-- Auto-generated TOC -->
  </div>
  
  <div class="chapter" id="chapter-1">
    <h2>Chapter 1: [Title]</h2>
    <!-- Chapter content -->
  </div>
  
  <!-- More chapters -->
</body>
</html>
```

### Export Options

- Single HTML file (all chapters)
- Separate HTML files per chapter
- Include title page
- Include table of contents
- Custom CSS styling
- Print-ready formatting

### Output
- `export/book.html` - Complete formatted book
- `export/style.css` - Separate stylesheet (optional)

---

## Scripts

### `scripts/discovery.py`
Interactive questionnaire with 10 suggestions per question.

```bash
python scripts/discovery.py
python scripts/discovery.py --output my-story.json
```

### `scripts/story-bible-generator.py`
Generate story bible from discovery answers.

```bash
python scripts/story-bible-generator.py --discovery discovery.json
```

### `scripts/book-bible-generator.py`
Generate detailed chapter outline from story bible.

```bash
python scripts/book-bible-generator.py --story-bible story-bible.md
```

### `scripts/draft-chapter.py`
Write a chapter based on book bible.

```bash
python scripts/draft-chapter.py --chapter 1 --book-bible book-bible.md
python scripts/draft-chapter.py --all  # Write all chapters
```

### `scripts/review-book.py`
Basic review of all chapters for quality.

```bash
python scripts/review-book.py --chapters chapters/
python scripts/review-book.py --fix   # Auto-fix minor issues
```

### `scripts/review-book-enhanced.py`
Enhanced review with 5-category scoring system.

```bash
python scripts/review-book-enhanced.py --chapters chapters/ --book-bible book-bible.md --discovery discovery.json
```

**Output:** `review-notes-enhanced.md` with:
- 5 category scores (0-10 each)
- Overall composite score
- Priority recommendations
- Publication readiness assessment
- Grammar analysis
- Chapter statistics
- Target market suggestions

### `scripts/export-html.py`
Export to HTML book format.

```bash
python scripts/export-html.py --chapters chapters/ --output export/book.html
```

### `scripts/chapter-tracker.py`
Track writing progress.

```bash
python scripts/chapter-tracker.py --chapters 24 --target 80000 --completed 6 --written 18000
```

### `scripts/beat-sheet.py`
Generate Save the Cat beat sheet.

```bash
python scripts/beat-sheet.py --target 80000
```

---

## References

### `references/fiction-genres-encyclopedia.md`
Comprehensive list of 150+ fiction genres and subgenres across all major categories: Literary Fiction, Action/Adventure, Speculative Fiction (Fantasy, Sci-Fi, Horror), Crime/Mystery, Romance, and experimental hybrids.

### `references/structure-frameworks.md`
Five story structures with word count breakdowns.

### `references/revision-checklist.md`
Four-pass revision system.

### `references/world-building-prompts.md`
Deep-dive questions for world development.

### `references/query-submission.md`
Traditional publishing guide.

### `references/style-guide.md`
Writing standards and common issues.

---

## Workflow Example

```
1. Discovery      → Answer 10 questions → discovery.json
2. Story Bible    → Generate world/characters → story-bible.md
3. Book Bible     → Plan every chapter → book-bible.md
4. Drafting       → Write chapter by chapter → chapters/*.md
5. Review         → Quality check → review-notes.md
6. Export         → Format as book → export/book.html
```

---

## Project Status Command

Check current project status:

```bash
python scripts/project-status.py
```

Output:
```
Project: My Novel
Status: Stage 3 - Drafting
Progress: 12/24 chapters (50%)
Words: 36,000/80,000 (45%)
Next: Continue drafting chapter 13
```

---

## Notes

- **Sequential**: Processes run in order; each builds on the previous
- **Iterative**: Can regenerate any stage if story evolves
- **Flexible**: Skip stages if you have existing material
- **Persistent**: All work saved to project folder
- **Exportable**: Final HTML can be converted to EPUB/PDF