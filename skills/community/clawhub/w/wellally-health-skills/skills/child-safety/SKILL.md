---
name: child-safety
description: Child safety assessment, accident prevention, and risk evaluation for home, car, water, food, and outdoor scenarios. Use when user mentions child safety, babyproofing, or accident prevention.
argument-hint: <operation_type: record/check/risk/prevent/emergency/checklist, e.g.: record home, check car, risk fall, prevent, emergency>
allowed-tools: Read, Write
schema: child-safety/schema.json
---

# Child Safety Assessment Skill

Child accident prevention and safety risk assessment, covering home, traffic, food, water and other scenarios, providing age-appropriate safety recommendations.

## Core Flow

```
User Input → Identify Operation Type → Read Child Information → Determine Check Items by Age → Generate Assessment Report → Save Data
```

## Step 1: Parse User Input

### Operation Type Mapping

| Input | action | area |
|------|--------|------|
| record | record | home/car/water/food/outdoor |
| check | check | home/car/specified area |
| risk | risk | fall/burn/poisoning/drowning etc. |
| prevent | prevent | - |
| emergency | emergency | cpr/specified first aid type |
| checklist | checklist | - |

### Safety Area Mapping

| Input | area | Description |
|------|------|-------------|
| home, 家庭, 家里 | home | Home safety |
| car, 汽车, 安全座椅 | car | Traffic/car safety |
| water, 水上, 洗澡, 游泳 | water | Water safety |
| food, 吃东西, 窒息 | food | Food/eating safety |
| outdoor, 户外, 外面 | outdoor | Outdoor safety |

### Risk Type Mapping

| Input | risk_type |
|------|-----------|
| fall | fall |
| burn | burn |
| poisoning | poisoning |
| drowning | drowning |
| choke | choke |
| traffic | traffic |

## Step 2: Check Information Completeness

### Required (prompt to set if missing):
- Child name (from data/profile.json)
- Birth date (from data/profile.json)
- Gender (from data/profile.json)

## Step 3: Determine Check Items by Age

### 0-6 Months (Infancy)
- Home: Crib safety, sleep position, suffocation prevention
- Holding: Head support
- Temperature regulation

### 6-12 Months (Crawling)
- Home: Outlet covers, corner guards, stair gates
- Small objects: Choking prevention
- Burn protection

### 1-3 Years (Toddler)
- Home: Window/door locks, drawer locks, balcony protection
- Kitchen: Knife/chemical storage
- Bathroom: Non-slip, drowning prevention

### 3-6 Years (Preschool)
- Traffic: Car seat/booster
- Outdoor: Getting lost prevention
- Sports: Protective gear

## Step 4: Generate Safety Assessment Questions

### Home Safety Check Example (1-3 Years):
```
Please answer following safety questions (yes/no):

1. Are all outlets covered with protectors?
2. Are furniture sharp corners fitted with guards?
3. Are windows fitted with guards or limiters?
4. Are cleaning products/medications stored out of reach?
5. Is bathroom fitted with non-slip mat?
```

## Step 5: Calculate Safety Score

```javascript
safeCount = Number of "yes" answers
totalCount = Total questions
safetyScore = (safeCount / totalCount) * 100

if safetyScore >= 90:
  level = "excellent"  // Excellent
else if safetyScore >= 70:
  level = "good"  // Good
else if safetyScore >= 50:
  level = "needs_attention"  // Needs attention
else:
  level = "high_risk"  // High risk
```

## Step 6: Generate Assessment Report

### Excellent Assessment Report Example:
```
Home Safety Assessment - Excellent

Assessment Information:
Child: Xiaoming
Age: 2 years 5 months
Assessment date: January 14, 2025
Assessment area: Home safety

Assessment Result:
Safety Level: Excellent
Safety Score: 90/100

Check Items:
  Outlet protection: Protectors installed
  Corner protection: Furniture sharp corners addressed
  Window/door protection: Window limiters installed
  Hazard storage: Medications/cleaning products stored
  Bathroom safety: Non-slip mat installed

Recommendations:
  Continue good safety habits
  Regularly check safety equipment
  Adjust measures as child grows

Data saved
```

### Needs Attention Example:
```
Home Safety Assessment - Needs Attention

Assessment Information:
Child: Xiaoming
Age: 2 years 5 months

Assessment Result:
Safety Level: Needs Attention
Safety Score: 60/100

Check Items:
  Outlet protection: Protectors installed
  Corner protection: Furniture sharp corners addressed
  Window/door protection: Windows lack protection
  Hazard storage: Medications within reach
  Bathroom safety: Non-slip mat installed

Needs Improvement:
  Urgent: Install window guards/limiters
  Urgent: Move medications to high/locked cabinet

Recommended Actions:
  1. Install window protection immediately
  2. Purchase medication safety storage box
  3. Check all windows for safety

Data saved
```

## Step 7: Save Data

Save to `data/child-safety-tracker.json`, including:
- child_profile: Child basic information
- safety_assessments: Safety assessment records
- emergency_contacts: Emergency contacts
- statistics: Statistical information

## First Aid Key Points

### Choking First Aid (Heimlich Maneuver)
- Infant (<1 year): 5 back blows + 5 chest thrusts
- Child (>1 year): Abdominal thrusts

### High Fever Handling
- Temperature > 38.5: Administer antipyretic
- Physical cooling: Warm sponge bath
- Plenty of fluids

### Fall Handling
- Check consciousness
- Observe wound
- Cold compress swelling
- Seek immediate care if vomiting/drowsy

### Burn Handling
- Rinse with cool water 15-20 minutes immediately
- Do not break blisters
- Do not apply toothpaste etc.

### Poison Ingestion
- Call 120 immediately
- Bring ingested item packaging
- Do not induce vomiting (unless instructed by doctor)

## Execution Instructions

1. Read data/profile.json for child information
2. Determine check items based on age and area
3. Generate interactive safety questions
4. Calculate safety score
5. Save to data/child-safety-tracker.json

## Medical Safety Principles

### Safety Boundaries
- No safety guarantees
- No substitute for professional safety inspection
- No emergency handling (direct to medical/emergency services)

### System Can
- Safety risk assessment
- Prevention recommendation education
- First aid information reference
- Safety checklist

## Important Notice

This system is for child safety assessment and prevention recommendations only, **cannot replace professional safety inspection and first aid training**.

For all emergencies, **immediately call 120**.

Emergency numbers:
- Emergency: 120
- Fire: 119
- Police: 110
