import https from "https";
import http from "http";
import { URL } from "url";
import fs from "fs";
import path from "path";

export interface QuantumMessage {
  type: "text" | "image" | "file" | "news";
  textMsg?: {
    content: string;
    isMentioned?: boolean;
    mentionType?: 1 | 2;
    mentionedMobileList?: string[];
  };
  imageMsg?: {
    fileId: string;
    height?: number;
    width?: number;
  };
  fileMsg?: {
    fileId: string;
    id?: string;
    name?: string;
    type?: string;
    size?: string | number;
  };
  news?: {
    info: {
      title: string;
      description?: string;
      url: string;
      picUrl?: string;
    };
  };
}

export interface UploadResult {
  id: string;
  name: string;
  type: string;
  size: number | string;
}

export interface SendResult {
  messageId: string;
}

export class QuantumImApi {
  private static readonly MAX_FILE_SIZE_BYTES = 30 * 1024 * 1024;
  private static readonly MAX_MESSAGES_PER_MINUTE = 20;

  private robotId: string;
  private key: string;
  private host: string;
  private sendTimestamps: number[] = [];
  private rateLimitChain: Promise<void> = Promise.resolve();

  constructor(config: { robotId: string; key: string; host: string }) {
    this.robotId = config.robotId;
    this.key = config.key;
    this.host = config.host;
  }

  async sendText(
    target: string,
    content: string,
    groupId?: string,
  ): Promise<SendResult> {
    const isGroup = Boolean(groupId);
    
    const payload: QuantumMessage = {
      type: "text",
      textMsg: {
        content,
        isMentioned: isGroup,
        mentionType: isGroup ? 2 : undefined,
        mentionedMobileList: isGroup ? [target] : undefined,
      },
    };

    return this.sendRequest(payload);
  }

  async sendImage(
    target: string,
    filePath: string,
    groupId?: string,
  ): Promise<SendResult> {
    const uploadResult = await this.uploadFile(filePath, 1);
    const { width, height } = this.resolveImageDimensions(filePath);
    
    const payload: QuantumMessage = {
      type: "image",
      imageMsg: {
        fileId: uploadResult.id,
        width,
        height,
      },
    };

    return this.sendRequest(payload);
  }

  async sendFile(
    target: string,
    filePath: string,
    groupId?: string,
  ): Promise<SendResult> {
    const uploadResult = await this.uploadFile(filePath, 2);
    
    const payload: QuantumMessage = {
      type: "file",
      fileMsg: {
        fileId: uploadResult.id,
        id: uploadResult.id,
        name: uploadResult.name,
        type: uploadResult.type,
        size: uploadResult.size,
      },
    };

    return this.sendRequest(payload);
  }

  async uploadFile(filePath: string, fileType: 1 | 2): Promise<UploadResult> {
    return new Promise((resolve, reject) => {
      const url = new URL(`${this.host}/im-external/v1/webhook/upload-attachment?key=${this.key}&type=${fileType}`);

      console.log(`[quantum-im] upload start type=${fileType} path=${filePath}`);

      const stat = fs.statSync(filePath);
      if (stat.size > QuantumImApi.MAX_FILE_SIZE_BYTES) {
        reject(new Error(`File too large: ${stat.size} bytes (limit: ${QuantumImApi.MAX_FILE_SIZE_BYTES} bytes)`));
        return;
      }

      const fileContent = fs.readFileSync(filePath);
      const fileName = filePath.split(/[\\/]/).pop() || "unknown";
      
      const boundary = "----WebKitFormBoundary" + Math.random().toString(36).substring(2);
      const bodyParts = [
        `--${boundary}`,
        `Content-Disposition: form-data; name="file"; filename="${fileName}"`,
        `Content-Type: application/octet-stream`,
        "",
        "",
      ];
      
      const header = Buffer.from(bodyParts.join("\r\n") + "\r\n");
      const footer = Buffer.from("\r\n--" + boundary + "--\r\n");
      const body = Buffer.concat([header, fileContent, footer]);

      const options = {
        hostname: url.hostname,
        port: url.port || (url.protocol === "https:" ? 443 : 80),
        path: url.pathname + url.search,
        method: "POST",
        headers: {
          "Content-Type": `multipart/form-data; boundary=${boundary}`,
          "Content-Length": body.length,
        },
      };

      const lib = url.protocol === "https:" ? https : http;
      const req = lib.request(options, (res) => {
        let data = "";
        res.on("data", (chunk) => (data += chunk));
        res.on("end", () => {
          try {
            console.log(`[quantum-im] upload response status=${res.statusCode ?? "unknown"} body=${data}`);
            const response = JSON.parse(data);
            if (response.ok && response.code === 200 && response.data) {
              resolve(response.data as UploadResult);
            } else {
              reject(new Error(`Upload failed: ${response.message || data}`));
            }
          } catch (e) {
            reject(new Error(`Parse error: ${data}`));
          }
        });
      });

      req.on("error", reject);
      req.write(body);
      req.end();
    });
  }

