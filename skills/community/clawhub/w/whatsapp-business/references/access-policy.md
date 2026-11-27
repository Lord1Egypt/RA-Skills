# WhatsApp Business access policy

An access policy limits which endpoints WhatsApp Business connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/whatsapp-business#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for WhatsApp Business: its 39 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create whatsapp-business --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "v25.0/me/assigned_whatsapp_business_accounts"},
    {"method": "GET", "path": "v25.0/{id}/client_whatsapp_business_accounts"},
    {"method": "GET", "path": "v25.0/{id}/owned_whatsapp_business_accounts"},
    {"method": "GET", "path": "v25.0/{id}/activities"},
    {"method": "GET", "path": "v25.0/{id}/call_analytics"},
    {"method": "GET", "path": "v25.0/{id}/conversation_analytics"},
    {"method": "GET", "path": "v25.0/{id}/group_analytics"},
    {"method": "GET", "path": "v25.0/{id}/pricing_analytics"},
    {"method": "GET", "path": "v25.0/{id}/template_analytics"},
    {"method": "GET", "path": "v25.0/{id}/template_group_analytics"},
    {"method": "GET", "path": "v25.0/{id}/audiences"},
    {"method": "GET", "path": "v25.0/{id}/conversational_automation"},
    {"method": "GET", "path": "v25.0/{id}/block_users"},
    {"method": "GET", "path": "v25.0/{id}/message_campaigns"},
    {"method": "GET", "path": "v25.0/{id}/product_catalogs"},
    {"method": "GET", "path": "v25.0/{id}/whatsapp_commerce_settings"},
    {"method": "GET", "path": "v25.0/{id}/dataset"},
    {"method": "GET", "path": "v25.0/{id}/whatsapp_business_encryption"},
    {"method": "GET", "path": "v25.0/{id}/flows"},
    {"method": "GET", "path": "v25.0/{id}/groups"},
    {"method": "GET", "path": "v25.0/{id}/join_requests"},
    {"method": "GET", "path": "v25.0/{id}"},
    {"method": "GET", "path": "v25.0/{id}/payment_configuration"},
    {"method": "GET", "path": "v25.0/{id}/payment_configurations"},
    {"method": "GET", "path": "v25.0/{id}/phone_numbers"},
    {"method": "GET", "path": "v25.0/{id}/business_compliance_info"},
    {"method": "GET", "path": "v25.0/{id}/whatsapp_business_profile"},
    {"method": "GET", "path": "v25.0/{id}/message_qrdls"},
    {"method": "GET", "path": "v25.0/{id}/message_qrdls/{id}"},
    {"method": "GET", "path": "v25.0/{id}/schedules"},
    {"method": "GET", "path": "v25.0/{id}/settings"},
    {"method": "GET", "path": "v25.0/{id}/solutions"},
    {"method": "GET", "path": "v25.0/{id}/degrees_of_freedom_spec"},
    {"method": "GET", "path": "v25.0/{id}/message_template_previews"},
    {"method": "GET", "path": "v25.0/{id}/message_templates"},
    {"method": "GET", "path": "v25.0/{id}/template_groups"},
    {"method": "GET", "path": "v25.0/{id}/assigned_users"},
    {"method": "GET", "path": "v25.0/{id}/subscribed_apps"},
    {"method": "GET", "path": "v25.0/{id}/welcome_message_sequences"}
  ],
  "deny": []
}
```

## Endpoints

The WhatsApp Business endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| POST | v25.0/{id}/business_messaging_feature_status | write | account | Set a business messaging feature status. |
| GET | v25.0/me/assigned_whatsapp_business_accounts | read | accounts | List the WhatsApp Business Accounts assigned to the calling user. |
| GET | v25.0/{id}/client_whatsapp_business_accounts | read | accounts | List the client WhatsApp Business Accounts of a business. |
| GET | v25.0/{id}/owned_whatsapp_business_accounts | read | accounts | List the WhatsApp Business Accounts owned by a business. |
| GET | v25.0/{id}/activities | read | activity-log | List activities of the WhatsApp Business Account. |
| GET | v25.0/{id}/call_analytics | read | analytics | Get call analytics. |
| GET | v25.0/{id}/conversation_analytics | read | analytics | Get conversation analytics. |
| GET | v25.0/{id}/group_analytics | read | analytics | Get group analytics. |
| GET | v25.0/{id}/pricing_analytics | read | analytics | Get pricing analytics. |
| GET | v25.0/{id}/template_analytics | read | analytics | Get message template analytics. |
| GET | v25.0/{id}/template_group_analytics | read | analytics | Get template group analytics. |
| GET | v25.0/{id}/audiences | read | audiences | List marketing messages audiences. |
| GET | v25.0/{id}/conversational_automation | read | automation | Get conversational automation settings (welcome message, commands, prompts). |
| POST | v25.0/{id}/conversational_automation | write | automation | Update conversational automation settings. |
| GET | v25.0/{id}/block_users | read | blocking | List users blocked by a phone number. |
| POST | v25.0/{id}/block_users | write | blocking | Block users. |
| DELETE | v25.0/{id}/block_users | write | blocking | Unblock users. |
| POST | v25.0/{id}/calls | write | calls | Initiate or act on a call. |
| GET | v25.0/{id}/message_campaigns | read | campaigns | List marketing message campaigns. |
| GET | v25.0/{id}/product_catalogs | read | catalogs | List product catalogs linked to the account. |
| POST | v25.0/{id}/product_catalogs | write | catalogs | Link a product catalog. |
| DELETE | v25.0/{id}/product_catalogs | write | catalogs | Unlink a product catalog. |
| GET | v25.0/{id}/whatsapp_commerce_settings | read | commerce | Get commerce settings of a phone number. |
| POST | v25.0/{id}/whatsapp_commerce_settings | write | commerce | Update commerce settings. |
| GET | v25.0/{id}/dataset | read | datasets | Get the dataset linked to the account. |
| POST | v25.0/{id}/dataset | write | datasets | Create the account dataset. |
| GET | v25.0/{id}/whatsapp_business_encryption | read | encryption | Get the business public key used for flows encryption. |
| POST | v25.0/{id}/whatsapp_business_encryption | write | encryption | Set the business public key. |
| GET | v25.0/{id}/flows | read | flows | List flows of the account. |
| POST | v25.0/{id}/flows | write | flows | Create a flow. |
| POST | v25.0/{id}/migrate_flows | write | flows | Migrate flows to another account. |
| GET | v25.0/{id}/groups | read | groups | List groups of a phone number. |
| POST | v25.0/{id}/groups | write | groups | Create a group. |
| GET | v25.0/{id}/invite_link | write | groups | Get a group invite link. Kept out of read: response is a link that lets anyone join the group. |
| GET | v25.0/{id}/join_requests | read | groups | List pending join requests of a group. |
| POST | v25.0/{id}/media | write | media | Upload a media file. |
| POST | v25.0/{id}/messages | write | messages | Send a message or mark a message as read. |
| GET | v25.0/{id} | read | nodes | Get a node by ID: a WhatsApp Business Account, phone number, media object, template, flow or group. |
| POST | v25.0/{id} | write | nodes | Update a node by ID, for example a WhatsApp Business Account or flow. |
| DELETE | v25.0/{id} | write | nodes | Delete a node by ID, for example a media object or flow. |
| POST | v25.0/{id}/generate_payment_configuration_oauth_link | write | payments | Generate a payment configuration OAuth link. |
| GET | v25.0/{id}/payment_configuration | read | payments | Get a payment configuration. |
| POST | v25.0/{id}/payment_configuration | write | payments | Create or update a payment configuration. |
| DELETE | v25.0/{id}/payment_configuration | write | payments | Delete a payment configuration. |
| GET | v25.0/{id}/payment_configurations | read | payments | List payment configurations. |
| POST | v25.0/{id}/deregister | write | phone-numbers | Deregister a phone number. |
| GET | v25.0/{id}/phone_numbers | read | phone-numbers | List phone numbers of the account. |
| POST | v25.0/{id}/phone_numbers | write | phone-numbers | Add a phone number to the account. |
| POST | v25.0/{id}/register | write | phone-numbers | Register a phone number. |
| POST | v25.0/{id}/request_code | write | phone-numbers | Request a verification code for a phone number. |
| POST | v25.0/{id}/verify_code | write | phone-numbers | Verify a phone number with a code. |
| GET | v25.0/{id}/business_compliance_info | read | profile | Get business compliance information of a phone number. |
| POST | v25.0/{id}/business_compliance_info | write | profile | Update business compliance information. |
| GET | v25.0/{id}/whatsapp_business_profile | read | profile | Get the WhatsApp business profile of a phone number. |
| POST | v25.0/{id}/whatsapp_business_profile | write | profile | Update the WhatsApp business profile. |
| GET | v25.0/{id}/message_qrdls | read | qr-codes | List message QR codes of a phone number. |
| POST | v25.0/{id}/message_qrdls | write | qr-codes | Create a message QR code. |
| GET | v25.0/{id}/message_qrdls/{id} | read | qr-codes | Get a message QR code. |
| POST | v25.0/{id}/message_qrdls/{id} | write | qr-codes | Update a message QR code. |
| DELETE | v25.0/{id}/message_qrdls/{id} | write | qr-codes | Delete a message QR code. |
| GET | v25.0/{id}/schedules | read | schedules | List schedules of the account. |
| GET | v25.0/{id}/settings | read | settings | Get settings of a phone number. |
| POST | v25.0/{id}/settings | write | settings | Update settings of a phone number. |
| POST | v25.0/{id}/set_solution_migration_intent | write | solutions | Set a solution migration intent. |
| GET | v25.0/{id}/solutions | read | solutions | List solutions the account is part of. |
| GET | v25.0/{id}/degrees_of_freedom_spec | read | templates | Get the degrees of freedom spec for templates. |
| POST | v25.0/{id}/message_samples | write | templates | Create message samples. |
| GET | v25.0/{id}/message_template_previews | read | templates | Get previews of message templates. |
| GET | v25.0/{id}/message_templates | read | templates | List message templates of the account. |
| POST | v25.0/{id}/message_templates | write | templates | Create a message template. |
| DELETE | v25.0/{id}/message_templates | write | templates | Delete a message template. |
| POST | v25.0/{id}/migrate_message_templates | write | templates | Migrate message templates to another account. |
| GET | v25.0/{id}/template_groups | read | templates | List template groups. |
| POST | v25.0/{id}/template_groups | write | templates | Create a template group. |
| POST | v25.0/{id}/upsert_message_templates | write | templates | Create or update message templates. |
| GET | v25.0/{id}/assigned_users | read | users | List users assigned to the WhatsApp Business Account. |
| POST | v25.0/{id}/assigned_users | write | users | Assign a user to the account. |
| DELETE | v25.0/{id}/assigned_users | write | users | Remove a user from the account. |
| GET | v25.0/{id}/subscribed_apps | read | webhooks | List apps subscribed to the account webhooks. |
| POST | v25.0/{id}/subscribed_apps | write | webhooks | Subscribe an app to the account webhooks. |
| DELETE | v25.0/{id}/subscribed_apps | write | webhooks | Unsubscribe an app from the account webhooks. |
| GET | v25.0/{id}/welcome_message_sequences | read | welcome-messages | List welcome message sequences. |
| POST | v25.0/{id}/welcome_message_sequences | write | welcome-messages | Create or update a welcome message sequence. |
| DELETE | v25.0/{id}/welcome_message_sequences | write | welcome-messages | Delete a welcome message sequence. |
