---
name: task-orchestrator
description: Intelligent task management and execution coordination officer. Automatically generates task lists, intelligently decomposes complex tasks, matches AI agents, makes priority decisions, and monitors progress.
---

# Task Orchestrator

End-to-end automated task management: from goals to execution, intelligent decomposition, agent matching, and progress monitoring.

## Use Cases
- User mentions keywords such as "task management," "task planning," "task decomposition," "multi-task parallelism," "task orchestration"
- User needs to decompose complex objectives into executable steps
- User needs multiple Agents to collaborate on work
- User needs to track task progress and resource allocation
- User needs intelligent decision-making for execution order and dependencies.

## Core Capabilities

### 1. Task Parsing and Decomposition
Automatically decompose natural language objectives into a structured task tree:
- **Goal Decomposition**: Break complex objectives into atomic tasks
- **Dependency Identification**: Establish dependency relationships between tasks
- **Effort Estimation**: Estimate execution time based on task complexity

### 2. Intelligent Agent Matching
Match the most suitable execution agent based on task characteristics:
- **Capability Matching**: Select specialized agents based on task type
- **Load Balancing**: Avoid agent overload
- **Cost Optimization**: Balance quality and cost

### 3. Priority Decision-Making
Autonomously decide task execution order:
- **Urgency Assessment**: Based on time constraints and impact scope
- **Value Assessment**: Based on business value and user expectations
- **Dependency Priority**: Ensure dependency chains execute correctly

### 4. Progress Monitoring
Track task execution status in real time:
- **Status Tracking**: Pending, In Progress, Completed, Blocked
- **Anomaly Detection**: Identify timed-out, failed, and blocked tasks
- **Automatic Retry**: Intelligent retry strategy for failed tasks

## Workflow

```
User Goal → Task Parsing → Task Decomposition → Dependency Analysis → Priority Sorting → Agent Matching → Execution → Monitoring → Summary
```

### Step 1: Receive and Parse Goal

Understand user intent and identify core objectives:
- Clarify task boundaries and expected outputs
- Identify time constraints and priority hints
- Confirm available resources and constraints

**Example Dialogue:**
```
User: "Help me complete a product launch, including documentation, testing, and promotional materials"
Orchestrator: Parse goal into 3 main tasks:
  1. Product documentation writing (parallelizable)
  2. Test case design and execution (depends on partial completion of 1)
  3. Promotional material production (parallelizable)
```

### Step 2: Task Decomposition

Use a script to generate a structured task tree:

```bash
python3 scripts/task_decomposer.py --goal "User Goal" --output tasks.json
```

Output structure:
```json
{
  "main_goal": "Product Launch",
  "tasks": [
    {
      "id": "T1",
      "title": "Write Product Documentation",
      "description": "Includes feature descriptions, user guides, and API documentation",
      "priority": "high",
      "estimated_time": "2h",
      "dependencies": [],
      "subtasks": [
        {"id": "T1.1", "title": "Feature Description Document"},
        {"id": "T1.2", "title": "User Guide"},
        {"id": "T1.3", "title": "API Interface Documentation"}
      ],
      "required_skills": ["doc-writing-skill"],
      "status": "pending"
    }
  ]
}
```

### Step 3: Agent Matching and Resource Allocation

Select execution agents based on task characteristics. See [references/agent_matching.md](references/agent_matching.md) for details.

### Step 4: Execution and Monitoring

Initiate task execution and continuously monitor:
- Execute tasks without dependencies in parallel
- Execute tasks with dependencies serially
- Update task status in real time
- Automatically adjust plans upon anomalies

### Step 5: Result Integration and Feedback

After task completion:
- Integrate execution results from each agent
- Generate an execution report
- Collect feedback to optimize subsequent tasks

## Quick Start

### Scenario 1: Complex Task Decomposition

```
User: "Help me prepare for next week's tech sharing session; I need a PPT, demo code, and a promotional poster"

Orchestrator: 
1. Parse Goal → Identify 3 parallel tasks
2. Decompose Tasks → Estimate total effort 8h
3. Match Agents → 
   - PPT: doc-writing-skill + ppt-parser-local
   - Demo: Code generation agent
   - Poster: image_generation
4. Suggest Execution Order → PPT outline → demo development → poster design → PPT refinement
```

### Scenario 2: Multi-Agent Collaboration

```
User: "Complete a competitive analysis report; need data scraping, chart generation, and report writing"

Orchestrator:
1. Task Decomposition: Data scraping (T1) → Data analysis (T2) → Chart generation (T3) → Report writing (T4)
2. Dependency Chain: T1→T2→T3→T4
3. Agent Matching:
   - T1: web-search + deep-search-skill
   - T2: Data analysis agent
   - T3: image_generation
   - T4: doc-writing-skill
4. Execution Plan: Serial execution, estimated total duration 6h
```

## Decision Framework

### Priority Decision Matrix

| Dimension | Weight | Scoring Criteria |
|-----------|--------|------------------|
| Urgency | 30% | Deadline, blocking impact |
| Value | 40% | Business value, user expectations |
| Cost | 20% | Time cost, resource consumption |
| Risk | 10% | Failure risk, dependency risk |

### Agent Selection Strategy

See [references/agent_matching.md](references/agent_matching.md) for details.

## Resource Files

### scripts/
- `task_decomposer.py` - Task decomposition script, generates structured task tree
- `priority_calculator.py` - Priority calculation script, supports custom weights
- `progress_monitor.py` - Progress monitoring script, tracks task status in real time

### references/
- `agent_matching.md` - Agent matching strategies and capability matrix
- `workflow_patterns.md` - Common workflow patterns and best practices
- `task_templates.md` - Common task template library

### assets/
- `task_plan_template.md` - Task planning document template
- `execution_report_template.md` - Execution report template