async () => {
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
