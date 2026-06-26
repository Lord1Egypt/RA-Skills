---
name: sentiment-monitoring
description: Use when monitoring brand sentiment on Xiaohongshu, tracking public opinion, managing reputation, responding to negative feedback, analyzing brand perception trends, or handling PR crises
---

# Sentiment Monitoring (舆情监控)

## Overview

Sentiment monitoring is the systematic tracking and analysis of brand mentions, comments, and conversations on Xiaohongshu to understand public perception, identify reputation risks early, and respond proactively to maintain positive brand image.

## When to Use

**Use when**:
- Monitoring brand health and public perception
- Tracking sentiment during marketing campaigns
- Identifying and addressing negative feedback early
- Managing PR crises or reputation issues
- Analyzing competitor sentiment and positioning
- Measuring brand sentiment changes over time
- Responding to customer complaints or concerns

**Do NOT use when**:
- Monitoring basic engagement metrics (use data-analytics)
- Tracking daily content performance (use data-analytics)
- Analyzing competitor content strategies (use competitive-analysis)

## Core Pattern

**Before** (blind to public opinion):
```
❌ "No idea what people are saying about our brand"
❌ "Negative comment goes viral before we notice"
❌ "Can't measure if our campaigns improved perception"
❌ "Reputation crisis catches us completely off guard"
```

**After** (proactive sentiment management):
```
✅ "Real-time alerts: sentiment dropped 15%, investigate immediately"
✅ "Identified negative trend emerging, addressed before crisis"
✅ "Campaign improved sentiment from 65% to 82% positive"
✅ "Comprehensive sentiment dashboard informs every decision"
```

**3-Level Monitoring Framework**:
1. **Monitoring** - Track mentions, comments, conversations in real-time
2. **Analysis** - Classify sentiment, identify themes, track trends
3. **Response** - Engage proactively, address issues, amplify positives

## Quick Reference

| Sentiment Type | Indicators | Benchmark | Response Priority |
|----------------|------------|-----------|-------------------|
| **Positive** | Praise, recommendations, love | Target >75% | Amplify, thank users |
| **Neutral** | Questions, information-seeking | 15-25% | Inform, educate |
| **Negative** | Complaints, criticism, issues | <15% | Address within 24hrs |
| **Crisis** | Viral negative, PR nightmare | <5% | Immediate response |

## Implementation

### Step 1: Set Up Monitoring Infrastructure

**Define Monitoring Scope**:
```
What to Monitor:
1. Brand Mentions
   - Official brand name and variations
   - Product names and variations
   - Hashtags associated with brand
   - Account handles and nicknames

2. Executive and Spokespeople
   - Founder, CEO, key spokespeople
   - Influencers representing brand
   - Brand ambassadors and partners

3. Product Categories
   - Category terms where brand competes
   - Generic product terms + brand
   - Competitor mentions for comparison

4. Campaign Monitoring
   - Campaign-specific hashtags and keywords
   - Campaign launch to 30 days post-end
   - Influencer campaign mentions

Monitoring Frequency:
- Real-time: Crisis situations, major campaigns
- Hourly: During active campaigns or launches
- Daily: Standard brand health monitoring
- Weekly: Competitive analysis, trend reporting
```

**Monitoring Tools Setup**:
```
Platform Native Tools:
✅ Xiaohongshu Professional Account Analytics
   - Track comment sentiment on your posts
   - Monitor mention notifications
   - Review direct messages and inquiries

✅ Native Search and Alerts
   - Save searches for brand name
   - Monitor hashtag usage
   - Track location-based mentions

Third-Party Tools:
✅ Huitun Data (灰豚数据)
   - Brand mention tracking
   - Sentiment analysis over time
   - Competitor comparison

✅ Chanmama (蝉妈妈)
   - Real-time comment monitoring
   - Influencer sentiment tracking
   - Crisis alert system

✅ Social Listening Platforms
   - Mention.com, Brandwatch, etc.
   - Cross-platform sentiment tracking
   - Automated alerts and reports

Custom Monitoring:
✅ Manual review spreadsheet
   - Daily sentiment logging
   - Issue categorization
   - Response tracking

✅ Google Alerts for web mentions
   - News articles featuring brand
   - Blog posts and reviews
   - Forum discussions
```

### Step 2: Establish Sentiment Baseline

