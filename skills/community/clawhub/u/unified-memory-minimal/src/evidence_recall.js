/**
 * Evidence-Driven Recall - Memory Retrieval Based on Evidence Chains
 * Enhances memory retrieval by weighting memories based on their evidence quality
 * 
 * Storage: ~/.openclaw/workspace/memory/evidence_recall.json
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const HOME = process.env.HOME || '/root';
const MEMORY_DIR = join(HOME, '.openclaw', 'workspace', 'memory');
const EVIDENCE_RECALL_FILE = join(MEMORY_DIR, 'evidence_recall.json');

// Ensure memory directory exists
if (!existsSync(MEMORY_DIR)) {
  mkdirSync(MEMORY_DIR, { recursive: true });
}

// ============================================================================
// Evidence Weighting Configuration
// ============================================================================

const EVIDENCE_WEIGHTS = {
  transcript: 1.0,  // Direct transcript evidence - highest weight
  message: 0.9,      // Direct message evidence
  manual: 0.7,       // Manually created evidence
  inference: 0.5,    // Inferred evidence - lowest weight
};

const CONFIDENCE_MULTIPLIERS = {
  high: 1.5,   // Confidence >= 0.8
  medium: 1.0, // Confidence 0.5-0.8
  low: 0.5,    // Confidence < 0.5
};

// ============================================================================
// Evidence-Driven Recall Engine
// ============================================================================

export class EvidenceDrivenRecall {
  constructor() {
    this.evidenceIndex = new Map(); // memory_id -> evidence list
    this.sourceIndex = new Map();   // source_id -> memory_ids
    // Auto-rebuild index from evidence_recall.json on startup
    this._rebuildIndex();
  }

  /**
   * Rebuild indexes from evidence_recall.json (called automatically on startup)
   */
  _rebuildIndex() {
    if (!existsSync(EVIDENCE_RECALL_FILE)) return;
    try {
      const data = JSON.parse(readFileSync(EVIDENCE_RECALL_FILE, 'utf-8'));
      if (!data || typeof data !== 'object') return;
      for (const [memoryId, evidenceList] of Object.entries(data)) {
        if (Array.isArray(evidenceList)) {
          this.indexEvidence(memoryId, evidenceList);
        }
      }
      console.log(`[EvidenceDrivenRecall] Index rebuilt: ${this.evidenceIndex.size} memories indexed`);
    } catch (err) {
      console.warn(`[EvidenceDrivenRecall] Failed to rebuild index: ${err.message}`);
    }
  }

  /**
   * Index evidence for a memory
   */
  indexEvidence(memoryId, evidence) {
    if (!this.evidenceIndex.has(memoryId)) {
      this.evidenceIndex.set(memoryId, []);
    }
    
    this.evidenceIndex.get(memoryId).push(...evidence);
    
    // Index by source
    evidence.forEach(evidenceItem => {
      if (evidenceItem.source_id) {
        if (!this.sourceIndex.has(evidenceItem.source_id)) {
          this.sourceIndex.set(evidenceItem.source_id, []);
        }
        if (!this.sourceIndex.get(evidenceItem.source_id).includes(memoryId)) {
          this.sourceIndex.get(evidenceItem.source_id).push(memoryId);
        }
      }
    });
  }

  /**
   * Calculate evidence score for a memory
   */
  calculateEvidenceScore(memory) {
    const evidenceList = this.evidenceIndex.get(memory.id) || [];
    
    if (evidenceList.length === 0) {
      return { score: 0.0, evidenceCount: 0 };
    }
    
    let totalWeight = 0;
    let totalConfidence = 0;
    
    evidenceList.forEach(evidence => {
      const weight = EVIDENCE_WEIGHTS[evidence.type] || 0.5;
      const confidence = evidence.confidence || 0.5;
      const confidenceMultiplier = CONFIDENCE_MULTIPLIERS[confidence >= 0.8 ? 'high' : confidence >= 0.5 ? 'medium' : 'low'];
      
      totalWeight += weight;
      totalConfidence += confidence * confidenceMultiplier;
    });
    
    const avgScore = totalConfidence / evidenceList.length;
    const evidenceBoost = Math.min(1.5, 1 + (evidenceList.length * 0.1)); // Max 1.5x boost
    
    return {
      score: avgScore * evidenceBoost,
      evidenceCount: evidenceList.length,
      totalWeight,
      avgConfidence: totalConfidence / evidenceList.length
    };
  }

  /**
   * Rank memories by evidence score
   */
  rankByEvidence(memories) {
    return memories.map(memory => {
      const evidenceScore = this.calculateEvidenceScore(memory);
      return {
        ...memory,
        evidence_score: evidenceScore.score,
        evidence_count: evidenceScore.evidenceCount,
        avg_confidence: evidenceScore.avgConfidence
      };
    }).sort((a, b) => b.evidence_score - a.evidence_score);
  }

  /**
   * Filter memories by evidence type
   */
  filterByEvidenceType(memories, evidenceType) {
    return memories.filter(memory => {
      const evidenceList = this.evidenceIndex.get(memory.id) || [];
      return evidenceList.some(e => e.type === evidenceType);
    });
  }

  /**
   * Filter memories by evidence source
   */
  filterByEvidenceSource(memories, sourceId) {
    const memoryIds = this.sourceIndex.get(sourceId) || [];
    return memories.filter(memory => memoryIds.includes(memory.id));
  }

  /**
   * Get memories with high-confidence evidence
   */
  getHighConfidenceMemories(memories, minConfidence = 0.8) {
    return memories.filter(memory => {
      const evidenceList = this.evidenceIndex.get(memory.id) || [];
      return evidenceList.some(e => (e.confidence || 0) >= minConfidence);
    });
  }

  /**
   * Get memories with transcript evidence
   */
  getTranscriptEvidenceMemories(memories) {
    return this.filterByEvidenceType(memories, 'transcript');
  }

  /**
   * Get evidence summary for a memory
   */
  getEvidenceSummary(memoryId) {
    const evidenceList = this.evidenceIndex.get(memoryId) || [];
    
    const summary = {
      memory_id: memoryId,
      total_evidence: evidenceList.length,
      by_type: {},
      avg_confidence: 0,
      max_confidence: 0
    };
    
    let totalConfidence = 0;
    
    evidenceList.forEach(evidence => {
      const type = evidence.type || 'unknown';
      summary.by_type[type] = (summary.by_type[type] || 0) + 1;
      
      const confidence = evidence.confidence || 0;
      totalConfidence += confidence;
      summary.max_confidence = Math.max(summary.max_confidence, confidence);
    });
    
    summary.avg_confidence = evidenceList.length > 0 ? totalConfidence / evidenceList.length : 0;
    
    return summary;
  }

  /**
   * Get evidence-driven recall results
   */
  recall(query, memories, options = {}) {
    const {
      topK = 10,
      minEvidenceScore = 0,
      evidenceTypes = ['transcript', 'message', 'manual', 'inference'],
      includeEvidence = true
    } = options;
    
    // Filter by evidence types
    let filteredMemories = memories.filter(memory => {
      const evidenceList = this.evidenceIndex.get(memory.id) || [];
      return evidenceList.some(e => evidenceTypes.includes(e.type));
    });
    
    // Rank by evidence score
    const rankedMemories = this.rankByEvidence(filteredMemories);
    
    // Filter by minimum evidence score
    if (minEvidenceScore > 0) {
      rankedMemories.filter(m => m.evidence_score >= minEvidenceScore);
    }
    
    // Take top K
    const results = rankedMemories.slice(0, topK);
    
    // Add evidence information if requested
    if (includeEvidence) {
      return results.map(memory => ({
        ...memory,
        evidence_summary: this.getEvidenceSummary(memory.id)
      }));
    }
    
    return results;
  }

  /**
   * Get recall statistics
   */
  getStatistics() {
    const totalMemories = this.evidenceIndex.size;
    let totalEvidence = 0;
    let memoriesWithEvidence = 0;
    
    const evidenceByType = {};
    
    this.evidenceIndex.forEach((evidenceList, memoryId) => {
      if (evidenceList.length > 0) {
        memoriesWithEvidence++;
        totalEvidence += evidenceList.length;
        
        evidenceList.forEach(evidence => {
          const type = evidence.type || 'unknown';
          evidenceByType[type] = (evidenceByType[type] || 0) + 1;
        });
      }
    });
    
    return {
      total_memories_indexed: totalMemories,
      memories_with_evidence: memoriesWithEvidence,
      total_evidence_entries: totalEvidence,
      evidence_by_type: evidenceByType,
      coverage_rate: totalMemories > 0 ? (memoriesWithEvidence / totalMemories) * 100 : 0
    };
  }

  /**
   * Clear evidence index
   */
  clear() {
    this.evidenceIndex.clear();
    this.sourceIndex.clear();
  }
}

