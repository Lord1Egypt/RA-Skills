'use strict';

const RULES = {
  after_sales: {
    label: '售后/维修回访',
    detect: /售后|维修|回访|满意度|投诉|服务体验/,
    minRequired: 1,
    required: [
      { key: 'serviceItem', label: '是哪次维修或服务，维修内容/产品是什么', pattern: /上次|本次|昨天|今天|\d+月|\d+日|空调|手机|设备|产品|服务单|工单|订单|报修|安装|上门|维修内容|维修项目/ },
      { key: 'checkGoal', label: '希望确认哪些问题', pattern: /满意|不满意|是否解决|是否正常|体验|问题|反馈|原因|建议/ },
      { key: 'followUp', label: '不满意时是否安排人工客服跟进', pattern: /人工客服|人工|跟进|回访|记录|工单|安排|升级/ },
      { key: 'boundary', label: '不能承诺哪些事项', pattern: /不承诺|不能承诺|不得承诺|不保证|不赔偿|不退款|不承诺上门|边界/ }
    ],
    question: '请补充这次售后/维修回访的业务背景：\n1. 是哪次维修或服务，维修内容/产品是什么？\n2. 希望确认哪些问题？\n3. 如果客户不满意，是否安排人工客服跟进？\n4. 有哪些不能承诺的事项，例如赔偿、退款或上门时间？'
  },
  course_invite: {
    label: '课程/培训/体验课邀约',
    detect: /课程|培训|试听|体验课|学员|家长|公开课/,
    minRequired: 1,
    required: [
      { key: 'courseName', label: '课程名称或主题', pattern: /AI|编程|英语|数学|课程|训练营|体验课|公开课|主题/ },
      { key: 'timeOrSchedule', label: '体验课时间或活动周期', pattern: /今天|明天|后天|周末|\d+点|上午|下午|晚上|\d+月|\d+日|时间|周期/ },
      { key: 'audience', label: '适合对象', pattern: /孩子|学生|家长|成人|年级|年龄|适合|对象|人群/ },
      { key: 'target', label: '目标是预约试听、确认兴趣还是介绍课程', pattern: /预约|试听|确认|兴趣|报名|了解|介绍/ },
      { key: 'boundary', label: '不能承诺的优惠或效果', pattern: /不承诺|不能承诺|优惠|效果|保证|不保证|边界/ }
    ],
    question: '请补充课程邀约背景：\n1. 课程名称或主题是什么？\n2. 体验课时间或活动周期是什么？\n3. 适合哪些对象？\n4. 目标是预约试听、确认兴趣，还是介绍课程？\n5. 有哪些不能承诺的优惠或效果？'
  },
  meeting_notice: {
    label: '会议/活动/通知',
    detect: /会议|通知|活动|签到|公告|参会|讲座|变更/,
    minRequired: 1,
    required: [
      { key: 'content', label: '通知事项', pattern: /会议|活动|通知|讲座|签到|变更|改到|取消|提醒/ },
      { key: 'time', label: '具体时间', pattern: /今天|明天|后天|周一|周二|周三|周四|周五|周六|周日|\d+点|上午|下午|晚上|\d+月|\d+日|时间/ },
      { key: 'place', label: '地点或线上方式', pattern: /地点|会议室|线上|线下|腾讯会议|飞书|Zoom|地址|办公室|中心|楼|室/ },
      { key: 'confirmation', label: '是否需要确认参加或知晓', pattern: /确认|知晓|参加|回复|是否|能否/ }
    ],
    question: '请补充通知背景：\n1. 通知的具体事项是什么？\n2. 时间和地点/线上方式是什么？\n3. 是否需要对方确认参加或知晓？\n4. 如果对方不方便，是否允许改期或记录反馈？'
  },
  interview_invite: {
    label: '招聘/面试邀约',
    detect: /招聘|面试|候选人|简历|岗位|HR/,
    minRequired: 1,
    required: [
      { key: 'position', label: '面试岗位', pattern: /岗位|工程师|销售|运营|客服|Java|前端|后端|产品|设计|蓝领/ },
      { key: 'time', label: '面试时间', pattern: /今天|明天|后天|\d+点|上午|下午|晚上|\d+月|\d+日|时间/ },
      { key: 'methodOrPlace', label: '线上/线下面试方式或地点', pattern: /线上|线下|地点|地址|腾讯会议|飞书|Zoom|办公室|视频|现场/ },
      { key: 'backup', label: '不方便时的备选时间', pattern: /不方便|备选|改约|其他时间|大后天|另约|协调/ }
    ],
    question: '请补充面试邀约背景：\n1. 面试岗位是什么？\n2. 面试时间是什么？\n3. 面试方式是线上还是线下，地点在哪里？\n4. 如果候选人不方便，是否提供备选时间？\n5. 是否需要提醒准备材料？'
  },
  health_reminder: {
    label: '健康/体检/用药提醒',
    detect: /健康|体检|用药|服药|复诊|医院|门诊|老人|长辈/,
    minRequired: 1,
    required: [
      { key: 'time', label: '预约/提醒时间', pattern: /今天|明天|后天|\d+点|上午|下午|晚上|\d+月|\d+日|时间/ },
      { key: 'place', label: '地点或机构', pattern: /医院|门诊|体检中心|地点|地址|机构|科室/ },
      { key: 'notice', label: '提醒事项', pattern: /空腹|身份证|医保卡|报告|用药|服药|注意|携带|提醒/ },
      { key: 'boundary', label: '只做提醒不提供医疗建议', pattern: /不提供医疗建议|不诊断|只做提醒|不做诊断|边界/ }
    ],
    question: '请补充健康提醒背景：\n1. 体检/用药/复诊时间是什么？\n2. 地点或机构是什么？\n3. 需要提醒哪些注意事项？\n4. 请确认 Bot 只做提醒，不提供医疗诊断或治疗建议。'
  },
  business_contact: {
    label: '商务合作/客户沟通',
    detect: /商务|合作|客户沟通|项目合作|对接|方案|企业/,
    minRequired: 1,
    required: [
      { key: 'topic', label: '合作主题', pattern: /合作|方案|项目|系统|产品|服务|集成|采购|商务/ },
      { key: 'target', label: '电话目标', pattern: /确认兴趣|预约会议|介绍方案|了解需求|约时间|沟通|对接/ },
      { key: 'nextStep', label: '感兴趣时的下一步安排', pattern: /下一步|会议|演示|方案|资料|加微信|回访|跟进|安排/ },
      { key: 'boundary', label: '不能承诺的价格、资源或交付时间', pattern: /不承诺|不能承诺|价格|报价|交付|资源|优惠|边界/ }
    ],
    question: '请补充商务沟通背景：\n1. 合作主题是什么？\n2. 本次电话目标是介绍方案、确认兴趣，还是预约会议？\n3. 如果对方感兴趣，下一步怎么安排？\n4. 有哪些不能承诺的价格、资源或交付时间？'
  },
  chat_companion: {
    label: '聊天/陪伴/关怀沟通',
    detect: /聊天|聊聊|陪聊|陪伴|关怀|问候|近况|闲聊|生活状态/,
    minRequired: 1,
    required: [
      { key: 'relationship', label: 'Bot 应以什么身份联系对方', pattern: /社区|关怀助手|客服|朋友|朋友式关怀|志愿者|活动助理|家政|物业|身份|角色/ },
      { key: 'purpose', label: '聊天目的', pattern: /聊天|闲聊|关心|问候|了解近况|陪伴|节日|生活状态|回访|目的/ },
      { key: 'topics', label: '可以聊哪些话题', pattern: /聊天|闲聊|普通聊天|天气|吃饭|睡眠|生活|兴趣|爱好|日常|活动|话题|可以聊/ },
      { key: 'avoidTopics', label: '不能聊的话题', pattern: /不要|不能|不得|隐私|银行卡|验证码|疾病诊断|医疗建议|家庭矛盾|金钱|投资/ },
      { key: 'stop', label: '聊多久或什么时候结束', pattern: /分钟|结束|不想聊|不方便|拒绝|控制在|时长/ }
    ],
    question: '请补充聊天场景的基本边界：\n1. Bot 应以什么身份联系对方？\n2. 这次聊天的目的或可聊话题是什么？\n3. 希望聊多久，或什么情况下结束？\n可以同时说明不聊隐私、金钱、投资、医疗法律建议等敏感话题。'
  }
};

