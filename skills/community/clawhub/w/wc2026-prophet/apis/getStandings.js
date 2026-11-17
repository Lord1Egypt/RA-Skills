// 获取小组积分榜
var data = require('../utils/data.js')

async function getStandings({ group } = {}) {
  try {
    var groups = []
    if (group) {
      // 单组
      var g = group.toUpperCase()
      var standings = data.getGroupStandings(g)
      if (!standings || standings.length === 0) {
        return {
          isError: true,
          content: [{ type: 'text', text: '未找到小组 ' + group + ' 的积分数据。请引导用户输入正确的小组字母（A-L）。' }]
        }
      }
      groups.push({ group: g, standings: standings })
    } else {
      // 全部12组
      var allGroups = Object.keys(data.GROUPS)
      allGroups.forEach(function(g) {
        var standings = data.getGroupStandings(g)
        groups.push({ group: g, standings: standings })
      })
    }
    return {
      isError: false,
      content: [{
        type: 'text',
        text: '已加载 ' + groups.length + ' 个小组的积分榜。接下来为用户展示积分榜卡片，禁止以纯文本列出积分数据。'
      }],
      structuredContent: {
        groups: groups
      },
      _meta: {
        viewGroups: groups
      }
    }
  } catch (err) {
    console.error('[getStandings] error', err)
    return {
      isError: true,
      content: [{ type: 'text', text: '获取积分榜失败：' + (err.message || '未知错误') + '。请引导用户稍后重试。' }]
    }
  }
}
module.exports = getStandings
