# HEADLESS FRONTENDS

Compiled excerpts from the Shopware Developer Documentation snapshot. Prefer live docs at [developer.shopware.com](https://developer.shopware.com/) when in doubt.

---

## Work with languages
**Source:** [frontends/getting-started/languages.md](https://developer.shopware.com/frontends/getting-started/languages.md)  
# Work with languages

:::warning
This is the implementation working with `vue-demo-store` template only. To see the details, please go to the `templates/vue-demo-store` directory in the repository.
:::
Each store has two sources of translations.

Backend source for:

* CMS translations
* Product and categories
* Routing paths

Frontend source for:

* All static content declared on the frontend app

## Configuration

More about backend translations can be found [here](https://docs.shopware.com/en/shopware-6-en/tutorials-and-faq/translations)

For the frontend app we recommend to use `vue-i18n` module.

***When you are using same domain:***

:::warning
Backend languages codes and frontend languages codes must be the same!
:::

```
www.example.com         // GB site
www.example.com/de-DE   // DE site
```

```
{
  i18n: {
    vueI18n: {
      fallbackLocale: "en-GB",
    },
    strategy: "prefix_except_default",
    defaultLocale: "en-GB",
    langDir: "i18n/src/",
    locales: [
    {
      code: "en-GB",
      iso: "en-GB",
      file: "en-GB.ts",
    },
    {
      code: "de-DE",
      iso: "de-DE",
      file: "de-DE.ts",
    },
  ],
  },
}
```

***When you are using different domains:***

```
www.example1.com     // GB site
www.example2.com     // DE site
```

```
{
  i18n: {
    vueI18n: {
      fallbackLocale: "en-GB",
    },
    langDir: "i18n/src/",
    locales: [
    {
      domain: 'example1.com'
      code: "en-GB",
      iso: "en-GB",
      file: "en-GB.ts",
    },
    {
      domain: 'example2.com'
      code: "de-DE",
      iso: "de-DE",
      file: "de-DE.ts",
    },
  ],
  },
}
```

## Routing

When you are using *prefix* domain languages, you have to use `formatLink()` method from `useInternationalization` composable for building URLs.
The main task of this composable is to add a prefix to URL if needed.

```vue
<script setup lang="ts">
const localePath = useLocalePath();
const { formatLink } = useInternationalization(localePath);
</script>
<template>
  <NuxtLink :to="formatLink('/account')"> Account</NuxtLink>
</template>
```

## Testing

If you want to test languages locally, and your local domain differs from what is declared on the backend, you can use environment variables.

```
NUXT_PUBLIC_SHOPWARE_DEV_STOREFRONT_URL=http://127.0.0.1:3000
```

## localeId

In more complex scenarios, such as when different prefixes are used on the backend and frontend, the `localeId` attribute can be utilized.

```
  i18n: {
    strategy: "prefix_except_default",
    defaultLocale: "en-GB",
    detectBrowserLanguage: false,
    langDir: "./i18n/src/langs/",
    vueI18n: "./i18n/config",
    locales: [
      {
        code: "en-GB",
        iso: "en-GB",
        file: "en-GB.ts",
      },
      {
        code: "testde",
        iso: "de-DE",
        file: "de-DE.ts",
        localeId: "c19b753b5f2c4bea8ad15e00027802d4",
      },
    ],
  },
```

The `localeId` attribute corresponds to a specific language identifier, which can be located within the Shopware administrative panel. Additional information is available at this link: https://docs.shopware.com/en/shopware-6-en/settings/languages

## Multi domain example

To handle multiple domains for different languages, you can configure your application to recognize and switch between these domains seamlessly. Here's an example of how to set up your configuration:

[Check example](https://github.com/shopware/frontends/tree/main/examples/i18n-multi-domain)

*This example should be run locally because of the multi-domain requirements*

## Switching language locally

**Problem**

After switching the language, the URL returned from the backend is used as the basis for redirection which leads to exiting the localhost context.

```typescript
const onChangeHandler = async (option: Event) => {
  const data = await changeLanguage((option.target as HTMLSelectElement).value);

  if (data.redirectUrl) {
    window.location.replace(replaceToDevStorefront(data.redirectUrl));
  } else {
    window.location.reload();
  }
};
```

This can be problematic if you are trying to locally test the language switch flow. Below are some examples of how to resolve this problem:

### Locally host overrides

The idea of this solution is to override the domain locally in the `hosts` file.

Windows: `C:\Windows\System32\drivers\etc`
Linux: `/etc/hosts`
macOS: `/etc/hosts`

```
127.0.0.1       yourDomainFromBackend.com
#IPv6
::1             yourDomainFromBackend.com
```

Thanks to this, you will be able to use your local Frontends app instance with the domain returned by the backend.

### Add dev resolver

You can add own dev resolver to avoid redirection

```typescript
const dev = process.dev;

const onChangeHandler = async (option: Event) => {
  const data = await changeLanguage((option.target as HTMLSelectElement).value);

  // Check dev mode
  if (dev) {
    // Set locale
    locale.value = getLanguageCodeFromId(
      (option.target as HTMLSelectElement).value,
    );
    // Refresh page
    window.location.replace(`${window.location.origin}/${locale.value}`);
    return;
  }
  
  if (data.redirectUrl) {
    window.location.replace(replaceToDevStorefront(data.redirectUrl));
  } else {
    window.location.reload();
  }
};
```

## Troubleshooting in reverse proxy environments

When deploying your application behind a reverse proxy, such as Fastly, Cloudflare, or Vercel, you may encounter issues with language switching. This is primarily due to how these services cache responses and handle headers, which can affect the way languages are served to users.

To face possible issues with language switching, you would need to understand how [@nuxtjs/i18n](https://i18n.nuxtjs.org/) module works:

### **Language Detection**

The i18n module detects the user's preferred language based on the URL or the `Accept-Language` header.xz
The setting can be disabled by setting `detectBrowserLanguage: false` in the i18n module configuration. Then, the language will be determined solely based on the URL and the configured locales.

### **URL Structure**

The i18n module uses a specific URL structure to differentiate between languages. For example, it might use `/en/` for English and `/de/` for German. There are two strategies for this:

* `prefix_except_default`: This strategy adds a prefix to the URL for all languages except the default one.
* `prefix_and_default`: This strategy adds a prefix to the URL for all languages, including the default one.

### Multiple locales for the same domain

If you have multiple locales for the same domain, you can configure them in the i18n module. This allows you to serve different languages from the same domain without needing to switch domains.

### [@nuxtjs/i18n](https://i18n.nuxtjs.org/) module reads `x-forwarded-host` header

The i18n module can read the `x-forwarded-host` header to determine the original host of the request. This is useful when your application is behind a reverse proxy, as it allows the i18n module to correctly identify the requested language based on the original host.

### **Caching Issues**

Caching can cause issues with language switching, especially if the cache is not properly configured to handle different languages. To avoid this, ensure that your reverse proxy is set up to cache responses based on the `Accept-Language` header or the URL structure used by the i18n module.

Also, ensure that proxy caching is purged after the deployment of new language configurations or updates to the i18n module.

---

---

## Page elements
**Source:** [frontends/getting-started/page-elements.md](https://developer.shopware.com/frontends/getting-started/page-elements.md)  
# Page elements

Collection of page elements and documentation how to use them.





# Examples

Take a look at our cookbook recipe examples to get your front-end project started.

---

---

## Breadcrumbs managing
**Source:** [frontends/getting-started/page-elements/breadcrumbs.md](https://developer.shopware.com/frontends/getting-started/page-elements/breadcrumbs.md)  
# Breadcrumbs managing

In this chapter you will learn how to

* Build breadcrumbs for static page
* Build dynamic breadcrumbs for category/product page

### Quick reference

* [useBreadcrumbs](../../packages/composables/useBreadcrumbs) is a composable used for a breadcrumbs management with sharable state
* [getCategoryBreadcrumbs](../../packages/helpers.html#getcategorybreadcrumbs) is a helper used for converting `Category` to the `Breadcrumb` object
* [getCmsBreadcrumbs](../../packages/helpers#getcmsbreadcrumbs) is a helper used for building breadcrumbs for `Landing Pages`

## Building breadcrumbs for a static page

```ts
useBreadcrumbs([
  {
    name: "Shopware",
    path: "/shopware",
  },
]);
```

## Building breadcrumbs for a category/product page

```ts
// props.navigationId is a page id

const { buildDynamicBreadcrumbs } = useBreadcrumbs();
buildDynamicBreadcrumbs(props.navigationId);
```

## Building breadcrumbs for CMS pages - without additional request

Each CMS page contains the `Category` with `breadcrumb` array, which contains a list of names, like:

```
breadcrumb: ["Home", "Main navigation ", "Summer Party"]
```

we can convert current `string` array to the `Breadcrumb` object using [getCategoryBreadcrumbs](../../packages/helpers.html#getcategorybreadcrumbs) helper, and then pass it to [useBreadcrumbs](../../packages/composables/useBreadcrumbs) composable.

```ts
import { getCategoryBreadcrumbs } from "@shopware/helpers";

let breadcrumbs = getCategoryBreadcrumbs(
  productResponse.value?.product?.seoCategory,
);
useBreadcrumbs(breadcrumbs);
```

## Clearing breadcrumbs list

It's important to clear breadcrumbs list when you leave the page, otherwise you'll see breadcrumbs from the previous page if your not setting them on that page.

```ts
const { clearBreadcrumbs } = useBreadcrumbs();

onBeforeRouteLeave(() => {
  clearBreadcrumbs();
});
```

## Displaying Breadcrumbs

Breadcrumbs are stored in sharable variable `breadcrumbs` in [useBreadcrumbs](../../packages/composables/useBreadcrumbs) composable.

```vue
<script setup lang="ts">
const { breadcrumbs } = useBreadcrumbs();
</script>
<template>
  <nav>
    <ol>
      <li v-for="(breadcrumb, index) in breadcrumbs" :key="breadcrumb.path">
        <NuxtLink v-if="breadcrumb.path" :to="breadcrumb.path">
          {{ breadcrumb.name }}
        </NuxtLink>
        <span v-else>
          {{ breadcrumb.name }}
        </span>
        <div v-if="index < breadcrumbs.length - 1"></div>
      </li>
    </ol>
  </nav>
</template>
```

---

---

## Examples (Copy & Paste)
**Source:** [frontends/getting-started/page-elements/examples.md](https://developer.shopware.com/frontends/getting-started/page-elements/examples.md)  
# Examples (Copy & Paste)

Take a look at our cookbook recipe examples to get your front-end project started.

::: tip 🙋♀️ How to use examples?
Just copy the code snippet and paste it into your project. Sometimes it's useful to create a new component and use it in a higher level component like a page or a layout.
:::

## Navigation

## Cart

## Product Listings

## Product Detail Page

## Footer Navigation

---

---

## Cart
**Source:** [frontends/getting-started/page-elements/examples/cart.md](https://developer.shopware.com/frontends/getting-started/page-elements/examples/cart.md)  
# Cart

::: tip 🙋♀️ How to use these example?
Just copy the code snippet and paste it into your project. Sometimes it's useful to create a new component and use it in a higher level component like a page or a layout.
:::

## Simple cart

This cart is position in a sticky position on the right side of your screen and contains a basic overview of all products, including their price, quantities and the total price.

```vue
<script setup lang="ts">
const { count, refreshCart, cartItems, removeItem, totalPrice } = useCart();

onMounted(() => {
  refreshCart();
});
</script>
<template>
  <div
    class="fixed right-0 bg-white top-0 w-96 h-screen bg-blue p-6 shadow-lg z-10"
  >
    <h2 class="text-xl">Your Basket</h2>
    <span class="text-sm">{{ count }} items</span>
    <div v-for="item in cartItems" :key="item.id" class="flex gap-3 my-5">
      <div
        class="mr-4 h-24 w-24 flex-shrink-0 overflow-hidden rounded-md border border-gray-200"
      >
        <img
          v-if="item.type == 'product'"
          :src="item.cover?.url"
          class="h-full w-full object-cover object-center"
        />
      </div>
      <div class="flex justify-between grow">
        <div>
          <p class="font-medium mb-3">{{ item.label }}</p>
          <p class="text-gray-600 text-xs">{{ item.quantity }}</p>
        </div>
        <div class="text-right flex flex-col justify-between">
          <p>$ {{ item.price.totalPrice }}</p>
          <p
            class="text-blue-600 cursor-pointer hover:underline"
            @click="removeItem({ id: item.id })"
          >
            Remove
          </p>
        </div>
      </div>
    </div>
    <div
      class="mt-10 py-10 border-t border-gray-200 text-lg flex justify-between"
    >
      <span>Total</span><span>$ {{ totalPrice }}</span>
    </div>
  </div>
</template>
```

---

---

## Footer navigation
**Source:** [frontends/getting-started/page-elements/examples/footer-navigation.md](https://developer.shopware.com/frontends/getting-started/page-elements/examples/footer-navigation.md)  
# Footer navigation

::: tip 🙋♀️ How to use these example?
Just copy the code snippet and paste it into your project. Sometimes it's useful to create a new component and use it in a higher level component like a page or a layout.
:::

## Explanation

Implementing Footer navigation can be described in few steps:

1. Use [useNavigation](../../../../packages/composables/useNavigation) composable to `loadNavigationElements` to display a navigation configured in admin panel.
2. Iterate over `navigationElements` array of categories and display them.
3. Add some static links next-to dynamic ones if needed.
4. Resolve URLs and implement dedicated pages for it.

## Code Example

```vue
<script setup lang="ts">
import { useNavigation } from "@shopware/composables";
import { getCategoryRoute } from "@shopware/helpers";
const { navigationElements, loadNavigationElements } = useNavigation({
  type: "footer-navigation", // footer-navigation selected
});
loadNavigationElements({
  // invoke an API call to fetch navigation categories
  depth: 1,
});
</script>
<template>
  <Transition>
    <footer v-if="navigationElements.length" class="bg-white dark:bg-gray-900">
      <div class="mx-auto w-full max-w-screen-xl">
        <div class="grid grid-cols-2 gap-8 px-4 py-6 lg:py-8 md:grid-cols-4">
          <div v-for="category in navigationElements" :key="category.id">
            <h2
              class="mb-6 text-sm font-semibold text-gray-900 uppercase dark:text-white"
            >
              {{ category.translated.name }}
            </h2>
            <ul
              class="text-gray-500 dark:text-gray-400 font-medium"
              v-if="category?.childCount"
            >
              <li
                class="mb-4"
                v-for="childCategory in category.children"
                :key="childCategory.id"
              >
                <a
                  :href="getCategoryRoute(childCategory)"
                  class="hover:underline"
                  >{{ childCategory.translated.name }}</a
                >
              </li>
            </ul>
          </div>
        </div>
      </div>
    </footer>
  </Transition>
</template>
<style scoped>
.v-enter-active,
.v-leave-active {
  transition: opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>
```

[getCategoryUrl](../../../../packages/helpers#getcategoryurl) method imported from `helpers-next` package can extract a SEO Url or technical URL for given category.

:::warning
`getCategoryUrl` returns absolute path for corresponding category, which means you will get for example `/some-category/some-subcategory` and not the entire URL including domain.

By design, the URL can point also to the Product or Landing Page.
In order to resolve an entity assigned to each category path, utilize a [composable](../../../../packages/composables/useNavigation) dedicated for expected entity:

1. `search` from `useNavigationSearch` to find entity type.
2. use [dedicated composable](../../../../getting-started/routing#resolve-a-route-to-a-page) to process page resolving.
   :::

---

---

## Product Listing
**Source:** [frontends/getting-started/page-elements/examples/listing.md](https://developer.shopware.com/frontends/getting-started/page-elements/examples/listing.md)  
# Product Listing

::: tip 🙋♀️ How to use these example?
Just copy the code snippet and paste it into your project. Sometimes it's useful to create a new component and use it in a higher level component like a page or a layout.
:::

## Condensed product listing

This listing shows the product name and price with soft hover effects and a fade-in animation.

```vue
<script setup lang="ts">
import { useProductSearchSuggest } from "@shopware/composables";
import { getTranslatedProperty } from "@shopware/helpers";

const { search, searchTerm, getTotal, getProducts } = useProductSearchSuggest();

onMounted(() => {
  // Replace that with your custom logic to fetch products
  searchTerm.value = "sal";
  search();
});

const addProductAndRefresh = async ({ id }) => {
  await addProduct({ id });
  refreshCart();
};

const { addProduct, refreshCart } = useCart();
</script>

<template>
  <div
    class="grid grid-cols-2 md:grid-cols-4 gap-3 max-w-screen-xl mx-auto p-3 transition-opacity pt-32"
    :class="[getTotal > 0 ? 'opacity-100' : 'opacity-0']"
  >
    <div v-for="product in getProducts" :key="product.id" class="h-96 group">
      <div class="h-48">
        <div
          class="h-full w-full object-cover bg-white cursor-pointer overflow-hidden"
        >
          <img
            :src="product.cover.media.url"
            class="w-full h-full object-cover group-hover:scale-110 transition-all duration-300"
          />
        </div>
        <div class="h-36 py-5 font-light flex flex-col justify-between">
          <h3
            class="text-xl line-clamp-1 mb-2 group-hover:text-gray-800"
            @click="addProduct({ id: product.id })"
          >
            {{ getTranslatedProperty(product, "name") }}
          </h3>
          <p class="text-gray-700 group-hover:text-gray-500">
            {{ product.calculatedPrice.totalPrice }} €
          </p>
        </div>
        <div
          class="bg-gray-300 p-2 h-12 flex items-center justify-center text-gray-800 cursor-pointer hover:bg-gray-400"
          @click="addProductAndRefresh({ id: product.id })"
        >
          Add to basket
        </div>
      </div>
    </div>
  </div>
</template>
```

---

---

## Navigation
**Source:** [frontends/getting-started/page-elements/examples/navigation.md](https://developer.shopware.com/frontends/getting-started/page-elements/examples/navigation.md)  
# Navigation

::: tip 🙋♀️ How to use these example?
Just copy the code snippet and paste it into your project. Sometimes it's useful to create a new component and use it in a higher level component like a page or a layout.
:::

## Simple navigation

```vue
<script setup lang="ts">
const { loadNavigationElements, navigationElements } = useNavigation();
await loadNavigationElements({ depth: 2 });

const { path: currentPath } = useRoute();

const isActive = (path: string) => {
  return "/" + path === currentPath;
};
</script>

<template>
  <div class="w-full shadow-lg mb-10 bg-white fixed">
    <nav
      class="w-full flex flex-col divide-gray-200 divide-y md:flex-row md:max-w-screen-xl md:mx-auto md:divide-y-0 md:divide-x"
    >
      <RouterLink
        v-for="navigationElement in navigationElements"
        :key="navigationElement.id"
        :to="'/' + navigationElement.seoUrls[0]?.seoPathInfo"
      >
        <div
          class="flex p-4 h-full border-l-5 hover:border-gray-200 md:border-l-none md:border-b-5 md:w-60 transition duration-200 items-center"
          :class="[
            isActive(navigationElement.seoUrls[0]?.seoPathInfo)
              ? 'border-indigo-500'
              : 'border-white',
          ]"
        >
          {{ navigationElement.translated.name }}
        </div>
      </RouterLink>
    </nav>
  </div>
</template>
```

---

---

## Simple Product Detail Page
**Source:** [frontends/getting-started/page-elements/examples/product-detail-page.md](https://developer.shopware.com/frontends/getting-started/page-elements/examples/product-detail-page.md)  
# Simple Product Detail Page

::: tip 🙋♀️ How to use these example?
Just copy the code snippet and paste it into your project. Sometimes it's useful to create a new component and use it in a higher level component like a page or a layout.
:::

See also the [complete guide](../../../e-commerce/product-detail-page) about the product detail page from the BUILDING section.

## Simple Product Detail Page

Path: `templates/vue-demo-store/components/product/ProductStatic.vue`

```vue
<script setup lang="ts">
import type { Schemas } from "#shopware";
import { getProductRoute, getTranslatedProperty } from "@shopware/helpers";
import type { Ref } from "vue";

const router = useRouter();

const { search } = useProductSearch();
const { data: productResponse } = await useAsyncData(
  "productExample",
  async () => {
    const productResponse = await search("4fd7aa46370147d4963784e4e8821f8c", {
      withCmsAssociations: true,
    });
    return productResponse;
  },
);

const { product } = useProduct(
  productResponse.value?.product,
  productResponse.value?.configurator,
);
const { loadProductReviews, productReviews } = useProductReviews(product);

onMounted(async () => {
  await loadProductReviews();
});

const productName = computed(() =>
  getTranslatedProperty(product.value, "name"),
);
const manufacturerName = computed(() =>
  getTranslatedProperty(product.value.manufacturer, "name"),
);

const description = computed(() =>
  getTranslatedProperty(product.value, "description"),
);
const properties = computed(() => product.value?.properties || []);

const handleVariantChange = (val: Schemas["Product"]) => {
  const newRoute = getProductRoute(val);
  router.push(newRoute);
};
</script>

<template>
  <div class="m-5 flex flex-row flex-wrap justify-start">
    <!-- Product name for mobile view -->
    <div class="basis-12/12 display lg:hidden">
      <h1
        class="pl-4 py-4 text-2xl font-extrabold tracking-tight text-gray-900 sm:text-3xl"
        v-html="productName"
      />
    </div>
    <div class="basis-12/12 lg:basis-7/12 product-gallery overflow-hidden">
      <ProductGallery :product="product" />
    </div>
    <div class="basis-12/12 lg:basis-5/12 product-description">
      <!-- Product info -->
      <div
        class="max-w-2xl mx-auto pb-16 px-4 sm:px-6 lg:max-w-7xl lg:pb-24 lg:pl-16 lg:pr-0"
      >
        <!-- Product name starting from lg breakpoint -->
        <div
          class="hidden lg:block text-2xl font-extrabold tracking-tight text-gray-900 sm:text-3xl"
          v-html="productName"
        />

        <div
          v-show="manufacturerName !== ''"
          class="lg:col-span-2 lg:pr-8 static-container"
        >
          <div class="container mx-auto pt-8 flex flex-row">
            <div class="basis-2/6 text-right">
              {{ manufacturerName }}
            </div>
          </div>
        </div>

        <!-- Options -->
        <div class="mt-4 lg:mt-0 lg:row-span-3">
          <h2 class="sr-only">Product information</h2>
          <div class="product-variants mt-10">
            <ProductPrice :product="product" />
            <ProductUnits :product="product" class="text-sm" />
            <ProductVariantConfigurator @change="handleVariantChange" />
            <ProductAddToCart :product="product" />
          </div>
        </div>

        <div
          class="py-10 lg:pt-6 lg:pb-16 lg:col-start-1 lg:col-span-2 lg:pr-8"
        >
          <div class="container mx-auto mb-8">
            <!-- Description and details -->
            <div v-if="description">
              <h3 class="text-sm font-bold text-gray-900">
                {{ $t("product.description") }}
              </h3>
              <div class="mt-4 space-y-6">
                <div class="text-base text-gray-900" v-html="description" />
              </div>
            </div>

            <div v-if="properties?.length" class="mt-10">
              <h3 class="text-sm font-medium text-gray-900">
                {{ $t("product.price.properties") }}
              </h3>

              <div class="mt-4">
                <ul role="list" class="pl-4 list-disc text-sm space-y-2">
                  <li
                    v-for="property in properties"
                    :key="property.id"
                    class="text-gray-400"
                  >
                    <span class="text-gray-600">{{
                      getTranslatedProperty(property, "name")
                    }}</span>
                  </li>
                </ul>
              </div>
            </div>

            <div v-if="productReviews?.length" class="mt-10">
              <h3 class="text-sm font-medium text-gray-900">
                {{ $t("product.reviews") }}
              </h3>
              <div v-if="productReviews?.length" class="mt-4">
                <ul role="list" class="pl-4 list-disc text-sm space-y-2">
                  <li
                    v-for="review in productReviews"
                    :key="review.id"
                    class="text-gray-400"
                  >
                    <span class="text-gray-600">{{ review.content }}</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
```

---

---

## Working with Images
**Source:** [frontends/getting-started/page-elements/images.md](https://developer.shopware.com/frontends/getting-started/page-elements/images.md)  
# Working with Images

This section covers topics related to images, with a focus on what comes from API.

:::warning Not auto-loaded
Although images are not always contained in API responses, we try to keep the composables logic aware of that and ready to load if they are needed.

Which means if you need to work with images, ensure the requests contains additional [associations](https://shopware.stoplight.io/docs/store-api/cf710bf73d0cd-search-queries#associations).

Example of request's payload with media association included, to avoid an empty `media` object within the response:

```json
{
  "associations": {
    "media": {}
  }
}
```

:::

## Structure of media objects

Media objects can be used in many places, such as:

* CMS objects (containing [CmsElementImage](https://github.com/shopware/frontends/blob/main/packages/composables/src/types/cmsElementTypes.ts#L71) element)
* Product (cover image, image gallery, attributes in type media, etc.)
* Category (main image, ...)
* ...

Regardless the outer container (see [ProductMedia](https://github.com/shopware/frontends/blob/main/packages/types/shopware-6-client/models/content/product/ProductMedia.d.ts#L8) as example) an image object can be wrapped with, the inner structure is reflected in type definition at [Media](https://github.com/shopware/frontends/blob/main/packages/types/shopware-6-client/models/content/media/Media.d.ts#L23)

Let's have a look what's inside:

```json
{
  // irrelevant data omitted
  ...
  "mimeType": "image/webp", // mime-type of media object, supported by the Shopware 6 platform
  "fileExtension": "webp",
  "fileSize": 492024,
  "title": "Frontends Logo",
  "metaData": {
      "hash": "b795091b0a92b8a0605281f710dc1c28",
      "type": 2,
      "width": 3505, // original width
      "height": 5258 // original height
  },
  "alt": "Shopware Frontends",
  "url": "http://localhost/media/shopware-frontends-4P8HWu_NRp4-unsplash.jpg",
  "fileName": "shopware-frontends-4P8HWu_NRp4-unsplash",
  "thumbnails": [ // list of resized images for previously configured ranges
    {
      "width": 1920,
      "height": 1920,
      "url": "http://localhost/thumbnail/ainars-cekuls-4P8HWu_NRp4-unsplash_1920x1920.webp",
    },
    {
      // omitted irrelevant data
      "width": 800,
      "height": 800,
      "url": "http://localhost/thumbnail/ainars-cekuls-4P8HWu_NRp4-unsplash_800x800.webp",
      "apiAlias": "media_thumbnail"
    },
    ...
  ]
  ...
}
```

The media object, and its `thumbnails` list, contain all required information about the file to be used in the browser like URL and sizes.

## Thumbnails and resolutions

By default, every uploaded image is resized to the predefined width and height sizes (in pixels):

* 1920x1920
* 800x800
* 400x400

In order to change those sizes, or add another one (also the quality, or to keep aspect ratio), the values need to be adjusted in administration panel, for specific media folder.

![Edit media sizes](../../.assets/edit-media-sizes.png)

:::warning Image processing
While a file is uploaded, it's been automatically resized for the current configuration in Administration > Media section. Thanks to this, the newly uploaded files will be available for all required dimensions. However keep in mind that if your settings have changes, the new dimensions won't be applied automatically for the old images.
:::

## Helpers

There are few functions that could be used to extract some crucial information about the media in short way. For example [getMainImageUrl](../../packages/helpers#getmainimageurl) or [getMedia](../../packages/helpers#getmedia).

Example how to work with Product's main image:

```ts
import { getMainImageUrl } from "@shopware/helpers";

const coverUrl = getMainImageUrl(product);
// coverUrl is now an URL to the resource (or undefined)
```

## Responsive Images

Having additional information about resized images (see `thumbnails` array in `Media` object), we are able to use them to define [srcset](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img#attr-srcset) attribute for `<img>`.

```vue{8}
<script>
import type { Schemas } from "#shopware";
const product: Schemas['Product'] = {} // an object omitted
// get the cover media image (main image for a product)
const coverMedia = product.cover?.media
// prepare `srcset` string for available thumbnails
// let the breakpoints be for every width range
const srcset = coverMedia?.thumbnails?.map((thumb) => `${thumb.url} ${thumb.width}w`).join(", ")
</script>

<template>
   <img
    :srcset="srcset"
    :src="coverMedia?.url"
    :alt="coverMedia?.alt"
    :title="coverMedia?.title"
  >
</template>
```

### Live example

Have a look on live example:



The example above shows how to use dimension sizes configured in admin panel as ranges for viewport. However it can be adjusted to your needs.

The `src` attribute points to the main image URL (not resized) as a fallback.

As long as `thumbnails` array is fulfilled, the same strategy can be applied when we work with every `media` object for each entity available in Shopware 6.

---

---

## Create a login form
**Source:** [frontends/getting-started/page-elements/login-form.md](https://developer.shopware.com/frontends/getting-started/page-elements/login-form.md)  
# Create a login form

In this chapter, you will learn how to

* Sign in using username and password
* Display data of an authenticated user
* Display authentication errors
* Logout

## Build the form

Let us start by providing some reactive objects and input elements to get customer login credentials from the browser.

```vue{3,4,10,11}
<script setup lang="ts">
    const loginCredentials = reactive({
        username: "",
        password: "",
    })
    const invokeLogin = () => {}
</script>
<template>
    <div>
        <input type="text" v-model="loginCredentials.username" />
        <input type="password" v-model="loginCredentials.password" />

        <button @click="invokeLogin">Sign in</button>
    </div>
</template>
```

## Manage the user session

Now, the presentation layer has all required fields to perform a login process.

In the next step, use the `useUser` composable. It provides user data, login methods, and other interfaces.

```vue
<script setup lang="ts">
const {
  login, // login method, accepts username and password
  logout, // performing a logout
  errors, // errors from API prefixed with a method name, which is the source of the problem
  isLoggedIn, // flag that says if customer is logged in
  user, // the whole customer object
} = useUser();

const invokeLogin = () => login(loginCredentials);
</script>
...
```

The `invokeLogin` method is triggered using the `@click` event of the button. It executes the `login()` method from the `useUser` composable, accepting `loginCredentials` (the `v-model` of inputs) as an argument.

## Display user data

If the login process was successful, the `isLoggedIn` computed property becomes `true`. Now we can use `user` object to access customer data.

```vue{2,6}
<template>
  <div v-if="!isLoggedIn">
    <!-- DISPLAY FORM HERE -->
  </div>
  <div v-else>
    <h1>Hi, {{ user.firstName }}!</h1>
    <button @click="logout()">sign out</button>
  </div>
</template>
```

The example above shows the conditional visibility of content depending on the customer's logged in state.

## Handle authentication errors

To finish, we would like to inform the user about problems that may appear during the authentication.

In order to achieve it, the `errors` computed ref can be used:

```vue{5}
<template>
    <div v-if="!isLoggedIn">
        <div v-if="errors.login.length">
            {{ errors.login[0].detail }}
        </div>
    </div>
</template>
```

The example explains how to display only the first error that may appear in the response while processing the `login` method (see, the `errors` computed has prefixed `login` nested object).

## Full example

```vue
<script setup lang="ts">
const { logout, login, errors, isLoggedIn, user } = useUser();
const loginCredentials = reactive({
  username: "",
  password: "",
});
const invokeLogin = () => login(loginCredentials);
</script>
<template>
  <div v-if="!isLoggedIn">
    <h1>Sign in to your account</h1>
    <input type="text" v-model="loginCredentials.username" />
    <input type="password" v-model="loginCredentials.password" />
    <button @click="invokeLogin">sign in</button>
    <div v-if="errors.login.length">
      {{ errors.login[0].detail }}
    </div>
  </div>
  <div v-else>
    <h1>Hi, {{ user.firstName }}!</h1>
    <button @click="logout()">sign out</button>
  </div>
</template>
<style scoped>
.errors {
  color: red;
  margin-top: 10px;
}
</style>
```

---

---

## Create a navigation
**Source:** [frontends/getting-started/page-elements/navigation.md](https://developer.shopware.com/frontends/getting-started/page-elements/navigation.md)  
# Create a navigation

In this chapter you will learn how to

* Fetch the navigation of a store
* Display navigation items

## Fetch the navigation

We can retrieve the navigation of a store using the `useNavigation` composable hook.

```js
const { loadNavigationElements, navigationElements } = useNavigation();
```

The `navigationElements` property is a reactive reference to the navigation items which is updated as we fetch the navigation elements:

```js
await loadNavigationElements({ depth: 2 });
```

## Build a navigation template

Now all values can be accessed in the template to build a navigation menu

Note that all the navigation items are in type `Category`, and thanks to this the `getCategoryUrl` helper can be used to extract the correct pretty URL or technical URL as a fallback.

```vue
<script setup lang="ts">
import { getCategoryUrl } from "@shopware/helpers";
const { loadNavigationElements, navigationElements } = useNavigation();
await loadNavigationElements({ depth: 2 });
</script>

<template>
  <ul>
    <li
      v-for="navigationElement in navigationElements"
      :key="navigationElement.id"
    >
      <RouterLink
        :to="getCategoryRoute(navigationElement)"
        :target="
          navigationElement.externalLink || navigationElement.linkNewTab
            ? '_blank'
            : ''
        "
      >
        {{ navigationElement.translated.name }}
      </RouterLink>
    </li>
  </ul>
</template>
```

There is an additional attribute `target` used, in order to open a link in another window (external links or configured as `new tab` link).

## Next steps

---

---

## Work with routing
**Source:** [frontends/getting-started/routing.md](https://developer.shopware.com/frontends/getting-started/routing.md)  
# Work with routing

In the [building a navigation](./page-elements/navigation.html) chapter you have already learned how to create a menu structure for your frontend. In this chapter you will learn how to resolve the paths of each menu item, so that users can navigate the store. Specifically, you will learn how to

* Resolve a path string to a route configuration
* Resolve a route configuration to its page or entity

## Resolve a URL path to a route

In Shopware, the concept of routing is connected to `SeoUrl` routes. A `SeoUrl` contains information about the path and what page it resolves to.

In the most common routing scenario, you will have a URL path like `/Winter-Season/My-Product` and want to resolve it to a route configuration. The `useNavigationSearch` composable provides a function to do that:

```js
import {
  useNavigationContext,
  useNavigationSearch,
} from "@shopware/composables";

const { resolvePath } = useNavigationSearch();

const seoResult = await resolvePath("/Winter-Season/My-Product");

const { routeName, foreignKey } = useNavigationContext(ref(seoResult));
```

The result of the `resolvePath` function is a reduced `SeoUrl` object, which you can access safely via the useNavigationContext composable.

```json
{
  "routeName": "frontend.detail.page",
  "foreignKey": "f2f6b6b3a0a04e2a8b0f8a2b2b5b5b1a"
}
```

This is all information you need to resolve the route to a page, or rather an entity.

## Resolve a route to a page

There are three different type of routes that Shopware natively supports. When there are extensions active in your store, there can be more. The three types are:

* `frontend.detail.page` - A product detail page
* `frontend.navigation.page` - A category page
* `frontend.landing.page` - A landing page

Depending on which type of route you have, the way of fetching the page data is different - because routes don't point to pages. They point to entities that are used to render pages.

Possibly, the easiest approach is to set up a catch-all component, that resolves the route and then renders the correct page component. This is how it could look like:

```ts
import type { Schemas } from "#shopware";

import {
  useNavigation,
  useNavigationContext,
  useNavigationSearch,
  useCategorySearch,
} from "@shopware/composables";

const seoResult: Schemas["SeoUrl"] | null = await resolvePath(route.path);

const { routeName, foreignKey } = useNavigationContext(ref(seoResult));

const data = ref(null);

switch (routeName.value) {
  case "frontend.navigation.page":
    let { search: categorySearch } = useCategorySearch();
    const categoryResponse = await categorySearch(foreignKey.value, {
      withCmsAssociations: true,
    });
    const { category } = useCategory(categoryResponse);
    data.value = category;
    break;
  case "frontend.detail.page":
    let { search: productSearch } = useProductSearch();
    const productResponse = await productSearch(foreignKey.value, {
      withCmsAssociations: true,
    });
    const { product } = useProduct(productResponse);
    data.value = product;
    break;
  case "frontend.landing.page":
    let { search: landingSearch } = useLandingSearch();
    const landing = await landingSearch(foreignKey.value, {
      withCmsAssociations: true,
    });
    data.value = ref(landing);
    break;
}
```

This switch statement handles all options that Shopware natively supports and can easily be enhanced. Another option is to build custom components for each route type and do the rest in there.

:::tip Module imports
If you use the `@shopware/nuxt-module`, all composables will be automatically imported for you.
:::

You are done at this point if you choose to build/design custom pages or integrate an external CMS system for the page content.

## Omitting store API calls for seoURLs

Having pretty URLs is important for SEO and user experience. To display the proper page for that URL, it must be resolved first. This often requires two API calls.

* seoURL lookup, which returns the kind of page we should display and the id of the entity
* API call to fetch the entity data

Thankfully, we do not need to do that in every case. Only the first request (handled on the server side) is required to resolve the URL. After we render the page, every link information contains not only SEOUrl for redirection but also metadata information containing redirection data. Thanks to this, we can load page data directly without first resolving the URL.

To create speaking links for products or categories, you must know the `seoPathInfo` from the `seoURLs` object. In some situations, you only have the ID of the product or category and then you may need to make an additional call to get the speaking link. This call costs time and can be omitted.

We have created two new helper functions that can be used to avoid these extra calls. Just use [getCategoryRoute](../packages/helpers.html#getcategoryroute) and [getProductRoute](../packages/helpers.html#getproductroute) from helpers package. Use them in combination of `RouterLink` or `NuxtLink` in Vue.js or Nuxt.js projects.

##### Example getCategoryRoute with NuxtLink

```vue
<script setup lang="ts">
import { getCategoryRoute } from "@shopware/helpers";
</script>

<template>
  <NuxtLink :to="getCategoryRoute(navigationChild)">
    {{ getTranslatedProperty(navigationChild, "name") }}
  </NuxtLink>
</template>
```

##### Example getProductRoute with RouterLink

```vue
<script setup lang="ts">
import { getProductRoute } from "@shopware/helpers";
</script>

<template>
  <RouterLink :to="getProductRoute(product)">
    {{ getTranslatedProperty(product, "name") }}
  </RouterLink>
</template>
```

##### How does "Omitting store API calls for seoURLs" work in detail?

Several things happen during a request. It should be noted that some operations take place on the server side and some on the client side. Also, data can be passed from the server side to the client side and reused there without the need for a new request. Check the documentation about [useAsyncData](https://nuxt.com/docs/api/composables/use-async-data) in a Nuxt environment.

> Simplified process
>
> 1. The user loads an arbitrary page (we don't know which one it is)
> 2. The server-side rendering (SSR) always happens first and that's where we need to resolve the page, as you learned [above](#resolve-a-route-to-a-page). You will see in the developer tools (network tab) that we load the CMS data (seoURL is included in the response) from the store API.
> 3. After the initial loading (as described in 1 and 2), we already show pretty links to the user. From now on, we don't need to call the store API endpoint for seo-urls, because we already have the data we need. So we simply return it to the user via the [History State API](https://developer.mozilla.org/en-US/docs/Web/API/History/state). This is why we use helpers always in our demo-store template.

To check it out on a code level have a look at the `[...all].vue` file in the demo-store template.

## Next steps

---

---

## Setup Templates
**Source:** [frontends/getting-started/templates.md](https://developer.shopware.com/frontends/getting-started/templates.md)  
# Setup Templates

Shopware Frontends offers shortcuts to getting started with your custom frontend. These so-called templates offer different levels of "completeness" of a project.

:::tip HINT 💡
Integrate Shopware Frontends as an **npm package** into your existing [custom Vue project](./templates/custom-vue-project).
:::

## Vue Starter Template

The Vue Starter Template is a production-ready foundation for building custom Shopware storefronts. Unlike the Demo Store Template, it contains no demo UI or boilerplate - just the essential packages and configuration you need to start building.

**What's included:**

* Nuxt 4.x with full SSR
* All Shopware Frontends core packages
* UnoCSS (Tailwind-compatible) styling
* i18n support
* TypeScript with type generation

**Best for:** Starting a new production storefront project from a clean foundation.

## Vue Starter Template Extended

An example implementation showing how to extend the Vue Starter Template using Nuxt layers. This "Lumora" branded demo demonstrates how to create brand-specific storefronts while inheriting all base functionality.

**Layer benefits:**

* Minimal code duplication
* Override only what you need
* Automatic base template updates
* Multiple brand variants from one base

**Best for:** Learning the layer pattern or managing multiple brand storefronts.

## Blank Template

If you like to start from scratch, you can use the blank template. It can be handy if you want to use a different CSS framework or create a completely new frontend, but leverage the built-in functionality of all Shopware Frontends packages.

The blank template has all "non-UI" packages pre-installed, but you have to bring your own styles and components.

## Demo Store Template

:::warning DEPRECATED
This standalone template is deprecated. We recommend using the **Vue Starter Template** approach, which leverages Nuxt layers to extend a base template. This pattern provides better maintainability, automatic updates, and allows you to build multiple brand storefronts from a single foundation.
:::


:::info
The **Demo Store Template** is not production-ready. It is only a **reference implementation** that contains most of the features which you can use as a starting point. It is not possible to update it automatically or install Shopware extensions on it.
:::

The demo store template is a **reference implementation** of an online store UI. It comes with all default features implemented as boilerplate code - such as

* Navigation & Header
* Cart
* Checkout
* CMS Pages

It is based on Nuxt3 and UnoCSS (Tailwind)

## Custom projects

It is possible to integrate Shopware Frontends into an existing project. This can be applicable if you have an existing frontend application and you want to build eCommerce functionality into it.

As of now, **Vue.js** and **React** projects are supported.

## Framework supporting Vue

In theory, every place where the Vue instance is available, is supported by Shopware Frontends too.

The only requirement is to have a possibility to register a Vue 3 plugin, and that's what can be done in [Astro.js](https://astro.build/) as well.

---

---

## Astro Blank Template
**Source:** [frontends/getting-started/templates/astro-template.md](https://developer.shopware.com/frontends/getting-started/templates/astro-template.md)  
# Astro Blank Template

The blank Astro bootstrap application with pre-installed dependencies, so you can start working on your project right away.

**Now you can use `composables` and `api-client` libraries in every Vue component created in an Astro project.**

## Setup & run

Alternatively, set up the astro-blank template manually by running the following commands in a new directory:

```bash
npx tiged shopware/frontends/templates/astro astro-blank && cd astro-blank
npm i && npm run dev
```

## Configure

The blank template is pre-configured to connect to a public Shopware backend, so you can follow our [building guides](../) right away.

In order to connect it to your own store backend, you need to edit the `env.development`:

```bash
# .env.development
API_URL="https://demo-frontends.shopware.store"
API_ACCESS_TOKEN="SWSCBHFSNTVMAWNZDNFKSHLAYW"
```

:::info Production
For production build it's good to prepare a separate `.env.production` file containing other credentials if needed.
:::

If the customization isn't enough, visit `src/entrypoints/_shopware.ts` file and customize it on your own. Like, change cookie manager, or add some other configuration for API client instance.

## What next?

---

---

## Blank Template
**Source:** [frontends/getting-started/templates/blank-template.md](https://developer.shopware.com/frontends/getting-started/templates/blank-template.md)  
# Blank Template

The blank template contains no UI or markup - it's just a blank Nuxt3 application with pre-installed dependencies, so you can start working on your project right away.

## Setup & run

Alternatively, set up the vue-blank template manually by running the following commands in a new directory:

```bash
npx tiged shopware/frontends/templates/vue-blank vue-blank && cd vue-blank
npm i && npm run dev
```

## Configure

The blank template is pre-configured to connect to a public Shopware backend, so you can follow our [building guides](../) right away.

In order to connect it to your own store backend, you need to edit the `nuxt.config.ts` file and add a configuration details:

```ts
/* ... */
export default defineNuxtConfig({
  runtimeConfig: {
    // shopware: {
    /**
     * SSR Shopware Endpoint
     * More here: https://frontends.shopware.com/getting-started/templates/custom-vue-project.html#shopware-endpoint-on-the-ssr-mode
     */
    //   endpoint: ""
    // },
    public: {
      shopware: {
        endpoint: "https://your-business.shopware.store",
        accessToken: "access-token-from-settings",
      },
    },
  },
});
```

## What next?

---

---

## Custom React project
**Source:** [frontends/getting-started/templates/custom-react-project.md](https://developer.shopware.com/frontends/getting-started/templates/custom-react-project.md)  
# Custom React project

:::info
This template is a prototype. It shows how to integrate Composable Forntends into React.
::::

## About this project

* **React** and **Next.js** with **App Router**
* It is based on the [vercel-commerce](https://github.com/shopwareLabs/vercel-commerce) template
* It uses the new [api-client](https://www.npmjs.com/package/@shopware/api-client)
* There is **no headless checkout**, we are currently working on supporting the default checkout
* Each page is currently **pre-generated** during build time
  * Vercel supports building partial pages after updating when sending a webhook
  * This feature was not tested with Shopware (see API endpoint [here](https://github.com/shopwareLabs/vercel-commerce/blob/main/lib/shopware/index.ts#L302))

---

---

## Custom Vue.js project
**Source:** [frontends/getting-started/templates/custom-vue-project.md](https://developer.shopware.com/frontends/getting-started/templates/custom-vue-project.md)  
# Custom Vue.js project

Follow these steps to integrate Shopware Frontends into an existing, custom Vue.js project

* Install the required dependencies
* Prepare a Vue plugin for better encapsulation
* Configure the API client and create application instance
* Store and handle client state

## Creating Vue project

:::info
You can skip this part if you have an existing project.
::::

```bash
pnpm create vue@latest
```

More information about creating a new Vue project can be found [here](https://vuejs.org/guide/quick-start.html)

## Install dependencies

First of all, install the required npm dependencies:

```bash
pnpm add @shopware/composables @shopware/api-client
```

Additionally, to keep the current session context even after page reloads, we are going to install a cookie helper to set and get value of [context token](https://shopware.stoplight.io/docs/store-api/ZG9jOjEwODA3NjQx-authentication-and-authorisation) in our plugin:

```bash
pnpm add js-cookie
```

For CMS components, you can add a package that contains ready-to-use components.
You can read more about CMS pages here:

```sh
# ✨ Auto-detect
npx nypm install -D @shopware/cms-base-layer

# npm
npm install -D @shopware/cms-base-layer

# yarn
yarn add -D @shopware/cms-base-layer

# pnpm
pnpm install -D @shopware/cms-base-layer

# bun
bun install -D @shopware/cms-base-layer

# deno
deno install --dev @shopware/cms-base-layer
```

## Configure API client

:::tip Code example
Find a full example of the Vue.js plugin [here](#plugin-code).
:::

Now, let's configure the API client and business logic together.

:::info
The business logic is written to be Vue 3 compatible. Under the hood, it utilizes the composition API, especially the `provide`/`inject` feature for sharing state.
:::

In order to configure the business logic and API client together with your Vue 3 application, it's required to create a Shopware instance provided by a factory method within the `@shopware/composables` package. Everything will be encapsulated in a plugin and installed later on.

:::tip Vue plugins
This section requires having knowledge about the [concept of Vue 3 plugins](https://vuejs.org/guide/reusability/plugins.html#writing-a-plugin).
:::

Import necessary methods from `@shopware/api-client`, `@shopware/composables` and `js-cookie` packages:

```ts
// ./plugins/vue-shopware-frontends.ts file
import { ref } from "vue";
import type { App } from "vue";
import { createAPIClient } from "@shopware/api-client";
import { createShopwareContext } from "@shopware/composables";
import Cookies from "js-cookie";

export default {
  install: (app: App, options: ShopwareFrontendsOptions) => {
    ...
  },
};

```

We prepare some types to be used during the registration of the plugin to pass basic credentials for your Shopware 6 instance.

```ts
export type ShopwareFrontendsOptions = {
  endpoint: string;
  accessToken: string;
  shopwareApiClient?: {
    timeout: number;
  };
  enableDevtools?: boolean;
};
```

Now, once the plugin is created, we need to create an API client instance and the Shopware instance for Vue application.

The install method is a good place to do that:

```ts
const cookieContextToken = Cookies.get("sw-context-token");
const cookieLanguageId = Cookies.get("sw-language-id");

const contextToken = ref(cookieContextToken);
const languageId = ref(cookieLanguageId);

const instance = createInstance({
  endpoint: options.endpoint,
  accessToken: options.accessToken,
  timeout: options.shopwareApiClient?.timeout || 5000,
  contextToken: contextToken.value,
  languageId: languageId.value,
});
```

## Handle client state

:::tip Code example
Complete code example can be found [HERE](./custom-vue-project.html#plugin-code) you can find a full example of the plugin
:::

Now, we need to ensure that the context token, which identifies a user session, is properly stored and updated. The context token may change after operations like login or logout.

Then, we can take advantage of the onConfigChange method. It executes when the API client detects a new value of the context token coming from the API (as a header parameter or in the response body). In that case, the new context token should be saved in the cookie to keep the correct session:

```ts
/**
 * Save current contextToken when it changes
 */
instance.onConfigChange(({ config }) => {
  try {
    Cookies.set("sw-context-token", config.contextToken || "", {
      expires: 365,
      sameSite: "Lax",
      path: "/",
    });
    Cookies.set("sw-language-id", config.languageId || "", {
      expires: 365,
      sameSite: "Lax",
      path: "/",
    });

    contextToken.value = config.contextToken;
    languageId.value = config.languageId;
  } catch (e) {
    // Sometimes cookie is set on server after request is send, it can fail silently
  }
});
```

Another step is to create a Shopware instance that combines API Client and the business logic in composables to be used in entire Vue application:

```ts
const shopwareContext = createShopwareContext(app, {
  enableDevtools: !!options.enableDevtools, // decide if devtools should be enabled
});
```

And the last step is to provide the shopwareContext:

```ts
app.provide("apiClient", apiClient);
app.provide("shopware", shopwareContext);
// thanks to this, `shopwareContext` can be injected in a component and other Vue-instance-aware places (like composables).
app.provide("swSessionContext", ref());
```

## Register the plugin

```ts{6,9-14}
// main.ts
import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";
// import previously implemented module
import ShopwareFrontends from "./plugins/vue-shopware-frontends";
const app = createApp(App);

app.use(ShopwareFrontends, {
    // pass options described under ShopwareFrontendsOptions type in the previous section
    endpoint: "https://demo-frontends.swstage.store",
    accessToken: "SWSCBHFSNTVMAWNZDNFKSHLAYW",
    apiDefaults: {},
});

app.mount("#app");
```

## Plugin code

```ts
// ./plugins/vue-shopware-frontends.ts file
import { ref } from "vue";
import type { App } from "vue";
import { createAPIClient } from "@shopware/api-client";
import { createShopwareContext } from "@shopware/composables";
import Cookies from "js-cookie";

// Types to be used during the registration of the plugin to pass basic credentials for your Shopware 6 instance.
export type ShopwareFrontendsOptions = {
  endpoint: string;
  accessToken: string;
  shopwareApiClient?: {
    timeout: number;
  };
  enableDevtools?: boolean;
};

export default {
  install: (app: App, options: ShopwareFrontendsOptions) => {
    const cookieContextToken = Cookies.get("sw-context-token");
    const cookieLanguageId = Cookies.get("sw-language-id");

    const contextToken = ref(cookieContextToken);
    const languageId = ref(cookieLanguageId);

    const apiClient = createAPIClient<operations>({
      baseURL: options.endpoint,
      accessToken: options.accessToken,
      contextToken: contextToken.value,
    });

    const shopwareContext = createShopwareContext(app, {
      enableDevtools: !!options.enableDevtools,
    });

    app.provide("apiClient", apiClient);
    app.provide("shopware", shopwareContext);
    app.provide("swSessionContext", ref());
  },
};
```

## Shopware Endpoint on the SSR mode

It may happen that for SSR and CSR, you need two different shopware endpoints. One of the most common situations is when you are using an internal network for communication between apps.

```
Server URL to the backend: http://shopware (not exposed)
Client URL to the backend  https://demo-frontends.shopware.store (exposed)
```

If you are using the Nuxt plugin, you can set private and public envs:

```
NUXT_SHOPWARE_ENDPOINT=http://shopware
NUXT_PUBLIC_SHOPWARE_ENDPOINT=https://demo-frontends.shopware.store
```

Otherwise, make sure that you are setting different values on the create instance phase

```ts
const instance = createInstance({
  endpoint: ssrValue || clientValue,
  accessToken: options.accessToken,
  timeout: options.shopwareApiClient?.timeout || 5000,
  contextToken: contextToken.value,
  languageId: languageId.value,
});
```

:::warning
If you need to redirect your media, you can use the `shopware.yaml` file to configure the main media URL.
For more details, please visit this [site](https://developer.shopware.com/docs/guides/hosting/infrastructure/filesystem.html#flysystem-overview).
:::

## Next steps

After your setup, you can follow our building guides to get started with Shopware Frontends

---

---

## Demo Store Template
**Source:** [frontends/getting-started/templates/demo-store-template.md](https://developer.shopware.com/frontends/getting-started/templates/demo-store-template.md)  
# Demo Store Template

The demo store template is a reference implementation of an online store UI.

:::info
The **Demo Store Template** is a reference implementation. It is under constant development and is not subject to versioning. Please go to [Limitations](#limitations) for more information.
:::

## Setup & run

Alternatively, set up the vue-demo-store template manually by running the following commands in a new directory:

```bash
npx tiged shopware/frontends/templates/vue-demo-store demo-store && cd demo-store
npm i && npm run dev
```

The vue-demo-store template is connected to a Shopware Cloud instance by default. However, you can change the [configuration](#configure) to use your own instance.

We recommend using [devenv](https://developer.shopware.com/docs/guides/installation/devenv.html) and Composable Frontends on your local machine. But if you want to use Docker and Composable Frontends, you should have a look at the [docker-composable-frontends](https://github.com/shopwareLabs/docker-composable-frontends) repository.

## Directory structure

The directory structure is the same as in a [default Nuxt project](https://nuxtjs.org/docs/get-started/directory-structure/):

```json
demo-store/
├─ components/
|  ├─ layout/       /* header, footer, account menu etc. */
|  ├─ checkout/     /* cart items, cart overview */
|  ├─ account/      /* order history, account settings */
|  ├─ shared/       /* modals, notifications */
|  ├─ ...
├─ layouts/
│  ├─ checkout.vue  /* minimal layout without navigation and footer */
│  ├─ default.vue   /* default layout with navigation and footer */
├─ pages/
│  ├─ checkout/     /* checkout pages */
│  ├─ account/      /* user account pages */
│  ├─ ...
├─ app.vue          /* app root component */
├─ nuxt.config.ts   /* app configuration */
├─ package.json
├─ tsconfig.json
```

The `components` directory contains components that have been extracted from their corresponding page components, so these become more readable. The components within `components` are organized based on the page and layout components they are used in. The `shared` directory contains generic components that are used across multiple pages and layouts.

## Customizing the template

There is no concept of overwriting components in the demo store template. Instead, all components are modified directly. When you create a new project, we recommend adding your custom Git repository as a remote repository and keeping the original demo store template as a second repository so that you can always pull changes manually (see als Git Docu [Working with Remotes](https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes)).

:::warning Updates & Breaking Changes
The demo store template is a boilerplate, so it will constantly be updated, as we will continously add new features and make improvements. These updates include breaking changes. If you want to stay up to date with the latest changes, you need to keep your project in sync manually.
:::

### CMS Components

One exception to the rule are CMS components. CMS components are handled as a separate package `cms-base` in Shopware Frontends and can be updated automatically. However, you can still override the components from the package in your custom project.

## Configure

The blank template is pre-configured to connect to a public Shopware backend, so you start building right away.

In order to connect it to your own store backend, you need to edit the `nuxt.config.ts` file and edit a configuration object with `shopware` as a key:

```ts
/* ... */
export default defineNuxtConfig({
  runtimeConfig: {
    // shopware: {
    /**
     * SSR Shopware Endpoint
     * More here: https://frontends.shopware.com/getting-started/templates/custom-vue-project.html#shopware-endpoint-on-the-ssr-mode
     */
    //   endpoint: ""
    // },
    public: {
      shopware: {
        endpoint: "https://your-business.shopware.store",
        accessToken: "access-token-from-settings",
      },
    },
  },
});
```

You can also use `.env` file to override this configuration. More about this you can find [here](https://nuxt.com/docs/guide/going-further/runtime-config#environment-variables)

## Limitations

The **Demo Store Template** suggests how to build a store UI with Shopware Frontends. It does not make any assumptions about custom implementations and hence does not contain every feature of Shopware.

Some important limitations are

* Frontend settings are not synchronized from the backend - such as
  * Available fields for checkout and registration
* Not all Plugins or Apps are API aware
* Not all Commercial features are supported, check the [Commercial Integrations](../../resources/integrations/commercial/) page

If you think a specific feature should be part of the demo store template, feel free to create an [issue](https://github.com/shopware/frontends/issues/new) or make a [contribution](https://github.com/shopware/frontends/pulls).

---

---

## Vue Starter Template Extended
**Source:** [frontends/getting-started/templates/vue-starter-template-extended.md](https://developer.shopware.com/frontends/getting-started/templates/vue-starter-template-extended.md)  
# Vue Starter Template Extended

The Vue Starter Template Extended (Lumora Demo Store) is an example implementation that demonstrates how to extend the Vue Starter Template using [Nuxt layers](https://nuxt.com/docs/getting-started/layers). This approach allows you to inherit all features from a base template while maintaining only your customizations.

:::tip Learn by Example
This template showcases the **Nuxt layer pattern** - a powerful way to create brand-specific storefronts without code duplication.
:::

## Setup & run

Set up the vue-starter-template-extended manually by running the following commands in a new directory:

```bash
npx tiged shopware/frontends/templates/vue-starter-template-extended lumora-store && cd lumora-store
npm i && npm run dev
```

## What is Lumora?

Lumora is a fictional brand selling modern home scents (candles, reed diffusers, and room sprays). The template demonstrates how to:

* Extend an existing template using Nuxt layers
* Customize the theme with brand colors
* Override specific configurations
* Maintain a minimal, focused codebase

## How It Works: Nuxt Layers

### Layer Architecture

This template extends the Vue Starter Template using Nuxt's layer system:

```ts
// nuxt.config.ts
export default defineNuxtConfig({
  extends: ["../vue-starter-template"],  // Extend base template
  // ... Lumora-specific configuration
})
```

### What You Inherit

By extending the base template, you automatically get:

* ✅ All page components (navigation, product, checkout, etc.)
* ✅ All layout components (headers, footers, forms)
* ✅ All composables and business logic
* ✅ CMS integration
* ✅ i18n support
* ✅ Type generation setup

### What You Customize

The extended template contains only:

```
lumora-store/
├─ app/
│  └─ app.config.ts        # Brand customizations (colors, settings)
├─ public/                  # Brand-specific assets (logo, favicon)
├─ nuxt.config.ts          # Layer configuration
├─ uno.config.ts           # Custom theme styles
└─ package.json            # Dependencies
```

## Customization Example

### Brand Color Configuration

The template demonstrates how to customize the image placeholder color using `app.config.ts`:

```ts
// app/app.config.ts
export default defineAppConfig({
  imagePlaceholder: {
    color: "#B38A65",  // Lumora brand-primary color
  },
});
```

This setting is used by the `useImagePlaceholder` composable from `@shopware/cms-base-layer`.

### Theme Customization

Custom UnoCSS configuration in `uno.config.ts` adds Lumora-specific styles:

```ts
// uno.config.ts
export default mergeConfigs([config, {
  theme: {
    colors: {
      'brand-primary': '#B38A65',
      'brand-secondary': '#2C2C2C',
    },
  },
}])
```

## Overriding Components

To override a component from the base template, create a file with the same name in your `app/components/` directory:

```
lumora-store/
  app/
    components/
      SwProductCard.vue  # Overrides base SwProductCard
      layout/
        LayoutHeader.vue # Overrides base header
```

Nuxt automatically prioritizes your local components over the base template components.

## Benefits of the Layer Approach

### 1. Minimal Code Duplication

Only maintain code that differs from the base template. In this example, the entire Lumora store is customized with just a few files.

### 2. Automatic Updates

When the base template improves (bug fixes, new features), you can update it without touching your customizations:

```bash
# Update base template dependency
npm update vue-starter-template
```

### 3. Multiple Brands

Create multiple brand variants from a single base:

```
my-monorepo/
├─ vue-starter-template/      # Base template
├─ lumora-store/              # Brand A (extends base)
├─ another-brand/             # Brand B (extends base)
└─ premium-brand/             # Brand C (extends base)
```

### 4. Clean Separation

Your brand-specific code stays separate from the framework code, making it easier to:

* Understand what's custom vs. standard
* Update dependencies safely
* Test customizations in isolation

## Using Layers in Your Project

### Extend from npm Package

Instead of a local path, you can extend from an npm package:

```ts
// nuxt.config.ts
export default defineNuxtConfig({
  extends: ["@your-company/store-base"],
  // ... your customizations
})
```

### Extend Multiple Layers

You can extend multiple layers:

```ts
// nuxt.config.ts
export default defineNuxtConfig({
  extends: [
    "@your-company/store-base",
    "@your-company/payment-layer",
  ],
})
```

## Production Deployment

The extended template can be deployed like any Nuxt application:

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

## Learn More

---

---

## Vue Starter Template
**Source:** [frontends/getting-started/templates/vue-starter-template.md](https://developer.shopware.com/frontends/getting-started/templates/vue-starter-template.md)  
# Vue Starter Template

The Vue Starter Template is a production-ready Nuxt application with all Shopware Frontends core packages pre-configured. It provides a clean foundation for building your custom storefront without the demo content or boilerplate UI found in the Demo Store Template.

:::tip Production Ready
Unlike the Demo Store Template, the **Vue Starter Template** is designed for production use and can be used as a foundation for your custom storefront.
:::

## Setup & run

Alternatively, set up the vue-starter-template manually by running the following commands in a new directory:

```bash
npx tiged shopware/frontends/templates/vue-starter-template my-store && cd my-store
npm i && npm run dev
```

The vue-starter-template is connected to a Shopware Cloud instance by default. However, you can change the [configuration](#configure) to use your own instance.

## What's Included

The template comes with:

* **Nuxt 4.x** - Latest Nuxt framework with full SSR support
* **All core packages** - Pre-installed and configured:
  * `@shopware/api-client` - HTTP client for Shopware API
  * `@shopware/composables` - Vue composables for business logic
  * `@shopware/helpers` - Utility functions
  * `@shopware/cms-base-layer` - CMS component integration
  * `@shopware/nuxt-module` - Nuxt module for Shopware
* **UnoCSS** - Utility-first CSS framework (Tailwind-compatible)
* **i18n support** - Internationalization ready
* **TypeScript** - Full type safety with generated Shopware types
* **Type generation** - Script to generate types from your Shopware instance

## Directory Structure

The directory structure follows [Nuxt conventions](https://nuxt.com/docs/guide/directory-structure):

```
vue-starter-template/
├─ app/
│  ├─ components/      /* Your custom components */
│  ├─ pages/           /* Page components */
│  ├─ layouts/         /* Layout components */
│  └─ ...
├─ public/             /* Static assets */
├─ nuxt.config.ts      /* Nuxt configuration */
├─ uno.config.ts       /* UnoCSS configuration */
├─ package.json
├─ tsconfig.json
```

## Configure

### Shopware Connection

To connect to your own Shopware instance, edit the `nuxt.config.ts` file:

```ts
export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      shopware: {
        endpoint: "https://your-shop.shopware.store/store-api",
        accessToken: "your-access-token",
      },
    },
  },
});
```

You can also use a `.env` file to override configuration:

```bash
NUXT_PUBLIC_SHOPWARE_ENDPOINT=https://your-shop.shopware.store/store-api
NUXT_PUBLIC_SHOPWARE_ACCESS_TOKEN=your-access-token
```

### Generate Types

After connecting to your Shopware instance, generate TypeScript types:

```bash
npm run generate-types
```

This command uses `@shopware/api-gen` to create type definitions based on your Shopware configuration.

## Customizing

### Adding Components

Create components in the `app/components/` directory. They will be auto-imported:

```vue
<!-- app/components/MyCustomButton.vue -->
<template>
  <button class="px-4 py-2 bg-brand-primary text-brand-on-primary rounded">
    <slot />
  </button>
</template>
```

### Override CMS Components

The template uses `@shopware/cms-base-layer` for CMS integration. You can override any CMS component by creating a file with the same name in your `app/components/` directory.

For example, to override the product card:

```vue
<!-- app/components/SwProductCard.vue -->
<template>
  <!-- Your custom product card implementation -->
</template>
```

### Styling with UnoCSS

The template uses UnoCSS (Tailwind-compatible). Customize your theme in `uno.config.ts`:

```ts
import { mergeConfigs } from '@unocss/core'
import config from './.nuxt/uno.config.mjs'

export default mergeConfigs([config, {
  theme: {
    colors: {
      primary: '#your-brand-color',
      secondary: '#your-secondary-color',
    },
  },
}])
```

## Extending with Layers

The Vue Starter Template can be extended using [Nuxt layers](https://nuxt.com/docs/getting-started/layers), allowing you to:

* Inherit all features from the base template
* Override only specific components
* Maintain multiple brand variants from a single base
* Keep your customizations separate and maintainable

## What's Next?

---

---

## Demo Store Template
**Source:** [frontends/installation.md](https://developer.shopware.com/frontends/installation.md)  
# Demo Store Template

The demo store template is a reference implementation of an online store UI.

:::info
The **Demo Store Template** is not suitable for production stores. It is under constant development and does not adhere to any versioning. Please go to [Limitations](#limitations) for more information.
:::

## Setup & run

Alternatively, set up the vue-demo-store template manually by running the following commands in a new directory:

```bash
npx tiged shopware/frontends/templates/vue-demo-store demo-store && cd demo-store
npm i && npm run dev
```

## Directory structure

The directory structure is the same as in a [default Nuxt project](https://nuxtjs.org/docs/get-started/directory-structure/):

```json
demo-store/
├─ components/
|  ├─ layout/       /* header, footer, account menu etc. */
|  ├─ checkout/     /* cart items, cart overview */
|  ├─ account/      /* order history, account settings */
|  ├─ shared/       /* modals, notifications */
|  ├─ ...
├─ layouts/
│  ├─ checkout.vue  /* minimal layout without navigation and footer */
│  ├─ default.vue   /* default layout with navigation and footer */
├─ pages/
│  ├─ checkout/     /* checkout pages */
│  ├─ account/      /* user account pages */
│  ├─ ...
├─ app.vue          /* app root component */
├─ nuxt.config.ts   /* app configuration */
├─ package.json
├─ tsconfig.json
```

The `components` directory contains components that have been extracted from their corresponding page components, so these become more readable. The components within `components` are organized based on the page and layout components they are used in. The `shared` directory contains generic components that are used across multiple pages and layouts.

## Customizing the template

There is no concept of overwriting components in the demo store template. Instead, all components are modified directly. When you create a new project, we recommend adding your custom Git repository as a remote repository and keeping the original demo store template as a second repository so that you can always pull changes manually (see als Git Docu [Working with Remotes](https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes)).

:::warning Updates & Breaking Changes
The demo store template is a boilerplate, so it will constantly be updated, as we will continously add new features and make improvements. These updates include breaking changes. If you want to stay up to date with the latest changes, you need to keep your project in sync manually.
:::

### CMS Components

One exception to the rule are CMS components. CMS components are handled as a separate package `cms-base` in Shopware Frontends and can be updated automatically. However, you can still override the components from the package in your custom project.

## Configure

The blank template is pre-configured to connect to a public Shopware backend, so you start building right away.

In order to connect it to your own store backend, you need to edit the `nuxt.config.ts` file and edit a configuration object with `shopware` as a key:

```ts
/* ... */
export default defineNuxtConfig({
  runtimeConfig: {
    // shopware: {
    /**
     * SSR Shopware Endpoint
     * More here: https://frontends.shopware.com/getting-started/templates/custom-vue-project.html#shopware-endpoint-on-the-ssr-mode
     */
    //   endpoint: ""
    // },
    public: {
      shopware: {
        endpoint: "https://your-business.shopware.store",
        accessToken: "access-token-from-settings",
      },
    },
  },
});
```

You can also use `.env` file to override this configuration. More about this you can find [here](https://nuxt.com/docs/guide/going-further/runtime-config#environment-variables)

## Limitations

The **Demo Store Template** suggests how to build a store UI with Shopware Frontends. It does not make any assumptions about custom implementations and hence does not contain every feature of Shopware.

Some important limitations are

* Frontend settings are not synchronized from the backend - such as
  * Available fields for checkout and registration
  * Multiple domains
  * Translations and snippets
* No support for multiple currencies

If you think a specific feature should be part of the demo store template, feel free to create an [issue](https://github.com/shopware/frontends/issues/new) or make a [contribution](https://github.com/shopware/frontends/pulls).

---

---

## Overview
**Source:** [frontends/overview.md](https://developer.shopware.com/frontends/overview.md)  
# Overview

Shopware Composable Frontends is Shopware's toolkit for creating platform-agnostic custom storefronts. The demo store implementation is based on Vue.js and Nuxt3.

## Quick Links

* **Announcements**: To keep yourself up to date with the latest news regarding the project, please regularly check our Github Discussions page: [shopware/frontends/dicsussions](https://github.com/shopware/frontends/discussions). Especially the [Announcements](https://github.com/shopware/frontends/discussions/categories/announcements) category.

## How Shopware Frontends work?

Frontends is a collection of multiple packages that you can use to implement your custom storefront project.

## Data Sources

Shopware 6 is considered one "supported" data source, but you can integrate any other data source you like - such as CMS or analytics. Shopware Frontends uses the Store API to connect with your Shopware 6 instance at runtime.

## Logic

A big part (and a risk factor) of every custom storefront project is the implementation of domain-specific business functionality. That's why Shopware Frontends offers various packages that take care of some heavy lifting:

* Routing
* Shopping worlds (Shopware CMS) integration
* Product searches and filters
* Price formatting
* Authentication & state handling

It also comes with TypeScript support.

## Template/UI

You can decide to start from scratch and use no template at all, but we recommend looking at our [Templates](./getting-started/templates.html) which are based on **Nuxt.js** and **Tailwind CSS**.

---

---

## PACKAGE REFERENCE
**Source:** [frontends/packages.md](https://developer.shopware.com/frontends/packages.md)  
# PACKAGE REFERENCE

---

---

## frontends/packages/api-client.md
**Source:** [frontends/packages/api-client.md](https://developer.shopware.com/frontends/packages/api-client.md)  
---

---

## frontends/packages/cms-base-layer.md
**Source:** [frontends/packages/cms-base-layer.md](https://developer.shopware.com/frontends/packages/cms-base-layer.md)  
---

---

## Composables list
**Source:** [frontends/packages/composables.md](https://developer.shopware.com/frontends/packages/composables.md)  
{{INTRO}}

## Composables list

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useAddToCart.md](https://developer.shopware.com/frontends/packages/composables/useAddToCart.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useAddress.md](https://developer.shopware.com/frontends/packages/composables/useAddress.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useB2bQuoteManagement.md](https://developer.shopware.com/frontends/packages/composables/useB2bQuoteManagement.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useBreadcrumbs.md](https://developer.shopware.com/frontends/packages/composables/useBreadcrumbs.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useCart.md](https://developer.shopware.com/frontends/packages/composables/useCart.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useCartErrorParamsResolver.md](https://developer.shopware.com/frontends/packages/composables/useCartErrorParamsResolver.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useCartItem.md](https://developer.shopware.com/frontends/packages/composables/useCartItem.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useCartNotification.md](https://developer.shopware.com/frontends/packages/composables/useCartNotification.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useCategory.md](https://developer.shopware.com/frontends/packages/composables/useCategory.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useCategorySearch.md](https://developer.shopware.com/frontends/packages/composables/useCategorySearch.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useCheckout.md](https://developer.shopware.com/frontends/packages/composables/useCheckout.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useCmsBlock.md](https://developer.shopware.com/frontends/packages/composables/useCmsBlock.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useCmsMeta.md](https://developer.shopware.com/frontends/packages/composables/useCmsMeta.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useCmsSection.md](https://developer.shopware.com/frontends/packages/composables/useCmsSection.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useCmsTranslations.md](https://developer.shopware.com/frontends/packages/composables/useCmsTranslations.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useContext.md](https://developer.shopware.com/frontends/packages/composables/useContext.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useCountries.md](https://developer.shopware.com/frontends/packages/composables/useCountries.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useCustomerOrders.md](https://developer.shopware.com/frontends/packages/composables/useCustomerOrders.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useCustomerPassword.md](https://developer.shopware.com/frontends/packages/composables/useCustomerPassword.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useDefaultOrderAssociations.md](https://developer.shopware.com/frontends/packages/composables/useDefaultOrderAssociations.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useInternationalization.md](https://developer.shopware.com/frontends/packages/composables/useInternationalization.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useLandingSearch.md](https://developer.shopware.com/frontends/packages/composables/useLandingSearch.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useListing.md](https://developer.shopware.com/frontends/packages/composables/useListing.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useLocalWishlist.md](https://developer.shopware.com/frontends/packages/composables/useLocalWishlist.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useNavigation.md](https://developer.shopware.com/frontends/packages/composables/useNavigation.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useNavigationContext.md](https://developer.shopware.com/frontends/packages/composables/useNavigationContext.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useNavigationSearch.md](https://developer.shopware.com/frontends/packages/composables/useNavigationSearch.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useNewsletter.md](https://developer.shopware.com/frontends/packages/composables/useNewsletter.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useNotifications.md](https://developer.shopware.com/frontends/packages/composables/useNotifications.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useOrderDetails.md](https://developer.shopware.com/frontends/packages/composables/useOrderDetails.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useOrderPayment.md](https://developer.shopware.com/frontends/packages/composables/useOrderPayment.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/usePrice.md](https://developer.shopware.com/frontends/packages/composables/usePrice.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useProduct.md](https://developer.shopware.com/frontends/packages/composables/useProduct.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useProductAssociations.md](https://developer.shopware.com/frontends/packages/composables/useProductAssociations.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useProductConfigurator.md](https://developer.shopware.com/frontends/packages/composables/useProductConfigurator.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useProductPrice.md](https://developer.shopware.com/frontends/packages/composables/useProductPrice.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useProductReviews.md](https://developer.shopware.com/frontends/packages/composables/useProductReviews.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useProductSearch.md](https://developer.shopware.com/frontends/packages/composables/useProductSearch.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useProductSearchSuggest.md](https://developer.shopware.com/frontends/packages/composables/useProductSearchSuggest.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useProductWishlist.md](https://developer.shopware.com/frontends/packages/composables/useProductWishlist.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useSalutations.md](https://developer.shopware.com/frontends/packages/composables/useSalutations.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useSessionContext.md](https://developer.shopware.com/frontends/packages/composables/useSessionContext.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useShopwareContext.md](https://developer.shopware.com/frontends/packages/composables/useShopwareContext.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useSyncWishlist.md](https://developer.shopware.com/frontends/packages/composables/useSyncWishlist.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useUrlResolver.md](https://developer.shopware.com/frontends/packages/composables/useUrlResolver.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useUser.md](https://developer.shopware.com/frontends/packages/composables/useUser.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## {{NAME}}
**Source:** [frontends/packages/composables/useWishlist.md](https://developer.shopware.com/frontends/packages/composables/useWishlist.md)  
# {{NAME}}

{{DESCRIPTION}}

{{ADDITIONAL\_README}}

{{DEMO\_BLOCK}}

## Types

{{INTERFACE\_CONTENT}}

{{RETURN\_TYPES\_CONTENT}}

---

---

## frontends/packages/helpers.md
**Source:** [frontends/packages/helpers.md](https://developer.shopware.com/frontends/packages/helpers.md)  
---

---

## frontends/packages/nuxt-module.md
**Source:** [frontends/packages/nuxt-module.md](https://developer.shopware.com/frontends/packages/nuxt-module.md)  
---

---

## RESOURCES
**Source:** [frontends/resources.md](https://developer.shopware.com/frontends/resources.md)  
# RESOURCES

---

---

## 🤗 Community Modules
**Source:** [frontends/resources/community-modules.md](https://developer.shopware.com/frontends/resources/community-modules.md)  
# 🤗 Community Modules

:::warning
The modules listed here are not officially supported or maintained by Shopware. Please use them at your own risk.
:::

The following section contains modules, plugins and other resources that are created and maintaned by the community. If you want to contribute to this list, please create a [pull request](https://github.com/shopware/frontends/pulls) or submit a new [idea](https://github.com/shopware/frontends/discussions/categories/ideas).

---

---

## 🛠️ Integrations
**Source:** [frontends/resources/integrations.md](https://developer.shopware.com/frontends/resources/integrations.md)  
# 🛠️ Integrations

This is your go-to resource for seamlessly incorporating various platforms into Shopware Composable Frontends. Explore the following sub-pages to find detailed instructions on integrating different systems,
ensuring a harmonious and efficient synergy between your Shopware store and diverse external services.

## Overview

---

---

## CMS Integrations
**Source:** [frontends/resources/integrations/cms.md](https://developer.shopware.com/frontends/resources/integrations/cms.md)  
# CMS Integrations

## Overview

---

---

## Storyblok Integration
**Source:** [frontends/resources/integrations/cms/storyblok.md](https://developer.shopware.com/frontends/resources/integrations/cms/storyblok.md)  
# Storyblok Integration




Storyblok is a headless CMS that can be easily integrated into any Nuxt 3 application.
On this page we explain the basics of how to integrate it into our [vue-blank template](../../../getting-started/templates/blank-template).

## Step by step guide

1. Checkout the vue-blank template\
   `pnpx tiged shopware/frontends/templates/vue-blank vue-blank-storyblok && cd vue-blank-storyblok`

2. Install the dependencies and run the dev server\
   `pnpm i && pnpm run dev`

3. Install the [storyblok nuxt module](https://nuxt.com/modules/storyblok)\
   `pnpx nuxi@latest module add storyblok`

4. Install the [storyblok vue](https://github.com/storyblok/storyblok-vue) dependency\
   `pnpm add @storyblok/vue -D`

5. Now add the storyblok access token to you `nuxt.config.ts` file\
   *(you need a storyblok account to get that token)*
   ```ts
   modules: ["@shopware/nuxt-module", "@storyblok/nuxt"],
     storyblok: {
     accessToken: "super-secret-token"
   },
   ```

6. In the root directory of your project create a `storyblok` folder.

7. Let's create our base components files inside our `vue-blank-storyblok/storyblok` folder

   **Feature.vue**

   ```vue
   <script setup>
   defineProps({ blok: Object });
   </script>

   <template>
     <div v-editable="blok" class="py-2" data-test="feature">
       <h1 class="text-lg">{{ blok.name }}</h1>
     </div>
   </template>
   ```

   **Grid.vue**

   ```vue
   <script setup>
   defineProps({ blok: Object });
   </script>

   <template>
     <div v-editable="blok" class="flex py-8 mb-6" data-test="grid">
       <div
         v-for="blok in blok.columns"
         :key="blok._uid"
         class="flex-auto px-6"
       >
         <StoryblokComponent :blok="blok" />
       </div>
     </div>
   </template>
   ```

   **Page.vue**

   ```vue
   <script setup>
   defineProps({ blok: Object });
   </script>

   <template>
     <div v-editable="blok" class="px-6" data-test="page">
       <StoryblokComponent
         v-for="blok in blok.body"
         :key="blok._uid"
         :blok="blok"
       />
     </div>
   </template>
   ```

   **Teaser.vue**

   ```vue
   <script setup>
   defineProps({ blok: Object });
   </script>

   <template>
     <div
       v-editable="blok"
       :cat="$attrs.cat"
       class="py-8 mb-6 text-5xl font-bold text-center"
       data-test="teaser"
     >
       {{ blok.headline }}
     </div>
   </template>
   ```

8. Change the `app.vue` file, we adding the `NuxtLayout` and `NuxtPage` components.

   ```vue
   <script setup lang="ts">
   const { refreshSessionContext } = useSessionContext();

   onMounted(() => {
     refreshSessionContext();
   });
   </script>

   <template>
     <NuxtLayout>
       <NuxtPage />
     </NuxtLayout>
   </template>
   <style>
   @import "./style.css";
   </style>
   ```

9. Create `pages/[...all].vue` and `pages/storyblok/[slug].vue` files

   **\[...all].vue**

   ```vue
   <script setup lang="ts">
   import Frontends from "../components/Frontends.vue";
   </script>

   <template>
     <div id="app">
       <Frontends template="Blank Vue 3 template (Nuxt)" />
       <NuxtLink to="storyblok/home">Storyblok Home</NuxtLink>
     </div>
   </template>
   <style>
   @import "../style.css";
   </style>
   ```

   **storyblok/\[slug].vue**

   ```vue
   <script setup lang="ts">
   const route = useRoute();
   const slug = route.params.slug.toString() ?? "home";
   const story = await useAsyncStoryblok(
     slug,
     { version: "draft", resolve_relations: "Article.author" }, // API Options
     { resolveRelations: ["Article.author"], resolveLinks: "url" }, // Bridge Options
   );
   if (story.value.status) {
     throw createError({
       statusCode: story.value.status,
       statusMessage: story.value.response,
     });
   }
   </script>

   <template>
     <StoryblokComponent v-if="story" :blok="story.content" />
   </template>
   ```

10. Log into your storyblok account and create a page called **home** inside the content.\
    We already linked the slug "home" inside our `[...all].vue` file.


11. Now start you local dev server and open `http://localhost:3000/storyblok/home`.\
    You should see a page looking like the screen below.


12. Optional: [Add UnoCSS](https://unocss.dev/integrations/nuxt) for Tailwind CSS support.\
    We already used some Tailwind Classes in the templates.

### Further topics

* [Create a Preview Environment for Your Nuxt 3 Website](https://www.storyblok.com/tp/create-a-preview-environment-for-your-nuxt-3-website)

---

---

## Strapi Integration
**Source:** [frontends/resources/integrations/cms/strapi.md](https://developer.shopware.com/frontends/resources/integrations/cms/strapi.md)  
# Strapi Integration




Strapi is a headless CMS that can be integrated with the Composable Frontends.
This example requires NUXT 3 instance.

### How to install

Add Strapi Nuxt module as a dev dependencies

```cmd
pnpm add -D @nuxtjs/strapi
```

Update Nuxt config `nuxt.config.ts`

```js
export default {
  modules: ["@nuxtjs/strapi"],
};
```

More about installation can be found [HERE](https://strapi.nuxtjs.org/setup)

### Cases of use

## Fetching and displaying single element

As a example we will add a global banner to our demo shop.
At the beginning we created a single type on the Strapi collection, with fallowing fields

```ts
interface {
  text: string; // short input field - this will represent a text that we want to display in the banner
  color: string; // short input field - this will represent a color of the banner (this can be done also with color picker filed, but for this example we will use input text)
}

```

The next step is to create a banner component

```vue
<script setup lang="ts">
interface GlobalBanner {
  text: string;
  color: string;
}

const { findOne } = useStrapi();

const { data } = await findOne<GlobalBanner>("global-banner");
const bgColor = computed(() => data.attributes?.color || "#fff");
</script>
<template>
  <section>
    <div class="text-center py-1" :style="{ 'background-color': bgColor }">
      {{ data.attributes.text }}
    </div>
  </section>
</template>
```

Now we can add our component to the layout.
`frontends/templates/vue-demo-store/layouts/default.vue`

```vue
<template>
  <div>
    <GlobalBanner />
    <LayoutHeader />
    <LayoutNotifications />
    <main class="mx-auto">
      <slot />
    </main>
    <LayoutFooter />
  </div>
</template>
```

## Fetching and displaying pages

:::warning
This example is written for the vue-demo-store template and assuming that you [implemented Multiple CMS middleware](../../../getting-started/cms/multiple-cms#adding-middleware)
:::

Create new collection type `Page` on the Stripe admin site with fields:

```ts
interface {
  text: string; // Content page
  seoUrl: string; // Page slug
}
```

Composable for resolving components

```ts
interface StripePage {
  text: string;
  seoUrl: string;
}
export function useSWStrapi() {
  const getPage = async (route: string) => {
    const { findOne } = useStrapi();
    const response = await findOne<StripePage>("pages", undefined, {
      filters: {
        seoUrl: route,
      },
    });
    return response;
  };

  const resolveComponent = async (route: string) => {
    const page = await getPage(route);
    if (!page.data[0]) return null;
    return h("div", {}, page.data[0].attributes.text);
  };

  return {
    resolveComponent,
  };
}
```

Provide Strapi resolver to the `pageRenderMiddlewares`

```ts
const { resolveComponent } = useSWStrapi();
provide("pageRenderMiddlewares", resolveComponent);
```

---

---

## Commercial Integrations
**Source:** [frontends/resources/integrations/commercial.md](https://developer.shopware.com/frontends/resources/integrations/commercial.md)  
# Commercial Integrations

Here you will find all integration documents for the commercial features of Rise, Evolve and Beyond Plans for Shopware.

* [B2B Quick-Order](b2b-quick-order.html)
* [B2B Quote-Management](b2b-quote-management.html)
* [Custom Products](custom-products.html)
* [Digital Sales Rooms](digital-sales-rooms.html)

---

---

## frontends/resources/integrations/commercial/b2b-quick-order.md
**Source:** [frontends/resources/integrations/commercial/b2b-quick-order.md](https://developer.shopware.com/frontends/resources/integrations/commercial/b2b-quick-order.md)  
---

---

## B2B Quote Management
**Source:** [frontends/resources/integrations/commercial/b2b-quote-management.md](https://developer.shopware.com/frontends/resources/integrations/commercial/b2b-quote-management.md)  
# B2B Quote Management

In this chapter you will learn how to

* Request new quote
* Fetch a list of quote and display detail
* Decline quote
* Request change in quote
* Change payment or shipping in quote
* Create a order from a quote

## Quick reference

* [useB2bQuoteManagement](../../../packages/composables/useB2bQuoteManagement) is a composable used for a quote management

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
const { requestQuote } = UseB2bQuoteManagement();
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

## frontends/resources/integrations/commercial/custom-products.md
**Source:** [frontends/resources/integrations/commercial/custom-products.md](https://developer.shopware.com/frontends/resources/integrations/commercial/custom-products.md)  
---

---

## Digital Sales Rooms
**Source:** [frontends/resources/integrations/commercial/digital-sales-rooms.md](https://developer.shopware.com/frontends/resources/integrations/commercial/digital-sales-rooms.md)  
# Digital Sales Rooms

The Customer Documentation about the Admin Extension for Digital Sales Rooms can be found [here](https://docs.shopware.com/en/shopware-6-en/extensions/digital-sales-rooms).

---

---

## Payment Integrations
**Source:** [frontends/resources/integrations/payments.md](https://developer.shopware.com/frontends/resources/integrations/payments.md)  
# Payment Integrations

## Overview

---

---

## frontends/resources/integrations/payments/adyen.md
**Source:** [frontends/resources/integrations/payments/adyen.md](https://developer.shopware.com/frontends/resources/integrations/payments/adyen.md)  
---

---

## frontends/resources/integrations/payments/amazon-pay.md
**Source:** [frontends/resources/integrations/payments/amazon-pay.md](https://developer.shopware.com/frontends/resources/integrations/payments/amazon-pay.md)  
---

---

## PayPal Integration
**Source:** [frontends/resources/integrations/payments/paypal.md](https://developer.shopware.com/frontends/resources/integrations/payments/paypal.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# PayPal Integration

:::tip Advanced Guide - prior knowledge required
In order to follow this guide properly, we recommend that you get familiar with the payment flow and payment API concepts first.

* [Payment Flow in Shopware 6](https://developer.shopware.com/docs/concepts/commerce/checkout-concept/payments)
* [Payment API](https://shopware.stoplight.io/docs/store-api/8218801e50fe5-handling-the-payment)
  :::

In this chapter you will learn how to integrate a payment flow with Shopware Frontends. There are various ways in which payment providers integrate with Shopware's API, so it is likely that you need to consult the documentation of your payment provider to get the details.

This specific guides shows how to integrate the **PayPal Checkout** including **PayPal Express Checkout**. However, the general flow is the same for all payment providers, so you will be able to use this guide as a reference for different providers.

Specifically, you will learn how to

* Prepare the Shopware instance for taking PayPal payments
* Embed payment buttons in your frontend
* React on PayPal events to prepare and capture the payment

## Install the payment extension

Payment integrations require communication with the backend for various scenarios

* Create a PayPal order
* Inform PayPal which payment was selected
* Capture the user payment after approval from the provider
* Update the order status
* Notify customers on successful/failed payment
* Other actions that need additional credentials which should stay hidden (i.e. secret authorization tokens)

That's why the backend as a Payment middleware is a good option to store additional information, credentials, react on events and so on.

:::tip
Make sure that the Payment Provider you would like to install, provides also an interface to interact via Store-API for headless solutions, specially when it's a synchronous payment flow.
:::

The [SwagPayPal](https://github.com/shopware/SwagPayPal) extension is available on Shopware Cloud stores and also can be installed manually in self-managed instances. It provides useful endpoints to conduct payments with PayPal. We will be using two PayPal-specific endpoints in this guide:

### Create order

`/store-api/paypal/create-order`
`/store-api/paypal/express/create-order` (Express)

* Creates an order directly with PayPal which contains information about the cart and the user
* Updates an existing order if given an order ID
* Returns a payment intent token that identifies the order in PayPal

### Prepare checkout (Express)

`/store-api/paypal/express/prepare-checkout`

* Used after PayPal approved the payment process request
* Registers a customer based on PayPal account's data (name, address, email) and logs them in
* The API Client receives a new context token that points to the logged-in customer

## Embed Payment buttons

The next step is to embed the PayPal Checkout buttons in your frontend using the PayPal Javascript SDK. The SDK can be loaded from the PayPal CDN or using an npm package ([PayPal SDK Documentation](https://developer.paypal.com/sdk/js/configuration/)). In our example we're going to use the second option.

### Load the PayPal SDK

:::tip Client only
The PayPal SDK and all its methods should only be invoked on client side rendered pages.
:::

In a Vue component we can use the `loadScript` method from the [`@paypal/paypal-js`](https://www.npmjs.com/package/@paypal/paypal-js) npm package:

```ts
import { loadScript } from "@paypal/paypal-js";

loadScript({
  // client id is generated in the PayPal account's apps section
  "client-id":
    "AUAcLFoadrmy9JiW2cHgriy1mTy0MCqQOP_1SSeQEUArz_zPeF1VcNY2CCxcFBQpf_N4g1k5wFVNJ1Bk",
  currency: "EUR", // or use some reference to the current currency
  locale: "en_US", // as same as in the field above
});
```

Now, the `paypal` object will be available in the global `window` object.

Alternatively, the `loadScript` function returns a promise resolving to the paypal object. This can be useful if you want to load the script multiple times with different options. Note that you must delete `window.paypal` first.

### Register the buttons

In order to display a PayPal Button component, we need to mount it in the DOM.

```ts
const divContainer = ref();

// client only
window
  .paypal
  .Buttons({/** configuration skipped */})
  .render(divContainer)
// this script will mount the component in element `divContainer`
```

## React on PayPal events

Now, that the buttons are properly displayed, we need to react to two basic events.

* `createOrder`
* `onApprove`

There are additional events like `onInit`, `onClick`, `onCancel` or `onError` (and more) to be used on specific cases, which we are not going to cover in this guide.

### `createOrder` event

In the `creatOrder` callback, you need to prepare the PayPal order and return a token that identifies the order in PayPal. This token will be used later on to capture the payment.
It is called when the user clicks on the PayPal checkout button.

```ts
const divContainer = ref();

// client only
window
  .paypal
  .Buttons({
      createOrder: async (
        data: CreateOrderData,
        actions: CreateOrderActions
      ) => {
        const response = await apiClient.invoke(
          "createPayPalOrder post /store-api/paypal/create-order"
        );
        return response.data?.token;
      },
  })
  .render(divContainer)
```

### `createOrder` event (Express)

In the `creatOrder` callback, you need to prepare the PayPal order and return a token that identifies the order in PayPal. This token will be used later on to capture the payment.
It is called when the user clicks on the PayPal express checkout button.

```ts
const divContainer = ref();

// client only
window
  .paypal
  .Buttons({
      createOrder: async (
        data: CreateOrderData,
        actions: CreateOrderActions
      ) => {
        await setPaymentMethod(paypalMethod.value);

        await addToCart();

        const response = await apiClient.invoke(
          "createPayPalExpressOrder post /store-api/paypal/express/create-order"
        );
        return response.data?.token;
      },
  })
  .render(divContainer)
```

The approach here is to set the payment method internally, then add a current product to the cart, and then prepare a PayPal token to be used later on.

In the example above we do a couple of things:

1. Set the payment method for the current context
2. Add a product to the cart
3. Create a PayPal order and return the token

### `onApprove` event

This event is called when the user approves the payment process. It's the last step before the payment is captured.

```ts
  ...
  // part of window.paypal.Buttons({}) params
  onApprove: async (data: OnApproveData, actions: OnApproveActions) => {
    // createOrder from useCheckout composable
    orderCreated.value = await createOrder({
      paypalOrderId: data.orderID,
    });
    refreshCart()
    // apiClient from useShopwareContext composable
    const handlePaymentResponse = await apiClient.invoke(
      "handlePaymentMethod post /handle-payment",
      {
        query: {
          paypalOrderId: data.orderID,
        },
        body: {
          orderId: order.id,
          finishUrl: `${window.location.origin}/order/finish?order=${order.id}&success=true`,
        },
      },
    );
    // call the /payment/finalize-transaction endpoint
    await fetch(handlePaymentResponse.data.redirectUrl);
    // ...
  },
  ...
```

The example above shows the code that is executed after a payer approves the PayPal popup. This function calls `createOrder()` which creates an order through the Store-API. Once the order is created, its `id` can be used to invoke the `handle-payment` action to process payment. This action captures the money or redirects the user to an external payment gateway.

### `onApprove` event (Express)

This event is called when the user approves the payment process. It's the last step before the payment is captured.

```ts
  ...
  // part of window.paypal.Buttons({}) params
  onApprove: async (data: OnApproveData, actions: OnApproveActions) => {
    await apiClient.invoke(
      "preparePayPalExpressCheckout post /store-api/paypal/express/prepare-checkout",
      {
        body: { token: data.orderID },
      }
    );
    // createOrder from useCheckout composable
    const order = await createOrder({ paypalOrderId: data.orderID });
    refreshCart()

    // redirect to order confirmation site

    // - OR - one-click checkout
    const handlePaymentResponse = await apiClient.invoke(
      "handlePaymentMethod post /handle-payment",
      {
        query: {
          isPayPalExpressCheckout: true,
          paypalOrderId: data.orderID,
        },
        body: {
          orderId: order.id,
          finishUrl: `${window.location.origin}/order/finish?order=${order.id}&success=true`,
        },
      },
    );
    // call the /payment/finalize-transaction endpoint
    await fetch(handlePaymentResponse.data.redirectUrl);
    // ...
  },
  ...
```

The example above shows the code that is executed after a payer approves the PayPal popup. This function calls the `prepare-checkout` endpoint to register the upcoming PayPal transaction.

Thanks to the internal logic of the PayPal extension, the is already connected with the logged in customer. Now you can call `createOrder()` which creates an order through the Store-API. Once the order is created, its `id` can be used to invoke the `handle-payment` action to process payment. This action captures the money or redirects the user to an external payment gateway.

## Working example (Express)

The example shows the specific case, when a product can be bought in one action from the frontend.

## Integrating other PayPal payment methods

PayPal additionally provides Pay Later and Credit card (ACDC) alongside with a variety of alternative payment methods like Apple Pay, Google Pay or Venmo.
For reference check out [PayPal's documentation](https://developer.paypal.com/docs/checkout/) on integrating these.

### Shared behaviour of `createOrder` and `onApprove`

The `createOrder` and `onApprove` events are the same for all payment methods.
The only difference is the product used to create the order.

```ts
async function createOrder(product?: 'paylater' | 'acdc' | 'applepay' | 'googlepay' | 'applepay' | 'venmo') {
  const response = await apiClient.invoke(
    "createPayPalOrder post /store-api/paypal/create-order",
    { body: { product } },
  );

  return response?.data?.token;
}

async function onApprove(data: { orderID: string }) {
  // createOrder from useCheckout composable
  orderCreated.value = await createOrder({
    paypalOrderId: data.orderID,
  });
  refreshCart()
  // apiClient from useShopwareContext composable
  const handlePaymentResponse = await apiClient.invoke(
    "handlePaymentMethod post /handle-payment",
    {
      query: {
        paypalOrderId: data.orderID,
      },
      body: {
        orderId: order.id,
        finishUrl: `${window.location.origin}/order/finish?order=${order.id}&success=true`,
      },
    },
  );
  // call the /payment/finalize-transaction endpoint
  await fetch(handlePaymentResponse.data.redirectUrl);
  ...
}
```

### Load the PayPal SDK including the additional payment methods

Depending on the type of the payment method and how it integrates with PayPal, you need to add it to `enable-funding` or `components`:

```ts
import { loadScript } from "@paypal/paypal-js";

loadScript({
  // Pay Later or venmo
  "enable-funding": "paylater,venmo",
  // ACDC, Apple Pay or Google Pay
  components: "card-fields,applepay,googlepay",
  ...
});
```

### Pay Later

```ts
const divContainer = ref();

window
  .paypal
  .Buttons({
    fundingSource: paypal.FUNDING.PAYLATER,
    createOrder: createOrder.bind(this, "paylater"),
    onApprove: onApprove.bind(this),

    // ...
  })
  .render(divContainer)
```

### Venmo

```ts
const divContainer = ref();

window
  .paypal
  .Buttons({
    fun

… **Truncated.** Full document: https://developer.shopware.com/frontends/resources/integrations/payments/paypal.md


---

## 🚀 Links
**Source:** [frontends/resources/links.md](https://developer.shopware.com/frontends/resources/links.md)  
# 🚀 Links

::: tip Do we miss some Link? 😶🌫️
Please tell us via [Community Discord](https://discord.com/channels/1308047705309708348/1405501315160739951/archives/C050L6NCMGQ), so we can add it.
:::

## Blog posts

Sorted by date, newest first

* [Unofficial API aware guidelines for Shopware 6](https://www.brocksi.net/blog/unofficial-api-aware-guidelines-shopware-6/)
* [How to work with Shopware Frontends: Experience creating POC](https://itdelight.io/how-to-work-with-shopware-frontends-experience-creating-poc/)
* [Multi-Page or Single-Page Variants Selection](https://www.brocksi.net/blog/variants-selection-multi-page-or-single-page/)
* [Create a CI/CD Pipeline for Shopware Frontends](https://kiplingi.de/create-a-ci-cd-pipeline-for-shopware-frontends/)
* [Gross and Net-Switch for B2B and B2C Shops built with Composable Frontends](https://dev.to/shopware/gross-and-net-switch-for-b2b-and-b2c-shops-built-with-composable-frontends-2b24)
* [Komponentenbasierte Entwicklung mit dem Shopware Frontends Framework](https://sitegeist.de/blog/e-commerce/komponentenbasierte-entwicklung-mit-dem-shopware-frontends-framework.html)
* [Frontend API with Nuxt + Nitro = Flexibility 🐙](https://www.brocksi.net/blog/frontend-api-with-nuxt-and-nitro-will-lead-to-flexibility/)
* [Remixing the Shopware Checkout (Part 1)](https://elkmod.dev/blogs/remixing-shopware-checkout)
* [Create a vue.js composable and call any API within Shopware Frontends](https://www.brocksi.net/blog/vue-js-composable-call-api-shopware-frontends/)
* [The future of Shopware PWA](https://www.shopware.com/de/news/the-future-of-shopware-pwa/)
* [Frontends - yet another storefront?](https://www.shopware.com/en/news/frontends-yet-another-storefront/)

## Presentations

* [Quick-Start Composable Frontends - Shopware Boostday 2023](https://ecommerce.shopware.com/hubfs/Boost%20Days/Quick%20Start%20-%20Shopware%20Composable%20Frontends.pdf) (PDF)

## Videos

Sorted by date, newest first

* [Developer Brunch April 2024 - "Composable frontends"](https://www.youtube.com/watch?v=Tz-86f72cDk)
* [Going Headless - One Page Shop mit Shopware & Nuxt 🚀 | shopware x synaigy Meetup](https://www.youtube.com/watch?v=RXaNWRMuea8)
* [Performance Improvements Headless Shopware Frontends - Niklas Wolf, Mothership GmbH](https://www.youtube.com/watch?v=GhniPTMtIt8)
* [Ein Microstore mit Shopware Frontends | Shopware Meetup der Mothership GmbH in München](https://www.youtube.com/watch?v=Dal-z94WLCk)
* [Shopware Composable Frontends in Action - A real-life example with Miriam Müller](https://www.youtube.com/watch?v=AClnII3-GhQ)
* [Quick-Start Composable Frontends - Shopware Boostday 2023](https://www.youtube.com/watch?v=2AwLWvPOffw)
* [Shopware Composable Frontends: An interview. What is it, when to use it?](https://www.youtube.com/watch?v=A_O2nke4yoo)
* [Your new tool: Composable Frontends | #SCD23](https://www.youtube.com/watch?v=hN3t96zVfpw)
* [Shopware’s Vue.js framework for building custom storefronts](https://www.youtube.com/watch?v=0W_3xWIpYho)
* [Ramona Schwering - Ecommerce as easy as an UI component - Vuejs Amsterdam 2023](https://www.youtube.com/watch?v=VivLHGGds6c)
* [shopcast.fm Folge 38 - "Frontends" Revisited](https://www.youtube.com/watch?v=eW9-jrXx4wA)
* [shopcast.fm Folge 37 - Projekt Shopware "Frontends"](https://www.youtube.com/watch?v=vupiRTNoePU)

## Code examples

* [Multi sales channel support Nuxt plugin](https://github.com/shopware/frontends/tree/main/examples/multi-sales-channel)
* [Multi-Instances Repo Example for Composable Frontends](https://github.com/patzick/frontends-multiinstances-example)
* Language/Translation Switch [StackBlitz](https://stackblitz.com/github/mkucmus/language-translations?file=app.vue) / [GitHub](https://github.com/mkucmus/language-translations)

::: tip More Code examples
Check the [examples folder](https://github.com/shopware/frontends/tree/main/examples) in our Frontends Repository.
:::

---

---

## 😱 Troubleshooting
**Source:** [frontends/resources/troubleshooting.md](https://developer.shopware.com/frontends/resources/troubleshooting.md)  
# 😱 Troubleshooting

Collection of common issues you may run into while working with Shopware Composable Frontends. If you need help or have other questions, feel free to join the [frontends Discord channel](https://discord.com/channels/1308047705309708348/1405501315160739951/archives/C050L6NCMGQ).

## Which SalesChannel type to use for Composable Frontends?

Currently you should use the default **Storefront SalesChannel type**. This sounds wrong, but if you using the Headless SalesChannel type you will not have nice speaking seo urls at the moment. Because the generation of seo urls will only be executed for SalesChannels with the type Storefront. We working on a more flexible solution with the core team to not have this confusion in the future.

## The access token for the store API is public visible?

In general, the store API should only output content that would also be visible on a standard storefront. Therefore, do not output any sensitive data to the store API. For our vue-demo-store template, we decided to use a public access token, also to have a simple configuration. However, this does not mean that you should do the same in a production environment. To secure your access token, you can use [proxy api requests](#proxy-api-requests) also have a look at our [community modules](../resources/community-modules/) how others are doing this.

## How to use https for your localhost with Composable Frontends?

### Option 1: Manual with mkcert

* Make sure you have `mkcert` installed on your system. Otherwise, follow [here](https://github.com/FiloSottile/mkcert) to set it up.
* Create a valid certificate in your project folder by running `mkcert localhost`.
* Update the `nuxt dev` command in your `package.json`.\
  It should look like this: `NODE_TLS_REJECT_UNAUTHORIZED=0 nuxt dev --https --ssl-cert localhost.pem --ssl-key localhost-key.pem`
* Now run your project with `npm run dev` or `pnpm run dev` from your project root.
* Your browser may ask you to accept the risk when you visit `https://localhost:3000`. This is because it is a self-signed certificate.

### Option 2: Vite plugin

* Execute `pnpm add -D @vitejs/plugin-basic-ssl` in your project folder
* Edit your `nuxt.config.ts` file and add:
  ```ts
  import basicSsl from '@vitejs/plugin-basic-ssl'
  // https://v3.nuxtjs.org/docs/directory-structure/nuxt.config
  export default defineNuxtConfig({
  // ...
  devServer: {
    https: true,
  },
  vite: {
    plugins: [
      basicSsl(),
    ],
  },
  // ...
  ```
* Start your dev server with `pnpm run dev`
* Your browser may ask you to accept the risk when you visit `https://localhost:3000`. This is because it is a self-signed certificate.

## SSR throws error in local environment with DDEV?

If you are using DDEV as a local environment with SSR = true (Nuxt config for routes) and you always get a 500 error message that the context is not provided for category, you may have a problem with the SSL certificate. Try to use `NODE_TLS_REJECT_UNAUTHORIZED = 0` in [.env file](https://nuxt.com/docs/guide/directory-structure/env) (this is a issue with self-signed certificates). To validate if this is your problem: Connect the local Frontend with a valid SSL from a cloud instance and check it against this instance. Also check if you can reach any local store API endpoint with some API client.

## 412 error page during local development?

The HTTP status code 412 (Precondition Failed) usually means in the Shopware `store API` context that the specified `accessToken` is incorrect or not correct for the specified `endpoint`. Check your `nuxt.config.ts` file, if you do not see an error, please try connecting directly to your `store API` endpoint using an API client.

```ts
// a part of nuxt.config.ts

  shopware: {
    accessToken: "SWSCBHFSNTVMAWNZDNFKSHLAYW", // access token for corresponding sales channel
    endpoint: "https://demo-frontends.shopware.store/store-api/", // endpoint where store-api is available
    devStorefrontUrl: "", // to simulate a storefrontUrl which is used in registration process and should cover the domain settings for a sales channel
  },

```

## Access from origin 127.0.0.1:3000 has been blocked by CORS policy

Depending on your server, you may need to set the `Access-Control-Allow-Origin` header to access your server from an external origin. And yes, your local development server is also an external origin in this case. Also, have a look at this [documentation](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS/Errors/CORSMissingAllowOrigin) from MDN.

## Proxy API requests

If you're encountering issues related to Cross-Origin Resource Sharing (CORS) or if you wish to conceal the backend API URL, you can use Vite's proxy mechanism

### Nuxt example

Edit your `nuxt.config.ts` file and add:

```
  vite: {
    server: {
      proxy: {
        "/store-api": {
          target: "<backend url>",
          changeOrigin: true,
          secure: false,
        },
      },
    },
  },
```

Modify the Shopware API endpoint to match your local frontend URL.

```
  {
    ...
      shopware: {
          endpoint: "<frontends >store-api/",
          ...
      }
  }
```

## Broadcasting and BFCache Compatibility

### Issue

When Broadcasting is enabled, the BFCache (Back-Forward Cache) functionality is not operational. This incompatibility can lead to suboptimal performance and user experience when navigating back and forth between pages.

### Resolution (vue-demo template)

To leverage the benefits of BFCache, we have decided to disable Broadcasting. By turning off Broadcasting, we ensure that the BFCache can function correctly, providing a smoother and faster navigation experience for users.

```
...
runtimeConfig: {
  broadcasting: true,
},
...
```

### Additional Information

BFCache is a browser optimization that allows pages to be stored in memory, enabling instant loading when users navigate back or forward. While Broadcasting is useful for real-time updates, its current implementation conflicts with BFCache. Disabling Broadcasting allows us to prioritize the performance improvements offered by BFCache.

For more details on BFCache, refer to the [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/Performance/Navigation_and_resource_timing#bfcache), [WHATWG](https://github.com/whatwg/html/issues/7253)

## CORS (Cross-Origin Resource Sharing) Issues

See the [CORS](./troubleshooting/CORS) page for more information on how to handle CORS issues in your project.

---

---

