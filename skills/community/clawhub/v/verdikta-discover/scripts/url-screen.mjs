// Screens for a connected agent that reads public pages. Pure functions: no network, files,
// environment or process access, so a host hook, an agent with exec and an offline scorer can all
// run the same checks. They reduce risk; they do not make a page trustworthy. A URL screen cannot
// see an injection inside a reputable page, and the content screen is advisory heuristics that
// will miss novel phrasing. Name resolution to a public address belongs to the host (see isPublicIp).

export const ALLOW = 'ALLOW', FLAG = 'FLAG', BLOCK = 'BLOCK';
const MAX_URL_LENGTH = 2048;

const INTERNAL_SUFFIXES = ['.localhost', '.local', '.internal', '.lan', '.home', '.home.arpa', '.corp', '.intranet', '.private', '.localdomain'];
const INTERNAL_NAMES = new Set(['localhost', 'metadata', 'instance-data', 'kubernetes', 'host.docker.internal']);
const SHORTENERS = new Set(['bit.ly', 't.co', 'tinyurl.com', 'goo.gl', 'ow.ly', 'is.gd', 'buff.ly', 'rebrand.ly', 'cutt.ly', 'shorturl.at', 't.ly', 'rb.gy', 'tiny.cc', 'lnkd.in', 'v.gd']);

// Values that look like secrets or exfiltrated data, wherever they appear in a composed URL.
const SECRET_VALUES = [
  /0x[0-9a-f]{40,}/i, /\b[0-9a-f]{32,}\b/i, /eyJ[\w-]{10,}\.[\w-]{10,}\./, /-----BEGIN/, /\bAKIA[0-9A-Z]{16}\b/, /\bsk-[A-Za-z0-9]{20,}/, /\bgh[pousr]_[A-Za-z0-9]{20,}/,
  /(?:\b[a-z]{3,8}[-+ ]){11,}[a-z]{3,8}\b/i,
];
// A long token that mixes upper case, lower case and digits looks like base64 or a random key; a slug of lowercase words does not.
const looksEncoded = token => token.length >= 40 && /^[A-Za-z0-9+/_=-]+$/.test(token) && /[a-z]/.test(token) && /[A-Z]/.test(token) && /[0-9]/.test(token);
const hasEncodedSegment = decoded => decoded.split(/[/?&;=]/).some(looksEncoded);
const SECRET_FILES = /(?:^|[/\\])(?:\.env(?!\.(?:example|sample|template)\b)|id_rsa|id_ed25519|[^/]*\.pem|[^/]*keystore[^/]*|wallet\.json|\.ssh|\.aws|\.npmrc|[^/]*-bot\.json)(?:$|[/\\.?])/i;
const SECRET_PARAMS = /(?:^|[?&;])(?:password|passwd|pwd|secret|token|api[_-]?key|apikey|key|auth|authorization|signature|sig|session|cookie|mnemonic|seed)=/i;

// A bare 40-hex path segment is a git commit on a code host, not a payload. Anywhere else, or at 64 hex, it stays suspect.
const CODE_HOSTS = new Set(['raw.githubusercontent.com', 'github.com', 'gitlab.com', 'bitbucket.org', 'codeberg.org']);
const withoutCommitSegments = (decoded, host) => CODE_HOSTS.has(host) ? decoded.split('/').filter(seg => !/^[0-9a-f]{40}$/i.test(seg)).join('/') : decoded;

const words = text => String(text).toLowerCase().normalize('NFKC').match(/[a-z0-9]+/g) || [];

function normalize(url) {
  try { const u = new URL(url); u.hash = ''; return u.href; } catch { return null; }
}

/** Task-text shingles (three consecutive words) with public vendor, product and entity names removed. */
function taskShingles(taskTexts, publicNames) {
  const names = new Set(publicNames.flatMap(words));
  const shingles = new Set();
  for (const text of taskTexts) {
    let run = [];
    const flush = () => { for (let i = 0; i + 3 <= run.length; i++) shingles.add(run.slice(i, i + 3).join(' ')); run = []; };
    for (const w of words(text)) { if (names.has(w)) flush(); else run.push(w); }
    flush();
  }
  return shingles;
}

