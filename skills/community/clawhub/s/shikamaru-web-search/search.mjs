#!/usr/bin/env node

const fail = (msg) => {
  console.error(msg)
  process.exit(1)
}

const args = process.argv.slice(2)
const take = (name) => {
  const i = args.indexOf(name)
  if (i < 0) return
  return args[i + 1]
}

const query = take("--query") ?? take("-q")
if (!query) fail('Missing --query "..."')

const num = take("--numResults")
const type = take("--type")
const live = take("--livecrawl")
const max = take("--contextMaxCharacters")

if (type && !["auto", "fast", "deep"].includes(type)) {
  fail('Invalid --type. Use: auto, fast, deep')
}

if (live && !["fallback", "preferred"].includes(live)) {
  fail('Invalid --livecrawl. Use: fallback, preferred')
}

if (num && (!Number.isInteger(Number(num)) || Number(num) <= 0)) {
  fail('Invalid --numResults. Use a positive integer')
}

if (max && (!Number.isInteger(Number(max)) || Number(max) <= 0)) {
  fail('Invalid --contextMaxCharacters. Use a positive integer')
}

const body = {
  jsonrpc: "2.0",
  id: 1,
  method: "tools/call",
  params: {
    name: "web_search_exa",
    arguments: {
      query,
      type: type || "auto",
      numResults: num ? Number(num) : 8,
      livecrawl: live || "fallback",
      ...(max ? { contextMaxCharacters: Number(max) } : {}),
    },
  },
}

const res = await fetch("https://mcp.exa.ai/mcp", {
  method: "POST",
  headers: {
    accept: "application/json, text/event-stream",
    "content-type": "application/json",
  },
  body: JSON.stringify(body),
  signal: AbortSignal.timeout(25000),
}).catch((err) => fail(err instanceof Error ? err.message : String(err)))

if (!res.ok) fail(`Search error (${res.status}): ${await res.text()}`)

const text = await res.text()
const hit = text
  .split("\n")
  .filter((line) => line.startsWith("data: "))
  .map((line) => JSON.parse(line.slice(6)))
  .find((item) => item?.result?.content?.[0]?.text)

const out = hit?.result?.content?.[0]?.text
if (!out) fail("No search results found. Try a different query.")

process.stdout.write(`${out}\n`)
