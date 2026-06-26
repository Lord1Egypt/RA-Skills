import process from "node:process"
import {
  executeScript,
  inspectShopifyRuntime,
  loadScript,
  loadShopifyConnectionFromEnv,
  parseArgs,
  readIntegerFlag,
  requireStringFlag,
  runCli,
  searchDocumentation,
} from "../lib/runtime.mjs"
import { shopifyProvider } from "../lib/shopify-provider.mjs"

const usage = `Usage:
  node skills/shopify-runtime/scripts/seller-runtime.mjs status
  node skills/shopify-runtime/scripts/seller-runtime.mjs search --query <text> [--limit <n>] [--refresh]
  node skills/shopify-runtime/scripts/seller-runtime.mjs execute --mode <read|write> [--timeout-ms <n>] [--script <text> | --script-file <path> | stdin]
`

const formatExecuteSummary = input => {
  const lines = [
    `Provider: ${input.provider}`,
    `Store: ${input.connection.storeDomain}`,
    `Status: ${input.status}`,
    `Requests: ${input.requestSummary.length}`,
  ]

  if (input.error) {
    lines.push(`Error: ${input.error}`)
  }

  if (input.logs.length > 0) {
    lines.push("Logs:")
    lines.push(...input.logs.map(line => `- ${line}`))
  }

  if (input.status === "ok") {
    lines.push(
      `Result: ${typeof input.result === "string" ? input.result : JSON.stringify(input.result)}`,
    )
  }

  return lines.join("\n")
}

const runSearch = async flags => {
  const query = requireStringFlag(flags, "query")
  const limit = readIntegerFlag(flags, "limit", 5)
  const refresh = flags.refresh === true
  const results = await searchDocumentation({
    query,
    limit,
    refresh,
    notes: shopifyProvider.curatedNotes,
    sources: shopifyProvider.defaultDocs,
  })

  return {
    status: "ok",
    provider: shopifyProvider.name,
    query,
    limit,
    refresh,
    results,
  }
}

const runExecute = async flags => {
  const mode = requireStringFlag(flags, "mode")
  if (mode !== "read" && mode !== "write") {
    throw new Error('Expected --mode to be "read" or "write".')
  }

  const connection = loadShopifyConnectionFromEnv()
  const script = await loadScript(flags)
  const timeoutMs = readIntegerFlag(flags, "timeout-ms", 15000)
  const result = await executeScript({
    provider: shopifyProvider,
    connection,
    mode,
    script,
    timeoutMs,
  })

  if (result.status === "error") {
    process.exitCode = 1
  }

  return {
    status: result.status,
    provider: shopifyProvider.name,
    connection: shopifyProvider.describeConnection(connection).connection,
    runtime: "javascript",
    mode,
    script,
    result: result.result,
    logs: result.logs,
    warnings: result.warnings,
    requestSummary: result.requestSummary,
    rawResponses: result.rawResponses,
    error: result.error ?? null,
    text: formatExecuteSummary({
      provider: shopifyProvider.name,
      connection,
      status: result.status,
      result: result.result,
      logs: result.logs,
      requestSummary: result.requestSummary,
      error: result.error,
    }),
  }
}

await runCli(async () => {
  const [command, ...rest] = process.argv.slice(2)
  if (!command || command === "--help" || command === "help") {
    process.stdout.write(usage)
    return
  }

  const flags = parseArgs(rest)

  if (command === "status") {
    return inspectShopifyRuntime()
  }

  if (command === "search") {
    return runSearch(flags)
  }

  if (command === "execute") {
    return runExecute(flags)
  }

  throw new Error(`Unknown command "${command}".`)
})
