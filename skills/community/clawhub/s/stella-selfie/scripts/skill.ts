/**
 * Stella — OpenClaw image generation skill runtime.
 *
 * This is the entrypoint invoked by SKILL.md.
 */

import * as path from "path";
import * as os from "os";
import * as fs from "fs";

import { parseIdentity } from "./identity";
import { selectAvatars } from "./avatars";
import { generateWithGemini, Resolution as GeminiResolution } from "./providers/gemini";
import { generateWithFal } from "./providers/fal";
import { generateWithLaozhang } from "./providers/laozhang";
import { sendImage, sendMessage } from "./sender";
import { asStellaError, formatFailureMessage } from "./errors";

type Provider = "gemini" | "fal" | "laozhang";
type Resolution = "1K" | "2K" | "4K";

interface CliArgs {
  prompt: string;
  target: string;
  channel: string;
  caption: string;
  resolution: Resolution;
  count: number;
}

function getMissingProviderCredential(provider: Provider): string | null {
  if (provider === "gemini" && !process.env.GEMINI_API_KEY) return "GEMINI_API_KEY";
  if (provider === "fal" && !process.env.FAL_KEY) return "FAL_KEY";
  if (provider === "laozhang" && !process.env.LAOZHANG_API_KEY) return "LAOZHANG_API_KEY";
  return null;
}

function hasConfiguredAvatarsDirFailure(options: {
  avatarsDir: string | null;
  avatarBlendEnabled: boolean;
}): boolean {
  const { avatarsDir, avatarBlendEnabled } = options;
  if (!avatarBlendEnabled || !avatarsDir) return false;
  if (!fs.existsSync(avatarsDir)) return true;
  try {
    fs.readdirSync(avatarsDir);
    return false;
  } catch {
    return true;
  }
}

function getReferenceConfigGuideMessage(provider: Provider): string {
  if (provider === "fal") {
    return [
      "我暂时不能生成图片：参考图配置不完整。",
      "请在 ~/.openclaw/workspace/IDENTITY.md 中正确配置 AvatarsURLs（多个 URL 用逗号分隔，且必须是可公开访问的 http/https 图片地址）。",
      "示例：AvatarsURLs: https://cdn.example.com/ref1.jpg, https://cdn.example.com/ref2.jpg",
    ].join("\n");
  }

  return [
    "我暂时不能生成图片：参考图目录读取失败。",
    "请检查 ~/.openclaw/workspace/IDENTITY.md 中的 AvatarsDir 是否存在且可读取，并放入同一角色的参考图。",
    "示例：AvatarsDir: ./avatars",
  ].join("\n");
}

function parseArgs(argv: string[]): CliArgs {
  const args = argv.slice(2);
  const get = (flag: string): string | undefined => {
    const idx = args.indexOf(flag);
    if (idx === -1 || idx + 1 >= args.length) return undefined;
    return args[idx + 1];
  };

  const prompt = get("--prompt");
  const target = get("--target");
  const channel = get("--channel");

  if (!prompt || !target || !channel) {
    console.error(`
Usage: node dist/scripts/skill.js \\
  --prompt "<assembled prompt>" \\
  --target "<channel destination>" \\
  --channel "<channel provider>" \\
  [--caption "<caption>"] \\
  [--resolution <1K|2K|4K>] \\
  [--count <number>]
`);
    process.exit(1);
  }

  const resolutionRaw = get("--resolution") || "1K";
  const validResolutions: Resolution[] = ["1K", "2K", "4K"];
  if (!validResolutions.includes(resolutionRaw as Resolution)) {
    console.error(`[stella] Invalid resolution: ${resolutionRaw}. Use 1K, 2K, or 4K.`);
    process.exit(1);
  }

  const countRaw = get("--count");
  const count = countRaw ? parseInt(countRaw, 10) : 1;
  if (isNaN(count) || count < 1) {
    console.error(`[stella] Invalid count: ${countRaw}`);
    process.exit(1);
  }

  return {
    prompt,
    target,
    channel,
    caption: get("--caption") || "",
    resolution: resolutionRaw as Resolution,
    count,
  };
}

