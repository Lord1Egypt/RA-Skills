// Persistent watchlist store using JSON file (watchlist persists across restarts)
const fs = require('fs');
const path = require('path');

const STORAGE_FILE = path.join(__dirname, 'watchlist.json');

function load() {
  try {
    if (fs.existsSync(STORAGE_FILE)) {
      const data = fs.readFileSync(STORAGE_FILE, 'utf8');
      return JSON.parse(data);
    }
  } catch (err) {
    console.error('Failed to load watchlist:', err.message);
  }
  return { channels: [] };
}

function save(watchlist) {
  try {
    fs.writeFileSync(STORAGE_FILE, JSON.stringify(watchlist, null, 2));
  } catch (err) {
    console.error('Failed to save watchlist:', err.message);
  }
}

let WATCHLIST = load();

function getWatchlist() {
  return WATCHLIST.channels;
}

function findChannel(channelId) {
  return WATCHLIST.channels.find(c => c.id === channelId);
}

function addChannel(channel) {
  if (!findChannel(channel.id)) {
    WATCHLIST.channels.push(channel);
    save(WATCHLIST);
    return true;
  }
  return false;
}

function removeChannelById(channelId) {
  const index = WATCHLIST.channels.findIndex(c => c.id === channelId);
  if (index !== -1) {
    WATCHLIST.channels.splice(index, 1);
    save(WATCHLIST);
    return true;
  }
  return false;
}

function clear() {
  WATCHLIST = { channels: [] };
  save(WATCHLIST);
}

module.exports = {
  WATCHLIST,
  getWatchlist,
  findChannel,
  addChannel,
  removeChannelById,
  clear
};