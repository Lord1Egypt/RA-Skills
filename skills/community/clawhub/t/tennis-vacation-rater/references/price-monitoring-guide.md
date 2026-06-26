# Price Monitoring Guide

## When to Suggest

Suggest price monitoring when:
- User has not specified travel dates
- Travel date is >15 days away
- User mentions "waiting for good price" or similar

## How to Suggest

After report generation, add this section at the end:

```markdown
---

###  Price Monitoring

Since your travel date is flexible / more than 2 weeks away, 
would you like me to monitor flight prices for you?

**What I'll monitor**:
- [Origin]  [Destination] round-trip flights
- Price drops below your target
- Best booking windows

**How it works**:
- Check prices daily at 9 AM
- Notify you immediately when price drops
- Provide booking recommendation

Interested? Just tell me:
1. Your budget limit (e.g., 2,000)
2. Preferred travel months
```

## User Response Handling

### If User Agrees

1. **Collect info** (if not already known):
   - Departure city
   - Budget limit
   - Preferred months

2. **Perform immediate price check** (no automatic monitoring):
   - Use WebSearch or flyai CLI to check current prices
   - Compare with user's budget
   - Provide booking recommendation based on current data

3. **Confirm to user**:

```markdown
 **Price check completed!**

**Current Status**:
- Route: [Origin]  [Destination]
- Current Price: [price]
- Your Budget: [budget]
- Recommendation: [Book now / Wait]

**Note**: This is a one-time check. For continuous monitoring, please check periodically or use dedicated price tracking tools.
```

### If User Declines

Simply acknowledge and end the conversation:

```markdown
No problem! If you change your mind later, just let me know. 
Have a great trip! 
```

## Price Check Process

### One-Time Check

When user agrees to price monitoring suggestion:

1. **Search current prices** using WebSearch or flyai CLI
2. **Compare with target budget**
3. **Provide recommendation**:
   - If price < budget: Recommend booking
   - If price >= budget: Suggest waiting or adjusting budget
4. **No automatic follow-up** - this is a one-time check only

### Response Template

```markdown
 **Price Check: [Origin]  [Destination]**

Current market status:

| Detail | Info |
|--------|------|
| Current Price | [price] |
| Your Budget | [budget] |
| Status | [Within budget / Over budget] |

**Recommendation**: [Book now / Wait for better price / Adjust budget]

Want me to help you with anything else?
```

## Best Practices

1. **Respect user preference**: Don't push if user declines
2. **Clear expectations**: Explain exactly what will be monitored
3. **Easy opt-out**: User can cancel monitoring anytime
4. **Actionable alerts**: Include specific recommendation, not just price
5. **Privacy**: Don't store user data longer than necessary

## No Automatic Monitoring

This skill does **NOT** create automatic cron jobs or persistent monitoring tasks. All price checks are performed on-demand during the current conversation session only.
