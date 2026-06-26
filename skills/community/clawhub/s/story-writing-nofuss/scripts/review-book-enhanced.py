#!/usr/bin/env python3
"""
Enhanced Book Review Script with 5-Category Scoring System
Reviews all chapters for quality, flow, and adherence to story bible.
"""

import argparse
import json
import sys
from pathlib import Path
import re
from datetime import datetime

# Handle Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def load_chapters(chapter_dir):
    """Load all chapter files from directory."""
    chapter_dir = Path(chapter_dir)
    chapters = []
    
    for filepath in sorted(chapter_dir.glob("chapter-*.md")):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract chapter number from filename
        match = re.search(r'chapter-(\d+)', filepath.stem)
        chapter_num = int(match.group(1)) if match else 0
        
        chapters.append({
            'number': chapter_num,
            'filename': filepath.name,
            'content': content,
            'word_count': len(content.split())
        })
    
    return sorted(chapters, key=lambda x: x['number'])


def load_book_bible(filepath):
    """Load book bible for reference."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def get_assessment_text(score):
    """Get text assessment based on score."""
    if score >= 9:
        return "Excellent"
    elif score >= 8:
        return "Very Good"
    elif score >= 7:
        return "Good"
    elif score >= 6:
        return "Adequate"
    else:
        return "Needs Work"


def get_score_bar(score, width=10):
    """Create a visual score bar."""
    filled = int(score)
    return "█" * filled + "░" * (width - filled)


def calculate_category_scores(chapters, book_bible_content, discovery_data):
    """Calculate scores for 5 review categories."""
    
    answers = discovery_data.get('answers', {})
    genre = answers.get('genre', '')
    atmosphere = answers.get('atmosphere', '')
    
    scores = {
        'plot': {'score': 0, 'max': 10, 'comments': []},
        'story_line': {'score': 0, 'max': 10, 'comments': []},
        'dramas': {'score': 0, 'max': 10, 'comments': []},
        'love_sensuality': {'score': 0, 'max': 10, 'comments': []},
        'humanity': {'score': 0, 'max': 10, 'comments': []}
    }
    
    # 1. PLOT SCORE (Structure, pacing, beats)
    plot_score = 8  # Base score
    
    # Check for clear 3-act structure
    if len(chapters) >= 3:
        # Act 1 setup (first 25%)
        setup_chapters = chapters[:max(1, len(chapters)//4)]
        # Act 2 confrontation (middle 50%)
        middle_chapters = chapters[max(1, len(chapters)//4):-max(1, len(chapters)//4)]
        # Act 3 resolution (last 25%)
        resolution_chapters = chapters[-max(1, len(chapters)//4):]
        
        if len(setup_chapters) > 0 and len(middle_chapters) > 0 and len(resolution_chapters) > 0:
            plot_score += 0.5
            scores['plot']['comments'].append("✓ Clear 3-act structure")
        else:
            plot_score -= 0.5
            scores['plot']['comments'].append("⚠️ Structure could be clearer")
    
    # Check for rising tension
    middle_word_avg = sum(c['word_count'] for c in chapters[len(chapters)//3:2*len(chapters)//3]) // max(1, len(chapters)//3)
    overall_avg = sum(c['word_count'] for c in chapters) // len(chapters)
    
    if middle_word_avg >= overall_avg * 0.9:
        plot_score += 0.5
        scores['plot']['comments'].append("✓ Good tension in middle section")
    else:
        plot_score -= 0.5
        scores['plot']['comments'].append("⚠️ Middle section may sag")
    
    # Check for climax positioning
    climax_position = len(chapters) * 0.85  # Ideal climax at 85%
    last_quarter = chapters[int(len(chapters)*0.75):]
    if len(last_quarter) > 0:
        plot_score += 0.5
        scores['plot']['comments'].append("✓ Climax positioned well")
    
    scores['plot']['score'] = min(10, max(1, plot_score))
    
    # 2. STORY LINE SCORE (Emotional coherence, character arcs)
    story_line_score = 9  # Base score
    
    # Check for character development
    char_names = set()
    for chapter in chapters:
        # Simple character name detection
        words = re.findall(r'\b[A-Z][a-z]+\b', chapter['content'])
        char_names.update([w for w in words if len(w) > 2 and w not in ['The', 'And', 'But', 'For', 'She', 'He', 'They']])
    
    if len(char_names) >= 2:
        story_line_score += 0.5
        scores['story_line']['comments'].append(f"✓ {len(char_names)} distinct characters")
    else:
        story_line_score -= 1
        scores['story_line']['comments'].append("⚠️ Limited character development")
    
    # Check for emotional consistency with atmosphere
    atmosphere_map = {
        'dark/gritty': ['dark', 'grim', 'bleak', 'harsh'],
        'hopeful/uplifting': ['hope', 'light', 'warm', 'bright'],
        'mysterious/enigmatic': ['secret', 'mystery', 'unknown', 'hidden'],
        'romantic/sensual': ['love', 'touch', 'warmth', 'heart'],
        'adventurous/exciting': ['action', 'thrill', 'danger', 'race']
    }
    
    target_atmosphere = atmosphere.lower()
    atmosphere_words = atmosphere_map.get(target_atmosphere, [])
    
    if atmosphere_words:
        atmosphere_count = sum(1 for word in atmosphere_words 
                              if any(word in chapter['content'].lower() for chapter in chapters))
        if atmosphere_count >= 5:
            story_line_score += 0.5
            scores['story_line']['comments'].append(f"✓ Atmosphere consistent with '{atmosphere}'")
    
    scores['story_line']['score'] = min(10, max(1, story_line_score))
    
    # 3. DRAMAS SCORE (Conflict, tension, stakes)
    dramas_score = 7  # Base score
    
    # Check for conflict in each chapter
    conflict_words = ['but', 'however', 'yet', 'although', 'despite', 'conflict', 'problem', 'danger', 'threat']
    chapters_with_conflict = 0
    
    for chapter in chapters:
        conflict_count = sum(1 for word in conflict_words if word in chapter['content'].lower())
        if conflict_count >= 2:
            chapters_with_conflict += 1
    
    conflict_percentage = chapters_with_conflict / len(chapters) if chapters else 0
    
    if conflict_percentage >= 0.8:
        dramas_score += 1.5
        scores['dramas']['comments'].append("✓ Strong conflict throughout")
    elif conflict_percentage >= 0.5:
        dramas_score += 0.5
        scores['dramas']['comments'].append("✓ Moderate conflict level")
    else:
        dramas_score -= 1
        scores['dramas']['comments'].append("⚠️ Conflict could be stronger")
    
    # Check for external obstacles (medical crisis, storms, etc.)
    external_obstacles = ['storm', 'fever', 'sick', 'injured', 'broken', 'lost', 'trapped', 'attack']
    external_count = sum(1 for word in external_obstacles 
                        if any(word in chapter['content'].lower() for chapter in chapters))
    
    if external_count >= 3:
        dramas_score += 1
        scores['dramas']['comments'].append("✓ Good external obstacles")
    elif external_count >= 1:
        dramas_score += 0.5
        scores['dramas']['comments'].append("✓ Some external obstacles")
    else:
        dramas_score -= 0.5
        scores['dramas']['comments'].append("⚠️ Consider adding external obstacles")
    
    scores['dramas']['score'] = min(10, max(1, dramas_score))
    
    # 4. LOVE & SENSUALITY SCORE (Relationships, emotional intimacy)
    love_score = 8  # Base score
    
    # Check for relationship development
    relationship_words = ['love', 'care', 'touch', 'hand', 'heart', 'together', 'alone', 'connection']
    relationship_count = sum(1 for word in relationship_words 
                           if any(word in chapter['content'].lower() for chapter in chapters))
    
    if relationship_count >= 10:
        love_score += 1
        scores['love_sensuality']['comments'].append("✓ Strong relationship development")
    elif relationship_count >= 5:
        love_score += 0.5
        scores['love_sensuality']['comments'].append("✓ Moderate relationship development")
    else:
        love_score -= 0.5
        scores['love_sensuality']['comments'].append("⚠️ Relationship could be deeper")
    
    # Check for emotional intimacy over physical
    emotional_words = ['understand', 'listen', 'share', 'memory', 'story', 'truth', 'vulnerable']
    physical_words = ['kiss', 'sex', 'body', 'physical', 'touch', 'embrace']
    
    emotional_count = sum(1 for word in emotional_words 
                         if any(word in chapter['content'].lower() for chapter in chapters))
    physical_count = sum(1 for word in physical_words 
                        if any(word in chapter['content'].lower() for chapter in chapters))
    
    if emotional_count > physical_count * 2:
        love_score += 1
        scores['love_sensuality']['comments'].append("✓ Emotional intimacy prioritized (good)")
    elif emotional_count > physical_count:
        love_score += 0.5
        scores['love_sensuality']['comments'].append("✓ Balanced emotional/physical")
    
    scores['love_sensuality']['score'] = min(10, max(1, love_score))
    
    # 5. HUMANITY SCORE (Theme, meaning, emotional impact)
    humanity_score = 9  # Base score
    
    # Check for theme words
    theme_words = ['human', 'humanity', 'legacy', 'memory', 'hope', 'survival', 'choice', 'meaning', 'purpose']
    theme_count = sum(1 for word in theme_words 
                     if any(word in chapter['content'].lower() for chapter in chapters))
    
    if theme_count >= 5:
        humanity_score += 1
        scores['humanity']['comments'].append("✓ Strong thematic elements")
    elif theme_count >= 3:
        humanity_score += 0.5
        scores['humanity']['comments'].append("✓ Some thematic depth")
    
    # Check for hope in bleak settings
    if 'post-apocalyptic' in genre.lower() or 'dystopian' in genre.lower():
        hope_words = ['hope', 'light', 'future', 'tomorrow', 'rebuild', 'grow', 'heal']
        hope_count = sum(1 for word in hope_words 
                        if any(word in chapter['content'].lower() for chapter in chapters))
        
        if hope_count >= 3:
            humanity_score += 1
            scores['humanity']['comments'].append("✓ Hope present in bleak setting")
        elif hope_count >= 1:
            humanity_score += 0.5
            scores['humanity']['comments'].append("✓ Some hope elements")
    
    scores['humanity']['score'] = min(10, max(1, humanity_score))
    
    return scores


def generate_grammar_analysis(chapters):
    """Generate detailed grammar and style analysis."""
    
    total_words = sum(c['word_count'] for c in chapters)
    
    # Count filter words
    filter_words = ['felt', 'saw', 'heard', 'noticed', 'realized', 'watched', 'looked', 'seemed', 'appeared']
    filter_counts = {}
    
    for word in filter_words:
        count = sum(len(re.findall(rf'\b{word}\b', c['content'].lower())) for c in chapters)
        if count > 0:
            filter_counts[word] = count
    
    # Count adverbs
    adverb_count = sum(len(re.findall(r'\w+ly\b', c['content'])) for c in chapters)
    
    # Count passive voice
    passive_count = sum(len(re.findall(r'\b(am|is|are|was|were|be|being|been)\s+\w+ed\b', c['content'].lower())) 
                       for c in chapters)
    
    # Count dialogue tags
    dialogue_tags = ['said', 'asked', 'replied', 'whispered', 'shouted', 'muttered', 'exclaimed']
    tag_count = sum(sum(len(re.findall(rf'\b{tag}\b', c['content'].lower())) for tag in dialogue_tags) 
                   for c in chapters)
    
    return {
        'total_words': total_words,
        'filter_words': filter_counts,
        'adverb_count': adverb_count,
        'passive_count': passive_count,
        'dialogue_tag_count': tag_count,
        'chapters': len(chapters)
    }


def generate_recommendations(scores, grammar_analysis, chapters):
    """Generate specific recommendations based on scores."""
    
    recommendations = {
        'critical': [],
        'high': [],
        'medium': [],
        'low': []
    }
    
    # Critical recommendations (score < 6)
    for category, data in scores.items():
        if data['score'] < 6:
            category_name = category.replace('_', ' ').title()
            recommendations['critical'].append(
                f"**{category_name} ({data['score']}/10):** Major improvement needed"
            )
    
    # High priority (score 6-7)
    for category, data in scores.items():
        if 6 <= data['score'] < 7.5:
            category_name = category.replace('_', ' ').title()
            recommendations['high'].append(
                f"**{category_name} ({data['score']}/10):** Significant improvement possible"
            )
    
    # Grammar recommendations
    if grammar_analysis['filter_words']:
        total_filter = sum(grammar_analysis['filter_words'].values())
        if total_filter > 20:
            recommendations['high'].append(
                f"**Filter words ({total_filter} instances):** Replace with action, show don't tell"
            )
    
    if grammar_analysis['adverb_count'] > 30:
        recommendations['medium'].append(
            f"**Adverbs ({grammar_analysis['adverb_count']} instances):** Consider stronger verbs"
        )
    
    if grammar_analysis['passive_count'] > 20:
        recommendations['medium'].append(
            f"**Passive voice ({grammar_analysis['passive_count']} instances):** Use active voice for stronger prose"
        )
    
    # Drama recommendations
    if scores['dramas']['score'] < 8:
        recommendations['high'].append(
            "**Drama enhancement:** Add external obstacles (medical crisis, storms, threats)"
        )
    
    # Check chapter hooks
    hooks_missing = 0
    for i, chapter in enumerate(chapters):
        if i < len(chapters) - 1:
            last_para = chapter['content'].strip().split('\n')[-1]
            if len(last_para) < 50 or not any(q in last_para for q in ['?', 'but', 'however', 'yet', 'suddenly']):
                hooks_missing += 1
    
    if hooks_missing > len(chapters) * 0.3:  # More than 30% missing hooks
        recommendations['medium'].append(
            f"**Chapter hooks:** {hooks_missing} chapters need stronger ending hooks"
        )
    
    return recommendations


def generate_review_report(chapters, scores, grammar_analysis, recommendations, discovery_data):
    """Generate comprehensive review report."""
    
    answers = discovery_data.get('answers', {})
    total_words = sum(c['word_count'] for c in chapters)
    
    # Calculate overall score
    overall_score = sum(data['score'] for data in scores.values()) / len(scores)
    
    report = f"""# Book Review: {answers.get('title', 'Untitled')}

