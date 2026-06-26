import type { KnowledgeResponse } from "../schemas.js";

export class ExportService {
  buildExports(result: Omit<KnowledgeResponse, "exports">, formats: string[]): Record<string, unknown> {
    const exports: Record<string, unknown> = {};
    if (formats.includes("json")) exports.json = JSON.stringify(result, null, 2);
    if (formats.includes("markdown")) exports.markdown = this.toMarkdown(result);
    if (formats.includes("notion")) exports.notion = this.toNotion(result);
    return exports;
  }

  private toMarkdown(result: Omit<KnowledgeResponse, "exports">): string {
    const lines = [
      "# Video To Knowledge",
      "",
      "## Summary",
      result.summary || "No summary generated.",
      "",
      "## Topics",
      ...(result.topics.length ? result.topics.map((topic) => `- ${topic}`) : ["- None"]),
      "",
      "## Key Points",
      ...(result.key_points.length ? result.key_points.map((point) => `- ${point}`) : ["- None"]),
      "",
      "## Action Items",
      ...(result.action_items.length ? result.action_items.map((item) => `- ${item.task} | owner: ${item.owner} | deadline: ${item.deadline}`) : ["- None"]),
      "",
      "## Q&A",
      ...(result.qa_pairs.length ? result.qa_pairs.map((pair) => `- Q: ${pair.question}\n  A: ${pair.answer}`) : ["- None"]),
      "",
      "## Flashcards",
      ...(result.flashcards.length ? result.flashcards.map((card) => `- Front: ${card.front}\n  Back: ${card.back}`) : ["- None"]),
      "",
      "## Entities",
      ...(result.entities.length ? result.entities.map((entity) => `- ${entity.name} (${entity.type})`) : ["- None"]),
    ];
    return lines.join("\n");
  }

  private toNotion(result: Omit<KnowledgeResponse, "exports">): Record<string, unknown> {
    const blocks = [
      { type: "heading_1", text: "Video To Knowledge" },
      { type: "paragraph", text: result.summary || "No summary generated." },
      { type: "heading_2", text: "Topics" },
      ...result.topics.map((topic) => ({ type: "bulleted_list_item", text: topic })),
      { type: "heading_2", text: "Key Points" },
      ...result.key_points.map((point) => ({ type: "bulleted_list_item", text: point })),
      { type: "heading_2", text: "Action Items" },
      ...result.action_items.map((item) => ({ type: "to_do", text: `${item.task} | ${item.owner} | ${item.deadline}` })),
    ];
    return { title: "Video To Knowledge", blocks };
  }
}
