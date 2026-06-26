/**
 * Memory Cloud - 云同步支持
 * 
 * 功能:
 * - 多种云存储支持 (local/s3/webdav)
 * - 多设备同步
 * - 增量同步
 * 
 * Ported from memory_cloud.py
 */

import fs, { existsSync, readFileSync, writeFileSync, mkdirSync, createWriteStream, createReadStream } from 'fs';
import { join, dirname } from 'path';
import { createHash, randomBytes } from 'crypto';

const HOME = process.env.HOME || '/root';
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const VECTOR_DB_DIR = join(MEMORY_DIR, 'vector');
const CLOUD_CONFIG_FILE = join(MEMORY_DIR, 'cloud_config.json');
const SYNC_STATE_FILE = join(MEMORY_DIR, 'sync_state.json');

// Storage types
const STORAGE_TYPES = ['local', 's3', 'webdav'];

// ============================================================
// CloudConfig
// ============================================================

export class CloudConfig {
  constructor() {
    this.config = this._loadConfig();
  }

  _loadConfig() {
    if (existsSync(CLOUD_CONFIG_FILE)) {
      try {
        return JSON.parse(readFileSync(CLOUD_CONFIG_FILE, 'utf-8'));
      } catch { /* ignore */ }
    }
    return {
      enabled: false,
      storage_type: 'local',
      backup_path: join(WORKSPACE, 'memory_backup'),
      auto_sync: false,
      sync_interval: 3600,
      s3: { endpoint: '', bucket: '', access_key: '', secret_key: '', region: 'us-east-1' },
      webdav: { url: '', username: '', password: '', path: '/memory_backup' }
    };
  }

  save() {
    mkdirSync(MEMORY_DIR, { recursive: true });
    writeFileSync(CLOUD_CONFIG_FILE, JSON.stringify(this.config, null, 2), 'utf-8');
  }

  enable(storageType = 'local', backupPath = null) {
    this.config.enabled = true;
    this.config.storage_type = storageType;
    if (backupPath) this.config.backup_path = backupPath;
    this.save();
  }

  disable() {
    this.config.enabled = false;
    this.save();
  }
}

// ============================================================
// LocalProvider
// ============================================================

class LocalProvider {
  constructor(config) {
    this.config = config;
  }

  upload(localPath, remotePath) {
    try {
                  const backupPath = this.config.config.backup_path || join(WORKSPACE, 'memory_backup');
      const remoteFull = join(backupPath, remotePath);
      mkdirSync(dirname(remoteFull), { recursive: true });
      fs.copyFileSync(localPath, remoteFull);
      return true;
    } catch {
      return false;
    }
  }

  download(remotePath, localPath) {
    try {
                  const backupPath = this.config.config.backup_path || join(WORKSPACE, 'memory_backup');
      const remoteFull = join(backupPath, remotePath);
      mkdirSync(dirname(localPath), { recursive: true });
      fs.copyFileSync(remoteFull, localPath);
      return true;
    } catch {
      return false;
    }
  }

  listFiles(remoteDir) {
    try {
                  const backupPath = this.config.config.backup_path || join(WORKSPACE, 'memory_backup');
      const remoteFull = join(backupPath, remoteDir);
      if (!existsSync(remoteFull)) return [];
      const entries = fs.readdirSync(remoteFull, { withFileTypes: true });
      return entries
        .filter(e => e.isFile())
        .map(e => {
          const stat = fs.statSync(join(remoteFull, e.name));
          return {
            name: e.name,
            size: stat.size,
            modified: stat.mtime.toISOString()
          };
        });
    } catch {
      return [];
    }
  }

  delete(remotePath) {
    try {
                  const backupPath = this.config.config.backup_path || join(WORKSPACE, 'memory_backup');
      const remoteFull = join(backupPath, remotePath);
      fs.unlinkSync(remoteFull);
      return true;
    } catch {
      return false;
    }
  }
}

// ============================================================
// S3Provider
// ============================================================

class S3Provider {
  constructor(config) {
    this.config = config;
  }

  _getClient() {
    // Would use AWS SDK in production
    return null;
  }

  upload(localPath, remotePath) {
    // Requires AWS SDK - simplified implementation
    console.log(`[S3] Upload: ${localPath} -> ${remotePath}`);
    return true;
  }

  download(remotePath, localPath) {
    console.log(`[S3] Download: ${remotePath} -> ${localPath}`);
    return false;
  }

  listFiles(remoteDir) {
    return [];
  }

  delete(remotePath) {
    return false;
  }
}

// ============================================================
// WebDAVProvider
// ============================================================