export async function runSkill(argv: string[] = process.argv): Promise<void> {
  const args = parseArgs(argv);

  const provider: Provider = (process.env.Provider as Provider) || "gemini";
  const avatarBlendEnabled =
    (process.env.AvatarBlendEnabled || "true").toLowerCase() !== "false";

  if (provider !== "gemini" && provider !== "fal" && provider !== "laozhang") {
    console.error(`[stella] Unknown Provider: "${provider}". Use "gemini", "fal", or "laozhang".`);
    process.exit(1);
  }

  const missingCredential = getMissingProviderCredential(provider);
  if (missingCredential) {
    console.error(
      `[stella] ${missingCredential} is not set. Configure it in OpenClaw skills.entries.stella-selfie.env.`
    );
    process.exit(1);
  }

  // Parse identity from the OpenClaw workspace on this machine
  const workspaceRoot = path.join(os.homedir(), ".openclaw", "workspace");
  let identity: ReturnType<typeof parseIdentity>;
  try {
    identity = parseIdentity(workspaceRoot);
  } catch (err) {
    const msg = (err as Error)?.message || String(err);
    console.error(
      `[stella] Failed to read identity config from ${workspaceRoot}: ${msg}. Configure ~/.openclaw/workspace/IDENTITY.md first.`
    );
    process.exit(1);
  }

  const envMaxRefs = process.env.AvatarMaxRefs ? parseInt(process.env.AvatarMaxRefs, 10) : null;
  const avatarMaxRefs =
    envMaxRefs && !isNaN(envMaxRefs) && envMaxRefs > 0 ? envMaxRefs : 3;

  const referenceImages = selectAvatars({
    avatar: identity.avatar,
    avatarsDir: identity.avatarsDir,
    avatarMaxRefs,
    avatarBlendEnabled,
  });

  const avatarsDirCheckFailed = hasConfiguredAvatarsDirFailure({
    avatarsDir: identity.avatarsDir,
    avatarBlendEnabled,
  });
  const localReferenceImages = referenceImages.slice(0, avatarMaxRefs);
  const missingNonFalAvatarsDir =
    provider !== "fal" && avatarBlendEnabled && !identity.avatarsDir;
  const missingValidLocalRefs = provider !== "fal" && localReferenceImages.length === 0;
  const missingFalAvatarUrls = provider === "fal" && identity.avatarsURLs.length === 0;
  if (
    avatarsDirCheckFailed ||
    missingNonFalAvatarsDir ||
    missingValidLocalRefs ||
    missingFalAvatarUrls
  ) {
    const message = getReferenceConfigGuideMessage(
      missingFalAvatarUrls ? "fal" : "gemini"
    );
    await sendMessage({
      channel: args.channel,
      target: args.target,
      message,
    });
    return;
  }

  try {
    const sendGeneratedMedia = async (media: string): Promise<void> => {
      try {
        await sendImage({
          channel: args.channel,
          target: args.target,
          media,
          message: args.caption,
        });
      } catch (err) {
        throw asStellaError("openclaw", err);
      }
    };

    if (provider === "gemini") {
      const results = await generateWithGemini({
        prompt: args.prompt,
        referenceImages: localReferenceImages,
        resolution: args.resolution as GeminiResolution,
        count: args.count,
      });

      for (const result of results) {
        await sendGeneratedMedia(result.outputPath);
        try {
          fs.unlinkSync(result.outputPath);
        } catch (cleanupErr) {
          const cleanupMsg =
            (cleanupErr as Error)?.message || String(cleanupErr);
          console.warn(
            `[stella] Failed to remove generated file: ${result.outputPath} (${cleanupMsg})`
          );
        }
      }
    } else if (provider === "laozhang") {
      const results = await generateWithLaozhang({
        prompt: args.prompt,
        referenceImages: localReferenceImages,
        resolution: args.resolution,
        count: args.count,
      });

      for (const result of results) {
        await sendGeneratedMedia(result.outputPath);
        try {
          fs.unlinkSync(result.outputPath);
        } catch (cleanupErr) {
          const cleanupMsg =
            (cleanupErr as Error)?.message || String(cleanupErr);
          console.warn(
            `[stella] Failed to remove generated file: ${result.outputPath} (${cleanupMsg})`
          );
        }
      }
    } else {
      // fal provider: reference images must be HTTP/HTTPS URLs
      const referenceImageUrls =
        identity.avatarsURLs.length > 0
          ? identity.avatarsURLs.slice(0, avatarMaxRefs)
          : referenceImages.filter((p) => p.startsWith("http://") || p.startsWith("https://"));

      const results = await generateWithFal({
        prompt: args.prompt,
        referenceImageUrls,
        resolution: args.resolution,
        count: args.count,
      });

      for (const result of results) {
        await sendGeneratedMedia(result.imageUrl);
      }
    }
  } catch (err) {
    const stellaErr = asStellaError(provider, err);
    const failureMessage = formatFailureMessage(stellaErr.details);

    // Only attempt proactive failure notification for generation/provider errors.
    // If sending path itself fails, a second notification on the same path is unlikely to succeed.
    if (stellaErr.details.provider !== "openclaw") {
      try {
        await sendMessage({
          channel: args.channel,
          target: args.target,
          message: failureMessage,
        });
      } catch (notifyErr) {
        const notifyMsg =
          (notifyErr as Error)?.message || String(notifyErr);
        console.warn(`[stella] Failed to notify channel about generation error: ${notifyMsg}`);
      }
    }

    throw stellaErr;
  }
}

if (require.main === module) {
  runSkill().catch((err) => {
    console.error(`[stella] Fatal error: ${(err as Error).message}`);
    process.exit(1);
  });
}
