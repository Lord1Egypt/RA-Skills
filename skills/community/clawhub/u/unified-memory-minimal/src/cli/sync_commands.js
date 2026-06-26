/**
 * sync_commands.js - Extended CLI commands for distributed sync
 * 
 * Extends the CLI with peer management and sync control:
 *   memory sync --add-peer <path>
 *   memory sync --list-peers
 *   memory sync --sync-now
 *   memory sync --watch
 *   memory sync --remove-peer <peer-id>
 *   memory sync --ping-peers
 *   memory sync --peer-status <peer-id>
 */

import { existsSync, mkdirSync } from 'fs';
import { join } from 'path';
import { addPeer, removePeer, listPeers, getPeer, pingPeer, pingAllPeers } from '../collab/peer_registry.js';
import { getSyncWatcher, startSyncWatcher, stopSyncWatcher } from '../sync_watcher.js';

const HOME = process.env.HOME || '/root';
const MEMORY_DIR = join(HOME, '.openclaw/workspace/memory');
const SHARED_DIR = join(MEMORY_DIR, 'shared');

// Ensure shared directory exists
function ensureShared() {
  if (!existsSync(SHARED_DIR)) mkdirSync(SHARED_DIR, { recursive: true });
}

/**
 * Parse sync sub-commands from CLI args
 * @param {string[]} args
 * @returns {object}
 */
export function parseSyncArgs(args) {
  const cmd = {
    subcmd: null,
    peerId: null,
    path: null,
    json: false,
    _unknown: []
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    switch (arg) {
      case '--add-peer':
      case '-a':
        cmd.subcmd = 'add-peer';
        cmd.path = args[++i] || null;
        break;
      case '--remove-peer':
      case '-r':
        cmd.subcmd = 'remove-peer';
        cmd.peerId = args[++i] || null;
        break;
      case '--list-peers':
      case '-l':
        cmd.subcmd = 'list-peers';
        break;
      case '--ping-peers':
      case '-p':
        cmd.subcmd = 'ping-peers';
        break;
      case '--peer-status':
      case '-s':
        cmd.subcmd = 'peer-status';
        cmd.peerId = args[++i] || null;
        break;
      case '--sync-now':
        cmd.subcmd = 'sync-now';
        break;
      case '--watch':
      case '-w':
        cmd.subcmd = 'watch';
        break;
      case '--stop':
        cmd.subcmd = 'stop-watcher';
        break;
      case '--json':
        cmd.json = true;
        break;
      default:
        if (!arg.startsWith('-')) cmd._unknown.push(arg);
    }
  }
  return cmd;
}

/**
 * Execute sync command
 * @param {object} cmd
 * @returns {object}
 */
