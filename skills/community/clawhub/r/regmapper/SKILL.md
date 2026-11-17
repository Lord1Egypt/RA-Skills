---
name: regmapper
description: Browse, search, and annotate regulations via the RegMapper API. Use when asked about regulations, rules, compliance requirements, project annotations, or comparing regulation versions.
metadata:
  {
    "openclaw": {
      "emoji": "📋",
      "homepage": "https://regmapper.net",
      "primaryEnv": "REGMAPPER_API_TOKEN",
      "requires": { "env": ["REGMAPPER_API_TOKEN"] }
    }
  }
---
# Regulatory research with RegMapper API

Use the regmapper skill to browse and research laws and regulations in the RegMapper database. You can search for regulations, explore their chapter and rule structure, and read detailed rule content. You can also access project-scoped comments to gain insights from human reviewers. If you have write access to a project, you can add or update comments and set their status and category to enrich the dataset for future use. Additionally, you can compare different versions of a regulation and get a diff of changed rules.

## Authentication

- **Header for all API calls:**
  ```http
  Authorization: Token <token_value>
  ```
  - Replace `<token_value>` with your actual API token.
  - **Without this header or with an invalid token:** `401 Unauthorized`

- **Storing the token:**
  - Store the token in `skills/.env` as `REGMAPPER_API_TOKEN` so it is loaded automatically:
    ```env
    REGMAPPER_API_TOKEN=your_token_here
    ```

- **Base URL:**
  ```http
  https://regmapper.net/api/v1
  ```

## Obtaining an API Token

To use this skill, you need a RegMapper API token:

