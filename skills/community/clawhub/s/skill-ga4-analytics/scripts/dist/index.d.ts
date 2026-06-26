/**
 * GA4 Analytics Toolkit - Main Entry Point
 *
 * Simple interface for Google Analytics 4 data analysis.
 * All results are automatically saved to the /results directory with timestamps.
 *
 * Usage:
 *   import { siteOverview, trafficAnalysis } from './index.js';
 *   const overview = await siteOverview('30d');
 */
export * from './api/reports.js';
export * from './api/realtime.js';
export * from './api/metadata.js';
export * from './api/searchConsole.js';
export * from './api/indexing.js';
export * from './api/bulk-lookup.js';
export { getClient, getPropertyId, getSearchConsoleClient, getIndexingClient, getSiteUrl, resetClient } from './core/client.js';
export { saveResult, loadResult, listResults, getLatestResult } from './core/storage.js';
export { getSettings, validateSettings } from './config/settings.js';
import { type DateRange } from './api/reports.js';
import { type SearchConsoleDateRange } from './api/searchConsole.js';
/**
 * Comprehensive site overview - combines multiple reports
 */
export declare function siteOverview(dateRange?: string | DateRange): Promise<Record<string, unknown>>;
/**
 * Deep dive on traffic sources
 */
export declare function trafficAnalysis(dateRange?: string | DateRange): Promise<Record<string, unknown>>;
/**
 * Content performance analysis
 */
export declare function contentPerformance(dateRange?: string | DateRange): Promise<Record<string, unknown>>;
/**
 * User behavior analysis
 */
export declare function userBehavior(dateRange?: string | DateRange): Promise<Record<string, unknown>>;
/**
 * Compare two date ranges
 */
export declare function compareDateRanges(range1: DateRange, range2: DateRange, dimensions?: string[], metrics?: string[]): Promise<{
    period1: {
        dateRange: DateRange;
        data: import("./api/reports.js").ReportResponse;
    };
    period2: {
        dateRange: DateRange;
        data: import("./api/reports.js").ReportResponse;
    };
}>;
/**
 * Get current live data snapshot
 */
export declare function liveSnapshot(): Promise<Record<string, unknown>>;
/**
 * Comprehensive Search Console overview
 */
export declare function searchConsoleOverview(dateRange?: string | SearchConsoleDateRange): Promise<Record<string, unknown>>;
/**
 * Deep dive into keyword/query analysis
 */
export declare function keywordAnalysis(dateRange?: string | SearchConsoleDateRange): Promise<Record<string, unknown>>;
/**
 * SEO page performance analysis
 */
export declare function seoPagePerformance(dateRange?: string | SearchConsoleDateRange): Promise<Record<string, unknown>>;
/**
 * Request re-indexing for updated URLs
 */
export declare function reindexUrls(urls: string[]): Promise<{
    url: string;
    status: string;
    error?: string;
}[]>;
/**
 * Check index status for URLs
 */
export declare function checkIndexStatus(urls: string[]): Promise<{
    url: string;
    indexed: boolean;
    status: unknown;
}[]>;
/**
 * Get available dimensions and metrics
 */
export declare function getAvailableFields(): Promise<import("./api/metadata.js").MetadataResponse>;
//# sourceMappingURL=index.d.ts.map