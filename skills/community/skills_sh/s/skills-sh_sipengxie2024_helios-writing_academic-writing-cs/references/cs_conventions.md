# Computer Science Writing Conventions

## Overview

Computer science writing follows general academic norms but has field-specific conventions that vary by subfield (AI/ML, systems, theory, HCI, security, etc.). This guide covers shared conventions and highlights subfield variations.

---

## 1. Notation and Mathematical Writing

### 1.1 General Principles

**Consistency is paramount:**
- Define all symbols on first use
- Use the same symbol for the same concept throughout
- Create a notation table for papers with >20 symbols (appendix)

**Common CS notation conventions:**

| Concept | Typical Notation | Notes |
|---------|------------------|-------|
| Sets | Capital letters: `S`, `V`, `E` | Calligraphic for special sets: `𝒳`, `𝒴` |
| Vectors | Bold lowercase: **x**, **y** | Or arrow notation: `x⃗` |
| Matrices | Bold capitals: **A**, **W** | Or sans-serif: `𝖠`, `𝖶` |
| Scalars | Italic lowercase: `x`, `α`, `λ` | Greek for hyperparameters |
| Functions | Italic lowercase: `f(x)`, `g(·)` | Calligraphic for special: `ℒ`, `ℋ` |
| Probability | `P(X)` or `Pr(X)` | Use consistently |
| Expected value | `E[X]` or `𝔼[X]` | Use consistently |
| Cardinality | `|S|` or `#S` | Use consistently |
| Complexity | `O(n)`, `Θ(n)`, `Ω(n)` | Big-O family |

### 1.2 Integrating Math into Text

**Rule: Treat equations as part of the sentence.**

**Bad:**
> The loss function is
>
> ℒ = -∑ᵢ yᵢ log ŷᵢ
>
> This is the cross-entropy loss.

**Good:**
> The loss function is the cross-entropy:
>
> ℒ = -∑ᵢ yᵢ log ŷᵢ,
>
> where yᵢ is the true label and ŷᵢ is the predicted probability.

**Key practices:**
- Add punctuation (commas, periods) to equations
- Define all variables immediately after the equation
- Use "where" clauses for variable definitions

### 1.3 Algorithm Presentation

**Use pseudocode or algorithm boxes (e.g., algorithmicx package in LaTeX).**

**Structure:**
```
Algorithm 1: Descriptive Name
Input: List all inputs
Output: What the algorithm returns
1: Initialize variables
2: for each item in collection do
3:    Perform action
4:    if condition then
5:       Take action
6:    end if
7: end for
8: return result
```

**Best practices:**
- **Clarity over brevity**: Use descriptive variable names
- **Abstraction level**: Match the paper's focus (high-level for concepts; detailed for novel algorithms)
- **Consistency**: If you use pseudocode, use it throughout
- **Complexity annotation**: Indicate time/space complexity in caption if relevant

---

## 2. Figures and Tables

### 2.1 General Guidelines

**Every figure/table must:**
- Be referenced in the text before it appears
- Have a self-contained caption (reader understands without reading main text)
- Use readable fonts (≥8pt) and clear labels
- Follow consistent visual style throughout the paper

### 2.2 Figures

**Common figure types in CS:**

#### Result Plots
- **Bar charts**: Comparing methods across metrics
- **Line plots**: Showing trends (e.g., training curves, scaling behavior)
- **Heatmaps**: Visualizing matrices (attention, confusion, correlations)
- **Scatter plots**: Showing relationships between variables

**Best practices:**
- **Axis labels**: Always include units (e.g., "Time (seconds)", "Accuracy (%)")
- **Legends**: Place inside plot if space allows; otherwise, in caption
- **Error bars/bands**: Show standard deviation or confidence intervals
- **Color blindness**: Use colorblind-friendly palettes (avoid red-green)
- **Resolution**: Vector formats (PDF, SVG) preferred; raster ≥300 DPI

#### Architecture Diagrams
- **Purpose**: Show system/model structure
- **Style**: Block diagrams with clear data flow
- **Labels**: Annotate dimensions (e.g., "256-dim embedding") and operations (e.g., "Conv 3×3")

**Example caption:**
> Figure 1: Architecture of our model. The input image (224×224) is processed by a ResNet-50 backbone, followed by a custom attention module (Section 3.2), producing a 512-dimensional feature vector. FC denotes fully-connected layers.

#### Qualitative Results
- **Purpose**: Show visual outputs (images, text, graphs)
- **Organization**: Side-by-side comparison (Ground Truth | Baseline | Ours)
- **Selection**: Choose representative examples, including failure cases

### 2.3 Tables

**Standard table formats:**

#### Main Results Table

**Structure:**
- Methods in rows, metrics in columns (or vice versa)
- **Bold** best results; underline second-best
- Include standard deviations (e.g., "92.3 ± 0.5")
- Sort by performance (best first) or logical grouping

