/**
 * Sitemap API — Edge Function
 *
 * Phase 3 L2-1 实现
 *
 * GET /api/sitemap.xml
 * 返回：XML Sitemap
 *
 * EdgeOne Pages 缓存：5 分钟 TTL
 */

/**
 * Generate XML Sitemap from URL entries
 * @param {Array<{loc:string, changefreq?:string, priority?:string, lastmod?:string}>} urls
 * @returns {string} XML sitemap string
 */
function generateSitemapXml(urls) {
  const urlElements = urls.map(u => {
    let xml = `  <url><loc>${u.loc}</loc>`;
    if (u.lastmod) xml += `\n    <lastmod>${u.lastmod}</lastmod>`;
    if (u.changefreq) xml += `\n    <changefreq>${u.changefreq}</changefreq>`;
    if (u.priority) xml += `\n    <priority>${u.priority}</priority>`;
    xml += '</url>';
    return xml;
  }).join('\n');
  return `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urlElements}</urlset>`;
}

export async function onRequest(context) {
  const { env } = context;
  const baseUrl = env.SITE_URL || 'https://example.com';

  try {
    const cacheKey = 'sitemap:products';
    const cached = await env.KV.get(cacheKey);

    let productUrls = [];
    if (cached) {
      productUrls = JSON.parse(cached);
    }

    const staticUrls = [
      { loc: `${baseUrl}/`, changefreq: 'daily', priority: '1.0' },
      { loc: `${baseUrl}/login`, changefreq: 'monthly', priority: '0.3' },
      { loc: `${baseUrl}/register`, changefreq: 'monthly', priority: '0.3' },
      { loc: `${baseUrl}/cart`, changefreq: 'weekly', priority: '0.5' },
      { loc: `${baseUrl}/orders`, changefreq: 'weekly', priority: '0.5' },
    ];

    const productPageUrls = productUrls.map(p => ({
      loc: `${baseUrl}/products/${p.id}`,
      lastmod: p.updated_at || p.created_at,
      changefreq: 'weekly',
      priority: '0.8'
    }));

    const allUrls = [...staticUrls, ...productPageUrls];
    const xml = generateSitemapXml(allUrls);

    return new Response(xml, {
      status: 200,
      headers: {
        'Content-Type': 'application/xml; charset=utf-8',
        'Cache-Control': 'public, max-age=300, stale-while-revalidate=600'
      }
    });
  } catch (err) {
    console.error('[Sitemap] Error:', err);
    return new Response('<?xml version="1.0"?><urlset/>', {
      status: 200,
      headers: { 'Content-Type': 'application/xml' }
    });
  }
}
