# Sentence-Level Clarity: The Science of Scientific Writing

## Foundation: Reader Expectations

**Core Principle (Gopen & Swan):**

"Science is often hard to read. Most scientists don't realize that the cause is not what they say but how they say it."

Readers bring expectations about where to find information in a sentence. When writing violates these expectations, comprehension suffers—even if the grammar is perfect.

---

## Key Structural Positions

### 1. Topic Position (Start of Sentence)

**What it is:** The first 5-7 words of a sentence.

**Reader Expectation:** This position contains:
- Information already known to the reader (backward-looking)
- The topic/subject of the sentence
- Context linking to the previous sentence

**Why it matters:** Readers use the topic position to:
- Orient themselves ("What is this sentence about?")
- Link to prior information (maintain coherence)
- Anticipate what comes next

**Bad Example:**
> High accuracy was achieved by our neural network on ImageNet, with 87% top-1 accuracy reported in Table 3.

The sentence starts with "High accuracy," which is new information. The reader doesn't know what to connect this to.

**Good Example:**
> Our neural network achieved high accuracy on ImageNet: 87% top-1 accuracy (Table 3).

Now the sentence starts with "Our neural network" (previously established topic), creating clear connection.

---

### 2. Stress Position (End of Sentence)

**What it is:** The final phrase/clause of a sentence, especially the last 5-7 words.

**Reader Expectation:** This position contains:
- The most important new information
- The point or conclusion of the sentence
- Information that will be elaborated in subsequent sentences

**Why it matters:** The stress position has maximum rhetorical power. Readers remember and emphasize what comes at the end.

**Bad Example:**
> The model achieves 92% accuracy on the test set, as shown in Table 2, exceeding prior work.

"Exceeding prior work" is the key point, but it's buried. "As shown in Table 2" is weak ending.

**Good Example:**
> As shown in Table 2, the model achieves 92% accuracy on the test set, exceeding prior work.

Now "exceeding prior work" occupies the stress position, receiving proper emphasis.

---

### 3. Verb Position (Close to Subject)

**What it is:** The main verb of the sentence.

**Reader Expectation:** The action/verb should appear soon after the subject.

**Why it matters:** Long gaps between subject and verb strain comprehension. Readers hold the subject in memory while waiting for the verb, causing cognitive load.

**Bad Example:**
> Our method, which leverages self-supervised learning on unlabeled data and incorporates a novel consistency regularization term to enforce prediction stability under augmentations, outperforms baselines.

The subject is "Our method," but the verb "outperforms" appears after 22 words. The reader must hold "Our method" in memory through the entire description.

**Good Example:**
> Our method outperforms baselines by leveraging self-supervised learning on unlabeled data and incorporating a novel consistency regularization term to enforce prediction stability.

The verb "outperforms" immediately follows the subject, clarifying the action early. The details follow naturally.

---

## Principle 1: Old-to-New Information Flow

### The Rule

**Place old/familiar information at the beginning; place new/unfamiliar information at the end.**

This creates a coherent information flow where each sentence builds on what came before.

### Example: Poor Flow

> Deep learning models require large datasets. Data collection is expensive. Label noise is a common problem in large datasets. Our method addresses this issue.

**Problem:** Each sentence introduces a new topic at the start, forcing readers to constantly reorient.

### Example: Good Flow

> Deep learning models require large datasets. These datasets are expensive to collect. Moreover, large-scale data collection introduces label noise. This noise degrades model performance. To address this problem, we propose a robust training method.

**Why it works:** Each sentence starts with a concept mentioned in the previous sentence ("These datasets" ← "large datasets"; "large-scale data collection" ← "collect"; "This noise" ← "label noise").

---

## Principle 2: Topic Consistency

### The Rule

**Keep the topic consistent across consecutive sentences when discussing the same subject.**

This reduces cognitive load and maintains narrative coherence.

### Example: Poor Topic Consistency

> We propose a new optimization algorithm. Convergence speed is improved by our method. Memory usage is also reduced significantly.

