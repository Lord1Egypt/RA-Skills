/**
 * Reports API - Standard GA4 report generation
 */
/**
 * Date range configuration
 */
export interface DateRange {
    startDate: string;
    endDate: string;
}
/**
 * Report options
 */
export interface ReportOptions {
    dimensions: string[];
    metrics: string[];
    dateRange?: string | DateRange;
    filters?: Record<string, string>;
    orderBy?: string[];
    limit?: number;
    save?: boolean;
}
/**
 * Report response structure
 */
export interface ReportResponse {
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
    metadata?: Record<string, unknown>;
}
/**
 * Parse shorthand date range (e.g., "7d", "30d") to GA4 date range format
 */
export declare function parseDateRange(range: string | DateRange | undefined): DateRange;
/**
 * Run a custom GA4 report
 */
export declare function runReport(options: ReportOptions): Promise<ReportResponse>;
/**
 * Get page view data
 */
export declare function getPageViews(dateRange?: string | DateRange): Promise<ReportResponse>;
/**
 * Get traffic source data
 */
export declare function getTrafficSources(dateRange?: string | DateRange): Promise<ReportResponse>;
/**
 * Get user demographic data (country, device, browser)
 */
export declare function getUserDemographics(dateRange?: string | DateRange): Promise<ReportResponse>;
/**
 * Get event count data
 */
export declare function getEventCounts(dateRange?: string | DateRange): Promise<ReportResponse>;
/**
 * Get conversion data
 */
export declare function getConversions(dateRange?: string | DateRange): Promise<ReportResponse>;
/**
 * Get e-commerce revenue data
 */
export declare function getEcommerceRevenue(dateRange?: string | DateRange): Promise<ReportResponse>;
//# sourceMappingURL=reports.d.ts.map