/**
 * @param {string} input
 * @param {{ taskTexts?: string[], publicNames?: string[], provenance?: string[] }} context
 *   taskTexts: claim texts, field definitions and excerpts that must not appear in a URL.
 *   publicNames: vendor, product and entity names a URL may carry.
 *   provenance: URLs given verbatim by the owner, the request, a documented route, or a link in a page already fetched.
 */
export function screenUrl(input, { taskTexts = [], publicNames = [], provenance = [] } = {}) {
  const reasons = [];
  const block = (code, detail) => reasons.push({ code, severity: BLOCK, detail });
  const flag = (code, detail) => reasons.push({ code, severity: FLAG, detail });
  const done = () => ({ verdict: reasons.some(r => r.severity === BLOCK) ? BLOCK : reasons.length ? FLAG : ALLOW, reasons });

  if (typeof input !== 'string' || !input) { block('NOT_A_URL', 'empty or not a string'); return done(); }
  if (input.length > MAX_URL_LENGTH) block('TOO_LONG', `${input.length} characters`);
  if (/[\u0000-\u001f\u007f\u0085\u2028\u2029]/.test(input)) block('CONTROL_CHARS', 'control characters in the URL');
  let u;
  try { u = new URL(input); } catch { block('NOT_A_URL', 'does not parse'); return done(); }

  // Hard network checks: apply to every URL, including ones that came from a page.
  if (u.protocol !== 'https:') block('NOT_HTTPS', u.protocol);
  if (u.username || u.password) block('USERINFO', 'credentials in the URL');
  if (u.port && u.port !== '443') block('PORT', `port ${u.port}`);
  const host = u.hostname.toLowerCase().replace(/\.$/, '');
  if (host.startsWith('[') || /^\d{1,3}(?:\.\d{1,3}){3}$/.test(host)) block('IP_LITERAL', host);
  if (INTERNAL_NAMES.has(host) || INTERNAL_SUFFIXES.some(s => host.endsWith(s)) || (!host.includes('.') && !host.startsWith('['))) block('INTERNAL_HOST', host);
  if (SHORTENERS.has(host)) block('SHORTENER', `${host} hides the destination`);
  if (host.split('.').some(l => l.startsWith('xn--'))) flag('IDN_HOST', 'punycode hostname: check it is the site meant');

  // Composed-URL checks: a URL the owner, the request or a fetched page supplied verbatim is exempt.
  const verbatim = new Set(provenance.map(normalize).filter(Boolean)).has(normalize(input) ?? '');
  if (!verbatim) {
    let decoded = '';
    try { decoded = decodeURIComponent(u.pathname + u.search); } catch { block('BAD_ENCODING', 'malformed percent-encoding'); }
    if (/%[0-9a-f]{2}/i.test(decoded)) block('DOUBLE_ENCODING', 'percent-encoding survives one decode');
    if (u.search) block('QUERY_NOT_VERBATIM', 'a composed URL must not carry a query string');
    if (u.hash) flag('FRAGMENT', 'fragment is never sent to the server');
    const unsplit = withoutCommitSegments(decoded, host);
    if (SECRET_VALUES.some(re => re.test(unsplit)) || hasEncodedSegment(unsplit)) block('SECRET_SHAPED', 'a path or query segment looks like a secret or a data payload');
    if (SECRET_FILES.test(decoded) || SECRET_PARAMS.test(u.search)) block('SECRET_NAME', 'a credential-like file or parameter name');
    if (taskTexts.length) {
      const shingles = taskShingles(taskTexts, publicNames);
      const tokens = words(decoded);
      if (tokens.some((_, i) => i + 3 <= tokens.length && shingles.has(tokens.slice(i, i + 3).join(' ')))) block('TASK_TEXT_IN_URL', 'three or more consecutive words of task text');
      const flat = words(decoded).join(' ');
      if (taskTexts.some(t => { const w = words(t).join(' '); return w.length >= 25 && flat.includes(w.slice(0, 25)); })) block('TASK_TEXT_IN_URL', 'a run of task text');
    }
  }
  return done();
}

