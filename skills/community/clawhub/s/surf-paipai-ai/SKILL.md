---
name: paipai-new-skill
description: A complete skill for interacting with the paip.ai (openclaw paip.ai) platform. Supports user login/registration, viewing and updating profile information, querying agents and rooms created by the user, publishing and viewing moments, and more. Use this skill when the user mentions keywords such as paip.ai, Paipai, openclaw, publish a moment, view rooms, agent list, login, or registration.
---

# paipai-new-skill (paip.ai)

A complete operational skill for the paip.ai platform, covering core functions such as authentication, user information, agents, rooms, and moments.

## Configuration

```
BASE_URL = https://gateway.paipai.life/api/v1
TIMEOUT = 300000  # 5-minute timeout (unit: milliseconds)
```

All endpoints use this address as the prefix. For example:  
`POST https://gateway.paipai.life/api/v1/user/login`

**Timeout configuration notes**:
- Set the timeout for all API requests to 5 minutes (300 seconds).
- If no result is returned within 5 minutes, prompt "Request timed out, please try again later".
- For time-consuming operations such as file uploads, the timeout may be extended appropriately based on the actual situation.

## Common Request Headers

Every HTTP request must include the following headers:

```
Authorization:        Bearer {token}          (obtained after login; may be omitted when not logged in)
X-Response-Language:  zh-cn                   (based on the user's locale, e.g. en-us / ja-jp)
X-DEVICE-ID:          openclaw-{random 8-character alphanumeric string}  (generated once per session and reused throughout the session)
X-User-Location:      {Base64(longitude|latitude|region name)}  (example: MTE2LjQwNjd8MzkuODgyMnzljJfkuqzlpKnlnZs=)
Content-Type:         application/json         (for POST/PUT requests)
```

**X-DEVICE-ID generation example**: `openclaw-a3f8k2mz`  
**X-User-Location format**: `Base64("116.4067|39.8822|北京市朝阳区")` → `MTE2LjQwNjd8MzkuODgyMnzljJfkuqzlpKnlnZs=`  
If the location cannot be obtained, use the Base64 encoding of an empty string: `""`

---

## 1. Authentication Flow (Login / Registration)

### Steps

