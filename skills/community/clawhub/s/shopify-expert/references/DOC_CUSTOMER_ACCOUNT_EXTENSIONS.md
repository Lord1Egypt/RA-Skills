# Shopify docs: Customer Account Extensions

> Generated from Shopify official LLM documentation snapshot (maintainer export). Prefer live docs at [shopify.dev](https://shopify.dev/) for API versions and current behaviour.

---
## Customer account extensions

### Customer account extensions

[Customer account UI extensions](https://shopify.dev/docs/api/customer-account-ui-extensions) let app developers build custom functionality that merchants can install at defined points on the Order index, Order status, and Profile pages in customer accounts.

Customers can navigate to their account from the online store, from order notification emails, or any custom entrypoint placed by the merchant. If the customer is not already logged in, clicking a link from an order notification email to view their order will bring them to the pre-authenticated Order status page. From there, if the customer tries to navigate to another page in their account, or tries to take an action, they’ll be prompted to log in. Once the customer logs in, they are fully authenticated and able to access all customer account pages.

Using customer account UI extensions, apps can extend the functionality of existing customer account pages, as well as, create new pages (full-page extensions).

#### Scaffold an extension

Use Shopify CLI to generate a new extension in the directory of your app:

```
npm init @shopify/app@latest
cd your-app
npm run shopify app generate extension
```

#### Configure extension targets

[Extension targets](https://shopify.dev/docs/api/customer-account-ui-extensions/2025-01/extension-targets-overview) provide locations for customer account UI extensions to appear. Extension UIs are rendered using remote UI, a fast and secure environment for custom (non-DOM) UIs.

```
import {
  reactExtension,
  Banner,
  useTranslate,
} from '@shopify/ui-extensions-react/customer-account';

reactExtension('customer-account.order-index.block.render', () => (
  <App />
));

function App() {
  const translate = useTranslate();
  return <Banner>{translate('welcomeMessage')}</Banner>;
}
```

#### Update your configuration file

When you create a customer account UI extension, the `shopify.extension.toml` file is automatically generated in your customer account UI extension directory. It contains the extension's configuration, which includes the extension name, extension targets, metafields, capabilities and settings definition.

```
api_version = "unstable"

[[extensions]]
name = "My customer account ui extension"
handle = "customer-account-ui"
type = "ui_extension"

[[extensions.targeting]]
target = "customer-account.order-status.block.render"
module = "./Extension.jsx"
```

#### Extension APIs

APIs enable customer account UI extensions to get information about the customer or related objects and to perform actions. For example, you can use APIs to retrieve previous orders of the customer so that you can offer related products as upsells. Extensions use JavaScript to read and write data and call external services, and natively render UIs built using Shopify's checkout and customer account components.

```
import {
  reactExtension,
  Banner,
  useTranslate,
} from '@shopify/ui-extensions-react/customer-account';

reactExtension(
  'customer-account.order-status.block.render',
  () => <App />,
);

function App() {
  const translate = useTranslate();
  return <Banner>{translate('welcomeMessage')}</Banner>;
}

```

#### UI components

Customer account UI extensions declare their interface using supported UI components. Shopify renders the UI natively so it's performant, accessible, and works in all of customer account supported browsers. Components are designed to be flexible, enabling you to layer and mix them to create highly-customized app extensions that feel seamless within the customer account experience. All components that will inherit a merchant's brand settings and the CSS cannot be altered or overridden.

To build customer account UI extensions, you can use checkout components, and customer account components.

```
import {
  reactExtension,
  BlockStack,
  InlineStack,
  Button,
  Image,
  Text,
} from '@shopify/ui-extensions-react/customer-account';

reactExtension(
  'customer-account.order-status.block.render',
  () => <App />,
);

function App() {
  return (
    <InlineStack>
      <Image source="/url/for/image" />
      <BlockStack>
        <Text size="large">Heading</Text>
        <Text size="small">Description</Text>
      </BlockStack>
      <Button
        onPress={() => {
          console.log('button was pressed');
        }}
      >
        Button
      </Button>
    </InlineStack>
  );
}
```

