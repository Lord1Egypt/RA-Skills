# Memory Trigger Decision Logic

## 🧠 Decision Flowchart
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

## 📊 Complexity Evaluation Algorithm

### Input: Task Description
### Output: Complexity Score (0-10 points)

```javascript
function evaluateComplexity(task) {
  let score = 0;
  
  // 1. Step Count Evaluation
  if (task.contains("first step") && task.contains("second step")) score += 2;
  if (task.contains("third step")) score += 2;
  if (task.contains("fourth step") || task.contains("finally")) score += 2;
  
  // 2. System Involvement Evaluation
  if (task.contains("configuration file") || task.contains(".json")) score += 1;
  if (task.contains("command line") || task.contains("command")) score += 1;
  if (task.contains("restart") || task.contains("gateway")) score += 1;
  if (task.contains("Feishu") || task.contains("WeChat") || task.contains("platform")) score += 1;
  
  // 3. Configuration Impact Evaluation
  if (task.contains("configuration") || task.contains("settings")) score += 1;
  if (task.contains("modify") || task.contains("edit")) score += 1;
  if (task.contains("add") || task.contains("delete")) score += 1;
  
  // 4. Collaboration Requirement Evaluation
  if (task.contains("team") || task.contains("collaboration")) score += 1;
  if (task.contains("multiple") || task.contains("several")) score += 1;
  
  return score;
}
```

### Scoring Interpretation
- **0-3 points**: Simple task, no workflow needed
- **4-5 points**: Moderate complexity, consider workflow
- **6-7 points**: High complexity, recommend workflow
- **8-10 points**: Very high complexity, must create workflow

## 🔍 Repetition Pattern Detection

### Similarity Calculation
```javascript
function calculateSimilarity(task1, task2) {
  // Extract keywords from both tasks
  const keywords1 = extractKeywords(task1);
  const keywords2 = extractKeywords(task2);
  
  // Calculate Jaccard similarity
  const intersection = keywords1.filter(k => keywords2.includes(k)).length;
  const union = new Set([...keywords1, ...keywords2]).size;
  
  return intersection / union;
}

function extractKeywords(text) {
  const keywords = [
    // System configuration
    "configuration", "settings", "install", "deploy", "setup",
    // File operations
    "create", "edit", "delete", "move", "copy", "rename",
    // Command line
    "execute", "run", "command", "script", "terminal",
    // Platform integration
    "Feishu", "WeChat", "API", "integration", "connect",
    // Common operations
    "backup", "restore", "update", "upgrade", "test"
  ];
  
  return keywords.filter(keyword => text.toLowerCase().includes(keyword));
}
```

### Repetition Threshold
- **Similarity > 0.7**: Strong repetition, reference existing workflow
- **Similarity 0.4-0.7**: Moderate repetition, consider creating workflow
- **Similarity < 0.4**: Weak repetition, treat as new task

## 🎯 User Intent Analysis

### Explicit Intent Keywords
```javascript
const explicitIntentKeywords = {
  recording: ["remember", "record", "save", "memo", "document"],
  summary: ["summarize", "organize", "arrange", "sort", "compile"],
  process: ["process", "steps", "method", "operation", "procedure"],
  future: ["next time", "in the future", "later", "repeat", "again"]
};
```

### Implicit Intent Detection
```javascript
function detectImplicitIntent(task) {
  const implicitIndicators = {
    // Questions about process
    "how to": 0.8,
    "what are the steps": 0.9,
    "can you show me": 0.7,
    
    // References to future use
    "for future reference": 0.9,
    "so I can do it again": 0.8,
    "in case I need it later": 0.85,
    
    // Complexity indicators
    "complicated": 0.6,
    "multiple steps": 0.7,
    "tricky": 0.5
  };
  
  let maxScore = 0;
  for (const [indicator, score] of Object.entries(implicitIndicators)) {
    if (task.toLowerCase().includes(indicator)) {
      maxScore = Math.max(maxScore, score);
    }
  }
  
  return maxScore;
}
```

## 📝 Decision Matrix

### Decision Rules
| Condition | Score Range | User Intent | Repetition | Decision |
|-----------|-------------|-------------|------------|----------|
| Hard Requirement | Any | Any | Any | Create Workflow |
| Complexity | 8-10 | Any | Any | Create Workflow |
| Complexity | 6-7 | Medium-High | Any | Ask User |
| Complexity | 6-7 | Low | High | Create Workflow |
| Complexity | 4-5 | High | High | Ask User |
| Complexity | 0-3 | Any | Any | No Workflow |

### Hard Requirements (Always Create Workflow)
1. Steps ≥ 3
2. Cross-system ≥ 2
3. Configuration changes
4. Task repeats for 2nd time
5. User explicit request

## 💬 Inquiry Decision Logic