**Example:**

| Method | Accuracy (%) | F1 Score | Training Time (hrs) |
|--------|--------------|----------|---------------------|
| **Ours** | **94.2 ± 0.3** | **0.93** | 2.1 |
| Baseline A | 91.5 ± 0.5 | 0.89 | 1.8 |
| Baseline B | 90.1 ± 0.4 | 0.87 | 3.5 |

**Caption:**
> Table 1: Comparison on ImageNet. Our method achieves the highest accuracy while maintaining competitive training time. Results averaged over 3 runs.

#### Ablation Study Table

**Purpose:** Show effect of removing/modifying components.

**Structure:**
- Full model at top
- Each row removes one component
- Clearly indicate what's changed

**Example:**

| Configuration | Accuracy (%) | ΔAccuracy |
|---------------|--------------|-----------|
| Full model | 94.2 | — |
| w/o attention module | 91.3 | -2.9 |
| w/o data augmentation | 92.1 | -2.1 |
| w/o both | 89.5 | -4.7 |

**Caption:**
> Table 2: Ablation study. Removing the attention module causes the largest performance drop, demonstrating its importance.

### 2.4 Figure/Table Placement

**Conference papers:** Figures/tables can be placed at top/bottom of columns or pages (use `[t]` or `[b]` in LaTeX).

**Journals:** More flexible; can span two columns if necessary.

**Rule:** Always reference before placement.

**Example:**
> Figure 3 shows the training dynamics. Our method converges faster than baselines...

---

## 3. Citations and References

### 3.1 Citation Style

**In-text citations:**
- **CS standard:** Author-year (ACM, IEEE style) or numbered [1]
- **Check venue requirements:** ACL uses (Author, Year); ICML uses [1]

**Common patterns:**

**Integral (author as subject):**
> LeCun et al. (1998) proposed convolutional neural networks for image classification.

**Non-integral (claim as focus):**
> Convolutional neural networks have proven effective for image classification [LeCun et al., 1998; Krizhevsky et al., 2012].

**Referring to multiple works:**
- **Related work**: Cite 3-5 representative papers, not exhaustive
- **Grouping**: Use semicolons: [1; 3; 5] or [Smith, 2020; Jones, 2021]

### 3.2 Reference List Quality

**Essential elements:**
- Authors (all, or "et al." if >10)
- Title (exact, including capitalization for acronyms)
- Venue (conference/journal full name, not abbreviations)
- Year
- Pages (if applicable)

**Common mistakes:**
- Inconsistent formatting
- Missing venue information
- Using arXiv when published version exists
- Broken URLs or DOIs

**Best practice:** Use BibTeX and a standard `.bst` file (e.g., `ACM-Reference-Format.bst`).

### 3.3 What to Cite

**Always cite:**
- Prior work you build on or compare against
- Methods/datasets/benchmarks you use
- Theoretical results you invoke
- Claims that are not your original contribution

**Don't over-cite:**
- Common knowledge (e.g., "Neural networks consist of layers")
- Your own prior work (cite once, not repeatedly)

---

## 4. Code and Reproducibility

### 4.1 Code Availability

**Modern expectation:** Code should be released (GitHub, Zenodo, etc.).

**In paper:**
- **Conference submission:** Anonymize or provide anonymous repo (e.g., Anonymous GitHub)
- **Camera-ready:** Include non-anonymized link

**Statement in paper:**
> Code is available at [URL].

### 4.2 Reproducibility Sections

**Many venues now require or encourage reproducibility statements.**

**Typical content:**
- Hardware used (e.g., "4× NVIDIA A100 GPUs")
- Software versions (e.g., "PyTorch 2.0, Python 3.10")
- Hyperparameters and training procedures
- Random seeds and number of runs
- Datasets and preprocessing steps

**Placement:**
- Main paper (if space permits)
- Appendix (common for ML conferences)
- Supplementary material

---

## 5. Subfield-Specific Conventions

### 5.1 Machine Learning / AI

**Emphasis on:**
- **Empirical evaluation**: Multiple datasets, strong baselines, statistical significance
- **Ablation studies**: Demonstrating each component's contribution
- **Hyperparameter sensitivity**: Showing robustness to hyperparameter choices
- **Computational cost**: Training time, inference time, parameter count

**Common figures:**
- Training/validation curves (loss, accuracy over epochs)
- t-SNE/UMAP embeddings (for representation learning)
- Attention visualizations (for interpretability)

**Notation conventions:**
- Bold for vectors/matrices: **x**, **W**
- `ℒ` for loss functions
- `θ` for model parameters
- `𝒟` for datasets

### 5.2 Systems / Networking

