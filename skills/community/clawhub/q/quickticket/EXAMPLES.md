# QuickTicket examples

## A small repair

Request:

> Quickticket this: clicking Save twice creates duplicate notes. Keep the editor usable if saving fails.

One coherent ticket: **Prevent duplicate notes when Save is clicked repeatedly**.

- Outcome: one note is saved for a single save operation.
- Scope: inspect the existing save flow, prevent duplicate submissions and preserve recoverable editing after a failed save. Use the existing persistence contract.
- Acceptance: repeated clicks during one pending save create one note; a failed save retains the draft and permits a retry; a later separate save still works.
- Verification: reproduce the duplicate-save problem and check the pending, failed and subsequent-save cases using the existing test setup or a reproducible manual check.

The ticket carries QuickTicket's research, implementation and passing-acceptance completion instruction. A routine repair can reuse applicable established evidence.

## A project with dependencies

Request:

> Quickticket this project: let people register for our workshops and give the organizer a list of registrations. We already have a website and a form tool.

First inspect the existing tools and clarify which workshops, required registration details and organizer access matter. Consider configuring the form tool before proposing custom development. If that approach fits, a possible plan is:

| Ticket | Result | Depends on |
| --- | --- | --- |
| QT-001 | A visitor can register for one workshop using the existing form tool | Existing tool supports the required fields and storage |
| QT-002 | The organizer can access the registrations and the required workshop details | QT-001 supplies saved registrations |
| QT-003 | Visitors can reach the appropriate registration form from the website | QT-001 supplies a usable form link |
| QT-004 | The complete visitor-to-organizer workflow works in its intended environment | QT-002 and QT-003 supply organizer access and visitor entry |

QT-001 includes a way to try the first working registration flow. Feedback that changes later decisions is reflected in the affected tickets. QT-002 and QT-003 can proceed independently only if the form's shared configuration permits it.

Each saved ticket includes its scope, relevant context, observable acceptance and verification. For example, QT-004 checks that a visitor submits the intended details, receives the agreed response and appears in the organizer's list. The plan does not add payments, accounts or a new database unless the requested outcome needs them.

The agent saves the tickets in the project's usual location, or uses a linked Markdown index. Its chat response gives the location, first actionable ticket and anything preventing work from starting.
