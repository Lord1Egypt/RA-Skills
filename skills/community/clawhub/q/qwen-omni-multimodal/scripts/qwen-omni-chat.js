#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const DEFAULT_BASE_URL =
  process.env.DASHSCOPE_BASE_URL || 'https://dashscope.aliyuncs.com/compatible-mode/v1';
const DEFAULT_MODEL = 'qwen3.5-omni-flash';
const DEFAULT_VOICE = 'Tina';
const DEFAULT_OUTPUT_SAMPLE_RATE = 24000;
const DEFAULT_HISTORY_WINDOW = 6;
const SESSION_VERSION = 1;
const SESSIONS_DIR = path.join(__dirname, '..', 'sessions');
const CONFIG_PATH = path.join(__dirname, '..', 'config.json');
const OMNI_VOICE_PROFILES = {
  'qwen3.5-omni': [
    { id: 'Tina', alias: '甜甜 Tina', description: '默认音色，甜暖自然' },
    { id: 'Cindy', alias: '林欣宜 Cindy', description: '台湾说话嗲嗲的小姐姐' },
    { id: 'Liora Mira', alias: '清欢 Liora Mira', description: '用声音织就烟火人间的温柔' },
    { id: 'Sunnybobi', alias: '知芝 Sunnybobi', description: '大大咧咧的社恐邻家姑娘' },
    { id: 'Raymond', alias: '林川野 Raymond', description: '声音清亮，爱吃外卖的宅男' },
    { id: 'Ethan', alias: '晨煦 Ethan', description: '标准普通话，带部分北方口音，阳光温暖' },
    { id: 'Theo Calm', alias: '予安 Theo Calm', description: '在静默处传递理解，在言语间疗愈人心' },
    { id: 'Serena', alias: '苏瑶 Serena', description: '温柔小姐姐' },
    { id: 'Harvey', alias: '厚 Harvey', description: '低沉温和，像咖啡与旧书' },
    { id: 'Maia', alias: '四月 Maia', description: '知性与温柔的碰撞' },
    { id: 'Evan', alias: '江晨 Evan', description: '男大学生，年下奶狗' },
    { id: 'Qiao', alias: '小乔妹 Qiao', description: '表面甜妹，个性十足' },
    { id: 'Momo', alias: '茉兔 Momo', description: '撒娇搞怪，逗你开心' },
    { id: 'Wil', alias: '伟伦 Wil', description: '在深圳长大的港台腔小哥哥' },
    { id: 'Angel', alias: '台普 - 安琪 Angel', description: '略带台式口音，甜美轻快' },
    { id: 'Li Cassian', alias: '东厂 - 李公公 Li Cassian', description: '话中三分留白、七分察言观色' },
    { id: 'Mia', alias: '温柔生活博主 - 舒然 Mia', description: '细腻治愈的慢生活声线' },
    { id: 'Joyner', alias: '喜剧担当 - 阿逗 Joyner', description: '搞笑、夸张、接地气' },
    { id: 'Gold', alias: '金爷 Gold', description: '西海岸黑人 Rapper' },
    { id: 'Katerina', alias: '卡捷琳娜 Katerina', description: '御姐音色，韵律回味十足' },
    { id: 'Ryan', alias: '甜茶 Ryan', description: '节奏拉满，戏感炸裂' },
    { id: 'Jennifer', alias: '詹妮弗 Jennifer', description: '品牌级、电影质感般美语女声' },
    { id: 'Aiden', alias: '艾登 Aiden', description: '精通厨艺的美语大男孩' },
    { id: 'Mione', alias: '敏儿 Mione', description: '成熟知性的英国邻家妹妹' },
    { id: 'Sunny', alias: '四川 - 晴儿 Sunny', description: '甜到你心里的川妹子' },
    { id: 'Dylan', alias: '北京 - 晓东 Dylan', description: '北京胡同里长大的少年' },
    { id: 'Eric', alias: '四川 - 程川 Eric', description: '跳脱市井的四川成都男子' },
    { id: 'Peter', alias: '天津 - 李彼得 Peter', description: '天津相声，专业捧哏' },
    { id: 'Joseph Chen', alias: '阿樸伯 Joseph Chen', description: '南洋老华侨' },
    { id: 'Marcus', alias: '陕西 - 秦川 Marcus', description: '面宽话短，心实声沉' },
    { id: 'Li', alias: '南京 - 老李 Li', description: '骂骂咧咧的伯伯' },
    { id: 'Rocky', alias: '粤语 - 阿强 Rocky', description: '幽默风趣的阿强，在线陪聊' },
    { id: 'Sohee', alias: '素熙 Sohee', description: '温柔开朗，情绪丰富的韩国欧尼' },
    { id: 'Lenn', alias: '莱恩 Lenn', description: '理性克制，带一点叛逆' },
    { id: 'Ono Anna', alias: '小野杏 Ono Anna', description: '鬼灵精怪的青梅竹马' },
    { id: 'Sonrisa', alias: '索尼莎 Sonrisa', description: '热情开朗的拉美大姐' },
    { id: 'Bodega', alias: '博德加 Bodega', description: '热情的西班牙大叔' },
    { id: 'Emilien', alias: '埃米尔安 Emilien', description: '浪漫的法国大哥哥' },
    { id: 'Andre', alias: '安德雷 Andre', description: '自然舒服、沉稳磁性男声' },
    { id: 'Radio Gol', alias: '拉迪奥·戈尔 Radio Gol', description: '足球诗人式解说' },
    { id: 'Alek', alias: '阿列克 Alek', description: '冷暖并存的俄语男声气质' },
    { id: 'Rizky', alias: '阿力 Rizky', description: '印尼青年小伙，声线有个性' },
    { id: 'Roya', alias: '萝雅 Roya', description: '热爱运动的自由女孩' },
    { id: 'Arda', alias: '阿尔达 Arda', description: '干净利落，带温润气质' },
    { id: 'Hana', alias: '阿幸 Hana', description: '爱狗狗的越南成熟姐姐' },
    { id: 'Dolce', alias: '多尔切 Dolce', description: '慵懒的意大利大叔' },
    { id: 'Jakub', alias: '雅克 Jakub', description: '波兰小镇文艺青年' },
    { id: 'Griet', alias: '海娜 Griet', description: '荷兰成熟又文艺的女性' },
    { id: 'Eliška', alias: '艾莉卡 Eliška', description: '传递中欧匠心与温度' },
    { id: 'Marina', alias: '玛丽娜 Marina', description: '在多元文化城市中长大的女孩' },
    { id: 'Siiri', alias: '西芮 Siiri', description: '内敛温柔，语速舒缓' },
    { id: 'Ingrid', alias: '林恩 Ingrid', description: '挪威乡村姑娘' },
    { id: 'Sigga', alias: '海娜 Sigga', description: '冰岛小镇的知性女青年' },
    { id: 'Bea', alias: '雅娜 Bea', description: '爱喝咖啡的菲律宾甜甜小姐姐' },
    { id: 'Chloe', alias: '思怡 Chloe', description: '马来西亚白领女生' }
  ],
  'qwen-omni-turbo': [
    { id: 'Cherry', alias: '辛悦', description: '阳光积极，亲切自然小姐姐' },
    { id: 'Serena', alias: '苏瑶', description: '温柔小姐姐' },
    { id: 'Ethan', alias: '晨煦', description: '标准普通话，带部分北方口音，阳光温暖' },
    { id: 'Chelsie', alias: '千雪', description: '二次元虚拟女友' }
  ],
  'qwen3-omni-flash': [
    { id: 'Cherry', alias: '辛悦', description: '阳光积极，亲切自然小姐姐' },
    { id: 'Ethan', alias: '晨煦', description: '标准普通话，带部分北方口音，阳光温暖、活力、朝气' },
    { id: 'Nofish', alias: '不吃鱼', description: '不会配音腔的过审师傅' },
    { id: 'Jennifer', alias: '詹妮弗', description: '品牌级、电影质感的美语女声' },
    { id: 'Ryan', alias: '甜茶', description: '节奏拉满，戏感炸裂，真实与张力共舞' },
    { id: 'Katerina', alias: '卡捷琳娜', description: '御姐音色，韵律回味十足' },
    { id: 'Elias', alias: '墨讲师', description: '既保持学界严谨性，又通过叙事技巧将复杂知识转化为可消化认知模块' },
    { id: 'Jada', alias: '上海-阿珍', description: '风风火火的上海姐' },
    { id: 'Dylan', alias: '北京-晓东', description: '北京胡同里长大的少年' },
    { id: 'Sunny', alias: '四川-晴儿', description: '甜到你心里的川妹子' },
    { id: 'Li', alias: '南京-老李', description: '耐心的辅导老师' },
    { id: 'Marcus', alias: '陕西-秦川', description: '面宽话短，心实声沉' },
    { id: 'Roy', alias: '闽南-阿杰', description: '海道直爽，市井活泼的台湾哥仔形象' },
    { id: 'Peter', alias: '天津-李彼得', description: '天津相声，专业捧哏' },
    { id: 'Rocky', alias: '粤语-阿强', description: '幽默风趣的阿强，在线陪聊' },
    { id: 'Kiki', alias: '粤语-阿清', description: '甜美的港味闺蜜' },
    { id: 'Eric', alias: '四川-程川', description: '一个能甩串串的四川成都男声' }
  ]
};
const OMNI_PRICING_CNY_PER_MILLION = {
  'qwen3.5-omni-plus': {
    kind: 'tiered',
    input: {
      text_image_video: [
        { maxInputTokens: 128000, unitPrice: 0.8 },
        { maxInputTokens: 256000, unitPrice: 2.0 }
      ],
      audio: 4.96
    },
    output: {
      text: [
        { maxInputTokens: 128000, unitPrice: 9.6 },
        { maxInputTokens: 256000, unitPrice: 24.0 }
      ],
      audio_only_when_text_plus_audio: 61.322
    }
  },
  'qwen3.5-omni-plus-2026-03-15': {
    kind: 'tiered',
    input: {
      text_image_video: [
        { maxInputTokens: 128000, unitPrice: 0.8 },
        { maxInputTokens: 256000, unitPrice: 2.0 }
      ],
      audio: 4.96
    },
    output: {
      text: [
        { maxInputTokens: 128000, unitPrice: 9.6 },
        { maxInputTokens: 256000, unitPrice: 24.0 }
      ],
      audio_only_when_text_plus_audio: 61.322
    }
  },
  'qwen3.5-omni-flash': {
    kind: 'tiered',
    input: {
      text_image_video: [
        { maxInputTokens: 128000, unitPrice: 0.2 },
        { maxInputTokens: 256000, unitPrice: 0.8 }
      ],
      audio: 1.24
    },
    output: {
      text: [
        { maxInputTokens: 128000, unitPrice: 4.0 },
        { maxInputTokens: 256000, unitPrice: 16.0 }
      ],
      audio_only_when_text_plus_audio: 25.551
    }
  },
  'qwen3.5-omni-flash-2026-03-15': {
    kind: 'tiered',
    input: {
      text_image_video: [
        { maxInputTokens: 128000, unitPrice: 0.2 },
        { maxInputTokens: 256000, unitPrice: 0.8 }
      ],
      audio: 1.24
    },
    output: {
      text: [
        { maxInputTokens: 128000, unitPrice: 4.0 },
        { maxInputTokens: 256000, unitPrice: 16.0 }
      ],
      audio_only_when_text_plus_audio: 25.551
    }
  },
  'qwen3-omni-flash': {
    kind: 'flat',
    input: {
      text: 1.8,
      audio: 15.8,
      image_video: 3.3
    },
    output: {
      text_pure_text_input: 6.9,
      text_multimodal_input: 12.7,
      audio_only_when_text_plus_audio: 62.6
    }
  },
  'qwen3-omni-flash-2025-12-01': {
    kind: 'flat',
    input: {
      text: 1.8,
      audio: 15.8,
      image_video: 3.3
    },
    output: {
      text_pure_text_input: 6.9,
      text_multimodal_input: 12.7,
      audio_only_when_text_plus_audio: 62.6
    }
  },
  'qwen3-omni-flash-2025-09-15': {
    kind: 'flat',
    input: {
      text: 1.8,
      audio: 15.8,
      image_video: 3.3
    },
    output: {
      text_pure_text_input: 6.9,
      text_multimodal_input: 12.7,
      audio_only_when_text_plus_audio: 62.6
    }
  },
  'qwen-omni-turbo': {
    kind: 'flat',
    input: {
      text: 0.4,
      audio: 25.0,
      image_video: 1.5
    },
    output: {
      text_pure_text_input: 1.6,
      text_multimodal_input: 4.5,
      audio_only_when_text_plus_audio: 50.0
    }
  },
  'qwen-omni-turbo-latest': {
    kind: 'flat',
    input: {
      text: 0.4,
      audio: 25.0,
      image_video: 1.5
    },
    output: {
      text_pure_text_input: 1.6,
      text_multimodal_input: 4.5,
      audio_only_when_text_plus_audio: 50.0
    }
  },
  'qwen-omni-turbo-2025-03-26': {
    kind: 'flat',
    input: {
      text: 0.4,
      audio: 25.0,
      image_video: 1.5
    },
    output: {
      text_pure_text_input: 1.6,
      text_multimodal_input: 4.5,
      audio_only_when_text_plus_audio: 50.0
    }
  },
  'qwen-omni-turbo-2025-01-19': {
    kind: 'flat',
    input: {
      text: 0.4,
      audio: 25.0,
      image_video: 1.5
    },
    output: {
      text_pure_text_input: 1.6,
      text_multimodal_input: 4.5,
      audio_only_when_text_plus_audio: 50.0
    }
  }
};

