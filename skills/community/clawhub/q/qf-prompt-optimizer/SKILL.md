# Prompt Optimizer

Transform vague, underperforming prompts into precise, structured prompts that consistently produce high-quality AI outputs.

## Description

This skill takes any user prompt — whether vague, ambiguous, or poorly structured — and systematically refines it into a professional-grade prompt following established prompt engineering principles. It applies techniques from chain-of-thought, role-prompting, few-shot learning, and structured output formatting to maximize AI performance.

## When to Use

- The user provides a vague prompt like "write something about marketing" and expects better results
- A prompt produces inconsistent or off-topic outputs
- Converting natural language requests into structured prompts
- Building prompt templates for repeated use
- Debugging prompts that fail in edge cases

## Instructions

### The OPTIMIZE Framework

When refining a prompt, apply these six principles in order:

#### O — Objective (明确目标)

**Problem**: Vague verbs like "write about," "explain," "help with"
**Fix**: Specify exact deliverable and success criteria

| Vague | Optimized |
|-------|-----------|
| "Write about AI" | "Write a 500-word blog post explaining how large language models work, targeting software developers with 2+ years of experience" |
| "Make it better" | "Improve clarity and reduce sentence length by 30% while preserving all technical details" |
| "Fix the code" | "Refactor this Python function to reduce cyclomatic complexity below 5 and add type hints" |

#### P — Persona (设定角色)

Assign a specific role to ground the AI's expertise:

- "You are a senior staff engineer at Google with 15 years of distributed systems experience"
- "You are a Nature journal reviewer specializing in immunology"
- "You are a direct-response copywriter trained by Eugene Schwartz's methods"

Include constraints: "Respond only with what you're confident about. If uncertain, say so."

#### T — Task Structure (任务结构)

Break complex tasks into ordered steps:

```
1. First, analyze X and identify Y
2. Then, based on Y, generate Z using method A
3. Finally, format the output as...
```

For multi-step tasks, use numbered steps rather than one compound instruction.

#### I — Input Specification (输入规范)

Define what the user will provide:

- "I will provide: (1) a product description, (2) target audience, (3) competitor list"
- "Input: A CSV file with columns [date, revenue, expenses]"
- "Here is the code to review: ```<language>\n...\n```"

Explicit input templates reduce ambiguity.

#### M — Metrics & Constraints (约束条件)

Add specific constraints:

```
Constraints:
- Maximum 500 words
- Use only peer-reviewed sources
- No jargon; explain all technical terms
- Output in Chinese
- Format as a comparison table
- Must include 3 concrete examples
```

#### I — Ideal Output (理想输出)

Show or describe the desired output format:

- Provide an example of expected output (few-shot)
- Specify format: JSON schema, markdown table, numbered list, code block
- Define evaluation criteria: "The output is successful if a non-expert can understand the explanation"

### Prompt Optimization Process

Given a raw prompt, produce:

1. **Diagnosis**: What's wrong with the original (vague goal? missing context? no format? no constraints?)
2. **Optimized Prompt**: The refined version following OPTIMIZE framework
3. **Explanation**: What was changed and why

### Common Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| "Just make it good" | No quality criteria | Define what "good" means with measurable criteria |
| Giant wall of text | AI loses focus | Break into numbered sections with clear headers |
| Contradictory instructions | AI guesses priority | Remove conflicts; rank priorities explicitly |
| Missing negative constraints | AI makes unwanted assumptions | Add "Do NOT..." instructions for known failure modes |
| No examples | AI style is unpredictable | Provide 1-3 input/output examples |

## Examples

**Raw Prompt**: "Write an email to my boss asking for a raise"

**Optimized Prompt**:
```
You are a professional career coach helping a software engineer draft a salary negotiation email.

Task: Write a salary increase request email to my manager.

Context:
- I'm a mid-level software engineer, 2 years at the company
- I recently led a project that saved the company $200K annually
- The company just closed a successful funding round
- My current salary is below market rate based on Levels.fyi data

Requirements:
- Professional but warm tone (not aggressive, not passive)
- 150-250 words
- Lead with value delivered, not personal needs
- Include a specific meeting request
- No ultimatums or comparisons with colleagues

Format: Standard email with subject line
```

**Raw Prompt**: "分析这个数据"

**Optimized Prompt**:
```
You are a senior data analyst. Analyze the provided dataset and produce a business report.

Input: I will provide a CSV file with monthly sales data (columns: date, product, quantity, revenue, region).

Steps:
1. Identify the top 3 revenue-generating products
2. Detect any seasonal trends or anomalies
3. Compare regional performance
4. Provide 3 actionable business recommendations

Output format:
- Executive summary (3 sentences)
- Key findings as a numbered list
- Recommendations with expected impact (high/medium/low)
- Any data quality concerns

Language: Chinese
```

## Tips

- The best prompts read like briefs given to a competent professional, not commands given to a machine
- Always test optimized prompts with edge cases before standardizing
- Keep prompts under 500 words when possible — longer prompts can confuse the model
- Version your prompts (v1, v2) and track which versions produce better results
- When a prompt still fails after optimization, the task may need to be decomposed into subtasks
