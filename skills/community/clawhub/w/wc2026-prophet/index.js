// 注册所有原子接口
// 必须使用 createSkill 创建 skill 实例后通过 skill.registerAPI 注册
var getUpcomingMatches = require('./apis/getUpcomingMatches.js')
var getMatchResult = require('./apis/getMatchResult.js')
var getStandings = require('./apis/getStandings.js')
var getKnockoutBracket = require('./apis/getKnockoutBracket.js')
var predictMatch = require('./apis/predictMatch.js')
var getChampionPrediction = require('./apis/getChampionPrediction.js')
var getTeamInfo = require('./apis/getTeamInfo.js')
var getTeamFortune = require('./apis/getTeamFortune.js')

// 创建 skill 实例，path 需与 app.json 中 agent.skills[].path 一致
var skill = wx.modelContext.createSkill('skills/worldcup-skill')

// 注册原子接口，name 需与 mcp.json 中声明的一致
skill.registerAPI('getUpcomingMatches', getUpcomingMatches)
skill.registerAPI('getMatchResult', getMatchResult)
skill.registerAPI('getStandings', getStandings)
skill.registerAPI('getKnockoutBracket', getKnockoutBracket)
skill.registerAPI('predictMatch', predictMatch)
skill.registerAPI('getChampionPrediction', getChampionPrediction)
skill.registerAPI('getTeamInfo', getTeamInfo)
skill.registerAPI('getTeamFortune', getTeamFortune)

console.log('[worldcup-skill] APIs registered via createSkill')
