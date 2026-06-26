'use strict';

const VOICE_TYPES = {
  COMFORT: '0',
  ELDER: '1',
  BUSINESS: '2',
  NOTICE: '3',
  DAILY: '4'
};

const VOICE_OPTIONS_TEXT = '请选择音色：0 知愈（女，安抚/回访）；1 安辰（男，长辈/老人）；2 景珩（男，商务/课程/科普）；3 知言（女，通知/公告）；4 星苒（女，闲聊/电商/生活服务）。';

const VOICE_OPTIONS = [
  { id: 'voice_0', value: '0', code: '0', name: '知愈', gender: '女', label: '0 知愈（女）', description: '适合情绪安抚、心理陪伴、售后回访、不知道选什么' },
  { id: 'voice_1', value: '1', code: '1', name: '安辰', gender: '男', label: '1 安辰（男）', description: '适合给长辈/老人做的任何语音内容' },
  { id: 'voice_2', value: '2', code: '2', name: '景珩', gender: '男', label: '2 景珩（男）', description: '适合商务沟通、企业合作、科普讲解、课程介绍' },
  { id: 'voice_3', value: '3', code: '3', name: '知言', gender: '女', label: '3 知言（女）', description: '适合通知、公告、正式播报类内容' },
  { id: 'voice_4', value: '4', code: '4', name: '星苒', gender: '女', label: '4 星苒（女）', description: '适合日常闲聊、陪伴、电商带货、生活服务类内容' }
];

function parseVoiceType(text) {
  const value = String(text || '');
  if (/(?:voiceType|音色|声音|声线)\s*[:：=]?\s*([0-4])/.test(value)) return value.match(/(?:voiceType|音色|声音|声线)\s*[:：=]?\s*([0-4])/)[1];
  if (/(?:选|用|使用)\s*([0-4])\s*(?:号|号音色|音色)?/.test(value)) return value.match(/(?:选|用|使用)\s*([0-4])\s*(?:号|号音色|音色)?/)[1];
  if (/知愈/.test(value)) return VOICE_TYPES.COMFORT;
  if (/安辰/.test(value)) return VOICE_TYPES.ELDER;
  if (/景珩/.test(value)) return VOICE_TYPES.BUSINESS;
  if (/知言/.test(value)) return VOICE_TYPES.NOTICE;
  if (/星苒/.test(value)) return VOICE_TYPES.DAILY;
  if (/(?:轻松|自然|亲切|活泼|日常|随和|聊天|闲聊|陪聊|生活感).*(?:女声|女生|女性|声音|声线)|(?:女声|女生|女性|声音|声线).*(?:轻松|自然|亲切|活泼|日常|随和|聊天|闲聊|陪聊|生活感)/.test(value)) return VOICE_TYPES.DAILY;
  if (/(?:温柔|柔和|安抚|耐心|舒缓|关怀|陪伴).*(?:女声|女生|女性|声音|声线)|(?:女声|女生|女性|声音|声线).*(?:温柔|柔和|安抚|耐心|舒缓|关怀|陪伴)/.test(value)) return VOICE_TYPES.COMFORT;
  if (/(?:成熟|稳重|低沉|可靠|长辈|老人|健康).*(?:男声|男生|男性|声音|声线)|(?:男声|男生|男性|声音|声线).*(?:成熟|稳重|低沉|可靠|长辈|老人|健康)/.test(value)) return VOICE_TYPES.ELDER;
  if (/(?:专业|商务|清晰|理性|课程|销售|介绍|科普).*(?:男声|男生|男性|声音|声线)|(?:男声|男生|男性|声音|声线).*(?:专业|商务|清晰|理性|课程|销售|介绍|科普)/.test(value)) return VOICE_TYPES.BUSINESS;
  if (/(?:正式|清楚|标准|播报|通知|公告|提醒).*(?:女声|女生|女性|声音|声线)|(?:女声|女生|女性|声音|声线).*(?:正式|清楚|标准|播报|通知|公告|提醒)/.test(value)) return VOICE_TYPES.NOTICE;
  if (/(?:轻松|自然|亲切|活泼|日常|随和|聊天|闲聊|陪聊|生活感)/.test(value)) return VOICE_TYPES.DAILY;
  if (/(?:温柔|柔和|安抚|耐心|舒缓|关怀|陪伴)/.test(value)) return VOICE_TYPES.COMFORT;
  if (/(?:成熟|稳重|低沉|可靠)/.test(value)) return VOICE_TYPES.ELDER;
  if (/女声.*(?:安抚|回访|售后)|(?:安抚|回访|售后).*女声/.test(value)) return VOICE_TYPES.COMFORT;
  if (/男声.*(?:老人|长辈|健康|用药)|(?:老人|长辈|健康|用药).*男声/.test(value)) return VOICE_TYPES.ELDER;
  if (/男声.*(?:商务|课程|科普|销售)|(?:商务|课程|科普|销售).*男声/.test(value)) return VOICE_TYPES.BUSINESS;
  if (/女声.*(?:通知|公告|正式)|(?:通知|公告|正式).*女声/.test(value)) return VOICE_TYPES.NOTICE;
  if (/女声.*(?:生活|电商|闲聊)|(?:生活|电商|闲聊).*女声/.test(value)) return VOICE_TYPES.DAILY;
  return '';
}

function chooseVoiceType(intent = {}) {
  if (intent.voiceType && /^[0-4]$/.test(String(intent.voiceType))) {
    return String(intent.voiceType);
  }

  const text = [intent.scenario, intent.role, intent.goal, intent.background, intent.rawPrompt]
    .filter(Boolean)
    .join(' ');

  if (/老人|长辈|父母|用药|服药|体检|健康|复诊/.test(text)) return VOICE_TYPES.ELDER;
  if (/售后|回访|满意|投诉|安抚|心理|陪伴|情绪/.test(text)) return VOICE_TYPES.COMFORT;
  if (/商务|合作|企业|销售|课程|顾问|邀约|介绍|产品|科普/.test(text)) return VOICE_TYPES.BUSINESS;
  if (/通知|公告|会议|面试|提醒|变更|预约|确认|报名|签到/.test(text)) return VOICE_TYPES.NOTICE;
  if (/生活|电商|导购|闲聊|活动|服务/.test(text)) return VOICE_TYPES.DAILY;

  return VOICE_TYPES.NOTICE;
}

module.exports = { VOICE_TYPES, VOICE_OPTIONS, VOICE_OPTIONS_TEXT, chooseVoiceType, parseVoiceType };
