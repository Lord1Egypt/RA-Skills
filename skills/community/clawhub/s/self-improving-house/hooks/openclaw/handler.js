/**
 * Self-Improving Domotics Hook for OpenClaw
 *
 * Injects a reminder to capture domotics learnings at bootstrap.
 * Reminder-only behavior; no direct actuator actions.
 */

const REMINDER_CONTENT = `
## Domotics Self-Improvement Reminder

After completing domotics work, evaluate if learnings should be captured:

**Log issues (\`.learnings/DOMOTICS_ISSUES.md\`) when:**
- Automation loop or rule conflict occurred (\`automation_conflict\`)
- Device became unreachable/offline (\`device_unreachable\`)
- Integration API/schema/auth changed and broke flow (\`integration_break\`)
- Schedule was missed or highly delayed (\`latency_jitter\`)

**Log learnings (\`.learnings/LEARNINGS.md\`) when:**
- Sensor values drift or go stale (\`sensor_drift\`)
- Occupancy inference mismatches reality (\`occupancy_mismatch\`)
- Energy pattern can be optimized safely (\`energy_optimization\`)
- Safety guardrails are missing (\`safety_rule_gap\`)

**Log feature requests (\`.learnings/FEATURE_REQUESTS.md\`) when:**
- New observability, reliability, or safety capability is needed

**Safety default:**
- Documentation/reminder workflow only
- Require human confirmation for locks, alarms, gas/water shutoff, heaters

Promote recurring patterns (3+) to playbooks, compatibility matrix, rule library, or safety automations.
`.trim();

const handler = async (event) => {
  if (!event || typeof event !== 'object') {
    return;
  }

  if (event.type !== 'agent' || event.action !== 'bootstrap') {
    return;
  }

  if (!event.context || typeof event.context !== 'object') {
    return;
  }

  if (Array.isArray(event.context.bootstrapFiles)) {
    event.context.bootstrapFiles.push({
      path: 'DOMOTICS_SELF_IMPROVEMENT_REMINDER.md',
      content: REMINDER_CONTENT,
      virtual: true,
    });
  }
};

module.exports = handler;
module.exports.default = handler;
