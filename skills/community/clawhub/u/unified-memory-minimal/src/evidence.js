/**
 * evidence.js - Evidence Chain Mechanism
 * 
 * Tracks the source and evolution of memories through evidence chains.
 * Each memory can trace back to its origin (transcript, message, etc.)
 * 
 * Inspired by Smart Memory's evidence chain mechanism
 */

import { writeFileSync, readFileSync, existsSync, mkdirSync, appendFileSync } from 'fs';
import { join } from 'path';

const HOME = process.env.HOME || '/root';
const MEMORY_DIR = join(HOME, '.openclaw', 'workspace', 'memory');
const EVIDENCE_DIR = join(MEMORY_DIR, 'evidence');
const EVIDENCE_FILE = join(EVIDENCE_DIR, 'evidence.json');

// Ensure evidence directory exists
if (!existsSync(EVIDENCE_DIR)) {
  mkdirSync(EVIDENCE_DIR, { recursive: true });
}

/**
 * Evidence Chain structure:
 * {
 *   memory_id: string,
 *   chain: [
 *     {
 *       type: 'transcript' | 'message' | 'manual' | 'inference',
 *       source_id: string,
 *       timestamp: number,
 *       confidence: number (0-1),
 *       context: string
 *     }
 *   ],
 *   created_at: number,
 *   updated_at: number
 * }
 */

/**
 * Initialize evidence chain for a memory
 */
function getEvidenceChain(memoryId) {
  if (!existsSync(EVIDENCE_FILE)) {
    return null;
  }

  try {
    const content = readFileSync(EVIDENCE_FILE, 'utf-8');
    const evidence = JSON.parse(content);
    return evidence[memoryId] || null;
  } catch (err) {
    console.error(`[Evidence] Error reading evidence file: ${err.message}`);
    return null;
  }
}

/**
 * Add evidence to a memory's chain
 */
export function evidenceAdd(memoryId, evidence) {
  let chains = {};
  
  if (existsSync(EVIDENCE_FILE)) {
    try {
      const content = readFileSync(EVIDENCE_FILE, 'utf-8');
      chains = JSON.parse(content);
    } catch (err) {
      console.error(`[Evidence] Error reading evidence file: ${err.message}`);
    }
  }

  if (!chains[memoryId]) {
    chains[memoryId] = {
      memory_id: memoryId,
      chain: [],
      created_at: Date.now(),
      updated_at: Date.now()
    };
  }

  // Add new evidence
  chains[memoryId].chain.push({
    type: evidence.type || 'manual',
    source_id: evidence.source_id,
    timestamp: evidence.timestamp || Date.now(),
    confidence: evidence.confidence || 1.0,
    context: evidence.context || ''
  });

  chains[memoryId].updated_at = Date.now();

  writeFileSync(EVIDENCE_FILE, JSON.stringify(chains, null, 2));
  return chains[memoryId];
}

/**
 * Get evidence chain for a memory
 */
export function evidenceGet(memoryId) {
  return getEvidenceChain(memoryId);
}

/**
 * Get memories by evidence type
 */
export function evidenceFindByType(type) {
  if (!existsSync(EVIDENCE_FILE)) {
    return [];
  }

  try {
    const content = readFileSync(EVIDENCE_FILE, 'utf-8');
    const chains = JSON.parse(content);
    
    return Object.values(chains).filter(chain => 
      chain.chain.some(e => e.type === type)
    );
  } catch (err) {
    console.error(`[Evidence] Error searching evidence: ${err.message}`);
    return [];
  }
}

/**
 * Get memories by source
 */
export function evidenceFindBySource(sourceId) {
  if (!existsSync(EVIDENCE_FILE)) {
    return [];
  }

  try {
    const content = readFileSync(EVIDENCE_FILE, 'utf-8');
    const chains = JSON.parse(content);
    
    return Object.values(chains).filter(chain => 
      chain.chain.some(e => e.source_id === sourceId)
    );
  } catch (err) {
    console.error(`[Evidence] Error searching evidence: ${err.message}`);
    return [];
  }
}

/**
 * Get highest confidence evidence for a memory
 */
export function evidenceGetHighestConfidence(memoryId) {
  const chain = getEvidenceChain(memoryId);
  if (!chain || chain.chain.length === 0) {
    return null;
  }

  return chain.chain.reduce((highest, current) => 
    current.confidence > highest.confidence ? current : highest
  );
}

/**
 * Get all evidence chains with high confidence
 */
export function evidenceGetHighConfidence(minConfidence = 0.8) {
  if (!existsSync(EVIDENCE_FILE)) {
    return [];
  }

  try {
    const content = readFileSync(EVIDENCE_FILE, 'utf-8');
    const chains = JSON.parse(content);
    
    return Object.values(chains).filter(chain => 
      chain.chain.some(e => e.confidence >= minConfidence)
    );
  } catch (err) {
    console.error(`[Evidence] Error filtering evidence: ${err.message}`);
    return [];
  }
}

/**
 * Export evidence for backup
 */
export function evidenceExport() {
  if (!existsSync(EVIDENCE_FILE)) {
    return null;
  }
  return readFileSync(EVIDENCE_FILE, 'utf-8');
}

/**
 * Import evidence from backup
 */
export function evidenceImport(evidenceContent) {
  if (!evidenceContent) return;
  
  try {
    writeFileSync(EVIDENCE_FILE, evidenceContent);
  } catch (err) {
    console.error(`[Evidence] Error importing evidence: ${err.message}`);
  }
}

/**
 * Get evidence statistics
 */
export function evidenceStats() {
  if (!existsSync(EVIDENCE_FILE)) {
    return { total: 0, byType: {}, avgConfidence: 0 };
  }

  try {
    const content = readFileSync(EVIDENCE_FILE, 'utf-8');
    const chains = JSON.parse(content);
    
    const byType = {};
    let totalConfidence = 0;
    let totalEvidence = 0;

    Object.values(chains).forEach(chain => {
      chain.chain.forEach(e => {
        byType[e.type] = (byType[e.type] || 0) + 1;
        totalConfidence += e.confidence;
        totalEvidence++;
      });
    });

    return {
      total: Object.keys(chains).length,
      byType,
      avgConfidence: totalEvidence > 0 ? totalConfidence / totalEvidence : 0
    };
  } catch (err) {
    console.error(`[Evidence] Error calculating stats: ${err.message}`);
    return { total: 0, byType: {}, avgConfidence: 0 };
  }
}
