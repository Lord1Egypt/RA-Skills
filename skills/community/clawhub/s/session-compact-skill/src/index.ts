import { Command } from 'commander';
import { loadConfig, loadFromOpenClawConfig } from './compact/config.js';
import {
  compactSession,
  estimateTokenCount,
  shouldCompact,
  getCurrentModel,
  calculateActualTokenUsage
} from './compact/engine.js';
import {
  createSessionManager,
  SessionManager,
  SessionState
} from './compact/session-manager.js';
import { createSessionStore } from './compact/session-store.js';
import {
  ConversationMessage,
  TokenUsage,
  Session,
  createUserMessage,
  createAssistantMessage,
  createToolResultMessage,
  createSystemMessage
} from './compact/types.js';

// Mock session messages (TODO: integrate with actual OpenClaw session storage)
function getCurrentSessionMessages(): Array<{ role: string; content?: string }> {
  return [
    { role: 'user', content: 'Hello, how do I start a new project?' },
    { role: 'assistant', content: 'Sure! Let me help you set up a new project.' },
    { role: 'user', content: 'A TypeScript CLI tool' },
    { role: 'assistant', content: 'Great choice! I will help you set up a TypeScript CLI tool.' },
  ];
}

/**
 * OpenClaw plugin register function.
 */
export function register(api: any) {
  // 从 OpenClaw 配置系统读取配置
  const pluginConfig = api.getConfig?.() || {};
  
  // 调试日志：查看 api.getConfig() 返回的内容
  console.error('[DEBUG] api.getConfig() returned:', JSON.stringify(pluginConfig, null, 2));
  
  // 使用新的 loadFromOpenClawConfig 函数，正确解析配置
  // pluginConfig 可能包含在 plugins.entries 或 skills.entries 中
  const config = loadFromOpenClawConfig(pluginConfig);
  
  console.error('[DEBUG] Final config:', JSON.stringify(config, null, 2));

  // Register CLI commands
  api.registerCli(
    async ({ program }: { program: Command }) => {
      // compact command
      program
        .command('compact')
        .description('Manually compact the current session history to save tokens')
        .option('--force', 'Force compact even if under threshold')
        .action(async (opts: any) => {
          const messages = getCurrentSessionMessages();
          const totalTokens = estimateTokenCount(messages);
          const force = opts?.force === true;

          console.log(`📊 Current session tokens: ${totalTokens}`);
          console.log(`📉 Threshold: ${config.max_tokens}`);

          if (!force && !shouldCompact(messages, config)) {
            console.log('✅ Session is within token limits. No compaction needed.');
            return;
          }

          console.log('🔄 Compacting session...');
          const result = await compactSession(messages, config);

          if (result.removedCount === 0) {
            console.log('⚠️ No messages to compact.');
            return;
          }

          console.log(`✅ Successfully compacted ${result.removedCount} messages.`);
          console.log(`💰 Saved ~${result.savedTokens} tokens.`);
          console.log(`📝 Summary preview:\n${result.formattedSummary.substring(0, 200)}...`);
        });

      // compact-status command
      program
        .command('compact-status')
        .description('Show current session token usage and compression status')
        .action(() => {
          const messages = getCurrentSessionMessages();
          const totalTokens = estimateTokenCount(messages);
          const needsCompact = shouldCompact(messages, config);
          const actualModel = config.model || getCurrentModel();

          console.log('📊 Session Status');
          console.log('────────────────────────────────────');
          console.log(`  Current tokens: ${totalTokens.toLocaleString()}`);
          console.log(`  Threshold:      ${config.max_tokens.toLocaleString()}`);
          console.log(`  Usage:          ${Math.round((totalTokens / config.max_tokens) * 100)}%`);
          console.log(`  Status:         ${needsCompact ? '⚠️ Needs compact' : '✅ OK'}`);
          console.log('────────────────────────────────────');
          console.log(`  Preserve recent: ${config.preserve_recent} messages`);
          console.log(`  Auto compact:    ${config.auto_compact ? 'Enabled' : 'Disabled'}`);
          console.log(`  Model:           ${actualModel}`);
        });

      // compact-config command
      program
        .command('compact-config')
        .description('Show or update compact configuration')
        .argument('[key]', 'Configuration key (e.g., max_tokens, preserve_recent)')
        .argument('[value]', 'New value')
        .action((key: string, value: string) => {
          if (!key) {
            console.log('🔧 Current Configuration');
            console.log('────────────────────────────────────');
            Object.entries(config).forEach(([k, v]) => {
              console.log(`  ${k}: ${v}`);
            });
            return;
          }

          if (!value) {
            const val = (config as any)[key];
            if (val === undefined) {
              console.error(`❌ Unknown config key: ${key}`);
              return;
            }
            console.log(`${key} = ${val}`);
            return;
          }

          console.log(`⚙️  Setting ${key} = ${value} (not persisted yet)`);
        });

      // sessions command - list all sessions
      program
        .command('sessions')
        .description('List all saved sessions')
        .action(() => {
          try {
            const store = createSessionStore();
            const sessions = store.listSessions();

            if (sessions.length === 0) {
              console.log('📭 No saved sessions found.');
              return;
            }

            console.log('📚 Saved Sessions');
            console.log('────────────────────────────────────');
            sessions.forEach(s => {
              const totalTokens = s.total_input_tokens + s.total_output_tokens + s.total_cache_tokens;
              console.log(`  ${s.session_id}`);
              console.log(`    Messages: ${s.message_count}, Tokens: ${totalTokens.toLocaleString()}, Compactions: ${s.compaction_count}`);
              console.log(`    Updated: ${new Date(s.updated_at).toLocaleString()}`);
            });
          } catch (error) {
            console.error('❌ Failed to list sessions:', error);
          }
        });

      // session-info command - show current session details
      program
        .command('session-info')
        .description('Show detailed session information')
        .option('--session-id <id>', 'Session ID')
        .action((opts: any) => {
          const messages = getCurrentSessionMessages();
          const estimatedTokens = estimateTokenCount(messages);
          const actualUsage = calculateActualTokenUsage(messages as any);
          const totalTokens = actualUsage.input_tokens + actualUsage.output_tokens +
                            actualUsage.cache_creation_input_tokens + actualUsage.cache_read_input_tokens;
          const needsCompact = shouldCompact(messages, config);

          console.log('📊 Session Information');
          console.log('────────────────────────────────────');
          console.log(`  Session ID:      ${opts?.sessionId || 'current (mock)'}`);
          console.log(`  Messages:        ${messages.length}`);
          console.log('');
          console.log('  Token Estimates:');
          console.log(`    Estimated:     ${estimatedTokens.toLocaleString()}`);
          console.log(`    Actual Input:  ${actualUsage.input_tokens.toLocaleString()}`);
          console.log(`    Actual Output: ${actualUsage.output_tokens.toLocaleString()}`);
          console.log(`    Actual Cache:  ${(actualUsage.cache_creation_input_tokens + actualUsage.cache_read_input_tokens).toLocaleString()}`);
          console.log(`    Total Actual:  ${totalTokens.toLocaleString()}`);
          console.log('');
          console.log('  Configuration:');
          console.log(`    Threshold:     ${config.max_tokens.toLocaleString()}`);
          console.log(`    Usage:         ${Math.round((estimatedTokens / config.max_tokens) * 100)}%`);
          console.log(`    Needs Compact: ${needsCompact ? '⚠️ Yes' : '✅ No'}`);
          console.log(`    Auto Compact:  ${config.auto_compact ? 'Enabled' : 'Disabled'}`);
        });
    },
    {
      commands: ['compact', 'compact-status', 'compact-config', 'sessions', 'session-info'],
      descriptors: [
        { name: 'compact', description: 'Manually compact the current session history to save tokens' },
        { name: 'compact-status', description: 'Show current session token usage and compression status' },
        { name: 'compact-config', description: 'Show or update compact configuration' },
        { name: 'sessions', description: 'List all saved sessions' },
        { name: 'session-info', description: 'Show detailed session information' },
      ]
    }
  );
}

// Export types and core functions for programmatic use
export type { CompactConfig } from './compact/config.js';
export {
  generateSummary,
  estimateTokenCount,
  compactSession,
  calculateActualTokenUsage
} from './compact/engine.js';
export {
  SessionManager,
  SessionState,
  createSessionManager
} from './compact/session-manager.js';
export {
  SessionStore,
  createSessionStore
} from './compact/session-store.js';
export {
  ConversationMessage,
  TokenUsage,
  Session,
  ContentBlock,
  MessageRole,
  SessionMetadata,
  createUserMessage,
  createAssistantMessage,
  createToolResultMessage,
  createSystemMessage,
  calculateTotalTokens
} from './compact/types.js';
