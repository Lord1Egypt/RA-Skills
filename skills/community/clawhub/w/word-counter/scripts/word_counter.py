#!/usr/bin/env python3
"""
Word Counter - Comprehensive text analysis tool

Counts words, characters, sentences, paragraphs, calculates reading/speaking time,
reading level (Flesch-Kincaid), and keyword density.

Usage:
    python word_counter.py "Your text here"
    python word_counter.py --file path/to/file.txt
    python word_counter.py --json "Your text here"
"""

import re
import sys
import argparse
import json
from collections import Counter
from typing import Dict, Any


def count_words(text: str) -> int:
    """Count words in text, handling multiple spaces and special characters."""
    # Remove extra whitespace and split
    words = text.strip().split()
    return len(words)


def count_characters(text: str) -> Dict[str, int]:
    """Count characters with and without spaces."""
    return {
        'with_spaces': len(text),
        'without_spaces': len(text.replace(' ', '').replace('\n', '').replace('\t', ''))
    }


def count_sentences(text: str) -> int:
    """Count sentences based on sentence-ending punctuation."""
    # Split by sentence-ending punctuation
    sentences = re.split(r'[.!?]+', text)
    # Filter out empty strings
    sentences = [s.strip() for s in sentences if s.strip()]
    return len(sentences)


def count_paragraphs(text: str) -> int:
    """Count paragraphs based on line breaks."""
    # Split by double newlines or more
    paragraphs = re.split(r'\n\s*\n', text.strip())
    # Filter out empty paragraphs
    paragraphs = [p.strip() for p in paragraphs if p.strip()]
    return len(paragraphs) if paragraphs else 1


def calculate_reading_time(word_count: int, wpm: int = 200) -> Dict[str, Any]:
    """Calculate reading time based on words per minute."""
    minutes = word_count / wpm
    return {
        'minutes': round(minutes, 2),
        'seconds': round(minutes * 60, 1),
        'display': format_time(minutes)
    }


def calculate_speaking_time(word_count: int, wpm: int = 130) -> Dict[str, Any]:
    """Calculate speaking time based on words per minute."""
    minutes = word_count / wpm
    return {
        'minutes': round(minutes, 2),
        'seconds': round(minutes * 60, 1),
        'display': format_time(minutes)
    }


def format_time(minutes: float) -> str:
    """Format time in human-readable format."""
    if minutes < 1:
        seconds = int(minutes * 60)
        return f"{seconds} sec"
    elif minutes < 60:
        mins = int(minutes)
        secs = int((minutes - mins) * 60)
        if secs > 0:
            return f"{mins} min {secs} sec"
        return f"{mins} min"
    else:
        hours = int(minutes / 60)
        mins = int(minutes % 60)
        if mins > 0:
            return f"{hours} hr {mins} min"
        return f"{hours} hr"


def calculate_flesch_kincaid(text: str, word_count: int, sentence_count: int) -> Dict[str, Any]:
    """
    Calculate Flesch-Kincaid reading level.
    
    Formula: 0.39 * (words/sentences) + 11.8 * (syllables/words) - 15.59
    
    Grade levels:
    - 6-8: General audience
    - 10+: Academic writing
    """
    if sentence_count == 0 or word_count == 0:
        return {'grade_level': 0, 'difficulty': 'Unknown'}
    
    # Estimate syllables (simplified algorithm)
    syllable_count = estimate_syllables(text)
    
    avg_words_per_sentence = word_count / sentence_count
    avg_syllables_per_word = syllable_count / word_count
    
    grade_level = 0.39 * avg_words_per_sentence + 11.8 * avg_syllables_per_word - 15.59
    grade_level = max(0, round(grade_level, 1))
    
    # Determine difficulty
    if grade_level <= 6:
        difficulty = "Easy"
    elif grade_level <= 8:
        difficulty = "Standard"
    elif grade_level <= 12:
        difficulty = "Moderate"
    else:
        difficulty = "Advanced"
    
    return {
        'grade_level': grade_level,
        'difficulty': difficulty,
        'avg_words_per_sentence': round(avg_words_per_sentence, 1),
        'avg_syllables_per_word': round(avg_syllables_per_word, 2)
    }


def estimate_syllables(text: str) -> int:
    """Estimate syllable count using vowel group counting."""
    text = text.lower()
    # Remove non-alphabetic characters
    text = re.sub(r'[^a-z\s]', '', text)
    words = text.split()
    
    total_syllables = 0
    for word in words:
        if not word:
            continue
        # Count vowel groups
        syllables = len(re.findall(r'[aeiouy]+', word))
        # Every word has at least one syllable
        syllables = max(1, syllables)
        # Silent e handling (simplified)
        if word.endswith('e') and syllables > 1:
            syllables -= 1
        total_syllables += syllables
    
    return total_syllables


