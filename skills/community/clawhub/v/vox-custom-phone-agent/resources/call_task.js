'use strict';

const { maskPhone } = require('./phone_validator');
const { getVoiceInfo } = require('./voice_requirements');

function buildCallTask({ intent = {}, agentProfile = {}, voiceType = '', taskBriefing = '', requestId = '' }) {
  const voice = getVoiceInfo(voiceType);
  const taskName = inferTaskName(intent, agentProfile);
  return {
    callee: intent.callee || '',
    maskedCallee: maskPhone(intent.callee),
    useMode: intent.useMode || '',
    requestId,
    taskName,
    scenarioDescription: agentProfile.background || intent.scenario || taskName,
    taskBriefing,
    voice,
    agentProfile
  };
}

function inferTaskName(intent = {}, agentProfile = {}) {
  const text = `${intent.scenario || ''} ${agentProfile.role || ''} ${agentProfile.goals || ''}`;
  if (/售后|维修|满意/.test(text)) return '售后维修回访';
  if (/课程|试听|培训/.test(text)) return '课程体验邀约';
  if (/会议|活动|通知/.test(text)) return '通知提醒';
  if (/聊天|陪伴|关怀/.test(text)) return '关怀聊天';
  if (/商务|合作/.test(text)) return '商务沟通';
  if (/健康|体检|用药/.test(text)) return '健康提醒';
  return intent.scenario || '自定义电话任务';
}

module.exports = { buildCallTask, inferTaskName };
