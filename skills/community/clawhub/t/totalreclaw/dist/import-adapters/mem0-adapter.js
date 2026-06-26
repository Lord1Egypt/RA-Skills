import { BaseImportAdapter } from './base-adapter.js';
/**
 * Category mapping from Mem0 categories to TotalReclaw types.
 */
const CATEGORY_MAP = {
    preference: 'preference',
    preferences: 'preference',
    like: 'preference',
    dislike: 'preference',
    fact: 'fact',
    personal: 'fact',
    biographical: 'fact',
    decision: 'decision',
    goal: 'goal',
    objective: 'goal',
    experience: 'episodic',
    event: 'episodic',
    memory: 'episodic',
};
export class Mem0Adapter extends BaseImportAdapter {
    source = 'mem0';
    displayName = 'Mem0';
    async parse(input, onProgress) {
        const warnings = [];
        const errors = [];
        let memories;
        if (input.content) {
            // Parse from pasted content or export file
            memories = this.parseExportContent(input.content, errors);
        }
        else if (input.api_key) {
            // Fetch from Mem0 API
            memories = await this.fetchFromApi(input.api_key, input.source_user_id, input.api_url, onProgress, errors);
        }
        else {
            errors.push('Mem0 import requires either content (export file) or api_key');
            return { facts: [], chunks: [], totalMessages: 0, warnings, errors };
        }
        if (onProgress) {
            onProgress({
                current: 0,
                total: memories.length,
                phase: 'parsing',
                message: `Parsing ${memories.length} Mem0 memories...`,
            });
        }
        // Convert Mem0 memories to NormalizedFacts
        const rawFacts = memories.map((mem) => ({
            text: mem.memory,
            type: this.mapCategory(mem.categories, mem.metadata?.category),
            importance: 6, // Mem0 doesn't provide importance — default to 6 (above threshold)
            source: 'mem0',
            sourceId: mem.id,
            sourceTimestamp: mem.metadata?.updated_at || mem.metadata?.created_at,
            tags: mem.categories || [],
        }));
        const { facts, invalidCount } = this.validateFacts(rawFacts);
        if (invalidCount > 0) {
            warnings.push(`${invalidCount} memories had invalid/empty text and were skipped`);
        }
        return { facts, chunks: [], totalMessages: 0, warnings, errors, source_metadata: { total_from_source: memories.length } };
    }
    /**
     * Parse Mem0 export file or pasted JSON.
     */
    parseExportContent(content, errors) {
        try {
            const data = JSON.parse(content.trim());
            // Handle export file format: { memories: [...] }
            if (data.memories && Array.isArray(data.memories)) {
                return data.memories;
            }
            // Handle API response format: { results: [...] }
            if (data.results && Array.isArray(data.results)) {
                return data.results;
            }
            // Handle bare array
            if (Array.isArray(data)) {
                return data;
            }
            errors.push('Unrecognized Mem0 format. Expected { memories: [...] }, { results: [...] }, or bare array.');
            return [];
        }
        catch (e) {
            errors.push(`Failed to parse Mem0 JSON: ${e instanceof Error ? e.message : 'Unknown error'}`);
            return [];
        }
    }
    /**
     * Fetch all memories from Mem0 API with pagination.
     */
    async fetchFromApi(apiKey, sourceUserId, apiUrl, onProgress, errors) {
        const baseUrl = apiUrl || 'https://api.mem0.ai';
        const allMemories = [];
        let page = 1;
        const pageSize = 100;
        let hasMore = true;
        while (hasMore) {
            try {
                const url = new URL(`${baseUrl}/v1/memories/`);
                url.searchParams.set('page', String(page));
                url.searchParams.set('page_size', String(pageSize));
                if (sourceUserId) {
                    url.searchParams.set('user_id', sourceUserId);
                }
                const response = await fetch(url.toString(), {
                    headers: {
                        Authorization: `Token ${apiKey}`,
                        'Content-Type': 'application/json',
                    },
                });
                if (!response.ok) {
                    const errorText = await response.text();
                    errors?.push(`Mem0 API error (${response.status}): ${errorText.slice(0, 200)}`);
                    break;
                }
                const data = await response.json();
                const memories = data.results || [];
                allMemories.push(...memories);
                if (onProgress) {
                    onProgress({
                        current: allMemories.length,
                        total: data.total || allMemories.length,
                        phase: 'fetching',
                        message: `Fetched ${allMemories.length} memories from Mem0...`,
                    });
                }
                hasMore = memories.length === pageSize;
                page++;
                // Safety limit: 10,000 memories max
                if (allMemories.length >= 10_000) {
                    errors?.push('Reached 10,000 memory limit. Some memories may not have been fetched.');
                    break;
                }
            }
            catch (e) {
                errors?.push(`Mem0 API fetch error: ${e instanceof Error ? e.message : 'Unknown error'}`);
                break;
            }
        }
        return allMemories;
    }
    /**
     * Map Mem0 category to TotalReclaw fact type.
     */
    mapCategory(categories, singleCategory) {
        const allCategories = [
            ...(categories || []),
            ...(singleCategory ? [singleCategory] : []),
        ];
        for (const cat of allCategories) {
            const mapped = CATEGORY_MAP[cat.toLowerCase()];
            if (mapped)
                return mapped;
        }
        return 'fact'; // default
    }
}
