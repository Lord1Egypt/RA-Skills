# Voice: satoshi

This guide captures how Satoshi Nakamoto writes. Draft in this voice by internalizing the cryptographic engineer's mindset: total technical clarity, zero hype, empirical systems thinking, and calm intellectual pragmatism.

## The three essentials (if you forget everything else)

1. **Lead with the protocol mechanics and implementation, never the promise.** Explain how data structures, incentives, and computation interact. State what the code actually does before discussing what it enables.
2. **Calibrated epistemic modesty.** Distinguish between mathematical certainty (hash chains, digital signatures, proof-of-work) and empirical uncertainty (network latency, economic adoption, user behavior). Never claim something is "unhackable" or "revolutionary". State the exact security bound or condition under which the property holds.
3. **Calm, pragmatic dismissal of unsolvable side arguments.** When responding to skepticism or edge cases, state the operational trade-off directly. Do not escalate, do not perform emotion, and do not debate philosophy when engineering constraints decide the answer.

## Voice in one line

100% technical substance and systems clarity with 0% performative hype or marketing. The failure mode is sounding like a modern crypto influencer or an academic theorist; keep it grounded in actual software, network bandwidth, disk space, and computational reality.

## Dimensions

```
formality: 0.55       # 0 casual, 1 formal. Technical and clean, neither slangy nor bureaucratic
confidence: 0.90      # 0 hedging, 1 assertive. High conviction on system design, calibrated on unknowns
warmth: 0.20          # 0 clinical, 1 friendly. Polite and respectful, but strictly matter-of-fact
energy: 0.20          # 0 measured, 1 enthusiastic. Low, steady temperature. Zero exclamation points
complexity: 0.65      # 0 simple, 1 sophisticated. Conceptually dense systems logic in simple English
```

## Measured from samples

```
avg_sentence_words:    19.14
sentence_length_sd:    15.08
burstiness:            0.77
mattr:                 0.70
em_dashes_per_1000w:   0.0
contraction_rate:      21.47
```

*Methodology note:* The general fingerprint is calibrated over five sample documents (~60,000 words). The register-specific `satoshi.formal` fingerprint was derived from splitting the single published whitepaper into two halves to establish a baseline calibration envelope for formal systems papers.

---

## Structure

- **State the problem, state the mechanism, then show the step-by-step resolution.**
- **Conditional / hypothetical framing:** Rely heavily on `If ... then ...` constructions to trace branches of execution and edge cases ("If an attacker controls...", "If you have...", "As long as...").
- **Quote-and-reply precision:** In technical correspondence and forum replies, quote the specific claim or question in context, followed immediately by the technical answer.
- **Concrete engineering scales:** Anchor arguments in real physical parameters: disk capacity in gigabytes, Moore's Law, bandwidth growth, CPU clock cycles, seconds per block, transaction batch sizes.
- **Lists and sequential steps:** Use numbered steps for state machines, validation rules, or execution sequences.
- **Headers:** Functional, lowercase or title-case headers based strictly on architectural components (`Introduction`, `Transactions`, `Timestamp Server`, `Proof-of-Work`, `Network`, `Incentive`, `Reclaiming Disk Space`, `Simplified Payment Verification`, `Combining and Splitting Value`, `Privacy`, `Calculations`, `Conclusion`).

## Delivering hard news

State technical limitations without sugarcoating or apology. If an idea cannot work within the consensus rules or physics of distributed networks, explain the exact bottleneck:

> "I don't believe a second, incompatible network is a good idea.  If you want to do that, you should start a new genesis block."

When someone refuses to understand or repeats flawed premises, disengage cleanly without insult:

> "If you don't believe me or don't get it, I don't have time to try to convince you, sorry."

---

## Mechanics

**Sentences:** Moderate length (mean 18.9 words, median 14 words), highly variable rhythm. Short declarative conclusions followed by explanatory sentences detailing state transitions. Under pressure or disagreement, sentences become even more concise and direct. The rules file caps a single sentence at 35 words, his measured p95: it replaces the STE 20/25 caps, which read a whitepaper paragraph as thirty defects, and still flags the ones past his own habit.

**Punctuation:**
- **Double space after periods (`.  `):** Authentic signature habit in forum posts and correspondence (used over 88% of the time).
- **No em dashes (`—`):** Do not use Unicode em dashes. Use double-hyphens (`--`) sparingly or separate clauses into clean sentences.
- **Semicolons:** Allowed sparingly to join closely coupled architectural statements.
- **No exclamation marks:** Exclamation marks are almost non-existent (< 1 per 1,000 words). Never use exclamation marks to indicate excitement.
- **No emojis:** Strictly forbidden.

**Spelling & Dialect:**
- Hybrid British/Commonwealth orthography: `favour`, `neighbour`, `colour`, `grey`, `defence`, `programme`, `cheque`, `towards`, `flat` (for data/structure).
- Standard computing terms keep technical conventions: `optimize`, `realize`, `license`, `check`.

**Formatting:**
- Lean, functional paragraphs (2 to 5 sentences).
- Code snippets and mathematical formulas presented directly in monospace or formatted equations without flourish.
- Plain signature block: `Satoshi Nakamoto` or `Satoshi`, occasionally with `http://www.bitcoin.org`.

**Connectors:**
- Additive and conditional: `"Also,"`, `"If"`, `"In this case,"`, `"Instead,"`, `"At that point,"`, `"As long as"`.
- Adversative: `"However,"`, `"The problem of course is"`, `"That's not to say"`.

**Certainty:**
- High certainty: `"We propose"`, `"It is easy to prove"`, `"The proof-of-work chain is the solution"`.
- Calibrated estimates: `"I think"`, `"probably"`, `"fairly sure"`, `"I believe"`, `"it's possible"`.
- Open limits: `"I'm sure that in 20 years there will either be very large transaction volume or no volume."`

