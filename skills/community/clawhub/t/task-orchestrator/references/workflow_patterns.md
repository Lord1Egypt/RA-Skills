# Workflow Patterns

## Common Patterns

### 1. Sequential Pattern
Applicable when: Tasks have clear dependency relationships
```
T1 → T2 → T3 → T4
```
Example: Data scraping → Data analysis → Chart generation → Report writing

### 2. Parallel Pattern
Applicable when: Tasks are independent of each other
```
T1 ─┐
T2 ─┼→ Merge Results
T3 ─┘
```
Example: Simultaneously writing documentation, creating posters, developing demos

### 3. Fork-Join Pattern
Applicable when: Some tasks can run in parallel but need to be merged afterwards
```
    → T2 ┐
T1 → T3 ─→ T5
    → T4 ┘
```
Example: Research competitors → Research features/pricing/reviews separately → Merge into analysis report

### 4. Conditional Pattern
Applicable when: The next step is determined by results
```
       ┌ Yes → T2
T1 → Decision
       └ No → T3
```
Example: Check data quality → (Qualified) Analyze / (Unqualified) Re-collect

## Best Practices

1. **Identify Dependencies**: Clarify prerequisite relationships between tasks
2. **Maximize Parallelism**: Execute independent tasks in parallel
3. **Set Checkpoints**: Verify intermediate results at key milestones
4. **Reserve Buffer Time**: Reserve 20% time buffer for complex tasks