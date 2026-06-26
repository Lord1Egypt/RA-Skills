import { getMemoryManager } from '../../src/index.js';

const handler = async (event) => {
  const callTime = new Date().toISOString();
  const { action, context } = event || {};
  const content = context?.content || '';
  const wallet = process.env.OPENCLAW_MEMORY_WALLET || 'assistant-shrimp-main';

  console.log('[Memory HookPack] message:preprocessed invoked', {
    time: callTime,
    action,
    wallet,
    contentPreview: content ? `${content.slice(0, 80)}${content.length > 80 ? '…' : ''}` : 'empty'
  });

  if (!content) {
    console.log('[Memory HookPack] skip: empty content');
    return;
  }

  const manager = getMemoryManager();

  const memories = await manager.analyzer.analyzeInteraction(
    { prompt: content, sessionId: context?.sessionId || event?.sessionKey || 'unknown', timestamp: callTime },
    { content: '', timestamp: callTime }
  );

  if (!memories || memories.length === 0) {
    console.log('[Memory HookPack] skip: analyzer returned no memories');
    return;
  }

  const quota = await manager.storage.getQuota(wallet);
  const quotaAvailable = await manager.storage.checkQuotaAvailable(wallet);

  if (!quotaAvailable) {
    console.log('[Memory HookPack] quota exceeded, pruning');
    await manager.pruner.enforceQuota(wallet);
  }

  for (const memory of memories) {
    await manager.storage.recordMemory({
      ...memory,
      agent_wallet: wallet,
      session_id: context?.sessionId || event?.sessionKey || 'unknown'
    });
  }

  await manager.storage.updateQuota(wallet, {
    memory_count: quota.memory_count + memories.length
  });

  console.log(`[Memory HookPack] stored ${memories.length} memories`);
};

export default handler;
