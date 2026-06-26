---
name: onboarding
description: First-time user onboarding flow for WellallyHealth. Guides users through language selection, profile setup, and feature introduction. Automatically triggered for new users.
argument-hint: <[start|continue|complete|skip] [step_number]>
allowed-tools: Read, Write
---

# Onboarding Skill

Guides new users through the initial setup process for WellallyHealth. This skill is automatically triggered when no user-settings.json exists.

## Core Flow

```
New User Detected -> Check onboarding status -> [start] Begin onboarding flow
                                                -> [continue] Resume from last step
                                                -> [complete] Mark as completed
                                                -> [skip] Skip onboarding
```

## Onboarding Steps

| Step | Name | Description | Required |
|------|------|-------------|----------|
| 1 | language_selection | Choose preferred language | Yes |
| 2 | profile_setup | Set gender, height, weight, birth date | Yes |
| 3 | feature_intro | Introduction to key features | No |
| 4 | completion | Confirm onboarding complete | Yes |

## Step 1: Language Selection

```
Welcome to WellallyHealth!

Please select your preferred language:
1. English
2. 中文 (Chinese)

Type "1" or "2" to select.
```

## Step 2: Profile Setup

After language selection, guide user to set up their profile:

```
Let's set up your profile.

Please provide the following information:
1. Gender (M/F)
2. Height (in cm)
3. Weight (in kg)
4. Birth date (YYYY-MM-DD)

Example: F 165 55 1990-01-15
```

## Step 3: Feature Introduction

Brief introduction to key features:

```
WellallyHealth offers the following features:

• /profile - View and update your profile
• /medication - Track medications and adherence
• /diet - Record meals and nutrition
• /fitness - Log exercise and activity
• /symptom - Record symptoms
• /ai-health - Get AI-powered health insights

Type "/help" anytime to see all available commands.
```

## Step 4: Completion

```
Setup complete! You're ready to use WellallyHealth.

Your profile:
[Display summary]

Next steps:
- Try "/diet add" to log a meal
- Use "/medication add" to track medications
- Check "/ai-health" for insights

Type "/onboarding complete" to finish, or "/onboarding skip" to exit.
```

## Data Structure

Updates `data/user-settings.json`:

```json
{
  "onboarding": {
    "completed": false,
    "language_set": false,
    "steps_completed": ["language_selection", "profile_setup"]
  }
}
```

## Auto-Detection

Onboarding should start automatically when:
1. `data/user-settings.json` does not exist
2. `onboarding.completed == false`

## Execution Instructions

```
1. Check if user-settings.json exists
2. If not, create with default values
3. Start from first incomplete step
4. Mark each step as completed in steps_completed array
5. When all required steps done, prompt for completion
```

## Example Interactions

### First-Time User (Auto-Trigger)

```
User: [First message - any content]

System:
Welcome to WellallyHealth!

I see you're new here. Let's set up your account.

[Step 1: Language Selection]
Please select your preferred language:
1. English
2. 中文 (Chinese)
```

### Resume Onboarding

```
User: /onboarding continue

System:
Welcome back! You've completed:
✓ Language selection
✓ Profile setup

Next: Feature introduction

Press Enter to continue, or type "skip" to skip this step.
```

### Skip Onboarding

```
User: /onboarding skip

System:
Onboarding skipped.

You can set up your profile later with /profile
Change language anytime with /language

Type "/help" to see available commands.
```

### Complete Onboarding

```
User: /onboarding complete

System:
Congratulations! You're all set up.

Your onboarding is now complete. All features are available.

[Shows profile summary]
```
