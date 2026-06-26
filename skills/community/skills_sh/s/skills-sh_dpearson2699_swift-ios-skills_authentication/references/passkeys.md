# Passkey Authentication Patterns

Use this reference when implementing app-native passkey registration, passkey
sign-in, AutoFill-assisted passkey suggestions, or physical security key
fallbacks with AuthenticationServices.

## Contents

- [Prerequisites](#prerequisites)
- [Registration](#registration)
- [Assertion Sign-In](#assertion-sign-in)
- [Handling Results](#handling-results)
- [AutoFill-Assisted Requests](#autofill-assisted-requests)
- [Physical Security Keys](#physical-security-keys)
- [Common Failure Modes](#common-failure-modes)
- [References](#references)

## Prerequisites

Passkeys are public-private key credentials. The device keeps the private key
in iCloud Keychain for platform passkeys, and your server, the relying party,
stores and verifies the public credential material.

Before making registration or assertion requests:

1. Add the Associated Domains capability.
2. Add `webcredentials:example.com` for the relying party domain.
3. Host a valid apple-app-site-association file for that domain.
4. Request every registration or assertion challenge from the server.

The relying party identifier passed to
`ASAuthorizationPlatformPublicKeyCredentialProvider` is normally the domain
name, such as `example.com`. The app cannot use passkeys for services that are
not configured as associated domains.

## Registration

Registration creates a new platform passkey for an account. The server should
generate a challenge and stable user ID bytes for the relying-party account.

```swift
import AuthenticationServices

func beginPasskeyRegistration(username: String) async throws {
    let challenge: Data = try await server.registrationChallenge(for: username)
    let userID: Data = try await server.passkeyUserID(for: username)

    let provider = ASAuthorizationPlatformPublicKeyCredentialProvider(
        relyingPartyIdentifier: "example.com"
    )
    let request = provider.createCredentialRegistrationRequest(
        challenge: challenge,
        name: username,
        userID: userID
    )

    let controller = ASAuthorizationController(authorizationRequests: [request])
    controller.delegate = passkeyDelegate
    controller.presentationContextProvider = presentationProvider
    controller.performRequests()
}
```

After the delegate receives
`ASAuthorizationPlatformPublicKeyCredentialRegistration`, send the registration
response to the server. The server verifies the challenge and stores the public
credential data for future assertions.

## Assertion Sign-In

Assertion signs in with an existing passkey. Always use a fresh server challenge.

```swift
func beginPasskeySignIn(usernameHint: String?) async throws {
    let challenge: Data = try await server.assertionChallenge(usernameHint)

    let provider = ASAuthorizationPlatformPublicKeyCredentialProvider(
        relyingPartyIdentifier: "example.com"
    )
    let request = provider.createCredentialAssertionRequest(challenge: challenge)

    let controller = ASAuthorizationController(authorizationRequests: [request])
    controller.delegate = passkeyDelegate
    controller.presentationContextProvider = presentationProvider
    controller.performRequests()
}
```

If the user has no passkey for the relying party, the request fails. Offer
registration, password sign-in, or Sign in with Apple as appropriate for the
account recovery flow.

## Handling Results

Handle passkey credentials in the same `ASAuthorizationControllerDelegate`
method as Sign in with Apple and password credentials:

```swift
func authorizationController(
    controller: ASAuthorizationController,
    didCompleteWithAuthorization authorization: ASAuthorization
) {
    switch authorization.credential {
    case let registration as ASAuthorizationPlatformPublicKeyCredentialRegistration:
        Task { try await server.finishRegistration(registration) }

    case let assertion as ASAuthorizationPlatformPublicKeyCredentialAssertion:
        Task { try await server.finishAssertion(assertion) }

    case let credential as ASAuthorizationAppleIDCredential:
        handleAppleIDCredential(credential)

    case let password as ASPasswordCredential:
        signIn(username: password.user, password: password.password)

    default:
        break
    }
}
```

Do not treat a local passkey result as the final proof of authentication. The
relying-party server must verify the challenge and credential response before
issuing an app session.

## AutoFill-Assisted Requests

Use AutoFill-assisted requests when the login screen has a username text field
and should show inline passkey suggestions.

```swift
usernameField.textContentType = .username

let request = provider.createCredentialAssertionRequest(challenge: challenge)
let controller = ASAuthorizationController(authorizationRequests: [request])
controller.delegate = passkeyDelegate
controller.presentationContextProvider = presentationProvider
controller.performAutoFillAssistedRequests()
```

The controller presents UI when a text field with the appropriate content type
gets focus. This is usually better than immediately showing a modal sheet on a
username/password screen.

## Physical Security Keys

Use `ASAuthorizationSecurityKeyPublicKeyCredentialProvider` only when the user
needs a physical FIDO security key over NFC, USB, or Lightning. Keep this as a
separate branch from platform passkeys because the provider, registration
request, and UX differ:

```swift
let provider = ASAuthorizationSecurityKeyPublicKeyCredentialProvider(
    relyingPartyIdentifier: "example.com"
)
let request = provider.createCredentialAssertionRequest(challenge: challenge)
```

Apps can offer both platform and security-key assertion requests in the same
`ASAuthorizationController` when the relying party supports both.

## Common Failure Modes

- Missing `webcredentials:` Associated Domains entitlement or AASA entry for
  the relying-party domain.
- Reusing challenges or generating challenges on device instead of on the
  relying-party server.
- Treating `ASAuthorizationPlatformPublicKeyCredentialAssertion` as complete
  authentication before server verification.
- Using the app bundle ID as the relying party identifier when the server's
  WebAuthn relying party is a domain.
- Forgetting `performAutoFillAssistedRequests()` for inline passkey suggestions.
- Using the platform provider when the product requirement is a physical
  security key.

## References

- [Supporting passkeys](https://sosumi.ai/documentation/authenticationservices/supporting-passkeys)
- [ASAuthorizationPlatformPublicKeyCredentialProvider](https://sosumi.ai/documentation/authenticationservices/asauthorizationplatformpublickeycredentialprovider)
- [ASAuthorizationPlatformPublicKeyCredentialRegistration](https://sosumi.ai/documentation/authenticationservices/asauthorizationplatformpublickeycredentialregistration)
- [ASAuthorizationPlatformPublicKeyCredentialAssertion](https://sosumi.ai/documentation/authenticationservices/asauthorizationplatformpublickeycredentialassertion)
- [ASAuthorizationSecurityKeyPublicKeyCredentialProvider](https://sosumi.ai/documentation/authenticationservices/asauthorizationsecuritykeypublickeycredentialprovider)
- [ASAuthorizationController.performAutoFillAssistedRequests](https://sosumi.ai/documentation/authenticationservices/asauthorizationcontroller/performautofillassistedrequests())
