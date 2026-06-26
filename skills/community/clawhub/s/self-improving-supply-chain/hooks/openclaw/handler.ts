/**
 * Self-Improving Supply Chain Hook for OpenClaw
 *
 * Injects a supply chain-specific reminder to evaluate learnings during agent bootstrap.
 * Fires on agent:bootstrap event before workspace files are injected.
 */

import type { HookHandler } from 'openclaw/hooks';

const REMINDER_CONTENT = `## Supply Chain Self-Improvement Reminder

After completing supply chain tasks, evaluate if any learnings should be captured:

**Log supply chain issues when:**
- Stockout or backorder event detected → \`.learnings/SUPPLY_CHAIN_ISSUES.md\` (inventory_mismatch)
- Delivery SLA missed or shipment delayed → \`.learnings/SUPPLY_CHAIN_ISSUES.md\` (logistics_delay)
- Quality rejection or defect rate spike → \`.learnings/SUPPLY_CHAIN_ISSUES.md\` (quality_deviation)
- Warehouse at or above 90% capacity → \`.learnings/SUPPLY_CHAIN_ISSUES.md\` (inventory_mismatch)

**Log learnings when:**
- Forecast miss exceeds 15% MAPE → \`.learnings/LEARNINGS.md\` (forecast_error)
- Supplier lead time increased or supplier failed → \`.learnings/LEARNINGS.md\` (supplier_risk)
- Unexpected demand spike or channel shift → \`.learnings/LEARNINGS.md\` (demand_signal_shift)
- Routing inefficiency or logistics optimization found → \`.learnings/LEARNINGS.md\` (logistics_delay)

**Log feature requests when:**
- Supply chain tool or automation needed → \`.learnings/FEATURE_REQUESTS.md\`

**Promote when pattern is proven (3+ occurrences):**
- Supplier patterns → supplier scorecards
- Inventory patterns → safety stock policies
- Routing patterns → routing playbooks
- Forecast patterns → demand planning models
- Quality patterns → quality acceptance criteria

Include impact metrics (units, cost, days). Specify area tag.`;

const handler: HookHandler = async (event) => {
  if (!event || typeof event !== 'object') {
    return;
  }

  if (event.type !== 'agent' || event.action !== 'bootstrap') {
    return;
  }

  if (!event.context || typeof event.context !== 'object') {
    return;
  }

  const sessionKey = event.sessionKey || '';
  if (sessionKey.includes(':subagent:')) {
    return;
  }

  if (Array.isArray(event.context.bootstrapFiles)) {
    event.context.bootstrapFiles.push({
      path: 'SUPPLY_CHAIN_SELF_IMPROVEMENT_REMINDER.md',
      content: REMINDER_CONTENT,
      virtual: true,
    });
  }
};

export default handler;
