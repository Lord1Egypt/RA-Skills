const API_BASE = "https://clawhub.ai/api/v1";
const PAGE_LIMIT = 50;
async function fetchPage(cursor) {
    const url = new URL(`${API_BASE}/skills`);
    url.searchParams.set("limit", String(PAGE_LIMIT));
    if (cursor)
        url.searchParams.set("cursor", cursor);
    const res = await fetch(url.toString(), {
        headers: { "User-Agent": "skill-surge-notifier/0.1.0" },
    });
    if (!res.ok) {
        throw new Error(`ClawHub API error: ${res.status} ${res.statusText}`);
    }
    return res.json();
}
export async function fetchTrending(maxPages = 4) {
    const all = [];
    let cursor = null;
    let page = 0;
    // Random delay 1-5min when called from scheduler (skip in direct runs)
    const isScheduled = process.env.SCHEDULED === "true";
    if (isScheduled) {
        const delay = Math.floor(Math.random() * 4 * 60 * 1000) + 60 * 1000;
        console.log(`Waiting ${Math.round(delay / 1000)}s before fetch...`);
        await new Promise((r) => setTimeout(r, delay));
    }
    do {
        const data = await fetchPage(cursor ?? undefined);
        all.push(...data.items);
        cursor = data.nextCursor;
        page++;
    } while (cursor && page < maxPages);
    // Sort by downloads descending
    return all.sort((a, b) => b.stats.downloads - a.stats.downloads);
}
// Run directly: npm run fetch
if (process.argv[1]?.endsWith("fetch_trending.ts")) {
    const skills = await fetchTrending();
    console.log(`\nTop 20 skills by downloads:\n`);
    skills.slice(0, 20).forEach((s, i) => {
        console.log(`${String(i + 1).padStart(2)}. ${s.displayName.padEnd(35)} ` +
            `DL: ${s.stats.downloads.toLocaleString().padStart(8)}  ` +
            `★ ${s.stats.stars}`);
    });
}
