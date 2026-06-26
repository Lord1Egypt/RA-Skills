/**
 * @skillboss/openclaw-plugin
 *
 * OpenClaw plugin that gives any agent access to SkillBoss's 700+ AI tools
 * via one wallet. Ships a generic `skillboss_run` tool dispatcher plus a
 * handful of convenience aliases for the most-used skills.
 *
 * See: https://www.skillboss.co/docs/openclaw-plugin
 * Protocol: Agent Shopping Protocol v0.1
 * https://www.skillboss.co/docs/agent-shopping-protocol
 */

import { Type, type Static, type TSchema } from '@sinclair/typebox'

// OpenClaw plugin API surface — typed loosely so we don't require a runtime
// dep on `openclaw`. The actual OpenClaw runtime injects a concrete `api`
// object at load time with the shape below.
type OpenClawToolContent = {
  type: 'text' | 'image' | 'json'
  text?: string
  data?: unknown
}

type OpenClawToolResult = {
  content: OpenClawToolContent[]
  isError?: boolean
  meta?: Record<string, unknown>
}

type RegisterToolOptions = {
  optional?: boolean
}

type OpenClawPluginApi = {
  config: SkillBossPluginConfig
  registerTool: (
    def: {
      name: string
      description: string
      parameters: TSchema | Record<string, unknown>
      execute: (
        id: string,
        params: Record<string, unknown>,
      ) => Promise<OpenClawToolResult>
    },
    options?: RegisterToolOptions,
  ) => void
  runtime?: Record<string, unknown>
}

type SkillBossPluginConfig = {
  apiKey: string
  agentName?: string
  baseUrl?: string
  maxCostPerCallUsd?: number
  defaultChatModel?: string
  defaultImageModel?: string
}

// -----------------------------------------------------------------------------
// Configuration & shared helpers
// -----------------------------------------------------------------------------

const DEFAULT_BASE_URL = 'https://api.skillboss.co/v1'
const DEFAULT_AGENT_NAME = 'openclaw'
const DEFAULT_CHAT_MODEL = 'claude-4-6-sonnet'
const DEFAULT_IMAGE_MODEL = 'vertex/gemini-3-pro-image-preview'
const DEFAULT_MAX_COST_USD = 2.0
const CATALOG_URL = 'https://www.skillboss.co/api/catalog'

type RunResponse = {
  ok: boolean
  result?: unknown
  cost_usd?: number
  wallet_balance_after_usd?: number
  receipt?: string
  error?: string
}

type CatalogProduct = {
  id: string
  slug: string
  name: string
  category: string
  vendor?: string
  description?: string
  pricing?: {
    unit: 'request' | 'token' | 'unknown'
    per_request_usd?: number
    per_1m_input_usd?: number
    per_1m_output_usd?: number
  }
  capabilities?: string[]
}

/**
 * POST /v1/run — the single endpoint every SkillBoss skill call goes
 * through. Handles auth, audit headers, retry hinting, and error
 * normalization for the LLM.
 */
async function skillbossRun(
  config: SkillBossPluginConfig,
  skill: string,
  inputs: Record<string, unknown>,
  opts?: { taskId?: string; maxCostUsd?: number },
): Promise<RunResponse> {
  const base = config.baseUrl || DEFAULT_BASE_URL
  const agentName = config.agentName || DEFAULT_AGENT_NAME
  const maxCost =
    opts?.maxCostUsd ?? config.maxCostPerCallUsd ?? DEFAULT_MAX_COST_USD

  const headers: Record<string, string> = {
    Authorization: `Bearer ${config.apiKey}`,
    'Content-Type': 'application/json',
    'X-Agent-Name': agentName,
    'X-Payment-Protocol': 'skillboss_wallet',
    'X-Max-Cost-Usd': String(maxCost),
  }
  if (opts?.taskId) headers['X-Parent-Task-Id'] = opts.taskId

  try {
    const res = await fetch(`${base}/run`, {
      method: 'POST',
      headers,
      body: JSON.stringify({ model: skill, inputs }),
    })
    const data = (await res.json()) as RunResponse
    if (!res.ok) {
      return {
        ok: false,
        error:
          data.error ||
          `SkillBoss /v1/run returned ${res.status} ${res.statusText}`,
      }
    }
    return { ...data, ok: true }
  } catch (err) {
    return {
      ok: false,
      error:
        err instanceof Error
          ? `SkillBoss /v1/run network error: ${err.message}`
          : 'SkillBoss /v1/run unknown network error',
    }
  }
}

