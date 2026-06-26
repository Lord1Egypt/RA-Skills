const unicodeExplorer = {
  toUtf8(str) {
    return unescape(encodeURIComponent(str)).split('').map(c => c.charCodeAt(0));
  },

  fromUtf8(bytes) {
    return decodeURIComponent(escape(String.fromCharCode.apply(null, bytes)));
  },

  toHtmlEntities(str) {
    return str.split('').map(c => {
      const code = c.charCodeAt(0);
      return code > 127 ? `&#${code};` : c;
    }).join('');
  },

  fromHtmlEntities(str) {
    return str.replace(/&#(\d+);/g, (match, code) => String.fromCharCode(code));
  },

  getCharInfo(char) {
    const code = char.charCodeAt(0);
    return {
      character: char,
      codePoint: code,
      hex: 'U+' + code.toString(16).toUpperCase().padStart(4, '0'),
      utf8: this.toUtf8(char),
      htmlEntity: this.toHtmlEntities(char)
    };
  },

  searchEmojis(keyword) {
    const emojis = {
      'smile': '😀', 'heart': '❤️', 'thumbsup': '👍', 'star': '⭐',
      'fire': '🔥', 'rocket': '🚀', 'lightbulb': '💡', 'check': '✅',
      'warning': '⚠️', 'error': '❌', 'info': 'ℹ️', 'question': '❓',
      'happy': '😊', 'sad': '😢', 'cool': '😎', 'love': '😍',
      'thinking': '🤔', 'wave': '👋', 'clap': '👏', 'pray': '🙏',
      'sun': '☀️', 'moon': '🌙', 'rainbow': '🌈', 'flower': '🌸'
    };

    const results = [];
    const lowerKeyword = keyword.toLowerCase();
    for (const [name, emoji] of Object.entries(emojis)) {
      if (name.includes(lowerKeyword) || emoji.includes(keyword)) {
        results.push({ name, emoji, ...this.getCharInfo(emoji) });
      }
    }
    return results;
  },

  getMathSymbols() {
    const symbols = ['∑', '∫', '∂', '√', '∞', '≠', '≤', '≥', '±', '×', '÷', '≈', '≡', '∈', '∉', '⊂', '⊃', '∪', '∩', '∀', '∃'];
    return symbols.map(s => ({ symbol: s, ...this.getCharInfo(s) }));
  },

  getArrows() {
    const arrows = ['←', '→', '↑', '↓', '↔', '↕', '⇐', '⇒', '⇑', '⇓', '↖', '↗', '↘', '↙'];
    return arrows.map(a => ({ arrow: a, ...this.getCharInfo(a) }));
  },

  getCurrencySymbols() {
    const currencies = [
      { symbol: '$', name: 'Dollar' },
      { symbol: '€', name: 'Euro' },
      { symbol: '£', name: 'Pound' },
      { symbol: '¥', name: 'Yen' },
      { symbol: '₹', name: 'Rupee' },
      { symbol: '₩', name: 'Won' },
      { symbol: '₿', name: 'Bitcoin' },
      { symbol: 'Ξ', name: 'Ether' }
    ];
    return currencies.map(c => ({ ...c, ...this.getCharInfo(c.symbol) }));
  }
};

export default unicodeExplorer;
