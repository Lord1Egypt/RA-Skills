#!/usr/bin/env python3
"""
Story Bible Generator
Creates comprehensive story documentation from discovery answers.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# Handle Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def load_discovery(filepath):
    """Load discovery session from JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_story_bible(discovery_data):
    """Generate comprehensive story bible from discovery answers."""
    
    answers = discovery_data.get('answers', {})
    
    # Parse values
    chapters_raw = answers.get('scope_chapters', '24 chapters')
    words_raw = answers.get('scope_words', '80,000 words')
    
    # Extract numbers
    import re
    chapter_match = re.search(r'(\d+)', chapters_raw)
    word_match = re.search(r'([\d,]+)', words_raw)
    
    num_chapters = int(chapter_match.group(1)) if chapter_match else 24
    total_words = int(word_match.group(1).replace(',', '')) if word_match else 80000
    
    # Calculate structure
    avg_words_per_chapter = total_words // num_chapters
    act1_chapters = max(1, round(num_chapters * 0.25))
    act2_chapters = max(1, round(num_chapters * 0.50))
    act3_chapters = max(1, round(num_chapters * 0.25))
    
    bible = f"""# Story Bible

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## Project Overview

| Element | Selection |
|---------|-----------|
| **Chapters** | {answers.get('scope_chapters', 'Not specified')} |
| **Word Count** | {answers.get('scope_words', 'Not specified')} |
| **Genre** | {answers.get('genre', 'Not specified')} |
| **Time Period** | {answers.get('time_period', 'Not specified')} |
| **Location** | {answers.get('location', 'Not specified')} |
| **Atmosphere** | {answers.get('atmosphere', 'Not specified')} |
| **Outcome** | {answers.get('outcome', 'Not specified')} |
| **Audience** | {answers.get('audience', 'Not specified')} |

---

## Structure Breakdown

| Act | Chapters | Est. Words | % of Story |
|-----|----------|------------|------------|
| **Act 1 (Setup)** | ~{act1_chapters} | ~{total_words // 4:,} | 25% |
| **Act 2 (Confrontation)** | ~{act2_chapters} | ~{total_words // 2:,} | 50% |
| **Act 3 (Resolution)** | ~{act3_chapters} | ~{total_words // 4:,} | 25% |

**Average chapter length:** ~{avg_words_per_chapter:,} words

---

## Logline

*[TO BE DEVELOPED - One sentence capturing your story]*

Template: When [PROTAGONIST] faces [INCITING INCIDENT], they must [GOAL], but [ANTAGONIST/CONFLICT] stands in their way, forcing them to [THEMATIC CHOICE].

---

## Theme Statement

*[TO BE DEVELOPED - What is this story really about?]*

Based on your **{answers.get('atmosphere', 'atmosphere')}** atmosphere and **{answers.get('outcome', 'outcome')}** ending, consider these thematic angles:

"""

    # Add theme suggestions based on atmosphere/outcome
    theme_suggestions = generate_theme_suggestions(answers)
    bible += theme_suggestions

    bible += f"""

---

## Character Development

### Protagonist

| Aspect | Details |
|--------|---------|
| **Name** | *[Create]* |
| **Want** (external goal) | *[What do they think they want?]* |
| **Need** (internal growth) | *[What do they actually need?]* |
| **Wound** | *[What past hurt drives them?]* |
| **Fear** | *[What are they running from?]* |
| **Lie they believe** | *[What false belief holds them back?]* |

**Arc:** They start believing [THE LIE] and must learn [THE TRUTH] to achieve [GOAL].

### Antagonist

| Aspect | Details |
|--------|---------|
| **Name** | *[Create]* |
| **Motivation** | *[Why do they oppose the protagonist?]* |
| **Philosophy** | *[What worldview justifies their actions?]* |
| **Connection to Protagonist** | *[How are they connected?]* |

### Supporting Cast

*Define 3-6 key supporting characters:*

1. **[ALLY]** - Helps protagonist, has own arc
2. **[MENTOR]** - Guides protagonist, may have flaw
3. **[LOVE INTEREST]** - If applicable
4. **[SIDEKICK]** - Comic relief or loyal friend
5. **[RECURRING OBSTACLE]** - Not villain but complicates things
6. **[MINOR ANTAGONIST]** - Secondary opposition

---

## World Building

### Setting: {answers.get('location', 'Not specified')}

**Time Period:** {answers.get('time_period', 'Not specified')}

### Key Locations (define 5-10)

1. **[PRIMARY LOCATION]** - Where most action happens
   - Sensory details: sights, sounds, smells
   - Emotional atmosphere
   - History/importance

2. **[SECONDARY LOCATION]** - Important recurring setting

3. **[TERTIARY LOCATIONS]** - Minor but memorable places

### World Rules

*Define any special systems:*

- **Magic system** (if applicable): Rules, costs, limitations
- **Technology** (if applicable): What exists, how it works
- **Social systems**: Politics, economics, class structure
- **Key conflicts/tensions** in the world

---

## Plot Outline

### Three-Act Structure

#### Act 1: Setup (Chapters 1-{act1_chapters})

| Beat | Chapter | Description |
|------|---------|-------------|
| Opening Image | 1 | [Establish the ordinary world] |
| Theme Stated | 1-2 | [Someone hints at the theme] |
| Set-Up | 1-{act1_chapters//2} | [Introduce protagonist and their world] |
| Catalyst | {act1_chapters//2} | [Inciting incident that changes everything] |
| Debate | {act1_chapters//2 + 1}-{act1_chapters-1} | [Protagonist hesitates] |
| Break into Two | {act1_chapters} | [Protagonist commits to journey] |

#### Act 2: Confrontation (Chapters {act1_chapters + 1}-{act1_chapters + act2_chapters})

| Beat | Chapter | Description |
|------|---------|-------------|
| B Story | {act1_chapters + 1}-{act1_chapters + 2} | [Relationship subplot begins] |
| Fun and Games | {act1_chapters + 3}-{act1_chapters + act2_chapters//2} | [Exploring the new world/conflict] |
| Midpoint | {act1_chapters + act2_chapters//2} | [Stakes raised, point of no return] |
| Bad Guys Close In | {act1_chapters + act2_chapters//2 + 1}-{act1_chapters + int(act2_chapters * 0.75)} | [Pressure mounts] |
| All Is Lost | {act1_chapters + int(act2_chapters * 0.75)} | [Lowest point, death (literal/symbolic)] |
| Dark Night | {act1_chapters + int(act2_chapters * 0.75) + 1}-{act1_chapters + act2_chapters} | [Processing the loss] |

#### Act 3: Resolution (Chapters {act1_chapters + act2_chapters + 1}-{num_chapters})

| Beat | Chapter | Description |
|------|---------|-------------|
| Break into Three | {act1_chapters + act2_chapters + 1} | [Solution found] |
| Finale | {act1_chapters + act2_chapters + 2}-{num_chapters - 1} | [Final confrontation] |
| Final Image | {num_chapters} | [Proof of change, opposite of opening] |

---

## Chapter Breakdown

"""

    # Generate chapter list
    for i in range(1, num_chapters + 1):
        act = "Act 1" if i <= act1_chapters else ("Act 2" if i <= act1_chapters + act2_chapters else "Act 3")
        bible += f"### Chapter {i} ({act})\n"
        bible += f"**Target:** ~{avg_words_per_chapter:,} words\n\n"
        bible += f"[Summary: What happens in this chapter?]\n\n"
        bible += f"- Key events:\n"
        bible += f"  - [Event 1]\n"
        bible += f"  - [Event 2]\n"
        bible += f"- Character development:\n"
        bible += f"  - [What does protagonist learn/feel/do?]\n"
        bible += f"- End hook:\n"
        bible += f"  - [What keeps reader turning pages?]\n\n"
        bible += "---\n\n"

    bible += f"""

---

## Style Guide

### POV & Tense

Based on your **{answers.get('genre', 'genre')}** and **{answers.get('audience', 'audience')}**:

"""

    # Add POV suggestions
    bible += generate_pov_suggestions(answers)

    bible += f"""

### Voice Notes

**Atmosphere:** {answers.get('atmosphere', 'Not specified')}

Based on this atmosphere, consider:
- Sentence rhythm (short/choppy vs. long/flowing)
- Word choice (concrete vs. abstract, simple vs. ornate)
- Narrative distance (close/intimate vs. distant/observational)
- Humor level (none/wry/dark/bright)

### Comp Titles

*Find 2-3 comparable titles to understand your market:*

1. [Title] by [Author] - [Why it's similar]
2. [Title] by [Author] - [Why it's similar]
3. [Title] by [Author] - [Why it's similar]

---

## Writing Schedule

### Draft Timeline

Assuming **{avg_words_per_chapter * 7:,} words/week** (1 chapter/week):

| Phase | Duration | Target |
|-------|----------|--------|
| First Draft | {num_chapters} weeks | Complete manuscript |
| Rest Period | 2-4 weeks | Distance from work |
| Revision Pass 1 | 2 weeks | Structural fixes |
| Revision Pass 2 | 2 weeks | Scene-level polish |
| Revision Pass 3 | 1 week | Line-level polish |
| Final Polish | 1 week | Grammar/formatting |

**Total:** ~{num_chapters + 8} weeks from start to submission-ready

### Check-in Milestones

- [ ] **25% complete** (Chapter {num_chapters // 4}) - Act 1 review
- [ ] **50% complete** (Chapter {num_chapters // 2}) - Midpoint review
- [ ] **75% complete** (Chapter {int(num_chapters * 0.75)}) - Act 2 review
- [ ] **100% complete** - First draft done!
- [ ] **Revision 1** - Structural pass
- [ ] **Revision 2** - Scene pass
- [ ] **Revision 3** - Line pass
- [ ] **Final** - Ready for beta readers

---

## Risk Factors

Based on your **{answers.get('genre', 'genre')}** with **{answers.get('atmosphere', 'atmosphere')}** atmosphere:

"""

    # Add risk factors
    bible += generate_risk_factors(answers)

    bible += """

---

## Next Steps

1. **Fill in the blanks** - Complete character names, world details, chapter summaries
2. **Research comp titles** - Find 2-3 similar books in your genre
3. **Write the opening** - Don't over-plan; start writing
4. **Revise as you go** - Adjust outline as story evolves
5. **Track progress** - Use chapter tracker to stay on target

---

*This story bible is a living document. Update it as your story develops.*

"""

    return bible


