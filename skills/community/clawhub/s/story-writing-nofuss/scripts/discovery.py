#!/usr/bin/env python3
"""
Story Discovery Questionnaire
Interactive process with 10 curated suggestions per question.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# Handle Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


# Question definitions with 10 suggestions each
QUESTIONS = {
    "scope_chapters": {
        "question": "How many chapters are you planning?",
        "suggestions": [
            ("12 chapters", "novella, tight pacing"),
            ("18 chapters", "shorter novel"),
            ("24 chapters", "standard novel length"),
            ("30 chapters", "fuller novel"),
            ("36 chapters", "epic fantasy typical"),
            ("40 chapters", "long novel"),
            ("50 chapters", "saga"),
            ("60 chapters", "multi-book feel"),
            ("80 chapters", "epic series"),
            ("100+ chapters", "multi-part epic"),
        ]
    },
    "scope_words": {
        "question": "What's your target word count?",
        "suggestions": [
            ("5,000 words", "short story"),
            ("15,000 words", "novelette"),
            ("30,000 words", "novella"),
            ("50,000 words", "short novel"),
            ("80,000 words", "standard novel"),
            ("100,000 words", "full-length novel"),
            ("120,000 words", "epic novel"),
            ("150,000 words", "fantasy/sci-fi typical"),
            ("200,000 words", "doorstopper"),
            ("300,000+ words", "epic saga"),
        ]
    },
    "genre": {
        "question": "What's the genre and sub-genre?",
        "suggestions": [
            ("Literary Fiction - Contemporary", "character-driven, introspective"),
            ("Fantasy - Epic/High", "world-building, quest"),
            ("Fantasy - Urban", "magic in modern world"),
            ("Science Fiction - Hard", "technology-focused, realistic"),
            ("Science Fiction - Space Opera", "adventure, galaxy-spanning"),
            ("Mystery - Cozy", "amateur detective, gentle"),
            ("Mystery - Thriller", "suspense, high stakes"),
            ("Romance - Contemporary", "modern love story"),
            ("Romance - Historical", "period love story"),
            ("Horror - Supernatural/Psychological", "fear-based"),
        ]
    },
    "time_period": {
        "question": "What year/time period is the story set?",
        "suggestions": [
            ("Ancient/Pre-Medieval", "BC to 500 AD"),
            ("Medieval", "500-1500 AD"),
            ("Renaissance/Victorian", "1500-1900"),
            ("1920s-1940s", "interwar, WWII era"),
            ("1950s-1970s", "post-war, cultural shifts"),
            ("1980s-1990s", "pre-internet modern"),
            ("Present Day", "2020s, contemporary"),
            ("Near Future", "10-50 years ahead"),
            ("Far Future", "100+ years ahead"),
            ("Timeless/Ambiguous", "no specific era"),
        ]
    },
    "location": {
        "question": "What's the primary location/setting?",
        "suggestions": [
            ("Small Town", "close community, everyone knows everyone"),
            ("Big City", "urban, diverse, anonymous"),
            ("Rural/Countryside", "isolated, nature-focused"),
            ("Coastal/Island", "ocean, islands, seaside"),
            ("Mountain/Wilderness", "harsh terrain, survival"),
            ("Desert/Wasteland", "extreme environment"),
            ("Fantasy Kingdom", "magical realm"),
            ("Space Station/Spaceship", "confined, sci-fi"),
            ("Multiple Worlds", "portal fantasy, travel"),
            ("Virtual/Digital", "inside computer, simulation"),
        ]
    },
    "story_outline": {
        "question": "What's the basic story outline/structure?",
        "suggestions": [
            ("Hero's Journey", "ordinary world → call → trials → transformation"),
            ("Rags to Riches", "poor/weak → rich/powerful through effort"),
            ("Tragedy", "good character falls through fatal flaw"),
            ("Quest", "search for object/person/knowledge"),
            ("Voyage and Return", "go to strange land → return changed"),
            ("Overcoming the Monster", "threat → battle → victory"),
            ("Comedy", "confusion → chaos → happy resolution"),
            ("Mystery", "crime/disappearance → investigation → revelation"),
            ("Rebellion", "oppression → resistance → freedom"),
            ("Coming of Age", "youth → maturity through experience"),
        ]
    },
    "plot_suggestions": {
        "question": "Based on your outline, here are 10 plot variations (choose one or describe your own):",
        "suggestions": [
            ("Standard variation", "Follows the classic structure with unique characters"),
            ("Role reversal", "Swap traditional roles (hero becomes mentor, etc.)"),
            ("Hidden identity", "Key character isn't who they seem"),
            ("False victory", "Success leads to greater problems"),
            ("Unlikely allies", "Enemies must work together"),
            ("Secret society", "Hidden group controls events"),
            ("Time pressure", "Race against the clock"),
            ("Moral dilemma", "No clear right choice"),
            ("Betrayal", "Trusted ally becomes enemy"),
            ("Redemption arc", "Villain seeks forgiveness"),
        ]
    },
    "atmosphere": {
        "question": "What's the atmosphere/tone of the story?",
        "suggestions": [
            ("Dark/Gritty", "serious, heavy themes"),
            ("Hopeful/Uplifting", "inspiring, positive"),
            ("Mysterious/Enigmatic", "secrets, revelations"),
            ("Romantic/Sensual", "love-focused, emotional"),
            ("Adventurous/Exciting", "action, thrills"),
            ("Melancholic/Reflective", "somber, thoughtful"),
            ("Satirical/Humorous", "comedy, wit"),
            ("Epic/Intimate", "grand scope, personal stakes"),
            ("Tense/Suspenseful", "page-turner thriller"),
            ("Whimsical/Magical", "light, fantastical"),
        ]
    },
    "outcome": {
        "question": "How does the story end?",
        "suggestions": [
            ("Happy Ending", "conflict resolved, joy"),
            ("Tragic Ending", "loss, sadness, death"),
            ("Bittersweet", "win with a cost"),
            ("Ambiguous/Open", "reader decides"),
            ("Triumphant", "complete victory"),
            ("Devastating", "complete loss"),
            ("Circular", "ends where it began"),
            ("Twist Ending", "unexpected revelation"),
            ("Redemptive", "character transformation wins"),
            ("Cliffhanger", "setup for sequel"),
        ]
    },
    "audience": {
        "question": "Who's the target audience?",
        "suggestions": [
            ("Middle Grade (MG)", "ages 8-12"),
            ("Young Adult (YA)", "ages 13-18"),
            ("New Adult (NA)", "ages 18-25"),
            ("Adult Literary", "sophisticated prose"),
            ("Adult Commercial", "mainstream appeal"),
            ("Women's Fiction", "female-focused themes"),
            ("Thriller/Mystery Fans", "suspense readers"),
            ("Sci-Fi/Fantasy Fans", "genre enthusiasts"),
            ("Romance Readers", "love story focus"),
            ("Crossover", "appeals to multiple groups"),
        ]
    },
}


def display_question(qkey, qdata, current_selection=None):
    """Display a question with its 10 suggestions."""
    print(f"\n{'='*60}")
    print(f"QUESTION: {qdata['question']}")
    print('='*60)
    
    for i, (suggestion, description) in enumerate(qdata['suggestions'], 1):
        marker = "✓" if current_selection == suggestion else " "
        print(f"{marker} {i:2}. {suggestion}")
        print(f"      └─ {description}")
    
    print("\n" + "-"*60)
    print("Options:")
    print("  • Enter a number (1-10) to select")
    print("  • Type your own custom answer")
    print("  • 'back' to revise previous question")
    print("  • 'summary' to see all your choices so far")
    print("-"*60)


def get_user_choice(qkey, qdata, answers):
    """Get user selection for a question."""
    current = answers.get(qkey)
    
    while True:
        display_question(qkey, qdata, current)
        
        try:
            choice = input("\nYour choice: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nExiting...")
            return None, "quit"
        
        if choice.lower() == 'back':
            return None, 'back'
        elif choice.lower() == 'summary':
            show_summary(answers)
            continue
        elif choice.lower() == 'quit':
            return None, 'quit'
        
        # Try to parse as number
        try:
            num = int(choice)
            if 1 <= num <= 10:
                suggestion, description = qdata['suggestions'][num - 1]
                return suggestion, 'next'
            else:
                print(f"Please enter a number between 1 and 10, or type a custom answer.")
                continue
        except ValueError:
            # Custom answer
            if choice:
                return choice, 'next'
            else:
                print("Please enter a valid choice.")
                continue


def show_summary(answers):
    """Display current answers."""
    print("\n" + "="*60)
    print("YOUR STORY SO FAR")
    print("="*60)
    
    for qkey, qdata in QUESTIONS.items():
        answer = answers.get(qkey, "Not answered")
        print(f"\n{qdata['question']}")
        print(f"  → {answer}")
    
    print("\n" + "="*60)


def run_discovery():
    """Run the full discovery questionnaire."""
    print("\n" + "╔"+"═"*58+"╗")
    print("║" + " "*15 + "STORY DISCOVERY QUESTIONNAIRE" + " "*14 + "║")
    print("╚"+"═"*58+"╝")
    print("\nLet's build your story. I'll ask 10 questions.")
    print("Each question has 10 curated suggestions for you to choose from,")
    print("or you can type your own custom answer.\n")
    
    answers = {}
    question_order = list(QUESTIONS.keys())
    current_idx = 0
    
    while current_idx < len(question_order):
        qkey = question_order[current_idx]
        qdata = QUESTIONS[qkey]
        
        result, action = get_user_choice(qkey, qdata, answers)
        
        if action == 'quit':
            print("\nSaving progress...")
            return answers, False
        elif action == 'back':
            if current_idx > 0:
                current_idx -= 1
            continue
        elif action == 'next':
            answers[qkey] = result
            current_idx += 1
    
    # Show final summary
    show_summary(answers)
    
    print("\nDiscovery complete!")
    return answers, True


def save_discovery(answers, output_path=None):
    """Save discovery results to JSON file."""
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = Path(f"discovery-session-{timestamp}.json")
    
    data = {
        "timestamp": datetime.now().isoformat(),
        "answers": answers
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Story Discovery Questionnaire")
    parser.add_argument("--output", "-o", help="Output file path", default=None)
    parser.add_argument("--load", "-l", help="Load previous session", default=None)
    args = parser.parse_args()
    
    # Load previous session if specified
    if args.load:
        with open(args.load, 'r', encoding='utf-8') as f:
            data = json.load(f)
            answers = data.get('answers', {})
        print(f"Loaded session from {args.load}")
        show_summary(answers)
        return
    
    # Run discovery
    answers, completed = run_discovery()
    
    if answers:
        output_path = save_discovery(answers, args.output)
        print(f"\n✓ Discovery saved to: {output_path}")
        
        if completed:
            print("\nReady for story bible generation!")
            print("Run: python scripts/story-bible-generator.py --discovery " + str(output_path))
    
    return 0 if completed else 1


if __name__ == "__main__":
    sys.exit(main())