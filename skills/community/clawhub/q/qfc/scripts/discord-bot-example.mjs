#!/usr/bin/env node

// Example: QFC Discord Bot using discord.js
// Install: npm install discord.js
// Run:     DISCORD_TOKEN=your_token node scripts/discord-bot-example.mjs
//
// This file is a usage example only — discord.js is NOT a dependency of this package.

import { Client, GatewayIntentBits } from 'discord.js';
import { QFCDiscordBot } from '../dist/discord.js';

const DISCORD_TOKEN = process.env.DISCORD_TOKEN;
if (!DISCORD_TOKEN) {
  console.error('Error: Set the DISCORD_TOKEN environment variable.');
  process.exit(1);
}

// Use testnet by default; set QFC_NETWORK=mainnet to override
const network = process.env.QFC_NETWORK === 'mainnet' ? 'mainnet' : 'testnet';
const bot = new QFCDiscordBot(network);

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
  ],
});

client.once('ready', () => {
  console.log(`QFC Bot logged in as ${client.user.tag} (network: ${network})`);
});

client.on('messageCreate', async (message) => {
  // Ignore bot messages
  if (message.author.bot) return;

  const response = await bot.handleMessage(message.content);
  if (response) {
    await message.reply(response.message);
  }
});

client.login(DISCORD_TOKEN);
