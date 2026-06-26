#!/usr/bin/env python3
"""
Turnitin AI Checker - Core detection algorithms
Analyzes text for AI-generated patterns similar to Turnitin's detection methods.
"""

import re
import math
import json
import sys
from typing import Dict, List, Tuple
from collections import Counter

# Common AI writing patterns
AI_PHRASES = [
    "it is important to note",
    "it should be noted",
    "it is worth mentioning",
    "it is essential to understand",
    "it is crucial to recognize",
    "in conclusion",
    "to summarize",
    "to conclude",
    "in summary",
    "furthermore",
    "moreover",
    "in addition",
    "additionally",
    "consequently",
    "therefore",
    "thus",
    "as a result",
    "hence",
    "for example",
    "for instance",
    "in other words",
    "to put it simply",
    "in today's world",
    "in recent years",
    "with the development of",
    "with the advancement of",
    "due to the fact that",
    "in order to",
    "in terms of",
    "with regard to",
    "regarding",
    "concerning",
    "not only",
    "but also",
    "on the other hand",
    "however",
    "nevertheless",
    "nonetheless",
    "although",
    "even though",
    "despite the fact that",
]

# Formal words often overused by AI
FORMAL_WORDS = [
    "utilize", "utilizes", "utilized", "utilizing",
    "demonstrate", "demonstrates", "demonstrated", "demonstrating",
    "indicate", "indicates", "indicated", "indicating",
    "significant", "significantly",
    "substantial", "substantially",
    "effective", "effectively",
    "appropriate", "appropriately",
    "relevant", "relevance",
    "numerous",
    "various",
    "several",
    "multiple",
]


def count_syllables(word: str) -> int:
    """Estimate syllable count for a word."""
    word = word.lower()
    vowels = "aeiouy"
    syllable_count = 0
    prev_was_vowel = False
    
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_was_vowel:
            syllable_count += 1
        prev_was_vowel = is_vowel
    
    if word.endswith("e"):
        syllable_count -= 1
    if word.endswith("le") and len(word) > 2 and word[-3] not in vowels:
        syllable_count += 1
    if syllable_count == 0:
        syllable_count = 1
    
    return syllable_count


def split_sentences(text: str) -> List[str]:
    """Split text into sentences."""
    # Simple sentence splitting
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def calculate_burstiness(sentences: List[str]) -> float:
    """
    Calculate burstiness score based on sentence length variation.
    Returns score 0-1, where higher = more human-like (more variation).
    """
    if len(sentences) < 2:
        return 0.5
    
    lengths = [len(s.split()) for s in sentences]
    mean_len = sum(lengths) / len(lengths)
    
    if mean_len == 0:
        return 0.5
    
    # Calculate standard deviation
    variance = sum((l - mean_len) ** 2 for l in lengths) / len(lengths)
    std_dev = math.sqrt(variance)
    
    # Coefficient of variation
    cv = std_dev / mean_len
    
    # Normalize to 0-1 range (typical CV for text is 0.2-0.8)
    burstiness = min(max(cv / 0.6, 0), 1)
    
    return burstiness


def detect_ai_patterns(text: str) -> Dict:
    """Detect common AI writing patterns."""
    text_lower = text.lower()
    words = text_lower.split()
    word_count = len(words)
    
    # Count AI phrases
    ai_phrase_count = 0
    found_phrases = []
    for phrase in AI_PHRASES:
        count = text_lower.count(phrase)
        if count > 0:
            ai_phrase_count += count
            found_phrases.append((phrase, count))
    
    # Count formal words
    formal_word_count = sum(1 for word in words if word in FORMAL_WORDS)
    
    # Calculate scores per 100 words
    ai_phrase_density = (ai_phrase_count / word_count * 100) if word_count > 0 else 0
    formal_word_density = (formal_word_count / word_count * 100) if word_count > 0 else 0
    
    # Pattern score (0-100)
    pattern_score = min((ai_phrase_density * 5) + (formal_word_density * 2), 100)
    
    return {
        "ai_phrase_count": ai_phrase_count,
        "ai_phrase_density": round(ai_phrase_density, 2),
        "formal_word_count": formal_word_count,
        "formal_word_density": round(formal_word_density, 2),
        "found_phrases": found_phrases[:10],  # Top 10
        "pattern_score": round(pattern_score, 2)
    }


def calculate_readability(text: str) -> Dict:
    """Calculate readability metrics."""
    sentences = split_sentences(text)
    words = text.split()
    
    if len(sentences) == 0 or len(words) == 0:
        return {"flesch_ease": 0, "flesch_kincaid": 0, "avg_sentence_length": 0}
    
    syllable_count = sum(count_syllables(w) for w in words)
    word_count = len(words)
    sentence_count = len(sentences)
    
    avg_sentence_length = word_count / sentence_count
    avg_syllables_per_word = syllable_count / word_count
    
    # Flesch Reading Ease
    flesch_ease = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
    
    # Flesch-Kincaid Grade Level
    flesch_kincaid = (0.39 * avg_sentence_length) + (11.8 * avg_syllables_per_word) - 15.59
    
    return {
        "flesch_ease": round(flesch_ease, 2),
        "flesch_kincaid": round(flesch_kincaid, 2),
        "avg_sentence_length": round(avg_sentence_length, 2),
        "avg_syllables_per_word": round(avg_syllables_per_word, 2),
        "word_count": word_count,
        "sentence_count": sentence_count
    }


