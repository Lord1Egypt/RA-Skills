import { pathToFileURL } from 'node:url';

export async function search(resource, input, options = {}) {
  if (!['brands', 'creators', 'media'].includes(resource)) throw new Error('Use brands, creators, or media');
  if (!input || Array.isArray(input) || typeof input !== 'object') throw new Error('Input must be a JSON object');
  const allowed = resource === 'media' ? ['query','accountId','channel','status','sortBy','limit','offset'] : ['query','names','igUsername','tiktokUsername','limit','offset'];
  if (Object.keys(input).some(key => !allowed.includes(key))) throw new Error('Unsupported search field');
  const body = { ...input, limit: input.limit ?? 10, offset: input.offset ?? 0 };
  if (!Number.isInteger(body.limit) || body.limit < 1 || body.limit > 100) throw new Error('Limit must be 1–100');
  if (!Number.isInteger(body.offset) || body.offset < 0) throw new Error('Offset must be a nonnegative integer');
  const key = options.apiKey ?? process.env.SPYGLASS_API_KEY;
  if (!key?.trim()) throw new Error('SPYGLASS_API_KEY is required');
  const response = await (options.fetch ?? fetch)(`https://api.spyglass.so/v2/${resource}`, {
    method: 'POST', headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
    body: JSON.stringify(body), signal: AbortSignal.timeout(60000), redirect: 'error',
  });
  if (!response.ok) throw new Error(`Spyglass request failed (${response.status})`);
  return response.json();
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try {
    console.log(JSON.stringify(await search(process.argv[2], JSON.parse(process.argv[3] ?? '{}')), null, 2));
  } catch (error) {
    console.error(error instanceof Error ? error.message : 'Spyglass request failed');
    process.exitCode = 1;
  }
}
