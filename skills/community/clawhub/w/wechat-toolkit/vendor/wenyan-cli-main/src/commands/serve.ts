import express, { Request, Response, NextFunction } from "express";
import fs from "node:fs/promises";
import path from "node:path";
import crypto from "node:crypto";
import { configDir } from "@wenyan-md/core/wrapper";
import multer from "multer";
import { publishToWechatDraft } from "@wenyan-md/core/publish";
import {
    countWechatDrafts,
    deleteWechatDraft,
    deleteWechatPublishedArticle,
    getWechatDraft,
    getWechatPublishStatus,
    getWechatPublishedArticle,
    listWechatDrafts,
    listWechatPublishedArticles,
    submitWechatDraftPublish,
} from "../wechat-admin.js";

export interface ServeOptions {
    port?: number;
    version?: string;
    apiKey?: string;
}

interface RenderRequest {
    fileId: string;
    theme?: string;
    highlight?: string;
    customTheme?: string;
    macStyle?: boolean;
    footnote?: boolean;
}

interface MediaIdRequest {
    mediaId?: string;
    media_id?: string;
}

interface PublishStatusRequest {
    publishId?: string;
    publish_id?: string;
}

interface ArticleIdRequest {
    articleId?: string;
    article_id?: string;
    index?: number;
}

interface ListRequest {
    offset?: number;
    count?: number;
    noContent?: boolean | number;
    no_content?: boolean | number;
}

class AppError extends Error {
    constructor(public message: string) {
        super(message);
        this.name = "AppError";
    }
}

const UPLOAD_TTL_MS = 10 * 60 * 1000;
const UPLOAD_DIR = path.join(configDir, "uploads");

