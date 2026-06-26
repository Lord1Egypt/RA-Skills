import { AgentConfig } from './types.js';
/**
 * Generate a SPARQL UPDATE to patch agent metadata into a WebID profile.
 * CSS auto-generates a basic profile; we add agent-specific triples.
 */
export declare function buildProfilePatch(config: AgentConfig, webId: string): string;
