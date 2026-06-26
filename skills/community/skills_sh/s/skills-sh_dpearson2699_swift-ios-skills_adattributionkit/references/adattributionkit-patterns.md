# AdAttributionKit Patterns

Extended patterns for postback verification, server-side handling, testing,
SKAdNetwork migration, alternative marketplaces, and attribution rules
configuration.

## Contents

- [Postback Verification](#postback-verification)
- [Server-Side Postback Handling](#server-side-postback-handling)
- [JWS Impression Generation](#jws-impression-generation)
- [Testing with Developer Mode](#testing-with-developer-mode)
- [Creating Postbacks in Developer Settings](#creating-postbacks-in-developer-settings)
- [Migration from SKAdNetwork](#migration-from-skadnetwork)
- [Alternative Marketplaces](#alternative-marketplaces)
- [Attribution Rules Configuration](#attribution-rules-configuration)
- [Conversion Tags for Overlapping Windows](#conversion-tags-for-overlapping-windows)
- [Error Handling](#error-handling)
- [References](#references)

## Postback Verification

The device signs postbacks with Apple's private key. Verify the JWS signature
before counting any conversion.

### Select the correct public key

Apple uses different keys depending on the environment:

| Key ID                            | Environment                          |
|-----------------------------------|--------------------------------------|
| `apple-cas-identifier/0`         | Production                           |
| `apple-development-identifier/0` | Development (end-to-end flows)       |
| `apple-development-identifier/1` | Development (developer settings)     |

### Verify with CryptoKit

```swift
import CryptoKit
import Foundation

enum PostbackVerificationError: Error {
    case unknownKeyID
    case invalidPublicKey
    case invalidJWS
    case signatureVerificationFailed
}

struct PostbackVerifier {

    static func verify(jwsString: String) throws -> [String: Any] {
        let parts = jwsString.split(separator: ".").map(String.init)
        guard parts.count == 3 else {
            throw PostbackVerificationError.invalidJWS
        }

        let headerData = try base64URLDecode(parts[0])
        let payloadData = try base64URLDecode(parts[1])
        let signatureData = try base64URLDecode(parts[2])

        guard let header = try JSONSerialization.jsonObject(
            with: headerData
        ) as? [String: String],
              let keyID = header["kid"] else {
            throw PostbackVerificationError.invalidJWS
        }

        let publicKey = try getPublicKey(forKeyID: keyID)
        let signedData = Data("\(parts[0]).\(parts[1])".utf8)
        let signature = try P256.Signing.ECDSASignature(
            rawRepresentation: signatureData
        )

        guard publicKey.isValidSignature(signature, for: signedData) else {
            throw PostbackVerificationError.signatureVerificationFailed
        }

        guard let payload = try JSONSerialization.jsonObject(
            with: payloadData
        ) as? [String: Any] else {
            throw PostbackVerificationError.invalidJWS
        }

        return payload
    }

    static func getPublicKey(
        forKeyID keyID: String
    ) throws -> P256.Signing.PublicKey {
        let base64Key: String
        switch keyID {
        case "apple-cas-identifier/0":
            base64Key = "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEWdp8GPcGqmhgzEFj9Z2nSpQVddayaPe4FMzqM9wib1+aHaaIzoHoLN9zW4K8y4SPykE3YVK3sVqW6Af0lfx3gg=="
        case "apple-development-identifier/0":
            base64Key = "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAELeEDzpJEP+/qRSE5hJVC1p1J0ssUnQGMzBBbvnACBok8OVGGLgxL0myrKiy6lvRtSlLRsWit87i+vftD8AEqeQ=="
        case "apple-development-identifier/1":
            base64Key = "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE8YzdO7eM97s/IJ25kdW5CZ3A14USE5IJ5Ha/vhWaxI6UBI1ZxCEvjrKxVluVGe6qWwF1BDFq+QHqKfH5u+wxHQ=="
        default:
            throw PostbackVerificationError.unknownKeyID
        }

        guard let keyData = Data(base64Encoded: base64Key) else {
            throw PostbackVerificationError.invalidPublicKey
        }
        return try P256.Signing.PublicKey(derRepresentation: keyData)
    }

    private static func base64URLDecode(_ string: String) throws -> Data {
        var base64 = string
            .replacingOccurrences(of: "-", with: "+")
            .replacingOccurrences(of: "_", with: "/")
        while base64.count % 4 != 0 {
            base64.append("=")
        }
        guard let data = Data(base64Encoded: base64) else {
            throw PostbackVerificationError.invalidJWS
        }
        return data
    }
}
```

### Ignore invalid postbacks

In production, always use the `apple-cas-identifier/0` key. Discard any
postback that fails signature verification -- do not count it as a conversion.

## Server-Side Postback Handling

### Postback JSON structure

The device sends an HTTPS POST with JSON:

```json
{
  "jws-string": "<JWS compact serialization>",
  "conversion-value": 24,
  "ad-interaction-type": "click",
  "country-code": "US"
}
```

The `conversion-value`, `ad-interaction-type`, and `country-code` fields are
outside the JWS and present only at higher crowd anonymity tiers.

### JWS payload fields

Decoded from the JWS `jws-string`:

| Field                          | Type    | Description                                     |
|--------------------------------|---------|-------------------------------------------------|
| `postback-identifier`          | String  | Unique ID for deduplication                     |
| `ad-network-identifier`        | String  | Ad network that signed the impression           |
| `source-identifier`            | String  | 2-4 digit hierarchical source ID                |
| `advertised-item-identifier`   | Integer | App Store item ID of the advertised app         |
| `publisher-item-identifier`    | Integer | App Store item ID of the publisher app (Tier 3) |
| `marketplace-identifier`       | String  | Bundle ID of the marketplace (if not App Store) |
| `impression-type`              | String  | Always `"app-impression"`                       |
| `did-win`                      | Boolean | Whether this postback won attribution           |
| `postback-sequence-index`      | Integer | 0, 1, or 2 (conversion window index)            |
| `conversion-type`              | String  | `"download"`, `"redownload"`, or `"re-engagement"` |

### Deduplication

Use `postback-identifier` to deduplicate. Discard any postback with a
`postback-identifier` already processed.

### Response requirements

Respond with HTTP 200 immediately. On HTTP 500, the device retries up to 9
times over a maximum of 9 days. Process the postback asynchronously.

### Winning vs. nonwinning postbacks

- **Winning**: one per conversion; contains full data per tier.
- **Nonwinning**: up to 5 ad networks receive one each per install conversion.
  Re-engagement has no nonwinning postbacks.

## JWS Impression Generation

Ad networks generate signed JWS impressions on their servers and deliver them
to the publisher app.

### JOSE header

```json
{
    "alg": "ES256",
    "kid": "example.adattributionkit"
}
```

Use `ES256` signing. The `kid` is the registered ad network ID.

### JWS payload

```json
{
    "impression-identifier": "7aa9f8cc-5689-4c02-b963-22ca22136015",
    "publisher-item-identifier": 525463029,
    "impression-type": "app-impression",
    "ad-network-identifier": "example.adattributionkit",
    "source-identifier": 5239,
    "timestamp": 1679790422446,
    "advertised-item-identifier": 1108187390,
    "eligible-for-re-engagement": true
}
```

| Field                          | Required | Notes                                  |
|--------------------------------|----------|----------------------------------------|
| `impression-identifier`        | Yes      | UUID generated per impression          |
| `publisher-item-identifier`    | Yes      | Use `0` for Developer Mode development impressions |
| `impression-type`              | Yes      | Always `"app-impression"`              |
| `ad-network-identifier`        | Yes      | Must match `kid` in header             |
| `source-identifier`            | Yes      | 2-4 digit hierarchical ID              |
| `timestamp`                    | Yes      | Milliseconds since 1970                |
| `advertised-item-identifier`   | Yes      | App Store item ID                      |
| `eligible-for-re-engagement`   | No       | `true` to enable re-engagement         |

### Signing

Sign with the private key generated during ad network registration using
ES256 (ECDSA with P-256 and SHA-256). The compact JWS format is:

```
BASE64URL(header) . BASE64URL(payload) . BASE64URL(signature)
```

### Key generation

Generate the ECDSA key pair using OpenSSL:

```bash
# Private key
openssl ecparam -name prime256v1 -genkey -noout \
    -out company_adattributionkit_private_key.pem

# Public key (share with Apple during registration)
openssl ec -in company_adattributionkit_private_key.pem \
    -pubout -out company_adattributionkit_public_key.pem
```

## Testing with Developer Mode

### Enable Developer Mode (iOS 18+)

1. Enable Developer Mode on the test device (Settings > Privacy & Security >
   Developer Mode).
2. Go to Settings > Developer > Ad Attribution Testing.
3. Enable the AdAttributionKit Developer Mode switch.

Developer Mode reduces conversion windows from days to minutes and postback
delays from hours to 5-10 minutes.

### Reduced time windows in Developer Mode

| Window | Normal duration | Developer Mode |
|--------|----------------|----------------|
| 1st    | Days 0-2       | 0-3 minutes    |
| 2nd    | Days 3-7       | 3-6 minutes    |
| 3rd    | Days 8-35      | 6-9 minutes    |
| Delay  | 24-48 hours    | 5-10 minutes   |

### Create development impressions

Use `publisher-item-identifier: 0` in the JWS payload for Developer Mode
development impressions. The system prioritizes production impressions over
development impressions if both exist.

### Inspect postbacks via HTTP proxy

With Developer Mode enabled, configure an HTTP proxy on the device (Settings >
Wi-Fi > network > HTTP Proxy > Manual) to intercept AdAttributionKit postbacks.

### Important testing notes

- Use a production Apple ID (not sandbox) for testing.
- Developer Mode automatically disables after two weeks.
- Development postbacks use `apple-development-identifier/0` as the key ID.
- Production impressions always take priority over development impressions.

## Creating Postbacks in Developer Settings

For testing without a publisher app, use the on-device development postbacks
tool.

### Steps

1. Enable Developer Mode on the test device.
2. Go to Settings > Developer > Ad Attribution Testing > Development Postbacks.
3. Enter the advertised app's bundle identifier (it must be installed).
4. Provide a server URL for receiving the postback.
5. Configure postback properties (interaction type, conversion type, conversion
   windows).
6. Optionally adjust crowd anonymity tiers to test different data levels.

### Transmit postbacks on demand

Tap "Transmit Development Postbacks" to send eligible postbacks immediately
instead of waiting for automatic delivery.

### Developer Settings postback differences

- `kid` in JWS header: `apple-development-identifier/1`
- `ad-network-identifier`: `development.adattributionkit`
- `conversion-type`: `"download"`, `"redownload"`, or `"re-engagement"`
- `advertised-item-identifier`: `0` for Xcode-installed apps; actual ID for
  App Store / marketplace installs.

## Migration from SKAdNetwork

AdAttributionKit is the successor to SKAdNetwork. Both frameworks coexist and
the system evaluates impressions from both when determining attribution winners.

### Key differences

| Feature                        | SKAdNetwork          | AdAttributionKit     |
|--------------------------------|----------------------|----------------------|
| Marketplace support            | App Store only       | App Store + alt      |
| Re-engagement                  | No                   | Yes (iOS 18+)        |
| Property list key              | `SKAdNetworkItems`   | `AdNetworkIdentifiers` |
| Postback copy key              | `NSAdvertisingAttributionReportEndpoint` | `AttributionCopyEndpoint` |
| Conversion value API           | `SKAdNetwork.updatePostbackConversionValue` | `Postback.updateConversionValue` |
| Framework import               | `StoreKit`           | `AdAttributionKit`   |
| Conversion tags                | No                   | Yes (iOS 18.4+)      |
| Attribution rules config       | No                   | Yes (current docs)   |

### Dual framework support

During interoperability, AdAttributionKit and SKAdNetwork impressions are ranked
together and only one impression wins a conversion. Click-through ads take
precedence over view-through ads. Within click-through impressions, the most
recent tap wins; if there are no taps, the most recent view-through impression
wins.

Use the conversion update API for the framework that owns the pending postback:
AdAttributionKit APIs for AdAttributionKit integrations, SKAdNetwork APIs for
SKAdNetwork integrations, and both sets when the app is integrated with both.
The system ignores update calls when there are no pending postbacks for that
framework.

```swift
import AdAttributionKit
import StoreKit

func updateConversion(value: Int, coarse: CoarseConversionValue) async {
    do {
        try await Postback.updateConversionValue(
            value,
            coarseConversionValue: coarse,
            lockPostback: false
        )
    } catch {
        print("AdAttributionKit update failed: \(error)")
    }

    do {
        try await SKAdNetwork.updatePostbackConversionValue(
            value,
            coarseValue: .high,
            lockWindow: false
        )
    } catch {
        print("SKAdNetwork update failed: \(error)")
    }
}
```

Apple documents bridging from SKAdNetwork conversion-update calls into
AdAttributionKit postback update APIs, but this is not a universal one-API
migration shortcut. Dual-framework apps should still call both APIs so each
framework receives the update it expects.

### Ad network ID compatibility

Ad network IDs ending in `.adattributionkit` and `.skadnetwork` are compatible
across both frameworks. An ad network registered with SKAdNetwork can reuse its
existing ID with AdAttributionKit.

### Publisher app migration

Include ad network IDs for both frameworks in Info.plist:

```xml
<!-- SKAdNetwork (legacy) -->
<key>SKAdNetworkItems</key>
<array>
    <dict>
        <key>SKAdNetworkIdentifier</key>
        <string>example123.skadnetwork</string>
    </dict>
</array>

<!-- AdAttributionKit -->
<key>AdNetworkIdentifiers</key>
<array>
    <string>example123.adattributionkit</string>
</array>
```

## Alternative Marketplaces

AdAttributionKit supports alternative app marketplaces in addition to the App
Store. The `marketplace-identifier` field in postbacks contains the bundle ID
of the marketplace from which the conversion originated.

- For App Store conversions: `marketplace-identifier` is `com.apple.AppStore`.
- For alternative marketplace conversions: the bundle ID of that marketplace.
- The `marketplace-identifier` is omitted from Tier 0 postbacks.

No additional client-side setup is required. The system automatically includes
the marketplace identifier based on where the app was installed from.

## Attribution Rules Configuration

Current AdAttributionKit documentation describes configurable attribution
windows and cooldown periods through Info.plist.

### Attribution windows

Control how long impressions remain eligible for attribution:

```xml
<key>AdAttributionKitConfigurations</key>
<dict>
    <key>AttributionWindows</key>
    <dict>
        <!-- Global settings for all ad networks -->
        <key>global</key>
        <dict>
            <key>install</key>
            <dict>
                <key>view</key>
                <integer>3</integer>  <!-- 1-7 days, default 1 -->
                <key>click</key>
                <integer>14</integer> <!-- 1-30 days, default 30 -->
            </dict>
        </dict>

        <!-- Per-network override -->
        <key>example.adattributionkit</key>
        <dict>
            <key>install</key>
            <dict>
                <key>click</key>
                <integer>7</integer>
                <key>ignoreInteractionType</key>
                <string>view</string>
            </dict>
        </dict>
    </dict>
</dict>
```

**Precedence**: ad network config > global config > system default.

The `ignoreInteractionType` key is only valid in per-ad-network configurations,
not in the global section. Set it to `"view"` or `"click"` to ignore that
interaction type from the specified ad network during attribution.

### Attribution cooldown

Control the minimum time between conversions:

```xml
<key>AdAttributionKitConfigurations</key>
<dict>
    <key>AttributionCooldown</key>
    <dict>
        <!-- Hours after install before accepting new conversions -->
        <key>install-cooldown-hours</key>
        <integer>24</integer>  <!-- 0-720 hours -->

        <!-- Hours after re-engagement before accepting new conversions -->
        <key>re-engagement-cooldown-hours</key>
        <integer>12</integer>  <!-- 0-720 hours -->
    </dict>
</dict>
```

## Conversion Tags for Overlapping Windows

When multiple re-engagement conversions occur close together, conversion tags
(iOS 18.4+) let the advertised app update specific postbacks independently.

### Receive the tag

The system delivers the conversion tag through the re-engagement URL:

```swift
func handleReengagementURL(_ url: URL) {
    let components = URLComponents(url: url, resolvingAgainstBaseURL: false)
    if let tagItem = components?.queryItems?.first(where: {
        $0.name == Postback.reengagementOpenURLParameter
    }) {
        let conversionTag = tagItem.value
        // Persist the tag alongside an internal conversion identifier
        saveConversionTag(conversionTag)
    }
}
```

### Update a specific conversion

```swift
func updateSpecificConversion(tag: String, value: Int) async {
    let update = PostbackUpdate(
        fineConversionValue: value,
        lockPostback: false,
        conversionTag: tag,
        conversionTypes: [.reengagement]
    )
    do {
        try await Postback.updateConversionValue(update)
    } catch {
        print("Failed to update tagged conversion: \(error)")
    }
}
```

If no conversion tag is specified, AdAttributionKit updates the most recent
conversion (pre-iOS 18.4 behavior).

## Error Handling

### AdAttributionKitError cases

| Error                              | Cause                                                   |
|------------------------------------|---------------------------------------------------------|
| `.impressionExpired`               | Impression older than its time window                   |
| `.missingAttributionView`          | `handleTap()` called without `UIEventAttributionView`   |
| `.invalidImpressionJWSComponents`  | JWS string is not valid compact JWS format              |
| `.invalidImpressionJWSHeader`      | JWS header missing required fields or wrong algorithm   |
| `.invalidImpressionJWSPayload`     | JWS payload missing required fields                     |
| `.invalidImpressionJWSSignature`   | Signature verification failed                           |
| `.invalidConversionTag`            | Conversion tag format is invalid                        |
| `.conversionTagNotSupported`       | Conversion tag used on unsupported OS version           |
| `.unknown`                         | Unrecoverable internal error                            |

### Defensive impression handling

```swift
func safeHandleImpression(_ jwsString: String) async {
    do {
        let impression = try await AppImpression(compactJWS: jwsString)
        try await impression.handleView()
    } catch let error as AdAttributionKitError {
        switch error {
        case .invalidImpressionJWSComponents,
             .invalidImpressionJWSHeader,
             .invalidImpressionJWSPayload,
             .invalidImpressionJWSSignature:
            // Log and request a new impression from the ad network
            reportInvalidImpression(jwsString, error: error)
        case .impressionExpired:
            // Request a fresh impression
            refreshImpression()
        case .missingAttributionView:
            // Only relevant for handleTap, not handleView
            break
        default:
            print("AdAttributionKit error: \(error)")
        }
    } catch {
        print("Unexpected error: \(error)")
    }
}
```

## References

- [Apple: Configuring an advertised app](https://sosumi.ai/documentation/adattributionkit/configuring-an-advertised-app)
- [Apple: Generating JWS impressions](https://sosumi.ai/documentation/adattributionkit/generating-jws-impressions)
- [Apple: Identifying postback parameters](https://sosumi.ai/documentation/adattributionkit/identifying-the-parameters-in-a-postback)
- [Apple: Receiving postbacks in multiple conversion windows](https://sosumi.ai/documentation/adattributionkit/receiving-postbacks-in-multiple-conversion-windows)
- [Apple: Testing with Developer Mode](https://sosumi.ai/documentation/adattributionkit/testing-adattributionkit-with-developer-mode)
- [Apple: Creating postbacks in Developer Settings](https://sosumi.ai/documentation/adattributionkit/creating-postbacks-in-developer-settings)
- [Apple: SKAdNetwork interoperability](https://sosumi.ai/documentation/adattributionkit/adattributionkit-skadnetwork-interoperability)
- [Apple: Configuring attribution rules](https://sosumi.ai/documentation/adattributionkit/configuring-attribution-rules-for-your-app)
- [WWDC24: Meet AdAttributionKit](https://sosumi.ai/videos/play/wwdc2024/10060)
- [WWDC25: What's new in AdAttributionKit](https://sosumi.ai/videos/play/wwdc2025/221)
