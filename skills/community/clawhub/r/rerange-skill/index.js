#!/usr/bin/env node

import { createRequire } from "node:module"
import { dirname, resolve } from "node:path"
import { fileURLToPath, pathToFileURL } from "node:url"

const require = createRequire(import.meta.url)
const baseDir = dirname(fileURLToPath(import.meta.url))

async function importWithFallback(packageName, fallbackPath) {
  try {
    return await import(packageName)
  } catch (error) {
    if (error?.code !== "ERR_MODULE_NOT_FOUND") {
      throw error
    }
    return import(pathToFileURL(resolve(baseDir, fallbackPath)).href)
  }
}

async function importViem() {
  try {
    return await import("viem")
  } catch (error) {
    if (error?.code !== "ERR_MODULE_NOT_FOUND") {
      throw error
    }
    return import(pathToFileURL(require.resolve("viem", {
      paths: [resolve(baseDir, "../sdk/node_modules")],
    })).href)
  }
}

const wagmi = await importWithFallback("@rerange/wagmi", "../sdk/dist/index.js")

function usage(exitCode = 0) {
  const output = [
    "Usage:",
    "  node index.js deployments [chainId]",
    "  node index.js abi hub|vault",
    "  node index.js encode hub|vault <functionName> <jsonArgs>",
    "  node index.js read <chainId> hub|vault <address> <functionName> <jsonArgs> [rpcUrl]",
    "",
    "Examples:",
    "  node index.js deployments 8453",
    "  node index.js encode hub getOrderState '[\"0x...\"]'",
    "  node index.js read 8453 hub 0x888956E46d2af8F6B2890a39E55542219F4bd192 hubConfig '[]' https://mainnet.base.org",
  ].join("\n")

  const stream = exitCode === 0 ? process.stdout : process.stderr
  stream.write(`${output}\n`)
  process.exit(exitCode)
}

function json(value) {
  return JSON.stringify(value, (_, nestedValue) => {
    if (typeof nestedValue === "bigint") {
      return nestedValue.toString()
    }
    return nestedValue
  }, 2)
}

function parseJsonArgs(raw) {
  if (!raw) {
    return []
  }

  const parsed = JSON.parse(raw)
  if (!Array.isArray(parsed)) {
    throw new Error("jsonArgs must be a JSON array")
  }

  return parsed
}

function getAbi(kind) {
  if (kind === "hub") {
    return wagmi.rerangeHubAbi ?? wagmi.hubAbi ?? wagmi.rawAbiConfig?.hub
  }

  if (kind === "vault") {
    return wagmi.rerangeVaultAbi ?? wagmi.vaultAbi ?? wagmi.rawAbiConfig?.vault
  }

  throw new Error("Contract kind must be 'hub' or 'vault'")
}

function getDeployment(chainIdRaw) {
  const chainId = Number(chainIdRaw)
  const deployment = wagmi.protocolDeployments?.[chainId]

  if (!deployment) {
    const supported = Object.keys(wagmi.protocolDeployments ?? {}).join(", ")
    throw new Error(`Unsupported chainId ${chainIdRaw}. Supported: ${supported}`)
  }

  return deployment
}

async function commandDeployments([chainIdRaw]) {
  if (chainIdRaw) {
    process.stdout.write(`${json(getDeployment(chainIdRaw))}\n`)
    return
  }

  process.stdout.write(`${json(wagmi.protocolDeployments)}\n`)
}

async function commandAbi([kind]) {
  if (!kind) {
    usage(1)
  }
  process.stdout.write(`${json(getAbi(kind))}\n`)
}

async function commandEncode([kind, functionName, rawArgs]) {
  if (!kind || !functionName) {
    usage(1)
  }

  const { encodeFunctionData } = await importViem()
  const data = encodeFunctionData({
    abi: getAbi(kind),
    functionName,
    args: parseJsonArgs(rawArgs),
  })

  process.stdout.write(`${json({ kind, functionName, data })}\n`)
}

async function commandRead([
  chainIdRaw,
  kind,
  address,
  functionName,
  rawArgs,
  rpcUrl,
]) {
  if (!chainIdRaw || !kind || !address || !functionName) {
    usage(1)
  }

  const deployment = getDeployment(chainIdRaw)
  const { createPublicClient, http } = await importViem()
  const client = createPublicClient({
    transport: http(rpcUrl),
  })

  const result = await client.readContract({
    address,
    abi: getAbi(kind),
    functionName,
    args: parseJsonArgs(rawArgs),
  })

  process.stdout.write(`${json({
    chainId: deployment.chainId,
    network: deployment.network,
    kind,
    address,
    functionName,
    result,
  })}\n`)
}

const [command, ...args] = process.argv.slice(2)

try {
  switch (command) {
    case "deployments":
      await commandDeployments(args)
      break
    case "abi":
      await commandAbi(args)
      break
    case "encode":
      await commandEncode(args)
      break
    case "read":
      await commandRead(args)
      break
    case "help":
    case "--help":
    case "-h":
    case undefined:
      usage(0)
      break
    default:
      throw new Error(`Unknown command: ${command}`)
  }
} catch (error) {
  process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`)
  process.exit(1)
}
