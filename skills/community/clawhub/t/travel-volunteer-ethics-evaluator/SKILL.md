---
name: Volunteer Tourism Ethics Evaluator
slug: travel-volunteer-ethics-evaluator
description: Helps evaluate volunteer tourism opportunities
category: tourism
type: descriptive
language: en
author: Golden Bean (OpenClaw)
version: "1.1.0"

tags: voluntourism, ethical-travel, volunteer-evaluation, responsible-tourism, impact-assessment
---

# Volunteer Tourism Ethics Evaluator

## Overview

Helps travelers evaluate volunteer tourism opportunities for ethical impact

This is a **pure descriptive skill** that provides frameworks, templates, and heuristic analysis for travel planning and preparation. No real code execution, external APIs, or network requests are performed.

## Trigger Keywords

Use this skill when planning travel experiences related to:

- **volunteer** and **ethics**
- evaluation considerations
- impact planning
- Travel sustainable if applicable
- community if applicable

### Primary Triggers
- "Help me plan volunteer tourism ethics evaluator for my upcoming trip"
- "Provide framework for volunteer in travel context"
- "Create checklist for volunteer tourism ethics evaluator"
- "Analyze my travel situation using volunteer tourism ethics evaluator principles"

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

- **Ethical evaluation framework**
- **Organization assessment checklist**
- **Skill-match analysis**
- **Sustainable impact planning**

### Detailed Module Descriptions

**Ethical evaluation framework**
- Provides structured approach to ethical evaluation framework
- Includes templates and checklists
- Offers best practices and considerations

**Organization assessment checklist**
- Delivers practical organization assessment checklist
- Includes implementation guides
- Provides customization options

**Skill-match analysis**
- Offers skill-match analysis
- Includes ethical considerations
- Provides risk mitigation strategies

**Sustainable impact planning**
- Provides sustainable impact planning
- Includes integration guidance
- Offers long-term planning support

## Usage Scenarios

### Scenario 1

**User input:** "Evaluate this orphanage volunteer program in Cambodia before I commit $2,000."

**Expected output:** Ethical evaluation scorecard — organization transparency, child-protection policy, local-staff ratio, community need vs. volunteer demand, long-term impact evidence, and 'orphanage tourism' red flags — with go/no-go recommendation and alternative suggestions.

### Scenario 2

**User input:** "I want to volunteer abroad but don't want to do harm. Create a vetting framework."

**Expected output:** 5-step vetting process — mission alignment check, community-led vs. outsider-imposed assessment, skills-match test (do they need what I offer or just my money?), economic displacement analysis, post-departure sustainability plan — with 20 vetting questions to ask organizations.

### Scenario 3

**User input:** "Compare these 3 wildlife conservation volunteer programs for ethical quality."

**Expected output:** Comparative ethical matrix scoring on animal welfare, research legitimacy, local employment, visitor education impact, and transparency — with specific green/yellow/red flags for each and recommended choice with justification.
### Scenario 4: 想去尼泊尔做义工旅行
**User input:** "看到网上有很多尼泊尔义工旅行的项目，就是那种一边旅游一边做公益的，交几千块报名费，靠谱吗？"
**Expected output:** 评估义工旅行项目的伦理问题：1）警惕'付费义工'陷阱——真正的NGO不会向志愿者收取高额费用，收费项目本质上是商业旅游；2）伦理风险——短期孤儿院义工可能对儿童造成依恋创伤（来了一批又走一批）；3）推荐替代——通过正规国际NGO组织（如UN Volunteers、IVHQ）报名，或者在国内参加'乡村支教'项目更方便（美丽中国、支教中国2.0）。建议优先考虑四川/云南的短期支教，文化壁垒小且费用低。

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
- "Help me with volunteer tourism ethics evaluator for my trip to Japan"
- "Provide volunteer framework for travel planning"
- "Create volunteer tourism ethics evaluator checklist for my upcoming vacation"

### Intermediate Usage
- "I'm traveling to volunteer destination for 2 weeks, help me plan volunteer tourism ethics evaluator"
- "Analyze my travel situation: destination Paris, duration 10 days, budget $3000"
- "Generate volunteer tourism ethics evaluator recommendations for family travel with children"

### Advanced Usage
- "I need comprehensive volunteer tourism ethics evaluator for business travel to multiple countries"
- "Create detailed volunteer tourism ethics evaluator plan for extended travel with specific ethics requirements"
- "Provide volunteer tourism ethics evaluator framework with risk assessment and contingency planning"

## Acceptance Criteria

### Functional Requirements
1. ✅ Returns structured JSON output with proper formatting
2. ✅ Includes actionable travel recommendations based on input analysis
3. ✅ Provides relevant travel planning frameworks and templates
4. ✅ Demonstrates input-based differentiation (different inputs → different outputs)
5. ✅ Covers all specified modules: Ethical evaluation framework, Organization assessment checklist, Skill-match analysis, Sustainable impact planning

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
