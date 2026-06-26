/* @meta
{
  "name": "ebay/search-uk",
  "description": "Search eBay UK (nationwide) listings (new, used, refurbished items)",
  "domain": "www.ebay.co.uk",
  "args": {
    "query": {"required": true, "description": "Search keyword"},
    "condition": {"required": false, "description": "Condition: used, new, refurbished, all (default: all)"},
    "sort": {"required": false, "description": "Sort: price=lowest first, -price=highest first, date=newest (default: price)"},
    "buyingFormat": {"required": false, "description": "Format: auction, buyitnow, all (default: all)"},
    "maxPrice": {"required": false, "description": "Max price filter, e.g. 500"}
  },
  "capabilities": ["search", "marketplace"],
  "readOnly": true,
  "example": "bb-browser site ebay/search-uk 'iPhone 15 Pro' --condition used --sort price"
}
*/
async function(args) {
  if (!args.query) return { error: 'Missing argument: query' };

  const SITE_HOST = 'www.ebay.co.uk';
  const SITE_CURRENCY = '£';
  const SITE_REGION = 'UK (nationwide)';
  const SITE_SOURCE = 'ebay.co.uk';

  const conditionMap = {
    'new': '1000',
    'refurbished': '2500',
    'used': '3000',
    'all': ''
  };
  const sortMap = {
    'price': '15',
    '-price': '16',
    'date': '10',
    'best': '12',
  };

  const condition = args.condition || 'all';
  const sort = args.sort || 'best';
  const condVal = conditionMap[condition] || '';
  const sortVal = sortMap[sort] || '15';

  let url = `https://${SITE_HOST}/sch/i.html?_nkw=${encodeURIComponent(args.query)}&_sop=${sortVal}`;

  if (condVal) {
    url += `&LH_ItemCondition=${condVal}`;
  }
  if (args.buyingFormat === 'auction') {
    url += '&LH_Auction=1';
  } else if (args.buyingFormat === 'buyitnow') {
    url += '&LH_BIN=1';
  }
  if (args.maxPrice) {
    url += `&_udhi=${args.maxPrice}`;
  }

  const resp = await fetch(url, { credentials: 'include' });
  if (!resp.ok) return { error: `HTTP ${resp.status}`, url, hint: 'eBay may be rate limiting' };

  const html = await resp.text();
  const parser = new DOMParser();
  const doc = parser.parseFromString(html, 'text/html');

  const listings = [];

  // 2025+ eBay layout uses .s-card; legacy uses .s-item
  const cards = doc.querySelectorAll('.s-card');
  if (cards.length > 0) {
    for (const card of cards) {
      const titleEl = card.querySelector('.s-card__title');
      const priceEl = card.querySelector('.s-card__price');
      const linkEl = card.querySelector('a.s-card__link');
      const subtitleEl = card.querySelector('.s-card__subtitle');
      const imageEl = card.querySelector('.s-card__image');

      if (!titleEl) continue;
      const rawTitle = titleEl.textContent.trim();
      const title = rawTitle.replace(/Opens in a new window or tab$/i, '').replace(/^New listing/i, '').trim();
      if (title === 'Shop on eBay' || title === 'Results matching fewer words') continue;

      const priceText = priceEl ? priceEl.textContent.trim() : '';
      const priceMatch = priceText.match(/[£$€A-C]?\$?[\d,]+\.?\d*/);
      const price = priceMatch ? priceMatch[0] : priceText;

      const href = linkEl ? linkEl.getAttribute('href') : '';
      const cleanUrl = href ? href.split('?')[0] : '';

      const attrRows = card.querySelectorAll('.s-card__attribute-row');
      const attrs = Array.from(attrRows).map(r => r.textContent.trim());
      const shippingAttr = attrs.find(a => /delivery|shipping|postage/i.test(a)) || '';
      const isFreeShipping = /free/i.test(shippingAttr);
      const sellerAttr = attrs.find(a => /positive/i.test(a)) || '';

      listings.push({
        title,
        price,
        url: cleanUrl,
        condition: subtitleEl ? subtitleEl.textContent.trim() : '',
        shipping: shippingAttr,
        freeShipping: isFreeShipping ? 'Yes' : '',
        seller: sellerAttr,
        image: imageEl ? (imageEl.getAttribute('src') || imageEl.getAttribute('data-src') || '') : '',
        source: SITE_SOURCE
      });
    }
  } else {
    // Legacy .s-item layout (fallback)
    const items = doc.querySelectorAll('.s-item');
    for (const item of items) {
      const titleEl = item.querySelector('.s-item__title span[role="heading"], .s-item__title');
      const priceEl = item.querySelector('.s-item__price');
      const linkEl = item.querySelector('.s-item__link');
      const condEl = item.querySelector('.SECONDARY_INFO');
      const shippingEl = item.querySelector('.s-item__shipping, .s-item__freeXDays');
      const locationEl = item.querySelector('.s-item__itemLocation, .s-item__location');
      const imageEl = item.querySelector('.s-item__image-img, img');

      if (!titleEl) continue;
      const title = titleEl.textContent.trim();
      if (title === 'Shop on eBay' || title === 'Results matching fewer words') continue;

      const priceText = priceEl ? priceEl.textContent.trim() : '';
      const priceMatch = priceText.match(/[£$€A-C]?\$?[\d,]+\.?\d*/);
      const price = priceMatch ? priceMatch[0] : priceText;

      const href = linkEl ? linkEl.getAttribute('href') : '';
      const cleanUrl = href ? href.split('?')[0] : '';

      const shipping = shippingEl ? shippingEl.textContent.trim() : '';
      const isFreeShipping = /free/i.test(shipping);

      listings.push({
        title,
        price,
        url: cleanUrl,
        condition: condEl ? condEl.textContent.trim() : '',
        shipping,
        freeShipping: isFreeShipping ? 'Yes' : '',
        location: locationEl ? locationEl.textContent.trim().replace('from ', '') : '',
        image: imageEl ? (imageEl.getAttribute('src') || imageEl.getAttribute('data-src') || '') : '',
        source: SITE_SOURCE
      });
    }
  }

  const prices = listings.map(l => parseFloat(l.price.replace(/[^0-9.]/g, ''))).filter(p => !isNaN(p));

  return {
    total: listings.length,
    listings,
    summary: {
      keyword: args.query,
      region: SITE_REGION,
      condition: condition,
      priceRange: prices.length ? `${SITE_CURRENCY}${Math.min(...prices).toFixed(2)} ~ ${SITE_CURRENCY}${Math.max(...prices).toFixed(2)}` : 'N/A',
      avgPrice: prices.length ? `${SITE_CURRENCY}${(prices.reduce((a, b) => a + b, 0) / prices.length).toFixed(2)}` : 'N/A',
      resultCount: listings.length
    }
  };
}
