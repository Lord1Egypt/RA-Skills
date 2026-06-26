---
name: social-media-content
description: Generate social media posts for LevelUpLove and PayLessTax brands
version: 1.0.0
author: Migration from Agent Zero
---

# Social Media Content Generator Skill

## Overview
Automated social media content generation for branded campaigns using OpenCV/Pillow.

## Input Variables
| Variable | Description | Example |
|----------|-------------|---------|
| HEADLINE | Main headline text | 2026 Tax Deadlines Guide |
| SUBHEADLINE | Supporting subheadline | Don't miss SARS deadlines |
| PANEL_1_TEXT | Carousel panel 1 content | Provisional tax due... |
| CTA_TEXT | Call-to-action button text | Download free guide |
| CTA_URL | URL for CTA | https://paylesstax.co.za |
| PANEL_2_STAT | Statistics for panel 2 | 10% penalty |

## Content Types
- carousel: 4-panel Instagram carousel
- infographic: Single detailed infographic  
- image: Single image with text overlay
- oneliner: Quick punchy post

## Brand Specifications

### LevelUpLove
- Colors: Warm pinks (#FF6B9D), soft purples (#C084FC)
- Vibe: Elegant, romantic, relationship advice

### PayLessTax
- Colors: Corporate blue (#2563EB), emerald green (#10B981)
- Vibe: Professional, trustworthy, tax compliance

## Triggers
- Scheduled content calendar
- Manual CLI execution
- API trigger

## Dependencies
- Pillow (PIL): Image generation
- numpy: Image operations

## Files
- index.py - Main generation logic
- templates/ - JSON templates for each type
