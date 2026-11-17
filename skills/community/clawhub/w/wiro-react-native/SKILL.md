---
name: wiro-react-native
description: Run Wiro AI models from React Native and Expo apps with the official @wiro-ai/wiro-react-native SDK, covering a backend proxy for credentials, typed and catalog model requests, file uploads, task tracking, cancellation and errors. Use it when a React Native or Expo app needs to generate images, video, speech, music or LLM output with Wiro.
---

# Wiro AI for React Native and Expo

`@wiro-ai/wiro-react-native` is the official TypeScript SDK for the Wiro AI model API in React Native and Expo apps, Expo Go included. It runs any model in the Wiro catalog through typed request factories or `Wiro.model`, uploads files, and follows each run (a task) by polling or over a WebSocket.

## Install

```sh
npm install @wiro-ai/wiro-react-native
npx expo install expo-file-system
```

- Requires React Native 0.76+ and Expo SDK 54+. Expo Go works. Bare React Native apps must have Expo Modules configured.
- Peer dependencies: `react-native`, `expo` and `expo-file-system` for Expo SDK 54 to 58 (`npx expo install` picks the version for your Expo SDK). `yarn add` and `pnpm add` work too.

## Credentials and the client

Long-lived Wiro API keys and secrets never ship inside an app binary. In a shipped app, use proxy mode: the app calls your backend, and the backend attaches the Wiro credentials server-side. The SDK never stores an API key in proxy mode.

```ts
import { WiroClient } from '@wiro-ai/wiro-react-native';

const client = new WiroClient({
  proxyUrl: 'https://api.example.com/wiro',
  headers: { Authorization: `Bearer ${sessionToken}` }, // your app's own user token, not a Wiro key
});
```

- The SDK sends the Wiro REST paths it uses (such as `/Run/{owner}/{project}`, `/Task/Detail` and `/File/Upload`) to `proxyUrl` with your `headers`. The backend adds the Wiro credentials and passes each call on to Wiro.
- `proxyUrl` must use HTTPS. Plain HTTP is accepted only for loopback hosts such as `localhost` during development.

For local development only, a key from an uncommitted env file is fine. The example app reads `EXPO_PUBLIC_WIRO_API_KEY` from `.env`, which `.gitignore` excludes, and commits only `.env.example`. Never put production credentials in `EXPO_PUBLIC_*` variables.

```ts
// API key only (local development)
const apiKey = process.env.EXPO_PUBLIC_WIRO_API_KEY?.trim() ?? '';
const devClient = apiKey.length > 0 ? new WiroClient({ apiKey }) : null;

// Key plus secret (local development only): the SDK signs each request with HMAC
const signedClient = new WiroClient({
  apiKey: 'YOUR_API_KEY',
  apiSecret: 'YOUR_API_SECRET',
});
```

- Match the project's auth method: add `apiSecret` for a Signature-Based project and leave it out for an API Key Only project. Projects and keys are created at https://wiro.ai/panel/project/new. Never ask the user to paste a key or secret into the chat.
- Create one client and close it when you are done. A closed client cannot be reused. In a component:

```ts
const client = useMemo(() => new WiroClient({ proxyUrl, headers }), []);
useEffect(() => () => client.close(), [client]);
```

## Run a model

Typed factories check parameters at compile time for FLUX.2 Pro, GPT Image 2, Nano Banana Pro, Seedream v4, Grok Imagine Image, Runway Gen-4.5, Seedance 2.0, Kling V3, Veo 3.1, Hailuo 2.3 Fast, Grok Imagine Video and Lyria 3 (`Wiro.flux2Pro`, `Wiro.gptImage2`, `Wiro.veo31` and so on). `subscribe` starts the run, follows the task and resolves when it ends. Tell the user the expected cost first (see Money rules).

```ts
import { Wiro, WiroFlux2ProOutputFormat } from '@wiro-ai/wiro-react-native';

const result = await client.subscribe(
  Wiro.flux2Pro({
    prompt: 'A cinematic mountain lake at sunrise',
    outputFormat: WiroFlux2ProOutputFormat.png,
  }),
  { onUpdate: (update) => console.log(update.status?.apiValue) },
);

if (result.kind === 'success') {
  for (const output of result.task.outputs) console.log(output.url?.toString());
} else {
  console.log('Failed:', result.reason);
}
```

Any other catalog model runs through `Wiro.model('owner/project', parameters)` with `WiroValue` values. Find the slug and the parameter names at https://wiro.ai/models, or in code:

```ts
import { Wiro, WiroModelId, WiroValue } from '@wiro-ai/wiro-react-native';

const models = await client.searchModels({ search: 'text to speech' });
const schema = await client.getModelSchema(new WiroModelId('owner', 'project'));
const request = Wiro.model('owner/project', {
  prompt: WiroValue.string('Hello from my app'),
});
const problems = schema.validate(request.parameters()); // empty when the request is valid
const speech = await client.subscribe(request);
```

- A search result's `modelId` is what you pass to `getModelSchema`. `schema.parameters` lists each input's `name`, `kind` and `isRequired`.
- Tracking: polling is the default. Pass `trackingMode: 'webSocket'` for live events, or call `await client.subscribeStream(request)` and read the updates with `for await`.
- Outputs: `result.task.outputs` holds items with `url`, `contentType`, `name` and `isImage`, `isVideo`, `isAudio` or `isText`. For LLM models the merged reply text is in `task.debugOutput`, and the text output's `content` has `rawText`, `answers` and `thinking`.
- `task.totalCost` is the amount charged for the run.

## Files

