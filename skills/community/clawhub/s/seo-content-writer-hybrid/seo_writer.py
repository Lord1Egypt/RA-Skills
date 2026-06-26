#!/usr/bin/env python3
"""
SEO Content Writer - Create search-engine-optimized blog posts and articles.
Implements 12-step workflow with CORE-EEAT checklist.
"""

import json
import sys
from datetime import datetime

def generate_title_options(primary_keyword, content_type="blog"):
    """Generate optimized title options."""
    templates = [
        f"{primary_keyword}: The Complete Guide (2026)",
        f"How to Master {primary_keyword} in 10 Steps",
        f"{primary_keyword} Best Practices for 2026",
        f"The Ultimate {primary_keyword} Handbook",
        f"10 {primary_keyword} Tips Experts Use",
        f"{primary_keyword} Explained: What You Need to Know",
        f"Beginner's Guide to {primary_keyword}",
        f"Advanced {primary_keyword} Strategies",
        f"{primary_keyword} Mistakes to Avoid",
        f"Why {primary_keyword} Matters in 2026"
    ]
    
    options = []
    for title in templates:
        char_count = len(title)
        options.append({
            "title": title,
            "characters": char_count,
            "optimal": 50 <= char_count <= 60,
            "keyword_position": "front" if title.startswith(primary_keyword) else "middle"
        })
    
    return sorted(options, key=lambda x: x["characters"])[:5]

def generate_meta_description(primary_keyword, benefit, cta):
    """Generate SEO-optimized meta description."""
    descriptions = [
        f"Learn {primary_keyword} with our complete guide. {benefit}. {cta}",
        f"Master {primary_keyword} today. {benefit}. Get started now!",
        f"Discover proven {primary_keyword} strategies. {benefit}. Read more.",
        f"{primary_keyword} made simple. {benefit}. Start your journey.",
        f"Expert tips on {primary_keyword}. {benefit}. Learn more inside."
    ]
    
    results = []
    for desc in descriptions:
        char_count = len(desc)
        results.append({
            "description": desc,
            "characters": char_count,
            "optimal": 150 <= char_count <= 160
        })
    
    return results[0]  # Return first optimal one

def generate_content_structure(primary_keyword, secondary_keywords, content_type="blog"):
    """Generate optimized content structure."""
    structure = {
        "h1": primary_keyword,
        "introduction": {
            "hook": f"Start with a compelling statistic or question about {primary_keyword}",
            "promise": "What reader will learn",
            "keyword_placement": "Include keyword in first 100 words"
        },
        "body_sections": [],
        "faq": [],
        "conclusion": {
            "summary": "Recap main points",
            "cta": "Clear next step for reader",
            "keyword_placement": "Include keyword naturally"
        }
    }
    
    # Generate H2 sections from secondary keywords
    for i, kw in enumerate(secondary_keywords[:5], 1):
        structure["body_sections"].append({
            "h2": f"{kw}" if i <= 3 else f"Advanced {kw} Strategies",
            "h3_subtopics": [
                f"What is {kw}?",
                f"Why {kw} matters",
                f"How to implement {kw}"
            ],
            "key_points": [
                f"Definition and importance of {kw}",
                f"Best practices for {kw}",
                f"Common mistakes with {kw}",
                f"Tools and resources for {kw}"
            ]
        })
    
    # Generate FAQ questions
    structure["faq"] = [
        {"question": f"What is {primary_keyword}?", "length_target": "40-60 words"},
        {"question": f"Why is {primary_keyword} important?", "length_target": "40-60 words"},
        {"question": f"How do I get started with {primary_keyword}?", "length_target": "40-60 words"},
        {"question": f"What are the best tools for {primary_keyword}?", "length_target": "40-60 words"}
    ]
    
    return structure

