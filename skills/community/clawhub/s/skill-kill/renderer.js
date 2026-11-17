const TRUST_ORDER = { 高: 4, 中: 3, 低: 2, 未知: 1 };
const RISK_ORDER = { 低: 1, 中: 2, 高: 3, 未知: 4 };
const TRUST_LEVELS = new Set(Object.keys(TRUST_ORDER));
const RISK_LEVELS = new Set(Object.keys(RISK_ORDER));
const RECOMMENDATIONS = new Set(["推荐", "谨慎", "不推荐"]);

function normalizeCandidate(item) {
  const value = item || {};
  const trustLevel = TRUST_LEVELS.has(value.trustLevel) ? value.trustLevel : "未知";
  const riskLevel = RISK_LEVELS.has(value.riskLevel) ? value.riskLevel : "未知";
  const recommendation = RECOMMENDATIONS.has(value.recommendation) ? value.recommendation : "谨慎";
  return {
    name: value.name || "未知",
    description: value.description || "未知",
    matchScore: Number.isFinite(Number(value.matchScore)) ? Math.max(0, Math.min(100, Number(value.matchScore))) : 0,
    trustLevel,
    riskLevel,
    recommendation,
    sourceType: value.sourceType || "未知来源",
    sourceUrl: value.sourceUrl || "未知",
    repositoryUrl: value.repositoryUrl || "未知",
    version: value.version || "未知",
    lastUpdated: value.lastUpdated || "未知",
    permissions: Array.isArray(value.permissions) && value.permissions.length ? value.permissions : ["未知"],
    evidence: Array.isArray(value.evidence) && value.evidence.length ? value.evidence : ["未知"],
    limitations: Array.isArray(value.limitations) && value.limitations.length ? value.limitations : ["未知"],
    installCommand: value.installCommand || "需按来源页手动安装"
  };
}

function prepareCandidates(candidates) {
  return (Array.isArray(candidates) ? candidates : [])
    .map(normalizeCandidate)
    .sort((a, b) => b.matchScore - a.matchScore || TRUST_ORDER[b.trustLevel] - TRUST_ORDER[a.trustLevel] || RISK_ORDER[a.riskLevel] - RISK_ORDER[b.riskLevel])
    .slice(0, 5);
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, char => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[char]));
}

function renderCandidates(candidates, mode = "markdown") {
  const items = prepareCandidates(candidates);
  const headers = ["候选 Skill", "功能简介", "匹配度", "信任度", "安全风险", "来源", "关键权限/行为", "推荐结论", "安装命令"];
  if (mode === "html") {
    const head = `<table><thead><tr>${headers.map(header => `<th>${escapeHtml(header)}</th>`).join("")}</tr></thead><tbody>`;
    const rows = items.map(item => `<tr><td>${escapeHtml(item.name)}</td><td>${escapeHtml(item.description)}</td><td>${item.matchScore}</td><td>${escapeHtml(item.trustLevel)}</td><td>${escapeHtml(item.riskLevel)}</td><td><a href="${escapeHtml(item.sourceUrl)}">${escapeHtml(item.sourceUrl)}</a></td><td>${item.permissions.map(escapeHtml).join("、")}</td><td>${escapeHtml(item.recommendation)}</td><td><code>${escapeHtml(item.installCommand)}</code></td></tr>`).join("");
    return `${head}${rows}</tbody></table>`;
  }
  const header = `| ${headers.join(" | ")} |\n|${headers.map((_, index) => index === 2 ? "---:" : "---").join("|")}|`;
  const rows = items.map(item => `| ${item.name} | ${item.description} | ${item.matchScore} | ${item.trustLevel} | ${item.riskLevel} | [来源](${item.sourceUrl}) | ${item.permissions.join("、")} | ${item.recommendation} | \`${item.installCommand}\` |`);
  return [header, ...rows].join("\n");
}

if (typeof module !== "undefined") {
  module.exports = { normalizeCandidate, prepareCandidates, renderCandidates };
}
