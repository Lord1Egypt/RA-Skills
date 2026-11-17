// 获取冠军预测
var data = require('../utils/data.js')

async function getChampionPrediction() {
  try {
    var pred = data.CHAMPION_PREDICTION
    return {
      isError: false,
      content: [{
        type: 'text',
        text: '已加载冠军预测数据，Top5概率合计 ' + pred.top5Total + '%。接下来为用户展示冠军预测卡片，必须附加"预测仅供娱乐参考"的免责说明。禁止以纯文本展开预测详情。'
      }],
      structuredContent: pred,
      _meta: {
        viewPrediction: pred
      }
    }
  } catch (err) {
    console.error('[getChampionPrediction] error', err)
    return {
      isError: true,
      content: [{ type: 'text', text: '获取冠军预测失败：' + (err.message || '未知错误') + '。请引导用户稍后重试。' }]
    }
  }
}
module.exports = getChampionPrediction
