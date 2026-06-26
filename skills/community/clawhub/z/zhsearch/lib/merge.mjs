export function mergeResults(sourceResults) {
  const all = [];
  const seen = new Set();
  for (const [source, results] of Object.entries(sourceResults)) {
    if (!Array.isArray(results)) continue;
    for (const r of results) {
      const key = r.title?.trim().toLowerCase();
      if (key && seen.has(key)) continue;
      if (key) seen.add(key);
      all.push({ ...r, source: r.source || source });
    }
  }
  return all;
}

export function formatForAgent(results, query) {
  if (!results || results.length === 0) {
    return JSON.stringify({ query, total: 0, results: [], message: "No results found." });
  }

  const grouped = {};
  for (const r of results) {
    const src = r.source || "unknown";
    if (!grouped[src]) grouped[src] = [];
    grouped[src].push({
      title: r.title?.trim(),
      snippet: r.snippet ? r.snippet.replace(/\s+/g, " ").trim().slice(0, 500) : "",
      url: r.url,
      ...(r.account ? { account: r.account } : {}),
      ...(r.date ? { date: r.date } : {}),
    });
  }

  return JSON.stringify(
    {
      query,
      total: results.length,
      sources: Object.keys(grouped),
      results: grouped,
    },
    null,
    2,
  );
}