**Review Date:** {datetime.now().strftime('%Y-%m-%d')}  
**Total Chapters:** {len(chapters)}  
**Total Words:** {total_words:,}  
**Target:** {answers.get('word_count_target', 'N/A')} words ({total_words/int(answers.get('word_count_target', total_words))*100 if answers.get('word_count_target') else 100:.1f}% of target)

---

## 📊 **SCORING SUMMARY**

### **Overall Composite: {overall_score:.1f}/10**

| Category | Score | Assessment |
|----------|-------|------------|
| **Plot** | {scores['plot']['score']:.1f}/10 | {get_assessment_text(scores['plot']['score'])} |
| **Story Line** | {scores['story_line']['score']:.1f}/10 | {get_assessment_text(scores['story_line']['score'])} |
| **Dramas** | {scores['dramas']['score']:.1f}/10 | {get_assessment_text(scores['dramas']['score'])} |
| **Love & Sensuality** | {scores['love_sensuality']['score']:.1f}/10 | {get_assessment_text(scores['love_sensuality']['score'])} |
| **Humanity** | {scores['humanity']['score']:.1f}/10 | {get_assessment_text(scores['humanity']['score'])} |

### **Score Breakdown:**
```
Plot:        {get_score_bar(scores['plot']['score'])} {scores['plot']['score']:.1f}/10
Story Line:  {get_score_bar(scores['story_line']['score'])} {scores['story_line']['score']:.1f}/10  
Dramas:      {get_score_bar(scores['dramas']['score'])} {scores['dramas']['score']:.1f}/10
Love/Sens:   {get_score_bar(scores['love_sensuality']['score'])} {scores['love_sensuality']['score']:.1f}/10
Humanity:    {get_score_bar(scores['humanity']['score'])} {scores['humanity']['score']:.1f}/10
────────────────────────────
Overall:     {get_score_bar(overall_score)} {overall_score:.1f}/10
```

