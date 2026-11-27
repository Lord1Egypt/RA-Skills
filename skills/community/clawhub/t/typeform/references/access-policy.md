# Typeform access policy

An access policy limits which endpoints Typeform connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/typeform#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Typeform: its 25 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create typeform --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "me"},
    {"method": "GET", "path": "forms"},
    {"method": "GET", "path": "forms/{id}"},
    {"method": "GET", "path": "forms/{id}/messages"},
    {"method": "GET", "path": "images"},
    {"method": "GET", "path": "images/{id}"},
    {"method": "GET", "path": "images/{id}/background/{id}"},
    {"method": "GET", "path": "images/{id}/choice/{id}"},
    {"method": "GET", "path": "images/{id}/image/{id}"},
    {"method": "GET", "path": "insights/{id}/summary"},
    {"method": "GET", "path": "media/audios/{id}/master"},
    {"method": "POST", "path": "media/videos/list"},
    {"method": "GET", "path": "media/videos/{id}/master"},
    {"method": "GET", "path": "forms/{id}/responses"},
    {"method": "POST", "path": "forms/{id}/responses/search"},
    {"method": "GET", "path": "themes"},
    {"method": "GET", "path": "themes/{id}"},
    {"method": "GET", "path": "forms/{id}/translations/main"},
    {"method": "GET", "path": "forms/{id}/translations/status"},
    {"method": "GET", "path": "forms/{id}/translations/{id}"},
    {"method": "GET", "path": "forms/{id}/responses/files"},
    {"method": "GET", "path": "forms/{id}/responses/{id}/fields/{id}/files/{id}"},
    {"method": "GET", "path": "accounts/{id}/workspaces"},
    {"method": "GET", "path": "workspaces"},
    {"method": "GET", "path": "workspaces/{id}"}
  ],
  "deny": []
}
```

## Endpoints

The Typeform endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | me | read | account | Retrieve the authenticated user account information. |
| GET | forms | read | forms | List all forms in the account (public and private). |
| POST | forms | write | forms | Create a new form. |
| GET | forms/{id} | read | forms | Retrieves a form by the given form_id. |
| PUT | forms/{id} | write | forms | Replace an existing form with a full new definition. |
| PATCH | forms/{id} | write | forms | Partially update an existing form with JSON Patch operations. |
| DELETE | forms/{id} | write | forms | Deletes the form with the given form_id and all of the form's responses. |
| GET | forms/{id}/messages | read | forms | Retrieve the customizable messages for a form in its language. |
| PUT | forms/{id}/messages | write | forms | Specifies new values for the customizable messages in a form (specified by form_id). |
| GET | images | read | images | List all images in the account. |
| POST | images | write | images | Adds an image in your Typeform account. |
| GET | images/{id} | read | images | Retrieves the JSON description or the binary of the original image for the specified image_id. |
| DELETE | images/{id} | write | images | Deletes an image from your Typeform account. |
| GET | images/{id}/background/{id} | read | images | Retrieve the JSON description or the binary of the requested background format. |
| GET | images/{id}/choice/{id} | read | images | Retrieve the JSON description or the binary of the requested choice format. |
| GET | images/{id}/image/{id} | read | images | Retrieve the JSON description or the binary of the requested image. |
| GET | insights/{id}/summary | read | insights | Get a summary of insights for a form. |
| GET | media/audios/{id}/master | read | media | Retrieves the processed master audio file URL. |
| POST | media/audios/{id}/master | write | media | Initiates the master file generation process for an audio file. |
| POST | media/videos | write | media | Creates a new video upload. |
| POST | media/videos/list | read | media | Retrieves multiple videos with optional per-video clip time configurations for instant clipping. |
| GET | media/videos/{id}/master | read | media | Retrieves the processed master video file URL. |
| POST | media/videos/{id}/master | write | media | Initiates the master file generation process for a video. |
| GET | forms/{id}/responses | read | responses | Returns form responses and date and time of form landing and submission. |
| DELETE | forms/{id}/responses | write | responses | Delete responses to a form. |
| POST | forms/{id}/responses/search | read | responses | Retrieves form responses using a structured filter format that supports combining multiple conditions on answers, metadata, tags, hidden fields, response IDs, and... |
| GET | themes | read | themes | List all themes in the account (public and private). |
| POST | themes | write | themes | Creates a new theme. |
| GET | themes/{id} | read | themes | Retrieves a theme in your Typeform account. |
| PUT | themes/{id} | write | themes | Replace a theme with a full new definition. |
| PATCH | themes/{id} | write | themes | Partially update a theme. |
| DELETE | themes/{id} | write | themes | Deletes a theme from your Typeform account. |
| GET | forms/{id}/translations/main | read | translations | Retrieves the form content in the main language, as if it were a translation. |
| GET | forms/{id}/translations/status | read | translations | Retrieve the status of the translations for each language for a given form. |
| GET | forms/{id}/translations/{id} | read | translations | Serves the translation payload for a given language. |
| PUT | forms/{id}/translations/{id} | write | translations | Updates the content of a translation for a given form and language. |
| DELETE | forms/{id}/translations/{id} | write | translations | Deletes the content of a translation for a given form and language. |
| POST | forms/{id}/translations/{id}/auto | write | translations | Requests an automatic translation for a form and language, stores and returns it. |
| GET | forms/{id}/responses/files | read | uploaded files | Download a zip archive containing all files uploaded by respondents for the specified form ID. |
| GET | forms/{id}/responses/{id}/fields/{id}/files/{id} | read | uploaded files | Download an uploaded file knowing its form, response, field and name. |
| GET | forms/{id}/webhooks | write | webhooks | Retrieve all webhooks for the specified typeform. Kept out of read: the webhook object schema includes the signing secret. |
| GET | forms/{id}/webhooks/{id} | write | webhooks | Retrieve a single webhook. Kept out of read: the webhook object schema includes the signing secret. |
| PUT | forms/{id}/webhooks/{id} | write | webhooks | Create or update a webhook. |
| DELETE | forms/{id}/webhooks/{id} | write | webhooks | Delete a webhook. |
| GET | accounts/{id}/workspaces | read | workspaces | Retrieve all workspaces you have access to within the specific account. |
| POST | accounts/{id}/workspaces | write | workspaces | Create a workspace in a specific account. |
| GET | workspaces | read | workspaces | Retrieve all workspaces you have access to. |
| POST | workspaces | write | workspaces | Create a workspace. |
| GET | workspaces/{id} | read | workspaces | Retrieve a workspace. |
| PATCH | workspaces/{id} | write | workspaces | Update a workspace. |
| DELETE | workspaces/{id} | write | workspaces | Delete a workspace. |
