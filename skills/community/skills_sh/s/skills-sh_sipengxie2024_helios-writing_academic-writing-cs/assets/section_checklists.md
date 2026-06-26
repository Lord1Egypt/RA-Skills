# Section-by-Section Quality Checklists

## How to Use These Checklists

These checklists serve as quality gates for each paper section. Use them:

1. **During drafting**: As a planning guide (what should this section contain?)
2. **After drafting**: As a review checklist (did I include everything?)
3. **Before submission**: As a final quality check

**Not all items apply to every paper.** Adapt based on paper type and venue requirements.

---

## Abstract Checklist

**4-Sentence Structure:**
- [ ] **Context (1 sentence)**: Establishes the broad area and its importance
- [ ] **Gap/Problem (1 sentence)**: States what's missing or what problem exists
- [ ] **Contribution (1-2 sentences)**: Describes what this paper provides (method/system/analysis)
- [ ] **Impact (1 sentence)**: Summarizes key results or implications

**Quality Criteria:**
- [ ] Self-contained (readable without the paper)
- [ ] Specific contribution (not vague: "we improve X" → "we achieve Y% improvement on X")
- [ ] Concrete results (includes numbers/metrics)
- [ ] Within word limit (typically 150-250 words)
- [ ] No citations (most venues)
- [ ] Matches paper content (no overclaiming)

**Language:**
- [ ] Present tense for general facts
- [ ] Past tense for what the paper did
- [ ] Active voice ("We propose" not "A method is proposed")

---

## Introduction Checklist

**Funnel Structure (Broad → Narrow → Specific):**
- [ ] **Opening (1 para)**: Establishes the problem domain and its importance to the field
- [ ] **Background & Motivation (1-2 paras)**: Narrows to the specific problem
  - [ ] Concrete example or scenario illustrating the problem
  - [ ] Why existing approaches fall short (brief)
- [ ] **Gap Statement (0.5-1 para)**: Explicitly states what's missing
  - [ ] Uses signal phrases: "However, existing work lacks...", "An open question is..."
- [ ] **Contribution Overview (1 para)**: Clearly states what the paper provides
  - [ ] High-level description of the approach
  - [ ] Key insight or novelty
- [ ] **Results Summary (0.5 para)**: Main empirical findings
  - [ ] 2-3 concrete results with numbers
- [ ] **Paper Organization (0.5 para)**: Roadmap (optional for conferences, expected for journals)

**Quality Criteria:**
- [ ] Contribution is clear by end of 4th paragraph
- [ ] Includes at least one figure (architecture or key result) for systems/ML papers
- [ ] Balances motivation and technical preview
- [ ] Avoids overselling or vague claims
- [ ] Sets appropriate scope (not promising more than delivered)

**Common Pitfalls to Avoid:**
- [ ] No "inverted pyramid" (starting narrow and expanding)
- [ ] No excessive background (save for Related Work)
- [ ] No premature technical details (save for Method)

---

## Related Work Checklist

**Organization:**
- [ ] Grouped thematically (not chronologically or alphabetically)
  - [ ] 3-5 clear categories/themes
  - [ ] Each category has a descriptive subheading
- [ ] Each category describes the general approach first
- [ ] Representative works cited with 1-sentence descriptions
- [ ] Limitations relevant to your contribution are pointed out

