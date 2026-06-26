import { randomUUID } from "crypto";
import { readFileSync, writeFileSync, existsSync } from "fs";
import { join } from "path";
import { tmpdir } from "os";

const TRIPO_API_BASE = "https://api.tripo3d.ai/v2/openapi";
const PROXY_BASE = "https://skills.vast-internal.com/platform/tripo";

let ephemeralUserId = null;

function getUserId() {
  const baseDir = process.env.HOME || process.env.USERPROFILE || tmpdir();
  const idFile = join(baseDir, ".tripo-skill-id");
  try {
    if (existsSync(idFile)) {
      const id = readFileSync(idFile, "utf-8").trim();
      if (id) return id;
    }
  } catch {
    /* fall through */
  }
  const id = randomUUID().replace(/-/g, "").slice(0, 16);
  try {
    writeFileSync(idFile, id, "utf-8");
    return id;
  } catch {
    if (!ephemeralUserId) ephemeralUserId = randomUUID().replace(/-/g, "").slice(0, 16);
    return ephemeralUserId;
  }
}

function proxyHeaders(ctx) {
  const secret = ctx.secrets?.TRIPO_PROXY_SECRET;
  if (!secret) {
    return null;
  }
  return {
    "Content-Type": "application/json",
    "x-proxy-secret": secret,
  };
}

async function postJson(url, body, extraHeaders = {}) {
  const res = await fetch(url, {
    method: "POST",
    headers: { ...extraHeaders },
    body: JSON.stringify(body),
  });
  return res.json();
}

async function getJson(url, extraHeaders = {}) {
  const res = await fetch(url, { headers: { ...extraHeaders } });
  return res.json();
}

async function tripoPostTask(userApiKey, taskBody) {
  return postJson(`${TRIPO_API_BASE}/task`, taskBody, {
    "Content-Type": "application/json",
    Authorization: `Bearer ${userApiKey}`,
  });
}

async function tripoGetTask(userApiKey, taskId) {
  return getJson(`${TRIPO_API_BASE}/task/${encodeURIComponent(taskId)}`, {
    Authorization: `Bearer ${userApiKey}`,
  });
}

function formatCreditsInfo(data) {
  if (data.credits_remaining != null) {
    return `\n(Free credits remaining: ${data.credits_remaining}/${data.credits_total})`;
  }
  if (data.using_own_key) {
    return "\n(Using your own API key — unlimited usage)";
  }
  return "";
}

function formatQuotaExceeded(data) {
  const guide = data.setup_guide || {};
  return [
    `🚀 ${data.message}`,
    "",
    `Step 1: ${guide.step_1}`,
    `Step 2: ${guide.step_2}`,
    `Step 3: ${guide.step_3}`,
    `Step 4: ${guide.step_4}`,
    `Step 5: ${guide.step_5}`,
    "",
    `Platform: ${data.platform_url}`,
    `API Keys: ${data.api_keys_url}`,
  ].join("\n");
}

function formatStatusResponse(data) {
  const task = data.data || data;
  const status = task.status || "unknown";
  const progress = task.progress ?? "N/A";

  if (status === "success" || status === "SUCCESS") {
    const output = task.output || {};
    return {
      task_id: task.task_id,
      status: "SUCCESS",
      progress: 100,
      pbr_model_url: output.pbr_model,
      model_url: output.model,
      base_model_url: output.base_model,
      rendered_image_url: output.rendered_image,
      message: "3D model generated successfully! Use the pbr_model_url to download.",
    };
  }

  const failedStatuses = ["failed", "cancelled", "banned", "expired", "FAILED", "CANCELLED", "BANNED", "EXPIRED"];
  if (failedStatuses.includes(status)) {
    return {
      task_id: task.task_id,
      status: status.toUpperCase(),
      message: `Task ${status}. Try again with a different description.`,
    };
  }

  return {
    task_id: task.task_id,
    status: "IN_PROGRESS",
    progress: `${progress}%`,
    message: `Still generating... (${progress}%). 3D models typically take 30s-3min. Please call status again in a few seconds.`,
  };
}

function directDownloadShape(taskId, data) {
  const inner = data.data || data;
  if (inner.status !== "success" && inner.status !== "SUCCESS") {
    return {
      error: "task_not_ready",
      status: inner.status,
      progress: inner.progress,
    };
  }
  const output = inner.output || {};
  return {
    task_id: taskId,
    status: "SUCCESS",
    pbr_model_url: output.pbr_model,
    model_url: output.model,
    rendered_image_url: output.rendered_image,
    message: "Model ready! Download using the pbr_model_url (recommended) or model_url.",
  };
}

