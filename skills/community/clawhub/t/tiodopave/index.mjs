#!/usr/bin/env node

import { readFileSync, writeFileSync } from 'fs';

const REDDIT_SUB = 'tiodopave';
const REDDIT_URL = `https://www.reddit.com/r/${REDDIT_SUB}/hot.json?limit=25`;
const LAST_JOKE_FILE = '/tmp/last-joke.txt';

function getLastJoke() {
  try {
    return readFileSync(LAST_JOKE_FILE, 'utf8').trim();
  } catch {
    return '';
  }
}

function setLastJoke(id) {
  writeFileSync(LAST_JOKE_FILE, id);
}

function cleanText(text) {
  return text
    .replace(/\[.*?\]\(.*?\)/g, '') // Remove links markdown
    .replace(/https?:\/\/[^\s]*/g, '') // Remove URLs
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&nbsp;/g, ' ')
    .replace(/\n{3,}/g, '\n\n') // Max 2 quebras de linha
    .trim();
}

function containsNSFW(title, selftext) {
  const nsfwKeywords = ['nsfw', 'porn', 'sexo', 'erótico', '18+', 'xxx', 'nu', 'nu(a)?'];
  const combined = `${title} ${selftext}`.toLowerCase();
  return nsfwKeywords.some(k => new RegExp(k).test(combined));
}

async function fetchJoke() {
  console.error('Buscando piadas do Reddit...');
  
  const res = await fetch(REDDIT_URL, {
    headers: {
      'User-Agent': 'OpenClaw/1.0 (Seth Bot)',
      'Accept': 'application/json'
    }
  });
  
  if (!res.ok) {
    throw new Error(`Reddit API error: ${res.status}`);
  }
  
  const data = await res.json();
  const posts = data.data.children
    .map(p => p.data)
    .filter(p => p.score >= 5) // Só posts com upvote razoável
    .filter(p => !containsNSFW(p.title, p.selftext || '')); // Sem NSFW
  
  if (posts.length === 0) {
    throw new Error('Nenhuma piada encontrada');
  }
  
  // Tentar não repetir a última
  const lastId = getLastJoke();
  const filtered = posts.filter(p => p.id !== lastId);
  const chosen = filtered.length > 0 
    ? filtered[Math.floor(Math.random() * filtered.length)]
    : posts[Math.floor(Math.random() * posts.length)];
  
  setLastJoke(chosen.id);
  
  const title = cleanText(chosen.title);
  const selftext = cleanText(chosen.selftext || '');
  
  if (selftext) {
    return `${title}\n\n${selftext}`;
  }
  return title;
}

fetchJoke()
  .then(joke => {
    console.log(joke);
    process.exit(0);
  })
  .catch(err => {
    console.error('Erro:', err.message);
    process.exit(1);
  });
