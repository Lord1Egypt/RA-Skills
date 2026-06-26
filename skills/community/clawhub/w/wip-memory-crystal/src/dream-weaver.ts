// memory-crystal/dream-weaver.ts — Memory Crystal integration for Dream Weaver.
// Thin wrapper that imports the canonical engine from dream-weaver-protocol
// and adds Memory Crystal infrastructure: crystal.db embedding, crystal_remember,
// LDM path resolution.
//
// The protocol repo is the source of truth for HOW consolidation works.
// This file is the bridge between the protocol and Memory Crystal's plumbing.

import {
  runDreamWeaver as runProtocol,
  type DreamWeaverOptions,
  type DreamWeaverResult,
  type DreamWeaverHooks,
} from 'dream-weaver-protocol';
import { Crystal, resolveConfig, type Chunk } from './core.js';
import { ldmPaths } from './ldm.js';

export type { DreamWeaverOptions, DreamWeaverResult } from 'dream-weaver-protocol';

/** Run Dream Weaver with Memory Crystal integration.
 *  Wraps the protocol engine with crystal.db embedding and crystal_remember hooks. */
export async function runDreamWeaver(options: DreamWeaverOptions): Promise<DreamWeaverResult> {
  const paths = ldmPaths(options.agentId);
  const stateDir = paths.state;

  // Default paths from LDM if not provided
  const resolvedOptions: DreamWeaverOptions = {
    ...options,
    transcriptsDir: options.transcriptsDir || paths.transcripts,
    outputDir: options.outputDir || paths.agentRoot,
  };

  // Set up hooks for crystal.db integration
  const hooks: DreamWeaverHooks = {
    async onJournalWritten(journalPath, journalText, agentId) {
      try {
        const config = resolveConfig();
        const crystal = new Crystal(config);
        await crystal.init();

        const chunks: Chunk[] = [{
          text: journalText,
          role: 'assistant' as const,
          source_type: 'journal',
          source_id: `dream-weaver:${agentId}:${new Date().toISOString().slice(0, 10)}`,
          agent_id: agentId,
          token_count: Math.ceil(journalText.length / 4),
          created_at: new Date().toISOString(),
        }];

        await crystal.ingest(chunks);
        if ('close' in crystal) (crystal as any).close();
      } catch {} // Embedding failures are non-fatal
    },

    async onMemoryExtracted(text, category) {
      try {
        const config = resolveConfig();
        const crystal = new Crystal(config);
        await crystal.init();
        await crystal.remember(text, category as any);
        if ('close' in crystal) (crystal as any).close();
      } catch {} // Individual memory failures are non-fatal
    },
  };

  return runProtocol(resolvedOptions, hooks, stateDir);
}
