import crypto from "node:crypto";
import * as cheerio from "cheerio";
import { fetchText, normalizeWhitespace } from "./http.mjs";

function stableId(url, title) {
  return crypto
    .createHash("sha1")
    .update(`${url || ""}\n${title || ""}`)
    .digest("hex")
    .slice(0, 16);
}

function parseTrackMeta(value) {
  if (!value) return {};
  try {
    return JSON.parse(value);
  } catch {
    return {};
  }
}

function cleanReason(text) {
  return normalizeWhitespace(text).replace(/^推荐理由：?/, "").trim();
}

export async function fetchAihotFeaturedItems(aihotUrl) {
  const html = await fetchText(aihotUrl);
  const $ = cheerio.load(html);
  const items = [];

  $(".timeline-day").each((_, day) => {
    const dateLabel = normalizeWhitespace($(day).find(".timeline-date").first().text());

    $(day).find(".timeline-item").each((index, node) => {
      const card = $(node).find(".timeline-card").first();
      if (!card.length) return;

      const titleLink = card.find("a.timeline-title").first();
      const bodyLink = card.find("a.uc-body").first();
      const link = titleLink.length ? titleLink : bodyLink;
      const url = link.attr("href") || "";
      if (!url || url.startsWith("/")) return;

      const trackMeta = parseTrackMeta(link.attr("data-track-meta"));
      const sourceId = trackMeta.itemId || stableId(url, link.text());
      const sourceName = normalizeWhitespace(card.find(".timeline-source").first().text());
      const handle = normalizeWhitespace(card.find(".uc-handle").first().text()).replace(/\s+/g, "");
      const scoreText = normalizeWhitespace(card.find(".timeline-score").first().text());
      const score = Number.parseInt(scoreText, 10);
      const timeLabel = normalizeWhitespace($(node).find(".timeline-time").first().text());
      const tags = card.find(".timeline-tags .tag").map((__, tag) => normalizeWhitespace($(tag).text())).get().filter(Boolean);
      const reason = cleanReason(card.find(".timeline-reason").first().text());
      const summary = normalizeWhitespace(card.find(".timeline-summary").first().text());
      const body = normalizeWhitespace(card.find(".uc-body-p").first().text());
      const quoted = normalizeWhitespace(card.find(".uc-quoted").first().text());
      const title = normalizeWhitespace(titleLink.length ? titleLink.text() : body.slice(0, 80));
      const coverImageUrl = card.find(".x-tweet-media-img").first().attr("src") || "";

      items.push({
        sourceId,
        order: items.length + index,
        url,
        title,
        sourceName,
        handle,
        dateLabel,
        timeLabel,
        score: Number.isFinite(score) ? score : null,
        tags,
        reason,
        summary,
        body,
        quoted,
        coverImageUrl,
        collectedAt: new Date().toISOString()
      });
    });
  });

  return items;
}