File inputs are uploaded automatically before the run. `WiroFileInput.uri` takes an Expo picker URI, `.bytes` a `Uint8Array`, `.blob` a `Blob`, and `.url` a file URL that is sent as is, without an upload. Typed factories take them directly (for example `inputImages` on `Wiro.flux2Pro`). In `Wiro.model`, wrap them with `WiroValue.fileInput`.

```ts
import { Wiro, WiroFileInput, WiroValue } from '@wiro-ai/wiro-react-native';

const image = WiroFileInput.uri(pickerAsset.uri, {
  fileName: pickerAsset.name ?? 'photo.jpg',
  mediaType: pickerAsset.mimeType ?? 'image/jpeg',
  sizeBytes: pickerAsset.size,
});
const result = await client.subscribe(
  Wiro.model('owner/project', { image: WiroValue.fileInput(image) }),
);
```

- Manual uploads return a `WiroUploadResult` whose `files[0]` has the `url` and `id`: `client.uploadFile(bytesOrBlob, 'photo.png')`, `client.uploadFileFromUri(uri, { fileName: 'photo.png' })` and `client.uploadStream(stream, 'video.mp4', { contentLength, onProgress, signal })`. Pass an uploaded file's `url` to later runs with `WiroFileInput.url(...)`.
- Bytes and Blobs are read into memory. For large files, pass a picker URI (sent with native `FormData`) or use `uploadStream`.
- `uploadStream` takes an `AsyncIterable<Uint8Array>` or a `ReadableStream`, writes it to a temporary app-cache file with `expo-file-system`, and sends it with Expo's native upload task, so the file stays out of the JavaScript heap. `onProgress` reports a `spooling` phase, then `uploading`. The temporary file is removed after success or failure.

## Long jobs: keep the task id

`subscribe`, `subscribeStream` and `waitForTask` stop following a task after `timeoutMs` and throw `WiroTimeoutError`. The task itself may still be running. For long or costly jobs such as video, start the run and wait in a separate step, so you always hold the task id and token:

```ts
import { WiroNetworkError, WiroTimeoutError } from '@wiro-ai/wiro-react-native';

const run = await client.run(request); // sent once: the SDK never retries a run by itself
const token = run.taskToken; // keep run.taskId and the token
if (token === undefined) throw new Error('The run returned no task token.');
try {
  const task = await client.waitForTask(token);
  console.log(
    task.isSuccessful,
    task.outputs.map((output) => output.url?.toString()),
  );
} catch (error) {
  if (!(error instanceof WiroTimeoutError || error instanceof WiroNetworkError))
    throw error;
  const task = await client.getTask(token); // look it up, and call waitForTask again if it is still running
}
```

`getTaskById(run.taskId)` works too. If the `run` call itself failed and you have no task id, ask the user to check the usage history at https://wiro.ai/panel/billing before anything runs again.

## Stop work and handle errors

Every async call accepts an `AbortSignal`. Aborting, like `client.close()`, only stops the SDK's local requests and tracking: a task that was already created keeps running on Wiro. To stop the task itself, and only when the user asks, call `cancelTask` while it is queued or `killTask` once it is running.

```ts
const controller = new AbortController();
try {
  const result = await client.subscribe(request, { signal: controller.signal });
} catch (error) {
  if (controller.signal.aborted) return; // stopped locally; the error's name is 'AbortError'
  throw error;
}
await client.cancelTask(taskId); // a queued task
await client.killTask(taskId); // a running task; a WiroTaskToken works too
```

- A failed task is a result, not an exception: `result.kind === 'failure'`, with `result.reason` (`cancelled`, `nonZeroExit` or `other`) and `result.task`.
- Thrown errors extend `WiroError` (`code`, `statusCode`): `WiroAuthenticationError`, `WiroValidationError`, `WiroSchemaValidationError`, `WiroApiResultError` (`apiCode`), `WiroRateLimitError` (`retryAfterMs`, so back off), `WiroNetworkError`, `WiroTimeoutError`, `WiroWebSocketError` and `WiroUnknownApiError`. Show users a short message based on `error.code`.
- Retries: the client option `retryPolicy` (default `WiroRetryPolicy.default`, exponential backoff with jitter; `WiroRetryPolicy.none` turns it off) covers calls such as task lookups and model search. Runs and uploads are never retried automatically.
- Timeouts: `requestTimeoutMs` (each HTTP request) and `pollIntervalMs` on the client, `timeoutMs` on the tracking calls. If the WebSocket fails, `subscribe` continues by polling.
- Logging: never log keys, secrets, proxy tokens or raw response bodies. Use `JSON.stringify` on SDK objects for redacted output, and keep `task.raw`, `result.raw`, token `rawValue` and `error.rawResponseBody` out of logs, crash reports and analytics.

## Money rules

- Tell the user the expected cost before any paid run. Prices are on each model's page at https://wiro.ai/models and at https://wiro.ai/product/pricing. In code, `schema.model.dynamicPrice` and `approximateCost` carry the model's pricing (format: https://wiro.ai/docs/pricing).
- Ask before large or open-ended jobs: batches, loops, many outputs, long videos.
- After a timeout or a dropped connection, never resubmit the same run blindly, because a second run bills a second job. Look the task up first with `getTask`, `getTaskById` or `waitForTask`. Do not build automatic "generate again" retries around `run` or `subscribe`.
- Cancel or kill a task only when the user asks.

## More

- The REST API and the MCP server are covered by the general skill: `npx skills add wiroai/Wiro-Plugin --skill wiro-ai`.
- Docs: https://wiro.ai/docs/introduction. Models: https://wiro.ai/models. SDK: https://github.com/wiroai/ReactNative-QuickStart and https://www.npmjs.com/package/@wiro-ai/wiro-react-native.