  private sendRequest(payload: QuantumMessage): Promise<SendResult> {
    return this.withRateLimit(async () => {
      return new Promise((resolve, reject) => {
        const url = new URL(`${this.host}/im-external/v1/webhook/send?key=${this.key}`);
        
        const body = JSON.stringify(payload);
        const options = {
          hostname: url.hostname,
          port: url.port || (url.protocol === "https:" ? 443 : 80),
          path: url.pathname + url.search,
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Content-Length": Buffer.byteLength(body),
          },
        };

        const lib = url.protocol === "https:" ? https : http;
        const req = lib.request(options, (res) => {
          let data = "";
          res.on("data", (chunk) => (data += chunk));
          res.on("end", () => {
            console.log(`[quantum-im] send response status=${res.statusCode ?? "unknown"} payloadType=${payload.type} body=${data}`);
            try {
              const response = data ? JSON.parse(data) : undefined;
              const httpOk = Boolean(res.statusCode && res.statusCode >= 200 && res.statusCode < 300);
              const bizOk = !response || (response.ok === true && response.code === 200);
              if (httpOk && bizOk) {
                resolve({ messageId: Date.now().toString() });
                return;
              }
              const reason = response?.message || data || `HTTP ${res.statusCode}`;
              reject(new Error(`Send failed: ${reason}`));
            } catch {
              if (res.statusCode && res.statusCode >= 200 && res.statusCode < 300) {
                resolve({ messageId: Date.now().toString() });
              } else {
                reject(new Error(`HTTP ${res.statusCode}: ${data}`));
              }
            }
          });
        });

        req.on("error", reject);
        req.write(body);
        req.end();
      });
    });
  }

  private async withRateLimit<T>(fn: () => Promise<T>): Promise<T> {
    const run = async () => {
      await this.enforceRateLimit();
      return fn();
    };
    const next = this.rateLimitChain.then(run, run);
    this.rateLimitChain = next.then(() => undefined, () => undefined);
    return next;
  }

  private async enforceRateLimit(): Promise<void> {
    while (true) {
      const now = Date.now();
      this.sendTimestamps = this.sendTimestamps.filter((ts) => now - ts < 60_000);
      if (this.sendTimestamps.length < QuantumImApi.MAX_MESSAGES_PER_MINUTE) {
        this.sendTimestamps.push(now);
        return;
      }
      const waitMs = 60_000 - (now - this.sendTimestamps[0]) + 50;
      await new Promise((r) => setTimeout(r, Math.max(waitMs, 50)));
    }
  }

  private resolveImageDimensions(filePath: string): { width: number; height: number } {
    const ext = path.extname(filePath).toLowerCase();
    const buf = fs.readFileSync(filePath);

    if (ext === ".png" && buf.length >= 24) {
      return { width: buf.readUInt32BE(16), height: buf.readUInt32BE(20) };
    }

    if ((ext === ".jpg" || ext === ".jpeg") && buf.length > 4) {
      let offset = 2;
      while (offset + 9 < buf.length) {
        if (buf[offset] !== 0xff) {
          offset += 1;
          continue;
        }
        const marker = buf[offset + 1];
        const size = buf.readUInt16BE(offset + 2);
        if (size < 2) break;
        if (
          marker === 0xc0 || marker === 0xc1 || marker === 0xc2 ||
          marker === 0xc3 || marker === 0xc5 || marker === 0xc6 ||
          marker === 0xc7 || marker === 0xc9 || marker === 0xca ||
          marker === 0xcb || marker === 0xcd || marker === 0xce ||
          marker === 0xcf
        ) {
          return {
            height: buf.readUInt16BE(offset + 5),
            width: buf.readUInt16BE(offset + 7),
          };
        }
        offset += 2 + size;
      }
    }

    if (ext === ".gif" && buf.length >= 10) {
      return { width: buf.readUInt16LE(6), height: buf.readUInt16LE(8) };
    }

    if (ext === ".webp" && buf.length >= 30 && buf.toString("ascii", 0, 4) === "RIFF" && buf.toString("ascii", 8, 12) === "WEBP") {
      const chunk = buf.toString("ascii", 12, 16);
      if (chunk === "VP8X") {
        const width = 1 + buf.readUIntLE(24, 3);
        const height = 1 + buf.readUIntLE(27, 3);
        return { width, height };
      }
    }

    throw new Error(`Unsupported image dimension format: ${filePath}`);
  }
}
