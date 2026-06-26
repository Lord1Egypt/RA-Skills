'use strict';

const VOICE_INFO = {
  '0': { type: '0', name: '知愈', gender: '女', reason: '适合售后回访、情绪安抚、心理陪伴' },
  '1': { type: '1', name: '安辰', gender: '男', reason: '适合长辈、老人、用药或健康提醒' },
  '2': { type: '2', name: '景珩', gender: '男', reason: '适合商务沟通、课程介绍、企业合作、科普讲解' },
  '3': { type: '3', name: '知言', gender: '女', reason: '适合通知、公告、正式播报类内容' },
  '4': { type: '4', name: '星苒', gender: '女', reason: '适合日常闲聊、陪伴、电商和生活服务' }
};

function getVoiceInfo(voiceType) {
  return VOICE_INFO[String(voiceType)] || { type: String(voiceType || ''), name: '未知音色', gender: '', reason: '' };
}

function analyzeVoiceRequirement(intent = {}, voiceType = '') {
  const voice = getVoiceInfo(voiceType);
  const text = [intent.scenario, intent.role, intent.goal, intent.rawPrompt].filter(Boolean).join(' ');
  const recommended = recommendedVoiceTypes(text);
  const scenarioFit = recommended.includes(String(voiceType)) ? 'high' : 'medium';
  return {
    selectedVoiceType: voice.type,
    selectedVoiceName: voice.name,
    gender: voice.gender,
    scenarioFit,
    reason: voice.reason,
    recommendedVoices: recommended.map(getVoiceInfo),
    deliveryStyle: inferDeliveryStyle(text),
    warnings: scenarioFit === 'high' ? [] : [`当前场景更推荐：${recommended.map((v) => getVoiceInfo(v).name).join('、')}`]
  };
}

function recommendedVoiceTypes(text) {
  if (/老人|长辈|体检|用药|健康/.test(text)) return ['1', '0', '3'];
  if (/售后|维修|回访|满意|投诉/.test(text)) return ['0', '3', '4'];
  if (/课程|商务|合作|销售|科普/.test(text)) return ['2', '4', '3'];
  if (/聊天|陪伴|关怀|闲聊/.test(text)) return ['4', '0', '1'];
  if (/会议|活动|通知|面试/.test(text)) return ['3', '2', '0'];
  return ['3', '0', '2'];
}

function inferDeliveryStyle(text) {
  if (/老人|长辈|体检|用药|健康/.test(text)) return ['语速稍慢', '短句优先', '温和清楚'];
  if (/售后|维修|回访|投诉/.test(text)) return ['耐心', '真诚', '安抚', '避免连续追问'];
  if (/聊天|陪伴|关怀/.test(text)) return ['自然', '轻松', '尊重', '控制时长'];
  if (/会议|活动|通知/.test(text)) return ['正式', '简洁', '清晰'];
  return ['礼貌', '清晰', '专业'];
}

module.exports = { VOICE_INFO, analyzeVoiceRequirement, getVoiceInfo };
