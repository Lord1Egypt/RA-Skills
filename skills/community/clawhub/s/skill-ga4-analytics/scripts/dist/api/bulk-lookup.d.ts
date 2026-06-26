/**
 * Bulk URL Lookup - Get GA4 metrics for specific page paths
 *
 * This module provides a convenient way to look up analytics data
 * for a list of specific URLs, similar to a bulk URL lookup field.
 */
import type { ReportResponse, DateRange } from './reports.js';
/**
 * Options for bulk URL lookup
 */
export interface BulkLookupOptions {
    /** Date range (e.g., "7d", "30d") or explicit dates */
    dateRange?: string | DateRange;
    /** Custom metrics to retrieve (defaults to standard page metrics) */
    metrics?: string[];
    /** Whether to save results to file (default: true) */
    save?: boolean;
}
/**
 * Dimension filter expression for GA4 API
 */
export interface DimensionFilterExpression {
    filter: {
        fieldName: string;
        inListFilter?: {
            values: string[];
            caseSensitive?: boolean;
        };
        stringFilter?: {
            matchType: string;
            value: string;
            caseSensitive?: boolean;
        };
    };
}
/**
 * Normalize URLs to ensure consistent format
 *
 * - Trims whitespace
 * - Adds leading slash if missing
 * - Preserves trailing slashes
 *
 * @param urls - Array of URLs to normalize
 * @returns Normalized URL array
 */
export declare function normalizeUrls(urls: string[]): string[];
/**
 * Build a dimension filter expression for the given URLs
 *
 * @param urls - Array of page paths to filter by
 * @returns Filter expression or null if no URLs provided
 */
export declare function buildUrlFilter(urls: string[]): DimensionFilterExpression | null;
/**
 * Get GA4 metrics for specific page paths (bulk URL lookup)
 *
 * @param urls - Array of page paths to look up (e.g., ['/pricing', '/about'])
 * @param options - Optional configuration
 * @returns Report response with metrics for the specified URLs
 *
 * @example
 * ```typescript
 * // Get metrics for specific pages
 * const result = await getMetricsForUrls(['/pricing', '/about', '/blog']);
 *
 * // With custom date range and metrics
 * const result = await getMetricsForUrls(['/pricing'], {
 *   dateRange: '7d',
 *   metrics: ['sessions', 'bounceRate'],
 * });
 * ```
 */
export declare function getMetricsForUrls(urls: string[], options?: BulkLookupOptions): Promise<ReportResponse>;
//# sourceMappingURL=bulk-lookup.d.ts.map