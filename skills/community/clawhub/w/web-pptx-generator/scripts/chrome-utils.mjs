import { execFileSync } from "node:child_process";

export const DEFAULT_CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";

export function renderHtmlToPng({
  chromePath = process.env.CHROME_BIN || DEFAULT_CHROME,
  inputUrl,
  outputPath,
  width = 1600,
  height = 900,
  fullPage = false,
}) {
  const args = [
    "--headless=new",
    "--disable-gpu",
    "--no-first-run",
    "--no-default-browser-check",
    "--allow-file-access-from-files",
    `--window-size=${width},${height}`,
    `--screenshot=${outputPath}`,
  ];

  if (fullPage) args.push("--hide-scrollbars");
  args.push(inputUrl);

  try {
    execFileSync(chromePath, args, {
      stdio: ["ignore", "pipe", "pipe"],
      encoding: "utf8",
    });
  } catch (error) {
    const stderr = String(error?.stderr || "").trim();
    const stdout = String(error?.stdout || "").trim();
    throw new Error(`Chrome preview render failed.${stderr ? `\n${stderr}` : stdout ? `\n${stdout}` : ""}`);
  }
}
