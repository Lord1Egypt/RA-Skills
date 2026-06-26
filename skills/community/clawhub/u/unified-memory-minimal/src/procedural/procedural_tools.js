import { z } from 'zod';
/**
 * Procedural Memory Tools
 *
 * Tool wrappers for procedural memory operations.
 * These are the public API for the memory system.
 */

import {
  loadProcedurals,
  addProcedure,
  findProcedure,
  deleteProcedure,
  touchProcedure,
} from './procedural_store.js';

/**
 * Add a new procedural memory
 * @param {string} name - procedure name
 * @param {Array<{step: number, action: string, tool?: string|null}>} steps
 * @param {string} trigger - regex trigger pattern
 * @returns {object} result with the created procedural
 */
export function memory_procedure_add({ name, steps, trigger }) {
  try {
    const proc = addProcedure(name, steps, trigger);
    return {
      ok: true,
      procedure: proc,
    };
  } catch (err) {
    return { ok: false, error: err.message };
  }
}

/**
 * Find procedurals matching a trigger
 * @param {string} trigger - text to match against trigger patterns
 * @returns {object} result with matching procedurals
 */
export function memory_procedure_find({ trigger }) {
  try {
    const matches = findProcedure(trigger);
    return {
      ok: true,
      matches,
      count: matches.length,
    };
  } catch (err) {
    return { ok: false, error: err.message };
  }
}

/**
 * List all procedural memories
 * @returns {object} result with all procedurals
 */
export function memory_procedure_list() {
  try {
    const procedurals = loadProcedurals();
    return {
      ok: true,
      procedurals,
      count: procedurals.length,
    };
  } catch (err) {
    return { ok: false, error: err.message };
  }
}

/**
 * Delete a procedural by id
 * @param {string} id
 * @returns {object} result
 */
export function memory_procedure_delete({ id }) {
  try {
    const deleted = deleteProcedure(id);
    return { ok: deleted, deleted: id };
  } catch (err) {
    return { ok: false, error: err.message };
  }
}

/**
 * Record usage of a procedural (increment counter + update timestamp)
 * @param {string} id
 */
export function memory_procedure_touch({ id }) {
  try {
    touchProcedure(id);
    return { ok: true };
  } catch (err) {
    return { ok: false, error: err.message };
  }
}

export function registerProceduralTools(server) {
  server.registerTool('memory_procedure_add', {
    description: 'Add a new procedural memory (how-to steps for a task).',
    inputSchema: z.object({
      name: z.string().describe('Procedure name'),
      steps: z.array(z.object({ step: z.number(), action: z.string(), tool: z.string().nullable().optional() })).describe('Ordered list of steps'),
      trigger: z.string().optional().describe('Regex pattern to auto-trigger this procedure'),
    }),
  }, memory_procedure_add);

  server.registerTool('memory_procedure_find', {
    description: 'Find procedural memories matching a trigger keyword or pattern.',
    inputSchema: z.object({
      trigger: z.string().describe('Keyword or pattern to match against triggers'),
    }),
  }, memory_procedure_find);

  server.registerTool('memory_procedure_list', {
    description: 'List all stored procedural memories.',
    inputSchema: z.object({}),
  }, memory_procedure_list);

  server.registerTool('memory_procedure_delete', {
    description: 'Delete a procedural memory by ID.',
    inputSchema: z.object({
      id: z.string().describe('Procedural memory ID to delete'),
    }),
  }, memory_procedure_delete);
}
