/**
 * PersonaGenerator: generates or updates user persona using the four-layer
 * deep scan model via CleanContextRunner.
 */

import fs from "node:fs/promises";
import path from "node:path";
import { CleanContextRunner } from "../utils/clean_context_runner.js";
import { CheckpointManager } from "../utils/checkpoint.js";
import { readSceneIndex } from "../scene/scene_index.js";
import { generateSceneNavigation, stripSceneNavigation } from "../scene/scene_navigation.js";
import { buildPersonaPrompt } from "../prompts/persona_generation.js";
import { BackupManager } from "../utils/backup.js";
import { escapeXmlTags } from "../utils/sanitize.js";

const TAG = "[unified-memory] [persona]";

/**
 * @typedef {Object} PersonaLogger
 * @property {(message: string) => void} [debug]
 * @property {(message: string) => void} info
 * @property {(message: string) => void} warn
 * @property {(message: string) => void} error
 */

export class PersonaGenerator {
  /**
   * @param {{
   *   dataDir: string,
   *   config: unknown,
   *   model?: string,
   *   backupCount?: number,
   *   logger?: PersonaLogger
   * }} opts
   */
  constructor(opts) {
    this.dataDir = opts.dataDir;
    this.logger = opts.logger;
    this.backupCount = opts.backupCount ?? 3;
    this.runner = new CleanContextRunner({
      config: opts.config,
      modelRef: opts.model,
      logger: opts.logger,
    });
    this.logger?.debug?.(`${TAG} Generator created: model=${opts.model ?? "(default)"}, dataDir=${opts.dataDir}`);
  }

  /**
   * Execute persona generation.
   * @param {string} [triggerReason]
   * @returns {Promise<boolean>}
   */
  async generate(triggerReason) {
    const startMs = Date.now();
    this.logger?.debug?.(`${TAG} Starting generation: reason="${triggerReason ?? "none"}"`);

    const cpManager = new CheckpointManager(this.dataDir);
    const cp = await cpManager.read();
    this.logger?.debug?.(`${TAG} Checkpoint: total_processed=${cp.total_processed}, last_persona_at=${cp.last_persona_at}`);

    const personaPath = path.join(this.dataDir, "persona.md");

    // 1. Read existing persona (strip navigation)
    let existingPersona;
    try {
      const raw = await fs.readFile(personaPath, "utf-8");
      existingPersona = stripSceneNavigation(raw).trim() || undefined;
      this.logger?.debug?.(`${TAG} Existing persona: ${existingPersona ? `${existingPersona.length} chars` : "empty"}`);
    } catch {
      this.logger?.debug?.(`${TAG} No existing persona file`);
    }

    // 2. Load scene index + identify changed scenes
    const index = await readSceneIndex(this.dataDir);
    const changedScenes = index.filter((e) => {
      if (!cp.last_persona_time) return true;
      const updatedMs = new Date(e.updated).getTime();
      const personaMs = new Date(cp.last_persona_time).getTime();
      if (Number.isNaN(updatedMs) || Number.isNaN(personaMs)) return true;
      return updatedMs > personaMs;
    });
    this.logger?.debug?.(`${TAG} Scene index: ${index.length} total, ${changedScenes.length} changed since last persona`);

    // 3. Read changed scene contents (full raw content including META)
    const blocksDir = path.join(this.dataDir, "scene_blocks");
    const changedSceneContents = [];
    for (const entry of changedScenes) {
      try {
        const raw = await fs.readFile(path.join(blocksDir, entry.filename), "utf-8");
        changedSceneContents.push(
          `### [${changedSceneContents.length + 1}] ${entry.filename}\n\n\`\`\`markdown\n${raw}\n\`\`\``,
        );
      } catch {
        this.logger?.warn(`${TAG} Could not read scene block: ${entry.filename}`);
      }
    }

    if (changedSceneContents.length === 0 && existingPersona) {
      this.logger?.debug?.(`${TAG} No scene changes and persona exists, skipping generation`);
      return false;
    }

    // 4. Determine mode
    const mode = existingPersona ? "incremental" : "first";
    this.logger?.debug?.(`${TAG} Generation mode: ${mode}, ${changedSceneContents.length} scene blocks to process`);

    // 5. Build changed scenes section with guidance
    let changedScenesContent;
    if (changedSceneContents.length > 0) {
      changedScenesContent =
        `\n\n## 📄 变化场景完整内容\n\n` +
        `*自上次 Persona 更新后，以下 ${changedSceneContents.length} 个场景发生了变化。工程已为你预加载完整内容：*\n\n` +
        changedSceneContents.join("\n\n") +
        `\n\n---\n\n` +
        `⚠️ **重点分析变化场景**：上述场景是自上次更新后的**新增/修改内容**，请**重点分析**这些场景中的新信息。\n`;
    } else {
      changedScenesContent = `\n\n⚠️ **无变化场景**：所有场景均已在上次 Persona 更新中分析过，本次可直接读取所有场景进行全局审视。\n`;
    }

    // 6. Build prompt
    const prompt = buildPersonaPrompt({
      mode,
      currentTime: new Date().toISOString(),
      totalProcessed: cp.total_processed,
      sceneCount: index.length,
      changedSceneCount: changedScenes.length,
      changedScenesContent,
      existingPersona,
      triggerInfo: triggerReason,
      personaFilePath: personaPath,
      checkpointPath: path.join(this.dataDir, ".metadata", "recall_checkpoint.json"),
    });

    // 7. Run in clean context
    let personaText;
    try {
      this.logger?.debug?.(`${TAG} Calling LLM for persona generation (timeout=180s)...`);
      personaText = await this.runner.run({
        prompt,
        taskId: "persona-generation",
        timeoutMs: 180_000,
      });
      this.logger?.debug?.(`${TAG} LLM response received: ${personaText.length} chars`);
    } catch (err) {
      const elapsedMs = Date.now() - startMs;
      this.logger?.error(`${TAG} Persona generation failed after ${elapsedMs}ms: ${err instanceof Error ? err.stack ?? err.message : String(err)}`);
      return false;
    }

    // 8. Strip any navigation the LLM might have added + sanitize
    personaText = escapeXmlTags(stripSceneNavigation(personaText).trim());

    // 9. Append fresh scene navigation
    const nav = generateSceneNavigation(index);
    const finalContent = nav ? `${personaText}\n\n${nav}\n` : personaText;

    // 10. Backup before overwriting
    const bm = new BackupManager(path.join(this.dataDir, ".backup"));
    await bm.backupFile(personaPath, "persona", `offset${cp.total_processed}`, this.backupCount);

    // 11. Write persona file
    await fs.writeFile(personaPath, finalContent, "utf-8");

    // 12. Update checkpoint
    await cpManager.markPersonaGenerated(cp.total_processed);

    const elapsedMs = Date.now() - startMs;
    this.logger?.info(`${TAG} Persona written (${finalContent.length} chars) in ${elapsedMs}ms`);

    return true;
  }
}
