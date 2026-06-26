#!/usr/bin/env node
const https = require('https');

function inferMarket(code) {
  if (!/^\d{6}$/.test(code)) return null;
  if (code.startsWith('6') || code.startsWith('9') || code.startsWith('5')) return 'sh';
  return 'sz';
}

function fetchText(url) {
  return new Promise((resolve, reject) => {
    const req = https.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 OpenClaw stock-tools',
        'Referer': 'https://finance.sina.com.cn/'
      }
    }, (res) => {
      const chunks = [];
      res.on('data', chunk => chunks.push(chunk));
      res.on('end', () => {
        try {
          const buffer = Buffer.concat(chunks);
          const text = new TextDecoder('gbk').decode(buffer);
          resolve(text);
        } catch (err) {
          reject(err);
        }
      });
    });
    req.on('error', reject);
    req.setTimeout(10000, () => req.destroy(new Error('Request timeout')));
  });
}

function isInvalidPrice({ price, prevClose, open, high, low, volume, amount }) {
  if (!Number.isFinite(price) || price < 0) return true;
  if (price === 0 && prevClose > 0) return true;
  if (price === 0 && open === 0 && high === 0 && low === 0 && volume === 0 && amount === 0) return true;
  return false;
}

function parseSina(code, text) {
  const market = inferMarket(code);
  const symbol = `${market}${code}`;
  const re = new RegExp(`var hq_str_${symbol}="([^"]*)"`);
  const m = text.match(re);
  if (!m) throw new Error(`Quote not found for ${symbol}`);
  const raw = m[1];
  const parts = raw.split(',');
  if (parts.length < 32) throw new Error('Unexpected quote payload');

  const name = parts[0] || code;
  const open = Number(parts[1]);
  const prevClose = Number(parts[2]);
  const price = Number(parts[3]);
  const high = Number(parts[4]);
  const low = Number(parts[5]);
  const volume = Number(parts[8]);
  const amount = Number(parts[9]);
  const date = parts[30] || null;
  const time = parts[31] || null;
  const invalid = isInvalidPrice({ price, prevClose, open, high, low, volume, amount });
  const safePrice = invalid ? null : price;
  const change = !invalid && Number.isFinite(prevClose) ? Number((price - prevClose).toFixed(2)) : null;
  const pct = !invalid && prevClose ? Number((((price - prevClose) / prevClose) * 100).toFixed(2)) : null;

  return {
    code,
    market,
    symbol,
    name,
    open,
    prevClose,
    price: safePrice,
    high,
    low,
    volume,
    amount,
    change,
    pct,
    quoteDate: date,
    quoteTime: time,
    detailUrl: `https://stockpage.10jqka.com.cn/${code}/`,
    valid: !invalid,
    note: invalid ? '报价异常或暂不可用' : null
  };
}

function formatLine(item) {
  const ts = item.quoteDate && item.quoteTime ? `${item.quoteDate} ${item.quoteTime}` : '时间未确认';

  // 非交易时段/未产生有效现价：给更人话的提示，并尽量展示昨收
  if (!item.valid) {
    const prev = Number.isFinite(item.prevClose) && item.prevClose > 0 ? `昨收：${item.prevClose} 元` : '昨收不可用';
    return `${item.code} ${item.name}｜非交易时段或无有效实时报价｜${prev}｜${ts}`;
  }

  const changeText = item.change === null || item.pct === null
    ? '涨跌未确认'
    : `${item.change >= 0 ? '+' : ''}${item.change}（${item.pct >= 0 ? '+' : ''}${item.pct}%）`;
  return `${item.code} ${item.name}｜${item.price} 元｜${changeText}｜${ts}`;
}

async function main() {
  const argv = process.argv.slice(2).filter(Boolean);
  const plain = argv.filter(arg => arg !== '--json');
  const wantJson = argv.includes('--json');
  if (!plain.length) {
    console.error('Usage: fetch_quote.js [--json] <code> [code2 ...]');
    process.exit(1);
  }

  const normalized = plain.map(code => code.trim()).filter(code => /^\d{6}$/.test(code));
  if (!normalized.length) {
    console.error('No valid 6-digit stock codes provided');
    process.exit(1);
  }

  const symbols = normalized.map(code => `${inferMarket(code)}${code}`).join(',');
  const text = await fetchText(`https://hq.sinajs.cn/list=${symbols}`);
  const result = normalized.map(code => parseSina(code, text));

  if (wantJson) {
    process.stdout.write(JSON.stringify(result, null, 2));
    return;
  }

  process.stdout.write(result.map(formatLine).join('\n'));
}

main().catch(err => {
  console.error(err.message || String(err));
  process.exit(1);
});
