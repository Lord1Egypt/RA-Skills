---
name: token-kill
description: Reduce OpenClaw token consumption by 95%+ using three optimization techniques (slash commands, script-first principle, and model tiering)
---

# Token Kill - OpenClaw Token Optimizer

Need help optimizing your OpenClaw token usage costs? This Skill will guide you through three powerful optimization techniques to dramatically reduce token consumption.

Based on real-world case studies, applying these optimization techniques can reduce token consumption from **$200+/day** to **$10/day**, achieving a **95%+ cost reduction**.

## Three Core Token Optimization Techniques

### 1️⃣ Slash Commands Optimization
- `/new` - Start a fresh conversation and clear old context (saves 50,000+ tokens)
- `/compress` - Compress memory by keeping important info and forgetting details (saves 30,000+ tokens)
- `/stop` - Immediately stop current task to prevent further token consumption
- `/restart` - Restart the system to clear lag and resolve issues

### 2️⃣ Script-First Principle
**Core Philosophy: AI is your brain, not your hands**

Automate with scripts instead of using the model for mechanical tasks:
- 📧 **Email Checking** - Scripts monitor emails; AI only notified of new messages ($100+/month → <$1/month)
- 🌤️ **Weather Queries** - Direct API calls, zero token consumption
- 📊 **Data Fetching** - Scripts retrieve data; AI only handles formatting
- ⏰ **Scheduled Tasks** - Scripts execute; prevent AI from polling
- 🔄 **Data Processing** - Script handles transformations

### 3️⃣ Model Tiering Strategy
**Use premium models for complex tasks, budget models for simple ones**

| Complexity | Recommended Model | Cost | Use Cases | Savings |
|-----------|------------------|------|-----------|---------|
| 🔴 High | GPT-4 / Claude | $0.03/1k tokens | Code generation, creative writing, complex reasoning | Baseline |
| 🟡 Medium | GPT-3.5-Turbo / Ernie | $0.0005/1k tokens | General tasks, text editing | 98% |
| 🟢 Low | Qwen, Tongyi (Budget Models) | $0.00001/1k tokens | Data processing, report generation, formatting | **99.97%** |

## Real-World Cost Reduction Cases

### Case 1: Email Monitoring System
**Problem**: Model checks emails every 5 minutes

| Approach | Monthly Cost |
|----------|-------------|
| ❌ Model Polling | **$100+/month** |
| ✅ Script + AI Notification | **<$1/month** |
| **Savings** | **99%** |

### Case 2: Daily Report Generation
**Scenario**: Generate reports every 30 minutes (2000 tokens/call)

| Model | Daily Cost | Monthly Cost | Savings |
|-------|-----------|-------------|---------|
| GPT-4 | $2.88 | $86 | Baseline |
| GPT-3.5 | $0.048 | $1.44 | 98% |
| Qwen | $0.001 | $0.03 | **99.97%** |

## Examples

### Example 1: Compressing Large Memory
**Scenario**: After many conversations, memory.md has grown to hundreds of thousands of characters

**Solution**:
1. Execute `/compress` command
2. System removes trivial details while preserving core information
3. Memory size reduced by 30-50%

**Result**: Reduced context loading on each turn, saves 30,000+ tokens

### Example 2: Replacing AI with Scripts
**Scenario**: Need to check for new orders every hour

**Wrong Approach**:
```
Have model check orders API every hour
→ Model must understand and judge each time
→ 24 checks per day = huge costs
```

**Correct Approach**:
```
Script checks order API every hour
Notify model only on new orders
Model handles decision-making only
```

**Savings**: Script uses only CPU, saves 90%+ tokens

### Example 3: Model Tiering Workflow
**Scenario**: Handle various complexity levels

**Strategy**:
- 💻 **Code Writing** → GPT-4 (worth the investment)
- 📝 **Content Editing** → GPT-3.5 (good balance)
- 📊 **Report Generation** → Budget Model (fully sufficient)

**Result**: 90% cost reduction, zero functionality loss

## Guidelines

### ✅ Best Practices for Token Savings

#### 1. Use Slash Commands Regularly
- **Execute `/compress` once daily** - Prevent memory bloat
- **Use `/new` for long conversations** - Start fresh after 1+ hours
- **Use `/stop` on wrong tasks** - Stop immediately to prevent waste

#### 2. Strictly Follow Script-First Principle
- ✅ **Scripts handle**: Scheduled checks, data fetching, API calls, data processing
- ❌ **Never let AI handle**: Polling, mechanical work, repetitive checks, resource-intensive operations
- 💡 **Core rule**: AI = decision-making and judgment; Scripts = execution and heavy lifting

#### 3. Enforce Model Tiering
| Task Type | Model Choice | Reason |
|-----------|-------------|--------|
| Code generation, deep analysis | GPT-4 | Complex tasks worth the cost |
| General tasks, text editing | GPT-3.5 | Best value proposition |
| Data processing, reports | Budget Models | Fully capable, lowest cost |

#### 4. Regular Token Usage Audit
- Review billing distribution
- Identify high-cost tasks for optimization
- Adjust model configuration and scripts

### ❌ Common Token Wastage Patterns

| Bad Practice | Consequence | Solution |
|-------------|-------------|----------|
| Unlimited conversation history | Growing memory = more tokens | Regular `/compress` or `/new` |
| AI polling for updates | Token burn on each check | Use scripts instead |
| Using GPT-4 for simple tasks | Overkill, high cost | Use appropriate model tier |
| Never compressing memory | Linear token cost growth | Establish compression habit |
| Continuing failed tasks | Wasted tokens | Use `/stop` immediately |

## Token Cost Formula

```
Total Cost = Context Consumption + Task Consumption

Optimization Formula:
New Cost = (Original Context × 30%) + (Task Cost × 20%)
         = Original Cost × (0.3 + 0.2)
         = Original Cost × 0.5 or lower
```

Combining all three techniques achieves **95%+ cost reduction**.

## Key Principle

> 💡 **Remember**: High costs don't come from AI itself, but from making it do tasks it shouldn't do and remember information it shouldn't store.
>
> Assign the right tasks to the right tools, and AI becomes truly cost-effective.
