#!/usr/bin/env python3
"""
Book Bible Generator
Creates detailed chapter-by-chapter outline from story bible.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# Handle Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def load_story_bible(filepath):
    """Load story bible markdown file and extract key info."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse story bible (simplified - in real version would parse markdown structure)
    # For now, we'll extract key info from discovery
    return {"content": content}


def generate_book_bible(story_bible_data, discovery_data):
    """Generate detailed book bible with chapter-by-chapter outline."""
    
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
    
    # Get story outline
    story_outline = answers.get('story_outline', 'Hero\'s Journey')
    
    bible = f"""# Book Bible

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Based on: {story_outline}

---

## Project Summary

| Element | Value |
|---------|-------|
| **Chapters** | {num_chapters} |
| **Word Count** | {total_words:,} |
| **Average per Chapter** | ~{avg_words_per_chapter:,} |
| **Structure** | {story_outline} |

---

## Structure Breakdown

### Three-Act Framework

| Act | Chapters | Est. Words | Purpose |
|-----|----------|------------|---------|
| **Act 1 (Setup)** | 1-{act1_chapters} | ~{total_words // 4:,} | Introduce world, characters, inciting incident |
| **Act 2 (Confrontation)** | {act1_chapters + 1}-{act1_chapters + act2_chapters} | ~{total_words // 2:,} | Rising action, complications, midpoint |
| **Act 3 (Resolution)** | {act1_chapters + act2_chapters + 1}-{num_chapters} | ~{total_words // 4:,} | Climax, resolution, denouement |

### Beat Mapping

Based on **{story_outline}**:

"""

    # Add beat mapping based on outline
    bible += generate_beat_mapping(story_outline, num_chapters, total_words)
    
    bible += f"""

---

## Chapter Outline

"""

    # Generate chapter outlines
    for i in range(1, num_chapters + 1):
        act = "Act 1" if i <= act1_chapters else ("Act 2" if i <= act1_chapters + act2_chapters else "Act 3")
        beat = get_beat_for_chapter(i, story_outline, num_chapters)
        
        bible += f"""### Chapter {i}: [Title]

**Act:** {act}
**Beat:** {beat}
**Target:** ~{avg_words_per_chapter:,} words

#### Summary
[One-paragraph summary of what happens in this chapter]

#### Key Events
- [Event 1 - advances plot]
- [Event 2 - character development]
- [Event 3 - world-building/reveal]
- [Event 4 - tension/conflict]

#### Character Development
- **Protagonist:** [What they learn/feel/decide]
- **Antagonist:** [If they appear, what they do]
- **Supporting:** [Key supporting character moments]

#### Scene Breakdown
1. **Scene 1** (Opening)
   - Location: [Where]
   - Purpose: [Hook, establish, introduce]
   - Conflict: [What's at stake]
   - Outcome: [What changes]

2. **Scene 2** (Development)
   - Location: [Where]
   - Purpose: [Advance plot, reveal info]
   - Conflict: [Escalation]
   - Outcome: [New complication]

3. **Scene 3** (Climax)
   - Location: [Where]
   - Purpose: [Chapter climax]
   - Conflict: [Peak tension]
   - Outcome: [Resolution/decision]

4. **Scene 4** (Ending)
   - Location: [Where]
   - Purpose: [Transition to next chapter]
   - Conflict: [New question/hook]
   - Outcome: [What reader wonders next]

#### End Hook
[What question/tension keeps reader turning pages?]

#### Notes
- [Special considerations: POV, tone, pacing]
- [Connections to previous/next chapters]
- [Theme reinforcement]

---

"""

    bible += f"""

---

## Subplot Tracking

### A-Story: Main Plot
- **Chapters:** All
- **Purpose:** Primary conflict and resolution
- **Key beats:** [List major plot points]

### B-Story: Relationship/Character
- **Chapters:** [List chapters where this appears]
- **Purpose:** Character development, emotional core
- **Key beats:** [Relationship milestones]

### C-Story: World/Theme
- **Chapters:** [List chapters where this appears]
- **Purpose:** World-building, theme exploration
- **Key beats:** [Revelations about the world]

---

## Pacing Guide

### Tension Graph
```
Chapter 1-{act1_chapters//2}: Rising tension (setup)
Chapter {act1_chapters//2 + 1}-{act1_chapters}: Peak (inciting incident)
Chapter {act1_chapters + 1}-{act1_chapters + act2_chapters//2}: Fluctuating (exploration)
Chapter {act1_chapters + act2_chapters//2 + 1}-{act1_chapters + int(act2_chapters * 0.75)}: Rising (complications)
Chapter {act1_chapters + int(act2_chapters * 0.75) + 1}-{act1_chapters + act2_chapters}: Peak (all is lost)
Chapter {act1_chapters + act2_chapters + 1}-{num_chapters - 2}: Rising (climax build)
Chapter {num_chapters - 1}-{num_chapters}: Peak then resolution
```

### Breath Moments
- **Chapter {act1_chapters + 3}:** After inciting incident
- **Chapter {act1_chapters + act2_chapters//2 - 1}:** Before midpoint
- **Chapter {act1_chapters + int(act2_chapters * 0.75) + 2}:** After all is lost
- **Chapter {num_chapters - 3}:** Before final climax

---

## Writing Notes

### Chapter Length Strategy
- **Opening chapters (1-3):** Slightly shorter for momentum
- **Middle chapters ({act1_chapters + 1}-{act1_chapters + act2_chapters - 2}):** Can vary, some longer
- **Climax chapters ({num_chapters - 5}-{num_chapters - 1}):** Shorter for pace
- **Final chapter ({num_chapters}):** Appropriate length for resolution

### POV Strategy
- [Which chapters use which POV]
- [POV character for each chapter]

### Style Notes
- **Tone:** {answers.get('atmosphere', 'Not specified')}
- **Pacing:** Vary sentence length by tension
- **Dialogue:** Natural, character-specific
- **Description:** Show through action

---

## Revision Checklist

*To be completed after first draft:*

### Plot
- [ ] Each chapter advances main plot
- [ ] Subplots resolved appropriately
- [ ] No plot holes
- [ ] Setup/payoff balanced

### Character
- [ ] Character voices consistent
- [ ] Arcs progress naturally
- [ ] Motivations clear
- [ ] Relationships develop

### Pacing
- [ ] No sagging middle
- [ ] Tension rises appropriately
- [ ] Breath moments placed well
- [ ] Climax earned

### Style
- [ ] POV consistent
- [ ] Show vs. tell balanced
- [ ] Dialogue natural
- [ ] Sensory details present

---

*This book bible is your roadmap. Follow it, but allow the story to evolve.*
"""

    return bible