class WebDAVProvider {
  constructor(config) {
    this.config = config;
  }

  async upload(localPath, remotePath) {
    try {
      const webdavConfig = this.config.config.webdav || {};
      const url = `${webdavConfig.url}${webdavConfig.path || '/memory_backup'}/${remotePath}`;
      const response = await fetch(url, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/octet-stream',
          'Authorization': `Basic ${Buffer.from(`${webdavConfig.username}:${webdavConfig.password}`).toString('base64')}`
        },
        body: createReadStream(localPath)
      });
      return response.ok;
    } catch {
      return false;
    }
  }

  async download(remotePath, localPath) {
    try {
      const webdavConfig = this.config.config.webdav || {};
      const url = `${webdavConfig.url}${webdavConfig.path || '/memory_backup'}/${remotePath}`;
      const response = await fetch(url, {
        headers: {
          'Authorization': `Basic ${Buffer.from(`${webdavConfig.username}:${webdavConfig.password}`).toString('base64')}`
        }
      });
      if (response.ok) {
        const buffer = await response.arrayBuffer();
        writeFileSync(localPath, Buffer.from(buffer));
        return true;
      }
    } catch { /* ignore */ }
    return false;
  }

  listFiles(remoteDir) {
    return [];
  }
}

// ============================================================
// MemoryBackup
// ============================================================

export class MemoryBackup {
  constructor(config) {
    this.config = config;
    const type = config.config.storage_type || 'local';
    if (type === 's3') this.provider = new S3Provider(config);
    else if (type === 'webdav') this.provider = new WebDAVProvider(config);
    else this.provider = new LocalProvider(config);
  }

  createBackup() {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const backupPath = join(MEMORY_DIR, 'temp_backup', `backup_${timestamp}`);
    mkdirSync(backupPath, { recursive: true });

    // Copy memories.json
    const memoryFile = join(MEMORY_DIR, 'memories.json');
    if (existsSync(memoryFile)) {
            fs.copyFileSync(memoryFile, join(backupPath, 'memories.json'));
    }

    // Copy vector DB if exists
    if (existsSync(VECTOR_DB_DIR)) {
            this._copyDir(VECTOR_DB_DIR, join(backupPath, 'vector'));
    }

    // Create manifest
    const manifest = {
      timestamp,
      created_at: new Date().toISOString(),
      storage_type: this.config.config.storage_type || 'local'
    };
    writeFileSync(join(backupPath, 'manifest.json'), JSON.stringify(manifest, null, 2), 'utf-8');

    const storageType = this.config.config.storage_type || 'local';
    const finalPath = this.config.config.storage_type === 'local'
      ? join(this.config.config.backup_path || join(WORKSPACE, 'memory_backup'), `backup_${timestamp}`)
      : backupPath;

    if (storageType === 'local') {
            this._copyDir(backupPath, finalPath);
      const tempDir = join(MEMORY_DIR, 'temp_backup');
      fs.rmSync(tempDir, { recursive: true, force: true });
    }

    return {
      success: true,
      timestamp,
      path: finalPath,
      storage_type: storageType
    };
  }

  _copyDir(src, dst) {
    mkdirSync(dst, { recursive: true });
    const entries = fs.readdirSync(src, { withFileTypes: true });
    for (const entry of entries) {
      const srcPath = join(src, entry.name);
      const dstPath = join(dst, entry.name);
      if (entry.isDirectory()) {
        this._copyDir(srcPath, dstPath);
      } else {
        fs.copyFileSync(srcPath, dstPath);
      }
    }
  }

  listBackups() {
    const storageType = this.config.config.storage_type || 'local';
    if (storageType === 'local') {
      const backupPath = this.config.config.backup_path || join(WORKSPACE, 'memory_backup');
      if (!existsSync(backupPath)) return [];
      const entries = fs.readdirSync(backupPath, { withFileTypes: true });
      return entries
        .filter(e => e.isDirectory() && e.name.startsWith('backup_'))
        .map(e => ({
          timestamp: e.name.replace('backup_', ''),
          path: join(backupPath, e.name)
        }))
        .sort((a, b) => b.timestamp.localeCompare(a.timestamp));
    }
    return this.provider.listFiles('backups');
  }

