// formatters/news.mjs

export function render(results) {
  if (!Array.isArray(results) || results.length === 0) {
    console.log("No news articles found for the given criteria.");
    return;
  }

  console.log("\n\x1b[1m\x1b[34m📰 --- Top News Stories ---\x1b[0m\n");

  results.forEach((item, index) => {
    const title = item.title || 'Untitled';
    const url = item.url || 'No URL provided';
    const date = item.publishedDate ? `[\x1b[33m${item.publishedDate}\x1b[0m] ` : "";
    const source = item.source ? ` - \x1b[2m${item.source}\x1b[0m` : "";

    console.log(`\x1b[1m${index + 1}. ${title}\x1b[0m`);
    console.log(`   ${date}Read more at:${source}`);
    console.log(`   \x1b[4m\x1b[36m${url}\x1b[0m`);
    console.log("");
  });
}