function toToolResult(response: RunResponse): OpenClawToolResult {
  if (!response.ok) {
    return {
      content: [
        {
          type: 'text',
          text: response.error || 'SkillBoss call failed with no error body.',
        },
      ],
      isError: true,
    }
  }
  const meta: Record<string, unknown> = {}
  if (typeof response.cost_usd === 'number') meta.cost_usd = response.cost_usd
  if (typeof response.wallet_balance_after_usd === 'number') {
    meta.wallet_balance_after_usd = response.wallet_balance_after_usd
  }
  if (response.receipt) meta.receipt = response.receipt
  return {
    content: [
      {
        type: 'text',
        text:
          typeof response.result === 'string'
            ? response.result
            : JSON.stringify(response.result ?? null, null, 2),
      },
    ],
    meta: Object.keys(meta).length > 0 ? meta : undefined,
  }
}

// -----------------------------------------------------------------------------
// Typebox schemas for the tools
// -----------------------------------------------------------------------------

const RunParams = Type.Object({
  skill: Type.String({
    description:
      'Skill id to invoke. Use skillboss_catalog_search to discover valid skill ids, or see https://www.skillboss.co/api/catalog.',
  }),
  inputs: Type.Record(Type.String(), Type.Unknown(), {
    description:
      'Vendor-specific inputs object for the skill. Schema varies by skill — check the product page at https://www.skillboss.co/use/{slug}/product.json.',
  }),
  max_cost_usd: Type.Optional(
    Type.Number({
      minimum: 0,
      description:
        'Optional per-call hard cap. If the server estimates the call costs more than this, it will return an error instead of charging.',
    }),
  ),
  task_id: Type.Optional(
    Type.String({
      description:
        'Optional parent task id. Grouped in the SkillBoss audit log so you can reconstruct "everything this task bought".',
    }),
  ),
})

const CatalogSearchParams = Type.Object({
  query: Type.String({
    description:
      "Free-form description of the skill you want, e.g. 'scrape a JS-rendered site' or 'transcribe an audio file'.",
  }),
  category: Type.Optional(
    Type.Union(
      [
        Type.Literal('intelligence'),
        Type.Literal('information'),
        Type.Literal('creation'),
        Type.Literal('action'),
        Type.Literal('commerce'),
      ],
      { description: 'Optional category filter.' },
    ),
  ),
  limit: Type.Optional(
    Type.Integer({ minimum: 1, maximum: 20, default: 5 }),
  ),
})

const WebScrapeParams = Type.Object({
  url: Type.String({ description: 'Target URL to scrape.' }),
  format: Type.Optional(
    Type.Union([Type.Literal('markdown'), Type.Literal('json'), Type.Literal('html')], {
      default: 'markdown',
    }),
  ),
})

const WebSearchParams = Type.Object({
  query: Type.String({ description: 'Search query.' }),
  max_results: Type.Optional(Type.Integer({ minimum: 1, maximum: 20, default: 5 })),
})

const SendEmailParams = Type.Object({
  to: Type.String({ description: 'Recipient email address.' }),
  subject: Type.String(),
  body: Type.String(),
  from: Type.Optional(Type.String()),
})

const GenerateImageParams = Type.Object({
  prompt: Type.String({ description: 'Image generation prompt.' }),
  aspect_ratio: Type.Optional(
    Type.Union([
      Type.Literal('1:1'),
      Type.Literal('16:9'),
      Type.Literal('9:16'),
      Type.Literal('4:3'),
      Type.Literal('3:4'),
    ]),
  ),
  model: Type.Optional(Type.String()),
})

const ChatParams = Type.Object({
  prompt: Type.String({ description: 'User message for the LLM.' }),
  system: Type.Optional(Type.String({ description: 'Optional system prompt.' })),
  model: Type.Optional(
    Type.String({
      description:
        'Optional model override, e.g. claude-4-6-opus, gpt-5, deepseek-v3, gemini-2.5-pro.',
    }),
  ),
  max_tokens: Type.Optional(Type.Integer({ minimum: 1, maximum: 32000 })),
})

