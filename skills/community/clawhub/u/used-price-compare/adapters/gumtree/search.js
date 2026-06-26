/* @meta
{
  "name": "gumtree/search",
  "description": "Search Gumtree UK classified listings (second-hand goods, local services)",
  "domain": "www.gumtree.com",
  "args": {
    "query": {"required": true, "description": "Search keyword"},
    "location": {"required": false, "description": "Location name, e.g. London, Manchester, Birmingham (default: London)"},
    "sort": {"required": false, "description": "Sort: price=lowest first, -price=highest first, date=newest (default: price)"},
    "category": {"required": false, "description": "Category: all, for-sale, electronics, phones (default: all)"},
    "maxPrice": {"required": false, "description": "Max price filter, e.g. 500"},
    "minPrice": {"required": false, "description": "Min price filter, e.g. 10"}
  },
  "capabilities": ["search", "marketplace"],
  "readOnly": true,
  "example": "bb-browser site gumtree/search 'iPhone 15 Pro' --location London --sort price"
}
*/
async function(args) {
  if (!args.query) return { error: 'Missing argument: query' };

  const sortMap = {
    'price': 'price_lowest_first',
    '-price': 'price_highest_first',
    'date': 'date',
    'best': '',
  };

  const categoryMap = {
    'all': 'all',
    'for-sale': 'for-sale',
    'electronics': 'computers-software',
    'phones': 'phones-mobile-phones',
  };

  const location = args.location || 'London';
  const sort = args.sort || 'best';
  const category = args.category || 'all';
  const sortVal = sortMap[sort] || '';
  const catVal = categoryMap[category] || 'all';

  let url = `https://www.gumtree.com/search?search_category=${encodeURIComponent(catVal)}&q=${encodeURIComponent(args.query)}&search_location=${encodeURIComponent(location)}`;

  if (sortVal) {
    url += `&sort=${sortVal}`;
  }
  if (args.minPrice) {
    url += `&min_price=${args.minPrice}`;
  }
  if (args.maxPrice) {
    url += `&max_price=${args.maxPrice}`;
  }

  const resp = await fetch(url, { credentials: 'include' });
  if (!resp.ok) return { error: `HTTP ${resp.status}`, url, hint: 'Gumtree may be rate limiting' };

  const html = await resp.text();
  const parser = new DOMParser();
  const doc = parser.parseFromString(html, 'text/html');

  const listings = [];

  const articles = doc.querySelectorAll('article[data-q="search-result"]');
  for (const article of articles) {
    const titleEl = article.querySelector('[data-q="tile-title"]');
    const priceEl = article.querySelector('[data-q="tile-price"]');
    const locationEl = article.querySelector('[data-q="tile-location"]');
    const descEl = article.querySelector('[data-q="tile-description"]');
    const linkEl = article.querySelector('a');
    const imageEl = article.querySelector('img');

    if (!titleEl) continue;
    const title = titleEl.textContent.trim();
    if (!title) continue;

    const priceText = priceEl ? priceEl.textContent.trim() : '';
    const isFree = /^free$/i.test(priceText);
    const priceMatch = priceText.match(/£[\d,]+\.?\d*/);
    const price = priceMatch ? priceMatch[0] : (isFree ? '£0' : priceText);

    const href = linkEl ? linkEl.getAttribute('href') : '';
    const fullUrl = href && !href.startsWith('http') ? `https://www.gumtree.com${href}` : href;

    listings.push({
      title,
      price,
      url: fullUrl ? fullUrl.split('?')[0] : '',
      condition: '',
      location: locationEl ? locationEl.textContent.trim() : '',
      description: descEl ? descEl.textContent.trim().substring(0, 200) : '',
      image: imageEl ? (imageEl.getAttribute('src') || imageEl.getAttribute('data-src') || '') : '',
      source: 'gumtree.com'
    });
  }

  const prices = listings.map(l => parseFloat(l.price.replace(/[^0-9.]/g, ''))).filter(p => !isNaN(p));

  return {
    total: listings.length,
    listings,
    summary: {
      keyword: args.query,
      region: `UK (${location})`,
      sort: sort,
      priceRange: prices.length ? `£${Math.min(...prices).toFixed(2)} ~ £${Math.max(...prices).toFixed(2)}` : 'N/A',
      avgPrice: prices.length ? `£${(prices.reduce((a, b) => a + b, 0) / prices.length).toFixed(2)}` : 'N/A',
      resultCount: listings.length
    }
  };
}