**Positioning:**
- [ ] **Positioning paragraph** clearly articulates differences from prior work
  - [ ] "In contrast to [X], our approach..."
  - [ ] Explicit comparison to closest work
  - [ ] Differences are justified (not just different for novelty's sake)
- [ ] Claims about improvements are supported (or will be in Results)

**Quality Criteria:**
- [ ] Comprehensive coverage of relevant subfields
- [ ] Not just a "laundry list" of citations
- [ ] Respectful tone (not dismissive of prior work)
- [ ] Connected to your contribution (not isolated)
- [ ] Citations are accurate and complete

**Placement Decision:**
- [ ] After Introduction (if contribution is simple to state) ✓ Common in ML/AI
- [ ] Before Conclusion (if contribution requires deep technical understanding) ✓ Common in Systems/Theory

---

## Methodology Checklist

**Dual Objectives:**
- [ ] **Reproducibility**: Enough detail for reimplementation
- [ ] **Intuition**: Explains why the approach works

**Structure (Adapt Based on Paper Type):**

### For Algorithmic/ML Papers:
- [ ] **Problem Formulation**: Formal definitions and notation
  - [ ] All symbols defined
  - [ ] Problem formally stated (input, output, objective)
- [ ] **High-Level Overview**: 1-2 paragraphs + figure
  - [ ] Architecture diagram or algorithm flowchart
  - [ ] Intuitive explanation of how it works
- [ ] **Detailed Design**: Algorithm boxes or mathematical derivations
  - [ ] Pseudocode for key algorithms
  - [ ] Mathematical formulations with explanations
- [ ] **Implementation Details**: Hyperparameters and architecture choices
  - [ ] Design choices justified
- [ ] **Complexity Analysis** (if relevant): Time/space bounds

### For Systems Papers:
- [ ] **Architecture Overview**: Block diagram + walkthrough
- [ ] **Component Design**: Per-component deep dive
  - [ ] Interfaces between components
  - [ ] Data structures used
- [ ] **Key Mechanisms**: Protocols, algorithms, optimizations
  - [ ] Trade-offs discussed
- [ ] **Implementation**: Language, libraries, tools
  - [ ] Deployment considerations

### For Empirical/Measurement Papers:
- [ ] **Experimental Design**: Hypotheses, variables, controls
- [ ] **Data Collection**: Sources, preprocessing, cleaning
  - [ ] Ethical considerations (if human subjects)
- [ ] **Analysis Methods**: Statistical tests, metrics
- [ ] **Threats to Validity**: Limitations and mitigation

**Quality Criteria:**
- [ ] Notation is consistent with Introduction
- [ ] Every design choice is justified (or will be in Ablations)
- [ ] Balance: detailed enough for experts, accessible for non-experts
- [ ] Figures/diagrams illustrate complex mechanisms
- [ ] No hand-waving ("we simply..." for non-trivial steps)

---

## Experiments/Results Checklist

**Experimental Setup:**
- [ ] **Datasets** described:
  - [ ] Size, domain, source
  - [ ] Train/validation/test splits
  - [ ] Preprocessing steps
- [ ] **Baselines** specified:
  - [ ] All compared methods listed
  - [ ] Citations for each baseline
  - [ ] Fairness: all use same data/setup
- [ ] **Metrics** defined:
  - [ ] What you measure (accuracy, F1, latency, etc.)
  - [ ] Why these metrics are appropriate
- [ ] **Hardware/Software**:
  - [ ] Compute infrastructure (GPUs, CPUs)
  - [ ] Software versions (framework, libraries)
- [ ] **Hyperparameters**:
  - [ ] How selected (grid search, validation set, etc.)
  - [ ] Reported for reproducibility

**Main Results:**
- [ ] Table/figure showing primary comparison
- [ ] Text interpretation: "Table 1 shows that..."
- [ ] Key findings highlighted (e.g., "achieves 15% improvement")
- [ ] Statistical significance reported (confidence intervals, p-values, or standard deviations)
- [ ] Best results clearly marked (bold, underline)

**Ablation Studies (Critical for ML/Systems):**
- [ ] Each component's contribution demonstrated
- [ ] Table showing effect of removing/modifying components
- [ ] Results justify design choices

**Analysis:**
- [ ] Where does the method excel? Where does it fail?
- [ ] Qualitative analysis (visualizations, examples)
- [ ] Error analysis: Common failure modes identified
- [ ] Additional experiments probing specific aspects

**Computational Cost (if relevant):**
- [ ] Training time, inference time, memory usage
- [ ] Comparison with baselines
- [ ] Scalability discussed

**Presentation Quality:**
- [ ] Tables are clean, readable, well-formatted
- [ ] Figures are high-resolution with readable fonts
- [ ] All figures/tables referenced in text before they appear
- [ ] Captions are self-contained

**Common Mistakes to Avoid:**
- [ ] No cherry-picking without justification
- [ ] No missing ablations (readers won't believe unvalidated design choices)
- [ ] No "data vomit" (numbers without interpretation)
- [ ] No ignoring computational cost

---

## Discussion Checklist

**Content (typically 2-4 paragraphs):**
- [ ] **Summary of Findings**: Restates key empirical results
  - [ ] "Our experiments demonstrate that..."
- [ ] **Interpretation**: Explains why the method works
  - [ ] Connects results to design choices
  - [ ] Provides insights beyond raw numbers
- [ ] **Limitations**: Honestly acknowledges scope restrictions
  - [ ] What scenarios does the method not handle?
  - [ ] What assumptions are made?
  - [ ] Failure cases discussed
- [ ] **Broader Implications**: Discusses impact
  - [ ] How this advances the field
  - [ ] New research directions opened
  - [ ] Potential real-world applications

**Quality Criteria:**
- [ ] Balanced tone (confident but not overselling)
- [ ] Limitations stated honestly (increases credibility)
- [ ] Connects back to problem motivation in Introduction
- [ ] Avoids introducing new results (those go in Results section)

---

## Conclusion Checklist

**Structure (typically 2-3 paragraphs):**
- [ ] **Restate Contribution (1 para)**:
  - [ ] Recap the problem and solution
  - [ ] Summarize key findings
  - [ ] "In this paper, we presented [X], which addresses [Y] by [Z]."
- [ ] **Broader Impact (0.5-1 para)**:
  - [ ] Reiterate significance
  - [ ] Potential applications
- [ ] **Future Work (0.5-1 para)**:
  - [ ] Open questions
  - [ ] Extensions or improvements
  - [ ] Phrase as opportunities: "An interesting direction is..." (not "In future work, we will...")

**Quality Criteria:**
- [ ] Concise (no unnecessary repetition)
- [ ] No new ideas or results introduced
- [ ] Not a copy-paste of Abstract
- [ ] Ends on a strong, forward-looking note

**Avoid:**
- [ ] Vague statements: "We did some cool stuff"
- [ ] Promises: "In future work, we will..." (implies current work is incomplete)
- [ ] Defensive language: "While we didn't achieve X, we hope..."

---

## Figures and Tables Checklist

**General Requirements:**
- [ ] Every figure/table is referenced in text before it appears
- [ ] Captions are self-contained (reader understands without reading main text)
- [ ] Fonts are readable (≥8pt)
- [ ] Consistent visual style throughout paper

**Figures:**
- [ ] Axis labels include units (e.g., "Time (seconds)", "Accuracy (%)")
- [ ] Legends are present and clear
- [ ] Error bars/bands shown (standard deviation or confidence intervals)
- [ ] Colorblind-friendly palette used (avoid red-green)
- [ ] High resolution (vector formats preferred; raster ≥300 DPI)
- [ ] Architecture diagrams have clear data flow and labeled dimensions

**Tables:**
- [ ] Methods/metrics clearly labeled
- [ ] Best results highlighted (bold, underline)
- [ ] Standard deviations or confidence intervals included
- [ ] Sorted logically (by performance or grouping)
- [ ] Units specified in column headers

---

## Writing Quality Checklist

**Clarity:**
- [ ] Every sentence serves the narrative (no filler)
- [ ] Technical jargon is defined on first use
- [ ] Acronyms spelled out on first use
- [ ] Pronoun references are unambiguous

**Sentence-Level (Gopen & Swan Principles):**
- [ ] Familiar information at sentence start (topic position)
- [ ] Important new information at sentence end (stress position)
- [ ] Verb close to subject (no long gaps)
- [ ] Active voice preferred (passive only when appropriate)
- [ ] Parallel structures for parallel ideas

**Paragraph-Level:**
- [ ] Each paragraph has a clear topic (issue sentence at start)
- [ ] Sentences within paragraph flow logically (old-to-new information)
- [ ] Paragraph ends with key takeaway (point sentence)
- [ ] Transitions between paragraphs are smooth

**Notation and Math:**
- [ ] All symbols defined on first use
- [ ] Consistent notation throughout
- [ ] Equations integrated into sentences (with punctuation)
- [ ] Variables defined immediately after equations ("where x is...")

**Language:**
- [ ] Appropriate verb tense for each section
- [ ] First person plural ("we") used consistently
- [ ] Precise language (avoid "very good", "much faster" without numbers)
- [ ] No marketing language ("amazing", "dramatically")
- [ ] No unsupported claims

---

## Pre-Submission Checklist

**Content Completeness:**
- [ ] All sections present and complete
- [ ] All figures/tables referenced in text
- [ ] All citations formatted correctly
- [ ] Code availability statement included
- [ ] Ethics statement included (if required)
- [ ] Acknowledgments included (if not anonymous)

**Formatting:**
- [ ] Follows venue template exactly
- [ ] Within page limits
- [ ] Margins correct
- [ ] Fonts correct
- [ ] Line spacing correct
- [ ] Bibliography formatted per venue requirements

**Anonymization (if double-blind):**
- [ ] Author names and affiliations removed
- [ ] Acknowledgments removed or anonymized
- [ ] Self-citations anonymized
- [ ] URLs anonymized (use anonymous GitHub repos)
- [ ] No identifiable details in text

**Reproducibility:**
- [ ] Sufficient detail for reimplementation
- [ ] Hyperparameters reported
- [ ] Dataset information complete
- [ ] Code/data availability stated

**Final Quality Checks:**
- [ ] Spell-check run
- [ ] Grammar check run
- [ ] All co-authors reviewed
- [ ] Mock reviews conducted (if possible)
- [ ] Checked against venue requirements one final time

**Supplementary Material (if applicable):**
- [ ] Referenced correctly in main paper
- [ ] Anonymized (if required)
- [ ] Within size limits
- [ ] Properly formatted

---

## Revision Checklist (After Reviews)

**Addressing Reviewer Comments:**
- [ ] Every reviewer comment addressed in rebuttal or revision
- [ ] Changes clearly marked (if required by venue)
- [ ] Response letter lists all changes made
- [ ] Tone is respectful and professional

**Common Revision Tasks:**
- [ ] Additional experiments requested by reviewers
- [ ] Clarifications of confusing sections
- [ ] Additional baselines or comparisons
- [ ] Expanded related work
- [ ] Fixed notation inconsistencies
- [ ] Improved figure/table clarity

**Meta-Review Integration:**
- [ ] Address meta-reviewer's synthesis and concerns
- [ ] Prioritize major issues over minor ones
- [ ] If revisions exceed page limits, move content to appendix

---

## Long-Form Paper Checklist (Journal/Thesis)

**Additional Requirements Beyond Conference Papers:**
- [ ] Comprehensive literature review (not just related work)
- [ ] Deeper methodology explanation
  - [ ] Detailed derivations
  - [ ] More implementation details
- [ ] Extended experimental evaluation
  - [ ] More datasets
  - [ ] More baselines
  - [ ] Additional ablations
  - [ ] Sensitivity analyses
- [ ] Longer discussion section
  - [ ] Deeper implications
  - [ ] Lessons learned
  - [ ] Can include negative results
- [ ] Appendices with proofs, derivations, additional results
- [ ] More comprehensive future work section

---

## Quick Pre-Draft Planning Checklist

**Before Writing, Ensure You Can Answer:**
- [ ] What is the single main contribution? (1 sentence)
- [ ] What problem does this solve, and why does it matter?
- [ ] What are the 3 key results that support the contribution?
- [ ] What are the closest 3-5 papers, and how is this different?
- [ ] What figure/table will best demonstrate the main result?
- [ ] What are the 2-3 ablations that justify design choices?
- [ ] What are the main limitations?
- [ ] Who is the target audience, and what venue is appropriate?

If you can't answer these, clarify before writing.

---

## Emergency "Paper Due Tomorrow" Checklist

**Priority 1 (Must Have):**
- [ ] Abstract clearly states contribution and results
- [ ] Introduction ends with explicit contribution statement
- [ ] Main results table is clear and shows key comparisons
- [ ] At least one ablation study included
- [ ] Figures are readable and referenced in text
- [ ] Bibliography is correctly formatted
- [ ] Follows venue formatting requirements

**Priority 2 (Should Have):**
- [ ] Related work positions your contribution
- [ ] All design choices are justified (ablations or rationale)
- [ ] Limitations are acknowledged
- [ ] Spell-check and grammar-check completed

**Priority 3 (Nice to Have):**
- [ ] Extended analysis and qualitative results
- [ ] Polished writing (sentence-level clarity)
- [ ] Additional experiments probing edge cases

**In a time crunch, focus on Priority 1, then 2. Priority 3 can wait for revision.**

---

## Summary: The Golden Rules

1. **Clarity**: Every sentence should serve the narrative arc (Problem → Solution → Evidence → Implications)
2. **Honesty**: Acknowledge limitations; don't oversell
3. **Reproducibility**: Provide enough detail for others to replicate
4. **Rigor**: Support every claim with evidence (experiments, citations, or formal analysis)
5. **Consistency**: Notation, style, formatting throughout

**When in doubt, ask:**
- "Does this advance the story?"
- "Can a reader reproduce this?"
- "Is this claim supported?"
- "Is this the simplest, clearest way to say it?"
