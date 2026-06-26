/**
 * Health Check Module for telebiz-mcp
 *
 * Provides status checking and health monitoring for the relay and executor.
 */
export interface HealthStatus {
    relay: 'up' | 'down' | 'unknown';
    executor: 'connected' | 'disconnected' | 'unknown';
    timestamp: number;
    error?: string;
}
export interface DetailedStatus extends HealthStatus {
    relayUrl: string;
    tools?: number;
    lastCheck?: number;
}
/**
 * Check if the relay server is running and if an executor is connected
 */
export declare function checkHealth(): Promise<HealthStatus>;
/**
 * Get detailed status including tool count
 */
export declare function getDetailedStatus(): Promise<DetailedStatus>;
/**
 * Format status for display
 */
export declare function formatStatus(status: DetailedStatus): string;
