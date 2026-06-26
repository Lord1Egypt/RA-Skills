/**
 * Settings Module - Environment configuration for GA4 API
 */
import { config } from 'dotenv';
import { join } from 'path';
// Load .env file from current working directory
config();
/**
 * Get current settings from environment variables
 */
export function getSettings() {
    return {
        propertyId: process.env.GA4_PROPERTY_ID || '',
        clientEmail: process.env.GA4_CLIENT_EMAIL || '',
        privateKey: (process.env.GA4_PRIVATE_KEY || '').replace(/\\n/g, '\n'),
        defaultDateRange: process.env.GA4_DEFAULT_DATE_RANGE || '30d',
        resultsDir: join(process.cwd(), 'results'),
        siteUrl: process.env.SEARCH_CONSOLE_SITE_URL || '',
    };
}
/**
 * Validate that all required settings are present
 */
export function validateSettings() {
    const settings = getSettings();
    const errors = [];
    if (!settings.propertyId) {
        errors.push('GA4_PROPERTY_ID is required');
    }
    if (!settings.clientEmail) {
        errors.push('GA4_CLIENT_EMAIL is required');
    }
    if (!settings.privateKey) {
        errors.push('GA4_PRIVATE_KEY is required');
    }
    return {
        valid: errors.length === 0,
        errors,
    };
}
//# sourceMappingURL=settings.js.map