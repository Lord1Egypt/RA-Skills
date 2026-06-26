'use strict';

function buildTaskBriefing({ intent = {}, agentProfile = {}, voice = null, risk = null }) {
  const parts = [];
  parts.push(`这通电话由 ${agentProfile.role || intent.role || '电话 Bot'} 发起。`);
  if (agentProfile.background) parts.push(`业务背景：${agentProfile.background}。`);
  if (agentProfile.goals) parts.push(`通话目标：${agentProfile.goals}。`);
  if (agentProfile.workflow) parts.push(`执行流程：${agentProfile.workflow}。`);
  if (agentProfile.constraint) parts.push(`约束边界：${agentProfile.constraint}。`);
  if (voice) parts.push(`音色要求：使用 ${voice.name || voice.selectedVoiceName}（${voice.gender || ''}），${voice.reason || '按用户选择执行'}。`);
  if (risk && risk.level !== 'low') parts.push(`风险提示：${risk.reason}。`);

  const missingBriefingFields = [];
  if (!intent.callee) missingBriefingFields.push('callee');
  if (!agentProfile.role) missingBriefingFields.push('role');
  if (!agentProfile.goals) missingBriefingFields.push('goals');
  if (!agentProfile.background || /^(售后回访|课程邀约|聊天陪伴|电话沟通任务)$/.test(agentProfile.background)) missingBriefingFields.push('specificBackground');
  if (!agentProfile.workflow) missingBriefingFields.push('workflow');
  if (!agentProfile.constraint) missingBriefingFields.push('constraint');

  const briefingQuality = missingBriefingFields.length === 0
    ? 'strong'
    : missingBriefingFields.length <= 2 ? 'medium' : 'weak';

  return {
    taskBriefing: parts.join(' '),
    briefingQuality,
    missingBriefingFields,
    briefingWarnings: buildBriefingWarnings(missingBriefingFields)
  };
}

function buildBriefingWarnings(missing) {
  const warnings = [];
  if (missing.includes('specificBackground')) warnings.push('业务背景偏泛，建议补充具体服务、产品、时间或事项。');
  if (missing.includes('workflow')) warnings.push('缺少通话流程，Bot 可能无法稳定处理分支情况。');
  if (missing.includes('constraint')) warnings.push('缺少边界约束，建议补充不能承诺或不能询问的内容。');
  return warnings;
}

module.exports = { buildTaskBriefing };
