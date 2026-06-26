/**
 * GA4 API Client - Singleton wrapper for BetaAnalyticsDataClient
 * Also includes Search Console and Indexing API clients
 */
import { BetaAnalyticsDataClient } from '@google-analytics/data';
import { searchconsole } from '@googleapis/searchconsole';
import { indexing } from '@googleapis/indexing';
/**
 * Get the GA4 Analytics Data API client (singleton)
 *
 * @returns The BetaAnalyticsDataClient instance
 * @throws Error if credentials are invalid
 */
export declare function getClient(): BetaAnalyticsDataClient;
/**
 * Get the GA4 property ID formatted for API calls
 *
 * @returns Property ID with "properties/" prefix
 */
export declare function getPropertyId(): string;
/**
 * Reset the client singleton (useful for testing)
 */
export declare function resetClient(): void;
/**
 * Get the Search Console API client (singleton)
 *
 * @returns The Search Console client instance
 * @throws Error if credentials are invalid
 */
export declare function getSearchConsoleClient(): ReturnType<typeof searchconsole>;
/**
 * Get the Indexing API client (singleton)
 *
 * @returns The Indexing client instance
 * @throws Error if credentials are invalid
 */
export declare function getIndexingClient(): ReturnType<typeof indexing>;
/**
 * Get the Search Console site URL
 *
 * @returns Site URL from settings
 */
export declare function getSiteUrl(): string;
//# sourceMappingURL=client.d.ts.map