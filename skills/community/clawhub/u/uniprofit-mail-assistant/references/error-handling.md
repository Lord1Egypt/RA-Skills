# Error Handling

## 401 Invalid credential

Meaning:

- key missing
- key revoked
- wrong key value

Action:

- tell the user the UniProfit mail key is invalid or missing

## 403 Wrong skill

Meaning:

- using a non-`mail_send` key

Action:

- tell the user the current key cannot send mail

## 400 or 403 Mail account problems

Meaning:

- mail account missing
- mail account disabled
- SMTP endpoint not verified

Action:

- surface the backend error directly
- suggest checking account binding and SMTP verification

## SMTP failure

Meaning:

- upstream mail server rejected or failed the send

Action:

- state that the email was not sent
- surface the actionable error if available
