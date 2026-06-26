# Shopify docs: Polaris

> Generated from Shopify official LLM documentation snapshot (maintainer export). Prefer live docs at [shopify.dev](https://shopify.dev/) for API versions and current behaviour.

---
## Polaris Web Components

### Polaris Web Components

Polaris Web Components are Shopify's unified UI toolkit built on web platform standards. They provide consistent design and functionality across all Shopify surfaces including Admin, Checkout, Customer accounts, and POS. Built with actual web components technology, they're framework-agnostic and work with any JavaScript library or framework.

#### Why use Polaris Web Components?

We base our design guidelines on some basic principles, so you can build apps that are predictable and easy to use. Here are four key reasons to use Polaris Web Components:

* **Built for Shopify**: Apps must meet all directives to qualify for the [Built for Shopify](https://shopify.dev/docs/apps/launch/built-for-shopify) program.
* **A better merchant experience**: Merchants expect a predictable user experience that works like the rest of the Shopify admin.
* **Framework agnostic**: Works with React, Vue, vanilla JS, or any framework using standard HTML.
* **Accessible**: Built-in accessibility features ensure great experiences for all users.
* **Consistent**: Use the same components across all Shopify surfaces.

#### Setup Polaris Web Components

**Required script tag:**
```html
<script src="https://cdn.shopify.com/shopifycloud/polaris.js"></script>
```

**For TypeScript projects:**
```bash
npm install -D @shopify/polaris-types@latest
```

**Configure TypeScript:**
```json
{
  "compilerOptions": {
    "types": ["@shopify/polaris-types"]
  }
}
```

**For React projects:**

See our [App template](https://github.com/Shopify/shopify-app-template-react-router).

Getting set up with [React router](https://github.com/Shopify/shopify-app-js/blob/main/packages/apps/shopify-app-react-router/src/react/components/AppProvider/AppProvider.tsx#L111-L126)

#### Best practices

* **Follow accessibility guidelines**: [Ensure your app is accessible](https://shopify.dev/docs/apps/build/accessibility); Polaris components are designed with accessibility in mind.
* **Keep design consistent**: Stick to the guidelines provided in the Polaris documentation to maintain a cohesive user experience.
* **Use the latest version**: The CDN script automatically provides the latest version of components.

#### Common Polaris Web Components

You can find all the Polaris web components in the [Polaris documentation](/docs/api/app-home/polaris-web-components). Here are a few of the most common components along with their syntax.

##### Box

Box components provide layout and spacing control for content grouping. They're used similarly to cards for organizing content.

```html
<s-box padding="base" background="subdued" border="base" borderRadius="base">
  <s-heading>Content inside a box</s-heading>
  <s-text>Additional text content goes here</s-text>
</s-box>
```

##### Page Layout

Pages are structured using s-page as the main container with sections for content organization.

```html
<s-page heading="3/4 inch Leather pet collar">
  <s-link slot="breadcrumb-actions">Back</s-link>
  <s-button slot="secondary-actions">Duplicate</s-button>
  <s-button slot="secondary-actions">View</s-button>
  <s-button slot="primary-action" variant="primary" disabled>Save</s-button>

  <s-section heading="Credit card">
    <s-text>Credit card information</s-text>
  </s-section>
</s-page>
```

##### Grid Layout

Grid components are used for creating responsive layouts with consistent spacing and alignment.

```html
<s-grid gridTemplateColumns="repeat(2, 1fr)" gap="small">
  <s-box padding="base" border="base" borderRadius="base">
    <s-heading>Online store dashboard</s-heading>
    <s-text>View a summary of your online store's performance.</s-text>
  </s-box>
  <s-box padding="base" border="base" borderRadius="base">
    <s-heading>Analytics</s-heading>
    <s-text>Track your store performance.</s-text>
  </s-box>
</s-grid>
```

##### Button

Buttons are used in Polaris primarily for actions, such as "Add", "Close", "Cancel", or "Save".

```html
<s-button variant="primary">Add product</s-button>
<s-button variant="secondary">Cancel</s-button>
<s-button variant="tertiary" tone="critical">Delete</s-button>

<!-- Buttons with icons -->
<s-button variant="primary" icon="plus">Add product</s-button>
<s-button variant="secondary" loading>Processing...</s-button>

<!-- Button with href for navigation -->
<s-button href="/products" target="_self">View products</s-button>
```

##### Text Field

Text fields are used as input fields that merchants can type into. They support various formats including text, email, and numbers.

```html
<s-text-field
  label="Store name"
  value="Jaded Pixel"
  placeholder="Enter store name"
  details="This will be displayed to customers">
</s-text-field>

<!-- For email fields -->
<s-email-field
  label="Email"
  placeholder="user@example.com"
  details="Used for sending notifications"
  required>
</s-email-field>

<!-- For numbers -->
<s-number-field
  label="Price"
  value="29.99"
  prefix="$"
  min="0">
</s-number-field>
```

##### Checkbox

Checkboxes are most commonly used in Polaris to give merchants a way to make a range of selections (zero, one, or multiple).

```html
<s-checkbox
  label="Basic checkbox"
  details="Additional information about this option">
</s-checkbox>

<s-checkbox
  label="Require a confirmation step"
  details="Ensure all criteria are met before proceeding"
  checked>
</s-checkbox>
```

##### Choice List

Choice lists are used to present options where merchants must make a single selection. The choice list automatically handles radio button behavior when multiple=false and checkbox behavior when multiple=true.

```html
<s-choice-list
  label="Company name"
  name="Company name"
  details="The company name will be displayed on the checkout page."
>
  <s-choice value="hidden">Hidden</s-choice>
  <s-choice value="optional">Optional</s-choice>
  <s-choice value="required">Required</s-choice>
</s-choice-list>
```

##### Additional Common Components

**Badge**: Used to highlight status or provide quick visual context.
```html
<s-badge tone="success">Active</s-badge>
<s-badge tone="warning">Pending</s-badge>
<s-badge tone="critical">Error</s-badge>
<s-badge color="strong" size="large">Featured</s-badge>
```

**Banner**: Used for important messaging that affects the entire page or section.
```html
<s-banner heading="Order archived" tone="info" dismissible>
  This order was archived on March 7, 2017 at 3:12pm EDT.
</s-banner>
```

**Modal**: Used for focused tasks that require user attention.
```html
<s-modal heading="Delete product" size="small">
  <s-text>Are you sure you want to delete this product? This action cannot be undone.</s-text>
  <s-button variant="primary" tone="critical" slot="primary-action">Delete</s-button>
  <s-button variant="secondary" slot="secondary-actions">Cancel</s-button>
</s-modal>
```

**Stack**: Used for flexible layout with consistent spacing.
```html
<s-stack direction="block" gap="base">
  <s-heading>Customer information</s-heading>
  <s-text>Email: customer@example.com</s-text>
  <s-text>Phone: +1 (555) 123-4567</s-text>
</s-stack>

<s-stack direction="inline" gap="small">
  <s-button variant="primary">Save</s-button>
  <s-button variant="secondary">Cancel</s-button>
</s-stack>
```


## Polaris

### Polaris

Shopify Polaris is the design system used by Shopify to create a consistent user interface across applications. We believe that the best apps provide merchants with a user experience that matches the appearance and behaviors of the Shopify admin UI. Using Polaris lets you achieve that consistency.

#### Why follow Polaris?

We base our design guidelines on some basic principles, so you can build apps that are predictable and easy to use. Here are four key reasons to follow the guidelines:

* **Built for Shopify**: Apps must meet all directives to qualify for the [Built for Shopify](https://shopify.dev/docs/apps/launch/built-for-shopify) program.
* **A better merchant experience**: Merchants expect a predictable user experience that works like the rest of the Shopify admin.
* **Adaptive:** Designing for mobile devices must be at the forefront of the app building process.
* **Accessible**: To provide a great experience for all Shopify merchants and their customers, apps must be built using accessibility best practices.

#### Install Polaris

```
npm install @shopify/polaris
```

#### Best practices

* **Use components**: Always use Polaris components for consistency and accessibility.
* **Follow accessibility guidelines**: [Ensure your app is accessible](https://shopify.dev/docs/apps/build/accessibility); Polaris components are designed with accessibility in mind.
* **Keep design consistent**: Stick to the guidelines provided in the Polaris documentation to maintain a cohesive user experience.
* **Use the latest version**: Regularly check for updates to Polaris to take advantage of new components and features.

#### Common Polaris Components

You can find all the Polaris components on [polaris.shopify.com](https://polaris.shopify.com/). Here are a few of the most common components along with their syntax.

##### Card

Cards are used in Polaris to group similar concepts and tasks together for merchants to scan, read, and get things done. It displays content in a familiar and recognizable style.

```
import {Card, Text} from '@shopify/polaris';
import React from 'react';

function CardDefault() {
  return (
    <Card>
      <Text as="h2" variant="bodyMd">
        Content inside a card
      </Text>
    </Card>
  );

}
```

##### Page

Pages are used in Polaris to build the outer wrapper of a page, including the page title and associated actions.

```
import {Page, Badge, LegacyCard} from '@shopify/polaris';
import React from 'react';

function PageExample() {
  return (
    <Page
      backAction={{content: 'Products', url: '#'}}
      title="3/4 inch Leather pet collar"
      titleMetadata={<Badge tone="success">Paid</Badge>}
      subtitle="Perfect for any pet"
      compactTitle
      primaryAction={{content: 'Save', disabled: true}}
      secondaryActions={[
        {
          content: 'Duplicate',
          accessibilityLabel: 'Secondary action label',
          onAction: () => alert('Duplicate action'),
        },
        {
          content: 'View on your store',
          onAction: () => alert('View on your store action'),
        },
      ]}
      actionGroups={[
        {
          title: 'Promote',
          actions: [
            {
              content: 'Share on Facebook',
              accessibilityLabel: 'Individual action label',
              onAction: () => alert('Share on Facebook action'),
            },
          ],
        },
      ]}
      pagination={{
        hasPrevious: true,
        hasNext: true,
      }}
    >
      <LegacyCard title="Credit card" sectioned>
        <p>Credit card information</p>
      </LegacyCard>
    </Page>
  );
}
```

##### Layout

The layout component is used in Polaris to create the main layout on a page. Layouts sections come in three main configurations. one-column, two-column, and annotated.

```
import {Page, Layout, LegacyCard} from '@shopify/polaris';
import React from 'react';

function LayoutExample() {
  return (
    <Page fullWidth>
      <Layout>
        <Layout.Section>
          <LegacyCard title="Online store dashboard" sectioned>
            <p>View a summary of your online store’s performance.</p>
          </LegacyCard>
        </Layout.Section>
      </Layout>
    </Page>
  );
}
```

##### Tabs

Tabs are used in Polaris to alternate among related views within the same context.

```
import {LegacyCard, Tabs} from '@shopify/polaris';
import {useState, useCallback} from 'react';

function TabsDefaultExample() {
  const [selected, setSelected] = useState(0);

  const handleTabChange = useCallback(
    (selectedTabIndex: number) => setSelected(selectedTabIndex),
    [],
  );

  const tabs = [
    {
      id: 'all-customers-1',
      content: 'All',
      accessibilityLabel: 'All customers',
      panelID: 'all-customers-content-1',
    },
    {
      id: 'accepts-marketing-1',
      content: 'Accepts marketing',
      panelID: 'accepts-marketing-content-1',
    },
    {
      id: 'repeat-customers-1',
      content: 'Repeat customers',
      panelID: 'repeat-customers-content-1',
    },
    {
      id: 'prospects-1',
      content: 'Prospects',
      panelID: 'prospects-content-1',
    },
  ];

  return (
    <Tabs tabs={tabs} selected={selected} onSelect={handleTabChange}>
      <LegacyCard.Section title={tabs[selected].content}>
        <p>Tab {selected} selected</p>
      </LegacyCard.Section>
    </Tabs>
  );
}
```

##### Button

Buttons are used in Polaris primarily for actions, such as “Add”, “Close”, “Cancel”, or “Save”.

```
import {Button} from '@shopify/polaris';
import React from 'react';

function ButtonExample() {
  return <Button>Add product</Button>;
}
```

##### TextField

A text field are used in Polaris as input fields that merchants can type into. It has a range of options and supports several text formats including numbers.

```
import {TextField} from '@shopify/polaris';
import {useState, useCallback} from 'react';

function TextFieldExample() {
  const [value, setValue] = useState('Jaded Pixel');

  const handleChange = useCallback(
    (newValue: string) => setValue(newValue),
    [],
  );

  return (
    <TextField
      label="Store name"
      value={value}
      onChange={handleChange}
      autoComplete="off"
    />
  );
}
```

##### Checkbox

Checkboxes are most commonly used in Polaris to give merchants a way to make a range of selections (zero, one, or multiple).

```
import {Checkbox} from '@shopify/polaris';
import {useState, useCallback} from 'react';

function CheckboxExample() {
  const [checked, setChecked] = useState(false);
  const handleChange = useCallback(
    (newChecked: boolean) => setChecked(newChecked),
    [],
  );

  return (
    <Checkbox
      label="Basic checkbox"
      checked={checked}
      onChange={handleChange}
    />
  );
}
```

##### Radio button

Radio buttons are used in Polaris to present each item in a list of options where merchants must make a single selection.

```
import {LegacyStack, RadioButton} from '@shopify/polaris';
import {useState, useCallback} from 'react';

function RadioButtonExample() {
  const [value, setValue] = useState('disabled');

  const handleChange = useCallback(
    (_: boolean, newValue: string) => setValue(newValue),
    [],
  );

  return (
    <LegacyStack vertical>
      <RadioButton
        label="Accounts are disabled"
        helpText="Customers will only be able to check out as guests."
        checked={value === 'disabled'}
        id="disabled"
        name="accounts"
        onChange={handleChange}
      />
      <RadioButton
        label="Accounts are optional"
        helpText="Customers will be able to check out with a customer account or as a guest."
        id="optional"
        name="accounts"
        checked={value === 'optional'}
        onChange={handleChange}
      />
    </LegacyStack>
  );
}
```

