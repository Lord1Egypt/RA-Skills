/**
 * Plugin Manager - Core plugin system for Unified Memory
 * 
 * Provides a pluggable architecture where plugins can hook into:
 * - beforeSearch / afterSearch
 * - beforeWrite / afterWrite  
 * - beforeRead / afterRead
 * - onMemoryAccess
 * - onConflictDetected
 * 
 * @module plugin/plugin_manager
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import crypto from 'crypto';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const HOME = process.env.HOME || '/root';
const PLUGIN_DIR = join(HOME, '.openclaw', 'workspace', 'memory', 'plugins');
const PLUGIN_REGISTRY_FILE = join(PLUGIN_DIR, 'registry.json');

// ============ Plugin Interface ============

/**
 * @typedef {Object} PluginHook
 * @property {string} name          - Hook name (e.g., 'beforeSearch')
 * @property {Function} handler    - Handler function
 * @property {number} priority     - Execution order (lower = earlier)
 */

/**
 * @typedef {Object} MemoryPlugin
 * @property {string} name         - Plugin name
 * @property {string} version      - Plugin version
 * @property {string} description   - Plugin description
 * @property {string} author       - Plugin author
 * @property {Object} hooks        - Hook implementations
 * @property {Object} config       - Plugin-specific config
 * @property {boolean} enabled     - Is plugin active
 * @property {string} [path]       - Plugin file path
 */

// ============ Built-in Plugins ============

/**
 * Knowledge Graph Enrichment Plugin
 * Adds entity/relation context to search results
 */
const kgEnrichPlugin = {
  name: 'kg-enrich',
  version: '1.0.0',
  description: 'Enriches search results with knowledge graph context',
  author: 'unified-memory',
  enabled: true,
  hooks: {
    afterSearch: async (results, context) => {
      // Import here to avoid circular deps
      const { searchContext } = await import('../graph/graph.js').catch(() => ({ searchContext: null }));
      if (!searchContext || results.length === 0) return results;
      
      try {
        const query = context?.query || '';
        const kgContext = searchContext(query, 3);
        
        // Attach KG context to each result
        return results.map(r => ({
          ...r,
          _kgContext: {
            entities: kgContext.entities?.slice(0, 5) || [],
            relations: kgContext.relations?.slice(0, 3) || [],
          }
        }));
      } catch {
        return results;
      }
    },
    beforeWrite: async (memory, context) => {
      // Extract and store entities when writing memory
      const { extractEntities } = await import('../graph/entity.js').catch(() => ({ extractEntities: null }));
      if (!extractEntities) return memory;
      
      try {
        const entities = await extractEntities(memory.text || '', { useLLM: false });
        return {
          ...memory,
          _extractedEntities: entities,
        };
      } catch {
        return memory;
      }
    },
  },
  config: {
    maxEntities: 10,
    includeRelations: true,
  },
};

/**
 * Deduplication Plugin
 * Prevents duplicate memories from being written
 */
const dedupPlugin = {
  name: 'dedup',
  version: '1.0.0',
  description: 'Deduplicates memories before write',
  author: 'unified-memory',
  enabled: true,
  hooks: {
    beforeWrite: async (memory, context) => {
      const { getAllMemories } = await import('../storage.js').catch(() => ({ getAllMemories: null }));
      if (!getAllMemories) return memory;
      
      try {
        const existing = getAllMemories();
        const text = (memory.text || '').toLowerCase().trim();
        
        // Check for similar memories
        for (const m of existing) {
          const existingText = (m.text || '').toLowerCase().trim();
          const similarity = calculateSimilarity(text, existingText);
          
          if (similarity > 0.85) {
            // High similarity - return existing ID to prevent duplicate
            return {
              ...memory,
              _dedupWarning: `Similar memory exists: ${m.id}`,
              _similarity: similarity,
              _existingId: m.id,
            };
          }
        }
      } catch {
        // Ignore dedup errors
      }
      
      return memory;
    },
  },
  config: {
    similarityThreshold: 0.85,
    checkOnWrite: true,
  },
};

