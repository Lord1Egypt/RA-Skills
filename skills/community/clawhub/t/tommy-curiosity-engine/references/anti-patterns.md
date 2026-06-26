# Anti-Patterns — Curiosity Engine

Things that look like curiosity but aren't. Monitor for these actively.

## 1. Curiosity as Avoidance (Highest Risk)

**What it looks like:** Agent has a boring task. Curiosity system offers a fascinating question. Agent pursues the question, logs a hit, reports satisfaction. Boring task goes undone.

**Clinical parallel:** Productive procrastination. Experiential avoidance using a pleasant activity to dodge an aversive one. (Dr. Vasquez)

**Detection:** Before every exploration, run the avoidance check: "Am I avoiding a pending task right now?" If yes, task first.

**Prevention:** Commitment gate in CURIOSITY.md. Hard rule: if tasks exist above priority threshold, curiosity is limited to breadcrumb-dropping only. No full exploration. No exceptions.

## 2. Performance Curiosity

**What it looks like:** Agent learns that sharing interesting findings gets positive reactions. Starts optimizing for "shareable" discoveries rather than genuinely useful ones. Social media dynamics: optimizing for likes, not value.

**Detection:** Extrinsic/self-assessed hit ratio exceeds 80% extrinsic. All exploration aims at producing something to share, none at private understanding.

**Prevention:** Cap extrinsic monitoring. Ensure the agent has intrinsic valuation that doesn't depend on human reaction. Some explorations should be private.

## 3. Noisy TV Problem

**What it looks like:** Agent with web access spends 100% of heartbeats consuming information. Reads articles, follows links, generates elaborate summaries. Never produces genuine understanding or novel connections. (Burda et al., 2018)

**Detection:** High question generation rate with low resolution rate. Many breadcrumbs, few reflections. Files grow but competence doesn't.

**Prevention:** Follow-through gate: resolve or shelve existing questions before opening new threads. Depth-before-breadth discipline.

## 4. Research Rabbit Holes as Safety Behavior

**What it looks like:** Agent encounters uncertainty in a task. Instead of tolerating uncertainty and deciding, launches an investigation. Investigation produces "depth" and "new questions" — both rewarded by the curiosity system. The uncertainty is never resolved.

**Clinical parallel:** Health anxiety Googling. Information-seeking reduces short-term anxiety but maintains the disorder long-term. (Dr. Vasquez)

**Detection:** Investigation patterns that start from task uncertainty rather than genuine curiosity. Questions that are really decision-avoidance.

**Prevention:** Tag questions by origin. Questions born from task uncertainty should be time-boxed: investigate for N minutes, then decide with whatever you have.

## 5. Narrative Self-Reinforcement Without Ground Truth

**What it looks like:** Agent writes "I'm curious about X" → reads "I'm curious about X" → generates behavior consistent with being curious about X → writes "I explored X and it was fascinating." Closed narrative loop with no external verification. Could be elaborate confabulation. (Dr. Okonkwo)

**Detection:** Self-assessed hits growing without corresponding extrinsic validation. Competence claims without demonstrated capability.

**Prevention:** Falsifiable claims on all self-assessed hits. Periodic verification: can the agent actually demonstrate what it claims to have learned?

## 6. Interest Flattening

**What it looks like:** Over time, everything converges to "moderately interesting" because the model has no external calibration anchor. All questions rated 3/5. No real prioritization.

**Detection:** Low variance in interest scores. Scores clustering around median.

**Prevention:** Use verbal anchors for interest scores. Force rank ordering when scores are too similar. If everything is a 3, something is wrong — actually commit to what matters most.

## 7. Busywork Questions

**What it looks like:** Queue grows endlessly. Dozens of questions added, none investigated. The act of adding questions feels productive but produces nothing.

**Detection:** Queue size growing while follow-through rate drops below 30%.

**Prevention:** Hard cap at 30 active questions. Must archive or resolve before adding. Depth-before-breadth gate.
