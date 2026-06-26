# Troubleshooting

## Contents

- [Handling Zero Results](#handling-zero-results)
- [Handling Anomalous Results](#handling-anomalous-results)
- [Decision Tree: Ask vs. Investigate](#decision-tree-ask-vs-investigate)
- [Common Investigation Steps](#common-investigation-steps)
- [Red Flags: When to Stop and Ask](#red-flags-when-to-stop-and-ask)

## Handling Zero Results

When queries return no data, follow this diagnostic workflow:

1. **Validate Timeframe**
   - Check if timeframe is appropriate for the data type
   - RUM data may have delay (1-2 minutes for recent events)
   - Verify timeframe syntax: `-1h to now()` or similar
   - Try expanding timeframe: `now()-24h` for initial exploration

2. **Verify frontend Configuration**
   - Confirm frontend is instrumented and sending RUM data
   - Check `frontend.name` filter is correct
   - Test without frontend filter to see if any RUM data exists
   - Verify frontend name matches the environment

3. **Check Data Availability**
   - Run basic query: `fetch user.events | limit 1`
   - If no events exist, RUM may not be configured
   - Check if timeframe predates frontend deployment
   - Verify user has access to the environment

4. **Review Query Syntax**
   - Validate filters aren't too restrictive
   - Check for typos in field names or metric names
   - Test query incrementally: start simple, add filters gradually
   - Verify characteristics filters match event types

**When to Ask User for Clarification:**
- No RUM data exists in environment → "Is RUM configured for this frontend?"
- Timeframe unclear → "What time period should I analyze?"
- Expected data missing → "Has this frontend sent data recently?"

## Handling Anomalous Results

When query results seem unexpected or suspicious:

**Unexpected High Values:**
- **Metric spikes**: Verify interval aggregation (avg vs. max vs. sum)
- **Session counts**: Check for bot traffic or synthetic monitoring
- **Error rates**: Confirm error definition matches expectations
- **Performance degradation**: Look for deployment or infrastructure changes

**Unexpected Low Values:**
- **Missing sessions**: Verify `dt.rum.user_type` filter isn't excluding real users
- **Low request counts**: Check if frontend filter is too narrow
- **Few errors**: Confirm error characteristics filter is correct
- **Missing mobile data**: Verify platform-specific fields exist

**Inconsistent Data:**
- **Metrics vs. Events mismatch**: Different aggregation methods are expected
- **Geographic anomalies**: Check timezone assumptions
- **Device distribution skew**: May reflect actual user base
- **Version mismatches**: Verify app version filtering logic

## Decision Tree: Ask vs. Investigate

```
Query returns unexpected results
│
├─ Is this a zero-result scenario?
│  ├─ YES → Follow "Handling Zero Results" workflow
│  └─ NO → Continue
│
├─ Can I validate the result independently?
│  ├─ YES → Run validation query
│  │        ├─ Validation confirms result → Report findings
│  │        └─ Validation contradicts → Investigate further
│  └─ NO → Continue
│
├─ Is the anomaly clearly explained by data?
│  ├─ YES → Report with explanation
│  └─ NO → Continue
│
├─ Do I need domain knowledge to interpret?
│  ├─ YES → Ask user for context
│  │        Example: "The error rate is 15%. Is this expected for your frontend?"
│  └─ NO → Continue
│
└─ Is the issue ambiguous or requires clarification?
   ├─ YES → Ask specific question with data context
   │        Example: "I see two frontends named 'web-app'. Which frontend name should I use?"
   └─ NO → Investigate and report findings with caveats
```

## Common Investigation Steps

**For Performance Issues:**
1. Compare to baseline: Query same metric for previous week
2. Segment by dimension: Break down by device, browser, geography
3. Check for outliers: Use percentiles (p50, p95, p99) vs. averages
4. Correlate with deployments: Filter by app version or time windows

**For Data Availability Issues:**
1. Start broad: Query all RUM data without filters
2. Add filters incrementally: Isolate which filter eliminates data
3. Check related metrics: If events missing, try timeseries
4. Validate entity relationships: Confirm frontend-to-service links

**For Unexpected Patterns:**
1. Expand timeframe: Look for historical context
2. Cross-reference data sources: Compare events and metrics
3. Check sampling: Verify no sampling is affecting results
4. Consider external factors: Holidays, outages, traffic changes

## Red Flags: When to Stop and Ask

**Always ask the user when:**
- No RUM data exists anywhere in the environment
- Multiple frontends match the user's description
- Results contradict user's stated expectations explicitly
- Data suggests monitoring is misconfigured
- Query requires business context (e.g., "acceptable error rate")
- Timeframe is ambiguous and affects interpretation significantly

**Example clarifying questions:**
- "I found two frontends named 'checkout'. Which one: `checkout-web` or `checkout-mobile`?"
- "The query returns 0 results for the past hour. Should I expand the timeframe, or do you expect real-time data?"
- "The average LCP is 8 seconds, which exceeds the 4-second threshold. Is this frontend known to have performance issues?"
- "I see only synthetic traffic. Should I include `dt.rum.user_type=='REAL_USER'` to focus on real users?"
