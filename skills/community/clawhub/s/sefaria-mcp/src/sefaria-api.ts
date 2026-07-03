/**
 * Sefaria API wrapper
 * https://www.sefaria.org/developers
 */

const BASE_URL = "https://www.sefaria.org/api";
const USER_AGENT = "SefariaMCP/1.0";

interface ApiResponse {
  error?: string;
  [key: string]: unknown;
}

async function apiRequest(
  endpoint: string,
  options: {
    params?: Record<string, string>;
    method?: "GET" | "POST";
    body?: Record<string, unknown>;
  } = {}
): Promise<ApiResponse> {
  const { params, method = "GET", body } = options;
  
  let url = `${BASE_URL}/${endpoint}`;
  if (params && method === "GET") {
    url += "?" + new URLSearchParams(params).toString();
  }

  try {
    const fetchOptions: RequestInit = {
      method,
      headers: {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
      },
    };

    if (body) {
      fetchOptions.headers = {
        ...fetchOptions.headers,
        "Content-Type": "application/json",
      };
      fetchOptions.body = JSON.stringify(body);
    }

    const response = await fetch(url, fetchOptions);
    
    if (!response.ok) {
      return { error: `HTTP ${response.status}: ${response.statusText}` };
    }
    
    return await response.json();
  } catch (error) {
    return { error: `Request failed: ${error instanceof Error ? error.message : String(error)}` };
  }
}

function stripHtml(text: string): string {
  return text.replace(/<[^>]+>/g, "").replace(/\s+/g, " ").trim();
}

function normalizeRef(ref: string): string {
  // Convert "Genesis 1:1" to "Genesis.1.1" for URL
  return ref.replace(/:/g, ".").replace(/ /g, "_");
}

export interface TextResult {
  ref: string;
  hebrew: string;
  english: string;
  book: string;
  categories: string[];
  error?: string;
}

export async function getText(ref: string, withContext = false): Promise<TextResult> {
  const normalizedRef = normalizeRef(ref);
  const encodedRef = encodeURIComponent(normalizedRef);
  
  const params: Record<string, string> = {};
  if (withContext) params.context = "1";
  
  const data = await apiRequest(`texts/${encodedRef}`, { params: Object.keys(params).length ? params : undefined });
  
  if (data.error) {
    return {
      ref,
      hebrew: "",
      english: "",
      book: "",
      categories: [],
      error: data.error,
    };
  }

  // Process Hebrew text
  let hebrewText = "";
  const he = data.he;
  if (Array.isArray(he)) {
    hebrewText = he
      .map((v, i) => `${i + 1}. ${stripHtml(String(v))}`)
      .join("\n");
  } else if (typeof he === "string") {
    hebrewText = stripHtml(he);
  }

  // Process English text
  let englishText = "";
  const en = data.text;
  if (Array.isArray(en)) {
    englishText = en
      .map((v, i) => `${i + 1}. ${stripHtml(String(v))}`)
      .join("\n");
  } else if (typeof en === "string") {
    englishText = stripHtml(en);
  }

  return {
    ref: String(data.ref || ref),
    hebrew: hebrewText,
    english: englishText,
    book: String(data.book || ""),
    categories: Array.isArray(data.categories) ? data.categories.map(String) : [],
  };
}

export interface SearchHit {
  ref: string;
  snippet: string;
  category: string;
}

export interface SearchResult {
  query: string;
  total: number;
  hits: SearchHit[];
  error?: string;
}

export async function search(query: string, limit = 10, filters?: { book?: string }): Promise<SearchResult> {
  const body: Record<string, unknown> = {
    query,
    size: limit,
    type: "text",
    field: "naive_lemmatizer",
    sort_type: "relevance",
  };

  if (filters?.book) {
    body.filters = [filters.book];
  }

  const data = await apiRequest("search-wrapper/es6", { method: "POST", body });

  if (data.error) {
    return { query, total: 0, hits: [], error: data.error };
  }

  const hits = (data.hits as { hits?: unknown[]; total?: number })?.hits || [];
  const total = (data.hits as { total?: number })?.total || 0;

  const results: SearchHit[] = [];
  for (const hit of hits as Array<{ _id?: string; highlight?: Record<string, string[]>; _source?: { categories?: string[] } }>) {
    const refId = hit._id || "Unknown";
    const ref = refId.includes(" (") ? refId.split(" (")[0] : refId;
    
    const highlight = hit.highlight || {};
    const snippets = highlight.naive_lemmatizer || highlight.exact || [];
    const snippet = snippets.length > 0
      ? stripHtml(snippets[0].replace(/<b>/g, "**").replace(/<\/b>/g, "**"))
      : "";
    
    const categories = hit._source?.categories || [];
    
    results.push({
      ref,
      snippet,
      category: categories[0] || "Unknown",
    });
  }

  return { query, total, hits: results };
}