export async function execSyncCommand(cmd) {
  ensureShared();

  switch (cmd.subcmd) {
    case 'add-peer': {
      if (!cmd.path) return { error: 'Usage: memory sync --add-peer <path-or-url>' };
      const id = `peer_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 6)}`;
      const type = cmd.path.startsWith('http') ? 'remote' : 'local';
      const result = addPeer(id, cmd.path, { type });
      if (cmd.json) return { type: 'json', data: result };
      return {
        type: 'text',
        text: result.success
          ? `✅ Peer added: ${id} (${type}) → ${cmd.path}`
          : `⚠️ ${result.reason}: ${id}`
      };
    }

    case 'remove-peer': {
      if (!cmd.peerId) return { error: 'Usage: memory sync --remove-peer <peer-id>' };
      const result = removePeer(cmd.peerId);
      if (cmd.json) return { type: 'json', data: result };
      return {
        type: 'text',
        text: result.success
          ? `✅ Peer removed: ${cmd.peerId}`
          : `⚠️ ${result.reason}`
      };
    }

    case 'list-peers': {
      const peers = listPeers();
      if (cmd.json) return { type: 'json', data: peers };
      if (peers.length === 0) {
        return { type: 'text', text: '📋 No peers registered. Use --add-peer <path> to add one.' };
      }
      const lines = [`📋 Registered peers (${peers.length}):`];
      for (const p of peers) {
        const statusIcon = p.status === 'online' ? '🟢' : p.status === 'offline' ? '🔴' : '⚪';
        lines.push(`   ${statusIcon} ${p.peer_id} [${p.type}] ${p.path}`);
        lines.push(`      status: ${p.status} | priority: ${p.priority} | enabled: ${p.enabled}`);
        if (p.last_ping) lines.push(`      last ping: ${p.last_ping}`);
      }
      return { type: 'text', text: lines.join('\n') };
    }

    case 'ping-peers': {
      const peers = listPeers();
      if (peers.length === 0) {
        return { type: 'text', text: '📋 No peers to ping.' };
      }
      const results = await pingAllPeers();
      if (cmd.json) return { type: 'json', data: results };
      const lines = [`🏓 Ping results (${results.online}/${results.total} online):`];
      for (const r of results.results) {
        const icon = r.success ? '🟢' : '🔴';
        lines.push(`   ${icon} ${r.peer_id}: ${r.status}${r.latency_ms !== null ? ` (${r.latency_ms}ms)` : ''}`);
      }
      return { type: 'text', text: lines.join('\n') };
    }

    case 'peer-status': {
      if (!cmd.peerId) return { error: 'Usage: memory sync --peer-status <peer-id>' };
      const peer = getPeer(cmd.peerId);
      if (!peer) return { error: `Peer not found: ${cmd.peerId}` };
      const pingResult = await pingPeer(cmd.peerId);
      if (cmd.json) return { type: 'json', data: { ...peer, ping: pingResult } };
      const lines = [
        `📊 Peer status: ${cmd.peerId}`,
        `   Type: ${peer.type} | Path: ${peer.path}`,
        `   Status: ${peer.status} | Enabled: ${peer.enabled} | Priority: ${peer.priority}`,
        `   Added: ${peer.added_at}`,
        `   Last ping: ${peer.last_ping || 'never'} | Last sync: ${peer.last_sync || 'never'}`,
        `   Ping: ${pingResult.success ? '✅ online' : '❌ offline'}${pingResult.latency_ms !== null ? ` (${pingResult.latency_ms}ms)` : ''}`
      ];
      return { type: 'text', text: lines.join('\n') };
    }

    case 'sync-now': {
      const watcher = getSyncWatcher();
      watcher.forceSync();
      const status = watcher.getStatus();
      if (cmd.json) return { type: 'json', data: status };
      return {
        type: 'text',
        text: `🔄 Force sync triggered.\n   Watcher: ${status.running ? 'running' : 'stopped'}\n   Memory count: ${status.last_stats?.memoryCount || 0}`
      };
    }

    case 'watch': {
      const watcher = startSyncWatcher();
      const status = watcher.getStatus();
      if (!status.running) {
        return { type: 'text', text: `❌ Watcher failed to start: ${MEMORY_DIR}/memories.json not found` };
      }
      watcher.on('sync:triggered', (data) => {
        process.stdout.write(`\n🔔 Sync triggered (${data.type}): ${data.stats.memoryCount} memories\n`);
      });
      watcher.on('watcher:error', (err) => {
        process.stderr.write(`\n⚠️ Watcher error: ${err.error}\n`);
      });
      if (cmd.json) return { type: 'json', data: status };
      return {
        type: 'text',
        text: `👁️ Watcher started.\n   File: ${MEMORY_DIR}/memories.json\n   Debounce: ${status.debounce_ms}ms\n   Press Ctrl+C to stop.`
      };
    }

    case 'stop-watcher': {
      stopSyncWatcher();
      if (cmd.json) return { type: 'json', data: { running: false } };
      return { type: 'text', text: '✅ Watcher stopped.' };
    }

    default: {
      return {
        type: 'text',
        text: `🔄 Sync commands:\n` +
          `   --add-peer <path>     Add a peer node\n` +
          `   --remove-peer <id>    Remove a peer node\n` +
          `   --list-peers          List all registered peers\n` +
          `   --ping-peers          Ping all peers\n` +
          `   --peer-status <id>    Show peer status\n` +
          `   --sync-now            Force an immediate sync\n` +
          `   --watch               Start file watcher mode\n` +
          `   --stop                Stop the watcher\n` +
          `   --json                Output as JSON`
      };
    }
  }
}

export default { parseSyncArgs, execSyncCommand };
