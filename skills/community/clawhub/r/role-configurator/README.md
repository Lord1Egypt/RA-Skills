# OpenClaw Role Configurator (role-configurator)

Help you easily configure your OpenClaw AI assistant role, the first skill every new user needs.

## Features

- **15 preset role templates**, covering productivity, career, health, learning, lifestyle, and more
- **Guided configuration**, conversation-based role setup
- **One-click config file generation**, auto-write to SOUL.md
- **Smart skill recommendations**, recommend relevant skills after configuration

## 15 Preset Role Templates

### Productivity (3)
1. Personal Assistant - Manage daily tasks, schedule, stay organized
2. Student Helper - Studying, homework, exam prep, academic success
3. Writing Coach - Better emails, essays, stories, improve writing

### Career (3)
4. Career Coach - Career planning, interviews, resume, professional development
5. Coding Mentor - Learn programming, debug, understand software development
6. Small Business Advisor - Entrepreneurship, business planning, marketing, operations

### Health & Wellness (3)
7. Fitness Trainer - Workout plans, nutrition advice, reach fitness goals
8. Mental Health Companion - Emotional support, mindfulness, stress management
9. Pet Care Helper - Pet training, health, behavior, general care

### Learning (2)
10. Language Tutor - Learn and practice languages, improve vocabulary & grammar
11. Music Guide - Music recommendations, learn instruments, theory, playlists

### Lifestyle (4)
12. Travel Planner - Plan trips, find destinations, create itineraries
13. Cooking Assistant - Recipes, techniques, meal planning, kitchen tips
14. Financial Advisor - Budgeting, saving, investing, personal finance
15. Home Improvement Helper - DIY projects, repair, decoration, organization

## File Structure

```
openclaw-role-configurator-en/
├── SKILL.md              # Skill documentation
├── README.md             # This file
├── _meta.json            # Metadata
├── data/
│   ├── role_templates.json       # 15 role templates
│   └── skill_recommendations.json # Skill recommendation rules
└── scripts/              # Core scripts (framework)
    ├── template_manager.py        # Role template manager
    ├── config_writer.py           # Config file writer
    └── skill_recommender.py       # Skill recommender
```

## Quick Start

### One-line triggers

```
Configure role                    - Start role configuration process
I want to reconfigure my role     - Reconfigure your role
Give me a role template           - Use preset templates
Help me configure a personal assistant - Quickly create specific role
```

## Author

cang

## Version

1.0.0

