### /savenow preview — memory/2026-05-15.md

**3 candidates** → 1 add, 1 merge, 1 skip. No write performed.

---

**1. ADD — Gateway token mismatch fix**
- Resolved `unauthorized: gateway token mismatch` by updating `gateway.cmd` and the related env variables.
- Next time a similar error appears, check token and env alignment first.
_compared against:_ (no close match above 0.4)

**2. MERGE — Telegram inline button rules → existing "Telegram UI conventions" (14:02)**
_reason: Two new rules belong to the same existing topic._
_all 2 bullet(s) already present — will be skipped by merge._

**3. SKIP — Sprint planning notes**
_reason: Temporary plan, no lasting value._
_(closest existing: none — agent skipped on judgement)_

---

Buttons expire in 30 min. Or `/savenow auto` next time to skip preview.

---

Below the message, Telegram renders a 1-row inline keyboard:

```
[ ✅ Apply ]  [ ❌ Cancel ]
```
