# Twilio access policy

An access policy limits which endpoints Twilio connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/twilio#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Twilio: its 100 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create twilio --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Addresses.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Addresses/{id}"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Addresses/{id}/DependentPhoneNumbers.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Applications.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Applications/{id}"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/AuthorizedConnectApps.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/AuthorizedConnectApps/{id}"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/AvailablePhoneNumbers.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/AvailablePhoneNumbers/{id}"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/AvailablePhoneNumbers/{id}/Local.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/AvailablePhoneNumbers/{id}/Mobile.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/AvailablePhoneNumbers/{id}/National.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/AvailablePhoneNumbers/{id}/SharedCost.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/AvailablePhoneNumbers/{id}/TollFree.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/AvailablePhoneNumbers/{id}/Voip.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Balance.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Calls.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Calls/{id}"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Calls/{id}/Events.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Calls/{id}/Notifications.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Calls/{id}/Notifications/{id}"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Calls/{id}/Recordings.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Calls/{id}/Recordings/{id}"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Conferences.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Conferences/{id}"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Conferences/{id}/Participants.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Conferences/{id}/Participants/{id}"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Conferences/{id}/Recordings.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Conferences/{id}/Recordings/{id}"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/ConnectApps.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/ConnectApps/{id}"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/IncomingPhoneNumbers.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/IncomingPhoneNumbers/Local.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/IncomingPhoneNumbers/Mobile.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/IncomingPhoneNumbers/TollFree.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/IncomingPhoneNumbers/{id}"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/IncomingPhoneNumbers/{id}/AssignedAddOns.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/IncomingPhoneNumbers/{id}/AssignedAddOns/{id}"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/IncomingPhoneNumbers/{id}/AssignedAddOns/{id}/Extensions.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/IncomingPhoneNumbers/{id}/AssignedAddOns/{id}/Extensions/{id}"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Keys.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Keys/{id}"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Messages.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Messages/{id}"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Messages/{id}/Media.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Messages/{id}/Media/{id}"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Notifications.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Notifications/{id}"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/OutgoingCallerIds.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/OutgoingCallerIds/{id}"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Queues.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Queues/{id}"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Queues/{id}/Members.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Queues/{id}/Members/{id}"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Recordings.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Recordings/{id}"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Recordings/{id}/AddOnResults.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Recordings/{id}/AddOnResults/{id}"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Recordings/{id}/AddOnResults/{id}/Payloads.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Recordings/{id}/AddOnResults/{id}/Payloads/{id}"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Recordings/{id}/AddOnResults/{id}/Payloads/{id}/Data.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Recordings/{id}/Transcriptions.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Recordings/{id}/Transcriptions/{id}"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/SigningKeys.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/SigningKeys/{id}"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/SIP/CredentialLists.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/SIP/CredentialLists/{id}"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/SIP/CredentialLists/{id}/Credentials.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/SIP/CredentialLists/{id}/Credentials/{id}"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/SIP/Domains.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/SIP/Domains/{id}"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/SIP/Domains/{id}/Auth/Calls/CredentialListMappings.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/SIP/Domains/{id}/Auth/Calls/CredentialListMappings/{id}"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/SIP/Domains/{id}/Auth/Calls/IpAccessControlListMappings.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/SIP/Domains/{id}/Auth/Calls/IpAccessControlListMappings/{id}"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/SIP/Domains/{id}/Auth/Registrations/CredentialListMappings.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/SIP/Domains/{id}/Auth/Registrations/CredentialListMappings/{id}"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/SIP/Domains/{id}/CredentialListMappings.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/SIP/Domains/{id}/CredentialListMappings/{id}"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/SIP/Domains/{id}/IpAccessControlListMappings.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/SIP/Domains/{id}/IpAccessControlListMappings/{id}"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/SIP/IpAccessControlLists.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/SIP/IpAccessControlLists/{id}"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/SIP/IpAccessControlLists/{id}/IpAddresses.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/SIP/IpAccessControlLists/{id}/IpAddresses/{id}"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/SMS/ShortCodes.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/SMS/ShortCodes/{id}"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Transcriptions.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Transcriptions/{id}"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Usage/Records.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Usage/Records/AllTime.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Usage/Records/Daily.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Usage/Records/LastMonth.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Usage/Records/Monthly.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Usage/Records/ThisMonth.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Usage/Records/Today.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Usage/Records/Yearly.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Usage/Records/Yesterday.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Usage/Triggers.json"},
    {"method": "GET", "path": "2010-04-01/Accounts/{id}/Usage/Triggers/{id}"}
  ],
  "deny": []
}
```

## Endpoints

The Twilio endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | 2010-04-01/Accounts.json | write | accounts | Retrieves a collection of Accounts belonging to the account used to make the request. Kept out of read: list includes each account's auth_token. |
| POST | 2010-04-01/Accounts.json | write | accounts | Create a new Twilio Subaccount from the account making the request. |
| GET | 2010-04-01/Accounts/{id} | write | accounts | Fetch the account specified by the provided Account Sid. Kept out of read: response includes the account auth_token. |
| POST | 2010-04-01/Accounts/{id} | write | accounts | Modify the properties of a given Account. |
| GET | 2010-04-01/Accounts/{id}/Addresses.json | read | addresses | List addresses. |
| POST | 2010-04-01/Accounts/{id}/Addresses.json | write | addresses | Create addresses. |
| GET | 2010-04-01/Accounts/{id}/Addresses/{id} | read | addresses | Fetch a addresse. |
| POST | 2010-04-01/Accounts/{id}/Addresses/{id} | write | addresses | Update a addresse. |
| DELETE | 2010-04-01/Accounts/{id}/Addresses/{id} | write | addresses | Delete a addresse. |
| GET | 2010-04-01/Accounts/{id}/Addresses/{id}/DependentPhoneNumbers.json | read | addresses | List dependent phone numbers. |
| GET | 2010-04-01/Accounts/{id}/Applications.json | read | applications | Retrieve a list of applications representing an application within the requesting account. |
| POST | 2010-04-01/Accounts/{id}/Applications.json | write | applications | Create a new application within your account. |
| GET | 2010-04-01/Accounts/{id}/Applications/{id} | read | applications | Fetch the application specified by the provided sid. |
| POST | 2010-04-01/Accounts/{id}/Applications/{id} | write | applications | Updates the application's properties. |
| DELETE | 2010-04-01/Accounts/{id}/Applications/{id} | write | applications | Delete the application by the specified application sid. |
| GET | 2010-04-01/Accounts/{id}/AuthorizedConnectApps.json | read | authorizedconnectapps | Retrieve a list of authorized-connect-apps belonging to the account used to make the request. |
| GET | 2010-04-01/Accounts/{id}/AuthorizedConnectApps/{id} | read | authorizedconnectapps | Fetch an instance of an authorized-connect-app. |
| GET | 2010-04-01/Accounts/{id}/AvailablePhoneNumbers.json | read | availablephonenumbers | List available phone numbers. |
| GET | 2010-04-01/Accounts/{id}/AvailablePhoneNumbers/{id} | read | availablephonenumbers | Fetch a available phone number. |
| GET | 2010-04-01/Accounts/{id}/AvailablePhoneNumbers/{id}/Local.json | read | availablephonenumbers | List local. |
| GET | 2010-04-01/Accounts/{id}/AvailablePhoneNumbers/{id}/Mobile.json | read | availablephonenumbers | List mobile. |
| GET | 2010-04-01/Accounts/{id}/AvailablePhoneNumbers/{id}/National.json | read | availablephonenumbers | List national. |
| GET | 2010-04-01/Accounts/{id}/AvailablePhoneNumbers/{id}/SharedCost.json | read | availablephonenumbers | List shared cost. |
| GET | 2010-04-01/Accounts/{id}/AvailablePhoneNumbers/{id}/TollFree.json | read | availablephonenumbers | List toll free. |
| GET | 2010-04-01/Accounts/{id}/AvailablePhoneNumbers/{id}/Voip.json | read | availablephonenumbers | List voip. |
| GET | 2010-04-01/Accounts/{id}/Balance.json | read | balance | Fetch the balance for an Account based on Account Sid. Balance changes may not be reflected immediately. Child accounts do not contain balance information. |
| GET | 2010-04-01/Accounts/{id}/Calls.json | read | calls | Retrieves a collection of calls made to and from your account. |
| POST | 2010-04-01/Accounts/{id}/Calls.json | write | calls | Create a new outgoing call to phones, SIP-enabled endpoints or Twilio Client connections. |
| GET | 2010-04-01/Accounts/{id}/Calls/{id} | read | calls | Fetch the call specified by the provided Call SID. |
| POST | 2010-04-01/Accounts/{id}/Calls/{id} | write | calls | Initiates a call redirect or terminates a call. |
| DELETE | 2010-04-01/Accounts/{id}/Calls/{id} | write | calls | Delete a Call record from your account. Once the record is deleted, it will no longer appear in the API and Account Portal logs. |
| GET | 2010-04-01/Accounts/{id}/Calls/{id}/Events.json | read | calls | Retrieve a list of all events for a call. |
| GET | 2010-04-01/Accounts/{id}/Calls/{id}/Notifications.json | read | calls | List notifications. |
| GET | 2010-04-01/Accounts/{id}/Calls/{id}/Notifications/{id} | read | calls | Fetch a notification. |
| POST | 2010-04-01/Accounts/{id}/Calls/{id}/Payments.json | write | calls | create an instance of payments. This will start a new payments session. |
| POST | 2010-04-01/Accounts/{id}/Calls/{id}/Payments/{id} | write | calls | update an instance of payments with different phases of payment flows. |
| GET | 2010-04-01/Accounts/{id}/Calls/{id}/Recordings.json | read | calls | Retrieve a list of recordings belonging to the call used to make the request. |
| POST | 2010-04-01/Accounts/{id}/Calls/{id}/Recordings.json | write | calls | Create a recording for the call. |
| GET | 2010-04-01/Accounts/{id}/Calls/{id}/Recordings/{id} | read | calls | Fetch an instance of a recording for a call. |
| POST | 2010-04-01/Accounts/{id}/Calls/{id}/Recordings/{id} | write | calls | Changes the status of the recording to paused, stopped, or in-progress. Note: Pass `Twilio.CURRENT` instead of recording sid to reference current active. |
| DELETE | 2010-04-01/Accounts/{id}/Calls/{id}/Recordings/{id} | write | calls | Delete a recording from your account. |
| POST | 2010-04-01/Accounts/{id}/Calls/{id}/Siprec.json | write | calls | Create a Siprec. |
| POST | 2010-04-01/Accounts/{id}/Calls/{id}/Siprec/{id} | write | calls | Stop a Siprec using either the SID of the Siprec resource or the `name` used when creating the resource. |
| POST | 2010-04-01/Accounts/{id}/Calls/{id}/Streams.json | write | calls | Create a Stream. |
| POST | 2010-04-01/Accounts/{id}/Calls/{id}/Streams/{id} | write | calls | Stop a Stream using either the SID of the Stream resource or the `name` used when creating the resource. |
| POST | 2010-04-01/Accounts/{id}/Calls/{id}/Transcriptions.json | write | calls | Create a Transcription. |
| POST | 2010-04-01/Accounts/{id}/Calls/{id}/Transcriptions/{id} | write | calls | Stop a Transcription using either the SID of the Transcription resource or the `name` used when creating the resource. |
| POST | 2010-04-01/Accounts/{id}/Calls/{id}/UserDefinedMessageSubscriptions.json | write | calls | Subscribe to User Defined Messages for a given Call SID. |
| DELETE | 2010-04-01/Accounts/{id}/Calls/{id}/UserDefinedMessageSubscriptions/{id} | write | calls | Delete a specific User Defined Message Subscription. |
| POST | 2010-04-01/Accounts/{id}/Calls/{id}/UserDefinedMessages.json | write | calls | Create a new User Defined Message for the given Call SID. |
| GET | 2010-04-01/Accounts/{id}/Conferences.json | read | conferences | Retrieve a list of conferences belonging to the account used to make the request. |
| GET | 2010-04-01/Accounts/{id}/Conferences/{id} | read | conferences | Fetch an instance of a conference. |
| POST | 2010-04-01/Accounts/{id}/Conferences/{id} | write | conferences | Update a conference. |
| GET | 2010-04-01/Accounts/{id}/Conferences/{id}/Participants.json | read | conferences | Retrieve a list of participants belonging to the account used to make the request. |
| POST | 2010-04-01/Accounts/{id}/Conferences/{id}/Participants.json | write | conferences | Create participants. |
| GET | 2010-04-01/Accounts/{id}/Conferences/{id}/Participants/{id} | read | conferences | Fetch an instance of a participant. |
| POST | 2010-04-01/Accounts/{id}/Conferences/{id}/Participants/{id} | write | conferences | Update the properties of the participant. |
| DELETE | 2010-04-01/Accounts/{id}/Conferences/{id}/Participants/{id} | write | conferences | Kick a participant from a given conference. |
| GET | 2010-04-01/Accounts/{id}/Conferences/{id}/Recordings.json | read | conferences | Retrieve a list of recordings belonging to the call used to make the request. |
| GET | 2010-04-01/Accounts/{id}/Conferences/{id}/Recordings/{id} | read | conferences | Fetch an instance of a recording for a call. |
| POST | 2010-04-01/Accounts/{id}/Conferences/{id}/Recordings/{id} | write | conferences | Changes the status of the recording to paused, stopped, or in-progress. Note: To use `Twilio.CURRENT`, pass it as recording sid. |
| DELETE | 2010-04-01/Accounts/{id}/Conferences/{id}/Recordings/{id} | write | conferences | Delete a recording from your account. |
| GET | 2010-04-01/Accounts/{id}/ConnectApps.json | read | connectapps | Retrieve a list of connect-apps belonging to the account used to make the request. |
| GET | 2010-04-01/Accounts/{id}/ConnectApps/{id} | read | connectapps | Fetch an instance of a connect-app. |
| POST | 2010-04-01/Accounts/{id}/ConnectApps/{id} | write | connectapps | Update a connect-app with the specified parameters. |
| DELETE | 2010-04-01/Accounts/{id}/ConnectApps/{id} | write | connectapps | Delete an instance of a connect-app. |
| GET | 2010-04-01/Accounts/{id}/IncomingPhoneNumbers.json | read | incomingphonenumbers | Retrieve a list of incoming-phone-numbers belonging to the account used to make the request. |
| POST | 2010-04-01/Accounts/{id}/IncomingPhoneNumbers.json | write | incomingphonenumbers | Purchase a phone-number for the account. |
| GET | 2010-04-01/Accounts/{id}/IncomingPhoneNumbers/Local.json | read | incomingphonenumbers | List local. |
| POST | 2010-04-01/Accounts/{id}/IncomingPhoneNumbers/Local.json | write | incomingphonenumbers | Create local. |
| GET | 2010-04-01/Accounts/{id}/IncomingPhoneNumbers/Mobile.json | read | incomingphonenumbers | List mobile. |
| POST | 2010-04-01/Accounts/{id}/IncomingPhoneNumbers/Mobile.json | write | incomingphonenumbers | Create mobile. |
| GET | 2010-04-01/Accounts/{id}/IncomingPhoneNumbers/TollFree.json | read | incomingphonenumbers | List toll free. |
| POST | 2010-04-01/Accounts/{id}/IncomingPhoneNumbers/TollFree.json | write | incomingphonenumbers | Create toll free. |
| GET | 2010-04-01/Accounts/{id}/IncomingPhoneNumbers/{id} | read | incomingphonenumbers | Fetch an incoming-phone-number belonging to the account used to make the request. |
| POST | 2010-04-01/Accounts/{id}/IncomingPhoneNumbers/{id} | write | incomingphonenumbers | Update an incoming-phone-number instance. |
| DELETE | 2010-04-01/Accounts/{id}/IncomingPhoneNumbers/{id} | write | incomingphonenumbers | Delete a phone-numbers belonging to the account used to make the request. |
| GET | 2010-04-01/Accounts/{id}/IncomingPhoneNumbers/{id}/AssignedAddOns.json | read | incomingphonenumbers | Retrieve a list of Add-on installations currently assigned to this Number. |
| POST | 2010-04-01/Accounts/{id}/IncomingPhoneNumbers/{id}/AssignedAddOns.json | write | incomingphonenumbers | Assign an Add-on installation to the Number specified. |
| GET | 2010-04-01/Accounts/{id}/IncomingPhoneNumbers/{id}/AssignedAddOns/{id} | read | incomingphonenumbers | Fetch an instance of an Add-on installation currently assigned to this Number. |
| DELETE | 2010-04-01/Accounts/{id}/IncomingPhoneNumbers/{id}/AssignedAddOns/{id} | write | incomingphonenumbers | Remove the assignment of an Add-on installation from the Number specified. |
| GET | 2010-04-01/Accounts/{id}/IncomingPhoneNumbers/{id}/AssignedAddOns/{id}/Extensions.json | read | incomingphonenumbers | Retrieve a list of Extensions for the Assigned Add-on. |
| GET | 2010-04-01/Accounts/{id}/IncomingPhoneNumbers/{id}/AssignedAddOns/{id}/Extensions/{id} | read | incomingphonenumbers | Fetch an instance of an Extension for the Assigned Add-on. |
| GET | 2010-04-01/Accounts/{id}/Keys.json | read | keys | List keys. |
| POST | 2010-04-01/Accounts/{id}/Keys.json | write | keys | Create keys. |
| GET | 2010-04-01/Accounts/{id}/Keys/{id} | read | keys | Fetch a key. |
| POST | 2010-04-01/Accounts/{id}/Keys/{id} | write | keys | Update a key. |
| DELETE | 2010-04-01/Accounts/{id}/Keys/{id} | write | keys | Delete a key. |
| GET | 2010-04-01/Accounts/{id}/Messages.json | read | messages | Retrieve a list of Message resources associated with a Twilio Account. |
| POST | 2010-04-01/Accounts/{id}/Messages.json | write | messages | Send a message. |
| GET | 2010-04-01/Accounts/{id}/Messages/{id} | read | messages | Fetch a specific Message. |
| POST | 2010-04-01/Accounts/{id}/Messages/{id} | write | messages | Update a Message resource (used to redact Message `body` text and to cancel not-yet-sent messages). |
| DELETE | 2010-04-01/Accounts/{id}/Messages/{id} | write | messages | Deletes a Message resource from your account. |
| POST | 2010-04-01/Accounts/{id}/Messages/{id}/Feedback.json | write | messages | Create Message Feedback to confirm a tracked user action was performed by the recipient of the associated Message. |
| GET | 2010-04-01/Accounts/{id}/Messages/{id}/Media.json | read | messages | Read a list of Media resources associated with a specific Message resource. |
| GET | 2010-04-01/Accounts/{id}/Messages/{id}/Media/{id} | read | messages | Fetch a single Media resource associated with a specific Message resource. |
| DELETE | 2010-04-01/Accounts/{id}/Messages/{id}/Media/{id} | write | messages | Delete the Media resource. |
| GET | 2010-04-01/Accounts/{id}/Notifications.json | read | notifications | Retrieve a list of notifications belonging to the account used to make the request. |
| GET | 2010-04-01/Accounts/{id}/Notifications/{id} | read | notifications | Fetch a notification belonging to the account used to make the request. |
| GET | 2010-04-01/Accounts/{id}/OutgoingCallerIds.json | read | outgoingcallerids | Retrieve a list of outgoing-caller-ids belonging to the account used to make the request. |
| POST | 2010-04-01/Accounts/{id}/OutgoingCallerIds.json | write | outgoingcallerids | Create outgoing caller ids. |
| GET | 2010-04-01/Accounts/{id}/OutgoingCallerIds/{id} | read | outgoingcallerids | Fetch an outgoing-caller-id belonging to the account used to make the request. |
| POST | 2010-04-01/Accounts/{id}/OutgoingCallerIds/{id} | write | outgoingcallerids | Updates the caller-id. |
| DELETE | 2010-04-01/Accounts/{id}/OutgoingCallerIds/{id} | write | outgoingcallerids | Delete the caller-id specified from the account. |
| GET | 2010-04-01/Accounts/{id}/Queues.json | read | queues | Retrieve a list of queues belonging to the account used to make the request. |
| POST | 2010-04-01/Accounts/{id}/Queues.json | write | queues | Create a queue. |
| GET | 2010-04-01/Accounts/{id}/Queues/{id} | read | queues | Fetch an instance of a queue identified by the QueueSid. |
| POST | 2010-04-01/Accounts/{id}/Queues/{id} | write | queues | Update the queue with the new parameters. |
| DELETE | 2010-04-01/Accounts/{id}/Queues/{id} | write | queues | Remove an empty queue. |
| GET | 2010-04-01/Accounts/{id}/Queues/{id}/Members.json | read | queues | Retrieve the members of the queue. |
| GET | 2010-04-01/Accounts/{id}/Queues/{id}/Members/{id} | read | queues | Fetch a specific member from the queue. |
| POST | 2010-04-01/Accounts/{id}/Queues/{id}/Members/{id} | write | queues | Dequeue a member from a queue and have the member's call begin executing the TwiML document at that URL. |
| GET | 2010-04-01/Accounts/{id}/Recordings.json | read | recordings | Retrieve a list of recordings belonging to the account used to make the request. |
| GET | 2010-04-01/Accounts/{id}/Recordings/{id} | read | recordings | Fetch an instance of a recording. |
| DELETE | 2010-04-01/Accounts/{id}/Recordings/{id} | write | recordings | Delete a recording from your account. |
| GET | 2010-04-01/Accounts/{id}/Recordings/{id}/AddOnResults.json | read | recordings | Retrieve a list of results belonging to the recording. |
| GET | 2010-04-01/Accounts/{id}/Recordings/{id}/AddOnResults/{id} | read | recordings | Fetch an instance of an AddOnResult. |
| DELETE | 2010-04-01/Accounts/{id}/Recordings/{id}/AddOnResults/{id} | write | recordings | Delete a result and purge all associated Payloads. |
| GET | 2010-04-01/Accounts/{id}/Recordings/{id}/AddOnResults/{id}/Payloads.json | read | recordings | Retrieve a list of payloads belonging to the AddOnResult. |
| GET | 2010-04-01/Accounts/{id}/Recordings/{id}/AddOnResults/{id}/Payloads/{id} | read | recordings | Fetch an instance of a result payload. |
| DELETE | 2010-04-01/Accounts/{id}/Recordings/{id}/AddOnResults/{id}/Payloads/{id} | write | recordings | Delete a payload from the result along with all associated Data. |
| GET | 2010-04-01/Accounts/{id}/Recordings/{id}/AddOnResults/{id}/Payloads/{id}/Data.json | read | recordings | Fetch an instance of a result payload. |
| GET | 2010-04-01/Accounts/{id}/Recordings/{id}/Transcriptions.json | read | recordings | List transcriptions. |
| GET | 2010-04-01/Accounts/{id}/Recordings/{id}/Transcriptions/{id} | read | recordings | Fetch a transcription. |
| DELETE | 2010-04-01/Accounts/{id}/Recordings/{id}/Transcriptions/{id} | write | recordings | Delete a transcription. |
| GET | 2010-04-01/Accounts/{id}/SigningKeys.json | read | signingkeys | List signing keys. |
| POST | 2010-04-01/Accounts/{id}/SigningKeys.json | write | signingkeys | Create a new Signing Key for the account making the request. |
| GET | 2010-04-01/Accounts/{id}/SigningKeys/{id} | read | signingkeys | Fetch a signing key. |
| POST | 2010-04-01/Accounts/{id}/SigningKeys/{id} | write | signingkeys | Update a signing key. |
| DELETE | 2010-04-01/Accounts/{id}/SigningKeys/{id} | write | signingkeys | Delete a signing key. |
| GET | 2010-04-01/Accounts/{id}/SIP/CredentialLists.json | read | sip | Get All Credential Lists. |
| POST | 2010-04-01/Accounts/{id}/SIP/CredentialLists.json | write | sip | Create a Credential List. |
| GET | 2010-04-01/Accounts/{id}/SIP/CredentialLists/{id} | read | sip | Get a Credential List. |
| POST | 2010-04-01/Accounts/{id}/SIP/CredentialLists/{id} | write | sip | Update a Credential List. |
| DELETE | 2010-04-01/Accounts/{id}/SIP/CredentialLists/{id} | write | sip | Delete a Credential List. |
| GET | 2010-04-01/Accounts/{id}/SIP/CredentialLists/{id}/Credentials.json | read | sip | Retrieve a list of credentials. |
| POST | 2010-04-01/Accounts/{id}/SIP/CredentialLists/{id}/Credentials.json | write | sip | Create a new credential resource. |
| GET | 2010-04-01/Accounts/{id}/SIP/CredentialLists/{id}/Credentials/{id} | read | sip | Fetch a single credential. |
| POST | 2010-04-01/Accounts/{id}/SIP/CredentialLists/{id}/Credentials/{id} | write | sip | Update a credential resource. |
| DELETE | 2010-04-01/Accounts/{id}/SIP/CredentialLists/{id}/Credentials/{id} | write | sip | Delete a credential resource. |
| GET | 2010-04-01/Accounts/{id}/SIP/Domains.json | read | sip | Retrieve a list of domains belonging to the account used to make the request. |
| POST | 2010-04-01/Accounts/{id}/SIP/Domains.json | write | sip | Create a new Domain. |
| GET | 2010-04-01/Accounts/{id}/SIP/Domains/{id} | read | sip | Fetch an instance of a Domain. |
| POST | 2010-04-01/Accounts/{id}/SIP/Domains/{id} | write | sip | Update the attributes of a domain. |
| DELETE | 2010-04-01/Accounts/{id}/SIP/Domains/{id} | write | sip | Delete an instance of a Domain. |
| GET | 2010-04-01/Accounts/{id}/SIP/Domains/{id}/Auth/Calls/CredentialListMappings.json | read | sip | Retrieve a list of credential list mappings belonging to the domain used in the request. |
| POST | 2010-04-01/Accounts/{id}/SIP/Domains/{id}/Auth/Calls/CredentialListMappings.json | write | sip | Create a new credential list mapping resource. |
| GET | 2010-04-01/Accounts/{id}/SIP/Domains/{id}/Auth/Calls/CredentialListMappings/{id} | read | sip | Fetch a specific instance of a credential list mapping. |
| DELETE | 2010-04-01/Accounts/{id}/SIP/Domains/{id}/Auth/Calls/CredentialListMappings/{id} | write | sip | Delete a credential list mapping from the requested domain. |
| GET | 2010-04-01/Accounts/{id}/SIP/Domains/{id}/Auth/Calls/IpAccessControlListMappings.json | read | sip | Retrieve a list of IP Access Control List mappings belonging to the domain used in the request. |
| POST | 2010-04-01/Accounts/{id}/SIP/Domains/{id}/Auth/Calls/IpAccessControlListMappings.json | write | sip | Create a new IP Access Control List mapping. |
| GET | 2010-04-01/Accounts/{id}/SIP/Domains/{id}/Auth/Calls/IpAccessControlListMappings/{id} | read | sip | Fetch a specific instance of an IP Access Control List mapping. |
| DELETE | 2010-04-01/Accounts/{id}/SIP/Domains/{id}/Auth/Calls/IpAccessControlListMappings/{id} | write | sip | Delete an IP Access Control List mapping from the requested domain. |
| GET | 2010-04-01/Accounts/{id}/SIP/Domains/{id}/Auth/Registrations/CredentialListMappings.json | read | sip | Retrieve a list of credential list mappings belonging to the domain used in the request. |
| POST | 2010-04-01/Accounts/{id}/SIP/Domains/{id}/Auth/Registrations/CredentialListMappings.json | write | sip | Create a new credential list mapping resource. |
| GET | 2010-04-01/Accounts/{id}/SIP/Domains/{id}/Auth/Registrations/CredentialListMappings/{id} | read | sip | Fetch a specific instance of a credential list mapping. |
| DELETE | 2010-04-01/Accounts/{id}/SIP/Domains/{id}/Auth/Registrations/CredentialListMappings/{id} | write | sip | Delete a credential list mapping from the requested domain. |
| GET | 2010-04-01/Accounts/{id}/SIP/Domains/{id}/CredentialListMappings.json | read | sip | Read multiple CredentialListMapping resources from an account. |
| POST | 2010-04-01/Accounts/{id}/SIP/Domains/{id}/CredentialListMappings.json | write | sip | Create a CredentialListMapping resource for an account. |
| GET | 2010-04-01/Accounts/{id}/SIP/Domains/{id}/CredentialListMappings/{id} | read | sip | Fetch a single CredentialListMapping resource from an account. |
| DELETE | 2010-04-01/Accounts/{id}/SIP/Domains/{id}/CredentialListMappings/{id} | write | sip | Delete a CredentialListMapping resource from an account. |
| GET | 2010-04-01/Accounts/{id}/SIP/Domains/{id}/IpAccessControlListMappings.json | read | sip | Retrieve a list of IpAccessControlListMapping resources. |
| POST | 2010-04-01/Accounts/{id}/SIP/Domains/{id}/IpAccessControlListMappings.json | write | sip | Create a new IpAccessControlListMapping resource. |
| GET | 2010-04-01/Accounts/{id}/SIP/Domains/{id}/IpAccessControlListMappings/{id} | read | sip | Fetch an IpAccessControlListMapping resource. |
| DELETE | 2010-04-01/Accounts/{id}/SIP/Domains/{id}/IpAccessControlListMappings/{id} | write | sip | Delete an IpAccessControlListMapping resource. |
| GET | 2010-04-01/Accounts/{id}/SIP/IpAccessControlLists.json | read | sip | Retrieve a list of IpAccessControlLists that belong to the account used to make the request. |
| POST | 2010-04-01/Accounts/{id}/SIP/IpAccessControlLists.json | write | sip | Create a new IpAccessControlList resource. |
| GET | 2010-04-01/Accounts/{id}/SIP/IpAccessControlLists/{id} | read | sip | Fetch a specific instance of an IpAccessControlList. |
| POST | 2010-04-01/Accounts/{id}/SIP/IpAccessControlLists/{id} | write | sip | Rename an IpAccessControlList. |
| DELETE | 2010-04-01/Accounts/{id}/SIP/IpAccessControlLists/{id} | write | sip | Delete an IpAccessControlList from the requested account. |
| GET | 2010-04-01/Accounts/{id}/SIP/IpAccessControlLists/{id}/IpAddresses.json | read | sip | Read multiple IpAddress resources. |
| POST | 2010-04-01/Accounts/{id}/SIP/IpAccessControlLists/{id}/IpAddresses.json | write | sip | Create a new IpAddress resource. |
| GET | 2010-04-01/Accounts/{id}/SIP/IpAccessControlLists/{id}/IpAddresses/{id} | read | sip | Read one IpAddress resource. |
| POST | 2010-04-01/Accounts/{id}/SIP/IpAccessControlLists/{id}/IpAddresses/{id} | write | sip | Update an IpAddress resource. |
| DELETE | 2010-04-01/Accounts/{id}/SIP/IpAccessControlLists/{id}/IpAddresses/{id} | write | sip | Delete an IpAddress resource. |
| GET | 2010-04-01/Accounts/{id}/SMS/ShortCodes.json | read | sms | Retrieve a list of short-codes belonging to the account used to make the request. |
| GET | 2010-04-01/Accounts/{id}/SMS/ShortCodes/{id} | read | sms | Fetch an instance of a short code. |
| POST | 2010-04-01/Accounts/{id}/SMS/ShortCodes/{id} | write | sms | Update a short code with the following parameters. |
| POST | 2010-04-01/Accounts/{id}/Tokens.json | write | tokens | Create a new token for ICE servers. |
| GET | 2010-04-01/Accounts/{id}/Transcriptions.json | read | transcriptions | Retrieve a list of transcriptions belonging to the account used to make the request. |
| GET | 2010-04-01/Accounts/{id}/Transcriptions/{id} | read | transcriptions | Fetch an instance of a Transcription. |
| DELETE | 2010-04-01/Accounts/{id}/Transcriptions/{id} | write | transcriptions | Delete a transcription from the account used to make the request. |
| GET | 2010-04-01/Accounts/{id}/Usage/Records.json | read | usage | Retrieve a list of usage-records belonging to the account used to make the request. |
| GET | 2010-04-01/Accounts/{id}/Usage/Records/AllTime.json | read | usage | List all time. |
| GET | 2010-04-01/Accounts/{id}/Usage/Records/Daily.json | read | usage | List daily. |
| GET | 2010-04-01/Accounts/{id}/Usage/Records/LastMonth.json | read | usage | List last month. |
| GET | 2010-04-01/Accounts/{id}/Usage/Records/Monthly.json | read | usage | List monthly. |
| GET | 2010-04-01/Accounts/{id}/Usage/Records/ThisMonth.json | read | usage | List this month. |
| GET | 2010-04-01/Accounts/{id}/Usage/Records/Today.json | read | usage | List today. |
| GET | 2010-04-01/Accounts/{id}/Usage/Records/Yearly.json | read | usage | List yearly. |
| GET | 2010-04-01/Accounts/{id}/Usage/Records/Yesterday.json | read | usage | List yesterday. |
| GET | 2010-04-01/Accounts/{id}/Usage/Triggers.json | read | usage | Retrieve a list of usage-triggers belonging to the account used to make the request. |
| POST | 2010-04-01/Accounts/{id}/Usage/Triggers.json | write | usage | Create a new UsageTrigger. |
| GET | 2010-04-01/Accounts/{id}/Usage/Triggers/{id} | read | usage | Fetch and instance of a usage-trigger. |
| POST | 2010-04-01/Accounts/{id}/Usage/Triggers/{id} | write | usage | Update an instance of a usage trigger. |
| DELETE | 2010-04-01/Accounts/{id}/Usage/Triggers/{id} | write | usage | Delete a trigger. |