/**
 * Revision Tracking Plugin
 * Automatically tracks memory revisions
 */
const revisionPlugin = {
  name: 'revision',
  version: '1.0.0',
  description: 'Tracks memory revisions and conflicts',
  author: 'unified-memory',
  enabled: true,
  hooks: {
    afterWrite: async (memory, context) => {
      const { recordRevision } = await import('../revision_manager_enhanced.js').catch(() => ({ recordRevision: null }));
      if (!recordRevision) return memory;
      
      try {
        await recordRevision(
          memory.id,
          memory.text,
          context?.isUpdate ? 'updated' : 'created',
          'plugin',
          null,
          'approved'
        );
      } catch {
        // Ignore revision errors
      }
      
      return memory;
    },
    onConflictDetected: async (localMemory, remoteMemory) => {
      console.log(`[RevisionPlugin] Conflict detected between ${localMemory.id} and ${remoteMemory.id}`);
      return {
        resolution: 'merged',
        strategy: 'last-write-wins',
      };
    },
  },
  config: {
    autoMerge: true,
    keepHistory: true,
  },
};

const BUILTIN_PLUGINS = {
  'kg-enrich': kgEnrichPlugin,
  'dedup': dedupPlugin,
  'revision': revisionPlugin,
};

// ============ Plugin Registry ============

/**
 * @type {Map<string, MemoryPlugin>}
 */
const pluginCache = new Map();

/**
 * Load plugin registry from disk
 */
function loadRegistry() {
  if (!existsSync(PLUGIN_REGISTRY_FILE)) {
    // Initialize with built-in plugins
    const initial = {
      version: '1.0.0',
      plugins: {},
      builtins: Object.keys(BUILTIN_PLUGINS),
    };
    saveRegistry(initial);
    return initial;
  }
  
  try {
    return JSON.parse(readFileSync(PLUGIN_REGISTRY_FILE, 'utf-8'));
  } catch {
    return { version: '1.0.0', plugins: {}, builtins: Object.keys(BUILTIN_PLUGINS) };
  }
}

/**
 * Save plugin registry to disk
 */
function saveRegistry(registry) {
  if (!existsSync(PLUGIN_DIR)) {
    mkdirSync(PLUGIN_DIR, { recursive: true });
  }
  writeFileSync(PLUGIN_REGISTRY_FILE, JSON.stringify(registry, null, 2), 'utf-8');
}

/**
 * Generate plugin ID
 */
function generatePluginId(name) {
  return `plugin_${crypto.randomBytes(4).toString('hex')}`;
}

// ============ Core Functions ============

/**
 * Get all registered plugins (including builtins)
 */
export async function getPlugins() {
  const registry = loadRegistry();
  const plugins = { ...BUILTIN_PLUGINS };
  
  // Load external plugins
  for (const [name, meta] of Object.entries(registry.plugins)) {
    if (meta.enabled && !BUILTIN_PLUGINS[name]) {
      try {
        const pluginPath = meta.path || join(PLUGIN_DIR, `${name}.js`);
        if (existsSync(pluginPath)) {
          const mod = await import(pluginPath);
          plugins[name] = { ...mod.default || mod, ...meta };
        }
      } catch (err) {
        console.warn(`[PluginManager] Failed to load plugin ${name}: ${err.message}`);
      }
    }
  }
  
  return plugins;
}

/**
 * Get plugin by name
 */
export async function getPlugin(name) {
  const plugins = await getPlugins();
  return plugins[name] || null;
}

/**
 * Enable a plugin
 */
export async function enablePlugin(name) {
  const registry = loadRegistry();
  
  if (BUILTIN_PLUGINS[name]) {
    // Toggle built-in
    if (!registry.builtins.includes(name)) {
      registry.builtins.push(name);
    }
  } else {
    if (!registry.plugins[name]) {
      registry.plugins[name] = { enabled: false };
    }
    registry.plugins[name].enabled = true;
  }
  
  saveRegistry(registry);
  return { success: true, name };
}