function parseArgs(argv) {
  const args = {};

  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith('--')) {
      continue;
    }

    const body = token.slice(2);
    const eqIndex = body.indexOf('=');
    let key;
    let value;

    if (eqIndex >= 0) {
      key = body.slice(0, eqIndex);
      value = body.slice(eqIndex + 1);
    } else {
      key = body;
      const next = argv[i + 1];
      if (next && !next.startsWith('--')) {
        value = next;
        i += 1;
      } else {
        value = 'true';
      }
    }

    if (args[key] === undefined) {
      args[key] = value;
    } else if (Array.isArray(args[key])) {
      args[key].push(value);
    } else {
      args[key] = [args[key], value];
    }
  }

  return args;
}

function printUsage() {
  console.log(`
Usage:
  node scripts/qwen-omni-chat.js --prompt="..." [options]
  node scripts/qwen-omni-chat.js --list-sessions
  node scripts/qwen-omni-chat.js --list-voices [--model qwen3.5-omni-flash]
  node scripts/qwen-omni-chat.js --show-session --session demo
  node scripts/qwen-omni-chat.js --clear-session --session demo

Core options:
  --prompt              Required for chat. User prompt text.
  --system              Optional system prompt.
  --model               Model name. Default: qwen3.5-omni-flash
  --selection-policy    fixed|auto. Default: fixed
  --image               Image path, URL, or data URL. Repeatable.
  --audio               Audio path, URL, or data URL.
  --video               Video path, URL, or data URL.
  --video-frames        Comma-separated image list for video-style input.
  --video-fps           FPS for video_url input. Default: 2.0
  --with-audio          Enable text+audio output.
  --voice               Output voice. Default: Tina
  --audio-out           WAV output path. Default: /tmp/qwen-omni-<timestamp>.wav
  --enable-thinking     true|false. Default: false
  --temperature         Optional number.
  --max-tokens          Optional integer.
  --dry-run             Print a sanitized request preview and exit.

Session options:
  --session             Session id for multi-turn chat.
  --new-session         Create or switch to a new session. Optional value.
  --mode                auto|continue|fresh. Default: auto
  --history-window      Recent rounds to keep verbatim. Default: 6
  --reset-session       Reset current active thread before this turn.
  --list-sessions       List saved sessions.
  --list-voices         List supported voices for the selected model family.
  --show-session        Show a session summary. Uses --session unless a value is passed.
  --clear-session       Delete a session file. Uses --session unless a value is passed.

Examples:
  node scripts/qwen-omni-chat.js --prompt="描述这张图" --image="/tmp/demo.jpg"
  node scripts/qwen-omni-chat.js --session demo --prompt="先分析这段音频" --audio="/tmp/demo.mp3"
  node scripts/qwen-omni-chat.js --session demo --prompt="提炼成三点" --mode=continue
  node scripts/qwen-omni-chat.js --session demo --prompt="现在换个新话题" --mode=fresh
`);
}

