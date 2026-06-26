---
name: self-improving-life
description: "Holistic life satisfaction and balance optimization across health, relationships, work, finances, learning, leisure, and personal growth. Use for life audit, life wheel review, burnout prevention, routine reset, quarterly reflection, habit alignment, and systematic self-improvement."
version: v1.0.0
tags: life-balance, self-improvement, holistic-wellness
---

# Self-Improving Life

## Usage Scenarios

### Scenario 1: Quick Life Balance Check
**User input:** "I feel unbalanced lately — give me a quick life check"
**Expected output:** A 5-minute triage output: asks for current satisfaction scores across domains, identifies the most neglected area and one likely root cause, and provides a single 7-day experiment to address the biggest gap.

### Scenario 2: Monthly Life Wheel Review
**User input:** "Help me with my monthly life review"
**Expected output:** A full life wheel assessment including domain scores (1-10) for health, relationships, work, finances, growth, leisure; time allocation vs satisfaction analysis; critical insights; and specific adjustments for the next month.

### Scenario 3: Plan for a Major Life Transition
**User input:** "I'm starting a new job next month — help me plan the transition"
**Expected output:** A life transition plan with before/desired state comparison, phased transition schedule (month 1-12), impact analysis on each life domain, success metrics, and catch-up plans for domains likely to suffer during the transition.

Comprehensive life optimization system that tracks satisfaction across key domains, identifies imbalances, and provides evidence-based adjustments for greater fulfillment and balance.
### Scenario 4: 觉得自己在混日子想改变
**User input:** "每天上班摸鱼下班刷剧，年初定的目标基本没动，年底了发现自己还是原地踏步，好sad。"
**Expected output:** 提供'微改变'启动计划：1）从最小行动开始——每天做一件'对未来的自己有用'的事（哪怕只有5分钟）；2）重新审视年初目标：砍掉'假大空'的目标，保留1个最重要最可行的小目标；3）设置'不做就罚款'的承诺机制（在朋友圈立flag，或者把钱交给朋友代管）；4）推荐中国本土的积极心理学书籍（《心流》《被讨厌的勇气》《终身成长》）。核心建议：不要追求完美，先完成再谈优化。

## Best Use Cases

- Monthly or quarterly life wheel review
- Feeling unbalanced, stuck, burned out, or over-optimized for work
- Resetting routines after a move, new job, breakup, illness, or family change
- Comparing health, relationships, work, money, learning, and leisure trade-offs
- Turning vague dissatisfaction into one measurable next experiment
- Aligning habits and goals with the life domain that most needs attention

## Quick Start

Ask the user for:

1. Current overall life satisfaction from 1-10
2. Scores for health, relationships, work, finances, growth, and leisure
3. The domain that feels most neglected
4. One constraint that cannot change this month

Then return a concise life-balance diagnosis, one likely root cause, and a 7-day experiment. Avoid overwhelming the user with a full monthly template unless they ask for a deep audit.

## Output Modes

- `quick_check`: 5-minute triage with one next action
- `monthly_review`: full life wheel assessment and trend notes
- `transition_plan`: reset plan for a major life change
- `routine_rebalance`: weekly schedule and habit adjustment
- `reflection`: gentle review when the user feels stuck but unclear

## Privacy Note

This skill may involve sensitive health, relationship, work, and finance reflections. Keep details minimal unless the user wants to record them, and remind the user when a log will be stored locally.

## Quick Reference

| Situation | Action |
|-----------|--------|
| Feeling overwhelmed or unbalanced | Complete life wheel assessment, identify lowest-scoring areas |
| Major life transition (new job, move, relationship) | Update life priorities, adjust time allocation |
| Quarterly/annual review | Comprehensive life audit, set new goals |
| Daily mood tracking | Log energy, mood, satisfaction scores |
| Comparing life satisfaction over time | Generate trend reports, identify improvement patterns |

## Life Domains & Metrics

### Health & Wellness (20-25% ideal allocation)
- **Physical**: Sleep quality, exercise frequency, nutrition score
- **Mental**: Stress level, mindfulness practice, emotional balance
- **Energy**: Daily energy score, fatigue patterns, recovery quality

