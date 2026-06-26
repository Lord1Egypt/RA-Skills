---
name: source-code-analysis
description: This skill should be used when the user asks to "analyze source code", "understand this codebase", "perform code analysis", "study this project", "explain this repository", or discusses source code learning, codebase comprehension, open source project analysis, understanding software architecture, or learning from existing code.
version: 1.0.0
---

# Source Code Analysis

This skill provides a systematic 7-step methodology for analyzing and understanding source code repositories. It helps developers efficiently comprehend complex codebases by focusing on high-value content and following a structured approach.

## Core Methodology

### The 7-Step Analysis Process

1. **Build Global Cognition**
   - Create a mental map before diving into details
   - Understand project structure, directory organization, and code distribution
   - Identify main entry points and startup sequences
   - Recognize architectural patterns from directory structure

2. **Trace Core Pathways**
   - Follow complete functional chains end-to-end
   - Track user requests from input to output
   - Understand data flow and transformation through the system
   - Map key call chains and interaction patterns

3. **Understand Design Decisions**
   - Comprehend design rationale and architectural trade-offs
   - Identify key design patterns and abstractions
   - Learn why certain technical choices were made
   - Understand extension mechanisms and plugin systems

4. **Examine Engineering Practices**
   - Focus on production code realities, not ideals
   - Study error handling and edge case patches
   - Learn from code comments and engineering wisdom
   - Understand technical debt as conscious choices

5. **Running Analysis**
   - Validate understanding through actual execution
   - Analyze build, test, and deployment processes
   - Verify assumptions by running code
   - Use debugging tools to observe runtime behavior

6. **Identify Core 20%**
   - Focus on high-value paths, not all files equally
   - Prioritize startup entries, core logic, extension mechanisms
   - Identify configuration management and state management systems
   - Map external interaction boundaries

7. **Feature Deep-Dive**
   - Use specific features to understand the broader system
   - Trace implementation details of key functionality
   - Expand understanding outward from focused points
   - Follow one thread through the entire system

## When This Skill Applies

This skill activates when the user's request involves:
- Analyzing unfamiliar codebases
- Understanding open source projects
- Learning from existing software architecture
- Planning contributions to open source
- Evaluating technologies and frameworks
- Studying design patterns and implementation
- Comprehending complex software systems

## Analysis Approach

### Before Starting

Always ask clarifying questions:
1. **What is your goal?** Learning, contributing, evaluating, or fixing?
2. **What's your experience level?** Beginner, intermediate, or advanced?
3. **What specifically interests you?** Architecture, features, patterns, or practices?
4. **How deep should the analysis go?** Overview, standard, deep, or comprehensive?

### During Analysis

**Follow this systematic approach:**

1. **Start with questions before code**
   - What problem does this project solve?
   - Who are the users/clients of this code?
   - What are the core concepts and terminology?

2. **Establish global cognition first**
   - Read README and documentation
   - Examine directory structure
   - Identify main entry points
   - Map module organization
   - Understand technology stack

3. **Trace one complete pathway**
   - Choose a user-visible feature
   - Follow it from input to output
   - Document key files and functions
   - Understand data transformation
   - Map module interactions

4. **Understand design decisions**
   - Question "why" not just "what"
   - Identify trade-offs and constraints
   - Understand extension mechanisms
   - Learn architectural patterns

5. **Study engineering practices**
   - Look for error handling patterns
   - Find performance optimizations
   - Read valuable comments
   - Understand testing approach

### Output Format

**Structure your analysis with these sections:**

#### 1. Executive Summary
- Project purpose and core functionality
- Key technologies and patterns
- Overall architecture style
- Main findings and recommendations

#### 2. Global Cognition Report
```
## Project Overview
- **Core Goal**: [What problem it solves]
- **Main Features**: [Key functionality]
- **Technology Stack**: [Languages, frameworks, tools]
- **Code Scale**: [Size metrics]

## Architecture Analysis
- **Architecture Pattern**: [Identified pattern]
- **Directory Organization**: [Structure analysis]
- **Module Boundaries**: [Main modules and responsibilities]
- **Entry Points**: [Startup and initialization]
```

