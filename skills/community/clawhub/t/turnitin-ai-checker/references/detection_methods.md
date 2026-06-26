# AI Detection Methods Reference

## Perplexity Analysis

### What is Perplexity?

Perplexity measures how well a probability distribution or probability model predicts a sample. In NLP, it quantifies how "surprised" a language model is by text.

- **Lower perplexity** = Text is more predictable = Likely AI-generated
- **Higher perplexity** = Text is less predictable = Likely human-written

### Calculation

```
Perplexity = exp(-1/N * Σ log P(wi | w1...wi-1))
```

Where:
- N = number of tokens
- P(wi | w1...wi-1) = probability of token given previous context

### Implementation Approach

1. Use a pre-trained language model (e.g., GPT-2, RoBERTa)
2. Calculate log probabilities for each token
3. Average and exponentiate
4. Compare against thresholds:
   - Perplexity < 20: High AI probability
   - Perplexity 20-50: Moderate AI probability
   - Perplexity > 50: Low AI probability

## Burstiness Detection

### What is Burstiness?

Burstiness measures the variation in sentence length and structure. AI-generated text tends to be more uniform, while human writing has natural variation.

### Metrics

1. **Sentence Length Variance**
   - Calculate standard deviation of sentence lengths
   - Lower variance = more AI-like

2. **Sentence Length Distribution**
   - AI: Often clustered around mean
   - Human: Long tail distribution with outliers

3. **Punctuation Burstiness**
   - Variance in comma usage per sentence
   - Variance in clause complexity

### Implementation

```python
def calculate_burstiness(sentences):
    lengths = [len(s.split()) for s in sentences]
    mean_len = np.mean(lengths)
    std_len = np.std(lengths)
    
    # Coefficient of variation
    cv = std_len / mean_len if mean_len > 0 else 0
    
    # Burstiness score (0-1, higher = more human-like)
    burstiness = min(cv / 0.5, 1.0)
    return burstiness
```

## AI Pattern Recognition

### Common AI Writing Patterns

1. **Repetitive Transitions**
   - "Furthermore", "Moreover", "In addition"
   - Overused at paragraph starts

2. **Generic Conclusions**
   - "In conclusion", "To summarize"
   - Formulaic ending patterns

3. **Hedging Language**
   - "It is important to note"
   - "It should be noted that"
   - "It is worth mentioning"

4. **List-like Structures**
   - Overly organized bullet points
   - Parallel structure that feels mechanical

5. **Lack of Personal Voice**
   - No opinions or subjective statements
   - Absence of "I think", "In my experience"

### Pattern Detection Implementation

```python
AI_PHRASES = [
    "it is important to note",
    "it should be noted",
    "it is worth mentioning",
    "in conclusion",
    "to summarize",
    "furthermore",
    "moreover",
    "in addition",
    "additionally",
    "consequently",
    "therefore",
    "thus",
    "as a result",
    "for example",
    "for instance",
    "in other words",
    "to put it simply",
    "in today's world",
    "in recent years",
    "with the development of",
]

def detect_ai_patterns(text):
    text_lower = text.lower()
    pattern_count = sum(1 for phrase in AI_PHRASES if phrase in text_lower)
    # Normalize by text length
    return min(pattern_count / (len(text.split()) / 100), 1.0)
```

## Readability Metrics

### Flesch Reading Ease

```
206.835 - (1.015 × ASL) - (84.6 × ASW)
```

Where:
- ASL = Average sentence length (words/sentences)
- ASW = Average syllables per word

### Flesch-Kincaid Grade Level

```
(0.39 × ASL) + (11.8 × ASW) - 15.59
```

### AI vs Human Patterns

- **AI text**: Often consistently in 12-16 grade level range
- **Human text**: More variation, occasional simple/complex sections

## Combined Scoring Algorithm

### Weighted Average Approach

```python
def calculate_ai_score(text):
    # Individual component scores (0-100, higher = more AI-like)
    perplexity_score = analyze_perplexity(text)  # 30% weight
    burstiness_score = 100 - calculate_burstiness(text) * 100  # 25% weight
    pattern_score = detect_ai_patterns(text) * 100  # 25% weight
    readability_variance = analyze_readability_variance(text)  # 20% weight
    
    # Weighted combination
    ai_score = (
        perplexity_score * 0.30 +
        burstiness_score * 0.25 +
        pattern_score * 0.25 +
        readability_variance * 0.20
    )
    
    return min(max(ai_score, 0), 100)
```

### Risk Levels

- **0-20%**: Safe - No action needed
- **20-40%**: Warning - Consider review
- **40-60%**: Moderate Risk - Humanization recommended
- **60-100%**: High Risk - Humanization strongly recommended

## Humanization Techniques

### 1. Sentence Length Variation

**Before (AI-like):**
> "The research methodology employed a mixed-methods approach. This approach allowed for comprehensive data collection. The data was analyzed using statistical software."

**After (Humanized):**
> "We went with a mixed-methods approach for this research. Why? It gave us the full picture. After collecting everything, we ran the numbers through statistical software."

### 2. Personal Voice Addition

**Before:**
> "It is important to note that the results may vary."

**After:**
> "From my experience, results can really vary depending on the context."

### 3. Breaking Formulaic Structure

**Before:**
> "In conclusion, this study has demonstrated three key findings. First... Second... Third..."

**After:**
> "So what did we actually find? Three things stood out. The first was..."

### 4. Natural Transitions

Replace formal transitions with natural flow:
- "Furthermore" → "Plus" or "Also"
- "Moreover" → "What's more"
- "Consequently" → "So" or "That meant"
- "Therefore" → "That's why"

### 5. Minor Imperfections

Humans naturally include:
- Occasional sentence fragments
- Varying punctuation usage
- Personal asides
- Rhetorical questions
