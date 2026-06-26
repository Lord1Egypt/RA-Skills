/**
 * Metadata API - Available dimensions and metrics
 */
/**
 * Dimension metadata
 */
export interface DimensionMetadata {
    apiName: string;
    uiName: string;
    description: string;
}
/**
 * Metric metadata
 */
export interface MetricMetadata {
    apiName: string;
    uiName: string;
    description: string;
}
/**
 * Full property metadata response
 */
export interface MetadataResponse {
    name?: string;
    dimensions?: DimensionMetadata[];
    metrics?: MetricMetadata[];
}
/**
 * Get all available dimensions for the property
 */
export declare function getAvailableDimensions(save?: boolean): Promise<MetadataResponse>;
/**
 * Get all available metrics for the property
 */
export declare function getAvailableMetrics(save?: boolean): Promise<MetadataResponse>;
/**
 * Get full property metadata (dimensions and metrics)
 */
export declare function getPropertyMetadata(save?: boolean): Promise<MetadataResponse>;
//# sourceMappingURL=metadata.d.ts.map