/**
 * Modular Entry Points Index
 * Re-exports all modular entry files for structured imports
 * Part of God Object refactoring: splits 3783-line src/index.js into focused modules
 *
 * Structure:
 * - wal-tools: WAL tool registration
 * - evidence-tools: Evidence chain tool registration
 * - organize-tools: Memory organization tool registration
 * - transcript-tools: Transcript-first tool registration
 * - scene-tools: Scene block & pipeline tool registration
 * - system-tools: Cleaner, embedding, benchmark, entity, plugin tool registrations
 */

export { registerWALTools } from './wal-tools.js';
export { registerEvidenceTools } from './evidence-tools.js';
export { registerOrganizeTools } from './organize-tools.js';
export { registerTranscriptFirstTools } from './transcript-tools.js';
export { registerSceneBlockTools, registerPipelineTools } from './scene-tools.js';
export { registerCleanerTools, registerLocalEmbeddingTools, registerBenchmarkTools, registerEntityTools, registerPluginToolsInline } from './system-tools.js';
