export function sanitizeFileName(name) {
  return String(name || '未命名书籍').replace(/[《》]/g, '').replace(/[\\/:*?"<>|]/g, ' ').replace(/\s+/g, ' ').trim();
}

export function cleanText(text) {
  return String(text || '').replace(/\u200b/g, '').replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/\r\n/g, '\n').replace(/\r/g, '\n').replace(/\n{3,}/g, '\n\n').trim();
}

export function yamlScalar(value) {
  const text = String(value ?? '');
  return JSON.stringify(text);
}

export function reviewPayload(item) {
  return item?.review || item || {};
}
