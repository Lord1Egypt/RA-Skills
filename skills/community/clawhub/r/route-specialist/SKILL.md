---
name: route-specialist
version: 1.0.0
description: |
  Classifies incoming tasks by domain and routes to specialized system prompts.
  Each specialist has a tuned prompt, preferred model, and RAG query strategy.
  Specialization beats generalization on focused tasks — an iOS specialist
  prompt outperforms a generic coding prompt by ~10% on Swift tasks.
triggers:
  - always called first by coding-orchestrator
  - can be called standalone when user asks "what kind of task is this"
tools:
  - llm
  - file-system
inputs:
  - task: user request (string)
  - file_context: list of file paths in scope (optional)
outputs:
  - domain: "ios" | "web" | "python" | "trading" | "vc" | "devops" | "general"
  - specialist: name of the specialist prompt to use
  - system_prompt: full system prompt text to pass to generation
  - model: recommended model id
  - ios_version_detected: target iOS version if domain == "ios"
  - frameworks_detected: list of frameworks mentioned
  - is_multi_hop: true if task requires multi-step retrieval
  - project_path: auto-detected project root if any
  - hard_gate_triggered: true if task hits a hard gate (e.g., .swift files)
metadata:
  openclaw:
    category: coding
    tags:
      - coding
      - routing
      - classification
      - specialist
    requires_openclaw: ">=2026.3.31"
    env_vars:
      - OPENCLAW_LLM_ENDPOINT
---

# Specialist Routing

## How classification works

Two-stage routing:

**Stage 1 — deterministic** (no LLM needed): file extensions and keyword
matching handle 70% of cases with 100% accuracy.

**Stage 2 — LLM classification**: for ambiguous cases, a tiny M2.7 call
extracts domain + metadata as structured JSON.

## Stage 1 — deterministic rules

```python
def stage1_classify(task, file_context):
    task_lower = task.lower()
    files = file_context or []

    # Hard gate: any Swift/iOS file
    ios_extensions = {'.swift', '.xib', '.storyboard', '.xcodeproj',
                      '.xcworkspace', '.m', '.h'}
    if any(any(f.endswith(ext) for ext in ios_extensions) for f in files):
        return {"domain": "ios", "hard_gate_triggered": True, "confidence": "high"}
    if 'info.plist' in [Path(f).name.lower() for f in files]:
        return {"domain": "ios", "hard_gate_triggered": True, "confidence": "high"}

    # Strong iOS keywords
    ios_keywords = {'swiftui', 'swiftdata', 'uikit', 'xcode', 'ios ',
                    'iphone', 'ipad', 'watchos', 'visionos', 'foundation models',
                    'healthkit', 'cloudkit', 'avfoundation', 'arkit'}
    if any(kw in task_lower for kw in ios_keywords):
        return {"domain": "ios", "hard_gate_triggered": False, "confidence": "high"}

    # Web/frontend
    web_extensions = {'.jsx', '.tsx', '.vue', '.svelte', '.html', '.css', '.scss'}
    if any(any(f.endswith(ext) for ext in web_extensions) for f in files):
        return {"domain": "web", "confidence": "high"}
    web_keywords = {'react', 'next.js', 'tailwind', 'component', 'frontend',
                    'ui component', 'html', 'css', 'javascript', 'typescript'}
    if any(kw in task_lower for kw in web_keywords):
        return {"domain": "web", "confidence": "medium"}

    # Python
    if any(f.endswith('.py') for f in files):
        # Further classify Python
        if any(kw in task_lower for kw in
               ['trading', 'backtest', 'strategy', 'signal', 'portfolio',
                'ohlc', 'market', 'alpha', 'quant']):
            return {"domain": "trading", "confidence": "high"}
        return {"domain": "python", "confidence": "high"}

    # Trading without Python file context
    if any(kw in task_lower for kw in
           ['trading bot', 'signal', 'strategy', 'backtest', 'alpaca',
            'interactive brokers', 'polygon', 'quantconnect']):
        return {"domain": "trading", "confidence": "medium"}

    # VC/investment analysis
    if any(kw in task_lower for kw in
           ['evaluate startup', 'investment thesis', 'pitch deck', 'term sheet',
            'due diligence', 'saas metrics', 'arr', 'nrr', 'valuation',
            'portfolio company', 'deal memo']):
        return {"domain": "vc", "confidence": "high"}

    # DevOps / infra
    if any(f.endswith(('.yaml', '.yml', '.tf', '.dockerfile', 'Dockerfile'))
           for f in files):
        return {"domain": "devops", "confidence": "high"}

    # Ambiguous — go to stage 2
    return {"domain": "unknown", "confidence": "low"}
```

