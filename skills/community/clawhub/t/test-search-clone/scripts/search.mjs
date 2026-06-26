#!/usr/bin/env node

const apiKey = (process.env.TAVILY_API_KEY ?? "").trim();
if (!apiKey) {
  console.error("Missing TAVILY_API_KEY");
  process.exit(1);
}

const query = process.argv[2] ?? "test";

const resp = await fetch("https://api.tavily.com/search", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ api_key: apiKey, query, max_results: 5, include_answer: true }),
});

if (!resp.ok) {
  const text = await resp.text().catch(() => "");
  throw new Error(`Failed (${resp.status}): ${text}`);
}

const data = await resp.json();
if (data.answer) console.log(data.answer);
