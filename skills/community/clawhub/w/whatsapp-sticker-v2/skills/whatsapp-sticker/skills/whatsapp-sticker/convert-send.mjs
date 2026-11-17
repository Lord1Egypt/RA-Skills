
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { randomUUID, createHash } from "node:crypto";
import { execFile } from "node:child_process";
import { promisify } from "node:util";

const exec = promisify(execFile);

const [sourceArg, chatId] = process.argv.slice(2);

const bridgeUrl = (
  process.env.WHATSAPP_BRIDGE_URL || "http://127.0.0.1:3000"
).replace(/\/+$/, "");

const bridgeFile =
  process.env.WHATSAPP_BRIDGE_FILE ||
  path.join(
    os.homedir(),
    ".hermes/hermes-agent/scripts/whatsapp-bridge/bridge.js"
  );

const checkHash = process.env.WHATSAPP_CHECK_BRIDGE_HASH !== "false";
const output = path.join(os.tmpdir(), `sticker-${randomUUID()}.webp`);
const maxStickerSize = 100 * 1024;

async function requestJson(url, options = {}) {
  const response = await fetch(url, {
    ...options,
    signal: AbortSignal.timeout(15000)
  });

  const body = await response.text();
  let result;

  try {
    result = JSON.parse(body);
  } catch {
    throw new Error(`Bridge mengembalikan respons yang tidak valid (${response.status}).`);
  }

  if (!response.ok) {
    throw new Error(
      result.error || result.message || `Permintaan bridge gagal (${response.status}).`
    );
  }

  return result;
}

async function main() {
  if (!sourceArg || !chatId) {
    throw new Error(
      "Gunakan: node convert-send.mjs /path/foto.jpg ID_CHAT"
    );
  }

  const source = path.resolve(sourceArg);

  if (!fs.existsSync(source) || !fs.statSync(source).isFile()) {
    throw new Error("File sumber tidak ditemukan atau bukan file biasa.");
  }

  if (!/^[A-Za-z0-9._:-]+@[A-Za-z0-9.-]+$/.test(chatId)) {
    throw new Error("Format ID chat tidak valid.");
  }

  await exec("ffmpeg", ["-version"]);

  const health = await requestJson(`${bridgeUrl}/health`);

  if (health.status !== "connected") {
    throw new Error("Bridge WhatsApp belum terhubung.");
  }

  if (checkHash) {
    if (!fs.existsSync(bridgeFile)) {
      throw new Error(
        "File bridge tidak ditemukan. Atur WHATSAPP_BRIDGE_FILE ke lokasi bridge.js yang benar, atau nonaktifkan pemeriksaan hash hanya jika bridge sudah dipercaya."
      );
    }

    if (!health.scriptHash) {
      throw new Error(
        "Bridge tidak menyediakan scriptHash. Periksa kompatibilitas bridge atau atur WHATSAPP_CHECK_BRIDGE_HASH=false jika kamu mempercayai bridge tersebut."
      );
    }

    const diskHash = createHash("sha256")
      .update(fs.readFileSync(bridgeFile))
      .digest("hex")
      .slice(0, 16);

    if (health.scriptHash !== diskHash) {
      throw new Error(
        "Hash bridge aktif berbeda dari file di disk. Perbarui atau mulai ulang bridge, lalu coba lagi."
      );
    }
  }

  let converted = false;

  for (const quality of [70, 55, 40, 25, 15]) {
    await exec("ffmpeg", [
      "-y",
      "-v", "error",
      "-i", source,
      "-frames:v", "1",
      "-vf",
      "scale=512:512:force_original_aspect_ratio=decrease:flags=lanczos,pad=512:512:(ow-iw)/2:(oh-ih)/2:color=0x00000000,format=yuva420p",
      "-c:v", "libwebp",
      "-quality", String(quality),
      "-compression_level", "6",
      output
    ]);

    if (fs.existsSync(output) && fs.statSync(output).size <= maxStickerSize) {
      converted = true;
      break;
    }
  }

  if (!converted) {
    throw new Error("Stiker gagal dikonversi di bawah batas 100 KB.");
  }

  const result = await requestJson(`${bridgeUrl}/send-media`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      chatId,
      filePath: output,
      mediaType: "sticker"
    })
  });

  if (!result.success) {
    throw new Error(result.error || "Bridge gagal mengirim stiker.");
  }

  console.log("Permintaan pengiriman stiker berhasil:", result.messageId || "(ID pesan tidak tersedia)");
}

main()
  .catch(error => {
    console.error("GAGAL:", error.message);
    process.exitCode = 1;
  })
  .finally(() => {
    fs.rmSync(output, { force: true });
  });

