---
name: Travel Skill Transfer Planner
slug: travel-skill-transfer-planner
description: Helps plan skill development through travel
category: tourism
type: descriptive
language: en
author: Golden Bean (OpenClaw)
version: v1.1.0
tags: skill-development, learning-travel, educational-travel, experiential-learning, personal-growth
---

# Travel Skill Transfer Planner

## Overview

Helps travelers identify and plan for skill development and transfer during travel

This is a **pure descriptive skill** that provides frameworks, templates, and heuristic analysis for travel planning and preparation. No real code execution, external APIs, or network requests are performed.

## Trigger Keywords

Use this skill when planning travel experiences related to:

- **skill** and **transfer**
- development considerations
- planning planning
- Travel career if applicable
- growth if applicable

### Primary Triggers
- "Help me plan travel skill transfer planner for my upcoming trip"
- "Provide framework for skill in travel context"
- "Create checklist for travel skill transfer planner"
- "Analyze my travel situation using travel skill transfer planner principles"

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

- **Skill gap analysis**
- **Travel-based skill development planning**
- **Transfer strategy framework**
- **Integration into resume/life**

### Detailed Module Descriptions

**Skill gap analysis**
- Provides structured approach to skill gap analysis
- Includes templates and checklists
- Offers best practices and considerations

**Travel-based skill development planning**
- Delivers practical travel-based skill development planning
- Includes implementation guides
- Provides customization options

**Transfer strategy framework**
- Offers transfer strategy framework
- Includes ethical considerations
- Provides risk mitigation strategies

**Integration into resume/life**
- Provides integration into resume/life
- Includes integration guidance
- Offers long-term planning support


## Usage Scenarios

1. **User input:** "I want to learn ceramics in Japan. Plan a 3-week trip that maximizes skill acquisition."
→ **Expected output:** Skill-acquisition itinerary — pre-trip foundation (wheel-throwing basics online), 2-week intensive workshop placement in Seto/Tokoname, post-workshop practice with local potters, studio-access logistics, and portfolio-documentation plan for continued practice at home.
2. **User input:** "Design a 'gap month' where I learn 3 different skills in 3 different European cities."
→ **Expected output:** Multi-skill itinerary — Barcelona (1 week: Spanish + cooking), Florence (1 week: leather craft), Berlin (1 week: electronic music production) — with vetted workshop providers and skill-transfer-home sustainability plan.
3. **User input:** "I want to turn my annual vacation into a recurring skill-building practice. Build the framework."
→ **Expected output:** Annual skill-travel framework — skill-interest audit, destination-skill matching matrix, pre-trip learning phase template, in-trip immersion design, post-trip integration rituals, and year-over-year progression tracking journal.



### Scenario 2: 出国旅游学了新东西回国怎么继续
**User input:** "我在日本学了茶道，回来发现根本没法复现。还有什么旅途中可以学、回国也能继续的技能？"
**Expected output:** 可迁移旅行技能清单——烹饪类：各地菜市场逛一圈学3个本地菜，回国用美团买菜复刻（食材用替代）；手工类：扎染/陶艺/木工等带作品回国，拍制作视频留底；语言类：每天记3句当地实用口语，回来用多邻国+本地语言角巩固；运动类：冲浪/攀岩/潜水留教练联系方式，回国查迪卡侬找同类课程。关键：出发前就想好要学什么，预约课程+准备好收纳空间。

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
- "Help me with travel skill transfer planner for my trip to Japan"
- "Provide skill framework for travel planning"
- "Create travel skill transfer planner checklist for my upcoming vacation"

### Intermediate Usage
- "I'm traveling to skill destination for 2 weeks, help me plan travel skill transfer planner"
- "Analyze my travel situation: destination Paris, duration 10 days, budget $3000"
- "Generate travel skill transfer planner recommendations for family travel with children"

### Advanced Usage
- "I need comprehensive travel skill transfer planner for business travel to multiple countries"
- "Create detailed travel skill transfer planner plan for extended travel with specific transfer requirements"
- "Provide travel skill transfer planner framework with risk assessment and contingency planning"

## Acceptance Criteria

### Functional Requirements
1. ✅ Returns structured JSON output with proper formatting
2. ✅ Includes actionable travel recommendations based on input analysis
3. ✅ Provides relevant travel planning frameworks and templates
4. ✅ Demonstrates input-based differentiation (different inputs → different outputs)
5. ✅ Covers all specified modules: Skill gap analysis, Travel-based skill development planning, Transfer strategy framework, Integration into resume/life

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
