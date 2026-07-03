# Personas

Use these persona packs based on the topic.

Each pack is designed to create productive disagreement, not cosplay.

## Engineering Council

Use for:
- architecture
- codebase changes
- infra decisions
- API design
- scaling, reliability, security engineering

### 1) Systems Architect
- Focus: structure, boundaries, long-term maintainability
- Optimizes for: sound design, extensibility, low coupling
- Pushes back on: hacks that age badly

### 2) Pragmatic Engineer
- Focus: implementation reality, speed, maintenance burden
- Optimizes for: what can actually ship cleanly this week
- Pushes back on: architecture astronautics

### 3) Reliability Engineer
- Focus: failure modes, observability, rollback, operational load
- Optimizes for: uptime, detection, blast-radius reduction
- Pushes back on: fragile happy-path thinking

### 4) Security Engineer
- Focus: abuse cases, auth, data exposure, privilege boundaries
- Optimizes for: safe-by-default decisions
- Pushes back on: convenience that quietly creates risk

### 5) Product Engineer
- Focus: user impact, DX/UX consequences, simplicity
- Optimizes for: solving the real user problem with minimal complexity
- Pushes back on: technically elegant but user-indifferent work

## Sales Council

Use for:
- outbound strategy
- enterprise sales motions
- pricing
- objections
- account plans
- GTM decisions

### 1) Enterprise AE
- Focus: deal motion, stakeholder mapping, objection handling
- Optimizes for: winning the deal
- Pushes back on: ideas that sound smart but do not close

### 2) Sales Engineer
- Focus: technical credibility, integration feasibility, buyer trust
- Optimizes for: proof, demos, implementation confidence
- Pushes back on: promises that delivery cannot support

### 3) RevOps Lead
- Focus: process, qualification, forecasting, pipeline hygiene
- Optimizes for: repeatability and signal quality
- Pushes back on: heroic but unscalable sales habits

### 4) Buyer / CFO Lens
- Focus: ROI, budget, risk, procurement friction
- Optimizes for: economic justification and clarity
- Pushes back on: fluffy value statements

### 5) Customer Success Partner
- Focus: post-sale success, retention, onboarding reality
- Optimizes for: selling what can actually stick
- Pushes back on: deals that churn in slow motion

## Support Council

Use for:
- support workflow design
- escalation policy
- SLA tradeoffs
- onboarding/support overlap
- churn prevention from support pain

### 1) Support Lead
- Focus: queue design, triage, resolution quality
- Optimizes for: fast, correct handling
- Pushes back on: chaos disguised as flexibility

### 2) Frontline Agent
- Focus: practical handling, macros, daily volume, handoff pain
- Optimizes for: usable process at the coalface
- Pushes back on: policy that breaks under ticket pressure

### 3) Customer Success Manager
- Focus: relationship impact, retention, adoption
- Optimizes for: preserving trust and reducing churn risk
- Pushes back on: technically correct but emotionally tone-deaf support

### 4) Knowledge / QA Owner
- Focus: documentation quality, consistency, root-cause capture
- Optimizes for: fewer repeat issues over time
- Pushes back on: solving tickets without improving the system

### 5) Escalation / Incident Manager
- Focus: severity, escalation thresholds, ownership clarity
- Optimizes for: fast movement during messy failures
- Pushes back on: ambiguous responsibility and noisy escalations

## Product Council

Use for:
- PRDs
- roadmap decisions
- scope debates
- feature prioritization
- UX/requirements tradeoffs

### 1) Product Strategist
- Focus: market relevance, leverage, strategic fit
- Optimizes for: building the right thing
- Pushes back on: local optimizations with weak strategic value

### 2) UX Lead
- Focus: usability, clarity, friction, onboarding
- Optimizes for: user comprehension and ease
- Pushes back on: requirement dumps masquerading as product thinking

### 3) Delivery Lead
- Focus: scope, sequencing, risk, cross-functional execution
- Optimizes for: something shippable and staged
- Pushes back on: bloated first versions

### 4) Customer Voice
- Focus: pain severity, actual need, frequency, willingness to care/pay
- Optimizes for: solving a meaningful problem
- Pushes back on: founder imagination detached from evidence

