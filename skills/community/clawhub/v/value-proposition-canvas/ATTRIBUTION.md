# Third-Party Attributions

This skill synthesizes ideas from public academic and practitioner sources. The implementation, phrasing, and structure of the skill itself are original work licensed under MIT (see `LICENSE`). The underlying frameworks and concepts are attributed below.

## Primary sources (the framework itself)

**Osterwalder, A., Pigneur, Y., Smith, A. (2014).** *Value Proposition Design.* Wiley.

The Value Proposition Canvas — the two-sided structure (Customer Profile with Jobs/Pains/Gains, Value Map with Products & Services/Pain Relievers/Gain Creators) and the canonical UVP formula — was introduced in this work. The framework itself (the idea, the structure, the formula) is a published business-design framework and is not copyrightable; only specific *expressions* of it are. The wording in this skill is original.

The v2.0 skill produces the **full VPC** through both phases: Phase 1 (Customer Profile) and Phase 2 (Value Map with three substeps: Pain Relievers mapping, Gain Creators mapping, Products & Services bundling), plus Phase 2.5 (Framework Selection). It ends at "framework selected, ready for prioritization" — UVP drafting is the user's responsibility, downstream of the chosen framework (default: Kano). v2.1 added the multi-file output structure; v2.2 (current) added the Co-creation discipline described in `SKILL.md`.

**Strategyzer.** https://www.strategyzer.com — Osterwalder's company. The canonical steward of the VPC and the Business Model Canvas that VPC extends. The skill's "one canvas per segment", "competitor value maps", and "fit is not all jobs addressed" rules are drawn from Strategyzer's public best-practices guidance.

**Interaction Design Foundation (2024).** *The Value Proposition Canvas.* https://www.interaction-design.org — Synthesizes Osterwalder et al. with worked examples (Amazon, IxDF) and is the source for the canonical Pain categories (concerns, dissatisfaction, challenges, barriers, cost) and Gain categories (current-positive, social, improvements, success criteria, savings, adoption) used in Layers 2 and 3. The IxDF article also contributed the two rules "Gains are not the simple result of the job" and "Gains are not the inverse of pains" (drawn from Osterwalder's text but stated more sharply in the IxDF synthesis).

## Customer discovery and research

**Blank, S. (2013).** *The Four Steps to the Epiphany.* K&S Ranch. — Customer Development methodology, including the GOOB principle ("Get Out Of the Building"). Section 0 of the methodology is grounded in Blank's discipline: a VPC built on assumption is a Webvan-shaped product, no matter how polished the bundle.

**Christensen, C. M., Hall, T., Dillon, K., Duncan, D. S. (2016).** *Know Your Customers' Jobs to Be Done.* Harvard Business Review. — Foundational JTBD framing used in Layer 1.

**Ulwick, A. W. (2016).** *Jobs to be Done: Theory to Practice.* Idea Bite Press. — Outcome-Driven Innovation. The "outcome not output" discipline enforced in Layer 3 echoes Ulwick's framing.

**Klement, A. (2016).** *When Coffee and Kale Compete.* — Origin of the Job Story format (`When [situation], I want [need], so I can [outcome]`) used in Layer 1.3.

**Patton, J. (2014).** *User Story Mapping.* O'Reilly. — Precursor discipline to Job Stories. Used as background.

**Ries, E. (2011).** *The Lean Startup.* Crown Business. — The Build Trap concept, named explicitly in the skill as the failure mode the Solution-First Lock prevents.

**Perri, M. (2018).** *Escaping the Build Trap.* O'Reilly. — The modern critique of feature-factory product management. The webvan.md worked example is grounded in the Perri/Ries literature.

## Strategy, innovation, and competitive positioning

**Kim, W. C., Mauborgne, R. (2005).** *Blue Ocean Strategy.* Harvard Business Review Press. — Value Innovation framework (the four actions: eliminate, reduce, raise, create) applied in Layer 4.4.

**Levy, J. (2015).** *UX Strategy.* O'Reilly. — Demand validation discipline, porters-of-progress framing. Background for Section 0 (GOOB).

**Christensen, C. M. (1997).** *The Innovator's Dilemma.* Harvard Business Review Press. — Background for the "good execution of a bad plan is still a bad plan" lesson in the webvan.md example.

## Lean product and pain-driven design

**Gothelf, J., Seiden, J. (2016).** *Lean UX.* O'Reilly. — The three-level outcome verification (functional / emotional / long-term) used in Layer 3 Filter 3. The classification of gains as functional / emotional / social draws on Gothelf & Seiden.