function toBoolean(value, defaultValue = false) {
  if (value === undefined) {
    return defaultValue;
  }
  if (typeof value === 'boolean') {
    return value;
  }
  return ['1', 'true', 'yes', 'on'].includes(String(value).toLowerCase());
}

function toNumber(value) {
  if (value === undefined) {
    return undefined;
  }
  const num = Number(value);
  return Number.isFinite(num) ? num : undefined;
}

function nowIso() {
  return new Date().toISOString();
}

function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function ensureEnv(name) {
  const value = process.env[name];
  if (!value) {
    throw new Error(`缺少环境变量 ${name}`);
  }
  return value;
}

function loadConfig() {
  if (!fs.existsSync(CONFIG_PATH)) {
    return {};
  }

  try {
    const raw = fs.readFileSync(CONFIG_PATH, 'utf8');
    const parsed = JSON.parse(raw);
    return parsed && typeof parsed === 'object' ? parsed : {};
  } catch (error) {
    throw new Error(`读取配置文件失败: ${CONFIG_PATH}\n${error.message}`);
  }
}

function firstNonEmpty(...values) {
  for (const value of values) {
    if (value === undefined || value === null) {
      continue;
    }
    if (typeof value === 'string' && value.trim() === '') {
      continue;
    }
    return value;
  }
  return undefined;
}

function normalizeStringList(value) {
  const items = Array.isArray(value) ? value : value === undefined || value === null ? [] : [value];
  return Array.from(
    new Set(
      items
        .flatMap((item) => String(item).split(','))
        .map((item) => item.trim())
        .filter(Boolean)
    )
  );
}

function resolveConfiguredModelCandidates(config) {
  return normalizeStringList(config.modelCandidates);
}

function getOmniModelFamily(model) {
  if (String(model).startsWith('qwen3.5-omni-plus') || String(model).startsWith('qwen3.5-omni-flash')) {
    return 'qwen3.5-omni';
  }
  if (String(model).startsWith('qwen3-omni-flash')) {
    return 'qwen3-omni-flash';
  }
  if (String(model).startsWith('qwen-omni-turbo')) {
    return 'qwen-omni-turbo';
  }
  return null;
}

function normalizeSelectionPolicy(value) {
  const policy = String(firstNonEmpty(value, 'fixed')).trim().toLowerCase();
  if (!['fixed', 'auto'].includes(policy)) {
    throw new Error(`不支持的 selectionPolicy: ${value}，可选值为 fixed|auto`);
  }
  return policy;
}

function pickCandidateByFamily(candidates, family, preferredDefaultModel) {
  if (
    preferredDefaultModel &&
    getOmniModelFamily(preferredDefaultModel) === family &&
    (!candidates.length || candidates.includes(preferredDefaultModel))
  ) {
    return preferredDefaultModel;
  }
  return candidates.find((candidate) => getOmniModelFamily(candidate) === family) || null;
}

function resolveModelSelection(args, config, context = {}) {
  const candidates = resolveConfiguredModelCandidates(config);
  const selectionPolicy = normalizeSelectionPolicy(firstNonEmpty(args['selection-policy'], config.selectionPolicy, 'fixed'));
  const explicitModel = firstNonEmpty(args.model, process.env.DASHSCOPE_MODEL);
  if (explicitModel) {
    return {
      model: explicitModel,
      source: args.model ? 'cli.model' : 'env.DASHSCOPE_MODEL',
      candidates,
      selectionPolicy,
      preferredFamily: null
    };
  }

  const configuredDefaultModel = firstNonEmpty(config.defaultModel, config.model);
  if (selectionPolicy === 'auto') {
    const preferredFamily =
      context.inputMediaType === 'audio' || context.inputMediaType === 'video'
        ? 'qwen3.5-omni'
        : 'qwen3.5-omni';
    const preferredDefaultModel =
      context.inputMediaType === 'audio' || context.inputMediaType === 'video'
        ? 'qwen3.5-omni-plus'
        : 'qwen3.5-omni-flash';
    const autoModel =
      pickCandidateByFamily(candidates, preferredFamily, configuredDefaultModel) ||
      pickCandidateByFamily(candidates, preferredFamily, preferredDefaultModel) ||
      configuredDefaultModel ||
      candidates[0] ||
      preferredDefaultModel ||
      DEFAULT_MODEL;
    return {
      model: autoModel,
      source: 'auto-policy',
      candidates,
      selectionPolicy,
      preferredFamily
    };
  }

  if (configuredDefaultModel) {
    return {
      model: configuredDefaultModel,
      source: config.defaultModel ? 'config.defaultModel' : 'config.model',
      candidates,
      selectionPolicy,
      preferredFamily: null
    };
  }

  return {
    model: DEFAULT_MODEL,
    source: 'built-in-default',
    candidates,
    selectionPolicy,
    preferredFamily: null
  };
}

function getSupportedVoices(model) {
  const family = getOmniModelFamily(model);
  return family ? OMNI_VOICE_PROFILES[family] || [] : [];
}

function resolveConfiguredVoiceByModelFamily(config, model) {
  const family = getOmniModelFamily(model);
  if (!family || !config.voiceByModelFamily || typeof config.voiceByModelFamily !== 'object') {
    return undefined;
  }
  return config.voiceByModelFamily[family];
}

function findVoiceProfile(model, rawVoice) {
  if (!rawVoice) {
    return null;
  }
  const normalized = String(rawVoice).trim().toLowerCase();
  const voices = getSupportedVoices(model);
  for (const voice of voices) {
    if (voice.id.toLowerCase() === normalized) {
      return voice;
    }
    if (voice.alias && String(voice.alias).trim().toLowerCase() === normalized) {
      return voice;
    }
  }
  return null;
}

function resolveVoiceSelection(args, config, model) {
  const configuredVoiceByModelFamily = resolveConfiguredVoiceByModelFamily(config, model);
  const requestedVoice = firstNonEmpty(
    args.voice,
    process.env.DASHSCOPE_VOICE,
    configuredVoiceByModelFamily,
    config.voice,
    DEFAULT_VOICE
  );
  const source = args.voice
    ? 'cli.voice'
    : process.env.DASHSCOPE_VOICE
      ? 'env.DASHSCOPE_VOICE'
      : configuredVoiceByModelFamily
        ? `config.voiceByModelFamily.${getOmniModelFamily(model)}`
      : config.voice
          ? 'config.voice'
          : 'built-in-default';
  const supportedVoices = getSupportedVoices(model);
  let matchedProfile = findVoiceProfile(model, requestedVoice);
  let effectiveSource = source;

  if (!matchedProfile && supportedVoices.length > 0 && !args.voice && !process.env.DASHSCOPE_VOICE && !configuredVoiceByModelFamily && config.voice) {
    matchedProfile = findVoiceProfile(model, DEFAULT_VOICE) || supportedVoices[0];
    effectiveSource = `${source}->fallback.${matchedProfile.id}`;
  }

  return {
    voice: matchedProfile ? matchedProfile.id : String(requestedVoice),
    source: effectiveSource,
    profile: matchedProfile,
    supportedVoices
  };
}