// ============================================================================
// Singleton Instance
// ============================================================================

let _recallEngineInstance = null;

export function getEvidenceRecallEngine() {
  if (!_recallEngineInstance) {
    _recallEngineInstance = new EvidenceDrivenRecall();
  }
  return _recallEngineInstance;
}

// ============================================================================
// Tool Functions
// ============================================================================

/**
 * memory_evidence_recall - Evidence-driven memory recall
 */
export function memory_evidence_recall(query, memories, options = {}) {
  const engine = getEvidenceRecallEngine();
  return engine.recall(query, memories, options);
}

/**
 * memory_evidence_index - Index evidence for a memory
 */
export function memory_evidence_index(memoryId, evidence) {
  const engine = getEvidenceRecallEngine();
  engine.indexEvidence(memoryId, evidence);
  return { success: true, indexed: evidence.length };
}

/**
 * memory_evidence_score - Calculate evidence score for a memory
 */
export function memory_evidence_score(memoryId) {
  const engine = getEvidenceRecallEngine();
  
  // Create a mock memory object
  const mockMemory = { id: memoryId };
  return engine.calculateEvidenceScore(mockMemory);
}

/**
 * memory_evidence_rank - Rank memories by evidence score
 */
export function memory_evidence_rank(memories) {
  const engine = getEvidenceRecallEngine();
  return engine.rankByEvidence(memories);
}