1. Visit [https://www.regmapper.net/account/signup/](https://www.regmapper.net/account/signup/) to register, confirm your email, and request a free account, then log in.
2. Go to **User profile** ([https://www.regmapper.net/users/user/myprofile/](https://www.regmapper.net/users/user/myprofile/)) → **API Token**
3. Generate a new token (keep it secret!)
4. Store it in `skills/.env` as shown above

**Security Note:** Never commit your `.env` file or share your token publicly.

*Note: For creating comments or using advanced features, you will need to create a project through the web interface first ([create project](https://www.regmapper.net/regs/project/create/))  *

## Token Storage & Setup

Store only `REGMAPPER_API_TOKEN` in `skills/.env`; create the file if missing. Add `.env` to `.gitignore`.

## Troubleshooting

401: Token invalid/expired → regenerate at RegMapper. 403: No project access → contact project admin.

## API Specification

The full OpenAPI specification is included as `openapi.json` in this skill package. See [https://www.regmapper.net/api/v1/schema/](https://www.regmapper.net/api/v1/schema/) for the live schema reference.

## Pagination

List endpoints are paginated (`page` query param, default page size 100).
Envelope: `count`, `next`, `previous`, `results`.

## Endpoints

- `GET /projects/`
  - Returns accessible projects.
  - Fields: `id`, `name`, `auth` (`read` or `write`).
  - Only call comment write endpoints when `auth=write`.

- `GET /projects/{id}/`
  - Returns project metadata and project-specific values for comments.
  - Fields: `id`, `name`, `reference`, `description`, `auth`, `categories` (`id`, `category`), `statuses` (`id`, `status`).
  - Requires `view_project` on that project (`403` otherwise).
  - Call this before create/update comment to obtain valid status and category IDs.

- `GET /projects/{id}/regulations/`
  - Returns all regulations linked to that project.
  - Fields: `regid`, `title`, `shortname`.

- `GET /projects/{id}/statuses/`
  - Returns statuses linked to that project.
  - Fields: `id`, `status`.

- `GET /projects/{id}/categories/`
  - Returns categories linked to that project.
  - Fields: `id`, `category`.

- `GET /regulations/`
  - Search/filter: `title`, `shortname`, `versdate`, `status`, `regulator`, `language`.
  - Returns all statuses when `status` is omitted. Add `status=current` to restrict to current versions only.

- `GET /regulations/{regid}/rules/overview/`
  - Lightweight chapter/rule overview.

- `GET /regulations/{regid}/rules/`
  - Detailed rules (optional `chapter`, `rule`, `page`).
  - Use the numeric rule `id` from results when creating comments.

- `GET /regulations/compare/{obs}/{new}/overview/` and `/rules/{rule}/{chapter}/`
  - Compare two regulation versions; use overview to discover changed rule/chapter pairs, then call detailed.
  - When calling compare detailed, always source `chapter` from an overview `merge` row to avoid ambiguity.
  - Overview rows expose `agg` (aggregated number of changed characters per rule) and `diff`; `sim`, `obs`, and `new` are only available on detailed compare rows.
  - Overview response also includes `rules_any` (rules with any project comments) and `rules_current` (rules with current-project comments) — useful for prioritizing which rules to inspect.
  - Detailed response includes `comment_refs` (list of `{id, project_id, rule_id, status_id}`) — use to detect existing annotations before creating a duplicate.
  - Detailed response includes `orig_url` and `copyright_url` — URLs to the source document and copyright page for citations.
  - In detailed results, `changes_html` uses semantic diff tags: `<ins>` = added text, `<del>` = removed text.
  - Color styles in HTML are presentational only; for robust bot logic prefer `diff`, `sim`, and `obs/new` text fields.

- `GET /comments/?project=<id>`
  - Read comments for one project.
  - Optional filters: `regulation|regulations`, `category|categories`, `status|statuses`, `q|text`.
  - Optional toggle: `include_note=true` (include full note in list/search response).
  - Missing `project` → `400`; no project access → `403`.
  - Default list payload is lightweight: includes `note_preview` (50 chars) and does not include `rule_content`.

- `GET /comments/{id}/`
  - Read exactly one comment with full content.
  - Includes full `note` and full `rule_content`.
  - Requires `view_project` on the comment's project.

- `POST /comments/`
  - Create comment.
  - Payload: `project`, `rule`, optional `note`, optional `status`, optional `category` (list of category ids).
  - Requires `change_project` on `project`.
  - `created_by` and `changed_by` are set from the token user automatically.

- `PATCH /comments/{id}/`
  - Partial update of `note`, `status`, `category`.
  - Requires `change_project` on the comment's project.
  - `changed_by` is set from the token user automatically.

## Recommended Bot Flow

1. Call `/projects/` and pick a project with `auth=read` or `auth=write`.
2. Call `/projects/{id}/regulations/`, `/projects/{id}/statuses/`, and `/projects/{id}/categories/` for linked metadata.
3. Use `/comments/?project=<id>` for search/list (compact response; add `include_note=true` if needed).
4. Use `/comments/{id}/` when full note and rule text are required.
5. Only if `auth=write`, use comment create/update endpoints.

## Comparing regulation versions

**Goal:** Identify changes between two versions of a regulation.

**Steps:**
1. **Find the older version:**
   ```bash
   curl -H "Authorization: Token <YOUR_TOKEN>" "https://regmapper.net/api/v1/regulations/?shortname=<REG>&status=obsolete"
   ```
   → Note the `regid` and `versdate` of the older version.

2. **Find the current version:**
   ```bash
   curl -H "Authorization: Token <YOUR_TOKEN>" "https://regmapper.net/api/v1/regulations/?shortname=<REG>&status=current"
   ```
   → Note the `regid` and `versdate` of the current version.

3. **Get comparison overview:**
   ```bash
   curl -H "Authorization: Token <YOUR_TOKEN>" "https://regmapper.net/api/v1/regulations/compare/{obs_regid}/{new_regid}/overview/"
   ```
   → Check the `diff` field: `"diff"` = changes present, `"same"` = no changes.

4. **Get detailed changes:**
   For each changed rule (`diff: "diff"`):
   ```bash
   curl -H "Authorization: Token <YOUR_TOKEN>" "https://regmapper.net/api/v1/regulations/compare/{obs_regid}/{new_regid}/rules/{rule}/{chapter}/"
   ```
   → Analyse `changes_html` (`<ins>` = added, `<del>` = removed) and `sim` (similarity score).

**Note:**
- `agg` = number of changed characters (useful for prioritization).
- Always use `chapter` from the `merge` row of the overview to avoid ambiguity.