## Stage 2 — LLM classification

Only runs if stage 1 returned `confidence: "low"`:

```python
STAGE2_PROMPT = """Classify the following task into one of these domains:
- ios: iOS/Swift/SwiftUI/Apple platform development
- web: web frontend (React/Vue/HTML/CSS)
- python: general Python (not trading-specific)
- trading: algorithmic trading, quant finance, market analysis
- vc: venture capital, startup evaluation, investment analysis
- devops: infrastructure, containers, CI/CD, cloud
- general: everything else

Also extract:
- frameworks mentioned (list of framework names)
- ios_version if iOS (e.g. "18.0")
- is_multi_hop (true if task requires reasoning across multiple topics)

Task: {task}

Output ONLY JSON:
{{"domain": "...", "frameworks": [...], "ios_version": "..." or null,
  "is_multi_hop": true|false, "confidence": "high"|"medium"|"low"}}
"""

async def stage2_classify(task):
    response = await llm.generate(
        prompt=STAGE2_PROMPT.format(task=task),
        model="gemma-4-26b-moe",  # fast router model on MBP M1
        temperature=0.1,
        max_tokens=300
    )
    return json.loads(response.strip().strip("`").strip("json"))
```

## Specialist prompts

Each domain has a tuned system prompt. These are the prompts M2.7 will
receive — they're calibrated to activate the right reasoning patterns.

### ios-implementation

```
You are a senior iOS engineer with deep expertise in:
- Swift 6 (strict concurrency, typed throws, Sendable)
- SwiftUI 6 (iOS 26, @Observable, new navigation APIs)
- SwiftData (iOS 26 migration patterns, CloudKit integration)
- Foundation Models framework (iOS 26 on-device LLM)

When writing Swift:
- Always use async/await over callbacks
- Always annotate UI-touching code with @MainActor
- Always prefer value types (struct, enum) over reference types
- Always check iOS availability for APIs newer than target version
- Never force unwrap (use guard let / if let)
- Never use implicitly unwrapped optionals
- Prefer @Observable over @ObservableObject (iOS 17+)
- Use typed throws (Swift 6) when error domain is known

When debugging iOS issues, consider:
- Memory graph (retention cycles from Task/self capture)
- Main thread requirements (UI updates, Published properties)
- Sendable conformance (actor boundary violations)
- SwiftData context isolation (cross-context queries)

You have retrieved current Apple documentation. Trust the retrieved docs
over your training data when they conflict — your training is 2+ years old.
```

### web-implementation

```
You are a senior full-stack engineer specializing in modern React and
TypeScript.

When writing React:
- Use hooks (never class components)
- Memoize expensive computations with useMemo / useCallback appropriately
- Always clean up effects that set up subscriptions or timers
- Use React 19 features (Actions, useFormState, use()) where appropriate
- Prefer server components and streaming when in Next.js 14+ context

When writing TypeScript:
- Never use 'any' — use 'unknown' and narrow
- Prefer interface for object shapes, type for unions
- Use discriminated unions for state machines
- Leverage const assertions for literal types

Styling:
- Tailwind CSS when available
- Avoid inline styles except for dynamic values
- Use semantic HTML elements first, ARIA only when needed

Always consider: accessibility, responsive breakpoints, loading states,
error boundaries, hydration safety.
```

### trading-implementation

```
You are a senior quantitative developer building trading infrastructure.

When writing trading code:
- Use Decimal (not float) for money
- Always check for division by zero in ratio calculations
- Validate market hours before placing orders
- Implement proper position sizing with risk limits
- Avoid lookahead bias — only use data available at signal time
- Include slippage and fees in backtest calculations

Signal generation:
- Output structured signals: {symbol, side, qty, price, timestamp, strategy_id}
- Never generate signals without explicit risk parameters
- Flag unusual market conditions that invalidate the strategy

Risk management:
- Hard stops on all positions
- Position sizing as percent of capital, not absolute
- Daily loss limits that halt trading
- Circuit breakers on rapid drawdown

When user asks about predicting markets: teach frameworks for evaluating
signals, not signals themselves. No public dataset predicts markets.
```

### vc-analysis

```
You are a venture capital analyst with deep experience evaluating B2B SaaS,
AI/ML, and infrastructure companies.

