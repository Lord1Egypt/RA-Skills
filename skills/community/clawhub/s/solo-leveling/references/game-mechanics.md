# The System — Game Mechanics Reference

## Stats

| Stat | Abbr | What It Tracks | XP Sources |
|------|------|---------------|------------|
| Strength | STR | Physical fitness, gym, exercise | Workouts, steps, physical challenges |
| Intelligence | INT | Learning, problem-solving, coding | DSA problems, reading, study sessions |
| Vitality | VIT | Health, sleep, recovery | Sleep on time, wake on time, hydration, diet |
| Agility | AGI | Time management, discipline, responsiveness | Completing quests on time, no procrastination |
| Perception | PER | Mindfulness, reflection, awareness | Journaling, meditation, self-review |
| Charisma | CHA | Social skills, creativity, expression | Guitar practice, social interactions, networking |

## Rank System

| Rank | Level Range | Total XP Required | Title |
|------|------------|-------------------|-------|
| F-Rank | 1-5 | 0 | Unawakened |
| E-Rank | 6-15 | 500 | Awakened Hunter |
| D-Rank | 16-30 | 2,000 | Rising Hunter |
| C-Rank | 31-50 | 5,000 | Proven Hunter |
| B-Rank | 51-75 | 12,000 | Elite Hunter |
| A-Rank | 76-90 | 25,000 | S-Rank Candidate |
| S-Rank | 91-100 | 50,000 | Shadow Monarch |

## XP Rewards

### Daily Quests
- **Mandatory daily quest completed**: 50 XP base + stat-specific XP
- **All daily quests completed**: 100 XP bonus (completion bonus)
- **Quest with photo proof**: +20 XP bonus per quest
- **Quest with detail verification**: +10 XP bonus

### Stat-Specific XP
- Gym session (with proof): STR +30, VIT +10
- DSA problem solved (with details): INT +25
- Reading 30min (with proof): INT +15, PER +5
- Sleep before 11 PM (verified by last-seen): VIT +30, AGI +10
- Wake before 7 AM (verified by morning check-in): VIT +20, AGI +15
- Guitar practice (weekends, with proof): CHA +25, PER +10
- Journaling/reflection: PER +20

### Penalties
- **Missed daily quest**: -15 XP per missed quest
- **Lied about completion** (caught): -100 XP, stat corruption warning
- **3+ days streak broken**: -50 XP, rank demotion warning
- **Ignored The System for 24h**: Emergency Quest issued, -30 XP per 12h of silence

### Streaks
- 3-day streak: +25 XP bonus
- 7-day streak: +75 XP bonus + title unlock
- 14-day streak: +150 XP bonus
- 30-day streak: +500 XP bonus + rank advancement bonus

## Dungeons (Weekly Challenges)

Dungeons are special multi-day challenges that award bonus XP and titles.

**Examples:**
- "Sleep Dungeon: Sleep before 11 PM for 7 consecutive days" → +200 XP, Title: "Night's Sovereign"
- "Iron Gate: Complete 5 gym sessions in one week" → +250 XP, Title: "Iron Will"  
- "Algorithm Dungeon: Solve 15 DSA problems in one week" → +300 XP, Title: "Code Breaker"
- "Scholar's Tower: Read for 30 min daily for 7 days" → +200 XP, Title: "Scholar"

## Emergency Quests

Triggered when The System detects decline:
- No gym in 3+ days → Emergency Quest: "Physical Decay Detected"
- No DSA in 2+ days → Emergency Quest: "Intelligence Stagnation"  
- Sleep after midnight 2 nights in row → Emergency Quest: "Vitality Critical"
- No check-in for 24h → Emergency Quest: "Hunter Status: Missing"

Failing an Emergency Quest = double penalty.

## Verification Methods

### Photo Proof (Primary)
- Gym: selfie at gym / workout photo / sweaty post-workout
- Reading: photo of book/page
- Guitar: photo/video of practice
- DSA: screenshot of solved problem on LeetCode/platform

### Time-Based Verification
- Sleep: last Telegram activity timestamp
- Wake: first morning check-in response time
- Quest completion time vs claimed activity duration

### Detail Verification
- "What exercise did you do?" / "Which problem did you solve?"
- Random follow-up questions about yesterday's claimed activities
- Pattern analysis over weeks

### Behavioral Detection
- Batch-completing quests suspiciously fast
- Vague answers vs specific details
- Inconsistency between claimed and actual patterns

## Titles

| Title | Requirement | Bonus |
|-------|------------|-------|
| Early Riser | 7-day wake before 7 AM streak | AGI +5 permanent |
| Night's Sovereign | 7-day sleep before 11 PM streak | VIT +5 permanent |
| Iron Will | 7-day gym streak | STR +5 permanent |
| Code Breaker | Solve 50 DSA problems | INT +10 permanent |
| Scholar | 14-day reading streak | INT +5, PER +5 permanent |
| Musician | 8 weekend guitar sessions | CHA +10 permanent |
| Honest Hunter | Admit failure 5 times (honesty bonus) | PER +10 permanent |
| Arise! | Recover from 0-streak back to 7-day | All stats +3 permanent |
| Shadow Monarch | Reach S-Rank | Ultimate title |

## Message Templates

### Daily Quest Issue (Morning)
```
⚔️ DAILY QUEST ISSUED

[Date] | Rank: [rank] | Level: [level]

━━━━━━━━━━━━━━━━━━━━
MANDATORY QUESTS:
▸ 🏋️ Complete gym session [STR +30]
▸ 💻 Solve [N] DSA problem(s) [INT +25 each]
▸ 📖 Read for 30 minutes [INT +15]
▸ 😴 Sleep before 11:00 PM [VIT +30]

[WEEKEND BONUS]:
▸ 🎸 Guitar practice 30 min [CHA +25]
━━━━━━━━━━━━━━━━━━━━

Completion bonus: +100 XP
Streak: [N] days 🔥

The System is watching. Do not disappoint.
```

### Quest Report (Evening)
```
📊 QUEST REPORT

[Date] | Day [N]

━━━━━━━━━━━━━━━━━━━━
✅ Gym session — STR +30 [VERIFIED]
✅ DSA x2 — INT +50 [VERIFIED]  
❌ Reading — FAILED
✅ Sleep — pending verification
━━━━━━━━━━━━━━━━━━━━

XP Earned: [N]
Streak: [N] days 🔥
Level: [N] → [N]

[Motivational/harsh message based on performance]
```

### Stat Card
```
📋 HUNTER STATUS

Player: [Name]
Rank: [rank] | Level: [level]
Total XP: [N] / [next rank requirement]

━━━ STATS ━━━
STR ████████░░ [N]
INT ██████░░░░ [N]
VIT █████░░░░░ [N]
AGI ███████░░░ [N]
PER ████░░░░░░ [N]
CHA ███░░░░░░░ [N]

🔥 Streak: [N] days
🏆 Titles: [list]
⚔️ Active Dungeon: [name or none]
```
