/**
 * Reports API - Standard GA4 report generation
 */
import { getClient, getPropertyId } from '../core/client.js';
import { saveResult } from '../core/storage.js';
import { getSettings } from '../config/settings.js';
/**
 * Parse shorthand date range (e.g., "7d", "30d") to GA4 date range format
 */
export function parseDateRange(range) {
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
        return {
            startDate: `${days}daysAgo`,
            endDate: 'today',
        };
    }
    // Default to 30 days
    return {
        startDate: '30daysAgo',
        endDate: 'today',
    };
}
/**
 * Run a custom GA4 report
 */
export async function runReport(options) {
    const { dimensions, metrics, dateRange, filters, orderBy, limit, save = true, } = options;
    const client = getClient();
    const property = getPropertyId();
    const parsedDateRange = parseDateRange(dateRange);
    const request = {
        property,
        dateRanges: [parsedDateRange],
        dimensions: dimensions.map(name => ({ name })),
        metrics: metrics.map(name => ({ name })),
        ...(limit && { limit }),
    };
    const [response] = await client.runReport(request);
    if (save) {
        const operation = dimensions.join('_') || 'custom';
        const extra = typeof dateRange === 'string' ? dateRange : undefined;
        saveResult(response, 'reports', operation, extra);
    }
    return response;
}
/**
 * Get page view data
 */
export async function getPageViews(dateRange) {
    return runReport({
        dimensions: ['pagePath', 'pageTitle'],
        metrics: ['screenPageViews', 'activeUsers', 'averageSessionDuration'],
        dateRange,
    });
}
/**
 * Get traffic source data
 */
export async function getTrafficSources(dateRange) {
    return runReport({
        dimensions: ['sessionSource', 'sessionMedium', 'sessionCampaignName'],
        metrics: ['sessions', 'activeUsers', 'newUsers', 'bounceRate'],
        dateRange,
    });
}
/**
 * Get user demographic data (country, device, browser)
 */
export async function getUserDemographics(dateRange) {
    return runReport({
        dimensions: ['country', 'deviceCategory', 'browser'],
        metrics: ['activeUsers', 'sessions', 'newUsers'],
        dateRange,
    });
}
/**
 * Get event count data
 */
export async function getEventCounts(dateRange) {
    return runReport({
        dimensions: ['eventName'],
        metrics: ['eventCount', 'eventCountPerUser', 'activeUsers'],
        dateRange,
    });
}
/**
 * Get conversion data
 */
export async function getConversions(dateRange) {
    return runReport({
        dimensions: ['eventName', 'sessionSource'],
        metrics: ['conversions', 'totalRevenue'],
        dateRange,
    });
}
/**
 * Get e-commerce revenue data
 */
export async function getEcommerceRevenue(dateRange) {
    return runReport({
        dimensions: ['date', 'transactionId'],
        metrics: ['totalRevenue', 'ecommercePurchases', 'averagePurchaseRevenue'],
        dateRange,
    });
}
//# sourceMappingURL=reports.js.map