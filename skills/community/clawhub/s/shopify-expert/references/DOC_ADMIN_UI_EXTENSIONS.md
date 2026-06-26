# Shopify docs: Admin Ui Extensions

> Generated from Shopify official LLM documentation snapshot (maintainer export). Prefer live docs at [shopify.dev](https://shopify.dev/) for API versions and current behaviour.

---
## Admin UI extensions

### Admin UI extensions

An [admin UI extension](https://shopify.dev/docs/api/admin-extensions) is a JavaScript-based module that can hook in to client-side behaviors on any of Shopify’s first-party UI surface areas. These extensions enable your app to embed workflows and UX on core admin pages while automatically matching the Shopify admin's look and feel.

Shopify provides different “variants” of UI extension APIs that are suitable for different developers:

* [@shopify/ui-extensions](https://github.com/Shopify/ui-extensions/blob/unstable/packages/ui-extensions) lets developers use a small, strongly-typed JavaScript API for creating UI extensions.
* [@shopify/ui-extensions-react](https://github.com/Shopify/ui-extensions/blob/unstable/packages/ui-extensions-react) lets developers create UI extensions using [React](https://reactjs.org/).

#### Types of admin extensions

* **Admin actions**: Admin action extensions enable you to create transactional workflows within existing pages of the Shopify admin. Merchants can launch these extensions from the More actions menus on resource pages or from an index table's bulk action menu when one or more resources are selected.
* **Admin blocks**: Admin block extensions enable your app to embed contextual information and inputs directly on resource pages in the Shopify admin. When a merchant has added them to their pages, these extensions display as cards inline with the other resource information. With admin block extensions, merchants can view and modify information from your app and other data on the page simultaneously. To facilitate complex interactions and transactional changes, you can launch admin actions directly from an admin block.
* **Admin print actions**: Admin print actions extensions are a special form of action extension designed to let your app print documents from key pages in the Shopify admin. Unlike a typical admin action extension, these extensions are found under the Print menu on orders and product pages.

#### Create a new admin extension

To create a new extension, use Shopify CLI:

```
shopify app generate extension
```

##### Deploy an admin extension

To deploy an admin extension, run this within your app's directory:

```
npm run deploy
```

#### Example: Build an admin action

In this example, we create an extension’s UI and render it.

First, we’ll create a `shopify.extension.toml` file that targets `admin.product-details.action.render`:

```
api_version = "2025-01"

[[extensions]]
# Change the merchant-facing name of the extension in locales/en.default.json
name = "t:name"
handle = "issue-tracker-action"
type = "ui_extension"
[[extensions.targeting]]
module = "./src/ActionExtension.jsx"
# The target used here must match the target used in the module file (./src/ActionExtension.jsx)
target = "admin.product-details.action.render"

```

Next, we set the title of the page in `/locales/en.default.json`:

```
{
  "name": "Create an issue"
}
```

Then, in `/src/ActionExtension.jsx` we’ll import the necessary components from Remote UI:

```
import {
  reactExtension,
  useApi,
  TextField,
  AdminAction,
  Button,
  TextArea,
  Box,
} from "@shopify/ui-extensions-react/admin";
```

Then we’ll build out the file with the target, logic, and UI rendering:

```
import { useCallback, useEffect, useState } from "react";
import {
  reactExtension,
  useApi,
  TextField,
  AdminAction,
  Button,
  TextArea,
  Box,
} from "@shopify/ui-extensions-react/admin";
import { getIssues, updateIssues } from "./utils";

function generateId (allIssues) {
  return !allIssues?.length ? 0 : allIssues[allIssues.length - 1].id + 1;
};

function validateForm ({title, description}) {
  return {
    isValid: Boolean(title) && Boolean(description),
    errors: {
      title: !title,
      description: !description,
    },
  };
};

// The target used here must match the target used in the extension's .toml file at ./shopify.extension.toml
const TARGET = "admin.product-details.action.render";

export default reactExtension(TARGET, () => <App />);

function App() {
  //connect with the extension's APIs
  const { close, data } = useApi(TARGET);
  const [issue, setIssue] = useState({ title: "", description: "" });
  const [allIssues, setAllIssues] = useState([]);
  const [formErrors, setFormErrors] = useState(null);
  const { title, description } = issue;

  useEffect(() => {
    getIssues(data.selected[0].id).then(issues => setAllIssues(issues || []));
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const onSubmit = useCallback(async () => {
    const {isValid, errors} = validateForm(issue);
    setFormErrors(errors);

    if (isValid) {
      // Commit changes to the database
      await updateIssues(data.selected[0].id, [
        ...allIssues,
        {
          id: generateId(allIssues),
          completed: false,
          ...issue,
        }
      ]);
      // Close the modal using the 'close' API
      close();
    }
  }, [issue, data.selected, allIssues, close]);

  return (
    <AdminAction
      title="Create an issue"
      primaryAction={
        <Button onPress={onSubmit}>Create</Button>
      }
      secondaryAction={<Button onPress={close}>Cancel</Button>}
    >
      <TextField
        value={title}
        error={formErrors?.title ? "Please enter a title" : undefined}
        onChange={(val) => setIssue((prev) => ({ ...prev, title: val }))}
        label="Title"
        maxLength={50}
      />
      <Box paddingBlockStart="large">
        <TextArea
          value={description}
          error={
            formErrors?.description ? "Please enter a description" : undefined
          }
          onChange={(val) =>
            setIssue((prev) => ({ ...prev, description: val }))
          }
          label="Description"
          maxLength={300}
        />
      </Box>
    </AdminAction>
  );
}

```

