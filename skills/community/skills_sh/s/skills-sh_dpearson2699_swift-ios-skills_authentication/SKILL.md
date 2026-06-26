---
name: authentication
description: "Implement iOS authentication flows with AuthenticationServices and LocalAuthentication. Use when building Sign in with Apple, passkey/WebAuthn registration or sign-in with ASAuthorizationPlatformPublicKeyCredentialProvider, ASAuthorizationController credential state and revocation handling, ASWebAuthenticationSession OAuth or third-party login, Password AutoFill, identity-token server validation, or local biometric re-authentication with LAContext."
---

# Authentication

Implement authentication flows on iOS using the AuthenticationServices
framework, including Sign in with Apple, passkeys, OAuth/third-party web
auth, Password AutoFill, and biometric re-authentication.

## Contents

- [Sign in with Apple](#sign-in-with-apple)
- [Credential Handling](#credential-handling)
- [Credential State Checking](#credential-state-checking)
- [Token Validation](#token-validation)
- [Existing Account Setup Flows](#existing-account-setup-flows)
- [Passkeys](#passkeys)
- [ASWebAuthenticationSession (OAuth)](#aswebauthenticationsession-oauth)
- [Password AutoFill Credentials](#password-autofill-credentials)
- [Biometric Authentication](#biometric-authentication)
- [Security Boundaries](#security-boundaries)
- [SwiftUI SignInWithAppleButton](#swiftui-signinwithapplebutton)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Sign in with Apple

Add the "Sign in with Apple" capability in Xcode before using these APIs.

### UIKit: ASAuthorizationController Setup

```swift
import AuthenticationServices

final class LoginViewController: UIViewController {
    func startSignInWithApple() {
        let provider = ASAuthorizationAppleIDProvider()
        let request = provider.createRequest()
        request.requestedScopes = [.fullName, .email]

        let controller = ASAuthorizationController(authorizationRequests: [request])
        controller.delegate = self
        controller.presentationContextProvider = self
        controller.performRequests()
    }
}

extension LoginViewController: ASAuthorizationControllerPresentationContextProviding {
    func presentationAnchor(for controller: ASAuthorizationController) -> ASPresentationAnchor {
        view.window!
    }
}
```

### Delegate: Handling Success and Failure

```swift
extension LoginViewController: ASAuthorizationControllerDelegate {
    func authorizationController(
        controller: ASAuthorizationController,
        didCompleteWithAuthorization authorization: ASAuthorization
    ) {
        guard let credential = authorization.credential
            as? ASAuthorizationAppleIDCredential else { return }

        let userID = credential.user  // Stable, unique, per-team identifier
        let email = credential.email  // nil after first authorization
        let fullName = credential.fullName  // nil after first authorization
        let identityToken = credential.identityToken  // JWT for server validation
        let authCode = credential.authorizationCode  // Short-lived code for server exchange

        // Save userID to Keychain for credential state checks
        // See references/keychain-biometric.md for Keychain patterns
        saveUserID(userID)

        // Send identityToken and authCode to your server
        authenticateWithServer(identityToken: identityToken, authCode: authCode)
    }

    func authorizationController(
        controller: ASAuthorizationController,
        didCompleteWithError error: any Error
    ) {
        let authError = error as? ASAuthorizationError
        switch authError?.code {
        case .canceled:
            break  // User dismissed
        case .failed:
            showError("Authorization failed")
        case .invalidResponse:
            showError("Invalid response")
        case .notHandled:
            showError("Not handled")
        case .notInteractive:
            break  // Non-interactive request failed -- expected for silent checks
        default:
            showError("Unknown error")
        }
    }
}
```

## Credential Handling

`ASAuthorizationAppleIDCredential` properties and their behavior:

| Property | Type | First Auth | Subsequent Auth |
|---|---|---|---|
| `user` | `String` | Always | Always |
| `email` | `String?` | Provided if requested | `nil` |
| `fullName` | `PersonNameComponents?` | Provided if requested | `nil` |
| `identityToken` | `Data?` | JWT encoded as UTF-8 data | JWT encoded as UTF-8 data |
| `authorizationCode` | `Data?` | Short-lived code | Short-lived code |
| `realUserStatus` | `ASUserDetectionStatus` | Fraud-prevention signal | Do not rely on later attempts |

**Critical:** `email` and `fullName` are provided ONLY on the first
authorization. Cache them immediately during the initial sign-up flow. If the
user later deletes and re-adds the app, these values will not be returned.

```swift
func handleCredential(_ credential: ASAuthorizationAppleIDCredential) {
    // Always persist the user identifier
    let userID = credential.user

    // Cache name and email IMMEDIATELY -- only available on first auth
    if let fullName = credential.fullName {
        let name = PersonNameComponentsFormatter().string(from: fullName)
        UserProfile.saveName(name)  // Persist to your backend
    }
    if let email = credential.email {
        UserProfile.saveEmail(email)  // Persist to your backend
    }
}
```

## Credential State Checking

Check credential state on every app launch. The user may revoke access at
any time via Settings > Apple Account > Sign-In & Security.

```swift
func checkCredentialState() {
    let provider = ASAuthorizationAppleIDProvider()
    guard let userID = loadSavedUserID() else {
        showLoginScreen()
        return
    }

    provider.getCredentialState(forUserID: userID) { state, _ in
        DispatchQueue.main.async {
            switch state {
            case .authorized:
                proceedToMainApp()
            case .revoked:
                // User revoked -- sign out and clear local data
                signOut()
                showLoginScreen()
            case .notFound:
                showLoginScreen()
            case .transferred:
                // App transferred to new team -- migrate user identifier
                migrateUser()
            @unknown default:
                showLoginScreen()
            }
        }
    }
}
```

### Credential Revocation Notification

```swift
NotificationCenter.default.addObserver(
    forName: ASAuthorizationAppleIDProvider.credentialRevokedNotification,
    object: nil,
    queue: .main
) { _ in
    // Sign out immediately
    AuthManager.shared.signOut()
}
```

## Token Validation

The `identityToken` is a JWT. Send it to your server for validation --
never trust it client-side alone.

```swift
func sendTokenToServer(credential: ASAuthorizationAppleIDCredential) async throws {
    guard let tokenData = credential.identityToken,
          let token = String(data: tokenData, encoding: .utf8),
          let authCodeData = credential.authorizationCode,
          let authCode = String(data: authCodeData, encoding: .utf8) else {
        throw AuthError.missingToken
    }

    var request = URLRequest(url: URL(string: "https://api.example.com/auth/apple")!)
    request.httpMethod = "POST"
    request.setValue("application/json", forHTTPHeaderField: "Content-Type")
    request.httpBody = try JSONEncoder().encode(
        ["identityToken": token, "authorizationCode": authCode]
    )

    let (data, response) = try await URLSession.shared.data(for: request)
    guard (response as? HTTPURLResponse)?.statusCode == 200 else {
        throw AuthError.serverValidationFailed
    }
    let session = try JSONDecoder().decode(SessionResponse.self, from: data)
    // Store session token in Keychain -- see references/keychain-biometric.md
    try KeychainHelper.save(session.accessToken, forKey: "accessToken")
}
```

Server-side, validate the JWT against Apple's public keys at
`https://appleid.apple.com/auth/keys` (JWKS). Verify: `iss` is
`https://appleid.apple.com`, `aud` matches your bundle ID, `exp` not passed.

## Existing Account Setup Flows

On launch, silently check for existing Sign in with Apple and password
credentials before showing a login screen:

```swift
func performExistingAccountSetupFlows() {
    let appleIDRequest = ASAuthorizationAppleIDProvider().createRequest()
    let passwordRequest = ASAuthorizationPasswordProvider().createRequest()

    let controller = ASAuthorizationController(
        authorizationRequests: [appleIDRequest, passwordRequest]
    )
    controller.delegate = self
    controller.presentationContextProvider = self
    controller.performRequests(
        options: .preferImmediatelyAvailableCredentials
    )
}
```

Call this in `viewDidAppear` or on app launch. If no existing credentials
are found, the delegate receives a `.notInteractive` error -- handle it
silently and show your normal login UI.

## Passkeys

Use passkeys for passwordless WebAuthn-style registration and sign-in. The
app must have an Associated Domains entitlement for the relying party domain
using the `webcredentials:` service; passkey requests fail for services the app
has not configured as associated domains.

For platform passkeys synced through iCloud Keychain, request a server-provided
challenge and create requests with `ASAuthorizationPlatformPublicKeyCredentialProvider`:

```swift
let challenge: Data = try await server.registrationChallenge()
let userID: Data = try await server.passkeyUserID()
let provider = ASAuthorizationPlatformPublicKeyCredentialProvider(
    relyingPartyIdentifier: "example.com"
)
let request = provider.createCredentialRegistrationRequest(
    challenge: challenge,
    name: username,
    userID: userID
)

let controller = ASAuthorizationController(authorizationRequests: [request])
controller.delegate = self
controller.presentationContextProvider = self
controller.performRequests()
```

For sign-in, use `createCredentialAssertionRequest(challenge:)` with a fresh
server challenge, then send the resulting registration or assertion object to
the relying-party server for verification:

```swift
let request = provider.createCredentialAssertionRequest(challenge: challenge)

switch authorization.credential {
case let registration as ASAuthorizationPlatformPublicKeyCredentialRegistration:
    try await server.finishPasskeyRegistration(registration)
case let assertion as ASAuthorizationPlatformPublicKeyCredentialAssertion:
    try await server.finishPasskeySignIn(assertion)
default:
    break
}
```

For inline passkey suggestions, set the username field's `textContentType` to
`.username`, include the passkey assertion request in the controller, and call
`performAutoFillAssistedRequests()`. Use `ASAuthorizationSecurityKeyPublicKeyCredentialProvider`
only when the user must authenticate with a physical security key. See
[references/passkeys.md](references/passkeys.md) for complete registration,
assertion, AutoFill, and security-key patterns.

## ASWebAuthenticationSession (OAuth)

Use `ASWebAuthenticationSession` for OAuth and third-party authentication
(Google, GitHub, etc.). Never use `WKWebView` for auth flows.

```swift
import AuthenticationServices

final class OAuthController: NSObject, ASWebAuthenticationPresentationContextProviding {
    private weak var presentationAnchor: ASPresentationAnchor?

    init(presentationAnchor: ASPresentationAnchor) {
        self.presentationAnchor = presentationAnchor
    }

    func startOAuthFlow() {
        let authURL = URL(string:
            "https://provider.com/oauth/authorize?client_id=YOUR_ID&redirect_uri=myapp://callback&response_type=code"
        )!
        let session = ASWebAuthenticationSession(
            url: authURL, callback: .customScheme("myapp")
        ) { callbackURL, error in
            guard let callbackURL, error == nil,
                  let code = URLComponents(url: callbackURL, resolvingAgainstBaseURL: false)?
                      .queryItems?.first(where: { $0.name == "code" })?.value else { return }
            Task { await self.exchangeCodeForTokens(code) }
        }
        session.presentationContextProvider = self
        session.prefersEphemeralWebBrowserSession = true  // No shared cookies
        session.start()
    }

    func presentationAnchor(for session: ASWebAuthenticationSession) -> ASPresentationAnchor {
        guard let presentationAnchor else {
            fatalError("ASWebAuthenticationSession needs the active window")
        }
        return presentationAnchor
    }
}
```

In SwiftUI, use `@Environment(\.webAuthenticationSession)` and call
`authenticate(using:callback:preferredBrowserSession:additionalHeaderFields:)`
with `.customScheme("myapp")` or `.https(host:path:)`; prefer `.ephemeral`
only when the provider flow should avoid shared browser cookies.

## Password AutoFill Credentials

Use `ASAuthorizationPasswordProvider` to offer saved keychain credentials
alongside Sign in with Apple:

```swift
func performSignIn() {
    let appleIDRequest = ASAuthorizationAppleIDProvider().createRequest()
    appleIDRequest.requestedScopes = [.fullName, .email]

    let passwordRequest = ASAuthorizationPasswordProvider().createRequest()

    let controller = ASAuthorizationController(
        authorizationRequests: [appleIDRequest, passwordRequest]
    )
    controller.delegate = self
    controller.presentationContextProvider = self
    controller.performRequests()
}

// In delegate:
func authorizationController(
    controller: ASAuthorizationController,
    didCompleteWithAuthorization authorization: ASAuthorization
) {
    switch authorization.credential {
    case let appleIDCredential as ASAuthorizationAppleIDCredential:
        handleAppleIDLogin(appleIDCredential)
    case let passwordCredential as ASPasswordCredential:
        // User selected a saved password from keychain
        signInWithPassword(
            username: passwordCredential.user,
            password: passwordCredential.password
        )
    default:
        break
    }
}
```

Set `textContentType` on text fields for AutoFill to work:

```swift
usernameField.textContentType = .username
passwordField.textContentType = .password
```

## Biometric Authentication

Use `LAContext` from LocalAuthentication for local re-authentication before
showing account settings or starting sensitive actions. Do not treat a returned
`Bool` as proof to unlock a stored secret; protect secrets with Keychain access
control instead. See [references/keychain-biometric.md](references/keychain-biometric.md)
for `SecAccessControl` and `.biometryCurrentSet` patterns.

```swift
import LocalAuthentication

func authenticateWithBiometrics() async throws -> Bool {
    let context = LAContext()
    var error: NSError?

    guard context.canEvaluatePolicy(
        .deviceOwnerAuthenticationWithBiometrics, error: &error
    ) else {
        throw AuthError.biometricsUnavailable
    }

    return try await context.evaluatePolicy(
        .deviceOwnerAuthenticationWithBiometrics,
        localizedReason: "Sign in to your account"
    )
}
```

**Required:** Add `NSFaceIDUsageDescription` to Info.plist. Missing this
key crashes on Face ID devices.

## Security Boundaries

This skill owns user-facing account authentication: Sign in with Apple,
passkeys, Password AutoFill, ASAuthorizationController, OAuth session
presentation, credential state, and local biometric re-authentication. Route
deep security work to `swift-security`: Keychain architecture/migration,
CryptoKit, Secure Enclave, certificate pinning/trust, keychain sharing, storage
hardening, and OWASP MASVS/MASTG. Keep only the storage minimum here: tokens and
secrets belong in Keychain; `LAContext.evaluatePolicy` alone must not release
protected secrets.

## SwiftUI SignInWithAppleButton

Use `SignInWithAppleButton` in SwiftUI views when the login surface is SwiftUI.
Request `.fullName` and `.email`, handle `.success` and `.failure`, downcast to
`ASAuthorizationAppleIDCredential`, and send the credential through the same
server-validation flow as UIKit. Style with `.signInWithAppleButtonStyle(...)`.

## Common Mistakes

- Assuming a saved local session means the Apple ID credential is still valid.
  Check credential state at launch and handle revocation notifications.
- Showing a full login screen before trying existing account setup flows.
  Treat `.notInteractive` as the normal "no local credential" path.
- Force-unwrapping `email` or `fullName`. Cache them on first authorization and
  handle `nil` later.
- Creating an `ASAuthorizationController` without a presentation context
  provider. Authorization UI needs the active presentation anchor.
- Storing identity tokens, authorization codes, access tokens, passwords, or
  passkey server state in `UserDefaults`, files, or Core Data. Store secrets in
  Keychain and keep relying-party passkey verification server-side.
- Adding passkey requests without `webcredentials:` Associated Domains for the
  relying-party domain, or trying to use app-native passkeys for unrelated
  websites.
- Expanding authentication work into CryptoKit, Secure Enclave, certificate
  pinning, or OWASP MASVS. Route those to `swift-security`.

## Review Checklist

- [ ] "Sign in with Apple" capability added in Xcode project
- [ ] `ASAuthorizationControllerPresentationContextProviding` implemented
- [ ] Credential state checked on every app launch (`getCredentialState(forUserID:completion:)`)
- [ ] `credentialRevokedNotification` observer registered; sign-out handled
- [ ] `email` and `fullName` cached on first authorization (not assumed available later)
- [ ] `identityToken` sent to server for validation, not trusted client-side only
- [ ] Tokens stored in Keychain, not UserDefaults or files
- [ ] `performExistingAccountSetupFlows` called before showing login UI
- [ ] Error cases handled: `.canceled`, `.failed`, `.notInteractive`
- [ ] `NSFaceIDUsageDescription` in Info.plist for biometric auth
- [ ] `ASWebAuthenticationSession` used for OAuth (not `WKWebView`)
- [ ] `prefersEphemeralWebBrowserSession` set for OAuth when appropriate
- [ ] `textContentType` set on username/password fields for AutoFill
- [ ] Passkey relying party has `webcredentials:` Associated Domains configured
- [ ] Passkey registration/assertion challenges come from the server and are verified server-side
- [ ] Deep Keychain, CryptoKit, Secure Enclave, certificate pinning, and MASVS work routed to `swift-security`

## References

- Keychain & biometric patterns: [references/keychain-biometric.md](references/keychain-biometric.md)
- Passkey patterns: [references/passkeys.md](references/passkeys.md)
- [AuthenticationServices](https://sosumi.ai/documentation/authenticationservices)
- [ASAuthorizationAppleIDProvider](https://sosumi.ai/documentation/authenticationservices/asauthorizationappleidprovider)
- [ASAuthorizationAppleIDCredential](https://sosumi.ai/documentation/authenticationservices/asauthorizationappleidcredential)
- [ASAuthorizationController](https://sosumi.ai/documentation/authenticationservices/asauthorizationcontroller)
- [ASWebAuthenticationSession](https://sosumi.ai/documentation/authenticationservices/aswebauthenticationsession)
- [Supporting passkeys](https://sosumi.ai/documentation/authenticationservices/supporting-passkeys)
- [ASAuthorizationPlatformPublicKeyCredentialProvider](https://sosumi.ai/documentation/authenticationservices/asauthorizationplatformpublickeycredentialprovider)
- [ASAuthorizationPasswordProvider](https://sosumi.ai/documentation/authenticationservices/asauthorizationpasswordprovider)
- [SignInWithAppleButton](https://sosumi.ai/documentation/authenticationservices/signinwithapplebutton)
- [Implementing User Authentication with Sign in with Apple](https://sosumi.ai/documentation/authenticationservices/implementing-user-authentication-with-sign-in-with-apple)
