const path = require('path');
const {
  insertWineEntry,
  updateWineEntry,
  findRecentWineEntryByImagePath,
  recallWineEntries,
  recallWineCatalog,
  summarizeWine,
  queryWineEntries,
} = require('./wine-store');
const { extractFromText, parseLabelText } = require('./wine-extractor');
const { classifyWineIntentWithLlm } = require('./wine-llm');

function normalizeText(value) {
  return String(value || '').trim();
}

function cleanTelegramEnvelope(text = '') {
  return normalizeText(text)
    .replace(/^\[media attached:[^\n]*\]\n?/i, '')
    .replace(/To send an image back,[\s\S]*?Keep caption in the text body\.\n?/i, '')
    .replace(/Conversation info \(untrusted metadata\):[\s\S]*?```\n?/gi, '')
    .replace(/Sender \(untrusted metadata\):[\s\S]*?```\n?/gi, '')
    .replace(/<media:image>/gi, '')
    .replace(/```json[\s\S]*?```/gi, '')
    .replace(/```[\s\S]*?```/gi, '')
    .replace(/\s+/g, ' ')
    .trim();
}

function classifyWineIntent(text = '', { hasImage = false } = {}) {
  const raw = cleanTelegramEnvelope(text);
  const lower = raw.toLowerCase();

  if (!raw && hasImage) return 'remember';
  if (!raw) return 'unknown';
  if (hasImage && /\b(remember|save|log|archive|add|this|it|bottle|wine|vino verde|vintag|origin|from|got it at|stars?)\b/.test(lower)) return 'remember';
  if (/\b(show|send)\b/.test(lower) && /\b(label|image|photo|picture)\b/.test(lower)) return 'show-label';
  if (/\b(show me|show|display|tell me about|what about)\b/.test(lower) && /\bwine\b/.test(lower)) return 'show-wine';
  if (/\b(show|tell me about|what about)\b/.test(lower) && /\b(vino verde|pinot|cabernet|merlot|riesling|santa|serea|serẽa|gloria|azevedo|bleue|brut)\b/.test(lower)) return 'show-wine';
  if (/\b(remember|save|log|archive|add|insert|update)\b/.test(lower) && /\b(wine|bottle|drank|had|bought|label|vino verde)\b/.test(lower)) return 'remember';
  if (/\b(what|which|find|show|recall|list)\b/.test(lower) && /\b(wine|wines|bottle|bottles|drank|drink|tried|try|had|bought|buy|vino verde|pinot|cabernet|merlot|riesling|nugget|costco|last week|last month|yesterday|today|last night)\b/.test(lower)) return 'recall';
  if (hasImage || (/\b(label|ocr|image|photo|picture)\b/.test(lower) && /\b(wine|bottle)\b/.test(lower))) return 'label';
  return 'unknown';
}

async function classifyWineIntentOptionalLlm(text = '', options = {}) {
  const fallback = classifyWineIntent(text, options);
  if (!process.env.WINE_LLM_INTENT_CLASSIFIER || process.env.WINE_LLM_INTENT_CLASSIFIER === '0') {
    return { intent: fallback, source: 'regex', confidence: 1 };
  }

  try {
    const result = await (options.classifyWithLlm || classifyWineIntentWithLlm)(text, options);
    if (result.confidence >= Number(process.env.WINE_LLM_INTENT_MIN_CONFIDENCE || 0.65)) {
      return { intent: result.intent, source: 'llm', confidence: result.confidence, reason: result.reason };
    }
  } catch {
    // fall through to regex path
  }

  return { intent: fallback, source: 'regex-fallback', confidence: 1 };
}

function today(referenceDate = null) {
  if (referenceDate) return new Date(referenceDate).toISOString().slice(0, 10);
  return new Date().toISOString().slice(0, 10);
}

function shiftDate(baseIso, days) {
  const date = new Date(`${baseIso}T12:00:00Z`);
  date.setUTCDate(date.getUTCDate() + days);
  return date.toISOString().slice(0, 10);
}

function monthWindow(baseIso, deltaMonths = 0) {
  const date = new Date(`${baseIso}T12:00:00Z`);
  date.setUTCMonth(date.getUTCMonth() + deltaMonths, 1);
  const start = date.toISOString().slice(0, 10);
  const next = new Date(`${start}T12:00:00Z`);
  next.setUTCMonth(next.getUTCMonth() + 1, 1);
  next.setUTCDate(next.getUTCDate() - 1);
  return { start, end: next.toISOString().slice(0, 10) };
}

