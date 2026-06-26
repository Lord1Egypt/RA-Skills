#!/usr/bin/env node

const fs = require("fs/promises")
const path = require("path")
const os = require("os")

const max = 5 * 1024 * 1024
const def = 30
const cap = 120

const fail = (msg) => {
  console.error(msg)
  process.exit(1)
}

const args = process.argv.slice(2)
const take = (name, alt) => {
  const i = args.findIndex((x) => x === name || x === alt)
  if (i < 0) return
  return args[i + 1]
}

const url0 = take("--url", "-u")
if (!url0) fail('Missing --url "https://example.com"')

const format = take("--format", "-f") || "markdown"
if (!["markdown", "text", "html"].includes(format)) {
  fail('Invalid --format. Use: markdown, text, html')
}

const out = take("--output", "-o")
const secs = Number(take("--timeout", "-t") || def)
if (!Number.isFinite(secs) || secs <= 0) {
  fail("Invalid --timeout. Use a positive number of seconds")
}

const timeout = Math.min(secs, cap) * 1000
const make = (kind) => {
  if (kind === "markdown") {
    return "text/markdown;q=1.0, text/x-markdown;q=0.9, text/plain;q=0.8, text/html;q=0.7, */*;q=0.1"
  }
  if (kind === "text") {
    return "text/plain;q=1.0, text/markdown;q=0.9, text/html;q=0.8, */*;q=0.1"
  }
  return "text/html;q=1.0, application/xhtml+xml;q=0.9, text/plain;q=0.8, text/markdown;q=0.7, */*;q=0.1"
}

const hdrs = (agent) => ({
  "User-Agent": agent,
  Accept: make(format),
  "Accept-Language": "en-US,en;q=0.9",
})

const esc = (txt) =>
  txt
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")

const dec = (txt) =>
  txt
    .replaceAll("&nbsp;", " ")
    .replaceAll("&amp;", "&")
    .replaceAll("&lt;", "<")
    .replaceAll("&gt;", ">")
    .replaceAll("&quot;", '"')
    .replaceAll("&#39;", "'")

const trim = (txt) => txt.replace(/\r/g, "").replace(/\n{3,}/g, "\n\n").trim()

async function textify(html) {
  return trim(
    dec(
      html
        .replace(/<script[\s\S]*?<\/script>/gi, "")
        .replace(/<style[\s\S]*?<\/style>/gi, "")
        .replace(/<noscript[\s\S]*?<\/noscript>/gi, "")
        .replace(/<(iframe|object|embed)[\s\S]*?<\/\1>/gi, "")
        .replace(/<(br|hr)[^>]*>/gi, "\n")
        .replace(/<(p|div|section|article|main|header|footer|aside|nav|ul|ol|li|table|tr|pre)[^>]*>/gi, "\n")
        .replace(/<[^>]+>/g, "")
    ),
  )
}

function mark(html) {
  return trim(
    dec(
      html
        .replace(/<script[\s\S]*?<\/script>/gi, "")
        .replace(/<style[\s\S]*?<\/style>/gi, "")
        .replace(/<(meta|link)[^>]*>/gi, "")
        .replace(/<pre[^>]*>([\s\S]*?)<\/pre>/gi, (_, x) => `\n\n\
\`\`\`\n${dec(x.replace(/<[^>]+>/g, ""))}\n\`\`\`\n\n`)
        .replace(/<code[^>]*>([\s\S]*?)<\/code>/gi, (_, x) => `\`${dec(x.replace(/<[^>]+>/g, ""))}\``)
        .replace(/<h1[^>]*>([\s\S]*?)<\/h1>/gi, (_, x) => `\n\n# ${dec(x.replace(/<[^>]+>/g, " "))}\n\n`)
        .replace(/<h2[^>]*>([\s\S]*?)<\/h2>/gi, (_, x) => `\n\n## ${dec(x.replace(/<[^>]+>/g, " "))}\n\n`)
        .replace(/<h3[^>]*>([\s\S]*?)<\/h3>/gi, (_, x) => `\n\n### ${dec(x.replace(/<[^>]+>/g, " "))}\n\n`)
        .replace(/<h[4-6][^>]*>([\s\S]*?)<\/h[4-6]>/gi, (_, x) => `\n\n#### ${dec(x.replace(/<[^>]+>/g, " "))}\n\n`)
        .replace(/<a [^>]*href=["']([^"']+)["'][^>]*>([\s\S]*?)<\/a>/gi, (_, href, x) => {
          const txt = dec(x.replace(/<[^>]+>/g, " ")).trim()
          return txt ? `[${txt}](${href})` : href
        })
        .replace(/<li[^>]*>([\s\S]*?)<\/li>/gi, (_, x) => `\n- ${dec(x.replace(/<[^>]+>/g, " ")).trim()}`)
        .replace(/<(p|div|section|article|main|header|footer|aside|nav|ul|ol|table|tr)[^>]*>/gi, "\n\n")
        .replace(/<(br|hr)[^>]*>/gi, "\n")
        .replace(/<[^>]+>/g, "")
    ),
  )
}

