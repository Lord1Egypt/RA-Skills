---
name: Multi-Generational Travel Harmonizer
slug: travel-multigenerational-harmonizer
description: Creates travel experiences for multiple generations
category: tourism
type: descriptive
language: en
author: Golden Bean (OpenClaw)
version: "1.1.0"

tags: family-travel, multigenerational, trip-planning, travel-design, group-coordination
---

# Multi-Generational Travel Harmonizer

## Overview

Creates travel experiences that work for multiple generations traveling together

This is a **pure descriptive skill** that provides frameworks, templates, and heuristic analysis for travel planning and preparation. No real code execution, external APIs, or network requests are performed.

## Trigger Keywords

Use this skill when planning travel experiences related to:

- **multi-generational** and **family**
- generations considerations
- harmony planning
- Travel activities if applicable
- needs if applicable

### Primary Triggers
- "Help me plan multi-generational travel harmonizer for my upcoming trip"
- "Provide framework for multi-generational in travel context"
- "Create checklist for multi-generational travel harmonizer"
- "Analyze my travel situation using multi-generational travel harmonizer principles"

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

- **Need assessment framework**
- **Activity layering system**
- **Pace management strategies**
- **Conflict prevention mechanisms**

### Detailed Module Descriptions

**Need assessment framework**
- Provides structured approach to need assessment framework
- Includes templates and checklists
- Offers best practices and considerations

**Activity layering system**
- Delivers practical activity layering system
- Includes implementation guides
- Provides customization options

**Pace management strategies**
- Offers pace management strategies
- Includes ethical considerations
- Provides risk mitigation strategies

**Conflict prevention mechanisms**
- Provides conflict prevention mechanisms
- Includes integration guidance
- Offers long-term planning support

## Usage Scenarios

### Scenario 1

**User input:** "Plan a 7-day trip for my family: grandparents (70s), us (40s), and kids (8 & 12). Budget $12K."

**Expected output:** Day-by-day itinerary with activity tiers — morning (gentle pace for grandparents), afternoon (active for middle generation with kids), evening (all-together) — with mobility-friendly accommodations, rest-day scheduling, dining that satisfies all palates, and contingency plans.

### Scenario 2

**User input:** "Grandparents want to relax, teenagers want adventure, we want culture. How do we not kill each other in Italy for 10 days?"

**Expected output:** Split-and-meet schedule model — morning independent blocks (grandparents: piazza + café, teens: bike tour, parents: museum), afternoon family activities (cooking class, villa pool), evening dinners together — with communication norms and 'opt-out without guilt' policy.

### Scenario 3

**User input:** "Create a multigenerational trip planning template our family can reuse annually."

**Expected output:** Reusable planning workbook — interest survey for each generation, budget calculator, accommodation filter (step-free, connecting rooms, kitchen), activity-vetting checklist, packing list by generation, and pre-trip family meeting agenda.
### Scenario 4: 带爸妈和小孩一起去三亚
**User input:** "想暑假带爸妈（60多岁）和小孩（6岁）一起去三亚玩一周，怎么安排才能大家都满意？"
**Expected output:** 设计三代同堂三亚行程策略：1）住宿——推荐三亚湾/亚龙湾的公寓式酒店（可做饭，老人吃得惯），订两室一厅套房比分两间房便宜；2）活动分配——上午安排全家适合的项目（沙滩玩沙、亚龙湾热带天堂森林公园），下午老人可以回酒店午休，年轻夫妻带孩子去亚特兰蒂斯水世界；3）交通——租车（携程租车约200/天）比打车方便；4）餐饮——找有清淡选项的海鲜餐厅，也可以自己做粥和面条。注意给老人备好防暑药和防晒用品。

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
- "Help me with multi-generational travel harmonizer for my trip to Japan"
- "Provide multi-generational framework for travel planning"
- "Create multi-generational travel harmonizer checklist for my upcoming vacation"

### Intermediate Usage
- "I'm traveling to multi-generational destination for 2 weeks, help me plan multi-generational travel harmonizer"
- "Analyze my travel situation: destination Paris, duration 10 days, budget $3000"
- "Generate multi-generational travel harmonizer recommendations for family travel with children"

### Advanced Usage
- "I need comprehensive multi-generational travel harmonizer for business travel to multiple countries"
- "Create detailed multi-generational travel harmonizer plan for extended travel with specific family requirements"
- "Provide multi-generational travel harmonizer framework with risk assessment and contingency planning"

## Acceptance Criteria

### Functional Requirements
1. ✅ Returns structured JSON output with proper formatting
2. ✅ Includes actionable travel recommendations based on input analysis
3. ✅ Provides relevant travel planning frameworks and templates
4. ✅ Demonstrates input-based differentiation (different inputs → different outputs)
5. ✅ Covers all specified modules: Need assessment framework, Activity layering system, Pace management strategies, Conflict prevention mechanisms

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
