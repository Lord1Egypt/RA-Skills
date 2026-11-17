// 获取球队运势分析
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

var FORTUNES = [
  { text: '🔥火势旺盛，攻势如潮。今日攻击线火力全开，有望大比分取胜。', color: '红色', num: 7 },
  { text: '🌊水润万物，防守稳固。后防线坚如磐石，对手难以攻破。', color: '蓝色', num: 3 },
  { text: '🌳木生之气，中场掌控。控球率占优，节奏把握得当。', color: '绿色', num: 8 },
  { text: '⚡金光闪闪，效率至上。反击犀利，把握机会能力强。', color: '金色', num: 5 },
  { text: '🌍土蕴厚重，体能充沛。全场奔跑不息，加时赛也不怕。', color: '黄色', num: 4 },
  { text: '🌪️风起云涌，变数颇多。比赛起伏较大，需警惕冷门。', color: '紫色', num: 9 }
]

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

async function getTeamFortune({ teamCode } = {}) {
  try {
    if (!teamCode) {
      return {
        isError: true,
        content: [{ type: 'text', text: '缺少球队参数。请反问用户想查看哪支球队的运势。' }]
      }
    }
    var code = resolveTeamCode(teamCode)
    if (!code) {
      return {
        isError: true,
        content: [{ type: 'text', text: '无法识别球队「' + teamCode + '」。请引导用户使用正确的球队名称。' }]
      }
    }
    var team = data.getTeam(code)
    if (!team) {
      return {
        isError: true,
        content: [{ type: 'text', text: '未找到球队「' + teamCode + '」的数据。' }]
      }
    }
    // 基于球队代码hash选择运势（确保同一球队每次结果一致）
    var hash = 0
    for (var i = 0; i < code.length; i++) { hash = (hash * 31 + code.charCodeAt(i)) & 0x7fffffff }
    var fortune = FORTUNES[hash % FORTUNES.length]
    
    return {
      isError: false,
      content: [{
        type: 'text',
        text: '已生成 ' + team.name + ' 的运势分析。接下来为用户展示运势卡片，必须附加"仅供娱乐参考"的免责说明。'
      }],
      structuredContent: {
        teamName: team.name,
        teamFlag: team.flag,
        fortune: fortune.text,
        luckyColor: fortune.color,
        luckyNumber: fortune.num
      },
      _meta: {
        viewFortune: {
          teamName: team.name,
          teamFlag: team.flag,
          fortune: fortune.text,
          luckyColor: fortune.color,
          luckyNumber: fortune.num
        }
      }
    }
  } catch (err) {
    console.error('[getTeamFortune] error', err)
    return {
      isError: true,
      content: [{ type: 'text', text: '获取运势失败：' + (err.message || '未知错误') + '。请引导用户稍后重试。' }]
    }
  }
}
module.exports = getTeamFortune
