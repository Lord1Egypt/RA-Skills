function normalizeSeverity(severity) {
  return severity || "all";
}

function run(input) {
  const region = input.region || "unknown";
  const severity = normalizeSeverity(input.severity);
  const alerts = [];

  return {
    alert_count: alerts.length,
    summary: alerts.length
      ? `${alerts.length} ${severity} alerts for ${region}`
      : `No active ${severity} alerts for ${region}`
  };
}

module.exports = { run, normalizeSeverity };