**Measure Current Brand Sentiment**:
```
Baseline Metrics to Track:
1. Overall Sentiment Score
   - Percentage of positive vs negative mentions
   - Track over time (weekly, monthly)
   - Benchmark: >75% positive is healthy

2. Sentiment by Content Type
   - Product posts sentiment
   - Educational content sentiment
   - Promotional content sentiment
   - Personal/lifestyle content sentiment

3. Sentiment by Audience Segment
   - New followers vs long-time followers
   - Different age demographics
   - Different geographic regions

4. Sentiment Drivers
   - What topics generate positive sentiment?
   - What issues trigger negative sentiment?
   - What questions or concerns come up repeatedly?

Baseline Data Collection:
- Analyze last 30 days of comments and mentions
- Classify minimum 500 comments as positive/neutral/negative
- Identify top themes and topics
- Calculate baseline sentiment percentages
```

**Sentiment Classification Guide**:
```
Positive Indicators (友好的):
✅ Praise and compliments: "太棒了", "很喜欢", "好漂亮"
✅ Recommendations: "强烈推荐", "姐妹们快冲", "种草了"
✅ Purchase intent: "已经下单", "想要", "在哪里买"
✅ Gratitude: "谢谢分享", "学到了", "很有帮助"
✅ Emotional connection: "爱了爱了", "太心动了", "必须支持"
✅ Positive emojis: ❤️, 🔥, 👍, 😍, ✨

Neutral Indicators (中性的):
❓ Questions: "请问", "怎么", "多少钱", "哪里买"
❓ Information-seeking: "有没有", "是什么", "怎么样"
❓ Tagging friends: "@某某 看看", "@闺蜜"
❓ Factual comments: "收到", "知道了", "好的"

Negative Indicators (负面的):
⚠️ Complaints: "不好用", "踩雷", "失望"
⚠️ Criticism: "太贵了", "不推荐", "别买"
⚠️ Issues: "质量差", "客服差", "物流慢"
⚠️ Comparison: "还是XX品牌好", "不如XX"
⚠️ Skepticism: "广告吧", "像是假的", "不可信"
⚠️ Negative emojis: 👎, 😡, 😞, 💔

Crisis Indicators (危机级别):
🚨 Viral negative post with 1K+ engagements
🚨 Mass complaints about same issue
🚨 News media coverage of negative issue
🚨 Competitor or influencer attacking brand
🚨 Regulatory or legal investigation mentioned
```

### Step 3: Monitor Real-Time Sentiment

**Daily Monitoring Routine**:
```
Morning Check (9:00 AM):
1. Review overnight mentions and comments
2. Check sentiment alerts and notifications
3. Identify any negative trends or spikes
4. Flag urgent issues for immediate response

Mid-Day Check (2:00 PM):
1. Monitor campaign post performance and sentiment
2. Respond to customer inquiries and complaints
3. Track influencer post sentiment
4. Engage with positive user-generated content

Evening Check (6:00 PM):
1. Final sentiment check of day's activity
2. Log sentiment metrics for daily report
3. Plan next day's responses and engagement
4. Escalate any emerging issues to team

Weekly Review (Friday PM):
1. Analyze sentiment trends for the week
2. Compare to baseline and previous weeks
3. Identify recurring themes or issues
4. Create weekly sentiment report
5. Recommend adjustments to strategy
```

**Real-Time Alert Triggers**:
```
Set Up Automated Alerts For:
- Sentiment drops >10% in 24 hours
- Negative comment spike (>50 negative comments in 1 hour)
- Viral negative post (>500 engagements in 1 hour)
- Mass complaints about same issue
- Competitor attack or negative comparison
- News media mention of brand
- Influencer with 100K+ followers mentions negatively
- Any comment with >100 likes that's negative

Alert Escalation:
Yellow Alert (Monitor closely):
- Sentiment down 10-15%
- Cluster of negative comments (not viral)
- Single issue raised by multiple users

Orange Alert (Prepare response):
- Sentiment down 15-25%
- Negative post gaining traction (100-500 engagements)
- Influencer or media mentions issue

Red Alert (Immediate action):
- Sentiment down >25%
- Viral negative post (>500 engagements)
- PR crisis emerging
- Mass complaints or coordinated attacks
```

### Step 4: Analyze Sentiment Trends

