# task-cost

Before starting any AI task, find the most cost-effective model and estimated cost. One command tells you which model to use and what you'll spend.

## Install

```bash
pip install git+https://github.com/minirr890112-byte/HermesMade.git#subdirectory=task-cost-estimator
```

## Usage

```bash
task-cost "describe your task here"
```

## How it works

1. **Profiles** your task → reasoning need, coding need, writing need, complexity
2. **Matches** 18 models against your requirements
3. **Ranks** by cost-effectiveness (capability ÷ cost)
4. **Estimates** cost per run, per day

## Examples

```bash
$ task-cost "build a REST API with JWT auth in Python"

📋 Task: REST API with JWT auth
   Needs: reasoning=7/10  coding=9/10  writing=3/10
   Est. tokens: ~1,000 in / ~1,000 out

⭐ DeepSeek V4 Flash    $0.0004/run  87% match
   DeepSeek V4 Pro      $0.0027/run  96% match
   OpenAI o3 (most capable) $0.05/run

$ task-cost "write a blog post about AI ethics"

⭐ Mistral Small 3      $0.0004/run  91% match

$ task-cost "debug a recursive stack overflow"

⭐ DeepSeek V4 Flash    $0.0003/run  84% match
```

## Task signals detected

| Signal | Examples |
|--------|----------|
| Coding-heavy | debug, refactor, implement, API, algorithm, optimize |
| Writing-heavy | blog post, article, essay, tutorial, proposal |
| Research | research, analyze, statistics, machine learning |
| Simple Q&A | explain, what is, how to, difference |
