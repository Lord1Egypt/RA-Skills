// 目录发布使用的独立上传协议实现，无单文件发布入口。
import crypto from 'node:crypto';
export const ENDPOINT = 'https://alioss.wangxiaobao.com/minio/upload';
export const timeout = fallback => AbortSignal.timeout(Number(process.env.WXB_UPLOAD_TIMEOUT_MS) || fallback);
export const digest = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
export function safeURL(value) {
  const u = new URL(value);
  if (u.protocol !== 'https:' || u.hostname !== 's2.wangxiaobao.com' || u.port || u.username || u.password || u.hash || u.search) throw new Error('返回URL不属于已知HTTPS存储主机，停止访问并保留上传回执');
  return u.href;
}
export async function upload(bytes, fetcher, options) {
  const { name, group, mime } = options;
  const form = new FormData();
  form.append('file', new Blob([bytes], { type: mime }), name);
  form.append('group', group);
  form.append('name', name);
  const r = await fetcher(ENDPOINT, { method: 'POST', headers: { accept: 'application/json' }, body: form, redirect: 'manual', signal: timeout(60000) });
  if (!r.ok) throw new Error(`HTTP ${r.status}，禁止自动重传`);
  if (!r.body) throw new Error('上传响应为空');
  const chunks = []; let size = 0;
  for await (const chunk of r.body) {
    size += chunk.length;
    if (size > 65536) throw new Error('上传回执异常过大');
    chunks.push(Buffer.from(chunk));
  }
  const data = JSON.parse(Buffer.concat(chunks).toString('utf8'));
  if (data.code !== 0 || typeof data.data !== 'string') throw new Error('业务失败或响应格式异常，禁止自动重传');
  return { url: data.data, name };
}
