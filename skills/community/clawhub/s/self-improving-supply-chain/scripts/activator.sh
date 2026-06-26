#!/bin/bash
# Supply Chain Self-Improvement Activator Hook
# Triggers on UserPromptSubmit to remind about supply chain learning capture
# Keep output minimal (~50-100 tokens) to minimize overhead

set -e

cat << 'EOF'
<supply-chain-self-improvement-reminder>
After completing this supply chain task, evaluate if extractable knowledge emerged:
- Stockout or backorder event? → SUPPLY_CHAIN_ISSUES.md [SCM-YYYYMMDD-XXX]
- Delivery delay or SLA miss? → SUPPLY_CHAIN_ISSUES.md (logistics_delay)
- Supplier lead time increase or failure? → LEARNINGS.md (supplier_risk)
- Quality rejection or defect spike? → SUPPLY_CHAIN_ISSUES.md (quality_deviation)
- Forecast miss >15% MAPE? → LEARNINGS.md (forecast_error)
- Demand spike or channel shift? → LEARNINGS.md (demand_signal_shift)
- Warehouse capacity >90%? → SUPPLY_CHAIN_ISSUES.md (inventory_mismatch)

If recurring pattern (3+ occurrences): promote to scorecard, policy, or playbook.
If broadly applicable: consider skill extraction.
</supply-chain-self-improvement-reminder>
EOF
