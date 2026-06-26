#!/usr/bin/env node
/**
 * cluster-second-brain.js
 * Reads second-brain-atoms.json, calls your local OpenClaw gateway LLM,
 * writes second-brain-clusters.json
 *
 * Usage: node scripts/cluster-second-brain.js
 */

const fs = require('fs');
const path = require('path');

const ATOMS_FILE = process.env.SBV_ATOMS_FILE || path.join(__dirname, '../data/second-brain-atoms.json');
const OUT_FILE   = process.env.SBV_CLUSTERS_FILE || path.join(__dirname, '../data/second-brain-clusters.json');
const MODEL = process.env.SBV_MODEL || 'openclaw:main';

// Reads gateway config from credentials file (mirrors Ghost Pro credential pattern)
const CREDS_FILE = path.join(
  process.env.HOME || process.env.USERPROFILE || '~',
  '.openclaw', 'credentials', 'openclaw-gateway.json'
);

function loadGatewayCreds() {
  if (!fs.existsSync(CREDS_FILE)) {
    console.error(
      `[SBV] Missing credentials file: ${CREDS_FILE}\n` +
      'Create it with: { "host": "127.0.0.1", "port": 18789, "key": "<your-gateway-key>" }'
    );
    process.exit(1);
  }
  const creds = JSON.parse(fs.readFileSync(CREDS_FILE, 'utf8'));
  if (!creds.key) {
    console.error('[SBV] openclaw-gateway.json must include a "key" field.');
    process.exit(1);
  }
  const host = creds.host || '127.0.0.1';
  if (host !== '127.0.0.1' && host !== 'localhost') {
    console.warn(
      `[SBV] Warning: gateway host is "${host}". ` +
      'This will send your atom corpus to a remote host. ' +
      'Set host to 127.0.0.1 in openclaw-gateway.json to keep data local.'
    );
  }
  return { host, port: creds.port || 18789, key: creds.key };
}

// All LLM calls go to the configured local gateway — no external API calls
function callLLM(gatewayKey, gatewayHost, gatewayPort, prompt) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({
      model: MODEL,
      max_tokens: 4096,
      temperature: 0.3,
      messages: [{ role: 'user', content: prompt }],
    });

    const req = require('http').request({
      hostname: gatewayHost,
      port: gatewayPort,
      path: '/v1/chat/completions',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${gatewayKey}`,
        'Content-Length': Buffer.byteLength(body),
      },
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          if (parsed.error) return reject(new Error(JSON.stringify(parsed.error)));
          const text = parsed.choices?.[0]?.message?.content ?? '';
          resolve(text);
        } catch (e) {
          reject(new Error('Failed to parse response: ' + data.slice(0, 200)));
        }
      });
    });

    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

async function main() {
  if (!fs.existsSync(ATOMS_FILE)) {
    console.error('Run build-second-brain.js first');
    process.exit(1);
  }

  const { host: GATEWAY_HOST, port: GATEWAY_PORT, key: gatewayKey } = loadGatewayCreds();

  const { atoms, atomCount } = JSON.parse(fs.readFileSync(ATOMS_FILE, 'utf8'));
  // log(`Clustering ${atomCount} atoms…`);

  const corpus = atoms.map(a =>
    `[${a.id}] (${a.date?.slice(0, 10) ?? '?'}) ${a.raw}`
  ).join('\n');

  const prompt = `You are a cognitive analyst reading the unfiltered thought stream of a single person over an extended period of time. Your input is a corpus of raw personal notes — voice to text, incomplete, misspelled, joke-form, fragment-form, action-item-form. Treat low fidelity as intentional. The roughness is not a bug. It is what unguarded thinking looks like.

Your job is not to categorize what was said. It is to identify what the person is becoming.

WHAT YOU ARE LOOKING FOR

Beneath every note is a layer of intent. A joke about AI models and computational overhead is not about overhead — it is a probe into the transactional nature of machine intelligence. Read the joke. Then ask: what is the person actually working out?

Look for:
- Strategic direction: what is this person building toward, even when they don't say it directly?
- Recurring preoccupations: what questions keep returning in different forms, different domains, different registers?
- Underlying tensions: where is the person arguing with themselves across multiple notes?
- Aesthetic commitments: what do the design observations, humor choices, and word selections reveal?

HOW TO CLUSTER

Group atoms by affinity of intent — not surface similarity of words. Two atoms belong in the same cluster if they are reaching toward the same underlying question, even if one is a joke about LLMs and the other is a note about Simone Weil.

Do not impose categories onto the data. Let the categories emerge from the mass and direction of the atoms.

CLUSTER REQUIREMENTS
- Minimum 3 atoms to form a cluster
- Minimum 3, maximum 10 clusters total — determined by the data
- A cluster that was strong months ago and gone quiet is FADING, not absent

FOR EACH CLUSTER use exactly these fields:
- id: stable kebab-case string
- name: sharp specific name capturing underlying drive, NOT generic domain labels
- insight: one sentence — what does this pattern reveal about how this person thinks?
- atom_ids: array of atom id strings
- confidence: number 0.0 to 1.0
- status: string, one of: ESTABLISHED, FORMING, FADING
- time_spread: integer, number of distinct calendar weeks this theme spans

TOP LEVEL OUTPUT FIELDS (all required):
- clusters: array of cluster objects
- emerging_signals: array of atom id strings (atoms with distinct intent but not enough mass for a cluster)
- tensions: array of objects with fields: name (string), atom_ids (array), description (string)
- absences: array of strings naming themes notably absent given the overall profile

RULES:
- Do NOT name a cluster after a domain: not Technology, Business, Humor, Writing
- Do NOT group by keyword overlap — intent makes a cluster
- Do NOT invent themes the data doesn't support
- Output ONLY valid JSON, no prose, no markdown fences

CORPUS:
${corpus}`;

  try {
    const response = await callLLM(gatewayKey, GATEWAY_HOST, GATEWAY_PORT, prompt);
    
    // Extract JSON
    const jsonMatch = response.match(/\{[\s\S]*\}/);
    if (!jsonMatch) throw new Error('No JSON found in response');
    
    const clusters = JSON.parse(jsonMatch[0]);
    
    const output = {
      generated: new Date().toISOString(),
      atomCount,
      ...clusters,
    };

    fs.writeFileSync(OUT_FILE, JSON.stringify(output, null, 2));
    // log(`✓ ${clusters.clusters?.length ?? 0} clusters written to ${OUT_FILE}`);
    clusters.clusters?.forEach(c => {
      // log(`  [${c.status}] ${c.name} — ${c.atom_ids?.length} atoms, ${c.time_spread}w spread`);
    });
    // log(`  ${clusters.emerging_signals?.length ?? 0} emerging signals`);
    // log(`  ${clusters.tensions?.length ?? 0} tensions`);
  } catch (e) {
    console.error('Clustering failed:', e.message);
    process.exit(1);
  }
}

main();