def generate_theme_suggestions(answers):
    """Generate theme suggestions based on atmosphere and outcome."""
    atmosphere = answers.get('atmosphere', '').lower()
    outcome = answers.get('outcome', '').lower()
    
    suggestions = []
    
    # Theme suggestions based on atmosphere
    if 'dark' in atmosphere:
        suggestions.append("- **Dark atmosphere:** Consider themes of redemption, sacrifice, or the cost of power")
    if 'hopeful' in atmosphere or 'uplifting' in atmosphere:
        suggestions.append("- **Hopeful atmosphere:** Consider themes of resilience, community, or transformation through adversity")
    if 'mysterious' in atmosphere:
        suggestions.append("- **Mysterious atmosphere:** Consider themes of truth vs. perception, the weight of secrets, or knowledge as power")
    if 'romantic' in atmosphere:
        suggestions.append("- **Romantic atmosphere:** Consider themes of vulnerability, trust, or love as transformation")
    if 'adventurous' in atmosphere:
        suggestions.append("- **Adventurous atmosphere:** Consider themes of courage, identity, or home vs. journey")
    
    # Theme suggestions based on outcome
    if 'happy' in outcome:
        suggestions.append("- **Happy ending:** Theme should show growth, reward for struggle, or the power of choice")
    if 'tragic' in outcome:
        suggestions.append("- **Tragic ending:** Theme should show the cost of flaws, fate vs. free will, or the limits of human agency")
    if 'bittersweet' in outcome:
        suggestions.append("- **Bittersweet ending:** Theme should show the complexity of life, trade-offs, or growth through loss")
    if 'ambiguous' in outcome:
        suggestions.append("- **Ambiguous ending:** Theme should embrace uncertainty, reader interpretation, or the nature of truth")
    if 'redemptive' in outcome:
        suggestions.append("- **Redemptive ending:** Theme should show transformation, forgiveness, or the possibility of change")
    
    return '\n'.join(suggestions)


