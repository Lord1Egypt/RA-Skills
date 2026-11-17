// 获取球队详细信息
var data = require('../utils/data.js')

var NAME_TO_CODE = {
  '墨西哥':'MEX','南非':'RSA','韩国':'KOR','捷克':'CZE','加拿大':'CAN','瑞士':'SUI',
  '卡塔尔':'QAT','波黑':'BIH','巴西':'BRA','摩洛哥':'MAR','海地':'HAI','苏格兰':'SCO',
  '美国':'USA','巴拉圭':'PAR','澳大利亚':'AUS','土耳其':'TUR','德国':'GER','库拉索':'CUW',
  '科特迪瓦':'CIV','厄瓜多尔':'ECU','荷兰':'NED','日本':'JPN','突尼斯':'TUN','瑞典':'SWE',
  '比利时':'BEL','埃及':'EGY','伊朗':'IRN','新西兰':'NZL','西班牙':'ESP','佛得角':'CPV',
  '沙特':'KSA','沙特阿拉伯':'KSA','乌拉圭':'URU','法国':'FRA','塞内加尔':'SEN','挪威':'NOR',
  '伊拉克':'IRQ','阿根廷':'ARG','阿尔及利亚':'ALG','奥地利':'AUT','约旦':'JOR','葡萄牙':'POR',
  '乌兹别克':'UZB','哥伦比亚':'COL','刚果':'COD','刚果民主':'COD','英格兰':'ENG','克罗地亚':'CRO',
  '加纳':'GHA','巴拿马':'PAN'
}

function resolveTeamCode(input) {
  if (!input) return null
  var s = String(input).trim()
  if (s.length === 3 && data.TEAM_STATS[s.toUpperCase()]) return s.toUpperCase()
  if (NAME_TO_CODE[s]) return NAME_TO_CODE[s]
  for (var name in NAME_TO_CODE) {
    if (s.indexOf(name) >= 0 || name.indexOf(s) >= 0) return NAME_TO_CODE[name]
  }
  return null
}

async function getTeamInfo({ teamCode } = {}) {
  try {
    if (!teamCode) {
      return {
        isError: true,
        content: [{ type: 'text', text: '缺少球队参数。请反问用户想查看哪支球队的信息。' }]
      }
    }
    var code = resolveTeamCode(teamCode)
    if (!code) {
      return {
        isError: true,
        content: [{ type: 'text', text: '无法识别球队「' + teamCode + '」。请引导用户使用正确的球队名称或代码。' }]
      }
    }
    var team = data.getTeam(code)
    if (!team) {
      return {
        isError: true,
        content: [{ type: 'text', text: '未找到球队「' + teamCode + '」的数据。' }]
      }
    }
    return {
      isError: false,
      content: [{
        type: 'text',
        text: '已加载 ' + team.name + ' 的球队信息。接下来为用户展示球队信息卡片，禁止以纯文本展开球队详情。'
      }],
      structuredContent: team,
      _meta: {
        viewTeam: team
      }
    }
  } catch (err) {
    console.error('[getTeamInfo] error', err)
    return {
      isError: true,
      content: [{ type: 'text', text: '获取球队信息失败：' + (err.message || '未知错误') + '。请引导用户稍后重试。' }]
    }
  }
}
module.exports = getTeamInfo
