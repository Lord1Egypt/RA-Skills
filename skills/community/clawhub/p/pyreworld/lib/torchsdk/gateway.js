"use strict";
/**
 * Gateway URL utilities for Arweave content
 * Irys gateway is dead (deprecated Nov 2025) — all reads go through arweave.net
 * Data uploaded via Irys was settled to Arweave, so same tx IDs work on arweave.net
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.fetchWithFallback = exports.isIrysUrl = exports.irysToUploader = exports.irysToArweave = void 0;
const IRYS_GATEWAY = 'gateway.irys.xyz';
const IRYS_UPLOADER = 'uploader.irys.xyz';
const ARWEAVE_GATEWAY = 'arweave.net';
/**
 * Convert any Irys URL to arweave.net
 */
const irysToArweave = (url) => url.replace(IRYS_GATEWAY, ARWEAVE_GATEWAY).replace(IRYS_UPLOADER, ARWEAVE_GATEWAY);
exports.irysToArweave = irysToArweave;
/** @deprecated Use irysToArweave */
exports.irysToUploader = exports.irysToArweave;
/**
 * Check if URL is from Irys (dead) gateway or uploader
 */
const isIrysUrl = (url) => {
    try {
        const host = new URL(url).hostname;
        return host === IRYS_GATEWAY || host === IRYS_UPLOADER;
    }
    catch {
        return false;
    }
};
exports.isIrysUrl = isIrysUrl;
/**
 * Fetch with automatic rewrite from dead Irys domains to arweave.net
 */
const fetchWithFallback = async (url, options, timeoutMs = 10000) => {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);
    const opts = { ...options, signal: controller.signal };
    try {
        if ((0, exports.isIrysUrl)(url)) {
            return await fetch((0, exports.irysToArweave)(url), opts);
        }
        return await fetch(url, opts);
    }
    finally {
        clearTimeout(timer);
    }
};
exports.fetchWithFallback = fetchWithFallback;
//# sourceMappingURL=gateway.js.map