function parseNaturalDateQuery(text, { referenceDate = null } = {}) {
  const raw = cleanTelegramEnvelope(text);
  const lower = raw.toLowerCase();
  const criteria = {};
  const now = today(referenceDate);

  if (/\b(last week)\b/.test(lower)) {
    criteria.consumed_after = shiftDate(now, -7);
    criteria.consumed_before = now;
  }
  if (/\b(this week)\b/.test(lower)) {
    criteria.consumed_after = shiftDate(now, -6);
    criteria.consumed_before = now;
  }
  if (/\b(yesterday)\b/.test(lower)) {
    const day = shiftDate(now, -1);
    criteria.consumed_after = day;
    criteria.consumed_before = day;
  }
  if (/\b(last night)\b/.test(lower)) {
    const day = shiftDate(now, -1);
    criteria.consumed_after = day;
    criteria.consumed_before = day;
  }
  if (/\b(today)\b/.test(lower)) {
    criteria.consumed_after = now;
    criteria.consumed_before = now;
  }
  if (/\b(last month)\b/.test(lower)) {
    const window = monthWindow(now, -1);
    criteria.consumed_after = window.start;
    criteria.consumed_before = window.end;
  }
  if (/\b(this month)\b/.test(lower)) {
    const window = monthWindow(now, 0);
    criteria.consumed_after = window.start;
    criteria.consumed_before = window.end;
  }

  const ratingMatch = raw.match(/\b(?:rated|rating)\s*(?:at least|>=|above)?\s*(\d(?:\.\d+)?)\b/i);
  if (ratingMatch) criteria.min_subjective_rating = Number(ratingMatch[1]);

  const matchedTerms = [];
  const fieldPatterns = {
    varietal: /\b(pinot noir|cabernet sauvignon|merlot|syrah|shiraz|zinfandel|tempranillo|grenache|garnacha|malbec|sauvignon blanc|chardonnay|riesling|chenin blanc|albariño|albarino|loureiro|arinto|trajadura)\b/i,
    style: /\b(vino verde|sparkling|dessert|fortified|still)\b/i,
    color: /\b(red|white|rose|rosé|orange)\b/i,
    region: /\b(minho|douro|rioja|burgundy|bourgogne|napa valley|sonoma coast|willamette valley|marlborough|mosel|tuscany|piemonte|barossa valley)\b/i,
    place_of_purchase: /\b(nugget|costco|safeway|trader joe'?s|bevmo|total wine|whole foods)\b/i,
  };

  for (const [field, pattern] of Object.entries(fieldPatterns)) {
    const m = raw.match(pattern);
    if (m) {
      criteria[field] = m[1];
      matchedTerms.push(m[1].toLowerCase());
    }
  }

  let sanitizedText = lower
    .replace(/\b(show|find|recall|what|which|wines|wine|did|do|i|have|had|drank|drink|bought|buy|tried|try|from|that|were|was|the|a|an|me|my|entries|at)\b/g, ' ')
    .replace(/\b(last week|this week|yesterday|today|last month|this month|last night)\b/g, ' ')
    .replace(/\b(rated|rating)\s*(?:at least|>=|above)?\s*\d(?:\.\d+)?\b/gi, ' ');

  for (const term of matchedTerms) {
    const escaped = term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    sanitizedText = sanitizedText.replace(new RegExp(`\\b${escaped}\\b`, 'gi'), ' ');
  }

  sanitizedText = sanitizedText.replace(/[?!.]+/g, ' ').replace(/\s+/g, ' ').trim();
  if (sanitizedText) criteria.text = sanitizedText;
  return criteria;
}

function maybeInferEntryDatesFromText(text, entry, { referenceDate = null } = {}) {
  const raw = cleanTelegramEnvelope(text);
  if (entry.purchased_on || entry.consumed_on) return entry;
  if (/\blast week\b/i.test(raw)) entry.consumed_on = shiftDate(today(referenceDate), -7);
  else if (/\byesterday\b/i.test(raw)) entry.consumed_on = shiftDate(today(referenceDate), -1);
  else if (/\btoday\b/i.test(raw)) entry.consumed_on = today(referenceDate);
  return entry;
}

function detectTextOnlyUpdate(text = '') {
  const raw = cleanTelegramEnvelope(text);
  if (!raw) return false;
  return /\b(update|include|insert it|set|change)\b/i.test(raw) || /\b(origin|portugal|name|description|notes?)\b/i.test(raw);
}

function buildPatchFromText(text) {
  const raw = cleanTelegramEnvelope(text);
  const extracted = extractFromText(raw);
  const patch = {};

  if (/\b(?:name|include the name|called)\b/i.test(raw)) {
    const m = raw.match(/(?:name\s+|name\s+["“']?|called\s+["“']?|include the name\s+["“']?)([^"”'.,\n]+)["”']?/i);
    if (m) patch.wine_name = m[1].trim();
  }
  if (/\borigin\b/i.test(raw) || /\bfrom portugal\b/i.test(raw)) {
    const m = raw.match(/(?:origin\s+|from\s+)(Portugal|Spain|France|Italy|USA|United States|Argentina|Chile|Australia|New Zealand|Germany|South Africa)\b/i);
    if (m) patch.country = m[1];
  }
  if (/\bdescription\b/i.test(raw) || /\bnotes?\b/i.test(raw) || /\bliked it\b/i.test(raw)) {
    patch.notes = raw
      .replace(/^.*?(?:description|notes?)\s*[:\-]?\s*/i, '')
      .trim() || extracted.notes || raw;
  }

  for (const field of ['wine_name', 'country', 'style', 'vintage', 'place_of_purchase']) {
    if (!patch[field] && extracted[field]) patch[field] = extracted[field];
  }
  if (patch.subjective_rating == null && extracted.subjective_rating != null) patch.subjective_rating = extracted.subjective_rating;

  return patch;
}

function rememberWineFromText(text, extras = {}) {
  const cleaned = cleanTelegramEnvelope(text);
  let entry = extractFromText(cleaned);
  entry = maybeInferEntryDatesFromText(cleaned, entry, extras);
  entry = {
    ...entry,
    ...extras,
    source_text: extras.source_text || cleaned || entry.source_text,
    source_type: extras.source_type || entry.source_type || 'chat',
  };
  const created = insertWineEntry(entry);
  return {
    ok: true,
    action: 'remember',
    entry: created,
    reply: `Saved wine instance: ${summarizeWine(created) || 'wine entry stored.'}`,
  };
}

function rememberWineFromLabel({ labelText, imagePath, text = '', extras = {} }) {
  const cleanedText = cleanTelegramEnvelope(text);
  const parsedLabel = labelText ? parseLabelText(labelText) : {};
  const textExtracted = cleanedText ? extractFromText(cleanedText) : {};
  let entry = {
    ...parsedLabel,
    ...textExtracted,
    ...extras,
    source_image_path: imagePath ? path.resolve(imagePath) : null,
    source_text: cleanedText || textExtracted.source_text || parsedLabel.source_text || null,
    source_type: 'image',
  };
  entry = maybeInferEntryDatesFromText(cleanedText, entry, extras);

  const existing = imagePath ? findRecentWineEntryByImagePath(path.resolve(imagePath)) : null;
  if (existing) {
    const updated = updateWineEntry(existing.id, {
      ...existing,
      ...entry,
      source_type: 'image',
      source_image_path: path.resolve(imagePath),
    });
    return {
      ok: true,
      action: 'update-label',
      entry: updated,
      reply: `Updated wine entry: ${summarizeWine(updated) || 'wine entry stored.'}`,
    };
  }

  const created = insertWineEntry(entry);
  return {
    ok: true,
    action: 'remember-label',
    entry: created,
    reply: `Saved label-derived wine instance: ${summarizeWine(created) || 'wine entry stored.'}`,
  };
}

function updateRecentWineFromText(text, { imagePath } = {}) {
  const resolvedImagePath = imagePath ? path.resolve(imagePath) : null;
  const existing = resolvedImagePath ? findRecentWineEntryByImagePath(resolvedImagePath) : null;
  if (!existing) return rememberWineFromText(text, imagePath ? { source_image_path: resolvedImagePath, source_type: 'image' } : {});

  const patch = buildPatchFromText(text);
  const mergedNotes = [existing.notes, patch.notes].filter(Boolean).join(' ').trim() || existing.notes;
  const updated = updateWineEntry(existing.id, {
    ...patch,
    notes: mergedNotes,
    source_text: [existing.source_text, cleanTelegramEnvelope(text)].filter(Boolean).join(' '),
    source_image_path: resolvedImagePath,
    source_type: existing.source_type || 'image',
  });

  return {
    ok: true,
    action: 'update',
    entry: updated,
    reply: `Updated wine entry: ${summarizeWine(updated) || 'wine entry stored.'}`,
  };
}

function recallWineFromText(text, extras = {}) {
  const criteria = { ...parseNaturalDateQuery(text, extras), ...extras };
  const cleaned = cleanTelegramEnvelope(text).toLowerCase();

  if (/\b(history|instances?|bought more than once|more than once|over time|prices? have i paid|price history)\b/.test(cleaned)) {
    const catalog = recallWineCatalog(criteria);
    if (!catalog.count) {
      return {
        ok: true,
        action: 'recall-catalog',
        criteria,
        result: catalog,
        reply: 'I couldn’t find a matching wine history yet.',
      };
    }

    const wine = catalog.wines[0];
    const lines = wine.instances.slice(0, 10).map((item) => {
      const when = item.consumed_on || item.purchased_on || item.created_at;
      const price = item.price != null ? `, $${Number(item.price).toFixed(2)}` : '';
      const rating = item.subjective_rating != null ? `, rated ${item.subjective_rating}/5` : '';
      return `- ${item.vintage || 'NV'} on ${when}${price}${rating}`;
    });
    return {
      ok: true,
      action: 'recall-catalog',
      criteria,
      result: catalog,
      reply: `${wine.producer ? `${wine.producer} — ` : ''}${wine.wine_name} has ${wine.instance_count} instance(s):\n${lines.join('\n')}`,
    };
  }

  if (!criteria.consumed_after && !criteria.consumed_before && /\b(show me|tell me about|what about)\b/.test(cleaned)) {
    const catalog = recallWineCatalog(criteria);
    if (catalog.count === 1) {
      const wine = catalog.wines[0];
      const primary = wine.instances[0] || {};
      const detailLines = [
        wine.region ? `- region: ${wine.region}` : null,
        wine.country ? `- country: ${wine.country}` : null,
        wine.style ? `- style: ${wine.style}` : null,
        wine.color ? `- color: ${wine.color}` : null,
        wine.varietal ? `- varietal: ${wine.varietal}` : null,
        wine.official_rating != null ? `- official rating: ${wine.official_rating}${wine.official_rating_source ? ` (${wine.official_rating_source})` : ''}` : null,
        primary.notes ? `- notes: ${primary.notes}` : null,
      ].filter(Boolean);
      const labelPath = wine.source_image_path
        ? `./${path.relative(path.resolve(__dirname, '..'), wine.source_image_path).replace(/\\/g, '/')}`
        : null;
      return {
        ok: true,
        action: 'recall-catalog',
        criteria,
        result: catalog,
        entry: primary,
        mediaPath: labelPath,
        caption: `${wine.wine_name || wine.producer || 'Wine'} label`,
        reply: `${wine.producer ? `${wine.producer} — ` : ''}${wine.wine_name}\n${detailLines.join('\n')}`,
      };
    }

    if (!catalog.count && criteria.text) {
      const broadCatalog = recallWineCatalog({ limit: 200 });
      const needle = criteria.text.normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
      const matched = broadCatalog.wines.filter((wine) => {
        const haystack = [wine.producer, wine.wine_name, wine.varietal, wine.region, wine.country, wine.style]
          .filter(Boolean)
          .join(' ')
          .normalize('NFKD')
          .replace(/[\u0300-\u036f]/g, '')
          .toLowerCase();
        return haystack.includes(needle);
      });

      if (matched.length === 1) {
        const wine = matched[0];
        const primary = wine.instances[0] || {};
        const detailLines = [
          wine.region ? `- region: ${wine.region}` : null,
          wine.country ? `- country: ${wine.country}` : null,
          wine.style ? `- style: ${wine.style}` : null,
          wine.color ? `- color: ${wine.color}` : null,
          wine.varietal ? `- varietal: ${wine.varietal}` : null,
          wine.official_rating != null ? `- official rating: ${wine.official_rating}${wine.official_rating_source ? ` (${wine.official_rating_source})` : ''}` : null,
          primary.notes ? `- notes: ${primary.notes}` : null,
        ].filter(Boolean);
        const labelPath = wine.source_image_path
          ? `./${path.relative(path.resolve(__dirname, '..'), wine.source_image_path).replace(/\\/g, '/')}`
          : null;
        return {
          ok: true,
          action: 'recall-catalog',
          criteria,
          result: { criteria, count: 1, wines: matched },
          entry: primary,
          mediaPath: labelPath,
          caption: `${wine.wine_name || wine.producer || 'Wine'} label`,
          reply: `${wine.producer ? `${wine.producer} — ` : ''}${wine.wine_name}\n${detailLines.join('\n')}`,
        };
      }
    }
  }

  const result = recallWineEntries(criteria);

  if (!result.count) {
    return {
      ok: true,
      action: 'recall',
      criteria,
      result,
      reply: 'I couldn’t find a matching wine entry yet.',
    };
  }

  if (result.count === 1) {
    return {
      ok: true,
      action: 'recall',
      criteria,
      result,
      reply: `I found 1 match: ${result.summary[0].summary}`,
    };
  }

  const top = result.summary.slice(0, 5).map((item) => `- ${item.summary}`).join('\n');
  return {
    ok: true,
    action: 'recall',
    criteria,
    result,
    reply: `I found ${result.count} matches:\n${top}`,
  };
}

function showWineLabelFromText(text, extras = {}) {
  const cleaned = cleanTelegramEnvelope(text);
  const criteria = { ...parseNaturalDateQuery(cleaned), ...extras, limit: extras.limit || 5 };
  if (criteria.text) {
    criteria.text = criteria.text
      .replace(/\b(label|image|photo|picture)\b/gi, ' ')
      .replace(/\s+/g, ' ')
      .trim();
    if (!criteria.text) delete criteria.text;
  }
  let results = queryWineEntries(criteria);
  if (!results.length && criteria.text) {
    const asciiText = criteria.text
      .normalize('NFKD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/ẽ/gi, 'e');
    if (asciiText && asciiText !== criteria.text) {
      results = queryWineEntries({ ...criteria, text: asciiText });
    }
  }
  if (!results.length && criteria.text) {
    const needle = criteria.text
      .normalize('NFKD')
      .replace(/[\u0300-\u036f]/g, '')
      .toLowerCase();
    results = queryWineEntries({ limit: 100 }).filter((entry) => {
      const haystack = [entry.wine_name, entry.producer, entry.notes, entry.source_text]
        .filter(Boolean)
        .join(' ')
        .normalize('NFKD')
        .replace(/[\u0300-\u036f]/g, '')
        .toLowerCase();
      return haystack.includes(needle);
    });
  }
  const withImages = results.filter((entry) => entry.source_image_path);

  if (!withImages.length) {
    return {
      ok: false,
      action: 'show-label',
      criteria,
      reply: 'I found the wine entry, but there is no archived label image attached yet.',
    };
  }

  const entry = withImages[0];
  const relPath = path.relative(path.resolve(__dirname, '..'), entry.source_image_path);
  return {
    ok: true,
    action: 'show-label',
    criteria,
    entry,
    mediaPath: `./${relPath.replace(/\\/g, '/')}`,
    caption: `${entry.wine_name || entry.producer || 'Wine'} label`,
    reply: `MEDIA:./${relPath.replace(/\\/g, '/')} ${entry.wine_name || entry.producer || 'Wine'} label`,
  };
}

function showWineFromText(text, extras = {}) {
  const cleaned = cleanTelegramEnvelope(text);
  const criteria = { ...parseNaturalDateQuery(cleaned, extras), ...extras, limit: extras.limit || 5 };
  if (criteria.text) {
    criteria.text = criteria.text
      .replace(/\bwine\b/gi, ' ')
      .replace(/\s+/g, ' ')
      .trim();
    if (!criteria.text) delete criteria.text;
  }

  const catalog = recallWineCatalog(criteria);
  let wines = catalog.wines;

  if (!wines.length && criteria.text) {
    const broadCatalog = recallWineCatalog({ limit: 200 });
    const needle = criteria.text.normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
    wines = broadCatalog.wines.filter((wine) => {
      const haystack = [wine.producer, wine.wine_name, wine.varietal, wine.region, wine.country, wine.style]
        .filter(Boolean)
        .join(' ')
        .normalize('NFKD')
        .replace(/[\u0300-\u036f]/g, '')
        .toLowerCase();
      return haystack.includes(needle);
    });
  }

  if (!wines.length) {
    return {
      ok: true,
      action: 'show-wine',
      criteria,
      reply: 'I couldn’t find a matching wine entry yet.',
    };
  }

  const wine = wines[0];
  const primary = wine.instances[0] || {};
  const detailLines = [
    primary.vintage ? `- vintage: ${primary.vintage}` : null,
    wine.region ? `- region: ${wine.region}` : null,
    wine.country ? `- country: ${wine.country}` : null,
    wine.style ? `- style: ${wine.style}` : null,
    wine.color ? `- color: ${wine.color}` : null,
    wine.varietal ? `- varietal: ${wine.varietal}` : null,
    wine.official_rating != null ? `- official rating: ${wine.official_rating}${wine.official_rating_source ? ` (${wine.official_rating_source})` : ''}` : null,
    primary.place_of_purchase ? `- place of purchase: ${primary.place_of_purchase}` : null,
    primary.price != null ? `- price: $${Number(primary.price).toFixed(2)}` : null,
    primary.purchased_on ? `- purchased_on: ${primary.purchased_on}` : null,
    primary.consumed_on ? `- consumed_on: ${primary.consumed_on}` : null,
    primary.subjective_rating != null ? `- personal rating: ${primary.subjective_rating}/5` : null,
    primary.notes ? `- notes: ${primary.notes}` : null,
  ].filter(Boolean);
  const labelPath = wine.source_image_path
    ? `./${path.relative(path.resolve(__dirname, '..'), wine.source_image_path).replace(/\\/g, '/')}`
    : null;

  return {
    ok: true,
    action: 'show-wine',
    criteria,
    result: { criteria, count: wines.length, wines },
    entry: primary,
    mediaPath: labelPath,
    caption: `${wine.wine_name || wine.producer || 'Wine'} label`,
    reply: `${wine.producer ? `${wine.producer} — ` : ''}${wine.wine_name}\n${detailLines.join('\n')}`,
  };
}

function handleWineChat(input = {}) {
  const text = normalizeText(input.text);
  const labelText = normalizeText(input.labelText);
  const imagePath = input.imagePath || null;
  const hasImage = Boolean(imagePath || /\[media attached:/i.test(text) || /<media:image>/i.test(text));
  const intent = input.intent || classifyWineIntent(text || labelText, { hasImage });

  if (hasImage && !labelText && detectTextOnlyUpdate(text)) {
    return updateRecentWineFromText(text, { imagePath });
  }
  if (labelText && (intent === 'label' || intent === 'remember' || imagePath)) {
    return rememberWineFromLabel({ labelText, imagePath, text, extras: input.entry || {} });
  }
  if (hasImage && intent !== 'recall') {
    if (!cleanTelegramEnvelope(text)) {
      return {
        ok: false,
        action: 'awaiting-vision',
        reply: 'Image received, but I still need extracted label text before saving a reliable wine entry.',
      };
    }
    return rememberWineFromLabel({ labelText: '', imagePath, text, extras: input.entry || {} });
  }
  if (intent === 'remember') {
    return rememberWineFromText(text, input.entry || {});
  }
  if (intent === 'show-label') {
    return showWineLabelFromText(text, input.criteria || {});
  }
  if (intent === 'show-wine') {
    return showWineFromText(text, input.criteria || {});
  }
  if (intent === 'recall') {
    return recallWineFromText(text, input.criteria || {});
  }
  return {
    ok: false,
    action: 'unknown',
    reply: 'No wine action recognized. Try asking to remember a wine, parse a label, or recall one.',
  };
}

module.exports = {
  classifyWineIntent,
  classifyWineIntentOptionalLlm,
  cleanTelegramEnvelope,
  handleWineChat,
  parseNaturalDateQuery,
  rememberWineFromText,
  rememberWineFromLabel,
  recallWineFromText,
  showWineFromText,
  showWineLabelFromText,
  updateRecentWineFromText,
};