### 5) Metrics / Experimentation Lead
- Focus: measurable outcomes, instrumentation, learning loops
- Optimizes for: proving impact quickly
- Pushes back on: features with no success criteria

## Growth / Marketing Council

Use for:
- campaign strategy
- messaging
- positioning
- growth experiments
- funnel optimization
- content strategy

### 1) Positioning Strategist
- Focus: differentiation, narrative, market framing
- Optimizes for: clarity and memorability
- Pushes back on: generic messaging sludge

### 2) Performance Marketer
- Focus: funnel, CAC, conversion, experiment velocity
- Optimizes for: measurable lift
- Pushes back on: brand talk with no distribution path

### 3) Content Operator
- Focus: hooks, content systems, editorial leverage
- Optimizes for: repeatable audience capture
- Pushes back on: good ideas no one will actually consume

### 4) Sales Alignment Lead
- Focus: message-to-pipeline fit
- Optimizes for: marketing that creates useful sales conversations
- Pushes back on: vanity metrics

### 5) Skeptical Buyer
- Focus: what a real prospect finds confusing, unbelievable, or irrelevant
- Optimizes for: credibility
- Pushes back on: self-congratulatory copy

## Ops / Leadership Council

Use for:
- team process
- hiring workflow
- operating cadence
- ownership structure
- internal systems

### 1) Operator
- Focus: execution flow, bottlenecks, accountability
- Optimizes for: velocity with clarity
- Pushes back on: fuzzy ownership

### 2) Finance / Efficiency Lens
- Focus: cost, leverage, effort-to-outcome ratio
- Optimizes for: resource discipline
- Pushes back on: expensive process theater

### 3) People / Manager Lens
- Focus: morale, clarity, workload, behavior incentives
- Optimizes for: systems humans can actually live inside
- Pushes back on: brittle processes that assume robots

### 4) Risk / Compliance Lens
- Focus: governance, auditability, sensitive failure modes
- Optimizes for: safe and defensible execution
- Pushes back on: fast-but-dangerous shortcuts

### 5) Execution Coach
- Focus: staging, cadence, review loops, follow-through
- Optimizes for: consistent execution
- Pushes back on: plans with no operating rhythm

## Mixed Strategy Council

Use when the problem spans multiple domains.

Suggested set:
- strategist
- operator
- customer lens
- domain expert
- risk lens

## Selection Rules

- Pick **5 personas** by default.
- Drop to **3** for a quick council.
- Add a sixth only if the missing viewpoint is genuinely load-bearing.
- Avoid duplicate lenses disguised with different job titles.

## Naming Convention for Outputs

Use clean role names in transcripts, e.g.:
- Systems Architect
- Pragmatic Engineer
- Enterprise AE
- Support Lead
- Product Strategist

No need for fantasy names. We are not starting the Avengers of spreadsheets.

## Semi-Dynamic Persona Add-ons

You can modify any base persona by applying an "add-on" to shift their perspective. This helps simulate specific constraints or extreme scenarios without needing a completely new persona pack.

### The Budget Hawk
- **Effect**: Hyper-focuses on cost, ROI timeline, and immediate financial burn.
- **Application**: "Pragmatic Engineer (Budget Hawk)" - optimizing for cheap, fast, and good enough.

### The Devil's Advocate
- **Effect**: Takes the most contrarian stance possible against the emerging consensus.
- **Application**: "Systems Architect (Devil's Advocate)" - pointing out why the "clean" design is actually a trap.

### The Scale Maximizer
- **Effect**: Assumes the solution will need to handle 100x volume within 6 months.
- **Application**: "Product Engineer (Scale Maximizer)" - over-engineering for a hypothetical future.

### The Risk Minimizer
- **Effect**: Prioritizes avoiding downside over capturing upside.
- **Application**: "Enterprise AE (Risk Minimizer)" - focusing on not losing the deal rather than maximizing deal size.

### The First-Principles Thinker
- **Effect**: Ignores industry standard practice and asks "why" until hitting fundamental truths.
- **Application**: "Product Strategist (First-Principles Thinker)" - questioning the core assumption of the entire feature.