function printVoiceList(model) {
  const family = getOmniModelFamily(model) || 'unknown';
  const voices = getSupportedVoices(model);
  if (!voices.length) {
    console.log(`model=${model}`);
    console.log(`model_family=${family}`);
    console.log('voices: unavailable');
    return;
  }

  console.log(`model=${model}`);
  console.log(`model_family=${family}`);
  voices.forEach((voice) => {
    console.log(`${voice.id}\t${voice.alias}\t${voice.description}`);
  });
}

function formatSupportedVoiceList(model) {
  return getSupportedVoices(model)
    .map((voice) => `${voice.id}${voice.alias ? `(${voice.alias})` : ''}`)
    .join(', ');
}

function formatCny(value) {
  return `${value.toFixed(4)} 元`;
}

function formatRate(value) {
  return `${value.toFixed(1)} 元/百万Token`;
}

function formatRateRange(tiers) {
  const prices = Array.from(new Set((tiers || []).map((tier) => tier.unitPrice)));
  if (!prices.length) {
    return 'unavailable';
  }
  if (prices.length === 1) {
    return formatRate(prices[0]);
  }
  return `${Math.min(...prices).toFixed(1)}~${Math.max(...prices).toFixed(1)} 元/百万Token`;
}

function getOmniPricing(model) {
  if (OMNI_PRICING_CNY_PER_MILLION[model]) {
    return OMNI_PRICING_CNY_PER_MILLION[model];
  }
  if (String(model).startsWith('qwen3.5-omni-plus')) {
    return OMNI_PRICING_CNY_PER_MILLION['qwen3.5-omni-plus'];
  }
  if (String(model).startsWith('qwen3.5-omni-flash')) {
    return OMNI_PRICING_CNY_PER_MILLION['qwen3.5-omni-flash'];
  }
  if (String(model).startsWith('qwen3-omni-flash')) {
    return OMNI_PRICING_CNY_PER_MILLION['qwen3-omni-flash'];
  }
  if (String(model).startsWith('qwen-omni-turbo')) {
    return OMNI_PRICING_CNY_PER_MILLION['qwen-omni-turbo'];
  }
  return null;
}

function getTierUnitPrice(tiers, totalInputTokens) {
  if (!Array.isArray(tiers) || !tiers.length) {
    return undefined;
  }
  const normalizedTotal = Number.isFinite(totalInputTokens) ? totalInputTokens : undefined;
  if (normalizedTotal === undefined) {
    return undefined;
  }
  for (const tier of tiers) {
    if (normalizedTotal <= tier.maxInputTokens) {
      return tier.unitPrice;
    }
  }
  return tiers[tiers.length - 1].unitPrice;
}

function supportsThinkingMode(model) {
  return getOmniModelFamily(model) === 'qwen3-omni-flash';
}

function validateVideoFrames(model, videoFrames) {
  if (!videoFrames.length) {
    return;
  }

  const family = getOmniModelFamily(model);
  if (family === 'qwen3.5-omni') {
    if (videoFrames.length < 4 || videoFrames.length > 512) {
      throw new Error('Qwen3.5-Omni 的图片列表视频输入要求 4 到 512 张图片');
    }
    return;
  }

  if (family === 'qwen3-omni-flash' && (videoFrames.length < 2 || videoFrames.length > 128)) {
    throw new Error('qwen3-omni-flash 的图片列表视频输入要求 2 到 128 张图片');
  }
}

function extractNumber(...values) {
  for (const value of values) {
    if (typeof value === 'number' && Number.isFinite(value)) {
      return value;
    }
  }
  return undefined;
}

function getTokenCount(detail, keys) {
  if (!detail || typeof detail !== 'object') {
    return undefined;
  }
  for (const key of keys) {
    if (typeof detail[key] === 'number' && Number.isFinite(detail[key])) {
      return detail[key];
    }
  }
  return undefined;
}

function printPricingReminder({ model, inputMediaType, withAudio }) {
  const pricing = getOmniPricing(model);
  if (!pricing) {
    console.error('pricing region=中国内地 unavailable=未内置该模型价格');
    return;
  }

  if (pricing.kind === 'tiered') {
    const inputParts = [];
    if (inputMediaType === 'audio') {
      inputParts.push(`text/image/video:${formatRateRange(pricing.input.text_image_video)}`);
      inputParts.push(`audio:${formatRate(pricing.input.audio)}`);
    } else {
      inputParts.push(`text/image/video:${formatRateRange(pricing.input.text_image_video)}`);
    }
    const outputRate = withAudio
      ? formatRate(pricing.output.audio_only_when_text_plus_audio)
      : formatRateRange(pricing.output.text);
    console.error(
      `pricing region=中国内地 input=${inputParts.join('+')} output=${withAudio ? 'audio' : 'text'}:${outputRate} note=Qwen3.5-Omni 文本类计费按单次请求输入Token阶梯计费`
    );
    return;
  }

  const inputRate =
    inputMediaType === 'audio'
      ? pricing.input.audio
      : inputMediaType === 'image' || inputMediaType === 'video' || inputMediaType === 'video-frames'
        ? pricing.input.image_video
        : pricing.input.text;
  const outputRate = withAudio
    ? pricing.output.audio_only_when_text_plus_audio
    : inputMediaType === 'text'
      ? pricing.output.text_pure_text_input
      : pricing.output.text_multimodal_input;

  console.error(
    `pricing region=中国内地 input=${inputMediaType}:${formatRate(inputRate)} output=${withAudio ? 'audio' : 'text'}:${formatRate(outputRate)}`
  );
}

function estimateOmniCost(usage, { model, inputMediaType, withAudio }) {
  const pricing = getOmniPricing(model);
  if (!pricing || !usage || typeof usage !== 'object') {
    return null;
  }

  const promptDetails = usage.prompt_tokens_details || usage.input_tokens_details || {};
  const completionDetails = usage.completion_tokens_details || usage.output_tokens_details || {};
  const inputTextTokens = extractNumber(
    getTokenCount(promptDetails, ['text_tokens', 'text']),
    inputMediaType === 'text' ? usage.prompt_tokens : undefined,
    inputMediaType === 'text' ? usage.input_tokens : undefined
  );
  const inputAudioTokens = extractNumber(
    getTokenCount(promptDetails, ['audio_tokens', 'audio'])
  );
  const inputImageVideoTokens = extractNumber(
    getTokenCount(promptDetails, ['image_tokens', 'video_tokens', 'vision_tokens', 'image_video_tokens', 'image_video'])
  );
  const outputTextTokens = extractNumber(
    getTokenCount(completionDetails, ['text_tokens', 'text']),
    !withAudio ? usage.completion_tokens : undefined,
    !withAudio ? usage.output_tokens : undefined
  );
  const outputAudioTokens = extractNumber(
    getTokenCount(completionDetails, ['audio_tokens', 'audio'])
  );
  const totalInputTokens = extractNumber(usage.prompt_tokens, usage.input_tokens);

  const components = [];

  if (pricing.kind === 'tiered') {
    const textLikeUnitPrice = getTierUnitPrice(pricing.input.text_image_video, totalInputTokens);
    const outputTextUnitPrice = getTierUnitPrice(pricing.output.text, totalInputTokens);

    if (inputTextTokens !== undefined && textLikeUnitPrice !== undefined) {
      components.push({
        label: 'input_text',
        tokens: inputTextTokens,
        unitPrice: textLikeUnitPrice
      });
    }
    if (inputAudioTokens !== undefined) {
      components.push({
        label: 'input_audio',
        tokens: inputAudioTokens,
        unitPrice: pricing.input.audio
      });
    }
    if (inputImageVideoTokens !== undefined && textLikeUnitPrice !== undefined) {
      components.push({
        label: 'input_image_video',
        tokens: inputImageVideoTokens,
        unitPrice: textLikeUnitPrice
      });
    }
    if (!withAudio && outputTextTokens !== undefined && outputTextUnitPrice !== undefined) {
      components.push({
        label: 'output_text',
        tokens: outputTextTokens,
        unitPrice: outputTextUnitPrice
      });
    }
    if (withAudio && outputAudioTokens !== undefined) {
      components.push({
        label: 'output_audio',
        tokens: outputAudioTokens,
        unitPrice: pricing.output.audio_only_when_text_plus_audio
      });
    }

    if (!components.length) {
      return null;
    }

    const normalized = components.map((component) => ({
      ...component,
      cost: component.tokens / 1000000 * component.unitPrice
    }));
    return {
      components: normalized,
      totalCost: normalized.reduce((sum, component) => sum + component.cost, 0)
    };
  }

  if (inputTextTokens !== undefined) {
    components.push({
      label: 'input_text',
      tokens: inputTextTokens,
      unitPrice: pricing.input.text
    });
  }
  if (inputAudioTokens !== undefined) {
    components.push({
      label: 'input_audio',
      tokens: inputAudioTokens,
      unitPrice: pricing.input.audio
    });
  }
  if (inputImageVideoTokens !== undefined) {
    components.push({
      label: 'input_image_video',
      tokens: inputImageVideoTokens,
      unitPrice: pricing.input.image_video
    });
  }
  if (!withAudio && outputTextTokens !== undefined) {
    components.push({
      label: 'output_text',
      tokens: outputTextTokens,
      unitPrice: inputMediaType === 'text'
        ? pricing.output.text_pure_text_input
        : pricing.output.text_multimodal_input
    });
  }
  if (withAudio && outputAudioTokens !== undefined) {
    components.push({
      label: 'output_audio',
      tokens: outputAudioTokens,
      unitPrice: pricing.output.audio_only_when_text_plus_audio
    });
  }

  if (!components.length) {
    return null;
  }

  const normalized = components.map((component) => ({
    ...component,
    cost: component.tokens / 1000000 * component.unitPrice
  }));
  const totalCost = normalized.reduce((sum, component) => sum + component.cost, 0);
  return {
    components: normalized,
    totalCost
  };
}

