---
name: wiro-kotlin
description: Run Wiro AI models from Android and Kotlin apps with WiroKit, the official Wiro SDK for Kotlin and Android, covering Gradle setup, client auth, typed and catalog model runs with coroutines and Flows, file uploads and task control. Use when Kotlin, Android or Jetpack Compose code generates images, video, speech, music or LLM output with Wiro, or when the user mentions WiroKit.
---

# WiroKit for Kotlin and Android

WiroKit (`ai.wiro:wirokit`) is the official Kotlin library for the Wiro AI API on Android. It runs any model in the Wiro catalog through typed request factories or `Wiro.model`, tracks each task by polling or WebSocket with coroutines and Flows, and uploads input files for you. Source and a Jetpack Compose sample app: https://github.com/wiroai/Kotlin-QuickStart.

WiroKit is an Android library (AAR). For Kotlin on a server or desktop JVM, call the REST API instead (see the last section).

## Install

Requirements: Android `minSdk` 26+, Kotlin 2.4+, JDK 17+ for builds, and a Wiro project with an API key (https://wiro.ai/panel/project/new).

```kotlin
// module build.gradle.kts, with mavenCentral() in your repositories
dependencies {
    implementation("ai.wiro:wirokit:0.1.0")
}
```

- Version catalog: `wirokit = { module = "ai.wiro:wirokit", version = "0.1.0" }`, then `implementation(libs.wirokit)`.
- If the artifact does not resolve from Maven Central yet, clone the Kotlin-QuickStart repo, run `./gradlew :wirokit:publishToMavenLocal` and add `mavenLocal()` before `mavenCentral()` in your repositories. Remove `mavenLocal()` once the Maven Central release is out.
- The SDK manifest already declares the `INTERNET` permission, and the AAR ships its own R8 consumer rules.

## Create a client

Keep Wiro credentials off the device. WiroKit's guidance is proxy mode for shipped apps, so long-lived API secrets never ship inside the binary; a key on the device is for local development and debug builds. Never hard-code, commit or log keys, secrets or proxy tokens. If the user has no key, send them to https://wiro.ai/panel/project/new and do not ask them to paste it into the chat.

```kotlin
// Shipped apps: your backend adds the Wiro credentials
val client = WiroClient(
    proxyUrl = "https://api.myapp.com/wiro/v1",
    headers = mapOf("Authorization" to "Bearer app-token"),
)

// Debug builds: API key
val client = WiroClient(apiKey = "YOUR_API_KEY")

// Debug builds of a signature project: key plus secret, every request HMAC signed
val client = WiroClient(apiKey = "YOUR_API_KEY", apiSecret = "YOUR_API_SECRET")
```

- Proxy mode stores no Wiro key. It sends the normal REST paths (`/Run/{owner}/{project}`, `/Task/Detail`, `/Task/Cancel`, `/Task/Kill`, `/File/Upload`, `/Tool/List`, `/Tool/Detail`, `/Tool/Explore`) to `proxyUrl` with your `headers`. Your backend checks its own user, adds the Wiro auth headers, forwards the call to `https://api.wiro.ai/v1` and returns Wiro's response unchanged.
- Pass `apiSecret` only for a project that uses signature auth (https://wiro.ai/docs/authentication).
- Name the first argument (`apiKey =` or `proxyUrl =`), since both constructors take a `String` first.
- Optional settings: `requestTimeout`, `pollInterval`, `retryPolicy`, `logger`, and `okHttpClient` to share your app's OkHttp client. The SDK's default client sets `retryOnConnectionFailure(false)`; set it on yours too, so OkHttp does not retry calls after connection failures on its own.
- `WiroClient` is `Closeable`. Keep one app-scoped instance, or `close()` each client you own.

## Money rules

- Before any paid run (a live test, the sample app, a script), tell the user the model, the settings and the expected cost from the model's page on https://wiro.ai/models or https://wiro.ai/product/pricing. A finished `WiroTask` reports its cost in `totalCost`.
- Ask first for large or open-ended jobs: many outputs, long videos, loops or batches.
- Each `run`, `runModel`, `subscribe` or `subscribeStream` call starts a new billable task. After a timeout or a dropped connection, never resubmit the same run blindly. Look the task up first (see Control and errors). App code follows the same rule: no automatic resubmits.
- Cancel or kill a task only when the user asks.

## Run a model

```kotlin
import ai.wiro.wirokit.Wiro
import ai.wiro.wirokit.WiroTaskResult
import ai.wiro.wirokit.subscribe

val result = client.subscribe(
    Wiro.flux2Pro(prompt = "A cinematic mountain lake", width = 1024, height = 1024),
)
when (result) {
    is WiroTaskResult.Success -> println(result.task.outputs.firstOrNull()?.url)
    is WiroTaskResult.Failure -> println("Failed: ${result.reason}")
}
```

- Typed factories on `Wiro`: `flux2Pro`, `gptImage2`, `nanoBananaPro`, `seedreamV4`, `grokImagineImage` (image), `runwayGen45`, `seedance20`, `klingV3`, `veo31`, `sora2Pro`, `hailuo23Fast`, `grokImagineVideo` (video) and `lyria3` (music). They check inputs and throw `WiroValidationException` before any network call.
- Every other catalog model, speech and LLMs included, runs through `Wiro.model`:

```kotlin
val request = Wiro.model(
    slug = "black-forest-labs/flux-2-pro",
    parameters = mapOf(
        "prompt" to WiroValue.StringValue("Sunset over the bay"),
        "width" to WiroValue.number(1024),
        "height" to WiroValue.number(1024),
    ),
) // then client.subscribe(request)
```

- Find slugs with `client.searchModels(search = "...")` (each of `.items` has a `modelId`) or `client.explore()`. `client.getModelSchema(WiroModelId("owner", "project"))` describes the inputs: each entry of `schema.parameters` has a `name` (the key to send) and `isRequired`, and `schema.validate(parameters)` returns a list of problems, empty when the map fits.
- Live updates: `client.subscribeStream(request)` returns a `Flow<WiroTaskUpdate>` (`Snapshot`, `Event` with progress, `Binary`). The billable run starts before the Flow is returned, so collecting it again only re-tracks the same task. `trackingMode = WiroTaskTrackingMode.WEB_SOCKET` streams socket events with a polling fallback; both modes end on a terminal `Snapshot`.
- Start now and wait later, the pattern to use when you may need to recover:

```kotlin
val run = client.run(request)             // starts one billable task
val token = requireNotNull(run.taskToken) // persist run.taskId and the token
val task = client.waitForTask(token)
```

- Outputs: `task.outputs` holds `WiroTaskOutput` items with `url` (a `java.net.URI`), `contentType`, `name` and `isImage`, `isVideo`, `isAudio`, `isText`. LLM replies are in an output's `content?.answers` (plus `thinking` and `rawText`), and the merged text is in `task.debugOutput`. `task.isSuccessful` means it completed with exit code 0.
- `subscribe`, `subscribeStream`, `run`, `waitForTask` and the `ContentResolver` overloads are extension functions, so import them from `ai.wiro.wirokit`.

## Files

```kotlin
val bytes = WiroFileInput.Bytes(bytes = imageBytes, fileName = "photo.png")
val photo = WiroFileInput.ContentUri(uri = contentUri, fileName = "photo.png") // streamed
val result = client.subscribe(
    Wiro.flux2Pro(prompt = "The same lake at night", inputImages = listOf(photo)),
    contentSource = WiroUriContentSource.from(contentResolver),
)
```

- File inputs inside the run parameters are uploaded automatically before `/Run`. `ContentUri` inputs need a `contentSource`, or the `runModel(..., contentResolver = contentResolver)` overload.
- `WiroFileInput.Url(URI("https://..."))` sends a public file URL as is.
- In a `Wiro.model` map, wrap a file as `WiroValue.FileInputValue(input)`.
- To reuse a file, upload it once: `client.uploadFile(bytes)` or `client.uploadFile(photo, contentResolver)` returns a `WiroUploadResult` whose `files` carry the hosted `url`.

## Control and errors

- Cancelling the coroutine or `Job` that collects stops local work at once; rethrow `CancellationException`. It does not stop the task on Wiro.
- To stop it on Wiro, only when the user asks: `client.cancelTask(taskId)` while it is queued, `client.killTask(token)` or `client.killTask(taskId)` once it runs. Both return a `Boolean`.
- A task that finishes unsuccessfully is a `WiroTaskResult.Failure` with a `reason` (`CANCELLED`, `NON_ZERO_EXIT`, `OTHER`), not an exception.
- Thrown errors extend `WiroException`: `WiroValidationException`, `WiroAuthenticationException`, `WiroApiResultException` (the API answered `result: false`, see `code`), `WiroRateLimitException` (`retryAfter`), `WiroNetworkException`, `WiroWebSocketException`, `WiroUnknownApiException` and `WiroTimeoutException`. Error codes: https://wiro.ai/docs/error-reference.
- Retries: `WiroRetryPolicy.Default` retries transient failures with exponential backoff and respects `retryAfter`; `WiroRetryPolicy.None` turns retries off. `/Run` and uploads are never retried automatically.
- Timeouts: `requestTimeout` covers one HTTP call, and `timeout` on `subscribe`, `subscribeStream` and `waitForTask` covers tracking (default `WiroTracking.DEFAULT_TIMEOUT`). A `WiroTimeoutException` means the task was still running at the deadline.
- Recovering: after a `WiroTimeoutException`, a `WiroNetworkException` or a dropped connection, look the task up with `client.getTask(token)` or `client.getTaskById(id)`, or keep waiting with `client.waitForTask(token)`. With `subscribe`, keep the token from `onUpdate` (`Snapshot.task.taskToken`). If `run` itself failed and you hold no id, ask the user to check the dashboard (https://wiro.ai/panel) before sending it again.
- Never log keys, secrets, proxy tokens or raw response bodies. Use `rawResponseBody` only for local diagnostics.

## Android and Compose

Patterns from the sample app (`app/` in the repo):

```kotlin
// In a ViewModel; the show* calls stand for your own StateFlow updates.
generationJob = viewModelScope.launch {
    try {
        client.subscribeStream(request).collect { update ->
            update.status?.let { showStatus(it.apiValue) }
            if (update is WiroTaskUpdate.Snapshot && update.task.status.isTerminal) {
                val task = update.task
                if (task.isSuccessful) {
                    showImages(task.outputs.mapNotNull { it.url?.toASCIIString() })
                } else {
                    showError(task.debugOutput ?: "Generation failed")
                }
            }
        }
    } catch (error: CancellationException) {
        throw error
    } catch (error: WiroException) {
        showError(error.toFriendlyMessage()) // the sample's safe UI text helper
    }
}
```

- Read the `StateFlow` in Compose with `collectAsStateWithLifecycle()`, and keep the `Job` for a local cancel.
- Save `task.id` and `task.taskToken` from snapshots (or `message.id` and `message.taskToken` from WebSocket events) so a cancel or kill button can use them.
- The sample opens a client per generation and closes it in `finally` and in `onCleared()`.
- Render images with Coil: `AsyncImage(model = url, ...)` from `io.coil-kt.coil3:coil-compose` with `coil-network-okhttp`.
- Do not restart a billable run automatically after process death; start one only when the user taps Generate again.
- Release builds of the sample accept only a backend proxy URL (`BuildConfig.ALLOW_DIRECT_CREDENTIALS` is false there), and debug builds keep a typed-in key encrypted with Android Keystore-backed AES-GCM. Keep `android:allowBackup="false"` if the app stores secrets.

## More

- The REST API and the Wiro MCP server are covered by the general skill: `npx skills add wiroai/Wiro-Plugin --skill wiro-ai`.
- Docs: https://wiro.ai/docs/introduction
- Models: https://wiro.ai/models
