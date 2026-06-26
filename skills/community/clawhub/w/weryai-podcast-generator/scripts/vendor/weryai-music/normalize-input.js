export function normalizeMusicInput(rawInput) {
  const input = { ...rawInput };
  const rawType = input.type ?? input.mode ?? input.musicType ?? input.songType;

  if (rawType) {
    input.type = normalizeType(rawType);
  } else {
    input.type = hasInstrumentalSignals(input) ? 'ONLY_MUSIC' : 'VOCAL_SONG';
  }

  mergeCategorizedStyles(input);
  normalizeTimbre(input);

  if (input.type === 'VOCAL_SONG' && !input.gender) {
    input.gender = 'm';
  }

  return input;
}

const STYLE_VALUE_MAP = {
  POP: 'pop',
  ROCK: 'rock',
  RAP: 'rap',
  ELECTRONIC: 'electronic',
  RNB: 'r&b',
  JAZZ: 'jazz',
  FOLK: 'folk',
  CLASSIC: 'classical',
  WORLD: 'world music',
  HAPPY: 'happy',
  RELAXED: 'relaxed',
  WARM: 'warm',
  ROMANTIC: 'romantic',
  TOUCHING: 'touching',
  SAD: 'sad',
  LONELY: 'lonely',
  DEPRESSED: 'depressed',
  TENSE: 'tense',
  EXCITED: 'excited',
  EPIC: 'epic',
  MYSTERIOUS: 'mysterious',
  PIANO: 'piano',
  GUITAR: 'guitar',
  BASS: 'bass',
  DRUMS: 'drums',
  STRINGS: 'strings',
  WIND: 'wind instruments',
  SYNTHESIZER: 'synthesizer',
  ELECTRONIC_SOUND: 'electronic sound',
  FOLK_INSTRUMENT: 'folk instrument',
  MIXED_ORCHESTRATION: 'mixed orchestration',
};

const GENRE_MAP = {
  POP: 'POP',
  流行: 'POP',
  ROCK: 'ROCK',
  摇滚: 'ROCK',
  RAP: 'RAP',
  说唱: 'RAP',
  ELECTRONIC: 'ELECTRONIC',
  电子: 'ELECTRONIC',
  RNB: 'RNB',
  'R&B': 'RNB',
  JAZZ: 'JAZZ',
  爵士: 'JAZZ',
  FOLK: 'FOLK',
  民谣: 'FOLK',
  CLASSIC: 'CLASSIC',
  古典: 'CLASSIC',
  WORLD: 'WORLD',
  世界音乐: 'WORLD',
};

const EMOTION_MAP = {
  HAPPY: 'HAPPY',
  开心: 'HAPPY',
  RELAXED: 'RELAXED',
  轻松: 'RELAXED',
  WARM: 'WARM',
  温暖: 'WARM',
  ROMANTIC: 'ROMANTIC',
  浪漫: 'ROMANTIC',
  TOUCHING: 'TOUCHING',
  感动: 'TOUCHING',
  SAD: 'SAD',
  忧伤: 'SAD',
  LONELY: 'LONELY',
  孤独: 'LONELY',
  DEPRESSED: 'DEPRESSED',
  压抑: 'DEPRESSED',
  TENSE: 'TENSE',
  紧张: 'TENSE',
  EXCITED: 'EXCITED',
  激昂: 'EXCITED',
  EPIC: 'EPIC',
  史诗: 'EPIC',
  MYSTERIOUS: 'MYSTERIOUS',
  神秘: 'MYSTERIOUS',
};

const INSTRUMENT_MAP = {
  PIANO: 'PIANO',
  钢琴: 'PIANO',
  GUITAR: 'GUITAR',
  吉他: 'GUITAR',
  BASS: 'BASS',
  贝斯: 'BASS',
  DRUMS: 'DRUMS',
  架子鼓: 'DRUMS',
  STRINGS: 'STRINGS',
  弦乐: 'STRINGS',
  WIND: 'WIND',
  管乐: 'WIND',
  SYNTHESIZER: 'SYNTHESIZER',
  合成器: 'SYNTHESIZER',
  ELECTRONIC_SOUND: 'ELECTRONIC_SOUND',
  电子音色: 'ELECTRONIC_SOUND',
  FOLK_INSTRUMENT: 'FOLK_INSTRUMENT',
  民族乐器: 'FOLK_INSTRUMENT',
  MIXED_ORCHESTRATION: 'MIXED_ORCHESTRATION',
  混合编制: 'MIXED_ORCHESTRATION',
};

const TIMBRE_MAP = {
  m: 'm',
  male: 'm',
  男: 'm',
  男声: 'm',
  f: 'f',
  female: 'f',
  女: 'f',
  女声: 'f',
};

function normalizeType(value) {
  const normalized = String(value).trim().toUpperCase();

  if (
    normalized === 'VOCAL_SONG' ||
    normalized === 'VOCAL' ||
    normalized === 'SONG' ||
    normalized === '人声歌曲' ||
    normalized === '人声'
  ) {
    return 'VOCAL_SONG';
  }

  if (
    normalized === 'ONLY_MUSIC' ||
    normalized === 'MUSIC_ONLY' ||
    normalized === 'INSTRUMENTAL' ||
    normalized === 'BGM' ||
    normalized === '纯音乐'
  ) {
    return 'ONLY_MUSIC';
  }

  return normalized;
}

function hasInstrumentalSignals(input) {
  const textSignals = [input.mode, input.musicType, input.songType, input.description, input.prompt]
    .filter(Boolean)
    .join(' ')
    .toLowerCase();

  return (
    textSignals.includes('instrumental') ||
    textSignals.includes('background music') ||
    textSignals.includes('soundtrack') ||
    textSignals.includes('bgm') ||
    textSignals.includes('纯音乐') ||
    textSignals.includes('伴奏')
  );
}

function mergeCategorizedStyles(input) {
  const merged = { ...(isPlainObject(input.styles) ? input.styles : {}) };

  addStyleEntries(merged, input.genre ?? input.genres ?? input.styleGenre, GENRE_MAP);
  addStyleEntries(merged, input.emotion ?? input.emotions ?? input.mood, EMOTION_MAP);
  addStyleEntries(merged, input.instrument ?? input.instruments, INSTRUMENT_MAP);

  if (Object.keys(merged).length > 0) {
    input.styles = merged;
  }
}

function addStyleEntries(target, rawValue, dictionary) {
  for (const value of normalizeList(rawValue)) {
    const key = dictionary[String(value).trim()];
    if (key && !target[key]) {
      target[key] = STYLE_VALUE_MAP[key];
    }
  }
}

function normalizeTimbre(input) {
  const raw = input.timbre ?? input.voice ?? input.voiceTone ?? input.gender;
  if (raw == null) return;

  const resolved = TIMBRE_MAP[String(raw).trim().toLowerCase()] ?? TIMBRE_MAP[String(raw).trim()];
  if (resolved) {
    input.gender = resolved;
  }
}

function normalizeList(value) {
  if (Array.isArray(value)) return value;
  if (typeof value === 'string' && value.trim()) {
    return value.split(/[,，/|]/).map((item) => item.trim()).filter(Boolean);
  }
  return [];
}

function isPlainObject(value) {
  return Boolean(value) && typeof value === 'object' && !Array.isArray(value);
}
