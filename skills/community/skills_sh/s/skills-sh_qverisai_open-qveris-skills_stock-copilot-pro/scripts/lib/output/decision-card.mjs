function scoreToLight(score) {
  if (!Number.isFinite(score)) return { emoji: "⚪", label: "未评级" };
  if (score >= 75) return { emoji: "🟢", label: "偏积极" };
  if (score >= 55) return { emoji: "🟡", label: "中性" };
  return { emoji: "🔴", label: "偏谨慎" };
}

export function buildDecisionCard(report) {
  const score = report?.analysis?.scorecard?.composite;
  const grade = report?.analysis?.scorecard?.grade || "N/A";
  const signal = report?.analysis?.recommendation?.signal || "N/A";
  const risk = report?.analysis?.chaseRisk?.risk || "unknown";
  const light = scoreToLight(score);

  return {
    symbol: report?.symbol || "N/A",
    market: report?.market || "GLOBAL",
    light: light.label,
    emoji: light.emoji,
    score: Number.isFinite(score) ? score : null,
    grade,
    signal,
    risk,
    asText: `${light.emoji} ${report?.symbol || "N/A"} | ${grade} | ${signal} | 风险:${risk}`,
  };
}
