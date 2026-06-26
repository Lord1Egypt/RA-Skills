/**
 * 参数解析器
 * 解析 CLI 参数或 Gateway 传入的参数
 */

/**
 * 解析参数
 * 支持 --key=value 或 --key value 格式
 */
function parseArgs() {
  const args = {
    // 默认参数
    mode: 'handle',           // handle: 直接处理, build-and-handle: 先组装 prompt 再处理
    visitorUid: null,
    dbPath: null,
    prompt: null,             // Base64 编码的 prompt
    messageIds: null,         // JSON 数组，要处理的消息 ID 列表
    ownerUid: 'tjyu',         // 主人 UID
    timeout: 120,             // 子 Agent 超时时间（秒）
  };
  
  const argv = process.argv.slice(2);
  
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    
    if (arg.startsWith('--')) {
      const key = arg.slice(2).replace(/-([a-z])/g, (_, letter) => letter.toUpperCase());
      let value = argv[i + 1];
      
      // 处理 --key=value 格式
      if (arg.includes('=')) {
        const parts = arg.split('=');
        const keyName = parts[0].slice(2).replace(/-([a-z])/g, (_, letter) => letter.toUpperCase());
        args[keyName] = parts[1];
        continue;
      }
      
      // 处理 --key value 格式
      if (value && !value.startsWith('--')) {
        // 尝试解析 JSON
        if (value.startsWith('[') || value.startsWith('{')) {
          try {
            value = JSON.parse(value);
          } catch (e) {
            // 保持原样
          }
        }
        args[key] = value;
        i++;
      } else {
        // 布尔标志
        args[key] = true;
      }
    }
  }
  
  // 验证必要参数
  if (!args.visitorUid) {
    throw new Error('缺少必要参数: --visitor-uid');
  }
  
  return args;
}

module.exports = { parseArgs };
