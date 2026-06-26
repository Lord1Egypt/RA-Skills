/**
 * Abstract base class for import adapters.
 *
 * Adapters are PARSERS only — they convert raw export data into either:
 * - Pre-structured facts (Mem0, MCP Memory — facts are already atomic)
 * - Conversation chunks (ChatGPT, Claude — need LLM extraction)
 *
 * The caller (import tool) handles LLM extraction, encryption, and storage.
 */
export class BaseImportAdapter {
    /**
     * Validate and clean a single fact.
     * Returns null if the fact should be skipped.
     */
    validateFact(fact) {
        // Text is required and must be non-empty
        if (!fact.text || typeof fact.text !== 'string' || fact.text.trim().length < 3) {
            return null;
        }
        // Truncate to 512 chars
        const text = fact.text.trim().slice(0, 512);
        // Normalize type
        const validTypes = ['fact', 'preference', 'decision', 'episodic', 'goal', 'context', 'summary'];
        const type = validTypes.includes(fact.type)
            ? fact.type
            : 'fact';
        // Normalize importance to 1-10
        let importance = fact.importance ?? 5;
        if (importance < 0 || importance > 1) {
            // Already on 1-10 scale
            importance = Math.max(1, Math.min(10, Math.round(importance)));
        }
        else {
            // 0-1 scale — convert to 1-10
            importance = Math.max(1, Math.round(importance * 10));
        }
        return {
            text,
            type,
            importance,
            source: fact.source ?? this.source,
            sourceId: fact.sourceId,
            sourceTimestamp: fact.sourceTimestamp,
            tags: fact.tags,
        };
    }
    /**
     * Batch-validate an array of partial facts.
     */
    validateFacts(rawFacts) {
        const facts = [];
        let invalidCount = 0;
        for (const raw of rawFacts) {
            const validated = this.validateFact(raw);
            if (validated) {
                facts.push(validated);
            }
            else {
                invalidCount++;
            }
        }
        return { facts, invalidCount };
    }
}
