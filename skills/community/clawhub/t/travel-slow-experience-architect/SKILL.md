---
name: Slow Travel Experience Architect
slug: travel-slow-experience-architect
description: Designs meaningful slow travel experiences
category: tourism
type: descriptive
language: en
author: Golden Bean (OpenClaw)
version: "1.1.0"

tags: slow-travel, experience-design, meaningful-travel, immersive-travel, itinerary-planning
---

# Slow Travel Experience Architect

## Overview

Designs meaningful slow travel experiences focused on depth over checklist tourism

This is a **pure descriptive skill** that provides frameworks, templates, and heuristic analysis for travel planning and preparation. No real code execution, external APIs, or network requests are performed.

## Trigger Keywords

Use this skill when planning travel experiences related to:

- **slow travel** and **experience**
- depth considerations
- immersion planning
- Travel meaningful if applicable
- pace if applicable

### Primary Triggers
- "Help me plan slow travel experience architect for my upcoming trip"
- "Provide framework for slow travel in travel context"
- "Create checklist for slow travel experience architect"
- "Analyze my travel situation using slow travel experience architect principles"

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

- **Pace and rhythm design**
- **Local integration strategies**
- **Meaningful connection frameworks**
- **Personal growth integration**

### Detailed Module Descriptions

**Pace and rhythm design**
- Provides structured approach to pace and rhythm design
- Includes templates and checklists
- Offers best practices and considerations

**Local integration strategies**
- Delivers practical local integration strategies
- Includes implementation guides
- Provides customization options

**Meaningful connection frameworks**
- Offers meaningful connection frameworks
- Includes ethical considerations
- Provides risk mitigation strategies

**Personal growth integration**
- Provides personal growth integration
- Includes integration guidance
- Offers long-term planning support

## Usage Scenarios

### Scenario 1

**User input:** "Design a 30-day slow travel experience through Portugal by train. Not just sightseeing — I want to feel like I lived there."

**Expected output:** Pod-based itinerary — 3 towns, 10 days each — with neighborhood-living setup (local market shopping, café-as-office, language-exchange meetups), deep-dive themes (azulejo art, port wine, fado music), and 'resident-for-a-week' immersion activities.

### Scenario 2

**User input:** "I have 2 weeks but want a slow travel experience in Japan. What's realistic?"

**Expected output:** Single-region focus recommendation (Kansai: Kyoto + Nara + rural Uji) with 4-5 day stays per location, morning rituals (temple meditation, tea ceremony), afternoon explorations (craft workshops, countryside walks), and no-transfer-day buffer built into schedule.

### Scenario 3

**User input:** "Convert my usual checklist-style itinerary into a slow-travel version for Tuscany."

**Expected output:** Before/after transformation — from '7 towns in 5 days' to '2 towns in 7 days' with fewer destinations, deeper experiences (olive harvest participation, nonna cooking mentorship, village festival attendance), and spaciousness principles applied throughout.
### Scenario 4: 慢游大理
**User input:** "不想走马观花去旅游，想去大理待一个月，过一下'有风的地方'那种慢生活，怎么安排好？"
**Expected output:** 设计大理慢生活月计划：第一周——住古城民宿，每天睡到自然醒，逛古城菜市场买菜做饭，傍晚去人民路听民谣；第二周——移居到喜洲古镇，学扎染、逛稻田、喝咖啡发呆；第三周——搬到洱海东岸的双廊，骑车环海、每天换个角度看苍山；第四周——回大理或去沙溪古镇，整理这一个月的感悟。预算建议：民宿月租约2000-4000元（比日租省60%），餐饮月均1500-2000元。推荐关注大理的'集市日历'（如柴米多集市、床单厂集市）。

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
- "Help me with slow travel experience architect for my trip to Japan"
- "Provide slow travel framework for travel planning"
- "Create slow travel experience architect checklist for my upcoming vacation"

### Intermediate Usage
- "I'm traveling to slow travel destination for 2 weeks, help me plan slow travel experience architect"
- "Analyze my travel situation: destination Paris, duration 10 days, budget $3000"
- "Generate slow travel experience architect recommendations for family travel with children"

### Advanced Usage
- "I need comprehensive slow travel experience architect for business travel to multiple countries"
- "Create detailed slow travel experience architect plan for extended travel with specific experience requirements"
- "Provide slow travel experience architect framework with risk assessment and contingency planning"

## Acceptance Criteria

### Functional Requirements
1. ✅ Returns structured JSON output with proper formatting
2. ✅ Includes actionable travel recommendations based on input analysis
3. ✅ Provides relevant travel planning frameworks and templates
4. ✅ Demonstrates input-based differentiation (different inputs → different outputs)
5. ✅ Covers all specified modules: Pace and rhythm design, Local integration strategies, Meaningful connection frameworks, Personal growth integration

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
