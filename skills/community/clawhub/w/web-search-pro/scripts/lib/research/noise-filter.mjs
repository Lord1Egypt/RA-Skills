import { assessResearchDocumentQuality } from "./document-quality.mjs";

export function curateResearchEntry({ taskKind, entry, sourceType }) {
  const assessment = assessResearchDocumentQuality({
    taskKind,
    title: entry.title ?? entry.url ?? "",
    snippet: entry.snippet ?? entry.content ?? "",
    content: entry.content ?? "",
  });

  if (assessment.interstitial) {
    return {
      dropped: true,
      dropReason: "interstitial",
      assessment,
      entry: null,
    };
  }

  if (
    taskKind !== "map" &&
    sourceType !== "site-map" &&
    assessment.documentQuality === "low" &&
    assessment.hasPrimaryContent !== true
  ) {
    return {
      dropped: true,
      dropReason: "low-signal",
      assessment,
      entry: null,
    };
  }

  return {
    dropped: false,
    dropReason: null,
    assessment,
    entry: {
      ...entry,
      title: assessment.cleanedTitle || entry.title || entry.url || "",
      snippet: assessment.cleanedSnippet,
      content: assessment.cleanedContent,
    },
  };
}
