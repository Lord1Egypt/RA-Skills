// formatters/default.mjs

export function render(results) {
  if (!Array.isArray(results) || results.length === 0) {
    console.log("No results found.");
    return;
  }

  console.log("\n\x1b[1m\x1b[35m=== General Search Results ===\x1b[0m\n");

  results.forEach((item, index) => {
    const title = item.title || 'Untitled';
    const url = item.url || 'No URL provided';
    const snippet = item.content ? item.content.substring(0, 150).replace(/\n/g, ' ') + '...' : '';

    console.log(`\x1b[1m${index + 1}. ${title}\x1b[0m`);
    console.log(`\x1b[32m   ${url}\x1b[0m`);
    if (snippet) {
      console.log(`   ${snippet}`);
    }
    console.log(""); 
  });
}