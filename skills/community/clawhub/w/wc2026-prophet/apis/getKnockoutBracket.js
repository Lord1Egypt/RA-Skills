// 获取淘汰赛对阵图
var data = require('../utils/data.js')

async function getKnockoutBracket() {
  try {
    var allMatches = data.getMergedSchedule()
    var koMatches = allMatches.filter(function(m) { return m.round; })
    
    // 按轮次分组
    var roundsMap = {}
    var roundOrder = ['1/16决赛', '1/8决赛', '1/4决赛', '半决赛', '季军赛', '决赛']
    koMatches.forEach(function(m) {
      if (!roundsMap[m.round]) roundsMap[m.round] = []
      roundsMap[m.round].push(m)
    })
    
    var rounds = roundOrder.filter(function(r) { return roundsMap[r]; }).map(function(r) {
      return { round: r, matches: roundsMap[r] }
    })
    
    return {
      isError: false,
      content: [{
        type: 'text',
        text: '已加载淘汰赛对阵图，共 ' + rounds.length + ' 个轮次。接下来为用户展示对阵图卡片，禁止以纯文本列出对阵详情。'
      }],
      structuredContent: {
        rounds: rounds
      },
      _meta: {
        viewRounds: rounds
      }
    }
  } catch (err) {
    console.error('[getKnockoutBracket] error', err)
    return {
      isError: true,
      content: [{ type: 'text', text: '获取对阵图失败：' + (err.message || '未知错误') + '。请引导用户稍后重试。' }]
    }
  }
}
module.exports = getKnockoutBracket