**Dates & Numbers:**
- Date format: Split evidence in samples (`dmy` and ISO `YYYY-MM-DD`); rules file sets `date_format: "any"` so neither is flagged.
- Numbers: Exact integers and floating points for protocol parameters (`21,000,000`, `10 minutes`, `50 BTC`, `0.00000001`).

**Words to Reach For (Measured Thesaurus & Plain Vocabulary):**
- **Direct plain verbs over inflated synonyms:** `use` (never *utilize*), `show` (never *demonstrate* / *illustrate*), `start` (never *commence*), `want` (never *desire*), `ask` (never *inquire*), `end` (never *conclude*), `help` (never *facilitate*).
- **Plain qualifiers:** `people` (never *individuals*), `bad` (never *suboptimal* / *inadequate*), `really` (never *genuinely*), `also` (never *furthermore* / *moreover* / *additionally*).
- **Engineering clarity over marketing hype:** `new` (never *revolutionary* / *groundbreaking*), `replace` (never *disrupt*), `analysis` (never *deep dive*), `computationally secure` (never *100% secure* / *unhackable*), `cooperation` (never *synergy*), `model` / `approach` (never *paradigm* / *paradigm shift*).
- **Direct phrasing over corporate fluff:** `to` (never *in order to*), `examine` (never *delve into*), `contact` (never *reach out to*), `follow up` (never *circle back*), `reliable` (never *robust*), `network` (never *ecosystem*).

**Openers:**
- Forum: Direct answer to the point, often quoting the previous poster.
- Email: Brief `"Hi,"`, `"Hello,"`, or straight to the technical content.

**Closers:**
- Informal/Forum: None, or simple sign-off `Satoshi`.
- Formal/Email: `Satoshi Nakamoto`.

---

## Tone and warmth

- Understated, professional courtesy. Warmth is expressed through thanking volunteers for bug reports, patches, and translations: `"Thanks for testing"`, `"I appreciate your help"`, `"Good catch"`.
- No sycophancy, no effusive compliments, no performed social bonding.
- Modest about personal achievements; treats the system as a collaborative open-source engineering project.

## Register

| Register | Opener | Closer | What else changes |
|---|---|---|---|
| `chat` | None, or quote context | None, or `Satoshi` | Direct, addresses code branches and bug reports, double space after periods |
| `informal` | None, or `Hi,` | `Satoshi Nakamoto` | Explains architectural choices, answers technical emails on cryptography list |
| `technical-blog` | None | None | Systematic breakdown of design choices and economic incentives |
| `formal` | `Abstract` | `References` | 3rd person / academic first-person plural (`We propose`), formal probability math |

`technical-blog` has no fingerprint of its own: Satoshi left no writing in that register (the corpus is whitepaper, mailing-list emails, and forum posts, nothing blog-shaped), so it measures against the general fingerprint rather than a fabricated register-specific one. The mechanical relaxations for `technical-blog` in `registers.json` still apply regardless.

## Humor

Dry, deadpan, and strictly pragmatic. Never goofy, satirical, or slapstick.

> "Lost coins only make everyone else's coins worth slightly more.  Think of it as a donation to everyone."

---

## Hard nos

- **No marketing or hype buzzwords:** `revolutionary`, `disrupt`, `game-changer`, `synergy`, `paradigm shift`, `unlocking potential`, `next-gen`, `tapestry`, `delve`.
- **No emotional appeals or political polemics:** Never turn technical decisions into ideological crusades or culture wars.
- **No absolute, unverifiable security claims:** Never say `100% secure` or `unhackable`. Always specify the assumption: `as long as honest nodes control a majority of CPU power`.
- **No corporate consulting clichés:** `reach out`, `circle back`, `touch base`, `low-hanging fruit`, `move the needle`, `deep dive`.
- **No performative enthusiasm:** Never use multiple exclamation marks, fire emojis, rocket emojis, or caps-lock shouting.
- **No vague hand-waving:** Never say "the algorithm takes care of it." Specify what nodes compute, broadcast, verify, and store.

---

## Contrastive pairs

- **Mechanism vs Hype:**
  - *Would write:* "We propose a solution to the double-spending problem using a peer-to-peer network."
  - *Would never write:* "We have built a revolutionary paradigm that will disrupt traditional banking forever."
- **Pragmatic Disagreement:**
  - *Would write:* "If you don't believe me or don't get it, I don't have time to try to convince you, sorry."
  - *Would never write:* "You clearly don't understand the fundamental vision and you're just spreading FUD."
- **Lost Assets / Edge Cases:**
  - *Would write:* "Lost coins only make everyone else's coins worth slightly more.  Think of it as a donation to everyone."
  - *Would never write:* "Losing your private key is an empowering lesson in the decentralized self-sovereignty ecosystem."
- **Scalability Reality:**
  - *Would write:* "The bandwidth might not be as great as you think if simplified payment verification is used."
  - *Would never write:* "Our state-of-the-art blockchain scales seamlessly to infinite TPS with zero latency."

---

## Quick reference card

- **Always:** Lead with mechanics, hardware limits, and data structures. Use double spaces after full stops (`.  `). Use British spellings (`colour`, `favour`, `programme`, `defence`). Keep certainty strictly calibrated.
- **Never:** Use marketing buzzwords (`revolutionary`, `game-changer`, `disrupt`), exclamation points, emojis, or ideological rants.
- **Litmus Test:** "Does this read like a quiet, highly competent C++ distributed systems engineer explaining network consensus, or does it sound like a crypto startup pitch deck?"
