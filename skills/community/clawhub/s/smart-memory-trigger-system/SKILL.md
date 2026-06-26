---
name: intelligent-memory-trigger-system
displayName: Intelligent Memory Trigger System
description: "Intelligent system that automatically determines when to create workflow documentation based on task complexity, repetition patterns, and user intent. Transforms from 'passively waiting for instructions' to 'actively providing help'."
version: 2.0.0
type: skill
tags: memory, workflow, automation, intelligence, decision-making
---

# 🧠 Intelligent Memory Trigger System

## 🎯 Skill Overview
An intelligent system that automatically determines when to create workflow documentation based on task complexity, repetition patterns, and user intent. Transforms agents from "passively waiting for instructions" to "actively providing help."

## 📋 Usage Scenarios
Automatically triggers this skill when encountering the following situations:

### Mandatory Trigger Conditions (Hard Requirements)
1. **Steps ≥ 3**: Task contains 3 or more operational steps
2. **Cross-system ≥ 2**: Task involves 2 or more system components
3. **Configuration Changes**: Modifying core configuration files or system settings
4. **Repetition Occurrence**: Same or similar task appears for the 2nd time
5. **User Explicit Request**: User indicates "remember", "summarize", "process"

### Recommended Trigger Conditions
1. **Complexity Score ≥ 6 points** (see evaluation algorithm)
2. **Potential Reuse**: User mentions "next time", "in the future"
3. **Team Collaboration Tasks**: Involving multiple agent collaboration
4. **Error Risk**: Complex operations prone to errors

## 🧠 Core Decision Logic

### Complexity Evaluation Algorithm
```javascript
function evaluateComplexity(taskDescription) {
  let score = 0;
  
  // 1. Step Count Evaluation
  if (taskDescription contains "first step" and "second step") score += 2;
  if (taskDescription contains "third step") score += 2;
  if (taskDescription contains "fourth step" or "finally") score += 2;
  
  // 2. System Involvement Evaluation
  if (taskDescription contains "configuration file" or ".json") score += 1;
  if (taskDescription contains "command line" or "command") score += 1;
  if (taskDescription contains "restart" or "gateway") score += 1;
  if (taskDescription contains "Feishu" or "WeChat" or "platform") score += 1;
  
  // 3. Configuration Impact Evaluation
  if (taskDescription contains "configuration" or "settings") score += 1;
  if (taskDescription contains "modify" or "edit") score += 1;
  if (taskDescription contains "add" or "delete") score += 1;
  
  // 4. Collaboration Requirement Evaluation
  if (taskDescription contains "team" or "collaboration") score += 1;
  if (taskDescription contains "multiple" or "several") score += 1;
  
  return score;
}
```

### Decision Thresholds
- **Total Score ≥ 8 points** → Must create memory trigger
- **Total Score 6-7 points** → Recommend creating memory trigger
- **Total Score ≤ 5 points** → No need to create memory trigger

## 🔍 Repetition Pattern Detection

### Task Type Identification Keywords
```
System Configuration: ["configuration", "settings", "install", "deploy"]
File Operations: ["create", "edit", "delete", "move"]
Command Line: ["execute", "run", "command", "script"]
Platform Integration: ["Feishu", "WeChat", "API", "integration"]
```

### Repetition Detection Logic
When similarity between current task and historical tasks > 0.7, treat as repetition pattern and should create or reference existing workflow.

## 🎯 User Intent Analysis

### Explicit Request Keywords
```
Recording Requests: ["remember", "record", "save", "memo"]
Summary Requests: ["summarize", "organize", "arrange", "sort"]
Process Requests: ["process", "steps", "method", "operation"]
Future Use: ["next time", "in the future", "later", "repeat"]
```

When detecting these keywords, proactively ask if workflow documentation is needed.

## 💬 Proactive Inquiry Templates

### Based on Complexity
"Teacher Sun, this task appears to be relatively complex (score: X points) and may be reused. Would you like me to create a workflow document?"

### Based on Repetition Pattern
"Teacher Sun, this task is very similar to the previous [similar task]. Should I reference the previous workflow?"

