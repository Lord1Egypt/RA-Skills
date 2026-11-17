// 获取已完赛比赛结果
var data = require('../utils/data.js')

async function getMatchResult({ count } = {}) {
  try {
    var n = count || 5
    var matches = data.getRecentResults(n)
    return {
      isError: false,
      content: [{
        type: 'text',
        text: '已加载 ' + matches.length + ' 场已完赛比赛结果。接下来为用户展示比赛结果卡片，禁止以纯文本列出比分详情。'
      }],
      structuredContent: {
        matches: matches,
        total: matches.length
      },
      _meta: {
        viewItems: matches
      }
    }
  } catch (err) {
    console.error('[getMatchResult] error', err)
    return {
      isError: true,
      content: [{ type: 'text', text: '获取结果失败：' + (err.message || '未知错误') + '。请引导用户稍后重试。' }]
    }
  }
}
module.exports = getMatchResult
