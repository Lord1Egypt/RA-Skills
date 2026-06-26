# Skill Evaluation Rubric

Detailed scoring criteria for each evaluation dimension.

## Quality/Utility (35%)

### User Ratings (0-100)
- 90-100: 4.5+ stars, 1000+ downloads
- 70-89: 4.0+ stars, 100+ downloads
- 50-69: 3.5+ stars, any downloads
- 30-49: Below 3.5 stars
- 0-29: No ratings or mostly negative

### Functionality Match (0-100)
- 90-100: Perfect match for task requirements
- 70-89: Good match, minor gaps
- 50-69: Partial match, some workarounds needed
- 30-49: Poor match, significant gaps
- 0-29: Wrong tool for the job

### Documentation Quality (0-100)
- 90-100: Comprehensive docs with examples
- 70-89: Good docs, some examples
- 50-69: Basic docs, minimal examples
- 30-49: Poor documentation
- 0-29: No documentation

**Quality Score = (Ratings × 0.4) + (Match × 0.4) + (Docs × 0.2)**

## Token Cost (30%)

### Estimation Levels
- 90-100: < 1000 tokens expected
- 70-89: 1000-2000 tokens
- 50-69: 2000-4000 tokens
- 30-49: 4000-8000 tokens
- 0-29: > 8000 tokens

### Efficiency Factors
- Caching support (+10 points)
- Batch operations (+10 points)
- Minimal context requirements (+10 points)

**Token Score = Base Score + Efficiency Bonuses (max 100)**

## Security/Reliability (20%)

### Code Audit (0-100)
- 90-100: Clean code, no suspicious patterns
- 70-89: Minor issues, no security concerns
- 50-69: Some questionable practices
- 30-49: Concerning patterns detected
- 0-29: Security risks identified

### Permission Appropriateness (0-100)
- 90-100: Minimal permissions for functionality
- 70-89: Reasonable permissions
- 50-69: Slightly excessive permissions
- 30-49: Overly broad permissions
- 0-29: Dangerous permissions requested

### Maintenance Status (0-100)
- 90-100: Updated within last month
- 70-89: Updated within last 3 months
- 50-69: Updated within last 6 months
- 30-49: Updated within last year
- 0-29: No updates > 1 year

**Security Score = (Audit × 0.4) + (Permissions × 0.3) + (Maintenance × 0.3)**

## Speed (15%)

### Response Time
- 90-100: < 1 second
- 70-89: 1-3 seconds
- 50-69: 3-5 seconds
- 30-49: 5-10 seconds
- 0-29: > 10 seconds

### Efficiency
- Async operations (+10 points)
- Parallel processing (+10 points)
- Minimal API calls (+10 points)

**Speed Score = Base Score + Efficiency Bonuses (max 100)**

## Final Score Calculation

```
Final Score = (Quality × 0.35) + (Token × 0.30) + (Security × 0.20) + (Speed × 0.15)
```

## Minimum Thresholds

A skill must meet these minimums to be recommended:
- Security Score ≥ 50 (no security risks)
- Quality Score ≥ 40 (functional for the task)

Skills failing these thresholds are excluded regardless of final score.
