# MCP Server Evaluation Guide

## Overview

Create evaluations to test whether LLMs can effectively use your MCP server to answer realistic, complex questions.

---

## Quick Reference

### Evaluation Requirements
- Create 10 human-readable questions
- Questions must be READ-ONLY, INDEPENDENT, NON-DESTRUCTIVE
- Each question requires multiple tool calls
- Answers must be single, verifiable values
- Answers must be STABLE (won't change over time)

### Output Format
```xml
<evaluation>
   <qa_pair>
      <question>Your question here</question>
      <answer>Single verifiable answer</answer>
   </qa_pair>
</evaluation>
```

---

## Question Guidelines

### Core Requirements

1. **Questions MUST be independent** - Not dependent on other questions
2. **Questions MUST require ONLY NON-DESTRUCTIVE operations**
3. **Questions must be REALISTIC, CLEAR, CONCISE, and COMPLEX**
4. **Questions must require deep exploration** - Multiple tool calls
5. **Questions should NOT be solvable with straightforward keyword search**

### Stability

- Questions must be designed so the answer DOES NOT CHANGE
- Do not ask about "current state" which is dynamic
- Look at old/completed content

---

## Answer Guidelines

1. **Answers must be VERIFIABLE via direct string comparison**
2. **Answers should prefer HUMAN-READABLE formats** (names, dates, yes/no)
3. **Answers must be STABLE** - Based on historical data
4. **Answers must be DIVERSE** - Various formats and data types
5. **Answers must NOT be complex structures** - Single values only

---

## Good Question Examples

**Multi-hop question:**
```xml
<qa_pair>
   <question>Find the repository archived in Q3 2023 that had previously been the most forked. What was the primary programming language?</question>
   <answer>Python</answer>
</qa_pair>
```

**Aggregation question:**
```xml
<qa_pair>
   <question>Among bugs reported in January 2024 marked as critical, which assignee resolved the highest percentage within 48 hours? Provide their username.</question>
   <answer>alex_eng</answer>
</qa_pair>
```

---

## Poor Question Examples

**Answer changes over time:**
```xml
<qa_pair>
   <question>How many open issues are currently assigned?</question>
   <answer>47</answer>
</qa_pair>
```

**Too easy with keyword search:**
```xml
<qa_pair>
   <question>Find the PR with title "Add authentication feature"</question>
   <answer>developer123</answer>
</qa_pair>
```

---

## Running Evaluations

```bash
# Install dependencies
pip install anthropic mcp

# Set API key
export ANTHROPIC_API_KEY=your_api_key

# Run evaluation
python scripts/evaluation.py \
  -t stdio \
  -c python \
  -a my_server.py \
  evaluation.xml
```
