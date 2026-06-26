import { z } from "https://deno.land/x/zod@v3.22.4/mod.ts";
import { encodeHex } from "https://deno.land/std@0.214.0/encoding/hex.ts";

// 类型定义
const MemoryItem = z.object({
  id: z.string(),
  content: z.string(),
  type: z.enum(["short-term", "long-term", "important"]).default("short-term"),
  timestamp: z.number().default(() => Date.now()),
  metadata: z.record(z.any()).default({}),
  embedding: z.array(z.number()).optional(),
});

const MemoryManagerParams = z.union([
  z.object({
    action: z.literal("add"),
    content: z.string(),
    type: z.enum(["short-term", "long-term", "important"]).optional().default("short-term"),
    metadata: z.record(z.any()).optional(),
    persist: z.boolean().optional().default(false),
  }),
  z.object({
    action: z.literal("search"),
    query: z.string(),
    limit: z.number().optional().default(5),
    typeFilter: z.enum(["short-term", "long-term", "important", "all"]).optional().default("all"),
    searchMode: z.enum(["keyword", "semantic", "hybrid"]).optional().default("keyword"),
  }),
  z.object({
    action: z.literal("summarize"),
    typeFilter: z.enum(["short-term", "long-term", "important", "all"]).optional().default("short-term"),
    maxTokens: z.number().optional().default(1000),
  }),
  z.object({
    action: z.literal("clear"),
    typeFilter: z.enum(["short-term", "long-term", "important", "all"]).optional().default("short-term"),
  }),
  z.object({
    action: z.literal("list"),
    limit: z.number().optional().default(20),
    typeFilter: z.enum(["short-term", "long-term", "important", "all"]).optional().default("all"),
  }),
  z.object({
    action: z.literal("load"),
    persistPath: z.string().optional().default("./memory-store.json"),
  }),
  z.object({
    action: z.literal("save"),
    persistPath: z.string().optional().default("./memory-store.json"),
  })
]);

type MemoryItem = z.infer<typeof MemoryItem>;
type MemoryManagerParams = z.infer<typeof MemoryManagerParams>;

// 内存存储
let memoryStore: MemoryItem[] = [];
let config = {
  persistPath: "./memory-store.json",
  shortTermMaxCount: 100,
  autoPersist: false,
};

/**
 * OpenClaw Skill: 智能记忆管理器
 * 支持短期/长期/重要记忆分层、语义检索、自动摘要，解决Agent上下文溢出问题
 */
