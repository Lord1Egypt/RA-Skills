---
name: wiro-flutter
description: Build Flutter and Dart apps on the official Wiro AI SDK (the wiro package on pub.dev) to generate images, video, speech, music and LLM output with typed or generic model requests, file inputs, task tracking and typed results. Use when the user wants AI generation in a Flutter or Dart app through Wiro, or mentions package:wiro, Wiro or a Wiro API key in Dart code.
---

# Wiro AI SDK for Dart and Flutter

`wiro` is the official Dart package for the Wiro AI model API. It runs any of the 1,000+ models in the Wiro catalog from Flutter apps, Dart servers and command-line tools. Every run creates a task on Wiro. The SDK starts it, follows it by polling or over a WebSocket, and returns a typed result with the outputs.

## Money rules

- Before any paid run (example scripts and test runs too), tell the user the model, the settings and the expected cost. Prices: https://wiro.ai/product/pricing. After the run, `task.totalCost` is the billed cost.
- Ask first before large or open-ended jobs: many outputs, long videos, loops, batches.
- After a timeout or a dropped connection, never resubmit the same run blindly. The task may still be running, and a resubmit bills a second job. Look the task up first (see "Long jobs and recovery").
- Cancel or kill a task only when the user asks.

## Install

Needs Dart 3.8.0 or newer, and Flutter 3.32.8 or newer in a Flutter app. The core is pure Dart and runs on the Dart VM, Android, iOS, web, macOS, Windows and Linux. Import `package:wiro/wiro.dart`.

```bash
flutter pub add wiro   # Flutter app
dart pub add wiro      # Dart server or CLI
```

## Create a client

Never ship long-lived Wiro credentials in a mobile binary, or in a web or desktop build. That includes `--dart-define` values, which can be extracted from a distributed app. In production, use the proxied client so the credentials stay on your backend:

```dart
final client = WiroClient.proxied(
  proxyUri: Uri.parse('https://your-backend.example.com/wiro'),
  headers: {'Authorization': 'Bearer $sessionToken'},
);
```

- The device sends no Wiro auth headers. Your proxy must accept the same REST paths as the Wiro API, attach `x-api-key` (plus the signature headers when the project needs them) and forward the request to `https://api.wiro.ai/v1`. Use `headers` to authenticate your own users against the proxy.
- Task WebSocket streams still connect straight to Wiro, because they use per-task tokens instead of API credentials.

On a server, in a CLI, or for local development only, pass the credentials directly:

```dart
final client = WiroClient(
  apiKey: 'YOUR_API_KEY',
  apiSecret: 'YOUR_API_SECRET', // signature projects only; omit for API key auth
);
```

- The credentials must match the authentication type chosen for the Wiro project. Create a project and key at https://wiro.ai/panel/project/new.
- In scripts, read `WIRO_API_KEY` and `WIRO_API_SECRET` from `Platform.environment`, as the example scripts do. Never print, log or commit them. The SDK's own logs never contain keys, secrets, headers or request bodies.
- Reuse one client and call `client.close()` when you are done.

## Run a model

Popular models have typed requests. Required parameters and select options are checked at compile time, value ranges by assertions in debug builds:

```dart
final result = await client.subscribeRequest(
  Wiro.flux2Pro(
    prompt: 'A cinematic mountain lake at sunrise',
    width: 1024,
    height: 1024,
    outputFormat: WiroFlux2ProOutputFormat.png,
  ),
);

switch (result) {
  case WiroTaskSuccess(:final task):
    print(task.outputs.first.url);
  case WiroTaskFailure(:final reason):
    print('Failed: ${reason.name}');
}
```

Typed factories (type `Wiro.` in the IDE): images `flux2Pro`, `gptImage2`, `nanoBananaPro`, `seedreamV4`, `grokImagineImage`; video `runwayGen45`, `seedance20`, `klingV3`, `veo31`, `hailuo23Fast`, `grokImagineVideo`; music `lyria3`.

Any other catalog model runs through `Wiro.model` with a parameter map. Validate the map against the model's schema first, so mistakes fail locally before a paid run:

```dart
const slug = 'black-forest-labs/flux-2-pro';
final schema = await client.getModelSchema(WiroModelId.parse(slug));
final parameters = <String, Object?>{'prompt': 'A cinematic mountain lake at sunrise'};
schema.validate(parameters); // throws WiroSchemaValidationException
final result = await client.subscribeRequest(Wiro.model(slug, parameters: parameters));
```

- Find models with `client.searchModels(search: '...')` or `client.explore()`, or browse https://wiro.ai/models. The slug is the `owner/model` shown on the model's page, and `schema.parameters` lists the input ids.
- LLMs have no typed request, so run them with `Wiro.model`. `task.debugOutput` holds the merged reply text. The text output (`output.isText`) carries `content`, and `output.raw` keeps the fields the SDK does not parse. For live text, track over WebSocket: each LLM progress event is a full snapshot (fields in `progress.raw`), so replace what you show instead of appending. See https://wiro.ai/docs/llm-chat-streaming.
- `subscribeRequest` (or `subscribe` with a `WiroModelId`) starts the run and tracks it to the end. Polling is the default; `trackingMode: WiroTaskTrackingMode.webSocket` gives live events. `onUpdate` receives each `WiroTaskUpdate` (`update.status`, `update.statusValue`).
- `client.subscribeStream(modelId, parameters: {...})` yields the same updates for an `await for` loop. Cancelling the subscription stops tracking.
- `task.outputs` is a list of `WiroTaskOutput` with `url`, `name`, `contentType` and the `isImage`, `isVideo`, `isAudio` and `isText` getters. `task.elapsed` is the task duration, and `task.isSuccessful` is the definitive success check.