---

## 📝 **CATEGORY DETAILS**

### **1. Plot ({scores['plot']['score']:.1f}/10)**
**Comments:**
"""
    
    for comment in scores['plot']['comments']:
        report += f"- {comment}\n"
    
    report += f"""
**Key Factors:** Structure, pacing, plot beats, climax positioning

### **2. Story Line ({scores['story_line']['score']:.1f}/10)**
**Comments:**
"""
    
    for comment in scores['story_line']['comments']:
        report += f"- {comment}\n"
    
    report += f"""
**Key Factors:** Emotional coherence, character arcs, atmosphere consistency

### **3. Dramas ({scores['dramas']['score']:.1f}/10)**
**Comments:**
"""
    
    for comment in scores['dramas']['comments']:
        report += f"- {comment}\n"
    
    report += f"""
**Key Factors:** Conflict, tension, external obstacles, stakes

### **4. Love & Sensuality ({scores['love_sensuality']['score']:.1f}/10)**
**Comments:**
"""
    
    for comment in scores['love_sensuality']['comments']:
        report += f"- {comment}\n"
    
    report += f"""
**Key Factors:** Relationship development, emotional intimacy, appropriate sensuality

### **5. Humanity ({scores['humanity']['score']:.1f}/10)**
**Comments:**
"""
    
    for comment in scores['humanity']['comments']:
        report += f"- {comment}\n"
    
    report += f"""
