---
name: renfe
description: Search Renfe trains in Spain (AVE, AVLO, regional and other trains sold on renfe.com) and book them for the user with the renfe CLI, paying by Bizum with the user's approval in their bank app. Use for Spanish train timetables, fares, cheapest-day questions, and buying or downloading Renfe tickets.
license: MIT
metadata:
  version: "0.1.0"
  homepage: https://github.com/mejiasd3v/renfe-cli
  hermes:
    tags: [travel, trains, spain, renfe, bizum]
  openclaw:
    emoji: "🚆"
    homepage: https://github.com/mejiasd3v/renfe-cli
    os: [darwin, linux]
    install:
      - id: go
        kind: go
        module: github.com/mejiasd3v/renfe-cli/cmd/renfe@v0.1.0
        bins: [renfe]
        label: Install renfe with go install
---

# Renfe trains

Run the CLI as `sh <skill folder>/scripts/renfe <arguments>`, where `<skill folder>` is the folder containing this SKILL.md and the arguments are those shown below after `renfe`. The launcher runs the binary bundled in `bin/`, or a matching `renfe` on PATH, or downloads this skill's release binary once from GitHub Releases and checks its SHA-256 before running it. JSON goes to stdout and progress to stderr. Errors exit 1 with Renfe's message.

## Setup

- Supported on macOS and Linux. The CLI needs network access to renfe.com. Booking also starts a Chromium-based browser (Helium, Chrome or Chromium; `RENFE_BROWSER` overrides it) and writes to `~/.config/renfe/`. In a sandboxed agent, request those permissions for `book`, `pay` and `ticket`.
- Booking reads travellers from `~/.config/renfe/passengers.json`. If it is missing, ask the user for each traveller's details and write the file in this format, with permissions 600. Never invent personal details.
  ```json
  {"bizum_phone": "+34600000000", "passengers": [{"id": "me", "type": "adult", "name": "...", "surname1": "...", "surname2": "...", "document_type": "DNI", "document": "...", "email": "...", "phone": "+34600000000"}]}
  ```
  `type` is `adult`, `child` (4 to 13) or `infant`; `document_type` is `DNI`, `NIE` or `passport`; the buyer (first passenger) needs `email` and `phone`.

## Find trains

```sh
renfe stations "barcelona sants"
renfe search --from madrid --to barcelona --date 2026-10-15
renfe search --from valencia --to sevilla --date 2026-10-20 --return 2026-10-22 --adults 2
renfe search --from atocha --to "barcelona sants" --date 2026-10-15 --direct
```

- Stations take names (accents optional, word prefixes) or codes. `madrid` means all Madrid stations. stderr names the station picked when several match.
- Each train has `departure`, `arrival`, `duration_minutes`, `legs` (train numbers), `sold_out`, `fares` (`code`, `name`, `price_eur` per passenger, `conditions`) and `notices`. Each journey has a ±3-day `price_calendar` for cheapest-day questions.

## Book

Travellers are referenced by `id` from the passengers file; the first `--passenger` is the buyer, an adult who receives the tickets by email. Never put personal details in command arguments.

1. Search, pick the train and fare the user wants, and check it with `--dry-run`.
2. Prepare the purchase. `--max-total` is the user's budget for the whole purchase:
   ```sh
   renfe book --from madrid --to guadalajara --date 2026-10-08 --train 07:46 --fare basico --passenger me --max-total 10
   ```
   Expect `"status": "ready_to_pay"` and Renfe's `total_eur`.
3. Tell the user the train, date, times, fare and `total_eur`, and that a Bizum request is about to reach their bank app. Then pay, using exactly that total:
   ```sh
   renfe pay --max-total 6.30
   ```
   This waits up to 5 minutes (`--wait`) for the approval and returns `"status": "confirmed"` with the `locator` and `ticket_pdf`, the saved ticket (`~/.config/renfe/tickets/<LOCATOR>.pdf`).

`--train` takes the departure time or train numbers (`05095+02140` for a connection). `--fare` takes a name, code or `cheapest`. For a round trip add `--return`, `--return-train` and `--return-fare`. `book ... --pay bizum --max-total X` does steps 2 and 3 in one run, when the user has already agreed to the train and price.

## Rules

- Buy only when the user asked to book or buy. Searching and `--dry-run` need no approval.
- Never raise `--max-total` above the user's budget or the quoted total without asking.
- Pay at most once per trip. After `payment_pending`, a timeout, or any error once `pay` started, do not run `book` or `pay` again for that trip. Ask the user whether they approved the Bizum request and check for Renfe's email first.
- Run one `book`/`pay` at a time; they share one browser and fail if another is running.
- Report the `locator` from a confirmed booking and give the user `ticket_pdf`. A `ticket_error` means only the PDF failed; the purchase stands. Fix it with `renfe ticket LOCATOR`, never by paying again.
- `renfe ticket LOCATOR` re-downloads the PDF of a purchase made with this CLI; `--tickets-dir` chooses the folder. Tickets bought elsewhere are only in Renfe's email.
- Payment is Bizum only. For card or PayPal, run `book` without `--passenger`, and the user finishes in the opened browser window.