**Emphasis on:**
- **Scalability**: How performance changes with load, data size, number of nodes
- **Throughput and latency**: Concrete measurements (ops/sec, ms)
- **System design**: Architecture diagrams showing components and interactions
- **Overheads**: Quantifying costs of the approach

**Common figures:**
- System architecture block diagrams
- Performance vs. load (throughput, latency under varying conditions)
- CDF plots (cumulative distribution functions) for latency

**Writing style:**
- More detailed implementation description
- Focus on "how" (not just "what")
- Discuss deployment considerations

### 5.3 Theory / Algorithms

**Emphasis on:**
- **Formal definitions**: Precise problem statements
- **Theorems and proofs**: Rigorous analysis
- **Complexity bounds**: Worst-case, average-case, amortized
- **Comparison to prior bounds**: Improvements over existing results

**Structure:**
- **Problem Definition** section with formal notation
- **Main Results** section stating theorems
- **Proof Sketch** in main paper; full proofs in appendix

**Notation conventions:**
- `O(·)`, `Θ(·)`, `Ω(·)` for asymptotic complexity
- Use logical symbols: `∀`, `∃`, `∈`, `∉`, `⊆`
- Clearly state assumptions

### 5.4 HCI / Visualization

**Emphasis on:**
- **User studies**: Methodology, participants, tasks, metrics
- **Qualitative feedback**: Quotes from participants, thematic analysis
- **Visual design**: Screenshots, interactive prototypes
- **Usability metrics**: Task completion time, error rates, user satisfaction scores

**Common figures:**
- Interface screenshots (before/after, comparisons)
- User study setup and tasks
- Qualitative results (word clouds, thematic maps)

**Writing style:**
- More narrative, user-centered
- Discuss design rationale and iterations
- Integrate qualitative and quantitative results

### 5.5 Security / Privacy

**Emphasis on:**
- **Threat models**: Clearly define adversary capabilities and goals
- **Attack scenarios**: Concrete examples and impact assessment
- **Defense mechanisms**: Detailed description and security analysis
- **Evaluation against attacks**: Red-team testing, penetration testing

**Common figures:**
- Threat model diagrams (attacker, defender, system components)
- Attack flow diagrams
- ROC curves (for detection methods)

**Notation conventions:**
- `𝒜` for adversary
- `Pr[E]` for probability of event E
- Security definitions using game-based notation

---

## 6. Language and Style

### 6.1 Verb Tense

**Follow these conventions:**

| Section | Tense | Example |
|---------|-------|---------|
| Abstract | Present (findings), Past (actions) | "We propose a method that **achieves** 95% accuracy. We **conducted** experiments on..." |
| Introduction | Present (facts), Past (prior work) | "Neural networks **are** widely used. Smith et al. **proposed** X in 2020." |
| Related Work | Past | "LeCun et al. **introduced** CNNs." |
| Method | Present | "Our algorithm **computes** X by..." |
| Experiments | Past | "We **trained** the model on ImageNet. The model **achieved** 92% accuracy." |
| Discussion | Present (interpretations) | "This result **suggests** that X **is** important." |
| Conclusion | Present (contributions) | "We **present** a method that **improves** X." |

### 6.2 Voice: Active vs. Passive

**Modern CS writing prefers active voice**, but passive is acceptable when:
- The agent is unknown or irrelevant: "The dataset was collected in 2020."
- Emphasizing the object: "Errors were reduced by 30%."
- Maintaining topic consistency: "Our model was trained on ImageNet. It was evaluated on five benchmarks."

**Active voice (preferred):**
> We trained the model using SGD.

**Passive voice (acceptable):**
> The model was trained using SGD.

### 6.3 Person: First vs. Third

**Modern CS writing uses first person plural ("we")** to describe the authors' work.

**Use "we":**
> We propose a novel attention mechanism.
> In Section 3, we describe our approach.

**Avoid "the authors":**
> The authors propose... ❌

**Exception:** Avoid "I" even for single-author papers (use "we").

### 6.4 Precision in Language

**Be specific, not vague:**

| Vague | Precise |
|-------|---------|
| "very good accuracy" | "92.3% accuracy" |
| "much faster" | "3× faster" or "reduces time from 10s to 3s" |
| "significant improvement" | "15% relative improvement (p < 0.01)" |
| "a lot of data" | "10 million samples" |

### 6.5 Common Pitfalls

**Avoid marketing language:**
- ❌ "Our amazing method dramatically outperforms all prior work."
- ✅ "Our method achieves 15% higher accuracy than the strongest baseline."

**Avoid unsupported claims:**
- ❌ "Our method is the first to solve X."
  - Unless you've done exhaustive literature review
- ✅ "To our knowledge, our method is the first to address X in the context of Y."

**Avoid ambiguous pronouns:**
- ❌ "We apply the model to the dataset. It improves performance."
  - What does "it" refer to?
