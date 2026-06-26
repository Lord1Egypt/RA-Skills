export const DEFAULT_MODEL = 'GEMINI_3_1_PRO';

export const PRESETS = {
  chat: {
    id: 'chat',
    label: 'general assistant chat',
    maxTokens: 1800,
    temperature: 0.7,
    systemPrompt:
      'You are a helpful general-purpose assistant. Answer clearly and directly, follow the user requested language, and preserve multi-turn context from the provided messages. Do not use markdown code fences unless explicitly requested.',
  },
  adCopy: {
    id: 'adCopy',
    label: 'ad copy writing',
    maxTokens: 1400,
    temperature: 0.9,
    systemPrompt:
      'You are an ad copywriter. Write concise, persuasive, audience-aware marketing copy with a clear hook, benefit framing, and call to action. Match the requested language and channel. Do not use markdown code fences unless explicitly requested.',
  },
  email: {
    id: 'email',
    label: 'email writing',
    maxTokens: 1400,
    temperature: 0.65,
    systemPrompt:
      'You are a professional email writer. Draft emails that are clear, purposeful, and appropriate for the relationship and context. Match the requested language and tone. Keep subject lines concise when asked for one. Do not use markdown code fences unless explicitly requested.',
  },
  longform: {
    id: 'longform',
    label: 'long-form writing',
    maxTokens: 2600,
    temperature: 0.8,
    systemPrompt:
      'You are a professional long-form writer. Produce clear, well-structured prose with strong flow, factual restraint, and useful subheadings when appropriate. Keep the output in the user requested language, or preserve the language of the request when no target language is given. Do not use markdown code fences unless explicitly requested.',
  },
  blog: {
    id: 'blog',
    label: 'blog writing',
    maxTokens: 2200,
    temperature: 0.85,
    systemPrompt:
      'You are a blog writer. Write scannable, engaging, practical posts with strong openings, descriptive section headings, and concrete examples. Keep the output in the user requested language, or preserve the language of the request when no target language is given. Do not use markdown code fences unless explicitly requested.',
  },
  social: {
    id: 'social',
    label: 'social post writing',
    maxTokens: 1600,
    temperature: 0.9,
    systemPrompt:
      'You are a social media writer. Produce platform-native copy with a strong hook, clear pacing, and concise lines. When the user asks for X or Twitter, optimize for threads or short posts. When the user asks for Reddit, favor credibility, natural community tone, and readable paragraphs. Keep the output in the user requested language, or preserve the language of the request when no target language is given. Do not use markdown code fences unless explicitly requested.',
  },
  summary: {
    id: 'summary',
    label: 'summary writing',
    maxTokens: 1200,
    temperature: 0.45,
    systemPrompt:
      'You are a summarization assistant. Produce accurate, compressed summaries that preserve the key meaning, decisions, claims, and action items. Match the requested language and output shape. Do not use markdown code fences unless explicitly requested.',
  },
  translation: {
    id: 'translation',
    label: 'copy translation',
    maxTokens: 1400,
    temperature: 0.35,
    systemPrompt:
      'You are a translation and localization specialist. Translate copy accurately while preserving intent, tone, and audience fit. When the user asks for localization, adapt phrasing naturally instead of translating word-for-word. Do not use markdown code fences unless explicitly requested.',
  },
  rewrite: {
    id: 'rewrite',
    label: 'rewrite and polishing',
    maxTokens: 1500,
    temperature: 0.6,
    systemPrompt:
      'You are a rewriting and editing assistant. Improve clarity, tone, flow, and readability while preserving the original meaning unless the user explicitly asks for a stronger rewrite. Do not use markdown code fences unless explicitly requested.',
  },
};

export function normalizeInput(input) {
  return {
    prompt: pickString(input.prompt, input.instruction, input.brief, input.request, input.topic),
    sourceText: pickString(input.sourceText, input.source, input.text, input.material),
    audience: pickString(input.audience, input.reader, input.targetAudience),
    tone: pickString(input.tone, input.voice, input.style),
    language: pickString(input.language, input.lang),
    format: pickString(input.format, input.platform, input.postType),
    length: pickString(input.length, input.wordCount, input.size),
    title: pickString(input.title, input.headline),
    sourceLanguage: pickString(input.sourceLanguage, input.sourceLang, input.fromLanguage, input.fromLang),
    targetLanguage: pickString(input.targetLanguage, input.targetLang, input.toLanguage, input.toLang),
    subject: pickString(input.subject, input.emailSubject),
    recipient: pickString(input.recipient, input.to, input.receiver),
    sender: pickString(input.sender, input.from, input.senderRole),
    purpose: pickString(input.purpose, input.goal, input.objective),
    product: pickString(input.product, input.productName, input.offer),
    brand: pickString(input.brand, input.brandName),
    cta: pickString(input.cta, input.callToAction),
    keywords: normalizeList(input.keywords ?? input.keyword ?? input.tags),
    mustInclude: normalizeList(input.mustInclude ?? input.must_include ?? input.include),
    avoid: normalizeList(input.avoid ?? input.doNotInclude ?? input.do_not_include),
    messages: Array.isArray(input.messages) ? input.messages : null,
    model: pickString(input.model),
    maxTokens: toNumber(input.maxTokens ?? input.max_tokens),
    temperature: toNumber(input.temperature),
    topP: toNumber(input.topP ?? input.top_p),
  };
}

