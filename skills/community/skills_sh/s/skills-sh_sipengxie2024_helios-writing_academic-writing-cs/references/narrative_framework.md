# Academic Paper Narrative Framework

## Core Principle

A scientific paper tells a story with a clear narrative arc:

**Problem → Solution → Evidence → Implications**

Every element of the paper must advance this narrative. Readers should understand:
1. What problem exists (and why it matters)
2. What solution the paper proposes
3. What evidence supports the solution
4. What the implications are for the field

---

## Section-Level Narrative Structure

### Abstract (4-Sentence Structure)

The abstract is a compressed version of the entire narrative arc:

1. **Context (1 sentence)**: Broad area and why it matters
2. **Gap/Problem (1 sentence)**: What's missing or broken
3. **Contribution (1-2 sentences)**: What this paper provides
4. **Impact (1 sentence)**: Key results or implications

**Example:**
> Deep learning models require massive labeled datasets (context). However, labeling is expensive and error-prone (problem). We propose SemiSupervised Training with Consistency Regularization (STCR), which leverages unlabeled data by enforcing prediction consistency under perturbations (contribution). On ImageNet with 10% labels, STCR achieves 82% accuracy, outperforming prior semi-supervised methods by 7% (impact).

### Introduction (Funnel Structure)

**Goal:** Lead readers from broad context to specific contribution.

Structure (typically 4-6 paragraphs):

1. **Opening (1 para)**: Broad problem domain and importance
   - Why does this area matter to the CS community?
   - What are the high-level challenges?

2. **Background & Motivation (1-2 paras)**: Narrow down
   - What specific problem are we solving?
   - Why existing approaches fall short (brief)
   - Concrete example or scenario illustrating the problem

3. **Gap Statement (0.5-1 para)**: Explicit statement of what's missing
   - "However, current approaches lack..."
   - "An open question is..."

4. **Contribution Overview (1 para)**: What this paper provides
   - "In this paper, we present..."
   - High-level description of the approach
   - Key insight or novelty

5. **Results Summary (0.5 para)**: Main empirical findings
   - 2-3 bullet points or brief sentences
   - Concrete numbers demonstrating effectiveness

6. **Paper Organization (0.5 para)**: Roadmap
   - "The rest of the paper is organized as follows..."
   - Optional for conferences; expected for journals

**Critical Requirements:**
- By the end of paragraph 4, readers must understand the contribution
- Don't oversell: be precise about scope and claims
- For systems/ML papers: include a figure (architecture or key result) early

### Related Work

**Goal:** Position the paper within the research landscape.

**Two Viable Strategies:**

#### Strategy A: Related Work After Introduction (Common in ML/AI)
- Advantages: Readers understand the contribution before seeing comparisons
- Structure: Organize by theme or approach, conclude with positioning

#### Strategy B: Related Work Before Conclusion (Common in Systems/Theory)
- Advantages: Better flow if the contribution depends on deep technical content
- Structure: Same thematic organization

**Content Organization:**

1. **Taxonomy**: Group related work into 3-5 categories
   - E.g., "Supervised Methods," "Self-Supervised Methods," "Semi-Supervised Methods"

2. **Per-Category Structure**:
   - Describe the general approach
   - Cite representative works with 1-sentence descriptions
   - Point out limitations relevant to your contribution

3. **Positioning Paragraph** (crucial):
   - "In contrast to [X], our approach..."
   - Clearly articulate differences and advantages
   - Avoid claims you can't support empirically

**Common Pitfalls:**
- Laundry list of citations without synthesis
- Failing to connect related work to your contribution
- Being dismissive of prior work (respect, but differentiate)

### Methodology

**Goal:** Enable reproduction and convey technical insight.

**Dual Objectives:**
1. **Reproducibility**: Provide enough detail for reimplementation
2. **Intuition**: Explain why the approach works

**Structure (Adapt Based on Paper Type):**

#### For Algorithmic/ML Papers:
1. **Problem Formulation**: Formal definitions, notation
2. **High-Level Overview**: 1-2 paragraphs + figure
3. **Detailed Design**: Algorithm boxes, mathematical derivations
4. **Implementation Details**: Hyperparameters, architecture choices
5. **Complexity Analysis** (if relevant): Time/space bounds

#### For Systems Papers:
1. **Architecture Overview**: Block diagram + walkthrough
2. **Component Design**: Per-component deep dive
3. **Key Mechanisms**: Protocols, algorithms, data structures
4. **Implementation**: Language, libraries, optimizations

#### For Empirical/Measurement Papers:
1. **Experimental Design**: Hypotheses, variables, controls
2. **Data Collection**: Sources, preprocessing, cleaning
3. **Analysis Methods**: Statistical tests, metrics
4. **Threats to Validity**: Limitations and mitigation

**Writing Principles:**
- Use formal notation consistently (define all symbols)
- Balance detail: enough for experts to reproduce, not overwhelming for non-experts
- Use examples/figures to illustrate complex mechanisms
- Highlight design choices and trade-offs

