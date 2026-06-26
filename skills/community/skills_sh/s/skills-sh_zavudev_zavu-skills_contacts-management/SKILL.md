---
name: contacts-management
description: Manage multi-channel contacts with channel operations, merge suggestions, and phone introspection.
---

# Contacts Management

## When to Use

Use this skill when building code to create, update, or manage contacts and their communication channels. Covers the multi-channel contact model, merge operations, and phone number introspection.

## Contact Model

Contacts are multi-channel: one contact can have multiple channels (SMS, WhatsApp, Email, Telegram, Voice), each with its own identifier and delivery metrics. Top-level fields expose primary identifiers for quick access.

```
Contact (John Doe)
├── primaryPhone: +14155551234           (E.164)
├── primaryEmail: john@example.com
├── profileName: "John D."               (WhatsApp profile name, if available)
├── verified: true
├── countryCode: "US"
└── Channels:
    ├── SMS: +14155551234 (primary)
    ├── WhatsApp: +14155551234 (primary)
    ├── Email: john@example.com (primary)
    ├── Email: john.work@company.com (label: "work")
    ├── Telegram: @johndoe
    └── Voice: +14155551234
```

> **Note:** The legacy `phoneNumber` field on Contact is deprecated — use `primaryPhone` instead.

Valid contact channel types: `sms`, `whatsapp`, `email`, `telegram`, `voice` (note: `instagram`, `auto`, `sms_oneway` are message-send channels, not contact channel types).

## Auto-Creation

Contacts are automatically created when you send a message to a new recipient. No explicit creation needed for basic messaging.

## Create Contact

```typescript
const contact = await zavu.contacts.create({
  displayName: "John Doe",
  channels: [
    { channel: "sms", identifier: "+14155551234", isPrimary: true },
    { channel: "whatsapp", identifier: "+14155551234", isPrimary: true },
    { channel: "email", identifier: "john@example.com", isPrimary: true },
  ],
  metadata: { source: "import", plan: "enterprise" },
});
console.log(contact.id);
```

**Python:**
```python
contact = zavu.contacts.create(
    display_name="John Doe",
    channels=[
        {"channel": "sms", "identifier": "+14155551234", "isPrimary": True},
        {"channel": "email", "identifier": "john@example.com", "isPrimary": True},
    ],
)
```

**Go:**
```go
contact, err := client.Contacts.Create(context.TODO(), zavudev.ContactCreateParams{
    DisplayName: zavudev.String("John Doe"),
    Channels: []zavudev.ContactChannelParam{
        {Channel: "sms", Identifier: "+14155551234", IsPrimary: zavudev.Bool(true)},
        {Channel: "email", Identifier: "john@example.com", IsPrimary: zavudev.Bool(true)},
    },
})
```

**Ruby:**
```ruby
contact = client.contacts.create(
    display_name: "John Doe",
    channels: [
        { channel: "sms", identifier: "+14155551234", is_primary: true },
        { channel: "email", identifier: "john@example.com", is_primary: true },
    ],
)
```

**PHP:**
```php
$contact = $client->contacts->create([
    'displayName' => 'John Doe',
    'channels' => [
        ['channel' => 'sms', 'identifier' => '+14155551234', 'isPrimary' => true],
        ['channel' => 'email', 'identifier' => 'john@example.com', 'isPrimary' => true],
    ],
]);
```

## Get & List Contacts

```typescript
// Get by ID
const contact = await zavu.contacts.get({ contactId: "ct_abc123" });

// Get by phone number
const contact = await zavu.contacts.getByPhone({
  phoneNumber: "+14155551234",
});

// List with filters
let cursor: string | undefined;
do {
  const result = await zavu.contacts.list({
    phoneNumber: "+14155551234",
    limit: 50,
    cursor,
  });
  for (const contact of result.items) {
    console.log(contact.id, contact.displayName, contact.availableChannels);
  }
  cursor = result.nextCursor ?? undefined;
} while (cursor);
```

## Channel Operations

```typescript
// Add channel
const channel = await zavu.contacts.channels.add({
  contactId: "ct_abc123",
  channel: "email",
  identifier: "john.work@company.com",
  label: "work",       // optional
  countryCode: "US",   // optional, 2-letter ISO
});

// Update channel
await zavu.contacts.channels.update({
  contactId: "ct_abc123",
  channelId: "ch_xyz789",
  label: "personal",
  verified: true,
});

// Set as primary
await zavu.contacts.channels.setPrimary({
  contactId: "ct_abc123",
  channelId: "ch_xyz789",
});

// Remove channel (cannot remove the last channel)
await zavu.contacts.channels.remove({
  contactId: "ct_abc123",
  channelId: "ch_xyz789",
});
```

## Update Contact

```typescript
await zavu.contacts.update({
  contactId: "ct_abc123",
  defaultChannel: "whatsapp",
  metadata: { plan: "premium", region: "US" },
});

// Clear default channel
await zavu.contacts.update({
  contactId: "ct_abc123",
  defaultChannel: null,
});
```

## Merge Contacts

When duplicate contacts are detected, the API suggests merges:

```typescript
// Check for merge suggestion
const contact = await zavu.contacts.get({ contactId: "ct_abc123" });
if (contact.suggestedMergeWith) {
  // Merge source into target (all channels move to target)
  const merged = await zavu.contacts.merge({
    contactId: "ct_abc123",
    sourceContactId: contact.suggestedMergeWith,
  });
  console.log("Merged channels:", merged.channels.length);
}

// Dismiss suggestion
await zavu.contacts.mergeSuggestion.dismiss({
  contactId: "ct_abc123",
});
```

## Phone Introspection

Validate phone numbers and check carrier info:

```typescript
const result = await zavu.introspect.phone({
  phoneNumber: "+14155551234",
});
console.log(result.validNumber);      // true
console.log(result.countryCode);       // "US"
console.log(result.nationalFormat);    // "(415) 555-1234"
console.log(result.lineType);         // "mobile" | "landline" | "voip" | "toll_free"
console.log(result.carrier?.name);    // "Verizon Wireless"
console.log(result.availableChannels); // ["sms", "whatsapp", "voice"]
```

**Python:**
```python
result = zavu.introspect.phone(phone_number="+14155551234")
print(result.valid_number)
print(result.line_type)
print(result.carrier.name if result.carrier else "Unknown")
```

**Go:**
```go
result, err := client.Introspect.Phone(context.TODO(), zavudev.PhoneIntrospectionParams{
    PhoneNumber: zavudev.String("+14155551234"),
})
fmt.Println(result.ValidNumber, result.LineType, result.Carrier.Name)
```

**Ruby:**
```ruby
result = client.introspect.phone(phone_number: "+14155551234")
puts result.valid_number, result.line_type, result.carrier&.name
```

**PHP:**
```php
$result = $client->introspect->phone(['phoneNumber' => '+14155551234']);
echo $result->validNumber, $result->lineType, $result->carrier?->name;
```

## Constraints

- Max 20 channels per contact
- Channel labels: max 50 characters
- Display name: max 200 characters
- Cannot remove the last channel from a contact
- Cannot merge a contact with itself
- Phone numbers must be E.164 format
- Duplicate identifiers across contacts are rejected (use merge instead)