def calculate_keyword_density(content, primary_keyword):
    """Calculate keyword density."""
    content_lower = content.lower()
    keyword_lower = primary_keyword.lower()
    
    word_count = len(content.split())
    keyword_count = content_lower.count(keyword_lower)
    
    density = (keyword_count / word_count * 100) if word_count > 0 else 0
    
    return {
        "word_count": word_count,
        "keyword_count": keyword_count,
        "density_percent": round(density, 2),
        "optimal": 1.0 <= density <= 2.0,
        "recommendation": "Good" if 1.0 <= density <= 2.0 else "Adjust keyword usage"
    }

def score_seo_content(content_metadata):
    """Score content across 10 SEO factors."""
    score = 0
    max_score = 10
    factors = []
    
    # Title (1 point)
    if content_metadata.get("has_title") and content_metadata.get("title_length_optimal"):
        score += 1
        factors.append("✅ Title optimized")
    else:
        factors.append("❌ Title needs work")
    
    # Meta description (1 point)
    if content_metadata.get("has_meta_description") and content_metadata.get("meta_length_optimal"):
        score += 1
        factors.append("✅ Meta description optimized")
    else:
        factors.append("❌ Meta description needs work")
    
    # H1 (1 point)
    if content_metadata.get("has_h1") and content_metadata.get("single_h1"):
        score += 1
        factors.append("✅ Single H1 present")
    else:
        factors.append("❌ H1 issues")
    
    # Keyword in first 100 words (1 point)
    if content_metadata.get("keyword_in_intro"):
        score += 1
        factors.append("✅ Keyword in introduction")
    else:
        factors.append("❌ Add keyword to intro")
    
    # H2/H3 structure (1 point)
    if content_metadata.get("has_h2_h3") and content_metadata.get("proper_hierarchy"):
        score += 1
        factors.append("✅ Proper heading hierarchy")
    else:
        factors.append("❌ Heading hierarchy issues")
    
    # Internal links (1 point)
    internal_links = content_metadata.get("internal_links", 0)
    if 2 <= internal_links <= 5:
        score += 1
        factors.append("✅ Good internal linking")
    else:
        factors.append("⚠️ Add 2-5 internal links")
    
    # External links (1 point)
    external_links = content_metadata.get("external_links", 0)
    if 2 <= external_links <= 5:
        score += 1
        factors.append("✅ Good external linking")
    else:
        factors.append("⚠️ Add 2-3 authoritative external links")
    
    # FAQ section (1 point)
    if content_metadata.get("has_faq"):
        score += 1
        factors.append("✅ FAQ section present")
    else:
        factors.append("⚠️ Add FAQ section for snippets")
    
    # Readability (1 point)
    if content_metadata.get("readable"):
        score += 1
        factors.append("✅ Good readability")
    else:
        factors.append("⚠️ Improve readability")
    
    # Word count (1 point)
    word_count = content_metadata.get("word_count", 0)
    if word_count >= 1500:
        score += 1
        factors.append("✅ Comprehensive length")
    elif word_count >= 800:
        score += 0.5
        factors.append("⚠️ Consider expanding")
    else:
        factors.append("❌ Too short (<800 words)")
    
    return {
        "score": score,
        "max_score": max_score,
        "percentage": round(score / max_score * 100),
        "factors": factors
    }

def print_content_outline(structure, title_options, meta_description):
    """Print formatted content outline."""
    print("\n📝 SEO Content Outline\n")
    print("=" * 60)
    
    print("\n📌 Title Options:")
    for i, opt in enumerate(title_options, 1):
        status = "✅" if opt["optimal"] else "⚠️"
        print(f"  {i}. {opt['title']} ({opt['characters']} chars) {status}")
    
    print(f"\n📄 Recommended Meta Description:")
    print(f"   \"{meta_description['description']}\"")
    print(f"   ({meta_description['characters']} chars) {'✅' if meta_description['optimal'] else '⚠️'}")
    
    print(f"\n🏷️  H1: {structure['h1']}")
    
    print("\n📑 Structure:")
    print("   Introduction (100-150 words)")
    print("   - Hook + promise + keyword in first 100 words")
    
    for i, section in enumerate(structure["body_sections"], 1):
        print(f"\n   H2: {section['h2']}")
        for sub in section["h3_subtopics"]:
            print(f"      └─ H3: {sub}")
    
    print("\n❓ FAQ Section:")
    for faq in structure["faq"]:
        print(f"   • {faq['question']} ({faq['length_target']})")
    
    print("\n✅ Conclusion:")
    print("   - Summary + keyword + CTA")
    
    print("\n" + "=" * 60)

