# Gemma Model Optimization Strategies

This guide covers specific token reduction and prompt compression techniques when working with Google's Gemma models.

## 1. The SentencePiece Vocabulary Advantage

Unlike many other models that use ~100k vocabularies, Gemma uses a SentencePiece tokenizer with a massive **~256k vocabulary**. 

**Token Cost of Words:**
- Many multi-syllable or moderately obscure words that break into 2-3 tokens in other models will tokenize as **1 token** in Gemma.
- You do not need to over-simplify language as aggressively as with older models. A dense, specific technical term might cost *fewer* tokens than spelling it out simply.

**Whitespace & Spacing:**
- Gemma is trained heavily on code. Structured formatting like `<tag>` is extremely efficient.
- Tabs vs. Spaces: Check `count_tokens.py`, but typically replacing 4 spaces with 1 tab saves ~3 tokens per line in indentation. In a 500-line script, that is 1500 tokens saved!

## 2. "Model Dialect" - XML Tags

Gemma models have been shown to perform extremely well with **XML and structured text block separators**.

Instead of writing instructions as flowing prose:
```text
Here is the context of the user's issue which happens in the API. Please read it and write a python script.
```

Write them like this:
```xml
<context>Issue happens in the API.</context><task>Write python script.</task>
```

**Why this saves tokens:** 
XML tags like `<context>` are often single tokens in Gemma. It saves you from writing "The following section is the..." which costs 6+ tokens. Over a long prompt, this adds up to 10-20% savings.

## 3. Tool Loading Efficiency

Gemma processes long structured schemas efficiently, but you should avoid having bloated descriptions in your tools.
- Focus on parameter names and `enum` options over lengthy natural-language descriptions of what the parameter does. Gemma Infers intent from parameter names well.

## 4. Context DNA Strategy (Code Compression)

When passing existing, repetitive UI code (e.g. React imports or Tailwind grids) to Gemma, you can compress it locally:

Instead of providing:
```typescript
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardContent } from "@/components/ui/card"
```

Summarize standard boilerplate into a single line:
```typescript
// Imports: standard UI components (Button, Card)
```

Gemma knows standard libraries and standard file layouts. Do not feed it the parts of the file it doesn't need to change. If you extract only the *logic*, you reduce code length by 80%.
