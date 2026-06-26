#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");
const MarkdownIt = require("markdown-it");
const hljs = require("highlight.js");

const CODE_THEME_COLORS = {
  "hljs-keyword": "color: #c678dd;",
  "hljs-string": "color: #98c379;",
  "hljs-number": "color: #d19a66;",
  "hljs-comment": "color: #5c6370; font-style: italic;",
  "hljs-function": "",
  "hljs-params": "",
  "hljs-built_in": "color: #e6c07b;",
  "hljs-literal": "color: #56b6c2;",
  "hljs-attr": "color: #d19a66;",
  "hljs-attribute": "color: #98c379;",
  "hljs-title": "color: #61afef;",
  "hljs-tag": "color: #569cd6;",
  "hljs-name": "color: #e06c75;",
  "hljs-selector-tag": "color: #e06c75;",
  "hljs-selector-class": "color: #d19a66;",
  "hljs-selector-id": "color: #61afef;",
  "hljs-variable": "color: #e06c75;",
  "hljs-template-variable": "color: #e06c75;",
  "hljs-type": "color: #e6c07b;",
  "hljs-class": "color: #e6c07b;",
  "hljs-meta": "color: #61afef;",
  "hljs-decoration": "color: #d19a66;",
  "hljs-emphasis": "font-style: italic;",
  "hljs-strong": "font-weight: bold;",
};

const CODE_BASE_STYLE = "overflow-x: auto; padding: 16px; color: #abb2bf; background: #282c34; display: -webkit-box; font-family: Operator Mono, Consolas, Monaco, Menlo, monospace; border-radius: 0px; font-size: 12px; -webkit-overflow-scrolling: touch;";

function highlightCode(code, lang) {
  // markdown-it adds a trailing newline to code blocks, remove it
  if (code.endsWith('\n')) {
    code = code.slice(0, -1);
  }

  let highlighted;
  if (lang && hljs.getLanguage(lang)) {
    highlighted = hljs.highlight(code, { language: lang }).value;
  } else {
    // No language specified - escape as plain text to avoid incorrect auto-highlighting of URLs
    highlighted = code
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
  }

  // Remove &#x27; encoding and convert to regular quotes
  highlighted = highlighted.replace(/&#x27;/g, "'");

  let processed = highlighted;

  // Remove hljs-built_in class (used for built-in functions like print) - make plain
  processed = processed.replace(/<span class="hljs-built_in">([^<]*)<\/span>/gi, '$1');

  // Transform def(a): pattern into function wrapper with params
  // Pattern: keyword def + (possibly some text) + (params):
  processed = processed.replace(
    /(<span class="hljs-keyword"[^>]*>def<\/span>)\(([^)]*)\):/gi,
    '<span class="hljs-function" style="line-height: 26px;">$1<span class="hljs-params" style="line-height: 26px;">($2)</span>:</span>'
  );

  // Process the remaining highlighted HTML to add inline styles
  processed = processed.replace(/<span class="([^"]+)">([^<]*)<\/span>/gi, (match, classes, content) => {
    classes = classes.replace(/language-/g, '');

    const classList = classes.split(' ').filter(c => c && c.startsWith('hljs-'));
    let inlineStyle = 'line-height: 26px;';
    let firstClass = '';

    for (const cls of classList) {
      firstClass = cls;
      if (CODE_THEME_COLORS[cls]) {
        inlineStyle = CODE_THEME_COLORS[cls] + ' line-height: 26px;';
        break;
      }
    }

    return `<span class="${firstClass}" style="${inlineStyle}">${content}</span>`;
  });

  // Split lines and join with <br>
  let lines = processed.split('\n');

  // Remove trailing empty lines (markdown-it adds a trailing newline to code blocks)
  while (lines.length > 0 && lines[lines.length - 1].trim() === '') {
    lines.pop();
  }

  // Collapse consecutive empty lines into single separator
  const result = [];
  let lastWasEmpty = false;
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (line.trim() === '') {
      if (!lastWasEmpty) {
        result.push('');  // Empty string for blank line
        lastWasEmpty = true;
      }
    } else {
      // Replace all spaces with &nbsp; for proper rendering in WeChat
      const processedLine = line.replace(/ /g, '&nbsp;');
      result.push(processedLine);
      lastWasEmpty = false;
    }
  }

  // Add trailing empty string for trailing <br>
  result.push('');

  // Join with <br> - empty strings become just <br>
  return result.join('<br>');
}