export function validateInput(input) {
  const errors = [];

  if (!input.prompt && (!Array.isArray(input.messages) || input.messages.length === 0)) {
    errors.push('Provide `prompt` (or `instruction` / `brief`) or a non-empty `messages` array.');
  }

  if (input.messages && input.messages.some((item) => !item || !item.role || typeof item.content !== 'string')) {
    errors.push('Each item in `messages` must include `role` and string `content`.');
  }

  if (input.maxTokens != null && (!Number.isFinite(input.maxTokens) || input.maxTokens < 1)) {
    errors.push('`maxTokens` must be a positive number.');
  }

  if (input.temperature != null && (!Number.isFinite(input.temperature) || input.temperature < 0 || input.temperature > 2)) {
    errors.push('`temperature` must be between 0 and 2.');
  }

  if (input.topP != null && (!Number.isFinite(input.topP) || input.topP < 0 || input.topP > 1)) {
    errors.push('`topP` must be between 0 and 1.');
  }

  return errors;
}

export function buildMessages(input, preset) {
  if (input.messages) {
    return hasSystemMessage(input.messages)
      ? input.messages
      : [{ role: 'system', content: preset.systemPrompt }, ...input.messages];
  }

  return [
    { role: 'system', content: preset.systemPrompt },
    { role: 'user', content: buildUserPrompt(input, preset) },
  ];
}

function buildUserPrompt(input, preset) {
  const sections = [
    `Task type: ${preset.label}`,
    `Core request: ${input.prompt}`,
  ];

  if (input.format) sections.push(`Target format or platform: ${input.format}`);
  if (input.audience) sections.push(`Audience: ${input.audience}`);
  if (input.tone) sections.push(`Tone: ${input.tone}`);
  if (input.language) sections.push(`Target language: ${input.language}`);
  if (input.length) sections.push(`Target length: ${input.length}`);
  if (input.title) sections.push(`Preferred title or angle: ${input.title}`);
  if (input.sourceLanguage) sections.push(`Source language: ${input.sourceLanguage}`);
  if (input.targetLanguage) sections.push(`Target language for translation or rewrite: ${input.targetLanguage}`);
  if (input.subject) sections.push(`Preferred subject line: ${input.subject}`);
  if (input.recipient) sections.push(`Recipient: ${input.recipient}`);
  if (input.sender) sections.push(`Sender or sender role: ${input.sender}`);
  if (input.purpose) sections.push(`Purpose: ${input.purpose}`);
  if (input.product) sections.push(`Product or offer: ${input.product}`);
  if (input.brand) sections.push(`Brand: ${input.brand}`);
  if (input.cta) sections.push(`Call to action: ${input.cta}`);
  if (input.keywords?.length) sections.push(`Keywords to cover: ${input.keywords.join(', ')}`);
  if (input.mustInclude?.length) sections.push(`Must include: ${input.mustInclude.join(', ')}`);
  if (input.avoid?.length) sections.push(`Avoid: ${input.avoid.join(', ')}`);
  if (input.sourceText) sections.push(`Source material:\n${input.sourceText}`);

  sections.push(
    'Write the final deliverable directly. Do not explain your reasoning unless the user explicitly asks for notes or alternatives.'
  );

  return sections.join('\n\n');
}

function hasSystemMessage(messages) {
  return messages.some((message) => message?.role === 'system');
}

function pickString(...values) {
  for (const value of values) {
    if (typeof value === 'string' && value.trim()) return value.trim();
  }
  return null;
}

function normalizeList(value) {
  if (Array.isArray(value)) {
    return value.map((item) => (typeof item === 'string' ? item.trim() : '')).filter(Boolean);
  }
  if (typeof value === 'string' && value.trim()) {
    return value
      .split(',')
      .map((item) => item.trim())
      .filter(Boolean);
  }
  return null;
}

function toNumber(value) {
  if (value == null || value === '') return null;
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : NaN;
}
