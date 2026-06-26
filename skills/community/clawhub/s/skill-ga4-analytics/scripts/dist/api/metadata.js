/**
 * Metadata API - Available dimensions and metrics
 */
import { getClient, getPropertyId } from '../core/client.js';
import { saveResult } from '../core/storage.js';
/**
 * Get all available dimensions for the property
 */
export async function getAvailableDimensions(save = true) {
    const client = getClient();
    const property = getPropertyId();
    const [response] = await client.getMetadata({
        name: `${property}/metadata`,
    });
    const result = {
        dimensions: response.dimensions || [],
    };
    if (save) {
        saveResult(result, 'metadata', 'dimensions');
    }
    return result;
}
/**
 * Get all available metrics for the property
 */
export async function getAvailableMetrics(save = true) {
    const client = getClient();
    const property = getPropertyId();
    const [response] = await client.getMetadata({
        name: `${property}/metadata`,
    });
    const result = {
        metrics: response.metrics || [],
    };
    if (save) {
        saveResult(result, 'metadata', 'metrics');
    }
    return result;
}
/**
 * Get full property metadata (dimensions and metrics)
 */
export async function getPropertyMetadata(save = true) {
    const client = getClient();
    const property = getPropertyId();
    const [response] = await client.getMetadata({
        name: `${property}/metadata`,
    });
    if (save) {
        saveResult(response, 'metadata', 'full');
    }
    return response;
}
//# sourceMappingURL=metadata.js.map