function ensureSingleModality({ images, audio, video, videoFrames }) {
  const used = [
    images.length > 0 ? 'image' : null,
    audio ? 'audio' : null,
    video ? 'video' : null,
    videoFrames.length > 0 ? 'video-frames' : null
  ].filter(Boolean);

  if (used.length > 1) {
    throw new Error(`一次请求只能包含一种非文本模态，当前传入了: ${used.join(', ')}`);
  }
}

function normalizeList(value) {
  const items = Array.isArray(value) ? value : value ? [value] : [];
  return items
    .flatMap((item) => String(item).split(','))
    .map((item) => item.trim())
    .filter(Boolean);
}

function isRemote(input) {
  return /^https?:\/\//i.test(input);
}

function isDataUrl(input) {
  return /^data:/i.test(input);
}

function extnameLower(input) {
  if (isRemote(input)) {
    try {
      const parsed = new URL(input);
      return path.extname(parsed.pathname).toLowerCase().replace(/^\./, '');
    } catch (_) {
      return '';
    }
  }
  return path.extname(input).toLowerCase().replace(/^\./, '');
}

function mimeForImage(ext) {
  const map = {
    jpg: 'image/jpeg',
    jpeg: 'image/jpeg',
    png: 'image/png',
    webp: 'image/webp',
    gif: 'image/gif',
    bmp: 'image/bmp',
    tif: 'image/tiff',
    tiff: 'image/tiff'
  };
  return map[ext] || 'image/jpeg';
}

function mimeForAudio(ext) {
  const map = {
    mp3: 'audio/mpeg',
    wav: 'audio/wav',
    m4a: 'audio/mp4',
    aac: 'audio/aac',
    flac: 'audio/flac',
    ogg: 'audio/ogg',
    opus: 'audio/ogg'
  };
  return map[ext] || 'audio/mpeg';
}

function mimeForVideo(ext) {
  const map = {
    mp4: 'video/mp4',
    mov: 'video/quicktime',
    webm: 'video/webm',
    mkv: 'video/x-matroska',
    avi: 'video/x-msvideo',
    mpeg: 'video/mpeg',
    mpg: 'video/mpeg'
  };
  return map[ext] || 'video/mp4';
}

function audioFormatFor(ext) {
  const map = {
    mp3: 'mp3',
    wav: 'wav',
    m4a: 'm4a',
    aac: 'aac',
    flac: 'flac',
    ogg: 'ogg',
    opus: 'opus'
  };
  return map[ext] || 'mp3';
}

function toAbsolute(input) {
  return path.isAbsolute(input) ? input : path.resolve(process.cwd(), input);
}

function localFileToDataUrl(input, mimeResolver) {
  const absPath = toAbsolute(input);
  if (!fs.existsSync(absPath)) {
    throw new Error(`文件不存在: ${absPath}`);
  }
  const buffer = fs.readFileSync(absPath);
  const mime = mimeResolver(extnameLower(absPath));
  return `data:${mime};base64,${buffer.toString('base64')}`;
}

function materializeUrl(input, mimeResolver) {
  if (isRemote(input) || isDataUrl(input)) {
    return input;
  }
  return localFileToDataUrl(input, mimeResolver);
}

function previewMaterializeUrl(input, mimeResolver) {
  if (isRemote(input)) {
    return input;
  }
  if (isDataUrl(input)) {
    return `${String(input).slice(0, 64)}...`;
  }

  const absPath = toAbsolute(input);
  if (!fs.existsSync(absPath)) {
    throw new Error(`文件不存在: ${absPath}`);
  }
  const stats = fs.statSync(absPath);
  const mime = mimeResolver(extnameLower(absPath));
  return `[local-file path=${absPath} mime=${mime} bytes=${stats.size}]`;
}

function buildContentInternal(
  { prompt, images, audio, video, videoFrames, videoFps },
  materializers
) {
  const content = [{ type: 'text', text: prompt }];

  if (images.length > 0) {
    images.forEach((image) => {
      content.push({
        type: 'image_url',
        image_url: {
          url: materializers.image(image, mimeForImage)
        }
      });
    });
  }

  if (audio) {
    const source = isRemote(audio) || isDataUrl(audio) ? audio : toAbsolute(audio);
    const ext = extnameLower(source);
    content.push({
      type: 'input_audio',
      input_audio: {
        data: materializers.audio(audio, mimeForAudio),
        format: audioFormatFor(ext)
      }
    });
  }

  if (video) {
    content.push({
      type: 'video_url',
      video_url: {
        url: materializers.video(video, mimeForVideo),
        fps: videoFps
      }
    });
  }

  if (videoFrames.length > 0) {
    content.push({
      type: 'video',
      video: videoFrames.map((frame) => materializers.image(frame, mimeForImage))
    });
  }

  return content;
}

function buildContent({ prompt, images, audio, video, videoFrames, videoFps }) {
  return buildContentInternal(
    { prompt, images, audio, video, videoFrames, videoFps },
    {
      image: materializeUrl,
      audio: materializeUrl,
      video: materializeUrl
    }
  );
}

function buildPreviewContent({ prompt, images, audio, video, videoFrames, videoFps }) {
  return buildContentInternal(
    { prompt, images, audio, video, videoFrames, videoFps },
    {
      image: previewMaterializeUrl,
      audio: previewMaterializeUrl,
      video: previewMaterializeUrl
    }
  );
}