export default async function smartMemoryManager(params: MemoryManagerParams) {
  const validatedParams = MemoryManagerParams.parse(params);

  switch (validatedParams.action) {
    case "add": {
      const { content, type, metadata, persist } = validatedParams;
      
      const memory: MemoryItem = {
        id: encodeHex(crypto.getRandomValues(new Uint8Array(8))),
        content,
        type,
        timestamp: Date.now(),
        metadata: metadata || {},
      };
      
      // 短期记忆自动清理
      if (memory.type === "short-term") {
        const shortTermMemories = memoryStore.filter(m => m.type === "short-term");
        if (shortTermMemories.length >= config.shortTermMaxCount) {
          // 删除最早的短期记忆
          memoryStore = memoryStore.filter(m => m.type !== "short-term")
            .concat(shortTermMemories.sort((a, b) => b.timestamp - a.timestamp).slice(0, config.shortTermMaxCount - 1));
        }
      }
      
      memoryStore.push(memory);
      
      // 自动持久化
      if (persist || config.autoPersist) {
        await saveMemory(config.persistPath);
      }
      
      return { success: true, memoryId: memory.id };
    }

    case "search": {
      const { query, limit, typeFilter, searchMode } = validatedParams;
      
      // 过滤记忆类型
      const filtered = typeFilter === "all" 
        ? memoryStore 
        : memoryStore.filter(m => m.type === typeFilter);
      
      let scoredItems: { memory: MemoryItem; score: number }[] = [];
      
      if (searchMode === "keyword" || searchMode === "hybrid") {
        // 关键词匹配
        const keywordScored = filtered.map(memory => ({
          memory,
          score: memory.content.toLowerCase().includes(query.toLowerCase()) ? 1 : 0
        })).filter(item => item.score > 0);
        scoredItems = [...scoredItems, ...keywordScored];
      }
      
      if (searchMode === "semantic" || searchMode === "hybrid") {
        // 简单语义匹配（可扩展为向量检索）
        const semanticScored = filtered.map(memory => {
          // 简单相似度计算：统计共同关键词数量
          const queryWords = new Set(query.toLowerCase().split(/\s+/));
          const contentWords = new Set(memory.content.toLowerCase().split(/\s+/));
          const intersection = [...queryWords].filter(w => contentWords.has(w)).length;
          return {
            memory,
            score: intersection / queryWords.size
          };
        }).filter(item => item.score > 0);
        scoredItems = [...scoredItems, ...semanticScored];
      }
      
      // 去重、排序、分页
      const uniqueItems = Array.from(new Map(scoredItems.map(item => [item.memory.id, item])).values());
      const results = uniqueItems
        .sort((a, b) => {
          // 先按分数排序，再按时间排序
          if (b.score !== a.score) return b.score - a.score;
          return b.memory.timestamp - a.memory.timestamp;
        })
        .slice(0, limit)
        .map(item => item.memory);

      return {
        success: true,
        results,
        count: results.length,
        searchMode
      };
    }

    case "summarize": {
      const { typeFilter, maxTokens } = validatedParams;
      const filtered = typeFilter === "all" 
        ? memoryStore 
        : memoryStore.filter(m => m.type === typeFilter);
      
      // 按时间排序，取最近的内容
      const recentContent = filtered
        .sort((a, b) => b.timestamp - a.timestamp)
        .map(m => `${new Date(m.timestamp).toLocaleString()}: ${m.content}`)
        .join("\n\n")
        .slice(0, maxTokens * 4); // 粗略估算，1token≈4字符

      const summary = recentContent.length > 0 
        ? `## 记忆摘要（共${filtered.length}条）\n\n${recentContent.slice(0, 2000)}${recentContent.length > 2000 ? "...（内容过长已截断）" : ""}`
        : "暂无记忆内容";

      return { success: true, summary, memoryCount: filtered.length };
    }

    case "clear": {
      const { typeFilter } = validatedParams;
      const beforeCount = memoryStore.length;
      
      if (typeFilter === "all") {
        memoryStore = [];
      } else {
        memoryStore = memoryStore.filter(m => m.type !== typeFilter);
      }

      // 持久化
      if (config.autoPersist) {
        await saveMemory(config.persistPath);
      }

      return {
        success: true,
        clearedCount: beforeCount - memoryStore.length,
        remainingCount: memoryStore.length
      };
    }

    case "list": {
      const { limit, typeFilter } = validatedParams;
      const filtered = typeFilter === "all" 
        ? memoryStore 
        : memoryStore.filter(m => m.type === typeFilter);
      
      const memories = filtered
        .sort((a, b) => b.timestamp - a.timestamp)
        .slice(0, limit);

      return { success: true, memories, totalCount: filtered.length };
    }

    case "load": {
      const { persistPath } = validatedParams;
      try {
        const content = await Deno.readTextFile(persistPath);
        memoryStore = JSON.parse(content);
        config.persistPath = persistPath;
        return { success: true, loadedCount: memoryStore.length, persistPath };
      } catch (error) {
        return { success: false, error: `Failed to load memory: ${(error as Error).message}` };
      }
    }

    case "save": {
      const { persistPath } = validatedParams;
      try {
        await saveMemory(persistPath);
        return { success: true, savedCount: memoryStore.length, persistPath };
      } catch (error) {
        return { success: false, error: `Failed to save memory: ${(error as Error).message}` };
      }
    }

    default:
      return { success: false, error: "Invalid action" };
  }
}

// 持久化存储
async function saveMemory(path: string) {
  await Deno.writeTextFile(path, JSON.stringify(memoryStore, null, 2));
}