const norm = (url) => {
  if (url.startsWith("https://")) return url
  if (url.startsWith("http://")) return `https://${url.slice(7)}`
  fail("URL must start with http:// or https://")
}

async function grab(url) {
  const sig = AbortSignal.timeout(timeout)
  const init = {
    signal: sig,
    headers: hdrs("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"),
  }
  const first = await fetch(url, init).catch((err) => ({ err }))

  if (first && "err" in first) throw first.err

  if (first.status === 403 && first.headers.get("cf-mitigated") === "challenge") {
    return fetch(url, { signal: sig, headers: hdrs("opencode") })
  }

  return first
}

async function main() {
  const src = norm(url0)
  const tried = []
  let res
  let url = src

  for (const next of [src, url0]) {
    if (tried.includes(next)) continue
    tried.push(next)
    try {
      res = await grab(next)
      url = next
      break
    } catch (err) {
      if (next === url0) {
        fail(err instanceof Error ? err.message : String(err))
      }
    }
  }

  if (!res) fail("Request failed")
  if (!res.ok) fail(`Request failed with status code: ${res.status}`)

  const len = res.headers.get("content-length")
  if (len && Number(len) > max) {
    fail("Response too large (exceeds 5MB limit)")
  }

  const buf = await res.arrayBuffer()
  if (buf.byteLength > max) {
    fail("Response too large (exceeds 5MB limit)")
  }

  const type = res.headers.get("content-type") || "application/octet-stream"
  const mime = type.split(";")[0]?.trim().toLowerCase() || "application/octet-stream"
  const title = `${url} (${type})`
  const img = mime.startsWith("image/") && mime !== "image/svg+xml" && mime !== "image/vnd.fastbidsheet"

  if (img) {
    const ext = mime.split("/")[1] || "bin"
    const file = out || path.join(os.tmpdir(), `opencode-web-fetch-${Date.now()}.${ext}`)
    await fs.writeFile(file, Buffer.from(buf))
    process.stdout.write(
      [
        "<web_fetch>",
        `<title>${esc(title)}</title>`,
        `<url>${esc(url)}</url>`,
        `<mime>${esc(mime)}</mime>`,
        `<image>${esc(file)}</image>`,
        "</web_fetch>",
        "",
      ].join("\n"),
    )
    process.exit(0)
  }

  const body = new TextDecoder().decode(buf)
  const html = type.includes("text/html") || mime === "application/xhtml+xml"
  const content = format === "html" ? body : html ? (format === "text" ? await textify(body) : mark(body)) : body

  process.stdout.write(
    [
      "<web_fetch>",
      `<title>${esc(title)}</title>`,
      `<url>${esc(url)}</url>`,
      `<mime>${esc(mime)}</mime>`,
      `<format>${esc(format)}</format>`,
      "<content>",
      content,
      "</content>",
      "</web_fetch>",
      "",
    ].join("\n"),
  )
}

main().catch((err) => fail(err instanceof Error ? err.message : String(err)))
