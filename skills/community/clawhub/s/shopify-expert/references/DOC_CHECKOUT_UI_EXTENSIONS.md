# Shopify docs: Checkout Ui Extensions

> Generated from Shopify official LLM documentation snapshot (maintainer export). Prefer live docs at [shopify.dev](https://shopify.dev/) for API versions and current behaviour.

---
## Checkout UI extensions

### Checkout UI extensions

[Checkout UI Extensions](https://shopify.dev/docs/api/checkout-ui-extensions) allow developers to customize the checkout experience for Shopify stores. They allow merchants to add custom fields, promotional messages, and more.

#### Key concepts

* [**Extension targets**](https://shopify.dev/docs/api/checkout-ui-extensions/2025-01/extension-targets-overview): Extension targets provide locations where merchants can insert custom content.
  * **Static extension targets** are tied to core checkout features like contact information, shipping methods, and order summary line items.
  * **Block extension targets** can be displayed at any point in the checkout process and will always render regardless of which checkout features are available.
* **Configuration file**: The `shopify.extension.toml` contains the extension's configuration, which includes the extension name, extension targets, metafields, capabilities, and settings definition.
* [**Extension APIs**](https://shopify.dev/docs/api/checkout-ui-extensions/2025-01/apis): APIs enable checkout UI extensions to get information about the checkout or related objects and to perform actions
* [**UI components**](https://shopify.dev/docs/api/checkout-ui-extensions/2025-01/components): Checkout UI extensions declare their interface using supported UI components. Shopify renders the UI natively, so it's performant, accessible, and works in all of checkout's supported browsers.
* **Security**: Checkout UI extensions are a safe and secure way to customize the appearance and functionality of the checkout page without compromising the security of checkout or customer data.

#### Create a new extension

To create a new extension, use the Shopify CLI:

```
shopify app generate extension
```

#### Common components

##### View

View in checkout UI extensions is a generic container component. Its contents will always be their “natural” size, so this component can be useful in layout components.

```
import {
  reactExtension,
  View,
} from '@shopify/ui-extensions-react/checkout';

export default reactExtension(
  'purchase.checkout.block.render',
  () => <Extension />,
);

function Extension() {
  return (
    <View padding="base" border="base">
      View
    </View>
  );
}

```

##### InlineLayout

InlineLayout in checkout UI extensions is used to lay out content over multiple columns.

```
import {
  reactExtension,
  InlineLayout,
  View,
} from '@shopify/ui-extensions-react/checkout';

export default reactExtension(
  'purchase.checkout.block.render',
  () => <Extension />,
);

function Extension() {
  return (
    <InlineLayout columns={['20%', 'fill']}>
      <View border="base" padding="base">
        20%
      </View>
      <View border="base" padding="base">
        fill
      </View>
    </InlineLayout>
  );
}

```

##### Button

Buttons in checkout UI extensions are used for actions, such as “Add”, “Continue”, “Pay now”, or “Save”.

```
import {
  reactExtension,
  Button,
} from '@shopify/ui-extensions-react/checkout';

export default reactExtension(
  'purchase.checkout.block.render',
  () => <Extension />,
);

function Extension() {
  return (
    <Button
      onPress={() => {
        console.log('onPress event');
      }}
    >
      Pay now
    </Button>
  );
}

```

##### Link

Links in checkout UI extensions make text interactive so customers can perform an action, such as navigating to another location.

```
import {
  reactExtension,
  Link,
} from '@shopify/ui-extensions-react/checkout';

export default reactExtension(
  'purchase.checkout.block.render',
  () => <Extension />,
);

function Extension() {
  return (
    <Link to="https://www.shopify.ca/climate/sustainability-fund">
      Sustainability fund
    </Link>
  );
}

```

##### Modal

Modals in checkout UI extensions are a special type of overlay that shift focus towards a specific action/set of information before the main flow can proceed.

```
import {
  reactExtension,
  useApi,
  Button,
  Link,
  Modal,
  TextBlock,
} from '@shopify/ui-extensions-react/checkout';

export default reactExtension(
  'purchase.checkout.block.render',
  () => <Extension />,
);

function Extension() {
  const {ui} = useApi();

  return (
    <Link
      overlay={
        <Modal
          id="my-modal"
          padding
          title="Return policy"
        >
          <TextBlock>
            We have a 30-day return policy, which
            means you have 30 days after receiving
            your item to request a return.
          </TextBlock>
          <Button
            onPress={() =>
              ui.overlay.close('my-modal')
            }
          >
            Close
          </Button>
        </Modal>
      }
    >
      Return policy
    </Link>
  );
}

```

##### Banner

Banners in checkout UI extensions are used to communicate important messages to customers in a prominent way.

```
import {
  reactExtension,
  Banner,
} from '@shopify/ui-extensions-react/checkout';

export default reactExtension(
  'purchase.checkout.block.render',
  () => <Extension />,
);

function Extension() {
  return (
    <Banner
      status="critical"
      title="Your payment details couldn’t be verified. Check your card details and try again."
    />
  );
}
```