export async function serveCommand(options: ServeOptions) {
    await fs.mkdir(UPLOAD_DIR, { recursive: true });

    cleanupOldUploads();
    setInterval(cleanupOldUploads, UPLOAD_TTL_MS).unref();

    const app = express();
    const port = options.port || 3000;
    const auth = createAuthHandler(options);

    app.use(express.json({ limit: "10mb" }));

    const storage = multer.diskStorage({
        destination: (_req, _file, cb) => {
            cb(null, UPLOAD_DIR);
        },
        filename: (_req, file, cb) => {
            const fileId = crypto.randomUUID();
            const ext = file.originalname.split(".").pop() || "";
            cb(null, ext ? `${fileId}.${ext}` : fileId);
        },
    });

    const upload = multer({
        storage,
        limits: {
            fileSize: 10 * 1024 * 1024,
        },
        fileFilter: (_req, file, cb) => {
            const ext = file.originalname.split(".").pop()?.toLowerCase();
            const allowedImageTypes = ["image/jpeg", "image/png", "image/gif", "image/webp", "image/svg+xml"];
            const allowedImageExts = ["jpg", "jpeg", "png", "gif", "webp", "svg"];

            const isImage = allowedImageTypes.includes(file.mimetype) || Boolean(ext && allowedImageExts.includes(ext));
            const isMarkdown = ext === "md" || file.mimetype === "text/markdown" || file.mimetype === "text/plain";
            const isCss = ext === "css" || file.mimetype === "text/css";
            const isJson = ext === "json" || file.mimetype === "application/json";

            if (isImage || isMarkdown || isCss || isJson) {
                cb(null, true);
            } else {
                cb(new AppError("不支持的文件类型，仅支持图片、Markdown、CSS 和 JSON 文件"));
            }
        },
    });

    app.get("/health", (_req: Request, res: Response) => {
        res.json({ status: "ok", service: "wenyan-cli", version: options.version || "unknown" });
    });

    app.get("/verify", auth, (_req: Request, res: Response) => {
        res.json({ success: true, message: "Authorized" });
    });

    app.post("/publish", auth, async (req: Request, res: Response) => {
        const body: RenderRequest = req.body;
        validateRenderRequest(body);

        const files = await fs.readdir(UPLOAD_DIR);
        const matchedFile = files.find((f) => f === body.fileId);

        if (!matchedFile) {
            throw new AppError(`文件不存在或已过期，请重新上传 (ID: ${body.fileId})`);
        }

        const ext = path.extname(matchedFile).toLowerCase();
        if (ext !== ".json") {
            throw new AppError("请提供 JSON 文件的 fileId，不能直接发布图片文件");
        }

        const filePath = path.join(UPLOAD_DIR, matchedFile);
        const fileContent = await fs.readFile(filePath, "utf-8");
        const gzhContent = JSON.parse(fileContent);

        if (!gzhContent.title) throw new AppError("未能找到文章标题");

        const resolveAssetPath = (assetUrl: string) => {
            const assetFileId = assetUrl.replace("asset://", "");
            const matchedAsset = files.find((f) => f === assetFileId || path.parse(f).name === assetFileId);
            return matchedAsset ? path.join(UPLOAD_DIR, matchedAsset) : assetUrl;
        };

        gzhContent.content = gzhContent.content.replace(
            /(<img\b[^>]*?\bsrc\s*=\s*["'])(asset:\/\/[^"']+)(["'])/gi,
            (_match: string, prefix: string, assetUrl: string, suffix: string) =>
                prefix + resolveAssetPath(assetUrl) + suffix,
        );

        if (gzhContent.cover && gzhContent.cover.startsWith("asset://")) {
            gzhContent.cover = resolveAssetPath(gzhContent.cover);
        }

        const data = await publishToWechatDraft({
            title: gzhContent.title,
            content: gzhContent.content,
            cover: gzhContent.cover,
            author: gzhContent.author,
            source_url: gzhContent.source_url,
        });

        if (data.media_id) {
            res.json({ media_id: data.media_id });
        } else {
            throw new AppError(`发布到微信公众号失败，\n${data}`);
        }
    });

    app.post("/draft/get", auth, async (req: Request, res: Response) => {
        const mediaId = getMediaId(req.body ?? {});
        const data = await getWechatDraft(mediaId);
        res.json(data);
    });

    app.post("/draft/list", auth, async (req: Request, res: Response) => {
        const listOptions = normalizeListRequest(req.body ?? {});
        const data = await listWechatDrafts(listOptions);
        res.json(data);
    });

    app.post("/draft/count", auth, async (_req: Request, res: Response) => {
        const data = await countWechatDrafts();
        res.json(data);
    });

    app.post("/draft/delete", auth, async (req: Request, res: Response) => {
        const mediaId = getMediaId(req.body ?? {});
        const data = await deleteWechatDraft(mediaId);
        res.json(data);
    });

    app.post("/draft/publish", auth, async (req: Request, res: Response) => {
        const mediaId = getMediaId(req.body ?? {});
        const data = await submitWechatDraftPublish(mediaId);
        res.json(data);
    });

    app.post("/publish/status", auth, async (req: Request, res: Response) => {
        const body = (req.body ?? {}) as PublishStatusRequest;
        const publishId = body.publishId ?? body.publish_id;
        validateStringField(publishId, "publishId");

        const data = await getWechatPublishStatus(publishId);
        res.json(data);
    });

    app.post("/published/list", auth, async (req: Request, res: Response) => {
        const listOptions = normalizeListRequest(req.body ?? {});
        const data = await listWechatPublishedArticles(listOptions);
        res.json(data);
    });

    app.post("/published/get", auth, async (req: Request, res: Response) => {
        const articleId = getArticleId(req.body ?? {});
        const data = await getWechatPublishedArticle(articleId);
        res.json(data);
    });

    app.post("/published/delete", auth, async (req: Request, res: Response) => {
        const body = (req.body ?? {}) as ArticleIdRequest;
        const articleId = getArticleId(body);
        const index = body.index ?? 0;
        validateNonNegativeInteger(index, "index");

        const data = await deleteWechatPublishedArticle(articleId, index);
        res.json(data);
    });

    app.post("/upload", auth, upload.single("file"), async (req: Request, res: Response) => {
        if (!req.file) {
            throw new AppError("未找到上传的文件");
        }

        const newFilename = req.file.filename;

        res.json({
            success: true,
            data: {
                fileId: newFilename,
                originalFilename: req.file.originalname,
                mimetype: req.file.mimetype,
                size: req.file.size,
            },
        });
    });

    app.use(errorHandler);

    return new Promise<void>((resolve, reject) => {
        const server = app.listen(port, () => {
            console.log(`文颜 Server 已启动，监听端口 ${port}`);
            console.log(`健康检查：http://localhost:${port}/health`);
            console.log(`鉴权探针：http://localhost:${port}/verify`);
            console.log(`发布接口：POST http://localhost:${port}/publish`);
            console.log(`草稿详情：POST http://localhost:${port}/draft/get`);
            console.log(`草稿列表：POST http://localhost:${port}/draft/list`);
            console.log(`草稿统计：POST http://localhost:${port}/draft/count`);
            console.log(`删稿接口：POST http://localhost:${port}/draft/delete`);
            console.log(`正式发布：POST http://localhost:${port}/draft/publish`);
            console.log(`发布状态：POST http://localhost:${port}/publish/status`);
            console.log(`已发布列表：POST http://localhost:${port}/published/list`);
            console.log(`已发布详情：POST http://localhost:${port}/published/get`);
            console.log(`已发布删除：POST http://localhost:${port}/published/delete`);
            console.log(`上传接口：POST http://localhost:${port}/upload`);
        });

        server.on("error", (err: any) => {
            if (err.code === "EADDRINUSE") {
                console.error(`端口 ${port} 已被占用`);
                reject(new Error(`端口 ${port} 已被占用`));
            } else {
                reject(err);
            }
        });

        process.on("SIGINT", () => {
            console.log("\n正在关闭服务器...");
            server.close(() => {
                console.log("服务器已关闭");
                resolve();
            });
        });

        process.on("SIGTERM", () => {
            server.close(() => resolve());
        });
    });
}

