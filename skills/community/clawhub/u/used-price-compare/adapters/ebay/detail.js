/* @meta
{
  "name": "ebay/detail",
  "description": "Fetch eBay listing detail page (any eBay domain: .com, .co.uk, .com.au, .ca)",
  "domain": "ebay.com",
  "args": {
    "url": {"required": true, "description": "Full URL of the eBay listing (e.g. https://www.ebay.com/itm/...)"}
  },
  "capabilities": ["detail", "marketplace"],
  "readOnly": true,
  "example": "bb-browser site ebay/detail 'https://www.ebay.com/itm/123456789'"
}
*/
async function(args) {
  if (!args.url) return { error: 'Missing argument: url' };

  const resp = await fetch(args.url, { credentials: 'include' });
  if (!resp.ok) return { error: `HTTP ${resp.status}`, hint: 'Check if the listing URL is valid' };

  const html = await resp.text();
  const parser = new DOMParser();
  const doc = parser.parseFromString(html, 'text/html');

  // Title
  const titleEl = doc.querySelector('.x-item-title__mainTitle span, h1.x-item-title span, #itemTitle');
  let title = titleEl ? titleEl.textContent.trim() : '';
  title = title.replace(/^Details about\s*/i, '').trim();

  // Price
  const priceEl = doc.querySelector('.x-price-primary span, #prcIsum, [itemprop="price"]');
  const price = priceEl ? priceEl.textContent.trim() : '';

  // Condition
  const condEl = doc.querySelector('.x-item-condition-text span, #vi-itm-cond');
  const condition = condEl ? condEl.textContent.trim() : '';

  // Description — eBay uses an iframe; grab meta + item specifics instead
  let description = '';
  const descMeta = doc.querySelector('meta[name="description"]');
  if (descMeta) {
    description = descMeta.getAttribute('content') || '';
  }

  const specifics = [];
  const labelEls = doc.querySelectorAll('.ux-labels-values--labels span.ux-textspans');
  const valueEls = doc.querySelectorAll('.ux-labels-values--values span.ux-textspans');
  const len = Math.min(labelEls.length, valueEls.length);
  for (let i = 0; i < len; i++) {
    const label = labelEls[i].textContent.trim();
    const value = valueEls[i].textContent.trim();
    if (label && value) specifics.push(`${label}: ${value}`);
  }
  if (specifics.length > 0) {
    description = (description ? description + '\n\n' : '') + 'Item Specifics:\n' + specifics.join('\n');
  }

  // Images
  const images = [];
  const seenUrls = new Set();
  const imgEls = doc.querySelectorAll('.ux-image-carousel-item img, #icImg, [data-testid="ux-image-magnify"] img');
  for (const img of imgEls) {
    const src = img.getAttribute('src') || img.getAttribute('data-src') || '';
    if (src && src.startsWith('http') && !seenUrls.has(src)) {
      seenUrls.add(src);
      images.push(src);
      if (images.length >= 10) break;
    }
  }

  // Seller info
  const sellerNameEl = doc.querySelector('.x-sellercard-atf__info__about-seller a span, a[data-testid="str-seller-name"] span');
  const sellerName = sellerNameEl ? sellerNameEl.textContent.trim() : '';

  let sellerRating = '';
  let reviewsCount = 0;
  const feedbackEls = doc.querySelectorAll('.x-sellercard-atf__data-item span, .x-sellercard-atf__info__about-seller .ux-textspans--SECONDARY');
  for (const el of feedbackEls) {
    const t = el.textContent.trim();
    const pctMatch = t.match(/([\d.]+)%/);
    if (pctMatch && !sellerRating) sellerRating = pctMatch[0];
    const countMatch = t.match(/([\d,.]+[Kk]?)\s*(?:feedback|ratings|reviews)/i);
    if (countMatch && !reviewsCount) {
      const raw = countMatch[1].replace(/,/g, '');
      reviewsCount = raw.toLowerCase().endsWith('k') ? parseFloat(raw) * 1000 : parseInt(raw);
    }
  }

  const sellerLocationEl = doc.querySelector('.ux-seller-section__item--location span, [data-testid="str-seller-location"] span');
  const sellerLocation = sellerLocationEl ? sellerLocationEl.textContent.trim().replace(/^Located in:\s*/i, '') : '';

  let memberSince = '';
  for (const el of feedbackEls) {
    const msMatch = el.textContent.match(/Member since\s+(\w+[\s-]*\d{4}|\d{4})/i);
    if (msMatch) { memberSince = msMatch[1]; break; }
  }

  // Shipping
  const shippingEl = doc.querySelector('#fshippingCost span, .ux-labels-values--shipping .ux-textspans');
  const shipping = shippingEl ? shippingEl.textContent.trim() : '';

  // Returns
  const returnsEl = doc.querySelector('.ux-labels-values--returns .ux-textspans');
  const returns = returnsEl ? returnsEl.textContent.trim() : '';

  if (!title && !price) {
    return { error: 'Could not parse listing detail', hint: 'eBay page structure may have changed' };
  }

  return {
    title,
    price,
    description,
    condition,
    images,
    seller: {
      name: sellerName,
      rating: sellerRating,
      reviews_count: reviewsCount,
      member_since: memberSince,
      location: sellerLocation
    },
    posted_date: '',
    views: 0,
    platform: 'ebay',
    source_url: args.url,
    platform_extras: {
      shipping,
      returns,
      item_specifics: specifics
    }
  };
}
