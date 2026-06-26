/**
 * SeedFlip MCP — Export Generators
 *
 * Produces ready-to-use config files directly from DesignSeed data.
 * All colors are already hex — no conversion needed.
 */
import type { DesignSeed } from './search.js';
export declare function formatTokens(seed: DesignSeed): string;
export declare function formatTailwind(seed: DesignSeed): string;
export declare function formatCSS(seed: DesignSeed): string;
export declare function formatOpenClaw(seed: DesignSeed): string;
export declare function formatShadcn(seed: DesignSeed): string;
