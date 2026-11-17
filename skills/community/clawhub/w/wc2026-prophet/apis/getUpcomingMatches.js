// 获取即将进行的比赛
var data = require('../utils/data.js')

async function getUpcomingMatches({ count } = {}) {
  try {
    var n = count || 5
    var matches = data.getUpcomingMatches(n)
    return {
      isError: false,
      content: [{
        type: 'text',
        text: '已加载 ' + matches.length + ' 场即将进行的比赛。接下来为用户展示比赛列表卡片，用简短话术引导用户查看，禁止以纯文本列出比赛详情。'
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
    console.error('[getUpcomingMatches] error', err)
    return {
      isError: true,
      content: [{ type: 'text', text: '获取赛程失败：' + (err.message || '未知错误') + '。请引导用户稍后重试。' }]
    }
  }
}
module.exports = getUpcomingMatches
