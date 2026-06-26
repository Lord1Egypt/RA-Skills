/* Star Search PWA - Service Worker v20.12
 * 离线缓存 + 网络优先策略 + 静态资源预缓存
 * 重要: 每次发版必须更新 CACHE_NAME (例如 star-search-v20.12.0 -> v20.13.0)
 *        让浏览器立即拉新资源
 */
const CACHE_NAME = 'star-search-v20.12.0';
const PRECACHE_URLS = [
  '/',
  '/index.html',
  '/manifest.json',
  '/icon.svg',
  '/icon-192.png',
  '/icon-512.png',
];

// ===== 安装: 预缓存静态资源 =====
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[SW] 预缓存:', PRECACHE_URLS);
        return cache.addAll(PRECACHE_URLS);
      })
      .then(() => self.skipWaiting())
  );
});

// ===== 激活: 清理旧缓存 =====
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames
            .filter((name) => name !== CACHE_NAME)
            .map((name) => {
              console.log('[SW] 清理旧缓存:', name);
              return caches.delete(name);
            })
        );
      })
      .then(() => self.clients.claim())
  );
});

// ===== Fetch: 网络优先 + 离线 fallback =====
self.addEventListener('fetch', (event) => {
  const { request } = event;

  // 跳过非 GET 请求
  if (request.method !== 'GET') return;

  // API 请求不缓存 (实时数据)
  if (request.url.includes('/v1/') || request.url.includes('/mcp/')) {
    return;
  }

  // SSE 流不缓存
  if (request.url.includes('/stream')) {
    return;
  }

  event.respondWith(
    fetch(request)
      .then((response) => {
        // 成功响应: 克隆并缓存 (HTML/CSS/JS/images)
        if (response && response.status === 200 && response.type === 'basic') {
          const responseClone = response.clone();
          caches.open(CACHE_NAME)
            .then((cache) => cache.put(request, responseClone));
        }
        return response;
      })
      .catch(() => {
        // 网络失败: 走缓存
        return caches.match(request)
          .then((cached) => {
            if (cached) {
              console.log('[SW] 离线 fallback:', request.url);
              return cached;
            }
            // 页面请求: 返 index.html
            if (request.mode === 'navigate') {
              return caches.match('/index.html');
            }
            return new Response('Offline', { status: 503 });
          });
      })
  );
});
