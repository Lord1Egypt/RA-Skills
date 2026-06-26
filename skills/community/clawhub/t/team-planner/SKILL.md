---
name: team-planner
description: This skill should be used when the user wants to plan a team of AI agents to work on a complex task. It analyzes task requirements, designs team structure, defines member roles, and plans collaboration workflows. Trigger phrases include "plan a team", "design agent roles", "how should agents collaborate", or any request for multi-agent coordination strategy.
---

# Team Planner

## Overview

This skill enables the planning and design of multi-agent teams for complex tasks. It analyzes task requirements, determines optimal team composition, defines member roles and responsibilities, and establishes collaboration workflows. The skill produces comprehensive team architecture plans that can be executed in separate WorkBuddy sessions.

## When to Use This Skill

Use this skill when:
- User wants to plan a team of AI agents to work on a complex task
- User asks "how should I organize agents for this project?"
- User requests advice on agent roles and collaboration
- User mentions "team", "multiple agents", "parallel work", or "agent coordination"
- Task complexity suggests benefit from multi-agent collaboration
- User wants expert guidance on team architecture before implementation

## Planning Process

Follow this structured workflow to create a comprehensive team plan:

### Step 1: Task Analysis

Gather essential information about the task:

**Required Information:**
- Task goal and objectives
- Scope and boundaries (what's included/excluded)
- Technical domain(s) involved
- Complexity assessment (simple/medium/complex)

**Clarify if Needed:**
- Time constraints or deadlines
- Quality requirements
- Resource limitations
- Dependencies or prerequisites

**Ask Targeted Questions:**
- "What is the primary objective you want to achieve?"
- "What are the key components or subtasks involved?"
- "Are there any specific technologies, frameworks, or tools involved?"
- "What defines success for this task?"

### Step 2: Determine Team Necessity

Evaluate whether a multi-agent approach is appropriate:

**Use Multi-Agent Team When:**
- Task has clear independent subtasks that can run in parallel
- Requires different expertise domains (frontend, backend, research, testing)
- Benefits from parallel processing or time savings
- Task is too complex for single agent to handle efficiently
- Multiple perspectives or approaches are beneficial

**Use Single Agent When:**
- Task is straightforward and sequential
- Limited benefit from parallelization
- Communication overhead would outweigh benefits
- Task can be completed effectively by one agent

**Communicate Decision:**
- Explain reasoning clearly
- Provide justification for team vs. single agent approach

### Step 3: Design Team Structure

If multi-agent is appropriate, design the optimal team composition:

**Determine Member Count:**
- Analyze task decomposition
- Identify independent work streams
- Consider complexity vs. coordination overhead
- Aim for 3-6 members (avoid over-engineering)

**Define Member Roles:**
Each member should have a clear, focused role:

**Common Role Patterns:**
- `researcher`: Investigates options, analyzes approaches, gathers information
- `architect`: Designs system structure, makes technical decisions
- `developer`: Implements code, builds features
- `tester`: Writes tests, validates functionality
- `documenter`: Creates documentation, guides, specifications
- `analyst`: Processes data, generates insights
- `reviewer`: Reviews work, ensures quality standards

**Role Assignment Guidelines:**
- Each role should have distinct responsibilities
- Avoid overlapping responsibilities between roles
- Ensure all critical tasks are covered
- Consider dependencies between roles

### Step 4: Define Responsibilities

For each member, specify:

**Clear Responsibility Statement:**
- What this member is responsible for
- Scope of their work
- Key deliverables

**Example Format:**
```
Member: frontend-dev
Responsibilities:
- Implement React components for user interface
- Integrate with backend API endpoints
- Handle state management and data flow
- Ensure responsive design and accessibility
- Deliver: Complete frontend codebase
```

### Step 5: Plan Collaboration Workflow

Design how members will work together:

**Identify Dependencies:**
- Which members need results from others?
- What information must be shared?
- What are the critical path dependencies?

**Define Communication Patterns:**
- Regular status updates (broadcast)
- Direct requests for specific deliverables (message)
- Review and feedback loops

**Establish Workflow Phases:**
```
Phase 1: [Name] - Members: [list] - Description
Phase 2: [Name] - Members: [list] - Description
...
```

**Example Workflow:**
```
Phase 1: Research & Architecture
Members: researcher, architect
- Researcher investigates options
- Architect designs system
- Architect uses research findings

Phase 2: Parallel Development
Members: frontend-dev, backend-dev, tester
- Frontend and backend develop independently
- Tester writes test cases based on requirements

Phase 3: Integration & Testing
Members: developer, tester, documenter
- Integrate frontend and backend
- Run comprehensive tests
- Documenter writes user guide
```

### Step 6: Specify Communication Mechanisms

Define how members will communicate:

**Broadcast Usage:**
- Team announcements
- Phase transitions
- Important updates affecting everyone

**Direct Messaging Usage:**
- Requesting specific deliverables
- Providing targeted feedback
- Coordinating between specific members

**Shutdown Requests:**
- When a member completes work
- When another member needs results

### Step 7: Create Implementation Plan

Generate actionable instructions for execution:

**Startup Sequence:**
- Order to start members (consider dependencies)
- Any prerequisite setup
- Initial context to provide

**Example:**
```javascript
// Start in this order
1. Task(name="researcher", prompt="...")
2. Task(name="architect", prompt="...")
3. Task(name="frontend-dev", prompt="...")
4. Task(name="backend-dev", prompt="...")
5. Task(name="tester", prompt="...")
```

**Prompt Templates:**
Provide example prompts for each member's startup:
- Include role definition
- Specify responsibilities
- Mention collaboration expectations
- Reference deliverables

### Step 8: Document Success Criteria

Define how to measure team success:

**Phase Completion Criteria:**
- What must be done before moving to next phase?
- What artifacts should be produced?

**Overall Success Metrics:**
- Key deliverables
- Quality standards
- Integration points validated

## Output Format

Present the team plan in this structure:

### 1. Task Summary
- Objective: [Clear statement of goal]
- Scope: [What's included]
- Complexity: [Simple/Medium/Complex]
- Recommended Approach: [Single Agent / Multi-Agent Team]

### 2. Team Architecture
- **Team Size**: [Number] members
- **Rationale**: [Why this structure is optimal]

### 3. Member Roles

For each member:
#### Member Name: [name]
- **Role**: [role description]
- **Responsibilities**:
  - [Responsibility 1]
  - [Responsibility 2]
  - ...
- **Key Deliverables**: [What this member produces]
- **Dependencies**: [What this member needs from others]
- **Startup Prompt Template**: [Example prompt]

### 4. Collaboration Workflow

**Phase-by-Phase Plan:**
```
Phase 1: [Phase Name]
- Members involved: [list]
- Activities: [description]
- Completion criteria: [when done]
- Dependencies: [what needed to start]

Phase 2: [Phase Name]
...
```

### 5. Communication Strategy
- **Broadcast for**: [situations]
- **Direct messaging for**: [situations]
- **Key coordination points**: [list]

### 6. Startup Sequence
Provide ordered list of Task calls with example prompts

### 7. Success Criteria
- Phase completion checkpoints
- Final deliverables
- Integration validation requirements

## Best Practices

**Team Design:**
- Keep teams focused and minimal (3-6 members is typical)
- Ensure each member has clear, distinct responsibilities
- Minimize dependencies to enable parallel work
- Consider adding a coordinator for complex teams

**Collaboration:**
- Design clear handoff points between phases
- Establish regular communication rhythms
- Plan for integration and testing phases
- Include documentation as a first-class concern

**Execution Guidance:**
- Start members in dependency order
- Provide sufficient context in initial prompts
- Plan for member shutdown when their work is complete
- Include quality checkpoints between phases

## Examples

### Example 1: Full-Stack Web Application

**Task:** Build a blog system with user authentication, article management, and comments

**Team Structure:**
- `researcher`: Analyze tech stack options, compare frameworks
- `architect`: Design system architecture, database schema
- `backend-dev`: Implement API, database, authentication
- `frontend-dev`: Build React UI, integrate with API
- `tester`: Write tests, validate functionality
- `documenter`: Create API docs, user guide

**Workflow:**
```
Phase 1: Research & Architecture
Members: researcher, architect

Phase 2: Backend Development
Members: backend-dev, tester

Phase 3: Frontend Development
Members: frontend-dev, backend-dev (for API support)

Phase 4: Integration & Documentation
Members: all members
```

### Example 2: Data Analysis Project

**Task:** Analyze customer data and generate insights report

**Team Structure:**
- `data-collector`: Gather and clean data sources
- `analyst`: Perform statistical analysis, generate insights
- `visualizer`: Create charts and visualizations
- `reporter`: Compile findings into comprehensive report

**Workflow:**
```
Phase 1: Data Collection
Members: data-collector

Phase 2: Parallel Analysis
Members: analyst, visualizer
- Analyst works on statistics
- Visualizer designs charts based on early findings

Phase 3: Report Generation
Members: reporter, analyst, visualizer
- Combine analysis and visualizations
```

## Clarification Questions

If information is missing, ask:

1. **Task Scope**: "What are the main components or deliverables of this task?"
2. **Technical Requirements**: "Are there specific technologies, frameworks, or tools that must be used?"
3. **Constraints**: "Are there any time constraints, resource limitations, or quality standards?"
4. **Priorities**: "What aspects of this task are most critical to get right?"
5. **Success Definition**: "How will you know when the task is complete and successful?"

## Final Deliverable

The skill produces a **Team Architecture Plan** that includes:
- Clear recommendation on single agent vs. multi-agent approach
- If multi-agent: complete team structure with roles and responsibilities
- Collaboration workflow with phases and dependencies
- Communication strategy
- Startup sequence with example prompts
- Success criteria and validation checkpoints

This plan enables the user to execute the team plan in a separate WorkBuddy session by following the startup sequence and workflow defined.
