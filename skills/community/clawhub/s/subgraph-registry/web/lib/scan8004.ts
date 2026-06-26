// 8004scan link helper.
//
// The Dune `agent_link` column currently carries the composite agent_id
// (chain:contract:token_id), which we used to think was the canonical URL
// path. It isn't — 8004scan's actual URL is `/agents/<chain-slug>/<token>`.
//
// We fix it on the way out so the live dashboard works even without a fresh
// Dune re-run. The seed script also writes the correct format going forward.

const CHAIN_SLUG: Record<number, string> = {
  1: "ethereum",
  8453: "base",
  42161: "arbitrum",
  10: "optimism",
  56: "bsc",
  137: "polygon",
  42220: "celo",
  130: "unichain",
  1923: "swellchain",
  2741: "abstract",
  5042002: "ronin",
  84532: "base-sepolia",
  11155111: "sepolia",
};

const COMPOSITE = /\/agent[s]?\/(\d+):0x[0-9a-fA-F]+:(\d+)$/;

export function fixScan8004Url(url: string): string {
  if (!url) return url;
  // Already the canonical /agents/<slug>/<id> form? Leave alone.
  if (/\/agents\/[a-z][a-z0-9-]+\/\d+(?:$|\?)/.test(url)) return url;
  const m = COMPOSITE.exec(url);
  if (!m) return url;
  const chainId = Number(m[1]);
  const tokenId = m[2];
  const slug = CHAIN_SLUG[chainId];
  if (!slug) return url; // unknown chain — keep original (will still 404, but at least no garbage)
  return `https://8004scan.io/agents/${slug}/${tokenId}`;
}

export function scan8004UrlFromAgentId(agentIdComposite: string | undefined | null): string | null {
  if (!agentIdComposite) return null;
  const m = /^(\d+):0x[0-9a-fA-F]+:(\d+)$/.exec(agentIdComposite);
  if (!m) return null;
  const slug = CHAIN_SLUG[Number(m[1])];
  if (!slug) return null;
  return `https://8004scan.io/agents/${slug}/${m[2]}`;
}
