/**
 * Audio Module - Audio transcription via Ollama Whisper
 * 
 * Supports:
 * - Ollama Whisper model for transcription
 * - File-based transcription (mp3, wav, m4a, ogg, webm, mp4)
 * 
 * Extracts: transcription, key_topics, speakers (if detectable)
 * Stores transcription as memory with category='audio'
 */

import { readFileSync, existsSync } from 'fs';
import { join } from 'path';
import { config } from '../config.js';
import { addMemory } from '../storage.js';

/** @returns {{ baseURL: string, model: string }} */
function getWhisperProvider() {
  const ollamaBase = process.env.OLLAMA_BASE_URL || process.env.OLLAMA_HOST || 'http://localhost:11434';
  const model = process.env.OLLAMA_WHISPER_MODEL || 'whisper';
  return { baseURL: ollamaBase, model };
}

/**
 * Read audio file and return base64
 * @param {string} filePath
 * @returns {Buffer|null}
 */
function readAudioFile(filePath) {
  try {
    const absolutePath = filePath.startsWith('/') ? filePath : join(process.cwd(), filePath);
    if (!existsSync(absolutePath)) {
      // Try workspace path
      const workspacePath = join(process.env.HOME || '/root', '.openclaw', 'workspace', filePath);
      if (existsSync(workspacePath)) {
        return readFileSync(workspacePath);
      }
      return null;
    }
    return readFileSync(absolutePath);
  } catch {
    return null;
  }
}

/**
 * Supported audio extensions
 */
const AUDIO_EXTS = new Set(['.mp3', '.wav', '.m4a', '.ogg', '.webm', '.mp4', '.aac', '.flac', '.opus']);

/**
 * Detect MIME type from extension
 * @param {string} filename
 * @returns {string}
 */
function getMimeType(filename) {
  const ext = (filename || '').toLowerCase().replace(/^.*\./, '');
  const mimeMap = {
    mp3: 'audio/mpeg',
    wav: 'audio/wav',
    m4a: 'audio/mp4',
    ogg: 'audio/ogg',
    webm: 'audio/webm',
    mp4: 'audio/mp4',
    aac: 'audio/aac',
    flac: 'audio/flac',
    opus: 'audio/opus',
  };
  return mimeMap[ext] || 'audio/mpeg';
}

/**
 * Check if Ollama Whisper model is available
 * @returns {Promise<boolean>}
 */
async function isWhisperAvailable() {
  try {
    const { baseURL } = getWhisperProvider();
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 3000);
    const res = await fetch(`${baseURL}/api/tags`, { signal: controller.signal });
    clearTimeout(timer);
    if (!res.ok) return false;
    const json = await res.json();
    const models = json.models || [];
    const whisperKeywords = ['whisper'];
    return models.some(m => whisperKeywords.some(k => (m.name || '').toLowerCase().includes(k)));
  } catch {
    return false;
  }
}

/**
 * Transcribe audio using Ollama Whisper
 * @param {string} audioPath - Path to audio file
 * @returns {Promise<{transcription: string, language: string|null}>}
 */
async function transcribeWithWhisper(audioPath) {
  const { baseURL, model } = getWhisperProvider();
  
  const buffer = readAudioFile(audioPath);
  if (!buffer) {
    throw new Error(`Audio file not found: ${audioPath}`);
  }

  const mimeType = getMimeType(audioPath);

  // Ollama Whisper uses multipart form data
  const formData = new FormData();
  const blob = new Blob([buffer], { type: mimeType });
  const filename = audioPath.split('/').pop() || 'audio.mp3';
  formData.append('file', blob, filename);
  formData.append('model', model);
  formData.append('language', 'auto');

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 120000); // 2min timeout for audio

  try {
    const res = await fetch(`${baseURL}/api/whisper`, {
      method: 'POST',
      body: formData,
      signal: controller.signal,
    });

    clearTimeout(timer);

    if (!res.ok) {
      throw new Error(`Whisper API error: ${res.status} ${res.statusText}`);
    }

    const json = await res.json();
    return {
      transcription: json.text || '',
      language: json.language || null,
    };
  } catch (err) {
    clearTimeout(timer);
    throw err;
  }
}

