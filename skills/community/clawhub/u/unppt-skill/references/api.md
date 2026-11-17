# JavaScript API 参考（@unppt/unppt 0.3.2）

## 包的导入路径

| 导入路径 | 内容 | 运行环境 |
|---|---|---|
| `@unppt/unppt` | `convert()`、`checkFonts()`、`createPainter()`、`UNPPT_VERSION` 及类型 | 任何环境（Node、浏览器、云函数），不读写磁盘、不联网 |
| `@unppt/unppt/node` | `createRasterPool()`、`autoWorkers()`、`loadFontPack()` | 仅 Node（worker_threads 多线程出图；读默认字体包） |
| `@unppt/unppt/resvg.wasm` | resvg WASM 文件 | 作为文件读取，传给 `rasterWasm` 或 `createRasterPool` |

包是 ESM（`"type": "module"`），用 `import`。最小版本要求同 unppt 本体（Node ≥ 20.12）。

## convert(input, options)

```ts
function convert(input: InputSource, options: ConvertOptions): Promise<ConvertResult>
```

### 输入 input: InputSource

```ts
type InputSource = Uint8Array | ArrayBuffer | RandomAccessSource;

interface RandomAccessSource {
  size: number;                                            // 文件总字节数
  read(offset: number, length: number): Promise<Uint8Array>;
}
```

小文件直接传 `Uint8Array`（Node 的 `Buffer` 就是）。大文件必须传 `RandomAccessSource`，转码器只读需要的部分（见下文"大文件"）。

### 选项 options

| 选项 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `write` | `(path, data) => Promise<void>` | **必填** | 输出写入函数，见下文 |
| `fontPack` | `FontPack` | 无 | 默认字体包。**Node 里必须用 `loadFontPack()` 读并传入**；不给时非嵌入字体字宽只能估算 |
| `fonts` | `InputSource[]` | `[]` | 自备字体文件（ttf/otf/ttc）内容，同名压过字体包 |
| `privateFonts` | `InputSource[]` | `[]` | 旧选项，同 `fonts` |
| `output` | `'single' \| 'paged' \| 'pages' \| 'data'` | `'single'` | 产物形式（`'html'` 是旧名） |
| `fileName` | `string` | `'index.html'`（data 时 `'deck.json'`） | 主文件名 |
| `inlineLimit` | number | `2097152` | 小于该大小的图片内联（仅 `single`）；音视频总是单独输出 |
| `embedFonts` | boolean | `true` | 用到的字做成子集嵌入产物；`false` 只用于调试 |
| `images` | boolean | `true` | 是否输出 `pic/{n}.jpg`、`thum/{n}.jpg`。`prop.json` 总是输出 |
| `rasterWasm` | `Uint8Array \| Promise` | 无 | resvg WASM 字节。**`images: true` 时必须给它或 `rasterPool`**，否则不出图并记警告 |
| `rasterPool` | `RasterPool` | 无 | 并行出图执行器（`createRasterPool()` 返回值），给了就不需要 `rasterWasm` |
| `onProgress` | `(done, total) => void` | 无 | 每处理完一页调用一次 |

### 结果 ConvertResult

| 字段 | 说明 |
|---|---|
| `slides` | 输出页数 |
| `width` / `height` | 幻灯片尺寸（像素，96 DPI） |
| `report.missingFonts` | 缺失字体名（已排序）；更完整结论看 `fontCheck` |
| `report.warnings` | 转码警告（如"第 3 页渲染失败：……"，同类合并为"……（N 处）"） |
| `fontCheck` | 字体检查，同 `unppt check --json`（见下文） |

出错行为：文件不是有效 pptx、`output` 写错等 → Promise reject；老格式 .ppt（OLE 二进制）或加密的 pptx → reject，错误信息为"这是老格式的 .ppt 文件（或加密的 pptx），暂不支持，请用 PowerPoint 另存为 .pptx 后再转码"；**单页**出错不整体失败，输出白页 + warning；`write` 回调抛错 → convert 失败。服务端处理上传时建议捕获该错误并提示用户重新上传 .pptx。

## write 回调（最重要的坑）

```ts
type WriteData = Uint8Array | string | AsyncIterable<Uint8Array>;
type WriteFn = (path: string, data: WriteData) => Promise<void>;
```

