#!/usr/bin/env node

import { access, mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";
import { parseArgs } from "node:util";
import { chromium } from "playwright-core";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const SKILL_DIR = path.resolve(__dirname, "..");
const DEFAULT_LOGIN_URL = "https://doc.weixin.qq.com/home/recent";
const DEFAULT_OUTPUT_DIR = path.join(SKILL_DIR, ".outputs");
const DEFAULT_PROFILE_DIR = path.join(SKILL_DIR, ".state", "chrome-profile");
const DEFAULT_QR_PATH = path.join(DEFAULT_OUTPUT_DIR, "wecom-login-qr.png");

function printHelp() {
  console.log(`wecom-drive-browser

用法：
  node ./scripts/wecom-drive-browser.mjs [选项]

选项：
  --url <url>           目标文件、文件夹或登录页面链接
  --qr-path <path>      需要登录时，把二维码截图保存到这里；未指定时默认覆盖 .outputs/wecom-login-qr.png
  --json-path <path>    把 JSON 结果保存到文件
  --profile-dir <path>  持久化浏览器配置目录
  --timeout-ms <n>      导航或等待超时时间，单位毫秒
  --wait-for-login      轮询等待登录完成，直到超时
  --keep-open           输出结果后保持浏览器不关闭；处理二维码登录时建议启用
  --headed              显示浏览器窗口，而不是无头模式
  --help                打印这段帮助信息
`);
}

function cleanText(value) {
  return String(value || "").replace(/\s+/g, " ").trim();
}

async function pathExists(filePath) {
  try {
    await access(filePath);
    return true;
  } catch {
    return false;
  }
}

async function ensureParentDir(filePath) {
  await mkdir(path.dirname(filePath), { recursive: true });
}

function defaultQrPath() {
  return DEFAULT_QR_PATH;
}

async function resolveBrowserExecutable() {
  const candidates = [
    process.env.WECOM_DRIVE_BROWSER_PATH,
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
  ].filter(Boolean);

  for (const candidate of candidates) {
    if (await pathExists(candidate)) {
      return candidate;
    }
  }

  throw new Error(
    "未找到受支持的浏览器可执行文件。请把 WECOM_DRIVE_BROWSER_PATH 设置为 Chrome 或 Chromium 的路径。"
  );
}

async function safePageText(page) {
  try {
    const text = await page.locator("body").innerText({ timeout: 5000 });
    return cleanText(text);
  } catch {
    return "";
  }
}

async function safeFrameSrcs(page) {
  try {
    return await page.locator("iframe").evaluateAll((nodes) =>
      nodes
        .map((node) => node.getAttribute("src") || "")
        .filter((value) => Boolean(value))
    );
  } catch {
    return [];
  }
}

async function captureQrScreenshot(page, qrPath) {
  await ensureParentDir(qrPath);

  const candidates = [
    page.frameLocator("iframe").locator("img, canvas").first(),
    page.locator("iframe").first(),
    page.locator("img[src*='qrcode'], img[src*='qr'], canvas").first(),
    page.locator("main").first(),
  ];

  for (const locator of candidates) {
    try {
      if ((await locator.count()) > 0 && (await locator.first().isVisible())) {
        await locator.first().screenshot({ path: qrPath });
        return qrPath;
      }
    } catch {
      continue;
    }
  }

  await page.screenshot({ path: qrPath, fullPage: false });
  return qrPath;
}

async function detectState(page) {
  const currentUrl = page.url();
  const title = await page.title().catch(() => "");
  const pageText = await safePageText(page);
  const frameSrcs = await safeFrameSrcs(page);
  const loginByUrl =
    /\/wework_admin\/loginpage_wx/.test(currentUrl) ||
    /\/scenario\/login\.html/.test(currentUrl) ||
    (/\/home\/recent/.test(currentUrl) &&
      /企业微信扫码登录|扫码登录|微信扫码登录|企业身份登录/.test(pageText));
  const loginByText = /企业微信扫码登录|扫码登录|微信扫码登录|企业身份登录/.test(
    pageText
  );
  const desktopConfirmationRequired = /请在桌面端确认登[录陆]|桌面端确认登[录陆]|无法扫码/.test(
    pageText
  );
  const loginByFrame = frameSrcs.some(
    (src) => src.includes("/wwqrlogin/") || src.includes("login_qrcode")
  );
  const loginRequired = loginByUrl || loginByText || loginByFrame;

  const textHints = pageText
    .split(/(?<=。)|\n/)
    .map((item) => cleanText(item))
    .filter(Boolean)
    .slice(0, 12);

  return {
    loginRequired,
    desktopConfirmationRequired,
    currentUrl,
    title,
    frameSrcs,
    textHints,
  };
}

async function extractLinks(page, limit) {
  try {
    return await page.evaluate((maxLinks) => {
      const seen = new Set();
      const items = [];

      for (const anchor of document.querySelectorAll("a[href]")) {
        const text = (anchor.textContent || "").replace(/\s+/g, " ").trim();
        const href = anchor.href || anchor.getAttribute("href") || "";
        if (!href) continue;

        const key = `${text}::${href}`;
        if (seen.has(key)) continue;
        seen.add(key);

        items.push({ text, href });
        if (items.length >= maxLinks) break;
      }

      return items;
    }, limit);
  } catch {
    return [];
  }
}

async function extractEditableElements(page, limit) {
  try {
    return await page.evaluate((maxItems) => {
      const selectors = [
        "[contenteditable='true']",
        "textarea",
        "input:not([type='hidden'])",
      ];

      return Array.from(document.querySelectorAll(selectors.join(",")))
        .map((node) => ({
          tag: node.tagName.toLowerCase(),
          name: node.getAttribute("name") || "",
          placeholder: node.getAttribute("placeholder") || "",
          ariaLabel: node.getAttribute("aria-label") || "",
          text: (node.textContent || "").replace(/\s+/g, " ").trim().slice(0, 80),
        }))
        .filter(
          (item) =>
            item.name || item.placeholder || item.ariaLabel || item.text || item.tag === "textarea"
        )
        .slice(0, maxItems);
    }, limit);
  } catch {
    return [];
  }
}

async function collectPageSummary(page) {
  return {
    links: await extractLinks(page, 30),
    editableElements: await extractEditableElements(page, 20),
  };
}

async function waitForLogin(page, timeoutMs) {
  const startedAt = Date.now();

  while (Date.now() - startedAt < timeoutMs) {
    await page.waitForTimeout(1500);
    const state = await detectState(page);
    if (!state.loginRequired) {
      return {
        status: "ready",
        timedOut: false,
        state,
      };
    }
  }

  return {
    status: "login_timeout",
    timedOut: true,
    state: await detectState(page),
  };
}

async function keepContextAlive(context) {
  return new Promise((resolve) => {
    let settled = false;
    const finish = () => {
      if (!settled) {
        settled = true;
        resolve();
      }
    };

    context.on("close", finish);

    const interval = setInterval(async () => {
      try {
        if (context.pages().length === 0) {
          clearInterval(interval);
          finish();
          return;
        }

        await context.pages()[0].waitForTimeout(1000);
      } catch {
        clearInterval(interval);
        finish();
      }
    }, 1000);
  });
}

async function main() {
  const { values } = parseArgs({
    args: process.argv.slice(2),
    options: {
      url: { type: "string" },
      "qr-path": { type: "string" },
      "json-path": { type: "string" },
      "profile-dir": { type: "string" },
      "timeout-ms": { type: "string" },
      "wait-for-login": { type: "boolean" },
      "keep-open": { type: "boolean" },
      headed: { type: "boolean" },
      help: { type: "boolean" },
    },
    allowPositionals: false,
  });

  if (values.help) {
    printHelp();
    return;
  }

  const targetUrl = values.url || DEFAULT_LOGIN_URL;
  const timeoutMs = Number.parseInt(values["timeout-ms"] || "30000", 10);
  const qrPath = values["qr-path"] || defaultQrPath();
  const jsonPath = values["json-path"];
  const profileDir = values["profile-dir"] || DEFAULT_PROFILE_DIR;
  const headed = Boolean(values.headed);
  const keepOpen = Boolean(values["keep-open"]);

  let context;
  try {
    const executablePath = await resolveBrowserExecutable();
    await mkdir(profileDir, { recursive: true });
    await mkdir(DEFAULT_OUTPUT_DIR, { recursive: true });

    context = await chromium.launchPersistentContext(profileDir, {
      executablePath,
      headless: !headed,
      viewport: { width: 1440, height: 960 },
      locale: "zh-CN",
      args: ["--disable-dev-shm-usage"],
    });

    const page = context.pages()[0] || (await context.newPage());
    await page.goto(targetUrl, {
      waitUntil: "domcontentloaded",
      timeout: timeoutMs,
    });
    await page.waitForLoadState("networkidle", { timeout: 5000 }).catch(() => {});

    const state = await detectState(page);
    const result = {
      status: state.loginRequired
        ? state.desktopConfirmationRequired
          ? "desktop_confirm_required"
          : "login_required"
        : "ready",
      targetUrl,
      currentUrl: state.currentUrl,
      title: state.title,
      loginRequired: state.loginRequired,
      desktopConfirmationRequired: state.desktopConfirmationRequired,
      loginHint: state.loginRequired
        ? state.desktopConfirmationRequired
          ? "当前登录页要求在企业微信桌面端确认登录，不能只靠扫码完成。"
          : "当前页面需要扫码登录。"
        : null,
      qrPath: null,
      profileDir,
      page: {
        textHints: state.textHints,
        links: [],
        editableElements: [],
      },
    };

    if (state.loginRequired) {
      result.qrPath = await captureQrScreenshot(page, qrPath);
      if (values["wait-for-login"]) {
        const waitResult = await waitForLogin(page, timeoutMs);
        result.status = waitResult.status;
        result.currentUrl = waitResult.state.currentUrl;
        result.title = waitResult.state.title;
        result.loginRequired = waitResult.state.loginRequired;
        result.desktopConfirmationRequired =
          waitResult.state.desktopConfirmationRequired;
        result.loginHint = waitResult.state.loginRequired
          ? waitResult.state.desktopConfirmationRequired
            ? "当前登录页要求在企业微信桌面端确认登录，不能只靠扫码完成。"
            : "当前页面需要扫码登录。"
          : null;
        result.page.textHints = waitResult.state.textHints;
      }
    }

    if (!result.loginRequired) {
      const summary = await collectPageSummary(page);
      result.page.links = summary.links;
      result.page.editableElements = summary.editableElements;
    }

    const output = `${JSON.stringify(result, null, 2)}\n`;
    process.stdout.write(output);

    if (jsonPath) {
      await ensureParentDir(jsonPath);
      await writeFile(jsonPath, output, "utf8");
    }

    if (keepOpen) {
      process.stdout.write("浏览器保持打开状态，等待手动关闭。\n");
      await keepContextAlive(context);
      context = null;
    }
  } finally {
    if (context) {
      await context.close();
    }
  }
}

main().catch((error) => {
  const result = {
    status: "error",
    error: error instanceof Error ? error.message : String(error),
  };
  process.stderr.write(`${JSON.stringify(result, null, 2)}\n`);
  process.exitCode = 1;
});
