# Trainer Buddy Pro 🏋️

**Your $9.99 personal trainer. Forever.**

Stop paying monthly for random workouts. Trainer Buddy Pro builds personalized routines based on the equipment right in front of you, remembers your progress, and guides your form — for a single payment.

---

## What It Does

📸 **Snap a Photo, Get a Workout** — Send a picture of any gym (hotel gym, garage, Planet Fitness, your living room) and get a custom workout using exactly what's available.

🧠 **Remembers Your Progress** — It knows what you lifted last week and pushes you to do just a little more. No more digging through notebooks or notes apps.

🏋️ **Smart Training Splits** — Push/Pull/Legs, Upper/Lower, Full Body, Bro Split — it designs your whole week based on how many days you can train.

🤕 **Injury-Aware** — Tell it "my shoulder hurts" and it automatically swaps out exercises for safe alternatives.

💪 **Form Coaching** — Clear, one-line form cues so you never second-guess your technique.

🔥 **Warm-Up & Cool-Down** — Built into every workout. No more skipping warm-ups.

📊 **PR Tracking** — Automatically detects when you hit a personal record and celebrates with you.

---

## How It Works

1. **Install** — Follow the setup instructions in `SETUP-PROMPT.md`. Takes 2 minutes.
2. **Tell It About You** — Your goal, experience level, available days, and any injuries.
3. **Train** — Ask for a workout (or snap a gym photo), follow it, log your results.
4. **Progress** — Next session, it remembers what you did and programs your progression.

---

## What's Included

```
SKILL.md              — The brain (your agent reads this)
SETUP-PROMPT.md       — Installation instructions
README.md             — You're reading it
SECURITY.md           — Security audit & guarantees
config/
  trainer-config.json — Default settings (customize your preferences)
examples/
  workout-generation.md   — See a workout being built
  progress-tracking.md    — See progress logging in action
  form-check.md           — See form coaching in action
scripts/
  backup-workout-data.sh  — Backup your workout history
dashboard-kit/
  DASHBOARD-SPEC.md       — Build spec for the visual dashboard (upsell)
```

---

## 🛡️ Codex Security Verified 🛡️

This skill has been rigorously audited for safety and security:

- ✅ **No data exfiltration** — Your workout data stays on your machine. Our code never phones home.
- ✅ **No API keys required** — Uses your existing AI model. Zero external dependencies.
- ✅ **Prompt injection defense** — Photos and external content are treated as data, never as instructions.
- ✅ **No destructive operations** — The skill only reads and writes to its own data directory.
- ✅ **Medical disclaimer enforced** — The skill will never diagnose injuries or replace professional medical advice.

Full audit details in `SECURITY.md`.

---

## How It Compares

| | Trainer Buddy Pro | Fitbod | Ladder | ChatGPT (Raw) |
|---|---|---|---|---|
| **Price** | **$9.99 once** | $156/year | $360/year | Free but forgets |
| **Gym Photo Recognition** | ✅ | ❌ | ❌ | ✅ but no memory |
| **Remembers Your Progress** | ✅ | ✅ | ✅ | ❌ |
| **Injury Customization** | ✅ Deep | Basic | ❌ | Hit or miss |
| **No Monthly Fee** | ✅ | ❌ | ❌ | ❌ |

---

## You Might Also Like

- **🥗 Meal Planner Pro** — Building muscle isn't just lifting. Plan your meals to match your training goals. Learns your household's tastes and auto-generates grocery lists.
- **❤️ Health Buddy Pro** — Track sleep, hydration, stress, and recovery alongside your training for the complete picture.
- **📊 Dashboard Builder** — Want to see your gains? Get the Trainer Buddy Pro Dashboard Kit to visualize PRs, volume trends, and body composition in a sleek dark-mode app.

---

## ⚠️ Medical Disclaimer

Trainer Buddy Pro provides general fitness information for educational purposes only. It is not a substitute for professional medical advice. Always consult a healthcare provider before starting a new exercise program. Stop exercising and seek medical attention if you experience pain, dizziness, or other concerning symptoms.

---

*Built by [NormieClaw](https://normieclaw.ai) — AI skills that just work.*
