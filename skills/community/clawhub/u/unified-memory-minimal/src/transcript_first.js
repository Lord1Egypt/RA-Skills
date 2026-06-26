/**
 * transcript_first.js - Transcript-First Architecture
 * 
 * Implements transcript-first memory system where transcripts are the
 * single source of truth. All memories can be rebuilt from transcripts.
 * 
 * Inspired by Smart Memory's Transcript-First architecture
 */

import { writeFileSync, readFileSync, existsSync, mkdirSync, readdirSync, statSync } from 'fs';
import { join } from 'path';

const HOME = process.env.HOME || '/root';
const MEMORY_DIR = join(HOME, '.openclaw', 'workspace', 'memory');
const TRANSCRIPTS_DIR = join(MEMORY_DIR, 'transcripts');
const TRANSCRIPT_INDEX_FILE = join(TRANSCRIPTS_DIR, 'index.json');

// Ensure transcripts directory exists
if (!existsSync(TRANSCRIPTS_DIR)) {
  mkdirSync(TRANSCRIPTS_DIR, { recursive: true });
}

/**
 * Transcript structure:
 * {
 *   id: string,
 *   type: 'session' | 'chat' | 'message',
 *   source_id: string,
 *   messages: [
 *     {
 *       role: 'user' | 'assistant' | 'system',
 *       content: string,
 *       timestamp: number,
 *       metadata: object
 *     }
 *   ],
 *   created_at: number,
 *   updated_at: number,
 *   memory_count: number,
 *   summary: string
 * }
 */

/**
 * Memory with transcript reference:
 * {
 *   id: string,
 *   text: string,
 *   transcript_id: string,  // ← Reference to source transcript
 *   message_index: number,  // ← Position in transcript
 *   evidence: [...],
 *   ...
 * }
 */

/**
 * Initialize transcript index
 */
function getTranscriptIndex() {
  if (!existsSync(TRANSCRIPT_INDEX_FILE)) {
    return { transcripts: {}, count: 0 };
  }

  try {
    const content = readFileSync(TRANSCRIPT_INDEX_FILE, 'utf-8');
    return JSON.parse(content);
  } catch (err) {
    console.error(`[Transcript-First] Error reading index: ${err.message}`);
    return { transcripts: {}, count: 0 };
  }
}

/**
 * Save transcript index
 */
function saveTranscriptIndex(index) {
  writeFileSync(TRANSCRIPT_INDEX_FILE, JSON.stringify(index, null, 2));
}

/**
 * Add transcript
 */
