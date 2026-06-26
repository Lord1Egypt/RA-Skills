# Keychain Token Storage & Biometric Authentication

Self-contained reference for storing authentication tokens in Keychain and
protecting them with Keychain-bound biometric authentication (Face ID /
Touch ID). Covers the patterns most commonly needed alongside Sign in with
Apple, passkey, and OAuth flows.

This is an authentication-adjacent quick reference, not a full security
architecture guide. Route Keychain migration, access-control policy design,
CryptoKit encryption, Secure Enclave keys, certificate pinning, keychain
sharing, storage-hardening strategy, and OWASP MASVS/MASTG mapping to
`swift-security`.

## Contents

- [Storing Tokens in Keychain](#storing-tokens-in-keychain)
- [Reading Tokens from Keychain](#reading-tokens-from-keychain)
- [Deleting Tokens from Keychain](#deleting-tokens-from-keychain)
- [Biometric Authentication with LAContext](#biometric-authentication-with-lacontext)
- [Biometric-Protected Keychain Items](#biometric-protected-keychain-items)
- [Keychain Error Handling](#keychain-error-handling)
- [References](#references)

## Storing Tokens in Keychain

The Keychain is the ONLY correct place to store tokens, passwords, API keys, or
secrets. Never store these in UserDefaults, files, or Core Data.

```swift
func saveToKeychain(account: String, data: Data, service: String) throws {
    let query: [String: Any] = [
        kSecClass as String: kSecClassGenericPassword,
        kSecAttrAccount as String: account,
        kSecAttrService as String: service,
        kSecValueData as String: data,
        kSecAttrAccessible as String: kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly
    ]

    let status = SecItemAdd(query as CFDictionary, nil)

    if status == errSecDuplicateItem {
        let updateQuery: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: account,
            kSecAttrService as String: service
        ]
        let updates: [String: Any] = [kSecValueData as String: data]
        let updateStatus = SecItemUpdate(updateQuery as CFDictionary, updates as CFDictionary)
        guard updateStatus == errSecSuccess else {
            throw KeychainError.updateFailed(updateStatus)
        }
    } else if status != errSecSuccess {
        throw KeychainError.saveFailed(status)
    }
}
```

## Reading Tokens from Keychain

```swift
func readFromKeychain(account: String, service: String) throws -> Data {
    let query: [String: Any] = [
        kSecClass as String: kSecClassGenericPassword,
        kSecAttrAccount as String: account,
        kSecAttrService as String: service,
        kSecReturnData as String: true,
        kSecMatchLimit as String: kSecMatchLimitOne
    ]

    var result: AnyObject?
    let status = SecItemCopyMatching(query as CFDictionary, &result)

    guard status == errSecSuccess, let data = result as? Data else {
        throw KeychainError.readFailed(status)
    }
    return data
}
```

## Deleting Tokens from Keychain

```swift
func deleteFromKeychain(account: String, service: String) throws {
    let query: [String: Any] = [
        kSecClass as String: kSecClassGenericPassword,
        kSecAttrAccount as String: account,
        kSecAttrService as String: service
    ]

    let status = SecItemDelete(query as CFDictionary)
    guard status == errSecSuccess || status == errSecItemNotFound else {
        throw KeychainError.deleteFailed(status)
    }
}
```

Use a `ThisDeviceOnly` accessibility class for sensitive app credentials unless
the product explicitly requires restore or sharing behavior. Choose broader
Keychain accessibility, migration, or sharing strategy in `swift-security`, not
in this authentication skill.

Do not use `kSecAttrAccessibleAlways` for app credentials; Apple marks it as not
recommended for application use because items remain accessible regardless of
lock state.


## Biometric Authentication with LAContext

Use `LAContext` from LocalAuthentication for Face ID / Touch ID prompts before
showing sensitive screens or performing protected actions. This is a local
interaction gate, not proof that a stored secret is safe to release. For tokens,
private keys, or high-value credentials, bind access to the Keychain item with
`SecAccessControl` and let `SecItemCopyMatching` perform the authentication.

```swift
import LocalAuthentication

func authenticateWithBiometrics() async throws -> Bool {
    let context = LAContext()
    var error: NSError?

    guard context.canEvaluatePolicy(
        .deviceOwnerAuthenticationWithBiometrics, error: &error
    ) else {
        // Biometrics not available -- fall back to passcode
        if context.canEvaluatePolicy(.deviceOwnerAuthentication, error: &error) {
            return try await context.evaluatePolicy(
                .deviceOwnerAuthentication,
                localizedReason: "Authenticate to access your account"
            )
        }
        throw AuthError.biometricsUnavailable
    }

    return try await context.evaluatePolicy(
        .deviceOwnerAuthenticationWithBiometrics,
        localizedReason: "Authenticate to access your account"
    )
}
```

### Info.plist Requirement

You MUST include `NSFaceIDUsageDescription` in Info.plist:

```xml
<key>NSFaceIDUsageDescription</key>
<string>Authenticate to access your secure data</string>
```

Missing this key causes a crash on Face ID devices.

### LAContext Configuration

```swift
let context = LAContext()
context.localizedFallbackTitle = "Use Passcode"
context.touchIDAuthenticationAllowableReuseDuration = 30
let currentState = context.evaluatedPolicyDomainState // Compare to detect enrollment changes
```

## Biometric-Protected Keychain Items

Protect keychain items so they require biometric authentication to read:

```swift
let access = SecAccessControlCreateWithFlags(
    nil,
    kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly,
    .biometryCurrentSet,
    nil
)!

let query: [String: Any] = [
    kSecClass as String: kSecClassGenericPassword,
    kSecAttrAccount as String: "auth-token",
    kSecValueData as String: tokenData,
    kSecAttrAccessControl as String: access
]
```

Read the protected item with an authentication context so Keychain, not app
logic, controls release of the secret:

```swift
let context = LAContext()
context.localizedReason = "Authenticate to access your account"

let query: [String: Any] = [
    kSecClass as String: kSecClassGenericPassword,
    kSecAttrAccount as String: "auth-token",
    kSecReturnData as String: true,
    kSecMatchLimit as String: kSecMatchLimitOne,
    kSecUseAuthenticationContext as String: context
]

var result: AnyObject?
let status = SecItemCopyMatching(query as CFDictionary, &result)
guard status == errSecSuccess, let tokenData = result as? Data else {
    throw KeychainError.readFailed(status)
}
```

Use `.biometryCurrentSet` when an auth token must be invalidated after biometric
enrollment changes. Route broader SecAccessControl flag selection and policy
tradeoffs to `swift-security`.


## Keychain Error Handling

```swift
enum KeychainError: Error {
    case saveFailed(OSStatus)
    case updateFailed(OSStatus)
    case readFailed(OSStatus)
    case deleteFailed(OSStatus)

    var localizedDescription: String {
        switch self {
        case .saveFailed(let status),
             .updateFailed(let status),
             .readFailed(let status),
             .deleteFailed(let status):
            return SecCopyErrorMessageString(status, nil) as String? ?? "Unknown error"
        }
    }
}
```

## References

- [Restricting keychain item accessibility](https://sosumi.ai/documentation/security/restricting-keychain-item-accessibility)
- [Accessing Keychain Items with Face ID or Touch ID](https://sosumi.ai/documentation/localauthentication/accessing-keychain-items-with-face-id-or-touch-id)
- [LAContext](https://sosumi.ai/documentation/localauthentication/lacontext)
- [NSFaceIDUsageDescription](https://sosumi.ai/documentation/bundleresources/information-property-list/nsfaceidusagedescription)
- [kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly](https://sosumi.ai/documentation/security/ksecattraccessiblewhenpasscodesetthisdeviceonly)
- [SecAccessControlCreateFlags.userPresence](https://sosumi.ai/documentation/security/secaccesscontrolcreateflags/userpresence)
- [SecAccessControlCreateFlags.biometryCurrentSet](https://sosumi.ai/documentation/security/secaccesscontrolcreateflags/biometrycurrentset)
