/**
 * version_tools.js — MCP Tools for Memory Versioning (v2.7.0)
 * Part of Task #2: 完整修订历史
 *
 * Implements MCP tools:
 * - memory_version_list:   查看记忆版本历史
 * - memory_version_diff:    比较两个版本差异
 * - memory_version_restore: 恢复到指定版本
 *
 * Tools follow the existing pattern in the codebase and are
 * backwards-compatible with the v2.6.0 tooling interface.
 */
import {
  getMemoryVersions,
  getMemoryVersion,
  restoreMemoryVersion,
  getVersionStats,
  compareMemoryVersions,
  getMemoryVersionCount,
  getMemory,
} from '../storage.js';

/**
 * Tool: memory_version_list
 * 列出记忆的版本历史，或全局版本统计
 *
 * @param {{ memoryId?: string, limit?: number, offset?: number }} opts
 */
export function memoryVersionListTool({ memoryId, limit = 10, offset = 0 } = {}) {
  try {
    if (!memoryId) {
      // 无 memoryId → 返回全局统计
      const stats = getVersionStats();
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            totalMemories: stats.totalMemories,
            totalVersions: stats.totalVersions,
            maxVersionsPerMemory: 10,
            memoriesWithVersions: stats.memoryCounts,
          }, null, 2),
        }],
      };
    }

    let versions = getMemoryVersions(memoryId);

    // 分页
    const total = versions.length;
    versions = versions.slice(offset, offset + limit);

    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          memoryId,
          total,
          offset,
          limit,
          versions,
        }, null, 2),
      }],
    };
  } catch (err) {
    return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
  }
}

/**
 * Tool: memory_version_diff
 * 比较两个版本的差异
 *
 * @param {{ memoryId: string, versionId1?: string, versionId2?: string }} opts
 */
export function memoryVersionDiffTool({ memoryId, versionId1, versionId2 } = {}) {
  try {
    if (!memoryId) throw new Error('memoryId is required');

    const versions = getMemoryVersions(memoryId);
    if (versions.length === 0) {
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({ error: `No version history for memory ${memoryId}` }, null, 2),
        }],
        isError: true,
      };
    }

    // 单 versionId → 与上一个版本比较
    if (versionId1 && !versionId2) {
      const idx = versions.findIndex((v) => v.versionId === versionId1);
      if (idx === -1) throw new Error(`Version ${versionId1} not found`);
      if (idx === 0) {
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              memoryId,
              note: 'First version, comparing with empty',
              fromVersion: null,
              toVersion: versions[0],
              diff: { addedCount: 1, removedCount: 0, added: ['[initial version]'], removed: [] },
            }, null, 2),
          }],
        };
      }
      const v2 = versions[idx];
      const v1 = versions[idx - 1];
      const diff = compareMemoryVersions(memoryId, v1.versionId, v2.versionId);
      return {
        content: [{ type: 'text', text: JSON.stringify(diff, null, 2) }],
      };
    }

    // 两个 versionId → 指定版本比较
    if (!versionId1 || !versionId2) {
      throw new Error('versionId1 and versionId2 are both required for diff');
    }

    const diff = compareMemoryVersions(memoryId, versionId1, versionId2);
    return {
      content: [{ type: 'text', text: JSON.stringify(diff, null, 2) }],
    };
  } catch (err) {
    return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
  }
}

/**
 * Tool: memory_version_restore
 * 恢复到指定版本
 *
 * @param {{ memoryId: string, versionId?: string, preview?: boolean }} opts
 */
export function memoryVersionRestoreTool({ memoryId, versionId, preview } = {}) {
  try {
    if (!memoryId) throw new Error('memoryId is required');

    const memory = getMemory(memoryId);
    if (!memory) {
      return {
        content: [{ type: 'text', text: JSON.stringify({ error: `Memory ${memoryId} not found` }, null, 2) }],
        isError: true,
      };
    }

    const versions = getMemoryVersions(memoryId);

    // preview 模式
    if (preview) {
      const target = versionId
        ? versions.find((v) => v.versionId === versionId)
        : versions[versions.length - 1];

      if (!target) {
        return {
          content: [{ type: 'text', text: JSON.stringify({ error: `Version ${versionId || 'latest'} not found` }, null, 2) }],
          isError: true,
        };
      }

      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            preview: true,
            memoryId,
            current: {
              text: memory.text?.slice(0, 200),
              updated_at: memory.updated_at,
              versionCount: versions.length,
            },
            restoreTo: {
              versionId: target.versionId,
              timestamp: target.timestamp,
              changeType: target.changeType,
            },
            hint: 'Set preview: false to actually restore',
          }, null, 2),
        }],
      };
    }

    // 实际恢复
    if (!versionId) {
      return {
        content: [{ type: 'text', text: JSON.stringify({ error: 'versionId is required (or use preview: true)' }, null, 2) }],
        isError: true,
      };
    }

    const result = restoreMemoryVersion(memoryId, versionId);
    return {
      content: [{ type: 'text', text: JSON.stringify(result, null, 2) }],
    };
  } catch (err) {
    return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
  }
}

export default {
  memoryVersionListTool,
  memoryVersionDiffTool,
  memoryVersionRestoreTool,
};