function checkBusinessContext(intent = {}) {
  const text = collectText(intent);
  const scenario = detectBusinessScenario(intent);
  const rule = RULES[scenario];
  if (!rule) return { complete: true, scenario: 'generic', missing: [], question: '', suggestedFields: [] };

  const missing = rule.required.filter((item) => !item.pattern.test(text));
  const satisfied = rule.required.length - missing.length;
  const complete = satisfied >= (rule.minRequired || rule.required.length);
  return {
    complete,
    scenario,
    label: rule.label,
    missing: missing.map((item) => item.key),
    question: rule.question,
    suggestedFields: missing.map((item) => ({ key: item.key, label: item.label }))
  };
}

function isGenericScenarioOnly(scenario, text) {
  const clean = String(text || '').replace(/\s/g, '');
  if (scenario === 'after_sales') return false;
  if (scenario === 'chat_companion') return false;
  if (scenario === 'course_invite') return false;
  return false;
}

function detectBusinessScenario(intent = {}) {
  const text = collectText(intent);
  const ordered = ['chat_companion', 'after_sales', 'course_invite', 'interview_invite', 'health_reminder', 'meeting_notice', 'business_contact'];
  for (const key of ordered) {
    if (RULES[key].detect.test(text)) return key;
  }
  return 'generic';
}

function collectText(intent = {}) {
  return [intent.scenario, intent.role, intent.goal, intent.workflow, intent.mustSay, intent.background, intent.rawPrompt]
    .filter(Boolean)
    .join(' ');
}

module.exports = {
  RULES,
  checkBusinessContext,
  detectBusinessScenario,
  isGenericScenarioOnly
};
