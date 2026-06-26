import { z } from "https://deno.land/x/zod@v3.22.4/mod.ts";

// 类型定义
const StreamFormatterParams = z.union([
  z.object({
    action: z.literal("init"),
    options: z.object({
      buffer_size: z.number().min(1).max(1000).optional().default(10),
      format_markdown: z.boolean().optional().default(true),
      fix_incomplete_sentences: z.boolean().optional().default(true),
      remove_duplicates: z.boolean().optional().default(true),
    }).optional().default({})
  }),
  z.object({
    action: z.literal("process"),
    chunk: z.string(),
    flush: z.boolean().optional().default(false),
  }),
  z.object({
    action: z.literal("reset"),
  })
]);

type StreamFormatterParams = z.infer<typeof StreamFormatterParams>;

// 全局状态
let buffer = "";
let lastOutput = "";
let config = {
  buffer_size: 10,
  format_markdown: true,
  fix_incomplete_sentences: true,
  remove_duplicates: true
};

// 标点符号集合（中英文）
const SENTENCE_ENDINGS = new Set([".", "!", "?", "。", "！", "？", "；", ";\n", "\n\n"]);
const INCOMPLETE_PATTERNS = [
  /\([^\)]*$/, // 未闭合的括号
  /\[[^\]]*$/, // 未闭合的方括号
  /`[^`]*$/, // 未闭合的反引号
  /\*[^\*]*$/, // 未闭合的星号
  /_[^_]*$/, // 未闭合的下划线
  /```[^\`]*$/, // 未闭合的代码块
  /#[^\n]*$/, // 未完成的标题
];

/**
 * OpenClaw Skill: 流式输出格式化器
 * 实时优化大模型流式输出，修复格式错误，提升用户体验
 */
export default async function streamFormatter(params: StreamFormatterParams) {
  const validatedParams = StreamFormatterParams.parse(params);

  switch (validatedParams.action) {
    case "init": {
      config = { ...config, ...validatedParams.options };
      buffer = "";
      lastOutput = "";
      return { success: true, config };
    }

    case "process": {
      const { chunk, flush } = validatedParams;
      
      // 添加到缓冲区
      buffer += chunk;
      
      // 去重处理
      if (config.remove_duplicates && buffer.includes(lastOutput) && lastOutput.length > 0) {
        buffer = buffer.replace(lastOutput, "");
      }

      let output = "";
      
      // 自适应缓冲区大小
      let adaptiveBufferSize = config.buffer_size;
      if (buffer.includes("```") || buffer.includes("$")) {
        adaptiveBufferSize = 50; // 代码块和公式增大缓冲区
      } else if (chunk.length > 0 && SENTENCE_ENDINGS.has(chunk[chunk.length - 1])) {
        adaptiveBufferSize = 5; // 句子结束时减小缓冲区
      }

      // 如果缓冲区足够大或者强制刷新，处理输出
      if (buffer.length >= adaptiveBufferSize || flush) {
        // 修复不完整句子
        if (config.fix_incomplete_sentences && !flush) {
          // 查找最后一个完整句子的位置
          let lastEndIndex = -1;
          for (let i = buffer.length - 1; i >= Math.max(0, buffer.length - 20); i--) {
            if (SENTENCE_ENDINGS.has(buffer[i])) {
              lastEndIndex = i + 1;
              break;
            }
          }
          
          if (lastEndIndex > 0) {
            // 输出完整句子
            output = buffer.slice(0, lastEndIndex);
            // 保留不完整的部分在缓冲区
            buffer = buffer.slice(lastEndIndex);
          } else if (flush) {
            // 强制刷新时输出所有内容
            output = buffer;
            buffer = "";
          }
        } else {
          // 不修复句子的话直接输出所有缓冲区内容
          output = buffer;
          buffer = "";
        }

        // Markdown格式修复
        if (config.format_markdown && output.length > 0) {
          output = fixMarkdownFormat(output);
        }

        // 记录最后输出内容用于去重
        lastOutput = output;
      }

      return {
        success: true,
        output,
        buffer_remaining: buffer.length,
        has_more: buffer.length > 0
      };
    }

    case "reset": {
      buffer = "";
      lastOutput = "";
      return { success: true };
    }

    default:
      return { success: false, error: "Invalid action" };
  }
}

// 修复Markdown格式
function fixMarkdownFormat(text: string): string {
  let fixed = text;
  
  // 修复代码块
  fixed = fixed.replace(/```(\w*)\n?([\s\S]*?)(```|$)/g, (match, lang, code, close) => {
    if (!close) {
      // 不完整的代码块，暂时去掉```避免渲染错误
      return code;
    }
    // 标准化语言标识
    const langMap: Record<string, string> = {
      "js": "javascript",
      "ts": "typescript",
      "py": "python",
      "md": "markdown",
      "c": "cpp",
      "java": "java"
    };
    const normalizedLang = lang ? langMap[lang.toLowerCase()] || lang : "";
    return `\`\`\`${normalizedLang}\n${code.trim()}\n\`\`\``;
  });

  // 修复列表
  fixed = fixed.replace(/^(•|-|\*)\s+/gm, "- ");
  fixed = fixed.replace(/^(\d+)\.\s+/gm, "$1. ");

  // 修复标题
  fixed = fixed.replace(/^(#+)\s*(.+)/gm, (match, hashes, title) => {
    return `${hashes} ${title.trim()}`;
  });

  // 修复链接
  fixed = fixed.replace(/\[([^\]]+)\]\(([^\)]*)\)?/g, (match, text, url) => {
    if (!url.endsWith(")")) {
      // 不完整的链接，暂时显示为文本
      return text;
    }
    return match;
  });

  // 去除多余的换行
  fixed = fixed.replace(/\n{3,}/g, "\n\n");
  
  return fixed;
}
