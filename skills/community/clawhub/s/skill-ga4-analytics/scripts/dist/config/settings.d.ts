/**
 * Settings Module - Environment configuration for GA4 API
 */
/**
 * Settings interface for GA4 API configuration
 */
export interface Settings {
    /** GA4 Property ID */
    propertyId: string;
    /** Service account email */
    clientEmail: string;
    /** Service account private key */
    privateKey: string;
    /** Default date range for reports (e.g., "30d", "7d") */
    defaultDateRange: string;
    /** Directory path for storing results */
    resultsDir: string;
    /** Search Console site URL (e.g., "https://example.com") */
    siteUrl: string;
}
/**
 * Validation result from validateSettings()
 */
export interface ValidationResult {
    valid: boolean;
    errors: string[];
}
/**
 * Get current settings from environment variables
 */
export declare function getSettings(): Settings;
/**
 * Validate that all required settings are present
 */
export declare function validateSettings(): ValidationResult;
//# sourceMappingURL=settings.d.ts.map