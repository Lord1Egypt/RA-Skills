# Soulsync

> Make your relationship with AI warmer

An OpenClaw Skill plugin that analyzes your conversation history with AI, identifies emotional expressions, calculates a **SyncRate**, and adjusts the AI's response style accordingly.

[中文文档](README_CN.md)

---

## Features

- **Two-way Sync**: Build better rapport with AI, responses feel more attuned
- **Non-intrusive**: Only affects response style, not functional efficiency
- **User Visible**: View your sync rate status anytime
- **Automatic**: Daily calculations without manual intervention
- **Daily Cap**: Prevents gaming the system, ensures natural growth
- **Dual Personality**: Switch between Warm / Sarcastic-Humorous styles

---

## Installation

```bash
clawhub install soulsync
```

---

## Usage

### View Sync Rate Status

```
/syncrate
```

### Switch Personality Style

```
/syncrate style warm      # Switch to warm style
/syncrate style humorous  # Switch to sarcastic-humorous style
```

### View History

```
/syncrate history
```

---

## Sync Rate Levels

| Level | Sync Rate | Warm Style | Humorous Style |
|-------|-----------|------------|----------------|
| Async | 0-20% | Professional, concise, task-focused | Professional, concise, task-focused |
| Connected | 21-40% | Friendly, professional yet warm | Slightly teasing professional execution |
| Synced | 41-60% | Relaxed, helpful | Roast mode activated, occasional tsundere |
| High Sync | 61-80% | Warm, in sync | Sarcastic yet humorous, caring through precise jabs |
| Perfect Sync | 81-100% | Deep understanding, anticipates needs | Intimate banter, deep understanding,默契 roasting |

---

## Configuration

Edit `config.json` to customize:

```json
{
  "levelUpSpeed": "normal",    // Level up speed: slow / normal / fast
  "dailyMaxIncrease": 2,       // Daily max increase (%)
  "dailyDecay": 0,             // Daily decay (0 = no decay)
  "decayThresholdDays": 14,    // Days without interaction before decay starts
  "personalityType": "warm",   // Default personality: warm / humorous
  "language": "en",            // Language: en / zh-CN
  "customLevels": {}           // Custom level names
}
```

### Custom Level Names

```json
{
  "customLevels": {
    "synced": "Kindred Spirits",
    "perfectSync": "Mind Meld"
  }
}
```

---

## How It Works

### Daily Analysis Flow

```
Cron Task (daily at midnight)
    │
    ├── Read sessions_history
    │
    ├── Phase 1: Keyword Filtering
    │   ├── No emotion words → Ignore
    │   ├── Pure emotion words → Direct scoring
    │   └── Mixed words → LLM analysis
    │
    ├── Phase 2: LLM Precise Analysis (mixed messages only)
    │
    ├── Calculate sync rate change (with daily cap)
    │
    └── Update state files
```

### Scoring Formula

```
baseScore = intensity(1-10) × (1 + currentSyncRate/200)
actualIncrease = baseScore / levelUpSpeedCoeff

# Daily cap: max +2%
# Decay rule: 14 days without interaction → -5%
```

---

## File Structure

```
soulsync/
├── SKILL.md                 # Skill definition
├── SKILL_CN.md              # Chinese skill definition
├── config.json              # Default configuration
├── emotion-words.json       # Emotion word dictionary
└── styles/
    ├── warm.md              # Warm style guide
    ├── warm_CN.md           # Chinese warm style guide
    ├── humorous.md          # Sarcastic-humorous style guide
    └── humorous_CN.md       # Chinese humorous style guide
```

---

## First-Time Installation

When first installed, Soulsync will:

1. Check if conversation history exists
2. If history exists, analyze the last 30 days of interaction
3. Calculate initial sync rate (no cap)
4. Send welcome notification

---

## License

MIT