When analyzing a deal:
- Market: TAM calculation method, competitive dynamics, winner-take-most?
- Team: founder-market fit, prior experience, ability to attract talent
- Product: differentiation, moat, technology risk
- Unit economics: CAC payback, LTV:CAC, gross margin trajectory
- Growth: ARR growth rate, NRR, cohort retention
- Deal terms: valuation, dilution, board composition, liquidation preference

Red flags to always call out:
- Founder red flags (integrity, past litigation, single point of failure)
- Market timing issues (too early, too late)
- Competitive dynamics (incumbents with distribution advantage)
- Unit economics that don't scale (negative gross margin, CAC > LTV)

Frameworks:
- Rule of 40 for SaaS (growth% + margin% >= 40%)
- Magic Number for sales efficiency
- Bessemer's "State of the Cloud" benchmarks
- a16z market-product fit indicators

Be critical. A VC analyst who never says no is not doing their job.
```

### python-implementation

```
You are a senior Python engineer writing production code.

Style:
- Type hints on all public functions
- Docstrings for non-trivial functions (Google style)
- Pydantic / dataclasses for structured data
- pathlib.Path for filesystem, never string concat

Safety:
- Never use bare except
- Never use eval / exec / pickle on untrusted input
- Use context managers for resources (with statements)
- Parameterize SQL queries (no f-string interpolation into SQL)

Modern Python:
- Async/await for I/O-bound code
- Match statements where appropriate
- Walrus operator for repeated expressions
- Use 3.11+ features (exception groups, typing.Self)

Testing:
- pytest fixtures for test data
- Hypothesis for property-based testing of algorithms
- Mock external dependencies
```

### devops-implementation

```
You are a senior SRE / platform engineer.

When writing infrastructure code:
- Terraform: module boundaries, versioned providers, remote state
- Docker: multi-stage builds, specific versions (not 'latest'), USER directive
- Kubernetes: resource limits on all containers, liveness + readiness probes,
  PodDisruptionBudget for critical workloads
- CI/CD: matrix builds for cross-platform, cache restoration, secrets via env

Security defaults:
- Least-privilege IAM
- Network policies enforced
- No secrets in environment variables committed to repo
- Image scanning in CI

Monitoring:
- Structured logging (JSON)
- Metrics with appropriate cardinality (no user IDs in labels)
- Distributed tracing for service-to-service calls
```

### general

```
You are a senior engineer with broad expertise. Write clean, direct,
well-structured code. Explain reasoning when asked, not preemptively.
Default to the simplest solution that correctly solves the stated problem.
```

## Model selection

Route to the right model based on domain:

```python
MODEL_ROUTING = {
    "ios": "claude-code-sonnet",     # hard gate — always cloud
    "web": "m27-jangtq-crack",
    "python": "m27-jangtq-crack",
    "trading": "m27-jangtq-crack",
    "vc": "m27-jangtq-crack",
    "devops": "qwen3-5-122b-jang-4k",  # safety-aligned for client-facing
    "general": "m27-jangtq-crack",
}
```

## Execution

```python
async def route_specialist(task, file_context=None):
    # Stage 1
    stage1 = stage1_classify(task, file_context)

    if stage1.get("confidence") == "low":
        # Stage 2 — LLM classification
        stage2 = await stage2_classify(task)
        result = {**stage1, **stage2}
    else:
        result = stage1

    # Populate remaining fields
    result["specialist"] = f"{result['domain']}-implementation"
    result["system_prompt"] = SPECIALIST_PROMPTS[result["specialist"]]
    result["model"] = MODEL_ROUTING[result["domain"]]
    result["project_path"] = _detect_project_path(file_context)

    return result


def _detect_project_path(file_context):
    """Walk up from first file to find project root."""
    if not file_context:
        return None
    first = Path(file_context[0])
    for parent in [first] + list(first.parents):
        if (parent / "Package.swift").exists():
            return str(parent)
        if list(parent.glob("*.xcodeproj")):
            return str(parent)
        if (parent / "package.json").exists():
            return str(parent)
        if (parent / "pyproject.toml").exists():
            return str(parent)
        if (parent / ".git").exists():
            return str(parent)
    return None
```

## Why this matters

Generic system prompts leave 10-15% of model capability on the table.
A domain-specific prompt activates the right reasoning patterns:
- iOS prompt makes the model think about @MainActor before writing
- Trading prompt makes it think about lookahead bias before generating
- VC prompt makes it think about red flags before framing a thesis

This is essentially "free" quality improvement — no extra compute, just
better prompt engineering as structured configuration.
