/**
 * VOICE NOTES PRO - OpenClaw Skill
 * Inteligentna transkrypcja i kategoryzacja notatek g≥osowych
 */

const fs = require('fs').promises;
const path = require('path');
const { OpenAI } = require('openai');

// ================================================================================
// KONFIGURACJA
// ================================================================================

const CONFIG = {
  whisper: {
    model: 'whisper-1',
    language: 'pl',
  },
  directories: {
    songs: '/root/notes/songs',
    tasks: '/root/notes/tasks',
    shopping: '/root/notes/lists',
    ideas: '/root/notes/ideas',
    people: '/root/notes/people',
    watchlist: '/root/notes/watchlist',
  },
  keywords: {
    songs: ['dyktuj', 'tekst utworu', 'piosenka', 'rap', 'zwrotka', 'refren'],
    tasks: ['zadanie', 'todo', 'zrÛb', 'zadzwoÒ', 'napisz', 'wyúlij'],
    shopping: ['zakupy', 'kup', 'kupiÊ', 'do sklepu', 'lista zakupÛw'],
    ideas: ['pomys≥', 'idea', 'projekt', 'fajnie by by≥o', 'moøe warto'],
    people: ['dodaj osobÍ', 'osoba', 'kontakt', 'sprawdü osobÍ'],
    watchlist: ['zapisz film', 'serial', 'obejrzeÊ', 'watchlist', 'do obejrzenia'],
  },
};

// ================================================================================
// WHISPER CLIENT
// ================================================================================

let openaiClient = null;

function getOpenAIClient() {
  if (!openaiClient) {
    const apiKey = process.env.OPENAI_API_KEY;
    if (!apiKey) {
      throw new Error('OPENAI_API_KEY not found in environment variables');
    }
    openaiClient = new OpenAI({ apiKey });
  }
  return openaiClient;
}

// ================================================================================
// TRANSKRYPCJA
// ================================================================================

async function transcribeAudio(audioPath) {
  try {
    const client = getOpenAIClient();
    const audioFile = await fs.readFile(audioPath);
    
    const response = await client.audio.transcriptions.create({
      file: audioFile,
      model: CONFIG.whisper.model,
      language: CONFIG.whisper.language,
    });

    return response.text;
  } catch (error) {
    console.error('Whisper transcription failed:', error);
    throw new Error(`Transkrypcja nie powiod≥a siÍ: ${error.message}`);
  }
}

// ================================================================================
// KATEGORYZACJA
// ================================================================================

function detectCategory(text) {
  const lowerText = text.toLowerCase();
  
  for (const [category, keywords] of Object.entries(CONFIG.keywords)) {
    if (keywords.some(keyword => lowerText.includes(keyword))) {
      return category;
    }
  }
  
  return 'ideas'; // Domyúlna kategoria
}

// ================================================================================
// POMOCNICZE FUNKCJE
// ================================================================================

function getTimestamp() {
  const now = new Date();
  return now.toLocaleString('pl-PL', { 
    timeZone: 'Europe/Warsaw',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  });
}

function getDateStamp() {
  const now = new Date();
  return now.toISOString().split('T')[0]; // YYYY-MM-DD
}

async function ensureDirectoryExists(dirPath) {
  try {
    await fs.mkdir(dirPath, { recursive: true });
  } catch (error) {
    console.error(`Failed to create directory ${dirPath}:`, error);
  }
}

async function appendToFile(filePath, content) {
  try {
    await fs.appendFile(filePath, content, 'utf8');
  } catch (error) {
    console.error(`Failed to append to file ${filePath}:`, error);
    throw error;
  }
}

async function readFile(filePath) {
  try {
    return await fs.readFile(filePath, 'utf8');
  } catch (error) {
    if (error.code === 'ENOENT') {
      return ''; // Plik nie istnieje
    }
    throw error;
  }
}

// ================================================================================
// KATEGORIE - HANDLERS
// ================================================================================

async function handleSongs(text) {
  const filePath = path.join(CONFIG.directories.songs, 'brudnopis.md');
  await ensureDirectoryExists(CONFIG.directories.songs);
  
  const content = `\n\n---\n**${getTimestamp()}**\n\n${text}\n`;
  await appendToFile(filePath, content);
  
  return `?? Zapisano tekst w ~/notes/songs/brudnopis.md`;
}

async function handleTasks(text) {
  const filePath = path.join(CONFIG.directories.tasks, 'inbox.md');
  await ensureDirectoryExists(CONFIG.directories.tasks);
  
  const content = `- [ ] ${text} *(dodano: ${getTimestamp()})*\n`;
  await appendToFile(filePath, content);
  
  return `? Dodano zadanie: ${text}`;
}

async function handleShopping(text) {
  const filePath = path.join(CONFIG.directories.shopping, 'shopping.md');
  await ensureDirectoryExists(CONFIG.directories.shopping);
  
  // Rozdziel produkty po przecinkach lub "i"
  const items = text
    .split(/[,;]| i /)
    .map(item => item.trim())
    .filter(item => item.length > 0);
  
  const content = items.map(item => `- [ ] ${item}`).join('\n') + '\n';
  await appendToFile(filePath, content);
  
  return `?? Dodano ${items.length} produkty do ~/notes/lists/shopping.md`;
}

