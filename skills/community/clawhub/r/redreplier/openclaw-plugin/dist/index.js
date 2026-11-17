import { Type } from "@sinclair/typebox";
import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import { jsonResult } from "openclaw/plugin-sdk/tool-results";
import { callApi, readConfig } from "./api.js";
const MentionStatus = Type.Union([
    Type.Literal("NEW"),
    Type.Literal("APPROVED"),
    Type.Literal("REJECTED"),
]);
const MentionSource = Type.Union([
    Type.Literal("REDDIT_POST"),
    Type.Literal("REDDIT_COMMENT"),
    Type.Literal("TWITTER"),
    Type.Literal("BLUESKY"),
    Type.Literal("HACKERNEWS"),
    Type.Literal("FACEBOOK"),
    Type.Literal("FACEBOOK_GROUP"),
]);
const RelevanceBucket = Type.Union([
    Type.Literal("VERY_LOW"),
    Type.Literal("LOW"),
    Type.Literal("MEDIUM"),
    Type.Literal("HIGH"),
    Type.Literal("VERY_HIGH"),
]);
export default definePluginEntry({
    id: "redreplier",
    name: "RedReplier",
    description: "Monitor Reddit, Hacker News, X, Bluesky and Facebook for keyword mentions of your product, AI-scored 0-100 for relevance.",
    register(api) {
        const cfg = () => readConfig(api);
        api.registerTool({
            name: "redreplier_websites",
            label: "RedReplier: list monitored websites",
            description: "List the websites this account monitors, each with its keywords (id, value, status: PENDING, ACTIVE, DISABLED, SUSPENDED). Call this first: redreplier_add_keywords needs a website id and redreplier_mentions filters by one. Reading changes nothing. Only ACTIVE keywords match new mentions, so a long PENDING list explains a quiet inbox; PENDING keywords move up when a slot frees up, and clearing the rest can cost a plan upgrade, which this plugin deliberately cannot trigger.",
            parameters: Type.Object({}),
            async execute(_toolCallId, _params, signal) {
                return jsonResult(await callApi(cfg(), "GET", "/websites", { signal }));
            },
        });
        api.registerTool({
            name: "redreplier_mentions",
            label: "RedReplier: list mentions",
            description: "List matched mentions across Reddit, Hacker News, X, Bluesky and Facebook, each AI-scored 0-100 with source, matched keyword, status, content, and any generated relevanceReason and aiReplySuggestion. Two defaults hide rows: REJECTED mentions are excluded unless statuses names them, and mentions below the website's minimum score (30 by default) are hidden unless includeLowRelevance is true, even when scoreBuckets asks for LOW or VERY_LOW. Returns { mentions, total, limit, offset }; page with offset while offset < total. Sort defaults to RELEVANCE; use RECENT when the question is about timing. from/to filter on ingestion time, not publish time. subreddit holds the subreddit for Reddit sources and the group id for FACEBOOK_GROUP; url can be null for FACEBOOK_GROUP. Use redreplier_explain_mention for one mention's reasoning and redreplier_set_mention_status to triage.",
            parameters: Type.Object({
                websiteId: Type.Optional(Type.String({ description: "Limit to one monitored website (UUID)." })),
                statuses: Type.Optional(Type.Array(MentionStatus, {
                    description: "Filter by triage status; omit to get everything except REJECTED.",
                })),
                scoreBuckets: Type.Optional(Type.Array(RelevanceBucket, {
                    description: "OR-combined: VERY_LOW under 10, LOW 10-29, MEDIUM 30-49, HIGH 50-74, VERY_HIGH 75 and above. LOW and VERY_LOW only show when includeLowRelevance is also true.",
                })),
                includeLowRelevance: Type.Optional(Type.Boolean({
                    description: "Include mentions below the website minimum score (30 by default), hidden otherwise.",
                })),
                minScore: Type.Optional(Type.Integer({
                    minimum: 0,
                    maximum: 100,
                    description: "Only mentions scoring at least this; unscored mentions are left out. Stacks on the website minimum, so set includeLowRelevance to go below it.",
                })),
                keywords: Type.Optional(Type.Array(Type.String(), {
                    description: "Only mentions matched by these keyword values (case-insensitive exact match, as listed by redreplier_websites).",
                })),
                sources: Type.Optional(Type.Array(MentionSource, {
                    description: "Filter by platform: REDDIT_POST, REDDIT_COMMENT, TWITTER (X), BLUESKY, HACKERNEWS, FACEBOOK, FACEBOOK_GROUP (posts inside a Facebook group).",
                })),
                sort: Type.Optional(Type.Union([Type.Literal("RELEVANCE"), Type.Literal("RECENT")], {
                    description: "RELEVANCE is the default, highest score first; RECENT is newest first.",
                })),
                from: Type.Optional(Type.String({ description: "ISO 8601. Only mentions ingested at or after this." })),
                to: Type.Optional(Type.String({ description: "ISO 8601. Only mentions ingested at or before this." })),
                limit: Type.Optional(Type.Integer({ minimum: 1, maximum: 500, description: "Page size, defaults to 50." })),
                offset: Type.Optional(Type.Integer({ minimum: 0, description: "Pagination offset; page while offset < total." })),
            }),
            async execute(_toolCallId, params, signal) {
                return jsonResult(await callApi(cfg(), "GET", "/mentions", {
                    query: params,
                    signal,
                }));
            },
        });
        api.registerTool({
            name: "redreplier_explain_mention",
            label: "RedReplier: explain a relevance score",
            description: "Get the AI relevance reasoning (relevanceReason), tags, and a drafted reply (aiReplySuggestion) for one mention, generating whatever is missing on first call and storing it, so later calls are instant reads. The website must have a description; without one the mention comes back unchanged. Use it when a score looks wrong or before redreplier_set_mention_status on a borderline lead, not across every row of redreplier_mentions, since generation is slow. Returns the full mention; an id unknown to this account returns 404.",
            parameters: Type.Object({
                mentionId: Type.String({ description: "Mention id (UUID) from redreplier_mentions." }),
            }),
            async execute(_toolCallId, params, signal) {
                const { mentionId } = params;
                return jsonResult(await callApi(cfg(), "POST", `/mentions/${encodeURIComponent(mentionId)}/explain`, { signal }));
            },
        });
        api.registerTool({
            name: "redreplier_set_mention_status",
            label: "RedReplier: triage a mention",
            description: "Set one mention's triage status. APPROVED marks it a real lead; REJECTED marks it noise and drops it from default redreplier_mentions results (pass statuses to see it again); NEW returns it to the inbox. Fully reversible: any status can move to any other; reviewedAt is stamped when leaving NEW and cleared on NEW. Judge on the content and relevanceScore, calling redreplier_explain_mention first when the score looks off; never approve a mention you have not read. Returns the updated mention.",
            parameters: Type.Object({
                mentionId: Type.String({ description: "Mention id (UUID) from redreplier_mentions." }),
                status: Type.Union(MentionStatus.anyOf, {
                    description: "APPROVED (real lead), REJECTED (noise, hidden from default lists), or NEW (back to inbox).",
                }),
            }),
            async execute(_toolCallId, params, signal) {
                const { mentionId, status } = params;
                return jsonResult(await callApi(cfg(), "PATCH", `/mentions/${encodeURIComponent(mentionId)}/status`, {
                    body: { status },
                    signal,
                }));
            },
        });
        api.registerTool({
            name: "redreplier_add_keywords",
            label: "RedReplier: add keywords",
            description: "Add keywords to a monitored website. Values are trimmed, lowercased, and de-duplicated; ones already ACTIVE on that site are skipped, and a re-added DISABLED one counts as new. New keywords that fit the plan's free headroom become ACTIVE at once, with no charge. Only the rest stay PENDING, and they match nothing until a slot frees up or the plan is upgraded in the RedReplier app. Adding is unlimited. Returns the whole website with its updated keyword list; check each keyword's status there.",
            parameters: Type.Object({
                websiteId: Type.String({ description: "Monitored website id (UUID) from redreplier_websites." }),
                keywords: Type.Array(Type.String({ maxLength: 255 }), {
                    minItems: 1,
                    description: "Keywords to start matching, for example a product name or a competitor; trimmed, lowercased, and de-duplicated, max 255 characters each.",
                }),
            }),
            async execute(_toolCallId, params, signal) {
                const { websiteId, keywords } = params;
                return jsonResult(await callApi(cfg(), "POST", `/websites/${encodeURIComponent(websiteId)}/keywords`, {
                    body: { keywords },
                    signal,
                }));
            },
        });
    },
});