function wavHeader(dataLength, sampleRate, channels, bitsPerSample) {
  const header = Buffer.alloc(44);
  const byteRate = sampleRate * channels * bitsPerSample / 8;
  const blockAlign = channels * bitsPerSample / 8;

  header.write('RIFF', 0);
  header.writeUInt32LE(36 + dataLength, 4);
  header.write('WAVE', 8);
  header.write('fmt ', 12);
  header.writeUInt32LE(16, 16);
  header.writeUInt16LE(1, 20);
  header.writeUInt16LE(channels, 22);
  header.writeUInt32LE(sampleRate, 24);
  header.writeUInt32LE(byteRate, 28);
  header.writeUInt16LE(blockAlign, 32);
  header.writeUInt16LE(bitsPerSample, 34);
  header.write('data', 36);
  header.writeUInt32LE(dataLength, 40);
  return header;
}

function writePcmAsWav(chunks, outputPath) {
  ensureDir(path.dirname(outputPath));
  const pcm = Buffer.concat(chunks);
  const header = wavHeader(pcm.length, DEFAULT_OUTPUT_SAMPLE_RATE, 1, 16);
  fs.writeFileSync(outputPath, Buffer.concat([header, pcm]));
}

function extractTextFromDelta(delta) {
  if (typeof delta.content === 'string') {
    return delta.content;
  }

  if (Array.isArray(delta.content)) {
    return delta.content
      .map((item) => {
        if (typeof item === 'string') {
          return item;
        }
        if (item && typeof item.text === 'string') {
          return item.text;
        }
        return '';
      })
      .join('');
  }

  return '';
}

function sanitizeSessionId(input) {
  const raw = String(input || '').trim();
  if (!raw) {
    return '';
  }
  return raw.replace(/[^a-zA-Z0-9._-]+/g, '-').replace(/^-+|-+$/g, '');
}

function generateSessionId() {
  const stamp = new Date().toISOString().replace(/[:.]/g, '-');
  const random = Math.random().toString(36).slice(2, 8);
  return `session-${stamp}-${random}`;
}

function sessionFilePath(sessionId) {
  ensureDir(SESSIONS_DIR);
  return path.join(SESSIONS_DIR, `${sessionId}.json`);
}

function createSession(sessionId) {
  return {
    version: SESSION_VERSION,
    id: sessionId,
    created_at: nowIso(),
    updated_at: nowIso(),
    context_start_index: 0,
    turns: []
  };
}

function loadSession(sessionId) {
  const filePath = sessionFilePath(sessionId);
  if (!fs.existsSync(filePath)) {
    return createSession(sessionId);
  }

  const parsed = JSON.parse(fs.readFileSync(filePath, 'utf8'));
  return {
    version: parsed.version || SESSION_VERSION,
    id: parsed.id || sessionId,
    created_at: parsed.created_at || nowIso(),
    updated_at: parsed.updated_at || nowIso(),
    context_start_index: Number.isInteger(parsed.context_start_index) ? parsed.context_start_index : 0,
    turns: Array.isArray(parsed.turns) ? parsed.turns : []
  };
}

function saveSession(session) {
  session.updated_at = nowIso();
  fs.writeFileSync(sessionFilePath(session.id), JSON.stringify(session, null, 2), 'utf8');
}

function deleteSession(sessionId) {
  const filePath = sessionFilePath(sessionId);
  if (fs.existsSync(filePath)) {
    fs.unlinkSync(filePath);
    return true;
  }
  return false;
}

function listSessions() {
  ensureDir(SESSIONS_DIR);
  const files = fs
    .readdirSync(SESSIONS_DIR)
    .filter((name) => name.endsWith('.json'))
    .sort();

  return files.map((fileName) => {
    const filePath = path.join(SESSIONS_DIR, fileName);
    const session = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    const activeTurns = getActiveTurns(session);
    return {
      id: session.id || fileName.replace(/\.json$/, ''),
      updated_at: session.updated_at || nowIso(),
      total_turns: Array.isArray(session.turns) ? session.turns.length : 0,
      active_turns: activeTurns.length
    };
  });
}

function getActiveTurns(session) {
  const start = Math.min(
    Math.max(session.context_start_index || 0, 0),
    Array.isArray(session.turns) ? session.turns.length : 0
  );
  return session.turns.slice(start);
}

function resetActiveContext(session) {
  session.context_start_index = session.turns.length;
  session.updated_at = nowIso();
}

function hasMediaInput({ images, audio, video, videoFrames }) {
  return images.length > 0 || Boolean(audio) || Boolean(video) || videoFrames.length > 0;
}

function getMediaType({ images, audio, video, videoFrames }) {
  if (images.length > 0) {
    return 'image';
  }
  if (audio) {
    return 'audio';
  }
  if (video) {
    return 'video';
  }
  if (videoFrames.length > 0) {
    return 'video-frames';
  }
  return 'text';
}

function createUserTurn({ prompt, images, audio, video, videoFrames, videoFps, mode }) {
  return {
    role: 'user',
    created_at: nowIso(),
    prompt,
    mode,
    media: {
      type: getMediaType({ images, audio, video, videoFrames }),
      images,
      audio: audio || null,
      video: video || null,
      video_frames: videoFrames,
      video_fps: videoFps
    }
  };
}

function createAssistantTurn({ text, transcript, usage, audioOut }) {
  return {
    role: 'assistant',
    created_at: nowIso(),
    text: text || '',
    transcript: transcript || '',
    usage: usage || null,
    audio_out: audioOut || null
  };
}

function buildContentFromUserTurn(turn, preview = false) {
  const media = turn.media || {};
  const builder = preview ? buildPreviewContent : buildContent;
  return builder({
    prompt: turn.prompt || '',
    images: Array.isArray(media.images) ? media.images : [],
    audio: media.audio || undefined,
    video: media.video || undefined,
    videoFrames: Array.isArray(media.video_frames) ? media.video_frames : [],
    videoFps: media.video_fps || 2.0
  });
}

function turnToMessage(turn, preview = false) {
  if (turn.role === 'user') {
    return {
      role: 'user',
      content: buildContentFromUserTurn(turn, preview)
    };
  }

  const text = typeof turn.text === 'string' && turn.text ? turn.text : turn.transcript || '';
  return {
    role: 'assistant',
    content: text
  };
}

function truncatePreviewValue(value, limit = 240) {
  if (typeof value === 'string') {
    return value.length > limit ? `${value.slice(0, limit)}...` : value;
  }
  if (Array.isArray(value)) {
    return value.map((item) => truncatePreviewValue(item, limit));
  }
  if (value && typeof value === 'object') {
    return Object.fromEntries(
      Object.entries(value).map(([key, item]) => [key, truncatePreviewValue(item, limit)])
    );
  }
  return value;
}

function ellipsis(text, limit = 120) {
  const value = String(text || '').replace(/\s+/g, ' ').trim();
  if (value.length <= limit) {
    return value;
  }
  return `${value.slice(0, Math.max(limit - 1, 1))}…`;
}

function summarizeTurns(turns, limit = 12) {
  if (!turns.length) {
    return '';
  }

  const lines = [];
  turns.forEach((turn) => {
    if (turn.role === 'user') {
      const mediaType = turn.media && turn.media.type && turn.media.type !== 'text'
        ? ` [${turn.media.type}]`
        : '';
      lines.push(`用户${mediaType}: ${ellipsis(turn.prompt, 80)}`);
      return;
    }

    const text = turn.text || turn.transcript || '';
    if (text) {
      lines.push(`助手: ${ellipsis(text, 90)}`);
    }
  });

  return lines.slice(-limit).join('\n');
}

function sliceTurnsByRecentRounds(turns, rounds) {
  if (!turns.length || rounds <= 0) {
    return turns.slice();
  }

  let seenUsers = 0;
  let startIndex = 0;

  for (let i = turns.length - 1; i >= 0; i -= 1) {
    if (turns[i].role === 'user') {
      seenUsers += 1;
      if (seenUsers > rounds) {
        startIndex = i + 1;
        break;
      }
    }
  }

  return turns.slice(startIndex);
}

