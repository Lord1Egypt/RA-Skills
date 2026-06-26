# CryptoTokenKit Extended Patterns

Advanced patterns for CryptoTokenKit: PIV smart card operations, TLV record
parsing, generic (non-smart-card) token drivers, APDU command helpers, and
token configuration management.

## Contents

- [PIV Smart Card Operations](#piv-smart-card-operations)
- [TLV Record Parsing](#tlv-record-parsing)
- [Generic Token Drivers](#generic-token-drivers)
- [APDU Command Helpers](#apdu-command-helpers)
- [Secure PIN Operations](#secure-pin-operations)
- [Token Configuration Management](#token-configuration-management)
- [Smart Card Slot Monitoring](#smart-card-slot-monitoring)
- [Token Registration](#token-registration)

## PIV Smart Card Operations

PIV (Personal Identity Verification, FIPS 201) smart cards use a standard
application identifier and defined data objects. Common operations include
selecting the PIV application, reading certificates, and performing
authentication.

### PIV Application Selection

```swift
import CryptoTokenKit

/// Standard PIV application identifier (NIST SP 800-73-4)
let pivAID = Data([
    0xA0, 0x00, 0x00, 0x03, 0x08, 0x00, 0x00, 0x10, 0x00, 0x01, 0x00
])

func selectPIVApplication(card: TKSmartCard) throws {
    try card.withSession {
        let (sw, _) = try card.send(
            ins: 0xA4,   // SELECT
            p1: 0x04,    // Select by name
            p2: 0x00,
            data: pivAID,
            le: nil
        )
        guard sw == 0x9000 else {
            throw PIVError.selectFailed(statusWord: sw)
        }
    }
}
```

### Reading PIV Data Objects

PIV defines standard data objects accessed via GET DATA:

```swift
/// PIV data object tags
enum PIVObject {
    /// X.509 Certificate for PIV Authentication (slot 9A)
    static let certAuth = Data([0x5C, 0x03, 0x5F, 0xC1, 0x05])
    /// X.509 Certificate for Digital Signature (slot 9C)
    static let certSign = Data([0x5C, 0x03, 0x5F, 0xC1, 0x0A])
    /// X.509 Certificate for Key Management (slot 9D)
    static let certKeyMgmt = Data([0x5C, 0x03, 0x5F, 0xC1, 0x0B])
    /// X.509 Certificate for Card Authentication (slot 9E)
    static let certCardAuth = Data([0x5C, 0x03, 0x5F, 0xC1, 0x01])
    /// Card Holder Unique Identifier (CHUID)
    static let chuid = Data([0x5C, 0x03, 0x5F, 0xC1, 0x02])
    /// Card Capability Container (CCC)
    static let ccc = Data([0x5C, 0x03, 0x5F, 0xC1, 0x07])
}

func readPIVObject(card: TKSmartCard, tag: Data) throws -> Data {
    try card.withSession {
        var fullResponse = Data()

        // GET DATA command (INS=CB for PIV)
        let (sw, response) = try card.send(
            ins: 0xCB,    // GET DATA
            p1: 0x3F,
            p2: 0xFF,
            data: tag,
            le: 0
        )

        fullResponse.append(response)

        // Handle chained responses (SW 61xx)
        var currentSW = sw
        while (currentSW >> 8) == 0x61 {
            let remaining = Int(currentSW & 0xFF)
            let (nextSW, nextResponse) = try card.send(
                ins: 0xC0,    // GET RESPONSE
                p1: 0x00,
                p2: 0x00,
                data: nil,
                le: remaining == 0 ? 256 : remaining
            )
            fullResponse.append(nextResponse)
            currentSW = nextSW
        }

        guard currentSW == 0x9000 else {
            throw PIVError.readFailed(statusWord: currentSW)
        }

        return fullResponse
    }
}
```

### PIV Authentication (GENERAL AUTHENTICATE)

```swift
func pivAuthenticate(
    card: TKSmartCard,
    keySlot: UInt8,
    algorithm: UInt8,
    challenge: Data
) throws -> Data {
    try card.withSession {
        // Build dynamic authentication template (tag 7C)
        var authData = Data()

        // Tag 81: challenge
        authData.append(0x81)
        authData.append(UInt8(challenge.count))
        authData.append(challenge)

        // Wrap in tag 7C
        var template = Data([0x7C])
        template.append(UInt8(authData.count))
        template.append(authData)

        let (sw, response) = try card.send(
            ins: 0x87,            // GENERAL AUTHENTICATE
            p1: algorithm,        // Algorithm reference
            p2: keySlot,          // Key reference (9A, 9C, 9D, 9E)
            data: template,
            le: 0
        )

        guard sw == 0x9000 else {
            throw PIVError.authFailed(statusWord: sw)
        }

        return response
    }
}
```

### PIV PIN Verification

```swift
func verifyPIN(card: TKSmartCard, pin: String) throws {
    try card.withSession {
        // PIV PIN is padded to 8 bytes with 0xFF
        var pinData = Data(pin.utf8.prefix(8))
        while pinData.count < 8 {
            pinData.append(0xFF)
        }

        let (sw, _) = try card.send(
            ins: 0x20,    // VERIFY
            p1: 0x00,
            p2: 0x80,    // PIV Application PIN
            data: pinData,
            le: nil
        )

        switch sw {
        case 0x9000:
            return  // Success
        case 0x6983:
            throw PIVError.pinBlocked
        case let sw where (sw >> 4) == 0x63C:
            let retriesLeft = Int(sw & 0x0F)
            throw PIVError.wrongPIN(retriesRemaining: retriesLeft)
        default:
            throw PIVError.verifyFailed(statusWord: sw)
        }
    }
}

enum PIVError: Error {
    case selectFailed(statusWord: UInt16)
    case readFailed(statusWord: UInt16)
    case authFailed(statusWord: UInt16)
    case verifyFailed(statusWord: UInt16)
    case wrongPIN(retriesRemaining: Int)
    case pinBlocked
}
```

### Extracting Certificates from PIV Response

PIV data objects are BER-TLV encoded. The certificate is nested inside
the response:

```swift
func extractCertificate(from pivResponse: Data) -> SecCertificate? {
    // Parse outer TLV (tag 53)
    guard let records = TKBERTLVRecord.sequenceOfRecords(from: pivResponse) else {
        return nil
    }

    for record in records {
        if record.tag == 0x53 {
            // Inside tag 53, find tag 70 (certificate)
            guard let innerRecords = TKBERTLVRecord.sequenceOfRecords(
                from: record.value
            ) else { continue }

            for inner in innerRecords {
                if inner.tag == 0x70 {
                    return SecCertificateCreateWithData(
                        nil, inner.value as CFData
                    )
                }
            }
        }
    }

    return nil
}
```

## TLV Record Parsing

CryptoTokenKit includes TLV (Tag-Length-Value) parsing classes for working
with structured smart card data.

### BER-TLV Records

BER-TLV is the standard encoding for ISO 7816 data objects:

```swift
import CryptoTokenKit

func parseBERTLV(data: Data) {
    guard let records = TKBERTLVRecord.sequenceOfRecords(from: data) else {
        print("Failed to parse TLV data")
        return
    }

    for record in records {
        print("Tag: 0x\(String(record.tag, radix: 16, uppercase: true))")
        print("Value length: \(record.value.count)")
        print("Value: \(record.value.map { String(format: "%02X", $0) }.joined())")

        // Recursively parse constructed tags
        if let nested = TKBERTLVRecord.sequenceOfRecords(from: record.value) {
            print("  Nested records:")
            for nestedRecord in nested {
                print("  Tag: 0x\(String(nestedRecord.tag, radix: 16, uppercase: true))")
            }
        }
    }
}
```

### Building BER-TLV Records

```swift
func buildTLVData() -> Data {
    // Build a simple TLV record
    let nameRecord = TKBERTLVRecord(
        tag: 0x5F20,
        value: Data("John Doe".utf8)
    )

    // Build a constructed TLV with nested records
    let container = TKBERTLVRecord(
        tag: 0x65,
        records: [nameRecord]
    )

    return container.data
}
```

### Compact TLV Records

Compact TLV is used in ATR historical bytes:

```swift
func parseATRHistoricalBytes(atr: TKSmartCardATR) {
    guard let records = atr.historicalRecords else {
        print("No historical records in ATR")
        return
    }

    for record in records {
        // Compact TLV tags are single bytes
        print("Tag: \(record.tag), Value: \(record.value.count) bytes")
    }
}
```

### Simple TLV Records

```swift
func buildSimpleTLV(tag: UInt8, value: Data) -> Data {
    let record = TKSimpleTLVRecord(tag: tag, value: value)
    return record.data
}
```

## Generic Token Drivers

For tokens that are not smart cards (USB security keys, software tokens),
use `TKTokenDriver` directly instead of `TKSmartCardTokenDriver`.

### Generic Driver Implementation

```swift
import CryptoTokenKit

final class GenericTokenDriver: TKTokenDriver, TKTokenDriverDelegate {
    override init() {
        super.init()
        self.delegate = self
    }

    func tokenDriver(
        _ driver: TKTokenDriver,
        tokenFor configuration: TKToken.Configuration
    ) throws -> TKToken {
        return GenericToken(
            tokenDriver: driver,
            instanceID: configuration.instanceID
        )
    }

    func tokenDriver(
        _ driver: TKTokenDriver,
        terminateToken token: TKToken
    ) {
        // Clean up resources when token is removed
    }
}
```

### Generic Token Implementation

```swift
final class GenericToken: TKToken, TKTokenDelegate {
    init(tokenDriver: TKTokenDriver, instanceID: TKToken.InstanceID) {
        super.init(tokenDriver: tokenDriver, instanceID: instanceID)
        self.delegate = self
    }

    func createSession(_ token: TKToken) throws -> TKTokenSession {
        return GenericTokenSession(token: token)
    }
}
```

### Generic Token Session

```swift
final class GenericTokenSession: TKTokenSession, TKTokenSessionDelegate {
    func tokenSession(
        _ session: TKTokenSession,
        supports operation: TKTokenOperation,
        keyObjectID: TKToken.ObjectID,
        algorithm: TKTokenKeyAlgorithm
    ) -> Bool {
        switch operation {
        case .signData:
            return algorithm.isAlgorithm(.ecdsaSignatureDigestX962SHA256)
                || algorithm.isAlgorithm(.rsaSignatureDigestPKCS1v15SHA256)
        case .decryptData:
            return algorithm.isAlgorithm(.rsaEncryptionOAEPSHA256)
        case .performKeyExchange:
            return algorithm.isAlgorithm(.ecdhKeyExchangeStandard)
        default:
            return false
        }
    }

    func tokenSession(
        _ session: TKTokenSession,
        sign dataToSign: Data,
        keyObjectID: TKToken.ObjectID,
        algorithm: TKTokenKeyAlgorithm
    ) throws -> Data {
        // Perform signing operation with the token hardware
        // Implementation depends on the specific token being supported
        throw TKError(.notImplemented)
    }

    func tokenSession(
        _ session: TKTokenSession,
        decrypt ciphertext: Data,
        keyObjectID: TKToken.ObjectID,
        algorithm: TKTokenKeyAlgorithm
    ) throws -> Data {
        throw TKError(.notImplemented)
    }

    func tokenSession(
        _ session: TKTokenSession,
        performKeyExchange otherPartyPublicKeyData: Data,
        keyObjectID: TKToken.ObjectID,
        algorithm: TKTokenKeyAlgorithm,
        parameters: TKTokenKeyExchangeParameters
    ) throws -> Data {
        throw TKError(.notImplemented)
    }

    func tokenSession(
        _ session: TKTokenSession,
        beginAuthFor operation: TKTokenOperation,
        constraint: Any
    ) throws -> TKTokenAuthOperation {
        let auth = TKTokenPasswordAuthOperation()
        return auth
    }
}
```

## APDU Command Helpers

Utility patterns for constructing and interpreting APDU commands.

### Status Word Interpretation

```swift
struct APDUStatus {
    let sw1: UInt8
    let sw2: UInt8
    let raw: UInt16

    init(_ sw: UInt16) {
        self.raw = sw
        self.sw1 = UInt8(sw >> 8)
        self.sw2 = UInt8(sw & 0xFF)
    }

    var isSuccess: Bool { raw == 0x9000 }
    var hasMoreData: Bool { sw1 == 0x61 }
    var bytesAvailable: Int { hasMoreData ? Int(sw2) : 0 }
    var isWrongLength: Bool { sw1 == 0x6C }
    var correctLength: Int { isWrongLength ? Int(sw2) : 0 }

    var isAuthenticationNeeded: Bool {
        raw == 0x6982  // Security status not satisfied
    }

    var isNotFound: Bool {
        raw == 0x6A82  // File or application not found
    }

    var description: String {
        switch raw {
        case 0x9000: return "Success"
        case 0x6283: return "Selected file deactivated"
        case 0x6882: return "Secure messaging not supported"
        case 0x6982: return "Security status not satisfied"
        case 0x6983: return "Authentication method blocked"
        case 0x6984: return "Reference data not usable"
        case 0x6985: return "Conditions of use not satisfied"
        case 0x6A82: return "File or application not found"
        case 0x6A86: return "Incorrect parameters P1-P2"
        case 0x6D00: return "Instruction not supported"
        case 0x6E00: return "Class not supported"
        default:
            if sw1 == 0x61 { return "More data: \(sw2) bytes" }
            if sw1 == 0x63 && (sw2 & 0xF0) == 0xC0 {
                return "Wrong PIN, \(sw2 & 0x0F) tries remaining"
            }
            return String(format: "Unknown: %04X", raw)
        }
    }
}
```

### Command Chaining for Large Data

Some cards require command chaining for data larger than the maximum
APDU size:

```swift
func sendChainedAPDU(
    card: TKSmartCard,
    ins: UInt8,
    p1: UInt8,
    p2: UInt8,
    data: Data,
    chunkSize: Int = 255
) throws -> (UInt16, Data) {
    try card.withSession {
        var offset = 0
        var lastSW: UInt16 = 0
        var fullResponse = Data()

        while offset < data.count {
            let end = min(offset + chunkSize, data.count)
            let chunk = data[offset..<end]
            let isLast = end >= data.count

            // Set CLA bit 4 for chaining, clear on last command
            card.cla = isLast ? 0x00 : 0x10

            let (sw, response) = try card.send(
                ins: ins,
                p1: p1,
                p2: p2,
                data: Data(chunk),
                le: isLast ? 0 : nil
            )

            fullResponse.append(response)
            lastSW = sw
            offset = end
        }

        card.cla = 0x00  // Reset CLA

        return (lastSW, fullResponse)
    }
}
```

### Reading Large Responses

Handle `61xx` (more data available) status words:

```swift
func readFullResponse(
    card: TKSmartCard,
    initialSW: UInt16,
    initialResponse: Data
) throws -> Data {
    var fullResponse = initialResponse
    var sw = initialSW

    while APDUStatus(sw).hasMoreData {
        let le = APDUStatus(sw).bytesAvailable
        let (nextSW, nextResponse) = try card.send(
            ins: 0xC0,    // GET RESPONSE
            p1: 0x00,
            p2: 0x00,
            data: nil,
            le: le == 0 ? 256 : le
        )
        fullResponse.append(nextResponse)
        sw = nextSW
    }

    guard sw == 0x9000 else {
        throw TKError(.communicationError)
    }

    return fullResponse
}
```

## Secure PIN Operations

For card readers with built-in PIN pads, use secure PIN verification
to prevent PIN exposure to the host system.

### Secure PIN Verification

```swift
func securePINVerify(card: TKSmartCard) {
    let pinFormat = TKSmartCardPINFormat()
    pinFormat.charset = .numeric
    pinFormat.encoding = .ascii
    pinFormat.minPINLength = 4
    pinFormat.maxPINLength = 8
    pinFormat.pinBlockByteLength = 8
    pinFormat.pinJustification = .left
    pinFormat.pinBitOffset = 0

    // VERIFY APDU template (PIN bytes will be inserted at offset)
    let apdu = Data([
        0x00, 0x20, 0x00, 0x80,  // CLA INS P1 P2
        0x08,                     // Lc (PIN block length)
        0xFF, 0xFF, 0xFF, 0xFF,   // PIN block placeholder
        0xFF, 0xFF, 0xFF, 0xFF
    ])

    guard let interaction = card.userInteractionForSecurePINVerification(
        pinFormat,
        apdu: apdu,
        pinByteOffset: 5
    ) else {
        print("Secure PIN verification not supported by this reader")
        return
    }

    interaction.initialTimeout = 30
    interaction.interactionTimeout = 30

    interaction.run { success, error in
        if success {
            let sw = interaction.resultSW
            print("PIN verify result: \(APDUStatus(sw).description)")
        } else {
            print("PIN entry failed: \(error?.localizedDescription ?? "")")
        }
    }
}
```

### Secure PIN Change

```swift
func securePINChange(card: TKSmartCard) {
    let pinFormat = TKSmartCardPINFormat()
    pinFormat.charset = .numeric
    pinFormat.encoding = .ascii
    pinFormat.minPINLength = 4
    pinFormat.maxPINLength = 8
    pinFormat.pinBlockByteLength = 8

    // CHANGE REFERENCE DATA APDU template
    let apdu = Data([
        0x00, 0x24, 0x00, 0x80,  // CLA INS P1 P2
        0x10,                     // Lc (two PIN blocks)
        0xFF, 0xFF, 0xFF, 0xFF,   // Current PIN placeholder
        0xFF, 0xFF, 0xFF, 0xFF,
        0xFF, 0xFF, 0xFF, 0xFF,   // New PIN placeholder
        0xFF, 0xFF, 0xFF, 0xFF
    ])

    guard let interaction = card.userInteractionForSecurePINChange(
        pinFormat,
        apdu: apdu,
        currentPINByteOffset: 5,
        newPINByteOffset: 13
    ) else {
        print("Secure PIN change not supported by this reader")
        return
    }

    interaction.pinConfirmation = [.current, .new]

    interaction.run { success, error in
        if success {
            let sw = interaction.resultSW
            print("PIN change result: \(APDUStatus(sw).description)")
        }
    }
}
```

## Token Configuration Management

Manage persistent token configurations for non-smart-card token drivers.

### Managing Driver Configurations

```swift
func manageTokenConfigurations() {
    // Access existing driver configurations
    let configs = TKTokenDriver.Configuration.driverConfigurations

    for (classID, config) in configs {
        print("Driver: \(classID)")

        for (instanceID, tokenConfig) in config.tokenConfigurations {
            print("  Token: \(instanceID)")

            if let data = tokenConfig.configurationData {
                print("  Config data: \(data.count) bytes")
            }

            // Access keychain items from configuration
            for item in tokenConfig.keychainItems {
                print("  Keychain item: \(item.objectID)")
            }
        }
    }
}
```

### Adding Token Configurations

```swift
func addTokenConfiguration(
    driverConfig: TKTokenDriver.Configuration,
    instanceID: String,
    configData: Data?
) {
    let tokenConfig = driverConfig.addTokenConfiguration(
        for: instanceID
    )
    tokenConfig.configurationData = configData
}
```

## Smart Card Slot Monitoring

Monitor smart card slot state changes for reader-aware applications. Always
guard `TKSmartCardSlotManager.default`; Apple documents that it returns `nil`
unless smart-card access is enabled, and available APIs still depend on device
hardware and runtime support.

```swift
import CryptoTokenKit
import Combine

final class SlotMonitor {
    private var observation: NSKeyValueObservation?

    func monitorSlot(named slotName: String) {
        guard let manager = TKSmartCardSlotManager.default else { return }

        manager.getSlot(withName: slotName) { [weak self] slot in
            guard let slot else {
                print("Slot not found: \(slotName)")
                return
            }

            // Observe slot state changes
            self?.observation = slot.observe(\.state, options: [.new]) { slot, change in
                switch slot.state {
                case .missing:
                    print("Reader disconnected")
                case .empty:
                    print("No card in reader")
                case .probing:
                    print("Card detected, probing...")
                case .muteCard:
                    print("Unresponsive card")
                case .validCard:
                    print("Valid card detected")
                    if let card = slot.makeSmartCard() {
                        self?.handleCard(card)
                    }
                @unknown default:
                    break
                }
            }

            // Check ATR if card is present
            if let atr = slot.atr {
                print("ATR: \(atr.bytes.map { String(format: "%02X", $0) }.joined())")
                print("Protocols: \(atr.protocols)")
            }
        }
    }

    private func handleCard(_ card: TKSmartCard) {
        print("Card in slot: \(card.slot.name)")
        print("Valid: \(card.isValid)")
        print("Protocol: \(card.currentProtocol)")
    }
}
```

## Token Registration

On iOS/iPadOS 26+, register and unregister NFC smart card tokens using
`TKSmartCardTokenRegistrationManager`. A registered smart card remains
reachable through Keychain Services, and the system can invoke an NFC slot when
a cryptographic operation needs the registered card.

```swift
@available(iOS 26.0, *)
func registerSmartCardToken(tokenID: String) {
    let manager = TKSmartCardTokenRegistrationManager.default

    do {
        try manager.registerSmartCard(
            tokenID: tokenID,
            promptMessage: "Insert your smart card to complete registration"
        )
        print("Token registered: \(tokenID)")
    } catch {
        print("Registration failed: \(error)")
    }
}

@available(iOS 26.0, *)
func unregisterSmartCardToken(tokenID: String) {
    let manager = TKSmartCardTokenRegistrationManager.default

    do {
        try manager.unregisterSmartCard(tokenID: tokenID)
        print("Token unregistered: \(tokenID)")
    } catch {
        print("Unregistration failed: \(error)")
    }
}

@available(iOS 26.0, *)
func listRegisteredTokens() {
    let manager = TKSmartCardTokenRegistrationManager.default
    for tokenID in manager.registeredSmartCardTokens {
        print("Registered token: \(tokenID)")
    }
}
```