def generate_pov_suggestions(answers):
    """Generate POV suggestions based on genre and audience."""
    genre = answers.get('genre', '').lower()
    audience = answers.get('audience', '').lower()
    
    suggestions = []
    
    if 'literary' in genre:
        suggestions.append("**Suggested POV:** Third person limited or first person")
        suggestions.append("**Suggested Tense:** Past or present")
        suggestions.append("**Rationale:** Literary fiction benefits from intimate character access and stylistic flexibility")
    elif 'fantasy' in genre or 'epic' in genre:
        suggestions.append("**Suggested POV:** Third person limited (multiple POVs for epic) or omniscient")
        suggestions.append("**Suggested Tense:** Past")
        suggestions.append("**Rationale:** Fantasy benefits from scope and world-building, past tense feels timeless")
    elif 'science fiction' in genre or 'sci-fi' in genre:
        suggestions.append("**Suggested POV:** Third person limited or first person")
        suggestions.append("**Suggested Tense:** Past or present")
        suggestions.append("**Rationale:** Sci-fi can be intimate or expansive; present tense can create immediacy")
    elif 'mystery' in genre or 'thriller' in genre:
        suggestions.append("**Suggested POV:** Third person limited or first person")
        suggestions.append("**Suggested Tense:** Past (can use present for tension)")
        suggestions.append("**Rationale:** Mystery needs careful information control; POV choice affects suspense")
    elif 'romance' in genre:
        suggestions.append("**Suggested POV:** Third person limited (dual POV common) or first person")
        suggestions.append("**Suggested Tense:** Past or present")
        suggestions.append("**Rationale:** Romance benefits from intimate access to both characters' emotions")
    elif 'ya' in audience:
        suggestions.append("**Suggested POV:** First person or third person limited")
        suggestions.append("**Suggested Tense:** Past or present (present is increasingly common)")
        suggestions.append("**Rationale:** YA readers connect strongly with immediate, personal voice")
    else:
        suggestions.append("**Suggested POV:** Third person limited (most flexible)")
        suggestions.append("**Suggested Tense:** Past (most common)")
    
    return '\n'.join(suggestions)


