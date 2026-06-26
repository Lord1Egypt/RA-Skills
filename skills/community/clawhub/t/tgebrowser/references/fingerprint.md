# FingerprintConfig (fingerprint config for create-browser / update-browser)

**fingerprint** is passed under `create-browser` / `update-browser`. All fields are optional unless noted.

- **os** (required for create-browser): Operating system. e.g. `"Windows"`, `"macOS"`, `"Android"`, `"iOS"`
- **kernel** (optional): Browser kernel version string, e.g. `"143"`. See [kernel-config.md](kernel-config.md) for valid values.
- **userAgent** (optional): Custom User-Agent string.
- **resolution** (optional): Screen resolution, e.g. `"1920_1080"`. Use `"none"` to follow computer.
- **windowWidth** / **windowHeight** (optional): Window size in pixels.
- **language** (optional): Language string, e.g. `"en-US"`.
- **languageBaseIp** (optional): Auto-set language by IP. `true` / `false`.
- **uiLanguage** (optional): UI language, e.g. `"en-US"`.
- **uiLanguageBaseIp** (optional): Auto-set UI language by IP. `true` / `false`.
- **timezone** (optional): Timezone, e.g. `"America/New_York"`.
- **timezoneBaseIp** (optional): Auto-set timezone by IP. `true` / `false`.
- **geolocationBaseIp** (optional): Auto-set geolocation by IP. `true` / `false`.
- **lat** / **lng** (optional): Custom latitude/longitude strings when geolocationBaseIp is false.
- **canvas** (optional): Canvas fingerprint noise. `true` add noise / `false` computer default.
- **audioContext** (optional): Audio fingerprint noise. `true` / `false`.
- **speechVoices** (optional): Replace speech voices. `true` / `false`.
- **clientRects** (optional): ClientRects noise. `true` / `false`.
- **fonts** (optional): Font list, e.g. `["Arial", "Times New Roman"]`.
- **webrtc** (optional): WebRTC policy. e.g. `"disabled"` / `"forward"` / `"proxy"` / `"local"`.
- **ram** (optional): Device memory (GB), e.g. `4`.
- **cpu** (optional): CPU cores, e.g. `4`.
- **hardwareAcceleration** (optional): `true` / `false`.
- **disableSandbox** (optional): `true` / `false`.
- **startupParams** (optional): Extra browser startup params string.
- **deviceName** (optional): Custom device name string.
- **deviceMedia** (optional): Media device noise. `true` / `false`.
- **portScanProtection** (optional): Port scan protection. e.g. `"1"` enable / `"0"` disable.
- **randomFingerprint** (optional): Randomize all fingerprint fields. `true` / `false`.
- **blockLargeImages** (optional): `true` / `false`.
- **maxImageKB** (optional): Max image size in KB.
- **syncCookies** (optional): `true` / `false`.
- **clearCacheOnStart** (optional): `true` / `false`.
- **clearCachePreserveExtensionsOnStart** (optional): `true` / `false`.
- **clearCookiesOnStart** (optional): `true` / `false`.
- **clearHistoryOnStart** (optional): `true` / `false`.
- **disableMediaAutoplay** (optional): `true` / `false`.
- **muteAllMedia** (optional): `true` / `false`.
- **disableGoogleTranslate** (optional): `true` / `false`.
- **disableSavePasswordPrompt** (optional): `true` / `false`.
- **disableNotifications** (optional): `true` / `false`.
- **blockClipboardRead** (optional): `true` / `false`.
- **stopOnNetworkIssue** (optional): `true` / `false`.
- **stopOnIPChange** (optional): `true` / `false`.
- **stopOnCountryChange** (optional): `true` / `false`.
- **disableTLS** (optional): Array of TLS cipher hex codes to disable. See [tls-cipher.md](tls-cipher.md).
- **mobileDeviceId** (optional): Mobile device id (number).
- **platformVersion** (optional): Platform version (number).

Example: `"fingerprint":{"os":"Windows","kernel":"143","timezone":"America/New_York","language":"en-US","webrtc":"disabled"}`