export function transcriptAdd(transcript) {
  const index = getTranscriptIndex();
  
  const transcriptData = {
    id: transcript.id || `trans_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
    type: transcript.type || 'session',
    source_id: transcript.source_id,
    messages: transcript.messages || [],
    created_at: Date.now(),
    updated_at: Date.now(),
    memory_count: 0,
    summary: transcript.summary || ''
  };

  index.transcripts[transcriptData.id] = transcriptData;
  index.count++;

  // Save transcript file
  const transcriptFile = join(TRANSCRIPTS_DIR, `${transcriptData.id}.json`);
  writeFileSync(transcriptFile, JSON.stringify(transcriptData, null, 2));

  saveTranscriptIndex(index);
  return transcriptData;
}

/**
 * Get transcript by ID
 */
export function transcriptGet(id) {
  const index = getTranscriptIndex();
  const transcriptData = index.transcripts[id];
  
  if (!transcriptData) {
    return null;
  }

  const transcriptFile = join(TRANSCRIPTS_DIR, `${id}.json`);
  if (existsSync(transcriptFile)) {
    return JSON.parse(readFileSync(transcriptFile, 'utf-8'));
  }

  return transcriptData;
}

/**
 * Update transcript
 */
export function transcriptUpdate(id, updates) {
  const transcript = transcriptGet(id);
  if (!transcript) {
    return null;
  }

  Object.assign(transcript, updates);
  transcript.updated_at = Date.now();

  const transcriptFile = join(TRANSCRIPTS_DIR, `${id}.json`);
  writeFileSync(transcriptFile, JSON.stringify(transcript, null, 2));

  const index = getTranscriptIndex();
  index.transcripts[id] = transcript;
  saveTranscriptIndex(index);

  return transcript;
}

/**
 * Delete transcript
 */
export function transcriptDelete(id) {
  const index = getTranscriptIndex();
  
  if (!index.transcripts[id]) {
    return false;
  }

  const transcriptFile = join(TRANSCRIPTS_DIR, `${id}.json`);
  if (existsSync(transcriptFile)) {
    // Don't delete, just mark as deleted
    writeFileSync(transcriptFile + '.deleted', JSON.stringify({
      deletedAt: Date.now(),
      originalFile: transcriptFile
    }));
  }

  delete index.transcripts[id];
  index.count--;
  saveTranscriptIndex(index);

  return true;
}

/**
 * List all transcripts
 */
export function transcriptList() {
  const index = getTranscriptIndex();
  return Object.values(index.transcripts);
}

/**
 * Find transcripts by source
 */
export function transcriptFindBySource(sourceId) {
  const index = getTranscriptIndex();
  return Object.values(index.transcripts).filter(
    t => t.source_id === sourceId
  );
}

/**
 * Rebuild memories from transcript
 */
export function rebuildMemoriesFromTranscript(transcriptId) {
  const transcript = transcriptGet(transcriptId);
  if (!transcript) {
    return { success: false, error: 'Transcript not found' };
  }

  // In a real implementation, this would:
  // 1. Parse transcript messages
  // 2. Extract important information
  // 3. Create memories with transcript references
  // 4. Link evidence chains
  
  const rebuiltMemories = [];
  
  transcript.messages.forEach((message, index) => {
    // Extract potential memories from message
    if (message.content.length > 50) {
      rebuiltMemories.push({
        id: `mem_${transcriptId}_${index}`,
        text: message.content,
        transcript_id: transcriptId,
        message_index: index,
        source: message.role,
        created_at: message.timestamp || Date.now()
      });
    }
  });

  // Update transcript memory count
  transcript.memory_count = rebuiltMemories.length;
  transcriptUpdate(transcriptId, { memory_count: rebuiltMemories.length });

  return {
    success: true,
    transcript_id: transcriptId,
    memories_rebuilt: rebuiltMemories.length,
    memories: rebuiltMemories
  };
}

/**
 * Get all memories for a transcript
 */
export function getMemoriesForTranscript(transcriptId) {
  // In a real implementation, this would query the memory store
  // for memories with transcript_id = transcriptId
  return [];
}

/**
 * Get transcript summary
 */
export function getTranscriptSummary(transcriptId) {
  const transcript = transcriptGet(transcriptId);
  if (!transcript) {
    return null;
  }

  if (transcript.summary) {
    return transcript.summary;
  }

  // Generate summary from messages
  const summary = transcript.messages
    .map(m => m.content)
    .join(' ')
    .substring(0, 200) + '...';

  transcriptUpdate(transcriptId, { summary });
  return summary;
}

/**
 * Get transcript statistics
 */
export function getTranscriptStats() {
  const index = getTranscriptIndex();
  const transcripts = Object.values(index.transcripts);

  return {
    total: index.count,
    byType: transcripts.reduce((acc, t) => {
      acc[t.type] = (acc[t.type] || 0) + 1;
      return acc;
    }, {}),
    totalMemories: transcripts.reduce((acc, t) => acc + t.memory_count, 0),
    avgMemoriesPerTranscript: index.count > 0 
      ? transcripts.reduce((acc, t) => acc + t.memory_count, 0) / index.count 
      : 0
  };
}

/**
 * Export all transcripts
 */
export function exportTranscripts() {
  const index = getTranscriptIndex();
  return Object.values(index.transcripts);
}

/**
 * Import transcripts
 */
export function importTranscripts(transcripts) {
  const index = getTranscriptIndex();
  
  transcripts.forEach(transcript => {
    const transcriptFile = join(TRANSCRIPTS_DIR, `${transcript.id}.json`);
    if (!existsSync(transcriptFile)) {
      writeFileSync(transcriptFile, JSON.stringify(transcript, null, 2));
      index.transcripts[transcript.id] = transcript;
      index.count++;
    }
  });

  saveTranscriptIndex(index);
  return { imported: transcripts.length };
}

/**
 * Verify transcript integrity
 */
export function verifyTranscriptIntegrity() {
  const index = getTranscriptIndex();
  const errors = [];

  Object.keys(index.transcripts).forEach(id => {
    const transcriptFile = join(TRANSCRIPTS_DIR, `${id}.json`);
    
    if (!existsSync(transcriptFile)) {
      errors.push({
        type: 'missing_file',
        transcript_id: id
      });
    }
  });

  return {
    valid: errors.length === 0,
    errors,
    total: index.count,
    missing_files: errors.filter(e => e.type === 'missing_file').length
  };
}

/**
 * Compact transcripts (remove old/deleted)
 */
export function compactTranscripts() {
  const index = getTranscriptIndex();
  const deletedFiles = [];

  Object.keys(index.transcripts).forEach(id => {
    const transcriptFile = join(TRANSCRIPTS_DIR, `${id}.json`);
    const deletedFile = transcriptFile + '.deleted';

    if (existsSync(deletedFile)) {
      // Remove the actual file
      if (existsSync(transcriptFile)) {
        // Don't delete, just mark
      }
      deletedFiles.push(id);
    }
  });

  // Clean up deleted entries
  deletedFiles.forEach(id => {
    delete index.transcripts[id];
  });

  index.count -= deletedFiles.length;
  saveTranscriptIndex(index);

  return {
    compacted: deletedFiles.length,
    deleted_files: deletedFiles
  };
}
