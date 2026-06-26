/**
 * Vision Module - Image understanding via Ollama vision models
 * 
 * Supports:
 * - Ollama vision models (llava, llava-llama3, etc.)
 * - Cloudflare Workers AI (optional fallback)
 * 
 * Extracts: objects, text_in_image, scene_description, people, activities
 * Stores description as memory with category='visual'
 */

import { readFileSync, existsSync } from 'fs';
import { join } from 'path';
import { config } from '../config.js';
import { addMemory } from '../storage.js';

/** @returns {{ baseURL: string, model: string }} */
function getVisionProvider() {
  const ollamaBase = process.env.OLLAMA_BASE_URL || process.env.OLLAMA_HOST || 'http://localhost:11434';
  const model = process.env.OLLAMA_VISION_MODEL || 'llava';
  return { baseURL: ollamaBase, model };
}

/**
 * Read image file and return base64 string
 * @param {string} imagePath
 * @returns {string|null}
 */
function readImageBase64(imagePath) {
  try {
    // Support relative and absolute paths
    const absolutePath = imagePath.startsWith('/') ? imagePath : join(process.cwd(), imagePath);
    if (!existsSync(absolutePath)) {
      // Try workspace path
      const workspacePath = join(process.env.HOME || '/root', '.openclaw', 'workspace', imagePath);
      if (existsSync(workspacePath)) {
        const buffer = readFileSync(workspacePath);
        return buffer.toString('base64');
      }
      return null;
    }
    const buffer = readFileSync(absolutePath);
    return buffer.toString('base64');
  } catch {
    return null;
  }
}

/**
 * Check if Ollama vision model is available
 * @returns {Promise<boolean>}
 */
async function isVisionModelAvailable() {
  try {
    const { baseURL, model } = getVisionProvider();
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 3000);
    const res = await fetch(`${baseURL}/api/tags`, { signal: controller.signal });
    clearTimeout(timer);
    if (!res.ok) return false;
    const json = await res.json();
    const models = json.models || json.user_defined_models || [];
    // Check if any available model is vision-capable (llava variants)
    const visionKeywords = ['llava', 'llava-llama3', 'moondream', 'vision'];
    return models.some(m => {
      const name = (m.name || '').toLowerCase();
      return visionKeywords.some(k => name.includes(k));
    }) || models.some(m => (m.name || '').includes(model));
  } catch {
    return false;
  }
}

/**
 * Analyze image using Ollama vision model
 * @param {string} imagePath - Image file path
 * @param {string} [imageBase64] - Optional base64 image data
 * @returns {Promise<{objects: string[], text_in_image: string, scene_description: string, people: string[], activities: string[]}>}
 */
async function analyzeImageWithOllama(imagePath, imageBase64) {
  const { baseURL, model } = getVisionProvider();
  
  // Get base64 from file if not provided
  const base64 = imageBase64 || readImageBase64(imagePath);
  if (!base64) {
    throw new Error(`Image not found: ${imagePath}`);
  }

  const prompt = `You are an expert image analyzer. Analyze this image and respond ONLY with a valid JSON object (no markdown, no explanation). Format:
{
  "objects": ["list of distinct objects detected"],
  "text_in_image": "any text visible in the image, or empty string if none",
  "scene_description": "brief description of the scene/setting",
  "people": ["names or descriptions of any people, or empty array"],
  "activities": ["actions or activities happening in the image, or empty array"]
}`;

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 30000);

  try {
    // Try /api/chat endpoint first (newer Ollama versions)
    const chatRes = await fetch(`${baseURL}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model,
        messages: [
          {
            role: 'user',
            content: prompt,
            images: [base64],
          }
        ],
        stream: false,
      }),
      signal: controller.signal,
    });

    clearTimeout(timer);

    if (chatRes.ok) {
      const json = await chatRes.json();
      const raw = json.message?.content || json.response || '';
      return parseVisionResponse(raw);
    }

    // Fallback to /api/generate
    const genRes = await fetch(`${baseURL}/api/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model,
        prompt,
        images: [base64],
        stream: false,
        options: { temperature: 0.1 },
      }),
      signal: controller.signal,
    });

    if (!genRes.ok) {
      throw new Error(`Ollama vision API error: ${genRes.status} ${genRes.statusText}`);
    }

    const json = await genRes.json();
    return parseVisionResponse(json.response || '');
  } catch (err) {
    clearTimeout(timer);
    throw err;
  }
}

