/**
 * Search Console API - Google Search Console data retrieval
 */
import { getSearchConsoleClient, getSiteUrl } from '../core/client.js';
import { saveResult } from '../core/storage.js';
import { getSettings } from '../config/settings.js';
/**
 * Parse shorthand date range (e.g., "7d", "30d") to Search Console date format
 * Note: Search Console requires YYYY-MM-DD format, not GA4's "NdaysAgo" format
 */
export function parseSearchConsoleDateRange(range) {
    if (!range) {
        const settings = getSettings();
        range = settings.defaultDateRange;
    }
    if (typeof range === 'object') {
        return range;
    }
    // Parse shorthand like "7d", "30d", "90d"
    const match = range.match(/^(\d+)d$/);
    if (match) {
        const days = parseInt(match[1], 10);
        const endDate = new Date();
        const startDate = new Date();
        startDate.setDate(startDate.getDate() - days);
        return {
            startDate: startDate.toISOString().split('T')[0],
            endDate: endDate.toISOString().split('T')[0],
        };
    }
    // Default to 30 days
    const endDate = new Date();
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - 30);
    return {
        startDate: startDate.toISOString().split('T')[0],
        endDate: endDate.toISOString().split('T')[0],
    };
}
/**
 * Query search analytics data
 */
export async function querySearchAnalytics(options) {
    const { dimensions = ['query'], dateRange, rowLimit = 1000, startRow = 0, save = true, } = options;
    const client = getSearchConsoleClient();
    const siteUrl = getSiteUrl();
    const parsedDateRange = parseSearchConsoleDateRange(dateRange);
    const response = await client.searchanalytics.query({
        siteUrl,
        requestBody: {
            startDate: parsedDateRange.startDate,
            endDate: parsedDateRange.endDate,
            dimensions,
            rowLimit,
            startRow,
        },
    });
    const result = response.data;
    if (save) {
        const operation = dimensions.join('_') || 'query';
        const extra = typeof dateRange === 'string' ? dateRange : undefined;
        saveResult(result, 'searchconsole', operation, extra);
    }
    return result;
}
/**
 * Get top search queries
 */
export async function getTopQueries(dateRange) {
    return querySearchAnalytics({
        dimensions: ['query'],
        dateRange,
        rowLimit: 100,
    });
}
/**
 * Get top pages by search performance
 */
export async function getTopPages(dateRange) {
    return querySearchAnalytics({
        dimensions: ['page'],
        dateRange,
        rowLimit: 100,
    });
}
/**
 * Get search performance by device type
 */
export async function getDevicePerformance(dateRange) {
    return querySearchAnalytics({
        dimensions: ['device'],
        dateRange,
    });
}
/**
 * Get search performance by country
 */
export async function getCountryPerformance(dateRange) {
    return querySearchAnalytics({
        dimensions: ['country'],
        dateRange,
        rowLimit: 50,
    });
}
/**
 * Get search appearance data (rich results, AMP, etc.)
 */
export async function getSearchAppearance(dateRange) {
    return querySearchAnalytics({
        dimensions: ['searchAppearance'],
        dateRange,
    });
}
//# sourceMappingURL=searchConsole.js.map