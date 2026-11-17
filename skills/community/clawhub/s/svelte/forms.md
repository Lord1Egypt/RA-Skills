# Forms, Actions, and Mutations

**Contents**: [The Baseline That Works Without JavaScript](#the-baseline-that-works-without-javascript) · [Action Rules](#action-rules) · [`use:enhance`](#useenhance) · [Multiple Actions, One Page](#multiple-actions-one-page) · [File Uploads](#file-uploads) · [Validation Placement](#validation-placement) · [CSRF and Origin Checks](#csrf-and-origin-checks) · [Preserving State Across Navigation](#preserving-state-across-navigation) · [Remote Functions](#remote-functions) · [Forms Checklist](#forms-checklist)

## The Baseline That Works Without JavaScript

```svelte
<!-- +page.svelte -->
<script>
  import { enhance } from '$app/forms';
  let { data, form } = $props();
</script>

<form method="POST" action="?/save" use:enhance>
  <input name="title" value={form?.values?.title ?? data.post.title} aria-invalid={form?.errors?.title ? 'true' : undefined} />
  {#if form?.errors?.title}<p class="error">{form.errors.title}</p>{/if}
  <button>Save</button>
</form>
```

```js
// +page.server.js
import { fail, redirect } from '@sveltejs/kit';

export const actions = {
  save: async ({ request, locals, params }) => {
    if (!locals.user) redirect(303, '/login');
    const data = await request.formData();
    const title = String(data.get('title') ?? '').trim();

    if (title.length < 3) {
      return fail(400, { values: { title }, errors: { title: 'Too short' } });
    }
    await db.updatePost(params.slug, { title });
    return { saved: true };
  }
};
```

Remove `use:enhance` and this still works: full page POST, 303 redirect, server-rendered errors. That is the property to protect.

## Action Rules

- `export const actions = { default: … }` for a single action; named actions are posted to `?/name`. **Default and named cannot coexist** in one file.
- Return value lands in the `form` prop of the page and in `page.form`. It must be serializable, like load data.
- `fail(status, data)` for validation failures: it sets the status and populates `form` without throwing. Returning `error(400)` instead renders the error page and loses the user's input.
- Never send the password (or any secret) back in `fail` — echo only the fields you want repopulated.
- `redirect(303, …)` after a successful mutation prevents the resubmit-on-refresh problem; `303` specifically, so the follow-up request is a GET.
- Actions run **after** any `handle` hook and have full access to `locals`, `cookies`, and `request`. Authorize inside the action: a hidden form or a client-side guard protects nothing.
- Actions receive `FormData`. For nested or repeated fields, name them `items[0].qty` and parse, or send JSON to a `+server.js` endpoint when the payload is genuinely not a form.

## `use:enhance`

Default behavior with no callback: submits via fetch, and on the response —

| Result type | What happens |
|---|---|
| `success` | `form` updates, `invalidateAll()` runs, the page keeps its scroll and focus |
| `failure` | `form` updates with the `fail` payload; no invalidation |
| `redirect` | Client-side navigation to the target |
| `error` | Nearest `+error.svelte` renders |

Custom callback replaces all of it — you must finish the job yourself:

```svelte
<form method="POST" use:enhance={({ formData, cancel }) => {
  submitting = true;
  return async ({ result, update }) => {
    submitting = false;
    if (result.type === 'success') toast('Saved');
    await update({ reset: false });        // keeps field values; also reinvalidates
  };
}}>
```

- `update({ reset: false })` is the usual choice for edit forms; the default resets the form.
- `applyAction(result)` when you need the standard handling without the rest of `update`.
- `cancel()` in the setup phase aborts the submission (client-side validation, double-submit guard).
- Disable the submit button from a `$state` flag set in the callback, not from `navigating` — an enhanced submit is not a navigation.

## Multiple Actions, One Page

```svelte
<button formaction="?/publish">Publish</button>
<button formaction="?/delete" formnovalidate>Delete</button>
```

One `<form>`, two buttons, two actions — no JavaScript required. This is the correct pattern for list rows with per-item operations; give each row its own small form rather than one form with hidden ids and a client-side dispatcher.

## File Uploads

- `<form method="POST" enctype="multipart/form-data">` — without the enctype the server receives filenames, not files.
- `const file = data.get('avatar')` is a `File`; check `file.size` and `file.type` before touching the bytes, and validate the type from the content, not from the extension.
- `adapter-node` caps request bodies at `BODY_SIZE_LIMIT` (512 kB by default) — a large upload fails there long before your handler runs. Raise it deliberately or upload straight to object storage with a presigned URL.
- Serverless platforms impose their own body and duration limits; presigned direct upload sidesteps both.

## Validation Placement

| Layer | Job |
|---|---|
| HTML attributes (`required`, `type`, `pattern`, `maxlength`) | Instant feedback, zero JS, free |
| Server action | The only one that counts; runs for every submission |
| Client schema (shared with the server) | Avoids a round trip, must reuse the same schema |

Never validate only on the client. Never validate only in a `+server.js` the form does not use. A shared schema module imported by both the action and the client keeps the two from drifting; that is the entire value proposition of the form libraries.

## CSRF and Origin Checks

SvelteKit rejects `POST`/`PUT`/`PATCH`/`DELETE` form submissions whose `Origin` header does not match the app, returning **403**. Same-origin forms pass automatically. If a third party must post to your app, expose a `+server.js` endpoint with its own authentication rather than turning `csrf.checkOrigin` off globally.

## Preserving State Across Navigation

```js
export const snapshot = {
  capture: () => draft,
  restore: (value) => (draft = value)
};
```

Exported from `+page.svelte`, this saves and restores component state when the user navigates away and comes back — the fix for "I lost my half-typed form by tapping a link". The captured value must be JSON-serializable and is stored per history entry.

## Remote Functions

`@sveltejs/kit >=2.27`, behind `experimental.remoteFunctions`: `query`, `form`, `command`, and `prerender` exported from a `.remote.js` file give type-safe server functions callable from components, with the form variant keeping progressive enhancement. Experimental and subject to change: recommend them only when `experimental_features` is true (SKILL.md Configuration). Form actions remain the default for mutations either way.

## Forms Checklist

- Works with JavaScript disabled before `use:enhance` is added
- Every action authorizes and validates server-side
- Failures return `fail()` with repopulation values, never the password
- Success ends in `redirect(303, …)` or an explicit invalidation
- Custom `enhance` callbacks call `update()` or `applyAction()`
- Uploads have `enctype`, a size check, and a body-limit plan
