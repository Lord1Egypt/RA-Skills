# Shopify docs: Pos Ui Extensions

> Generated from Shopify official LLM documentation snapshot (maintainer export). Prefer live docs at [shopify.dev](https://shopify.dev/) for API versions and current behaviour.

---
## POS UI extensions

### POS UI extensions

[POS UI extensions](https://shopify.dev/docs/api/pos-ui-extensions) allow developers to create custom experiences within Shopify's Point of Sale (POS) app. They enable merchants to extend POS functionality with custom screens, actions, and integrations directly within the POS interface, creating seamless workflows for in-store operations.

#### Key concepts

* [**Extension targets**](https://shopify.dev/docs/api/pos-ui-extensions/targets): Extension targets define specific locations within the POS app where custom content can be rendered.
  * **Smart Grid targets** (`pos.home.tile.render`, `pos.home.modal.render`) appear on the POS home screen for quick access to app functionality.
  * **Product detail targets** (`pos.product-details.action.render`, `pos.product-details.block.render`) extend product pages with custom actions and information.
  * **Customer detail targets** (`pos.customer-details.action.render`, `pos.customer-details.block.render`) add functionality to customer profiles.
  * **Order detail targets** (`pos.order-details.action.render`, `pos.order-details.block.render`) customize order screens with custom actions and information blocks.
  * **Post-purchase targets** (`pos.purchase.post.action.render`, `pos.purchase.post.block.render`) customize the post-purchase experience.
  * **Event targets** (`pos.transaction-complete.event.observe`, `pos.cart-update.event.observe`) listen to POS events for reactive functionality.
* **Configuration file**: The `shopify.extension.toml` is the extension level configuration that includes the extension's name, the targets it extends, API Version, and description.
* [**Extension APIs**](https://shopify.dev/docs/api/pos-ui-extensions/apis): APIs enable POS UI extensions to interact with cart data, navigate between screens, access device capabilities, and manage customer information.
* [**UI components**](https://shopify.dev/docs/api/pos-ui-extensions/components): POS UI extensions use specialized components optimized for touch interfaces and POS workflows. Components are rendered natively for optimal performance.
* **Navigation patterns**: Extensions use Navigator and Screen components to create multi-screen experiences with proper navigation flow.

#### Create a new extension

To create a new POS UI extension, use the Shopify CLI:

```
shopify app generate extension --name="your-extension-name" --template="pos_ui" --flavor="typescript-react"
```

#### Block extensions

Block extensions render content directly within POS screens, appearing as integrated sections rather than separate modals or actions. They provide contextual information and functionality that enhances the merchant's workflow without disrupting their current task.

##### Product details block

Display additional product information, inventory details, or related data within the product details screen.

Here's an example of a block that shows real-time inventory information inline with the product details:

```
import React from 'react';
import {
  reactExtension,
  Stack,
  Text,
  Badge,
} from '@shopify/ui-extensions-react/point-of-sale';

export default reactExtension('pos.product-details.block.render', () => (
  <Stack direction="block" gap="200">
    <Text variant="sectionHeader">Inventory Information</Text>
    <Stack direction="inline" gap="100">
      <Text variant="body">Warehouse: </Text>
      <Badge status="info">In Stock</Badge>
    </Stack>
    <Text variant="captionRegular" color="TextSubdued">
      Last restocked: 2 days ago
    </Text>
  </Stack>
));
```

##### Customer details block

Show customer loyalty information, purchase history, or account status within the customer details screen.

Here's an example that displays a customer's loyalty program status and allows them to apply points directly from the customer details screen:

```
import React from 'react';
import {
  reactExtension,
  Stack,
  Text,
  Badge,
  Button,
  useApi,
} from '@shopify/ui-extensions-react/point-of-sale';

export default reactExtension('pos.customer-details.block.render', () => {
  const api = useApi();

  return (
    <Stack direction="block" gap="200">
      <Text variant="sectionHeader">Loyalty Program</Text>
      <Stack direction="inline" gap="100">
        <Text variant="body">Status: </Text>
        <Badge status="success">Gold Member</Badge>
      </Stack>
      <Text variant="body">Points Available: 2,450</Text>
      <Button
        title="Apply Points"
        type="basic"
        onPress={() => api.toast.show('Points applied to cart')}
      />
    </Stack>
  );
});
```

##### Order details block

Add custom order information, shipping details, or fulfillment tracking within order screens.

This example shows how to display shipping and tracking information within an order's details:

```
import React from 'react';
import {
  reactExtension,
  Stack,
  Text,
} from '@shopify/ui-extensions-react/point-of-sale';

export default reactExtension('pos.order-details.block.render', () => (
  <Stack direction="block" gap="200">
    <Text variant="sectionHeader">Shipping Information</Text>
    <Stack direction="block" gap="100">
      <Text variant="body">Tracking: #1Z999AA1234567890</Text>
      <Text variant="body">Carrier: UPS Ground</Text>
      <Text variant="captionRegular" color="TextSubdued">
        Estimated delivery: Tomorrow
      </Text>
    </Stack>
  </Stack>
));
```


##### Post-purchase block

Display additional options or information after a transaction is completed.

Here's an example that offers additional services to customers after they complete their purchase:

```
import React from 'react';
import {
  reactExtension,
  Stack,
  Text,
  Button,
  useApi,
} from '@shopify/ui-extensions-react/point-of-sale';

export default reactExtension('pos.purchase.post.block.render', () => {
  const api = useApi();

  return (
    <Stack direction="block" gap="200">
      <Text variant="sectionHeader">Additional Services</Text>
      <Stack direction="block" gap="100">
        <Button
          title="Schedule Delivery"
          type="basic"
          onPress={() => api.action.presentModal()}
        />
        <Button
          title="Add Protection Plan"
          type="basic"
          onPress={() => console.log('Protection plan selected')}
        />
      </Stack>
    </Stack>
  );
});
```

#### Common components

##### Box

Box components provide a container for grouping content with padding, margins, and sizing control. They're useful for creating consistent layouts and visual boundaries.

This example demonstrates using a Box component to create a padded container for customer notes:

```
import React from 'react';
import {
  reactExtension,
  Box,
  Text,
  Button,
} from '@shopify/ui-extensions-react/point-of-sale';

export default reactExtension('pos.customer-details.block.render', () => (
  <Box
    paddingInlineStart="200"
    paddingInlineEnd="200"
    paddingBlockStart="100"
    paddingBlockEnd="100"
  >
    <Text variant="sectionHeader">Customer Notes</Text>
    <Text variant="body">Premium customer - offer special discounts</Text>
    <Button title="Add Note" type="basic" />
  </Box>
));
```

##### Button

Buttons in POS UI extensions enable merchants to initiate actions like adding items, processing transactions, or opening modals.

Here's a simple button example that renders on the home screen tile:

```
import React from 'react';
import {
  reactExtension,
  Button,
} from '@shopify/ui-extensions-react/point-of-sale';

export default reactExtension('pos.home.tile.render', () => (
  <Button
    title="Add to Cart"
    type="primary"
    onPress={() => console.log('Button pressed')}
  />
));
```

##### List

List components display scrollable data in rows, perfect for product listings, customer information, or transaction histories. This is the recommended component for displaying long lists of data as it is optimized for better memory management.

This example shows how to create a product list with multiple items, each displaying label, subtitle, and price information:

```
import React from 'react';
import {
  reactExtension,
  List,
  Navigator,
  Screen,
} from '@shopify/ui-extensions-react/point-of-sale';

const listData = [
  {
    id: 'item1',
    leftSide: {
      label: 'Coffee Mug',
      subtitle: [{content: 'Kitchen & Dining'}, {content: 'In Stock'}],
    },
    rightSide: {
      label: '$12.99',
      showChevron: true,
    },
    onPress: () => console.log('Coffee Mug selected'),
  },
  {
    id: 'item2',
    leftSide: {
      label: 'T-Shirt',
      subtitle: [{content: 'Apparel'}, {content: 'Limited Stock'}],
    },
    rightSide: {
      label: '$24.99',
      showChevron: true,
    },
  },
];

export default reactExtension('pos.home.modal.render', () => (
  <Navigator>
    <Screen name="ProductList" title="Products">
      <List title="Available Items" data={listData} />
    </Screen>
  </Navigator>
));
```

##### Navigator

Navigator components manage navigation between multiple screens within an extension, enabling complex multi-step workflows.

Here's an example of a multi-screen navigation flow with Home and Details screens:

```
import React from 'react';
import {
  reactExtension,
  Navigator,
  Screen,
  Button,
  Text,
  useApi,
} from '@shopify/ui-extensions-react/point-of-sale';

export default reactExtension('pos.home.modal.render', () => {
  const api = useApi();

  return (
    <Navigator>
      <Screen name="Home" title="Main Menu">
        <Text variant="body">Welcome to the app</Text>
        <Button
          title="View Details"
          onPress={() => api.navigation.navigate('Details')}
        />
      </Screen>
      <Screen name="Details" title="Details">
        <Text variant="body">Detailed information here</Text>
        <Button
          title="Go Back"
          onPress={() => api.navigation.goBack()}
        />
      </Screen>
    </Navigator>
  );
});
```

##### Stack

Stack components provide flexible layout options for organizing UI elements horizontally or vertically with consistent spacing. We do not recommend Stacks for displaying extremely long lists of data, instead please use the List component.

This example demonstrates nested stacks to create a layout with buttons arranged horizontally within a vertical stack:

```
import React from 'react';
import {
  reactExtension,
  Stack,
  Button,
  Text,
} from '@shopify/ui-extensions-react/point-of-sale';

export default reactExtension('pos.customer-details.block.render', () => (
  <Stack direction="block" gap="200">
    <Text variant="sectionHeader">Customer Actions</Text>
    <Stack direction="inline" gap="100">
      <Button title="Edit" type="basic" />
      <Button title="Delete" type="critical" />
    </Stack>
  </Stack>
));
```

##### Text

Text components in POS UI extensions support various styling options for displaying information with appropriate hierarchy and emphasis.

Here's an example showing different text variants and how to create visual hierarchy:

```
import React from 'react';
import {
  reactExtension,
  Text,
  Stack,
} from '@shopify/ui-extensions-react/point-of-sale';

export default reactExtension('pos.product-details.block.render', () => (
  <Stack direction="block" gap="100">
    <Text variant="headingLarge">Product Information</Text>
    <Text variant="body">Additional product details</Text>
    <Text variant="captionRegular" color="TextSubdued">
      Last updated: Today
    </Text>
  </Stack>
));
```

#### Common APIs

##### Cart API

The Cart API enables extensions to interact with the POS cart, managing items, discounts, and customer information.

This example shows how to use the Cart API to add items to the cart and display the current cart item count:

```
import React from 'react';
import {
  reactExtension,
  Button,
  useApi,
  useCartSubscription,
} from '@shopify/ui-extensions-react/point-of-sale';

export default reactExtension('pos.product-details.action.render', () => {
  const api = useApi();
  const cart = useCartSubscription();

  return (
    <Button
      title={`Add to Cart (${cart.lineItems.length} items)`}
      onPress={async () => {
        await api.cart.addLineItem(12345, 1);
        api.toast.show('Item added to cart');
      }}
    />
  );
});
```

##### Navigation API

The Navigation API provides programmatic navigation control between screens within an extension.

Here's an example of using the Navigation API to navigate to a different screen with parameters:

```
import React from 'react';
import {
  reactExtension,
  Button,
  useApi,
} from '@shopify/ui-extensions-react/point-of-sale';

export default reactExtension('pos.order-details.action.render', () => {
  const api = useApi();

  return (
    <Button
      title="View Order History"
      onPress={() => api.navigation.navigate('OrderHistory', {
        customerId: '123'
      })}
    />
  );
});
```

##### Toast API

The Toast API displays temporary notification messages to provide feedback for user actions.

This example demonstrates using the Toast API to show a success message when an action is completed:

```
import React from 'react';
import {
  reactExtension,
  Button,
  useApi,
} from '@shopify/ui-extensions-react/point-of-sale';

export default reactExtension('pos.purchase.post.action.render', () => {
  const api = useApi();

  return (
    <Button
      title="Send Receipt"
      onPress={() => api.toast.show('Receipt sent successfully!')}
    />
  );
});
```


