import { Command } from 'commander';
import { compactSession, estimateTokenCount, shouldCompact, getContinuationPrompt, type CompactionResult } from '../compact/engine.js';
import { loadConfig } from '../compact/config.js';
import { getCurrentModel } from '../compact/engine.js';

// 模拟当前会话消息（实际实现需从 OpenClaw 会话存储获取）
function getCurrentSessionMessages(): Array<{ role: string; content?: string }> {
  // TODO: 替换为实际的会话获取逻辑
  // 示例：从 ~/.openclaw/state/sessions/ 加载
  return [
    { role: 'user', content: 'Hello, how do I start a new project?' },
    { role: 'assistant', content: 'Sure! Let me help you set up a new project. What kind of project do you want to create?' },
    { role: 'user', content: 'A TypeScript CLI tool' },
    { role: 'assistant', content: 'Great choice! I will help you set up a TypeScript CLI tool with the necessary configuration.' },
    // ... 更多消息
  ];
}

export function registerCompactCommands(program: Command): void {
  // 手动压缩命令
  program
    .command('compact')
    .description('Manually compact the current session history to save tokens')
    .option('--force', 'Force compact even if under threshold')
    .action(async (options) => {
      const config = loadConfig();
      const messages = getCurrentSessionMessages();
      const totalTokens = estimateTokenCount(messages);

      console.log(`📊 Current session tokens: ${totalTokens}`);
      console.log(`📉 Threshold: ${config.max_tokens}`);

      if (!options.force && !shouldCompact(messages, config)) {
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

  // 状态查看命令
  program
    .command('compact-status')
    .description('Show current session token usage and compression status')
    .action(() => {
      const config = loadConfig();
      const messages = getCurrentSessionMessages();
      const totalTokens = estimateTokenCount(messages);
      const needsCompact = shouldCompact(messages, config);
      
      // 获取实际使用的模型（如果配置为空，则读取全局配置）
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

  // 配置命令（可选：集成到 openclaw config 系统）
  program
    .command('compact-config')
    .description('Show or update compact configuration')
    .argument('[key]', 'Configuration key (e.g., max_tokens, preserve_recent)')
    .argument('[value]', 'New value')
    .action((key, value) => {
      const config = loadConfig();
      
      if (!key) {
        console.log('🔧 Current Configuration');
        console.log('────────────────────────────────────');
        Object.entries(config).forEach(([k, v]) => {
          console.log(`  ${k}: ${v}`);
        });
        return;
      }

      if (!value) {
        // 获取配置值
        const val = (config as any)[key];
        if (val === undefined) {
          console.error(`❌ Unknown config key: ${key}`);
          return;
        }
        console.log(`${key} = ${val}`);
        return;
      }

      // 设置配置值（TODO: 实际实现需写入配置文件）
      console.log(`⚙️  Setting ${key} = ${value} (not persisted in demo)`);
    });
}