**Problem:** The topic shifts each sentence: "We" → "Convergence speed" → "Memory usage."

### Example: Good Topic Consistency

> We propose a new optimization algorithm. Our method improves convergence speed and significantly reduces memory usage.

**Why it works:** "We/Our method" remains the topic, creating a stable frame of reference.

### When to Shift Topics

Shift topics intentionally when:
1. Moving to a new subtopic (signal with transition: "However," "In contrast," etc.)
2. Zooming in on a specific aspect (signal with: "Specifically," "In particular," etc.)
3. Returning to a broader context (signal with: "Overall," "More generally," etc.)

---

## Principle 3: Agent-Action Alignment

### The Rule

**The grammatical subject (agent) should perform the action (verb).**

Passive voice and nominalization obscure who does what, reducing clarity.

### Example: Weak Agency

> The classification of images into categories is performed by the neural network.

**Problem:** The subject is "classification" (a noun), not the agent "neural network." The action "classify" is hidden in the noun "classification."

### Example: Strong Agency

> The neural network classifies images into categories.

**Why it works:** The agent "neural network" directly performs the action "classifies."

### When Passive Voice is Acceptable

Passive voice is appropriate when:
1. The agent is unknown or irrelevant: "The dataset was collected in 2020."
2. Emphasizing the action's recipient: "Errors were reduced by 30%."
3. Maintaining topic consistency: "Our model was trained on ImageNet. It was evaluated on five benchmarks."

---

## Principle 4: Parallelism

### The Rule

**Express parallel ideas in parallel grammatical structures.**

Parallelism signals to readers that items are coordinate in importance.

### Example: Poor Parallelism

> Our contributions are: (1) proposing a new loss function, (2) we demonstrate its effectiveness on benchmarks, and (3) theoretical analysis.

**Problem:** Mixed structures: gerund ("proposing"), clause ("we demonstrate"), noun phrase ("theoretical analysis").

### Example: Good Parallelism

> Our contributions are: (1) a new loss function, (2) empirical validation on benchmarks, and (3) theoretical analysis.

**Why it works:** All items are noun phrases, signaling their equal status.

---

## Principle 5: Context Before Detail

### The Rule

**Provide interpretive context before technical details.**

This primes the reader to understand why the details matter.

### Example: Detail-First (Poor)

> Our model uses a transformer architecture with 12 layers, 768 hidden dimensions, and 12 attention heads, trained with AdamW optimizer using a learning rate of 1e-4 and weight decay of 0.01. This configuration achieves strong performance.

**Problem:** Readers encounter technical details without knowing their purpose or relevance.

### Example: Context-First (Good)

> To balance model capacity and computational cost, we use a moderately-sized transformer architecture: 12 layers, 768 hidden dimensions, and 12 attention heads. We train with AdamW (learning rate 1e-4, weight decay 0.01), which stabilizes training for this architecture.

**Why it works:** The reason ("balance capacity and cost") precedes the technical specification.

---

## Application: Paragraph-Level Coherence

### Issue Sentences (Paragraph Start)

**Function:** State the main point of the paragraph.

**Placement:** First sentence (or second, after transition).

**Content:** Should connect to previous paragraph and introduce new topic.

**Example:**
> While supervised methods achieve high accuracy, they require expensive labeled data. (← connects to previous paragraph) To reduce this cost, semi-supervised learning leverages unlabeled data. (← introduces new topic)

### Point Sentences (Paragraph End)

**Function:** State the consequence or implication of the paragraph.

**Placement:** Last sentence.

**Content:** Should emphasize the key takeaway.

**Example:**
> ...experimental results on three benchmarks. These findings demonstrate that our approach consistently outperforms fully supervised baselines while using 10× less labeled data. (← key takeaway in stress position)

---

## Practical Checklist: Sentence Clarity

For each sentence, ask:

