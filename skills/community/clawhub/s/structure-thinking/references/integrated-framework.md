# Integrated Framework: Structure + Dynamics

## Core Premise
Good problem solving requires two things at once:
- A system model that explains why the behavior persists.
- A clear argument structure that makes decisions easy.

Build the model to find levers, then use the structure to communicate and decide.

## Unified Method

### Step 0: Orient
- Identify the decision owner, decision date, and success criteria.
- State the decision in one sentence.

### Step 1: Frame (SCQA)
- Draft Situation, Complication, Question.
- Write a provisional Answer.
- Capture assumptions and unknowns.

### Step 2: Model the System
- Define boundary and time horizon.
- List key stocks and flows.
- Draw reinforcing and balancing loops.
- Mark delays and information gaps.

### Step 3: Generate and Rank Hypotheses
- Use an issue tree with MECE buckets.
- Rank branches by impact and evidence availability.

### Step 4: Select Leverage Points
- Map top branches to leverage points.
- Propose 1-3 interventions with mechanisms.
- Identify risks, side effects, and system resistance.

### Step 5: Build the Argument
- Lead with the answer and 2-5 support points.
- Place evidence under each point.
- Keep each layer consistent and non-overlapping.

### Step 6: Validate and Iterate
- Run counterfactuals and stress tests.
- Update the model and argument as evidence changes.

## Evidence Strategy
- For each support point, define the minimum evidence needed.
- Add a falsification test: what would disprove it?
- Timebox data collection and proceed with best available data.

## Example Walkthrough (Software)
Problem: API latency spikes during peak traffic.

- Frame: Situation (latency target met historically), Complication (spikes during peak), Question (how to stabilize), Answer (shift load and remove a feedback bottleneck).
- Model: Stock = queued requests; flows = arrivals and completions; loop = slow responses -> retries -> more load -> slower responses.
- Leverage: information flow (better real-time load signals), rules (retry policy and rate limits), structure (autoscaling thresholds).
- Argument: Answer + 3 supports (retry loop is dominant, capacity response is too delayed, policy changes reduce amplification) with evidence under each.

## Output Checklist
- Top-line answer states action and rationale.
- System map highlights 2-3 dominant loops.
- Leverage points ranked by impact and risk.
- Intervention plan includes experiments and metrics.
- Argument outline ready for a memo or deck.
