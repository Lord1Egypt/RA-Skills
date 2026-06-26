# Gamification Loops

## Patterns


---
  #### **Name**
Core Loop Design
  #### **Description**
The fundamental engagement cycle
  #### **When To Use**
Designing any gamification system
  #### **Implementation**
    ## Core Loop Framework
    
    ### 1. The Engagement Loop
    
    ```
         ┌─────────────┐
         │   TRIGGER   │ (Internal or external)
         └──────┬──────┘
                │
                ▼
         ┌─────────────┐
         │   ACTION    │ (User does something)
         └──────┬──────┘
                │
                ▼
         ┌─────────────┐
         │   REWARD    │ (Variable is best)
         └──────┬──────┘
                │
                ▼
         ┌─────────────┐
         │ INVESTMENT  │ (User puts in effort)
         └──────┬──────┘
                │
                └──────────────────────┐
                                       │
                       ┌───────────────▼───────────────┐
                       │ Creates value, loads trigger  │
                       └───────────────────────────────┘
    ```
    
    ### 2. Loop Types
    
    | Loop Type | Frequency | Example |
    |-----------|-----------|---------|
    | Session | Minutes | Complete level |
    | Daily | Daily | Login bonus, streaks |
    | Weekly | Weekly | Weekly challenge |
    | Long-term | Months | Mastery progression |
    
    ### 3. Trigger Design
    
    | Trigger Type | Description | Example |
    |--------------|-------------|---------|
    | External | Push/notification | "You have 3 new rewards" |
    | Internal | User's own thought | "I wonder if I leveled up" |
    | Scheduled | Time-based | Daily reset |
    | Social | Friend activity | "Alex just passed you" |
    
    ### 4. Healthy Loop Criteria
    
    ```
    Check each loop:
    
    □ Does action have intrinsic value?
    □ Does user benefit beyond the reward?
    □ Can user disengage without penalty?
    □ Is frequency sustainable?
    □ Does it respect user's time?
    ```
    

---
  #### **Name**
Progress Systems
  #### **Description**
Making advancement visible and satisfying
  #### **When To Use**
Showing user progress
  #### **Implementation**
    ## Progress Design
    
    ### 1. Progress Types
    
    | Type | Best For | Pitfall |
    |------|----------|---------|
    | Linear | Clear skill building | Can feel grinding |
    | Branching | Multiple paths | Overwhelming |
    | Emergent | Skill discovery | Hard to track |
    | Social | Competition | Demotivating |
    
    ### 2. Progress Bar Psychology
    
    ```
    Progress bar principles:
    
    1. ENDOWED PROGRESS
       Start at 20%, not 0%
       "You're already on your way!"
    
    2. NEAR-COMPLETION
       Last 10% feels longest
       Add encouragement
    
    3. VARIABLE PACING
       Early wins = fast progress
       Later = meaningful progress
    
    4. VISUAL SATISFACTION
       Filling animation
       Celebratory completion
    ```
    
    ### 3. Level System Design
    
    | Curve Type | Experience | Use Case |
    |------------|------------|----------|
    | Linear | Same per level | Short progression |
    | Exponential | Increasing | Long progression |
    | S-curve | Slow-fast-slow | Natural mastery |
    
    ### 4. Milestone Moments
    
    ```
    Design milestones that:
    
    - Mark meaningful progress
    - Unlock new capabilities
    - Celebrate achievement
    - Create share moments
    - Set new goals
    ```
    

---
  #### **Name**
Reward Systems
  #### **Description**
What users get and when
  #### **When To Use**
Designing reward mechanics
  #### **Implementation**
    ## Reward Design
    
    ### 1. Reward Types
    
    | Type | Motivation | Sustainability |
    |------|------------|----------------|
    | Intrinsic | Internal satisfaction | High |
    | Extrinsic | External validation | Lower |
    | Social | Status/recognition | Medium |
    | Tangible | Real-world value | Low |
    
    ### 2. Variable Reward Schedule
    
    ```
    Fixed rewards get boring.
    Variable rewards create anticipation.
    
    VARIABLE RATIO
    Reward after variable # of actions
    Most engaging, most addictive
    
    VARIABLE INTERVAL
    Reward after variable time
    Keeps checking behavior
    
    FIXED RATIO
    Reward after X actions
    Predictable, less engaging
    
    FIXED INTERVAL
    Reward at set times
    Least engaging
    ```
    
    ### 3. Reward Calibration
    
    | Effort Required | Reward Size |
    |-----------------|-------------|
    | Low | Small, frequent |
    | Medium | Medium, regular |
    | High | Large, rare |
    | Very high | Unique, legendary |
    
    ### 4. The Reward Decay Problem
    
    ```
    Rewards lose impact over time.
    
    Solutions:
    - Evolving rewards (new types)
    - Increasing stakes (rarity)
    - Social layer (showing off)
    - Real utility (actual value)
    ```
    

---
  #### **Name**
Streak Mechanics
  #### **Description**
Building habits through consistency
  #### **When To Use**
Encouraging daily engagement
  #### **Implementation**
    ## Streak Design
    
    ### 1. Streak Psychology
    
    ```
    Why streaks work:
    
    LOSS AVERSION
    - Losing streak hurts more than gaining
    - Creates commitment
    
    SUNK COST
    - "I've come this far"
    - Increases investment
    
    IDENTITY
    - "I'm a person who..."
    - Self-image reinforcement
    ```
    
    ### 2. Streak Protection
    
    | Protection Type | When | Trade-off |
    |-----------------|------|-----------|
    | Freeze | User requests | Preserves value |
    | Grace period | Auto-applied | Forgiveness |
    | Repair | After break | Second chance |
    | Weekend pause | Scheduled | Life-friendly |
    
    ### 3. Healthy Streak Design
    
    ```
    Ethical streak patterns:
    
    DO:
    - Allow freezes
    - Weekend flexibility
    - Reasonable daily ask
    - Clear value to user
    
    DON'T:
    - Punish harshly
    - Require excessive time
    - Make life suffer
    - Create anxiety
    ```
    
    ### 4. Beyond Daily Streaks
    
    | Streak Type | Use Case |
    |-------------|----------|
    | Daily | Habit building |
    | Weekly | Sustainable goals |
    | Monthly | Long-term tracking |
    | Action-based | Behavior chains |
    

## Anti-Patterns


---
  #### **Name**
Dark Pattern Gamification
  #### **Description**
Manipulation disguised as engagement
  #### **Why Bad**
    Erodes trust.
    Regulatory risk.
    User resentment.
    
  #### **What To Do Instead**
    Ask if user benefits.
    Allow disengagement.
    Transparent mechanics.
    

---
  #### **Name**
Overjustification
  #### **Description**
External rewards killing intrinsic motivation
  #### **Why Bad**
    Users stop enjoying activity.
    Only do for reward.
    Engagement drops when rewards stop.
    
  #### **What To Do Instead**
    Enhance, don't replace motivation.
    Focus on mastery and autonomy.
    Use informational, not controlling rewards.
    

---
  #### **Name**
Demotivating Leaderboards
  #### **Description**
Competition that discourages majority
  #### **Why Bad**
    Top 10% motivated.
    Bottom 90% demotivated.
    Many give up entirely.
    
  #### **What To Do Instead**
    Personal bests.
    Cohort competition.
    Progress-based rankings.
    