**Key Factors:** Theme exploration, emotional impact, meaning, hope in bleakness

---

## 🔍 **GRAMMAR & STYLE ANALYSIS**

**Total Words:** {grammar_analysis['total_words']:,}
**Average Chapter Length:** {grammar_analysis['total_words']//grammar_analysis['chapters']:,} words

### **Issues Found:**
"""
    
    if grammar_analysis['filter_words']:
        total_filter = sum(grammar_analysis['filter_words'].values())
        report += f"- **Filter words:** {total_filter} instances\n"
        for word, count in grammar_analysis['filter_words'].items():
            if count > 5:
                report += f"  - '{word}': {count} times\n"
    
    if grammar_analysis['adverb_count'] > 0:
        report += f"- **Adverbs:** {grammar_analysis['adverb_count']} instances\n"
    
    if grammar_analysis['passive_count'] > 0:
        report += f"- **Passive voice:** {grammar_analysis['passive_count']} instances\n"
    
    if grammar_analysis['dialogue_tag_count'] > 0:
        report += f"- **Dialogue tags:** {grammar_analysis['dialogue_tag_count']} instances\n"
    
    report += f"""

### **Recommendations:**
"""
    
    if grammar_analysis['filter_words']:
        total_filter = sum(grammar_analysis['filter_words'].values())
        if total_filter > 20:
            report += "- **High priority:** Replace filter words with action (show don't tell)\n"
        elif total_filter > 10:
            report += "- **Medium priority:** Reduce filter words for stronger prose\n"
    
    if grammar_analysis['adverb_count'] > 30:
        report += "- **High priority:** Reduce adverbs, use stronger verbs\n"
    elif grammar_analysis['adverb_count'] > 15:
        report += "- **Medium priority:** Consider reducing adverbs\n"
    
    if grammar_analysis['passive_count'] > 20:
        report += "- **High priority:** Convert passive to active voice\n"
    elif grammar_analysis['passive_count'] > 10:
        report += "- **Medium priority:** Reduce passive voice\n"
    
    report += f"""

---

## 🎯 **RECOMMENDATIONS BY PRIORITY**

### **Critical (Must Fix)**
"""
    
    if recommendations['critical']:
        for rec in recommendations['critical']:
            report += f"- {rec}\n"
    else:
        report += "- No critical issues found ✓\n"
    
    report += f"""

### **High Priority (Should Fix)**
"""
    
    if recommendations['high']:
        for rec in recommendations['high']:
            report += f"- {rec}\n"
    else:
        report += "- No high priority issues found ✓\n"
    
    report += f"""

### **Medium Priority (Consider Fixing)**
"""
    
    if recommendations['medium']:
        for rec in recommendations['medium']:
            report += f"- {rec}\n"
    else:
        report += "- No medium priority issues found ✓\n"
    
    report += f"""

### **Low Priority (Optional Improvements)**
"""
    
    if recommendations['low']:
        for rec in recommendations['low']:
            report += f"- {rec}\n"
    else:
        report += "- No low priority issues found ✓\n"
    
    report += f"""

---

## 📈 **CHAPTER STATISTICS**

**Chapter Length Distribution:**
"""
    
    word_counts = [c['word_count'] for c in chapters]
    avg_length = sum(word_counts) // len(word_counts)
    
    report += f"- **Average:** {avg_length:,} words\n"
    report += f"- **Shortest:** Chapter {min(range(len(word_counts)), key=lambda i: word_counts[i])+1} ({min(word_counts):,} words)\n"
    report += f"- **Longest:** Chapter {max(range(len(word_counts)), key=lambda i: word_counts[i])+1} ({max(word_counts):,} words)\n"
    report += f"- **Range:** {max(word_counts) - min(word_counts):,} words difference\n"
    
    # Check for pacing issues
    middle_start = len(chapters) // 3
    middle_end = 2 * len(chapters) // 3
    middle_avg = sum(word_counts[middle_start:middle_end]) // max(1, middle_end - middle_start)
    
    if middle_avg < avg_length * 0.9:
        report += "- **⚠️ Warning:** Middle section may be sagging (lower word count)\n"
    else:
        report += "- **✓ Good:** Middle section maintains tension\n"
    
    report += f"""

### **Chapter-by-Chapter Word Count:**
```
"""
    
    for i, chapter in enumerate(chapters, 1):
        report += f"Chapter {i:2d}: {chapter['word_count']:5,} words\n"
    
    report += f"""```

---

## 🏆 **PUBLICATION READINESS ASSESSMENT**

### **Current State:**
"""
    
    if overall_score >= 9:
        report += "**Publication Ready - Excellent Quality**\n"
        report += "- Grammar: Professional level\n"
        report += "- Structure: Solid\n"
        report += "- Theme: Powerful and coherent\n"
        report += "- Ready for submission to literary magazines\n"
    elif overall_score >= 8:
        report += "**Near Publication Ready - Very Good Quality**\n"
        report += "- Minor polishing needed\n"
        report += "- Strong foundation\n"
        report += "- Ready after addressing high priority recommendations\n"
    elif overall_score >= 7:
        report += "**Good Draft - Needs Revision**\n"
        report += "- Solid foundation but needs work\n"
        report += "- Address critical and high priority issues\n"
        report += "- Consider beta reader feedback\n"
    else:
        report += "**Early Draft - Significant Revision Needed**\n"
        report += "- Focus on major structural issues first\n"
        report += "- Consider rewriting weak sections\n"
        report += "- Get feedback before major revisions\n"
    
    report += f"""

### **Target Markets (if {overall_score:.1f}/10 ≥ 8.0):**
- **Literary Magazines:** Clarkesworld, Asimov's, F&SF
- **Online Platforms:** Daily Science Fiction, Beneath Ceaseless Skies
- **Contests:** Writers of the Future, etc.

### **Next Steps:**
1. Address recommendations by priority
2. Final proofread for typos
3. Format for submission
4. Write query letter
5. Submit to target markets

---

## 📋 **FINAL ASSESSMENT**

**Strengths:**
- [List key strengths based on highest scores]

**Areas for Improvement:**
- [List areas based on lowest scores]

**Overall Verdict:**
This story scores **{overall_score:.1f}/10** overall. {get_verdict_text(overall_score)}

---

*Review generated by Story Writer Skill - Enhanced Scoring System*
"""
    
    return report


def get_verdict_text(score):
    """Get verdict text based on overall score."""
    if score >= 9:
        return "Exceptional quality - ready for immediate submission."
    elif score >= 8:
        return "Very good quality - minor polishing needed before submission."
    elif score >= 7:
        return "Good foundation - needs revision before publication."
    elif score >= 6:
        return "Adequate draft - significant revision needed."
    else:
        return "Early draft - focus on major structural issues first."


def main():
    parser = argparse.ArgumentParser(description="Enhanced Book Review with 5-Category Scoring")
    parser.add_argument("--chapters", "-c", required=True, help="Directory containing chapter files")
    parser.add_argument("--book-bible", "-b", required=True, help="Path to book bible markdown file")
    parser.add_argument("--discovery", "-d", required=True, help="Path to discovery JSON file")
    parser.add_argument("--output", "-o", default="review-notes-enhanced.md", help="Output file")
    parser.add_argument("--fix", action="store_true", help="Attempt to auto-fix minor issues")
    
    args = parser.parse_args()
    
    # Load data
    chapters = load_chapters(args.chapters)
    
    if not chapters:
        print(f"Error: No chapter files found in {args.chapters}")
        return 1
    
    book_bible_content = load_book_bible(args.book_bible)
    
    with open(args.discovery, 'r', encoding='utf-8') as f:
        discovery_data = json.load(f)
    
    # Calculate scores
    scores = calculate_category_scores(chapters, book_bible_content, discovery_data)
    
    # Generate grammar analysis
    grammar_analysis = generate_grammar_analysis(chapters)
    
    # Generate recommendations
    recommendations = generate_recommendations(scores, grammar_analysis, chapters)
    
    # Generate report
    report = generate_review_report(chapters, scores, grammar_analysis, recommendations, discovery_data)
    
    # Write report
    output_path = Path(args.output)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    # Print summary
    overall_score = sum(data['score'] for data in scores.values()) / len(scores)
    
    print(f"\n✓ Enhanced review complete: {output_path}")
    print(f"  Chapters reviewed: {len(chapters)}")
    print(f"  Total words: {sum(c['word_count'] for c in chapters):,}")
    print(f"  Overall score: {overall_score:.1f}/10")
    print(f"\n  Category scores:")
    for category, data in scores.items():
        category_name = category.replace('_', ' ').title()
        print(f"    {category_name:20} {data['score']:.1f}/10")
    
    # Count recommendations
    total_recs = sum(len(recs) for recs in recommendations.values())
    print(f"\n  Recommendations: {total_recs} total")
    print(f"    Critical: {len(recommendations['critical'])}")
    print(f"    High: {len(recommendations['high'])}")
    print(f"    Medium: {len(recommendations['medium'])}")
    print(f"    Low: {len(recommendations['low'])}")
    
    if args.fix:
        print("\nAuto-fix not yet implemented. Review report for manual fixes.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())