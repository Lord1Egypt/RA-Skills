// Adapted from OpenClaw Command Center intel/pipeline/monetization modules.
// See THIRD_PARTY_NOTICES.md for source and MIT attribution.
const { splitTableRow, isTableSeparator } = require("./markdown-table");
const { redactExtensionText } = require("./redaction");
const L = (en, zh) => ({ en, "zh-CN": zh });
const clean = (v) => redactExtensionText(v ?? "").slice(0, 2048);
const table = (id, title, fields, rows) => ({
  id,
  type: "table",
  title,
  columns: fields.map(([key, en, zh]) => ({ key, label: L(en, zh) })),
  rows: rows
    .slice(0, 100)
    .map((row) =>
      Object.fromEntries(fields.map(([key]) => [key, clean(row[key])])),
    ),
});
const metrics = (entries) => ({
  id: "summary",
  type: "metrics",
  title: L("Summary", "摘要"),
  metrics: entries.map(([en, zh, value]) => ({ label: L(en, zh), value })),
});
function parseTables(content) {
  const lines = content.split("\n");
  const tables = [];
  let headers = null;
  let rows;
  for (let i = 0; i < lines.length; i++) {
    const cells = splitTableRow(lines[i]);
    if (!cells.length) {
      headers = null;
      continue;
    }
    if (!headers && isTableSeparator(lines[i + 1] || "", cells.length)) {
      headers = cells.map((c) => c.replace(/\*\*/g, "").trim().toLowerCase());
      rows = [];
      tables.push({ headers, rows });
      i++;
      continue;
    }
    if (headers && cells.some(Boolean))
      rows.push(Object.fromEntries(headers.map((h, j) => [h, cells[j] || ""])));
  }
  return tables;
}
function hasPositiveRevenue(value) {
  const match = value
    .replace(/\*\*/g, "")
    .trim()
    .match(
      /^(?:(?:[$€£]|USD|EUR|GBP|CZK|KČ)\s*)?([+-]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?)\s*(?:USD|EUR|GBP|CZK|KČ)?(?:\s*\/(?:mo|month|yr|year))?$/i,
    );
  return !!match && Number(match[1].replace(/,/g, "")) > 0;
}
function intel(files, now) {
  const rows = files.map((f) => {
    const age = Math.max(0, now - f.mtimeMs);
    const line = f.content
      .slice(0, 1024)
      .split("\n")
      .slice(0, 10)
      .find((l) => /(?:Agent|Zpracoval|Autor)(?:\*\*)?:/i.test(l));
    const agent = line
      ? line
          .replace(/^.*?(?:Agent|Zpracoval|Autor)(?:\*\*)?:\s*/i, "")
          .replace(/\*\*/g, "")
          .replace(/\s*[|(,].*$/, "")
          .trim()
      : "";
    return {
      name: f.name,
      agent,
      modified: new Date(f.mtimeMs).toISOString(),
      age_hours: Math.floor(age / 3600000),
      freshness: age < 21600000 ? "fresh" : age < 86400000 ? "aging" : "stale",
    };
  });
  return [
    metrics([
      ["Files", "文件", rows.length],
      ["Fresh", "新鲜", rows.filter((r) => r.freshness === "fresh").length],
      ["Aging", "较旧", rows.filter((r) => r.freshness === "aging").length],
      ["Stale", "过期", rows.filter((r) => r.freshness === "stale").length],
    ]),
    table(
      "files",
      L("Intel files", "情报文件"),
      [
        ["name", "File", "文件"],
        ["agent", "Agent", "智能体"],
        ["modified", "Modified", "修改时间"],
        ["age_hours", "Age (hours)", "时龄（小时）"],
      ],
      rows,
    ),
  ];
}
function pipeline(files) {
  const rows = [];
  for (const f of files.filter((f) => /PIPELINE|QUEUE/i.test(f.name))) {
    const parsed = parseTables(f.content).flatMap((t) => t.rows);
    const counts = Object.create(null);
    for (const row of parsed) {
      const status = (row.status || row.stav || row["email odesílání"] || "")
        .replace(/[*_]/g, "")
        .trim()
        .toUpperCase();
      if (status && status !== "-") counts[status] = (counts[status] || 0) + 1;
    }
    rows.push({
      name: f.name.replace(/\.md$/i, "").replace(/-/g, " "),
      items: parsed.length,
      statuses: Object.entries(counts)
        .map(([k, v]) => `${k}: ${v}`)
        .join(", "),
      modified: new Date(f.mtimeMs).toISOString(),
    });
  }
  return [
    table(
      "pipelines",
      L("Pipelines", "业务流程"),
      [
        ["name", "Pipeline", "流程"],
        ["items", "Items", "项目数"],
        ["statuses", "Statuses", "状态"],
        ["modified", "Modified", "修改时间"],
      ],
      rows,
    ),
  ];
}
function monetization(files) {
  const file = files.find((f) => f.name === "MONETIZATION-TRACKER.md");
  if (!file) return null;
  const rows = [];
  for (const t of parseTables(file.content)) {
    const nameKey = t.headers.find((h) =>
      ["firma", "company", "firm"].includes(h),
    );
    if (!nameKey) continue;
    for (const r of t.rows) {
      const name = (r[nameKey] || "").replace(/\*\*/g, "").trim();
      if (name && name !== "-")
        rows.push({
          name,
          revenue: r.revenue || "",
          milestone: r.milestone || "",
          blocker: r.blocker || "",
          priority: (r.priority || "")
            .replace(/\*\*/g, "")
            .trim()
            .toUpperCase(),
        });
    }
  }
  return [
    metrics([
      ["Organizations", "组织", rows.length],
      [
        "High priority",
        "高优先级",
        rows.filter((r) => r.priority === "HIGH").length,
      ],
      [
        "With revenue",
        "有收入",
        rows.filter((r) => hasPositiveRevenue(r.revenue)).length,
      ],
    ]),
    table(
      "organizations",
      L("Monetization", "变现"),
      [
        ["name", "Organization", "组织"],
        ["revenue", "Revenue", "收入"],
        ["milestone", "Milestone", "里程碑"],
        ["blocker", "Blocker", "阻碍"],
        ["priority", "Priority", "优先级"],
      ],
      rows,
    ),
  ];
}
module.exports = {
  intel,
  pipeline,
  monetization,
  parseTables,
  hasPositiveRevenue,
};