#### 3. Core Pathways
```
## Feature: [Feature Name]
### Entry Point
- File: [path/to/file.ts:line-number]
- Function: [functionName()]

### Execution Flow
1. [Step 1] → [file:line]
2. [Step 2] → [file:line]
3. [Step 3] → [file:line]

### Data Flow
[Diagram or description of data transformation]
```

#### 4. Design Insights
```
## Key Design Decisions

### [Decision Name]
- **What**: [Description]
- **Why**: [Rationale]
- **Trade-offs**: [Considerations]
- **Alternatives considered**: [Other options]
```

#### 5. Engineering Practices
```
## Production Realities

### Error Handling
[Patterns and approaches found]

### Performance Optimizations
[Techniques and their rationale]

### Code Quality Practices
[Testing, documentation, standards]
```

#### 6. High-Value Files (The 20%)
```
## Priority Reading List

1. **[file-path]** - [Why it's critical]
2. **[file-path]** - [Why it's critical]
3. **[file-path]** - [Why it's critical]
...
```

#### 7. Learning Recommendations
```
## For [Beginner|Intermediate|Advanced] Learners

### Recommended Path
1. [Stage 1]: [Goal] → [Files to read]
2. [Stage 2]: [Goal] → [Files to read]
3. [Stage 3]: [Goal] → [Files to read]

### Practice Suggestions
[Specific exercises and projects]
```

## Best Practices

### For Analysts

- **Question-driven**: Always have specific questions before diving in
- **Progressive depth**: Start broad, then go deep selectively
- **Validation**: Run code to verify understanding
- **Documentation**: Take notes and document findings
- **Focus**: Avoid getting lost in details; stay on high-value paths

### Common Mistakes to Avoid

- **Starting at random**: Don't just open files and read linearly
- **Equal attention**: Not all files deserve equal study time
- **Missing the forest**: Don't get lost in trees; maintain global view
- **Static-only**: Don't just read; run and observe
- **Syntax over semantics**: Focus on design, not just code structure

### High-Value Indicators

**Prioritize files that are:**
- Entry points (main, index, app, server)
- Core logic (engine, core, kernel, handler)
- Extension mechanisms (plugin, adapter, strategy)
- Configuration (config, settings, options)
- State management (store, state, context, session)
- External interfaces (api, client, driver, protocol)

**Lower priority:**
- Tests (unless understanding behavior)
- Build tools (unless deployment focus)
- Documentation (already in README)
- Utility functions (use on-demand basis)

## Example Analyses

### Quick Overview Mode
```
"Give me a quick overview of the Next.js codebase focusing on
the routing system and server components"
```

### Deep Feature Analysis
```
"Trace the complete implementation of React's useState hook,
including the fiber architecture integration and scheduler coordination"
```

### Design Philosophy
```
"Analyze the design decisions in Go's standard library,
focusing on error handling philosophy and interface design"
```

### Learning Path Creation
```
"Create a learning path for an intermediate developer to
understand the TypeScript compiler, focusing on the type checking system"
```

## Integration with Other Tools

This skill works well with:
- **Read tool**: For examining file contents
- **Grep tool**: For finding patterns and usage
- **Glob tool**: For discovering file organization
- **Explore agent**: For parallel codebase investigation
- **Plan agent**: For architectural analysis

## Notes

- This methodology is based on proven approaches for understanding complex software systems
- The 20% rule comes from the observation that a small percentage of files contain most architectural insight
- Progressive understanding prevents getting overwhelmed by large codebases
- Question-driven analysis ensures relevance and efficiency
- Running code validates theoretical understanding

---

**Version**: 1.0.0
**Methodology**: 7-Step Source Code Analysis Framework
**Target Users**: Developers learning new codebases, open source contributors, technical leads, software engineering students
