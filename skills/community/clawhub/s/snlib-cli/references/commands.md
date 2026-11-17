# MoonBit command patterns

Each command takes one JSON object on stdin and emits a result envelope.
Inspect `outcome` / `code`; zero exit status does not imply success.
Account commands require login. List commands return the current page, with
server totals where available.

## Login

Prepare a private JSON file outside the repository (permissions `0600`) with
`{"user_id":"YOUR_ID","password":"YOUR_PASSWORD"}`. Do not put real credentials
in shell history.

```bash
"{baseDir}/scripts/snlib-cli.sh" login < /path/to/private-login.json
```

## Search

```bash
printf '%s\n' '{"keyword":"키워드"}' |
  "{baseDir}/scripts/snlib-cli.sh" search-books
printf '%s\n' '{"keyword":"키워드","manage_codes":["MA"],"page":1,"per_page":10,"sort":"SIMILAR","order":"DESC"}' |
  "{baseDir}/scripts/snlib-cli.sh" search-books
```

Use an array for `manage_codes`. See `manage-code.md` for mappings.

## Account reads

```bash
printf '%s\n' '{}' | "{baseDir}/scripts/snlib-cli.sh" my-info
printf '%s\n' '{"include_history":false}' | "{baseDir}/scripts/snlib-cli.sh" loan-status
printf '%s\n' '{}' | "{baseDir}/scripts/snlib-cli.sh" loan-history
printf '%s\n' '{}' | "{baseDir}/scripts/snlib-cli.sh" reservation-status
printf '%s\n' '{}' | "{baseDir}/scripts/snlib-cli.sh" interloan-status
printf '%s\n' '{}' | "{baseDir}/scripts/snlib-cli.sh" hope-book-list
printf '%s\n' '{"rec_key":"1938103961"}' | "{baseDir}/scripts/snlib-cli.sh" hope-book-detail
printf '%s\n' '{}' | "{baseDir}/scripts/snlib-cli.sh" basket-list
printf '%s\n' '{"group_key":"13840"}' | "{baseDir}/scripts/snlib-cli.sh" basket-list
```

Use `include_history:true` to retain returned items in loan status.
`rec_key` and `group_key` must be nonempty numeric strings.

## Writes: prepare first, confirm, then submit

The examples below only prepare. Review `data.prepared_payload`, ask the user
to confirm the complete request, then rerun with `"submit":true`.
Omitted `submit` defaults to false. These identifiers are illustrative.

### Interloan

```bash
printf '%s\n' '{"manage_code":"MA","reg_no":"CEM000334796","apl_lib_code":"141484","submit":false}' |
  "{baseDir}/scripts/snlib-cli.sh" interloan-request
```

`interlibrary-loan-request` is an alias. Optional fields: `give_lib_code`,
`user_key`, `appendix_apply_yn` (default `"N"`). Giving library and user key
default to the book's preparation form. See `lib-code.md` for six-digit codes.

### Hope book

```bash
printf '%s\n' '{"manage_code":"MU","submit":false,"request":{"title":"도서명","author":"저자","publisher":"출판사","publishYear":"2026","eaIsbn":"9788966264896","price":"54000","email":"user@example.com","smsReceiptYn":"Y","handPhone":"010-1234-5678"}}' |
  "{baseDir}/scripts/snlib-cli.sh" hope-book-request
```

An empty input `{}` inspects defaults. Submission requires title, author,
publisher, valid manage code, email, phone, and explicit `smsReceiptYn:"Y"`
consent. Price must be digits if present. Contact fields may use authenticated
form defaults; review them before confirming. The request is a JSON object
with string values, not EDN. Snake/hyphen aliases such as `publish_year`,
`hand_phone`, and `sms_receipt_yn` are accepted.

Do not automatically retry a submission after a network or session-save error.
Check `interloan-status` or `hope-book-list` first: the request may already
have been accepted. A plain HTTP 200 is not submission confirmation.
