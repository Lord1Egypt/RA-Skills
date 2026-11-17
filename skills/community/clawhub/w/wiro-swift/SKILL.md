---
name: wiro-swift
description: Build iOS and SwiftUI apps with WiroKit, the official Wiro AI Swift SDK, from Swift Package Manager setup and proxy, API key or signature auth to typed and catalog model runs, file uploads, task tracking, cancellation and errors. Use when Swift code needs to generate images, video, music, speech or LLM output with Wiro in an iOS app.
---

# WiroKit, the Wiro AI Swift SDK

WiroKit is the official Swift package for calling the Wiro AI model API from iOS apps. It runs any of the 1,000+ models in the Wiro catalog through typed request factories or `Wiro.model`, follows each task by polling or WebSocket, and uploads device files for you. It is written in Swift 6 with async/await and has no third-party dependencies.

## Money rules

Successful model runs are billed to the user's Wiro project. These rules cover the calls you make and the app code you write.

- Before you run a model yourself (a test call, the example app, a script), tell the user the model, the settings and the expected cost. Prices are on each model's page at https://wiro.ai/models and at https://wiro.ai/product/pricing.
- Ask before large or open-ended jobs: many outputs, long videos, loops or batch scripts.
- After a timeout or a dropped connection, never resubmit the same run blindly, because that bills a second job. Look the task up first with `getTask` or `waitForTask` and the token you kept (or `getTaskByID`). With no token at all, ask the user to check their usage history at https://wiro.ai/panel/billing before you run again.
- Cancel or kill a task only when the user asks. In an app, that means the user tapped a control for it.
- WiroKit never retries runs or uploads on its own. Do not add automatic retries for them, and do not restart a billable run after an app relaunch unless the user taps Generate again.

## Install

Requirements: iOS 17+, Swift 6 (Xcode 16 or later) and a Wiro project with an API key from https://wiro.ai/panel/project/new.

```swift
dependencies: [
    .package(url: "https://github.com/wiroai/Swift-QuickStart.git", from: "0.1.0"),
],
```

Then link the `WiroKit` product to the app target. In Xcode, choose **File > Add Package Dependencies...**, enter the repository URL and link `WiroKit`.

## Create a client

Long-lived Wiro secrets never ship inside the app binary. Shipped apps use proxy mode: your backend attaches the Wiro credentials server-side, and the SDK stores no API key.

```swift
import WiroKit

let client = try WiroClient(
    proxyURL: URL(string: "https://api.example.com/wiro/v1")!,
    headers: ["Authorization": "Bearer \(sessionToken)"] // your app's own user session
)
```