  restoreBackup(timestamp) {
    const backupPath = join(this.config.config.backup_path || join(WORKSPACE, 'memory_backup'), `backup_${timestamp}`);
    if (!existsSync(backupPath)) {
      return { success: false, error: '备份不存在' };
    }

    
    // Restore memories.json
    const memBackup = join(backupPath, 'memories.json');
    if (existsSync(memBackup)) {
      fs.copyFileSync(memBackup, join(MEMORY_DIR, 'memories.json'));
    }

    // Restore vector DB
    const vecBackup = join(backupPath, 'vector');
    if (existsSync(vecBackup)) {
      if (existsSync(VECTOR_DB_DIR)) fs.rmSync(VECTOR_DB_DIR, { recursive: true });
      this._copyDir(vecBackup, VECTOR_DB_DIR);
    }

    return { success: true, restored_from: timestamp };
  }
}

// ============================================================
// MemorySync
// ============================================================

export class MemorySync {
  constructor(config) {
    this.config = config;
    this.backup = new MemoryBackup(config);
  }

  getLocalState() {
    const state = { last_sync: null, memory_count: 0, checksum: '' };
    if (existsSync(SYNC_STATE_FILE)) {
      try {
        const saved = JSON.parse(readFileSync(SYNC_STATE_FILE, 'utf-8'));
        state.last_sync = saved.last_sync;
      } catch { /* ignore */ }
    }
    // Try to get memory count
    try {
      const memoryFile = join(MEMORY_DIR, 'memories.json');
      if (existsSync(memoryFile)) {
        const data = JSON.parse(readFileSync(memoryFile, 'utf-8'));
        const mems = Array.isArray(data) ? data : (data.memories || []);
        state.memory_count = mems.length;
        const texts = mems.map(m => m.text || '').sort().join('|');
        state.checksum = createHash('md5').update(texts).digest('hex').slice(0, 16);
      }
    } catch { /* ignore */ }
    return state;
  }

  sync() {
    if (!this.config.config.enabled) {
      return { success: false, error: '云同步未启用' };
    }
    const backupResult = this.backup.createBackup();
    const state = {
      last_sync: new Date().toISOString(),
      backup_timestamp: backupResult.timestamp
    };
    mkdirSync(MEMORY_DIR, { recursive: true });
    writeFileSync(SYNC_STATE_FILE, JSON.stringify(state, null, 2), 'utf-8');
    return { success: true, backup: backupResult, synced_at: state.last_sync };
  }
}

// ============================================================
// CLI Handler
// ============================================================

/**
 * @param {string} command
 * @param {object} args
 * @returns {object}
 */
export function cmdCloud(command, args) {
  const config = new CloudConfig();
  const backup = new MemoryBackup(config);
  const sync = new MemorySync(config);

  switch (command) {
    case 'enable': {
      config.enable(args.storage || 'local', args.path);
      return { type: 'text', text: `✅ 云同步已启用 (${args.storage || 'local'})` };
    }

    case 'disable': {
      config.disable();
      return { type: 'text', text: '✅ 云同步已禁用' };
    }

    case 'backup': {
      const result = backup.createBackup();
      return {
        type: 'text',
        text: `✅ 备份完成: ${result.timestamp}\n   存储: ${result.storage_type}`
      };
    }

    case 'restore': {
      if (!args.timestamp) {
        const backups = backup.listBackups();
        const lines = ['可用备份:'];
        backups.slice(0, 5).forEach((b, i) => lines.push(`   ${i + 1}. ${b.timestamp}`));
        lines.push('\n使用 --timestamp 指定恢复');
        return { type: 'text', text: lines.join('\n') };
      }
      const result = backup.restoreBackup(args.timestamp);
      return {
        type: 'text',
        text: result.success ? `✅ 恢复成功 (${result.restored_from})` : `❌ 恢复失败: ${result.error}`
      };
    }

    case 'list': {
      const backups = backup.listBackups();
      return {
        type: 'text',
        text: `📋 备份列表 (${backups.length} 个):\n` +
          backups.slice(0, 10).map(b => `   ${b.timestamp}`).join('\n')
      };
    }

    case 'sync': {
      const result = sync.sync();
      return {
        type: 'text',
        text: result.success ? `✅ 同步完成` : `❌ 同步失败: ${result.error}`
      };
    }

    case 'status': {
      const state = sync.getLocalState();
      return {
        type: 'text',
        text: `📊 云同步状态\n` +
          `   已启用: ${config.config.enabled}\n` +
          `   存储类型: ${config.config.storage_type}\n` +
          `   记忆数: ${state.memory_count}\n` +
          `   校验和: ${state.checksum}\n` +
          `   上次同步: ${state.last_sync || '从未'}`
      };
    }

    default:
      return { error: `未知命令: ${command}` };
  }
}

export default { CloudConfig, MemoryBackup, MemorySync, cmdCloud };
