# AI Quality Review Template

## Review Target
- Episode Number: Episode {episode_number}
- Pipeline ID: {pipeline_id}
- Generated At: {timestamp}

---

## Review Dimensions

### 1. Plot Coherence (Weight 25%)
**Scoring Criteria:**
- 9-10: Perfect connection with previous episode, plot progresses naturally and smoothly
- 7-8: Good connection with minor areas for optimization
- 5-6: Average connection with noticeable transition issues
- 0-4: Abrupt connection, plot discontinuity

**Comment:** {coherence_comment}

---

### 2. Character Consistency (Weight 20%)
**Scoring Criteria:**
- 9-10: Character behavior fully matches established traits, development is reasonable
- 7-8: Mostly matches traits with minor deviations
- 5-6: Some behaviors inconsistent with established traits
- 0-4: Character behavior severely deviates from established traits

**Comment:** {character_comment}

---

### 3. Hook Handling (Weight 20%)
**Scoring Criteria:**
- 9-10: Hooks handled cleverly, both continuing and innovative
- 7-8: Hooks handled reasonably, meets expectations
- 5-6: Hook handling flat or slightly problematic
- 0-4: Hooks handled poorly, confusing logic

**Comment:** {hook_comment}

---

### 4. Pacing Control (Weight 15%)
**Scoring Criteria:**
- 9-10: Perfect pacing with good tension and relaxation, engaging
- 7-8: Good pacing with occasional minor issues
- 5-6: Average pacing with dragging or rushing
- 0-4: Pacing out of control

**Comment:** {pacing_comment}

---

### 5. Emotional Curve (Weight 10%)
**Scoring Criteria:**
- 9-10: Rich emotions, strong appeal, reasonable emotional ups and downs
- 7-8: Good emotional expression
- 5-6: Average emotional expression
- 0-4: Insufficient or overly forced emotional expression

**Comment:** {emotion_comment}

---

### 6. Innovation (Weight 10%)
**Scoring Criteria:**
- 9-10: Novel and unique, surprising
- 7-8: Has some novelty
- 5-6: Conventional
- 0-4: Clichéd and dull

**Comment:** {innovation_comment}

---

## Review Results

| Dimension | Score | Weight | Weighted Score |
|-----------|-------|--------|----------------|
| Plot Coherence | {coherence_score} | 25% | {coherence_weighted} |
| Character Consistency | {character_score} | 20% | {character_weighted} |
| Hook Handling | {hook_score} | 20% | {hook_weighted} |
| Pacing Control | {pacing_score} | 15% | {pacing_weighted} |
| Emotional Curve | {emotion_score} | 10% | {emotion_weighted} |
| Innovation | {innovation_score} | 10% | {innovation_weighted} |
| **Total Score** | - | - | **{total_score}** |

---

## Review Conclusion

**Status:** {status} (Score {total_score}/10)

**Summary:** {summary}

**Improvement Suggestions:**
{suggestions}

---

## Processing Recommendation

- ✅ Score ≥ 7: PASSED, proceed to human confirmation
- ❌ Score < 7: FAILED, regenerate required