# RxLocal `/api` endpoint catalog

Base: `https://patient.rxlocal.com/api`. Auth: `Authorization: Bearer <token>`
(from `localStorage.kc_authRes.accessToken`) + `portalid: 370549AF-06A2-4E64-B17D-4040EF57D233`
on EVERY call (the web portal's public `patientPortalID`, a constant in the SPA
bundle; the native app uses a different id) + `rxlocaluserid: <globalUserID>`
where the SPA sends it. `groupOwnerID` == the account holder's own
`rxLocalPatientID`. Verified live from the signed-in tab, read-only: account
reads 2026-10-28; refills, conveyance options and messages 2026-10-29.

## Auth / token mechanics
- Token: Keycloak OIDC, realm `rxlocal`, client `patient-portal` (web),
  `aud: account`. **300-second lifespan**, refreshed by the SPA (threshold 90 s).
- On load the SPA also does `PUT /api/auth/session` and
  `PUT /api/account/token/user?forceUpdate=true` (token exchange). Neither is
  needed for the reads below; `portalid` is.
- reCAPTCHA v3 guards login/registration only, NOT the API.

## Account (lenient auth — tolerate an older token)
| Method | Path | Returns (keys) |
|---|---|---|
| GET | `account/check` | 200 |
| GET | `account/getuserinfo` | `globalUserID, userName, firstName, lastName, emailAddress, smsPhone, accountType, rxLocalPatientID, primaryPersonID, primaryDataExchangeIdentifier, roles, entityStatus, passwordExpired, termsAcceptanceRequired, smsTermsAcceptanceRequired, isTestUser, isDemoUser` |
| GET | `account/accountholderage` | `underMinimumAge, minimumAge` |
| PUT | `auth/session` | 200 (session touch) |
| PUT | `account/token/user?forceUpdate=true` | token exchange |

## Patient data (needs `portalid`; 401 without it)
| Method | Path | Notes |
|---|---|---|
| GET | `patients/{rxLocalPatientID}` | patient record (SPA loads this on home) |
| GET | `patients/{rxLocalPatientID}/patient` | demographics: `patientID, firstName, lastName, bornOn, smsPhone, email, dataExchangeIdentifier, globalUserID` |
| GET | `refill/{groupOwnerID}/v2` | **prescriptions** — `{serviceResult, data: {refills[], reportCards}}`. Row keys include `rxID, rxNumber, name, dispensedAs, ndc, pharmacyName, dateFilled, refillsRemaining, daysSupply, expirationDate, canRequestRefill, requiresRenewal, refillRequestStatus, unAvailableMessage, prescriber, dataExchangeIdentifier, rxLocalPatientID` (verified 2026-10-29). |
| GET | `refill/location/{DEI}/conveyanceOptions?groupOwnerID={id}&rxlocalPatientID={id}` | `data: {conveyanceOptions: number[] (1 pickup, 2 delivery, 3 mail), pickupTimeOptions: [{timeOptionType (1 asap, 2 later today, 3 tomorrow, 4 later), label, sortOrder}], patientAddress, mailingAddress, deliveryAddress, patientPhone, refillDisclaimers[], location, locationCalendar {nextOpen, minDate, maxDate, closed}, isPickupAvailable, isDeliveryAvailable}` (verified 2026-10-29). Addresses/phone are the patient's PII. |
| GET | `pharmacy/{pharmacyId}/hours/v2` | pharmacy hours (pharmacyId from patient/pharmacies) |
| GET | `patients/GetPatientPharmacies?GroupOwnerID={id}&RxLocalPatientId={id}` | pharmacies for the patient |
| GET | `patient/group/owner/{id}/locations` | group locations |
| GET | `notifications/most-relevant/v1?groupOwnerID={id}` | `{messageType}` banner |
| POST | `patients/getrxlocalpatientmedications` | medsync/report med list. Body `{groupOwnerID, rxLocalPatientID, startDate, endDate, active}`. Needs the **medsync-scoped token** from `account/token/user`, NOT the plain bearer — plain bearer 401s. Prefer `refill/{id}/v2` for the normal med list. |

