# Round-Robin Math, Bye Rotation & the Night Re-Flow

## The circle method (proof sketch)

Take N players. Fix player 1 at the top of a circle; arrange the rest around
it. Each round pairs opposite positions ((N/2) pairs), then everyone except
player 1 rotates one position clockwise. After N−1 rounds, every player has
occupied every position except the fixed one exactly once, and each pairing
appears exactly once.

Why exactly once: player 1 meets each rotating player exactly once (one round
each as their opposite), and two rotating players meet when their positions
become opposite — which happens exactly once per full cycle, since their
angular distance is invariant and each rotation moves both by one step.

**Odd N:** insert a phantom (BYE). Whoever is opposite the phantom sits out.
This yields N rounds (not N−1) with (N−1)/2 real matches per round and one
bye. The phantom rotates with everyone, so byes distribute one-per-player
across the N rounds — a perfect round-robin bye schedule for free.

**Double round-robin:** run the cycle twice with home/away mirrored
(pairs reversed) so everyone "hosts" once — mostly cosmetic in rec sports,
but it breaks the "always listed first" superstition.

## Bye distribution for odd N

The phantom construction gives every player exactly one bye per full cycle —
the strongest possible fairness guarantee for a complete round-robin. The
problem is real life: attendance is not the fixture list. That's what the
night re-flow solves.

## The night re-flow algorithm (`night`)

Given R roster, A absent today, C courts:

1. **Present** P = R − A. Slots S = 2C.
2. If |P| < S → **short-handed**: report the gap and list call-up candidates
   (absent roster members) rather than inventing matches. An empty court is a
   recruiting problem, not a scheduling one.
3. If |P| ≥ S → byes needed B = |P| − S. Assign byes to the B players with
   the **fewest recorded byes** (tie → alphabetical, so it's deterministic
   and not political). Persistent absence is its own penalty; presence should
   never additionally cost you court time.
4. Pair the remaining 2C players: greedy over skill-sorted order, each player
   matched with the **never-met** partner whose level is closest (fresh
   matchups first, competitive games second).
5. Record byes and played pairs for the next week's fairness data.

## Standings tiebreaker order

1. **Points** (2 per win; rec leagues rarely need 3-for-a-win complexity)
2. **Game difference** (score diff accumulated)
3. **Head-to-head** within the tied group: net wins against other tied
   members. This is the tiebreaker players actually consider fair — "we beat
   them directly" outranks any arithmetic.
4. Alphabetical (final resort, deterministic)

The implementation groups players tied on (points, diff) and re-sorts each
group by intra-group head-to-head — the standard league practice.

## Court assignment notes (optional skill levels)

The pairing greedy uses levels 1–5 to keep courts competitive *within* a
match, and to note de-facto "bloodbath court" vs "fun court" separation when
levels cluster. Levels are advisory only; rec leagues die of competitiveness
miscalibration more often than of unfair fixtures.

## What this deliberately is not

- **Not knockout brackets.** Elimination structures need a different tool;
  `fixtures` can seed groups (round-robin within groups) for group-stage +
  knockout formats — a common rec tournament shape.
- **Not multi-team league management.** Venues, referees, registration,
  fees, disciplinary processes — that's governing-body software. This is the
  Tuesday-night problem: who plays whom, who sits, is it fair, who's leading.

## Match-day sheet discipline

The printed sheet (courts, fixtures, score blanks, byes, next date) is the
memory of the league. Results recorded on the night survive; results
reconstructed on Thursday don't. The `result` command takes 10 seconds —
the sheet exists so nobody has to remember scores, only to copy them.