### Relationships & Social (15-20% ideal allocation)  
- **Intimate**: Connection quality, communication, shared experiences
- **Family**: Contact frequency, support exchange, harmony level
- **Friends**: Social engagement, meaningful conversations, support network
- **Community**: Contribution level, belongingness, social impact

### Work & Career (20-25% ideal allocation)
- **Engagement**: Interest level, challenge balance, flow states
- **Growth**: Skill development, responsibility increase, recognition
- **Impact**: Contribution value, alignment with values, legacy building
- **Balance**: Work-life boundaries, stress management, recovery time

### Finances & Security (10-15% ideal allocation)
- **Stability**: Emergency fund, debt level, income consistency
- **Growth**: Savings rate, investment performance, net worth trend
- **Freedom**: Financial independence progress, optionality, stress level
- **Generosity**: Giving amount, impact, alignment with values

### Personal Growth & Learning (10-15% ideal allocation)
- **Knowledge**: Learning hours, skill acquisition, curiosity satisfaction
- **Creativity**: Creative expression, problem-solving, innovation
- **Values**: Living in alignment, integrity, purpose pursuit
- **Legacy**: Contribution to others, teaching, mentoring

### Leisure & Enjoyment (10-15% ideal allocation)
- **Play**: Fun activities, spontaneity, joy moments
- **Rest**: Quality downtime, relaxation, digital detox
- **Adventure**: Novel experiences, travel, exploration
- **Beauty**: Art appreciation, nature connection, aesthetic experiences

## Logging Format

### Life Wheel Assessment (Monthly)
Append to `.learnings/life/MONTHLY_ASSESSMENTS.md`:

```markdown
## [LFA-YYYYMM-001] Life Wheel Assessment - March 2026

**Assessed**: 2026-03-31T20:00:00Z
**Overall Satisfaction**: 6.8/10
**Domain Balance Score**: 68% (ideal: 85%+)

### Domain Scores (1-10)
1. **Health & Wellness**: 7.5/10 ↑ (Last: 7.0)
   - Sleep: 8/10 (7.5 avg hours)
   - Exercise: 6/10 (3x/week, inconsistent)
   - Nutrition: 8/10 (home-cooked 80%)
   
2. **Relationships & Social**: 6.0/10 ↓ (Last: 6.5)
   - Intimate: 7/10 (quality time decreased)
   - Friends: 5/10 (only 2 social outings)
   - Family: 6/10 (weekly calls, good)
   
3. **Work & Career**: 8.0/10 → (Last: 8.0)
   - Engagement: 9/10 (challenging projects)
   - Growth: 7/10 (learning slowing)
   - Balance: 8/10 (good boundaries)
   
4. **Finances & Security**: 7.0/10 ↑ (Last: 6.5)
   - Stability: 8/10 (emergency fund complete)
   - Growth: 6/10 (savings rate 15%)
   
5. **Personal Growth**: 5.5/10 ↓ (Last: 6.0)
   - Learning: 4/10 (only 2 hours/week)
   - Creativity: 7/10 (weekend painting)
   
6. **Leisure & Enjoyment**: 6.5/10 → (Last: 6.5)
   - Play: 5/10 (too much screen time)
   - Rest: 8/10 (good weekend recovery)

### Time Allocation vs. Satisfaction
| Domain | Time Spent | Satisfaction | Gap |
|--------|------------|--------------|-----|
| Health | 22% | 7.5/10 | +0.5 |
| Relationships | 12% | 6.0/10 | -1.0 ⚠️ |
| Work | 35% | 8.0/10 | +1.5 |
| Finances | 8% | 7.0/10 | -0.5 |
| Growth | 5% | 5.5/10 | -2.0 ⚠️ |
| Leisure | 18% | 6.5/10 | -0.5 |

### Critical Insights
1. **Major Imbalance**: Spending 35% time on work (satisfaction 8/10) vs 5% on growth (satisfaction 5.5/10)
2. **Relationship Deficit**: 12% time allocation for 6.0 satisfaction - needs attention
3. **Leisure Quality**: 18% time but low satisfaction - screen time reducing quality

### Adjustments for Next Month
1. **Reduce Work**: From 35% to 30% (delegate, streamline)
2. **Increase Growth**: From 5% to 10% (schedule learning blocks)
3. **Improve Relationships**: From 12% to 15% (plan 2 social events)
4. **Enhance Leisure**: Replace 2 hours screen time with active leisure

### Progress Since Last Assessment
- Health improved from 7.0 to 7.5 (better sleep routine)
- Finances improved from 6.5 to 7.0 (emergency fund complete)
- Relationships declined from 6.5 to 6.0 (social isolation)
- Overall: +0.3 points (moderate improvement)

---
```