/** A fetch that ends on a different origin than it asked for makes that source unavailable. */
export function screenRedirect(requested, final) {
  const reasons = [];
  const parse = x => { try { return new URL(x); } catch { return null; } };
  const a = parse(requested), b = final == null || final === '' ? null : parse(final);
  if (!a) return { verdict: BLOCK, reasons: [{ code: 'NOT_A_URL', severity: BLOCK, detail: 'requested URL does not parse' }] };
  if (!b) return { verdict: FLAG, reasons: [{ code: 'FINAL_URL_UNKNOWN', severity: FLAG, detail: 'the tool did not report where the request ended' }] };
  if (a.origin !== b.origin) reasons.push({ code: 'CROSS_ORIGIN_REDIRECT', severity: BLOCK, detail: `${a.origin} -> ${b.origin}` });
  return { verdict: reasons.length ? BLOCK : ALLOW, reasons };
}

// ---- content screen -------------------------------------------------------------------------
const NEG = /\b(?:do not|don't|dont|never|must not|should not|shouldn't|avoid|without)\b[^.\n]{0,25}$/i;
const SECRET_NOUN = String.raw`(?:\.env(?!\.(?:example|sample|template)\b)|private keys?|seed phrases?|mnemonics?|ssh keys?|keystores?|credentials?|api[- ]?keys?|passwords?|secrets?|tokens?|wallet files?|config(?:uration)? files?|environment variables?)`;
const WHERE = String.raw`(?:your|the local|local|the workspace|workspace|working director(?:y|ies)|home director(?:y|ies)|current director(?:y|ies)|the agent'?s|this machine|the host)`;
const CATEGORIES = [
  { code: 'OVERRIDE', weight: 3, negatable: true, patterns: [
    /\b(?:ignore|disregard|forget|override|bypass|discard)\b[^.\n]{0,50}\b(?:previous|prior|above|earlier|all|any|every|your|the|these|those)\b[^.\n]{0,30}\b(?:instructions?|rules?|prompts?|guidelines?|directives?|constraints?|system prompt|programming|training|safety)\b/i,
    /\b(?:ignore|disregard|forget)\b[^.\n]{0,30}\b(?:your|the)\b[^.\n]{0,20}\b(?:owner|user|operator|principal)(?:'s|s')?\b/i,
    /\byour (?:task|instructions?|mission|goal) (?:has|have) (?:changed|been (?:updated|replaced))\b/i,
    /\b(?:forget|drop|abandon|stop) (?:about )?(?:the |your )?(?:task|job|work) (?:you were given|you are doing|at hand)\b|\bstop what you are doing\b/i,
    /\b(?:your|the (?:current|assigned|original|fact-?checking|verification|review)) task (?:is|has been) (?:suspended|cancell?ed|void|terminated|over)\b|\byour (?:new|real|actual) task is\b/i,
    /\byou are now (?:in |an? )?(?:developer|maintenance|debug|admin|god|jailbreak) mode\b|\bstay in character\b|\bwith no restrictions\b|\bfollows? any instruction (?:found|contained)\b/i,
    /\btreat (?:the )?(?:next|following|above) (?:paragraph|section|text|message) as (?:a |an )?(?:message|instruction|command|order)s? from (?:its|your|the) (?:operator|owner|developer|administrator|maintainers?)\b/i,
    /\b(?:print|output|reveal|show|repeat|dump|echo)\b[^.\n]{0,30}\b(?:your|the) (?:full |entire |complete |hidden |initial )?(?:system prompt|prompt|instructions|tool list|list of tools)\b/i,
    /<\|(?:im_start|im_end|endoftext|eot_id|start_header_id)\|>|\[\s*(?:system|developer|admin)(?: message| override| instruction)?[^\]]{0,40}\]/i,
    /\b(?:ai|llm)\s+(?:agents?|assistants?|tools?|models?|bots?)\s*[:,]\s*(?:stop|ignore|forget|output|print|reveal|send|read|run|do|you (?:must|should|will)|your)\b/i,
    /\b(?:new|updated|real|actual|revised) (?:instructions?|task|directive|system prompt)\s*:/i,
    /\bignor(?:a|e|ar|en)\b[^.\n]{0,40}\b(?:instrucciones|indicaciones|reglas)\b/i, /\bolvida (?:todas )?(?:tus|las) (?:instrucciones|reglas)\b/i,
    /\bignorier(?:e|en|t)?\b[^.\n]{0,40}\b(?:anweisungen|instruktionen|regeln|vorherigen)\b/i, /\bvergiss (?:alle|deine|die) (?:anweisungen|regeln|instruktionen)\b/i,
    /\bignore[sz]?\b[^.\n]{0,40}\b(?:instructions|consignes|directives)\b/i, /\boublie[sz]? (?:toutes )?(?:tes|vos|les) (?:instructions|consignes)\b/i] },
  { code: 'SECRET_ACCESS', weight: 3, negatable: true, patterns: [
    new RegExp(String.raw`\b(?:read|open|cat|print|reveal|show|send|paste|include|upload|share|output|exfiltrate|leak|post|copy|dump|attach|submit|forward|email)\b[^.\n]{0,60}\b${WHERE}\b[^.\n]{0,40}${SECRET_NOUN}`, 'i'),
    new RegExp(String.raw`\b(?:read|open|cat|print|reveal|send|paste|include|upload|output|exfiltrate|leak|dump)\b[^.\n]{0,30}(?:the )?(?:file )?(?:named |called )?\`?${SECRET_NOUN}\`?[^.\n]{0,60}\b(?:in|from|on) ${WHERE}`, 'i'),
    /\b(?:include|paste|put|append|add) (?:its|their|the|both|all) (?:full )?(?:contents?|outputs?)\b[^.\n]{0,40}\b(?:reply|response|answer|message|output)\b/i,
    /\b(?:cat|type|read|open|print|run)\b[^.\n]{0,25}(?:\.env(?!\.(?:example|sample|template)\b)|~\/\.ssh|id_rsa|\.aws\/credentials|\/etc\/passwd|\bkeystores?\b)[^.\n]{0,80}\b(?:paste|send|submit|upload|include|echo|reply|answer|post|contents?)\b/i,
    /\b(?:read|cat|open)\b[^.\n]{0,15}(?:~\/\.ssh|~\/\.aws|id_rsa|\.aws\/credentials|\/etc\/passwd)/i,
    /\b(?:send|submit|upload|forward|transmit|paste|post)\b[^.\n]{0,80}\b(?:credentials?|api keys?|passwords?|secrets?|conversation|working directory|system prompt|the user'?s (?:original )?(?:question|data)|your context|account email|owner'?s account)\b[^.\n]{0,80}\b(?:to|at|into|via)\b[^.\n]{0,60}https?:\/\/[^\s]+/i,
    /\b(?:fetch|visit|request|call|get|post|curl|open)\b[^.\n]{0,60}https?:\/\/[^\s]+[^.\n]{0,100}\b(?:your conversation|your context|(?:any )?(?:api )?keys? (?:in|from) your|credentials? (?:in|present in) your|the base64 of)\b/i,
    /\b(?:rotate|replace|verify)\b[^.\n]{0,60}\b(?:paste|enter|submit)\b[^.\n]{0,40}\b(?:api key|password|credentials?|token)\b[^.\n]{0,60}https?:\/\//i] },
  { code: 'CONCEAL', weight: 3, patterns: [
    /\b(?:do not|don't|dont|never|without)\b[^.\n]{0,30}\b(?:tell|inform|notify|alert|mention|disclose|reveal to|let)\b[^.\n]{0,25}\b(?:your |the |any )?(?:owner|user|operator|human|developer|principal|anyone)\b/i,
    /\b(?:keep|stay) (?:this|it|quiet|silent)\b[^.\n]{0,20}\b(?:secret|hidden|quiet|confidential|from)\b/i, /\bhidden from (?:the )?(?:user|owner|human)\b/i] },
  { code: 'EXFIL_URL', weight: 3, negatable: true, patterns: [
    /\b(?:fetch|visit|open|request|call|load|post|curl|navigate to|send (?:a |an )?(?:get |post )?(?:request )?to)\b[^.\n]{0,50}https?:\/\/[^\s)'"]+[?&][\w-]+=[^\s)'"]*(?:\{|<|\[|\$\(|%7[bB]|%3[cC])/i,
    /\b(?:append|attach|include|add|encode|embed|put)\b[^.\n]{0,60}\b(?:to|in|into|as)\b[^.\n]{0,25}\b(?:the )?(?:url|query string|query|link|request|parameter|path)\b/i] },
  { code: 'VALUE_TRANSFER', weight: 2, negatable: true, patterns: [
    /\b(?:send|transfer|pay|wire|deposit|approve|swap|withdraw)\b[^.\n]{0,40}\b(?:\d+(?:\.\d+)?\s*(?:eth|btc|usdc|usdt|sol|matic|dai|tokens?|coins?|usd|dollars?)|all (?:of )?(?:your |the )?(?:funds|eth|tokens|balance)|your (?:funds|balance|wallet))\b[^.\n]{0,60}(?:0x[0-9a-f]{40}|\bto\b)/i,
    /\b(?:send|transfer)\b[^.\n]{0,60}\bto\b[^.\n]{0,10}0x[0-9a-f]{40}\b[^.\n]{0,40}\b(?:unlock|access|continue|proceed|verify|complete)\b/i] },
  { code: 'AGENT_ADDRESSED', weight: 1, patterns: [
    /\b(?:attention|note|notice|message|instructions?|warning|tips?)\s+(?:to|for)\s+(?:any\s+|all\s+)?(?:ai|llm|language model|automated|assistants?|agents?|bots?|crawlers?|models?)\b/i,
    /\b(?:ai|llm|automated)\s+(?:agents?|assistants?|models?|bots?|systems?)\s+(?:reading|processing|visiting|crawling|scanning|summari[sz]ing|parsing|browsing)\b/i,
    /\b(?:the |an? |any )?(?:agent|assistant|bot|llm|model|crawler|automated reader|reviewing agent)s? (?:reading|processing|visiting|crawling|scanning|parsing|browsing) (?:this|it|the page|the document)\b[^.\n]{0,40}\b(?:should|must|needs? to|has to|is to)\b/i,
    /\bwhen an? (?:automated|ai|llm) (?:reader|agent|assistant|tool|system) (?:processes|reads|visits|parses)\b/i,
    /\bif you are (?:an? )?(?:ai|llm|language model|assistant|agent|bot|chatbot)\b/i, /\bdear (?:ai|assistant|agent|llm|model)\b/i, /\bas an? (?:ai|llm|assistant|agent)\b[^.\n]{0,40}\byou (?:must|should|will|need to)\b/i,
    /\bsystem(?: |-)?(?:prompt|message|override|instruction)s?\s*:/i, /\[\/?(?:system|inst|sys)\]|<\s*\/?\s*(?:system|instructions?|sys)\s*>/i,
    /\b(?:asistentes?|agentes?) de ia\b/i, /\bki-(?:assistenten|agenten)\b/i, /\bassistants? ia\b/i] },
  { code: 'MANDATED_OUTPUT', weight: 2, patterns: [
    /\b(?:your|the) (?:final )?(?:answer|response|report|verdict|summary)s? (?:must|should|will|has to)\b[^.\n]{0,60}\b(?:state|say|claim|conclude|report|declare)\b[^.\n]{0,40}\b(?:all|every|each)\b/i,
    /\bmust not (?:include|mention|add) (?:any )?(?:caveats|doubts|warnings|disclaimers|links|sources|reservations)\b/i,
    /\b(?:already|has already) (?:been )?(?:confirmed|verified|checked|approved)\b[^.\n]{0,40}\bevery claim\b/i] },
  { code: 'TOOL_HIJACK', weight: 1, negatable: true, patterns: [
    /\b(?:execute|run) (?:the following|this) (?:shell |bash |terminal )?(?:command|script|code)\b/i, /\bcurl\b[^|\n]{0,200}\|\s*(?:ba)?sh\b/i,
    /\b(?:call|invoke|use) the [\w.-]+ (?:tool|function)\b[^.\n]{0,60}\b(?:with|using|and send)\b/i] },
];
const HIDDEN_BLOCK = /<!--[\s\S]{0,600}?-->|<[^>]*style=["'][^"']*(?:display\s*:\s*none|visibility\s*:\s*hidden|font-size\s*:\s*0)[^"']*["'][^>]*>[\s\S]{0,400}?<\/[a-z]+>/gi;
const ZERO_WIDTH = /[\u200b-\u200f\u2060\ufeff\u202a-\u202e]/g;

function excerpt(text, index, length) { return text.slice(Math.max(0, index - 20), index + Math.min(length + 20, 140)).replace(/\s+/g, ' ').trim(); }

/**
 * Advisory screen for text fetched from a page. Never decides what is true, and a pass proves nothing.
 * @returns {{ severity: 'NONE'|'LOW'|'HIGH', score: number, flags: {code: string, excerpt: string}[] }}
 */
const LEET = { 0: 'o', 1: 'i', 3: 'e', 4: 'a', 5: 's', 7: 't', $: 's', '@': 'a' };
/** A second reading of the text with simple obfuscation undone: letter-spaced words and leetspeak. Only ever used to match patterns. */
function deobfuscate(text) {
  return text
    .replace(/\b(?:[a-z]\s){5,}[a-z]\b/gi, m => m.replace(/\s/g, ''))
    .replace(/(?<![\w.])(?=[\w$@]*[a-z])(?=[\w$@]*[013457$@])[\w$@]{3,}(?![\w.])/gi, tok => /\d\.\d|^[a-z]+\d+$|^[a-z]\d/i.test(tok) ? tok : tok.replace(/[013457$@]/g, c => LEET[c]));
}

export function screenContent(input) {
  const raw = typeof input === 'string' ? input : '';
  const zeroWidth = (raw.match(ZERO_WIDTH) || []).length;
  const text = raw.replace(ZERO_WIDTH, '').normalize('NFKC');
  // One flag per category per body of text: the first matching pattern that is not advice to a human.
  const scan = (body) => {
    const hits = new Map();
    for (const cat of CATEGORIES) for (const re of cat.patterns) {
      const m = re.exec(body);
      if (!m) continue;
      // "Do not share your API key" is advice to a human, not an instruction to the agent. (For CONCEAL the negation is the attack.)
      if (cat.negatable && NEG.test(body.slice(Math.max(0, m.index - 30), m.index + 12))) continue;
      hits.set(cat.code, { code: cat.code, weight: cat.weight, excerpt: excerpt(body, m.index, m[0].length) });
      break;
    }
    return hits;
  };
  const found = scan(text);
  const plain = deobfuscate(text);
  if (plain !== text) for (const [code, flag] of scan(plain)) if (!found.has(code)) found.set(code, { ...flag, code, excerpt: `(deobfuscated) ${flag.excerpt}` });
  // An instruction inside a comment or a hidden element is worse than the same words in the open.
  for (const hidden of text.match(HIDDEN_BLOCK) || []) {
    const inner = scan(hidden);
    if (!inner.size) continue;
    for (const [code, flag] of inner) if (!found.has(code)) found.set(code, flag);
    if (!found.has('HIDDEN_INSTRUCTION')) found.set('HIDDEN_INSTRUCTION', { code: 'HIDDEN_INSTRUCTION', weight: 2, excerpt: excerpt(hidden, 0, 120) });
  }
  if (zeroWidth >= 3) found.set('ZERO_WIDTH_TEXT', { code: 'ZERO_WIDTH_TEXT', weight: 1, excerpt: `${zeroWidth} zero-width or direction-control characters` });
  const flags = [...found.values()];
  const score = flags.reduce((n, f) => n + f.weight, 0);
  const severity = flags.some(f => f.weight >= 3) || score >= 3 ? 'HIGH' : score >= 1 ? 'LOW' : 'NONE';
  return { severity, score, flags: flags.map(({ code, excerpt: e }) => ({ code, excerpt: e })) };
}

// ---- host helper ------------------------------------------------------------------------------
/** True when an IP address a name resolved to is publicly routable. A host runs this at connect time; the screens above cannot. */
export function isPublicIp(ip) {
  const s = String(ip).trim().toLowerCase();
  const v4 = s.match(/^(?:::ffff:)?(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/);
  if (v4) {
    const [a, b] = v4.slice(1).map(Number);
    if ([a, ...v4.slice(2).map(Number)].some(n => n > 255) || b > 255) return false;
    return !(a === 0 || a === 10 || a === 127 || (a === 100 && b >= 64 && b <= 127) || (a === 169 && b === 254) || (a === 172 && b >= 16 && b <= 31)
      || (a === 192 && b === 168) || (a === 192 && b === 0) || (a === 198 && (b === 18 || b === 19)) || a >= 224);
  }
  if (s.includes(':')) {
    if (s === '::' || s === '::1') return false;
    const first = parseInt(s.split(':')[0] || '0', 16);
    return !((first & 0xfe00) === 0xfc00 || (first & 0xffc0) === 0xfe80 || (first & 0xff00) === 0xff00 || (first & 0xffc0) === 0xfec0);
  }
  return false;
}
