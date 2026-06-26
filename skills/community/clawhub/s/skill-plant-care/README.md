---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: "00000000000000000000000000000000"
    PropagateID: "00000000000000000000000000000000"
    ReservedCode1: 304502201d4d054706da93f5a7c4dc24f9e7d5d1c6019533a0330780e4f43da510b5cc08022100fae75ca28c0ffefd6000ba73e14715cfbff8e7ae3cfb0e59d8c5dd0bc97c1329
    ReservedCode2: 304502204ae2c6d7f74fab89f9c6d211a777a93e0f58fde56967109af2e7210258a90c47022100ac81b24482e6eb3098f5f76552bf6c48c1723185d84bb131ef3b5aa109b90ae4
---

# Plant Care Expert Skill

植物识别与养护专家技能 - OpenClaw Skill

## Overview

This is a professional plant identification and care skill that helps users:

- Identify plant species (via photos or descriptions)
- Assess care difficulty
- Determine if current environment is suitable for growing
- Provide detailed care guides
- Diagnose plant problems and offer solutions

## File Structure

```
skill-plant-care/
├── SKILL.md                         # Main skill file
├── SKILL.en.md                      # English version of skill file
├── README.md                        # Documentation (Chinese)
├── README.en.md                      # Documentation (English)
└── references/
    ├── plant_database.md            # Common plants (Chinese, 30+ species)
    ├── plant_database_extended.md   # Extended plants (Chinese, 167+ species)
    ├── plant_database_extended_en.md # Extended plants (English, 167+ species)
    ├── troubleshooting.md           # Problem diagnosis (Chinese)
    └── troubleshooting_en.md        # Problem diagnosis (English)
```

## Usage

### Triggers

This skill is triggered when users send:

- Plant photos
- Plant name inquiries
- Care questions
- Plant health diagnosis requests

### Example Conversations

**User**: Help me identify this plant

**Assistant**: Please upload a photo of the plant, and I will identify the species and provide care recommendations.

---

**User**: The leaves on my plant are turning yellow, what should I do?

**Assistant**: Could you please provide the following information?
1. Plant name or photo
2. Watering frequency
3. Placement (south-facing/north-facing/indoor)
4. How long has this been happening?

---

**User**: I want to grow an easy-to-care-for flowering plant

**Assistant**: What type of plant do you prefer?
- Foliage plants (Pothos, Spider Plant, etc.)
- Flowering plants (Kalanchoe, Jasmine, etc.)
- Succulents (Cacti, Aloe, etc.)

Also, please tell me about your growing environment:
1. Light conditions at placement location
2. Your local climate

## Core Features

### 1. Plant Identification

By analyzing photos or descriptions provided by users, identify plants and provide:

- Common name and scientific name
- Family and genus classification
- Morphological characteristics
- Care difficulty rating

### 2. Environment Assessment

Evaluate if the user's environment is suitable for the target plant:

- Light condition analysis
- Temperature range matching
- Humidity requirement comparison
- Ventilation assessment

### 3. Care Guide

Provide scientific care instructions:

- Light requirements
- Watering frequency and methods
- Soil mix recommendations
- Temperature ranges
- Fertilization schedule
- Repotting guide

### 4. Problem Diagnosis

Help users solve plant problems:

- Yellowing leaf diagnosis
- Wilting cause analysis
- Pest and disease identification
- Fertilization issue troubleshooting
- Emergency care instructions

## Care Difficulty Levels

| Level | Symbol | Description | Best For |
|-------|--------|-------------|----------|
| One | ⭐☆☆☆☆ | Extremely Easy | Beginners, busy people |
| Two | ⭐⭐☆☆☆ | Easy | Casual hobbyists |
| Three | ⭐⭐⭐☆☆ | Moderate | Experienced gardeners |
| Four | ⭐⭐⭐⭐☆ | Needs Attention | Advanced enthusiasts |
| Five | ⭐⭐⭐⭐⭐ | Expert Level | Professional growers |

## Frequently Asked Questions

### Q: How do I know if my plant needs water?

A: Use the finger test - insert your finger 2-3 cm into the soil, water when it feels dry. You can also observe soil color; water when it turns pale.

### Q: Why are my plant's leaves turning yellow?

A: Possible causes include: overwatering or underwatering, insufficient light, nutrient deficiency, soil alkalization, pests or diseases. Analysis needed based on specific situation.

### Q: How do I water succulents?

A: Succulents are drought-tolerant but dislike waterlogging. Follow the principle of "prefer dry over wet." Generally, watering once weekly is sufficient, and once monthly in winter.

### Q: Do indoor plants need fertilizer?

A: Yes. Plants need nutrient supplementation during the growing season. Generally, apply light fertilizer every 2 weeks in spring and summer, and stop fertilizing in winter.

## Plant Database

This skill includes comprehensive plant databases:

| Database | Language | Coverage |
|----------|----------|----------|
| plant_database.md | Chinese | 30+ common indoor plants |
| plant_database_extended.md | Chinese | 167+ Asian & North American plants |
| plant_database_extended_en.md | English | 167+ Asian & North American plants |

### Asian Plants (115+ species)
- Foliage Plants: 35 species
- Flowering Plants: 30 species
- Succulents & Cacti: 20 species
- Vines & Trailing: 15 species
- Fruit Plants & Herbs: 15 species

### North American Plants (52+ species)
- Foliage Plants: 15 species
- Flowering Plants: 15 species
- Succulents & Cacti: 12 species
- Outdoor & Garden: 10 species

## Important Notes

1. Information provided by this skill is for reference only; specific care methods should be adjusted based on actual conditions
2. For severe pest/disease problems or plants near death, seek help from professional gardeners
3. Some plants are toxic; do not ingest and keep away from children and pets
4. Do not plant or spread invasive species

## Changelog

### v1.0.0

- Initial release
- Plant identification feature
- Care difficulty assessment
- Plant database with 30+ common plants
- Problem diagnosis manual covering common issues

### v1.1.0

- Expanded plant database to 167+ species
- Added Asian plants (100+ species)
- Added North American plants (50+ species)
- Added English versions of all documentation

---

**Author**: MiniMax Agent AI
**Version**: 1.1.0
**License**: MIT