const GetBalanceParams = Type.Object({})

// Narrow types for the params the execute functions see at runtime.
type WebScrapeInput = Static<typeof WebScrapeParams>
type WebSearchInput = Static<typeof WebSearchParams>
type SendEmailInput = Static<typeof SendEmailParams>
type GenerateImageInput = Static<typeof GenerateImageParams>
type ChatInput = Static<typeof ChatParams>
type RunInput = Static<typeof RunParams>
type CatalogSearchInput = Static<typeof CatalogSearchParams>

// -----------------------------------------------------------------------------
// Catalog cache — fetched once per plugin load, refreshed on demand
// -----------------------------------------------------------------------------

type CatalogCache = { fetchedAt: number; products: CatalogProduct[] }
const CATALOG_TTL_MS = 5 * 60 * 1000
let catalogCache: CatalogCache | null = null

async function fetchCatalog(): Promise<CatalogProduct[]> {
  if (
    catalogCache &&
    Date.now() - catalogCache.fetchedAt < CATALOG_TTL_MS
  ) {
    return catalogCache.products
  }
  try {
    const res = await fetch(CATALOG_URL)
    if (!res.ok) return catalogCache?.products ?? []
    const body = (await res.json()) as { products: CatalogProduct[] }
    catalogCache = { fetchedAt: Date.now(), products: body.products || [] }
    return catalogCache.products
  } catch {
    return catalogCache?.products ?? []
  }
}

function scoreMatch(product: CatalogProduct, query: string): number {
  const q = query.toLowerCase()
  const hay = [
    product.name,
    product.description,
    product.category,
    product.vendor,
    ...(product.capabilities || []),
    product.slug,
    product.id,
  ]
    .filter(Boolean)
    .join(' ')
    .toLowerCase()

  const terms = q.split(/\s+/).filter(Boolean)
  let score = 0
  for (const term of terms) {
    if (!term) continue
    if (hay.includes(term)) score += 1
    if (hay.split(/\W+/).includes(term)) score += 2
  }
  return score
}

// -----------------------------------------------------------------------------
// Plugin entry point
// -----------------------------------------------------------------------------

