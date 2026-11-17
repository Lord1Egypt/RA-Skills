# 心理学研究方法参考手册

This reference document catalogs common experimental paradigms, research designs, statistical methods, and validity threat checklists used in psychology research. Consult this when analyzing a paper's methodology.

---

## 1. Common Experimental Paradigms

### 1.1 Cognitive Psychology Paradigms

| Paradigm | Task Description | Typical DV | What It Measures |
|----------|-----------------|------------|-----------------|
| **Stroop** | Name ink color of color words (congruent/incongruent) | RT, accuracy | Interference / inhibitory control |
| **Simon** | Respond to non-spatial stimulus attribute; stimulus position is congruent/incongruent with response | RT, accuracy | Spatial-response compatibility |
| **Flanker (Eriksen)** | Identify central target flanked by congruent/incongruent distractors | RT, accuracy | Selective attention / interference |
| **Posner Cueing** | Detect target after valid/invalid/neutral spatial cue | RT | Covert spatial attention |
| **N-back** | Indicate if current stimulus matches one presented N items back | RT, accuracy (d') | Working memory |
| **Lexical Decision** | Decide if letter string is a real word or non-word | RT, accuracy | Lexical access / semantic priming |
| **Go/No-Go** | Respond to "go" stimuli, withhold to "no-go" stimuli | RT, commission errors | Response inhibition |
| **Stop Signal** | Go task with occasional stop signal | SSRT | Inhibitory control (action cancellation) |
| **Task Switching** | Switch between two task rules | Switch cost (RT) | Cognitive flexibility |
| **Visual Search** | Find target among distractors | RT, accuracy | Attentional guidance |
| **Dot-Probe** | Detect probe replacing threat/neutral stimulus pair | RT | Attentional bias |
| **IAT (Implicit Association Test)** | Categorize paired concepts (e.g., flower/insect × pleasant/unpleasant) | D-score | Implicit attitudes |
| **AX-CPT** | Maintain context cue (A) to respond to probe (X) | RT, accuracy | Context processing / cognitive control |
| **Oddball** | Detect infrequent target among frequent standards | P300 ERP | Attention / novelty detection |

### 1.2 Social Psychology Paradigms

| Paradigm | Task Description | Typical DV | What It Measures |
|----------|-----------------|------------|-----------------|
| **Prisoner's Dilemma** | Choose cooperate/deflect; outcome depends on partner's choice | Cooperation rate | Social decision-making / trust |
| **Ultimatum Game** | Proposer offers split; responder accepts/rejects | Offer amount, rejection rate | Fairness / social norm |
| **Trust Game** | Investor sends money; trustee returns some | Amount sent / returned | Interpersonal trust |
| **Priming (social)** | Exposure to prime stimulus affects subsequent behavior/judgment | Rating, RT | Automatic activation of constructs |
| **False Consensus** | Estimate how many others share one's own preference | Percentage estimate | Social projection |
| **Minimal Group** | Arbitrary group assignment → in-group favoritism | Resource allocation | Intergroup bias |
| **Bystander Intervention** | Emergency scenario; measure helping behavior | Help latency/rate | Diffusion of responsibility |
| **Prisoner's Dilemma variants** | Iterated, n-player, public goods | Cooperation rate | Cooperation / free-riding |

### 1.3 Developmental Psychology Paradigms

| Paradigm | Task Description | Typical DV | What It Measures |
|----------|-----------------|------------|-----------------|
| **Preferential Looking / Habituation** | Present two stimuli; measure looking time | Looking time | Discrimination / preference |
| **Violation of Expectation** | Show expected vs. unexpected event | Looking time | Expectation / physical reasoning |
| **False Belief (Sally-Anne)** | Predict actor's behavior based on false belief | Pass/fail | Theory of Mind |
| **A-not-B Task** | Find hidden object at A, then B | Search location | Object permanence / executive function |
| **Delayed Gratification (Marshmallow Test)** | Wait for larger reward or take smaller now | Wait time | Self-control / delay ability |
| **Dimensional Change Card Sort (DCCS)** | Sort cards by one dimension, then switch | Sort accuracy | Cognitive flexibility |

### 1.4 Clinical / Affective Psychology Paradigms

| Paradigm | Task Description | Typical DV | What It Measures |
|----------|-----------------|------------|-----------------|
| **Emotional Stroop** | Name color of emotionally valenced words | RT | Attentional bias to emotional stimuli |
| **Affective Priming** | Prime with emotional stimulus; evaluate target | RT | Affective associations |
| **Fear Conditioning** | Pair CS with aversive US; measure CR | SCR, FPS, startle | Fear learning / extinction |
| **Self-Referential Encoding** | Judge adjectives as self-descriptive | Recall, RT | Self-concept / memory |
| **Emotion Regulation** | Reappraise / suppress emotional response | Self-report, physiology | Emotion regulation strategies |

### 1.5 Neuroimaging / Psychophysiology Paradigms

| Paradigm | Method | Typical DV | What It Measures |
|----------|--------|------------|-----------------|
| **Resting-state fMRI** | fMRI during rest | FC (functional connectivity) | Intrinsic brain networks |
| **Event-related potentials (ERP)** | EEG during cognitive task | P300, N400, ERN, LPP | Time-locked neural activity |
| **Galvanic Skin Response (GSR/SCR)** | Skin conductance electrodes | SCR amplitude | Arousal |
| **Eye Tracking** | Infrared eye tracking | Fixation, saccade, pupil | Visual attention / gaze patterns |
| **Heart Rate Variability (HRV)** | ECG | RMSSD, HF-HRV | Autonomic regulation |

---

## 2. Research Design Types

### 2.1 Experimental Designs

| Design | Description | Key Feature |
|--------|-------------|-------------|
| **Between-subjects** | Each participant in one condition only | No order effects; needs more participants |
| **Within-subjects (repeated measures)** | Each participant in all conditions | Order effects possible; fewer participants |
| **Mixed design** | At least one between and one within factor | Common in psychology |
| **Randomized controlled trial (RCT)** | Random assignment to treatment/control | Gold standard for causality |
| **Quasi-experimental** | Non-random assignment; pre-existing groups | Lower internal validity |
| **Single-subject / case design** | Intensive study of one or few subjects | A-B-A-B reversal, multiple baseline |

### 2.2 Non-Experimental Designs

| Design | Description | Key Feature |
|--------|-------------|-------------|
| **Correlational** | Measure relationship between variables | No causal inference |
| **Cross-sectional** | Single time point | Snapshot; no temporal precedence |
| **Longitudinal** | Multiple time points | Can infer temporal order |
| **Retrospective** | Look back at past events | Recall bias risk |
| **Prospective** | Follow forward in time | Better temporal inference |
| **Meta-analysis** | Synthesize effect sizes across studies | Systematic, quantitative review |

### 2.3 Design Decision Criteria

To classify a study's design, ask:
1. Were variables manipulated or only measured? (experiment vs. observational)
2. Was random assignment used? (true experiment vs. quasi)
3. Did each participant experience all conditions? (within vs. between)
4. How many time points were measured? (cross-sectional vs. longitudinal)
5. Is the unit of analysis individual or group?

---

## 3. Common Statistical Methods

### 3.1 Descriptive Statistics
- Mean, median, mode, SD, range, skewness, kurtosis

### 3.2 Inferential Tests

| Test | Use Case | Key Output |
|------|----------|------------|
| **Independent t-test** | Compare two independent groups | t, df, p, d |
| **Paired t-test** | Compare two related conditions | t, df, p, d |
| **One-way ANOVA** | Compare 3+ independent groups | F, p, η² |
| **Repeated measures ANOVA** | Compare 3+ within-subject conditions | F, p, partial η² |
| **Mixed ANOVA** | Between × within factors | F, p, partial η² |
| **ANCOVA** | ANOVA with covariate(s) | F, p, partial η² |
| **MANOVA** | Multiple DVs simultaneously | Wilks' Λ, F, p |
| **Pearson r** | Linear association between two continuous variables | r, p |
| **Spearman ρ** | Monotonic association (nonparametric) | ρ, p |
| **Chi-square (χ²)** | Association between categorical variables | χ², p, φ/Cramér's V |
| **Linear regression** | Predict continuous DV from IV(s) | β, R², F, p |
| **Logistic regression** | Predict binary DV from IV(s) | OR, Wald z, p |
| **Mediation analysis** | Test indirect effect through mediator | ab path, bootstrap CI |
| **Moderation analysis** | Test interaction effect on IV-DV relationship | Interaction β, p |
| **Structural Equation Modeling (SEM)** | Test complex path models with latent variables | χ², CFI, RMSEA, SRMR |
| **Hierarchical linear modeling (HLM)** | Nested data (e.g., students within schools) | ICC, fixed/random effects |
| **Bayesian analysis** | Probability-based inference | BF, posterior distribution |

### 3.3 Effect Size Benchmarks (Cohen, 1988)

| Effect Size | Small | Medium | Large |
|-------------|-------|--------|-------|
| Cohen's d | 0.20 | 0.50 | 0.80 |
| Pearson r | 0.10 | 0.30 | 0.50 |
| η² (ANOVA) | 0.01 | 0.06 | 0.14 |
| OR (odds ratio) | 1.68 | 3.47 | 6.71 |

### 3.4 Multiple Comparison Corrections
- **Bonferroni**: Divide α by number of comparisons (conservative)
- **Holm-Bonferroni**: Sequential, less conservative than Bonferroni
- **FDR (Benjamini-Hochberg)**: Controls false discovery rate
- **Tukey HSD**: For all pairwise post-hoc comparisons in ANOVA

---

## 4. Validity Threat Checklist

### 4.1 Internal Validity Threats
- **History**: External event between pre-test and post-test
- **Maturation**: Natural change over time (fatigue, development)
- **Testing**: Practice/familiarity from repeated testing
- **Instrumentation**: Change in measurement instrument
- **Statistical regression**: Regression to the mean with extreme groups
- **Selection bias**: Non-equivalent groups in quasi-experiments
- **Attrition/mortality**: Differential dropout between conditions
- **Demand characteristics**: Participants guess hypothesis and behave accordingly
- **Experimenter effects / expectancy**: Experimenter's expectations influence results
- **Confounding**: Third variable correlated with both IV and DV

### 4.2 External Validity Threats
- **Sample representativeness**: WEIRD samples (Western, Educated, Industrialized, Rich, Democratic)
- **Ecological validity**: Lab setting differs from real-world context
- **Temporal validity**: Findings may not generalize across time periods
- **Culture**: Findings may not generalize across cultures
- **Reactivity**: Awareness of being studied changes behavior (Hawthorne effect)

### 4.3 Construct Validity Threats
- **Operationalization gap**: Operational definition doesn't capture the construct
- **Mono-operation bias**: Single measure of a construct
- **Mono-method bias**: Single method for all measures
- **Social desirability**: Participants respond in socially acceptable way
- **Face validity vs. construct validity**: Appearing valid ≠ actually valid

### 4.4 Statistical Conclusion Validity Threats
- **Low statistical power**: Increased Type II error risk
- **Violated test assumptions**: Non-normality, heterogeneity of variance, sphericity
- **Fishing / p-hacking**: Multiple unplanned analyses without correction
- **Reliability of measures**: Low reliability attenuates effects
- **Restricted range**: Reduced variance limits effect detection

---

## 5. APA 7th Edition Citation Quick Reference

### Journal article (most common):
```
Author, A. A., & Author, B. B. (Year). Title of the article. Journal Name, Volume(Issue), pages. https://doi.org/xxxxx
```

### With 3+ authors (use "et al." for in-text after first):
```
Author, A. A., Author, B. B., & Author, C. C. (Year). Title of the article. Journal Name, Volume(Issue), pages. https://doi.org/xxxxx
```

### In-text citation:
- Parenthetical: (Author & Author, Year)
- Narrative: Author and Author (Year)
- 3+ authors: (Author et al., Year)

---

## 6. Quality Benchmarks for Psychology Papers

| Metric | Acceptable | Good | Excellent |
|--------|-----------|------|-----------|
| Statistical power (1-β) | ≥ .80 | ≥ .90 | ≥ .95 |
| Cronbach's α (reliability) | ≥ .70 | ≥ .80 | ≥ .90 |
| Test-retest reliability | ≥ .70 | ≥ .80 | ≥ .90 |
| Inter-rater reliability (Cohen's κ) | ≥ .60 | ≥ .75 | ≥ .90 |
| Sample size (experimental) | ≥ 30/cell | ≥ 50/cell | ≥ 100/cell |
| Pre-registration | None | Pre-registered | Pre-registered + open data |
