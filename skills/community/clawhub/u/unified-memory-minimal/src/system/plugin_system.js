/**
 * Memory Plugin System - 插件系统
 * 
 * Ported from memory_plugin_system.py
 */

import { existsSync, readdirSync, readFileSync, writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';

const HOME = process.env.HOME || '/root';
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const PLUGIN_DIR = join(MEMORY_DIR, 'plugins');
const PLUGIN_CONFIG_FILE = join(PLUGIN_DIR, 'plugins.json');

// ============================================================
// Plugin System
// ============================================================

export class PluginManager {
  constructor() {
    mkdirSync(PLUGIN_DIR, { recursive: true });
    this.pluginsFile = join(PLUGIN_DIR, 'plugins.json');
    this.plugins = this._loadPlugins();
  }

  _loadPlugins() {
    if (existsSync(this.pluginsFile)) {
      try { return JSON.parse(readFileSync(this.pluginsFile, 'utf-8')); } catch { /* ignore */ }
    }
    return { plugins: {}, hooks: {} };
  }

  _savePlugins() {
    writeFileSync(this.pluginsFile, JSON.stringify(this.plugins, null, 2), 'utf-8');
  }

  /**
   * Register a plugin
   * @param {string} pluginId
   * @param {object} plugin
   */
  register(pluginId, plugin) {
    this.plugins.plugins[pluginId] = {
      ...plugin,
      id: pluginId,
      enabled: true,
      registered_at: new Date().toISOString()
    };
    this._savePlugins();
    return { success: true };
  }

  /**
   * Enable a plugin
   * @param {string} pluginId
   */
  enable(pluginId) {
    if (this.plugins.plugins[pluginId]) {
      this.plugins.plugins[pluginId].enabled = true;
      this._savePlugins();
    }
    return { success: true };
  }

  /**
   * Disable a plugin
   * @param {string} pluginId
   */
  disable(pluginId) {
    if (this.plugins.plugins[pluginId]) {
      this.plugins.plugins[pluginId].enabled = false;
      this._savePlugins();
    }
    return { success: true };
  }

  /**
   * Register a hook
   * @param {string} hookName
   * @param {string} pluginId
   * @param {string} handler
   */
  registerHook(hookName, pluginId, handler) {
    if (!this.plugins.hooks[hookName]) this.plugins.hooks[hookName] = [];
    this.plugins.hooks[hookName].push({ pluginId, handler });
    this._savePlugins();
  }

  /**
   * Trigger a hook
   * @param {string} hookName
   * @param {object} data
   */
  async triggerHook(hookName, data) {
    const hooks = this.plugins.hooks[hookName] || [];
    const results = [];
    for (const hook of hooks) {
      const plugin = this.plugins.plugins[hook.pluginId];
      if (plugin && plugin.enabled) {
        results.push({ pluginId: hook.pluginId, result: data });
      }
    }
    return results;
  }

  listPlugins() {
    return Object.values(this.plugins.plugins);
  }

  getPlugin(pluginId) {
    return this.plugins.plugins[pluginId] || null;
  }

  getStatus() {
    const all = Object.values(this.plugins.plugins);
    const enabled = all.filter(p => p.enabled);
    return {
      total: all.length,
      enabled: enabled.length,
      plugins: all.map(p => ({ id: p.id, name: p.name, enabled: p.enabled }))
    };
  }
}

export default { PluginManager };
