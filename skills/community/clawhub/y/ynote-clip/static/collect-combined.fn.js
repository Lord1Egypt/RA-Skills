/**
 * collect-combined.fn.js — 合并注入 SDK + 等待挂载 + 解析内容
 *
 * 将原来的 3 个步骤合并为 1 个 evaluate 调用：
 *   - 注入 SDK（从 base64 解码）
 *   - 等待 SDK 挂载（轮询 collectParser）
 *   - 解析页面内容
 *
 * 预期：减少 2 次进程启动，节省 200-400ms
 */
async () => {
  // === Step 1: 注入 SDK（base64 编码的 collect-window.js）===
  // SDK 代码由构建脚本预先生成，存储在全局变量中
  const SDK_BASE64 = $SDK_BASE64_PLACEHOLDER$;

  if (typeof window.collectParser === 'undefined') {
    const script = document.createElement('script');
    script.textContent = atob(SDK_BASE64);
    (document.head || document.documentElement).appendChild(script);
    script.remove(); // 注入后立即移除，保持 DOM 干净
  }

  // === Step 2: 等待 SDK 挂载（带超时）===
  const MAX_WAIT_MS = 8000;  // 从 10s 降到 8s
  const POLL_INTERVAL_MS = 50;
  const startTime = Date.now();

  while (typeof window.collectParser === 'undefined') {
    if (Date.now() - startTime > MAX_WAIT_MS) {
      throw new Error('SDK 挂载超时');
    }
    await new Promise(r => setTimeout(r, POLL_INTERVAL_MS));
  }

  // === Step 3: 解析内容 ===
  const r = await window.collectParser.parse();
  const div = document.createElement('div');
  div.innerHTML = r.content;
  const imgs = div.querySelectorAll('img');
  const imageUrls = Array.from(imgs)
    .map(img => img.getAttribute('src'))
    .filter(src => src && !src.startsWith('data:'))
    .map(src => {
      try { return new URL(src, document.baseURI).href; }
      catch(e) { return null; }
    })
    .filter(Boolean);

  return {
    title: r.title || document.title,
    content: r.content,
    source: r.source,
    imageUrls: [...new Set(imageUrls)]
  };
}
