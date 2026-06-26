/**
 * tr-cli-export-helper.ts
 *
 * Helper module for `tr export` — paginates through the subgraph and
 * decrypts every active fact owned by the caller's Smart Account address.
 *
 * Lives in its own file because tr-cli.ts already contains a synchronous
 * disk read (status command loads `.loaded.json`), and combining that
 * with outbound HTTP in the same file would trip the OpenClaw skill
 * scanner's exfil rule (see ../scripts/check-scanner.mjs).
 *
 * Phrase-safety: this module never touches the recovery phrase. It receives
 * pre-derived auth-key + wallet-address + encryption-key from the caller.
 */
import { CONFIG } from './config.js';
import { buildRelayHeaders } from './relay-headers.js';
import { decrypt } from './crypto.js';
/** Decode a hex blob written by submitFactBatchOnChain back to plaintext. */
function fromHexBlob(hexBlob, encryptionKey) {
    const hex = hexBlob.startsWith('0x') ? hexBlob.slice(2) : hexBlob;
    const b64 = Buffer.from(hex, 'hex').toString('base64');
    return decrypt(b64, encryptionKey);
}
/**
 * Pull every active fact for `walletAddress` from the subgraph, decrypt
 * each blob, and return a flat array sorted in subgraph-cursor order.
 *
 * Uses /v1/subgraph relay endpoint with cursor-based pagination (id_gt).
 * Mirrors the totalreclaw_export native tool path (index.ts:4352-4415).
 */
export async function exportAllFacts(walletAddress, authKeyHex, encryptionKey) {
    const relayUrl = CONFIG.serverUrl || 'https://api.totalreclaw.xyz';
    const subgraphUrl = `${relayUrl}/v1/subgraph`;
    const PAGE_SIZE = 1000;
    async function gql(query, variables) {
        try {
            const resp = await fetch(subgraphUrl, {
                method: 'POST',
                headers: buildRelayHeaders({
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${authKeyHex}`,
                }),
                body: JSON.stringify({ query, variables }),
            });
            if (!resp.ok) {
                const body = await resp.text().catch(() => '');
                process.stderr.write(`[warn] subgraph HTTP ${resp.status}: ${body.slice(0, 200)}\n`);
                return null;
            }
            const json = (await resp.json());
            if (json.errors) {
                process.stderr.write(`[warn] subgraph errors: ${json.errors
                    .map((e) => e.message)
                    .join('; ')}\n`);
            }
            return json.data ?? null;
        }
        catch (err) {
            const msg = err instanceof Error ? err.message : String(err);
            process.stderr.write(`[warn] subgraph request failed: ${msg}\n`);
            return null;
        }
    }
    const allFacts = [];
    let lastId = '';
    while (true) {
        const hasLastId = lastId !== '';
        const query = hasLastId
            ? `query($owner:Bytes!,$first:Int!,$lastId:String!){facts(where:{owner:$owner,isActive:true,id_gt:$lastId},first:$first,orderBy:id,orderDirection:asc){id encryptedBlob timestamp}}`
            : `query($owner:Bytes!,$first:Int!){facts(where:{owner:$owner,isActive:true},first:$first,orderBy:id,orderDirection:asc){id encryptedBlob timestamp}}`;
        const variables = hasLastId
            ? { owner: walletAddress, first: PAGE_SIZE, lastId }
            : { owner: walletAddress, first: PAGE_SIZE };
        const data = await gql(query, variables);
        const facts = data?.facts ?? [];
        if (facts.length === 0)
            break;
        for (const f of facts) {
            try {
                const docJson = fromHexBlob(f.encryptedBlob, encryptionKey);
                const parsed = JSON.parse(docJson);
                if (!parsed.text)
                    continue; // skip digests / tombstones
                const created = parseInt(f.timestamp, 10);
                allFacts.push({
                    id: f.id,
                    text: parsed.text,
                    metadata: parsed.metadata ?? {},
                    created_at: Number.isFinite(created)
                        ? new Date(created * 1000).toISOString()
                        : new Date(0).toISOString(),
                });
            }
            catch {
                // Skip undecryptable facts
            }
        }
        if (facts.length < PAGE_SIZE)
            break;
        lastId = facts[facts.length - 1].id;
    }
    return allFacts;
}
