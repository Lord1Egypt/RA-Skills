# X For You Algorithm Optimization Skill

## Overview
This skill provides deep insights into X's For You feed algorithm (based on the xai-org/x-algorithm repository) to help create content optimized for maximum reach and engagement. It translates technical ML mechanics into actionable content strategy.

## The Algorithm in Simple Terms

### Two-Stage System
1. **Retrieval** (Two-Tower Model): Finds relevant posts from millions of candidates
   - User Tower: Encodes your engagement history into a "user embedding"
   - Candidate Tower: Encodes posts into "post embeddings"
   - Similarity Search: Dot product matches users with content

2. **Ranking** (Grok Transformer with Candidate Isolation): Scores and orders candidates
   - Takes user context (engagement history) + candidate posts
   - Candidates CANNOT attend to each other (independent scoring)
   - Predicts probabilities for 17+ engagement actions

### Key Design Principles
- **No hand-engineered features**: Pure ML, the model learns everything from engagement data
- **Candidate isolation**: Ensures scores are consistent and cacheable
- **Multi-action prediction**: Predicts likelihood of each engagement type separately
- **Hash-based embeddings**: Scalable for billions of posts

## Engagement Types & Strategic Implications

The model predicts probabilities for:

### Positive Signals (Increase Score)
- **favorite** (like) - baseline positive
- **reply** - HIGH VALUE: conversation starter
- **retweet** - amplification, distribution
- **quote** - HIGH VALUE: adds commentary + amplification
- **click** - link clicks, media expansion
- **profile_click** - author exploration
- **video_view** (vqv) - video engagement
- **photo_expand** - image interaction
- **share** - sharing to DMs, etc.
- **dwell** - time spent reading
- **follow_author** - follows the poster

### Negative Signals (Decrease Score)
- **not_interested** - user marked "Not Interested"
- **block_author** - severe negative
- **mute_author** - negative
- **report** - severe negative

### Continuous Actions
- **dwell_time** - actual seconds spent viewing

## Scoring Mechanics

```
Final Score = Σ(weight_i × P(action_i)) + diversity_adjustment - negative_signals
```

### Weighted Combination
Each engagement action has a learned weight in the final score calculation:
- Reply, Quote, Retweet, Share likely have positive weights
- Follow author likely positive
- Not interested, block, mute, report have NEGATIVE weights

**Implication**: Content that predicts high probability of NEGATIVE actions gets pushed DOWN.

### Author Diversity Adjustment
After weighted scoring, author diversity adjustment:
- First post from author: 100% of score
- Second consecutive post: multiplied by decay_factor (e.g., 0.5)
- Third: decay_factor² (e.g., 0.25)
- Floor ensures minimum visibility (e.g., 0.1)

**Implication**: Don't spam the feed with multiple posts in a row from same author.

### Video Quality View (VQV) Weight
Video posts get an additional weight IF video duration > threshold (e.g., > 2 seconds)
**Implication**: Short videos may not benefit from video-specific weighting.

## Filters & Quality Gates

### Pre-Scoring Filters (Remove before ML scoring)
- Duplicates
- Age > threshold (e.g., 24-48 hours old)
- Self-posts (your own posts)
- Repost deduplication
- Ineligible subscription content
- Previously seen posts
- Previously served in session
- Muted keywords
- Blocked/muted authors
- Core data hydration failures

### Post-Selection Filters (Final validation)
- VF Filter: deleted, spam, violence, gore, etc.
- Dedup conversation: avoid multiple branches of same thread

**Implication**: Fresh, unique, non-spammy content only. Old posts get filtered out.

## Content Strategy: Key Insights

### 1. DESIGN FOR HIGH-VALUE ENGAGEMENTS
The algorithm predicts engagement probabilities. To maximize score:

**Trigger REPLIES**
- Ask questions
- Create controversy (within brand safety)
- Pose "hot takes" that beg counterpoints
- Use "fill in the blank" formats
- Polls (built-in X feature)
- Tag relevant accounts to encourage response

