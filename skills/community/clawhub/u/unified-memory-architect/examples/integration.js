/**
 * 集成示例
 * 
 * 本示例展示如何将 Unified Memory Architect 集成到其他系统
 */

// 示例: REST API 包装器
const http = require('http');
const { queryByTag, queryByDate, searchMemories, getStats } = require('../memory/scripts/query.cjs');

// 创建简单的 REST API
const server = http.createServer((req, res) => {
  // CORS 头
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Content-Type', 'application/json');

  if (req.url === '/api/stats' && req.method === 'GET') {
    // GET /api/stats - 获取统计
    const stats = getStats();
    res.end(JSON.stringify({ success: true, data: stats }));
    return;
  }

  if (req.url.startsWith('/api/query/tag/') && req.method === 'GET') {
    // GET /api/query/tag/:tag - 按标签查询
    const tag = req.url.split('/').pop();
    const limit = parseInt(new URL(req.url, 'http://localhost').searchParams.get('limit') || '10');
    const results = queryByTag(tag, limit);
    res.end(JSON.stringify({ success: true, data: results }));
    return;
  }

  if (req.url.startsWith('/api/query/date/') && req.method === 'GET') {
    // GET /api/query/date/:date - 按日期查询
    const date = req.url.split('/').pop();
    const limit = parseInt(new URL(req.url, 'http://localhost').searchParams.get('limit') || '10');
    const results = queryByDate(date, limit);
    res.end(JSON.stringify({ success: true, data: results }));
    return;
  }

  if (req.url.startsWith('/api/search') && req.method === 'GET') {
    // GET /api/search?q=keyword - 全文搜索
    const keyword = new URL(req.url, 'http://localhost').searchParams.get('q') || '';
    const limit = parseInt(new URL(req.url, 'http://localhost').searchParams.get('limit') || '10');
    const results = searchMemories(keyword, limit);
    res.end(JSON.stringify({ success: true, data: results }));
    return;
  }

  // 404
  res.statusCode = 404;
  res.end(JSON.stringify({ success: false, error: 'Not Found' }));
});

// 启动服务器
const PORT = 3000;
server.listen(PORT, () => {
  console.log(`API Server running at http://localhost:${PORT}/`);
  console.log('');
  console.log('Available endpoints:');
  console.log('  GET /api/stats              - 获取系统统计');
  console.log('  GET /api/query/tag/:tag     - 按标签查询');
  console.log('  GET /api/query/date/:date   - 按日期查询');
  console.log('  GET /api/search?q=keyword   - 全文搜索');
  console.log('');
  console.log('Press Ctrl+C to stop');
});

// 测试函数
function testIntegration() {
  console.log('\n=== 集成测试 ===');
  
  // 模拟 API 调用
  const stats = getStats();
  console.log(`Stats API: ${stats.totalMemories} memories`);
  
  const reflections = queryByTag('reflection', 3);
  console.log(`Tag Query: ${reflections.length} results`);
  
  console.log('Integration test passed!');
}

// 取消注释以运行测试
// testIntegration();
