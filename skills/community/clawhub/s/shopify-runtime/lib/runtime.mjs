import fs from "node:fs/promises"
import path from "node:path"
import process from "node:process"
import vm from "node:vm"
import { shopifyProvider } from "./shopify-provider.mjs"

const DEFAULT_CACHE_TTL_MS = 60 * 60 * 1000
const DEFAULT_DOCS_CACHE = new Map()

const DEFAULT_DOCS_DEPENDENCIES = {
  fetch: globalThis.fetch,
  now: () => Date.now(),
  cacheTtlMs: DEFAULT_CACHE_TTL_MS,
  cacheStore: DEFAULT_DOCS_CACHE,
}

const FORBIDDEN_PATTERNS = [
  { pattern: /\bimport\s*\(/u, message: "Dynamic import is not available." },
  { pattern: /\bimport\s+/u, message: "Module imports are not available." },
  { pattern: /\brequire\s*\(/u, message: "require is not available." },
  { pattern: /\bprocess\b/u, message: "process is not available." },
  { pattern: /\bglobalThis\b/u, message: "globalThis is not available." },
  { pattern: /\bFunction\b/u, message: "Function constructors are not available." },
  { pattern: /\beval\s*\(/u, message: "eval is not available." },
  { pattern: /\bconstructor\b/u, message: "constructor access is not available." },
  {
    pattern: /\bfetch\s*\(/u,
    message: "Use provider.request or provider.graphql instead of fetch.",
  },
  { pattern: /\bchild_process\b/u, message: "child_process is not available." },
  { pattern: /\bworker_threads\b/u, message: "worker_threads is not available." },
  { pattern: /\bfs\b/u, message: "fs is not available." },
  { pattern: /\bvm\b/u, message: "vm is not available." },
]

const readEnvString = key => {
  const value = process.env[key]
  return typeof value === "string" && value.trim().length > 0 ? value.trim() : undefined
}

const toError = value =>
  value instanceof Error ? value : new Error(typeof value === "string" ? value : "Unknown error")

const decodeEntities = value =>
  value
    .replace(/&nbsp;/gi, " ")
    .replace(/&amp;/gi, "&")
    .replace(/&lt;/gi, "<")
    .replace(/&gt;/gi, ">")
    .replace(/&quot;/gi, '"')
    .replace(/&#39;/gi, "'")

const collapseWhitespace = value => value.replace(/\s+/g, " ").trim()

const stripHtml = value =>
  decodeEntities(
    value
      .replace(/<script[\s\S]*?<\/script>/gi, " ")
      .replace(/<style[\s\S]*?<\/style>/gi, " ")
      .replace(/<\/(p|div|section|article|li|ul|ol|h1|h2|h3|h4|h5|h6|br)>/gi, "\n")
      .replace(/<[^>]+>/g, " "),
  )
    .replace(/\r/g, "")
    .replace(/[ \t]+\n/g, "\n")
    .replace(/\n[ \t]+/g, "\n")
    .replace(/\n{3,}/g, "\n\n")
    .trim()

const readTitle = (body, fallback) => {
  const titleMatch = /<title[^>]*>([\s\S]*?)<\/title>/i.exec(body)
  return collapseWhitespace(decodeEntities(titleMatch?.[1] ?? "")) || fallback
}

const excerpt = (value, maxLength = 240) =>
  value.length > maxLength ? `${value.slice(0, maxLength - 1)}...` : value

const splitIntoChunks = (title, text) => {
  const paragraphs = text
    .split(/\n+/)
    .map(paragraph => collapseWhitespace(paragraph))
    .filter(Boolean)

  if (paragraphs.length === 0) {
    return [{ heading: title, excerpt: "", text: "" }]
  }

  const chunks = []
  let current = ""

  const flush = () => {
    const normalized = collapseWhitespace(current)
    if (!normalized) {
      return
    }

    chunks.push({
      heading: title,
      excerpt: excerpt(normalized),
      text: normalized,
    })
    current = ""
  }

  for (const paragraph of paragraphs) {
    const next = current ? `${current}\n${paragraph}` : paragraph
    if (next.length > 700 && current) {
      flush()
      current = paragraph
    } else {
      current = next
    }
  }

  flush()
  return chunks
}

const parseBody = async response => {
  const contentType = response.headers.get("content-type")?.toLowerCase() ?? ""
  const body = await response.text()
  if (contentType.includes("text/html")) {
    return {
      title: readTitle(body, response.url),
      text: stripHtml(body),
    }
  }

  return {
    title: response.url,
    text: collapseWhitespace(body),
  }
}

const isFresh = (document, now, cacheTtlMs) =>
  now - new Date(document.lastFetchedAt).getTime() <= cacheTtlMs

const fetchDocument = async (source, dependencies) => {
  const response = await dependencies.fetch(source.url, {
    headers: {
      Accept: "text/html, text/plain, text/markdown;q=0.9, application/json;q=0.1",
    },
  })

  if (!response.ok) {
    throw new Error(`Failed to fetch documentation ${source.url}: ${response.status}`)
  }

  const parsed = await parseBody(response)
  const document = {
    title: source.title ?? parsed.title,
    url: source.url,
    lastFetchedAt: new Date(dependencies.now()).toISOString(),
    sourceKind: "official_doc",
    chunks: splitIntoChunks(source.title ?? parsed.title, parsed.text),
  }

  dependencies.cacheStore.set(source.url, document)
  return document
}

const loadDocument = async (source, refresh, dependencies) => {
  const cached = dependencies.cacheStore.get(source.url)

  if (!refresh && cached && isFresh(cached, dependencies.now(), dependencies.cacheTtlMs)) {
    return cached
  }

  try {
    return await fetchDocument(source, dependencies)
  } catch (error) {
    if (cached) {
      return cached
    }
    throw error
  }
}

const tokenize = value =>
  value
    .trim()
    .toLowerCase()
    .split(/[^\p{L}\p{N}]+/u)
    .map(token => token.trim())
    .filter(Boolean)

const countMatches = (haystack, needles) =>
  needles.reduce((score, needle) => score + (haystack.includes(needle) ? 1 : 0), 0)

export const searchDocumentation = async (input, overrides = {}) => {
  const dependencies = {
    ...DEFAULT_DOCS_DEPENDENCIES,
    ...overrides,
    cacheStore: overrides.cacheStore ?? DEFAULT_DOCS_DEPENDENCIES.cacheStore,
    now: overrides.now ?? DEFAULT_DOCS_DEPENDENCIES.now,
    cacheTtlMs: overrides.cacheTtlMs ?? DEFAULT_DOCS_DEPENDENCIES.cacheTtlMs,
  }

  const limit = Math.max(1, Math.min(input.limit, 20))
  const settledDocs = await Promise.allSettled(
    input.sources.map(source => loadDocument(source, input.refresh, dependencies)),
  )
  const docs = settledDocs.flatMap(result => (result.status === "fulfilled" ? [result.value] : []))
  const failures = settledDocs.flatMap(result =>
    result.status === "rejected" ? [toError(result.reason)] : [],
  )
  const queryTokens = tokenize(input.query)
  const scored = []

  for (const note of input.notes) {
    const haystack = `${note.title} ${note.content}`.toLowerCase()
    const score = countMatches(haystack, queryTokens) + 10
    if (score > 10 || queryTokens.length === 0) {
      scored.push({
        title: note.title,
        url: note.url,
        heading: note.title,
        excerpt: excerpt(note.content),
        sourceKind: "provider_note",
        lastFetchedAt: new Date(dependencies.now()).toISOString(),
        score,
      })
    }
  }

  for (const document of docs) {
    for (const chunk of document.chunks) {
      const haystack =
        `${document.title} ${chunk.heading} ${chunk.text} ${document.url}`.toLowerCase()
      const score =
        countMatches(document.title.toLowerCase(), queryTokens) * 5 +
        countMatches(chunk.heading.toLowerCase(), queryTokens) * 3 +
        countMatches(haystack, queryTokens)
      if (score > 0 || queryTokens.length === 0) {
        scored.push({
          title: document.title,
          url: document.url,
          heading: chunk.heading,
          excerpt: chunk.excerpt,
          sourceKind: document.sourceKind,
          lastFetchedAt: document.lastFetchedAt,
          score,
        })
      }
    }
  }

  const results = scored
    .sort((left, right) => {
      if (left.sourceKind !== right.sourceKind) {
        return left.sourceKind === "provider_note" ? -1 : 1
      }
      if (right.score !== left.score) {
        return right.score - left.score
      }
      return left.title.localeCompare(right.title)
    })
    .slice(0, limit)

  if (failures.length > 0 && results.length === 0) {
    throw failures[0]
  }

  return results
}

export const inspectShopifyRuntime = () => {
  const storeDomain = readEnvString("SHOPIFY_STORE_DOMAIN")
  const clientId = readEnvString("SHOPIFY_CLIENT_ID")
  const apiKey = readEnvString("SHOPIFY_CLIENT_SECRET")
  const apiVersion = readEnvString("SHOPIFY_API_VERSION") ?? shopifyProvider.defaultApiVersion
  const status = storeDomain && clientId && apiKey ? "ready" : "missing_config"

  return {
    provider: shopifyProvider.name,
    status,
    connection: {
      storeDomain: storeDomain ?? "missing",
      clientId: clientId ?? "missing",
      apiVersion,
    },
    configured: {
      storeDomain: Boolean(storeDomain),
      clientId: Boolean(clientId),
      apiKey: Boolean(apiKey),
      apiVersion: Boolean(readEnvString("SHOPIFY_API_VERSION")),
    },
    text: [
      `Provider: ${shopifyProvider.name}`,
      `Status: ${status}`,
      `Store domain: ${storeDomain ?? "missing"}`,
      `Client ID: ${clientId ?? "missing"}`,
      `API version: ${apiVersion}`,
      `API key: ${apiKey ? "configured" : "missing"}`,
    ].join("\n"),
  }
}

export const loadShopifyConnectionFromEnv = () => {
  const connection = {
    storeDomain: readEnvString("SHOPIFY_STORE_DOMAIN"),
    clientId: readEnvString("SHOPIFY_CLIENT_ID"),
    apiKey: readEnvString("SHOPIFY_CLIENT_SECRET"),
    apiVersion: readEnvString("SHOPIFY_API_VERSION"),
  }

  const validation = shopifyProvider.validateConnection(connection)
  if (!validation.ok) {
    throw new Error(validation.reason)
  }

  return connection
}

const serializeLogArgs = args =>
  args
    .map(arg => {
      if (typeof arg === "string") {
        return arg
      }
      try {
        return JSON.stringify(arg)
      } catch {
        return "[unserializable]"
      }
    })
    .join(" ")

const validateScript = script => {
  for (const item of FORBIDDEN_PATTERNS) {
    if (item.pattern.test(script)) {
      return item.message
    }
  }
  return undefined
}

const freeze = value => {
  if (value && typeof value === "object") {
    return Object.freeze(value)
  }
  return value
}

const normalizeResult = value => {
  if (value === undefined || value === null) {
    return value
  }

  if (typeof value === "string" || typeof value === "number" || typeof value === "boolean") {
    return value
  }

  try {
    return JSON.parse(JSON.stringify(value))
  } catch {
    return value
  }
}

export const executeScript = async input => {
  const validationError = validateScript(input.script)
  if (validationError) {
    return {
      status: "error",
      result: null,
      logs: [],
      warnings: [],
      error: validationError,
      requestSummary: [],
      rawResponses: [],
    }
  }

  const controller = new AbortController()
  const logs = []
  const warnings = []
  let requestSummary = []
  let rawResponses = []

  try {
    const providerContext = await input.provider.createExecutorContext(
      input.connection,
      controller.signal,
      {
        mode: input.mode,
      },
    )
    requestSummary = providerContext.requestSummary
    rawResponses = providerContext.rawResponses
    const timeoutMs = Math.max(100, Math.min(input.timeoutMs, 60000))

    const sandbox = vm.createContext(
      {
        __input: freeze({
          provider: freeze({
            graphql: providerContext.graphql,
            request: providerContext.request,
          }),
          profile: freeze(providerContext.profile),
          connection: freeze(providerContext.connection),
          console: freeze({
            log: (...args) => {
              logs.push(serializeLogArgs(args))
            },
            error: (...args) => {
              logs.push(serializeLogArgs(args))
            },
          }),
        }),
        AbortController: undefined,
        Buffer: undefined,
        process: undefined,
        globalThis: undefined,
        require: undefined,
        fetch: undefined,
        module: undefined,
        exports: undefined,
      },
      {
        codeGeneration: {
          strings: false,
          wasm: false,
        },
      },
    )

    const runner = new vm.Script(
      `
        (async () => {
          const { provider, profile, connection, console } = __input
          ${input.script}
        })()
      `,
      {
        filename: `${input.provider.name}-${input.mode}.js`,
      },
    )

    const timeoutPromise = new Promise((_, reject) => {
      const handle = setTimeout(() => {
        controller.abort()
        reject(new Error(`Execution timed out after ${timeoutMs}ms.`))
      }, timeoutMs)

      controller.signal.addEventListener(
        "abort",
        () => {
          clearTimeout(handle)
        },
        { once: true },
      )
    })

    const result = await Promise.race([
      runner.runInContext(sandbox, {
        timeout: timeoutMs,
      }),
      timeoutPromise,
    ])

    controller.abort()
    return {
      status: "ok",
      result: normalizeResult(result),
      logs,
      warnings,
      requestSummary,
      rawResponses,
    }
  } catch (error) {
    controller.abort()
    return {
      status: "error",
      result: null,
      logs,
      warnings,
      error: error instanceof Error ? error.message : "Execution failed.",
      requestSummary,
      rawResponses,
    }
  }
}

export const parseArgs = argv => {
  const flags = {}

  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index]
    if (!token.startsWith("--")) {
      throw new Error(`Unexpected argument "${token}".`)
    }

    const key = token.slice(2)
    const next = argv[index + 1]
    if (!next || next.startsWith("--")) {
      flags[key] = true
      continue
    }

    flags[key] = next
    index += 1
  }

  return flags
}

export const requireStringFlag = (flags, key) => {
  const value = flags[key]
  if (typeof value !== "string" || value.trim().length === 0) {
    throw new Error(`Missing required --${key} value.`)
  }

  return value
}

export const readIntegerFlag = (flags, key, defaultValue) => {
  const value = flags[key]
  if (value === undefined || value === true) {
    return defaultValue
  }

  const parsed = Number.parseInt(String(value), 10)
  if (!Number.isFinite(parsed)) {
    throw new Error(`Expected --${key} to be an integer.`)
  }

  return parsed
}

const readStdin = async () => {
  if (process.stdin.isTTY) {
    return undefined
  }

  const chunks = []
  for await (const chunk of process.stdin) {
    chunks.push(typeof chunk === "string" ? chunk : chunk.toString("utf8"))
  }

  const value = chunks.join("")
  return value.trim().length > 0 ? value : undefined
}

export const loadScript = async flags => {
  if (typeof flags.script === "string" && flags.script.length > 0) {
    return flags.script
  }

  if (typeof flags["script-file"] === "string" && flags["script-file"].length > 0) {
    const absolutePath = path.resolve(process.cwd(), flags["script-file"])
    return fs.readFile(absolutePath, "utf8")
  }

  const stdin = await readStdin()
  if (stdin) {
    return stdin
  }

  throw new Error("Provide --script, --script-file, or pipe a script on stdin.")
}

export const printJson = value => {
  process.stdout.write(`${JSON.stringify(value, null, 2)}\n`)
}

export const runCli = async main => {
  try {
    const result = await main()
    if (result !== undefined) {
      printJson(result)
    }
  } catch (error) {
    process.exitCode = 1
    printJson({
      status: "error",
      error: error instanceof Error ? error.message : "Unexpected error.",
    })
  }
}
