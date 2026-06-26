import { readFileSync, writeFileSync, mkdirSync, existsSync } from "fs";
import { resolve } from "path";
const BASE = process.env.SURGE_DIR ?? resolve(process.env.HOME ?? "~", ".skill-surge-notifier");
const PROFILE_PATH = resolve(BASE, "profile.json");
export function loadProfile() {
    if (!existsSync(PROFILE_PATH))
        return null;
    return JSON.parse(readFileSync(PROFILE_PATH, "utf8"));
}
export function saveProfile(profile) {
    mkdirSync(BASE, { recursive: true });
    writeFileSync(PROFILE_PATH, JSON.stringify(profile, null, 2));
}
export function extractKeywords(description) {
    // Strip stopwords, return meaningful tokens
    const stopwords = new Set([
        "a", "an", "the", "and", "or", "for", "to", "of", "in", "on", "with",
        "is", "it", "my", "me", "i", "that", "this", "as", "at", "be", "by",
        "do", "has", "have", "not", "are", "was", "were", "but", "so", "if",
        "can", "will", "your", "their", "its", "our", "we", "he", "she", "they"
    ]);
    return [...new Set(description
            .toLowerCase()
            .replace(/[^a-z0-9\s]/g, " ")
            .split(/\s+/)
            .filter(w => w.length > 2 && !stopwords.has(w)))];
}
export function scoreRelevance(skillName, skillSummary, skillTags, profile) {
    const haystack = [skillName, skillSummary, ...skillTags]
        .join(" ")
        .toLowerCase();
    const matches = [];
    for (const keyword of profile.keywords) {
        if (haystack.includes(keyword.toLowerCase())) {
            matches.push(keyword);
        }
    }
    // Also match words from the description itself
    const descKeywords = extractKeywords(profile.description);
    for (const word of descKeywords) {
        if (!matches.includes(word) && haystack.includes(word)) {
            matches.push(word);
        }
    }
    const totalKeywords = new Set([...profile.keywords, ...descKeywords]).size;
    const score = totalKeywords === 0 ? 5 : Math.min(10, Math.round((matches.length / Math.max(totalKeywords, 1)) * 20));
    return { score, matches: [...new Set(matches)] };
}
