# Text Analysis Formulas Reference

## Reading Time Calculation

**Formula:**
```
Reading Time (minutes) = Word Count / 200
```

**Standard:**
- Average adult reading speed: 200 words per minute
- Technical/complex content: 150-180 wpm
- Easy content: 250-300 wpm

## Speaking Time Calculation

**Formula:**
```
Speaking Time (minutes) = Word Count / 130
```

**Standard:**
- Natural speaking pace: 130 words per minute
- Fast presentation: 150-160 wpm
- Slow/careful speech: 100-110 wpm

## Flesch-Kincaid Reading Level

**Formula:**
```
Grade Level = 0.39 × (Words/Sentences) + 11.8 × (Syllables/Words) - 15.59
```

**Interpretation:**
- **0-6**: Easy (elementary level)
- **6-8**: Standard (general audience)
- **8-10**: Moderate (high school level)
- **10-12**: Difficult (college level)
- **12+**: Advanced (graduate/academic)

**Target Guidelines:**
- General web content: Grade 6-8
- Mass market publications: Grade 8-10
- Academic papers: Grade 10-14
- Legal documents: Grade 12+

## Syllable Estimation Algorithm

**Method:**
1. Count vowel groups (a, e, i, o, u, y) in each word
2. Every word has at least 1 syllable
3. Subtract 1 for silent 'e' at word end (if more than 1 syllable)

**Examples:**
- "hello" → he-llo → 2 syllables
- "time" → ti-me → 1 syllable (silent e)
- "beautiful" → beau-ti-ful → 3 syllables

## Keyword Density

**Formula:**
```
Keyword Density (%) = (Keyword Count / Total Words) × 100
```

**SEO Guidelines:**
- Primary keyword: 1-2% density
- Secondary keywords: 0.5-1% density
- Avoid keyword stuffing (>3% looks spammy)

## Common Word Count Requirements

| Content Type | Words | Characters | Purpose |
|--------------|-------|------------|---------|
| Tweet/X post | 40-50 | ≤280 | Social engagement |
| Meta description | 25-30 | ≤155 | SEO snippet |
| Email subject | 6-10 | ≤60 | Open rates |
| Short blog | 300-600 | - | Quick reads |
| Standard blog | 1,000-1,500 | - | SEO articles |
| Long-form | 2,000-3,000 | - | Comprehensive guides |
| Essay | 500-5,000 | - | Academic work |