### Daily Life Log (Optional, for detailed tracking)
Append to `.learnings/life/DAILY_LOGS.md`:

```markdown
## [DLL-YYYYMMDD] Daily Log - 2026-03-12

**Logged**: 2026-03-12T21:00:00Z
**Overall Day Rating**: 7/10
**Energy Level**: 6/10 (morning: 8, evening: 4)
**Mood Trend**: Steady, slight afternoon dip

### Key Moments
- **Morning**: Productive work session, completed project milestone
- **Afternoon**: Team meeting ran long, felt drained
- **Evening**: Quality time with partner, cooked dinner together
- **Night**: Watched movie, but mind still on work

### Domain Experiences
1. **Health**: 7/10 - Good sleep, missed workout, healthy meals
2. **Relationships**: 8/10 - Good connection with partner
3. **Work**: 8/10 - Productive, but meeting fatigue
4. **Growth**: 4/10 - No learning time
5. **Leisure**: 6/10 - Passive entertainment

### Insights & Patterns
- Afternoon meetings consistently drain energy
- Evenings with partner boost satisfaction significantly  
- Work productivity high but crowding out growth time

### Tomorrow's Intention
- Block afternoon for focused work, not meetings
- Schedule 30-minute learning before dinner
- Plan active leisure (walk, game) instead of TV

---
```

### Life Transition Log (for major changes)
Append to `.learnings/life/TRANSITIONS.md`:

```markdown
## [TRN-YYYYMMDD-001] Career Change - Software to Management

**Transition Start**: 2026-03-01
**Expected Duration**: 6-12 months
**Priority**: high
**Status**: in_progress

### Before State (Software Engineer)
- Satisfaction: 7.5/10 (technical depth but limited impact)
- Time allocation: 40% coding, 20% meetings, 40% learning
- Growth trajectory: Technical expert path
- Values alignment: 70% (enjoys creation, misses leadership)

### Desired State (Engineering Manager)
- Target satisfaction: 8.5/10 (people leadership + technical)
- Time allocation: 30% people, 30% strategy, 20% technical, 20% growth
- Growth trajectory: Leadership track
- Values alignment: 90% (creation through others, mentorship)

### Transition Plan
1. **Month 1-2**: Take on mentoring responsibilities (current)
2. **Month 3-4**: Lead small project team
3. **Month 5-6**: Formal management training
4. **Month 7-9**: Transition to manager role
5. **Month 10-12**: Establish in new role

### Impact on Other Domains
- **Health**: May decrease initially (stress), need proactive management
- **Relationships**: More evening work possible, set boundaries
- **Finances**: Potential increase long-term, stable short-term
- **Growth**: High learning curve, good alignment
- **Leisure**: Protect weekends, schedule recovery

### Success Metrics
- Team satisfaction scores > 4/5
- Project delivery on time 90%+
- Personal energy > 6/10 average
- Management skill assessment > 80%

---
```

## Analysis Framework

### Life Balance Algorithm
```
Balance Score = 100% - Σ|Time% - Ideal%| / 2
Satisfaction-Adjusted Score = Σ(Satisfaction × Time%) / Total Time
```

### Imbalance Detection
- **Warning**: Any domain satisfaction < 5/10
- **Critical**: Satisfaction gap > 3 points between highest/lowest domains  
- **Time-Satisfaction Mismatch**: High time + low satisfaction = urgent change needed

### Trend Analysis
- **Positive Momentum**: 3+ consecutive months of improvement in any domain
- **Negative Spiral**: 2+ domains declining for 2+ months
- **Stagnation**: No domain change > 0.5 points for 3+ months

