#!/usr/bin/env python3
"""
Basic SEO Analyzer
Analyzes content for SEO optimization factors.
"""

import sys
import json
import argparse
import re
from typing import Dict, List, Any
from collections import Counter


def count_words(text: str) -> int:
    """Count words in text."""
    return len(text.split())


def count_sentences(text: str) -> int:
    """Count sentences in text."""
    return len(re.split(r'[.!?]+', text))


def calculate_readability(text: str) -> Dict[str, Any]:
    """Calculate basic readability metrics."""
    words = text.split()
    sentences = count_sentences(text)
    
    if not words or not sentences:
        return {"score": 0, "grade": "N/A", "issue": "Insufficient content"}
    
    avg_words_per_sentence = len(words) / sentences
    
    # Simple readability score (Flesch-Kincaid simplified)
    # Lower is easier to read
    if avg_words_per_sentence <= 15:
        readability = "Easy"
        score = 90
    elif avg_words_per_sentence <= 20:
        readability = "Medium"
        score = 70
    elif avg_words_per_sentence <= 25:
        readability = "Difficult"
        score = 50
    else:
        readability = "Very Difficult"
        score = 30
    
    return {
        "score": score,
        "level": readability,
        "avg_words_per_sentence": round(avg_words_per_sentence, 1)
    }


def analyze_headings(content: str) -> Dict[str, Any]:
    """Analyze heading structure."""
    h1_count = len(re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.I))
    h2_count = len(re.findall(r'<h2[^>]*>(.*?)</h2>', content, re.I))
    h3_count = len(re.findall(r'<h3[^>]*>(.*?)</h3>', content, re.I))
    
    issues = []
    score = 100
    
    if h1_count == 0:
        issues.append("Missing H1 heading")
        score -= 30
    elif h1_count > 1:
        issues.append(f"Multiple H1 headings found ({h1_count})")
        score -= 20
    
    if h2_count == 0:
        issues.append("No H2 subheadings found")
        score -= 15
    
    return {
        "h1": h1_count,
        "h2": h2_count,
        "h3": h3_count,
        "score": max(0, score),
        "issues": issues
    }


def analyze_links(content: str) -> Dict[str, Any]:
    """Analyze internal and external links."""
    # Find all links
    internal_links = len(re.findall(r'href=["\']/(?!/)', content))
    external_links = len(re.findall(r'href=["\']https?://', content))
    total_links = internal_links + external_links
    
    issues = []
    score = 100
    
    if total_links == 0:
        issues.append("No links found - add internal and external links")
        score -= 25
    elif internal_links == 0:
        issues.append("No internal links found")
        score -= 15
    
    if external_links > 10:
        issues.append("Too many external links may look spammy")
        score -= 10
    
    return {
        "internal": internal_links,
        "external": external_links,
        "total": total_links,
        "score": max(0, score),
        "issues": issues
    }


def analyze_images(content: str) -> Dict[str, Any]:
    """Analyze images and alt attributes."""
    images = re.findall(r'<img[^>]+>', content, re.I)
    
    images_with_alt = len(re.findall(r'<img[^>]+alt=["\'][^"\']+["\']', content, re.I))
    images_without_alt = len([i for i in images if 'alt=' not in i.lower()])
    
    issues = []
    score = 100
    
    if len(images) == 0:
        issues.append("No images found - consider adding relevant images")
        score -= 10
    elif images_without_alt > 0:
        issues.append(f"{images_without_alt} images missing alt text")
        score -= 20 * images_without_alt
    
    return {
        "total": len(images),
        "with_alt": images_with_alt,
        "without_alt": images_without_alt,
        "score": max(0, score),
        "issues": issues
    }


def analyze_keywords(content: str, target_keyword: str = "") -> Dict[str, Any]:
    """Analyze keyword usage."""
    content_lower = content.lower()
    words = re.findall(r'\b\w+\b', content_lower)
    word_count = len(words)
    
    # Remove common stop words
    stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 
                  'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                  'would', 'could', 'should', 'may', 'might', 'must', 'shall',
                  'and', 'but', 'or', 'if', 'then', 'else', 'when', 'at', 'by',
                  'for', 'with', 'about', 'against', 'between', 'into', 'through',
                  'of', 'to', 'in', 'on', 'that', 'this', 'it', 'as', 'from'}
    
    content_words = [w for w in words if w not in stop_words and len(w) > 2]
    word_freq = Counter(content_words)
    
    result = {
        "total_words": word_count,
        "unique_words": len(set(content_words)),
        "top_keywords": word_freq.most_common(5)
    }
    
    if target_keyword:
        keyword_lower = target_keyword.lower()
        keyword_count = content_lower.count(keyword_lower)
        keyword_density = (keyword_count / word_count * 100) if word_count > 0 else 0
        
        issues = []
        score = 100
        
        if keyword_density < 0.5:
            issues.append(f"Keyword density too low ({keyword_density:.1f}%)")
            score -= 20
        elif keyword_density > 3:
            issues.append(f"Keyword stuffing detected ({keyword_density:.1f}%)")
            score -= 30
        
        # Check keyword in important positions
        has_in_title = keyword_lower in content_lower[:200]
        has_in_heading = bool(re.search(r'<h[1-6][^>]*>.*?' + keyword_lower, content_lower, re.I))
        
        if not has_in_title:
            issues.append("Keyword not found in title area")
            score -= 15
        if not has_in_heading:
            issues.append("Keyword not found in headings")
            score -= 10
        
        result.update({
            "target_keyword": target_keyword,
            "count": keyword_count,
            "density": round(keyword_density, 2),
            "in_title": has_in_title,
            "in_heading": has_in_heading,
            "score": max(0, score),
            "issues": issues
        })
    
    return result


