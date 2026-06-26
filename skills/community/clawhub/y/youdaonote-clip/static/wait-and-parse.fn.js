/**
 * wait-and-parse.fn.js — 合并等待 SDK 挂载 + 解析内容
 *
 * 将原来的 2 个步骤（wait + parse）合并为 1 个 evaluate 调用：
 *   - 等待 SDK 挂载（轮询 collectParser）
 *   - 解析页面内容
 *
 * 预期：减少 1 次进程启动，节省 100-200ms
 */
async () => {
  // === Step 4a: 等待 SDK 挂载（带超时，从 10s 降到 8s）===
  const MAX_WAIT_MS = 8000;
  const POLL_INTERVAL_MS = 50;
  const startTime = Date.now();

  while (typeof window.collectParser === 'undefined') {
    if (Date.now() - startTime > MAX_WAIT_MS) {
      throw new Error('SDK 挂载超时');
    }
    await new Promise(r => setTimeout(r, POLL_INTERVAL_MS));
  }

  // === Step 4b: 解析内容 ===
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
