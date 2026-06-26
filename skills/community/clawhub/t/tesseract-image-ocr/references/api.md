# Tesseract.js Full API Reference

> Based on the [Tesseract.js Official API Documentation](https://github.com/naptha/tesseract.js/blob/master/docs/api.md)

---

## createWorker(langs, oem, options): Worker

Creates a Tesseract.js Worker instance. A Worker manages a single Tesseract instance within a Web Worker (browser) or Worker Thread (Node.js).

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `langs` | string\|string[] | Language code(s), e.g., `'eng'` or `['eng', 'chi_sim']` |
| `oem` | number | OCR engine mode (see OEM table) |
| `options` | object | Custom options |

**options Fields:**

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `corePath` | string | — | Path to the tesseract.js-core directory (**Note: points to a directory, not a single .js file**) |
| `langPath` | string | — | Download path for training language data (no trailing `/`) |
| `workerPath` | string | — | Download path for worker script |
| `cachePath` | string | — | Cache path; more commonly used in Node.js |
| `cacheMethod` | string | `'write'` | Cache strategy: `write`/`readOnly`/`refresh`/`none` |
| `legacyCore` | boolean | `false` | Whether to download Legacy model support code |
| `legacyLang` | boolean | `false` | Whether to download Legacy language data |
| `workerBlobURL` | boolean | `true` | Whether to load the Worker using a Blob URL |
| `gzip` | boolean | `true` | Whether remote training data is gzip compressed |
| `logger` | function | — | Progress callback, e.g., `m => console.log(m)` |
| `errorHandler` | function | — | Worker error callback |

---

## worker.recognize(image, options, output, jobId): Promise

Core OCR recognition method.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `image` | string\|Buffer\|... | Image (see supported image formats) |
| `options` | object | Recognition options |
| `options.rectangle` | object | Restrict recognition region `{top, left, width, height}` |
| `output` | object | Output format toggles, e.g., `{ hocr: true, blocks: true }` |
| `jobId` | string | Optional job ID |

**Returns:** `{ jobId, data: { text, hocr?, blocks?, tsv?, ... } }`

The returned `data.text` is the plain text result. An empty result is returned even if no text is detected; an exception will not be thrown.

---

## worker.setParameters(params, jobId): Promise

Sets Tesseract engine parameters (calls SetVariable).

**Common Parameters:**

| Parameter Name | Type | Default | Description |
|----------------|------|---------|-------------|
| `tessedit_pageseg_mode` | string | `'3'` | Page segmentation mode |
| `tessedit_char_whitelist` | string | `''` | Character whitelist |
| `preserve_interword_spaces` | string | `'0'` | Preserve inter-word spaces |
| `user_defined_dpi` | string | `''` | Manually specify DPI |

> `setParameters` cannot modify `oem`; to change the OEM, use `worker.reinitialize()`.

---

## worker.reinitialize(langs, oem, config, jobId): Promise

Reinitialize an existing Worker with different languages/OEM.

```javascript
await worker.reinitialize('chi_sim', 1);
```

To switch to the Legacy engine (OEM=0), the Worker must have been created with `legacyCore: true, legacyLang: true` set in `createWorker`.

---

## worker.detect(image, jobId): Promise

Performs OSD (Orientation and Script Detection) without performing OCR.

**Prerequisite:** The Worker must be created using `legacyCore: true, legacyLang: true`.

```javascript
const worker = await createWorker('eng', 0, { legacyCore: true, legacyLang: true });
const { data } = await worker.detect('rotated.jpg');
// data: { orientation_confidence, orientation_degrees, script, script_confidence }
```

---

## worker.terminate(jobId): Promise

Terminate the Worker and clean up resources.

```javascript
await worker.terminate();
```

---

## createScheduler(): Scheduler

Create a scheduler for parallel processing.

### Scheduler Methods

| Method | Description |
|--------|-------------|
| `scheduler.addWorker(worker)` | Add a Worker to the scheduling pool |
| `scheduler.addJob({ recognize(image, options, output) })` | Add a recognition job |
| `scheduler.getQueueLen()` | Get the current queue length |
| `scheduler.getNumWorkers()` | Get the number of Workers |

```javascript
const scheduler = createScheduler();
const w1 = await createWorker('eng');
const w2 = await createWorker('eng');
scheduler.addWorker(w1);
scheduler.addWorker(w2);

const results = await Promise.all(images.map(img =>
  scheduler.addJob('recognize', img)
));
await Promise.all([w1.terminate(), w2.terminate()]);
```

---

## setLogging(flag: boolean)

Enable/disable log output.

---

## PSM — Page Segmentation Modes

| Value | Name | Description |
|-------|------|-------------|
| 0 | OSD_ONLY | Orientation and script detection only |
| 1 | AUTO_OSD | Automatic page segmentation + orientation detection |
| 2 | AUTO_ONLY | Automatic page segmentation, no orientation detection |
| 3 | AUTO | Fully automatic page segmentation (default) |
| 4 | SINGLE_COLUMN | Single column of variable size text |
| 5 | SINGLE_BLOCK_VERT_TEXT | Single block of vertical text |
| 6 | SINGLE_BLOCK | Single block of text |
| 7 | SINGLE_LINE | Single line of text |
| 8 | SINGLE_WORD | Single word |
| 9 | CIRCLE_WORD | Single word in a circular arrangement |
| 10 | SINGLE_CHAR | Single character |
| 11 | SPARSE_TEXT | Sparse text |
| 12 | SPARSE_TEXT_OSD | Sparse text + orientation detection |
| 13 | RAW_LINE | Raw line |

## OEM — OCR Engine Modes

| Value | Description |
|-------|-------------|
| 0 | Legacy engine |
| 1 | LSTM neural network engine (default) |
| 2 | Legacy + LSTM |
| 3 | Default (selected automatically) |