### Based on User Intent
"Teacher Sun, you mentioned needing to [record/summarize/process]. Should I create the document now?"

### Based on Configuration Importance
"Teacher Sun, this configuration change may affect system stability. Should I record the detailed steps?"

## 📝 Workflow Document Creation

### Document Naming Convention
- `[task-type]-workflow.md`
- Example: `feishu-bot-configuration-workflow.md`

### Document Structure Requirements
1. **Workflow Overview**: Task objectives and value
2. **Configuration Steps**: Detailed operational steps (clearly numbered)
3. **Verification Methods**: How to verify successful configuration
4. **Common Issues**: Potential problems and solutions
5. **Related Files**: Involved configuration files and documents

### Storage Location
- Main Directory: `C:\Users\sjh65\.openclaw\workspace\workflows\`
- Quick Access: Dedicated documents in root directory

## 🔧 System Maintenance

### Regular Checks
- **Weekly**: Check task history, identify high-complexity tasks without workflows
- **Monthly**: Optimize complexity scoring standards
- **Quarterly**: Review and update all workflow documents

### Optimization Mechanism
- Adjust trigger conditions based on user feedback
- Optimize keywords based on actual usage
- Improve workflow documents based on task execution effectiveness

## 📈 Effectiveness Evaluation Metrics

### Quantitative Metrics
1. **Workflow Coverage**: Proportion of high-complexity tasks with established workflows
2. **Proactive Inquiry Rate**: Proportion of proactively asking to create workflows when needed
3. **User Reminder Rate**: Proportion needing user reminders to provide workflows (goal: reduce)
4. **Workflow Usage Rate**: Frequency of workflow documents being actually referenced

### Quality Metrics
1. **Workflow Completeness**: Whether steps are complete and clear
2. **Trigger Accuracy**: Whether keyword triggers are accurate
3. **User Satisfaction**: Whether workflows truly help with work

## 🎯 Practical Application Cases

### Case 1: Feishu Bot Configuration
- **Complexity Score**: 9 points (steps 4 + cross-system 3 + system impact 2)
- **Trigger Conditions**: Cross-system ≥ 2, configuration changes, repetition occurrence
- **Result**: Created `feishu-bot-configuration-workflow.md`
- **Trigger Keywords**: ["Feishu bot", "configure bot", "channel configuration", "pairing"]

### Case 2: File Reading
- **Complexity Score**: 3 points
- **Trigger Conditions**: None
- **Result**: No need to create workflow document

### Case 3: Model Testing
- **Complexity Score**: 6 points
- **Trigger Conditions**: Complexity score ≥ 6 points
- **Result**: Asked "Would you like me to create a workflow document?"

## 🔄 Complete Workflow

```
Start Task
    ↓
Analyze Task Description
    ↓
Evaluate Complexity (step count, system involvement, configuration impact)
    ↓
Check Task History (is it a repetitive type?)
    ↓
Analyze User Intent (are there "remember", "summarize" keywords?)
    ↓
    ┌─────────────────────┐
    │ Need to create memory trigger? │
    └─────────────────────┘
            ↓
    ┌─────────────────────┐
    │ Yes → Proactively ask user │
    │ No → Execute task normally │
    └─────────────────────┘
```

## 📋 Quick Reference

### Must Create Workflow Situations
1. Steps ≥ 3
2. Cross-system ≥ 2
3. Configuration changes
4. Task repeats for 2nd time
5. User explicit request
6. Complexity score ≥ 8 points

### Recommend Inquiry Situations
1. Complexity score 6-7 points
2. Potential reuse
3. Team collaboration tasks
4. Error risk

### No Need for Workflow Situations
1. Complexity score ≤ 5 points
2. Clearly one-time operations
3. Simple queries or information retrieval
4. Exploratory trial-and-error operations

---
*Skill Creation Time: 2026-03-18*
*Upgraded to English Version: 2026-03-20*
*Original Creator: Commander (based on Shrimp Assistant's design)*
*Upgraded By: Shrimp Assistant (main agent)*
*Goal: Achieve systematic, automated memory trigger decision-making*