const FONT_THEMES = {
  serif: "font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;",
  sans: "font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;"
};

const INLINE_STYLES = {
  section: "font-size: 16px; color: black; padding: 0 10px; line-height: 1.6; word-spacing: 0px; letter-spacing: 0px; word-wrap: break-word; text-align: left;",
  p: "font-size: 16px; padding-top: 8px; padding-bottom: 8px; margin: 0; line-height: 26px; color: #666;",
  h1: "margin-top: 30px; margin-bottom: 15px; padding: 0px; color: black; font-size: 1.7em; font-weight: normal; border-bottom: 2px solid hsl(216, 100%, 68%);",
  h2: "margin-top: 30px; margin-bottom: 15px; padding: 0px; font-weight: normal; color: #333; font-size: 1.4em; border-bottom: 1px solid hsl(216, 100%, 68%);",
  h3: "margin-top: 25px; margin-bottom: 12px; padding: 0px; font-weight: normal; color: #333; font-size: 1.2em;",
  h4: "margin-top: 20px; margin-bottom: 10px; padding: 0px; font-weight: normal; color: #333; font-size: 1.1em;",
  h5: "margin-top: 18px; margin-bottom: 8px; padding: 0px; font-weight: normal; color: #333; font-size: 1em;",
  h6: "margin-top: 16px; margin-bottom: 6px; padding: 0px; font-weight: normal; color: #666; font-size: 0.9em;",
  img: "max-width: 100%; border-radius: 8px; display: block; margin: 0 auto;",
  blockquote: "display: block; font-size: 0.9em; overflow: auto; overflow-scrolling: touch; border-left: 3px solid rgba(0, 0, 0, 0.4); color: #6a737d; padding-top: 10px; padding-bottom: 10px; padding-left: 20px; padding-right: 10px; margin-bottom: 20px; margin-top: 20px; background: #f9f9f9; border-left-color: hsl(216, 100%, 68%);",
  ul: "margin-top: 8px; margin-bottom: 8px; color: black; list-style-type: disc; padding-left: 2em;",
  ol: "margin-top: 8px; margin-bottom: 8px; color: black; list-style-type: decimal; padding-left: 2em;",
  li: "color: #666;",
  liSection: "margin-top: 5px; margin-bottom: 5px; line-height: 26px; text-align: left; color: rgb(1,1,1); font-weight: 500;",
  table: "border-collapse: collapse; width: 100%; margin: 0.9em 0; font-size: 14px; display: table;",
  th: "border: 1px solid #d9d9d9; padding: 8px 10px; text-align: left; background: #f5f5f5; font-weight: bold;",
  td: "border: 1px solid #d9d9d9; padding: 8px 10px; text-align: left;",
  hr: "height: 1px; margin-top: 10px; margin-bottom: 10px; border: none; width: 90%; margin: 1.5em auto; border-top: 2px dashed hsl(216, 100%, 68%);",
  pre: "margin-top: 10px; margin-bottom: 10px;",
  code: "overflow-x: auto; padding: 16px; color: #abb2bf; background: #282c34; display: -webkit-box; font-family: Operator Mono, Consolas, Monaco, Menlo, monospace; border-radius: 0px; font-size: 12px; -webkit-overflow-scrolling: touch; line-height: 26px;",
  inlineCode: "font-size: 14px; word-wrap: break-word; padding: 2px 4px; border-radius: 4px; margin: 0 2px; background-color: rgba(27,31,35,.05); font-family: Operator Mono, Consolas, Monaco, Menlo, monospace; word-break: break-all; color: hsl(216, 100%, 68%);",
  a: "color: #1565c0; text-decoration: none;",
  strong: "font-weight: bold; color: hsl(216, 80%, 44%);",
  em: "font-style: italic;",
  del: "text-decoration: line-through;",
};

