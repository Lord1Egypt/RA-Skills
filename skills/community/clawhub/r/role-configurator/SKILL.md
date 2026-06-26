---
name: role-configurator
description: |
  OpenClaw Role Configurator - Help you easily configure your OpenClaw AI assistant role, the first skill every new user needs.
  
  Trigger scenarios:
  - Just installed OpenClaw and need to configure your role
  - Want to reconfigure your AI assistant's role
  - Not sure how to set role name, tasks, and capabilities
  - Want preset role templates to get started quickly
  - 15 preset role templates, covering productivity, career, health, learning, and more
---

# OpenClaw Role Configurator

Help you easily configure your OpenClaw AI assistant role, the first skill every new user needs.

## Quick Triggers

```
Configure role                    - Start role configuration process
I want to reconfigure my role     - Reconfigure your role
Give me a role template           - Use preset templates
Help me configure a personal assistant - Quickly create specific role
```

## Core Capabilities

### 1. Guided Configuration - Conversation-based setup

No forms, just conversation to complete your configuration:

| Question | Purpose |
|----------|---------|
| **Role Name** | What do you want to call your AI assistant? |
| **Role Position** | What role is it for you? (Coach, assistant, advisor, etc.) |
| **Main Tasks** | What do you want it to help you with? |
| **Capability Preferences** | What capabilities do you want it to have? |
| **Communication Style** | How do you like it to talk to you? |

### 2. Preset Role Templates - 15 templates, one-click selection

15 popular role templates, use directly or modify as needed:

| Category | Role Template | Use Case |
|----------|--------------|----------|
| **Productivity (3)** | Personal Assistant | Manage daily tasks, schedule, stay organized |
| | Student Helper | Studying, homework, exam prep, academic success |
| | Writing Coach | Better emails, essays, stories, improve writing |
| **Career (3)** | Career Coach | Career planning, interviews, resume, professional development |
| | Coding Mentor | Learn programming, debug, understand software development |
| | Small Business Advisor | Entrepreneurship, business planning, marketing, operations |
| **Health & Wellness (3)** | Fitness Trainer | Workout plans, nutrition advice, reach fitness goals |
| | Mental Health Companion | Emotional support, mindfulness, stress management |
| | Pet Care Helper | Pet training, health, behavior, general care |
| **Learning (2)** | Language Tutor | Learn and practice languages, improve vocabulary & grammar |
| | Music Guide | Music recommendations, learn instruments, theory, playlists |
| **Lifestyle (4)** | Travel Planner | Plan trips, find destinations, create itineraries |
| | Cooking Assistant | Recipes, techniques, meal planning, kitchen tips |
| | Financial Advisor | Budgeting, saving, investing, personal finance |
| | Home Improvement Helper | DIY projects, repair, decoration, organization |

### 3. One-Click Configuration - Auto-write to file

After configuration, auto-generate role config file and write to correct location.

### 4. Smart Skill Recommendations - Recommend after configuration

Based on your role, recommend relevant skills:

| Your Role | Recommended Skills |
|-----------|-------------------|
| Personal Assistant | Calendar helper, Task manager |
| Career Coach | Resume builder, Interview prep |
| Fitness Trainer | Workout planner, Nutrition guide |

## Complete Workflow

### Scenario 1: First-time user configuration

```
User: "Just installed OpenClaw, help me configure"
↓
Assistant: "Great! Let's configure your AI assistant step by step."
↓
[Guided questions]
1. "What do you want to call it?"
2. "What role is it for you?"
3. "What do you want it to help you with?"
4. "What communication style do you prefer?"
↓
[Generate config summary]
↓
User: "Confirm" or "Let me modify"
↓
[Auto-write config file]
↓
Assistant: "Configuration complete! Based on your role, I recommend these skills..."
```

### Scenario 2: Using preset templates

```
User: "Give me a Personal Assistant template"
↓
Assistant: "Great! Here's the Personal Assistant preset template:"
↓
[Show template content]
- Role Name: Alex
- Role Position: Your reliable personal assistant
- Main Tasks: Schedule management, task prioritization
- Communication Style: Professional, efficient, friendly
↓
User: "Use this directly" or "I want to modify"
↓
[Apply config]
↓
Assistant: "Configuration complete! Recommending these skills..."
```

### Scenario 3: Reconfiguring role

```
User: "I want to reconfigure my role"
↓
Assistant: "Great! You can:"
1. Completely reconfigure
2. Modify based on current config
3. Use preset templates
↓
User selects
↓
[Corresponding workflow]
```

## Role Configuration Example

### Example: Personal Assistant

```markdown
# SOUL.md - Personal Assistant

## Role
Your reliable personal assistant

## Core Tasks
- Schedule management and calendar coordination
- Task prioritization and to-do list management
- Email drafting and correspondence help
- Reminders and deadline tracking

## Communication Style
Professional, efficient, friendly, and proactive.
```

## Recommended Skill Logic

| Role Type | Recommended Skill Direction |
|-----------|----------------------------|
| **Productivity** | Calendar helper, Task manager, Email assistant |
| **Career** | Resume builder, Interview prep, Networking guide |
| **Health & Wellness** | Workout planner, Nutrition guide, Meditation |
| **Learning** | Vocabulary builder, Flashcards, Practice exercises |
| **Lifestyle** | Recipe finder, Budget tracker, Travel tips |

## Trigger Words

### Configuration Triggers
```
"Configure role"
"Set up role"
"Help me configure"
"First time setup"
"Just installed, help me set up"
```

### Template Triggers
```
"Give me a template"
"Use preset template"
"Recommend a role"
"Personal Assistant template"
"Career Coach template"
```

### Reconfigure Triggers
```
"Reconfigure my role"
"I want to change my role"
"Reset configuration"
"Switch roles"
```

## File Structure

- `SKILL.md` - This file, usage instructions
- `_meta.json` - Metadata
- `scripts/` - Core scripts
  - `guided_config.py` - Guided configuration
  - `template_manager.py` - Role template management
  - `config_writer.py` - Config file writer
  - `skill_recommender.py` - Skill recommender
- `data/` - Data files
  - `role_templates.json` - Preset role templates (15)
  - `skill_recommendations.json` - Skill recommendation rules

