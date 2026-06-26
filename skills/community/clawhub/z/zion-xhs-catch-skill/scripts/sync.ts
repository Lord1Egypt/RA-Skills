/**
 * Zion BaaS 同步脚本
 * 将采集的小红书数据通过 GraphQL 写入 Zion
 * 包含图片二进制上传逻辑 (PUT + ID 保存)
 */

import * as fs from 'fs';
import * as path from 'path';
import * as crypto from 'crypto';

export interface XHSNote {
  xhs_note_id: string;
  title: string;
  content: string;
  author_name: string;
  author_id?: string;
  images: string[];
  likes: number;
  collects: number;
  comments_count: number;
  comments?: any[];
  keyword: string;
  note_url: string;
  crawl_time: string;
}

export interface ZionConfig {
  endpoint: string;
  token: string;
  tableName: string;
  userId?: string;
}

/**
 * 上传图片到 Zion 并返回 imageId
 */
async function uploadImage(url: string, config: ZionConfig): Promise<string | null> {
  try {
    const resp = await fetch(url);
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const buffer = Buffer.from(await resp.arrayBuffer());
    const md5 = crypto.createHash('md5').update(buffer).digest('base64');

    let suffix = 'JPG';
    if (url.toLowerCase().endsWith('.png')) suffix = 'PNG';
    else if (url.toLowerCase().endsWith('.webp')) suffix = 'WEBP';
    else if (url.toLowerCase().endsWith('.gif')) suffix = 'GIF';

    const gql = {
      query: `
        mutation GetImageUploadUrl($md5: String!, $suffix: MediaFormat!) {
          imagePresignedUrl(imgMd5Base64: $md5, imageSuffix: $suffix, acl: PUBLIC_READ) {
            imageId
            uploadUrl
            uploadHeaders
          }
        }
      `,
      variables: { md5, suffix },
    };

    const res = await fetch(config.endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${config.token}`,
      },
      body: JSON.stringify(gql),
    });

    const json = await res.json();
    if (json.errors) throw new Error(JSON.stringify(json.errors));

    const { imageId, uploadUrl, uploadHeaders } = json.data.imagePresignedUrl;

    const headers: Record<string, string> = {
      'Content-Type': resp.headers.get('content-type') || 'image/jpeg',
    };
    
    // 兼容 Array 和 Object 格式的 uploadHeaders
    if (uploadHeaders) {
      if (Array.isArray(uploadHeaders)) {
        uploadHeaders.forEach((h: any) => {
          headers[h.key] = h.value;
        });
      } else {
        Object.entries(uploadHeaders).forEach(([k, v]) => {
          headers[k] = v as string;
        });
      }
    }

    const putRes = await fetch(uploadUrl, {
      method: 'PUT',
      headers,
      body: buffer,
    });

    if (!putRes.ok) throw new Error(`PUT upload failed: ${putRes.statusText}`);

    return imageId;
  } catch (err) {
    console.error(`  ⚠ 图片上传失败 (${url.slice(0, 50)}...):`, (err as Error).message);
    return null;
  }
}

function parseYaml(text: string): any {
  const result: any = {};
  let current = result;
  const stack: any[] = [];
  const lines = text.split('\n');

  for (const rawLine of lines) {
    const line = rawLine.split('#')[0];
    if (!line.trim()) continue;

    const indent = line.search(/\S/);
    const keyVal = line.trim().split(':');
    const key = keyVal[0].trim();
    const val = keyVal.slice(1).join(':').trim();

    while (stack.length > 0 && indent <= (stack[stack.length - 1].indent || -1)) {
      stack.pop();
      current = stack.length > 0 ? stack[stack.length - 1].obj : result;
    }

    if (!val) {
      current[key] = {};
      stack.push({ obj: current, indent });
      current = current[key];
    } else {
      current[key] = val.replace(/^"|"$/g, '').replace(/^'|'$/g, '');
    }
  }

  return result;
}

function loadConfig(): ZionConfig {
  const zionCredPath = path.resolve(process.cwd(), '.zion', 'credentials.yaml');
  const siblingZionCredPath = path.resolve(process.cwd(), '..', 'pain-catcher', '.zion', 'credentials.yaml');
  
  let credPath = fs.existsSync(zionCredPath) ? zionCredPath : (fs.existsSync(siblingZionCredPath) ? siblingZionCredPath : null);

  if (credPath) {
    const cred = parseYaml(fs.readFileSync(credPath, 'utf-8'));
    const projectExId = cred.project?.exId || cred.project?.exid || 'rmLyJ0ZJXK8';
    const token = cred.project?.admin_token?.token || cred.admin_token?.token;
    const userId = cred.account?.user_id || cred.account?.userId || '';
    if (projectExId && token) {
      return {
        endpoint: `https://zion-app.functorz.com/zero/${projectExId}/api/graphql-v2`,
        token,
        tableName: 'articles',
        userId,
      };
    }
  }

  throw new Error('未找到有效 Zion 配置，请检查 .zion/credentials.yaml');
}