## Long jobs and recovery

`subscribeRequest` does not hand back the task token when it throws. For video, music or anything you may need to recover after a timeout, a dropped connection or an app restart, split the run from the wait:

```dart
final run = await client.runRequest(Wiro.runwayGen45(
  prompt: 'A drone shot over misty mountains',
  ratio: WiroRunwayGen45Ratio.landscape16x9,
  duration: 2,
));
final taskToken = run.taskToken ?? (throw StateError('Wiro did not return a task token.'));
// Save taskToken.value now. WiroTaskToken(savedValue) restores it later.
final task = await client.waitForTask(taskToken); // then check task.isSuccessful
```

- `waitForTask`, `watchTask` and the `subscribe` calls stop waiting after `timeout:` (10 minutes by default) and throw `WiroTimeoutException`. The task keeps running on Wiro. Call `client.getTask(taskToken)` to see where it is, and `waitForTask` again to keep waiting. Do not start a new run. `getTaskById(run.taskId!)` works as well.
- If the run call itself throws a timeout or network error, there is no token and the run may still have started. That is why the SDK never retries runs or uploads. Do not resubmit on your own: tell the user and have them check the Wiro dashboard (https://wiro.ai/panel) first.
- `callbackUrl:` on `runRequest`, `runModel` or the `subscribe` calls makes Wiro send the completed task to your backend webhook.

## Files

```dart
final result = await client.subscribeRequest(
  Wiro.model('wiroai/flux-upscaler', parameters: {
    'inputImage': [WiroFileInput.bytes(await image.readAsBytes(), fileName: 'photo.jpg')],
  }),
);
```

- `WiroFileInput.bytes` takes device bytes, such as a gallery pick or a camera shot. The client uploads them and swaps in the URL before the run starts. Keep the extension in `fileName`.
- `WiroFileInput.url(Uri.parse('https://example.com/input.jpg'))` passes a file that is already hosted.
- Typed requests take the same values, for example `inputImages: [...]` on `Wiro.flux2Pro`.
- To upload yourself, `client.uploadFile(bytes, fileName: ...)` returns a `WiroUploadResult` whose `files.first.url` you pass on. `uploadStream` takes a stream and its exact `contentLength` for large files.

## Cancel, errors and timeouts

- Only when the user asks: `client.cancelTask(taskToken)` cancels a queued task, `client.killTask(taskToken)` stops a running one. A `WiroCancellationToken` passed as `cancellationToken:` is different: it stops the SDK call or tracking in your app (with `WiroRequestCancelledException`), not the task on Wiro.
- A finished run is `WiroTaskSuccess` or `WiroTaskFailure`, and both carry `task`. A failure's `reason` is `cancelled`, `processFailed` or `unknown`. The examples show `task.debugOutput` when it is set, otherwise the reason.
- Thrown errors extend `WiroException`. Catch the ones you act on:
  - `WiroAuthenticationException`: invalid or expired credentials.
  - `WiroRateLimitException`: back off and retry later; `error.retryAfter` is the suggested delay when set.
  - `WiroSchemaValidationException`: the local schema check failed; read `error.issues`.
  - `WiroApiResultException`: Wiro rejected the operation; read `error.code` and `error.message`.
  - `WiroTimeoutException`, `WiroNetworkException`, `WiroWebSocketException`: if a run was already submitted, look the task up before anything else.
  - Also `WiroValidationException`, `WiroUnknownApiException` and `WiroRequestCancelledException`. See https://wiro.ai/docs/error-reference.
- Client options on both constructors: `requestTimeout` (per HTTP request), `pollInterval`, `retryPolicy` and `logger`. Use `WiroRetryPolicy(maxRetries: 3, initialDelay: Duration(milliseconds: 500))` or `WiroRetryPolicy.none()`. Automatic retries apply to safe calls such as model and task lookups, and rate-limit retries respect `Retry-After`. Runs and uploads are never retried automatically.

## Flutter notes

From the example app in the SDK repo (`example/lib`):

- Create the client in `initState`. In `dispose()`, cancel the active `WiroCancellationToken` and call `client.close()`. Leaving the page does not stop the task on Wiro, so keep its token if you still want the result.
- Ignore taps while a run is in flight and disable the button (`onPressed: isLoading ? null : onGenerate`), so one tap is one billed job.
- Show the stage from `onUpdate` (`update.status.name`) and check `mounted` before you set state. For a progress bar, track over WebSocket and read `progress.percentage` from `WiroProgressPayload` events, as `example/bin/generate_video.dart` does.
- Take the first output that has a URL and show it with `Image.network`:

```dart
Image.network(
  imageUrl.toString(),
  fit: BoxFit.cover,
  loadingBuilder: (context, child, progress) =>
      progress == null ? child : const Center(child: CircularProgressIndicator()),
  errorBuilder: (context, error, stackTrace) =>
      const Icon(Icons.broken_image_outlined),
)
```

- Video and audio outputs are URLs too (`output.isVideo`, `output.isAudio`). The SDK has no player, so use the media package your app already has.
- `flutter run --dart-define=WIRO_API_KEY=...` is for local demos only.

## More

- The REST API and the Wiro MCP server are covered by the general skill: `npx skills add wiroai/Wiro-Plugin --skill wiro-ai`.
- Docs: https://wiro.ai/docs/introduction
- Models catalog: https://wiro.ai/models
- SDK source and examples: https://github.com/wiroai/Dart-QuickStart