**Trend Analysis Framework**:
```
Weekly Sentiment Report:
Week of: [Date]

Overall Sentiment:
- Positive: 78% (↑ 3% from last week)
- Neutral: 16% (↓ 2% from last week)
- Negative: 6% (↓ 1% from last week)

Key Insights:
1. Sentiment Trend: [Improving/Stable/Declining]
2. Top Positive Themes: [What people love]
3. Top Negative Themes: [What people complain about]
4. Emerging Issues: [New concerns this week]
5. Resolved Issues: [Issues that improved]

Action Items:
1. [Specific actions to take next week]
2. [Content topics to address concerns]
3. [Customer service improvements needed]
4. [Product feedback to share with team]
```

**Identify Sentiment Drivers**:
```
Positive Driver Analysis:
What generates most positive sentiment?
- Product quality and results
- Educational content value
- Authenticity and transparency
- Customer service responsiveness
- Community and engagement

Negative Driver Analysis:
What causes most negative sentiment?
- Product issues (quality, not as expected)
- Price concerns
- Shipping or delivery problems
- Customer service experience
- Misleading marketing or expectations

Gap Analysis:
- Where does reality not match expectations?
- What promises are we not delivering on?
- What competitors do better?
- What improvements would have biggest impact?
```

**Competitive Sentiment Benchmarking**:
```
Monitor Competitor Sentiment:
- What's their overall sentiment score?
- What do customers love about them?
- What do customers complain about?
- What advantages do we have in sentiment?
- What can we learn from their sentiment issues?

Positioning Opportunities:
- Competitor weakness = Our opportunity
- Address pain points competitors ignore
- Emphasize strengths where competitors are weak
- Differentiate based on sentiment gaps
```

### Step 5: Respond to Sentiment Proactively

**Positive Sentiment Amplification**:
```
Engage with Positive Mentions:
✅ Reply to positive comments: "Thank you so much! We're so happy you love it! 💕"
✅ Repost user-generated content to stories with credit
✅ Feature positive reviews in posts (with permission)
✅ Create "thank you" posts highlighting community love
✅ Surprise and delight: Send freebies to super fans
✅ Turn positive feedback into testimonials

Best Practices:
- Respond within 24-48 hours to positive comments
- Personalize responses (not generic copy-paste)
- Ask follow-up questions to deepen engagement
- Invite them to share more or tag friends
- Build relationships with brand advocates

Amplification Tactics:
- "Fan Friday" features of positive community members
- Create highlight of customer love and results
- Share testimonials in ads and marketing
- Identify and nurture potential brand ambassadors
```

**Neutral Sentiment Education**:
```
Respond to Questions and Inquiries:
✅ Provide helpful, detailed information
✅ Link to relevant posts or resources
✅ Offer personalized advice when appropriate
✅ Invite them to DM for more complex questions
✅ Follow up to ensure their needs were met

Conversion Opportunities:
- Neutral questions often indicate purchase intent
- "Where can I buy?" = Ready to purchase, make it easy
- "How does this work?" = Needs education to convert
- "Is this right for me?" = Personalized consultation opportunity

Best Practices:
- Respond promptly (within 24 hours)
- Be thorough but concise
- Include clear call-to-action
- Track conversion from question to purchase
```

**Negative Sentiment Response**:
```
Negative Comment Response Framework:
1. Acknowledge Quickly (within 24 hours, ideally 4-8 hours)
   "Hi [Name], we're so sorry to hear about your experience..."

2. Validate Their Experience
   "...we completely understand why you'd feel disappointed..."

3. Take Responsibility (even if not entirely your fault)
   "...we clearly didn't meet expectations here, and that's on us."

4. Offer Solution or Next Step
   "We'd love to make this right. Can you DM us your order details?"

5. Follow Up and Resolve
   - Address the issue privately
   - Provide refund, replacement, or solution
   - Follow up to ensure satisfaction

6. Turn Around if Possible
   - After resolving, ask if they'd reconsider
   - Many will update review or comment positively
   - Creates positive PR out of negative situation

Response Templates:
⚠️ Product Issue:
"Hi [Name], we're so sorry this didn't work for you! We stand behind our products 100%. Please DM us your order info and we'll send a replacement or full refund immediately - whichever you prefer. We want to make this right! 💕"

⚠️ Shipping/Delivery Issue:
"So sorry for the delivery delay, [Name]! That's frustrating. We're looking into your order status right now and will DM you with an update and expedited shipping on us. Thank you for your patience! 🙏"

⚠️ General Complaint:
"Thank you for sharing this feedback, [Name]. We take this seriously and want to address it. Could you DM us more details so we can understand what happened and make it right? We appreciate you bringing this to our attention. 🙏"

⚠️ Unreasonable or Troll:
(For clearly malicious or false complaints, respond once politely, then disengage)
"Hi [Name], we're sorry you feel this way. We'd love to understand more about your experience so we can improve. Please feel free to DM us with details. Wishing you the best! 😊"

Response Best Practices:
- Speed matters: Respond within 24 hours, ideally faster
- Empathy first: Validate their feelings before defending
- Take responsibility: Even if partly customer error
- Offer solutions: Don't just apologize, fix the problem
- Take it offline: DM for complex issues
- Don't argue: Public arguments never help
- Know when to disengage: Trolls won't be satisfied
```

