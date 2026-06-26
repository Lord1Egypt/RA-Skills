#!/usr/bin/env node

/**
 * Pagination Logic - 分页逻辑
 * 
 * 支持分页导航、页码计算、用户输入解析
 * 
 * @version 1.0.0
 * @author Neo（宇宙神经系统）
 */

// 配置
const CONFIG = {
  pageSize: 5,
  maxPagesPerView: 5
};

/**
 * 计算分页信息
 */
function calculatePagination(totalItems, currentPage = 1, pageSize = CONFIG.pageSize) {
  const totalPages = Math.ceil(totalItems / pageSize);
  const start = (currentPage - 1) * pageSize;
  const end = Math.min(start + pageSize, totalItems);
  
  return {
    totalItems,
    currentPage,
    totalPages,
    pageSize,
    start,
    end,
    hasNext: currentPage < totalPages,
    hasPrev: currentPage > 1
  };
}

/**
 * 解析用户输入，判断是否要翻页
 */
function parseUserInput(input) {
  if (!input) return { action: 'none' };
  
  const lowerInput = input.toLowerCase().trim();
  
  // 下一页
  if (['是', 'yes', 'y', '下一页', 'next', '继续'].includes(lowerInput)) {
    return { action: 'next' };
  }
  
  // 上一页
  if (['上一页', 'prev', 'previous', 'back'].includes(lowerInput)) {
    return { action: 'prev' };
  }
  
  // 停止
  if (['不用', 'no', 'n', '停止', 'stop', '结束', '不用了'].includes(lowerInput)) {
    return { action: 'stop' };
  }
  
  // 指定页码（如"第 3 页"或"page 3"）
  const pageMatch = lowerInput.match(/(?:第？)?(\d+)[页页]|page\s*(\d+)/);
  if (pageMatch) {
    const pageNum = parseInt(pageMatch[1] || pageMatch[2]);
    return { action: 'goto', page: pageNum };
  }
  
  // 更新命令
  if (lowerInput.includes('更新') || lowerInput.includes('update')) {
    const skillMatch = lowerInput.match(/更新\s*(.+)|update\s+(.+)/);
    if (skillMatch) {
      return { action: 'update', skill: skillMatch[1] || skillMatch[2] };
    }
  }
  
  // 卸载命令
  if (lowerInput.includes('卸载') || lowerInput.includes('uninstall')) {
    const skillMatch = lowerInput.match(/卸载\s*(.+)|uninstall\s+(.+)/);
    if (skillMatch) {
      return { action: 'uninstall', skill: skillMatch[1] || skillMatch[2] };
    }
  }
  
  // 禁用命令
  if (lowerInput.includes('禁用') || lowerInput.includes('disable')) {
    const skillMatch = lowerInput.match(/禁用\s*(.+)|disable\s+(.+)/);
    if (skillMatch) {
      return { action: 'disable', skill: skillMatch[1] || skillMatch[2] };
    }
  }
  
  // 启用命令
  if (lowerInput.includes('启用') || lowerInput.includes('enable')) {
    const skillMatch = lowerInput.match(/启用\s*(.+)|enable\s+(.+)/);
    if (skillMatch) {
      return { action: 'enable', skill: skillMatch[1] || skillMatch[2] };
    }
  }
  
  // 地球图标（打开 ClawHub）
  if (['🌐', '🌍', '🪐'].includes(input) || lowerInput.includes('主页') || lowerInput.includes('homepage')) {
    return { action: 'open-clawhub' };
  }
  
  // 详情
  if (lowerInput.includes('详情') || lowerInput.includes('detail')) {
    const skillMatch = lowerInput.match(/详情\s*(.+)|detail\s+(.+)/);
    if (skillMatch) {
      return { action: 'detail', skill: skillMatch[1] || skillMatch[2] };
    }
  }
  
  return { action: 'none' };
}

/**
 * 生成页码显示（如"1/5"）
 */
function formatPageInfo(currentPage, totalPages) {
  return `${currentPage}/${totalPages}`;
}

/**
 * 生成页码导航（如"1 2 3 4 5"）
 */
function generatePageNumbers(currentPage, totalPages) {
  const pages = [];
  const halfView = Math.floor(CONFIG.maxPagesPerView / 2);
  
  let start = Math.max(1, currentPage - halfView);
  let end = Math.min(totalPages, currentPage + halfView);
  
  // 调整范围，确保显示 maxPagesPerView 个页码
  if (end - start < CONFIG.maxPagesPerView - 1) {
    if (start === 1) {
      end = Math.min(totalPages, start + CONFIG.maxPagesPerView - 1);
    } else {
      start = Math.max(1, end - CONFIG.maxPagesPerView + 1);
    }
  }
  
  for (let i = start; i <= end; i++) {
    pages.push({
      page: i,
      isCurrent: i === currentPage
    });
  }
  
  return pages;
}

/**
 * 生成人性化询问文本
 */
function generateAskText(page, totalPages, hasUpdate = false) {
  let messages = [];
  
  if (hasUpdate) {
    messages.push(`\n⚠️ 检测到有技能可以更新。`);
  }
  
  messages.push(`\n这 ${page} 页的技能有没有问题？`);
  
  if (page < totalPages) {
    messages.push(`要不要看下 一页？（回复"是"或"不用"）`);
  } else {
    messages.push(`已经到最后一页了。`);
  }
  
  messages.push(`你一共装了 ${totalPages * CONFIG.pageSize} 个技能，分 ${totalPages} 页显示。`);
  
  return messages.join('\n');
}

/**
 * 验证页码是否有效
 */
function isValidPage(page, totalPages) {
  return page >= 1 && page <= totalPages;
}

/**
 * 限制页码在有效范围内
 */
function clampPage(page, totalPages) {
  return Math.max(1, Math.min(page, totalPages));
}

// 导出函数
module.exports = {
  calculatePagination,
  parseUserInput,
  formatPageInfo,
  generatePageNumbers,
  generateAskText,
  isValidPage,
  clampPage,
  CONFIG
};

// 测试
if (require.main === module) {
  console.log('测试分页逻辑：');
  console.log('--------------');
  
  const pagination = calculatePagination(23, 3);
  console.log('23 个技能，第 3 页：');
  console.log(pagination);
  
  console.log('\n页码显示：');
  console.log(generatePageNumbers(3, 5));
  
  console.log('\n询问文本：');
  console.log(generateAskText(3, 5, true));
  
  console.log('\n解析用户输入：');
  console.log('是 ->', parseUserInput('是'));
  console.log('不用 ->', parseUserInput('不用'));
  console.log('第 3 页 ->', parseUserInput('第 3 页'));
  console.log('更新 Smart Router ->', parseUserInput('更新 Smart Router'));
  console.log('🌐 ->', parseUserInput('🌐'));
}
