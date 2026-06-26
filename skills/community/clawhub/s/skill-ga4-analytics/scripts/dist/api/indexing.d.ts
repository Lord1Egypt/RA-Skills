/**
 * Indexing API - Request re-indexing and URL inspection
 */
/**
 * Indexing request options
 */
export interface IndexingOptions {
    save?: boolean;
}
/**
 * URL notification result
 */
export interface UrlNotificationResult {
    url: string;
    type: 'URL_UPDATED' | 'URL_DELETED';
    notifyTime: string;
}
/**
 * URL inspection result
 */
export interface UrlInspectionResult {
    inspectionResultLink?: string;
    indexStatus: {
        verdict: 'PASS' | 'FAIL' | 'NEUTRAL';
        coverageState: string;
        robotsTxtState?: string;
        indexingState?: string;
        lastCrawlTime?: string;
        pageFetchState?: string;
        googleCanonical?: string;
        userCanonical?: string;
        crawledAs?: string;
    };
    mobileUsability?: {
        verdict: string;
        issues?: unknown[];
    };
    richResults?: {
        verdict: string;
        detectedItems?: unknown[];
    };
}
/**
 * Request indexing for a single URL (notify Google to re-crawl)
 *
 * @param url - The URL to request indexing for
 * @param options - Optional settings (save to file, etc.)
 * @returns Notification result with timestamp
 */
export declare function requestIndexing(url: string, options?: IndexingOptions): Promise<UrlNotificationResult>;
/**
 * Request indexing for multiple URLs
 *
 * @param urls - Array of URLs to request indexing for
 * @param options - Optional settings
 * @returns Array of notification results
 */
export declare function requestIndexingBatch(urls: string[], options?: IndexingOptions): Promise<UrlNotificationResult[]>;
/**
 * Request URL removal from index
 *
 * @param url - The URL to request removal for
 * @param options - Optional settings
 * @returns Notification result
 */
export declare function removeFromIndex(url: string, options?: IndexingOptions): Promise<UrlNotificationResult>;
/**
 * Inspect a URL to check its index status
 *
 * @param url - The URL to inspect
 * @param options - Optional settings
 * @returns URL inspection result with index status
 */
export declare function inspectUrl(url: string, options?: IndexingOptions): Promise<UrlInspectionResult>;
//# sourceMappingURL=indexing.d.ts.map