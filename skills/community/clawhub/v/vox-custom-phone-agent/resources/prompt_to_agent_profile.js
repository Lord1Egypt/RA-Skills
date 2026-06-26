'use strict';

function buildAgentProfile(intent = {}) {
  const role = intent.role || '通知助理';
  const scenario = intent.scenario || intent.background || '电话沟通任务';
  const goal = intent.goal || '完成本次电话沟通目标';
  const style = ensureArray(intent.communicationStyle, ['礼貌', '清晰', '专业']).slice(0, 4);
  const constraint = mergeConstraints([
    intent.constraint,
    '保持礼貌',
    '尊重对方意愿',
    '不得索要敏感隐私信息',
    '默认不主动披露 AI 身份；如果对方明确询问是否 AI、机器人或真人，则如实说明是 AI 语音助手',
    '如果用户打断或插话，先简短回应用户刚才的内容，不要重复开场白或重复上一句话',
    '如果用户表示已经听过、不要重复或不方便，立即切换到确认/结束流程',
    '对方拒绝或不方便时礼貌结束'
  ]);

  return {
    name: intent.name || defaultNameForRole(role),
    gender: intent.gender || '女',
    age: Number(intent.age || 26),
    role,
    communicationStyle: style,
    background: buildBackground(intent, scenario),
    goals: buildGoals(intent, goal),
    skills: intent.skills || inferSkills(role, scenario),
    workflow: buildWorkflow(intent, role, scenario, goal),
    constraint,
    openingPrompt: intent.openingPrompt || buildOpeningPrompt(role, scenario, goal, intent)
  };
}

function ensureArray(value, fallback) {
  if (Array.isArray(value) && value.length) return value;
  if (typeof value === 'string' && value.trim()) return value.split(/[、,，\s]+/).filter(Boolean);
  return fallback;
}

function defaultNameForRole(role) {
  if (/课程|销售|商务/.test(role)) return '小林';
  if (/售后|客服/.test(role)) return '小悦';
  if (/招聘|面试/.test(role)) return '小琪';
  if (/健康|体检|用药/.test(role)) return '小安';
  if (/聊天|陪伴|关怀|社区/.test(role)) return '小暖';
  return '小知';
}

function inferSkills(role, scenario) {
  const text = `${role} ${scenario}`;
  if (/课程|销售/.test(text)) return '需求确认、业务介绍、异议处理、预约确认';
  if (/售后|回访|满意/.test(text)) return '满意度回访、原因追问、情绪安抚、人工跟进说明';
  if (/会议|通知|活动/.test(text)) return '事项通知、时间确认、关键信息复述、礼貌结束';
  if (/招聘|面试/.test(text)) return '面试通知、时间确认、地点说明、候选人沟通';
  if (/商务|合作/.test(text)) return '合作沟通、需求确认、预约后续沟通、礼貌跟进';
  if (/健康|体检|用药/.test(text)) return '事项提醒、时间确认、温和表达、官方渠道引导';
  if (/聊天|陪伴|关怀/.test(text)) return '日常寒暄、关怀陪伴、倾听回应、礼貌结束';
  return '信息传达、需求确认、礼貌沟通、结果确认';
}

function inferWorkflow(role, scenario) {
  const text = `${role} ${scenario}`;
  if (/课程|销售/.test(text)) return '问候 -> 说明来意 -> 简要介绍内容 -> 询问兴趣 -> 确认预约意愿 -> 礼貌结束';
  if (/售后|回访|满意/.test(text)) return '问候 -> 说明回访目的 -> 询问是否满意 -> 根据回答感谢或致歉 -> 如不满意询问原因 -> 说明后续跟进 -> 礼貌结束';
  if (/会议|通知|活动/.test(text)) return '问候 -> 说明通知事项 -> 复述关键时间和地点 -> 确认是否知晓 -> 礼貌结束';
  if (/招聘|面试/.test(text)) return '问候 -> 说明招聘或面试事项 -> 确认时间安排 -> 说明注意事项 -> 礼貌结束';
  if (/商务|合作/.test(text)) return '问候 -> 说明来意 -> 简要介绍合作背景 -> 确认对方兴趣 -> 预约后续沟通 -> 礼貌结束';
  if (/健康|体检|用药/.test(text)) return '问候 -> 说明提醒事项 -> 复述时间和注意事项 -> 确认是否知晓 -> 引导官方渠道咨询 -> 礼貌结束';
  if (/聊天|陪伴|关怀/.test(text)) return '问候 -> 说明关怀来意 -> 询问是否方便聊天 -> 围绕允许话题轻松交流 -> 对方不想聊则礼貌结束 -> 控制通话时长';
  return '问候 -> 说明来意 -> 沟通核心事项 -> 确认对方反馈 -> 礼貌结束';
}

function buildWorkflow(intent, role, scenario, goal) {
  const inferred = inferWorkflow(role, scenario, goal);
  const interruptionStep = '如用户打断则先回应打断内容，避免重复开场或重复上一句';
  if (/聊天|陪伴|关怀/.test(`${role} ${scenario}`)) {
    return mergeWorkflow([inferred, intent.workflow, interruptionStep]);
  }
  return mergeWorkflow([intent.workflow || inferred, interruptionStep]);
}

function mergeWorkflow(values) {
  const parts = [];
  for (const value of values) {
    if (!value) continue;
    for (const part of String(value).split(/\s*->\s*/)) {
      const clean = part.trim();
      if (clean && !parts.includes(clean)) parts.push(clean);
    }
  }
  return parts.join(' -> ');
}

function buildBackground(intent, scenario) {
  const parts = [intent.background || scenario];
  if (intent.mustSay) parts.push(`关键传达信息：${intent.mustSay}`);
  return parts.filter(Boolean).join('；');
}

function buildGoals(intent, goal) {
  const parts = [goal];
  if (intent.workflow && /如果|若|如|满意|不满意|方便|不方便/.test(intent.workflow)) {
    parts.push('按用户描述的分支流程完成多轮沟通');
  }
  if (intent.mustSay) parts.push(`必须传达：${intent.mustSay}`);
  return parts.filter(Boolean).join('；');
}

function buildOpeningPrompt(role, scenario, goal, intent = {}) {
  if (intent.mustSay && /通知|提醒|会议|活动|面试/.test(`${role} ${scenario}`)) {
    return `您好，这里是${role}，有一项信息需要和您确认：${intent.mustSay}。`;
  }
  if (/会议|通知|活动|面试/.test(`${role} ${scenario}`)) {
    return `您好，这里是${role}，想和您确认一个${scenario}事项。`;
  }
  return `您好，我是${role}，想和您沟通一下${scenario}，主要是${goal}。`;
}

function mergeConstraints(values) {
  const parts = [];
  for (const value of values) {
    if (!value) continue;
    for (const part of String(value).split(/[；;。\n]+/)) {
      const clean = part.trim();
      if (clean && !parts.includes(clean)) parts.push(clean);
    }
  }
  return parts.join('；');
}

module.exports = { buildAgentProfile };