### When to Ask
```javascript
function shouldAskUser(complexityScore, userIntentScore, repetitionScore) {
  // Hard requirements always ask
  if (hasHardRequirements()) return true;
  
  // High complexity with medium intent
  if (complexityScore >= 8 && userIntentScore >= 0.5) return true;
  
  // Medium complexity with high intent or repetition
  if (complexityScore >= 6 && (userIntentScore >= 0.7 || repetitionScore >= 0.7)) return true;
  
  // Any complexity with very high intent
  if (userIntentScore >= 0.9) return true;
  
  return false;
}
```

### Inquiry Templates Selection
```javascript
function selectInquiryTemplate(primaryReason, secondaryReason) {
  const templates = {
    complexity: "Teacher Sun, this task appears to be relatively complex (score: {score} points) and may be reused. Would you like me to create a workflow document?",
    repetition: "Teacher Sun, this task is very similar to the previous '{similarTask}'. Should I reference the previous workflow?",
    userIntent: "Teacher Sun, you mentioned needing to {action}. Should I create the document now?",
    configuration: "Teacher Sun, this configuration change may affect system stability. Should I record the detailed steps?"
  };
  
  return templates[primaryReason]
    .replace("{score}", complexityScore)
    .replace("{similarTask}", similarTaskName)
    .replace("{action}", detectedAction);
}
```

## 🔄 Workflow Creation Logic

### Document Structure Generation
```javascript
function generateWorkflowStructure(taskType, steps, verificationMethods) {
  return {
    metadata: {
      taskType: taskType,
      created: new Date().toISOString(),
      complexityScore: complexityScore,
      creator: "Intelligent Memory Trigger System"
    },
    content: {
      overview: generateOverview(taskType),
      prerequisites: identifyPrerequisites(),
      steps: formatSteps(steps),
      verification: verificationMethods,
      troubleshooting: commonIssues(),
      relatedFiles: identifyRelatedFiles()
    }
  };
}
```

### Storage Decision
```javascript
function determineStorageLocation(importance, frequency) {
  if (importance >= 8 || frequency >= 0.7) {
    return "C:\\Users\\sjh65\\.openclaw\\workspace\\workflows\\priority\\";
  } else if (importance >= 6 || frequency >= 0.5) {
    return "C:\\Users\\sjh65\\.openclaw\\workspace\\workflows\\standard\\";
  } else {
    return "C:\\Users\\sjh65\\.openclaw\\workspace\\workflows\\archive\\";
  }
}
```

## 📊 Performance Metrics Calculation

### Real-time Metrics
```javascript
function calculateRealTimeMetrics() {
  return {
    workflowCoverage: calculateCoverage(),
    proactiveInquiryRate: calculateInquiryRate(),
    userReminderRate: calculateReminderRate(),
    workflowUsageRate: calculateUsageRate(),
    decisionAccuracy: calculateAccuracy()
  };
}

function calculateCoverage() {
  const highComplexityTasks = getHighComplexityTasks();
  const workflowsCreated = getWorkflowsCreated();
  return workflowsCreated.length / highComplexityTasks.length;
}

function calculateInquiryRate() {
  const shouldInquire = getShouldInquireCount();
  const didInquire = getDidInquireCount();
  return didInquire / shouldInquire;
}
```

## 🔧 System Tuning Parameters

### Adjustable Parameters
```javascript
const tuningParameters = {
  // Complexity scoring weights
  stepWeight: 2.0,
  systemWeight: 1.0,
  configWeight: 1.0,
  collaborationWeight: 1.0,
  
  // Decision thresholds
  mustCreateThreshold: 8,
  recommendThreshold: 6,
  askThreshold: 0.7,
  
  // Similarity thresholds
  strongRepetition: 0.7,
  moderateRepetition: 0.4,
  
  // Intent thresholds
  highIntent: 0.9,
  mediumIntent: 0.7,
  lowIntent: 0.5
};
```

### Auto-tuning Algorithm
```javascript
function autoTuneParameters(performanceData) {
  // Adjust based on workflow coverage
  if (performanceData.coverage < 0.7) {
    tuningParameters.mustCreateThreshold -= 1;
    tuningParameters.recommendThreshold -= 1;
  }
  
  // Adjust based on inquiry rate
  if (performanceData.inquiryRate < 0.8) {
    tuningParameters.askThreshold -= 0.1;
  }
  
  // Adjust based on accuracy
  if (performanceData.accuracy < 0.8) {
    // Be more conservative
    tuningParameters.mustCreateThreshold += 1;
    tuningParameters.askThreshold += 0.1;
  }
}
```

---
*Document Created: 2026-03-18*
*Upgraded to English Version: 2026-03-20*
*Algorithm Version: 2.0*
*Maintained By: Shrimp Assistant (main agent)*
*Next Algorithm Review: 2026-04-20*