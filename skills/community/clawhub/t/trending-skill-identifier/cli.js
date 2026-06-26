#!/usr/bin/env node
import { loadState, loadConfig, saveConfig } from "./state.js";
import { runCheck } from "./surge_check.js";
import { fetchTrending } from "./fetch_trending.js";
import { loadProfile, saveProfile } from "./profile.js";
const [, , command, ...args] = process.argv;
async function cmdStatus() {
    const state = loadState();
    const config = loadConfig();
    if (!state.lastChecked) {
        console.log("[surge-notifier] No checks run yet. Run: skill-surge-notifier check");
        return;
    }
    const top5 = Object.values(state.skills)
        .sort((a, b) => b.downloads - a.downloads)
        .slice(0, 5);
    console.log(`\n[surge-notifier] STATUS`);
    console.log(`  Last check:     ${new Date(state.lastChecked).toLocaleString()}`);
    console.log(`  Skills tracked: ${Object.keys(state.skills).length}`);
    console.log(`  Interval:       every ${config.intervalHours}h`);
    console.log(`  Thresholds:     DL>${config.thresholds.minDownloads.toLocaleString()}  ★>${config.thresholds.minStars}  growth>${config.thresholds.minGrowthPct}%`);
    console.log(`  Top movers:     ${config.topMovers.enabled ? `on (top ${config.topMovers.count})` : "off"}`);
    console.log(`\n  Top 5 by downloads:`);
    top5.forEach((s, i) => console.log(`    ${i + 1}. ${s.displayName.padEnd(35)} DL: ${s.downloads.toLocaleString().padStart(8)}  ★ ${s.stars}`));
}
async function cmdConfig(args) {
    const config = loadConfig();
    for (const arg of args) {
        const [key, val] = arg.split("=");
        switch (key) {
            case "interval":
                config.intervalHours = parseInt(val);
                break;
            case "downloads":
                config.thresholds.minDownloads = parseInt(val);
                break;
            case "stars":
                config.thresholds.minStars = parseInt(val);
                break;
            case "growth":
                config.thresholds.minGrowthPct = parseInt(val);
                break;
            case "movers":
                config.topMovers.count = parseInt(val);
                break;
            case "movers-off":
                config.topMovers.enabled = false;
                break;
            case "movers-on":
                config.topMovers.enabled = true;
                break;
            default: console.warn(`Unknown config key: ${key}`);
        }
    }
    saveConfig(config);
    console.log("[surge-notifier] Config saved.");
}
async function cmdFetch() {
    const skills = await fetchTrending();
    console.log(`\nTop 20 skills by downloads:\n`);
    skills.slice(0, 20).forEach((s, i) => {
        console.log(`${String(i + 1).padStart(2)}. ${s.displayName.padEnd(35)} ` +
            `DL: ${s.stats.downloads.toLocaleString().padStart(8)}  ★ ${s.stats.stars}`);
    });
}
async function cmdProfile(args) {
    const subcommand = args[0];
    if (subcommand === "set") {
        const description = args[1] ?? "";
        const keywords = args[2] ? args[2].split(",").map(k => k.trim()) : [];
        if (!description) {
            console.log(`Usage: skill-surge-notifier profile set "your agent description" "keyword1,keyword2"`);
            return;
        }
        saveProfile({ description, keywords, installedSkills: [] });
        console.log(`[surge-notifier] Profile saved!`);
        console.log(`  Description: ${description}`);
        console.log(`  Keywords:    ${keywords.length ? keywords.join(", ") : "(auto-extracted from description)"}`);
    }
    else {
        const profile = loadProfile();
        if (!profile) {
            console.log(`[surge-notifier] No profile set.`);
            console.log(`  Run: skill-surge-notifier profile set "your agent description" "keyword1,keyword2"`);
        }
        else {
            console.log(`\n[surge-notifier] PROFILE`);
            console.log(`  Description: ${profile.description}`);
            console.log(`  Keywords:    ${profile.keywords.join(", ") || "(none)"}`);
            console.log(`  Installed:   ${profile.installedSkills.join(", ") || "(none)"}`);
        }
    }
}
switch (command) {
    case "fetch":
        await cmdFetch();
        break;
    case "check":
    case "manual":
        await runCheck();
        break;
    case "status":
        await cmdStatus();
        break;
    case "profile":
        await cmdProfile(args);
        break;
    case "config":
        await cmdConfig(args);
        break;
    default:
        console.log(`Usage: skill-surge-notifier <command>\n`);
        console.log(`  fetch                          show top 20 trending skills`);
        console.log(`  check                          run surge detection and update state`);
        console.log(`  status                         last check, top 5, current config`);
        console.log(`  profile                        show current profile`);
        console.log(`  profile set "desc" "kw1,kw2"  set profile for relevance scoring`);
        console.log(`  config growth=30 downloads=50000 stars=200 movers=5 movers-on|movers-off`);
}
