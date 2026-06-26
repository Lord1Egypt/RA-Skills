/**
 * 时间验证函数（修复版）
 */

/**
 * 检查日期是否在过去N小时内
 * @param {string} dateStr - 日期字符串（支持多种格式）
 * @param {number} hours - 小时数（默认24）
 */
export function isWithinHours(dateStr, hours = 24) {
  if (!dateStr) return false;
  
  try {
    const date = new Date(dateStr);
    
    // 检查日期是否有效
    if (isNaN(date.getTime())) {
      return false;
    }
    
    const now = new Date();
    const diffMs = now - date;
    const hoursMs = hours * 60 * 60 * 1000;
    
    return diffMs <= hoursMs && diffMs >= 0;
  } catch (err) {
    return false;
  }
}

/**
 * 检查日期是否在过去24小时内
 */
export function isWithin24Hours(dateStr) {
  return isWithinHours(dateStr, 24);
}

/**
 * 检查日期是否在过去N天内
 */
export function isWithinDays(dateStr, days = 1) {
  return isWithinHours(dateStr, days * 24);
}

/**
 * 格式化相对时间
 */
export function formatRelativeTime(dateStr) {
  if (!dateStr) return '未知时间';
  
  try {
    const date = new Date(dateStr);
    
    if (isNaN(date.getTime())) {
      return '未知时间';
    }
    
    const now = new Date();
    const diffMs = now - date;
    
    if (diffMs < 0) {
      return '未来时间';
    }
    
    const minutes = Math.floor(diffMs / (60 * 1000));
    const hours = Math.floor(diffMs / (60 * 60 * 1000));
    const days = Math.floor(hours / 24);
    
    if (minutes < 1) {
      return '刚刚';
    } else if (minutes < 60) {
      return `${minutes}分钟前`;
    } else if (hours < 24) {
      return `${hours}小时前`;
    } else if (days < 7) {
      return `${days}天前`;
    } else {
      // 超过7天，显示具体日期
      return date.toLocaleDateString('zh-CN', {
        month: 'short',
        day: 'numeric'
      });
    }
  } catch (err) {
    return '未知时间';
  }
}

/**
 * 测试函数
 */
export function testTimeParsing() {
  const testCases = [
    'Mon, 09 Mar 2026 13:05:36 GMT',  // RFC 2822
    '2026-03-09T13:05:36Z',            // ISO 8601
    '2026-03-09 13:05:36',             // 简单格式
    'March 9, 2026',                   // 英文格式
    '2026年3月9日'                      // 中文格式
  ];
  
  console.log('🧪 时间解析测试：\n');
  
  for (const dateStr of testCases) {
    const date = new Date(dateStr);
    const isValid = !isNaN(date.getTime());
    const isRecent = isWithin24Hours(dateStr);
    const relative = formatRelativeTime(dateStr);
    
    console.log(`输入: ${dateStr}`);
    console.log(`  解析: ${isValid ? '✅' : '❌'} ${date.toISOString()}`);
    console.log(`  24h内: ${isRecent ? '✅' : '❌'}`);
    console.log(`  相对: ${relative}\n`);
  }
}

// 如果直接运行此文件，执行测试
if (import.meta.url === `file://${process.argv[1]}`) {
  testTimeParsing();
}
