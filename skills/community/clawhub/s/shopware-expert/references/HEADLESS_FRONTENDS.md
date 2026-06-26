# HEADLESS FRONTENDS

Compiled excerpts from the Shopware Developer Documentation snapshot. Prefer live docs at [developer.shopware.com](https://developer.shopware.com/) when in doubt.

---

## Documentation assistant (QA)
**Source:** [frontends/ai/search.md](https://developer.shopware.com/frontends/ai/search.md)  
# Documentation assistant (QA)

Please **ask your question** and I will do my best to guide you to the correct resource. I use **AI** to score the best answer in our documentation.

If my answer is correct, please give a **thumbs up** to help improve the **language model**. We are currently using the `deepset/roberta-base-squad2` language model, but it can be switched to `openai` or other models supported by Hugging Face.

Try it out, just ask a question:

---

---

## BEST PRACTICES
**Source:** [frontends/best-practices.md](https://developer.shopware.com/frontends/best-practices.md)  
# BEST PRACTICES

---

---

## Deployment
**Source:** [frontends/best-practices/deployment.md](https://developer.shopware.com/frontends/best-practices/deployment.md)  
# Deployment

Shopware Frontends can be deployed in multiple ways, depending on the setup you are using. Most likely you will be using either a static hosting service or a server with a Node.js runtime. The different options and approaches are described below.

## Static hosting

This option is the easiest to set up and will work best for small or static projects. With a static hosting, your site will be built once during the deployment and afterwards delivered as static HTML pages with Javascript for dynamic elements.

The biggest advantage is that there is no additional server needed to do the rendering of your page and it scales very well\*, because your entire site is made of files on a server.

### Single page application (SPA)

In a single page application the server sends the application as static HTML and Javascript. After receiving the data, the browser will parse the Javascript and the page becomes interactive. It requires an API at runtime to fetch data like products, categories or a navigation.

Drawbacks of this approach are that it is heavy on the API and that initial page loads take the longest, because the browser has to parse the Javascript before anything can be displayed to the user. That delay has a negative impact on UX and search engine scoring.

### Server-side generation (SSG)

In server-side generation your site's pages - products pages, category pages, content pages - are generated once at build time. Afterwards the site will be delivered as static HTML and Javascript to the client.

The main advantage of SSG is, that browsing activities are not affected by your API backend, because it's used to display products, categories etc. - in most cases it is the approach giving the most potential for good performance. For dynamic operations like cart, user account or checkout the API will still be called.

\*The main drawback is that any change of products, categories, etc. will invalidate the generated pages and require you to re-generate them, so this approach is not ideal for sites that change often.

### Popular static hosting services

There are various services that provide static hosting, such as

* [Vercel](https://vercel.com/)
* [Netlify](https://www.netlify.com/)
* [Amazon S3](https://aws.amazon.com/s3/)
* and many more

Each services has its own way of deploying your applications and you should refer to their documentation for more information.

## Dynamic hosting (SSR)

The dynamic hosting option requires a Node.js server to run your application. For every fresh page request, the application is rendered on the server in a process called SSR (server-side rendering) and then delivered as static HTML and Javascript to the client. Afterwards, the static page will become interactive after the browser parsed all Javascript in a process called hydration and it continues working like a [SPA](#single-page-application-spa).

It is the most dynamic and versatile approach and requires no invalidation and is generally better for SEO, since the page is visible to the user right away. For most eCommerce projects it is the best fit, bringing together the SEO and UX benefits of SSG and the actuality of SPA.

Drawbacks are that it requires API access at runtime for all operations. These calls are made by the Node.js server and introduce an additional round-trip (Node server>API>Node server) before the page can be fully rendered and sent to the client. For that reason, it is generally advised to optimize your network infrastructure with regard to that round trip in order to get the most out of the SSR approach. Obviously

### Popular dynamic hosting services

* [Vercel](https://vercel.com/)
* [Heroku](https://www.heroku.com/)

## Prepare you application

The final goal is always deployment, no less equal than development itself.

There are many good tools available that help you build and deploy your application.

### Nitro

The great example is [Nitro](https://github.com/unjs/nitro), which is used by default by [Nuxt 3](https://nuxt.com/docs/guide/concepts/server-engine) as its server engine, but can be also used broadly in the whole JS ecosystem.

Moreover, besides the frameworks or libraries that you can work with using Nitro, there are many ready-to-use platforms providers (called *presets*) which help you to build & deploy (docs included) your app with almost zero config:

* azure
* cloudflare\_pages
* netlify
* stormkit
* vercel

Nitro provides also really great examples for other well known platforms (full static, or those serving SSR) and the list you can find [here](https://nitro.unjs.io/deploy).

## Good Practices

Here are the collected rules that may be followed to avoid most common issues during the deployment.

### Automate the processes

Avoid doing manual work like running tests, building, release. The more work is being done automatically, there is less space for human mistake. Many platforms offer built-in CI/CD servers which help to achieve it for you codebase.

### Use Continuous Integration (CI) tools

Always test your application. Test the build, do the static analyze, and whatever that can detect a potential source of problem in production build.

### Use multiple environments

Test several configurations at the same time, like different nodejs version, or the upcoming release branch with upgraded dependencies. That concerns also the API your application relies on.

### Prepare a checklist

Be prepared, be organized before every roll-out. Deployment checklist shouldn't be to way complicated, but should describe the flow of the work in order to get the deployment done.

---

---

## Error Handling
**Source:** [frontends/best-practices/error-handling.md](https://developer.shopware.com/frontends/best-practices/error-handling.md)  
# Error Handling

:::warning
Deprecated. This doc is based on the old API client. Use The [new API client](../packages/api-client) instead.
:::

How to for error handling in different areas and different cases with examples.

---

---

## Images
**Source:** [frontends/best-practices/images.md](https://developer.shopware.com/frontends/best-practices/images.md)  
# Images

Best practices for images.

## Optimization

Let's have a look on some good practices to help display images efficiently.

### Image format & Compression

Compression is the first step, relatively easy to achieve in order to reduce loading time by reducing file size, thus saving network traffic for images.

**WebP** is a new format for images, developed by Google, in order to add an alternative for *png* images, but with lossy compression, enhanced by some new techniques allowing to compress with different level selectively within the same image. As it's become fully supported in all modern browsers - it can be recommended.

You can check how much you can save by using `webp` format instead of others raster-images formats. See how can it help you on [Thumbor](http://thumborize.globo.com/?url=https://frontends-demo.vercel.app).

:::info Test different formats
There are many image formats, which have different advantages, depending on images purposes. Probably you don't need `webp` files for vector images. Sometimes, when the high image quality is important, using lossy formats may not be a good idea. It always depends on the use case.

There are many tools to check different image formats, but the great one is [Squoosh](https://squoosh.app/) which allows you to experiment with images interactively:

![Squoosh screenshot](../.assets/squoosh-app.png)
:::

### Images hosting on CDN + Image processor

Using Content Delivery Network platforms (CDN) helps to reduce network distance, by serving resources from the closest server for an user.

Although it can be a standalone service, some platforms serves images with additional option of resizing on the fly, or being more general: processing the images, depending on provided query parameter, like `?width=400px`. Thanks to this, `<img>` element is more readable.

```html
<img
  src="https://images.swfrontends.com/frontends-unsplash.png?width=400px"
  srcset="
    https://images.swfrontends.com/frontends-unsplash.png?width=400px 320w,
    https://images.swfrontends.com/frontends-unsplash.png?width=800px 720w
  "
/>
```

Examples of open source image processors which can be used as a middleware to serve processed images:

* [thumbor](https://www.thumbor.org/)
* [lovell/sharp](https://github.com/lovell/sharp)
* [imgproxy/imgproxy](https://github.com/imgproxy/imgproxy)

## Responsive images

Utilize [srcset](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img#attr-srcset) attribute for `<img>` elements in order to load the image in size what is actually needed at the moment.
Decide what metric (pixel ratio - DPR or width) is more appropriate for your users when defining breakpoints.

Also, consider using `sizes` attribute which will indicate what image size is best to choose - if your images occupy less than 100% of viewport. The value can be defined in percentage of viewport width (`sizes="80vw"`) or fixed value (`sizes="600px"`) regardless the device size. Read more at [mdn web docs](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img#attr-sizes).

```html
<img
  sizes="50vw"
  srcset="
    frontends-header-xs.webp  600w,
    rontends-header-md.webp  1200w,
    rontends-header-xl.webp  2000w
  "
  src="rontends-header-xs.webp"
  alt="..."
/>
<!-- src fallback is set to be mobile first -->
```

If you application serves many image formats and there is a significant part of users with older browsers, you can use [picture](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/picture) element.

In this example, browser will decide which image format is available to serve, otherwise the `<img>` will be picked as a fallback.

```html
<picture>
  <source
    type="image/avif"
    srcset="
      https://images.swfrontends.com/frontends-unsplash-320.avif 320w,
      https://images.swfrontends.com/frontends-unsplash-720.avif 720w
    "
  />
  <source
    type="image/webp"
    srcset="
      https://images.swfrontends.com/frontends-unsplash-320.webp 320w,
      https://images.swfrontends.com/frontends-unsplash-720.webp 720w
    "
  />
  <img
    src="https://images.swfrontends.com/frontends-unsplash.png"
    alt="Logo Shopware Frontends"
  />
</picture>
```

## Reduce Cumulative Layout Shift (CLS)

When Images occupy a big amount of space on web pages, they are a common cause of high [CLS](https://web.dev/cls/) scores.

* Always set `width` and `hight` attributes for your `<img>` elements, with values matching size of image source. So even if they are being loaded, the space of layout will be filled out.
* Define CSS style to override `<img>` attributes (there is a moment when image element is available in DOM, and CSS is not loaded yet):
  ```css
  img {
    max-width: 100%;
    height: auto;
  }
  ```
* Try to use low-quality placeholders (based on svg, for example) to avoid having empty blank spaces within the layout:

## Speed up Largest Contentful Paint

"[LCP](https://web.dev/lcp/) element has an image on around three quarters of pages" says the result of [Web research](https://almanac.httparchive.org/en/2021/media#images). Moreover, on 70.6% mobile pages, LCP element has an image. On desktops, the rate is even bigger: 79.4%. So we can assume, that bad LCP scores are based on low image performance.

* Never use `loading="lazy"` on `<img>` elements if they are part of what an user see first on they viewport (consider editing the attributes for CMS elements in Shopware Experiences).
* Utilize `fetchpriority="high"` on `<img>` also tells the browser, that the asset (LCP resource is prioritized) is important and should be taken care of as fast as possible.

## Resources

Collection of useful blog posts and articles about performance related to images.

* https://web.dev/learn/images/
* https://austingil.com/better-html-images/
* https://www.smashingmagazine.com/2023/01/optimizing-image-element-lcp/
* https://web.dev/top-cwv-2023/

---

---

## Performance
**Source:** [frontends/best-practices/performance.md](https://developer.shopware.com/frontends/best-practices/performance.md)  
# Performance

## Lighthouse performance checklist

Below is a list of items that you can use to quickly audit the performance of your application. This list is not exhaustive, but rather a starting point.

:::warning
Please remember that the Lighthouse score should be checked only on the production build.
:::

### Performance

* Images have appropriate resolution
* Images are in `WebP` format
* Third part code is loaded asynchronously
* Images are lazy loaded
* All custom event listeners are destroyed with their components

### Accessibility

* All images are described by `alt` attribute
* Contrast is correct
* `aria-label` are added to HTML tags

### Best Practices

* `https` connection is used
* Page follows a semantic HTML structure

### SEO

* `robots.txt` is added
* All pages have metadata (title, description, tags)

---

---

## Testing
**Source:** [frontends/best-practices/testing.md](https://developer.shopware.com/frontends/best-practices/testing.md)  
# Testing

We splitted the section into different parts to cover the most important aspects of testing.

* [E2E Testing with Playwright](./testing/e2e-testing.md)
* [A/B Testing](./testing/ab-testing.md)
* [Accessibility Testing](./testing/accessibility-testing.md)

---

---

## A/B Testing practices
**Source:** [frontends/best-practices/testing/ab-testing.md](https://developer.shopware.com/frontends/best-practices/testing/ab-testing.md)  
# A/B Testing practices

A/B testing is a method of comparing two versions of a webpage or app against each other to determine which one performs better. It is a way to compare two versions of a single variable, typically by testing a subject's response to variant A against variant B, and determining which of the two variants is more effective.

## Providers

There are planty of A/B testing providers available. Here are some of the most popular ones:

* [AB Tasty](https://www.abtasty.com/)
* [Optimizely](https://www.optimizely.com/)
* [VWO](https://vwo.com/)
* [Split.io](https://www.split.io/)
* [Kameleoon](https://www.kameleoon.com/)
* [PostHog](https://posthog.com/)

You need to pick the right one for your needs. Depending on the size of your company, the complexity of your tests, and the budget you have available. There are generous free plans available in that list, so in most cases, you can start with that.

## Best practices

### Start with a hypothesis

Before you start your A/B test, you should have a clear hypothesis. What do you want to test? What do you expect to happen? What is the goal of the test?

### Split components dynamically to avoid enlagred bundle sizes

You should split your components dynamically. This will help you to avoid enlarged bundle sizes. You can use the `import()` function to load components on demand. Example:

```ts
const myExperimentFlag = useABTesting("myExperimentFlag");

const MyComponent = myExperimentFlag ? import("./MyComponentVariantA") : import("./MyComponentVariantB");

// later in the template

<MyComponent />
```

### Testing smaller components

While dynamic splitting is very effective to avoid loading too much code to the client's browser, this would not be efficient with some very small components. For example if you only want to test a different button variant, then in most cases it could be done in a single component. Example:

```ts
const myExperimentFlag = useABTesting("myExperimentFlag");

// later in the template

<button :class={{
  "bg-color-red": myExperimentFlag,
  "bg-color-blue": !myExperimentFlag
}}> Click me </button>

// or more slear split using v-show/v-if

<button v-if="myExperimentFlag" class="bg-color-red"> Click me </button>
<button v-else class="bg-color-blue"> Click me please! </button>
```

### Clean your code

After the test is finished, you should clean your code. Remove all the unused code and components. This will help you to keep your codebase clean and maintainable. Not removing unused variants will cost you many maintenance problems, especially while refactoring your application.

---

---

## Axe Core
**Source:** [frontends/best-practices/testing/accessibility-testing.md](https://developer.shopware.com/frontends/best-practices/testing/accessibility-testing.md)  
# Axe Core

Axe Core is an open-source accessibility testing engine used for automated web testing. You can use it as an extension for Chrome or Firefox to scan web pages for accessibility issues and also implement it in the e2e tests used (e.g. in Playwright) and automate accessibility checks in continuous integration environments.

## Axe Core

Playwright and e2e tests can also be used to test application for many types of accessibility issues.
By default, axe checks against a wide variety of accessibility rules, but rules can be defined easily at the test level

```js
const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze();
```

## Example accessibility tests

Using the ax core library is practically no different from typical work with playwright. You can create tests for each page from scratch or integrate accessibility scans and assertions into your existing test cases.

```js
import { test, expect } from '@playwright/test';
import AxeBuilder from "@axe-core/playwright";

//Uses normal Playwright Test syntax to define a test case
test('Check accessibility violations', async ({ page }) => {
//Uses normal Playwright syntax to navigate to the page under test
  await page.goto('https://example.com');
//Awaits AxeBuilder.analyze() to run the accessibility scan against the page
  const accessibilityScanResults = await new AxeBuilder({ page }).analyze();
  //Uses normal Playwright Test assertions to verify that there are no violations in the returned scan results
      expect(accessibilityScanResults.violations).toEqual([]);
```

You can also run tests for a specific part of the page

```js
test('navigation menu should not have automatically detectable accessibility violations', async ({
  page,
}) => {
  await page.goto('https://your-site.com/');

  await page.getByRole('button', { name: 'Navigation Menu' }).click();

  // It is important to waitFor() the page to be in the desired
  // state *before* running analyze(). Otherwise, axe might not
  // find all the elements your test expects it to scan.
  await page.locator('#navigation-menu-flyout').waitFor();

  const accessibilityScanResults = await new AxeBuilder({ page })
      .include('#navigation-menu-flyout')
      .analyze();

  expect(accessibilityScanResults.violations).toEqual([]);
});
```

---

---

## E2E Testing with Playwright
**Source:** [frontends/best-practices/testing/e2e-testing.md](https://developer.shopware.com/frontends/best-practices/testing/e2e-testing.md)  
# E2E Testing with Playwright

## Page object best practice

* Use `data-testid` selectors to locate your UI elements
* Use an unambiguous name for your page object class
* The page class should only contain methods for interacting with the HTML page or component
* The page class should only contain properties and methods
* Don't create an assertion on the page object level
* A page object doesn't have to be an entire HTML page and can be a small component

## Waits best practice

Avoiding hard waits in Playwright.

```js
await page.waitFor(1000); // hard wait for 1000ms
```

Never use hard waits in production tests. However, you can use them for testing or debugging purposes.
Replace them with playwright methods like `waitForNavigation`, `waitForLoadState`, `waitForSelector`.

### Pages

Follow the PageObjects pattern for the suite template to encapsulate each internal page structure and responsibilities inside its highly cohesive class file. This allows you to define a new page object for each page as per your needs.

Don't confuse the page objects you create with actual pages in the application. Pages are a lightweight concept of a view, a set of cohesive elements living under a known browser location.

## Page objects

Each page must contain a cohesive set of locators and actions.

### Structure

## Structure e2e-tests

|- page-objects # Set of pages for the applications
|- tests # Set of tests
|- utils # Predefined helpers and their factory functions

For a page object to be as readable as possible, you must follow the below structure:

```js
import { expect, Locator, Page } from "@playwright/test";

export class LoginForm {
  // Define selectors
  readonly page: Page;
  readonly usernameInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly closeLoginPopup: Locator

  // Init selectors using constructor
  constructor(page: Page) {
    this.page = page;
    this.usernameInput = page.locator("[data-testid='login-email-input']");
    this.passwordInput = page.locator("[data-testid='login-password-input']");
    this.submitButton = page.locator("[data-testid='login-submit-button']");
    this.closeLoginPopup =page.locator('text=close')
  }

  // Define login page methods
  async login(username: string, password: string) {
    await this.usernameInput.type(username);
    await this.passwordInput.type(password);
    await this.submitButton.click();
  }
};
```

## data-testid attribute

You are recommended to add the custom data attributes data-testid for:

* Active elements (buttons, links, forms etc.)
* Passive elements (essential elements like price, product options etc.)

The main benefit of adding those attributes is that you can easily get elements in E2E tests.

### Naming convention

```
data-testid="{scope}-{name}-{type}"
data-testid="header-search-input"
```

**Scope** - indicates where the element is placed. For example - page
**Name** - defines the element. For example - input name
**Type** - indicates the type of element. For example - input

### Usage in tests

```js
import { test, expect } from "@playwright/test";

test("failed login", async ({ page }) => {
  await page.goto("/");

  await Promise.all([
    page.waitForNavigation(),
    page.click("[data-testid='header-sign-in-link']"),
  ]);

  await page
    .locator("[data-testid='login-email-input']")
    .fill("test@shopware.com");
  await page
    .locator("[data-testid='login-password-input']")
    .fill("Password123!@#");

  await Promise.all([await page.click("[data-testid='login-submit-button']")]);

  await expect(
    page.locator("data-testid='login-errors-container']"),
  ).toBeVisible();
});
```

---

---

## frontends/examples.md
**Source:** [frontends/examples.md](https://developer.shopware.com/frontends/examples.md)  
:::warning
Our examples have moved, please follow the link below
:::

---

---

## FRAMEWORK
**Source:** [frontends/framework.md](https://developer.shopware.com/frontends/framework.md)  
# FRAMEWORK

---

---

## Composables
**Source:** [frontends/framework/composables.md](https://developer.shopware.com/frontends/framework/composables.md)  
# Composables

The section on composables describes context composables, shared composables and how to overwrite composables.

---

---

## Context Composables
**Source:** [frontends/framework/composables/context-composables.md](https://developer.shopware.com/frontends/framework/composables/context-composables.md)  
# Context Composables

Composables are containers for reusable logic and state. While some composables are entirely stateless and just provide a set of functions, there are so-called context composables that can share state between parent and child components without the need for property drilling or usage of `provide` and `inject`.

Context boundaries follow the component tree hierarchy, so that a child component can access the state of its parent component without explicit references.

## Why to use context composables

Context composables allow for a more granular way of sharing state between components.

Instead of doing this:

```vue
<!-- Product.vue -->
<script setup lang="ts">
const product = searchProduct();
</script>
<template>
  <div>
    <ProductConfigurator :product="product" />
  </div>
</template>
```

```vue
<!-- ProductConfigurator.vue -->
<script setup lang="ts">
const props = defineProps<{
  product: Product;
}>();
</script>
<template>
  <div>
    <ProductPrice :product="product" />
  </div>
</template>
```

```vue
<!-- ProductPrice.vue -->
<script setup lang="ts">
const props = defineProps<{
  product: Product;
}>();
</script>
<template>
  <div>
    {{ getFormattedPrice(product.price) }}
  </div>
</template>
```

A parent component calls the composable and provides context - all child components can feed off that context. Have a look at the example below:

![wireframe of an application showing multiple context composables](../../.assets/wireframe-proposal-01.png)

In the example above, there are multiple usages of the `useProduct` composable and one usage of the `useNavigationContext` composable. All calls create a new context boundary (indicated by the coloured boxes). Within their context boundaries (meaning further down the component tree), the child components can access the state of the parent component.

For example, the call

```js
const { product } = useProduct(detailProduct);
```

creates a new context boundary for all underlying components. The `ProductConfigurator` component can access the `product` state without having to pass it down as a prop.

### Navigation Context (blue)

This context boundary is usually global to the whole application, unless you have explicit requirements for sub-routes within your pages.
Just call the following to access navigation context information from almost anywhere in your application:

```js
const { routeName, foreignKey } = useNavigationContext();
```

### Detail page (red)

The detail page component calls the composable with the `detailProduct` parameter and creates a new context boundary (red). Every child component of the detail page can now call

```js
const { product } = useProduct();
```

and access data from the correct product, such as title, description or price.

### Quickview (green)

In the quickview component, a new context boundary (green) is created by calling the composable with the `quickViewProduct` parameter.

Again, all children components of the quickview components have access without passing the product context explicitly. You can even use the same components as in the product detail page.

## Using context composables

Context composables are used just as normal composables. However, they have one additional catch. They can be instantiated with and without a `context` parameter. If the `context` parameter is set, a new context boundary is created, which means all child components are able to retrieve the same state. Correspondingly, if the `context` parameter is omitted, the context state is resolved from the closest parent context boundary.

:::info
Internally, context composables use the `provide` and `inject` mechanism from Vue 3.
:::

### Example

See a simple example with the context composable `useCategory` below.

First, fetch a category from the API and store it in the context state by passing it to the `useCategory` composable.

```vue
<!-- Category.vue -->

<script setup>
const { path } = useRoute();
const { search } = useCategorySearch();

const categoryResponse = await search(path);

// Setting the context and creating a context boundary
const { category } = useCategory(categoryResponse);
</script>

<template>
  <CategoryHeader />
</template>
```

Then, use the `useCategory` composable in the child component to retrieve the category from the context state.

```vue
<!-- CategoryHeader.vue -->

<script setup>
// Resolving the category from the closest parent context boundary
const { category } = useCategory();
</script>

<template>
  <h1>{{ category.name }}</h1>
  <p>{{ category.description }}</p>
</template>
```

---

---

## Overwrite and extend composables
**Source:** [frontends/framework/composables/overwriting-composables.md](https://developer.shopware.com/frontends/framework/composables/overwriting-composables.md)  
# Overwrite and extend composables

:::warning Join the discussion
Currently we have open RFC for this topic - join the discussion and share your thoughts - https://github.com/shopware/frontends/discussions/44
:::

Designed architecture allows you to replace and overwrite almost any part of the composables package in order to achieve highly customized solution.

In order to extend or overwrite the logic of the composables, you need to create a new file in the `composables` folder with the same name as the one you want to overwrite. For example, if you want to overwrite the logic of the `useAddToCart` composable, you need to create a new file called `useAddToCart.ts` in the `composables` folder.

```ts
// composables/useAddToCart.ts
import { useAddToCart as coreUseAddToCart } from "@shopware/composables";

export function useAddToCart(product: Ref<Product>) {
  const coreFunctionality = coreUseAddToCart(product);
  return {
    ...coreFunctionality,
  };
}
```

this is our base for extending and overwriting the logic of the `useAddToCart` composable.
At this point you can:

* extend logic of the composable
* extend logic of specific method
* overwrite the whole method
* replace the whole composable

:::warning Overwriting the whole composable
If you want to overwrite the whole composable, you need to make sure that you are the same interface as the original one or that you are completly aware of the consequences of the change. This can lead to breaking changes in your application so be careful.
:::

## Extending the logic of the composable

Let's say we want additional method to be available in the `useAddToCart` composable.
This case is not problematic, as the existing API is not changing. Let's try to have additional computed property which returns quantity of the product in the cart.

```ts
// composables/useAddToCart.ts
import { useAddToCart as coreUseAddToCart } from "@shopware/composables";

export function useAddToCart(product: Ref<Product>) {
  const coreFunctionality = coreUseAddToCart(product);
  const { cartItems } = useCart();

  const getQuantityInCart = computed(() => {
    return cartItems.value.find(
      (item: LineItem) => item.referencedId === product.value?.id,
    )?.quantity;
  });

  return {
    ...coreFunctionality,
    getQuantityInCart,
  };
}
```

You can achieve the same effect by creating a new composable as well and write additional logic, this might be a better solution if you want to keep the logic of the original composable untouched.

## Extending the logic of the specific method

This might be especially useful for high customization. Let's say we want to add analytics after the product is added to the cart.

```ts
// composables/useAddToCart.ts
import { useAddToCart as coreUseAddToCart } from "@shopware/composables";

export function useAddToCart(product: Ref<Product>) {
  const coreFunctionality = coreUseAddToCart(product);

  const addToCart = async (quantity: number) => {
    const result = await coreFunctionality.addToCart(quantity);
    // here we can call analytics, we have access to product, added quantity and result of the core addToCart method
    return result; // going back to the original method, result can also be modified by you
  };

  return {
    ...coreFunctionality,
    addToCart,
  };
}
```

That kind of customisation is extremly powerful and can be used to achieve almost any kind of customisation. It replaces the need od interceprots for methods as you have full control over the place where intercepted logic is called and what are the results of that logic.

## Overwriting the whole method

Sometimes you want to completly replace original logic, maybe you want to call a different API endpoint or need another order of the things.

```ts
// composables/useAddToCart.ts
import { useAddToCart as coreUseAddToCart } from "@shopware/composables";

export function useAddToCart(product: Ref<Product>) {
  const coreFunctionality = coreUseAddToCart(product);

  const addToCart = async (quantity: number) => {
    // your own logic withoout core functionality. Mind to return the same interface as the original one and change it only if you know what you're doing
  };

  return {
    ...coreFunctionality,
    addToCart,
  };
}
```

## Replacing the whole composable

If you need to replace whole composable logic you can do this by not invoking core composable at all. This is the most radical way of customisation as you need to make sure that you are returning the same interface as the original one. A lot of things might break if you are not aware of the consequences of the change.

```ts
// composables/useAddToCart.ts

export function useAddToCart(product: Ref<Product>) {
  // your own implementation
}
```

---

---

## Shared composables
**Source:** [frontends/framework/composables/shared-composables.md](https://developer.shopware.com/frontends/framework/composables/shared-composables.md)  
# Shared composables

Using composable in a component can be imagined as copying all the code from that into that component, without the actual need to do so. This way we can reuse logic in a clean way. We need to remember, that every computed property/state is then replicated, so if we have multiple components using specific composable - we duplicate that in memory.

Sometimes we want only one instance of a specific composable to be shared between all components. This is where shared composables come in. They are just regular composables, but there is always one instance in the system.

Example:
`useCart` is composable which contains cart information, like items inside, count or totalPrice details. We want to use it in multiple components, but we don't want to duplicate the data in memory. This is a perfect use case for shared composable.

## How do I know which one is shared and what should I do with that?

We're adding information that the composable is shared into the description with a link to this documentation page.
There is no need to do anything with this information. The only difference is in [overwriting](./overwriting-composables.html)

## Overwrite/extend shared composable

Typically you extend shared composable by using the same core composable. In the case of shared composables you need to take `useXXFunction` to extend it.

Example:

```ts
import { useCartFunction } from "@shopware/composables";
import { createSharedComposable } from "@vueuse/core";

function myUseCart() {
  const coreCartFunctions = useCartFunction();

  // extend the core functions
  const myCustomFunction = () => {
    // do something
  };

  return {
    ...coreCartFunctions,
    myCustomFunction,
  };
}

export const useCart = createSharedComposable(myUseCart); // or skip `createSharedComposable` if you don't want it to be a shared composable anymore
```

---

---

## Internal Structure
**Source:** [frontends/framework/internal-structure.md](https://developer.shopware.com/frontends/framework/internal-structure.md)  
# Internal Structure

The internal structure of Shopware Frontends is designed to provide flexibility, reusability and abstraction. Shopware Frontends is a framework that is build with JavaScript and TypeScript.

Some of its components are based on Vue.js and Nuxt.js. The framework is designed to be used mostly with Vue.js and Nuxt.js, but it is not limited to these technologies. You can use it with any other JavaScript framework or library.

This section deals with the different packages and their abstractions. It is sorted by reusability / abstraction level from high to low and shows the main dependencies of each component respectively.

## api-client

The API client provides a common interface to access the Shopware API. It can be used standalone in any JavaScript project.

## helpers

Helpers are functions that can be used for formatting, data manipulation and other stateless tasks within any JavaScript project. They are not tied to any other components.

## composables

The composables are a set of Vue.js composition functions that can be used in any Vue.js project. They provide state management, UI logic and data fetching and are the base for all guides in our [building section](../getting-started/).

## nuxt-module

The Nuxt 3 module allows you to set up a Nuxt 3 project with Shopware Frontends. It provides the [composables](#composables) and [api-client](#api-client) packages.

If you want to use these packages with a different Vue.js framework, see the guide for using Shopware Frontends in a [custom project](../getting-started/templates/custom-vue-project).

## cms-base

The CMS base is a Nuxt module that provides an implementation of all CMS components in Shopware [based on utility-classes](./styling.html) using unocss/Tailwind.css syntax. It is useful for projects that want to use the CMS components but design their own layout.

Head to our [Content Pages](../getting-started/cms/content-pages#use-the-cms-base-package) guide to learn more.

## Templates & Examples

Our GitHub repository also contains reference implementations for different frameworks and use cases. You can find them in the [templates](https://github.com/shopware/frontends/tree/main/templates) and [examples](https://github.com/shopware/frontends/tree/main/examples) folders. These examples are not directly part of the framework, but can be useful for learning how to use Shopware Frontends.

---

---

## Environment requirements
**Source:** [frontends/framework/requirements.md](https://developer.shopware.com/frontends/framework/requirements.md)  
# Environment requirements

Shopware Frontends requires a Node.js runtime environment. Besides that, for development you can use your favourite package manager.

## Shopware API

Shopware Frontends does not differ between provisioning of the Shopware API. Both, cloud and self-managed Shopware 6 instances are supported.

Every development instance / setup template is pre-configured with a public demo API. That way you don't have to set up a Shopware instance yourself.

## IDE

For an ideal development experience, we recommend using [VSCode](https://code.visualstudio.com/download) with the following extensions

* Vue Language Features (`Vue.volar`)
* Biome - Code Formatter and linter (`biomejs.biome`)
* TS and JS Language Features (`vscode.typescript-language-features`)

If you are using the `demo-store-template`, we also recommend the following extension

* UnoCSS (`antfu.unocss`)

## Node.js

Shopware Frontends requires a Node.js runtime environment.

Supported versions:

* **v22.x** LTS
* **v20.x** - maintenance
* **v18.x** - maintenance

:::tip
Use [Node Version Manager](https://github.com/nvm-sh/nvm) to manage a Node.js version locally.

"Supported" signifies the framework is developed, run, and tested on mentioned versions.
:::

## Package manager

Supported managers:

* pnpm - recommended
* npm
* yarn

:::info
`npm` package manager is available out of the box with Node.js installed. Other managers need manual installation.
:::

---

---

## Shopping Experiences
**Source:** [frontends/framework/shopping-experiences.md](https://developer.shopware.com/frontends/framework/shopping-experiences.md)  
# Shopping Experiences

This guide will discuss how to use and customize [Shopping Experiences](https://docs.shopware.com/en/shopware-6-en/content/ShoppingExperiences) in your Shopware Frontends project.

## How it works

Shopping Experiences are implemented as a dedicated package that you can install in your project.

If your project is based on the [Demo Store Template](../getting-started/templates/demo-store-template), that package is already installed. If you are using a custom template, follow the instructions in [Install the package](#install-the-package) first.

## Install the package

The `@shopware/cms-base-layer` package provides an implementation of all default CMS components in Shopware's Shopping Experiences. It uses Tailwind.css syntax for styling. You will now use it to render a content page.

First of all, add the package to your project:

```bash
npm install -D @shopware/cms-base-layer
```

Next, you need to register all components in its `components/public` directory globally. How to do it, depends on your environment. However, the package also comes with a nuxt module which does that for you. So in any Nuxt application, you can just add if to the `modules` section of your Nuxt config file:

```diff
/* nuxt.config.ts */

export default defineNuxtConfig({
  /* ... */
- modules: [/* ... */, "@shopware/nuxt-module"],
+ modules: [/* ... */, "@shopware/cms-base-layer"],
});
```

## How to build Pages, Elements and Blocks?

---

---

## Styling
**Source:** [frontends/framework/styling.md](https://developer.shopware.com/frontends/framework/styling.md)  
# Styling

Shopware Frontends [Demo Store Template](../getting-started/templates/demo-store-template) applies a utility-first styling approach based on [unocss](https://github.com/unocss/unocss). You can either follow this approach or use [custom styling](#use-a-custom-css-framework).

## Utility CSS

Unocss supports multiple CSS frameworks, including

* Tailwind CSS
* Windy CSS
* Bootstrap

This means you can use utilities like `mt-10` or `bg-gray-100` in all of your components along with styles like `col-md-3`. Note, that the [Demo Store Template](../getting-started/templates/demo-store-template) applies only Tailwind CSS syntax and does not mix any of the approaches.

Unocss will analyse your components and generate a CSS file that contains only the utility classes used in the implementation.

As an introduction, we recommend reading the [Utility-First Fundamentals](https://tailwindcss.com/docs/utility-first) article from Tailwind CSS.

When building layouts in a utility-first manner, you should follow some fundamental rules.

### Reusability

There will be cases when you would like to create a class instead of using a long list of utility classes for multiple components. In that case, consider creating a reusable component instead:

```html
<img
  class="object-cover w-12 h-12 rounded-full border-3 border-white mr--6"
  src="https://picsum.photos/id/18/100/100"
/>
<img
  class="object-cover w-12 h-12 rounded-full border-3 border-white mr--6"
  src="https://picsum.photos/id/12/200/200"
/>
<img
  class="object-cover w-12 h-12 rounded-full border-3 border-white mr--6"
  src="https://picsum.photos/id/29/200/200"
/>
```

will become

```vue
<!-- ImageCircle.vue -->
<script setup>
defineProps(["imageSrc"]);
</script>

<template>
  <img
    class="object-cover w-12 h-12 rounded-full border-3 border-white mr--6"
    :src="imageSrc"
  />
</template>
```

```vue
<!--- ImageContainer.vue -->
<script setup>
defineProps(['images'])
</script>

<template>
    <ImageCircle v-for="image in images" :imageSrc="image">
</template>
```

### Responsive Design

Start your layout from the smallest viewport and work your way up. There are built in prefixes for the viewport sizes:

```html
<div class="grid md:grid-cols-2">
  <!-- some html -->
</div>
```

### State Variants

Similar to viewport breakpoints, you can also use state variants with prefixes:

```html
<div class="group flex justify-center">
  <input
    class="hover:shadow-xl border-2 border-indigo rounded-md p-3 shadow-md"
    type="text"
  />
</div>
```

## Use a custom CSS Framework

If you want to use a different CSS framework or fully custom styling, it's recommended to use the [Blank Template](../getting-started/templates/blank-template) as a starting point. It has no pre-installed CSS framework and you can install you own.

### Remove unocss from the Demo Store Template

However, it's also possible to remove unocss from the [Demo Store Template](../getting-started/templates/demo-store-template). This might be applicable when you want to make use of the component structure and logic that's already provided by the template.

Remove the `unocss` dependency from the `package.json` file

```diff
/* package.json */

-    "@unocss/nuxt": "66.5.6",
```

Remove the unocss imports, build modules and configuration from the `nuxt.config.js` file

```diff
/* nuxt.config.js */

 import { defineNuxtConfig } from "nuxt";
-import transformerDirective from "@unocss/transformer-directives";
-import presetIcons from "@unocss/preset-icons";

 export default defineNuxtConfig({
   },
   buildModules: [
     "@vueuse/nuxt",
-    "@unocss/nuxt",
     "@shopware/nuxt-module"
   ],
   vueuse: {
     ssrHandlers: true,
   },
-  unocss: {
-    uno: true, // enabled `@unocss/preset-uno`
-    icons: true, // enabled `@unocss/preset-icons`
-    attributify: true, // enabled `@unocss/preset-attributify`,
-    ...
-  },
```

Eventually, run `pnpm install` to remove the unocss dependency from your installation.

---

---

## BUILDING
**Source:** [frontends/getting-started.md](https://developer.shopware.com/frontends/getting-started.md)  
# BUILDING

---

---

## B2B modules
**Source:** [frontends/getting-started/b2b.md](https://developer.shopware.com/frontends/getting-started/b2b.md)  
# B2B modules

Collection of B2B elements and documentation how to use them.

---

---

## B2B Quote Management
**Source:** [frontends/getting-started/b2b/quote-management.md](https://developer.shopware.com/frontends/getting-started/b2b/quote-management.md)  
# B2B Quote Management

In this chapter you will learn how to

* Request new quote
* Fetch a list of quote and display detail
* Decline quote
* Request change in quote
* Change payment or shipping in quote
* Create a order from a quote

## Quick reference

* [useB2bQuoteManagement](../../packages/composables/useB2bQuoteManagement) is a composable used for a quote management

## Request new quote

The "Request New Quote" feature allows B2B users to request a custom quote for their current basket. This is particularly useful for large or complex orders where standard pricing may not apply, or special discounts may be negotiated.

This feature enhances the B2B shopping experience by providing flexibility in pricing and order customization. It also allows for direct communication between the buyer and seller, facilitating better negotiation and understanding of needs.

:::warning
Cart cannot be empty
:::

```vue
<script setup lang="ts">
import { ref } from "vue";
import { useCart, useB2bQuoteManagement } from "@shopware/composables";
const { cartItems } = useCart();
const { requestQuote } = useB2bQuoteManagement();
const comment = ref("");
const handleRequestQuote = async () => {
  await requestQuote(comment.value);
};
</script>
<template>
  <textarea v-model="comment"> </textarea>
  <button :disabled="cartItems.length <= 0" @click="handleRequestQuote">
    Request quote
  </button>
</template>
```

## Fetch a list of quote and display detail

This feature allows users to retrieve a list of all their requested quotes or quotes created by the admin.

```vue
<script setup lang="ts">
import { ref, onBeforeMount } from "vue";
import { useB2bQuoteManagement } from "@shopware/composables";
const quotesList = ref([]);
const { getQuoteList } = useB2bQuoteManagement();
onBeforeMount(async () => {
  quotesList.value = await getQuoteList();
});
</script>
<template>
  <table>
    <thead>
      <tr>
        <th>Quote #</th>
        <th>Created at</th>
        <th>Valid until</th>
        <th>Grand total</th>
        <th>Status</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="quote in quotesList" :key="quote.id">
        <td>{{ quote.quoteNumber }}</td>
        <td>{{ quote.createdAt }}</td>
        <td>{{ quote.expirationDate }}</td>
        <td>
          {{ quote.price.totalPrice }}
        </td>
        <td>
          {{ quote.stateMachineState.translated.name }}
        </td>
      </tr>
    </tbody>
  </table>
</template>
```

## Decline quote

The "Decline Quote" feature provides users with the ability to reject a quote that doesn't meet their requirements or expectations. By declining a quote, users can communicate their dissatisfaction with the proposed terms, prompting the sales team to review and potentially adjust the quote to better meet the user's needs. This feature ensures that the negotiation process is interactive and that the final agreement is satisfactory to both parties.

```vue
<script setup lang="ts">
import { ref } from "vue";
import { useB2bQuoteManagement } from "@shopware/composables";
const declineComment = ref("");
const quote = ref("example-id");
const { declineQuote } = useB2bQuoteManagement();
const handleDecline = async () => {
  declineQuote(quote.value.id, declineComment.value);
  declineComment.value = "";
};
</script>
<template>
  <form @submit.prevent="handleDecline">
    <textarea v-model="declineComment"> </textarea>
    <button>Decline</button>
  </form>
</template>
```

## Request change in quote

The "Request Change in Quote" feature empowers users to actively participate in the negotiation process. If a quote doesn't meet their expectations or requirements, users can request specific changes to the quote. This could involve adjustments to pricing, quantities, delivery terms, or product specifications. By requesting a change, users can ensure that the final agreement is tailored to their needs, fostering a more collaborative and satisfactory business relationship.

```vue
<script setup lang="ts">
import { ref } from "vue";
import { useB2bQuoteManagement } from "@shopware/composables";
const quote = ref("example-id");
const changeRequest = ref("");
const { requestChangeQuote } = useB2bQuoteManagement();
const handleChangeRequest = async () => {
  requestChangeQuote(quote.value.id, changeRequest.value);
  changeRequest.value = "";
};
</script>
<template>
  <form @submit.prevent="handleChangeRequest">
    <textarea v-model="changeRequest"> </textarea>
    <button type="submit">Send</button>
  </form>
</template>
```

## Change payment or shipping in quote

The "Change Payment or Shipping in Quote" feature provides users with the flexibility to modify the payment method or shipping details in a quote.

```vue
<script setup lang="ts">
import { ref } from "vue";
import { useB2bQuoteManagement } from "@shopware/composables";
const quote = ref("example-id");
const { changeShippingMethod, changePaymentMethod } = useB2bQuoteManagement();
changeShippingMethod(quote.value.id, "example-shipping-id");
changePaymentMethod(quote.value.id, "example-payment-id");
</script>
```

## Create an order from a quote

The "Create an Order from a Quote" feature allows users to seamlessly convert a negotiated quote into a formal order. Once a quote has been reviewed and agreed upon, users can use this feature to initiate the ordering process directly from the quote.

```vue
<script setup lang="ts">
import { ref } from "vue";
import { useB2bQuoteManagement } from "@shopware/composables";
const quote = ref("example-id");
const comment = ref("");
const { createOrderFromQuote } = useB2bQuoteManagement();
const handleCreateOrder = async () => {
  await createOrderFromQuote(quote.value.id, comment.value);
};
</script>
<template>
  <template>
    <form @submit.prevent="handleCreateOrder">
      <textarea v-model="comment"> </textarea>
      <button type="submit">Create order</button>
    </form>
  </template>
</template>
```

---

---

## CMS
**Source:** [frontends/getting-started/cms.md](https://developer.shopware.com/frontends/getting-started/cms.md)  
# CMS

Everything related to CMS ([Shopping Experiences](../../framework/shopping-experiences.html)).






---

---

## Create content pages
**Source:** [frontends/getting-started/cms/content-pages.md](https://developer.shopware.com/frontends/getting-started/cms/content-pages.md)  
# Create content pages

In this chapter you will learn how to display content pages with data from Shopware's own CMS. It is based on the mechanism of routing and fetching page content described in the [previous chapter](../routing). The case of building fully custom components from scratch will be covered as well. Specifically, you will learn how to

* Render a content page using the cms-base package
* Render a content page using custom components

## Use the cms-base package

Using the cms-base package, you don't have to implement any CMS components by yourself. You can start with a working implementation but add and override single components as you need. It requires a couple dependencies for styling and validation purposes to work properly.

### Install the package

Depending on which template you are using you need to install the package first.\
See [install the package](../../framework/shopping-experiences#install-the-package).

### Render the page

Now, you can import all components from the `@shopware/cms-base-layer` package and use them in your templates. The most straightforward way to render a page is to use the `CmsPage` component. It takes a `content` prop and resolves all subordinate sections, blocks and elements automatically. Put the following code in your catch-all component that also handles the [routing logic](../routing#resolve-a-route-to-a-page).

```vue-html
<CmsPage v-if="data" :content="data.cmsPage"/>
```

:::warning This will only work
if you followed the previous chapter on [routing](../routing). The `data` value in this example is a reactive reference to either a product, a category or a landing page response. If you are not sure how to get the data otherwise, check that chapter and see how the data is fetched.
:::

### Customize components

The `cms-base` package has an opinionated style of components and is based on Tailwind.css. If you want to override components or add custom ones, you can build them right into your project or import them as a separate package.

## Use custom components

If you use custom components and not the cms-base package, you have to ensure the correct rendering of the page. You also need to re-create all components that the Shopware CMS uses. For the creation of custom components - such as elements or blocks, you can follow the instructions given in [Shopping Experiences](../../framework/shopping-experiences) and benefit from typehinting and the `useCms*` composables.

---

---

## Create Blocks (CMS)
**Source:** [frontends/getting-started/cms/create-blocks.md](https://developer.shopware.com/frontends/getting-started/cms/create-blocks.md)  
# Create Blocks (CMS)

Make sure, you've created a new file as described in [customize components](customize-components.html#create-new-files).

Next, import the correct type for your block and use it to define the `content` property:

```vue
<!-- components/cms/CmsBlockImageThreeColumn.vue -->
<script setup lang="ts">
import { CmsBlockImageThreeColumn } from "@shopware/composables";

const props = defineProps<{
  content: CmsBlockImageThreeColumn;
}>();
</script>
```

## Slots

:::info Only for `cms-base` package
Also here, if you are not using the `cms-base` package, you have to come up with your own implementation of a generic component that handles the slot resolution. In that case, please ignore the mentions of `CmsGenericElement`.
:::

Since blocks are usually layouts, they have slots which can be filled with dynamic content - CMS elements. Since blocks are flexible, the specific type of the element is not known in advance.

For that reason, there's a generic element `CmsGenericElement` which can be placed in every slot. It receives the `content` configuration as its only prop.

Let's build the `image-three-column` block, which has three slots - `left`, `center` and `right`.

```vue{4-15}
<!-- components/cms/CmsBlockImageThreeColumn.vue -->
<template>
    <div class="grid grid-cols-3">
        <CmsGenericElement
            :content="props.content.slots.filter(
                (slot) => slot.slot === 'left')
            " />
        <CmsGenericElement
            :content="props.content.slots.filter(
                (slot) => slot.slot === 'center')
            " />
        <CmsGenericElement
            :content="props.content.slots.filter(
                (slot) => slot.slot === 'right')
            " />
    </div>
</template>
```

That works, but it's quite repetiive and hard to read. So we can use another composable `useCmsBlock` which makes our lives way easier.

```vue{8,10-12,16-18}
<script setup lang="ts">
import { CmsBlockImageThreeColumn } from "@shopware/composables";

const props = defineProps<{
  content: CmsBlockImageThreeColumn;
}>();

const { getSlotContent } = useCmsBlock(props.content);

const leftContent = getSlotContent("left");
const rightContent = getSlotContent("right");
const centerContent = getSlotContent("center");
</script>
<template>
    <div class="grid grid-cols-3">
        <CmsGenericElement :content="leftContent" />
        <CmsGenericElement :content="centerContent" />
        <CmsGenericElement :content="rightContent" />
    </div>
</template>
```

No you can go ahead and override blocks and elements step by step.

---

---

## Create Elements (CMS)
**Source:** [frontends/getting-started/cms/create-elements.md](https://developer.shopware.com/frontends/getting-started/cms/create-elements.md)  
# Create Elements (CMS)

Start with importing the correct element type from the `@shopware/composables` package and using it in the `defineProps` method to define the type of your `content` property:

```vue
<!-- components/cms/CmsElementImage.vue -->

<script setup lang="ts">
import { CmsElementImage } from "@shopware/composables";

const props = defineProps<{
  content: CmsElementImage;
}>();
</script>
```

Now, you can use `props.content` to access all properties of the element in your template.

```vue{8}
<!-- components/cms/CmsElementImage.vue -->

<script setup lang="ts">
// see above
</script>

<template>
    <img :src="props.content.data.media.url" />
</template>
```

However, for some elements the configuration can be quite complex, so there are composables to give you a hand:

```vue{10-14,18-20}
<!-- components/cms/CmsElementImage.vue -->

<script setup lang="ts">
import { CmsElementImage, useCmsElementImage } from "@shopware/composables";

const props = defineProps<{
    content: CmsElementImage
}>();

const {
    containerStyle, // padding, background-color etc.
    displayMode, // cover, contain, stretch etc.
    imageAttrs, // automatically resolves src, alt and srcset attributes
} = useCmsElementImage(props.content);
</script>

<template>
    <div :style="containerStyle">
        <img v-bind="imageAttrs"/>
    </div>
</template>
```

---

---

## Custom Elements (CMS)
**Source:** [frontends/getting-started/cms/custom-elements.md](https://developer.shopware.com/frontends/getting-started/cms/custom-elements.md)  
# Custom Elements (CMS)

:::warning
This tutorial is a continuation of example from the backend part. That can be found [here](https://developer.shopware.com/docs/guides/plugins/plugins/content/cms/add-cms-element.html)
:::

All custom CMS elements created in the backend require corresponding implementations in the frontend application.

The CMS package utilizes the [resolveComponent](https://vuejs.org/api/render-function#resolvecomponent) method from Vue to identify the component returned by the backend API.
Therefore, the only requirement is to globally register the component with the appropriate name.

## Registration

### Demo store

The demo store utilizes Nuxt 3, which by default registers all components globally. For optimal application structure, we recommend adding the components to the `/components/cms` directory.

### Vue apps

[Global registration](https://vuejs.org/guide/components/registration#global-registration) in Vue apps

```ts
import CmsBlockCustomBlock from "./components/cms/CmsElementDailymotion.vue";

app.component("CmsElementDailymotion", CmsBlockCustomBlock);
```

## Naming

The component is searched in the global component register by its name.

[Resolving component in CMS package](https://github.com/shopware/frontends/blob/main/packages/composables/src/index.ts#L74)

```js
const componentNameToResolve = pascalCase(`Cms-${type}-${componentName}`);
const resolvedComponent = resolveComponent(componentNameToResolve);
```

Component name must be the same as it was registered in the backed.

```ts{3}
Shopware.Service('cmsService').registerCmsElement({
    ...
    name: 'dailymotion',
    ...
});
```

Lets create new component `components/cms/element/CmsElementDailymotion.vue`

```vue
// components/cms/element/CmsElementDailymotion.vue
<script setup lang="ts">
import type { Schemas } from "#showpare";

type CmsElementDailymotion = Schemas["CmsSlot"] & {
  type: "dailymotion" | typeof String;
  slot: typeof String;
  config: CmsElementDailymotionConfig;
  translated: {
    config: CmsElementDailymotionConfig;
  };
};

type CmsElementDailymotionConfig = {
  dailyUrl: {
    value: string;
    source: "static";
  };
};
const props = defineProps<{
  content: CmsElementDailymotion;
}>();
</script>

<template>
  <div>
    <h2>Element!</h2>
    <div class="sw-cms-el-dailymotion">
      <div class="sw-cms-el-dailymotion-iframe-wrapper">
        <iframe
          frameborder="0"
          type="text/html"
          width="100%"
          height="100%"
          :src="props.content.config.dailyUrl.value"
        >
        </iframe>
      </div>
    </div>
  </div>
</template>
```

### Reading config

Component settings are passed via props. The declared `defaultConfig` can be accessed through the `props.content.config` property.

The following is an example of how to convert the backend registration config to a TypeScript type.

```ts{4-9}
Shopware.Service('cmsService').registerCmsElement({
  ...
    name: 'dailymotion',
    defaultConfig: {
        dailyUrl: {
            source: 'static',
            value: ''
        }
    }
  ...
});
```

```ts
type CmsElementDailymotionConfig = {
  dailyUrl: {
    value: string;
    source: "static";
  };
};
```

---

---

## Customize Components
**Source:** [frontends/getting-started/cms/customize-components.md](https://developer.shopware.com/frontends/getting-started/cms/customize-components.md)  
# Customize Components

:::info Only for `cms-base` package
The directory structure is only relevant, if you want to customize the components of the `cms-base` package. If you are using a custom template, you can place components where you want, because you handle their resolution by yourself. In that case skip to [Create Elements](./create-elements).
:::

### Create new files

In order to customize a component, you need to override it. The process is the same regardless what type of component you want to override

* Sections
* Blocks
* Elements

To do so, you need to create a file with the same name as the component in the `components` directory or wherever according to the project's configuration.

```json
demo-store/
├─ components/
|  ├─ cms/
|  ├─ ├─ CmsBlockImageHighlightRow.vue
```

Now the CMS module will automatically resolve that file based on the name and you can start writing your component.

## Internal components

❗**Internal components are not a part of public API. Once overwritten you need to track the changes on your own.**

There is also a possibility to override the internal components, shared between public blocks and elements, the ones starting with `Sw` prefix, like [SwSlider.vue](https://github.com/shopware/frontends/blob/main/packages/cms-base-layer/app/components/SwSlider.vue) or [SwProductCard.vue](https://github.com/shopware/frontends/blob/main/packages/cms-base-layer/app/components/SwProductCard.vue).

### Additional Example

---

---

## Multiple content management systems (CMS)
**Source:** [frontends/getting-started/cms/multiple-cms.md](https://developer.shopware.com/frontends/getting-started/cms/multiple-cms.md)  
# Multiple content management systems (CMS)

Add another [CMS system](../../resources/integrations/cms/), but still use the Shopware Shopping Experiences as a fallback.

This documentation guides users through the process of incorporating an additional CMS instance and use it seamlessly with the Shopware Shopping Experiences.

:::warning
This example is written for the vue-demo-store template
:::

## Adding middleware

All you need to do is adding a middleware injection to the main routing resolver file.

`templates/vue-demo-store/pages/[...all].vue`

```ts{16-23,46-54,61-66}
import { resolveComponent } from "vue";
import type { Ref } from "vue";
import { pascalCase } from "scule";
import {
  useNavigationContext,
  useNavigationSearch,
} from "@shopware/composables";
import type { Schemas } from "#shopware";
const { clearBreadcrumbs } = useBreadcrumbs();

const NOT_FOUND_COMPONENT = "errors/RoutingNotFound";
const { resolvePath } = useNavigationSearch();
const route = useRoute();
const { locale } = useI18n();
const routePath = route.path.replace(`${locale.value}`, "").replace("//", "/");

/**
 * Load CMS resolver if exists
 */
let cmsPageRendererComponent: VNode | null = null;
const cmsPageRenderer = inject<((path: string) => VNode | null) | null>(
  "pageRenderMiddlewares",
  null,
);

const { data: seoResult } = await useAsyncData(
  "cmsResponse" + routePath,
  async () => {
    // For client links if the history state contains seo url information we can omit the api call
    if (import.meta.client) {
      if (history.state?.routeName) {
        return {
          routeName: history.state?.routeName,
          foreignKey: history.state?.foreignKey,
        };
      }
    }
    const seoUrl = await resolvePath(routePath);
    return seoUrl;
  },
);

const { routeName, foreignKey } = useNavigationContext(
  seoResult as Ref<Schemas['SeoUrl']>,
);

/**
 * If there is no Shopware CMS component and an additional CMS
 * resolver is available, fetch content
 */
const componentName = routeName.value;
const path = routePath.substring(1);
if (!componentName && cmsPageRenderer) {
  cmsPageRendererComponent = await cmsPageRenderer(path);
}

onBeforeRouteLeave(() => {
  clearBreadcrumbs();
});

function render() {
    /**
     * Render additional CMS component if exists
     */
    if (cmsPageRendererComponent) {
        return cmsPageRendererComponent;
    }

    if (!componentName)
        return h("div", h(resolveComponent(pascalCase(NOT_FOUND_COMPONENT))));

    const componentNameToResolve = pascalCase(componentName as string);
    const cmsPageView = routeName && resolveComponent(componentNameToResolve);
    if (cmsPageView) {
        if (cmsPageView === componentNameToResolve)
        return h("div", {}, "Problem resolving component: " + componentName);
        return h("div", h(cmsPageView, { navigationId: foreignKey.value }));
    }
    return h("div", {}, "Loading...");
}
```

You see that the `cmsPageRendererComponent` is returned before the regular `cmsPageView` is resolved. But only if the `cmsPageRendererComponent` is not null and **no** routeName aka componentName is found. Further details can be found in the comments in the code above.

Also, you can find a complete example here at [Strapi CMS Integration](../../resources/integrations/cms/strapi).

---

---

## Overwrite CMS blocks in Nuxt 3 APP (Nuxt Layer way)
**Source:** [frontends/getting-started/cms/overwriting-cms.md](https://developer.shopware.com/frontends/getting-started/cms/overwriting-cms.md)  
# Overwrite CMS blocks in Nuxt 3 APP (Nuxt Layer way)

To override CMS blocks in the Nuxt 3 app, create a `.vue` file with the cms block name in the components directory.
Because of auto importing, CMS component import will be overwritten by the new file with the same name.

More about auto imports can be found [here](https://nuxt.com/docs/guide/concepts/auto-imports)

## Example how to overwrite the cms block product listing

We have this cms element **component** from **cms-base package**:\
`packages/cms-base-layer/app/components/public/cms/block/CmsBlockProductListing.vue`

If we want to create our own product listing **component** in **demo-store** the correct place would be:
`templates/vue-demo-store/components/cms/block/CmsBlockProductListing.vue`

:::tip HINT 💡

❗**Internal components are not a part of public API. Once overwritten you need to track the changes on your own.**
:::

### Resolving folder structure

**Nuxt** is resolving names by folder structure, so if you have:\
`/components/public/some/name.vue`\
then component name is **PublicSomeName**.

You can repeat folder structure in name like:\
`/components/cms/Name.vue`\
`/components/cms/CmsName.vue`

These are the same components resolving as **CmsName**. 💡

### Internal components

As example: some components use `SwSharedPrice.vue` to show prices with corresponding currency for products in many places like product card, product details page and so on. In order to change the way how the price is displayed consistently - create a one component with a name `SwSharedPrice.vue` and that's it. The new component will be used everywhere where is "imported" (autoimported actually).

### Generic CMS components

Generic components are responsible for resolving each CMS element

* [CmsGenericElement.vue](https://github.com/shopware/frontends/blob/main/packages/cms-base-layer/app/components/public/cms/CmsGenericElement.vue)
* [CmsGenericBlock.vue](https://github.com/shopware/frontends/blob/main/packages/cms-base-layer/app/components/public/cms/CmsGenericBlock.vue)

---

---

## E-Commerce
**Source:** [frontends/getting-started/e-commerce.md](https://developer.shopware.com/frontends/getting-started/e-commerce.md)  
# E-Commerce

Collection of specific E-Commerce elements and documentation how to use them.







---

---

## Work with the cart
**Source:** [frontends/getting-started/e-commerce/cart.md](https://developer.shopware.com/frontends/getting-started/e-commerce/cart.md)  
# Work with the cart

In this chapter you will learn how to

* Create a cart
* Add products and promotions to a cart
* Remove items from the cart
* Display the cart

## Create a cart

You don't need to create a cart explicitly. Upon calling `refreshCart`, a new cart will be created if it doesn't exist yet. A new cart contains no items.

:::tip
Internally, Shopware's Store API uses the `sw-context-token` header parameter to identify the current user and their cart.
:::

```ts
const { refreshCart } = useCart();

await refreshCart();
```

The `refreshCart` method is called automatically after any action within the cart (add product, remove item, etc.), but can be used explicitly if there was some request made outside the composables, for the same session context.

In a real application, we encourage you to use the `refreshCart` method in client-side calls only (for example using the `onMounted` nuxt hook) - unless required otherwise. It's useful to keep an eye on your browser's network tab to see if there are too many requests to the cart endpoint.

## Add items to the cart

The `useCart` composable also offers methods to add items to the cart, such as

* Products
* Promotions

### Add product to the cart

You can use the `useAddToCart` composable to add a product to the cart:

```vue
<script setup lang="ts">
const product: Product = {
  id: "7b5b97bd48454979b14f21c8ef38ce08",
};
const { addProduct, quantity, getAvailableStock } = useAddToCart({
  product,
});
</script>
<template>
  Only {{ getAvailableStock }} in stock<br />
  <input v-model="quantity" type="number" />
  <button @click="addToCart()">Add to cart</button>
</template>
```

### Add promotion to the cart

The process of adding a promotions code is just as straightforward as adding a product to the cart. You can use the `appliedPromotionCodes` field to receive a list of all applied promotion codes.

```vue
<script setup lang="ts">
const promotionCode = ref<string>();
const { addPromotionCode, appliedPromotionCodes } = useCart();
</script>
<template>
  <input type="text" v-model="promotionCode" />
  <button @click="addPromotionCode(promotionCode)">Apply promotion code</button>
</template>
```

Promitions will appear as a line item in the cart with a negative price.

## Display the cart items

Once the products are added to the cart, the can be accessed through the `cartItems` reference. In a similar fashion, you can access other information like `totalPrice`, `subtotal` or `cartErrors` which can occur in the case of invalid cart configurations.

```vue
<script setup lang="ts">
const { cartItems, totalPrice, count } = useCart();
</script>
<template>
  Items in the cart: {{ count }}<br />
  Total price: {{ totalPrice }}<br />

  <ul>
    <li v-for="cartItem in cartItems" :id="cartItem.id">
      {{ cartItem.label }} - {{ cartItem.price.totalPrice }}
    </li>
  </ul>
</template>
```

Find a table of commonly used properties of cart items below:

| Property       | Description                                                                                                                           |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `id`           | The unique identifier of the cart item                                                                                                |
| `referencedId` | Depends on `item.type``product`: ID of the referenced product`promotion`: Promotion code if applicable                        |
| `label`        | The label of the cart item                                                                                                            |
| `price`        | `totalPrice`: The total price of the cart item (can be negative)`unitPrice`: Price per unit[More about Prices](./prices.html) |
| `quantity`     | The quantity of units of the cart item                                                                                                |
| `type`         | The type of the cart item - `product` or `promotion`                                                                                  |
| `cover`        | The cover image of the cart item                                                                                                      |

## Change the quantity of a cart item

The `changeProductQuantity` method can be used to change the quantity of a cart item.

```ts
const { changeProductQuantity } = useCart();

const cartItem: LineItem = {
  id: "7b5b97bd48454979b14f21c8ef38ce08",
  quantity: 2,
};

changeProductQuantity(cartItem);
```

## Remove a cart item

You can remove items from the cart using the `useCart` or the `useCartItem` composables:

```ts
const { removeItem } = useCart();

await removeItem({ id: "7b5b97bd48454979b14f21c8ef38ce08" });
```

In case of the `useCartItem` composable, you pass the item identifier when calling the composable, but not when calling the `removeItem` method.

```ts
const { cartItem } = toRefs(props);
const { removeItem } = useCartItem(cartItem);

await removeItem();
```

---

---

## Create a checkout
**Source:** [frontends/getting-started/e-commerce/checkout.md](https://developer.shopware.com/frontends/getting-started/e-commerce/checkout.md)  
# Create a checkout

In this chapter you will learn how to

* Fetch and display payment and shipping information
* Create an order summary (totals, taxes)
* Place an order

## Shipping and payment information

:::warning
Please remember that payment and shipping methods shouldn't be cached.
It is important to refresh data before displaying it.
:::

Before fetching, ensure the cart is not empty by using `refreshCart` in the `useCart` composable.

**Get shipping methods**

```ts
const { getShippingMethods } = useCheckout();

await getShippingMethods();
```

**Display shipping methods**

```vue
<script setup lang="ts">
const {
  shippingMethods,
  setShippingMethod,
  selectedShippingMethod: shippingMethod,
  getShippingMethods,
} = useCheckout();

const selectedShippingMethod = computed({
  get(): string {
    return shippingMethod.value?.id || "";
  },
  async set(shippingMethodId: string) {
    await setShippingMethod({ id: shippingMethodId });
  },
});
</script>
<template>
  <div v-for="shippingMethod in shippingMethods" :key="shippingMethod.id">
    <input
      :id="shippingMethod.id"
      v-model="selectedShippingMethod"
      :value="shippingMethod.id"
      name="shipping-method"
      type="radio"
    />
    <label :for="shippingMethod.id">
      {{ shippingMethod.name }}
    </label>
  </div>
</template>
```

The shipping method position on the list is determined by the `position` field settled on the admin panel. Sorting logic in `useCheckout.ts::getShippingMethods()`

You can also display:

* Shipping delivery time
* Shipping icon
* Shipping description

**Get payment methods**

```ts
const { getPaymentMethods } = useCheckout();

await getPaymentMethods();
```

**Display payment methods**

```vue
<script setup lang="ts">
const {
  paymentMethods,
  selectedPaymentMethod: paymentMethod,
  setPaymentMethod,
} = useCheckout();

const selectedPaymentMethod = computed({
  get(): string {
    return paymentMethod.value?.id || "";
  },
  async set(paymentMethodId: string) {
    await setPaymentMethod({ id: paymentMethodId });
  },
});
</script>
<template>
  <div v-for="paymentMethod in paymentMethods" :key="paymentMethod.id">
    <input
      :id="paymentMethod.id"
      v-model="selectedPaymentMethod"
      :value="paymentMethod.id"
      name="payment-method"
      type="radio"
    />
    <label :for="paymentMethod.id">
      {{ paymentMethod.name }}
    </label>
  </div>
</template>
```

## Personal information

Each guest user has to provide billing data.
Those data will be used to create a standard or temporary account.

```vue
<script setup lang="ts">
const state = reactive({
  salutationId: "",
  firstName: "",
  lastName: "",
  email: "",
  password: "",
  guest: false,
  billingAddress: {
    street: "",
    zipcode: "",
    city: "",
    countryId: "",
  },
});
const { register } = useUser();
const { getCountries } = useCountries();
const { getSalutations } = useSalutations();
const invokeSubmit = () => {
  register(state);
};
</script>
<template>
  <form
    id="checkout-billing-address"
    name="checkout-billing-address"
    method="post"
    @submit.prevent="invokeSubmit"
  >
    <label for="salutation">Salutation</label>
    <select id="salutation" v-model="state.salutationId" name="salutation">
      <option disabled selected value="">Choose salutation...</option>
      <option
        v-for="salutation in getSalutations"
        :key="salutation.id"
        :value="salutation.id"
      >
        {{ salutation.displayName }}
      </option>
    </select>

    <label for="first-name">First name</label>
    <input
      id="first-name"
      v-model="state.firstName"
      type="text"
      name="first-name"
    />

    <label for="last-name">Last name</label>
    <input
      id="last-name"
      v-model="state.lastName"
      type="text"
      name="last-name"
    />

    <input id="create-account" v-model="state.guest" type="checkbox" />
    <label for="create-account">Do not create a customer account.</label>

    <label for="email-address">Email address</label>
    <input
      id="email-address"
      v-model="state.email"
      type="email"
      name="email-address"
    />

    <div v-if="!state.guest">
      <label for="password">Password</label>
      <input
        id="password"
        v-model="state.password"
        type="password"
        name="password"
      />
    </div>

    <label for="street-address">Street address</label>
    <input
      id="street-address"
      v-model="state.billingAddress.street"
      type="text"
      name="street-address"
    />

    <label for="postal-code">ZIP / Postal code</label>
    <input
      id="postal-code"
      v-model="state.billingAddress.zipcode"
      type="text"
      name="postal-code"
    />

    <label for="city">City</label>
    <input
      id="city"
      v-model="state.billingAddress.city"
      type="text"
      name="city"
    />

    <label for="country">Country</label>
    <select
      id="country"
      v-model="state.billingAddress.countryId"
      name="country"
    >
      <option disabled selected value="">Choose country...</option>
      <option
        v-for="country in getCountries"
        :key="country.id"
        :value="country.id"
      >
        {{ country.name }}
      </option>
    </select>

    <button type="submit">Save</button>
  </form>
</template>
```

## Order summary

We can use some helper methods from `useCart` composable to display an order summary and format prices.

Refer to [formatting prices](prices.html) for more information on displaying prices.

:::warning
Totals should **not** be calculated by the frontend. All calculations should be done on the backend side.
:::

```vue
<script setup lang="ts">
const { refreshCart, cartItems, subtotal, totalPrice, shippingTotal } =
  useCart();
const { getFormattedPrice } = usePrice();
await refreshCart();
</script>
<template>
  <div>
    <div>
      <p>Subtotal</p>
      <p>{{ getFormattedPrice(subtotal) }}</p>
    </div>
    <div>
      <p>Shipping estimate</p>
      <p>{{ getFormattedPrice(shippingTotal) }}</p>
    </div>
    <div>
      <p>Order total</p>
      <p>{{ getFormattedPrice(totalPrice) }}</p>
    </div>
  </div>
</template>
```

## Place an order

Placing an order requires

* A valid shipping address
* A selected payment method
* A selected shipping method

After placing an order with the `createOrder` method, the cart is refreshed automatically.

```ts
const { createOrder } = useCheckout();
const { refreshCart } = useCart();

const order = await createOrder();
refreshCart();
```

After creating an order, you can fetch order data. `orderId` is returned by the `createOrder` method from the `useCheckout` composable.
The backend allows fetching orders related only to the current user by checking the session.

```ts
const {
  loadOrderDetails,
  personalDetails,
  billingAddress,
  shippingAddress,
  order,
} = useOrderDetails({ order: { id: orderId } as any });

await loadOrderDetails();
```

---

---

## JSON-LD
**Source:** [frontends/getting-started/e-commerce/json-ld.md](https://developer.shopware.com/frontends/getting-started/e-commerce/json-ld.md)  
# JSON-LD

JSON-LD (JavaScript Object Notation for Linked Data) is a method of encoding Linked Data using JSON. It is a way to create machine-readable data from websites.

In the context of e-commerce, JSON-LD plays a crucial role in improving the visibility of the website to search engines. It allows search engines to understand the content on the website, leading to better SEO (Search Engine Optimization) results.

For example, JSON-LD can be used to provide detailed product information such as price, availability, and review ratings in a structured format that search engines understand. This can lead to rich results or rich snippets, where search engines display more than just the standard search result information, potentially increasing click-through rates and online visibility.

## JSON-LD in Vue demo store

The Vue demonstration store incorporates a specific composable, `useProductJsonLD.ts`, which facilitates the integration of JSON-LD structured data into the product page.

As first parameter composable takes product object.

```ts
useProductJsonLD(productResponse.value.product);
```

### Extending

```ts
useProductJsonLD(productResponse.value.product, {
  brand: {
    "@type": "Brand",
    name: "Test",
  },
});
```

---

---

## Payments
**Source:** [frontends/getting-started/e-commerce/payments.md](https://developer.shopware.com/frontends/getting-started/e-commerce/payments.md)  
# Payments

:::tip Advanced Guide - prior knowledge required
In order to follow this guide properly, we recommend that you get familiar with the payment flow and payment API concepts first.

* [Payments Concept](https://developer.shopware.com/docs/concepts/commerce/checkout-concept/payments) - especially `asynchronous` and `synchronous` chapters.
* [Payment API](https://shopware.stoplight.io/docs/store-api/8218801e50fe5-handling-the-payment)
  :::

## Synchronous Payment

Due to the fact the order can be placed without giving any additional payment information (only allowed data is a `customer comment` and `affiliate code`), the synchronous payment strongly depends on the specific implementation, and that's why it does not affect the way how to deal it in the headless client application.

In this case, the flow looks as follows:

```js
// the cart contains at least one item added
const { createOrder } = useCheckout();

// create an order from the current Cart
const order = await createOrder(/** optional params omitted */);
// order object on success, unhandled rejection otherwise
```

Under the hood, once the order is placed, a [PaymentHandler](https://developer.shopware.com/docs/guides/plugins/plugins/checkout/payment/add-payment-plugin#synchronous-example) is being invoked to process the payment right away:

* Execute the payment logic (may vary for every payment method / provider)
* Change the payment status according the result from previous step

In general, the client side does not have any direct control on the sync payment process.

## Asynchronous Payment

Contrary to the sync flow, the asynchronous payment has more options and thus, more control of the payment process.

This is a better option for those payment providers that would need to pass additional data (like credentials, one time tokens) to complete the payment process.

### External gateway

To give an example, let's say we need to implement a payment method which redirects a customer to the external payment gateway. Depending on success or failure, we need to be redirected to success page in case of payment was done properly, otherwise display an error page to the user in our shop page.

1. Create an order

   ```js{3}
   const { createOrder } = useCheckout();
   const { refreshCart } = useCart();
   // create an order
   const order = await createOrder();
   ```

2. Utilize `useOrderPayment` composable to proceed the payment process once order is placed

   ```js
   // utilize useOrderPayment to proceed on the provided order
   const { paymentUrl, handlePayment, isAsynchronous, state, paymentMethod } =
     useOrderPayment(ref(order));
   ```

3. Initialize a payment handler

   This is the moment, when any additional information can be passed (if a payment extension allows to do so). Payment handler can communicate with an external service to init some additional process, like preparation of external gateway session to process the payment for specific order.

   ```js{6-15}
   // where to redirect an user when payment is done correctly
   const SUCCESS_PAYMENT_URL: string = `${window?.location?.origin}/checkout/success/${orderId}/paid`;
   // go to this page otherwise
   const FAILURE_PAYMENT_URL: string = `${window?.location?.origin}/checkout/success/${orderId}/unpaid`;

   const handlePaymentResponse = await handlePayment(
     SUCCESS_PAYMENT_URL,
     FAILURE_PAYMENT_URL,
     {
       /**
        * here goes additional information required by payment provider
       * can be payment intent token
       */
     }
   )
   ```

   Note that, this is an example, does not show how to create success/failure pages.

4. Do the action on processed payment handler

   If payment provider (shipped via app/plugin/extension) has external payment gateway, you will probably get the URL to go to.

   ```js
   const handlePaymentResponse = await handlePayment();
   /* parameters omitted, see previous point */

   const redirectUrl = handlePaymentResponse?.redirectUrl; // URL or undefined
   ```

   Then you are ready to perform a redirection of an user to the URL in order to finish the payment.
   If succeed, the customer will be redirected back to `SUCCESS_PAYMENT_URL` defined before. Otherwise, `FAILURE_PAYMENT_URL` will be displayed.

### Credit cards

Flow for the credit cards may vary between providers, nevertheless there is a general rule: asynchronous payment flow applies also in this case. Because there is always additional data to be sent, like one time tokens, hash and other security solutions.

Sometimes the external authorization is needed and the external gateway can be used, or a popup to interact with payment provider.

However, if there are no plugin-specific endpoints to interact with, the `handlePayment` method (or `/store-api/handle-payment` endpoint) is always a good choice.

***

See what can be achieved on Express Checkout example for PayPal provider.

## App server integration

When a payment method uses an app server, for example as a [gateway](https://developer.shopware.com/docs/guides/plugins/apps/gateways/checkout/checkout-gateway.html) or middleware, there are some key information needed to identify the client source and the store related to the app itself.

In detached API consumer like headless app, the mentioned information can be obtained by using a [tailored endpoint](https://developer.shopware.com/docs/guides/plugins/apps/clientside-to-app-backend.html):

⚠️ **works only for logged-in customers**

```ts
const { apiClient } = useShopwareContext(); // or use an instance of @shopware/api-client library

const tokenResponse = await apiClient.invoke(
  "generateJWTAppSystemAppServer post /app-system/{name}/generate-token",
  {
    pathParams: {
      name: "MyPaymentApp",
    },
  },
);
```

The response may look like this:

```json
// tokenResponse:
{
  "token": "<example JWT redacted in skill bundle; see Shopware headless docs for shape>",
  "expires": "2024-12-05T14:48:57+00:00",
  "shopId": "QeqxZlmHpJBvfvDP"
}
```

Since the endpoint returns a `jwt` token containing all required data to identify the further requests: `salesChannelId` and `shopId`. Therefore using the `jwt` token should be the only way of authorization, in a request's header. The token is valid for 10 minutes by default.

For example:

```ts
await fetch("https://shopware.mypaymentgateway.com/api/store/card", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    Authorization: `Bearer ${tokenResponse.data?.token}`, // jwt token from the sample code above
  },
  body: JSON.stringify({
    cardId: "card_123",
    tokenId: "some-secret-token_123",
  }),
});
```

---

---

## Work with prices
**Source:** [frontends/getting-started/e-commerce/prices.md](https://developer.shopware.com/frontends/getting-started/e-commerce/prices.md)  
# Work with prices

In this chapter you will learn how

* The price object is structured
* To format and indicate pricing tiers
* Display the correct prices depending on the context
* Use `useProductPrice` composable to handle the most common cases

## Structure of a price

A product in Shopware can have multiple prices. All these prices are defined in a `CalculatedPrice` object, which contains the following fields:

| Field               | Description                                                                                                         |
| ------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **unitPrice**       | The price of a single product item (e.g. only selling toilet rolls in packs of 12)                                  |
| **quantity**        | The quantity of units that the price applies to (usually 1)                                                         |
| **totalPrice**      | The price for one product                                                                                           |
| **calculatedTaxes** | The calculated tax rates and their proportions of the total price                                                   |
| **taxRules**        | Composition of the underlying tax rates                                                                             |
| **referencePrice**  | The price per unit (e.g. 1.99€ per 100g)                                                                            |
| **listPrice**       | The list price of the product                                                                                       |
| **regulationPrice** | Some local laws enforce showing the cheapest price within the last 30 days. This is the price that is used for that |

::: details Example of a `CalculatedPrice` object

```json
{
  "unitPrice": 58,
  "quantity": 1,
  "totalPrice": 58,
  "calculatedTaxes": [
    {
      "tax": 9.26,
      "taxRate": 19,
      "price": 58,
      "apiAlias": "cart_tax_calculated"
    }
  ],
  "taxRules": [
    {
      "taxRate": 19,
      "percentage": 100,
      "apiAlias": "cart_tax_rule"
    }
  ],
  "referencePrice": null,
  "listPrice": {
    "price": 83.3,
    "discount": -25.3,
    "percentage": 30.37,
    "apiAlias": "cart_list_price"
  },
  "regulationPrice": {
    "price": 54,
    "apiAlias": "cart_regulation_price"
  },
  "apiAlias": "calculated_price"
}
```

:::

Each product has at least one `CalculatedPrice` object assigned to it, which can be accessed through `product.calculatedPrice`. It contains the product's default price, which applies when no other prices are defined.

## Display a default price

All prices are passed as floating point numbers, rounded to the decimals which are specified in your stores currency settings. You can use the `getFormattedPrice` helper method to apply the the correct formatting including currency symbol to the price.

```vue{4,16,24}
<script setup>
import { useProductSearch } from '@shopware/composables';

const { getFormattedPrice } = usePrice();
const { search } = useProductSearch();

const { product } = await search('some-product-id');

const { unitPrice, price, tierPrices, isListPrice } = useProductPrice(ref(product));
</script>

<template>
  <div>
    <div>
      <b>{{ product.name }}</b>
    </div>
    <div>
      {{ getFormattedPrice(unitPrice) }}
      <small>
        incl. {{ price.taxRules[0].taxRate }}% tax
      </small>
    </div>
    <div v-if="isListPrice">
      <small>
        <del>
          {{ getFormattedPrice(price.listPrice.price) }}
        </del>
        (-{{ price.listPrice.percentage }}%)
      </small>
    </div>
  </div>
</template>
```

## Pricing tiers and quantity prices

Pricing tiers add one layer of complexity to the pricing model. In Shopware, you can define multiple pricing tiers for a product. Each tier has a quantity and a price.

These pricing tiers are passed through a product's `calculatedPrices` field. The `calculatedPrices` field is an array of `CalculatedPrice` objects sorted by the `quantity` field, which defines the bounds of a pricing range.

```json
[
	{
		"unitPrice": 58,
		"quantity": 5, // quantity from 1 to 5
		"totalPrice": 290,
		/* ... */
	},
	{
		"unitPrice": 50,
		"quantity": 10, // quantity from 6 to 10
		"totalPrice": 500,
		/* ... */
	},
	{
		"unitPrice": 44,
		"quantity": 11, // quantity from 11 to max
		"totalPrice": 484,
		/* ... */
]
```

### Display tier prices

Displaying tier prices is fairly straightforward. You can just iterate through the `calculatedPrices` array and display the quantity limit and price for each tier.

```vue{3,9}
<script setup>
import { useProduct } from "@shopware/composables";

const { getFormattedPrice } = usePrice();
const { product, search } = useProduct();

await search("some-product-id");
</script>

<template>
  <ul>
    <li
      v-for="(tierPrice, index) in product.calculatedPrices"
      :key="tierPrice.quantity">
        <!-- Display "from" or "to" depending on quantity level -->
        {{ index == product.calculatedPrices.length - 1 ? 'from' : 'to' }}
        {{ tierPrice.quantity }} -
        {{ getFormattedPrice(tierPrice.unitPrice) }}
    </li>
  </ul>
</template>
```

### Advanced prices

For more complex pricing models, Shopware also supports advanced prices. The API automatically determines the correct prices for a product based on the user's context, so you don't have to deal with it in your frontend.

## Display the correct price

A product's `calculatedPrice` field is not always the default price since there may be tier prices or a single advanced price defined for the product. Therefore, you should create a switch within your template that differs correctly. You can use the following sudo-code as a starting point:

**if `product.calculatedPrices.length` is more than 1**

**else**

**if `product.calculatedPrices.length` equals 1**

### Full example

See a full example of displaying the default price or pricing tiers depending on the product's pricing structure below:

:::details Click to expand full example

```vue
<script setup>
import { useProduct } from "@shopware/composables";

const { getFormattedPrice } = usePrice();
const { product, search } = useProduct();

await search("some-product-id");

// If there is exactly one pricing tier, use it as the default price.
// Otherwise use the calculatedPrice
const defaultPrice = computed(() => {
  if (product.value?.calculatedPrices?.length === 1) {
    return product.value.calculatedPrices[0];
  }
  return product.value?.calculatedPrice;
});
</script>

<template>
  <ul v-if="product.calculatedPrices.length > 1">
    <!-- Show pricing tiers -->
    <li
      v-for="(tierPrice, index) in product.calculatedPrices"
      :key="tierPrice.quantity"
    >
      <!-- Display "from" or "to" depending on quantity level -->
      {{ index == product.calculatedPrices.length - 1 ? "from" : "to" }}
      {{ tierPrice.quantity }} -
      {{ getFormattedPrice(tierPrice.unitPrice) }}
    </li>
  </ul>

  <div v-else>
    <!-- Show default price -->
    <div>
      {{ getFormattedPrice(defaultPrice.totalPrice) }}
      <small> incl. {{ defaultPrice.taxRules[0].taxRate }}% tax </small>
    </div>
    <div v-if="!!defaultPrice.listPrice">
      <small>
        <del>
          {{ getFormattedPrice(defaultPrice.listPrice.price) }}
        </del>
        (-{{ defaultPrice.listPrice.percentage }}%)
      </small>
    </div>
  </div>
</template>
```

:::

## useProductPrice composable

See dedicated [Composables > useProductPrice](../../packages/composables/useProductPrice) page to check the details of the helper function.

### Product listing

Price for **non-variant** product (also for having tier pricing):

```vue{6}
<script setup lang="ts">
const { totalPrice, displayFrom } = useProductPrice(/** argument omitted - Product object */);
</script>
<template>
<div>
  <span v-if="displayFrom">from</span>{{ totalPrice }} $
</div>
</template>
```

If there is a range of prices available, you can point this out by adding `from` prefix, using the `displayFrom` indicator. The result will be a total price, prefixed by `from` phrase. In this case, unit price is equal to the lowest price available.

In order to ensure if the variant prices are available, you can utilize the `displayVariantsFrom` computed property, that contains the value in current currency:

```vue
<script setup lang="ts">
const { totalPrice, displayVariantsFrom } =
  useProductPrice(/** argument omitted - Product object */);
</script>
<template>
  <div>
    {{ totalPrice }} $
    <span v-if="displayVariantsFrom">
      Variants from {{ displayVariantsFrom }} $
    </span>
  </div>
</template>
```

### Product details page

In this case, there are few options to display:

* Regular price
* Product with list price (kind of discount)
* Tier prices

```ts
const { totalPrice, price, tierPrices, isListPrice } = useProductPrice(product);
const { getFormattedPrice } = usePrice();
```

Regular price, with list price included (in case of manufacturer's suggested retail price):

```vue
<template>
  <div v-if="isListPrice" class="old-price line-through">
    {{ price?.listPrice?.price }} $
    <!-- old price before discount -->
  </div>
  <div v-if="totalPrice">
    {{ totalPrice }} $
    <!-- actual price after discount -->
  </div>
</template>
```

Tier prices presented as a table with range labeled by "to" and "from":

```vue
<template>
  <div>
    <table v-if="tierPrices.length">
      <!-- check if tierPrices array is not empty -->
      <tr v-for="(tierPrice, index) in tierPrices" :key="tierPrice.label">
        <td>
          <span v-if="index < tierPrices.length - 1"> To </span>
          <span v-else> From </span>
          {{ tierPrice.quantity }}
        </td>
        <td>{{ tierPrice.totalPrice }} $</td>
      </tr>
    </table>
    <div v-else>
      <!-- show the regular unit price instead -->
      {{ totalPrice }} $
    </div>
  </div>
</template>
```

### Format price according to current context

There are additional metadata available in the *current* API context. One of them is the *current currency*. In order to display the price together with the currency symbol applied to the current context, use `getFormattedPrice` helper.

```ts
const price = 12.95;
const { getFormattedPrice } = usePrice();
const priceWithCurrency = getFormattedPrice(price);
// output: 12.95 $
```

Thanks to this, the `priceWithCurrency` will have the current currency symbol prefixed or suffixed, according to the configuration.

---

---

## Product Detail Page
**Source:** [frontends/getting-started/e-commerce/product-detail-page.md](https://developer.shopware.com/frontends/getting-started/e-commerce/product-detail-page.md)  
# Product Detail Page

In this chapter you will find how to build static product detail page on short example.

## Get Product data

In order to display information of a product there is a `Product` object needed, containing basic information like:

* Name
* Price
* Description
* Properties
* Images
* ...

To achieve that, you can utilize methods available within `composables` package (or directly via API client package named `@shopware/api-client`). In this example we will use [useProductSearch](../../packages/composables/useProductSearch).

:::info Associations
Keep in mind that not every field, or inner object of the `Product` entity is available automatically.
Some of relations need to be assigned explicitly by [associations](https://shopware.stoplight.io/docs/store-api/cf710bf73d0cd-search-queries#associations). The most common case is `media` object like `product.cover` or `product.media`, which keep additional information about the images: img url, thumbnails and so on.
:::

The `useProductSearch` allows us to `search` in the product's collection:

```ts
import type { Schemas } from "#shopware";
import { useProductSearch } from "@shopware/composables";

const { search } = useProductSearch();

const productResponse = await search("some-product-id", {
  /** parameters omitted */
});

// object that keeps a Product entity
const product: Schemas["Product"] = productResponse.product;
// object with variants configuration
const propertyGroups: Schemas["PropertyGroup"][] = productResponse.configurator;
```

Thanks to this, in the response we are able to access `Product` and `configurator` object. The latter is responsible for keeping related variants information to be used for more complex products.

:::info
If you are using Nuxt.js and a `Product` entity object contains `.cmsPage` property, you can also utilize `@shopware/cms-base-layer` Nuxt 3 module to display the whole Product page designed in Shopping Experiences.
:::

Having source of the data, you can display all you need in your Vue.js template:

```js
import { computed } from "vue";
...
const productName = computed(() => product.value?.translated.name);
const manufacturer = computed(() => product.value?.manufacturer?.name);
const description = computed(() => product.value?.translated.description);
const productNumber = computed(() => product.value?.productNumber);
...
```

## Load additional data asynchronously

Each product can have additional resource loaded asynchronously like Cross-Sells, or Customer Reviews.

Thanks to [useProductAssociations](../../packages/composables/useProductAssociations) composable, you can load it providing the product you are on:

```js
const { loadAssociations, isLoading, productAssociations } =
  useProductAssociations(product, {
    associationContext: "cross-selling",
  });
```

## Full source

## Live demo

---

---

## Create a product listing
**Source:** [frontends/getting-started/e-commerce/product-listing.md](https://developer.shopware.com/frontends/getting-started/e-commerce/product-listing.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Create a product listing

In this chapter you will learn how to

* Initialize the `useListing` composable
* Search for products
* Display products in a listing
* Implement a pagination
* Apply sortings, pagination, and filters
* Use the `helpers` package
* Configure variants presentation for store API

## Listing context

Product listing is a structure related to the predefined areas and it has always the same interface: `ProductListingResult`:

* Response of product-listing endpoint `/store-api/product-listing/{id}`
* Product search result
* Cms Page (via `product-listing` element, nested among other CMS element)

## Listing type and context

Before using the composable, define the type related to the context:

* `categoryListing` for navigation/category/cms pages
* `productSearchListing` for search page

```ts{3}
const { search, getElements } = useListing({
  listingType: "categoryListing",
  categoryId: "dfd52ab937f840fd87e9d24ebf6bd245",
});
```

The `categoryId` is obligatory only if the current page is not a result of using `useCms` composable (generated from Shopping Experiences).

:::info
If the `useListing` composable is used within a CMS Page, `categoryId` is resolved internally.
:::

## Define search criteria

In order to get the expected products, we need to define the search criteria. This criteria is an object of type Search Parameters explained in [documentation of API](https://shopware.stoplight.io/docs/store-api/cf710bf73d0cd-search-queries).

```ts
const { search } = useListing();

search({
  limit: 2, // get only 2 products
  p: 1, // page 1
  includes: {
    // things we actually need in the response for learning purposes
    product: ["id", "name", "cover", "calculatedPrice"],
    product_media: ["media"],
    media: ["url"],
  },
});
```

:::tip
Don't use [`includes`](https://shopware.stoplight.io/docs/store-api/cf710bf73d0cd-search-queries#includes-apialias) parameter if you want to have the whole entity object available in the response.
:::

## Display listing elements

In order to display products of product listing we need to:

* Invoke the `search()` method with a positive result
* Iterate over `getElements` array of elements, where each element has the `Product` type.

```vue{11,22}
<script setup lang="ts">
const { search, getElements } = useListing({
    listingType: "categoryListing",
    categoryId: "dfd52ab937f840fd87e9d24ebf6bd245", // entrypoint to browse
    defaultSearchCriteria: { // set the default criteria
        limit: 3,
        p: 1,
    },
});

search({ // invoke search() method
  includes: { // omit this parameter if you want to use the whole product entity
    product: ["id", "name", "cover", "calculatedPrice", "translated"],
    product_media: ["media"],
    media: ["url", "thumbnails"],
  },
});
</script>
<template>
 <div>
    <!-- iterate the getElements array -->
    <div v-for="product in getElements" :key="product.id">
        {{ product.name }}
        <!-- use other properties of type Product -->
    </div>
 </div>
</template>
```

## Sorting

Available methods of `useListing` to manage sorting order:

* `getSortingOrders()` - returns all available sorting options
* `getCurrentSortingOrder()` - returns the current order, available in the response
* `changeCurrentSortingOrder()` - sets the new order, invoking a `search` method internally

```ts{3-5}
// part of <script setup> section
const {
  getCurrentSortingOrder,
  getSortingOrders,
  changeCurrentSortingOrder,
} = useListing({
  listingType: "categoryListing",
  categoryId: "dfd52ab937f840fd87e9d24ebf6bd245",
  defaultSearchCriteria: {
    limit: 3,
    p: 1,
  },
});
```

Show all available sortings:

```html
<!-- part of <template> -->
<select>
  <option
    v-for="sortingOrder in getSortingOrders"
    :key="sortingOrder.key"
    :value="sortingOrder.key"
    :selected="sortingOrder.key === getCurrentSortingOrder"
  >
    {{ sortingOrder.label }}
  </option>
</select>
```

Refresh the product listing on option's change:

```ts{4-6}
const onOrderChange = (onOrderChangeEvent: Event) => {
    // accept the DOM Event and extract the option's value
    // pass the value to the listing method that triggers the search() method internally
    changeCurrentSortingOrder(
        (onOrderChangeEvent.target as HTMLSelectElement).value
    );
};
```

Add event listener to the `<select>` element:

```html
<select @change="onOrderChange"></select>
```

## Enable adding to the cart

To achieve this, you can use `useCart` composable which expose `addProduct` method, including other useful functions to manage a cart.

```ts
// part of <script setup> section
const { addProduct } = useCart();
```

Utilize the method in a template:

```html
<!-- part of <template> -->
<div>price: {{ product?.calculatedPrice?.unitPrice }} $</div>
<button @click="addProduct(product)">Add to cart</button>
```

Now, when the customer clicks the `Add to cart` button, a proper request is sent to the API. The cart is then refreshed and is up to date in the entire application.

:::tip
Alternative tip - Instead of using `useCart`, you can use `useAddToCart` composable when you create a separate Vue component to keep a single `Product` for product listing. That option would enhance the code organization.
:::

## Add pagination

Pagination is available by using three methods from `useListing` composable:

* `getCurrentPage`
* `changeCurrentPage` - invokes `search()` method internally with the provided number of the page
* `getTotalPagesCount` - calculates the number of available pages depending on products per page parameters (i.e. `limit` in search criteria)

```ts{5-7}
// part of <script setup> section
const {
    search,
    getElements,
    getCurrentPage,
    changeCurrentPage,
    getTotalPagesCount,
    getAvailableFilters
} = useListing({
    listingType: "categoryListing",
    categoryId: "dfd52ab937f840fd87e9d24ebf6bd245",
    defaultSearchCriteria: {
        limit: 3,
        p: 1,
    },
})
```

The implementation can look similar to:

```html
<!-- part of <template> -->
<div>
  <div>Pages: {{ getTotalPagesCount }}</div>
  <button
    v-if="getCurrentPage > 1"
    @click="changeCurrentPage(getCurrentPage - 1)"
  >
    prev
  </button>
  <span> {{ getCurrentPage }} </span>
  <button
    v-if="getCurrentPage < getTotalPagesCount"
    @click="changeCurrentPage(getCurrentPage + 1)"
  >
    next
  </button>
</div>
```

## Using Filters

:::info Available Filters
For more information about filters available in the Store API scope, see [Search Queries > Filter](https://shopware.stoplight.io/docs/store-api/cf710bf73d0cd-search-queries#filter)
:::

Available filters are strictly related to the aggregation's object available in the API response.

Built-in aggregations:

* manufacturer
* price
* rating
* shipping-free
* properties (contain all property entities configured in the admin panel)

### Get list of all available filters

[comment]: # "mermaid source: https://gist.github.com/mkucmus/4002882a229c2a9eb60fe83b84483b2b"

The diagram explains the source of available filters. The API response contains aggregations that are parsed into one interface structure.

In order to get the list of available filters, use the following command:

```ts
const { getAvailableFilters } = useListing(/** parameters omitted */);
```

You can then iterate the filter objects available in the array. The filter object has a [ListingFilter](https://github.com/shopware/frontends/blob/main/packages/types/shopware-6-client/response/ListingResult.d.ts#L19) interface and depending on the `code`, or `displayType`, the handling process can be different. Let us have a closer look at it:

`ListingFilter.code`: **manufacturer**

```vue{15,17}
<script setup lang="ts">
const { getAvailableFilters, getCurrentFilters, setCurrentFilters } = useListing(/** parameters omitted */)

const selectManufacturerAndSearch = (manufacturerId: string) => {
  setCurrentFilters({
    code: "manufacturer",
    value: manufacturerId
  })
}

// element from getAvailableFilters.value
// i.e: getAvailableFilters.value?.find(({code}) => code === "manufacturer")?.[0]
const manufacturerFilter = {
  apiAlias:"manufacturer_aggregation",
  code:"manufacturer",
  label:"manufacturer",
  entities: [
      {
        "extensions": {
          "foreignKeys": {
            "apiAlias": "array_struct"
          }
        },
        "_uniqueIdentifier": "1d39db66fd184de8bdcfbf995197f8ea",
        "versionId": "0fa91ce3e96a4bc2be4bd9ce752c3425",
        "translated": {
          "name": "Boomers Gourmet",
          "description": "Description",
          "customFields": {}
        },
        "createdAt": "2020-08-06T06:26:30.608+00:00",
        "updatedAt": null,
        "mediaId": "ef102a5043174d8b936623b175c8af57",
        "name": "Boomers Gourmet",
        "link": "http://www.gewuerze-boomers.de/",
        "description": "Description",
        "media": null,
        "translations": null,
        "id": "1d39db66fd184de8bdcfbf995197f8ea",
        "customFields": null,
        "apiAlias": "product_manufacturer"
      },]
    { // other manufacturer objects
    }
  ]
}
</script>
<template>
<h3>{{ manufacturerFilter.label }}</h3>
  <div v-for="manufacturer in manufacturerFilter?.entities">
    <input
        type="checkbox"
        :id="`filter-mobile-${manufacturerFilter.code}-${manufacturer.id}`"
        :key="manufacturer.id"
        :name="manufacturerFilter.code"
        @click="selectManufacturerAndSearch(manufacturer.id)"
        :checked="getCurrentFilters['manufacturer']?.includes(manufacturer.id)"
      />
      <label :for="`filter-mobile-${manufacturerFilter.code}-${manufacturer.id}`">
        {{ manufacturer.name }}
      </label>
  </div>

</template>
```

* All available options for the Manufacturer filter are displayed in `v-for` loop. See `entities` property for the same.
* If the `manufacturer.id` is present in `getCurrentFilters['manufacturer']` array, set the option as checked.
* On the `click` event, invoke `setCurrentFilters({code, value})` method with code (`manufacturer`) and value (specific manufacturer ID) provided.

***

`ListingFilter.code`: **properties**

[Properties](https://docs.shopware.com/en/shopware-6-en/products/properties?category=shopware-6-en/catalogues) is a generic type of filter responsible for displaying property entities that can describe a product that is configured on the backend side.

Despite being in the same filter group, every entity of property defined in the admin panel is available separately.

```ts
const ColorFilter: ListingFiler = {
  name: "Color",
  // other properties omitted
  options: [
    {
      id: "yellow-id",
      name: "Yellow",
      // other props omitted
    },
    {
      id: "green-id",
      name: "Gellow",
      // other props omitted
    },
  ],
};
```

### Apply filter value

In order to apply a specific filter you need to be aware of:

* Filter code (see available codes at [ListingFilterCode](https://github.com/shopware/frontends/blob/main/packages/types/shopware-6-client/response/ListingResult.d.ts#L7))
* Value

```vue
<script setup lang="ts">
const { setCurrentFilters } = useListing(/** parameters omitted */);

setCurrentFilters({
  code: "properties",
  value: "some-property-id",
});

// or

setCurrentFilters({
  code: "rating",
  value: 5, // 5 stars rated products
});
</script>
```

### Get list of applied (active) filters or its options

```vue
<script setup lang="ts">
const { getCurrentFilters } = useListing(/** parameters omitted */);
</script>
<template>
  {{ getCurrentFilters.navigationId }}
  <!-- "category-A-ID-1" -->
  {{ getCurrentFilters.manufacturer }}
  <!-- ["manufacturer-A-option-ID-1"] -->
  {{ getCurrentFilters.price }}
  <!-- { min: 0, max: 299 } -->
  {{ getCurrentFilters.rating }}
  <!-- null -->
  {{ getCurrentFilters.["shipping-free"] }}
  <!-- false -->
  {{ getCurrentFilters.properties }}
  <!-- ["property-A-option-ID-1", "property-A-option-ID-2", "property-B-option-ID-1"]-

… **Truncated.** Full document: https://developer.shopware.com/frontends/getting-started/e-commerce/product-listing.md


---

## Features
**Source:** [frontends/getting-started/features.md](https://developer.shopware.com/frontends/getting-started/features.md)  
# Features

Collection of specific Composable Frontends Features and documentation how to use them.





## Shopware Extensions

---

---

## Broadcasting
**Source:** [frontends/getting-started/features/broadcasting.md](https://developer.shopware.com/frontends/getting-started/features/broadcasting.md)  
# Broadcasting

The Broadcast Channel API allows simple communication between browsing contexts (e.g., different tabs, iframes, or workers) on the same origin.

For Vue app we are recommending to use `useBroadcastChannel` from `VueUse` [package](https://vueuse.org/core/useBroadcastChannel/)

## Enabling Broadcasting in Vue-Demo Template

By default, the broadcasting feature is disabled in the Vue-Demo template. To enable broadcasting, follow these steps:

1. Open the `nuxt.config.ts` file in your project.
2. Locate the broadcasting configuration setting.
3. Set the `broadcasting` property to `true` as shown below:

```typescript
export default defineNuxtConfig({
  // Other configurations...
  runtimeConfig: {
    broadcasting: false,
  },
});
```

For more information, please visit the [troubleshooting page](https://frontends.shopware.com/resources/troubleshooting.html#broadcasting-and-bfcache-compatibility)

## Synchronizing changes between tabs

In our demo store template we provide example of usage broadcasting for synchronizing changes between tabs.
We rely on the data fetched by the API client and send them to broadcast channel for synchronization.
This way:

* session data
* cart data
  are synchronized between tabs.

```ts [useBroadcastChannelSync.ts]
import type { Schemas } from "#shopware";

export function useSyncChannel<Entity>(
  name: string,
): [Ref<Entity | undefined>, (data: Entity) => void] {
  const { data, post } = useBroadcastChannel<Entity, Entity>({
    name,
  });

  return [data, post];
}

function isEntity<T extends { apiAlias: string }>(
  data: T,
  apiAlias: T["apiAlias"],
): data is T {
  return data?.apiAlias === apiAlias;
}

/**
 * Sync basic state like session/cart data between tabs
 */
export const useBroadcastChannelSync = createSharedComposable(() => {
  const { apiClient } = useShopwareContext();

  // Synchronize CART data
  const { refreshCart } = useCart();
  const [cartData, notifyCartDataChanged] =
    useSyncChannel<Schemas["Cart"]>("shopware-cart");
  watch([cartData], () => {
    refreshCart(cartData.value);
  });

  // Synchronize SESSION data
  const { setContext } = useSessionContext();
  const [sessionData, notifySessionDataChanged] = useSyncChannel<
    Schemas["SalesChannelContext"]
  >("shopware-session-data");
  watch([sessionData], () => {
    if (sessionData.value) {
      setContext(sessionData.value);
    }
  });

  // Listen for API responses and update the shared state
  apiClient.hook("onSuccessResponse", (response) => {
    // for cart
    if (isEntity<Schemas["Cart"]>(<Schemas["Cart"]>response._data, "cart")) {
      notifyCartDataChanged(<Schemas["Cart"]>response._data);
    }
    // for session data
    else if (
      isEntity<Schemas["SalesChannelContext"]>(
        <Schemas["SalesChannelContext"]>response._data,
        "sales_channel_context",
      )
    ) {
      notifySessionDataChanged(<Schemas["SalesChannelContext"]>response._data);
    }
  });
});
```

---

---

## Custom Products extension
**Source:** [frontends/getting-started/features/custom-products.md](https://developer.shopware.com/frontends/getting-started/features/custom-products.md)  
# Custom Products extension

The example explains how **Custom Products** feature is implemented in `vue-demo-store` template (already done), but also can be used as a guide how to deal with the process in any project.

:::warning Custom Products for Shopware 6 is an extension that is part of the Shopware Rise plan.
[Read more](https://docs.shopware.com/en/shopware-6-en/extensions/customproducts).
:::

## Logic: Composable function

See [the source code](https://github.com/shopware/frontends/blob/main/examples/commercial-customized-products/src/composables/useProductCustomizedProductConfigurator.ts) of `useProductCustomizedProductConfigurator` composable function.

The composable is a main place to keep the logic related to *custom product* features:

* adds TypeScript types
* stores the state
* extracts the custom product's specific data
* exposes method for adding to cart
* serializes the state to be in a correct format for the request's payload (adding to cart)

### Example of usage:

:::warning
Works only if the `useProduct` is fulfilled and the product data is known. Typically on Product Details Page, when the product context is provided.

Visit the \[useProduct]/packages/composables.html#useproduct) reference to see more details.
:::

```ts
// useProductCustomizedProductConfigurator is autoimported
// in vue-demo-store template as it's located in ~/composables
const {
  isActive, // indicates whether product is empowered by Custom Products extension and active
  customizedProduct, // returns the custom product's template data
  state, // state to be used in option selector / forms
  addToCart, // triggers add to cart action (refreshCart() action invoked afterwards)
  handleFileUpload, // uploads an image, then gets mediaId from API and assigns it to the state
} = useProductCustomizedProductConfigurator();
```

## Presentation: Vue component

See [the source code](https://github.com/shopware/frontends/blob/main/examples/commercial-customized-products/src/components/ProductCustomizedProductConfigurator.vue) of the `ProductCustomizedProductConfigurator` Vue component.

The component is responsible for:

* Displaying product options in any type: text field, image upload, select, color select, image select (this one has to be fixed in the core to get the URL's of the images)
* Showing corresponding additional price and currency of an option

## Implementation

Add the mentioned component in a template. For instance in `<ProductStatic/>` for templates that not come from CMS:

```html{9}
<!-- part of templates/vue-demo-store/components/product/ProductStatic.vue -->
<!-- Options -->
<div class="mt-4 lg:mt-0 lg:row-span-3">
  <h2 class="sr-only">Product information</h2>
  <div class="product-variants mt-10">
    <ProductPrice :product="product" />
    <ProductUnits :product="product" class="text-sm" />
    <ProductVariantConfigurator @change="handleVariantChange" />
    <ProductCustomizedProductConfigurator /> <!-- ADDED -->
    <ProductAddToCart :product="product" />
  </div>
</div>
```

Overwrite a logic in `<ProductAddToCart/>` (or any other responsible for adding a product to cart in your template):

```ts{3-6,9-10}
// part of templates/vue-demo-store/components/product/ProductAddToCart.vue;
// the <script setup lang="ts"> section
const {
  addToCart: customizedProductAddToCart,
  isActive: isCustomizedProductActive,
} = useProductCustomizedProductConfigurator();

const addToCartProxy = async () => {
  if (isCustomizedProductActive.value) {
    await customizedProductAddToCart();
  } else {
    await addToCart();
  }
...
```

Used composable function allows to use `addToCart()` method and `isActive` computed property. Both are described in "Example of usage" chapter above.

There was a condition added to use a different method to add to cart a product if the product is enhanced by Custom Product template ([how to set it up](https://docs.shopware.com/en/shopware-6-en/extensions/customproducts)):

* if the product has a Custom Product template, then use `customizedProductAddToCart()` method.
* otherwise, don't change the adding to cart behavior and use the default one

## Known issues

* Missing images for "Image select" option type (reported in the extension repository)
* Missing cover image (aka thumbnail) for Custom Product in the Cart (reported in the extension repository)
* Display selected option for Cart Item ([Issue](https://github.com/shopware/frontends/issues/456) reported)

---

---

## Maintenance mode
**Source:** [frontends/getting-started/features/maintenance-mode.md](https://developer.shopware.com/frontends/getting-started/features/maintenance-mode.md)  
# Maintenance mode

You can activate the maintenance mode of your store by selecting your sales channel and then activating the maintenance mode under Status

## Detecting maintenance mode via API

Maintenance mode is returned as an error from all of the endpoints. We can detect it by using `onResponseError` hook.

```ts
import { isMaintenanceMode } from "@shopware/helpers";

const apiClient = createAPIClient({
  baseURL: shopwareEndpoint,
  accessToken: shopwareAccessToken,
  contextToken: Cookies.get("sw-context-token"),
});

apiClient.hook("onResponseError", (response) => {
  const error = isMaintenanceMode(response._data?.errors ?? []);
  // do proper reaction to maintenance mode
});
```

## Displaying maintenance page

:::warning
This example is for Nuxt 3 apps
:::

### Throwing MAINTENANCE\_MODE error

Every error thrown within the application is automatically caught and the `error.vue` page is displayed.

```ts
import { isMaintenanceMode } from "@shopware/helpers";

apiClient.hook("onResponseError", (response) => {
  const error = isMaintenanceMode(response._data?.errors ?? []);
  if (error) {
    throw createError({
      statusCode: 503,
      statusMessage: "MAINTENANCE_MODE",
    });
  }
});
```

### Displaying maintenance mode page

```vue
// error.vue
<script setup lang="ts">
const props = defineProps<{
  error: {
    statusCode: number;
    statusMessage: string;
    message: string;
  };
}>();

const isMaintenanceMode = computed(() => {
  return props.error.statusMessage === "MAINTENANCE_MODE";
});
</script>

<template>
  <div v-if="isMaintenanceMode">Maintenance Mode Page Content</div>
</template>
```

### IP Allowlisting

This document provides a step-by-step guide on how to add the possibility for allowlisting in the Frontends app.
Allowlisting allows specific users or IP addresses to bypass certain restrictions or maintenance modes, ensuring
they have access to the application even when it is otherwise restricted.

The solution involves adding a server middleware that checks whether maintenance mode is enabled. If maintenance mode is active, SSR (Server-Side Rendering) mode will be off. This ensures that the backend IP is omitted, and CRS will take the role to display the maintenance page.

This code should be added to the `server/middleware/maintenance.ts` file.

```ts [maintenance.ts]
import { ApiClientError } from "@shopware/api-client";
import { isMaintenanceMode } from "@shopware/helpers";
import apiClient from "../apiBuilder";

export default defineEventHandler(async (event) => {
  try {
    await apiClient.invoke("readContext get /context");
  } catch (error) {
    if (error instanceof ApiClientError) {
      if (isMaintenanceMode(error.details.errors ?? [])) {
        event.context.nuxt = event.context.nuxt ?? {};
        event.context.nuxt.noSSR = true;
        console.log("Maintenance mode is active");
      }
    }
  }
});
```

---

---

## Sitemap
**Source:** [frontends/getting-started/features/sitemap.md](https://developer.shopware.com/frontends/getting-started/features/sitemap.md)  
# Sitemap

Sitemap is generated by combining two sitemaps, Frontends app and Shopware admin

Link:

```
http://<your_domain>/sitemap.xml
```

## Admin sitemap

```
/server/routes/sitemap.xml.ts
```

This sitemap contains links to pages like:

* Product pages
* Category pages
* CMS pages

More about the admin sitemap can be found [here](https://docs.shopware.com/en/shopware-6-en/settings/sitemap)

## Frontends sitemap

```
/server/routes/sitemap-local.xml.ts
```

This sitemap contains static page that are declared in the Frontends app

Each static page that comes from the Frontneds app, should be added manually to the `/server/sitemap.ts` file.

---

---

## Create a wishlist
**Source:** [frontends/getting-started/features/wishlist.md](https://developer.shopware.com/frontends/getting-started/features/wishlist.md)  
# Create a wishlist

In this chapter you will learn how to use the built-in wishlist API to create wishlist functionalities in your application. Specifically, you will learn how to

* Create a wishlist page
* Synchronize local and remote wishlist data
* Add products to and remove products from the wishlist

## Remote and local wishlists

In Shopware's Store API, only authenticated (logged-in) users can manage a custom wishlist.

The composables related to wishlists are built in a way that allows you to maintain a local (in-memory) wishlist for unauthenticated users and synchronize it with the server when the user logs in.

::: info
The `useWishlist` and `useProductWishlist` view helpers decide whether to use the local or the server wishlist based on the user's authentication status.
:::

| Composable           | Description                            |
| -------------------- | -------------------------------------- |
| `useLocalWishlist`   | manages the local (in-memory) wishlist |
| `useSyncWishlist`    | manages the remote (server) wishlist   |
| `useWishlist`        | view helper for the wishlist page      |
| `useProductWishlist` | view helper for a single product       |

## Get wishlist

You can use the `useWishlist` composable to get the wishlist products.

:::tip
`getWishlistProducts` method will detect if the customer is logged in or not
:::

```vue
<script>
import type { Schemas } from "#shopware";

// Contains a list of products ids in the wishlist
const { getWishlistProducts, items } = useWishlist();
const { apiClient } = useShopwareContext();

// Load products data
const loadProductsByItemIds = async (itemIds: string[]): Promise<void> => {
  isLoading.value = true;

  try {
    // Backend API call for product data
    const result = await apiClient.invoke("readProduct post /product", {
      body: {
        ids: itemIds || items.value,
      },
    });

    products.value = result.data.elements;
  } catch (error) {
    console.error(error);
  }
};

// Watch changes and update product data
watch(
  items,
  (items, oldItems) => {
    if (items.length !== oldItems?.length) {
      products.value = products.value.filter(({ id }) => items.includes(id));
    }
    if (!items.length) {
      return;
    }
    loadProductsByItemIds(items);
  },
  {
    immediate: true,
  }
);

onMounted(async () => {
  // Fetch wishlist products
  await getWishlistProducts();
});
</script>
<template>
  <div v-if="products.length">
    <h1>Wishlist</h1>
    <ProductCard
      v-for="product in products"
      :key="product.id"
      :product="product"
    />
  </div>
</template>
```

## Add product to the wishlist

You can use the `useProductWishlist` composable to add a product to the wishlist.
If the product is already added to the wishlist, the API will return an error.
To avoid such a situation, `isInWishlist` property should protect `addToWishlist` method.

:::tip
`addToWishlist` method will detect if the customer is logged in or not
:::

```vue
<script setup lang="ts">
// Mocked product
const product: Schemas["Product"] = {
  id: "7b5b97bd48454979b14f21c8ef38ce08",
};
const { addToWishlist, isInWishlist } = useProductWishlist(product);
</script>

<template>
  <button v-if="!isInWishlist" @click="addToWishlist">
    Add product to wishlist
  </button>
</template>
```

## Remove product from the wishlist

You can use the `useProductWishlist` composable to remove a product from the wishlist.
If the product doesn't exist in the wishlist, the API will return an error.
To avoid such a situation, `isInWishlist` property should protect `removeFromWishlist` method.

:::tip
`removeFromWishlist` method will detect if the customer is logged in or not
:::

```vue
<script setup lang="ts">
// Mocked product
const product: Product = {
  id: "7b5b97bd48454979b14f21c8ef38ce08",
};
const { removeFromWishlist, isInWishlist } = useProductWishlist(product);
</script>

<template>
  <button v-if="isInWishlist" @click="removeFromWishlist">
    Remove product from the wishlist
  </button>
</template>
```

## Merge wishlists

To synchronize the local wishlist with the remote wishlist (associated with the user's account), the `mergeWishlistProducts()` method must be triggered after the customer has logged in.

```vue{10}
<script setup lang="ts">
const formData = ref({
  username: "",
  password: "",
});
const invokeLogin = async (): Promise<void> => {
  try {
    // Login function
    await login(formData.value);
    mergeWishlistProducts();
  } catch (error) {
    console.error(error);
  }
};
</script>
<template>
  <form @submit.prevent="invokeLogin">
    <div>
      <label for="email-address">Email address</label>
      <input
        id="email-address"
        v-model="formData.username"
        name="email"
        type="email"
        autocomplete="email"
        required
        placeholder="Email address"
      />
    </div>
    <div>
      <label for="password" class="sr-only">Password</label>
      <input
        id="password"
        v-model="formData.password"
        name="password"
        type="password"
        autocomplete="current-password"
        required
        placeholder="Password"
      />
    </div>
    <div>
      <button type="submit">Sign in</button>
    </div>
  </form>
</template>
```

---

---