function applyInlineStyles(html) {
  const dataTool = 'data-tool="mdnice编辑器"';

  let result = html;

  // Handle h1 with span structure (highlighted background style)
  result = result.replace(/<h1([^>]*)>([\s\S]*?)<\/h1>/gi, (match, attrs, content) => {
    const style = INLINE_STYLES.h1;
    const cleanContent = content.replace(/<\/?span[^>]*>/gi, '');
    return `<h1 ${dataTool} style="${style}"><span class="prefix" style="display: none;"></span><span class="content" style="background: hsl(216, 100%, 68%); color: white; padding: 3px 10px; border-top-right-radius: 3px; border-top-left-radius: 3px; margin-right: 3px;">${cleanContent}</span><span class="suffix"></span></h1>`;
  });

  // Handle h2 with span structure
  result = result.replace(/<h2([^>]*)>([\s\S]*?)<\/h2>/gi, (match, attrs, content) => {
    const style = INLINE_STYLES.h2;
    const cleanContent = content.replace(/<\/?span[^>]*>/gi, '');
    return `<h2 ${dataTool} style="${style}"><span class="prefix" style="display: none;"></span><span class="content" style="border-bottom: 1px solid hsl(216, 100%, 68%);">${cleanContent}</span><span class="suffix"></span></h2>`;
  });

  // Handle h3-h6
  for (const tag of ['h3', 'h4', 'h5', 'h6']) {
    const regex = new RegExp(`<${tag}([^>]*)>([\\s\\S]*?)<\\/${tag}>`, "gi");
    result = result.replace(regex, (match, attrs, content) => {
      const style = INLINE_STYLES[tag];
      return `<${tag} ${dataTool} style="${style}">${content}</${tag}>`;
    });
  }

  // Protect pre blocks before processing p tags
  const prePlaceholders = [];
  result = result.replace(/<pre[\s\S]*?<\/pre>/gi, (match) => {
    const idx = prePlaceholders.length;
    prePlaceholders.push(match);
    return '__PREBLOCK_' + idx + '__';
  });

  // Handle p - now safe since pre blocks are protected
  result = result.replace(/<p([^>]*)>([\s\S]*?)<\/p>/gi, (match, attrs, content) => {
    if (attrs.includes('data-tool=')) return match;
    const style = INLINE_STYLES.p;
    return `<p ${dataTool} style="${style}">${content}</p>`;
  });

  // Restore pre blocks
  result = result.replace(/__PREBLOCK_(\d+)__/g, (_, idx) => prePlaceholders[parseInt(idx)]);

  // Handle hr
  result = result.replace(/<hr([^>]*)>/gi, (match, attrs) => {
    if (match.includes('data-tool=')) return match;
    const style = INLINE_STYLES.hr;
    return `<hr ${dataTool} style="${style}">`;
  });

  // Handle ul with list-style-type
  result = result.replace(/<ul([^>]*)>/gi, (match, attrs) => {
    const style = INLINE_STYLES.ul;
    if (attrs.includes('data-tool=')) return match;
    return `<ul ${dataTool} style="${style}">`;
  });

  // Handle ol with list-style-type
  result = result.replace(/<ol([^>]*)>/gi, (match, attrs) => {
    const style = INLINE_STYLES.ol;
    if (attrs.includes('data-tool=')) return match;
    return `<ol ${dataTool} style="${style}">`;
  });

  // Handle li with section wrapper - produce compact output (no newlines between li items)
  // The issue: regex ([\\s\\S]*?)</li> stops at FIRST </li> which breaks nested lists.
  // Solution: Use a function-based approach to process all li elements correctly.

  const style = INLINE_STYLES.li;
  const liSectionStyle = INLINE_STYLES.liSection;

  // Helper function to find matching closing tag for an opening tag
  // Uses a simple stack-based approach to handle nested tags correctly
  function findMatchingCloseTag(content, startIndex) {
    let tagName = '';
    let i = startIndex + 1;
    while (i < content.length && /\w/.test(content[i])) {
      tagName += content[i];
      i++;
    }
    tagName = tagName.toLowerCase();
    if (!tagName) return -1;

    while (i < content.length && content[i] !== '>') {
      i++;
    }
    if (i >= content.length) return -1;
    i++;

    let depth = 1;
    while (i < content.length && depth > 0) {
      if (content[i] === '<' && content[i + 1] !== '/') {
        const nextChar = content[i + 1];
        if (nextChar === '!' || nextChar === '?') {
          i++;
          continue;
        }
        let j = i + 1;
        let name = '';
        while (j < content.length && /\w/.test(content[j])) {
          name += content[j];
          j++;
        }
        name = name.toLowerCase();
        if (name === tagName) {
          depth++;
        }
        i++;
      } else if (content[i] === '<' && content[i + 1] === '/') {
        let j = i + 2;
        let name = '';
        while (j < content.length && /\w/.test(content[j])) {
          name += content[j];
          j++;
        }
        name = name.toLowerCase();
        if (name === tagName) {
          depth--;
          if (depth === 0) {
            while (j < content.length && content[j] !== '>') {
              j++;
            }
            return j + 1; // Return position PAST the > (consistent with how opening tag is handled)
          }
        }
        i++;
      } else {
        i++;
      }
    }
    return -1;
  }

  // Process all li elements by finding their proper closing tags
  // Use a global replace that finds <li> tags and their matching </li> tags
  // Skip nested li elements that are inside already-processed li elements
  function processAllLi(html) {
    const liOpenRegex = /<li([^>]*)>/gi;
    let result = '';
    let lastIndex = 0;
    let match;
    let skipUntil = -1; // Skip any <li> found before this position

    while ((match = liOpenRegex.exec(html)) !== null) {
      const openTagStart = match.index;
      const openTagEnd = liOpenRegex.lastIndex;
      const attrs = match[1];

      // Skip this <li> if it's inside a previously processed <li>
      if (openTagStart < skipUntil) {
        continue;
      }

      // Find the matching </li> using proper tag matching
      const closeIndex = findMatchingCloseTag(html, openTagStart);

      if (closeIndex !== -1) {
        // Extract content between <li...> and </li> (closeIndex is position AFTER >)
        // Include the closing </li> tag in rawContent so we can strip it with regex
        const rawContent = html.substring(openTagEnd, closeIndex);
        // Strip trailing </li> tag that markdown-it includes in the content
        const content = rawContent.replace(/\s*<\/li>\s*$/, '').trim();

        // Process this li element
        const processed = processLiContent(attrs, content);
        result += html.substring(lastIndex, openTagStart) + processed;
        lastIndex = closeIndex + 1;
        skipUntil = closeIndex + 1; // Skip any li inside this li
      } else {
        // No matching close tag found, keep as is
        result += html.substring(lastIndex, openTagStart) + match[0];
        lastIndex = openTagEnd;
      }
    }
    result += html.substring(lastIndex);
    return result;
  }

  function processLiContent(attrs, content) {
    const hasNestedList = /<ul[\s>]/i.test(content) || /<ol[\s>]/i.test(content);

    if (hasNestedList) {
      // Find the nested ul/ol tag
      const nestedListMatch = content.match(/<(ul|ol)[\s>]/i);
      if (nestedListMatch) {
        const nestedListTag = nestedListMatch[1].toLowerCase();
        const nestedListStartIndex = content.indexOf("<" + nestedListTag);
        const nestedListEndIndex = findMatchingCloseTag(content, nestedListStartIndex);

        if (nestedListEndIndex !== -1) {
          // Get the full nested list including wrapper tags
          const fullNestedList = content.substring(nestedListStartIndex, nestedListEndIndex + 1);
          const beforeNested = content.substring(0, nestedListStartIndex);
          const afterNested = content.substring(nestedListEndIndex + 1);

          const cleanBefore = beforeNested.replace(/<\/?section[^>]*>/gi, '').trim();
          let cleanAfter = afterNested.replace(/<\/?section[^>]*>/gi, '').trim();
          if (cleanAfter.startsWith('</') || cleanAfter.startsWith('<')) {
            cleanAfter = '';
          }

          // Process nested list items properly using processAllLi
          let processedNestedList = processAllLi(fullNestedList);

          let res = `<li${attrs} style="${style}"><section style="${liSectionStyle}">`;
          res += cleanBefore;
          if (cleanBefore) {
            res += '\n';
          }
          res += processedNestedList;
          res += `</section></li>`;
          return res;
        }
      }
    }

    // Simple li - no nested lists
    const cleanContent = content.replace(/<\/?section[^>]*>/gi, '');
    return `<li${attrs} style="${style}"><section style="${liSectionStyle}">${cleanContent}</section></li>`;
  }

  result = processAllLi(result);

  // === WeChat MP editor quirks: list normalization ===
  // Verified empirically on the MP draft editor (June 2026). The MP editor's HTML
  // ingester deviates from spec in two ways that destroy ordered/unordered lists:
  //
  // 1. <li><section>...</section></li> renders WITHOUT the list marker
  //    (numbers / bullets disappear) AND adds an extra blank row per item — the
  //    inner block element seems to take the marker slot from the <li>.
  //    Fix: for SIMPLE leaf li (no nested list inside), unwrap the <section>
  //    and merge its typographic styles onto the <li> directly. Skip li that
  //    contain a nested <ul>/<ol> — there the section wrapper helps with the
  //    sub-list layout, and marker rendering for that case is a separate issue.
  //
  // 2. Whitespace TEXT NODES between sibling <li> tags (and at the start/end
  //    of <ol>/<ul>) are interpreted as additional EMPTY <li> items, producing
  //    numbered/bulleted blank rows interleaved with real items. The previous
  //    compaction only stripped \n; spaces and tabs leaked through and were
  //    enough to trigger the bug.
  //    Fix: zero out ALL whitespace at the <ol>/<ul> ↔ <li> boundaries and
  //    between consecutive <li> siblings.
  result = result.replace(
    /<li([^>]*)>\s*<section\s+style="([^"]+)"\s*>([\s\S]*?)<\/section>\s*<\/li>/gi,
    (match, liAttrs, secStyle, inner) => {
      // Keep the section wrapper when the li contains a nested list — flattening
      // there would collapse the sub-list onto the parent's marker line.
      if (/<(?:ul|ol)\b/i.test(inner)) return match;
      const merged = secStyle
        .replace(/\s*margin-(?:top|bottom)\s*:\s*[^;]+;?/gi, '')
        .replace(/\s{2,}/g, ' ')
        .trim()
        .replace(/^;\s*|\s*;\s*$/g, '');
      // Strip any pre-existing style on the <li>; the section's typographic
      // styles (color / font-weight / line-height) supersede them anyway, and
      // emitting two style attributes lets the browser keep only the first one.
      const cleanLiAttrs = liAttrs.replace(/\s*style\s*=\s*"[^"]*"/gi, '');
      return `<li${cleanLiAttrs} style="${merged}">${inner.trim()}</li>`;
    }
  );
  result = result.replace(/(<(?:ol|ul)\b[^>]*>)\s+(<li\b)/gi, '$1$2');
  result = result.replace(/(<\/li>)\s+(<li\b)/gi, '$1$2');
  result = result.replace(/(<\/li>)\s+(<\/(?:ol|ul)>)/gi, '$1$2');

  // Handle inline code (not inside pre blocks or table cells) - add styled inline code
  // Strategy: temporarily replace code tags in table cells, then style remaining code tags
  const tableCodeReplacements = [];

  // Replace code tags in td/th with placeholders
  result = result.replace(/<t[dh][^>]*>[\s\S]*?<\/t[dh]>/gi, (tableCell) => {
    const protectedCell = tableCell.replace(/<code([^>]*)>([\s\S]*?)<\/code>/gi, (match, attrs, content) => {
      const idx = tableCodeReplacements.length;
      tableCodeReplacements.push(match);
      return `__TABLE_CODE_${idx}__`;
    });
    return protectedCell;
  });

  // Protect pre blocks
  const codePlaceholders = [];
  result = result.replace(/(<pre[^>]*>[\s\S]*?<\/pre>)/gi, (match) => {
    const idx = codePlaceholders.length;
    codePlaceholders.push(match);
    return `__PRE_PLACEHOLDER_${idx}__`;
  });

  // Style remaining code tags (inline code in paragraphs)
  result = result.replace(/<code([^>]*)>([\s\S]*?)<\/code>/gi, (match, attrs, content) => {
    if (attrs.includes('data-tool=')) return match;
    const style = INLINE_STYLES.inlineCode;
    return `<code${attrs} style="${style}">${content}</code>`;
  });

  // Restore pre blocks
  result = result.replace(/__PRE_PLACEHOLDER_(\d+)__/g, (match, idx) => codePlaceholders[parseInt(idx)]);

  // Restore table cell code tags
  result = result.replace(/__TABLE_CODE_(\d+)__/g, (match, idx) => tableCodeReplacements[parseInt(idx)]);

  // Handle strong - NO data-tool attribute for strong
  result = result.replace(/<strong([^>]*)>([\s\S]*?)<\/strong>/gi, (match, attrs, content) => {
    const style = INLINE_STYLES.strong;
    return `<strong${attrs} style="${style}">${content}</strong>`;
  });

  // Handle blockquote
  result = result.replace(/<blockquote([^>]*)>([\s\S]*?)<\/blockquote>/gi, (match, attrs, content) => {
    const style = INLINE_STYLES.blockquote;
    // Handle p inside blockquote with special style
    const blockquotePStyle = "font-size: 16px; padding-top: 8px; padding-bottom: 8px; margin: 0px; line-height: 26px; color: #999; padding: 3px 0;";
    const processedContent = content.replace(/<p([^>]*)>([\s\S]*?)<\/p>/gi, (pMatch, pAttrs, pContent) => {
      return `<p${pAttrs} style="${blockquotePStyle}">${pContent}</p>`;
    });
    return `<blockquote ${dataTool} style="${style}">${processedContent}</blockquote>`;
  });

  // Handle pre - ensure class attribute comes before data-tool
  result = result.replace(/<pre([^>]*)>([\s\S]*?)<\/pre>/gi, (match, attrs, content) => {
    if (match.includes('data-tool=')) return match;
    const style = INLINE_STYLES.pre;
    // Extract class attribute if present and place it first
    const classMatch = attrs.match(/class="[^"]*"/);
    const classAttr = classMatch ? classMatch[0] : '';
    const otherAttrs = attrs.replace(/class="[^"]*"/, '').trim();
    if (classAttr) {
      return `<pre ${classAttr} ${dataTool}${otherAttrs} style="${style}">${content}</pre>`;
    }
    return `<pre ${dataTool}${attrs} style="${style}">${content}</pre>`;
  });

  // Handle a
  result = result.replace(/<a([^>]*)>([\s\S]*?)<\/a>/gi, (match, attrs, content) => {
    if (match.includes('data-tool=')) return match;
    const style = INLINE_STYLES.a;
    return `<a ${dataTool}${attrs} style="${style}">${content}</a>`;
  });

  // Handle img
  result = result.replace(/<img([^>]*)>/gi, (match, attrs) => {
    if (match.includes('data-tool=')) return match;
    const style = INLINE_STYLES.img;
    return `<img ${dataTool}${attrs} style="${style}">`;
  });

  // Handle table: wrap in section container, style thead/tbody/tr/th/td all within the table block
  result = result.replace(/<table([^>]*)>([\s\S]*?)<\/table>/gi, (match, attrs, content) => {
    if (attrs.includes('data-tool=')) return match;  // only skip if <table> itself has data-tool
    const tableStyle = "display: table; text-align: left; margin: 1.5em auto; width: auto;";
    const thStyle = "font-size: 16px; border: 1px solid #ccc; padding: 5px 10px; text-align: left; background-color: #f0f0f0; color: #333; font-weight: normal; min-width: 85px;";
    const tdStyle = "font-size: 16px; border: 1px solid #ccc; padding: 5px 10px; text-align: left; color: #666; min-width: 85px;";

    // Style thead
    let processedContent = content.replace(/<thead([^>]*)>([\s\S]*?)<\/thead>/gi, (m, a, c) => {
      const styledC = c
        .replace(/<tr([^>]*)>/gi, '<tr style="border: 0; border-top: 1px solid #ccc; background-color: white;">')
        .replace(/<th([^>]*)>([\s\S]*?)<\/th>/gi, (tm, ta, tc) => `<th style="${thStyle}">${tc}</th>`);
      return `<thead>${styledC}</thead>`;
    });

    // Style tbody with zebra rows
    let rowIndex = 0;
    processedContent = processedContent.replace(/<tbody([^>]*)>([\s\S]*?)<\/tbody>/gi, (m, a, c) => {
      const styledC = c
        .replace(/<tr([^>]*)>/gi, () => {
          const bg = rowIndex++ % 2 === 0 ? 'white' : '#F8F8F8';
          return `<tr style="border: 0; border-top: 1px solid #ccc; background-color: ${bg};">`;
        })
        .replace(/<td([^>]*)>([\s\S]*?)<\/td>/gi, (tm, ta, tc) => `<td style="${tdStyle}">${tc}</td>`);
      return `<tbody style="border: 0;">${styledC}</tbody>`;
    });

    return `<section class="table-container" ${dataTool} style="overflow-x: auto;"><table style="${tableStyle}">${processedContent}</table>\n</section>`;
  });

  return result;
}

