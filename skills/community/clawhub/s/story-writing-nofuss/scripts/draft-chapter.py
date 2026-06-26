#!/usr/bin/env python3
"""
Chapter Drafting Script
Writes actual story text chapter by chapter based on book bible.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# Handle Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def load_book_bible(filepath):
    """Load book bible and parse chapter information."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse chapters from book bible
    chapters = []
    lines = content.split('\n')
    
    current_chapter = None
    in_chapter = False
    chapter_content = []
    
    for line in lines:
        if line.startswith('### Chapter '):
            if current_chapter:
                chapters.append({
                    'number': current_chapter,
                    'content': '\n'.join(chapter_content)
                })
            
            # Extract chapter number
            import re
            match = re.search(r'Chapter (\d+):', line)
            current_chapter = int(match.group(1)) if match else len(chapters) + 1
            chapter_content = [line]
            in_chapter = True
        
        elif in_chapter and line.startswith('### '):
            # Next chapter or section
            if current_chapter:
                chapters.append({
                    'number': current_chapter,
                    'content': '\n'.join(chapter_content)
                })
            current_chapter = None
            in_chapter = False
            chapter_content = []
        
        elif in_chapter:
            chapter_content.append(line)
    
    # Add last chapter
    if current_chapter:
        chapters.append({
            'number': current_chapter,
            'content': '\n'.join(chapter_content)
        })
    
    return {
        'content': content,
        'chapters': chapters
    }


def generate_chapter_content(chapter_info, discovery_data, chapter_num):
    """Generate actual story text for a chapter."""
    
    answers = discovery_data.get('answers', {})
    genre = answers.get('genre', 'Literary Fiction')
    atmosphere = answers.get('atmosphere', 'Hopeful/Uplifting')
    
    # Extract chapter summary from book bible
    chapter_text = chapter_info.get('content', '')
    
    # Parse summary (simplified - in real version would extract better)
    summary = "A chapter in the story."
    if "Summary" in chapter_text:
        lines = chapter_text.split('\n')
        for i, line in enumerate(lines):
            if "Summary" in line and i + 1 < len(lines):
                summary = lines[i + 1].strip()
                if summary.startswith('['):
                    summary = summary[1:-1] if summary.endswith(']') else summary[1:]
                break
    
    # Generate chapter content based on genre and atmosphere
    content = f"""# Chapter {chapter_num}

{get_chapter_opening(genre, atmosphere, chapter_num)}

{generate_scene_content(genre, atmosphere, "Scene 1", chapter_num)}

{generate_scene_content(genre, atmosphere, "Scene 2", chapter_num)}

{generate_scene_content(genre, atmosphere, "Scene 3", chapter_num)}

{get_chapter_ending(genre, atmosphere, chapter_num)}
"""
    
    return content


def get_chapter_opening(genre, atmosphere, chapter_num):
    """Generate chapter opening based on genre and atmosphere."""
    
    openings = {
        'Literary Fiction': [
            f"The morning light filtered through the window, casting long shadows across the room.",
            f"Memory has a way of distorting things, but this moment remained sharp and clear.",
            f"It began, as most things do, with a simple choice.",
        ],
        'Fantasy': [
            f"The air in the ancient chamber grew still, as if holding its breath.",
            f"Beyond the city walls, the forest whispered secrets only the brave could hear.",
            f"A single star fell from the sky, and with it, everything changed.",
        ],
        'Science Fiction': [
            f"The console blinked with urgent warnings, each more dire than the last.",
            f"In the silence of deep space, even thoughts seemed to echo.",
            f"The data stream revealed what no one had dared to suspect.",
        ],
        'Mystery': [
            f"The phone rang at precisely 3:17 AM, as it had every night for a week.",
            f"Something was wrong. The room felt different, though nothing appeared moved.",
            f"The letter arrived with no return address, just a single sentence inside.",
        ],
        'Romance': [
            f"Their eyes met across the crowded room, and for a moment, time stood still.",
            f"Sometimes love arrives quietly, like the first snow of winter.",
            f"She hadn't expected to find anything here, least of all him.",
        ],
    }
    
    # Default to Literary Fiction if genre not found
    genre_key = next((g for g in openings.keys() if g in genre), 'Literary Fiction')
    
    import random
    opening = random.choice(openings[genre_key])
    
    # Adjust for atmosphere
    if 'Dark' in atmosphere:
        opening = f"Darkness clung to the edges of the room. {opening.lower()}"
    elif 'Hopeful' in atmosphere:
        opening = f"A sense of possibility hung in the air. {opening.lower()}"
    elif 'Mysterious' in atmosphere:
        opening = f"Secrets whispered in the silence. {opening.lower()}"
    
    return opening