def calculate_overall_score(analyses: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate overall SEO score."""
    weights = {
        "readability": 0.15,
        "headings": 0.20,
        "links": 0.15,
        "images": 0.10,
        "keywords": 0.25,
        "content_length": 0.15
    }
    
    total_score = 0
    
    # Content length score
    word_count = analyses.get("keywords", {}).get("total_words", 0)
    if word_count >= 1500:
        length_score = 100
    elif word_count >= 1000:
        length_score = 80
    elif word_count >= 500:
        length_score = 60
    elif word_count >= 300:
        length_score = 40
    else:
        length_score = 20
    
    analyses["content_length"] = {"score": length_score, "words": word_count}
    
    # Calculate weighted score
    score_components = {
        "readability": analyses.get("readability", {}).get("score", 0),
        "headings": analyses.get("headings", {}).get("score", 0),
        "links": analyses.get("links", {}).get("score", 0),
        "images": analyses.get("images", {}).get("score", 0),
        "keywords": analyses.get("keywords", {}).get("score", 0),
        "content_length": length_score
    }
    
    for component, weight in weights.items():
        total_score += score_components[component] * weight
    
    # Determine grade
    if total_score >= 90:
        grade = "A"
    elif total_score >= 80:
        grade = "B"
    elif total_score >= 70:
        grade = "C"
    elif total_score >= 60:
        grade = "D"
    else:
        grade = "F"
    
    return {
        "score": round(total_score),
        "grade": grade,
        "components": score_components
    }


def analyze_content(content: str, target_keyword: str = "") -> Dict[str, Any]:
    """Perform full SEO analysis on content."""
    # Clean HTML for text analysis
    text_only = re.sub(r'<[^>]+>', ' ', content)
    text_only = re.sub(r'\s+', ' ', text_only).strip()
    
    analyses = {
        "readability": calculate_readability(text_only),
        "headings": analyze_headings(content),
        "links": analyze_links(content),
        "images": analyze_images(content),
        "keywords": analyze_keywords(content, target_keyword)
    }
    
    # Calculate overall score
    overall = calculate_overall_score(analyses)
    
    return {
        "overall": overall,
        "analyses": analyses
    }


def generate_recommendations(analyses: Dict[str, Any]) -> List[str]:
    """Generate actionable recommendations."""
    recommendations = []
    
    # Readability
    readability = analyses.get("readability", {})
    if readability.get("score", 0) < 60:
        recommendations.append("Simplify your writing - aim for shorter sentences")
    
    # Headings
    headings = analyses.get("headings", {})
    if headings.get("issues"):
        for issue in headings["issues"]:
            recommendations.append(f"Headings: {issue}")
    
    # Links
    links = analyses.get("links", {})
    if links.get("total", 0) == 0:
        recommendations.append("Add relevant internal and external links")
    
    # Images
    images = analyses.get("images", {})
    if images.get("without_alt", 0) > 0:
        recommendations.append(f"Add alt text to {images['without_alt']} images")
    
    # Keywords
    keywords = analyses.get("keywords", {})
    if keywords.get("issues"):
        for issue in keywords["issues"]:
            recommendations.append(f"Keywords: {issue}")
    
    # Content length
    words = keywords.get("total_words", 0)
    if words < 300:
        recommendations.append(f"Content too short ({words} words). Aim for 500+ words")
    elif words < 1000:
        recommendations.append("Consider expanding content to 1000+ words for better SEO")
    
    return recommendations


def main():
    parser = argparse.ArgumentParser(description="Basic SEO Analyzer")
    parser.add_argument("content", help="Content or URL to analyze")
    parser.add_argument("--keyword", "-k", help="Target keyword to optimize for")
    parser.add_argument("--format", choices=["json", "text"], default="text")
    
    args = parser.parse_args()
    
    content = args.content.strip()
    
    # Check if it's a URL (basic check)
    if content.startswith(('http://', 'https://')):
        content = f"Note: URL provided - {content}. Provide actual content for analysis."
    
    target_keyword = args.keyword or ""
    
    result = analyze_content(content, target_keyword)
    recommendations = generate_recommendations(result["analyses"])
    result["recommendations"] = recommendations
    
    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        overall = result["overall"]
        
        print("\n" + "=" * 50)
        print("🔍 SEO ANALYSIS RESULTS")
        print("=" * 50)
        
        print(f"\n📊 Overall Score: {overall['score']}/100 (Grade: {overall['grade']})")
        
        print("\n📈 Score Breakdown:")
        for component, score in overall["components"].items():
            bar = "█" * (score // 10) + "░" * (10 - score // 10)
            print(f"   {component:15} {bar} {score}")
        
        print(f"\n📝 Content Stats:")
        kw = result["analyses"]["keywords"]
        print(f"   Words: {kw.get('total_words', 0)}")
        print(f"   Unique: {kw.get('unique_words', 0)}")
        if kw.get("target_keyword"):
            print(f"   Keyword: {kw['target_keyword']} ({kw.get('density', 0)}% density)")
        
        if recommendations:
            print("\n💡 Recommendations:")
            for i, rec in enumerate(recommendations, 1):
                print(f"   {i}. {rec}")
        
        print()


if __name__ == "__main__":
    main()
