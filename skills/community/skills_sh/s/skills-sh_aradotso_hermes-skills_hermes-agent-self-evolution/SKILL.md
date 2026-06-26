---
name: hermes-agent-self-evolution
description: Evolutionary self-improvement for Hermes Agent using DSPy + GEPA to optimize skills, prompts, and code
triggers:
  - evolve a hermes agent skill
  - optimize hermes agent prompts
  - run GEPA optimization on skills
  - improve hermes agent with self-evolution
  - generate evaluation dataset for skill evolution
  - use DSPy to evolve agent prompts
  - run hermes self-evolution pipeline
  - optimize tool descriptions with GEPA
---

# Hermes Agent Self-Evolution

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

Hermes Agent Self-Evolution provides evolutionary self-improvement for [Hermes Agent](https://github.com/NousResearch/hermes-agent) using DSPy + GEPA (Genetic-Pareto Prompt Evolution). It automatically evolves and optimizes skills, tool descriptions, system prompts, and code through reflective evolutionary search—no GPU training required, everything operates via API calls.

## What It Does

- **Skill Evolution**: Optimizes SKILL.md files using execution traces and targeted mutations
- **Prompt Optimization**: Improves system prompts and tool descriptions through evolutionary search
- **Code Evolution**: Plans to support code-level optimization via Darwinian Evolver
- **Trace-Based Learning**: Analyzes *why* things fail, not just that they failed
- **Cost-Effective**: ~$2-10 per optimization run using LLM APIs

## Installation

```bash
# Clone the repository
git clone https://github.com/NousResearch/hermes-agent-self-evolution.git
cd hermes-agent-self-evolution

# Install with development dependencies
pip install -e ".[dev]"

# Set required environment variables
export HERMES_AGENT_REPO=~/.hermes/hermes-agent
export OPENAI_API_KEY=your_openai_api_key
```

## Core Workflow

The evolution pipeline follows this flow:

1. Read current skill/prompt/tool definition
2. Generate evaluation dataset (synthetic or from session history)
3. Run GEPA optimizer to create candidate variants
4. Evaluate variants against execution traces
5. Apply constraint gates (tests, size limits, benchmarks)
6. Select best variant and generate PR

## Evolving Skills

### Basic Skill Evolution with Synthetic Data

```python
# Command line
python -m evolution.skills.evolve_skill \
    --skill github-code-review \
    --iterations 10 \
    --eval-source synthetic

# Or programmatically
from evolution.skills.evolve_skill import evolve_skill

result = evolve_skill(
    skill_name="github-code-review",
    iterations=10,
    eval_source="synthetic",
    hermes_repo_path="~/.hermes/hermes-agent"
)

print(f"Best variant score: {result.best_score}")
print(f"Improvement: {result.improvement_pct}%")
```

### Using Real Session History

```python
# Use actual session data from Claude Code, Copilot, Hermes
python -m evolution.skills.evolve_skill \
    --skill github-code-review \
    --iterations 10 \
    --eval-source sessiondb \
    --session-db-path ~/.hermes/sessions.db
```

### Custom Evaluation Dataset

```python
from evolution.skills.evolve_skill import evolve_skill
from evolution.eval.dataset import EvalDataset, EvalExample

# Create custom evaluation examples
dataset = EvalDataset(examples=[
    EvalExample(
        input_query="Review this PR for security issues",
        expected_behavior="Check for SQL injection, XSS, secrets in code",
        context={"pr_url": "https://github.com/org/repo/pull/123"}
    ),
    EvalExample(
        input_query="Analyze code quality in this commit",
        expected_behavior="Check complexity, test coverage, documentation",
        context={"commit_sha": "abc123"}
    )
])

result = evolve_skill(
    skill_name="github-code-review",
    custom_dataset=dataset,
    iterations=10
)
```

## DSPy + GEPA Integration

### Understanding GEPA

GEPA (Genetic-Pareto Prompt Evolution) reads execution traces to understand failures and propose targeted improvements:

```python
from evolution.gepa.optimizer import GEPAOptimizer
from evolution.gepa.trace import ExecutionTrace

# Initialize GEPA optimizer
optimizer = GEPAOptimizer(
    population_size=20,
    mutation_rate=0.3,
    crossover_rate=0.5
)

# Load execution traces
traces = [
    ExecutionTrace(
        input="Review PR #123",
        output="Checked syntax only",
        error="Failed to identify security issues",
        metadata={"skill": "github-code-review"}
    )
]

# Generate improved variants
variants = optimizer.evolve(
    current_prompt="Review GitHub pull requests for code quality",
    traces=traces,
    num_generations=10
)

best_variant = variants[0]
print(f"Improved prompt: {best_variant.text}")
print(f"Fitness score: {best_variant.fitness}")
```

### Custom Mutation Strategies

```python
from evolution.gepa.mutations import (
    AddDetailMutation,
    SimplifyMutation,
    ReframeMutation,
    ExampleMutation
)

optimizer = GEPAOptimizer(
    mutations=[
        AddDetailMutation(weight=0.4),
        SimplifyMutation(weight=0.2),
        ReframeMutation(weight=0.2),
        ExampleMutation(weight=0.2)
    ]
)
```

## Configuration

### Evolution Config File

Create `evolution_config.yaml`:

```yaml
# Optimization parameters
gepa:
  population_size: 20
  num_generations: 10
  mutation_rate: 0.3
  crossover_rate: 0.5
  elitism: 2  # Keep top 2 variants

# Constraint gates
constraints:
  max_skill_size_kb: 15
  max_tool_description_chars: 500
  min_test_pass_rate: 1.0
  semantic_drift_threshold: 0.15

# Evaluation
evaluation:
  metrics:
    - accuracy
    - execution_success
    - response_quality
  weights:
    accuracy: 0.4
    execution_success: 0.4
    response_quality: 0.2

# API settings
api:
  provider: openai  # or anthropic, together
  model: gpt-4
  temperature: 0.7
  max_tokens: 2000
```

Load and use:

```python
from evolution.config import EvolutionConfig

config = EvolutionConfig.from_yaml("evolution_config.yaml")

result = evolve_skill(
    skill_name="github-code-review",
    config=config
)
```

## Guardrails and Constraints

All evolved variants must pass these gates:

```python
from evolution.constraints import (
    TestSuiteConstraint,
    SizeLimitConstraint,
    SemanticPreservationConstraint,
    CachingCompatibilityConstraint
)

constraints = [
    TestSuiteConstraint(
        test_command="pytest tests/ -q",
        required_pass_rate=1.0
    ),
    SizeLimitConstraint(
        max_skill_kb=15,
        max_tool_desc_chars=500
    ),
    SemanticPreservationConstraint(
        drift_threshold=0.15,
        embedding_model="text-embedding-3-small"
    ),
    CachingCompatibilityConstraint(
        allow_mid_conversation_changes=False
    )
]

# Validate a variant
from evolution.validation import validate_variant

is_valid, violations = validate_variant(
    variant_text="...",
    constraints=constraints
)

if not is_valid:
    print(f"Constraint violations: {violations}")
```

## Monitoring Evolution Progress

```python
from evolution.callbacks import (
    LoggingCallback,
    MetricsCallback,
    CheckpointCallback
)

callbacks = [
    LoggingCallback(verbose=True),
    MetricsCallback(
        track_metrics=["fitness", "diversity", "constraint_violations"]
    ),
    CheckpointCallback(
        checkpoint_dir="./checkpoints",
        save_every=5  # Save every 5 generations
    )
]

result = evolve_skill(
    skill_name="github-code-review",
    iterations=20,
    callbacks=callbacks
)

# Access metrics
print(result.metrics_history)
```

## Generating Evaluation Datasets

### Synthetic Data Generation

```python
from evolution.eval.synthetic import SyntheticDataGenerator

generator = SyntheticDataGenerator(
    skill_name="github-code-review",
    num_examples=50,
    difficulty_distribution={
        "easy": 0.3,
        "medium": 0.5,
        "hard": 0.2
    }
)

dataset = generator.generate()
dataset.save("eval_datasets/github-code-review.json")
```

### From Session History

```python
from evolution.eval.session_extractor import SessionExtractor

extractor = SessionExtractor(
    session_db_path="~/.hermes/sessions.db",
    skill_filter="github-code-review"
)

# Extract examples from last 30 days
dataset = extractor.extract(
    days_back=30,
    min_quality_score=0.7,
    max_examples=100
)
```

## Advanced Patterns

### Multi-Objective Optimization

```python
from evolution.objectives import (
    AccuracyObjective,
    LatencyObjective,
    TokenEfficiencyObjective
)

optimizer = GEPAOptimizer(
    objectives=[
        AccuracyObjective(weight=0.5),
        LatencyObjective(weight=0.3),
        TokenEfficiencyObjective(weight=0.2)
    ],
    pareto_frontier=True  # Find Pareto-optimal solutions
)

variants = optimizer.evolve(current_prompt, traces, num_generations=15)

# Get Pareto frontier
pareto_variants = [v for v in variants if v.is_pareto_optimal]
```

### Batch Evolution of Multiple Skills

```python
from evolution.batch import batch_evolve_skills

skills_to_evolve = [
    "github-code-review",
    "python-debugging",
    "api-design",
    "docker-optimization"
]

results = batch_evolve_skills(
    skills=skills_to_evolve,
    iterations=10,
    parallel=True,
    max_workers=4
)

for skill, result in results.items():
    print(f"{skill}: {result.improvement_pct}% improvement")
```

### Integration with CI/CD

```python
# evolution_pipeline.py
from evolution.ci import create_evolution_pr

# Run in GitHub Actions or similar
if __name__ == "__main__":
    result = evolve_skill(
        skill_name="github-code-review",
        iterations=10,
        eval_source="synthetic"
    )
    
    if result.improvement_pct > 5.0:  # Only PR if >5% improvement
        pr = create_evolution_pr(
            skill_name="github-code-review",
            variant_text=result.best_variant,
            metrics=result.metrics,
            repo_path=os.getenv("HERMES_AGENT_REPO"),
            branch_name=f"evolution/github-code-review-{result.run_id}"
        )
        print(f"Created PR: {pr.url}")
```

## Troubleshooting

### Evolution Gets Stuck in Local Optimum

```python
# Increase mutation rate and diversity
optimizer = GEPAOptimizer(
    mutation_rate=0.5,  # Higher mutation
    diversity_bonus=0.1,  # Reward novel variants
    restart_threshold=5  # Restart if no improvement for 5 gens
)
```

### Variants Fail Constraint Gates

```python
# Debug constraint failures
from evolution.debug import diagnose_constraints

diagnosis = diagnose_constraints(
    variant_text="...",
    constraints=constraints,
    verbose=True
)

print(diagnosis.summary())
```

### API Rate Limits

```python
from evolution.api import RateLimitedClient

client = RateLimitedClient(
    provider="openai",
    api_key=os.getenv("OPENAI_API_KEY"),
    requests_per_minute=50,
    retry_on_limit=True,
    backoff_factor=2.0
)
```

### Low Quality Evaluation Data

```python
# Filter and augment evaluation dataset
from evolution.eval.quality import filter_by_quality, augment_dataset

dataset = EvalDataset.load("eval_datasets/raw.json")
dataset = filter_by_quality(dataset, min_score=0.7)
dataset = augment_dataset(dataset, augmentation_factor=2)
```

## Environment Variables

```bash
# Required
export HERMES_AGENT_REPO=~/.hermes/hermes-agent
export OPENAI_API_KEY=your_api_key

# Optional
export EVOLUTION_CONFIG_PATH=./evolution_config.yaml
export EVOLUTION_CHECKPOINT_DIR=./checkpoints
export EVOLUTION_LOG_LEVEL=INFO
export SESSION_DB_PATH=~/.hermes/sessions.db
```

## Integration with Hermes Agent

Evolved skills automatically integrate with Hermes Agent:

```python
# After evolution completes, the improved skill is available
from hermes_agent import HermesAgent

agent = HermesAgent()
agent.load_skill("github-code-review")  # Uses evolved version

response = agent.chat("Review this PR for security issues")
```

## Project Structure

```
hermes-agent-self-evolution/
├── evolution/
│   ├── skills/           # Skill evolution
│   ├── prompts/          # Prompt optimization
│   ├── tools/            # Tool description evolution
│   ├── gepa/             # GEPA optimizer implementation
│   ├── eval/             # Evaluation datasets and metrics
│   ├── constraints/      # Constraint gates
│   └── callbacks/        # Evolution callbacks
├── tests/                # Test suite
├── eval_datasets/        # Evaluation data
└── evolution_config.yaml # Default configuration
```