### Experiments/Results

**Goal:** Provide evidence that the solution works.

**Standard Structure:**

1. **Experimental Setup** (subsection)
   - Datasets: Size, domain, train/val/test splits
   - Baselines: What you compare against (include citations)
   - Metrics: What you measure and why
   - Hardware/Software: Infrastructure details
   - Hyperparameters: How selected (grid search, validation set, etc.)

2. **Main Results** (subsection)
   - Table/figure showing primary comparison
   - Text: "Table 1 shows that our method outperforms..."
   - Highlight key findings (e.g., "achieves 15% improvement over...")

3. **Ablation Studies** (subsection, critical for ML/systems)
   - Remove or modify components to show their necessity
   - Table: "Effect of removing component X"
   - Demonstrates that design choices are justified

4. **Analysis** (subsection)
   - Dig deeper into results:
     - Where does the method excel? Where does it fail?
     - Qualitative analysis (e.g., visualize learned representations)
     - Error analysis: Common failure modes
   - Additional experiments probing specific aspects

5. **Computational Cost** (subsection, if relevant)
   - Training time, inference time, memory usage
   - Comparison with baselines

**Presentation Best Practices:**

- **Tables**: Clean, readable, bold best results, include standard deviations
- **Figures**: High-resolution, readable fonts, informative captions
- **Statistical Significance**: Report confidence intervals or p-values
- **Honesty**: Report negative results; acknowledge limitations

**Common Mistakes:**
- Cherry-picking results without justification
- Missing ablations (readers won't believe your design choices)
- Insufficient analysis (just showing numbers isn't enough)
- Ignoring computational cost

### Discussion

**Goal:** Interpret results and explore implications.

**Content (typically 2-4 paragraphs):**

1. **Summary of Findings**
   - Restate key empirical results
   - "Our experiments demonstrate that..."

2. **Interpretation**
   - Why does the method work?
   - What insights do the results provide?
   - Connect back to the problem motivation

3. **Limitations**
   - Be upfront about scope restrictions
   - What scenarios does the method not handle?
   - What assumptions are made?

4. **Broader Implications**
   - How does this advance the field?
   - What new research directions does it open?
   - Potential real-world applications

**Tone:** Balanced—confident but not overselling. Acknowledge limitations honestly.

### Conclusion

**Goal:** Concise summary and forward look.

**Structure (typically 2-3 paragraphs):**

1. **Restate Contribution** (1 para)
   - Recap the problem and solution
   - Summarize key findings
   - "In this paper, we presented [X], which addresses [Y] by [Z]."

2. **Broader Impact** (0.5-1 para)
   - Reiterate significance
   - Potential applications

3. **Future Work** (0.5-1 para)
   - Open questions
   - Extensions or improvements
   - Avoid: "In future work, we will..." (implies current work is incomplete)
   - Prefer: "An interesting direction is..."

**Do NOT:**
- Introduce new ideas or results
- Repeat abstract verbatim
- Be vague ("We did some cool stuff")

---

## Cross-Section Consistency

### Notation
- Define all symbols on first use
- Use consistent notation throughout
- Maintain a notation table (appendix) for complex papers

### Claims and Evidence
- Every claim in Intro/Abstract must be supported in Results
- Don't promise more than you deliver

### Figures and Tables
- Reference all figures/tables in text
- Captions should be self-contained
- Maintain consistent visual style

---

## Paper Types and Adaptations

### Conference Papers (6-8 pages, single-blind or double-blind)
- Tighter structure, less background
- Focus on key contribution and results
- Supplementary material for additional experiments

### Journal Papers (15-30 pages, typically single-blind)
- More comprehensive related work
- Deeper methodology explanation
- Extensive experimental evaluation
- Detailed proofs/derivations in appendix

### Thesis Chapters (flexible length)
- Comprehensive literature review
- More background material
- Extended discussion and future directions
- Can include negative results and lessons learned

---

## Common Structural Anti-Patterns

1. **"Inverted Pyramid"**: Starting narrow and expanding
   - Fix: Always funnel from broad to specific

2. **"Missing Bridge"**: No clear connection between sections
   - Fix: Use transition sentences; maintain narrative thread

3. **"Method Dump"**: Throwing equations without intuition
   - Fix: Always lead with intuition, follow with formalism

4. **"Data Vomit"**: Tables/figures without analysis
   - Fix: Every result needs textual interpretation

5. **"Scope Creep"**: Contribution statement too broad or vague
   - Fix: Be specific about what the paper does (and doesn't) do

---

## Checklist: Does Your Paper Have a Clear Narrative?

- [ ] Can a reader identify the single main contribution in 30 seconds?
- [ ] Does every section advance the core narrative?
- [ ] Are claims in the abstract/introduction supported by results?
- [ ] Would removing any major section break the story?
- [ ] Can a reader follow the logical flow without jumping back and forth?
