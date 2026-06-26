/**
 * Storage Module - Auto-save results to JSON files with metadata
 */
/**
 * Metadata wrapper for saved results
 */
export interface ResultMetadata {
    savedAt: string;
    category: string;
    operation: string;
    propertyId: string;
    extraInfo?: string;
}
/**
 * Wrapped result with metadata
 */
export interface SavedResult<T = unknown> {
    metadata: ResultMetadata;
    data: T;
}
/**
 * Save result data to a JSON file with metadata wrapper
 *
 * @param data - The data to save
 * @param category - Category directory (e.g., 'reports', 'realtime')
 * @param operation - Operation name (e.g., 'page_views', 'traffic_sources')
 * @param extraInfo - Optional extra info for filename
 * @returns The full path to the saved file
 */
export declare function saveResult<T>(data: T, category: string, operation: string, extraInfo?: string): string;
/**
 * Load a saved result from a JSON file
 *
 * @param filepath - Path to the JSON file
 * @returns The parsed result or null if file doesn't exist
 */
export declare function loadResult<T = unknown>(filepath: string): SavedResult<T> | null;
/**
 * List saved result files for a category
 *
 * @param category - Category to list results for
 * @param limit - Maximum number of results to return
 * @returns Array of file paths, sorted by date descending (newest first)
 */
export declare function listResults(category: string, limit?: number): string[];
/**
 * Get the most recent result for a category/operation
 *
 * @param category - Category to search
 * @param operation - Optional operation to filter by
 * @returns The most recent result or null
 */
export declare function getLatestResult<T = unknown>(category: string, operation?: string): SavedResult<T> | null;
//# sourceMappingURL=storage.d.ts.map