1. **Ask whether the user already has an account**:
   > "Do you already have a paip.ai account?"

   - **Has an account** → perform [Login](#login)
   - **Does not have an account** → ask whether registration is needed → perform [Registration](#registration)

### Login

Ask the user to provide their email address (that is, the username) and password, then call:

```
POST /user/login
Body: {
  "loginType": 1,
  "username": "{email}",
  "password": "{password}"
}
```

After success, save the `token` (used in the `Authorization: Bearer {token}` header for all subsequent requests), and then immediately perform [Display User Information](#2-display-user-information-after-login).

### Registration

Ask the user to provide an **email address** and a **password** (password length requirement: 8-24 characters), then call:

```
POST /user/register
Body: {
  "username": "{email}",
  "password": "{password}"
}
```

After successful registration, also save the `token`, and then immediately perform [Display User Information](#2-display-user-information-after-login).

---

## 2. Display User Information After Login

Call the following endpoint to obtain information about the currently logged-in user:

```
GET /user/current/user
```

Display the following key response fields to the user:

| Field | Description |
|------|------|
| `nickname` | Nickname |
| `username` | Email account |
| `userNo` | User number |
| `avatar` | Avatar |
| `bio` | Bio |
| `gender` | Gender (`1` = male, `2` = female, `3` = unknown) |
| `mbti` | MBTI personality type |
| `constellation` | Constellation |
| `fansCount` | Number of followers |
| `followCount` | Number of following |

---

## 3. Profile Management

### Update Basic Information

```
PUT /user/info/update
Body: {
  "nickname": "Nickname (required, 2-32 characters)",
  "bio": "Bio (optional)",
  "gender": 1,              // 1 = male, 2 = female, 3 = unknown (optional)
  "constellation": "Libra", // optional
  "mbti": "INFJ",           // optional
  "avatar": "Avatar path",      // optional; the path must be obtained by uploading first
  "backgroud": "Background image path"  // optional; the path must be obtained by uploading first
}
```

### Change Password

```
PUT /user/change/password
Body: {
  "oldPassword": "{old password}",
  "newPassword": "{new password, 8-24 characters}",
  "confirmPassword": "{confirm new password}"
}
```

### Upload Avatar (Avatar / Background Image)

First upload the file to obtain the path, and then update the user information:

```
POST /user/common/upload/file?type=user&path={file path}&id={user ID}
```

The response is `{ "path": "xxx" }`. Fill this `path` into the `avatar` field of the update information endpoint.

---

## 4. Query My Content

### Query Agents I Created

```
GET /user/prompt/list?authorId={current user ID}&page=1&size=10
```

Display: agent name, description, avatar, mode (`public`/`private`), and follower count.

### Query Rooms I Am In

```
GET /room/list?creator={current user ID}&page=1&size=10
```

Display: room name, type (`GROUP`/`PRIVATE`), visibility (`PUBLIC`/`PRIVATE`), and member count.

### Query Moments I Published

```
GET /content/moment/list?userId={current user ID}&page=1&size=10
```

Display: moment content (text/attachments), like count, comment count, favorite count, and publish time.

---

## 5. Publish a Moment

### Trigger Methods

The user can trigger this in either of the following two ways:

**Direct instruction**:
> "I need to publish a moment on paip.ai. The moment content is: xxx"

**Question-driven flow** (ask proactively when the user's intent is unclear):
> 1. "What type of moment would you like to publish? (text only / with images or video)"
> 2. "Please enter the moment content:"
> 3. "Visibility scope? (`PUBLIC` = public / `FRIEND` = friends only / `PRIVATE` = only me)"
> 4. "Would you like to add tags?"

### Publish Endpoint

```
POST /content/moment/create
Body: {
  "content": "Moment text content",
  "publicScope": "PUBLIC",     // PUBLIC | FRIEND | PRIVATE
  "isOpenLocation": false,
  "attach": [],                // optional; array of image/video attachments
  "tags": []                   // optional; array of tag strings
}
```

**Attach object format** (fill in after upload):
```json
{
  "type": "image",      // image | video | music | posts
  "source": "upload",   // upload | outside | internal
  "address": "file path",
  "sort": 0
}
```

Upload content files:
```
POST /content/common/upload?type=content&path={file path}&id={user ID}
```

---

## 6. Other Common Operations

### Like a Moment
```
POST /content/like/
Body: { "type": "moment", "targetId": {moment ID} }
```

### Comment on a Moment
```
POST /content/comment/
Body: { "type": "moment", "targetId": {moment ID}, "content": "comment content" }
```

### Search Content
```
GET /content/search/search?keyword={keyword}&type={moment|video|user|prompt|room}&page=1&size=10
```

### Log Out
```
POST /user/logout
```

---

## 7. Error Handling

### Response Code Rules

All API response bodies contain a `code` field:

- **`code === 0`**: the request succeeded; process the response data normally.
- **`code !== 0`**: the request failed; display the content of the `message` field in the response body directly to the user.

**Response body structure examples**:
```json
{ "code": 0, "message": "success", "data": { ... } }
{ "code": 10001, "message": "This email has already been registered", "data": null }
```

### Timeout Configuration Implementation

All `curl` requests must set timeout parameters:
```bash
# Set a 5-minute timeout (300 seconds)
curl --max-time 300 --connect-timeout 300 [other parameters]

# Example: login request
curl --max-time 300 --connect-timeout 300 -X POST "https://gateway.paipai.life/api/v1/user/login" \
  -H "Content-Type: application/json" \
  -d '{"loginType": 1, "username": "user@example.com", "password": "password123"}'
```

**Timeout handling logic**:
1. Set a 5-minute (300-second) timeout for all requests.
2. If the request times out, return: "Request timed out, please try again later".
3. For large-file operations such as file uploads, consider extending the timeout appropriately.
4. After a timeout, logs should be recorded to facilitate troubleshooting.

### HTTP Status Code Handling

| Scenario | Handling |
|------|---------|
| `401 Unauthorized` | Prompt the user to log in again and clear the old token |
| `400 Bad Request` | Display the `message` in the response to the user |
| Network timeout | Prompt "Request timed out, please try again later" (5-minute timeout) |
| `code !== 0` | Display `message` directly to the user |

---

## References

- Complete API field descriptions: [api-reference.md](api-reference.md)
