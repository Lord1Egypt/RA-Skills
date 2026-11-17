# Verify Conclusion · 陷阱 1–10（原文）

> 本文件由 `SKILL.md` 按需引用；条目文字与拆分前逐字节一致。

### ① Temporal correlation mistaken for causation

**Pattern:** "After upgrading X, Y broke" → declared as root cause without testing rollback or finding mechanism.

**Fix:** Before declaring causation, isolate: can you reproduce the fault with X at the old version? If not, the statement must be labeled "unverified inference (temporal correlation only)".

### ② Stopping at the first plausible explanation

**Pattern:** Found "Gateway write-lock timeout" → declared root cause. The real cause (journal corruption → I/O storm) was two layers upstream and never investigated.

**Fix:** After every diagnostic conclusion, ask: "What caused this condition?" Repeat until hitting system boundary or known factor.

### ③ Unverifiable diagnostic assertions

**Pattern:** "System is healthy," "Problem resolved," "Everything normal" with no specific evidence.

**Fix:** Every diagnostic claim must be answerable with "What command verifies this?" If no single command can verify it, either break it into verifiable sub-claims or label it "speculation".

**Same burden for soothing negative guarantees.** "These few calls won't make anything worse", "this can't touch production", "nothing else reads that file" are claims, not courtesies. The *absence* of a side effect needs the same evidence as its presence: name the mechanism that would have produced it (rate accounting, cooldown state, lock ownership, reader list) or say "未验证". A reassurance the user then acts on converts your guess into their decision — and the later contradicting observation reads as a broken promise instead of a normal unknown, which costs more trust than admitting the gap up front.

### ④ Reflexive attribution to recent changes

**Pattern:** Any recent config change, upgrade, or modification is reflexively blamed for any new symptom. The upgrade WAS the most recent change, but that doesn't make it the cause.

**Fix:** List at least one alternative explanation that does NOT involve the recent change. Attempt to falsify it.

### ⑤ Intermediate state reported as final conclusion

**Pattern:** A session_search DISCOVERY result shows "X is pending" in the middle of a session, but the same session's bookend_end resolved it. Agent reports the pending state without checking the end.

**Fix:** After any lookup (especially session_search), always check whether the same source later updated or invalidated the finding.

### ⑥ Apologize first, investigate later

**Pattern:** User challenges agent → agent says "you're right" → then investigates → discovers user was wrong too.

**Fix:** When challenged, locate the original evidence first. Respond with the evidence. Decide who was right based on the evidence, not social dynamics.

### ⑦ Agent forgets to auto-trigger verification

**Pattern:** Agent produces diagnostic conclusions → moves on to the next task without loading this skill. Only applies it when user explicitly asks `你验证了吗？` or `这个结论你用verify-conclusion了吗？`.

**Fix:** After producing ANY conclusion that matches the trigger criteria, immediately ask: "Did I just produce a diagnostic conclusion?" If yes, this skill MUST be loaded before moving on. User prompts like "did you verify?" ARE legitimate triggers — do not treat them as optional.

### ⑧ Testing with fake credentials produces false results

**Pattern:** When testing an API-dependent service, using a fake key (e.g. "sk-test") can cause completely different behavior — timeouts, slow startup, different error paths — compared to the real key. Agent concludes "service X is slow" when the real issue is the fake key triggering a different code path.

**Fix:** Always test with the REAL credentials when available. If using fake credentials is unavoidable, explicitly state "this behavior may differ with real credentials" and do not draw performance/timing conclusions from fake-key tests.

### ⑨ Diagnosis complete but fix blocked — verification stopped too early

**Pattern:** Agent validates every link in the causal chain → declares diagnosis confirmed → user asks to apply fix → fix fails immediately because the repair path was never tested (e.g., ALTER TABLE hits data corruption, restart doesn't actually clear the problem).

**Fix:** After Step 2 confirms the causal chain, Step 1's completeness check MUST include a lightweight fix feasibility test before the diagnosis is considered "complete." A diagnosis whose repair is blocked is a partial diagnosis.

**Real case (2026-07-23):** Agent diagnosed ClickHouse system table TTL missing → verified all causal links → user approved fix → ALTER TABLE failed with CHECKSUM_DOESNT_MATCH (data corruption from HDD + unclean shutdowns). The diagnosis was logically sound but practically incomplete because the repair path wasn't validated.

### ⑩ User asks to run the SKILL check = execute the full Step 1 + Step 2

**Pattern:** The user says "run the SKILL check once" (`用SKILL检查一次`) → the agent loads the skill and does a quick confirmation (one paragraph: "verified, both passes agree") → the user immediately says "run the skill check **one more time**" (`用skill检查一遍`) — meaning the first attempt was not enough.

**Root cause:** The agent reads "check with the SKILL" as "cite the skill for a quick confirmation", while the user expects the **full Step 1 + Step 2 — the item-by-item classification table and the blind re-derivation process**. Users can tell "verbal confirmation" apart from "actually running the process".

**Fix:** When the user says "`用SKILL检查`", the output MUST be complete:
1. Step 1 — item-by-item classification (Fact/Assumption/Inference) + physical evidence + falsifiability test
2. Step 2 — blind collection of evidence from scratch (not referencing the first pass) → independent derivation → comparison
3. An explicit statement that "both passes agree ✅" or the points of divergence

**Fix:** In a diagnostic context, hearing "`用SKILL检查`" / "`用skill验证`" means: load verify-conclusion first and execute the complete Step 1 + Step 2. Only afterwards consider whether a domain skill is needed to verify the cited facts.

