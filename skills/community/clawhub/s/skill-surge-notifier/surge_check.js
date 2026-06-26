import { fetchTrending } from "./fetch_trending.js";
import { loadState, saveState, loadConfig } from "./state.js";
import { loadProfile, scoreRelevance } from "./profile.js";
function toTracked(skill) {
    return {
        slug: skill.slug,
        displayName: skill.displayName,
        summary: skill.summary,
        downloads: skill.stats.downloads,
        stars: skill.stats.stars,
        versions: skill.stats.versions,
        checkedAt: new Date().toISOString(),
    };
}
function detectSurges(current, prevState) {
    const { minDownloads, minStars, minGrowthPct, top10Alert } = loadConfig().thresholds;
    const profile = loadProfile();
    const alerts = [];
    current.forEach((skill, i) => {
        const prev = prevState.skills[skill.slug] ?? null;
        const reasons = [];
        const growthPct = prev && prev.downloads > 0
            ? ((skill.downloads - prev.downloads) / prev.downloads) * 100
            : null;
        if (growthPct !== null && growthPct >= minGrowthPct)
            reasons.push(`+${growthPct.toFixed(1)}% download growth`);
        if (skill.downloads >= minDownloads)
            reasons.push(`${skill.downloads.toLocaleString()} total downloads`);
        if (skill.stars >= minStars)
            reasons.push(`${skill.stars} stars`);
        if (top10Alert && i < 10 && !prev)
            reasons.push(`new in top 10`);
        if (reasons.length > 0) {
            const relevance = profile
                ? scoreRelevance(skill.displayName, skill.summary, [], profile)
                : null;
            alerts.push({ skill, prev, growthPct, reason: reasons, relevance });
        }
    });
    if (profile) {
        alerts.sort((a, b) => (b.relevance?.score ?? 0) - (a.relevance?.score ?? 0));
    }
    return alerts;
}
function getTopMovers(current, prevState, count) {
    const movers = [];
    for (const skill of current) {
        const prev = prevState.skills[skill.slug];
        if (!prev || prev.downloads === 0)
            continue;
        const delta = skill.downloads - prev.downloads;
        if (delta <= 0)
            continue;
        const growthPct = (delta / prev.downloads) * 100;
        movers.push({ skill, delta, growthPct });
    }
    return movers
        .sort((a, b) => b.delta - a.delta)
        .slice(0, count);
}
function relevanceBar(score) {
    const filled = Math.round(score / 2);
    return "█".repeat(filled) + "░".repeat(5 - filled) + ` ${score}/10`;
}
function formatSurgeAlert(alert) {
    const { skill, growthPct, relevance } = alert;
    const growth = growthPct !== null ? ` (+${growthPct.toFixed(1)}%)` : "";
    const relevanceLine = relevance
        ? `   Relevance: ${relevanceBar(relevance.score)}${relevance.matches.length ? `  [${relevance.matches.join(", ")}]` : ""}\n`
        : "";
    return (`\n SURGE: ${skill.displayName}\n` +
        `   ${skill.summary}\n` +
        relevanceLine +
        `   Downloads: ${skill.downloads.toLocaleString()}${growth}  |  Stars: ${skill.stars}\n` +
        `   Why: ${alert.reason.join(", ")}\n` +
        `   Install: clawhub install ${skill.slug}\n`);
}
function formatTopMovers(movers) {
    if (movers.length === 0)
        return "  (no movement data yet — run check again after some time)\n";
    return movers
        .map((m, i) => `  ${i + 1}. ${m.skill.displayName.padEnd(35)} ` +
        `+${m.delta.toLocaleString().padStart(6)} DL  ` +
        `(+${m.growthPct.toFixed(1)}%)`)
        .join("\n") + "\n";
}
export async function runCheck() {
    console.log(`[surge-notifier] Fetching from ClawHub...`);
    let skills;
    try {
        skills = await fetchTrending();
    }
    catch (err) {
        console.error(`[surge-notifier] Fetch failed:`, err);
        return [];
    }
    const config = loadConfig();
    const prevState = loadState();
    const current = skills.map(toTracked);
    const alerts = detectSurges(current, prevState);
    const profile = loadProfile();
    // Top movers
    if (config.topMovers.enabled) {
        const movers = getTopMovers(current, prevState, config.topMovers.count);
        console.log(`\nTop ${config.topMovers.count} movers since last check:`);
        console.log(formatTopMovers(movers));
    }
    // Surge alerts
    if (alerts.length === 0) {
        console.log(`No surge thresholds crossed.`);
    }
    else {
        const label = profile
            ? `${alerts.length} surge(s) — ${alerts.filter(a => (a.relevance?.score ?? 0) >= 5).length} match your profile`
            : `${alerts.length} surge(s) detected`;
        console.log(`${label}\n`);
        alerts.forEach((a) => console.log(formatSurgeAlert(a)));
    }
    saveState({
        lastChecked: new Date().toISOString(),
        skills: Object.fromEntries(current.map((s) => [s.slug, s])),
    });
    return alerts;
}
// Direct run: npm run check
if (process.argv[1]?.endsWith("surge_check.ts")) {
    await runCheck();
}
