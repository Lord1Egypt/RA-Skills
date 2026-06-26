/**
 * Creates the standard container structure inside an agent's pod.
 * Containers in Solid are created by PUT-ing with the right content type.
 */
export declare function createPodContainers(podUrl: string, authFetch: typeof fetch): Promise<void>;