export interface Link {
  ref: string;
  category: string;
  text: string;
}

export interface LinksResult {
  ref: string;
  links: Link[];
  byCategory: Record<string, Link[]>;
  error?: string;
}

export async function getLinks(ref: string): Promise<LinksResult> {
  const encodedRef = encodeURIComponent(ref.replace(/ /g, "_"));
  const data = await apiRequest(`links/${encodedRef}`);

  if (data.error || !Array.isArray(data)) {
    return {
      ref,
      links: [],
      byCategory: {},
      error: data.error || "No links found",
    };
  }

  const links: Link[] = [];
  const byCategory: Record<string, Link[]> = {};

  for (const link of data as Array<{ ref?: string; category?: string; he?: string; text?: string }>) {
    const linkRef = link.ref || "Unknown";
    const category = link.category || "Other";
    const text = stripHtml(String(link.he || link.text || "")).slice(0, 200);

    const linkObj: Link = { ref: linkRef, category, text };
    links.push(linkObj);

    if (!byCategory[category]) byCategory[category] = [];
    byCategory[category].push(linkObj);
  }

  return { ref, links, byCategory };
}

export interface RelatedResult {
  ref: string;
  topics: string[];
  sheets: Array<{ title: string; id: number }>;
  error?: string;
}

export async function getRelated(ref: string): Promise<RelatedResult> {
  const encodedRef = encodeURIComponent(ref.replace(/ /g, "_"));
  const data = await apiRequest(`related/${encodedRef}`);

  if (data.error) {
    return { ref, topics: [], sheets: [], error: data.error };
  }

  const topics: string[] = [];
  const topicsData = data.topics;
  if (Array.isArray(topicsData)) {
    for (const t of topicsData as Array<{ topic?: string; slug?: string }>) {
      if (t.topic || t.slug) {
        topics.push(String(t.topic || t.slug));
      }
    }
  }

  const sheets: Array<{ title: string; id: number }> = [];
  const sheetsData = data.sheets;
  if (Array.isArray(sheetsData)) {
    for (const s of sheetsData.slice(0, 5) as Array<{ title?: string; id?: number }>) {
      if (s.title && s.id) {
        sheets.push({ title: String(s.title), id: Number(s.id) });
      }
    }
  }

  return { ref, topics, sheets };
}

export interface CalendarItem {
  name: string;
  ref: string;
  hebrew: string;
}

export interface CalendarsResult {
  items: CalendarItem[];
  error?: string;
}

export async function getCalendars(): Promise<CalendarsResult> {
  const data = await apiRequest("calendars");

  if (data.error) {
    return { items: [], error: data.error };
  }

  const items: CalendarItem[] = [];
  const calendarItems = data.calendar_items;
  
  if (Array.isArray(calendarItems)) {
    for (const item of calendarItems as Array<{
      title?: { en?: string };
      displayValue?: { en?: string; he?: string };
      ref?: string;
    }>) {
      items.push({
        name: item.title?.en || "Unknown",
        ref: item.ref || item.displayValue?.en || "",
        hebrew: item.displayValue?.he || "",
      });
    }
  }

  return { items };
}

export interface ParshaResult {
  name: string;
  ref: string;
  hebrew: string;
  error?: string;
}

export async function getParsha(): Promise<ParshaResult> {
  const calendars = await getCalendars();
  
  if (calendars.error) {
    return { name: "", ref: "", hebrew: "", error: calendars.error };
  }

  for (const item of calendars.items) {
    if (item.name === "Parashat Hashavua") {
      return {
        name: item.ref,
        ref: item.ref,
        hebrew: item.hebrew,
      };
    }
  }

  return { name: "", ref: "", hebrew: "", error: "Parsha not found" };
}

export interface BookInfo {
  title: string;
  heTitle: string;
  categories: string[];
  structure: string;
  length: number;
  error?: string;
}

export async function getBookInfo(title: string): Promise<BookInfo> {
  const encodedTitle = encodeURIComponent(title.replace(/ /g, "_"));
  const data = await apiRequest(`v2/index/${encodedTitle}`);

  if (data.error) {
    return {
      title,
      heTitle: "",
      categories: [],
      structure: "",
      length: 0,
      error: data.error,
    };
  }

  const schema = data.schema as { sectionNames?: string[] } | undefined;
  
  return {
    title: String(data.title || title),
    heTitle: String(data.heTitle || ""),
    categories: Array.isArray(data.categories) ? data.categories.map(String) : [],
    structure: String(schema?.sectionNames?.join(" > ") || ""),
    length: Number(data.length || 0),
  };
}
