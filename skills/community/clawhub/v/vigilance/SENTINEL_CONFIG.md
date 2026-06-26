# SENTINEL_CONFIG.md — OpenClaw Agent Guardrail Configuration
#
# This file is the single source of truth for what the OpenClaw agent is
# allowed to do on your behalf.  The Sentinel engine reads it before every
# high-stakes tool call.
#
# Placement (first file found wins):
#   1. ~/.openclaw/skills/agent-sentinel/SENTINEL_CONFIG.md   ← skill dir
#   2. <your project directory>/SENTINEL_CONFIG.md            ← project-specific
#   3. ~/.openclaw/SENTINEL_CONFIG.md                         ← user-wide default
#
# Format rules:
#   • Key_Name: Value   (colon) OR   Key_Name = Value   (equals) — both work.
#   • Lines starting with '#' are comments and are ignored.
#   • Section headers are H2 Markdown (## Section_Name).
#   • Sub-section headers are H3 (### Sub_Section).

---

## Global_Safety

# ── Child Age Policy ─────────────────────────────────────────────────────────
#
# The Sentinel engine enforces strict child-safety filtering when this section
# is present.  The primary household has a child aged 9 (under 10 years old).
#
# ALL agent actions — web searches, bookings, shell commands, and payments —
# are screened against this policy BEFORE execution.
#
# A two-pass check is performed:
#   Pass 1 (Heuristic): Regex scan for hard-blocked content categories.
#   Pass 2 (LLM Judge): Semantic evaluation by an AI safety model.
# Either pass can independently trigger a BLOCK (severity: HIGH).

Child_Age_Limit: 10

# Hard-blocked content categories — these are NEVER negotiable.
# Presence of any of these in the action data results in an immediate BLOCK.
#
# Blocked_Content_Categories:
#   - Adult Content / Pornography / Nudity / NSFW material
#   - Graphic Violence (gore, torture, execution videos)
#   - Child Sexual Abuse Material (CSAM / CSEM) — zero tolerance
#   - Horror content (horror films, games, jump-scare sites)
#   - Gambling (casinos, sports betting, online poker sites)
#   - Mature-rated video games (GTA, M-rated titles)
#   - Drug / alcohol acquisition instructions
#
# Note: this list is enforced by the engine regardless of what is written here.
# Adding or removing items in this comment does NOT change engine behavior.
# To adjust heuristic patterns, edit CHILD_SAFETY_PATTERNS in eval_engine.py.

---

## User_Preferences

# ── Travel ────────────────────────────────────────────────────────────────────
#
# All values below are enforced for booking_tool and web_search actions.
# BLOCK decisions are hard stops; ADVISE decisions require user confirmation.

### Travel

# Maximum total price for any single booking (USD).
# Engine behavior:
#   > Max_Budget           → BLOCK  (severity: MEDIUM)
#   > 85% of Max_Budget    → ADVISE (severity: LOW)  — "getting close to limit"
Max_Budget: $500

# Night-flight restriction.
# Set to 'true' to block any flight with a departure or arrival in the window.
# Engine behavior: any time in Night_Flight_Window → BLOCK (severity: MEDIUM)
Night_Flights_Blocked: true
Night_Flight_Window: 22:00 - 06:00

# Preferred airlines (soft preference — triggers ADVISE if none detected).
# Separate multiple values with commas.
Preferred_Airlines: Delta, United, Southwest

# Blocked airlines (hard block — triggers BLOCK if detected in booking data).
# Leave blank or remove to allow all airlines.
# Example: Blocked_Airlines: Spirit, Frontier
Blocked_Airlines: Spirit, Frontier

# Maximum number of stops (layovers) acceptable.
# Engine behavior: detected stops > Max_Stops → BLOCK (severity: MEDIUM)
Max_Stops: 1

# Preferred cabin class.
# Options: economy | premium economy | business | first
# Engine behavior: different cabin detected → ADVISE (severity: LOW)
Preferred_Cabin: economy

# Maximum number of days in advance to book.
# Engine behavior: booking window exceeds this → ADVISE (severity: LOW)
Max_Booking_Advance_Days: 90

---
# End of SENTINEL_CONFIG.md