def calculate_perplexity_proxy(text: str) -> float:
    """
    Calculate a perplexity proxy score.
    Since we don't have access to a full language model, we use heuristics.
    """
    words = text.lower().split()
    if len(words) < 10:
        return 50
    
    # Calculate word repetition patterns
    word_counts = Counter(words)
    total_words = len(words)
    unique_words = len(word_counts)
    
    # Type-token ratio (vocabulary diversity)
    ttr = unique_words / total_words if total_words > 0 else 0
    
    # Common word ratio (function words are predictable)
    common_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "is", "are", "was", "were", "be", "been", "have", "has", "had", "do", "does", "did", "will", "would", "could", "should", "may", "might", "can", "this", "that", "these", "those", "it", "they", "them", "their", "there", "then", "than", "as", "if", "so", "such", "when", "where", "why", "how", "all", "any", "both", "each", "more", "most", "other", "some", "very", "what", "which", "who", "whom", "whose", "from", "up", "about", "into", "through", "during", "before", "after", "above", "below", "between", "among", "within", "without", "against", "under", "over", "again", "further", "once", "here", "now", "also", "only", "own", "same", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "just", "but", "if", "or", "because", "until", "while", "although", "though", "unless", "whether", "since", "although", "even", "provided", "whereas"}
    common_count = sum(1 for w in words if w in common_words)
    common_ratio = common_count / total_words if total_words > 0 else 0
    
    # Repetitive phrase detection
    bigrams = [f"{words[i]} {words[i+1]}" for i in range(len(words)-1)]
    bigram_counts = Counter(bigrams)
    max_bigram_freq = max(bigram_counts.values()) if bigram_counts else 0
    repetition_score = min(max_bigram_freq / (total_words / 20), 1) if total_words > 20 else 0
    
    # Combine factors (lower = more AI-like)
    # AI tends to have: lower TTR, moderate common word ratio, some repetition
    perplexity_proxy = 100 - (ttr * 30) - (common_ratio * 20) + (repetition_score * 20)
    
    return min(max(perplexity_proxy, 0), 100)


def analyze_text(text: str) -> Dict:
    """
    Main analysis function that combines all detection methods.
    Returns comprehensive AI detection report.
    """
    if not text or len(text.strip()) < 50:
        return {
            "error": "Text too short for analysis (minimum 50 characters)",
            "ai_score": 0,
            "risk_level": "Unknown"
        }
    
    sentences = split_sentences(text)
    
    # Calculate individual components
    burstiness = calculate_burstiness(sentences)
    pattern_data = detect_ai_patterns(text)
    readability = calculate_readability(text)
    perplexity_proxy = calculate_perplexity_proxy(text)
    
    # Weighted AI score calculation
    # Burstiness: lower = more AI (invert)
    burstiness_score = (1 - burstiness) * 100
    
    # Perplexity proxy: lower = more AI
    perplexity_score = 100 - perplexity_proxy
    
    # Pattern score: higher = more AI
    pattern_score = pattern_data["pattern_score"]
    
    # Readability variance: AI tends to be consistent
    # Use Flesch-Kincaid as a consistency indicator
    fk_score = min(max((readability["flesch_kincaid"] - 8) * 5, 0), 100)
    
    # Weighted combination
    ai_score = (
        perplexity_score * 0.30 +      # 30% - predictability
        burstiness_score * 0.25 +       # 25% - variation
        pattern_score * 0.30 +          # 30% - AI patterns
        fk_score * 0.15                 # 15% - grade level consistency
    )
    
    ai_score = min(max(ai_score, 0), 100)
    
    # Determine risk level
    if ai_score < 20:
        risk_level = "Safe"
        risk_description = "No action needed. Your text is unlikely to be flagged."
    elif ai_score < 40:
        risk_level = "Warning"
        risk_description = "Consider reviewing. Some sections may trigger flags."
    elif ai_score < 60:
        risk_level = "Moderate Risk"
        risk_description = "Humanization recommended to reduce detection risk."
    else:
        risk_level = "High Risk"
        risk_description = "Strong humanization recommended before submission."
    
    return {
        "ai_score": round(ai_score, 1),
        "risk_level": risk_level,
        "risk_description": risk_description,
        "components": {
            "perplexity_proxy": round(perplexity_proxy, 1),
            "burstiness": round(burstiness * 100, 1),
            "pattern_score": round(pattern_score, 1),
            "readability_grade": round(readability["flesch_kincaid"], 1)
        },
        "pattern_analysis": pattern_data,
        "readability": readability,
        "threshold_note": "Turnitin flags submissions at 20% AI or above"
    }


def analyze_by_paragraphs(text: str) -> List[Dict]:
    """Analyze text paragraph by paragraph."""
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    results = []
    
    for i, paragraph in enumerate(paragraphs, 1):
        if len(paragraph) >= 100:
            analysis = analyze_text(paragraph)
            results.append({
                "paragraph": i,
                "preview": paragraph[:100] + "..." if len(paragraph) > 100 else paragraph,
                "ai_score": analysis.get("ai_score", 0),
                "risk_level": analysis.get("risk_level", "Unknown")
            })
    
    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ai_checker.py '<text>'")
        print("   or: python ai_checker.py --file <path>")
        sys.exit(1)
    
    if sys.argv[1] == "--file":
        with open(sys.argv[2], 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = sys.argv[1]
    
    result = analyze_text(text)
    print(json.dumps(result, indent=2, ensure_ascii=False))