export default function skillbossPlugin(api: OpenClawPluginApi): void {
  if (!api?.config?.apiKey) {
    throw new Error(
      'SkillBoss OpenClaw plugin: apiKey is required. Get one at https://skillboss.co/console.',
    )
  }

  const config = api.config

  // -----------------------------------------------------------------
  // skillboss_run — generic dispatcher. Always available.
  // -----------------------------------------------------------------
  api.registerTool({
    name: 'skillboss_run',
    description:
      'Invoke any SkillBoss skill through the SkillBoss wallet. Charges the wallet per call. Use skillboss_catalog_search to find a skill id. See the product page at https://www.skillboss.co/use/{slug} for each skill.',
    parameters: RunParams,
    async execute(_id, params) {
      const p = params as RunInput
      const resp = await skillbossRun(config, p.skill, p.inputs, {
        taskId: p.task_id,
        maxCostUsd: p.max_cost_usd,
      })
      return toToolResult(resp)
    },
  })

  // -----------------------------------------------------------------
  // skillboss_catalog_search — semantic-ish lookup over /api/catalog
  // -----------------------------------------------------------------
  api.registerTool({
    name: 'skillboss_catalog_search',
    description:
      'Search the SkillBoss catalog for a skill that matches a natural-language query. Returns the top matches with id, pricing, and description so you can pick one for skillboss_run.',
    parameters: CatalogSearchParams,
    async execute(_id, params) {
      const p = params as CatalogSearchInput
      const products = await fetchCatalog()
      const filtered = p.category
        ? products.filter((pr) =>
            (pr.capabilities || []).includes(p.category as string),
          )
        : products
      const ranked = filtered
        .map((pr) => ({ pr, score: scoreMatch(pr, p.query) }))
        .filter((x) => x.score > 0)
        .sort((a, b) => b.score - a.score)
        .slice(0, p.limit ?? 5)
        .map(({ pr, score }) => ({
          id: pr.id,
          slug: pr.slug,
          name: pr.name,
          category: pr.category,
          description: pr.description,
          pricing: pr.pricing,
          human_url: `https://www.skillboss.co/use/${pr.slug}`,
          product_json_url: `https://www.skillboss.co/use/${pr.slug}/product.json`,
          score,
        }))
      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify(
              {
                query: p.query,
                results: ranked,
                catalog_url: CATALOG_URL,
              },
              null,
              2,
            ),
          },
        ],
      }
    },
  })

  // -----------------------------------------------------------------
  // skillboss_get_balance — quick wallet check
  // -----------------------------------------------------------------
  api.registerTool({
    name: 'skillboss_get_balance',
    description:
      "Check the current balance of the SkillBoss wallet attached to this plugin. Use before large calls to make sure you won't overdraw.",
    parameters: GetBalanceParams,
    async execute() {
      try {
        const base = config.baseUrl || DEFAULT_BASE_URL
        const res = await fetch(`${base}/wallet/balance`, {
          headers: { Authorization: `Bearer ${config.apiKey}` },
        })
        const body = await res.json()
        return {
          content: [{ type: 'text', text: JSON.stringify(body, null, 2) }],
        }
      } catch (err) {
        return {
          content: [
            {
              type: 'text',
              text: `Balance check failed: ${
                err instanceof Error ? err.message : 'unknown error'
              }`,
            },
          ],
          isError: true,
        }
      }
    },
  })

  // -----------------------------------------------------------------
  // Convenience aliases — the five highest-leverage skills
  // -----------------------------------------------------------------

  api.registerTool({
    name: 'skillboss_web_scrape',
    description:
      'Scrape a web page and return clean markdown/JSON/HTML. Powered by Firecrawl through SkillBoss. One call, wallet charged.',
    parameters: WebScrapeParams,
    async execute(_id, params) {
      const p = params as WebScrapeInput
      const resp = await skillbossRun(config, 'web_scrape', {
        url: p.url,
        format: p.format || 'markdown',
      })
      return toToolResult(resp)
    },
  })

  api.registerTool({
    name: 'skillboss_web_search',
    description:
      'Live web search. Powered by Perplexity / Brave / Exa through SkillBoss. Returns ranked results with snippets.',
    parameters: WebSearchParams,
    async execute(_id, params) {
      const p = params as WebSearchInput
      const resp = await skillbossRun(config, 'web_search', {
        query: p.query,
        max_results: p.max_results || 5,
      })
      return toToolResult(resp)
    },
  })

  api.registerTool({
    name: 'skillboss_send_email',
    description:
      'Send a plain-text email via SkillBoss (AWS SES under the hood). Charges the wallet per email.',
    parameters: SendEmailParams,
    async execute(_id, params) {
      const p = params as SendEmailInput
      const resp = await skillbossRun(config, 'send_email', {
        to: p.to,
        subject: p.subject,
        body: p.body,
        from: p.from,
      })
      return toToolResult(resp)
    },
  })

  api.registerTool({
    name: 'skillboss_generate_image',
    description:
      'Generate an image from a text prompt. Default model is Vertex Gemini 3 Pro Image. Specify `model` to override (flux, imagen, etc).',
    parameters: GenerateImageParams,
    async execute(_id, params) {
      const p = params as GenerateImageInput
      const resp = await skillbossRun(
        config,
        p.model || config.defaultImageModel || DEFAULT_IMAGE_MODEL,
        {
          prompt: p.prompt,
          aspect_ratio: p.aspect_ratio,
        },
      )
      return toToolResult(resp)
    },
  })

  api.registerTool({
    name: 'skillboss_chat',
    description:
      'Call any LLM via SkillBoss. Default model is claude-4-6-sonnet. Specify `model` to override (claude-4-6-opus, gpt-5, deepseek-v3, gemini-2.5-pro, kimi, etc).',
    parameters: ChatParams,
    async execute(_id, params) {
      const p = params as ChatInput
      const model = p.model || config.defaultChatModel || DEFAULT_CHAT_MODEL
      const resp = await skillbossRun(config, model, {
        prompt: p.prompt,
        system: p.system,
        max_tokens: p.max_tokens,
      })
      return toToolResult(resp)
    },
  })
}

// Named exports so advanced consumers can call the underlying run helper
// without spinning up the full plugin.
export { skillbossRun, fetchCatalog }
export type {
  OpenClawPluginApi,
  OpenClawToolResult,
  SkillBossPluginConfig,
  CatalogProduct,
  RunResponse,
}
