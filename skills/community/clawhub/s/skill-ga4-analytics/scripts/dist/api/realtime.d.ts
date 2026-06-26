/**
 * Realtime API - Live GA4 data
 */
/**
 * Realtime report response structure
 */
export interface RealtimeResponse {
    dimensionHeaders?: Array<{
        name: string;
    }>;
    metricHeaders?: Array<{
        name: string;
    }>;
    rows?: Array<{
        dimensionValues: Array<{
            value: string;
        }>;
        metricValues: Array<{
            value: string;
        }>;
    }>;
    rowCount?: number;
}
/**
 * Get current active users
 */
export declare function getActiveUsers(save?: boolean): Promise<RealtimeResponse>;
/**
 * Get current event data
 */
export declare function getRealtimeEvents(save?: boolean): Promise<RealtimeResponse>;
/**
 * Get currently viewed pages
 */
export declare function getRealtimePages(save?: boolean): Promise<RealtimeResponse>;
/**
 * Get realtime traffic sources
 */
export declare function getRealtimeSources(save?: boolean): Promise<RealtimeResponse>;
//# sourceMappingURL=realtime.d.ts.map