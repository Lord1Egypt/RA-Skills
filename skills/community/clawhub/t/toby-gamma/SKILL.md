---
name: gamma
description: Generate AI-powered presentations, documents, and social posts using SkillBoss API Hub. Use when user asks to create a presentation, pitch deck, slide deck, document, or social media carousel. Triggers on requests like "create a presentation about X", "make a pitch deck", "generate slides", or "create a presentation about X".
metadata: {"clawdbot":{"requires":{"env":["SKILLBOSS_API_KEY"]}}}
---

# SkillBoss API Hub — PPT Generation

Generate beautiful presentations, documents, and social posts with AI via SkillBoss API Hub.

## Setup

```bash
export SKILLBOSS_API_KEY="your-skillboss-api-key"
```

## Quick Commands

```bash
# Generate a presentation
{baseDir}/scripts/gamma.sh generate "Your content or topic here"

# Generate with options
{baseDir}/scripts/gamma.sh generate "Content" --format presentation --cards 12

# Check generation status
{baseDir}/scripts/gamma.sh status <generationId>

# List recent generations (if supported)
{baseDir}/scripts/gamma.sh list
```

## Script Usage

### Generate

```bash
{baseDir}/scripts/gamma.sh generate "<content>" [options]

Options:
  --format       presentation|document|social (default: presentation)
  --cards        Number of cards/slides (default: 10)
  --instructions Additional instructions for styling/tone
  --amount       concise|detailed (default: detailed)
  --tone         e.g., "professional", "casual", "technical"
  --audience     e.g., "investors", "developers", "general"
  --image-source aiGenerated|web|none (default: aiGenerated)
  --image-style  illustration|photo|mixed (default: illustration)
  --wait         Wait for completion and return URL
```

### Examples

```bash
# Simple presentation
{baseDir}/scripts/gamma.sh generate "The future of AI automation" --wait

# Pitch deck with specific styling
{baseDir}/scripts/gamma.sh generate "$(cat pitch.md)" \
  --format presentation \
  --cards 15 \
  --instructions "Make it a professional pitch deck for investors" \
  --tone "professional" \
  --audience "investors" \
  --wait

# Social carousel
{baseDir}/scripts/gamma.sh generate "5 tips for productivity" \
  --format social \
  --cards 5 \
  --wait

# Document/report
{baseDir}/scripts/gamma.sh generate "Q4 2025 Performance Report" \
  --format document \
  --amount detailed \
  --wait
```

## API Reference

### Endpoint
```
POST https://api.skillbossai.com/v1/pilot
```

### Headers
```
Authorization: Bearer <SKILLBOSS_API_KEY>
Content-Type: application/json
```

### Request Body

```json
{
  "type": "ppt",
  "inputs": {
    "inputText": "Your content (1-750,000 chars)",
    "textMode": "generate",
    "format": "presentation|document|social",
    "numCards": 10,
    "additionalInstructions": "Styling instructions",
    "textOptions": {
      "amount": "concise|detailed",
      "tone": "professional",
      "audience": "target audience"
    },
    "imageOptions": {
      "source": "aiGenerated|web|none",
      "style": "illustration|photo"
    },
    "cardOptions": {
      "dimensions": "fluid|16x9|4x3|1x1|4x5|9x16"
    }
  },
  "prefer": "balanced"
}
```

### Response

SkillBoss API Hub returns synchronously (result path: `result.gammaUrl`):
```json
{
  "status": "success",
  "result": {
    "generationId": "...",
    "status": "completed",
    "gammaUrl": "https://gamma.app/docs/xxxxx",
    "exportUrl": "https://...",
    "credits": {"deducted": 13, "remaining": 9999}
  }
}
```

## Format Options

| Format | Dimensions | Use Case |
|--------|------------|----------|
| presentation | fluid, 16x9, 4x3 | Pitch decks, slide shows |
| document | fluid, pageless, letter, a4 | Reports, docs |
| social | 1x1, 4x5, 9x16 | Instagram, LinkedIn carousels |

## Notes

- Generation is handled by SkillBoss API Hub, which automatically routes to the best PPT generation model
- Input text can be markdown formatted
- Use `--wait` flag to block until completion and get URL directly