## Messaging (same-origin `/api/Messaging/*`)
| Method | Path | Body / Notes |
|---|---|---|
| POST | `Messaging/SyncPatientMessages` | READ. `{GroupOwnerID, RxLocalPatientID, DataExchangeIdentifier, EndDate:null, GetXMostRecentMessagesForDateRange:true, IsFirstDownloadOfMessages:false}` → `data.messagesToAddUpdate[]`: `messageID, sentOn, body, type, statusType, sender {displayName, employeeID…}, recipients [{displayName, emailAddress, phoneNumber, carrierDomain…}]` (verified 2026-10-29). Does not mark read. |
| POST | `Messaging/CreatePatientMessage` | WRITE — `{GroupOwnerID, RxLocalPatientID, DataExchangeIdentifier, Body}` (from the SPA bundle, unverified). Not wired here; rxlocal-mcp's `rxlocal_send_message` does it behind a confirm gate. |
| POST | `Messaging/EmployeeInfo` | pharmacy employee directory for a thread. |
| POST | `Messaging/UpdatePatientMessageStatus` | WRITE — mark read. |
| POST | `Messaging/Attachments` | message attachments. |

## Group / patient management (writes — not wired)
- `POST patients` · `POST patient/group/Owner/{owner}` (add) ·
  `DELETE patient/group/Owner/{owner}/Patient/{id}` (remove) ·
  `POST Account/VerifyPatientByPrescription {DataExchangeIdentifier, BornOn, LastName, RxNumber, RxLocalPatientID}`.

## Refill request (write — not wired here)
- Options: the `conveyanceOptions` read above.
- Submit: `POST refill/{groupOwnerID}/v1`, header `rxlocaluserid`, body
  `{Requests: [{RxLocalPatientID, DataExchangeIdentifier, DetailList: [{PioneerRxID, RxNumber, DisplayName, Status (1 refill, 2 renewal), PharmacyName, PatientName}], ConveyanceType, UserPickupTimeOption, PickupLaterDate, Comments}]}`
  (from the SPA bundle, unverified). rxlocal-mcp's `rxlocal_request_refill` does
  it behind a confirm gate.

## Required headers summary
- Every call: `Authorization: Bearer <accessToken>` + `portalid: 370549AF-06A2-4E64-B17D-4040EF57D233`.
- `rxlocaluserid: <globalUserID>`: sent by the SPA on refill calls; not required
  for the reads (verified 2026-10-29). The helper sends it once resolved.
- A static app header `rxlocal_mobile_ss` exists in the bundle; it was NOT
  required for any read tested here — do not send it.

## Patient-data reachability (corrected 2026-10-29)
An earlier test (2026-10-28) found `refill/{id}/v2`, `Messaging/SyncPatientMessages`
and `patients/{id}/*` answering **401** on every replay and concluded they were
bound to the SPA's live session. That was wrong: those requests lacked the
`portalid` header the SPA's axios instance adds to every call. A live A/B with
the same fresh bearer on `GET refill/{id}/v2` gave 401 without `portalid` and
200 with it (with or without `rxlocaluserid`). `Messaging/SyncPatientMessages`
and the conveyance-options read were then verified 200 with it too;
`patients/{id}/*` has not been re-tested.

The header is necessary but not sufficient: the same bearer + `portalid` sent
without the browser's cookies (`credentials: 'omit'`) answers 401 on the
patient-data reads, while `account/getuserinfo` passes either way. The SPA sends
`withCredentials: true`, and the cookie that matters is `session-id` (verified
from Node: bearer + `portalid` + the tab's `session-id` → 200). `PUT auth/session`
mints a new `session-id`, but the portal keeps one session per user: minting
one signed the browser tab out. Read the tab's cookie; never mint one.