**Crisis Response Protocol**:
```
Crisis Identification:
- Viral negative post or mass complaints
- Sentiment drops >25% rapidly
- News media or major influencer covers issue
- Coordinated attack or misinformation

Immediate Response (First Hour):
1. Assemble crisis response team
2. Verify facts and assess situation
3. Determine root cause and responsibility
4. Draft initial response statement

Initial Response (First 4 Hours):
- Acknowledge issue publicly
- Express genuine concern and empathy
- Commit to investigation and resolution
- Provide timeline for next update
- Stop all scheduled promotional content

Example Initial Crisis Post:
"Hi everyone, we're aware of the concerns about [issue] and we're taking this very seriously. We're investigating right now to understand exactly what happened. We'll provide another update by [specific time, e.g., 6 PM today]. We're committed to making this right. Thank you for your patience. 🙏"

Ongoing Crisis Management:
- Regular updates (at least daily)
- Transparency about progress
- Show action being taken, not just words
- Address questions and concerns directly
- Don't delete legitimate criticism (builds trust)

Resolution:
- Clearly explain what happened
- Take responsibility if at fault
- Detail corrective actions implemented
- Offer restitution to affected customers
- Share lessons learned and improvements

Post-Crisis:
- Monitor sentiment recovery
- Rebuild trust through consistent quality
- Document learnings to prevent recurrence
- Update crisis response playbook
```

### Step 6: Leverage Sentiment Insights

**Product Development Feedback**:
```
Identify Product Improvements:
- What features or benefits do users praise most?
- What complaints or issues come up repeatedly?
- What use cases do users discover that we didn't anticipate?
- What products do users wish we had?

Feed to Product Team:
- Weekly feedback summary from comments
- Feature request prioritization by sentiment volume
- User pain points and unmet needs
- Competitive advantages we should emphasize

Example Feedback:
"Sentiment analysis shows 87% positive feedback on our moisturizer's texture, but 23% of negative comments mention it's too heavy for oily skin. Opportunity: Create lightweight version for oily skin, or better communicate which skin types it's best for."
```

**Content Strategy Optimization**:
```
Learn What Content Resonates:
- Which topics generate highest positive sentiment?
- Which formats get most engagement and praise?
- Which educational content is most helpful and shared?
- Which promotional content is accepted vs seen as "too salesy"?

Content Adjustments:
- Double down on high-sentiment content types
- Address negative sentiment topics with educational content
- Test new content formats based on user preferences
- Personalize content for different audience segments

Example:
"Tutorial content gets 92% positive sentiment vs 65% for promotional posts. Shift content mix from 60% promotional / 40% educational to 30% promotional / 70% educational."
```

**Customer Service Improvements**:
```
Identify Service Pain Points:
- What customer service issues generate complaints?
- Where is the customer journey breaking down?
- What questions or concerns come up repeatedly?
- Which touchpoints generate negative sentiment?

Service Improvements:
- Address top 3 complaint causes systematically
- Create FAQ content for common questions
- Improve response time metrics
- Train customer service team on sentiment trends

Example:
"Sentiment shows 18% of negative comments relate to shipping delays. Partner with faster shipping provider, provide tracking updates, set realistic delivery expectations upfront."
```

**Marketing Strategy Adjustments**:
```
Optimize Based on Sentiment:
- Pause campaigns generating negative sentiment
- Double down on campaigns with positive response
- Adjust messaging based on feedback
- Target segments where brand sentiment is strongest

Brand Positioning:
- Emphasize strengths that generate positive sentiment
- Address perceived weaknesses head-on
- Differentiate from competitors based on sentiment advantages
- Rebrand if sentiment issues are fundamental to positioning

Example:
"Our authenticity and transparency drive 89% positive sentiment, but price concerns drive 34% of negative comments. Emphasize value and quality in messaging, create price-accessible product line, communicate why premium pricing is justified."
```

