function inferColor(text) {
  if (/\b(rose|rosé)\b/i.test(text)) return 'rose';
  if (/\bwhite\b/i.test(text)) return 'white';
  if (/\bred\b/i.test(text)) return 'red';
  if (/\borange\b/i.test(text)) return 'orange';
  if (/\bsparkling\b/i.test(text)) return 'sparkling';
  return null;
}

function inferStyle(text) {
  if (/\b(vino|vinho) verde\b/i.test(text)) return 'vino verde';
  if (/\bsparkling|cava|champagne|prosecco\b/i.test(text)) return 'sparkling';
  if (/\bstill\b/i.test(text)) return 'still';
  if (/\bdessert\b/i.test(text)) return 'dessert';
  if (/\bfortified\b/i.test(text)) return 'fortified';
  return null;
}

function firstMatch(text, regex) {
  const m = text.match(regex);
  return m ? m[1].trim() : null;
}

function normalizeWhitespace(value) {
  return value ? value.replace(/\s+/g, ' ').trim() : value;
}

function titleCaseLoose(value) {
  if (!value) return value;
  return value
    .split(/\s+/)
    .map((part) => (part ? part.charAt(0).toUpperCase() + part.slice(1) : part))
    .join(' ')
    .trim();
}

function normalizeSubjectiveRatingToFive(rawText) {
  const text = rawText || '';

  const starsMatch = text.match(/(\d(?:\.\d+)?)\s*(?:\/\s*5\s*)?stars?\b/i);
  if (starsMatch) {
    return Number(starsMatch[1]);
  }

  const outOfFiveMatch = text.match(/(?:rated|rating|i'?d give it|i give it|score)\s*(?:it)?\s*(\d(?:\.\d+)?)\s*\/\s*5\b/i);
  if (outOfFiveMatch) {
    return Number(outOfFiveMatch[1]);
  }

  const outOfTenMatch = text.match(/(?:rated|rating|i'?d give it|i give it|score)\s*(?:it)?\s*(\d(?:\.\d+)?)\s*\/\s*10\b/i);
  if (outOfTenMatch) {
    return Number((Number(outOfTenMatch[1]) / 2).toFixed(2));
  }

  return null;
}

function parseLabelText(text) {
  const raw = normalizeWhitespace(text || '');
  if (!raw) {
    return {
      source_type: 'image',
      notes: null,
      raw_extraction_json: {
        extractor: 'label-text-v1',
        input: text || '',
      },
    };
  }

  const lines = String(text)
    .split(/\r?\n/)
    .map((line) => normalizeWhitespace(line))
    .filter(Boolean);

  const yearMatch = raw.match(/\b(19\d{2}|20\d{2})\b/);
  const varietalMatch = raw.match(/\b(albariño|albarino|arinto|loureiro|trajadura|pinot noir|cabernet sauvignon|merlot|syrah|shiraz|zinfandel|tempranillo|grenache|garnacha|malbec|sauvignon blanc|chardonnay|riesling|chenin blanc)\b/i);
  const countryMatch = raw.match(/\b(portugal|spain|france|italy|united states|usa|argentina|chile|australia|new zealand|germany|south africa)\b/i);
  const regionMatch = raw.match(/\b(minho|douro|rioja|bourgogne|burgundy|napa valley|sonoma coast|willamette valley|marlborough|mosel|tuscany|piemonte|barossa valley)\b/i);

  let producer = null;
  let wineName = null;
  if (lines.length >= 1) producer = lines[0];
  if (lines.length >= 2) wineName = lines[1];

  if (!wineName && producer) {
    const cleaned = producer.replace(/\b(19\d{2}|20\d{2})\b/g, '').trim();
    if (cleaned.split(/\s+/).length >= 2) {
      wineName = cleaned;
    }
  }

  return {
    source_type: 'image',
    source_text: raw,
    wine_name: titleCaseLoose(wineName),
    producer: titleCaseLoose(producer),
    varietal: varietalMatch ? titleCaseLoose(varietalMatch[1].replace(/albarino/i, 'Albariño')) : null,
    region: regionMatch ? titleCaseLoose(regionMatch[1]) : null,
    country: countryMatch ? titleCaseLoose(countryMatch[1].replace(/^Usa$/i, 'USA')) : null,
    style: inferStyle(raw),
    color: inferColor(raw),
    vintage: yearMatch ? yearMatch[1] : null,
    notes: raw,
    raw_extraction_json: {
      extractor: 'label-text-v1',
      input: text,
      lines,
    },
  };
}

function extractFromText(text) {
  const raw = text || '';
  const cleaned = raw
    .replace(/^\s*(remember|save|log|archive|add)\s+(this\s+)?(wine|bottle)\s*:?\s*/i, '')
    .trim();
  const priceMatch = cleaned.match(/\$\s?(\d+(?:\.\d{1,2})?)/);
  const officialRatingMatch = cleaned.match(/(?:wine spectator|vivino|robert parker|ws)\s*(?:rated|score|gives?)\s*(\d{2,3})/i);
  const yearMatch = cleaned.match(/\b(19\d{2}|20\d{2})\b/);

  const varietalPatterns = [
    /\b(albariño|albarino|arinto|loureiro|trajadura|pinot noir|cabernet sauvignon|merlot|syrah|shiraz|zinfandel|tempranillo|grenache|garnacha|malbec|sauvignon blanc|chardonnay|riesling|chenin blanc)\b/i,
  ];
  let varietal = null;
  for (const pattern of varietalPatterns) {
    const m = cleaned.match(pattern);
    if (m) {
      varietal = m[1];
      break;
    }
  }

  const region = firstMatch(cleaned, /(?:from|region[:\-]?|in)\s+([A-Z][A-Za-zÀ-ÿ'\- ]{2,40}?)(?=\.|,| bought| purchased| rated| for\s+\$|$)/);
  let place_of_purchase = firstMatch(cleaned, /(?:bought at|purchased at)\s+([A-Z][A-Za-z0-9'&.\- ]{2,60}?)(?=\.|,| for\s+\$| rated|$)/);
  if (!place_of_purchase) {
    const storeMatch = cleaned.match(/\b(Nugget|Costco|Trader Joe'?s|BevMo|Total Wine|Whole Foods)\b/i);
    if (storeMatch) place_of_purchase = storeMatch[1];
  }
  const explicitWineName = firstMatch(cleaned, /(?:wine|bottle|label)[:\-]?\s*([A-Z][A-Za-z0-9'&.\- ]{2,80})/);
  const subjective_rating = normalizeSubjectiveRatingToFive(cleaned);
  const official_rating = officialRatingMatch ? Number(officialRatingMatch[1]) : null;
  const inferredWineName = /\b(vino|vinho) verde\b/i.test(cleaned) ? 'Vinho Verde' : null;
  const inferredStyle = inferStyle(cleaned);

  return {
    source_type: 'chat',
    source_text: raw,
    wine_name: explicitWineName || inferredWineName,
    varietal: varietal ? titleCaseLoose(varietal.replace(/albarino/i, 'Albariño')) : null,
    region,
    style: inferredStyle,
    color: inferColor(cleaned),
    vintage: yearMatch ? yearMatch[1] : null,
    price: priceMatch ? Number(priceMatch[1]) : null,
    currency: 'USD',
    place_of_purchase,
    subjective_rating,
    official_rating,
    official_rating_source: official_rating ? 'text_mentioned' : null,
    notes: cleaned,
    raw_extraction_json: {
      extractor: 'heuristic-text-v3',
      input: raw,
      cleaned,
    },
  };
}

module.exports = {
  extractFromText,
  parseLabelText,
  normalizeSubjectiveRatingToFive,
};