/**
 * Disable a plugin
 */
export async function disablePlugin(name) {
  const registry = loadRegistry();
  
  if (BUILTIN_PLUGINS[name]) {
    registry.builtins = registry.builtins.filter(b => b !== name);
  } else if (registry.plugins[name]) {
    registry.plugins[name].enabled = false;
  }
  
  saveRegistry(registry);
  return { success: true, name };
}

/**
 * Register an external plugin
 */
export async function registerPlugin(pluginDef) {
  const registry = loadRegistry();
  const id = pluginDef.name;
  
  registry.plugins[id] = {
    name: pluginDef.name,
    version: pluginDef.version || '1.0.0',
    description: pluginDef.description || '',
    author: pluginDef.author || 'unknown',
    enabled: pluginDef.enabled !== false,
    path: pluginDef.path,
    config: pluginDef.config || {},
    registeredAt: new Date().toISOString(),
  };
  
  saveRegistry(registry);
  return { success: true, id };
}

// ============ Hook Execution ============

/**
 * Execute a hook across all enabled plugins
 */
export async function executeHook(hookName, data, context = {}) {
  const plugins = await getPlugins();
  const results = [];
  
  for (const [name, plugin] of Object.entries(plugins)) {
    if (!plugin.enabled) continue;
    if (!plugin.hooks || !plugin.hooks[hookName]) continue;
    
    try {
      const result = await plugin.hooks[hookName](data, { ...context, plugin: name });
      results.push({ plugin: name, result });
    } catch (err) {
      console.warn(`[PluginManager] Hook ${hookName} failed for ${name}: ${err.message}`);
      results.push({ plugin: name, error: err.message });
    }
  }
  
  return results;
}

/**
 * Execute beforeSearch hooks
 */
export async function beforeSearch(query, context) {
  const results = await executeHook('beforeSearch', query, context);
  // Return modified query from first successful hook
  for (const r of results) {
    if (r.result !== undefined && r.result !== query) {
      return r.result;
    }
  }
  return query;
}

/**
 * Execute afterSearch hooks
 */
export async function afterSearch(results, context) {
  let modified = [...results];
  
  const hookResults = await executeHook('afterSearch', modified, context);
  for (const r of hookResults) {
    if (r.result && Array.isArray(r.result)) {
      modified = r.result;
    }
  }
  
  return modified;
}

/**
 * Execute beforeWrite hooks
 */
export async function beforeWrite(memory, context) {
  let modified = { ...memory };
  
  const hookResults = await executeHook('beforeWrite', modified, context);
  for (const r of hookResults) {
    if (r.result) {
      modified = { ...modified, ...r.result };
    }
  }
  
  return modified;
}

/**
 * Execute afterWrite hooks
 */
export async function afterWrite(memory, context) {
  return executeHook('afterWrite', memory, { ...context, memory });
}

/**
 * Get plugin stats
 */
export async function getPluginStats() {
  const registry = loadRegistry();
  const plugins = await getPlugins();
  
  const enabled = Object.values(plugins).filter(p => p.enabled).length;
  const total = Object.keys(plugins).length;
  
  return {
    total,
    enabled,
    disabled: total - enabled,
    builtins: Object.keys(BUILTIN_PLUGINS),
    external: Object.keys(registry.plugins),
    registry,
  };
}

// ============ Similarity Helper ============

function calculateSimilarity(a, b) {
  if (a === b) return 1;
  if (a.length === 0 || b.length === 0) return 0;
  
  const aWords = new Set(a.split(/\s+/));
  const bWords = new Set(b.split(/\s+/));
  
  let intersection = 0;
  for (const word of aWords) {
    if (bWords.has(word)) intersection++;
  }
  
  const union = aWords.size + bWords.size - intersection;
  return union > 0 ? intersection / union : 0;
}

export default {
  getPlugins,
  getPlugin,
  enablePlugin,
  disablePlugin,
  registerPlugin,
  executeHook,
  beforeSearch,
  afterSearch,
  beforeWrite,
  afterWrite,
  getPluginStats,
};