/**
 * memory_evidence_filter_by_type - Filter memories by evidence type
 */
export function memory_evidence_filter_by_type(memories, evidenceType) {
  const engine = getEvidenceRecallEngine();
  return engine.filterByEvidenceType(memories, evidenceType);
}

/**
 * memory_evidence_filter_by_source - Filter memories by evidence source
 */
export function memory_evidence_filter_by_source(memories, sourceId) {
  const engine = getEvidenceRecallEngine();
  return engine.filterByEvidenceSource(memories, sourceId);
}

/**
 * memory_evidence_high_confidence - Get high-confidence memories
 */
export function memory_evidence_high_confidence(memories, minConfidence = 0.8) {
  const engine = getEvidenceRecallEngine();
  return engine.getHighConfidenceMemories(memories, minConfidence);
}

/**
 * memory_evidence_transcript_only - Get transcript evidence memories
 */
export function memory_evidence_transcript_only(memories) {
  const engine = getEvidenceRecallEngine();
  return engine.getTranscriptEvidenceMemories(memories);
}

/**
 * memory_evidence_summary - Get evidence summary for a memory
 */
export function memory_evidence_summary(memoryId) {
  const engine = getEvidenceRecallEngine();
  return engine.getEvidenceSummary(memoryId);
}

/**
 * memory_evidence_statistics - Get recall statistics
 */
export function memory_evidence_statistics() {
  const engine = getEvidenceRecallEngine();
  return engine.getStatistics();
}

/**
 * memory_evidence_clear - Clear evidence index
 */
export function memory_evidence_clear() {
  const engine = getEvidenceRecallEngine();
  engine.clear();
  return { success: true };
}