function buildInsertMutation(tableName: string, note: XHSNote, imageIds: string[], userId?: string): { query: string; variables: Record<string, any> } {
  const objects: any = {
    xhs_note_id: note.xhs_note_id,
    title: note.title,
    content: note.content,
    author_name: note.author_name,
    author_id: note.author_id || '',
    likes: note.likes,
    collects: note.collects,
    comments_count: note.comments_count,
    comments: note.comments || [],
    keyword: note.keyword,
    note_url: note.note_url,
    crawl_time: note.crawl_time,
  };

  if (userId) {
    objects.user_id = userId;
  }

  // 处理图片列表关系 (Array Relationship)
  if (imageIds.length > 0) {
    objects.images = {
      data: imageIds.map(id => ({ image_id: id }))
    };
  }

  return {
    query: `
      mutation Insert${tableName}($objects: [${tableName}_insert_input!]!) {
        insert_${tableName}(
          objects: $objects
          on_conflict: {
            constraint: ${tableName}_xhs_note_id_key,
            update_columns: [title, content, author_name, author_id, likes, collects, comments_count, comments, keyword, note_url, crawl_time${userId ? ', user_id' : ''}]
          }
        ) {
          returning {
            id
          }
        }
      }
    `,
    variables: { objects: [objects] },
  };
}

export async function syncToZion(notes: XHSNote[], config?: ZionConfig) {
  const cfg = config || loadConfig();
  const results = { success: 0, failed: 0, errors: [] as string[] };

  console.log(`📡 正在上报情报至 弦外 Overtone 中心...`);

  for (const note of notes) {
    const imageIds: string[] = [];
    if (note.images && note.images.length > 0) {
      console.log(`  正在处理视觉资产: ${note.images.length} 张图片...`);
      for (const imgUrl of note.images.slice(0, 3)) {
        const id = await uploadImage(imgUrl, cfg);
        if (id) imageIds.push(id);
      }
    }

    const mutation = buildInsertMutation(cfg.tableName, note, imageIds, cfg.userId);

    try {
      const res = await fetch(cfg.endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${cfg.token}`,
        },
        body: JSON.stringify(mutation),
      });

      const json = await res.json();
      if (json.errors) throw new Error(JSON.stringify(json.errors));

      results.success++;
      console.log(`  ✓ 情报已归档: ${note.title.slice(0, 20)}... (云端资源: ${imageIds.length})`);
    } catch (err) {
      results.failed++;
      const msg = (err as Error).message;
      results.errors.push(`${note.xhs_note_id}: ${msg}`);
      console.error(`  ✗ 上报失败: ${note.xhs_note_id} - ${msg}`);
    }
    await new Promise((r) => setTimeout(r, 200));
  }

  console.log(`\n🏁 弦外上报完成: ${results.success} 成功, ${results.failed} 失败`);
  return results;
}

async function main() {
  const args = process.argv.slice(2);
  const fileArg = args.find((a) => a.startsWith('--file='));
  if (!fileArg) {
    console.error('用法: npx ts-node sync.ts --file=output/xxx.json');
    process.exit(1);
  }

  const filePath = fileArg.split('=')[1];
  if (!fs.existsSync(filePath)) {
    console.error(`文件不存在: ${filePath}`);
    process.exit(1);
  }

  const notes: XHSNote[] = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  console.log(`读取到 ${notes.length} 条笔记，开始同步...`);
  await syncToZion(notes);
}

if (require.main === module) {
  main().catch((err) => {
    console.error('同步异常:', err);
    process.exit(1);
  });
}
