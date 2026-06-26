/**
 * Web Search - StackOverflow and GitHub search
 */

// StackExchange API (no key needed for basic search)
const STACKOVERFLOW_API = 'https://api.stackexchange.com/2.3/search/advanced';

export async function searchWeb(parsed) {
  const results = [];
  
  // Build query from intent + keywords
  const query = [
    ...parsed.intents,
    ...parsed.languages.slice(0, 2),
    ...parsed.keywords.slice(0, 3)
  ].join(' ');
  
  if (!query.trim()) return results;

  try {
    // Search StackOverflow
    const soParams = new URLSearchParams({
      order: 'desc',
      sort: 'relevance',
      q: query,
      site: 'stackoverflow',
      answers: 'true',
      filter: '!nNPvSNVZJS'
    });
    
    const soResponse = await fetch(`${STACKOVERFLOW_API}?${soParams}`);
    const soData = await soResponse.json();
    
    if (soData.items) {
      for (const item of soData.items.slice(0, 5)) {
        results.push({
          type: 'stackoverflow',
          title: item.title,
          url: item.link,
          score: item.score,
          answerCount: item.answer_count,
          tags: item.tags,
          isAnswered: item.is_answered,
          relevance: item.score > 10 ? 'high' : item.score > 3 ? 'medium' : 'low'
        });
      }
    }
  } catch (error) {
    console.error('StackOverflow search failed:', error.message);
  }

  // Could add GitHub search here too
  
  return results;
}