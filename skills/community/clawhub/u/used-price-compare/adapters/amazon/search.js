/* @meta
{
  "name": "amazon/search",
  "description": "Search Amazon product listings (new, renewed/refurbished items)",
  "domain": "www.amazon.com",
  "args": {
    "query": {"required": true, "description": "Search keyword"},
    "sort": {"required": false, "description": "Sort: price=low to high, -price=high to low, reviews=avg reviews, date=newest (default: price)"},
    "condition": {"required": false, "description": "Condition: new, renewed, used, all (default: all)"},
    "maxPrice": {"required": false, "description": "Max price filter, e.g. 500"}
  },
  "capabilities": ["search", "marketplace"],
  "readOnly": true,
  "example": "bb-browser site amazon/search 'iPhone 15 Pro' --condition renewed --sort price"
}
*/
async function(args) {
  if (!args.query) return { error: 'Missing argument: query' };

  const SITE_HOST = 'www.amazon.com';
  const SITE_CURRENCY = '$';
  const SITE_REGION = 'US (nationwide)';

  const sortMap = {
    'price': 'price-asc-rank',
    '-price': 'price-desc-rank',
    'reviews': 'review-rank',
    'date': 'date-desc-rank',
    'best': 'relevanceblender',
  };

  const sort = args.sort || 'best';
  const condition = args.condition || 'all';
  const sortVal = sortMap[sort] || 'price-asc-rank';

  let url = `https://${SITE_HOST}/s?k=${encodeURIComponent(args.query)}&s=${sortVal}`;

  const conditionMap = {
    'new': '2224371011',
    'renewed': '16907720011',
    'refurbished': '16907720011',
    'used': '2224373011',
  };
  const condNode = conditionMap[condition];
  if (condNode) {
    url += `&rh=p_n_condition-type%3A${condNode}`;
  }

  if (args.maxPrice) {
    url += `&high-price=${args.maxPrice}`;
  }

  // Force USD currency
  url += '&currency=USD';

  const resp = await fetch(url, {
    credentials: 'include',
    headers: {
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Language': 'en-US,en;q=0.9',
      'Accept-Encoding': 'gzip, deflate, br',
      'Sec-Fetch-Dest': 'document',
      'Sec-Fetch-Mode': 'navigate',
      'Sec-Fetch-Site': 'none',
      'Sec-Fetch-User': '?1',
      'Upgrade-Insecure-Requests': '1',
    }
  });
  if (!resp.ok) return { error: `HTTP ${resp.status}`, hint: 'Amazon may require CAPTCHA or login' };

  const html = await resp.text();
  const parser = new DOMParser();
  const doc = parser.parseFromString(html, 'text/html');

  // --- CAPTCHA detection ---
  const captchaForm = doc.querySelector(
    '#captchacharacters, form[action*="validateCaptcha"], form[action*="errors/validateCaptcha"]'
  );
  if (captchaForm) {
    return {
      error: 'Amazon CAPTCHA triggered',
      hint: 'The browser session needs to solve a CAPTCHA. Open amazon.com in Chrome, solve the CAPTCHA, then retry.',
    };
  }

  // --- Region detection ---
  const deliverEl = doc.querySelector('#glow-ingress-line2');
  const deliverTo = deliverEl ? deliverEl.textContent.trim() : '';
  const isWrongRegion = deliverTo && !/US|United States|America/i.test(deliverTo) && !/^\d{5}/.test(deliverTo);

  const listings = [];

  const items = doc.querySelectorAll('[data-component-type="s-search-result"]');
  for (const item of items) {
    const asin = item.getAttribute('data-asin');
    if (!asin) continue;

    const titleEl = item.querySelector('h2 a span, h2 span');
    if (!titleEl) continue;
    const title = titleEl.textContent.trim();

    const priceEl = item.querySelector('.a-price .a-offscreen');
    let price = priceEl ? priceEl.textContent.trim() : '';

    const cleanUrl = `https://${SITE_HOST}/dp/${asin}`;

    const ratingEl = item.querySelector('.a-icon-alt');
    const rating = ratingEl ? ratingEl.textContent.trim() : '';

    const reviewEl = item.querySelector('.a-size-base.s-underline-text, [aria-label*="stars"] + span');
    const reviews = reviewEl ? reviewEl.textContent.trim().replace(/[,()]/g, '') : '';

    const primeEl = item.querySelector('.a-icon-prime, [aria-label="Amazon Prime"]');
    const isPrime = !!primeEl;

    const imageEl = item.querySelector('.s-image');
    const image = imageEl ? (imageEl.getAttribute('src') || '') : '';

    const condBadge = item.querySelector('.a-badge-text');
    const conditionText = condBadge ? condBadge.textContent.trim() : '';

    if (!price) continue;

    listings.push({
      title,
      price,
      url: cleanUrl,
      condition: conditionText || (condition === 'all' ? '' : condition),
      rating,
      reviews,
      prime: isPrime ? 'Prime' : '',
      image,
      source: 'amazon.com',
    });
  }

  const usdCount = listings.filter(l => l.price.startsWith('$')).length;
  const wrongCurrency = listings.length > 0 && usdCount === 0;

  if (listings.length === 0 && isWrongRegion) {
    return {
      error: `Amazon detected location as "${deliverTo}" instead of US — no results returned`,
      hint: 'Open amazon.com in Chrome, change delivery address to a US zip code, then retry.',
    };
  }

  if (wrongCurrency) {
    const samplePrice = listings[0]?.price || '';
    const detectedCurrency = samplePrice.replace(/[\d,.\s]/g, '').trim() || 'unknown';
    return {
      error: `Amazon US showing prices in ${detectedCurrency} instead of USD (delivery set to "${deliverTo}")`,
      hint: 'Open amazon.com → Account → Manage Currency Setting → change to USD, then retry.',
    };
  }

  const prices = listings.map(l => parseFloat(l.price.replace(/[^0-9.]/g, ''))).filter(p => !isNaN(p));

  return {
    total: listings.length,
    listings,
    summary: {
      keyword: args.query,
      region: SITE_REGION,
      condition,
      priceRange: prices.length ? `${SITE_CURRENCY}${Math.min(...prices).toFixed(2)} ~ ${SITE_CURRENCY}${Math.max(...prices).toFixed(2)}` : 'N/A',
      avgPrice: prices.length ? `${SITE_CURRENCY}${(prices.reduce((a, b) => a + b, 0) / prices.length).toFixed(2)}` : 'N/A',
      resultCount: listings.length,
    },
  };
}