- `path` 是 `/` 分隔的相对路径：`index.html`、`media/media1.1a2b3c4d.mp4`、`pic/3.jpg`、`pages/2.9f8e7d6c.js`、`prop.json`。
- `data` 三种形态：字符串、字节、**数据流**（`AsyncIterable`，用 `for await` 逐块读）。主文件和大视频以流给出，避免整文件进内存。
- **不要让写入排队互相等待**：`single`/`data` 会先 `write(主文件名, 数据流)`，转码器在读取该流的过程中还会调用 `write('media/…')` 等写其他文件。若实现成"上一个写完才下一个"就死锁。每次调用独立处理。
- Node 里最简单：`fs.promises.writeFile` 本身接受三种 data。

```js
import { mkdir, writeFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';

const write = async (path, data) => {
  const target = join(outDir, path);
  await mkdir(dirname(target), { recursive: true });
  await writeFile(target, data);
};
```

收集进内存（上传对象存储）：

```js
async function toBuffer(data) {
  if (typeof data === 'string') return Buffer.from(data);
  if (data instanceof Uint8Array) return Buffer.from(data);
  const chunks = [];
  for await (const chunk of data) chunks.push(chunk);
  return Buffer.concat(chunks);
}
```

## 大文件：按位置读取

```js
import { open, stat } from 'node:fs/promises';
import { convert } from '@unppt/unppt';

async function fileSource(path) {
  const { size } = await stat(path);
  const fh = await open(path, 'r');
  return {
    size,
    fh, // 自己留着，用完关闭
    async read(offset, length) {
      const buf = new Uint8Array(Math.max(0, Math.min(length, size - offset)));
      const { bytesRead } = await fh.read(buf, 0, buf.length, offset);
      return buf.subarray(0, bytesRead);
    },
  };
}

const source = await fileSource('big.pptx');
try {
  await convert(source, { write, images: false });
} finally {
  await source.fh.close();
}
```

字体也可这样传（`fonts: [await fileSource('/opt/fonts/MyFont.ttc')]`）。浏览器里用 `Blob.slice(offset, offset+length).arrayBuffer()` 实现 `read`。实测：300 页 + 800MB 视频、128MB 内存限制，约 1 秒转完，峰值约 120MB。

## 出图（pic/ 和 thum/）

```js
// 单线程：读 resvg.wasm 传给 rasterWasm
import { readFile } from 'node:fs/promises';
const wasm = new Uint8Array(await readFile(new URL(import.meta.resolve('@unppt/unppt/resvg.wasm'))));
await convert(pptxBytes, { write, rasterWasm: wasm });

// 多线程（仅 Node）：createRasterPool + autoWorkers
import { createRasterPool, autoWorkers } from '@unppt/unppt/node';
const pool = await createRasterPool(wasm, autoWorkers());
try {
  await convert(pptxBytes, { write, rasterPool: pool });
} finally {
  await pool.close(); // 结束工作线程
}
```

`autoWorkers()`：min(CPU 数（容器按 cgroup 配额）, 可用内存 ÷ 400MB)，至少 1。一个池可给多次 convert 共用。

## 字体：loadFontPack

```js
import { convert } from '@unppt/unppt';
import { loadFontPack } from '@unppt/unppt/node';

const fontPack = await loadFontPack();   // 读已安装的 @unppt/fonts；没装返回 undefined
const result = await convert(pptxBytes, { write, fontPack });
```

- 一个 `fontPack` 可给多次 convert/checkFonts 共用，读一次即可。
- 做子集、出整页图时用到的字体文件会进内存（单个 9~26MB，如霞鹜文楷 26MB），内存紧张时注意。
- 云函数无需装系统字体：部署带上 `@unppt/unppt`（连带 `@unppt/fonts` 约 100MB），调用 `loadFontPack()`。代码包超限时把字体包放层（layer）或挂载文件系统，用 `loadFontPack(目录)` 指定位置。

## checkFonts(input, options)：只检查字体

```ts
function checkFonts(
  input: InputSource,
  options?: { fontPack?: FontPack; fonts?: InputSource[]; onProgress?: (done, total) => void },
): Promise<FontCheck & { slides: number }>
```

返回字段：`slides` 页数；`fonts[]` 每个字体一项（`font` 名、`pages` 页码（从 1 起）、`status` 结论、可选 `substitute`/`shownWith`）；`missingChars[]` 无字体可显示的字 `{ page, chars }`；`errors` 必须处理的问题数；`warnings` 提醒数。

`status` 取值：`embedded`（PPT 嵌入）、`specified`（fonts 指定）、`default`（字体包接管，显示用 `shownWith`）、`substituted`（按 PowerPoint 规则替代）、`symbol-missing`（符号字体未嵌入，✗）、`missing`（连替代都没有，通常没传 fontPack，✗）。

