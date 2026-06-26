/* @meta
{
  "name": "ok/search",
  "description": "Search listings on OK.com marketplace (second-hand goods, jobs, property, etc.)",
  "domain": "ok.com",
  "args": {
    "query": {"required": true, "description": "Search keyword"},
    "country": {"required": false, "description": "Country code: us/uk/au/ca/ae (default: us)"},
    "city": {"required": false, "description": "City slug, e.g. los-angeles, london (default: los-angeles)"},
    "category": {"required": false, "description": "Category: marketplace|jobs|property|cars|services|community"},
    "sort": {"required": false, "description": "Sort: 0=Best Match, 1=Newest, 3=Lowest Price, 4=Highest Price (default: 0)"}
  },
  "capabilities": ["search", "marketplace"],
  "readOnly": true,
  "example": "bb-browser site ok/search 'iPhone 15' --country us --city los-angeles --category marketplace --sort 3"
}
*/
async function(args) {
  if (!args.query) return { error: 'Missing argument: query' };

  const country = args.country || 'us';
  const city = args.city || 'los-angeles';
  const category = args.category || '';
  const sort = parseInt(args.sort || '0', 10);
  const lang = 'en';

  const domainMap = { gb: 'uk', au: 'au', ca: 'ca', ae: 'ae', us: 'us' };
  const domain = domainMap[country] || country;

  const currencyMap = { us: '$', uk: '£', gb: '£', au: 'A$', ca: 'C$', ae: 'AED ' };
  const currency = currencyMap[country] || '$';

  const catPath = category ? `cate-${category}` : 'cate-marketplace';
  let url = `https://${domain}.ok.com/${lang}/city-${city}/${catPath}/?keyword=${encodeURIComponent(args.query)}`;
  if (sort) url += `&sortId=${sort}`;

  const resp = await fetch(url, { credentials: 'include' });
  if (!resp.ok) return { error: `HTTP ${resp.status}`, hint: 'Check country/city codes' };

  const html = await resp.text();

  const text = html
    .replace(/&quot;/g, '"')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>');

  // Check server-side total first — if the API returned 0, no parsing will help
  const totalMatch = text.match(/"total"\s*:\s*(\d+)/);
  const serverTotal = totalMatch ? parseInt(totalMatch[1]) : -1;

  const listings = [];

  // Primary pattern: objects with title + price + action fields
  const objPattern = /\{[^{}]*?"title"\s*:\s*"([^"]+)"[^{}]*?"price"\s*:\s*"([^"]+)"[^{}]*?"action"\s*:\s*"([^"]+)"[^{}]*\}/g;
  let match;
  while ((match = objPattern.exec(text)) !== null) {
    const title = match[1];
    const price = match[2];
    const action = match[3];

    if (title &&
        !title.includes('Marketplace in') &&
        !title.includes('pageTitle') &&
        !title.includes('Not Found') &&
        !title.includes('Marketplace"') &&
        title.length > 3 &&
        title.length < 200) {
      listings.push({ title, price, action });
    }
  }

  // Fallback: extract from self.__next_f chunks
  if (listings.length === 0) {
    const scriptPattern = /<script[^>]*>\s*self\.__next_f\.push\(\s*(\[[\s\S]*?\])\s*\)\s*<\/script>/g;
    const chunks = [];
    let m;
    while ((m = scriptPattern.exec(html)) !== null) {
      try {
        const arr = JSON.parse(m[1]);
        if (Array.isArray(arr) && typeof arr[1] === 'string') {
          const decoded = arr[1]
            .replace(/&quot;/g, '"')
            .replace(/&amp;/g, '&');
          chunks.push(decoded);
        }
      } catch (_) {}
    }

    const chunkText = chunks.join('\n');

    const tpMatch = /"title"\s*:\s*"([^"]+)"[^}]*?"price"\s*:\s*"([^"]+)"[^}]*?"action"\s*:\s*"([^"]+)"/g;
    while ((match = tpMatch.exec(chunkText)) !== null) {
      const title = match[1];
      if (title && !title.includes('Marketplace') && !title.includes('Not Found') && title.length > 3) {
        listings.push({ title, price: match[2], action: match[3] });
      }
    }
  }

  if (listings.length === 0) {
    const reason = serverTotal === 0
      ? `OK.com ${domain.toUpperCase()} marketplace has no results for '${args.query}' in ${city}`
      : `Could not parse listings (server reported ${serverTotal} results) — page structure may have changed`;
    return {
      total: serverTotal >= 0 ? serverTotal : 0,
      listings: [],
      summary: reason,
    };
  }

  // Deduplicate by title
  const seen = new Set();
  const unique = listings.filter(l => {
    if (seen.has(l.title)) return false;
    seen.add(l.title);
    return true;
  });

  const mapped = unique.slice(0, 20).map(item => {
    let price = item.price || '';
    // Normalize price: strip duplicate currency symbols (e.g. "$$300" → "$300")
    price = price.replace(/^\$\$/, '$').replace(/^££/, '£');
    // Ensure price has a currency symbol
    if (price && /^\d/.test(price)) {
      price = currency + price;
    }

    return {
      title: item.title,
      price,
      category: '',
      condition: '',
      seller: '',
      image: '',
      url: item.action?.startsWith('http') ? item.action : `https://${domain}.ok.com${item.action}`,
      location: '',
      postDate: '',
      source: 'ok.com',
    };
  });

  const prices = mapped
    .map(l => parseFloat(l.price?.replace(/[^0-9.]/g, '') || '0'))
    .filter(p => p > 0);

  return {
    total: serverTotal >= 0 ? serverTotal : mapped.length,
    listings: mapped,
    summary: {
      keyword: args.query,
      region: `${domain.toUpperCase()} / ${city}`,
      priceRange: prices.length ? `${currency}${Math.min(...prices).toFixed(2)} ~ ${currency}${Math.max(...prices).toFixed(2)}` : 'N/A',
      avgPrice: prices.length ? `${currency}${(prices.reduce((a, b) => a + b, 0) / prices.length).toFixed(2)}` : 'N/A',
      resultCount: mapped.length,
    },
  };
}
