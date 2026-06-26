# TrackUp Food Analyze

Analyze food images and search nutrition data using AISpark TrackUp APIs.

## Features

- Full food analysis with `AnalyzeWholeFood`
- Specialized macro extraction with `ExtractFoodMacros`
- Specialized ingredient and metabolic analysis with `AnalyzeIngredients`
- Professional health insights with `GetHealthInsight`
- Keyword-based food search

## Prerequisites

- Ensure network access to `https://deepeat.ai`

## Usage

### Full Food Analysis

Provide an image URL or base64 data. For complete food analysis, call:

1. `AnalyzeWholeFood`

Use this as the default image-analysis API. It returns a combined result including macros, ingredients, GI, fiber, sugar, health score, and health profile.

### Specialized Image Analysis

If the user only wants one specific aspect, call the matching API directly:

1. Basic macro extraction: `ExtractFoodMacros`
2. Deep ingredient and metabolic analysis: `AnalyzeIngredients`
3. Professional health insight: `GetHealthInsight`

### Food Search

Use keyword search to lookup foods without an image:

```
SearchFood: "banana"
```

Returns up to 20 results with macros and GI.

## Output Rules

- Numeric values are kept exactly as returned by the API
- Missing fields are not invented
- For complete image analysis, use `AnalyzeWholeFood` directly
- Only use the specialized APIs when the user explicitly wants a specific analysis dimension
- Health score (1-5) helps users make nutritionally informed choices
