/**
 * 忆流 - AI 笔记知识库
 * 主入口文件
 */

import { initDB } from './storage/db.js';
import * as note from './commands/note.js';
import { isAIAvailable, isLocalEmbeddingAvailable } from './ai/index.js';

let initialized = false;

async function ensureInit(): Promise<void> {
  if (!initialized) {
    await initDB();
    initialized = true;
  }
}

export interface SkillInput {
  message: string;
  context?: {
    userId?: string;
    sessionId?: string;
  };
}

export interface SkillOutput {
  message: string;
  actions?: {
    type: string;
    data?: any;
  }[];
}

export async function handle(input: SkillInput): Promise<SkillOutput> {
  await ensureInit();

  const msg = input.message.trim();
  
  // 斜杠命令
  if (msg.startsWith('/')) {
    return handleSlashCommand(msg);
  }
  
  // 关键字触发
  return handleKeyword(msg);
}

async function handleSlashCommand(msg: string): Promise<SkillOutput> {
  const [cmd, ...args] = msg.slice(1).split(' ');
  const arg = args.join(' ');
  
  switch (cmd) {
    case '记':
    case '记录': {
      if (!arg) {
        return { message: '请提供笔记内容：/记 <内容>' };
      }
      // 统一使用异步版本（带 AI 增强）
      const result = await note.handleNoteAsync(arg);
      return { message: result.message };
    }
      
    case '搜':
    case '搜索': {
      if (!arg) {
        return { message: '请提供搜索关键词：/搜 <关键词>' };
      }
      // 统一使用语义搜索
      const result = await note.handleSemanticSearch(arg);
      return { message: result };
    }
    
    case '列':
    case '列表':
      return { message: await note.handleList(20) };
    
    case '历史':
      return { message: await note.handleHistory(arg) };
    
    case '查看':
      return { message: await note.handleView(arg) };
    
    case '编辑':
    case '改':
      return { message: await handleEditFlow(arg) };
    
    case '删除':
      return { message: await note.handleDelete(arg) };
    
    case '导出':
      return { message: note.handleExport(arg || 'md') };
    
    case '统计':
    case '状态':
      return { message: await note.handleStats() };
    
    case '帮助':
      return { message: getHelp() };
    
    default:
      return { message: `未知命令：/${cmd}\n\n${getHelp()}` };
  }
}

async function handleEditFlow(arg: string): Promise<string> {
  const parts = arg.split(' ');
  if (parts.length < 2) {
    return '请提供笔记ID和新内容：\n/编辑 <id> <新内容>\n\n或使用：/搜 <关键词> 然后「改成 <新内容>」';
  }
  
  const idOrKeyword = parts[0];
  const newContent = parts.slice(1).join(' ');
  
  return await note.handleUpdate(idOrKeyword, newContent);
}

async function handleKeyword(msg: string): Promise<SkillOutput> {
  // 优先检查关键字
  if (msg.startsWith('记') || msg.startsWith('记录')) {
    const content = msg.replace(/^(记|记录)/, '').trim();
    if (!content) {
      return { message: '请提供笔记内容' };
    }
    // 统一使用异步版本
    const result = await note.handleNoteAsync(content);
    return { message: result.message };
  }
  
  if (msg.startsWith('搜') || msg.startsWith('搜索') || msg.startsWith('找')) {
    const query = msg.replace(/^(搜|搜索|找)/, '').trim();
    if (!query) {
      return { message: '请提供搜索关键词' };
    }
    // 统一使用语义搜索（内部会处理 AI 不可用的情况）
    const result = await note.handleSemanticSearch(query);
    return { message: result };
  }
  
  if (msg.startsWith('历史') || msg.startsWith('版本')) {
    const id = msg.replace(/^(历史|版本)/, '').trim();
    return { message: await note.handleHistory(id) };
  }
  
  if (msg.startsWith('编辑') || msg.startsWith('修改') || msg.startsWith('改成')) {
    const content = msg.replace(/^(编辑|修改|改成)/, '').trim();
    return { message: '请提供笔记ID：/编辑 <id> <新内容>' };
  }
  
  if (msg.startsWith('删除')) {
    return { message: '请提供笔记ID：删除 <id>' };
  }
  
  if (msg.startsWith('列表') || msg.startsWith('列')) {
    return { message: await note.handleList() };
  }
  
  if (msg.startsWith('导出') || msg.startsWith('备份')) {
    return { message: note.handleExport() };
  }
  
  if (msg.startsWith('帮助') || msg.startsWith('help')) {
    return { message: getHelp() };
  }
  
  if (msg.startsWith('统计') || msg.startsWith('状态')) {
    return { message: await note.handleStats() };
  }
  
  // 检测URL
  if (msg.match(/https?:\/\//)) {
    return { message: await note.handleLinkCapture(msg) };
  }
  
  // 默认当作记录（统一使用异步版本）
  const result = await note.handleNoteAsync(msg);
  return { message: result.message };
}

function getHelp(): string {
  const aiStatus = isAIAvailable() ? '✅' : '❌ (本地可用)';
  
  return `📝 忆流笔记 - 使用帮助

【记录】
/记 <内容> - 记录新笔记 ${aiStatus} AI增强
<内容> - 直接输入也记笔记

【搜索】
/搜 <关键词> - 搜索笔记 ${aiStatus} 语义搜索
/列表 - 查看所有笔记

【编辑】
/编辑 <id> <新内容> - 修改笔记

【版本】
/历史 <id或关键词> - 查看版本历史
/查看 <id或关键词> - 查看笔记详情

【导出】
/导出 - 导出Markdown

【其他】
/统计 - 查看统计信息
/帮助 - 显示帮助

AI状态: ${aiStatus}
`;
}

// OpenClaw skill interface
export default {
  handle
};
