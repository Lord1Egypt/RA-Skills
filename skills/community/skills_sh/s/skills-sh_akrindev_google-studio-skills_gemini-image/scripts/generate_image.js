#!/usr/bin/env node
"use strict";

import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { parseArgs } from "node:util";

import dotenv from "dotenv";
import { GoogleGenAI, Modality } from "@google/genai";

dotenv.config();

const DEFAULT_MODEL = "gemini-3.1-flash-image-preview";
const DEFAULT_OUTPUT_DIR = "images/";
const DEFAULT_OUTPUT_NAME = "generated_image";
const DEFAULT_ASPECT = "1:1";
const DEFAULT_SIZE = "1K";
const DEFAULT_NUM_IMAGES = 1;
const DEFAULT_PERSON = "allow_adult";

const SUPPORTED_MODELS = [
  "gemini-3.1-flash-image-preview",
  "gemini-3-pro-image-preview",
  "gemini-2.5-flash-image",
  "imagen-4.0-generate-001",
];

const SUPPORTED_PERSON_POLICIES = ["dont_allow", "allow_adult", "allow_all"];

function printUsage() {
  console.log(`Generate images using Gemini/Imagen API.

Usage:
  node scripts/generate_image.js "A futuristic city at sunset"
  node scripts/generate_image.js "Robot with skateboard" --model imagen-4.0-generate-001
  node scripts/generate_image.js "Mountain landscape" --aspect 16:9 --size 2K
  node scripts/generate_image.js "Portrait" --num 4 --output-dir ./my-images/ --name portrait
  node scripts/generate_image.js "Custom folder" --no-timestamp

Options:
  --model, -m         Model ID (default: ${DEFAULT_MODEL})
  --output-dir, -o    Output directory (default: ${DEFAULT_OUTPUT_DIR})
  --name, -n          Base output filename (default: ${DEFAULT_OUTPUT_NAME})
  --no-timestamp      Disable timestamp suffix in filename
  --aspect, -a        Aspect ratio (default: ${DEFAULT_ASPECT})
  --size, -s          Image size (default: ${DEFAULT_SIZE})
  --num               Number of images to generate (1-4, default: ${DEFAULT_NUM_IMAGES})
  --person            Person policy: dont_allow | allow_adult | allow_all (default: ${DEFAULT_PERSON})
  --help, -h          Show this help message

Requirements:
  npm install @google/genai@latest dotenv@latest
`);
}

function getApiKey() {
  const apiKey = process.env.GOOGLE_API_KEY || process.env.GEMINI_API_KEY;
  if (!apiKey) {
    throw new Error("Set GOOGLE_API_KEY or GEMINI_API_KEY environment variable");
  }
  return apiKey;
}

function getBaseFilename(outputName, useTimestamp) {
  if (!useTimestamp) {
    return outputName;
  }

  const now = new Date();
  const yyyy = String(now.getFullYear());
  const mm = String(now.getMonth() + 1).padStart(2, "0");
  const dd = String(now.getDate()).padStart(2, "0");
  const hh = String(now.getHours()).padStart(2, "0");
  const mi = String(now.getMinutes()).padStart(2, "0");
  const ss = String(now.getSeconds()).padStart(2, "0");
  const timestamp = `${yyyy}${mm}${dd}_${hh}${mi}${ss}`;

  return `${outputName}_${timestamp}`;
}

function decodeImageBytes(imageBytes) {
  if (!imageBytes) {
    return null;
  }

  if (typeof imageBytes === "string") {
    return Buffer.from(imageBytes, "base64");
  }

  if (imageBytes instanceof Uint8Array) {
    return Buffer.from(imageBytes);
  }

  if (Array.isArray(imageBytes)) {
    return Buffer.from(imageBytes);
  }

  return null;
}

async function saveImage(outputDir, baseFilename, imageBytes, suffix = "") {
  const filename = path.join(outputDir, `${baseFilename}${suffix}.png`);
  await writeFile(filename, imageBytes);
  console.log(`Saved: ${filename}`);
  return filename;
}

