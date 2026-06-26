# tryhair.ai OpenClaw Skill

## Overview

This skill integrates with tryhair.ai to provide two AI-powered image services:

* **Hairstyle Try-On**: Generate a preview of how a hairstyle would look on the user's face
* **Face Shape Analysis**: Analyze facial features to determine the user's face shape and proportions

Both services require a valid UID obtained from https://tryhair.ai after login.

---

## When to Run

### Hairstyle Try-On

Trigger this action when the user:

* Uploads a photo and says "Change my hairstyle"
* Asks "Try [curly hair/short hair/afro/long hair] on me"
* Wonders "Does this hairstyle suit me?" with a photo
* Mentions any specific hairstyle they want to try

---

### Face Shape Analysis

Trigger this action when the user:

* Uploads a photo and asks "What is my face shape?"
* Says "Analyze my face shape"
* Asks "What face shape do I have?"
* Wonders which hairstyles might suit their face shape

---

## Required Information

Before executing, ensure you have:

| Parameter | Description                                    | Required For          |
| --------- | ---------------------------------------------- | --------------------- |
| Photo     | Clear face photo (front-facing, good lighting) | Both actions          |
| UID       | User identifier from tryhair.ai                | Both actions          |
| Hairstyle | Text description of desired hairstyle          | Hairstyle try-on only |

---

## Obtaining a UID

If the user does not have a UID:

1. Visit https://tryhair.ai
2. Log in using Google or email
3. Find the UID displayed in the account dashboard
4. Provide the 16-character UID

---

## Execution

### Hairstyle Try-On

Run the script with `--action tryhair` (default action):

```bash
python3 scripts/tryhair.py \
  --image /path/to/user_photo.jpg \
  --style "desired hairstyle description" \
  --uid "USER_UID_FROM_TRYHAIR"
```

---

### Face Shape Analysis

```bash
python3 scripts/tryhair.py \
  --image /path/to/user_photo.jpg \
  --action faceshape \
  --uid "USER_UID_FROM_TRYHAIR"
```

---

### Example

```bash
python3 scripts/tryhair.py \
  --image /tmp/selfie.jpg \
  --action faceshape \
  --uid "aB3dEf9gH1jKlMnO"
```

---

## Output Handling

### Hairstyle Try-On – Success

```json
{
  "success": true,
  "output": "![Curly Bob Hairstyle](output_curly_bob_20250323_143022.jpg)",
  "message": "✨ Your curly bob hairstyle is ready!\nCredits remaining: 4",
  "saved_to": "output_curly_bob_20250323_143022.jpg",
  "remaining_credits": 4
}
```

---

### Face Shape Analysis – Success

```json
{
  "success": true,
  "output": "**Face Shape Analysis Result**\n\n**Primary shape:** Oval\n\n**Also possible:** Heart, Round\n\n**Face Width Ratio:** 1.00 : 0.95 : 0.82 : 1.28\n**Five-Eye Ratio:** 1.00 : 0.64 : 0.98\n**Three-Court Ratio:** 0.86 : 1.00 : 1.12",
  "message": "Face shape analysis completed.",
  "raw_data": {}
}
```

---

### Face Shape Types

* Round
* Square
* Oblong
* Oval
* Diamond
* Heart
* Triangle

---

### Additional Metrics

* **Face Width Ratio**: Width : Cheek : Jaw : Length proportions
* **Five-Eye Ratio**: Right eye : Inner eye : Left eye proportions
* **Three-Court Ratio**: Forehead : Mid-face : Lower-face proportions

---

## Need Purchase / Registration

### Insufficient Credits

```json
{
  "success": false,
  "need_purchase": true,
  "message": "⚠️ Insufficient credits. Please purchase a plan to continue.\n\n[Upgrade Now](https://tryhair.ai)",
  "redirect_url": "https://tryhair.ai",
  "action": "purchase",
  "plans": [
    {"name": "Trial Pack", "credits": 5, "price": "$1.99"},
    {"name": "Value Pack", "credits": 20, "price": "$4.99"}
  ]
}
```

---

### Invalid UID

```json
{
  "success": false,
  "need_purchase": true,
  "message": "⚠️ Invalid UID. Please log in to tryhair.ai to get your valid UID.\n\n[Register Now](https://tryhair.ai)",
  "redirect_url": "https://tryhair.ai",
  "action": "register"
}
```

---

## Error Responses

```json
{
  "success": false,
  "error": "Image file does not exist: /path/to/missing.jpg"
}
```

```json
{
  "success": false,
  "error": "Missing --style parameter for tryhair action"
}
```

```json
{
  "success": false,
  "error": "Request timed out. The service is taking longer than expected to process; please try again later."
}
```

---

## User Interaction Guidelines

### Asking for UID

> "To use this feature, I'll need your tryhair.ai UID. Please log in at https://tryhair.ai and share your UID with me."

---

### After Hairstyle Generation

> "Here's your {hairstyle} preview! You have {remaining_credits} credits left. Want to try another style?"

---

### After Face Shape Analysis

> "Your face shape appears to be {shape}. Based on this, hairstyles with {recommendation} typically work well. Would you like me to show you how a specific hairstyle would look?"

---

## Error Recovery

| Error Type           | Suggested Response                                                                                  |
| -------------------- | --------------------------------------------------------------------------------------------------- |
| Missing UID          | "I need your UID to continue. You can get it by logging in at https://tryhair.ai."                  |
| Insufficient credits | "You're out of free credits. Would you like to purchase a plan to continue?"                        |
| Image not clear      | "The image quality might be too low. Please upload a clear, front-facing photo with good lighting." |
| Network timeout      | "The service is taking longer than usual. Please try again in a moment."                            |

---

## Script Location

```
scripts/tryhair.py
```

---

## Environment Variables

| Variable               | Description                      | Default                                |
| ---------------------- | -------------------------------- | -------------------------------------- |
| OPENCLAW_TRYHAIR_API   | Hairstyle try-on API endpoint    | https://tryhair.ai/api/tryhair         |
| OPENCLAW_FACESHAPE_API | Face shape analysis API endpoint | https://tryhair.ai/api/facial_analysis |

---

## Notes

* The UID must be exactly 16 characters and is case-sensitive
* Face shape analysis may consume credits depending on backend configuration
* Generated images are saved in the current working directory
* Both services require an active internet connection
* The script automatically handles image preprocessing (resizing, format conversion)
* For best results, upload clear, front-facing photos with even lighting

