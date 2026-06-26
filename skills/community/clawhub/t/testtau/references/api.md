# TestTau API Reference For Agents

## Mail

Public base path:

```text
https://mail.testtau.com/i/<inbox>/api
```

Private base path:

```text
https://mail.testtau.com/private/i/<inbox>/api
Authorization: Bearer <mail-key>
```

Useful endpoints:

- `GET /list` - list recent messages.
- `GET /quota` - return stored message quota.
- `GET /wait?timeout=15000&subject=<text>&text=<text>` - long-poll for a matching message.
- `GET /message/<messageId>` - parsed message JSON.
- `GET /message/<messageId>/json` - parsed message JSON.
- `GET /message/<messageId>/raw` - raw `.eml`.
- `DELETE /message/<messageId>` - delete one message.
- `DELETE /all` - wipe inbox.

## Hooks

Public capture:

```text
POST https://hook.testtau.com/<hookId>
```

Public inspect API:

```text
https://hook.testtau.com/_/<hookId>/api
```

Private capture:

```text
POST https://hook.testtau.com/private/<hookId>
```

Private inspect API:

```text
https://hook.testtau.com/private/_/<hookId>/api
Authorization: Bearer <hook-key>
```

Useful endpoints:

- `GET /list` - list recent captures.
- `GET /request/<requestId>` - capture metadata.
- `GET /body/<requestId>` - capture body.
- `PUT /config` - set response behavior or JSON Schema.
- `POST /replay/<requestId>?target=<url>` - replay capture.
- `GET /assert?since=<epochMs>&min_count=1` - CI assertion gate.
- `DELETE /request/<requestId>` - delete one capture.
- `DELETE /all` - wipe hook.
