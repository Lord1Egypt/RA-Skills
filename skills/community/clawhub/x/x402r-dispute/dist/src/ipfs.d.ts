/**
 * IPFS pinning — uses Pinata JWT, falls back to placeholder CID.
 */
/**
 * Pin JSON to IPFS.
 * 1. Pinata JWT (required for production use)
 * 2. Placeholder CID fallback (dev/testing only)
 */
export declare function pinToIpfs(data: Record<string, unknown>): Promise<string>;
