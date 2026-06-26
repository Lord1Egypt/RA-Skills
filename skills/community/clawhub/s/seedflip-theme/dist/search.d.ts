/**
 * SeedFlip MCP — Search Engine
 *
 * Scores seeds against a natural language query.
 * Handles brand references ("Stripe"), vibes ("dark minimal"),
 * and style descriptors ("brutalist", "warm editorial").
 */
interface DesignSeed {
    name: string;
    fakeUrl: string;
    vibe: string;
    tags: string[];
    headingFont: string;
    bodyFont: string;
    headingWeight: number;
    letterSpacing: string;
    bg: string;
    surface: string;
    surfaceHover: string;
    border: string;
    text: string;
    textMuted: string;
    accent: string;
    accentSoft: string;
    radius: string;
    radiusSm: string;
    radiusXl: string;
    shadow: string;
    shadowSm: string;
    shadowStyle: string;
    gradient: string;
    aiPromptTypography: string;
    aiPromptColors: string;
    aiPromptShape: string;
    aiPromptDepth: string;
    aiPromptRules: string;
    collection?: string;
}
export type { DesignSeed };
export interface ScoredSeed {
    seed: DesignSeed;
    score: number;
    matchReasons: string[];
}
export declare function searchSeeds(seeds: DesignSeed[], query: string): ScoredSeed[];