def generate_beat_mapping(outline, num_chapters, total_words):
    """Generate beat mapping based on story outline."""
    
    if 'Hero' in outline:
        return f"""
1. **Ordinary World** (Chapters 1-{max(1, num_chapters//12)})
2. **Call to Adventure** (Chapter {max(2, num_chapters//12 + 1)})
3. **Refusal of the Call** (Chapters {max(3, num_chapters//12 + 2)}-{max(4, num_chapters//12 + 3)})
4. **Meeting the Mentor** (Chapter {max(5, num_chapters//12 + 4)})
5. **Crossing the Threshold** (Chapter {max(6, num_chapters//12 + 5)})
6. **Tests, Allies, Enemies** (Chapters {max(7, num_chapters//12 + 6)}-{num_chapters//2})
7. **Approach to the Inmost Cave** (Chapter {num_chapters//2 + 1})
8. **Ordeal** (Chapter {num_chapters//2 + 2})
9. **Reward** (Chapter {num_chapters//2 + 3})
10. **The Road Back** (Chapters {num_chapters//2 + 4}-{int(num_chapters * 0.75)})
11. **Resurrection** (Chapter {int(num_chapters * 0.75) + 1})
12. **Return with the Elixir** (Chapters {int(num_chapters * 0.75) + 2}-{num_chapters})
"""
    elif 'Three-Act' in outline or 'Standard' in outline:
        act1 = max(1, num_chapters//4)
        act2 = max(1, num_chapters//2)
        act3 = max(1, num_chapters//4)
        
        return f"""
1. **Setup** (Chapters 1-{act1//2})
2. **Inciting Incident** (Chapter {act1//2 + 1})
3. **Plot Point 1** (Chapter {act1})
4. **Rising Action** (Chapters {act1 + 1}-{act1 + act2//2})
5. **Midpoint** (Chapter {act1 + act2//2})
6. **Complications** (Chapters {act1 + act2//2 + 1}-{act1 + int(act2 * 0.75)})
7. **Plot Point 2** (Chapter {act1 + int(act2 * 0.75)})
8. **Climax** (Chapters {act1 + int(act2 * 0.75) + 1}-{act1 + act2})
9. **Resolution** (Chapters {act1 + act2 + 1}-{num_chapters - 1})
10. **Denouement** (Chapter {num_chapters})
"""
    else:
        return f"""
1. **Opening** (Chapters 1-{max(1, num_chapters//10)})
2. **Development** (Chapters {max(2, num_chapters//10 + 1)}-{num_chapters//2})
3. **Complications** (Chapters {num_chapters//2 + 1}-{int(num_chapters * 0.75)})
4. **Climax** (Chapters {int(num_chapters * 0.75) + 1}-{num_chapters - 1})
5. **Resolution** (Chapter {num_chapters})
"""


def get_beat_for_chapter(chapter_num, outline, total_chapters):
    """Get beat description for a specific chapter."""
    if 'Hero' in outline:
        beats = [
            (1, "Ordinary World"),
            (total_chapters//12, "Call to Adventure"),
            (total_chapters//6, "Refusal/Meeting Mentor"),
            (total_chapters//4, "Crossing Threshold"),
            (total_chapters//2, "Tests/Approach"),
            (total_chapters//2 + 2, "Ordeal"),
            (total_chapters//2 + 3, "Reward"),
            (int(total_chapters * 0.75), "Road Back"),
            (int(total_chapters * 0.75) + 1, "Resurrection"),
            (total_chapters, "Return with Elixir"),
        ]
    else:
        beats = [
            (1, "Opening"),
            (total_chapters//4, "Inciting Incident"),
            (total_chapters//2, "Midpoint"),
            (int(total_chapters * 0.75), "All Is Lost"),
            (total_chapters - 1, "Climax"),
            (total_chapters, "Resolution"),
        ]
    
    for beat_chapter, beat_name in beats:
        if chapter_num == beat_chapter:
            return f"**{beat_name}**"
    
    # Find closest beat
    closest = min(beats, key=lambda x: abs(x[0] - chapter_num))
    return f"Building toward {closest[1]}"


def main():
    parser = argparse.ArgumentParser(description="Generate Book Bible from Story Bible")
    parser.add_argument("--story-bible", "-s", required=True, help="Path to story bible markdown file")
    parser.add_argument("--discovery", "-d", required=True, help="Path to discovery JSON file")
    parser.add_argument("--output", "-o", help="Output markdown file (default: book-bible.md)")
    
    args = parser.parse_args()
    
    # Load data
    story_bible_data = load_story_bible(args.story_bible)
    
    with open(args.discovery, 'r', encoding='utf-8') as f:
        discovery_data = json.load(f)
    
    # Generate book bible
    bible_content = generate_book_bible(story_bible_data, discovery_data)
    
    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = Path("book-bible.md")
    
    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(bible_content)
    
    print(f"\n✓ Book Bible generated: {output_path}")
    print(f"  Based on: {args.story_bible}")
    print(f"\nNext steps:")
    print(f"  1. Review and customize chapter summaries")
    print(f"  2. Add specific scene details")
    print(f"  3. Start drafting with: python scripts/draft-chapter.py --chapter 1")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())