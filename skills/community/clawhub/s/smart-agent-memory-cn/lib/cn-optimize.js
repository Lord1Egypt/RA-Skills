/**
 * 中文记忆优化模块
 * 
 * 针对 FTS5 中文分词 bug 的修复和优化
 * 参考 memory-cn 技能的逻辑实现
 */

'use strict';
const fs = require('fs');
const path = require('path');

/**
 * 检测字符串是否包含中文
 */
function hasChinese(str) {
  return /[\u4e00-\u9fa5]/.test(str);
}

/**
 * 在中文字符之间插入空格（解决 FTS5 unicode61 分词问题）
 * 例如: "怀孕产检" -> "怀 孕 产 检"
 */
function insertSpacesBetweenChinese(str) {
  return str.replace(/[\u4e00-\u9fa5]+/g, (match) => {
    return match.split('').join(' ');
  });
}

/**
 * 优化 tags：自动在中文字符之间添加空格
 */
function optimizeTags(tags) {
  if (!tags || !Array.isArray(tags)) return tags;
  return tags.map(tag => {
    if (hasChinese(tag)) {
      return insertSpacesBetweenChinese(tag);
    }
    return tag;
  });
}

/**
 * 诊断记忆系统
 */
function diagnose(memoryDir) {
  const report = {
    fts5Bug: false,
    fileStats: [],
    tagsCoverage: 0,
    lessonsHealth: 0,
    totalFiles: 0,
    filesWithTags: 0,
    issues: [],
  };

  // 1. 检测 FTS5 中文分词 bug
  // 简单的检测方法：检查是否使用了 unicode61 分词器
  // 如果记忆中有连续的中文且没有空格，说明可能受影响
  try {
    const files = fs.readdirSync(memoryDir).filter(f => f.endsWith('.md'));
    let chineseFilesWithNoSpaces = 0;
    
    for (const file of files) {
      const filePath = path.join(memoryDir, file);
      const content = fs.readFileSync(filePath, 'utf8');
      const stat = fs.statSync(filePath);
      
      report.fileStats.push({
        name: file,
        size: stat.size,
        sizeKB: Math.round(stat.size / 1024 * 100) / 100,
        modified: stat.mtime.toISOString().slice(0, 10),
      });

      // 检查是否有中文但没有空格分隔
      const tagsMatch = content.match(/<!--\s*tags:\s*([^>]*)-->/i);
      if (tagsMatch) {
        report.filesWithTags++;
        const tags = tagsMatch[1];
        // 检查是否有连续的中文（没有空格）
        if (hasChinese(tags) && !tags.includes(' ') && !tags.includes(',')) {
          chineseFilesWithNoSpaces++;
        }
      }

      report.totalFiles++;
    }

    report.tagsCoverage = report.totalFiles > 0 
      ? Math.round((report.filesWithTags / report.totalFiles) * 100) 
      : 0;

    if (chineseFilesWithNoSpaces > 0) {
      report.fts5Bug = true;
      report.issues.push(`⚠️ 发现 ${chineseFilesWithNoSpaces} 个文件的中文 tags 未分词，可能影响 FTS5 搜索`);
    }
  } catch (e) {
    report.issues.push(`❌ 诊断错误: ${e.message}`);
  }

  // 2. 检查 lessons 目录
  const lessonsDir = path.join(memoryDir, 'lessons');
  if (fs.existsSync(lessonsDir)) {
    try {
      const lessonFiles = fs.readdirSync(lessonsDir).filter(f => f.endsWith('.md'));
      report.lessonsHealth = lessonFiles.length > 0 ? 100 : 0;
    } catch (e) {
      report.lessonsHealth = 0;
    }
  }

  return report;
}

/**
 * 批量添加/优化 tags
 */
