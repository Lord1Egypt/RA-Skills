/**
 * Self-Improving Robotics Hook for OpenClaw
 *
 * Injects a robotics-specific reminder to evaluate autonomy learnings during agent bootstrap.
 * Fires on agent:bootstrap event before workspace files are injected.
 */

const REMINDER_CONTENT = `
## Robotics Self-Improvement Reminder

After completing robotics tasks, evaluate if any learnings should be captured:

**Log robotics issues when:**
- Robot fails to localize in dynamic environment → \`.learnings/ROBOTICS_ISSUES.md\`
- Planner fails in narrow passage or obstacle-rich scene → \`.learnings/ROBOTICS_ISSUES.md\`
- Oscillatory control behavior appears (unstable PID tuning) → \`.learnings/ROBOTICS_ISSUES.md\`
- Sensor desync appears (camera-lidar-imu timestamp mismatch) → \`.learnings/ROBOTICS_ISSUES.md\`
- Hardware driver drops packets, CAN timeout, or serial disconnect occurs → \`.learnings/ROBOTICS_ISSUES.md\`
- Safety stop or emergency brake triggers unexpectedly → \`.learnings/ROBOTICS_ISSUES.md\`

**Log learnings when:**
- Localization drift pattern identified → \`.learnings/LEARNINGS.md\` (localization_drift)
- Planner weakness identified → \`.learnings/LEARNINGS.md\` (planning_failure)
- Control instability pattern identified → \`.learnings/LEARNINGS.md\` (control_instability)
- Sensor fusion alignment issue identified → \`.learnings/LEARNINGS.md\` (sensor_fusion_error)
- Simulation succeeds but real robot fails → \`.learnings/LEARNINGS.md\` (sim_to_real_gap)
- Thermal throttling, battery sag, or brownout observed → \`.learnings/LEARNINGS.md\` (power_thermal_constraint)

**Log feature requests when:**
- New robotics observability, safety, calibration, or autonomy tooling capability is needed → \`.learnings/FEATURE_REQUESTS.md\`

**Promote when pattern is proven:**
- Robotics behavior norms → \`SOUL.md\`
- Multi-agent autonomy workflows → \`AGENTS.md\`
- Tooling and runtime integration guidance → \`TOOLS.md\`
- Safety checklists and operating constraints → safety checklist docs
- Calibration and synchronization repeatables → calibration playbooks
- Stable tuning workflows → control/planning tuning runbooks
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
      path: 'ROBOTICS_SELF_IMPROVEMENT_REMINDER.md',
      content: REMINDER_CONTENT,
      virtual: true,
    });
  }
};

module.exports = handler;
module.exports.default = handler;