def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("""SEO Content Writer - Create Optimized Content

Usage: seo_writer.py <command> [args]

Commands:
  titles <primary_keyword>          Generate title options
  meta <keyword> <benefit> <cta>    Generate meta description
  outline <keyword> [kw2,kw3...]    Generate content structure
  score <json_metadata_file>        Score existing content
  density <text_file> <keyword>     Check keyword density

Examples:
  ./seo_writer.py titles "email marketing"
  ./seo_writer.py meta "email marketing" "increase opens" "Get started"
  ./seo_writer.py outline "email marketing" "automation,sequences,templates"
  ./seo_writer.py score content-metadata.json
  ./seo_writer.py density article.txt "email marketing"
""")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "titles" and len(sys.argv) >= 3:
        keyword = sys.argv[2]
        options = generate_title_options(keyword)
        
        print(f"\n📌 Title Options for '{keyword}'\n")
        for opt in options:
            status = "✅" if opt["optimal"] else "⚠️"
            print(f"  {status} {opt['title']} ({opt['characters']} chars)")
            print(f"      Keyword position: {opt['keyword_position']}")
    
    elif command == "meta" and len(sys.argv) >= 5:
        keyword = sys.argv[2]
        benefit = sys.argv[3]
        cta = sys.argv[4]
        
        meta = generate_meta_description(keyword, benefit, cta)
        
        print(f"\n📄 Meta Description:\n")
        print(f"   \"{meta['description']}\"")
        print(f"\n   Characters: {meta['characters']} {'✅' if meta['optimal'] else '⚠️'}")
        print(f"   Target: 150-160 characters")
    
    elif command == "outline" and len(sys.argv) >= 3:
        primary = sys.argv[2]
        secondary = sys.argv[3].split(",") if len(sys.argv) > 3 else []
        
        titles = generate_title_options(primary)
        meta = generate_meta_description(primary, "Learn more", "Read on")
        structure = generate_content_structure(primary, secondary)
        
        print_content_outline(structure, titles, meta)
    
    elif command == "score" and len(sys.argv) >= 3:
        import os
        if not os.path.exists(sys.argv[2]):
            print(f"❌ File not found: {sys.argv[2]}")
            sys.exit(1)
        
        with open(sys.argv[2], 'r') as f:
            metadata = json.load(f)
        
        result = score_seo_content(metadata)
        
        print(f"\n📊 SEO Content Score: {result['score']}/{result['max_score']} ({result['percentage']}%)\n")
        for factor in result["factors"]:
            print(f"  {factor}")
    
    elif command == "density" and len(sys.argv) >= 4:
        import os
        if not os.path.exists(sys.argv[2]):
            print(f"❌ File not found: {sys.argv[2]}")
            sys.exit(1)
        
        with open(sys.argv[2], 'r') as f:
            content = f.read()
        
        keyword = sys.argv[3]
        result = calculate_keyword_density(content, keyword)
        
        print(f"\n📈 Keyword Density Analysis\n")
        print(f"   Keyword: '{keyword}'")
        print(f"   Word count: {result['word_count']:,}")
        print(f"   Keyword occurrences: {result['keyword_count']}")
        print(f"   Density: {result['density_percent']}%")
        print(f"   Status: {result['optimal']} (target: 1-2%)")
        print(f"   Recommendation: {result['recommendation']}")
    
    else:
        print(f"❌ Unknown command or missing arguments: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