def generate_scene_content(genre, atmosphere, scene_name, chapter_num):
    """Generate scene content."""
    
    scene_templates = {
        'Literary Fiction': [
            "Character reflected on the past, seeing connections they'd missed before.",
            "A conversation revealed hidden tensions and unspoken truths.",
            "The setting itself seemed to comment on the character's internal state.",
        ],
        'Fantasy': [
            "Magic shimmered in the air, responding to unspoken emotions.",
            "An ancient prophecy seemed to edge closer to fulfillment.",
            "The landscape itself held memories of battles long forgotten.",
        ],
        'Science Fiction': [
            "Technology both solved and created problems in equal measure.",
            "The implications of the discovery were only beginning to surface.",
            "Humanity's place in the universe was called into question.",
        ],
        'Mystery': [
            "A clue emerged, contradicting everything they thought they knew.",
            "The suspect's alibi had a single, tiny flaw.",
            "Someone was lying, but the question was why.",
        ],
        'Romance': [
            "A moment of vulnerability created unexpected intimacy.",
            "Misunderstandings threatened what was just beginning to grow.",
            "External forces conspired to keep them apart.",
        ],
    }
    
    genre_key = next((g for g in scene_templates.keys() if g in genre), 'Literary Fiction')
    
    import random
    scene_content = random.choice(scene_templates[genre_key])
    
    # Add dialogue based on genre
    dialogue = generate_dialogue(genre, atmosphere)
    
    return f"""## {scene_name}

{scene_content}

{dialogue}

[Additional scene development based on book bible outline]
"""


def generate_dialogue(genre, atmosphere):
    """Generate sample dialogue based on genre and atmosphere."""
    
    dialogues = {
        'Literary Fiction': [
            '"I never realized," she said, her voice barely a whisper.',
            '"Sometimes the truth is too heavy to carry alone," he replied.',
            '"What are we afraid of?" she asked the empty room.',
        ],
        'Fantasy': [
            '"The old magic stirs," the elder warned.',
            '"Not all prophecies are meant to be fulfilled," the mage cautioned.',
            '"What price would you pay for power?" the voice echoed.',
        ],
        'Science Fiction': [
            '"The readings don\'t make sense," the scientist reported.',
            '"We\'re not alone out here," the pilot whispered.',
            '"What does it mean to be human?" the AI asked.',
        ],
        'Mystery': [
            '"There\'s something you\'re not telling me," the detective said.',
            '"I was there, but I didn\'t see anything," the witness insisted.',
            '"The pieces don\'t fit," she muttered, staring at the evidence.',
        ],
        'Romance': [
            '"I didn\'t expect to find you here," he said softly.',
            '"Sometimes the heart knows what the mind denies," she replied.',
            '"What if we\'re making a mistake?" he asked, though he already knew the answer.',
        ],
    }
    
    genre_key = next((g for g in dialogues.keys() if g in genre), 'Literary Fiction')
    
    import random
    return random.choice(dialogues[genre_key])


def get_chapter_ending(genre, atmosphere, chapter_num):
    """Generate chapter ending hook."""
    
    endings = {
        'Literary Fiction': [
            "And so the question remained, unanswered but no longer unasked.",
            "The decision, once made, could not be unmade.",
            "Tomorrow would bring answers, or perhaps only more questions.",
        ],
        'Fantasy': [
            "The path ahead was clear, but the cost was yet unknown.",
            "Power called, but at what price?",
            "The first step had been taken; there was no turning back now.",
        ],
        'Science Fiction': [
            "The data suggested possibilities too terrifying to contemplate.",
            "Humanity stood at a crossroads, though few realized it.",
            "The truth, once revealed, changed everything.",
        ],
        'Mystery': [
            "One piece of the puzzle remained, and it changed everything.",
            "The killer was closer than anyone suspected.",
            "The next move would be the most dangerous yet.",
        ],
        'Romance': [
            "Their eyes met, and in that moment, everything changed.",
            "The words hung between them, unspoken but understood.",
            "Love, it seemed, had been there all along.",
        ],
    }
    
    genre_key = next((g for g in endings.keys() if g in genre), 'Literary Fiction')
    
    import random
    ending = random.choice(endings[genre_key])
    
    # Add hook for next chapter
    hooks = [
        "But what happened next would surprise them all.",
        "Little did they know, the real challenge was just beginning.",
        "The consequences would arrive sooner than expected.",
    ]
    
    hook = random.choice(hooks)
    
    return f"{ending}\n\n{hook}"


def main():
    parser = argparse.ArgumentParser(description="Draft Chapters from Book Bible")
    parser.add_argument("--book-bible", "-b", required=True, help="Path to book bible markdown file")
    parser.add_argument("--discovery", "-d", required=True, help="Path to discovery JSON file")
    parser.add_argument("--chapter", "-c", type=int, help="Specific chapter to draft (omit for all)")
    parser.add_argument("--all", action="store_true", help="Draft all chapters")
    parser.add_argument("--output-dir", "-o", default="chapters", help="Output directory for chapters")
    
    args = parser.parse_args()
    
    # Load data
    book_bible_data = load_book_bible(args.book_bible)
    
    with open(args.discovery, 'r', encoding='utf-8') as f:
        discovery_data = json.load(f)
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Determine which chapters to draft
    if args.chapter:
        chapters_to_draft = [args.chapter]
    elif args.all:
        chapters_to_draft = list(range(1, len(book_bible_data['chapters']) + 1))
    else:
        print("Please specify --chapter X or --all")
        return 1
    
    # Draft chapters
    for chapter_num in chapters_to_draft:
        # Find chapter info
        chapter_info = None
        for chap in book_bible_data['chapters']:
            if chap['number'] == chapter_num:
                chapter_info = chap
                break
        
        if not chapter_info:
            print(f"Warning: Chapter {chapter_num} not found in book bible")
            continue
        
        # Generate content
        content = generate_chapter_content(chapter_info, discovery_data, chapter_num)
        
        # Write to file
        output_file = output_dir / f"chapter-{chapter_num:02d}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Drafted: {output_file}")
    
    print(f"\nTotal chapters drafted: {len(chapters_to_draft)}")
    print(f"Location: {output_dir}/")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())