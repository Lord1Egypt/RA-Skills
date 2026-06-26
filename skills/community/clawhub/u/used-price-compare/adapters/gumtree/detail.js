/* @meta
{
  "name": "gumtree/detail",
  "description": "Fetch Gumtree UK listing detail page",
  "domain": "www.gumtree.com",
  "args": {
    "url": {"required": true, "description": "Full URL of the Gumtree listing"}
  },
  "capabilities": ["detail", "marketplace"],
  "readOnly": true,
  "example": "bb-browser site gumtree/detail 'https://www.gumtree.com/p/phones/iphone-15-pro/12345'"
}
*/
async function(args) {
  if (!args.url) return { error: 'Missing argument: url' };

  const resp = await fetch(args.url, { credentials: 'include' });
  if (!resp.ok) return { error: `HTTP ${resp.status}`, hint: 'Check if the listing URL is valid' };

  const html = await resp.text();
  const parser = new DOMParser();
  const doc = parser.parseFromString(html, 'text/html');

  const titleEl = doc.querySelector('h1[data-q="ad-title"], h1');
  const title = titleEl ? titleEl.textContent.trim() : '';

  const priceEl = doc.querySelector('[data-q="ad-price"], .ad-price');
  let price = priceEl ? priceEl.textContent.trim() : '';
  const priceMatch = price.match(/£[\d,]+\.?\d*/);
  if (priceMatch) price = priceMatch[0];

  const descEl = doc.querySelector('[data-q="ad-description"], .ad-description, [itemprop="description"]');
  const description = descEl ? descEl.textContent.trim() : '';

  const images = [];
  const seenUrls = new Set();

  function addImage(src) {
    if (!src || !src.startsWith('http') || seenUrls.has(src)) return false;
    seenUrls.add(src);
    images.push(src);
    return images.length >= 10;
  }

  // Strategy 1: JSON-LD structured data (most reliable for static HTML)
  const ldScripts = doc.querySelectorAll('script[type="application/ld+json"]');
  for (const s of ldScripts) {
    try {
      const ld = JSON.parse(s.textContent);
      const candidates = Array.isArray(ld) ? ld : [ld];
      for (const obj of candidates) {
        const imgs = obj.image || obj.photo || [];
        const arr = Array.isArray(imgs) ? imgs : [imgs];
        for (const img of arr) {
          const url = typeof img === 'string' ? img : (img && (img.url || img.contentUrl));
          if (url && addImage(url)) break;
        }
        if (images.length >= 10) break;
      }
    } catch (_) {}
    if (images.length >= 10) break;
  }

  // Strategy 2: Open Graph / meta image tags
  if (images.length === 0) {
    const metaImgs = doc.querySelectorAll('meta[property="og:image"], meta[name="twitter:image"]');
    for (const m of metaImgs) {
      if (addImage(m.getAttribute('content'))) break;
    }
  }

  // Strategy 3: image URLs embedded in inline <script> (JS-rendered galleries)
  if (images.length === 0) {
    const allScripts = doc.querySelectorAll('script:not([src])');
    const imgUrlPattern = /https?:\/\/[^"'\s,]+?\.(?:jpg|jpeg|png|webp)(?:\?[^"'\s,]*)?/gi;
    for (const s of allScripts) {
      const text = s.textContent || '';
      if (text.length < 100 || text.length > 500000) continue;
      const matches = text.match(imgUrlPattern) || [];
      for (const m of matches) {
        const cleaned = m.replace(/\\u002F/g, '/').replace(/\\/g, '');
        if (addImage(cleaned)) break;
      }
      if (images.length >= 10) break;
    }
  }

  // Strategy 4: DOM img elements (original approach, works if JS has already run)
  if (images.length === 0) {
    const imgEls = doc.querySelectorAll('[data-q="gallery-image"] img, .gallery img, picture img, img[data-q]');
    for (const img of imgEls) {
      const src = img.getAttribute('src') || img.getAttribute('data-src') || '';
      if (addImage(src)) break;
    }
  }

  const locationEl = doc.querySelector('[data-q="ad-location"], .ad-location');
  const location = locationEl ? locationEl.textContent.trim() : '';

  const sellerNameEl = doc.querySelector('[data-q="seller-name"], .seller-name');
  const sellerName = sellerNameEl ? sellerNameEl.textContent.trim() : '';

  const memberSinceEl = doc.querySelector('[data-q="seller-member-since"], .seller-since');
  let memberSince = '';
  if (memberSinceEl) {
    const msText = memberSinceEl.textContent.trim();
    const msMatch = msText.match(/(?:since|joined)\s+(.+)/i);
    memberSince = msMatch ? msMatch[1] : msText;
  }

  const dateEl = doc.querySelector('[data-q="ad-posted-date"], time');
  let postedDate = '';
  if (dateEl) {
    postedDate = dateEl.getAttribute('datetime') || dateEl.textContent.trim();
  }

  let condition = '';
  const attrs = [];
  const dtEls = doc.querySelectorAll('dl dt');
  for (const dt of dtEls) {
    const label = dt.textContent.trim();
    const dd = dt.nextElementSibling;
    const value = dd ? dd.textContent.trim() : '';
    if (/condition/i.test(label)) condition = value;
    if (label && value) attrs.push(`${label}: ${value}`);
  }

  if (!title && !price) {
    return { error: 'Could not parse listing detail', hint: 'Gumtree page structure may have changed' };
  }

  return {
    title,
    price,
    description,
    condition,
    images,
    seller: {
      name: sellerName,
      rating: '',
      reviews_count: 0,
      member_since: memberSince,
      location: location
    },
    posted_date: postedDate,
    views: 0,
    platform: 'gumtree',
    source_url: args.url,
    platform_extras: {
      attributes: attrs
    }
  };
}