def generate_risk_factors(answers):
    """Generate risk factors based on genre and atmosphere."""
    genre = answers.get('genre', '').lower()
    atmosphere = answers.get('atmosphere', '').lower()
    
    risks = []
    
    if 'fantasy' in genre:
        risks.append("- **World-building trap:** Avoid info-dumps; reveal world through character experience")
        risks.append("- **Pacing:** Epic fantasy can drag in middle; maintain tension throughout Act 2")
    
    if 'science fiction' in genre:
        risks.append("- **Technology explanation:** Balance between explaining and overwhelming")
        risks.append("- **Future plausibility:** Make sure technology serves story, not just spectacle")
    
    if 'mystery' in genre:
        risks.append("- **Fair play:** Reader must have same information as detective")
        risks.append("- **Red herring balance:** Too many = confusing, too few = predictable")
    
    if 'romance' in genre:
        risks.append("- **Conflict dependency:** Avoid manufactured misunderstandings; conflict should feel organic")
        risks.append("- **Emotional pacing:** Build emotional beats carefully; don't rush the relationship")
    
    if 'dark' in atmosphere:
        risks.append("- **Reader fatigue:** Dark stories need moments of levity or hope to prevent exhaustion")
    
    if 'mysterious' in atmosphere:
        risks.append("- **Answer satisfaction:** Mysterious atmosphere needs payoff; questions must be answered")
    
    if 'adventurous' in atmosphere:
        risks.append("- **Stakes escalation:** Each challenge must feel bigger than the last")
        risks.append("- **Character depth:** Don't sacrifice character for action; both matter")
    
    if not risks:
        risks.append("- **Pacing:** Watch for sagging middle sections")
        risks.append("- **Character consistency:** Keep voice and motivation consistent")
        risks.append("- **Theme clarity:** Don't let theme become preachy; show, don't tell")
    
    return '\n'.join(risks)


def main():
    parser = argparse.ArgumentParser(description="Generate Story Bible from Discovery Session")
    parser.add_argument("--discovery", "-d", required=True, help="Path to discovery JSON file")
    parser.add_argument("--output", "-o", help="Output markdown file (default: story-bible.md)")
    
    args = parser.parse_args()
    
    # Load discovery
    discovery_data = load_discovery(args.discovery)
    
    # Generate bible
    bible_content = generate_story_bible(discovery_data)
    
    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = Path("story-bible.md")
    
    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(bible_content)
    
    print(f"\n✓ Story Bible generated: {output_path}")
    print(f"  Based on discovery: {args.discovery}")
    print(f"\nNext steps:")
    print(f"  1. Review and customize the story bible")
    print(f"  2. Fill in character names and world details")
    print(f"  3. Write chapter summaries")
    print(f"  4. Start drafting!")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())