## Improvement Strategies

### For Time Allocation Problems
1. **Time Audit**: Track actual time for 1 week
2. **Ideal Week Design**: Create template balancing all domains
3. **Gradual Shifts**: Change 5% allocation per week, not 20% at once
4. **Protection Rituals**: Guard time for low-satisfaction high-importance domains

### For Satisfaction Deficits
1. **Root Cause Analysis**: Is it time quantity or quality?
2. **Experimentation**: Try 3 different approaches for 2 weeks each
3. **Minimum Effective Dose**: Find smallest change that moves satisfaction 1 point
4. **Peer Benchmarking**: How do satisfied people in this domain spend time?

### For Life Transitions
1. **Phased Approach**: 3-month pilot before full commitment
2. **Safety Nets**: Maintain aspects of old life during transition
3. **Support Systems**: Identify who/what helps in each domain
4. **Exit Criteria**: Know when to persist vs. when to pivot

## Integration with Other Skills

### With Self-Improving-Habit
- Build habits supporting balanced life (exercise, meditation, social)
- Use habit streaks to reinforce domain priorities

### With Self-Improving-Work
- Ensure work domain enhances, doesn't dominate life
- Connect career growth to overall life satisfaction

### With Self-Improving-Skill
- Align skill development with life priorities
- Balance mastery pursuits with other domains

## Common Life Patterns & Solutions

### Pattern 1: "Work Martyr"
- **Symptoms**: Work > 40%, other domains < 5%, burnout cycles
- **Root Cause**: Identity tied to productivity, fear of inadequacy
- **Solution**: Redefine success, schedule non-work first, find other identity sources

### Pattern 2: "Relationship Desert"
- **Symptoms**: Social satisfaction < 5/10, loneliness, superficial connections
- **Root Cause**: Mobility, career focus, social anxiety
- **Solution**: Schedule social time, join interest groups, deepen existing connections

### Pattern 3: "Growth Stagnation"  
- **Symptoms**: Learning satisfaction < 5/10, boredom, feeling stuck
- **Root Cause**: Comfort zone, lack of challenge, no learning system
- **Solution**: Learning plan, accountability group, skill diversification

### Pattern 4: "Leisure Guilt"
- **Symptoms**: Can't relax, always "productive", leisure dissatisfaction
- **Root Cause**: Puritan work ethic, performance identity
- **Solution**: Permission to rest, scheduled guilt-free leisure, redefine productivity

## Success Metrics

### Leading Indicators (Weekly)
- Domain time allocation vs. target
- Daily satisfaction scores (1-3 domains)
- Energy level trends
- Balance ritual consistency

### Lagging Indicators (Monthly)
- Life wheel assessment scores
- Domain satisfaction changes
- Time allocation alignment
- Overall life satisfaction trend

### Ideal Targets
- **Balance Score**: > 85% (time aligns with priorities)
- **Minimum Satisfaction**: All domains > 6/10
- **Maximum Gap**: No domain difference > 3 points
- **Trend**: 0.5+ point improvement in lowest domain each quarter

## Getting Started

### Step 1: Initial Assessment (Week 1)
1. Complete first life wheel assessment
2. Track time for 3 typical days
3. Identify biggest gap (time vs. satisfaction)

### Step 2: Design Ideal Week (Week 2)
1. Create template allocating time to all domains
2. Start with current allocation + 5% adjustment toward ideal
3. Schedule non-negotiable time for lowest satisfaction domain

### Step 3: Continuous Optimization (Ongoing)
1. Monthly life wheel assessment
2. Quarterly major review and recalibration
3. Annual life vision update

## Philosophical Foundation

Based on:
- **Aristotle's Eudaimonia**: Flourishing through virtue and balance
- **Maslow's Hierarchy**: Addressing needs across levels
- **Positive Psychology**: Focusing on what enables thriving
- **Stoicism**: Focusing on what you control, accepting the rest

**Integration Note**: This skill provides the holistic context for other self-improving skills, ensuring skill development serves overall life satisfaction rather than becoming an end in itself.