async function generateImage({
  prompt,
  model = DEFAULT_MODEL,
  outputDir = DEFAULT_OUTPUT_DIR,
  outputName = DEFAULT_OUTPUT_NAME,
  aspectRatio = DEFAULT_ASPECT,
  imageSize = DEFAULT_SIZE,
  numImages = DEFAULT_NUM_IMAGES,
  personGeneration = DEFAULT_PERSON,
  useTimestamp = true,
}) {
  const ai = new GoogleGenAI({ apiKey: getApiKey() });

  await mkdir(outputDir, { recursive: true });
  const savedFiles = [];
  const baseFilename = getBaseFilename(outputName, useTimestamp);

  if (model.startsWith("imagen")) {
    const response = await ai.models.generateImages({
      model,
      prompt,
      config: {
        numberOfImages: numImages,
        aspectRatio,
        imageSize,
        personGeneration,
      },
    });

    for (const [index, generatedImage] of (response.generatedImages || []).entries()) {
      const imageBytes = decodeImageBytes(generatedImage?.image?.imageBytes);
      if (!imageBytes) {
        continue;
      }

      const suffix = numImages > 1 ? `_${index}` : "";
      const filePath = await saveImage(outputDir, baseFilename, imageBytes, suffix);
      savedFiles.push(filePath);
    }

    return savedFiles;
  }

  if (model.startsWith("gemini")) {
    const response = await ai.models.generateContent({
      model,
      contents: prompt,
      config: {
        responseModalities: [Modality.IMAGE],
        imageConfig: {
          aspectRatio,
          imageSize,
        },
      },
    });

    const parts = response.candidates?.[0]?.content?.parts || [];
    for (const [index, part] of parts.entries()) {
      const imageBytes = decodeImageBytes(part?.inlineData?.data);
      if (!imageBytes) {
        continue;
      }

      const suffix = parts.length > 1 ? `_${index}` : "";
      const filePath = await saveImage(outputDir, baseFilename, imageBytes, suffix);
      savedFiles.push(filePath);
    }

    return savedFiles;
  }

  throw new Error(`Unknown model ${model}`);
}

function parseCli() {
  const { values, positionals } = parseArgs({
    options: {
      model: { type: "string", short: "m", default: DEFAULT_MODEL },
      "output-dir": { type: "string", short: "o", default: DEFAULT_OUTPUT_DIR },
      name: { type: "string", short: "n", default: DEFAULT_OUTPUT_NAME },
      "no-timestamp": { type: "boolean", default: false },
      aspect: { type: "string", short: "a", default: DEFAULT_ASPECT },
      size: { type: "string", short: "s", default: DEFAULT_SIZE },
      num: { type: "string", default: String(DEFAULT_NUM_IMAGES) },
      person: { type: "string", default: DEFAULT_PERSON },
      help: { type: "boolean", short: "h", default: false },
    },
    allowPositionals: true,
  });

  if (values.help) {
    printUsage();
    process.exit(0);
  }

  if (positionals.length === 0) {
    printUsage();
    process.exit(1);
  }

  const prompt = positionals.join(" ");
  const numImages = Number(values.num);

  if (Number.isNaN(numImages) || numImages < 1 || numImages > 4) {
    throw new Error("--num must be an integer between 1 and 4");
  }

  if (!SUPPORTED_MODELS.includes(values.model)) {
    throw new Error(`Unsupported model '${values.model}'. Use one of: ${SUPPORTED_MODELS.join(", ")}`);
  }

  if (!SUPPORTED_PERSON_POLICIES.includes(values.person)) {
    throw new Error(
      `Unsupported --person '${values.person}'. Use one of: ${SUPPORTED_PERSON_POLICIES.join(", ")}`,
    );
  }

  return {
    prompt,
    model: values.model,
    outputDir: values["output-dir"],
    outputName: values.name,
    aspectRatio: values.aspect,
    imageSize: values.size,
    numImages,
    personGeneration: values.person,
    useTimestamp: !values["no-timestamp"],
  };
}

async function main() {
  try {
    const options = parseCli();
    const files = await generateImage(options);
    console.log(`\nGenerated ${files.length} image(s)`);
  } catch (error) {
    console.error(`Error: ${error instanceof Error ? error.message : String(error)}`);
    process.exit(1);
  }
}

await main();