async function handleIdeas(text) {
  // Wyciπgnij nazwÍ projektu (jeúli jest)
  const projectMatch = text.match(/projekt[:\s]+([a-zA-Z0-9\-πÊÍ≥ÒÛúüø•∆ £—”åèØ\s]+)/i);
  const projectName = projectMatch 
    ? projectMatch[1].trim().toLowerCase().replace(/\s+/g, '-')
    : 'general';
  
  const dateStamp = getDateStamp();
  const projectDir = path.join(CONFIG.directories.ideas, `${dateStamp}-${projectName}`);
  const filePath = path.join(projectDir, 'README.md');
  
  await ensureDirectoryExists(projectDir);
  
  const content = `# Pomys≥: ${projectName}\n\n**Data:** ${getTimestamp()}\n\n${text}\n`;
  await appendToFile(filePath, content);
  
  return `?? Zapisano pomys≥ w ~/notes/ideas/${dateStamp}-${projectName}/README.md`;
}

async function handlePeople(text) {
  const filePath = path.join(CONFIG.directories.people, 'database.md');
  await ensureDirectoryExists(CONFIG.directories.people);
  
  const lowerText = text.toLowerCase();
  
  // Sprawdü czy to query czy dodawanie
  if (lowerText.includes('sprawdü')) {
    // Wyciπgnij imiÍ osoby
    const nameMatch = text.match(/sprawdü osobÍ[:\s]+([a-zA-ZπÊÍ≥ÒÛúüø•∆ £—”åèØ\s]+)/i);
    if (!nameMatch) {
      return '? Nie podano imienia osoby do sprawdzenia';
    }
    
    const name = nameMatch[1].trim();
    const database = await readFile(filePath);
    
    if (database.includes(`## ${name}`)) {
      return `?? ${name} jest w bazie! Sprawdü szczegÛ≥y w ~/notes/people/database.md`;
    } else {
      return `? ${name} nie ma w bazie`;
    }
  }
  
  // Dodawanie osoby
  const nameMatch = text.match(/dodaj osobÍ[:\s]+([a-zA-ZπÊÍ≥ÒÛúüø•∆ £—”åèØ\s]+?)(?:,|$)/i);
  if (!nameMatch) {
    return '? Nie podano imienia osoby';
  }
  
  const name = nameMatch[1].trim();
  const details = text.replace(/dodaj osobÍ[:\s]+[^,]+,?\s*/i, '').trim();
  
  const content = `\n## ${name}\n- **Dodano:** ${getTimestamp()}\n- ${details}\n`;
  await appendToFile(filePath, content);
  
  return `? Dodano: ${name}\n?? ${details}\n?? ${getTimestamp()}\n?? ~/notes/people/database.md`;
}

async function handleWatchlist(text) {
  const filePath = path.join(CONFIG.directories.watchlist, 'watchlist.md');
  await ensureDirectoryExists(CONFIG.directories.watchlist);
  
  // Wyciπgnij tytu≥
  const titleMatch = text.match(/(?:zapisz film|serial)[:\s]+([a-zA-Z0-9\-πÊÍ≥ÒÛúüø•∆ £—”åèØ\s]+)/i);
  if (!titleMatch) {
    return '? Nie podano tytu≥u';
  }
  
  const title = titleMatch[1].trim();
  const content = `- [ ] ${title} *(dodano: ${getTimestamp()})*\n`;
  await appendToFile(filePath, content);
  
  return `?? Dodano: ${title}\n?? ~/notes/watchlist/watchlist.md`;
}

// ================================================================================
// G£”WNY HANDLER
// ================================================================================

async function processVoiceNote(audioPath) {
  try {
    // 1. Transkrypcja
    console.log('?? TranskrybujÍ notatkÍ g≥osowπ...');
    const transcription = await transcribeAudio(audioPath);
    
    if (!transcription || transcription.trim().length === 0) {
      return '? Transkrypcja nie powiod≥a siÍ - pusta notatka';
    }
    
    console.log(`? Transkrypcja: "${transcription}"`);
    
    // 2. Kategoryzacja
    const category = detectCategory(transcription);
    console.log(`??? Kategoria: ${category}`);
    
    // 3. Obs≥uga wed≥ug kategorii
    let result;
    switch (category) {
      case 'songs':
        result = await handleSongs(transcription);
        break;
      case 'tasks':
        result = await handleTasks(transcription);
        break;
      case 'shopping':
        result = await handleShopping(transcription);
        break;
      case 'ideas':
        result = await handleIdeas(transcription);
        break;
      case 'people':
        result = await handlePeople(transcription);
        break;
      case 'watchlist':
        result = await handleWatchlist(transcription);
        break;
      default:
        result = await handleIdeas(transcription); // Fallback
    }
    
    return result;
    
  } catch (error) {
    console.error('? B≥πd przetwarzania notatki g≥osowej:', error);
    return `? B≥πd: ${error.message}`;
  }
}

// ================================================================================
// OPENCLAW INTEGRATION
// ================================================================================

module.exports = {
  name: 'voice-notes-pro',
  description: 'Inteligentna transkrypcja i kategoryzacja notatek g≥osowych',
  version: '1.0.0',
  
  async execute({ message, context }) {
    // Sprawdü czy to notatka g≥osowa z WhatsApp
    if (!message.audio && !message.voice) {
      return {
        success: false,
        message: 'Ten skill obs≥uguje tylko notatki g≥osowe',
      };
    }
    
    // Pobierz úcieøkÍ do pliku audio
    const audioPath = message.audio?.path || message.voice?.path;
    if (!audioPath) {
      return {
        success: false,
        message: 'Nie znaleziono pliku audio',
      };
    }
    
    // PrzetwÛrz notatkÍ
    const result = await processVoiceNote(audioPath);
    
    return {
      success: true,
      message: result,
    };
  },
};