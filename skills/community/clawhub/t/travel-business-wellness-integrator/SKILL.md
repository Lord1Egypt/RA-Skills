---
name: Business Travel Wellness Integrator
slug: travel-business-wellness-integrator
description: Integrates wellness into business travel
category: tourism
type: descriptive
language: en
author: Golden Bean (OpenClaw)
version: v1.1.0
tags: business-travel, wellness-integration, work-life-balance, travel-health, corporate-wellness
---

# Business Travel Wellness Integrator

## Overview

Integrates wellness practices into business travel for sustained performance

This is a **pure descriptive skill** that provides frameworks, templates, and heuristic analysis for travel planning and preparation. No real code execution, external APIs, or network requests are performed.

## Trigger Keywords

Use this skill when planning travel experiences related to:

- **business travel** and **wellness**
- health considerations
- performance planning
- Travel routine if applicable
- recovery if applicable

### Primary Triggers
- "Help me plan business travel wellness integrator for my upcoming trip"
- "Provide framework for business travel in travel context"
- "Create checklist for business travel wellness integrator"
- "Analyze my travel situation using business travel wellness integrator principles"

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

- **Travel wellness assessment**
- **Routine adaptation framework**
- **Recovery optimization**
- **Performance sustainability planning**

### Detailed Module Descriptions

**Travel wellness assessment**
- Provides structured approach to travel wellness assessment
- Includes templates and checklists
- Offers best practices and considerations

**Routine adaptation framework**
- Delivers practical routine adaptation framework
- Includes implementation guides
- Provides customization options

**Recovery optimization**
- Offers recovery optimization
- Includes ethical considerations
- Provides risk mitigation strategies

**Performance sustainability planning**
- Provides performance sustainability planning
- Includes integration guidance
- Offers long-term planning support


## Usage Scenarios

1. **User input:** "I fly 3x/month for work and feel destroyed. Design a wellness integration system for my business travel."
→ **Expected output:** End-to-end wellness system — pre-trip preparation (sleep banking, immune support), in-flight routine (hydration schedule, compression socks, movement), hotel-room workout (bodyweight 15-min circuit), jet-lag management (light-exposure schedule), nutrition strategy, and post-trip recovery protocol.
2. **User input:** "Our sales team travels heavily and burnout is rising. Create a corporate business-travel wellness policy."
→ **Expected output:** Travel wellness policy template — maximum consecutive travel days, recovery-day mandate, wellness-expense budget, hotel wellness-filter criteria, and team-leader checklist for monitoring travel fatigue.
3. **User input:** "Turn my 5-day conference trip into something that doesn't wreck my health goals."
→ **Expected output:** Conference wellness plan — schedule audit, networking nutrition strategy, sleep-protection tactics, exercise micro-dosing (10-min sessions between sessions), and alcohol-moderation scripts.



### Scenario 2: 出差当牛做马还要顾身体
**User input:** "我在上海上班，每周都要出差去深圳/北京/成都，不是在酒店就是在高铁飞机上。胃病犯了还不敢请假，有什么保命方案？"
**Expected output:** 中国打工人出差保命手册——高铁场景：上车前买一瓶常温矿泉水+一盒水果切，拒绝动车盒饭；酒店场景：入住后第一件事烧一壶开水烫马桶圈和遥控器，随身带折叠烧水壶；吃饭场景：外卖点当地菜而非连锁快餐，每口咀嚼20下；作息场景：设23:30强制关机闹钟，拉窗帘全黑，戴蒸汽眼罩。一周最多接3天出差，第4天必须坐办公室。

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
- "Help me with business travel wellness integrator for my trip to Japan"
- "Provide business travel framework for travel planning"
- "Create business travel wellness integrator checklist for my upcoming vacation"

### Intermediate Usage
- "I'm traveling to business travel destination for 2 weeks, help me plan business travel wellness integrator"
- "Analyze my travel situation: destination Paris, duration 10 days, budget $3000"
- "Generate business travel wellness integrator recommendations for family travel with children"

### Advanced Usage
- "I need comprehensive business travel wellness integrator for business travel to multiple countries"
- "Create detailed business travel wellness integrator plan for extended travel with specific wellness requirements"
- "Provide business travel wellness integrator framework with risk assessment and contingency planning"

## Acceptance Criteria

### Functional Requirements
1. ✅ Returns structured JSON output with proper formatting
2. ✅ Includes actionable travel recommendations based on input analysis
3. ✅ Provides relevant travel planning frameworks and templates
4. ✅ Demonstrates input-based differentiation (different inputs → different outputs)
5. ✅ Covers all specified modules: Travel wellness assessment, Routine adaptation framework, Recovery optimization, Performance sustainability planning

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
