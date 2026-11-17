# TherapyPortal wire protocol & endpoints

Captured 2026-10-29 against portal site version `2026.8.9.49928.241710`, from the
shipped JS bundles (`/static/javascript/tsbin/...`, served without a session) and the
page's real XHRs.

## Request shape

Every data call is:

```
POST https://www.therapyportal.com/portal/practice/<area>/<verb>.aspx?msg=<n>
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest

<fields>&correlationid=<uuid4>&tnrac=<TNRAC>&tnv=<siteVersion>&portalpractice=<PracticeID>
```

The page's AJAX layer appends the last four fields to every request, in lowercase:

- `tnrac`: anti-forgery token, the value of the practice page's `<input id="TNRAC">`.
- `tnv`: `siteVersion = "…"` from the page. A stale value gets HTTP 409 (the version-warning path).
- `portalpractice`: the **numeric** `userInfo.PracticeID` from the page, NOT the URL slug.
  Without it, every endpoint answers **404 with the HTML "Page Not Found" page**, which
  looks exactly like a wrong path.
- `correlationid`: any uuid4.

The helper fetches `GET /p/<code>/` once per invocation and reads all three values from it.
A page with no `TNRAC`, or no `PracticeID`, means signed out.

JSON-object arguments go in ONE form field as a JSON string (often `request=`, sometimes
`Request=` or `json=`; the name matters).

## Endpoints (verified live unless marked)

| path | fields | notes |
|---|---|---|
| `getdashboardinfoforportaluser` | `request=1` | per client: names + `PatientStatisticsDocumentCounts` |
| `getportaldocumentstatisticsforportaluser` | — | pending-completion / pending-approval counts per client |
| `document/getpatientsforportaluser` | — | full demographic records. **Sensitive, always project** |
| `appointments/appointmentinformation` | `json={"searchAllAppointmentsForTheDay":false,"usersCurrentTimeInUtc":"<ISO Z>"}` | `Appointments[]` (future only), `AppointmentRequests[]`, practice name and phone |
| `documents/api/getportaluserdocumentrequestsbystatus` | `Request=[1,4,5]` | statuses: PortalDocRequestStatus `1` Pending, `4` InProgress, `5` Completed (`0` Deleted, `2` Canceled, `3` Expired). Each request has `PortalDocuments[]`, whose `PortalDocumentStatus` is `1` Pending, `2` InProgress, `3` Completed |
| `documents/api/getalwaysavailabledocumentsforportaluser` | — | standing forms |
| `billing/payments/getbalancesdueforportaluser` | — | `AmountToPatient` per client |
| `billing/payments/getreceiptsforportaluser` | — | `PaymentId`, amounts, `TransactionData[]` |
| `messages/getthreads` | `patientselection=null&readstatus=2&audiences=0,1,2&topicid=-1&patientid=<id>&newestfirst=true&recordnumber=0&recordstoretrieve=200&addresseetype=` | the exact body the UI sends for "All Conversations". `null` when there are no threads. Thread shape **not yet seen** (the test account had none); `readstatus` values other than `2` are unverified |
| `messages/getmessages` | `threadid=<id>` | **unverified** (no threads to test). Reading is separate from `markthreadasread`, which the helper never calls |
| `messages/getusercounts` | — | `null` with no messages |

## Downloads (job-based)

1. Create a job, which returns `{"JobId":n}`:
   - completed form: `document/createportalformdownloadrequest`, with
     `request={"PortalFormId":<PortalDocumentId>,"PatientId":<id>,"PatientDocumentType":<type>}`
     (captured from the document page's "Download Document" button; `PortalFormId` IS
     the `PortalDocumentId`). `document/downloadcompleteddocument` with
     `{"Id":<PortalDocumentId>}` returns HTTP 500 for these forms.
   - receipt: `billing/payments/createreceiptdownloadrequest` with `PaymentId=<id>`.
2. Poll `document/getdocumentdownloadstatus` with `request={"Id":<JobId>}` until it returns
   `{"ProgressPercentage":100,"EncryptedJobID":"…"}`. This usually takes a few seconds; the UI polls every 5 s.
3. `fpx download https://www.therapyportal.com/p/<code-lowercase>/document/download/<EncryptedJobID>/`
   returns a PDF.

Both download paths were verified with real PDFs (a form of about 68 KB, a receipt of about 41 KB).
`PatientDocumentType` `0` is a file the PRACTICE uploaded (e.g. a PDF sent for review). It
has no job: the document page links it directly, and
`fpx download https://www.therapyportal.com/p/<code>/documents/files/download/<PortalDocumentId>/`
returns the file (verified, a 134 KB PDF). Other types are unverified.

## Writes (NOT wrapped by the helper)

These exist in the bundles and are listed so nobody re-derives them by accident:
- messaging: `messages/createnewthread`, `respondtothread`, `markthreadasread`
- documents: `document/save*form`, `submitalwaysavailable*`, `uploadportalresponse*`, `savecapturedsignatureforportaluser`
- payments: `billing/payments/saveportalpayment`

All of them change the client's record at the practice.