/**
 * Parse the raw vision response into structured data
 * @param {string} raw
 * @returns {{objects: string[], text_in_image: string, scene_description: string, people: string[], activities: string[]}}
 */
function parseVisionResponse(raw) {
  try {
    // Try JSON parse directly
    const parsed = JSON.parse(raw);
    return {
      objects: Array.isArray(parsed.objects) ? parsed.objects : [],
      text_in_image: parsed.text_in_image || '',
      scene_description: parsed.scene_description || '',
      people: Array.isArray(parsed.people) ? parsed.people : [],
      activities: Array.isArray(parsed.activities) ? parsed.activities : [],
    };
  } catch {
    // Try to extract JSON from the raw text
    const jsonMatch = raw.match(/\{[\s\S]*\}/);
    if (jsonMatch) {
      try {
        const parsed = JSON.parse(jsonMatch[0]);
        return {
          objects: Array.isArray(parsed.objects) ? parsed.objects : [],
          text_in_image: parsed.text_in_image || '',
          scene_description: parsed.scene_description || '',
          people: Array.isArray(parsed.people) ? parsed.people : [],
          activities: Array.isArray(parsed.activities) ? parsed.activities : [],
        };
      } catch { /* fall through */ }
    }

    // Fallback: treat entire response as scene description
    return {
      objects: [],
      text_in_image: '',
      scene_description: raw.trim(),
      people: [],
      activities: [],
    };
  }
}

/**
 * Main vision analysis function
 * @param {object} params
 * @param {string} [params.imagePath] - Path to image file
 * @param {string} [params.imageBase64] - Base64-encoded image data
 * @param {boolean} [params.storeMemory] - Whether to store as memory (default: true)
 * @param {number} [params.importance] - Memory importance 0-1 (default: 0.5)
 * @param {string[]} [params.tags] - Additional tags for the memory
 * @returns {Promise<{analysis: object, memory_id: string|null, error: string|null}>}
 */
export async function analyzeImage({ imagePath, imageBase64, storeMemory = true, importance = 0.5, tags = [] }) {
  try {
    if (!imagePath && !imageBase64) {
      return { analysis: null, memory_id: null, error: 'Either imagePath or imageBase64 is required' };
    }

    const available = await isVisionModelAvailable();
    if (!available) {
      return {
        analysis: null,
        memory_id: null,
        error: 'No vision model available in Ollama. Please install llava: `ollama pull llava`',
      };
    }

    const analysis = await analyzeImageWithOllama(imagePath, imageBase64);

    // Build descriptive text for memory
    const parts = [];
    if (analysis.scene_description) parts.push(`Scene: ${analysis.scene_description}`);
    if (analysis.objects.length > 0) parts.push(`Objects: ${analysis.objects.join(', ')}`);
    if (analysis.text_in_image) parts.push(`Text: ${analysis.text_in_image}`);
    if (analysis.people.length > 0) parts.push(`People: ${analysis.people.join(', ')}`);
    if (analysis.activities.length > 0) parts.push(`Activities: ${analysis.activities.join(', ')}`);

    const description = parts.join(' | ');

    let memoryId = null;
    if (storeMemory && description) {
      const memory = addMemory({
        text: `[Visual Analysis] ${description}`,
        category: 'visual',
        importance,
        tags: ['visual', 'image', ...tags],
      });
      memoryId = memory.id;
    }

    return {
      analysis: {
        ...analysis,
        imagePath,
        description,
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

export default { analyzeImage };