- Each REST call goes to `proxyURL` plus the API path the SDK would call on Wiro (such as `/Run/{owner}/{project}`, `/Task/Detail` or `/File/Upload`). The backend forwards it to `https://api.wiro.ai/v1` and adds the project credentials (headers in https://wiro.ai/docs/authentication).
- Task WebSocket tracking still connects directly to Wiro, using a per-task token instead of a key.

The API key modes are for local development and the example app:

```swift
let client = try WiroClient(apiKey: "YOUR_API_KEY")
// Signature project: sends x-api-key, x-nonce and an HMAC-SHA256 x-signature
let signed = try WiroClient(apiKey: "YOUR_API_KEY", apiSecret: "YOUR_API_SECRET")
```

- The credentials must match the authentication method chosen for the Wiro project.
- Never hard-code or commit credentials, and never log keys, secrets, proxy tokens or raw response bodies.
- `WiroClient` is an actor, so every call is awaited. Both initializers also take `pollInterval`, `requestTimeout`, `retryPolicy` and `logger`.

## Run a model

```swift
let result = try await client.subscribe(
    Wiro.flux2Pro(prompt: "A cinematic mountain lake", width: 1024, height: 1024)
)

switch result {
case .success(let task):
    print(task.outputs.first?.url as Any)
case .failure(let task, let reason): // .cancelled, .nonZeroExit or .other
    print("Failed:", reason, task.status)
}
```

Typed factories (type `Wiro.` in Xcode): image `flux2Pro`, `gptImage2`, `nanoBananaPro`, `seedreamV4`, `grokImagineImage`; video `runwayGen45`, `seedance20`, `klingV3`, `veo31`, `sora2Pro`, `hailuo23Fast`, `grokImagineVideo`; music `lyria3`. They check required parameters and options at compile time and throw `WiroError.validation` when a value is out of range.

Any other catalog model, speech and LLMs included, runs through `Wiro.model` with its `owner/project` slug. Read the schema first:

```swift
let page = try await client.searchModels(search: "text to speech")
let ids = page.items.compactMap(\.modelID) // or copy a slug from https://wiro.ai/models

let schema = try await client.getModelSchema(WiroModelID(parsing: "owner/project")!)
let parameters: WiroJSON = ["prompt": "Hello from my app"]
let problems = schema.validate(parameters) // [] when the parameters fit
let result = try await client.subscribe(Wiro.model("owner/project", parameters: parameters))
```

`schema.parameters` lists each input's `name` and `isRequired`, and `schema.model.approximateCost` is Wiro's approximate cost for the model.

Where the results are:

- `task.outputs` holds `WiroTaskOutput` values: `url` for generated files, `contentType`, and `isImage`, `isVideo`, `isAudio`, `isText`.
- Text and LLM output: `task.outputs.first?.content?.rawText` (also `answers` and `thinking`). `task.debugOutput` has the merged text.
- `task.totalCost` is the final billed cost. Report it after a test run.
- `subscribe` returns `.success` only for a completed task with exit code 0. `waitForTask` and `getTask` return a `WiroTask`, so check `task.isSuccessful` or use `WiroTaskResult.from(task:)`.

## Wait for a task

- `subscribe` submits and then tracks by polling. Pass `onUpdate:` to see each update, or `trackingMode: .webSocket` for realtime events (it falls back to polling if the socket closes early).
- `subscribeStream` yields the same `WiroTaskUpdate` values for a `for try await` loop.
- `run` only submits, and returns `taskID` and `taskToken` right away. Use it for long jobs such as video: keep the token (save `token.rawValue`, rebuild it with `WiroTaskToken(rawValue:)`), then wait. A wait that times out leaves the task running on Wiro, so look it up again instead of submitting a new run.

```swift
let run = try await client.run(Wiro.flux2Pro(prompt: "A cinematic mountain lake"))
guard let token = run.taskToken else { return } // keep it, and run.taskID too
do {
    let task = try await client.waitForTask(token)
    print(task.isSuccessful, task.outputs.compactMap(\.url))
} catch WiroError.timedOut {
    let latest = try await client.getTask(token) // a lookup, not a new run
    print(latest.status)
}
```

## Files

```swift
let photo = WiroFileInput.data(imageData, fileName: "photo.png") // uploaded before the run
let hosted = WiroFileInput.url(URL(string: "https://example.com/photo.png")!)

let edit = try Wiro.nanoBananaPro(prompt: "Make it a watercolor", inputImages: [photo])
let other = try Wiro.model("owner/project", parameters: ["image": .fileInput(hosted)])
```

- Keep the extension in `fileName`. Typed factories take `WiroFileInput` values directly; in `Wiro.model` parameters, wrap each file in `.fileInput(...)` (arrays and nested objects work too).
- To upload yourself, call `uploadFile(_:fileName:)` for bytes or `uploadFile(at:fileName:)` to stream a file from disk, then read `upload.files.first?.url`.

## Control and errors

- **Stop local work:** cancel the Swift `Task` that awaits the call. The SDK throws `WiroError.cancelled`. Only on-device tracking stops; the task keeps running on Wiro.
- **Stop the task on Wiro, only when the user asks:** `cancelTask(taskID)` while it is queued, `killTask(token)` or `killTask(taskID)` once it runs. Each returns `true` when the API accepts the request.
- **Timeouts:** `subscribe`, `subscribeStream`, `waitForTask` and `watchTask` take `timeout:`, and the client's `requestTimeout` covers each HTTP attempt. A tracking timeout throws `WiroError.timedOut` and ends local tracking only.
- **Retries:** task and model lookups retry transient failures with exponential backoff (`retryPolicy: .default`; `.none` turns it off, or build your own `WiroRetryPolicy`). Runs and uploads are never retried.
- **Logging:** pass `logger: { event in ... }`. `WiroLogEvent` never includes credentials, headers or bodies.

```swift
do {
    let result = try await client.subscribe(request)
    print(result.task.status)
} catch let error as WiroError {
    switch error {
    case .timedOut, .network, .webSocket: break // the run may exist: look it up, do not resubmit
    case .cancelled: break // cancelled on the device
    case .authentication: break // check the key, secret or proxy headers
    case .validation, .schemaValidation: break // fix the parameters
    case .apiResult(let message, let code, _, _): print(code as Any, message) // the API declined it
    case .rateLimited, .unknownAPI: break // see https://wiro.ai/docs/error-reference
    }
}
```

## SwiftUI notes from the example app

The example app (`open Example/WiroExample.xcodeproj`) generates a FLUX.2 Pro image with `subscribeStream`.

- Keep the run in an `@Observable @MainActor` view model that holds the `Task` handle, so Cancel can call `generationTask?.cancel()` and navigation does not leak work.
- Ignore taps while a run is active (`guard !isRunning` and `.disabled(model.isRunning)`). A second tap is a second billed run.
- Loop with `for try await update in stream`, show `update.status`, and keep `task.id` and `task.taskToken` from `.snapshot` updates (`message.id` and `message.taskToken` from `.event`).
- Offer API cancel and kill as explicit choices next to local cancel (the example uses a `confirmationDialog`), never as automatic steps.
- Show images with `AsyncImage(url:)` from `task.outputs.compactMap(\.url)`.
- Keep development keys in the Keychain behind a `SecureField` (the example's `CredentialsStore`), never in source, and switch to proxy mode before shipping.

## More

- The REST API and the MCP server are covered by the general skill: `npx skills add wiroai/Wiro-Plugin --skill wiro-ai`.
- Docs: https://wiro.ai/docs/introduction
- Models: https://wiro.ai/models
- Realtime voice on iOS: https://github.com/wiroai/Swift-Realtime