```js
const r = await checkFonts(pptxBytes, { fontPack: await loadFontPack() });
if (r.errors > 0) {
  for (const f of r.fonts) if (f.status === 'symbol-missing' || f.status === 'missing') console.log(f.font, f.pages);
}
```

## 可运行示例

### Node 脚本：批量转换目录（与 scripts/batch-convert.mjs 相同思路）

见技能目录 `scripts/batch-convert.mjs`；要点：`pool`、`fontPack` 在循环外建一次共用，单文件失败不中断。

### HTTP 服务（Express）：上传 pptx 返回播放地址

```js
// server.mjs   npm install express @unppt/unppt
import express from 'express';
import { randomUUID } from 'node:crypto';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { convert } from '@unppt/unppt';
import { loadFontPack } from '@unppt/unppt/node';

const app = express();
const OUT = join(process.cwd(), 'converted');
const wasm = new Uint8Array(await readFile(new URL(import.meta.resolve('@unppt/unppt/resvg.wasm'))));
const fontPack = await loadFontPack();

app.use('/decks', express.static(OUT));

app.post('/convert', express.raw({ type: 'application/octet-stream', limit: '500mb' }), async (req, res) => {
  const id = randomUUID();
  const dir = join(OUT, id);
  const write = async (path, data) => {
    const target = join(dir, path);
    await mkdir(dirname(target), { recursive: true });
    await writeFile(target, data);
  };
  try {
    const result = await convert(new Uint8Array(req.body), { write, output: 'paged', rasterWasm: wasm, fontPack });
    res.json({ url: `/decks/${id}/index.html`, slides: result.slides, fontCheck: result.fontCheck, warnings: result.report.warnings });
  } catch (e) {
    res.status(400).json({ error: e.message });
  }
});

app.listen(3000, () => console.log('http://localhost:3000'));
```

测试：`curl -X POST --data-binary @demo.pptx -H "Content-Type: application/octet-stream" http://localhost:3000/convert`。返回的 `url` 可直接放进 `<iframe src="...">`。

### 云函数：从对象存储读、写回对象存储

```js
// handler.mjs
import { convert } from '@unppt/unppt';
import { loadFontPack } from '@unppt/unppt/node';

const fontPackReady = loadFontPack();   // 实例级只读一次

// —— 换成你的对象存储 SDK ——
async function getObject(key) { /* 返回 Uint8Array */ }
async function putObject(key, body) { /* body 是 Buffer */ }

async function toBuffer(data) {
  if (typeof data === 'string') return Buffer.from(data);
  if (data instanceof Uint8Array) return Buffer.from(data);
  const chunks = [];
  for await (const chunk of data) chunks.push(chunk);
  return Buffer.concat(chunks);
}

export async function handler(event) {
  const { inputKey, outputPrefix } = event;
  const bytes = await getObject(inputKey);
  const result = await convert(bytes, {
    output: 'paged',
    images: false,   // 需要图片时把 resvg.wasm 一起打包部署并传 rasterWasm
    fontPack: await fontPackReady,
    write: async (path, data) => putObject(outputPrefix + path, await toBuffer(data)),
  });
  return { entry: outputPrefix + 'index.html', slides: result.slides, fontCheck: result.fontCheck, warnings: result.report.warnings };
}
```

把 `index.html`、`pages/`、`media/` 放同一前缀下用 CDN 提供即可，无需服务器端程序。SDK 支持流式上传时直接把 `data`（AsyncIterable）交给它更省内存。

### 浏览器内转码（Vite/webpack 可直接打包）

```js
import { convert } from '@unppt/unppt';

const file = input.files[0];              // <input type="file">
const source = {
  size: file.size,
  read: async (offset, length) => new Uint8Array(await file.slice(offset, offset + length).arrayBuffer()),
};
const files = new Map();
const result = await convert(source, {
  images: false,
  write: async (path, data) => {
    if (typeof data === 'string' || data instanceof Uint8Array) { files.set(path, data); return; }
    const parts = [];
    for await (const c of data) parts.push(c);
    files.set(path, new Blob(parts));
  },
});
// files 里就是 index.html、media/... 等输出
```

浏览器里没有 `loadFontPack()`；不传 `fontPack` 时非嵌入字体字宽只能估算。可按 `FontPack` 接口（`faces`、`rules`、`metrics(id)`、`file(name)`）从网络实现。
