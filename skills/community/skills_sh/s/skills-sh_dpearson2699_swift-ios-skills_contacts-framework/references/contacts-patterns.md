# Contacts Framework Extended Patterns

Overflow reference for the `contacts-framework` skill. Contains advanced patterns that exceed the main skill file's scope.

## Contents

- [Contacts SwiftUI Integration](#contacts-swiftui-integration)
- [Multi-Select Contact Picker](#multi-select-contact-picker)
- [Search and Filtering](#search-and-filtering)
- [vCard Import and Export](#vcard-import-and-export)
- [Contact Groups](#contact-groups)
- [Change Notifications and Swift Boundaries](#change-notifications-and-swift-boundaries)

## Contacts SwiftUI Integration

### Contact Manager with `@Observable`

```swift
@preconcurrency import Contacts
import ContactsUI
import SwiftUI
import UIKit

@Observable
@MainActor
final class ContactManager {
    let store = CNContactStore()

    var contacts: [CNContact] = []
    var canAccessContacts = false
    var hasLimitedAccess = false
    var authorizationStatus: CNAuthorizationStatus = .notDetermined

    func checkAuthorization() {
        updateAuthorization(CNContactStore.authorizationStatus(for: .contacts))
    }

    func requestAccess() async throws {
        _ = try await store.requestAccess(for: .contacts)
        updateAuthorization(CNContactStore.authorizationStatus(for: .contacts))
    }

    func updateAuthorization(_ status: CNAuthorizationStatus) {
        authorizationStatus = status
        canAccessContacts = status == .authorized || status == .limited
        hasLimitedAccess = status == .limited
    }

    func loadContacts() async throws {
        guard canAccessContacts else { return }

        let keys: [CNKeyDescriptor] = [
            CNContactGivenNameKey as CNKeyDescriptor,
            CNContactFamilyNameKey as CNKeyDescriptor,
            CNContactPhoneNumbersKey as CNKeyDescriptor,
            CNContactEmailAddressesKey as CNKeyDescriptor,
            CNContactThumbnailImageDataKey as CNKeyDescriptor,
            CNContactFormatter.descriptorForRequiredKeys(for: .fullName)
        ]

        contacts = try await Task.detached { [store] in
            let request = CNContactFetchRequest(keysToFetch: keys)
            request.sortOrder = .givenName
            var results: [CNContact] = []
            try store.enumerateContacts(with: request) { contact, _ in
                results.append(contact)
            }
            return results
        }.value
    }

    func formattedName(for contact: CNContact) -> String {
        CNContactFormatter.string(from: contact, style: .fullName)
            ?? "\(contact.givenName) \(contact.familyName)"
    }
}
```

### Contact List View

```swift
struct ContactListView: View {
    @Environment(ContactManager.self) private var manager

    var body: some View {
        NavigationStack {
            Group {
                if !manager.canAccessContacts {
                    ContentUnavailableView {
                        Label("Contacts Access", systemImage: "person.crop.circle.badge.questionmark")
                    } description: {
                        Text("Grant access to view your contacts.")
                    } actions: {
                        Button("Allow Access") {
                            Task { try? await manager.requestAccess() }
                        }
                        .buttonStyle(.borderedProminent)
                    }
                } else {
                    contactList
                    if manager.hasLimitedAccess {
                        limitedAccessControls
                    }
                }
            }
            .navigationTitle("Contacts")
            .task {
                manager.checkAuthorization()
                if manager.canAccessContacts {
                    try? await manager.loadContacts()
                }
            }
        }
    }

    private var contactList: some View {
        List(manager.contacts, id: \.identifier) { contact in
            HStack {
                contactAvatar(contact)
                VStack(alignment: .leading) {
                    Text(manager.formattedName(for: contact))
                        .font(.body)
                    if let phone = contact.phoneNumbers.first?.value.stringValue {
                        Text(phone)
                            .font(.caption)
                            .foregroundStyle(.secondary)
                    }
                }
            }
        }
    }

    @ViewBuilder
    private func contactAvatar(_ contact: CNContact) -> some View {
        if let imageData = contact.thumbnailImageData,
           let uiImage = UIImage(data: imageData) {
            Image(uiImage: uiImage)
                .resizable()
                .scaledToFill()
                .frame(width: 40, height: 40)
                .clipShape(Circle())
        } else {
            Image(systemName: "person.circle.fill")
                .resizable()
                .frame(width: 40, height: 40)
                .foregroundStyle(.secondary)
        }
    }

    @State private var isPresentingContactAccessPicker = false

    private var limitedAccessControls: some View {
        Button {
            isPresentingContactAccessPicker = true
        } label: {
            Label("Add Contacts", systemImage: "person.crop.circle.badge.plus")
        }
        .contactAccessPicker(isPresented: $isPresentingContactAccessPicker) { identifiers in
            guard !identifiers.isEmpty else { return }
            Task { try? await manager.loadContacts() }
        }
    }
}
```

Under `.limited`, the app can still use Contacts APIs, but only for contacts the
user has granted or the app created. `ContactAccessButton` works well beside a
search field; `contactAccessPicker(isPresented:completionHandler:)` presents a
management sheet and returns identifiers for newly granted contacts only.

## Multi-Select Contact Picker

### SwiftUI Wrapper for Multi-Selection

```swift
import SwiftUI
import ContactsUI

struct MultiContactPicker: UIViewControllerRepresentable {
    @Binding var selectedContacts: [CNContact]

    func makeUIViewController(context: Context) -> CNContactPickerViewController {
        let picker = CNContactPickerViewController()
        picker.delegate = context.coordinator
        return picker
    }

    func updateUIViewController(_ uiViewController: CNContactPickerViewController, context: Context) {}

    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }

    final class Coordinator: NSObject, CNContactPickerDelegate {
        let parent: MultiContactPicker

        init(_ parent: MultiContactPicker) {
            self.parent = parent
        }

        func contactPicker(_ picker: CNContactPickerViewController, didSelect contacts: [CNContact]) {
            parent.selectedContacts = contacts
        }

        func contactPickerDidCancel(_ picker: CNContactPickerViewController) {}
    }
}
```

### Email-Only Picker

Configure the picker to only return email addresses.

```swift
struct EmailPicker: UIViewControllerRepresentable {
    @Binding var selectedEmail: String?

    func makeUIViewController(context: Context) -> CNContactPickerViewController {
        let picker = CNContactPickerViewController()
        picker.delegate = context.coordinator
        // Only show contacts with emails
        picker.predicateForEnablingContact = NSPredicate(format: "emailAddresses.@count > 0")
        // Show contact detail so user can pick a specific email
        picker.predicateForSelectionOfProperty = NSPredicate(
            format: "key == 'emailAddresses'"
        )
        picker.displayedPropertyKeys = [CNContactEmailAddressesKey]
        return picker
    }

    func updateUIViewController(_ uiViewController: CNContactPickerViewController, context: Context) {}

    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }

    final class Coordinator: NSObject, CNContactPickerDelegate {
        let parent: EmailPicker

        init(_ parent: EmailPicker) {
            self.parent = parent
        }

        func contactPicker(
            _ picker: CNContactPickerViewController,
            didSelect contactProperty: CNContactProperty
        ) {
            parent.selectedEmail = contactProperty.value as? String
        }
    }
}
```

## Search and Filtering

### Predicate-Based Search

```swift
// By name
let namePredicate = CNContact.predicateForContacts(matchingName: "John")

// By email address
let emailPredicate = CNContact.predicateForContacts(matchingEmailAddress: "john@example.com")

// By phone number
let phonePredicate = CNContact.predicateForContacts(
    matching: CNPhoneNumber(stringValue: "+1234567890")
)

// By identifiers (batch fetch)
let idsPredicate = CNContact.predicateForContacts(withIdentifiers: ["id1", "id2", "id3"])

// By group
let groupPredicate = CNContact.predicateForContactsInGroup(withIdentifier: groupId)

// By container
let containerPredicate = CNContact.predicateForContactsInContainer(
    withIdentifier: containerId
)
```

### Custom Filtering After Fetch

For complex filtering not supported by predicates, enumerate and filter in memory.

```swift
func fetchContactsWithBirthday(in month: Int) throws -> [CNContact] {
    let keys: [CNKeyDescriptor] = [
        CNContactGivenNameKey as CNKeyDescriptor,
        CNContactFamilyNameKey as CNKeyDescriptor,
        CNContactBirthdayKey as CNKeyDescriptor
    ]
    let request = CNContactFetchRequest(keysToFetch: keys)

    var contacts: [CNContact] = []
    try store.enumerateContacts(with: request) { contact, _ in
        if let birthday = contact.birthday, birthday.month == month {
            contacts.append(contact)
        }
    }
    return contacts
}
```

## vCard Import and Export

### Exporting Contacts to vCard

```swift
func exportToVCard(contacts: [CNContact]) throws -> Data {
    return try CNContactVCardSerialization.data(with: contacts)
}

// Save to file
func saveVCard(contacts: [CNContact], to url: URL) throws {
    let data = try CNContactVCardSerialization.data(with: contacts)
    try data.write(to: url)
}
```

### Importing Contacts from vCard

```swift
func importFromVCard(data: Data) throws -> [CNContact] {
    return try CNContactVCardSerialization.contacts(with: data)
}

// Save imported contacts to the store
func importAndSave(data: Data) throws {
    let contacts = try CNContactVCardSerialization.contacts(with: data)
    let saveRequest = CNSaveRequest()

    for contact in contacts {
        guard let mutable = contact.mutableCopy() as? CNMutableContact else { continue }
        saveRequest.add(mutable, toContainerWithIdentifier: nil)
    }

    try store.execute(saveRequest)
}
```

## Contact Groups

### Fetching Groups

```swift
func fetchGroups() throws -> [CNGroup] {
    return try store.groups(matching: nil) // nil returns all groups
}

func fetchContactsInGroup(_ group: CNGroup) throws -> [CNContact] {
    let predicate = CNContact.predicateForContactsInGroup(withIdentifier: group.identifier)
    let keys: [CNKeyDescriptor] = [
        CNContactGivenNameKey as CNKeyDescriptor,
        CNContactFamilyNameKey as CNKeyDescriptor
    ]
    return try store.unifiedContacts(matching: predicate, keysToFetch: keys)
}
```

### Creating and Managing Groups

```swift
func createGroup(name: String) throws {
    let group = CNMutableGroup()
    group.name = name

    let saveRequest = CNSaveRequest()
    saveRequest.add(group, toContainerWithIdentifier: nil)
    try store.execute(saveRequest)
}

func addContactToGroup(contact: CNContact, group: CNGroup) throws {
    let saveRequest = CNSaveRequest()
    saveRequest.addMember(contact, to: group)
    try store.execute(saveRequest)
}

func removeContactFromGroup(contact: CNContact, group: CNGroup) throws {
    let saveRequest = CNSaveRequest()
    saveRequest.removeMember(contact, from: group)
    try store.execute(saveRequest)
}
```

## Change Notifications and Swift Boundaries

For Swift-first apps, use `CNContactStoreDidChange` to invalidate caches and
refetch the contacts your authorization status allows. Do not write Swift code
that calls `store.enumerateChanges(matching:)`; that method does not exist.
Apple's change-history fetch entry point is the Objective-C
`enumeratorForChangeHistoryFetchRequest:error:` selector, while the Swift
`enumerator(for:)` overlay is marked unavailable. If a product truly needs
incremental history tokens, isolate that bridge in Objective-C and expose a
small Swift wrapper; otherwise, refetch on change notifications.

### Watching for Real-Time Changes

```swift
func observeChanges(handler: @escaping () -> Void) -> NSObjectProtocol {
    NotificationCenter.default.addObserver(
        forName: .CNContactStoreDidChange,
        object: nil,
        queue: .main
    ) { _ in
        handler()
    }
}
```
