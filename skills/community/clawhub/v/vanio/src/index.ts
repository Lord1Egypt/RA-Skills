import { readFileSync, writeFileSync, mkdirSync } from 'fs'
import { join } from 'path'
import { homedir } from 'os'
import { createServer } from 'http'
import { randomBytes } from 'crypto'

// ─── Config ──────────────────────────────────────────────────────────────────

const CONFIG_DIR = join(homedir(), '.config', 'vanio')
const CONFIG_FILE = join(CONFIG_DIR, 'config.json')
const DEFAULT_BASE_URL = 'https://api.vanio.ai'
// Production rewrites /:path* → /api/:path* so we don't include /api prefix
const API_PREFIX = '/v1'

interface Config {
  apiKey?: string
  baseUrl?: string
}

function loadConfig(): Config {
  try {
    return JSON.parse(readFileSync(CONFIG_FILE, 'utf-8'))
  } catch {
    return {}
  }
}

function saveConfig(config: Config) {
  mkdirSync(CONFIG_DIR, { recursive: true })
  writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2))
}

function getApiKey(): string {
  const envKey = process.env.VANIO_API_KEY
  if (envKey) return envKey
  const config = loadConfig()
  if (config.apiKey) return config.apiKey
  console.error('Error: No API key configured.')
  console.error('Run: vanio login <api-key>')
  console.error('Or set VANIO_API_KEY environment variable.')
  process.exit(1)
}

function getBaseUrl(): string {
  return process.env.VANIO_API_URL || loadConfig().baseUrl || DEFAULT_BASE_URL
}

// ─── HTTP Client ─────────────────────────────────────────────────────────────

async function apiCall(
  path: string,
  method: 'GET' | 'POST' = 'GET',
  body?: any,
): Promise<any> {
  const url = `${getBaseUrl()}${path}`
  const apiKey = getApiKey()

  const res = await fetch(url, {
    method,
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': apiKey,
    },
    ...(body ? { body: JSON.stringify(body) } : {}),
  })

  if (!res.ok) {
    const err = await res.json().catch(() => ({ message: res.statusText }))
    console.error(`Error ${res.status}: ${err.message || err.error || res.statusText}`)
    process.exit(1)
  }

  return res.json()
}

// ─── Commands ────────────────────────────────────────────────────────────────

async function cmdLogin(args: string[]) {
  // If a key is passed directly, use it (for scripts/CI)
  if (args[0] && !args[0].startsWith('--')) {
    const config = loadConfig()
    config.apiKey = args[0]
    saveConfig(config)
    console.log('API key saved to ~/.config/vanio/config.json')
    return
  }

  const baseUrl = process.env.VANIO_API_URL || loadConfig().baseUrl || DEFAULT_BASE_URL
  const state = randomBytes(16).toString('hex')

  // Start a temporary local server to receive the callback
  const server = createServer((req, res) => {
    const url = new URL(req.url || '/', `http://127.0.0.1`)

    if (url.pathname === '/callback') {
      const key = url.searchParams.get('key')
      const returnedState = url.searchParams.get('state')
      const user = url.searchParams.get('user') || ''

      if (returnedState !== state) {
        res.writeHead(400, { 'Content-Type': 'text/html' })
        res.end('<h1>State mismatch — login aborted</h1><p>Close this tab and try again.</p>')
        server.close()
        console.error('Error: state mismatch. Possible CSRF attack. Try again.')
        process.exit(1)
        return
      }

      if (!key) {
        res.writeHead(400, { 'Content-Type': 'text/html' })
        res.end('<h1>No API key received</h1><p>Close this tab and try again.</p>')
        server.close()
        console.error('Error: no API key received from server.')
        process.exit(1)
        return
      }

      // Save the key
      const config = loadConfig()
      config.apiKey = key
      config.baseUrl = baseUrl
      saveConfig(config)

      // Immediately redirect to strip the key from the URL bar, then show success
      res.writeHead(200, { 'Content-Type': 'text/html' })
      res.end(`
        <html>
          <head><title>Vanio CLI</title></head>
          <body style="font-family: system-ui; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; background: #0a0a0a; color: #fff;">
            <div style="text-align: center;">
              <h1 style="font-size: 2rem;">✓ Logged in to Vanio</h1>
              <p style="color: #888;">You can close this tab and return to your terminal.</p>
            </div>
          </body>
          <script>history.replaceState(null, '', '/')</script>
        </html>
      `)

      console.log(`\nLogged in as ${user || 'unknown'}`)
      console.log('API key saved to ~/.config/vanio/config.json')

      setTimeout(() => { server.close(); process.exit(0) }, 1000)
      return
    }

    res.writeHead(404)
    res.end()
  })

  // Find a free port
  await new Promise<void>((resolve) => {
    server.listen(0, '127.0.0.1', () => resolve())
  })

  const port = (server.address() as any).port
  const authUrl = `${baseUrl}${API_PREFIX}/auth/cli?port=${port}&state=${state}`

  console.log('Opening browser to authenticate...')
  console.log(`If it doesn't open, visit: ${authUrl}`)

  // Open browser
  const { exec } = await import('child_process')
  const openCmd = process.platform === 'darwin'
    ? `open "${authUrl}"`
    : process.platform === 'win32'
      ? `start "${authUrl}"`
      : `xdg-open "${authUrl}"`

  exec(openCmd)

  console.log('Waiting for authentication...')

  // Timeout after 2 minutes
  setTimeout(() => {
    console.error('\nLogin timed out. Try again.')
    server.close()
    process.exit(1)
  }, 120_000)
}