- ✅ "We apply the model to the dataset. The model improves performance."

---

## 7. Anonymization (Double-Blind Review)

**Many CS conferences use double-blind review (ICML, NeurIPS, ICLR, etc.).**

**What to anonymize:**
- Author names and affiliations
- Acknowledgments (remove or anonymize)
- Self-citations that reveal identity
  - ❌ "In our prior work [Smith et al., 2023], we..."
  - ✅ "Prior work [Anonymous, 2023] proposed..."
- URLs to personal websites, GitHub repos (use anonymous repos)
- Identifiable details (e.g., "our institution's compute cluster")

**What NOT to anonymize:**
- Published prior work by others
- Publicly available datasets/benchmarks
- Standard methods and baselines

**Supplementary material:** Also must be anonymous.

---

## 8. Venue-Specific Guidelines

**Always read the venue's author guidelines:**
- Page limits (strict in most conferences)
- Formatting requirements (LaTeX templates)
- Anonymization rules
- Supplementary material policies
- Reproducibility requirements
- Ethical considerations statements

**Major CS venues:**

### Conferences
- **ML/AI:** NeurIPS, ICML, ICLR, CVPR, ICCV, ACL, EMNLP, AAAI, IJCAI
- **Systems:** OSDI, SOSP, NSDI, EuroSys, SIGCOMM, SIGMOD, VLDB
- **Theory:** FOCS, STOC, SODA
- **HCI:** CHI, UIST, UbiComp
- **Security:** IEEE S&P, USENIX Security, CCS, NDSS

### Journals
- **General:** Journal of the ACM (JACM), Communications of the ACM (CACM)
- **ML/AI:** JMLR, IEEE TPAMI, Neural Networks, AI Journal
- **Systems:** ACM TOCS, IEEE TPDS, ACM ToN
- **Theory:** SICOMP, Algorithmica
- **Interdisciplinary:** Science, Nature, PNAS (for high-impact CS work)

**Submission cycle:**
- **Conferences:** Annual deadlines, fast turnaround (2-4 months)
- **Journals:** Rolling submission, longer review (6-12 months)

---

## 9. Ethical Considerations

**Many venues now require ethics statements.**

**Common topics:**
- **Broader impacts**: Potential positive and negative societal impacts
- **Data privacy**: How human data is collected, stored, anonymized
- **Bias and fairness**: Potential biases in datasets or models
- **Environmental cost**: Energy consumption for large-scale experiments
- **Dual use**: Potential misuse of the technology

**Placement:**
- Dedicated section (often required for NeurIPS, ACL)
- Appendix
- Checklist (NeurIPS Paper Checklist)

**Example statement:**
> **Broader Impacts.** Our method for detecting misinformation could be used to improve content moderation on social media platforms. However, it may also be misused for censorship or to suppress legitimate dissent. We recommend transparent deployment with human oversight to mitigate these risks.

---

## 10. Checklist: CS Paper Quality

### Content
- [ ] Clear problem statement and motivation
- [ ] Well-defined contributions (specific, not vague)
- [ ] Sufficient related work (representative, not exhaustive)
- [ ] Reproducible methodology (enough detail for reimplementation)
- [ ] Strong empirical evaluation (multiple datasets, baselines, ablations)
- [ ] Honest discussion of limitations

### Presentation
- [ ] Consistent notation throughout
- [ ] All figures/tables referenced in text
- [ ] Self-contained captions
- [ ] High-quality figures (readable, colorblind-friendly)
- [ ] Proper citation format
- [ ] Appropriate verb tense and voice
- [ ] No marketing language or unsupported claims

### Technical Quality
- [ ] Correct use of mathematical notation
- [ ] Statistical significance reported (if applicable)
- [ ] Computational cost discussed (if relevant)
- [ ] Code availability stated
- [ ] Ethical considerations addressed (if required)

### Compliance
- [ ] Follows venue formatting requirements
- [ ] Within page limits
- [ ] Properly anonymized (if double-blind)
- [ ] Supplementary material complies with rules
- [ ] Ethics statement included (if required)

---

## Further Resources

- **Style guides:**
  - ACM Author Guidelines: https://www.acm.org/publications/authors
  - IEEE Author Center: https://journals.ieeeauthorcenter.ieee.org/

- **LaTeX templates:**
  - Overleaf (search for venue-specific templates)
  - Venue websites (official templates)

- **Example papers:**
  - Read award-winning papers from target venues
  - Analyze structure, figures, writing style

- **Writing tools:**
  - Grammarly (grammar and style)
  - Hemingway Editor (readability)
  - Overleaf (collaborative LaTeX)
  - Git for version control

- **Peer feedback:**
  - Internal lab reviews
  - Writing groups or seminars
  - Mock reviews before submission