function errorHandler(error: any, _req: Request, res: Response, next: NextFunction): void {
    if (res.headersSent) {
        return next(error);
    }

    const message = error instanceof Error ? error.message : String(error);
    const isAppError = error instanceof AppError;
    const isMulterError = error.name === "MulterError";
    const statusCode = isAppError || isMulterError ? 400 : 500;

    if (statusCode === 500) {
        console.error("[Server Error]:", error);
    }

    res.status(statusCode).json({
        code: -1,
        desc: message,
    });
}

function createAuthHandler(config: { apiKey?: string }) {
    return (req: Request, res: Response, next: NextFunction): void => {
        if (!config.apiKey) {
            return next();
        }

        const clientApiKey = req.headers["x-api-key"];
        if (clientApiKey === config.apiKey) {
            next();
        } else {
            res.status(401).json({
                code: -1,
                desc: "Unauthorized: Invalid API Key",
            });
        }
    };
}

function validateRenderRequest(req: RenderRequest): void {
    if (!req.fileId) {
        throw new AppError("缺少必要参数：fileId");
    }
}

function validateStringField(value: string | undefined, fieldName: string): asserts value is string {
    if (!value?.trim()) {
        throw new AppError(`缺少必要参数：${fieldName}`);
    }
}

function validateNonNegativeInteger(value: number, fieldName: string) {
    if (!Number.isInteger(value) || value < 0) {
        throw new AppError(`${fieldName} 必须是大于等于 0 的整数`);
    }
}

function getMediaId(body: MediaIdRequest) {
    const mediaId = body.mediaId ?? body.media_id;
    validateStringField(mediaId, "mediaId");
    return mediaId;
}

function getArticleId(body: ArticleIdRequest) {
    const articleId = body.articleId ?? body.article_id;
    validateStringField(articleId, "articleId");
    return articleId;
}

function normalizeListRequest(body: ListRequest) {
    const offset = body.offset ?? 0;
    const count = body.count ?? 20;
    const rawNoContent = body.noContent ?? body.no_content ?? false;
    const noContent = rawNoContent === true || rawNoContent === 1;

    validateNonNegativeInteger(offset, "offset");
    if (!Number.isInteger(count) || count < 1 || count > 20) {
        throw new AppError("count 必须是 1 到 20 之间的整数");
    }

    return {
        offset,
        count,
        noContent,
    };
}

async function cleanupOldUploads() {
    try {
        const files = await fs.readdir(UPLOAD_DIR);
        const now = Date.now();
        for (const file of files) {
            const filePath = path.join(UPLOAD_DIR, file);
            try {
                const stats = await fs.stat(filePath);
                if (now - stats.mtimeMs > UPLOAD_TTL_MS) {
                    await fs.unlink(filePath);
                }
            } catch (_error) {
                // 忽略单个文件处理错误
            }
        }
    } catch (error) {
        console.error("Cleanup task error:", error);
    }
}