async function cmdAsk(args: string[]) {
  const query = args.join(' ')
  if (!query) {
    console.error('Usage: vanio ask <question>')
    console.error('       vanio ask "What are my check-ins today?"')
    process.exit(1)
  }

  const opts: any = { query }

  // Parse flags
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--reservation' && args[i + 1]) {
      opts.reservationId = parseInt(args[++i], 10)
    } else if (args[i] === '--listing' && args[i + 1]) {
      opts.listingId = parseInt(args[++i], 10)
    } else if (args[i] === '--thread' && args[i + 1]) {
      opts.threadId = args[++i]
    }
  }

  // Re-join non-flag args as query
  const queryParts = args.filter((a, i) => {
    if (a.startsWith('--')) return false
    if (i > 0 && args[i - 1].startsWith('--')) return false
    return true
  })
  opts.query = queryParts.join(' ')

  if (!opts.query) {
    console.error('No query provided.')
    process.exit(1)
  }

  const result = await apiCall(`${API_PREFIX}/chat`, 'POST', opts)

  console.log(result.answer)

  if (result.sources?.length) {
    console.log('')
    console.log('Sources:')
    for (const s of result.sources) {
      console.log(`  - ${s.label} (${s.type})`)
    }
  }

  if (result.usage) {
    console.error(`\n[${result.usage.model} | ${result.usage.inputTokens + result.usage.outputTokens} tokens | $${result.usage.cost?.toFixed(4) || '?'}]`)
  }
}

async function cmdChat(args: string[]) {
  const readline = await import('readline')
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout })

  const threadId = `cli-${Date.now()}`
  const history: Array<{ role: 'user' | 'assistant'; content: string }> = []

  console.log('Vanio AI — interactive chat (type "exit" to quit)')
  console.log('─'.repeat(50))

  const prompt = () => {
    rl.question('\nYou: ', async (input) => {
      const trimmed = input.trim()
      if (!trimmed || trimmed === 'exit' || trimmed === 'quit') {
        rl.close()
        return
      }

      history.push({ role: 'user', content: trimmed })

      const result = await apiCall(`${API_PREFIX}/chat`, 'POST', {
        query: trimmed,
        threadId,
        conversationHistory: history.slice(-20),
      })

      console.log(`\nVanio: ${result.answer}`)
      history.push({ role: 'assistant', content: result.answer })

      prompt()
    })
  }

  prompt()
}

async function cmdStatus() {
  const result = await apiCall(`${API_PREFIX}/chat`, 'GET')
  console.log(`Service: ${result.service}`)
  console.log(`Version: ${result.version}`)
  console.log(`Tools:   ${result.tools}`)
  console.log(`Status:  ${result.status}`)
}

async function cmdConfig(args: string[]) {
  const config = loadConfig()

  if (args[0] === 'set' && args[1] && args[2]) {
    const key = args[1] as keyof Config
    if (key === 'apiKey' || key === 'baseUrl') {
      config[key] = args[2]
      saveConfig(config)
      console.log(`Set ${key} = ${args[2]}`)
    } else {
      console.error(`Unknown config key: ${key}. Valid keys: apiKey, baseUrl`)
    }
    return
  }

  if (args[0] === 'get' && args[1]) {
    console.log(config[args[1] as keyof Config] || '(not set)')
    return
  }

  // Show all config
  console.log(`API Key:  ${config.apiKey ? config.apiKey.slice(0, 8) + '...' : '(not set)'}`)
  console.log(`Base URL: ${config.baseUrl || DEFAULT_BASE_URL}`)
  console.log(`Config:   ${CONFIG_FILE}`)
}

function showHelp() {
  console.log(`
Vanio AI CLI — manage your vacation rental portfolio via AI

Usage:
  vanio <command> [options]

Commands:
  login                    Authenticate via browser (opens Vanio dashboard)
  login <api-key>          Authenticate with an API key directly
  logout                   Remove saved credentials
  ask <question>           Ask Vanio AI a question (single query)
  chat                     Start interactive conversation
  status                   Check API connection
  config                   Show current configuration
  config set <key> <val>   Set config value (apiKey, baseUrl)
  help                     Show this help

Ask Options:
  --reservation <id>       Scope question to a specific reservation
  --listing <id>           Scope question to a specific listing
  --thread <id>            Continue a conversation thread

Examples:
  vanio ask "What are today's check-ins?"
  vanio ask "What's the WiFi password at Alpine Lodge?" --listing 42
  vanio ask "Why was this guest charged extra?" --reservation 214303
  vanio chat
  vanio config set baseUrl https://api.vanio.ai

Environment:
  VANIO_API_KEY            API key (overrides config file)
  VANIO_API_URL            Base URL (overrides config file)
`.trim())
}

// ─── Main ────────────────────────────────────────────────────────────────────

async function main() {
  const [command, ...args] = process.argv.slice(2)

  switch (command) {
    case 'login':
      return cmdLogin(args)
    case 'logout': {
      const config = loadConfig()
      delete config.apiKey
      saveConfig(config)
      console.log('Logged out. API key removed.')
      return
    }
    case 'ask':
      return cmdAsk(args)
    case 'chat':
      return cmdChat(args)
    case 'status':
      return cmdStatus()
    case 'config':
      return cmdConfig(args)
    case 'help':
    case '--help':
    case '-h':
      return showHelp()
    case undefined:
      showHelp()
      break
    default:
      // If no known command, treat the entire args as a query
      return cmdAsk([command, ...args])
  }
}

main().catch((err) => {
  console.error(err.message || err)
  process.exit(1)
})