function detectAutoMode({ prompt, hasMedia, activeTurns }) {
  if (!activeTurns.length) {
    return 'fresh';
  }

  const text = String(prompt || '').trim();
  const continuePattern = /(继续|接着|刚才|上一轮|上一个|基于刚才|结合刚才|延续|再详细|再展开|继续分析)/i;
  const freshPattern = /(新话题|新问题|重新开始|换个|另外一个|忽略前文|不要参考前文|重置|全新问题)/i;

  if (freshPattern.test(text)) {
    return 'fresh';
  }
  if (continuePattern.test(text)) {
    return 'continue';
  }
  if (hasMedia) {
    return 'fresh';
  }
  return 'continue';
}

function resolveMode({ requestedMode, prompt, hasMedia, activeTurns }) {
  if (!requestedMode || requestedMode === 'auto') {
    return detectAutoMode({ prompt, hasMedia, activeTurns });
  }
  if (!['fresh', 'continue'].includes(requestedMode)) {
    throw new Error(`不支持的 --mode: ${requestedMode}，可选值为 auto|continue|fresh`);
  }
  return requestedMode;
}

function resolveSessionId(args) {
  const direct = sanitizeSessionId(args.session);
  if (direct) {
    return direct;
  }

  if (args['new-session'] && args['new-session'] !== 'true') {
    const named = sanitizeSessionId(args['new-session']);
    if (!named) {
      throw new Error('无效的 session id');
    }
    return named;
  }

  if (toBoolean(args['new-session'], false)) {
    return generateSessionId();
  }

  return '';
}

function resolveTargetSessionId(flagValue, args) {
  if (flagValue && flagValue !== 'true') {
    const target = sanitizeSessionId(flagValue);
    if (!target) {
      throw new Error('无效的 session id');
    }
    return target;
  }

  const target = sanitizeSessionId(args.session);
  if (!target) {
    throw new Error('请通过 --session 指定 session id');
  }
  return target;
}

function printSessionList() {
  const sessions = listSessions();
  if (!sessions.length) {
    console.log('没有已保存的会话。');
    return;
  }

  sessions.forEach((session) => {
    console.log(
      `${session.id}\tupdated=${session.updated_at}\tactive_turns=${session.active_turns}\ttotal_turns=${session.total_turns}`
    );
  });
}

function printSessionDetails(session, historyWindow) {
  const activeTurns = getActiveTurns(session);
  const recentTurns = sliceTurnsByRecentRounds(activeTurns, historyWindow);
  const olderTurns = activeTurns.slice(0, Math.max(activeTurns.length - recentTurns.length, 0));

  console.log(`session: ${session.id}`);
  console.log(`created_at: ${session.created_at}`);
  console.log(`updated_at: ${session.updated_at}`);
  console.log(`total_turns: ${session.turns.length}`);
  console.log(`active_turns: ${activeTurns.length}`);
  console.log(`archived_turns: ${session.turns.length - activeTurns.length}`);

  if (olderTurns.length > 0) {
    console.log('\nolder_summary:');
    console.log(summarizeTurns(olderTurns) || '(empty)');
  }

  if (recentTurns.length > 0) {
    console.log('\nrecent_turns:');
    recentTurns.forEach((turn) => {
      if (turn.role === 'user') {
        const mediaType = turn.media && turn.media.type ? turn.media.type : 'text';
        console.log(`- user [${mediaType}] ${ellipsis(turn.prompt, 120)}`);
      } else {
        console.log(`- assistant ${ellipsis(turn.text || turn.transcript || '', 120)}`);
      }
    });
  }
}

async function streamChatCompletion({ apiKey, baseUrl, payload, audioOut }) {
  const response = await fetch(`${baseUrl}/chat/completions`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`请求失败: ${response.status} ${response.statusText}\n${errorText}`);
  }

  if (!response.body) {
    throw new Error('服务端没有返回可读取的流');
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder('utf-8');
  let lineBuffer = '';
  let eventLines = [];
  const audioChunks = [];
  let reasoning = '';
  let transcript = '';
  let assistantText = '';
  let usage = null;

  function handleEventData(data) {
    if (!data || data === '[DONE]') {
      return;
    }

    const parsed = JSON.parse(data);
    if (parsed.usage) {
      usage = parsed.usage;
    }

    const choice = Array.isArray(parsed.choices) ? parsed.choices[0] : null;
    const delta = choice && choice.delta ? choice.delta : null;
    if (!delta) {
      return;
    }

    if (typeof delta.reasoning_content === 'string' && delta.reasoning_content) {
      reasoning += delta.reasoning_content;
      process.stderr.write(delta.reasoning_content);
    }

    const text = extractTextFromDelta(delta);
    if (text) {
      assistantText += text;
      process.stdout.write(text);
    }

    if (delta.audio && typeof delta.audio.transcript === 'string') {
      transcript += delta.audio.transcript;
    }

    if (delta.audio && typeof delta.audio.data === 'string' && delta.audio.data) {
      audioChunks.push(Buffer.from(delta.audio.data, 'base64'));
    }
  }

  function flushEvent() {
    if (eventLines.length === 0) {
      return;
    }
    const data = eventLines.join('\n');
    eventLines = [];
    handleEventData(data);
  }

  while (true) {
    const { done, value } = await reader.read();
    if (done) {
      break;
    }

    lineBuffer += decoder.decode(value, { stream: true }).replace(/\r/g, '');

    while (true) {
      const newlineIndex = lineBuffer.indexOf('\n');
      if (newlineIndex === -1) {
        break;
      }

      const line = lineBuffer.slice(0, newlineIndex);
      lineBuffer = lineBuffer.slice(newlineIndex + 1);

      if (line === '') {
        flushEvent();
        continue;
      }

      if (line.startsWith('data:')) {
        eventLines.push(line.slice(5).trimStart());
      }
    }
  }

  if (lineBuffer.startsWith('data:')) {
    eventLines.push(lineBuffer.slice(5).trimStart());
  }
  flushEvent();

  process.stdout.write('\n');
  if (reasoning) {
    process.stderr.write('\n');
  }

  let savedAudioPath = null;
  if (audioChunks.length > 0) {
    writePcmAsWav(audioChunks, audioOut);
    savedAudioPath = audioOut;
    console.error(`音频已保存: ${audioOut}`);
    if (transcript) {
      console.error(`音频转写: ${transcript}`);
    }
  }

  if (usage) {
    console.error(`Usage: ${JSON.stringify(usage)}`);
  }

  return {
    assistantText,
    reasoning,
    transcript,
    usage,
    savedAudioPath
  };
}

