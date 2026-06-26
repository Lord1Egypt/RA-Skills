import { discoverSite } from "./crawl-runner.mjs";

export async function mapSite(entryUrls, options = {}) {
  const nodes = [];
  const edges = [];

  const discovery = await discoverSite(entryUrls, {
    ...options,
    maxChars: 4000,
    onVisit: async ({ page }) => {
      nodes.push({
        url: page.url,
        title: page.title,
        depth: page.depth,
        discoveredFrom: page.discoveredFrom,
      });
    },
    onDiscover: async ({ from, to }) => {
      edges.push({ from, to });
    },
  });

  return {
    nodes,
    edges,
    failed: discovery.failed,
    meta: {
      entryUrls: discovery.entryUrls,
      visitedPages: nodes.length,
      maxPagesReached: discovery.maxPagesReached,
    },
  };
}
