/**
 * Search Console API - Google Search Console data retrieval
 */
/**
 * Date range configuration for Search Console
 */
export interface SearchConsoleDateRange {
    startDate: string;
    endDate: string;
}
/**
 * Search analytics query options
 */
export interface SearchAnalyticsOptions {
    dimensions?: string[];
    dateRange?: string | SearchConsoleDateRange;
    rowLimit?: number;
    startRow?: number;
    save?: boolean;
}
/**
 * Search analytics row structure
 */
export interface SearchAnalyticsRow {
    keys: string[];
    clicks: number;
    impressions: number;
    ctr: number;
    position: number;
}
/**
 * Search analytics response structure
 */
export interface SearchAnalyticsResponse {
    rows?: SearchAnalyticsRow[];
    responseAggregationType?: string;
}
/**
 * Parse shorthand date range (e.g., "7d", "30d") to Search Console date format
 * Note: Search Console requires YYYY-MM-DD format, not GA4's "NdaysAgo" format
 */
export declare function parseSearchConsoleDateRange(range: string | SearchConsoleDateRange | undefined): SearchConsoleDateRange;
/**
 * Query search analytics data
 */
export declare function querySearchAnalytics(options: SearchAnalyticsOptions): Promise<SearchAnalyticsResponse>;
/**
 * Get top search queries
 */
export declare function getTopQueries(dateRange?: string | SearchConsoleDateRange): Promise<SearchAnalyticsResponse>;
/**
 * Get top pages by search performance
 */
export declare function getTopPages(dateRange?: string | SearchConsoleDateRange): Promise<SearchAnalyticsResponse>;
/**
 * Get search performance by device type
 */
export declare function getDevicePerformance(dateRange?: string | SearchConsoleDateRange): Promise<SearchAnalyticsResponse>;
/**
 * Get search performance by country
 */
export declare function getCountryPerformance(dateRange?: string | SearchConsoleDateRange): Promise<SearchAnalyticsResponse>;
/**
 * Get search appearance data (rich results, AMP, etc.)
 */
export declare function getSearchAppearance(dateRange?: string | SearchConsoleDateRange): Promise<SearchAnalyticsResponse>;
//# sourceMappingURL=searchConsole.d.ts.map