#!/usr/bin/env node
/**
 * archive_unused.js - 选题归档脚本（每日 23:55 跑）
 *
 * 功能：
 *   1. 扫描 ${TOPICS_DIR}/claude-hub/topics/*.md（不含 history/）
 *   2. 解析每个文件中的 "## 选题 N" 独立块
 *   3. 若选题块内有 "[x] 勾选采用" 标记 → 视为已选用，跳过
 *   4. 未选用的选题块统一收集，写入 history/YYYYMMDD_unused.md
 *   5. 清理 history/ 里超过 7 天的旧文件（rm）
 *
 * 输出格式：
 *   清理了 N 个选题 + 删除了 M 个 history 文件
 *
 * 依赖：Node.js >= 18（原生 fetch）
 *
 * 作者：Claude
 * 日期：2026-08-14
 */

'use strict';

const fs = require('fs');
const path = require('path');

// ============================================================
// 1. 路径配置（写死在代码里，不依赖环境变量）
// ============================================================

// ${TOPICS_DIR}/claude-hub/topics/
const TOPICS_DIR = path.join(
  process.env.HOME || require('os').homedir(),
  '.openclaw/workspace/claude-hub/topics'
);

// 历史归档目录：topics/history/
const HISTORY_DIR = path.join(TOPICS_DIR, 'history');

// ============================================================
// 2. 辅助函数
// ============================================================

/**
 * 获取今天日期字符串（YYYYMMDD），北京时间
 * 使用 TZ=Asia/Shanghai 保证时区正确
 */
function getTodayStr() {
  const now = new Date();
  // 使用 Asia/Shanghai 时区获取 YYYYMMDD
  const shanghaiTime = now.toLocaleString('en-CA', {
    timeZone: 'Asia/Shanghai',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  });
  // shanghaiTime 格式: YYYY-MM-DD
  return shanghaiTime.replace(/-/g, '');
}

/**
 * 解析文件内容，提取所有 "## 选题 N" 独立块
 *
 * 每个选题块的格式：
 *   ## 选题 1 · ⭐优先
 *   ## 选题 2 ·
 *   ...
 *
 * 选题块以 "## 选题 N" 开头，"---" 或文件末尾结束
 *
 * 实现策略：用 "---" 将内容切分为多个 section，
 * 每个 section 内找 "## 选题 N" 标题行，解析出编号和优先标记。
 * 这样做比跨块的 lookahead 正则更可靠。
 *
 * @param {string} content - 文件完整内容
 * @returns {Array<{num: number, isStarred: boolean, body: string, adopted: boolean}>}
 */