async function main() {
  if (typeof fetch !== 'function') {
    throw new Error('当前 Node.js 不支持全局 fetch，请升级到 Node.js 18 或更高版本');
  }

  const args = parseArgs(process.argv.slice(2));

  if (args.help || args.h) {
    printUsage();
    return;
  }

  const historyWindow = Math.max(1, Math.trunc(toNumber(args['history-window']) || DEFAULT_HISTORY_WINDOW));
  const config = loadConfig();
  const modelSelection = resolveModelSelection(args, config, { inputMediaType: 'text', withAudio: false });

  if (toBoolean(args['list-sessions'], false)) {
    printSessionList();
    return;
  }

  if (toBoolean(args['list-voices'], false)) {
    printVoiceList(modelSelection.model);
    return;
  }

  if (args['show-session'] !== undefined) {
    const sessionId = resolveTargetSessionId(args['show-session'], args);
    const session = loadSession(sessionId);
    printSessionDetails(session, historyWindow);
    return;
  }

  if (args['clear-session'] !== undefined) {
    const sessionId = resolveTargetSessionId(args['clear-session'], args);
    const deleted = deleteSession(sessionId);
    console.log(deleted ? `已删除 session: ${sessionId}` : `session 不存在: ${sessionId}`);
    return;
  }

  const prompt = args.prompt;
  if (!prompt) {
    printUsage();
    throw new Error('缺少必填参数 --prompt');
  }

  const dryRun = toBoolean(args['dry-run'], false);

  const images = normalizeList(args.image);
  const videoFrames = normalizeList(args['video-frames']);
  const audio = args.audio;
  const video = args.video;
  const withAudio = toBoolean(args['with-audio'], false);
  const enableThinking = toBoolean(args['enable-thinking'], false);
  const inputMediaType = getMediaType({ images, audio, video, videoFrames });
  const resolvedModelSelection = resolveModelSelection(args, config, { inputMediaType, withAudio });
  const model = resolvedModelSelection.model;
  const baseUrl = String(
    firstNonEmpty(process.env.DASHSCOPE_BASE_URL, config.baseUrl, DEFAULT_BASE_URL)
  ).replace(/\/$/, '');
  const apiKey = firstNonEmpty(process.env.DASHSCOPE_API_KEY, config.apiKey);
  if (!apiKey && !dryRun) {
    throw new Error(`缺少 DASHSCOPE_API_KEY。请设置环境变量，或在 ${CONFIG_PATH} 中配置 apiKey`);
  }
  const voiceSelection = resolveVoiceSelection(args, config, model);
  const voice = voiceSelection.voice;
  const audioOut = args['audio-out'] || `/tmp/qwen-omni-${Date.now()}.wav`;
  const videoFps = toNumber(args['video-fps']) || 2.0;
  const requestedMode = args.mode || 'auto';
  const sessionId = resolveSessionId(args);

  ensureSingleModality({ images, audio, video, videoFrames });

  validateVideoFrames(model, videoFrames);

  if (enableThinking && !supportsThinkingMode(model)) {
    throw new Error(`${model} 不支持思考模式，请关闭 --enable-thinking，或改用 qwen3-omni-flash`);
  }

  if (withAudio && enableThinking) {
    throw new Error('qwen3-omni-flash 开启思考模式时不支持音频输出，请关闭 --enable-thinking 或去掉 --with-audio');
  }

  if (withAudio && voiceSelection.supportedVoices.length > 0 && !voiceSelection.profile) {
    throw new Error(
      `当前模型 ${model} 不支持音色 ${voiceSelection.voice}。可选音色: ${formatSupportedVoiceList(model)}`
    );
  }

  if (resolvedModelSelection.candidates.length > 0 && !resolvedModelSelection.candidates.includes(model)) {
    console.error(
      `model_warning selected=${model} policy=${resolvedModelSelection.selectionPolicy} source=${resolvedModelSelection.source} not_in_modelCandidates=${resolvedModelSelection.candidates.join(',')}`
    );
  } else if (resolvedModelSelection.candidates.length > 0) {
    console.error(
      `model_selection selected=${model} policy=${resolvedModelSelection.selectionPolicy} source=${resolvedModelSelection.source}${resolvedModelSelection.preferredFamily ? ` preferred_family=${resolvedModelSelection.preferredFamily}` : ''} candidates=${resolvedModelSelection.candidates.join(',')}`
    );
  } else {
    console.error(
      `model_selection selected=${model} policy=${resolvedModelSelection.selectionPolicy} source=${resolvedModelSelection.source}${resolvedModelSelection.preferredFamily ? ` preferred_family=${resolvedModelSelection.preferredFamily}` : ''}`
    );
  }

  if (withAudio) {
    if (voiceSelection.profile) {
      console.error(
        `voice_selection selected=${voiceSelection.profile.id} alias=${voiceSelection.profile.alias} source=${voiceSelection.source} model_family=${getOmniModelFamily(model)}`
      );
    } else {
      console.error(`voice_selection selected=${voice} source=${voiceSelection.source} model_family=${getOmniModelFamily(model) || 'unknown'}`);
    }
  }

  printPricingReminder({
    model,
    inputMediaType,
    withAudio
  });

  let session = null;
  let effectiveMode = 'fresh';
  let historyMessages = [];

  if (sessionId) {
    session = loadSession(sessionId);

    if (toBoolean(args['reset-session'], false)) {
      if (dryRun) {
        session = { ...session, turns: session.turns.slice(), context_start_index: session.turns.length };
        console.error(`dry_run: session 将重置但不会落盘: ${session.id}`);
      } else {
        resetActiveContext(session);
        saveSession(session);
        console.error(`session 已重置: ${session.id}`);
      }
    }

    const activeTurns = getActiveTurns(session);
    effectiveMode = resolveMode({
      requestedMode,
      prompt,
      hasMedia: hasMediaInput({ images, audio, video, videoFrames }),
      activeTurns
    });

    if (effectiveMode === 'fresh' && activeTurns.length > 0) {
      if (dryRun) {
        session = { ...session, turns: session.turns.slice(), context_start_index: session.turns.length };
      } else {
        resetActiveContext(session);
      }
    }

    const currentActiveTurns = getActiveTurns(session);
    const recentTurns = sliceTurnsByRecentRounds(currentActiveTurns, historyWindow);
    const olderTurns = currentActiveTurns.slice(
      0,
      Math.max(currentActiveTurns.length - recentTurns.length, 0)
    );

    if (olderTurns.length > 0) {
      historyMessages.push({
        role: 'system',
        content: `以下是当前会话较早内容的摘要，仅作为背景参考；如果与本轮输入冲突，以最新输入为准。\n${summarizeTurns(olderTurns)}`
      });
    }

    historyMessages = historyMessages.concat(recentTurns.map((turn) => turnToMessage(turn, dryRun)));
    console.error(`session=${session.id} mode=${effectiveMode} history_turns=${currentActiveTurns.length}`);
  } else if (requestedMode !== 'auto' && requestedMode !== 'fresh') {
    throw new Error('未指定 --session 时，不能使用 --mode=continue');
  }

  const payload = {
    model,
    messages: [],
    stream: true,
    stream_options: {
      include_usage: true
    }
  };

  if (supportsThinkingMode(model)) {
    payload.enable_thinking = enableThinking;
  }

  if (args.system) {
    payload.messages.push({
      role: 'system',
      content: args.system
    });
  }

  payload.messages.push(...historyMessages);

  payload.messages.push({
    role: 'user',
    content: (dryRun ? buildPreviewContent : buildContent)({
      prompt,
      images,
      audio,
      video,
      videoFrames,
      videoFps
    })
  });

  const temperature = toNumber(args.temperature);
  if (temperature !== undefined) {
    payload.temperature = temperature;
  }

  const maxTokens = toNumber(args['max-tokens']);
  if (maxTokens !== undefined) {
    payload.max_tokens = Math.trunc(maxTokens);
  }

  if (withAudio) {
    payload.modalities = ['text', 'audio'];
    payload.audio = {
      voice,
      format: 'wav'
    };
  }

  if (dryRun) {
    console.log(JSON.stringify(truncatePreviewValue({
      baseUrl,
      payload
    }), null, 2));
    return;
  }

  const result = await streamChatCompletion({
    apiKey,
    baseUrl,
    payload,
    audioOut
  });

  const estimatedCost = estimateOmniCost(result.usage, {
    model,
    inputMediaType,
    withAudio
  });
  if (estimatedCost) {
    const detailText = estimatedCost.components
      .map((component) => `${component.label}=${component.tokens}tok(${formatCny(component.cost)})`)
      .join(' ');
    console.error(`cost_estimate region=中国内地 total=${formatCny(estimatedCost.totalCost)} ${detailText}`);
  } else if (result.usage) {
    console.error('cost_estimate region=中国内地 unavailable=usage 缺少足够的模态 token 明细，仅保留单价提醒');
  }

  if (session) {
    session.turns.push(
      createUserTurn({
        prompt,
        images,
        audio,
        video,
        videoFrames,
        videoFps,
        mode: effectiveMode
      })
    );
    session.turns.push(
      createAssistantTurn({
        text: result.assistantText,
        transcript: result.transcript,
        usage: result.usage,
        audioOut: result.savedAudioPath
      })
    );
    saveSession(session);
    console.error(`session 已保存: ${session.id}`);
  }
}

main().catch((error) => {
  console.error(`错误: ${error.message}`);
  process.exit(1);
});
