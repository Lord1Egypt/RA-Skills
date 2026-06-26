import fs from "node:fs";
import path from "node:path";
import { parseArgs } from "./args.mjs";
import { config, generatedDir, resolveProjectPath } from "./config.mjs";
import { loadState, saveState, updateItem } from "./state.mjs";
import { createDraft, fileSha1, getStableAccessToken, uploadArticleImage, uploadPermanentImage } from "./wechat.mjs";
import { validateGeneratedArticle } from "./generated-schema.mjs";

function generatedFiles(args) {
  if (args.all) {
    return fs.readdirSync(generatedDir)
      .filter((name) => name.endsWith(".json"))
      .map((name) => path.join(generatedDir, name));
  }
  return (args._ || []).map((file) => path.resolve(file));
}

async function uploadCachedCover(accessToken, state, coverPath) {
  const resolvedCoverPath = resolveProjectPath(coverPath);
  const hash = fileSha1(resolvedCoverPath);
  if (state.coverMedia[hash]?.mediaId) return state.coverMedia[hash].mediaId;

  const mediaId = await uploadPermanentImage(accessToken, resolvedCoverPath);
  state.coverMedia[hash] = {
    mediaId,
    path: resolvedCoverPath,
    uploadedAt: new Date().toISOString()
  };
  saveState(state);
  return mediaId;
}

async function resolveThumbMediaId(accessToken, state, article) {
  if (article.coverImagePath) {
    return await uploadCachedCover(accessToken, state, article.coverImagePath);
  }

  if (!config.allowStaticCoverFallback) {
    throw new Error("coverImagePath is required. Generate a model-based cover image under data/images/ and set coverImagePath before creating a WeChat draft.");
  }

  if (config.wechatThumbMediaId) return config.wechatThumbMediaId;

  const coverPath = resolveProjectPath(config.defaultCoverPath);
  return await uploadCachedCover(accessToken, state, coverPath);
}

function validateDraftReadiness(article) {
  const errors = [];
  if (!article.coverImagePath && !config.allowStaticCoverFallback) {
    errors.push("coverImagePath is required by default; use image2/imagegen to create a model-based cover image before drafting");
  }
  return errors;
}

function escapeHtml(value) {
  return String(value || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

async function applyInlineImages(accessToken, article) {
  if (!Array.isArray(article.inlineImages) || article.inlineImages.length === 0) return article;

  let contentHtml = article.contentHtml;
  for (const image of article.inlineImages) {
    const uploadedUrl = await uploadArticleImage(accessToken, image.path);
    const alt = escapeHtml(image.alt || image.caption || article.title);
    const caption = image.caption
      ? `<span style="display:block; margin-top: 6px; color: #6b7280; font-size: 13px; line-height: 1.6;">${escapeHtml(image.caption)}</span>`
      : "";
    const imageHtml = `<p style="margin: 22px 0; text-align: center;"><img src="${uploadedUrl}" alt="${alt}" style="max-width: 100%; height: auto; border-radius: 8px;" />${caption}</p>`;
    contentHtml = contentHtml.split(image.placeholder).join(imageHtml);
  }

  return { ...article, contentHtml };
}

const args = parseArgs();
const files = generatedFiles(args);
if (!files.length) {
  console.log("No generated article files found.");
  process.exit(0);
}

const state = loadState();
let accessToken = null;
let drafted = 0;
let skipped = 0;
let failed = 0;

for (const file of files) {
  const article = JSON.parse(fs.readFileSync(file, "utf8"));
  const errors = [
    ...validateGeneratedArticle(article),
    ...validateDraftReadiness(article)
  ];
  if (errors.length) {
    failed += 1;
    updateItem(state, article.sourceId || file, {
      status: "failed_validation",
      generatedPath: file,
      lastError: errors.join("; ")
    });
    console.error(`${file}: validation failed: ${errors.join("; ")}`);
    continue;
  }

  const existing = state.items[article.sourceId];
  if (existing?.status === "drafted" && !args.force) {
    skipped += 1;
    console.log(`${article.sourceId}: skipped, already drafted`);
    continue;
  }

  if (config.dryRun) {
    skipped += 1;
    updateItem(state, article.sourceId, {
      status: "dry_run_ready",
      generatedPath: file
    });
    console.log(`${article.sourceId}: dry run, draft not created`);
    continue;
  }

  try {
    accessToken ||= await getStableAccessToken();
    const thumbMediaId = await resolveThumbMediaId(accessToken, state, article);
    const articleWithImages = await applyInlineImages(accessToken, article);
    const result = await createDraft(accessToken, articleWithImages, thumbMediaId);
    drafted += 1;
    updateItem(state, article.sourceId, {
      status: "drafted",
      generatedPath: file,
      mediaId: result.media_id,
      creationSource: config.wechatCreationSource,
      creationSourceStatus: "manual_required",
      draftedAt: new Date().toISOString()
    });
    console.log(`${article.sourceId}: drafted ${result.media_id}; set 创作来源 manually to ${config.wechatCreationSource}`);
  } catch (error) {
    failed += 1;
    updateItem(state, article.sourceId, {
      status: "failed_draft",
      generatedPath: file,
      lastError: error.message
    });
    console.error(`${article.sourceId}: draft failed: ${error.message}`);
  }
}

state.runs.push({
  type: "draft",
  at: new Date().toISOString(),
  files: files.length,
  drafted,
  skipped,
  failed,
  dryRun: config.dryRun
});
saveState(state);

console.log(JSON.stringify({
  ok: failed === 0,
  drafted,
  skipped,
  failed,
  dryRun: config.dryRun,
  creationSource: config.wechatCreationSource,
  creationSourceStatus: "manual_required_by_wechat_backend"
}, null, 2));
if (failed) process.exit(1);
