/* @meta
{
  "name": "ok/detail",
  "description": "Fetch OK.com listing detail page (second-hand marketplace item)",
  "domain": "ok.com",
  "args": {
    "url": {"required": true, "description": "Full URL of the OK.com listing detail page"}
  },
  "capabilities": ["detail", "marketplace"],
  "readOnly": true,
  "example": "bb-browser site ok/detail 'https://us.ok.com/en/item/12345'"
}
*/
async function(args) {
  if (!args.url) return { error: 'Missing argument: url' };

  const resp = await fetch(args.url, { credentials: 'include' });
  if (!resp.ok) return { error: `HTTP ${resp.status}`, hint: 'Check if the listing URL is valid' };

  const html = await resp.text();

  const text = html
    .replace(/&quot;/g, '"')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>');

  const titleMatch = text.match(/"title"\s*:\s*"([^"]{3,200})"/);
  const title = titleMatch ? titleMatch[1] : '';

  const priceMatch = text.match(/"price"\s*:\s*"([^"]+)"/);
  const price = priceMatch ? priceMatch[1] : '';

  let description = '';
  const descMatch = text.match(/"description"\s*:\s*"([^"]{1,5000})"/);
  if (descMatch) {
    description = descMatch[1].replace(/\\n/g, '\n').replace(/\\"/g, '"');
  }
  if (!description) {
    const bodyMatch = text.match(/"body"\s*:\s*"([^"]{1,5000})"/);
    if (bodyMatch) {
      description = bodyMatch[1].replace(/\\n/g, '\n').replace(/\\"/g, '"');
    }
  }

  const condMatch = text.match(/"condition"\s*:\s*"([^"]+)"/);
  const condition = condMatch ? condMatch[1] : '';

  const images = [];
  const imgPattern = /"(https?:\/\/[^"]+\.(?:jpg|jpeg|png|webp)[^"]*)"/gi;
  let imgMatch;
  const seenUrls = new Set();
  while ((imgMatch = imgPattern.exec(text)) !== null) {
    const imgUrl = imgMatch[1];
    if (!seenUrls.has(imgUrl) && !imgUrl.includes('avatar') && !imgUrl.includes('logo') && !imgUrl.includes('icon')) {
      seenUrls.add(imgUrl);
      images.push(imgUrl);
      if (images.length >= 10) break;
    }
  }

  const sellerNameMatch = text.match(/"sellerName"\s*:\s*"([^"]+)"/) ||
                          text.match(/"seller"\s*:\s*\{[^}]*"name"\s*:\s*"([^"]+)"/);
  const sellerName = sellerNameMatch ? sellerNameMatch[1] : '';

  const sellerLocationMatch = text.match(/"sellerLocation"\s*:\s*"([^"]+)"/) ||
                              text.match(/"location"\s*:\s*"([^"]+)"/);
  const sellerLocation = sellerLocationMatch ? sellerLocationMatch[1] : '';

  const memberSinceMatch = text.match(/"memberSince"\s*:\s*"([^"]+)"/) ||
                           text.match(/"joinDate"\s*:\s*"([^"]+)"/) ||
                           text.match(/"createdAt"\s*:\s*"([^"]+)"/);
  const memberSince = memberSinceMatch ? memberSinceMatch[1] : '';

  const postDateMatch = text.match(/"postedDate"\s*:\s*"([^"]+)"/) ||
                        text.match(/"createdAt"\s*:\s*"([^"]+)"/) ||
                        text.match(/"publishDate"\s*:\s*"([^"]+)"/);
  const postedDate = postDateMatch ? postDateMatch[1] : '';

  const viewsMatch = text.match(/"views"\s*:\s*(\d+)/) ||
                     text.match(/"viewCount"\s*:\s*(\d+)/);
  const views = viewsMatch ? parseInt(viewsMatch[1]) : 0;

  if (!title && !price) {
    return { error: 'Could not parse listing detail', hint: 'Page structure may have changed' };
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
      location: sellerLocation
    },
    posted_date: postedDate,
    views,
    platform: 'ok.com',
    source_url: args.url,
    platform_extras: {}
  };
}
