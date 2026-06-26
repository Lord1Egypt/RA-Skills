// Formatter utilities for Reivo skill output.
// Reserved for future use when public stats API is available.

function formatStatus(data) {
  const lines = [
    "Reivo Daily Report",
    `\u251c\u2500\u2500 Requests: ${data.requests}`,
    `\u251c\u2500\u2500 Total Cost: $${data.totalCost.toFixed(2)}`,
    `\u2514\u2500\u2500 Saved: $${data.savedToday.toFixed(2)} today`,
  ];
  return lines.join("\n");
}

function formatMonthly(data) {
  const lines = [
    `Reivo Monthly Report (${data.month})`,
    `\u251c\u2500\u2500 Requests: ${data.totalRequests}`,
    `\u251c\u2500\u2500 Total Cost: $${data.totalCost.toFixed(2)}`,
    `\u2514\u2500\u2500 Saved: $${data.saved.toFixed(2)} this month`,
  ];
  return lines.join("\n");
}

module.exports = { formatStatus, formatMonthly };
