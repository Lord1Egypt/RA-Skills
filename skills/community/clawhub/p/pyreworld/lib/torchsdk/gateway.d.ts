/**
 * Gateway URL utilities for Arweave content
 * Irys gateway is dead (deprecated Nov 2025) — all reads go through arweave.net
 * Data uploaded via Irys was settled to Arweave, so same tx IDs work on arweave.net
 */
/**
 * Convert any Irys URL to arweave.net
 */
export declare const irysToArweave: (url: string) => string;
/** @deprecated Use irysToArweave */
export declare const irysToUploader: (url: string) => string;
/**
 * Check if URL is from Irys (dead) gateway or uploader
 */
export declare const isIrysUrl: (url: string) => boolean;
/**
 * Fetch with automatic rewrite from dead Irys domains to arweave.net
 */
export declare const fetchWithFallback: (url: string, options?: RequestInit, timeoutMs?: number) => Promise<Response>;
//# sourceMappingURL=gateway.d.ts.map