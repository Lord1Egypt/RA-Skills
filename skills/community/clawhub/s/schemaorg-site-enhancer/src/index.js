// src/index.js
// Minimal entry point for schemaorg-site-enhancer skill

// Placeholder exports for utility functions (to be implemented)
const utils = {
  generateFAQPage: (data) => {
    // Basic JSON-LD generation for FAQPage
    const jsonLd = {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": data.map(item => ({
        "@type": "Question",
        "name": item.question,
        "acceptedAnswer": {
          "@type": "Answer",
          "text": item.answer
        }
      }))
    };
    return JSON.stringify(jsonLd, null, 2);
  },

  injectJSONLD: (html, jsonLD) => {
    // Simple injection of JSON-LD script into HTML head
    const scriptTag = `<script type="application/ld+json">\n${jsonLD}\n</script>`;
    return html.replace('</head>', `${scriptTag}\n</head>`);
  },

  validateJSONLD: (jsonLDString) => {
    try {
      const parsed = JSON.parse(jsonLDString);
      return !!parsed['@context'] && !!parsed['@type'];
    } catch (e) {
      return false;
    }
  }
};

module.exports = utils;