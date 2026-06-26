/* @meta
{
  "name": "amazon/detail",
  "description": "Fetch Amazon product detail page (new, renewed, used items)",
  "domain": "www.amazon.com",
  "args": {
    "url": {"required": true, "description": "Full URL of the Amazon product (e.g. https://www.amazon.com/dp/B0...)"}
  },
  "capabilities": ["detail", "marketplace"],
  "readOnly": true,
  "example": "bb-browser site amazon/detail 'https://www.amazon.com/dp/B0CHX3QBCH'"
}
*/
async function(args) {
  if (!args.url) return { error: 'Missing argument: url' };

  const resp = await fetch(args.url, {
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
      hint: 'The browser session needs to solve a CAPTCHA. Open the Amazon page in Chrome, solve it, then retry.',
    };
  }

  const titleEl = doc.querySelector('#productTitle, #title span');
  const title = titleEl ? titleEl.textContent.trim() : '';

  const priceEl = doc.querySelector('.a-price .a-offscreen, #priceblock_ourprice, .priceToPay .a-offscreen');
  const price = priceEl ? priceEl.textContent.trim() : '';

  // Feature bullets
  const bullets = [];
  const bulletEls = doc.querySelectorAll('#feature-bullets li span, #feature-bullets .a-list-item');
  for (const b of bulletEls) {
    const t = b.textContent.trim();
    if (t && t.length > 5 && !t.includes('Make sure this fits')) {
      bullets.push(t);
    }
  }

  const descEl = doc.querySelector('#productDescription p, #productDescription span');
  const productDesc = descEl ? descEl.textContent.trim() : '';

  const description = bullets.length > 0
    ? bullets.join('\n') + (productDesc ? '\n\n' + productDesc : '')
    : productDesc;

  let condition = '';
  const condBadge = doc.querySelector('.a-badge-text');
  if (condBadge) condition = condBadge.textContent.trim();
  const condNote = doc.querySelector('#renewedProgramDescriptionAtf');
  if (condNote && !condition) condition = condNote.textContent.trim();

  const images = [];
  const seenUrls = new Set();
  const imgEls = doc.querySelectorAll('#imgTagWrapperId img, #altImages img, .imgTagWrapper img');
  for (const img of imgEls) {
    let src = img.getAttribute('data-old-hires') || img.getAttribute('src') || '';
    if (src.includes('._')) {
      src = src.replace(/\._[^.]+\./, '.');
    }
    if (src && src.startsWith('http') && !seenUrls.has(src) && !src.includes('sprite') && !src.includes('grey-pixel')) {
      seenUrls.add(src);
      images.push(src);
      if (images.length >= 10) break;
    }
  }

  const ratingEl = doc.querySelector('#acrPopover [title], .a-icon-alt');
  const rating = ratingEl ? ratingEl.textContent.trim() : '';

  let reviewsCount = 0;
  const reviewEl = doc.querySelector('#acrCustomerReviewText');
  if (reviewEl) {
    const rcMatch = reviewEl.textContent.match(/([\d,]+)/);
    if (rcMatch) reviewsCount = parseInt(rcMatch[1].replace(/,/g, ''));
  }

  const sellerNameEl = doc.querySelector('#sellerProfileTriggerId, #merchant-info a, .tabular-buybox-text a');
  const sellerName = sellerNameEl ? sellerNameEl.textContent.trim() : '';

  let sellerRating = '';
  const sellerRatingEl = doc.querySelector('#seller-rating-count-footer');
  if (sellerRatingEl) {
    const srMatch = sellerRatingEl.textContent.match(/([\d.]+%)/);
    if (srMatch) sellerRating = srMatch[1];
  }

  const primeEl = doc.querySelector('.a-icon-prime, #prime-tag');
  const isPrime = !!primeEl;

  const shippingEl = doc.querySelector('#deliveryBlockMessage .a-text-bold');
  const shipping = shippingEl ? shippingEl.textContent.trim() : '';

  if (!title && !price) {
    return { error: 'Could not parse product detail', hint: 'Amazon page structure may have changed or CAPTCHA required' };
  }

  return {
    title,
    price,
    description,
    condition,
    images,
    seller: {
      name: sellerName || 'Amazon',
      rating: sellerRating,
      reviews_count: reviewsCount,
      member_since: '',
      location: ''
    },
    posted_date: '',
    views: 0,
    platform: 'amazon',
    source_url: args.url,
    platform_extras: {
      product_rating: rating,
      prime: isPrime,
      shipping,
      feature_bullets: bullets
    }
  };
}
