/**
 * Natural Language Interface — parse human commands into Reach primitive calls.
 *
 * No LLM needed. Uses keyword matching and pattern recognition for common commands.
 *
 * Usage:
 *   import { parseCommand, executeCommand } from './natural.js';
 *   const plan = parseCommand("go to github and check my repos");
 *   // { primitive: 'fetch', method: 'fetch', params: { url: 'https://github.com' } }
 */

// Site aliases — common names to URLs
const SITE_ALIASES = {
  github: 'https://github.com',
  upwork: 'https://www.upwork.com',
  cantina: 'https://cantina.xyz',
  code4rena: 'https://code4rena.com',
  c4: 'https://code4rena.com',
  immunefi: 'https://immunefi.com',
  basescan: 'https://basescan.org',
  twitter: 'https://twitter.com',
  x: 'https://twitter.com',
  farcaster: 'https://warpcast.com',
  warpcast: 'https://warpcast.com',
  opensea: 'https://opensea.io',
  etherscan: 'https://etherscan.io',
  google: 'https://www.google.com',
  dexscreener: 'https://dexscreener.com',
  coingecko: 'https://www.coingecko.com',
};

// Patterns: [regex, handler function]
const PATTERNS = [
  // --- Navigation / Fetch ---
  {
    patterns: [
      /^(?:go to|open|visit|navigate to|browse)\s+(.+)/i,
      /^(?:fetch|get|read|load)\s+(.+)/i,
    ],
    handler: (match) => {
      const target = match[1].trim();
      const url = resolveUrl(target);
      return {
        primitive: 'fetch',
        method: 'fetch',
        params: { url },
        description: `Fetch ${url}`,
      };
    },
  },

  // --- Search ---
  {
    patterns: [
      /^search\s+(\w+)\s+for\s+(.+)/i,
      /^(?:find|look for)\s+(.+)\s+on\s+(\w+)/i,
    ],
    handler: (match) => {
      // "search upwork for solidity jobs" or "find solidity jobs on upwork"
      let site, query;
      if (/^search/i.test(match[0])) {
        site = match[1];
        query = match[2];
      } else {
        query = match[1];
        site = match[2];
      }

      const siteLower = site.toLowerCase();
      if (SITE_ALIASES[siteLower]) {
        return {
          primitive: 'site',
          method: 'search',
          site: siteLower,
          params: { query: query.trim() },
          description: `Search ${site} for "${query.trim()}"`,
        };
      }

      // Generic search via Google
      return {
        primitive: 'fetch',
        method: 'fetch',
        params: { url: `https://www.google.com/search?q=${encodeURIComponent(`${query} site:${site}`)}` },
        description: `Search Google for "${query}" on ${site}`,
      };
    },
  },

  // --- Click / Interact ---
  {
    patterns: [
      /^(?:click|press|tap|hit)\s+(?:on\s+)?(?:the\s+)?["']?(.+?)["']?$/i,
    ],
    handler: (match) => {
      const target = match[1].trim();
      return {
        primitive: 'act',
        method: 'click',
        params: { text: target },
        description: `Click "${target}"`,
      };
    },
  },

  // --- Type / Fill ---
  {
    patterns: [
      /^(?:type|enter|input|fill)\s+["'](.+?)["']\s+(?:in|into)\s+(.+)/i,
      /^(?:type|enter|input|fill)\s+(.+)/i,
    ],
    handler: (match) => {
      if (match[2]) {
        return {
          primitive: 'act',
          method: 'type',
          params: { text: match[1], selector: match[2].trim() },
          description: `Type "${match[1]}" into ${match[2]}`,
        };
      }
      return {
        primitive: 'act',
        method: 'type',
        params: { text: match[1] },
        description: `Type "${match[1]}"`,
      };
    },
  },

  // --- Email ---
  {
    patterns: [
      /^(?:email|send email|mail)\s+(\S+@\S+)\s+(?:about|subject|re)\s+["']?(.+?)["']?(?:\s+(?:saying|body|message)\s+["']?(.+?)["']?)?$/i,
      /^(?:email|send email|mail)\s+(\S+@\S+)\s+["']?(.+?)["']?$/i,
    ],
    handler: (match) => {
      const to = match[1];
      const subject = match[2] || '';
      const body = match[3] || '';
      return {
        primitive: 'email',
        method: 'sendEmail',
        params: { to, subject, body },
        description: `Email ${to}: "${subject}"`,
      };
    },
  },

  // --- Sign / Crypto ---
  {
    patterns: [
      /^(?:sign)\s+(?:message\s+)?["']?(.+?)["']?$/i,
    ],
    handler: (match) => {
      return {
        primitive: 'sign',
        method: 'sign',
        params: { payload: match[1] },
        description: `Sign message: "${match[1]}"`,
      };
    },
  },

  // --- Send ETH/Token ---
  {
    patterns: [
      /^(?:send|transfer|pay)\s+([\d.]+)\s*(ETH|USDC|WETH|DAI)?\s+to\s+(0x[a-fA-F0-9]{40}|\S+)/i,
    ],
    handler: (match) => {
      const amount = match[1];
      const currency = match[2] || 'ETH';
      const recipient = match[3];
      return {
        primitive: 'pay',
        method: 'pay',
        params: { recipient, amount, token: currency === 'ETH' ? undefined : currency },
        description: `Send ${amount} ${currency} to ${recipient}`,
      };
    },
  },

  // --- Watch / Monitor ---
  {
    patterns: [
      /^(?:watch|monitor|observe|track|alert)\s+(.+?)(?:\s+(?:every|each)\s+(\d+)\s*(?:s|sec|seconds?|m|min|minutes?|h|hr|hours?))?$/i,
    ],
    handler: (match) => {
      const target = resolveUrl(match[1].trim());
      let interval = 30000; // default 30s
      if (match[2]) {
        const num = parseInt(match[2]);
        const unit = match[0].match(/(\d+)\s*(s|sec|seconds?|m|min|minutes?|h|hr|hours?)/i)?.[2] || 's';
        if (unit.startsWith('m')) interval = num * 60000;
        else if (unit.startsWith('h')) interval = num * 3600000;
        else interval = num * 1000;
      }
      return {
        primitive: 'observe',
        method: 'observe',
        params: { target, interval, method: 'poll' },
        description: `Watch ${target} every ${interval / 1000}s`,
      };
    },
  },

  // --- Remember / Save ---
  {
    patterns: [
      /^(?:remember|save|store)\s+(?:that\s+)?["']?(.+?)["']?\s+(?:as|=|is)\s+["']?(.+?)["']?$/i,
    ],
    handler: (match) => {
      return {
        primitive: 'persist',
        method: 'persist',
        params: { key: match[1].trim(), value: match[2].trim() },
        description: `Store "${match[1].trim()}" = "${match[2].trim()}"`,
      };
    },
  },

  // --- Recall ---
  {
    patterns: [
      /^(?:recall|what (?:is|was)|get)\s+["']?(.+?)["']?\??$/i,
    ],
    handler: (match) => {
      return {
        primitive: 'persist',
        method: 'recall',
        params: { key: match[1].trim() },
        description: `Recall "${match[1].trim()}"`,
      };
    },
  },

  // --- Screenshot / See ---
  {
    patterns: [
      /^(?:screenshot|see|look at|capture)\s+(.+)/i,
    ],
    handler: (match) => {
      const url = resolveUrl(match[1].trim());
      return {
        primitive: 'see',
        method: 'see',
        params: { url },
        description: `Screenshot ${url}`,
      };
    },
  },

  // --- Login / Auth ---
  {
    patterns: [
      /^(?:login|log in|authenticate|auth)\s+(?:to\s+)?(\w+)/i,
    ],
    handler: (match) => {
      const service = match[1].toLowerCase();
      return {
        primitive: 'authenticate',
        method: 'authenticate',
        params: { service, method: 'cookie' },
        description: `Authenticate with ${service}`,
      };
    },
  },
];

/**
 * Parse a natural language command into a Reach primitive call plan.
 *
 * @param {string} text - Natural language command
 * @returns {object|null} { primitive, method, params, description } or null if not understood
 */
export function parseCommand(text) {
  if (!text || typeof text !== 'string') return null;

  const trimmed = text.trim();
  if (!trimmed) return null;

  for (const { patterns, handler } of PATTERNS) {
    for (const pattern of patterns) {
      const match = trimmed.match(pattern);
      if (match) {
        try {
          return handler(match);
        } catch {
          continue;
        }
      }
    }
  }

  // Fallback: if it looks like a URL, fetch it
  if (/^https?:\/\//i.test(trimmed) || /^\w+\.\w+/.test(trimmed)) {
    const url = resolveUrl(trimmed);
    return {
      primitive: 'fetch',
      method: 'fetch',
      params: { url },
      description: `Fetch ${url}`,
    };
  }

  return null;
}

/**
 * Execute a natural language command using a Reach instance.
 *
 * @param {string} text - Natural language command
 * @param {import('./index.js').Reach} reach - Reach instance
 * @returns {object} { plan, result } or { error }
 */
export async function executeCommand(text, reach) {
  const plan = parseCommand(text);

  if (!plan) {
    return {
      error: `Could not understand: "${text}"`,
      suggestions: [
        'go to <url>',
        'search <site> for <query>',
        'click <element>',
        'type "text" into <field>',
        'email <address> about <subject>',
        'send <amount> ETH to <address>',
        'watch <url> every <interval>',
        'remember <key> as <value>',
        'screenshot <url>',
        'login to <service>',
      ],
    };
  }

  try {
    let result;

    switch (plan.primitive) {
      case 'fetch':
        result = await reach.fetch(plan.params.url, plan.params);
        break;
      case 'act':
        result = await reach.act(plan.params.url || '', plan.method, plan.params);
        break;
      case 'authenticate':
        result = await reach.authenticate(plan.params.service, plan.params.method);
        break;
      case 'sign':
        result = await reach.sign(plan.params.payload);
        break;
      case 'persist':
        if (plan.method === 'persist') {
          result = reach.persist(plan.params.key, plan.params.value);
        } else {
          result = reach.recall(plan.params.key);
        }
        break;
      case 'observe':
        result = { status: 'observe requires a callback — use the API directly' };
        break;
      case 'pay':
        result = await reach.pay?.(plan.params.recipient, plan.params.amount, plan.params);
        break;
      case 'email':
        result = await reach.email(plan.params.to, plan.params.subject, plan.params.body);
        break;
      case 'see':
        result = await reach.see(plan.params.url);
        break;
      case 'site':
        // Delegate to site skill
        const siteSkill = reach.sites?.[plan.site];
        if (siteSkill?.searchJobs) {
          result = await siteSkill.searchJobs(plan.params.query);
        } else if (siteSkill?.search) {
          result = await siteSkill.search(plan.params.query);
        } else {
          result = { error: `No search method for site: ${plan.site}` };
        }
        break;
      default:
        result = { error: `Unknown primitive: ${plan.primitive}` };
    }

    return { plan, result };
  } catch (e) {
    return { plan, error: e.message };
  }
}

/**
 * Resolve a target string to a URL.
 */
function resolveUrl(target) {
  // Check aliases first
  const lower = target.toLowerCase().replace(/['"]/g, '');
  if (SITE_ALIASES[lower]) return SITE_ALIASES[lower];

  // Check if it's already a URL
  if (/^https?:\/\//i.test(target)) return target;

  // Check if it looks like a domain
  if (/^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/.test(target)) {
    return `https://${target}`;
  }

  // Check if any alias is contained in the target
  for (const [alias, url] of Object.entries(SITE_ALIASES)) {
    if (lower.includes(alias)) return url;
  }

  // Last resort: treat as a search query on Google
  return `https://www.google.com/search?q=${encodeURIComponent(target)}`;
}

export { SITE_ALIASES, resolveUrl };
export default { parseCommand, executeCommand, SITE_ALIASES };