**Hunt, V. (2016).** *The Product Taster / Sprint to Market.* — Pain-Driven Design. The "broken leg vs scratched knee" test used in Layer 2.2 is the canonical Hunt framing.

**Womack, J. P., Jones, D. T. (1996).** *Lean Thinking.* Simon & Schuster. — The muda (waste) discipline applied in Layer 4.2 (Pain Relievers via Muda Elimination) and the webvan.md example.

## Socratic dialogue and reasoning engine

**Vlastos, G. (1983, 1994).** *Socrates: Ironist and Moral Philosopher.* — The Elenchus as method. Used in Layer 1.2 Step 1.3 (Adversarial Probing).

**Seeskin, K. (1987).** *Dialogue and Discovery.* — Socratic terminology anchoring. Used in Layer 1.2 Step 1.2.

**Kahneman, D. (2011).** *Thinking, Fast and Slow.* Farrar, Straus and Giroux. — System 1 / System 2, cognitive strain as a trigger for deliberate reasoning, the "substitution" heuristic (answering an easier question than the one asked), and WYSIATI ("what you see is all there is"). Grounds the Confidence Gating used in the gate conditions between Layers 1-5 and the Socratic Pause used between pains in Layer 2.3.

**Kahneman, D., Klein, G. (2009).** "Conditions for Intuitive Expertise: A Failure to Disagree." *American Psychologist*, 64(6), 515-526. — Adversarial collaboration as a structured way to resolve disagreement between two framings of the same evidence. Grounds the Adversarial Probing stance in Layer 1.2 Step 1.3.

**Mitchell, D. J., Russo, J. E., Pennington, N. (1989).** "Back to the Future: Temporal Perspective in the Explanation of Events." *Journal of Behavioral Decision Making*, 2(1), 25-38. — Origin of "prospective hindsight": treating an outcome as already having occurred improves the ability to reason about its causes. Background for the Faithfulness Check (Focused Self-Query) used in Layer 1 Step 1.5 and Layer 5 Step 5.4.

**Klein, G. (2007).** "Performing a Project Premortem." *Harvard Business Review*, September 2007. — Popularized the pre-mortem technique, built on prospective hindsight. Background for the entire skill's "assume the canvas is wrong, find out why" stance.

**Torres, T. (2021).** *Continuous Discovery Habits.* Product Talk LLC. — Applies the pre-mortem / prospective-hindsight technique inside product discovery practice. Cited for the product-context adaptation, not as the originating source (see Mitchell/Russo/Pennington and Klein above for that).

The `socratic-dialogue` skill in this playbook is loaded at every gate transition.

## Business analysis and requirements

**IIBA (2018).** *A Guide to the Business Analysis Body of Knowledge (BABOK) v3.* — Stakeholder analysis and requirements anchoring. Background.

**Wiegers, K., Beatty, J. (2013).** *Software Requirements.* Microsoft Press. — Quality of requirements, verifiability. Background for the Quantification discipline in Layers 2.4 and 3.6.

## Sales-side validation (for money-shot questions)

**Rackham, N. (1988).** *SPIN Selling.* — Implication, need-payoff, money-shot question patterns. Used in Layer 5 Step 5.3.

**Weiss, A. (2013).** *Value-Based Fees.* Wiley. — Alan Weiss questioning framework, legacy and meaning questions. Used in Layer 1.2 (5 Whys).

**Hopkins, T. (1980).** *How to Master the Art of Selling.* — Classic money-shot sequencing. Background.

## What this skill is NOT derived from

- No text was copied from any specific blog post, book, or article. The IxDF article was used as a synthesis aid; all wording in this skill is original.
- No proprietary consulting framework material (no BCG / McKinsey / Gartner decks, no paid product-management courseware) is reproduced.
- No private client or employer data is included. The worked examples (Airbnb, Slack, Webvan, design-handoff) use only public-domain company cases and a fully abstracted "design-to-code handoff tool" pattern that draws on the public design-to-code literature.
- No user-specific product name, customer name, or proprietary artifact is named in the examples. The design-handoff example uses a generic "Date Picker" component, a generic `spec.md` document, and a generic solo-designer persona.

## How to attribute when you remix

If you build a derivative skill or fork this one, please keep:

1. This `ATTRIBUTION.md` file
2. The MIT `LICENSE`
3. A visible link back to the original primary source (Osterwalder, Pigneur, Smith 2014) somewhere in your derived work
4. A visible link to the IxDF synthesis (used as a key secondary source)

That keeps the chain of credit intact without burdening downstream users.