function optimizeAllTags(memoryDir) {
  const results = {
    processed: 0,
    updated: 0,
    errors: [],
  };

  try {
    const files = fs.readdirSync(memoryDir).filter(f => f.endsWith('.md'));

    for (const file of files) {
      const filePath = path.join(memoryDir, file);
      let content = fs.readFileSync(filePath, 'utf8');
      results.processed++;

      // 检查是否已有 tags
      const hasTags = /<!--\s*tags:\s*/i.test(content);

      if (!hasTags) {
        // 尝试从内容中提取关键词
        // 简单实现：从标题和内容中提取中文词语
        const titleMatch = content.match(/^#\s+(.+)$/m);
        if (titleMatch) {
          const title = titleMatch[1];
          // 提取标题中的关键词（简单实现：取前5个中文字符）
          const keywords = title.replace(/[^\u4e00-\u9fa5]/g, '').slice(0, 10);
          if (keywords.length > 0) {
            const optimizedKeywords = insertSpacesBetweenChinese(keywords);
            const tagsLine = `<!-- tags: ${optimizedKeywords} -->\n`;
            content = tagsLine + content;
            fs.writeFileSync(filePath, content);
            results.updated++;
          }
        }
      } else {
        // 已有 tags，优化中文分词
        content = content.replace(/<!--\s*tags:\s*([^>]*)-->/gi, (match, tags) => {
          const optimizedTags = insertSpacesBetweenChinese(tags.trim());
          return `<!-- tags: ${optimizedTags} -->`;
        });
        fs.writeFileSync(filePath, content);
        results.updated++;
      }
    }
  } catch (e) {
    results.errors.push(e.message);
  }

  return results;
}

/**
 * 压缩日志文件
 */
function compressLogs(memoryDir, maxKB = 5) {
  const results = {
    processed: 0,
    compressed: 0,
    archived: [],
    errors: [],
  };

  const archiveDir = path.join(memoryDir, '.archive');
  const maxBytes = maxKB * 1024;

  try {
    const files = fs.readdirSync(memoryDir).filter(f => /^\d{4}-\d{2}-\d{2}\.md$/.test(f));

    for (const file of files) {
      const filePath = path.join(memoryDir, file);
      const stat = fs.statSync(filePath);
      results.processed++;

      if (stat.size > maxBytes) {
        // 需要压缩
        let content = fs.readFileSync(filePath, 'utf8');
        const originalSize = content.length;

        // 简单压缩：移除多余空行、缩短内容
        const lines = content.split('\n');
        const keptLines = [];
        
        for (const line of lines) {
          // 保留标题、tags、决策、重要事实
          if (line.startsWith('# ') || 
              line.startsWith('## ') ||
              line.includes('<!-- tags:') ||
              line.includes('**') ||
              line.startsWith('- **')) {
            keptLines.push(line);
          } else if (line.trim()) {
            // 保留非空行，但截断过长的行
            keptLines.push(line.slice(0, 200));
          }
        }

        content = keptLines.join('\n');

        // 如果仍然太大，保留前几行
        if (content.length > maxBytes) {
          content = keptLines.slice(0, 20).join('\n') + '\n\n... (内容已截断)';
        }

        // 归档原文
        const month = file.slice(0, 7);
        const monthDir = path.join(archiveDir, month);
        if (!fs.existsSync(monthDir)) {
          fs.mkdirSync(monthDir, { recursive: true });
        }
        
        const archivePath = path.join(monthDir, file);
        fs.writeFileSync(archivePath, fs.readFileSync(filePath)); // 原文备份
        
        // 写入压缩后的内容
        fs.writeFileSync(filePath, content);
        
        results.compressed++;
        results.archived.push(`${file} -> .archive/${month}/${file}`);
      }
    }
  } catch (e) {
    results.errors.push(e.message);
  }

  return results;
}

/**
 * 获取优化后的 memoryFlush prompt 配置
 */
function getOptimizedMemoryFlushPrompt() {
  return {
    prompt: `将对话内容整理为结构化日志，写入 memory/YYYY-MM-DD.md。

格式要求：
1. 文件第一行必须是 <!-- tags: 关键词1, 关键词2, ... --> 标签行
2. 中文关键词之间加空格分隔（解决 FTS5 中文分词问题）
3. 只保留有价值的信息
4. 控制在 5KB 以内`
  };
}

/**
 * 获取优化后的搜索配置
 */
function getOptimizedSearchConfig() {
  return {
    memorySearch: {
      chunking: { tokens: 250, overlap: 60 },
      query: {
        maxResults: 10,
        minScore: 0.15,
        hybrid: {
          enabled: true,
          vectorWeight: 0.75,
          textWeight: 0.25,
          candidateMultiplier: 8,
          mmr: { enabled: true, lambda: 0.7 },
          temporalDecay: { enabled: true, halfLifeDays: 90 }
        }
      }
    }
  };
}

module.exports = {
  hasChinese,
  insertSpacesBetweenChinese,
  optimizeTags,
  diagnose,
  optimizeAllTags,
  compressLogs,
  getOptimizedMemoryFlushPrompt,
  getOptimizedSearchConfig,
};
