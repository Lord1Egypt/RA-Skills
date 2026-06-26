import * as fs from "fs";
import * as path from "path";
import FormData from "form-data";

const API_BASE = "https://api.trends.fun/v1";

/**
 * 通用请求头
 */
function authHeaders(token: string): Record<string, string> {
    return {
        accept: "application/json, text/plain, */*",
        authorization: `Bearer ${token}`,
        origin: "https://trends.fun",
        referer: "https://trends.fun/",
        "x-platform": "web",
        "x-lang": "zh-CN",
    };
}

/**
 * Step 1: 获取 IPFS 上传 URL（Pinata）
 */
export async function getUploadUrl(
    token: string,
    filename: string
): Promise<{ url: string; expiredAt: number }> {
    console.log("📦 Step 1: 获取 IPFS 上传 URL...");

    const resp = await fetch(`${API_BASE}/file/upload_url`, {
        method: "POST",
        headers: {
            ...authHeaders(token),
            "content-type": "application/json",
        },
        body: JSON.stringify({ filename }),
    });

    if (!resp.ok) {
        throw new Error(`获取上传 URL 失败: ${resp.status} ${resp.statusText}`);
    }

    const result = (await resp.json()) as {
        status: string;
        data: { url: string; expired_at: number };
        error_msg?: string;
    };

    if (result.status !== "success") {
        throw new Error(`获取上传 URL 错误: ${result.error_msg}`);
    }

    console.log("✅ 获取到 Pinata 上传 URL");
    return { url: result.data.url, expiredAt: result.data.expired_at };
}

/**
 * Step 2: 上传图片到 IPFS (Pinata V3)
 * 文档: https://docs.pinata.cloud/api-reference/endpoint/files/upload
 */
export async function uploadImage(
    uploadUrl: string,
    imagePath: string
): Promise<string> {
    console.log("🖼️  Step 2: 上传图片到 IPFS...");

    const absolutePath = path.resolve(imagePath);
    if (!fs.existsSync(absolutePath)) {
        throw new Error(`图片文件不存在: ${absolutePath}`);
    }

    // 1. 读取文件为 Buffer
    const fileBuffer = fs.readFileSync(absolutePath);
    const fileName = path.basename(absolutePath);

    // 2. 构建 FormData (完全符合文档要求的 multipart/form-data)
    const form = new FormData();

    // 字段: file (文档要求: Binary)
    form.append("file", fileBuffer, {
        filename: fileName,
        contentType: getContentType(fileName),
    });

    // 字段: network (文档要求: "public" | "private")
    // 你的 curl 中使用的是 public，必须加上，否则默认为 private 导致后续无法访问
    form.append("network", "public");

    // 可选: name (文档支持自定义文件名，这里用原始文件名)
    form.append("name", fileName);

    console.log(`📦 正在生成上传数据包...`);

    // 3. 核心修复: 转为 Buffer 解决 'source.on' 和 '408' 错误
    const payload = form.getBuffer();

    console.log(`📦 数据准备就绪，大小: ${payload.length} bytes`);

    try {
        const resp = await fetch(uploadUrl, {
            method: "POST",
            headers: {
                // 模拟浏览器/Curl 的 headers
                origin: "https://trends.fun",
                referer: "https://trends.fun/",

                // 必须包含 form-data 生成的 boundary
                ...form.getHeaders(),

                // 关键: 显式设置 Content-Length 避免服务器等待直到超时 (408)
                "Content-Length": payload.length.toString(),
            },
            body: payload as unknown as BodyInit,
            // Node.js 18+ fetch 需要此参数以支持非标准 body
            // @ts-ignore
            duplex: "half",
        });

        if (!resp.ok) {
            const text = await resp.text();
            throw new Error(`上传图片失败: ${resp.status} ${text}`);
        }

        const result = (await resp.json()) as {
            status: string; // 可能是 pinata 的返回结构，也可能是 trends.fun 封装的
            data: { cid: string; id: string; is_duplicate?: boolean };
        };

        // Pinata V3 文档显示的返回结构是在 data 字段里
        const cid = result.data?.cid || (result as any).cid;

        if (!cid) {
            console.error("❌ 返回结果异常:", JSON.stringify(result));
            throw new Error(`上传成功但未获取到 CID`);
        }

        const ipfsUrl = `https://ipfs.io/ipfs/${cid}`;
        console.log(`✅ 图片上传成功, IPFS URL: ${ipfsUrl}`);
        return ipfsUrl;

    } catch (error: any) {
        console.error("❌ 上传过程发生异常:", error);
        throw error;
    }
}

/**
 * Step 3: 获取 mint 地址
 */
export async function getMintAddress(token: string): Promise<string> {
    console.log("🔑 Step 3: 获取 mint 地址...");

    const t = Date.now();
    const resp = await fetch(
        `${API_BASE}/vanity/mint_address?t=${t}`,
        {
            method: "GET",
            headers: authHeaders(token),
        }
    );

    if (!resp.ok) {
        throw new Error(`获取 mint 地址失败: ${resp.status} ${resp.statusText}`);
    }

    const result = (await resp.json()) as {
        status: string;
        data: string;
        error_msg?: string;
    };

    if (result.status !== "success") {
        throw new Error(`获取 mint 地址错误: ${result.error_msg}`);
    }

    console.log(`✅ 获取到 mint 地址: ${result.data}`);
    return result.data;
}

/**
 * Step 4: 上传 coin tick 内容
 */
export async function uploadContent(
    token: string,
    params: {
        mintAddr: string;
        ticker: string;
        name: string;
        imageUrl: string;
        description: string;
        mode: number;
        url?: string;
    }
): Promise<string> {
    console.log("📝 Step 4: 上传 coin tick 内容...");

    const body: Record<string, unknown> = {
        mint_addr: params.mintAddr,
        ticker: params.ticker,
        name: params.name,
        image_url: params.imageUrl,
        description: params.description,
        mode: params.mode,
    };

    if (params.url) {
        body.url = params.url;
    }

    const resp = await fetch(`${API_BASE}/mint/upload_content`, {
        method: "POST",
        headers: {
            ...authHeaders(token),
            "content-type": "application/json",
        },
        body: JSON.stringify(body),
    });
    if (!resp.ok) {
        throw new Error(`上传内容失败: ${resp.status} ${resp.statusText}`);
    }

    const result = (await resp.json()) as {
        status: string;
        data: string;
        error_code?: number;
        error_msg?: string;
    };

    if (result.status !== "success") {
        throw new Error(
            `上传内容错误: ${result.error_msg} (code: ${result.error_code})`
        );
    }

    console.log(`✅ 内容上传成功, IPFS URI: ${result.data}`);
    return result.data;
}

/**
 * 根据文件扩展名获取 content type
 */
function getContentType(filename: string): string {
    const ext = path.extname(filename).toLowerCase();
    const map: Record<string, string> = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
        ".svg": "image/svg+xml",
    };
    return map[ext] || "application/octet-stream";
}
