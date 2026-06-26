/**
 * Text Processor Skill
 * Chinese text cleaning, normalization, and batch processing.
 */

/**
 * Clean and normalize Chinese/English mixed text
 */
function clean(text) {
  if (typeof text !== 'string') return '';
  
  return text
    .trim()
    .replace(/\s+/g, ' ')
    // Normalize full-width to half-width for ASCII chars
    .replace(/[\uff01-\uff5e]/g, ch => String.fromCharCode(ch.charCodeAt(0) - 0xfee0))
    // Normalize quotes
    .replace(/[\u201c\u201d\u300c\u300d\u300e\u300f\u00ab\u00bb]/g, '"')
    .replace(/[\u2018\u2019\u300a\u300b]/g, "'")
    // Normalize Chinese punctuation spacing
    .replace(/([.,!?;:，。！？；：、])/g, '$1 ')
    .replace(/\s+([，。！？；：、])/g, '$1')
    .trim();
}

/**
 * Extract Chinese keywords using simple frequency-based approach
 */
function extractKeywords(text, maxCount = 10) {
  if (!text) return [];
  
  // Simple Chinese word segmentation: extract 2-4 char segments as candidate keywords
  const candidates = {};
  const cleaned = text.replace(/[^\u4e00-\u9fff\w]/g, ' ');
  
  // Extract bigrams and trigrams
  const chars = cleaned.replace(/\s+/g, '');
  for (let i = 0; i < chars.length - 1; i++) {
    for (let len = 2; len <= 4 && i + len <= chars.length; len++) {
      const word = chars.substring(i, i + len);
      if (word.length >= 2 && /^[\u4e00-\u9fff]+$/.test(word)) {
        candidates[word] = (candidates[word] || 0) + 1;
      }
    }
  }
  
  return Object.entries(candidates)
    .sort((a, b) => b[1] - a[1])
    .slice(0, maxCount)
    .map(([word]) => word);
}

/**
 * Batch process multiple texts
 */
function batch(items, operation = 'clean', options = {}) {
  if (!Array.isArray(items)) items = [items];
  
  return items.map(item => {
    switch (operation) {
      case 'clean':
        return clean(item);
      case 'keywords':
        return extractKeywords(item, options.maxCount);
      default:
        return item;
    }
  });
}

module.exports = { clean, extractKeywords, batch };
