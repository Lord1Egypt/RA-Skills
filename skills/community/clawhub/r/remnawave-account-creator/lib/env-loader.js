/**
 * Remnawave API Token 加载器
 * 
 * 从 .env 文件读取 REMNAWAVE_API_TOKEN
 * 
 * 用法:
 * const { getRemnawaveToken } = require('./lib/env-loader');
 * const token = getRemnawaveToken();
 */

const fs = require('fs');
const path = require('path');

// .env 文件路径（workspace 根目录）
const ENV_FILE = path.join(__dirname, '../../../.env');

/**
 * 从 .env 文件读取 Remnawave API Token
 * @returns {string} API Token
 * @throws {Error} 如果 .env 不存在或 Token 未配置
 */
function getRemnawaveToken() {
  try {
    if (!fs.existsSync(ENV_FILE)) {
      throw new Error(`.env 文件不存在：${ENV_FILE}`);
    }
    
    const envContent = fs.readFileSync(ENV_FILE, 'utf-8');
    const match = envContent.match(/^REMNAWAVE_API_TOKEN=(.*)$/m);
    
    if (!match || !match[1]) {
      throw new Error('REMNAWAVE_API_TOKEN 未在 .env 中配置');
    }
    
    return match[1].trim();
  } catch (error) {
    console.error('❌ 读取 Remnawave API Token 失败:', error.message);
    console.error('');
    console.error('📝 请在 .env 文件中配置:');
    console.error('   REMNAWAVE_API_TOKEN=your_token_here');
    console.error('');
    console.error(`📂 .env 文件路径：${ENV_FILE}`);
    process.exit(1);
  }
}

/**
 * 从 .env 文件读取所有 Remnawave 相关配置
 * @returns {Object} 配置对象
 */
function getRemnawaveConfig() {
  try {
    const envContent = fs.readFileSync(ENV_FILE, 'utf-8');
    
    const config = {};
    const lines = envContent.split('\n');
    
    lines.forEach(line => {
      line = line.trim();
      if (line.startsWith('#') || !line) return;
      
      const match = line.match(/^REMNAWAVE_(\w+)=(.*)$/);
      if (match) {
        const key = match[1].toLowerCase();
        const value = match[2].trim();
        config[key] = value;
      }
    });
    
    return config;
  } catch (error) {
    console.error('❌ 读取 Remnawave 配置失败:', error.message);
    process.exit(1);
  }
}

module.exports = {
  getRemnawaveToken,
  getRemnawaveConfig
};
