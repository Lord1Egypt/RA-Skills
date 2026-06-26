/**
 * Minimal Cloudflare R2 helper — vendored into this skill so it stays
 * self-contained. Drop-in replacement for @vercel/blob put().
 */
import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";

let _client: S3Client | null = null;

function getClient(): S3Client {
  if (!_client) {
    const accountId = process.env.R2_ACCOUNT_ID;
    const accessKeyId = process.env.R2_ACCESS_KEY_ID;
    const secretAccessKey = process.env.R2_SECRET_ACCESS_KEY;
    if (!accountId || !accessKeyId || !secretAccessKey) {
      throw new Error("Missing R2 credentials (R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY)");
    }
    _client = new S3Client({
      region: "auto",
      endpoint: `https://${accountId}.r2.cloudflarestorage.com`,
      credentials: { accessKeyId, secretAccessKey },
    });
  }
  return _client;
}

function getBucket(): string {
  const bucket = process.env.R2_BUCKET_NAME;
  if (!bucket) throw new Error("Missing R2_BUCKET_NAME");
  return bucket;
}

function getPublicBaseUrl(): string {
  const url = process.env.R2_PUBLIC_URL;
  if (!url) throw new Error("Missing R2_PUBLIC_URL — set to your R2 public bucket URL or custom domain");
  return url.replace(/\/$/, "");
}

export interface PutResult {
  url: string;
  pathname: string;
}

export interface PutOptions {
  contentType?: string;
  addRandomSuffix?: boolean;
}

export async function put(
  pathname: string,
  body: Buffer,
  options?: PutOptions,
): Promise<PutResult> {
  const bucket = getBucket();
  const suffix = options?.addRandomSuffix === true
    ? `-${Math.random().toString(36).slice(2, 10)}`
    : "";

  let key = pathname;
  if (suffix) {
    const dotIdx = pathname.lastIndexOf(".");
    key = dotIdx > 0
      ? pathname.slice(0, dotIdx) + suffix + pathname.slice(dotIdx)
      : pathname + suffix;
  }

  await getClient().send(
    new PutObjectCommand({
      Bucket: bucket,
      Key: key,
      Body: body,
      ContentType: options?.contentType ?? "application/octet-stream",
    }),
  );

  return { url: `${getPublicBaseUrl()}/${key}`, pathname: key };
}
