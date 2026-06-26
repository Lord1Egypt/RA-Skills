/**
 * Telegram logging integration
 *
 * Formatters are shared with the standalone snake-rodeo-agents library.
 * Only sendTelegram and formatStatus (skill-specific) live here.
 */

import { loadSettings } from './config.mjs';
export { formatVote, formatGameEnd, formatTeamSwitch, formatError, formatWarning } from 'snake-rodeo-agents';

let cachedToken = null;

/**
 * Send a message to Telegram
 * Token resolution: TELEGRAM_BOT_TOKEN env var → settings.telegramBotToken → null
 */
export async function sendTelegram(text, chatId = null) {
  const settings = loadSettings();
  chatId = chatId || settings.telegramChatId;

  if (!chatId) return false;
  if (!settings.logToTelegram) return false;

  if (!cachedToken) {
    cachedToken = process.env.TELEGRAM_BOT_TOKEN || settings.telegramBotToken || null;
  }

  if (!cachedToken) {
    return false;
  }

  try {
    const res = await fetch(`https://api.telegram.org/bot${cachedToken}/sendMessage`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chat_id: chatId,
        text,
        parse_mode: 'HTML',
      }),
    });
    return res.ok;
  } catch {
    return false;
  }
}

export function formatStatus(state, settings) {
  const lines = [
    `🐍 Snake Daemon Status`,
    `├─ Strategy: ${settings.strategy}`,
    `├─ Server: ${settings.server}`,
    `├─ Paused: ${state.paused ? 'Yes' : 'No'}`,
    `├─ Current Team: ${state.currentTeam || 'None'}`,
    `├─ Games: ${state.gamesPlayed} (${state.wins} wins)`,
    `├─ Votes: ${state.votesPlaced}`,
    `└─ Running since: ${state.startedAt ? new Date(state.startedAt).toLocaleString() : 'N/A'}`,
  ];
  return lines.join('\n');
}