### Step 7: Report and Communicate Findings

**Internal Reporting**:
```
Weekly Sentiment Report:
- Overall sentiment score and trend
- Positive/negative themes and examples
- Top issues and recommendations
- Campaign performance and sentiment impact
- Competitive sentiment comparison

Monthly Executive Summary:
- Sentiment trend over 3-6 months
- Impact of marketing initiatives on sentiment
- Brand health vs competitors
- Risk assessment and recommendations
- Resource allocation for improvements

Quarterly Strategic Review:
- Long-term sentiment trends
- Correlation between sentiment and business metrics
- Major reputation risks and opportunities
- Strategic recommendations for brand positioning
- Investment priorities for sentiment improvement
```

**Cross-Functional Collaboration**:
```
Share Insights With:
Product Team:
- User feedback and feature requests
- Product improvement priorities
- New product opportunities based on unmet needs

Customer Service:
- Common complaints and response templates
- Training on emerging issues
- Feedback loop for resolved issues

Marketing Team:
- What messaging resonates vs flops
- Campaign performance and sentiment impact
- Content topics and formats that work

Executive Team:
- Brand health dashboard
- Risk assessment and early warning
- Strategic recommendations

Legal/Compliance:
- Emerging regulatory or legal concerns
- Potential liability issues from sentiment
- Crisis preparedness
```

## Common Mistakes

| Mistake | Why Happens | Fix |
|---------|-------------|-----|
| Only monitoring owned content | Easier to track | Monitor ALL brand mentions across platform |
| Ignoring negative feedback | Hope it goes away | Address promptly before it escalates |
| Responding defensively to criticism | Take it personally | Respond with empathy, take responsibility |
| Deleting negative comments | Want clean feed | Address issues transparently, builds trust |
| No sentiment baseline | Don't know where you started | Establish baseline before campaigns or changes |
| Only tracking volume, not sentiment | Easier to measure | Sentiment quality matters more than volume |
| Slow response to issues | Overwhelmed, missed alerts | Set up automated alerts, prioritize rapid response |
| Not learning from sentiment trends | Focus on day-to-day | Analyze trends for strategic insights |
| Ignoring competitor sentiment | Focus only on own brand | Monitor competitors for opportunities and threats |
| No cross-functional sharing | Siloed teams | Share insights broadly across organization |

## Real-World Impact

**Case Study: Sentiment Monitoring Averts Crisis**

A beauty brand's sentiment monitoring detected an emerging issue with a new product batch.

**Detection**:
- Alert triggered: 50+ negative comments in 1 hour about skin irritation
- Comments clustered around batch #XYZ123
- Sentiment dropped from 82% to 61% in 3 hours

**Immediate Response**:
- Issued statement within 2 hours acknowledging issue
- Paused all sales of affected batch immediately
- Offered full refunds to affected customers
- Launched investigation with manufacturing partner

**Resolution**:
- Identified quality control issue in manufacturing
- Recalled affected batch (reduced impact to 200 customers vs potential 2,000+)
- Implemented new quality control procedures
- Communicated transparently throughout process

**Outcome**:
- Sentiment recovered to 79% within 2 weeks
- Customers praised transparent handling
- Many affected customers became loyal advocates
- Prevented viral crisis that could have damaged brand permanently

**Data-Backed Insights**:
- Brands that respond to negative sentiment within 24 hours see 40% higher customer retention
- Addressing issues transparently improves sentiment more than ignoring them
- 70% of customers who have complaints resolved satisfactorily become repeat customers
- Sentiment monitoring reduces crisis impact by 60-80% through early detection
- Proactive sentiment management improves brand health scores by 25-35% over 6 months
- Brands with strong sentiment monitoring grow 2-3x faster than those without

## Related Skills

**REQUIRED**: Use data-analytics (analyze sentiment data quantitatively)
**REQUIRED**: Use community-management (engage based on sentiment insights)
**REQUIRED**: Use customer-service (resolve issues identified through monitoring)

**Recommended for comprehensive monitoring**:
- **social-listening** - Advanced social listening techniques
- **crisis-management** - Handle PR crises and reputation issues
- **customer-feedback** - Systematically collect and analyze feedback
- **competitive-intelligence** - Monitor competitor sentiment and strategies
- **brand-reputation-management** - Proactive reputation protection and building
