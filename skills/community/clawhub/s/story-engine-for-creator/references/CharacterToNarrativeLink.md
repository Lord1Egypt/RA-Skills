# Character → Narrative Link (P0 upgrade, v2.0)

Character consistency (visual) and narrative consistency (plot) are the same
problem at different layers. This module bridges the AI Drawing Composition
Template's character anchors into the story engine's causal chain, so a character
that looks stable also *behaves* stable.

## Bridge contract

| Layer | Source (Drawing Template) | Target (Story Engine) |
|---|---|---|
| Identity | CharacterAnchors.csv core identity anchor (≥1.6) | Character immutable facts (never violated) |
| Temperament | CharacterAnchors.csv temperament tag (≥1.3) | Behavior constraint set per scene |
| Emotional range | EmotionBehaviorMap (anthropomorphic engine) | Scene emotion budget (what the character may feel) |
| Props / wardrobe | Signature props + FeatureDetails | Item continuity checklist (no vanishing props) |
| Voice | (add to CharacterAnchors: speech style) | Dialogue style guard |

## Sync procedure (per character version)

1. In the Drawing Template, complete the CharacterAnchors row (identity,
   temperament, palette, props, negative anchoring).
2. Copy the **immutable facts** into the story engine's character record:
   `characters/<id>.md` with `immutable: []` list.
3. Derive the **behavior constraints** from the temperament tag:
   - gentle-quiet-timid → never initiates aggression, avoids confrontation
   - aloof-detached → keeps distance, resists intimacy
   - lively-outgoing → proactive, expressive
   (extend per temperament in the EmotionBehaviorMap).
4. On every chapter: run the **continuity checklist** (below) before accepting.

## Continuity checklist (per chapter)

- [ ] All immutable facts preserved verbatim (no synonym drift)
- [ ] Temperament-consistent behavior (no out-of-character actions without cause)
- [ ] Props/wardrobe continuity (nothing gained or lost unexplained)
- [ ] Emotional arc within the character's range (no unmotivated mood swings)
- [ ] Dialogue style matches voice guard

## Cross-skill rule

- The Drawing Template owns **visual identity**; the Story Engine owns **behavioral
  identity**; the anthropomorphic engine owns **emotional state**.
- All three key off the same `character_id` — a single source of truth, three
  renderings.
