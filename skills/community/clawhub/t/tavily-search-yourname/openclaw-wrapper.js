const { execSync } = require('child_process');
const query = process.argv[2] || '';

if (!query) {
  console.log('请提供搜索关键词');
  process.exit(1);
}

try {
  const result = execSync(`node scripts/search.mjs "${query}" -n 5 --topic news`, {
    env: { ...process.env, TAVILY_API_KEY: process.env.TAVILY_API_KEY }
  }).toString();
  console.log(result);
} catch (error) {
  console.error('搜索失败:', error.message);
}