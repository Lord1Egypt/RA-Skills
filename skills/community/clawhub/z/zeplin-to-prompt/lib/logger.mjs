import fs from "node:fs";

const stamp = () => new Date().toISOString().replace("T", " ").replace("Z", "");

export const createLogger = (quiet = false) => {
  const logFilePath = process.env.ZEPLIN_LOG_FILE || process.env.LOG_FILE || process.env.log_file;
  let fileStream = null;
  const writeToFile = (line) => {
    if (!logFilePath) return;
    try {
      if (!fileStream) {
        fileStream = fs.createWriteStream(logFilePath, { flags: "a" });
      }
      fileStream.write(line + "\n");
    } catch {
      // ignore file logging errors
    }
  };

  return (...args) => {
    const line = `[${stamp()}] ${args.map(arg => {
      if (typeof arg === "string") return arg;
      try {
        return JSON.stringify(arg);
      } catch {
        return String(arg);
      }
    }).join(" ")}`;
    if (!quiet) console.log(line);
    writeToFile(line);
  };
};

export { stamp };