/**
 * Extract key topics from transcription using Ollama LLM
 * @param {string} transcription
 * @returns {Promise<string[]>}
 */
async function extractKeyTopics(transcription) {
  if (!transcription || transcription.length < 20) return [];

  const { baseURL: llmBase, model: llmModel } = (() => {
    const providers = config.llmProviders || [];
    const ollama = providers.find(p => p.name === 'ollama') || {
      baseURL: process.env.OLLAMA_BASE_URL || 'http://localhost:11434',
      model: process.env.OLLAMA_LLM_MODEL || 'qwen2.5:7b',
    };
    return ollama;
  })();

  const prompt = `Extract 3-5 key topics from this transcription. Reply ONLY with a JSON array of strings, nothing else. Example: ["topic1", "topic2"]\n\nTranscription:\n${transcription.slice(0, 2000)}`;

  try {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 15000);
    const res = await fetch(`${llmBase}/api/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model: llmModel, prompt, stream: false, options: { num_predict: 80 } }),
      signal: controller.signal,
    });
    clearTimeout(timer);
    if (!res.ok) return [];
    const json = await res.json();
    const raw = json.response || '';
    const match = raw.match(/\[[\s\S]*?\]/);
    if (match) {
      return JSON.parse(match[0]);
    }
    return [];
  } catch {
    return [];
  }
}

/**
 * Attempt to detect speakers from transcription
 * Uses patterns like "Person A:", "Speaker 1:", "[John]:", etc.
 * @param {string} transcription
 * @returns {string[]}
 */
function detectSpeakers(transcription) {
  const patterns = [
    /^(.{1,20}):/m,           // "Name:" at start of line
    /^\[(.{1,20})\]:/m,        // "[Name]:" at start of line
    /^Speaker\s*(\d+)/im,      // Speaker 1, Speaker 2
    /^Person\s*([A-Z])/im,     // Person A, Person B
  ];

  /** @type {Set<string>} */
  const speakers = new Set();

  for (const pattern of patterns) {
    const matches = transcription.matchAll(new RegExp(pattern, 'gim'));
    for (const match of matches) {
      const name = (match[1] || match[0]).trim().replace(/[:\]]+$/, '');
      if (name && name.length < 30 && !/^\d+$/.test(name)) {
        speakers.add(name);
      }
    }
    if (speakers.size > 0) break;
  }

  return Array.from(speakers).slice(0, 10);
}

/**
 * Main audio analysis function
 * @param {object} params
 * @param {string} params.filePath - Path to audio file
 * @param {boolean} [params.storeMemory] - Whether to store as memory (default: true)
 * @param {number} [params.importance] - Memory importance 0-1 (default: 0.5)
 * @param {string[]} [params.tags] - Additional tags for the memory
 * @returns {Promise<{analysis: object|null, memory_id: string|null, error: string|null}>}
 */
export async function analyzeAudio({ filePath, storeMemory = true, importance = 0.5, tags = [] }) {
  try {
    if (!filePath) {
      return { analysis: null, memory_id: null, error: 'filePath is required' };
    }

    // Check file extension
    const ext = ('.' + filePath.split('.').pop()?.toLowerCase() || '').replace(/^.*(\.[^.]+)$/, '$1');
    if (!AUDIO_EXTS.has(ext)) {
      return {
        analysis: null,
        memory_id: null,
        error: `Unsupported audio format: ${ext}. Supported: ${[...AUDIO_EXTS].join(', ')}`,
      };
    }

    const available = await isWhisperAvailable();
    if (!available) {
      return {
        analysis: null,
        memory_id: null,
        error: 'Whisper model not available in Ollama. Please install: `ollama pull whisper`',
      };
    }

    const { transcription, language } = await transcribeWithWhisper(filePath);

    if (!transcription) {
      return { analysis: null, memory_id: null, error: 'No transcription returned' };
    }

    const speakers = detectSpeakers(transcription);
    const keyTopics = await extractKeyTopics(transcription);

    let memoryId = null;
    if (storeMemory && transcription) {
      const summary = `[Audio Transcription] ${transcription.slice(0, 300)}${transcription.length > 300 ? '...' : ''}`;
      const memory = addMemory({
        text: summary,
        category: 'audio',
        importance,
        tags: ['audio', 'transcription', language || '', ...tags],
      });
      memoryId = memory.id;
    }

    return {
      analysis: {
        transcription,
        language,
        speakers,
        key_topics: keyTopics,
        filePath,
        duration: null, // Could add with ffprobe if needed
        stored: storeMemory,
      },
      memory_id: memoryId,
      error: null,
    };
  } catch (err) {
    return {
      analysis: null,
      memory_id: null,
      error: err.message || String(err),
    };
  }
}

/**
 * Analyze a generic file - detect type and extract text content
 * For text-based files, extracts readable content
 * For other files, stores metadata only
 * @param {object} params
 * @param {string} params.filePath - Path to file
 * @param {boolean} [params.storeMemory] - Whether to store as memory
 * @param {number} [params.importance] - Memory importance 0-1
 * @param {string[]} [params.tags] - Additional tags
 * @returns {Promise<{analysis: object|null, memory_id: string|null, error: string|null}>}
 */
export async function analyzeFile({ filePath, storeMemory = true, importance = 0.5, tags = [] }) {
  try {
    if (!filePath) {
      return { analysis: null, memory_id: null, error: 'filePath is required' };
    }

    const absolutePath = filePath.startsWith('/') ? filePath : join(process.cwd(), filePath);
    const actualPath = existsSync(absolutePath)
      ? absolutePath
      : join(process.env.HOME || '/root', '.openclaw', 'workspace', filePath);

    if (!existsSync(actualPath)) {
      return { analysis: null, memory_id: null, error: `File not found: ${filePath}` };
    }

    const ext = ('.' + filePath.split('.').pop()?.toLowerCase() || '').replace(/^.*(\.[^.]+)$/, '$1');

    // Audio files: delegate to analyzeAudio
    if (AUDIO_EXTS.has(ext)) {
      return analyzeAudio({ filePath: actualPath, storeMemory, importance, tags });
    }

    // Image files: delegate to analyzeImage
    const IMAGE_EXTS = new Set(['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']);
    if (IMAGE_EXTS.has(ext)) {
      const { analyzeImage } = await import('./vision.js');
      return analyzeImage({ imagePath: actualPath, storeMemory, importance, tags });
    }

    // Text-based files: extract content
    const TEXT_EXTS = new Set(['.txt', '.md', '.json', '.xml', '.csv', '.log', '.html', '.css', '.js', '.ts', '.py', '.java', '.c', '.cpp', '.h', '.sh', '.yaml', '.yml', '.toml', '.ini', '.conf']);
    if (TEXT_EXTS.has(ext)) {
      try {
        const content = readFileSync(actualPath, 'utf-8').slice(0, 5000);
        if (storeMemory) {
          const summary = `[File Content] ${filePath}\n\n${content.slice(0, 500)}${content.length > 500 ? '...' : ''}`;
          const memory = addMemory({
            text: summary,
            category: 'document',
            importance,
            tags: ['document', 'file', ext.replace('.', ''), ...tags],
          });
          return {
            analysis: { filePath, ext, content_length: content.length, content_preview: content.slice(0, 200) },
            memory_id: memory.id,
            error: null,
          };
        }
      } catch {
        return { analysis: null, memory_id: null, error: `Could not read file: ${filePath}` };
      }
    }

    // Binary files: just store metadata
    const memory = addMemory({
      text: `[File Metadata] ${filePath} (${ext}, binary file)`,
      category: 'document',
      importance,
      tags: ['file', 'metadata', ext.replace('.', ''), ...tags],
    });

    return {
      analysis: { filePath, ext, type: 'binary', note: 'Binary file, content not extracted' },
      memory_id: memory.id,
      error: null,
    };
  } catch (err) {
    return { analysis: null, memory_id: null, error: err.message || String(err) };
  }
}

export default { analyzeAudio, analyzeFile };
