/**
 * Reading Notes Skill
 * Expand reading insights into detailed notes and reflections
 * 
 * SAFE VERSION: No external API calls, no filesystem access, pure local processing
 */

import { Skill } from 'openclaw';

export interface ReadingNotesOptions {
  insight: string;
  depth?: 'brief' | 'detailed' | 'comprehensive';
  includeConnections?: boolean;
}

/**
 * Safe template-based reading notes expansion
 * 
 * This implementation uses only local templates and does NOT:
 * - Call external APIs
 * - Access filesystem
 * - Require API keys or secrets
 * - Send user data outside the local environment
 */
export declare function expandReadingNotes(options: ReadingNotesOptions): Promise<string>;

/**
 * Local concept suggestion (no external search)
 */
export declare function suggestRelatedConcepts(insight: string, limit?: number): Promise<string[]>;

/**
 * Generate note-taking prompts for the insight
 */
export declare function generateNotePrompts(insight: string): Promise<string[]>;

/**
 * Main skill handler for OpenClaw - SAFE VERSION
 */
export declare const readingNotesSkill: Skill;

export default readingNotesSkill;