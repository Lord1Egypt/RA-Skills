// 预测比赛结果
var data = require('../utils/data.js')

// 中文球队名→代码映射
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
  // 直接是3字母代码
  if (s.length === 3 && data.TEAM_STATS[s.toUpperCase()]) return s.toUpperCase()
  // 英文名
  var upper = s.toUpperCase()
  for (var code in data.TEAM_STATS) {
    if (code === upper) return code
  }
  // 中文名
  if (NAME_TO_CODE[s]) return NAME_TO_CODE[s]
  // 模糊匹配
  for (var name in NAME_TO_CODE) {
    if (s.indexOf(name) >= 0 || name.indexOf(s) >= 0) return NAME_TO_CODE[name]
  }
  return null
}

async function predictMatch({ teamA, teamB } = {}) {
  try {
    if (!teamA || !teamB) {
      return {
        isError: true,
        content: [{ type: 'text', text: '缺少球队参数。请反问用户想预测哪两支球队的比赛。' }]
      }
    }
    var codeA = resolveTeamCode(teamA)
    var codeB = resolveTeamCode(teamB)
    if (!codeA) {
      return {
        isError: true,
        content: [{ type: 'text', text: '无法识别球队「' + teamA + '」。请引导用户使用正确的球队名称或代码。' }]
      }
    }
    if (!codeB) {
      return {
        isError: true,
        content: [{ type: 'text', text: '无法识别球队「' + teamB + '」。请引导用户使用正确的球队名称或代码。' }]
      }
    }
    if (codeA === codeB) {
      return {
        isError: true,
        content: [{ type: 'text', text: '两支球队不能相同。请反问用户想预测哪两支不同球队的比赛。' }]
      }
    }
    var prediction = data.predictMatch(codeA, codeB)
    return {
      isError: false,
      content: [{
        type: 'text',
        text: '已生成 ' + prediction.teamAName + ' vs ' + prediction.teamBName + ' 的预测结果。接下来为用户展示预测卡片，必须附加"预测仅供娱乐参考"的免责说明。禁止以纯文本展开预测详情。'
      }],
      structuredContent: prediction,
      _meta: {
        viewPrediction: prediction
      }
    }
  } catch (err) {
    console.error('[predictMatch] error', err)
    return {
      isError: true,
      content: [{ type: 'text', text: '预测失败：' + (err.message || '未知错误') + '。请引导用户稍后重试。' }]
    }
  }
}
module.exports = predictMatch