export async function run(params, ctx) {
  const { action } = params;
  const userId = getUserId();
  const userApiKey = ctx.secrets?.TRIPO_API_KEY || undefined;

  if (action === "generate") {
    const { prompt, image_url, files, model_version, format } = params;

    if (!prompt && !image_url && !files) {
      return { error: "Either 'prompt' (for text-to-3D), 'image_url' (for image-to-3D), or 'files' (array of image URLs for multiview-to-3D) is required." };
    }

    const type = files ? "multiview_to_model" : image_url ? "image_to_model" : "text_to_model";

    if (userApiKey) {
      const taskBody = { type, model_version: model_version || "v3.1-20260211" };
      if (prompt) taskBody.prompt = prompt;
      if (image_url) taskBody.image_url = image_url;
      if (files) taskBody.files = files;

      const data = await tripoPostTask(userApiKey, taskBody);
      if (data.code !== 0 && data.code !== undefined) {
        return { error: data.error || "tripo_error", message: data.message || JSON.stringify(data) };
      }
      const taskId = data.data?.task_id || data.task_id;
      if (!taskId) {
        return { error: "tripo_error", message: data.message || "No task_id in Tripo response." };
      }
      return {
        task_id: taskId,
        status: "CREATED",
        message: `3D generation task created! Task ID: ${taskId}. Call action='status' with this task_id to check progress.\n(Using your own API key — direct to Tripo API)`,
      };
    }

    const headers = proxyHeaders(ctx);
    if (!headers) {
      return {
        error: "missing_proxy_secret",
        message:
          "Free tier requires TRIPO_PROXY_SECRET (matches server PROXY_SECRET). Configure: openclaw config set skill.tripo-3d-generation.TRIPO_PROXY_SECRET <secret>. Or set TRIPO_API_KEY to call Tripo directly.",
      };
    }

    const data = await postJson(`${PROXY_BASE}/api/generate`, {
      user_id: userId,
      prompt,
      type,
      image_url,
      files,
      model_version: model_version || "v3.1-20260211",
      format: format || "glb",
    }, headers);

    if (data.error === "quota_exceeded") {
      return { error: "quota_exceeded", message: formatQuotaExceeded(data) };
    }

    if (data.error) {
      return { error: data.error, message: data.message || "Failed to create task." };
    }

    const taskId = data.data?.task_id || data.task_id;
    return {
      task_id: taskId,
      status: "CREATED",
      message: `3D generation task created! Task ID: ${taskId}. Call action='status' with this task_id to check progress.${formatCreditsInfo(data)}`,
    };
  }

  if (action === "status") {
    const { task_id } = params;
    if (!task_id) {
      return { error: "task_id is required for action='status'." };
    }

    if (userApiKey) {
      const data = await tripoGetTask(userApiKey, task_id);
      return formatStatusResponse(data);
    }

    const headers = proxyHeaders(ctx);
    if (!headers) {
      return {
        error: "missing_proxy_secret",
        message: "Configure TRIPO_PROXY_SECRET for free-tier status polling, or TRIPO_API_KEY for direct Tripo access.",
      };
    }

    const data = await getJson(`${PROXY_BASE}/api/status/${task_id}`, headers);
    return formatStatusResponse(data);
  }

  if (action === "download") {
    const { task_id } = params;
    if (!task_id) {
      return { error: "task_id is required for action='download'." };
    }

    if (userApiKey) {
      const data = await tripoGetTask(userApiKey, task_id);
      const shaped = directDownloadShape(task_id, data);
      if (shaped.error) return shaped;
      return shaped;
    }

    const headers = proxyHeaders(ctx);
    if (!headers) {
      return {
        error: "missing_proxy_secret",
        message: "Configure TRIPO_PROXY_SECRET for free-tier download URLs, or TRIPO_API_KEY for direct Tripo access.",
      };
    }

    const data = await getJson(`${PROXY_BASE}/api/download/${task_id}`, headers);

    if (data.error) {
      return data;
    }

    return {
      task_id: data.task_id,
      status: "SUCCESS",
      pbr_model_url: data.pbr_model_url,
      model_url: data.model_url,
      rendered_image_url: data.rendered_image_url,
      message: "Model ready! Download using the pbr_model_url (recommended) or model_url.",
    };
  }

  if (action === "credits") {
    if (userApiKey) {
      return {
        message: "You are using your own Tripo API key — usage is billed by your Tripo account (not the skill free tier).",
        using_own_key: true,
      };
    }

    const headers = proxyHeaders(ctx);
    if (!headers) {
      return {
        error: "missing_proxy_secret",
        message: "Configure TRIPO_PROXY_SECRET to check free credits, or TRIPO_API_KEY if you use your own key.",
      };
    }

    const data = await getJson(`${PROXY_BASE}/api/credits?user_id=${encodeURIComponent(userId)}`, headers);

    if (data.quota_exceeded) {
      return {
        ...data,
        message: `All ${data.credits_total} free credits used. Configure your own API key to continue: openclaw config set skill.tripo-3d-generation.TRIPO_API_KEY <your-key>`,
        get_key_url: "https://platform.tripo3d.ai/api-keys",
      };
    }

    return {
      ...data,
      message: `You have ${data.credits_remaining} free credits remaining out of ${data.credits_total}.`,
    };
  }

  const runTaskProxyOrDirect = async (body) => {
    if (userApiKey) {
      const { user_id: _u, user_api_key: _k, ...tripoBody } = body;
      const data = await tripoPostTask(userApiKey, tripoBody);
      if (data.code !== 0 && data.code !== undefined) {
        return { error: data.error || "tripo_error", message: data.message || JSON.stringify(data) };
      }
      return { data, formatCredits: "\n(Using your own API key — direct to Tripo API)" };
    }
    const headers = proxyHeaders(ctx);
    if (!headers) {
      return {
        error: "missing_proxy_secret",
        message: "Configure TRIPO_PROXY_SECRET for free-tier tasks, or TRIPO_API_KEY for direct Tripo API.",
      };
    }
    const data = await postJson(`${PROXY_BASE}/api/task`, body, headers);
    return { data, formatCredits: formatCreditsInfo(data) };
  };

  if (action === "rig") {
    const { task_id, out_format, spec } = params;
    if (!task_id) {
      return { error: "task_id is required for action='rig'. Provide the task_id of the generated model." };
    }

    const body = { user_id: userId, type: "animate_rig", original_model_task_id: task_id };
    if (out_format) body.out_format = out_format;
    if (spec) body.spec = spec;
    if (userApiKey) body.user_api_key = userApiKey;

    const result = await runTaskProxyOrDirect(body);
    if (result.error) return result;
    const { data, formatCredits } = result;
    if (data.error) return { error: data.error, message: data.message || "Failed to create rig task." };

    const rigTaskId = data.data?.task_id || data.task_id;
    return {
      task_id: rigTaskId,
      status: "CREATED",
      message: `Rig task created! Task ID: ${rigTaskId}. Call action='status' with this task_id to check progress. Once complete, use the rig task_id with action='animate' to apply animations.${formatCredits || ""}`,
    };
  }

  if (action === "animate") {
    const { task_id, animation, out_format, bake_animation } = params;
    if (!task_id) {
      return { error: "task_id is required for action='animate'. Provide the task_id of the RIGGED model (from action='rig')." };
    }
    if (!animation) {
      return { error: "animation is required. Use one of: preset:idle, preset:walk, preset:run, preset:jump, preset:climb, preset:slash, preset:shoot, preset:hurt, preset:fall, preset:turn" };
    }

    const body = { user_id: userId, type: "animate_retarget", original_model_task_id: task_id, animation };
    if (out_format) body.out_format = out_format;
    if (bake_animation != null) body.bake_animation = bake_animation;
    if (userApiKey) body.user_api_key = userApiKey;

    const result = await runTaskProxyOrDirect(body);
    if (result.error) return result;
    const { data, formatCredits } = result;
    if (data.error) return { error: data.error, message: data.message || "Failed to create animate task." };

    const animTaskId = data.data?.task_id || data.task_id;
    return {
      task_id: animTaskId,
      status: "CREATED",
      message: `Animation task created! Task ID: ${animTaskId}. Call action='status' with this task_id to check progress. Note: the model must be rigged first (action='rig') before animating.${formatCredits || ""}`,
    };
  }

  if (action === "prerigcheck") {
    const { task_id } = params;
    if (!task_id) {
      return { error: "task_id is required for action='prerigcheck'." };
    }

    const body = { user_id: userId, type: "animate_prerigcheck", original_model_task_id: task_id };
    if (userApiKey) body.user_api_key = userApiKey;

    const result = await runTaskProxyOrDirect(body);
    if (result.error) return result;
    const { data, formatCredits } = result;
    if (data.error) return { error: data.error, message: data.message || "Failed to create pre-rig check task." };

    const checkTaskId = data.data?.task_id || data.task_id;
    return {
      task_id: checkTaskId,
      status: "CREATED",
      message: `Pre-rig check task created! Task ID: ${checkTaskId}. Call action='status' with this task_id to see if the model can be rigged.${formatCredits || ""}`,
    };
  }

  if (action === "stylize") {
    const { task_id, style, block_size } = params;
    if (!task_id) {
      return { error: "task_id is required for action='stylize'." };
    }
    if (!style) {
      return { error: "style is required. Use one of: lego, voxel, voronoi, minecraft" };
    }

    const body = { user_id: userId, type: "stylize_model", original_model_task_id: task_id, style };
    if (block_size != null) body.block_size = block_size;
    if (userApiKey) body.user_api_key = userApiKey;

    const result = await runTaskProxyOrDirect(body);
    if (result.error) return result;
    const { data, formatCredits } = result;
    if (data.error) return { error: data.error, message: data.message || "Failed to create stylize task." };

    const stylizeTaskId = data.data?.task_id || data.task_id;
    return {
      task_id: stylizeTaskId,
      status: "CREATED",
      message: `Stylize task created (${style})! Task ID: ${stylizeTaskId}. Call action='status' with this task_id to check progress.${formatCredits || ""}`,
    };
  }

  if (action === "convert") {
    const { task_id, convert_format, quad, face_limit, texture_size, force_symmetry } = params;
    if (!task_id) {
      return { error: "task_id is required for action='convert'." };
    }
    if (!convert_format) {
      return { error: "convert_format is required. Use one of: GLTF, USDZ, FBX, OBJ, STL, 3MF" };
    }

    const body = { user_id: userId, type: "convert_model", original_model_task_id: task_id, format: convert_format };
    if (quad != null) body.quad = quad;
    if (face_limit != null) body.face_limit = face_limit;
    if (texture_size != null) body.texture_size = texture_size;
    if (force_symmetry != null) body.force_symmetry = force_symmetry;
    if (userApiKey) body.user_api_key = userApiKey;

    const result = await runTaskProxyOrDirect(body);
    if (result.error) return result;
    const { data, formatCredits } = result;
    if (data.error) return { error: data.error, message: data.message || "Failed to create convert task." };

    const convertTaskId = data.data?.task_id || data.task_id;
    return {
      task_id: convertTaskId,
      status: "CREATED",
      message: `Convert task created (to ${convert_format})! Task ID: ${convertTaskId}. Call action='status' with this task_id to check progress.${formatCredits || ""}`,
    };
  }

  if (action === "texture") {
    const { task_id, texture, pbr, texture_quality, texture_alignment } = params;
    if (!task_id) {
      return { error: "task_id is required for action='texture'." };
    }

    const body = { user_id: userId, type: "texture_model", original_model_task_id: task_id };
    if (texture) body.texture = texture;
    if (pbr != null) body.pbr = pbr;
    if (texture_quality) body.texture_quality = texture_quality;
    if (texture_alignment) body.texture_alignment = texture_alignment;
    if (userApiKey) body.user_api_key = userApiKey;

    const result = await runTaskProxyOrDirect(body);
    if (result.error) return result;
    const { data, formatCredits } = result;
    if (data.error) return { error: data.error, message: data.message || "Failed to create texture task." };

    const textureTaskId = data.data?.task_id || data.task_id;
    return {
      task_id: textureTaskId,
      status: "CREATED",
      message: `Re-texture task created! Task ID: ${textureTaskId}. Call action='status' with this task_id to check progress.${formatCredits || ""}`,
    };
  }

  if (action === "refine") {
    const { task_id } = params;
    if (!task_id) {
      return { error: "task_id is required for action='refine'. Provide the draft model's task_id (only works for models < v2.0)." };
    }

    const body = { user_id: userId, type: "refine_model", draft_model_task_id: task_id };
    if (userApiKey) body.user_api_key = userApiKey;

    const result = await runTaskProxyOrDirect(body);
    if (result.error) return result;
    const { data, formatCredits } = result;
    if (data.error) return { error: data.error, message: data.message || "Failed to create refine task." };

    const refineTaskId = data.data?.task_id || data.task_id;
    return {
      task_id: refineTaskId,
      status: "CREATED",
      message: `Refine task created! Task ID: ${refineTaskId}. Call action='status' with this task_id to check progress. Note: refine only works for draft models generated with versions < v2.0.${formatCredits || ""}`,
    };
  }

  return { error: `Unknown action: '${action}'. Supported actions: generate, status, download, credits, rig, animate, prerigcheck, stylize, convert, texture, refine` };
}