function parseTopicBlocks(content) {
  // 用 "\n---\n" 分割内容为各个选题块（先 split 再 join 处理多行 ---）
  // 这样每个 section 包含一个完整的选题块
  const sections = content.split(/\n---\n/);
  const blocks = [];

  for (const section of sections) {
    const trimmed = section.trim();
    if (!trimmed) continue;

    // 从 section 第一行解析 "## 选题 N · ⭐优先" 或 "## 选题 N ·"
    // 格式：## 选题 {数字} · ⭐优先   或   ## 选题 {数字} ·
    const titleMatch = trimmed.match(/^\s*## 选题 (\d+) ·(⭐)?/);
    if (!titleMatch) continue;

    const num = parseInt(titleMatch[1], 10);
    const isStarred = titleMatch[2] === '⭐';

    // body 是 section 内容去掉第一行标题后的剩余部分
    const body = trimmed.replace(/^.*?\n/, ''); // 去掉第一行

    // 检查是否标记为已选用：用户改用注释标记 `<!-- __ADOPTED__: 选题 N -->`
    const adopted = /<!-- __ADOPTED__: 选题 \d+ -->/.test(body);

    blocks.push({ num, isStarred, body, adopted });
  }

  return blocks;
}

/**
 * 判断文件是否为今天的选题文件（YYYYMMDD_topics.md）
 * 今天的文件由 generate_topics.js 刚生成，不应归档
 *
 * @param {string} filename
 * @returns {boolean}
 */
function isTodaysFile(filename) {
  const today = getTodayStr();
  return filename === `${today}_topics.md`;
}

/**
 * 计算 N 天前的日期字符串（YYYYMMDD）
 *
 * @param {number} daysAgo
 * @returns {string}
 */
function getDateStrDaysAgo(daysAgo) {
  const now = new Date();
  // 使用 Asia/Shanghai 时区计算 N 天前的日期
  const shanghaiTime = new Date(now.toLocaleString('en-CA', {
    timeZone: 'Asia/Shanghai',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  }));
  shanghaiTime.setDate(shanghaiTime.getDate() - daysAgo);
  return shanghaiTime.toLocaleString('en-CA', {
    timeZone: 'Asia/Shanghai',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  }).replace(/-/g, '');
}

/**
 * 主逻辑：扫描所有 .md 文件，收集未选用选题
 *
 * @returns {{unusedBlocks: Array, deletedHistoryCount: number, error: string|null}}
 */
function run() {
  const result = { unusedBlocks: [], deletedHistoryCount: 0, error: null };

  // 确保 history 目录存在
  if (!fs.existsSync(HISTORY_DIR)) {
    try {
      fs.mkdirSync(HISTORY_DIR, { recursive: true });
    } catch (e) {
      result.error = `创建 history 目录失败: ${e.message}`;
      return result;
    }
  }

  // 1) 扫描 topics/ 目录下所有 .md 文件（不含 history/）
  let files;
  try {
    files = fs.readdirSync(TOPICS_DIR).filter(f => {
      return f.endsWith('.md') && !f.startsWith('history');
    });
  } catch (e) {
    result.error = `读取 topics 目录失败: ${e.message}`;
    return result;
  }

  if (files.length === 0) {
    console.log('archive_unused: topics 目录无 .md 文件，跳过');
    return result;
  }

  // 2) 遍历每个文件，解析选题块
  for (const file of files) {
    // 跳过今天的文件（刚生成，还未被用户处理）
    if (isTodaysFile(file)) {
      console.log(`archive_unused: 跳过今天文件 ${file}`);
      continue;
    }

    const filePath = path.join(TOPICS_DIR, file);
    let content;
    try {
      content = fs.readFileSync(filePath, 'utf-8');
    } catch (e) {
      console.error(`archive_unused: 读取文件失败 ${file}: ${e.message}`);
      continue;
    }

    const blocks = parseTopicBlocks(content);

    for (const block of blocks) {
      if (!block.adopted) {
        // 附上来源文件名，方便回溯
        result.unusedBlocks.push({
          topicNum: block.num,
          sourceFile: file,
          isStarred: block.isStarred,
          body: block.body
        });
      }
    }
  }

  // 3) 写入 history/YYYYMMDD_unused.md（只有收集到未选用选题时才写）
  if (result.unusedBlocks.length > 0) {
    const today = getTodayStr();
    const unusedFile = path.join(HISTORY_DIR, `${today}_unused.md`);

    // 构建写入内容
    const lines = [
      `# 未选用选题归档 · ${today}`,
      `> 由 archive_unused.js 自动生成`,
      ``,
      `共 ${result.unusedBlocks.length} 个未选用选题`,
      ``,
      `---`,
      ``
    ];

    for (const block of result.unusedBlocks) {
      lines.push(`## 选题 ${block.topicNum} · ${block.isStarred ? '⭐优先' : ''}`);
      lines.push(`来源文件：${block.sourceFile}`);
      lines.push(``);
      lines.push(block.body);
      lines.push(``);
      lines.push(`---`);
      lines.push(``);
    }

    try {
      fs.writeFileSync(unusedFile, lines.join('\n'), 'utf-8');
      console.log(`archive_unused: 写入未选用选题 ${result.unusedBlocks.length} 条 → ${unusedFile}`);
    } catch (e) {
      console.error(`archive_unused: 写入归档文件失败: ${e.message}`);
      // 归档写入失败不阻塞，但记录错误
    }
  } else {
    console.log('archive_unused: 无未选用选题，跳过写入');
  }

  // 4) 清理 history/ 里超过 7 天的文件
  const KEEP_DAYS = 7;
  const cutoffDateStr = getDateStrDaysAgo(KEEP_DAYS);

  let historyFiles;
  try {
    historyFiles = fs.readdirSync(HISTORY_DIR).filter(f => f.endsWith('.md'));
  } catch (e) {
    console.error(`archive_unused: 读取 history 目录失败: ${e.message}`);
    return result;
  }

  for (const hf of historyFiles) {
    // 文件名格式：YYYYMMDD_unused.md 或 YYYYMMDD_topics.md
    const dateMatch = hf.match(/^(\d{8})_/);
    if (!dateMatch) continue;

    const fileDate = dateMatch[1];
    if (fileDate < cutoffDateStr) {
      const fullPath = path.join(HISTORY_DIR, hf);
      try {
        fs.unlinkSync(fullPath);
        result.deletedHistoryCount++;
        console.log(`archive_unused: 删除过期 history 文件 ${hf}`);
      } catch (e) {
        console.error(`archive_unused: 删除文件失败 ${hf}: ${e.message}`);
      }
    }
  }

  return result;
}

// ============================================================
// 3. 入口
// ============================================================

try {
  console.log(`=== archive_unused.js 启动 (${new Date().toISOString()}) ===`);

  const res = run();

  if (res.error) {
    console.error(`archive_unused: 严重错误 - ${res.error}`);
    process.exit(1);
  }

  console.log(
    `=== archive_unused.js 完成 ===` +
    `\n清理了 ${res.unusedBlocks.length} 个未选用选题` +
    `\n删除了 ${res.deletedHistoryCount} 个 history 文件`
  );
  process.exit(0);
} catch (err) {
  // 全局兜底：捕获所有未处理异常，不让脚本抛出
  console.error(`archive_unused: 未捕获异常 - ${err.message}`);
  process.exit(1);
}
