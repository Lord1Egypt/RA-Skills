# Health Chat Skill - Quick Start Guide

## Overview

`health-chat` is the **unified health conversation entry point** for WellallyHealth. It automatically loads all health data for each conversation and provides intelligent health consultation and data analysis services.

## How to Use

### Basic Invocation
```
/health-chat [your health question]
```

### Example Invocations
```
/health-chat How is my blood pressure lately?
/health-chat What medications should I take today?
/health-chat Give me a health assessment
/health-chat I've been feeling dizzy lately, what's the cause?
```

## Supported Conversation Types

### 1. Data Query
Query health data, test records, medication information, etc.

**Example Questions:**
- "How is my blood pressure?"
- "How has my weight changed recently?"
- "What medications do I take today?"
- "What is my BMI?"

### 2. Health Analysis
Comprehensive health status analysis, generate assessment reports.

**Example Questions:**
- "Give me a health assessment"
- "Analyze my overall health status"
- "How is my sleep quality?"

### 3. Risk Assessment
Assess various health risks.

**Example Questions:**
- "Is my hypertension risk high?"
- "What health risks should I be aware of?"
- "What needs special attention in my health?"

### 4. Health Recommendations
Get personalized health advice.

**Example Questions:**
- "How can I improve my sleep?"
- "Should I reduce my hypertension risk?"
- "What health recommendations do you have?"

### 5. Symptom Consultation
Analyze symptoms and provide reference.

**Example Questions:**
- "What's the cause of recent dizziness?"
- "Feeling fatigued, what could be the reason?"
- "Does this symptom need attention?"

### 6. Medication Related
Medication reminders and drug information.

**Example Questions:**
- "Did I take my meds today?"
- "What are the side effects of this medication?"
- "Do these medications have interactions?"

## Automatic Data Loading

Every time `/health-chat` is called, the system automatically:

1. **Must-Read Data (loaded every time):**
   - `data/profile.json` - User basic info
   - `data/user-settings.json` - User preferences
   - `data/ai-config.json` - AI configuration

2. **On-Demand Reading (based on question type):**
   - Chronic condition trackers (e.g., hypertension, diabetes)
   - Medication records (medications.json)
   - Allergy records (allergies.json)
   - Test records (index.json)
   - Health logs (health-feeling-logs.json)

3. **Database Files (read when needed):**
   - Food nutrition database
   - Vaccine database
   - Nutrition reference standards

## Conversation History

The system automatically saves conversation history to `data/ai-history.json`, including:
- User input
- Intent recognition
- Data sources used
- Response summary
- Follow-up suggestions

Can resume previous conversation:
```
/health-chat What did we talk about last time?
```

## Safety Boundaries

- ⚠️ This system **does not replace doctor diagnosis**
- ⚠️ This system **does not provide prescription recommendations**
- ⚠️ High-risk situations will **recommend medical care**
- All responses include medical disclaimer

## Relationship with Other Skills

`health-chat` is the unified entry point, internally calling other specialized skills:

| Scenario | Internal Call |
|-----------|----------------|
| Medication management | `/medication` |
| Symptom recording | `/symptom` |
| Health feeling logs | `/log-feel` |
| Medical records query | `/query-health` |
| Comprehensive analysis | `/ai-health` |

Users can simply use `/health-chat` without needing to remember specific skill names.

## Quick Test

Try these commands:

```
/health-chat Hello, please introduce yourself
/health-chat What is my health profile?
/health-chat What health issues need attention?
/health-chat What is my medication plan?
```

## Technical Details

- **Skill Location**: `.claude/skills/health-chat/`
- **Schema**: `schema.md` - Data structure and type definitions
- **Examples**: `examples.md` - Detailed conversation examples
- **Main Instructions**: `SKILL.md` - Complete execution flow

---

**Tip**: This is the recommended primary conversation entry point. Almost all health-related questions can be handled through `/health-chat`.
