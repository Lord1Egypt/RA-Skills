---
name: Travel Photography Storyteller
slug: travel-photography-storyteller
description: Helps travelers plan meaningful travel photography
category: tourism
type: descriptive
language: en
author: Golden Bean (OpenClaw)
version: v1.1.0
tags: travel-photography, visual-storytelling, photo-planning, creative-travel, content-creation
---

# Travel Photography Storyteller

## Overview

Helps travelers plan and execute meaningful travel photography that tells stories

This is a **pure descriptive skill** that provides frameworks, templates, and heuristic analysis for travel planning and preparation. No real code execution, external APIs, or network requests are performed.

## Trigger Keywords

Use this skill when planning travel experiences related to:

- **photography** and **story**
- travel considerations
- photos planning
- Travel narrative if applicable
- memory if applicable

### Primary Triggers
- "Help me plan travel photography storyteller for my upcoming trip"
- "Provide framework for photography in travel context"
- "Create checklist for travel photography storyteller"
- "Analyze my travel situation using travel photography storyteller principles"

## Workflow

1. **Input Reception**: User provides travel context through natural language input
2. **Input Analysis**: Skill parses input to extract key travel information:
   - Destination and travel context
   - Timeframe and duration
   - Traveler type and experience level
   - Specific concerns or requirements
   - Budget considerations (if mentioned)
   - Group composition and needs
3. **Framework Application**: Skill applies relevant travel planning frameworks and templates
4. **Recommendation Generation**: Skill generates structured, actionable recommendations
5. **Output Delivery**: User receives tailored travel planning insights and next steps

## Output Modules

Based on design specification, this skill covers:

- **Story concept development**
- **Shot planning framework**
- **Ethical photography guidelines**
- **Editing and narrative structure**

### Detailed Module Descriptions

**Story concept development**
- Provides structured approach to story concept development
- Includes templates and checklists
- Offers best practices and considerations

**Shot planning framework**
- Delivers practical shot planning framework
- Includes implementation guides
- Provides customization options

**Ethical photography guidelines**
- Offers ethical photography guidelines
- Includes ethical considerations
- Provides risk mitigation strategies

**Editing and narrative structure**
- Provides editing and narrative structure
- Includes integration guidance
- Offers long-term planning support


## Usage Scenarios

1. **User input:** "I'm going to Morocco for 10 days. Help me plan a photo essay that tells a story, not just snapshots."
→ **Expected output:** Story arc planning — 5-chapter narrative (Arrival, Medina Life, Craft Heritage, Sahara, Departure) with shot list per chapter, golden-hour scheduling, location scouting notes, subject-interaction etiquette, and gear-packing checklist optimized for storytelling.
2. **User input:** "I want to document our family road trip in a way that's creative but not burdensome."
→ **Expected output:** Lightweight documentary framework — one daily theme (faces, details, motion, quiet moments, the unexpected), phone-only shooting guide, in-camera editing principles, and end-of-day 5-minute curation ritual.
3. **User input:** "Create a travel photography shot-planning template for social media content creators."
→ **Expected output:** Content-creator shot planner — platform-specific ratio guide (Instagram 4:5, Reels 9:16, YouTube 16:9), storyboard template for 7-day trip, B-roll checklist, location-scouting app workflow, and batch-caption writing tips.



### Scenario 2: 旅行发朋友圈构图困难户
**User input:** "每次出去玩拍几百张照片，回来发朋友圈发现没有一张能看的，全是游客照。教我怎么拍出小红书那种质感照片？"
**Expected output:** 朋友圈出片三步法——第一步：黄金时刻法（日出后1小时/日落前1小时拍照，手机曝光往下拉半档让色彩更浓郁）；第二步：九宫格法则（手机打开网格线，主体放在交叉点上，避开人群俯拍/仰拍）；第三步：三张起手式（一张全景环境、一张局部特写、一张人物动作，三张一起发马上有故事感）。配文用场景+感受+一个emoji，不要写景点名称。

## Safety & Limitations

### What This Skill Does
- Provides descriptive travel planning frameworks
- Offers heuristic analysis and recommendations
- Delivers structured planning templates
- Suggests considerations and best practices

### What This Skill Does NOT Do
- ❌ **No real bookings**: Does not book flights, hotels, or activities
- ❌ **No real-time data**: Does not access live prices, availability, or weather
- ❌ **No professional advice**: Does not provide medical, legal, or financial advice
- ❌ **No guarantees**: Recommendations are informational only
- ❌ **No code execution**: Pure descriptive analysis only
- ❌ **No external APIs**: No network requests or external service calls
- ❌ **No cultural guarantees**: Provides general guidance but cannot guarantee cultural appropriateness

### Safety Boundaries
- All recommendations are informational only
- Users must verify information with official sources
- Users should consult professionals for specific needs
- Cultural guidance is general and may not apply to all situations

## Example Prompts

### Basic Usage
- "Help me with travel photography storyteller for my trip to Japan"
- "Provide photography framework for travel planning"
- "Create travel photography storyteller checklist for my upcoming vacation"

### Intermediate Usage
- "I'm traveling to photography destination for 2 weeks, help me plan travel photography storyteller"
- "Analyze my travel situation: destination Paris, duration 10 days, budget $3000"
- "Generate travel photography storyteller recommendations for family travel with children"

### Advanced Usage
- "I need comprehensive travel photography storyteller for business travel to multiple countries"
- "Create detailed travel photography storyteller plan for extended travel with specific story requirements"
- "Provide travel photography storyteller framework with risk assessment and contingency planning"

## Acceptance Criteria

### Functional Requirements
1. ✅ Returns structured JSON output with proper formatting
2. ✅ Includes actionable travel recommendations based on input analysis
3. ✅ Provides relevant travel planning frameworks and templates
4. ✅ Demonstrates input-based differentiation (different inputs → different outputs)
5. ✅ Covers all specified modules: Story concept development, Shot planning framework, Ethical photography guidelines, Editing and narrative structure

### Non-Functional Requirements
1. ✅ No code execution, external APIs, or network requests
2. ✅ Pure descriptive analysis only
3. ✅ Clear safety disclaimers present
4. ✅ File count ≤ 10
5. ✅ English documentation primary

### Quality Requirements
1. ✅ Clear, actionable travel recommendations
2. ✅ Input-based differentiation demonstrated
3. ✅ Skill-specific logic implemented
4. ✅ Test coverage for core functionality
5. ✅ Documentation complete and accurate

## Integration

This skill can be combined with:
- Destination research skills
- Budget planning skills
- Packing and preparation skills
- Cultural awareness skills
- Other tourism planning skills

## Version History

- **1.0.0 (2026-04-20)**: Initial release - P1 batch development
  - Added `.claw/identity.json`
  - Completed SKILL.md documentation
  - Fixed review blocking issues

## Technical Details

### Handler Interface
- Standard OpenClaw handler: `handle(user_input: str) -> str`
- Returns valid JSON with proper structure
- Includes `input_analysis` based on user input
- Contains comprehensive `disclaimer`

### Test Coverage
- JSON validation test
- Disclaimer presence test
- Input differentiation test
- Skill-specific logic test

### File Structure
- `SKILL.md` - Complete documentation (this file)
- `handler.py` - Main handler implementation
- `tests/test_handler.py` - Unit tests
- `skill.json` - Skill metadata
- `.claw/identity.json` - Identity information