function usage() {
  console.log(
    [
      "Usage:",
      "  node scripts/render-markdown-html.js --input in.md --output out.html [options]",
      "",
      "Options:",
      "  --text-theme normal|orange-heart|geek-black|minimal-dark",
      "  --font serif|sans",
      "  --website <url>        (optional, shown in data-website attribute)"
    ].join("\n")
  );
}

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith("--")) continue;
    const key = token.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith("--")) {
      args[key] = true;
    } else {
      args[key] = next;
      i += 1;
    }
  }
  return args;
}

function readFileSafe(filePath, label) {
  try {
    return fs.readFileSync(filePath, "utf8");
  } catch (error) {
    throw new Error(`${label} file not found: ${filePath}`);
  }
}

function buildHtmlFragment({ rendered, fontTheme, website }) {
  const fontStyle = FONT_THEMES[fontTheme] || FONT_THEMES.serif;

  return `<section id="nice" data-tool="markdown2wechat编辑器" data-website="${website}" style="${INLINE_STYLES.section} ${fontStyle} word-break: break-all;">${rendered}</section>`;
}

function getTextThemeColors(theme) {
  const colors = {
    "normal": "color: #F5F7FA; background: #1E4976;",
    "orange-heart": "color: #FF6B35; background: #5C1A1A;",
    "geek-black": "color: #00FF41; background: #0A0A0A;",
    "minimal-dark": "color: #E5E7EB; background: #111827;",
    "gold-sea": "color: #e7c249; background: #0A2540;",
  };
  return colors[theme] || colors.normal;
}

function main() {
  const args = parseArgs(process.argv);
  if (args.help || !args.input || !args.output) {
    usage();
    process.exit(args.help ? 0 : 1);
  }

  const inputPath = path.resolve(args.input);
  const outputPath = path.resolve(args.output);
  const textTheme = args["text-theme"] || "normal";
  const codeTheme = args["code-theme"] || "wechat";
  const fontTheme = args.font || "serif";
  const website = args.website || "";

  const markdown = readFileSafe(inputPath, "input markdown");

  const md = new MarkdownIt({
    html: true,
    linkify: false,
    typographer: false,
    highlight(code, lang) {
      const highlighted = highlightCode(code, lang);
      return `<pre class="custom"><code class="hljs" style="${CODE_BASE_STYLE}">${highlighted}</code></pre>`;
    }
  });

  const rendered = applyInlineStyles(md.render(markdown));
  let html = buildHtmlFragment({
    rendered,
    fontTheme,
    website
  });

  // Decode HTML entities back to original characters for proper rendering
  html = html.replace(/&quot;/g, '"');

  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, html, "utf8");
  console.log(`Rendered HTML saved to: ${outputPath}`);
}

main();