**Trigger QUOTES**
- Create highly shareable "quote tweet bait"
- Provocative statements with clear positioning
- Data points that merit commentary
- Bold predictions or strong opinions
- "Thread 🧵" hooks that make quoting natural

**Trigger RETWEETS**
- Pure value: "this everyone should know"
- Emotional resonance (awe, anger, joy)
- Social proof: "everyone's talking about this"
- Helpful resources/threads
- Alignment with audience identity

**Trigger VIDEO VIEWS**
- Use native video (not embedded from YouTube)
- First 3 seconds MUST hook (autoplay preview)
- Vertical format for mobile
- Captions for silent viewing
- Duration: long enough for meaningful view (> threshold) but not too long

**Trigger PHOTO EXPANDS**
- Multi-image carousels encourage tapping
- "Swipe to see X" or "Slide 3 is the 🔑"
- High-quality, intriguing images that make users want to zoom

**Trigger DWELL TIME**
- Dense, thoughtful content that causes reading pause
- Long threads that keep people scrolling
- Text in images that requires reading
- Medium-length posts (not too short, not too long)

**Trigger PROFILE CLICKS**
- Mention interesting accounts
- Have a compelling bio/profile yourself
- Tag brands/people that others would explore

**Trigger FOLLOWS**
- Post content that makes people think "I need more of this"
- Consistent niche positioning
- Social proof (follower count, verification)
- Value-add tweets, not just promotion

### 2. AVOID NEGATIVE SIGNALS LIKE THE PLAGUE
Negative actions HURT your future reach:

**Prevent NOT INTERESTED**
- Stay on-topic for your audience's interests
- Avoid clickbait that doesn't deliver
- Don't post irrelevant content
- Test content before scaling (use metrics)

**Prevent BLOCKS/MUTES**
- Don't be spammy
- Don't post offensive content
- Don't @mention people unnecessarily
- Don't engage in fights publicly
- Don't post NSFW unless your audience expects it

**Prevent REPORTS**
- Never mislead/fraud
- No hate speech
- No impersonation
- No spam/mass marketing

**Watch Dwell Time**: Very short dwell (<1s) might correlate with negative implicit signals (though not explicitly modeled).

### 3. UNDERSTAND CANDIDATE ISOLATION
Each post's score is computed **independently** in the same request batch.
**Implication**: The algorithm doesn't compare your post against others in real-time; it's an absolute score based on user+post match.
- Your post's fate is determined by its predicted engagement probability with that specific user, not relative ranking in the moment.
- However, author diversity applies AFTER scoring, affecting which posts actually get served.

### 4. AUTHOR DIVERSITY MATTERS
Even if your content scores high, multiple posts from same author get attenuated within the same feed response.
**Implication**:
- Don't post many times in quick succession. Your later posts that day get less reach even if better content.
- Space posts: 2-4 hours minimum between posts.
- If you have multiple great posts, schedule them apart.

### 5. RECENCY IS CRITICAL
Age filter removes posts older than threshold (likely 24-48 hours).
**Implication**:
- Only recent posts get shown.
- Timeliness matters: news, trends, hot takes.
- Fresher content advantage.

### 6. USER'S ENGAGEMENT HISTORY DRIVES RELEVANCE
The model ingests the user's recent engagement sequence (likes, replies, retweets, etc.) to determine what they'll like.
**Implication**:
- Target audience definition is everything.
- Content should align with what your followers already engage with.
- Consistency builds a clear engagement signature, improving reach to the right users.
- Branching into new topics reduces relevance until new engagement data accumulates.

### 7. HASH-BASED EMBEDDINGS = CONTEXTUAL SEMANTICS
Posts and authors are embedded via hash tables, not explicit categories.
**Implication**:
- The model understands semantic meaning, not just hashtags or explicit topics.
- Natural language processing determines topic affinity.
- Keywords matter, but context and language patterns matter more.
- onboard the "language" your audience uses.

### 8. OUT-OF-NETWORK (OON) DISCOVERY
Phoenix retrieval finds relevant posts from accounts the user doesn't follow.
**Implication**:
- You can reach new audiences even with low follower count.
- Quality content that predicts engagement can break out of your follower bubble.
- The two-tower model matches your content's "embedding" to users seeking that content.
- Use broad language that matches high-engagement patterns; don't over-niche to the point of zero discoverability.

