/**
 * Realtime API - Live GA4 data
 */
import { getClient, getPropertyId } from '../core/client.js';
import { saveResult } from '../core/storage.js';
/**
 * Get current active users
 */
export async function getActiveUsers(save = true) {
    const client = getClient();
    const property = getPropertyId();
    const [response] = await client.runRealtimeReport({
        property,
        dimensions: [{ name: 'unifiedScreenName' }],
        metrics: [{ name: 'activeUsers' }],
    });
    if (save) {
        saveResult(response, 'realtime', 'active_users');
    }
    return response;
}
/**
 * Get current event data
 */
export async function getRealtimeEvents(save = true) {
    const client = getClient();
    const property = getPropertyId();
    const [response] = await client.runRealtimeReport({
        property,
        dimensions: [{ name: 'eventName' }],
        metrics: [{ name: 'eventCount' }],
    });
    if (save) {
        saveResult(response, 'realtime', 'events');
    }
    return response;
}
/**
 * Get currently viewed pages
 */
export async function getRealtimePages(save = true) {
    const client = getClient();
    const property = getPropertyId();
    const [response] = await client.runRealtimeReport({
        property,
        dimensions: [{ name: 'unifiedScreenName' }],
        metrics: [{ name: 'screenPageViews' }],
    });
    if (save) {
        saveResult(response, 'realtime', 'pages');
    }
    return response;
}
/**
 * Get realtime traffic sources
 */
export async function getRealtimeSources(save = true) {
    const client = getClient();
    const property = getPropertyId();
    const [response] = await client.runRealtimeReport({
        property,
        dimensions: [{ name: 'firstUserSource' }, { name: 'firstUserMedium' }],
        metrics: [{ name: 'activeUsers' }],
    });
    if (save) {
        saveResult(response, 'realtime', 'sources');
    }
    return response;
}
//# sourceMappingURL=realtime.js.map