- [ ] **Topic Position**: Does the sentence start with familiar information?
- [ ] **Stress Position**: Does the sentence end with the most important new information?
- [ ] **Verb Position**: Does the verb appear soon after the subject?
- [ ] **Agency**: Is the grammatical subject the actual agent performing the action?
- [ ] **Flow**: Does this sentence connect to the previous one?

For each paragraph, ask:

- [ ] **Issue Sentence**: Does the first sentence clearly state the paragraph's topic?
- [ ] **Topic Consistency**: Do sentences maintain a consistent topic when appropriate?
- [ ] **Point Sentence**: Does the last sentence emphasize the key takeaway?

---

## Common Sentence-Level Anti-Patterns

### 1. "Buried Verb" Syndrome

**Problem:** Converting verbs to nouns (nominalization).

**Bad:** The comparison of the methods is shown in Table 1.

**Good:** Table 1 compares the methods.

### 2. "Throat-Clearing"

**Problem:** Starting sentences with weak phrases that don't convey information.

**Bad:** It is important to note that our method improves accuracy.

**Good:** Our method improves accuracy.

**Weak starts to avoid:**
- "It is interesting that..."
- "It should be noted that..."
- "It can be seen that..."
- "There is/are..."

### 3. "Modifier Soup"

**Problem:** Stacking adjectives and prepositional phrases, obscuring the core idea.

**Bad:** The proposed novel state-of-the-art deep learning-based method for image classification on large-scale datasets achieves improvements.

**Good:** Our deep learning method achieves state-of-the-art image classification on large-scale datasets.

### 4. "Dangling Emphasis"

**Problem:** Ending sentences with weak elements (citations, minor qualifications).

**Bad:** This approach significantly improves performance, as shown in [23].

**Good:** As shown in [23], this approach significantly improves performance.

### 5. "Topic Whiplash"

**Problem:** Abrupt topic shifts without signaling.

**Bad:** Our method uses self-attention. Convolutional networks have dominated vision tasks.

**Good:** Our method uses self-attention. In contrast, convolutional networks have traditionally dominated vision tasks.

---

## Advanced: Cohesion Devices

### Lexical Cohesion

**Technique:** Repeat key terms to maintain coherence.

**Example:**
> We propose a *robust training method*. This *method* addresses label noise by... Our *robust approach* outperforms...

### Pronominal Cohesion

**Technique:** Use pronouns to refer to previously mentioned entities.

**Example:**
> We trained the model on ImageNet. *It* achieved 87% accuracy.

**Caution:** Ensure pronoun reference is unambiguous.

### Logical Connectors

**Technique:** Use transition words to signal relationships.

**Types:**
- **Addition:** Moreover, Furthermore, Additionally
- **Contrast:** However, In contrast, Nevertheless
- **Cause-Effect:** Therefore, Thus, Consequently
- **Example:** For instance, Specifically, In particular
- **Sequence:** First, Next, Finally

---

## Exercise: Rewrite for Clarity

### Original (Poor):

> Improvements in accuracy of 15% are achieved by our method compared to baselines. This is due to the incorporation of a novel attention mechanism. Computational cost is also reduced.

### Analysis:

1. First sentence: "Improvements" in topic position (new info), "compared to baselines" in stress position (weak).
2. Second sentence: "This" is vague; "incorporation" is nominalization.
3. Third sentence: Shifts topic to "Computational cost" without connection.

### Rewritten (Good):

> Our method achieves 15% accuracy improvement over baselines by incorporating a novel attention mechanism. This mechanism also reduces computational cost.

### Changes:

1. "Our method" in topic position (familiar); "novel attention mechanism" in stress position (key idea).
2. "Mechanism" (not "incorporation"); agent-action aligned.
3. "This mechanism" maintains topic; ends with benefit ("reduces computational cost").

---

## Summary: Three Golden Rules

1. **Old Before New**: Start sentences with familiar information; end with new information.
2. **Subject-Verb Proximity**: Keep the verb close to the subject.
3. **Stress Position Power**: Place the most important information at the sentence end.

Follow these rules, and your writing will be clearer—even when the science is complex.