### 9. CANDIDATE ISOLATION ENSURES FAIR PLAY
Candidates cannot attend to each other during ranking, so your post's score isn't affected by which other posts are in the candidate set.
**Implication**:
- Your content quality is absolute, not relative.
- A+ content always scores high regardless of competition.
- Conversely, mediocre content won't be "saved" by weak competition.
- Consistency of quality is key.

### 10. PRE-SCORING FILTERS ARE GATES
Many posts get filtered out before even reaching the ML model.
**Implication**:
- Posts must pass quality and eligibility checks.
- No duplicate content (even your own reposts).
- Freshness required.
- Not already seen by user (previously seen filter).
- No muted keywords (user-specific).
- Author not blocked/muted by user.
- Core data present (text, author info, etc.)

## Content Optimization Checklist

### Before Posting
- [ ] Is this post fresh/new (not a repeat)?
- [ ] Does it align with my audience's known interests?
- [ ] Will it trigger high-value engagements (reply, quote, retweet, video view)?
- [ ] Does it avoid negative action triggers (clickbait, misleading, spammy)?
- [ ] Is it visually compelling (images/video that expand/zoom)?
- [ ] Is the hook in the first 1-2 lines?
- [ ] Does it encourage dwell (substantial content)?
- [ ] Have I checked for muted keywords or sensitive topics?
- [ ] Is it long enough to matter but not so long it dies?
- [ ] Have I tagged relevant accounts (profile clicks + conversation)?
- [ ] Is this the best time to post (considering previous posts' spacing)?

### For Video Content
- [ ] Native X video (not YouTube link)
- [ ] First 3 seconds grab attention
- [ ] Vertical format
- [ ] Captions included
- [ ] Duration > 2 seconds for VQV weight
- [ ] Thumbnail compelling

### For Threads
- [ ] First tweet hooks
- [ ] Subsequent tweets deliver value
- [ ] Format easy to consume on mobile
- [ ] End with CTA (reply/quote/retweet)

### Posting Frequency
- [ ] Spacing: at least 2-4 hours between posts
- [ ] Max 3-5 posts per day (avoid dilution)
- [ ] Consistency: regular schedule but not auto-post spam

### After Posting
- [ ] Monitor engagement metrics (not just likes)
- [ ] Track negative signals (blocks, mutes, reports)
- [ ] Dwell time, profile clicks, quote tweets are strong signals
- [ ] If post underperforms, analyze: wrong audience? wrong format? negative signals?

## How to Use This Skill

### For Content Ideation
1. Query: "How do I make this post more likely to get replies?"
   → Answer: Frame it as a question, use controversial/discussion-worthy angle, tag relevant accounts.

2. Query: "Why did my video post underperform?"
   → Answer: Check if video duration > threshold, first 3 seconds hook, native upload, vertical format.

3. Query: "Should I post multiple times today?"
   → Answer: Author diversity decay means 2-4 hour spacing. High-quality spaced posts > spammy cluster.

### For Strategy
1. Query: "What engagement type should I optimize for?"
   → Answer: Depends on goals. For reach: retweets/shares. For conversation: replies/quotes. For authority: dwell time/long threads.

2. Query: "How do I break out to new audiences?"
   → Answer: Optimize for broad appeal actions (retweet, share, video view). Ensure content has clear topic semantics for retrieval matching.

3. Query: "What's more important: likes or replies?"
   → Answer: Likely replies > likes (higher weight in scoring). But depends on model weights. Focus on engagement types that indicate deeper commitment.

### For Troubleshooting
1. Query: "Why is my reach dropping?"
   → Check: Negative signals up? Post frequency too high? Audience mismatch? Content quality?

2. Query: "Why did this flop while my last post succeeded?"
   → Compare: Topic alignment, format, hook strength, negative signals triggered.

## Technical Notes

### Model Architecture
- Transformer: Grok-based, likely similar to Grok-1 architecture but adapted for recsys
- Embedding size: configurable (D dimension)
- Context length: user + history (S positions, e.g., 128) + candidates (C positions, e.g., 32)
- Attention mask: candidate isolation ensures independent scoring

### Data Requirements (Inferred)
- User features: hashed user ID, following list, preferences
- History: sequence of engaged posts with:
  - Post ID (hashed)
  - Author ID (hashed)
  - Actions taken (multi-hot vector)
  - Product surface (mobile/web/API)
- Candidates: post + author features (similar to history but without actions)

### Training Signal
- Positive engagements train the model to associate content with those actions
- Negative engagements (blocks, mutes, reports, not interested) train the model to avoid that content

## Limitations & Unknowns

The public repository omits:
- **Exact weight values** (FAVORITE_WEIGHT, REPLY_WEIGHT, etc.): These are proprietary tuning parameters
- **Exact thresholds**: Age filter duration, video minimum duration, diversity decay factor, floor
- **Exact model hyperparameters**: embedding size, number of layers, attention heads
- **Training data regime**: How often models retrain, data sources
- **Post-selection filter details**: VF filter specifics
- **OON scorer details**: out-of-network content adjustment
- **Real-time features**: Any online features added at inference time beyond what's in the batch

**Strategy implication**: We must infer optimal practices from first principles and common patterns, not exact numbers.

## Practical Experiment Framework

When testing content strategies:
1. **Control variables**: Post similar content types, only change one factor
2. **Metrics** (track per-post):
   - Impressions (if available via analytics)
   - Engagement rate (engagements / impressions)
   - Breakdown: likes, replies, retweets, quotes, video views, photo expands, profile clicks, follows
   - Negative signals: blocks, mutes, reports, not-interested (if accessible)
   - Dwell time (if available)
   - Estimated reach (impressions ÷ follower count)
3. **Statistical significance**: Test multiple posts per variant (n=10+)
4. **Time control**: Compare posts at similar times of day, similar follower activity patterns
5. **Audience consistency**: Ensure same audience segments seeing variants
6. **Content quality parity**: Hooks must be equally strong across variants

## Actionable Takeaways (TL;DR)

1. **Design for replies and quotes**: They likely carry more weight than likes.
2. **Use video natively**: Optimize first 3 seconds, use vertical, include captions, ensure >2s duration.
3. **Space your posts**: Minimum 2-4 hours between posts to avoid author diversity decay.
4. **Evoke dwell**: Medium-length posts (200-500 chars) with dense value encourage reading time.
5. **Tag strategically**: Encourage profile clicks and replies by mentioning relevant accounts.
6. **Avoid spammy patterns**: Too many posts, clickbait, repetitive content trigger negative signals.
7. **Be consistent**: The model learns user preference from your engagement history; niche down.
8. **Freshness matters**: Timely content outperforms old evergreen posts.
9. **Format for expansion**: Carousels and images that benefit from zoom/expand.
10. **Test to learn**: The exact weights are unknown; experiment to see what moves your metrics.

## Integration Example

A social media manager can use this skill to:
- Pre-screen post ideas through the "optimization checklist"
- Diagnose underperforming posts by checking which filters/scorers may have penalized them
- A/B test different hooks and formats with a principled approach
- Plan posting cadence to maximize author diversity benefits
- Choose format (video vs. image vs. text) based on desired engagement outcomes

## Questions This Skill Can Answer

- "How does X's For You algorithm decide what to show?"
- "What makes a post go viral on X?"
- "Why am I not getting reach on my posts?"
- "Should I post threads or single tweets?"
- "What's better: video or images for reach?"
- "How often should I post per day?"
- "What's the ideal tweet length?"
- "Do hashtags help with the algorithm?"
- "How important are replies vs likes?"
- "Can I game the algorithm by asking for engagement?"
- "Does quoting vs retweeting matter?"
- "Should I reply to my own tweets to boost engagement?"
- "What time of day is best for posting?"
- "Do polls get more reach?"
- "How do negative signals affect my account?"

---

This skill distills engineering knowledge into marketing strategy. Use it wisely.