def calculate_keyword_density(text: str, top_n: int = 10) -> list:
    """Calculate keyword density (frequency of words)."""
    # Convert to lowercase and extract words
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    
    # Common stop words to exclude
    stop_words = {
        'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was',
        'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'its', 'may', 'new',
        'now', 'old', 'see', 'two', 'who', 'boy', 'did', 'she', 'use', 'her', 'way', 'many',
        'oil', 'sit', 'set', 'run', 'eat', 'far', 'sea', 'eye', 'ago', 'off', 'too', 'any',
        'say', 'man', 'try', 'ask', 'end', 'why', 'let', 'put', 'say', 'she', 'try', 'way',
        'own', 'say', 'too', 'old', 'tell', 'very', 'when', 'come', 'here', 'just', 'like',
        'long', 'make', 'over', 'such', 'take', 'than', 'them', 'well', 'were', 'will', 'with',
        'have', 'this', 'that', 'from', 'they', 'know', 'want', 'been', 'good', 'much', 'some',
        'time', 'very', 'when', 'come', 'here', 'just', 'like', 'long', 'make', 'over', 'such',
        'take', 'than', 'them', 'well', 'were', 'what', 'would', 'there', 'their', 'said',
        'each', 'which', 'about', 'could', 'other', 'after', 'first', 'never', 'these', 'think',
        'where', 'being', 'every', 'great', 'might', 'shall', 'still', 'those', 'while', 'your'
    }
    
    # Filter out stop words
    filtered_words = [w for w in words if w not in stop_words]
    
    if not filtered_words:
        return []
    
    # Count word frequencies
    word_counts = Counter(filtered_words)
    total_words = len(filtered_words)
    
    # Calculate density and return top N
    keywords = []
    for word, count in word_counts.most_common(top_n):
        density = (count / total_words) * 100
        keywords.append({
            'word': word,
            'count': count,
            'density': round(density, 2)
        })
    
    return keywords


def analyze_text(text: str) -> Dict[str, Any]:
    """Perform complete text analysis."""
    if not text or not text.strip():
        return {
            'error': 'No text provided'
        }
    
    word_count = count_words(text)
    char_count = count_characters(text)
    sentence_count = count_sentences(text)
    paragraph_count = count_paragraphs(text)
    reading_time = calculate_reading_time(word_count)
    speaking_time = calculate_speaking_time(word_count)
    reading_level = calculate_flesch_kincaid(text, word_count, sentence_count)
    keywords = calculate_keyword_density(text)
    
    return {
        'word_count': word_count,
        'character_count': char_count,
        'sentence_count': sentence_count,
        'paragraph_count': paragraph_count,
        'reading_time': reading_time,
        'speaking_time': speaking_time,
        'reading_level': reading_level,
        'keywords': keywords
    }


def format_output(result: Dict[str, Any], use_json: bool = False) -> str:
    """Format analysis results for display."""
    if use_json:
        return json.dumps(result, indent=2)
    
    if 'error' in result:
        return f"Error: {result['error']}"
    
    lines = [
        "=" * 50,
        "TEXT ANALYSIS RESULTS",
        "=" * 50,
        "",
        f"Word Count:          {result['word_count']}",
        f"Character Count:     {result['character_count']['with_spaces']} (with spaces)",
        f"                     {result['character_count']['without_spaces']} (without spaces)",
        f"Sentences:           {result['sentence_count']}",
        f"Paragraphs:          {result['paragraph_count']}",
        "",
        "Time Estimates:",
        f"   Reading Time:     {result['reading_time']['display']}",
        f"   Speaking Time:    {result['speaking_time']['display']}",
        "",
        "Reading Level (Flesch-Kincaid):",
        f"   Grade Level:      {result['reading_level']['grade_level']}",
        f"   Difficulty:       {result['reading_level']['difficulty']}",
        "",
        "Top Keywords:",
    ]
    
    if result['keywords']:
        for i, kw in enumerate(result['keywords'][:10], 1):
            lines.append(f"   {i}. {kw['word']} ({kw['count']} times, {kw['density']}%)")
    else:
        lines.append("   No significant keywords found")
    
    lines.extend([
        "",
        "=" * 50,
    ])
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Word Counter - Comprehensive text analysis tool'
    )
    parser.add_argument('text', nargs='?', help='Text to analyze')
    parser.add_argument('--file', '-f', help='Read text from file')
    parser.add_argument('--json', '-j', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    # Get text from file or argument
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                text = f.read()
        except FileNotFoundError:
            print(f"Error: File not found: {args.file}")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file: {e}")
            sys.exit(1)
    elif args.text:
        text = args.text
    else:
        # Read from stdin if no arguments
        text = sys.stdin.read()
    
    if not text.strip():
        parser.print_help()
        sys.exit(1)
    
    # Analyze and output
    result = analyze_text(text)
    print(format_output(result, args.json))


if __name__ == "__main__":
    main()
