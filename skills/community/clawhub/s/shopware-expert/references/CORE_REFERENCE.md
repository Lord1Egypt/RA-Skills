# CORE REFERENCE

Compiled excerpts from the Shopware Developer Documentation snapshot. Prefer live docs at [developer.shopware.com](https://developer.shopware.com/) when in doubt.

---

## Administration Reference
**Source:** [resources/references/administration-reference.md](https://developer.shopware.com/docs/v6.6/resources/references/administration-reference.md)  
# Administration Reference

This section covers concepts on Utils, Mixins and Directives.

---

---

## Directives reference
**Source:** [resources/references/administration-reference/directives.md](https://developer.shopware.com/docs/v6.6/resources/references/administration-reference/directives.md)  
# Directives reference

This is an overview of all the directives registered globally to Vue.
Directives are the same as normally in Vue. Checkout the [Using directives](../../../guides/plugins/plugins/administration/mixins-directives/adding-directives.md) article
or refer to the [directives](https://github.com/shopware/shopware/tree/trunk/src/Administration/Resources/app/administration/src/app/directive) folder in the GIT repository.

## Overview of directives

| Name         | Task                                                        |
|--------------|-------------------------------------------------------------|
| `autofocus`  | Focuses an `<input>` in an element on insertion.            |
| `dragdrop`   | Enables the drag and drop functionality of the CMS.         |
| `popover`    | Directive for automatic edge detection of the element place |
| `responsive` | Adds methods to add responsive element classes              |
| `tooltip`    | Provides utility functions to display tooltips.             |

---

---

## Mixins
**Source:** [resources/references/administration-reference/mixins.md](https://developer.shopware.com/docs/v6.6/resources/references/administration-reference/mixins.md)  
# Mixins

This is an overview of all the mixins provided by the Shopware 6 Administration. Mixins in the Shopware 6 Administration are essentially the same in default Vue. They behave generally the same as they do in Vue normally, differing only in the registration and the way mixins are included in a component. Learn more about them in the official [Vue documentation](https://vuejs.org/v2/guide/mixins.html).

Also take a look at [how to use them in your plugin](../../../guides/plugins/plugins/administration/mixins-directives/using-mixins.md) and [how to register your own mixin](../../../guides/plugins/plugins/administration/mixins-directives/add-mixins.md).

## Overview of all the mixins

| Name | Description | Link |
| :--- | :--- | :--- |
| `discard-detail-page-changes` | Mixin which resets entity changes on page leave or if the id of the entity changes. This also affects changes in associations of the entity | [link](https://github.com/shopware/shopware/blob/v6.6.9.0/src/Administration/Resources/app/administration/src/app/mixin/discard-detail-page-changes.mixin.ts) |
| `form-field` | This mixin is used to provide common functionality between form fields | [link](https://github.com/shopware/shopware/blob/v6.6.9.0/src/Administration/Resources/app/administration/src/app/mixin/form-field.mixin.ts) |
| `generic-condition` |  | [link](https://github.com/shopware/shopware/blob/v6.6.9.0/src/Administration/Resources/app/administration/src/app/mixin/generic-condition.mixin.ts) |
| `listing` | Mixin which is used in almost all listing pages to for example keep track of the current page of the administration | [link](https://github.com/shopware/shopware/blob/v6.6.9.0/src/Administration/Resources/app/administration/src/app/mixin/listing.mixin.ts) |
| `notification` | This mixin is used to create notifications in the administrations more easily | [link](https://github.com/shopware/shopware/blob/v6.6.9.0/src/Administration/Resources/app/administration/src/app/mixin/notification.mixin.ts) |
| `placeholder` | Provides a function to localize placeholders | [link](https://github.com/shopware/shopware/blob/v6.6.9.0/src/Administration/Resources/app/administration/src/app/mixin/placeholder.mixin.ts) |
| `position` | A Mixin which contains helpers to work with position integers | [link](https://github.com/shopware/shopware/blob/v6.6.9.0/src/Administration/Resources/app/administration/src/app/mixin/position.mixin.ts) |
| `remove-api-error` | This mixin removes API errors e.g. after the user corrected a invalid input i.e. leaving the product name field blank | [link](https://github.com/shopware/shopware/blob/v6.6.9.0/src/Administration/Resources/app/administration/src/app/mixin/remove-api-error.mixin.ts) |
| `rule-container` | Provides common functions between the `sw-condition-or-container` and the `sw-condition-and-container` | [link](https://github.com/shopware/shopware/blob/v6.6.9.0/src/Administration/Resources/app/administration/src/app/mixin/rule-container.mixin.ts) |
| `salutation` | A common adapter for the `salutation` filter | [link](https://github.com/shopware/shopware/blob/v6.6.9.0/src/Administration/Resources/app/administration/src/app/mixin/salutation.mixin.ts) |
| `sw-inline-snippet` | Makes it possible to use snippets inline | [link](https://github.com/shopware/shopware/blob/v6.6.9.0/src/Administration/Resources/app/administration/src/app/mixin/sw-inline-snippet.mixin.ts) |
| `user-settings` |  | [link](https://github.com/shopware/shopware/blob/v6.6.9.0/src/Administration/Resources/app/administration/src/app/mixin/form-field.mixin.ts) |
| `validation` | Is used to validate inputs in various form fields | [link](https://github.com/shopware/shopware/blob/v6.6.9.0/src/Administration/Resources/app/administration/src/app/mixin/validation.mixin.ts) |

---

---

## Utils
**Source:** [resources/references/administration-reference/utils.md](https://developer.shopware.com/docs/v6.6/resources/references/administration-reference/utils.md)  
# Utils

This is an overview of all the utility functions bound to the shopware global object. Utility functions provide many useful shortcuts for common tasks, see how to use them in your plugin [here](../../../guides/plugins/plugins/administration/services-utilities/using-utils.md). Or see the code that registers them [here](https://github.com/shopware/shopware/blob/v6.3.4.1/src/Administration/Resources/app/administration/src/core/service/util.service.js)

## General functions

| Function | Description | Link |
| :--- | :--- | :--- |
| createId | Returns a uuid string in hex format. Generated with [uuid](https://www.npmjs.com/package/uuid) | [link](https://lodash.com/docs/4.17.15#create) |
| throttle | Creates a `throttled` function that only invokes `func` at most once per every `wait` milliseconds. | [link](https://lodash.com/docs/4.17.15#throttle) |
| debounce | Creates a `debounced` function that delays invoking `func` until after `wait` milliseconds have elapsed since the last time the `debounced` function was invoked. | [link](https://lodash.com/docs/4.17.15#debounce) |
| flow | Creates a function that returns the result of invoking the given functions with the `this` binding of the created function, where each successive invocation is supplied the return value of the previous. | [link](https://lodash.com/docs/4.17.15#flow) |
| get | Gets the value at `path` of `object` | [link](https://lodash.com/docs/4.17.15#get) |

## Object

| Function | Description | Link |
| :--- | :--- | :--- |
| deepCopyObject | Deep copy an object |  |
| hasOwnProperty | Shorthand method for `Object.prototype.hasOwnProperty` |  |
| getObjectDiff | Gets a simple recursive diff of two objects. Does not consider an entity schema or entity related logic. |  |
| getArrayChanges | Check if the compared array has changes. |  |
| cloneDeep | Creates recursively a clone of value. | [link](https://lodash.com/docs/4.17.15#cloneDeep) |
| merge | This method is like \_.assign except that it recursively merges own and inherited enumerable string keyed properties of source objects into the destination object. | [link](https://lodash.com/docs/4.17.15#merge) |
| mergeWith | This method is like \_.merge except that it accepts customizer which is invoked to produce the merged values of the destination and source properties. | [link](https://lodash.com/docs/4.17.15#mergeWith) |
| deepMergeObject | Deep merge two objects |  |
| get | Gets the value at `path` of `object` | [link](https://lodash.com/docs/4.17.15#get) |
| set | Sets the value at `path` of `object` | [link](https://lodash.com/docs/4.17.15#set) |
| pick | Creates an object composed of the picked `object` properties. | [link](https://lodash.com/docs/4.17.15#pick) |

## Debug

| Function | Description |
| :--- | :--- |
| warn | General logging function which provides a unified style of log messages for developers. Please keep the log in mind. Messages will be displayed in the developer console when they're running the application in development mode. |
| debug | The same as `warn` but instead of `console.warn` it uses `console.error`. |

## Format

| Function | Description |
| :--- | :--- |
| currency | Converts a number to a formatted currency. Especially helpful for template filters. |
| date | Formats a Date object to a localized string with the [native `Intl.DateTimeFormat` method](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat) |
| fileSize | Formats a number of bytes to a string with a unit |
| md5 | Generates a md5 hash with [md5-es](https://www.npmjs.com/package/md5-es) of a given value. |

## Dom

| Function | Description |
| :--- | :--- |
| getScrollbarHeight | Returns the scrollbar height of an HTML element. |
| getScrollbarWidth | Returns the scrollbar width of an HTML element. |
| copyToClipboard | Uses the browser's copy function to copy a string |

## String

| Function | Description | Link |
| :--- | :--- | :--- |
| capitalizeString | Converts the first character of `string` to upper case and the remaining to lower case. | [link](https://lodash.com/docs/4.17.15#capitalize) |
| camelCase | Converts `string` to camel case. | [link](https://lodash.com/docs/4.17.15#camelCase) |
| kebabCase | Converts `string` to kebab case. | [link](https://lodash.com/docs/4.17.15#kebabCase) |
| snakeCase | Converts `string` to snake case. | [link](https://lodash.com/docs/4.17.15#snakeCase) |
| md5 | Generates a md5 hash with [md5-es](https://www.npmjs.com/package/md5-es) of a given value. |  |
| isEmptyOrSpaces | Gets if the content of the string is really empty. This does also removes any whitespaces that might exist in the text. |  |
| isUrl | Checks if the provided value is a URL |  |
| isValidIp | Checks if the provided value is an IP with this [Regex](https://regex101.com/r/qHTUIe/1) |  |

## Type

| Function | Description | Link |
| :--- | :--- | :--- |
| isObject | Checks if `value` is the [language type](http://www.ecma-international.org/ecma-262/7.0/#sec-ecmascript-language-types) of `Object`. *(e.g. arrays, functions, objects, regexes, `new Number(0)`, and `new String('')`)* | [link](https://lodash.com/docs/4.17.15#isObject) |
| isPlainObject | Checks if `value` is a plain object, that is, an object created by the `Object` constructor or one with a `[[Prototype]]` of `null`. | [link](https://lodash.com/docs/4.17.15#isPlainObject) |
| isEmpty | Checks if `value` is an empty object, collection, map, or set. | [link](https://lodash.com/docs/4.17.15#isEmpty) |
| isRegExp | Checks if `value` is classified as a `RegExp` object. | [link](https://lodash.com/docs/4.17.15#isRegExp) |
| isArray | Checks if `value` is classified as an `Array` object. | [link](https://lodash.com/docs/4.17.15#isArray) |
| isFunction | Checks if `value` is classified as a `Function` object. | [link](https://lodash.com/docs/4.17.15#isFunction) |
| isDate | Checks if `value` is classified as a `Date` object. | [link](https://lodash.com/docs/4.17.15#isDate) |
| isString | Checks if `value` is classified as a `String` primitive or object. | [link](https://lodash.com/docs/4.17.15#isString) |
| isBoolean | Checks if value is classified as a `boolean` primitive or object. | [link](https://lodash.com/docs/4.17.15#isBoolean) |
| isEqual | Performs a deep comparison between two values to determine if they are equivalent. | [link](https://lodash.com/docs/4.17.15#isEqual) |
| isNumber | Checks if `value` is classified as a Number primitive or object. | [link](https://lodash.com/docs/4.17.15#isNumber) |
| isUndefined | Checks if `value` is `undefined`. | [link](https://lodash.com/docs/4.17.15#isUndefined) |

## FileReader

| Function | Description | Link |
| :--- | :--- | :--- |
| readAsArrayBuffer | Reads a `file` as an `ArrayBuffer` | [link](https://developer.mozilla.org/en-US/docs/Web/API/FileReader/readAsArrayBuffer) |
| readAsDataURL | Reads a `file` as a `Data-URL` | [link](https://developer.mozilla.org/en-US/docs/Web/API/FileReader/readAsDataURL) |
| readAsText | Reads a `file` as `text` | [link](https://developer.mozilla.org/en-US/docs/Web/API/FileReader/readAsText) |
| getNameAndExtensionFromFile | Gets the `name` and `extension` from a file |  |
| getNameAndExtensionFromUrl | Gets the `name` and `extension` from a URL |  |

## Sort

| Function | Description |
| :--- | :--- |
| afterSort | Sorts the elements by their after id property chain |

## Array

| Function | Description | Link |
| :--- | :--- | :--- |
| flattenDeep | Recursively flattens `array`. | [link](https://lodash.com/docs/4.17.15#flattenDeep) |
| remove | Removes all elements from `array` that predicate returns truthy for and returns an array of the removed elements | [link](https://lodash.com/docs/4.17.15#remove) |
| slice | Creates a slice of `array` from `start` up to, but not including, `end`. | [link](https://lodash.com/docs/4.17.15#slice) |
| uniqBy | This method is like [`_.uniq`](https://lodash.com/docs/4.17.15#uniq) except that it accepts `iteratee` which is invoked for each element in `array` to generate the criterion by which uniqueness is computed. | [link](https://lodash.com/docs/4.17.15#uniqBy) |

---

---

## App Reference
**Source:** [resources/references/app-reference.md](https://developer.shopware.com/docs/v6.6/resources/references/app-reference.md)  
# App Reference

The app reference document gives you an understanding of the app structure, functions, methods, events, variables, responses, and examples for building quality apps in Shopware.

Overall, the app reference document is a valuable resource for creating feature-rich and seamless custom apps that integrate seamlessly with the Shopware platform.

---

---

## CMS Reference
**Source:** [resources/references/app-reference/cms-reference.md](https://developer.shopware.com/docs/v6.6/resources/references/app-reference/cms-reference.md)  
# CMS Reference

```xml
// cms.xml
<?xml version="1.0" encoding="utf-8" ?>
<cms xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Cms/Schema/cms-1.0.xsd">
    <blocks>
        <block>
            <!-- A unique technical name for your block. We recommend to use a shorthand prefix for your company, e.g. "Swag" for shopware AG. -->
            <name>my-first-block</name>
            <!-- The category your block is associated with. See the XSD for available categories. -->
            <category>text-image</category>

            <!-- Your block's label which will be shown in the CMS module in the Administration. -->
            <label>First block from app</label>
            <!-- The label is translatable by providing ISO codes. -->
            <label lang="de-DE">Erster Block einer App</label>

            <!-- The slots that your block holds which again hold CMS elements. -->
            <slots>
                <!-- A slot requires a unique name and a type which refers to the CMS element it shows. Right now you can only use the CMS elements provided by Shopware but at a later point you will be able to add custom elements too. -->
                <slot name="left" type="manufacturer-logo">
                    <!-- The slot requires some basic configuration. The following config-value elements highly depend on which element the slot holds. -->
                    <config>
                        <!-- The following config-value will be interpreted as "displayMode: { source: "static", value: "cover"}" in the JavaScript. -->
                        <config-value name="display-mode" source="static" value="cover"/>
                    </config>
                </slot>
                <slot name="middle" type="image-gallery">
                    <config>
                        <config-value name="display-mode" source="static" value="auto"/>
                        <config-value name="min-height" source="static" value="300px"/>
                    </config>
                </slot>
                <slot name="right" type="buy-box">
                    <config>
                        <config-value name="display-mode" source="static" value="contain"/>
                    </config>
                </slot>
            </slots>

            <!-- Each block comes with a default configuration which is pre-filled and customizable when adding a block to a section in the CMS module in the Administration. -->
            <default-config>
                <margin-bottom>20px</margin-bottom>
                <margin-top>20px</margin-top>
                <margin-left>20px</margin-left>
                <margin-right>20px</margin-right>
                <!-- The sizing mode of your block. Allowed values are "boxed" or "full_width". -->
                <sizing-mode>boxed</sizing-mode>
                <background-color>#000</background-color>
            </default-config>
        </block>

        <block>
            <name>my-second-block</name>
            <category>text-image</category>

            <label>Second block from app</label>
            <label lang="de-DE">Zweiter Block einer App</label>

            <slots>
                <slot name="left" type="form">
                    <config>
                        <config-value name="display-mode" source="static" value="cover"/>
                    </config>
                </slot>
                <slot name="middle" type="image">
                    <config>
                        <config-value name="display-mode" source="static" value="auto"/>
                        <config-value name="background-color" source="static" value="red"/>
                    </config>
                </slot>
                <slot name="right" type="youtube-video">
                    <config>
                        <config-value name="display-mode" source="static" value="contain"/>
                    </config>
                </slot>
            </slots>

            <default-config>
                <margin-bottom>20px</margin-bottom>
                <margin-top>20px</margin-top>
                <margin-left>20px</margin-left>
                <margin-right>20px</margin-right>
                <sizing-mode>boxed</sizing-mode>
                <background-color>#000</background-color>
            </default-config>
        </block>
    </blocks>
</cms>
```

---

---

## Entities Reference
**Source:** [resources/references/app-reference/entities-reference.md](https://developer.shopware.com/docs/v6.6/resources/references/app-reference/entities-reference.md)  
# Entities Reference

```xml
// entities.xml
<?xml version="1.0" encoding="utf-8" ?>
<entities xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/System/CustomEntity/Xml/entity-1.0.xsd">
    <entity name="custom_entity_blog">
        <fields>
            <!-- we support different scalar values: int, float, string, text, bool, date -->
            <int name="position" store-api-aware="true" />
            <float name="rating" store-api-aware="true" />
            <string name="title" required="true" translatable="true" store-api-aware="true" />
            <text name="content" allow-html="true" translatable="true" store-api-aware="true" />
            <bool name="display" translatable="true" store-api-aware="true" />
            <date name="my_date" store-api-aware="false" />

            <!-- additionally, to the scalar values, we have support for json fields  -->
            <json name="payload" store-api-aware="false" />
            
            <!-- beside the generic fields, we support different logical fields like email and price -->
            <email name="email"  store-api-aware="false" />
            <price name="price" store-api-aware="false" />
            
            <!--   each field also supports having a default value. This is only supported for scalar types -->
            <bool name="in_stock" store-api-aware="true" default="true" />

            <!-- you may want to define that some fields should not be available in the store-api -->
            <text name="internal_comment" store-api-aware="false" />

            <!-- you can also define relation between entities -->
            <many-to-many name="products" reference="product" store-api-aware="true" />

            <!-- it is also possible to cascading relations between you own custom entities. In this case, we delete all ce_blog_comment records, when the linked custom_entity_blog record deleted -->
            <one-to-many name="comments" reference="ce_blog_comment" store-api-aware="true" on-delete="cascade" reverse-required="true" />
            
            <!-- There are many other cascade cases which we support -->

            <!-- Restrict product deletion when the product is set as `top_seller` -->
            <many-to-one name="top_seller_restrict" reference="product" store-api-aware="true" required="false" on-delete="restrict" />
                <!-- This definition, generates a fk field automatically inside the product table -->

            <!-- when product deleted, delete all custom_entity_blog records where the product is defined as `top_seller_cascade`-->
            <many-to-one name="top_seller_cascade" reference="product" store-api-aware="true" required="true" on-delete="cascade" />

            <!-- when product deleted, set the `top_seller_set_null` column to null -->
            <many-to-one name="top_seller_set_null" reference="product" store-api-aware="true" on-delete="set-null" />

            <!-- restrict product deletion when the product is set as `link_product_restrict`-->
            <one-to-one name="link_product_restrict" reference="product" store-api-aware="false" on-delete="restrict" />

            <!-- when product deleted, delete all custom_entity_blog records where the product is defined as `link_product_cascade`-->
            <one-to-one name="link_product_cascade" reference="product" store-api-aware="false" on-delete="cascade" />

            <!-- when product deleted, set the `link_product_set_null_id` column to null -->
            <one-to-one name="link_product_set_null" reference="product" store-api-aware="false" on-delete="set-null" />

            <!-- restrict custom_entity_blog deletion, when the blog is linked in some category -->
            <one-to-many name="links_restrict" reference="category" store-api-aware="true" on-delete="restrict" />

            <!-- set custom_entity_blog_links_id to null, when the custom_entity_blog record deleted -->
            <one-to-many name="links_set_null" reference="category" store-api-aware="true" on-delete="set-null" />

            <!-- we also support inheritance for product relations  -->
            <many-to-many name="inherited_products" reference="product" store-api-aware="true" inherited="true"/>
            <many-to-one name="inherited_top_seller" reference="product" store-api-aware="true" required="false" inherited="true" on-delete="set-null"/>
            <one-to-one name="inherited_link_product" reference="product" store-api-aware="true" inherited="true" on-delete="set-null" />
        </fields>
    </entity>

    <!-- since shopware v6.5.15.0 you can use the `ce_` shorthand prefix, to make your entity names shorter -->
    <entity name="ce_blog_comment">
        <fields>
            <string name="title" required="true" translatable="true" store-api-aware="true" />
            <!-- <fk name="ce_blog_comments_id" required="true"   <<< defined over the one-to-many association in the custom_entity_blog definition -->
            <text name="content" allow-html="true" translatable="true" store-api-aware="true" />
            <email name="email"  store-api-aware="false" />
            <many-to-one name="recommendation" reference="product" store-api-aware="true" required="false" on-delete="set-null" />
        </fields>
    </entity>
</entities>
```

---

---

## Flow Action Reference
**Source:** [resources/references/app-reference/flow-action-reference.md](https://developer.shopware.com/docs/v6.6/resources/references/app-reference/flow-action-reference.md)  
# Flow Action Reference

```xml
// flow-action.xml
<flow-actions xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Flow/Schema/flow-1.0.xsd">
    <flow-action>
        <meta>
            <name>slack</name>
            <label>Send slack message</label>
            <label lang="de-DE">Slack-Nachricht senden</label>
            <headline>Headline for send slack message</headline>
            <headline lang="de-DE">Überschrift für das Senden einer Slack-Nachricht</headline>
            <description>Slack send message description</description>
            <description lang="de-DE">Beschreibung der Slack-Sendenachricht</description>
            <url>https://hooks.slack.com/services/{id}</url>
            <sw-icon>default-communication-speech-bubbles</sw-icon>
            <icon>slack.png</icon>
            <requirements>orderAware</requirements>
            <requirements>customerAware</requirements>
        </meta>
        <headers>
            <parameter type="string" name="content-type" value="application/json"/>
        </headers>
        <parameters>
            <parameter type="string" name="text" value="{{ subject }} \n {{ message }} \n Order Number: {{ order.orderNumber }}"/>
        </parameters>
        <config>
            <input-field type="text">
                <name>subject</name>
                <label>Subject</label>
                <label lang="de-DE">Gegenstand</label>
                <place-holder>Placeholder</place-holder>
                <place-holder lang="de-DE">Platzhalter</place-holder>
                <required>true</required>
                <helpText>Help Text</helpText>
                <helpText lang="de-DE">Hilfstext</helpText>
            </input-field>
            <input-field type="textarea">
                <name>message</name>
                <label>Message</label>
                <label lang="de-DE">Nachricht</label>
                <place-holder>Placeholder</place-holder>
                <place-holder lang="de-DE">Platzhalter</place-holder>
                <required>true</required>
                <helpText>Help Text</helpText>
                <helpText lang="de-DE">Hilfstext</helpText>
            </input-field>
        </config>
    </flow-action>
    <flow-action>
        <meta>
            <name>telegram</name>
            <label>Send telegram message</label>
            <label lang="de-DE">Telegrammnachricht senden</label>
            <url>https://api.telegram.org/{id}</url>
            <sw-icon>default-communication-speech-bubbles</sw-icon>
            <icon>telegram.png</icon>
            <requirements>orderAware</requirements>
            <requirements>customerAware</requirements>
        </meta>
        <headers>
            <parameter type="string" name="content-type" value="application/json"/>
        </headers>
        <parameters>
            <parameter type="string" name="chat_id" value="{{ chatId }}"/>
            <parameter type="string" name="text" value="{{ content }}"/>
        </parameters>
        <config>
            <input-field type="text">
                <name>chatId</name>
                <label>Chat Room</label>
                <label lang="de-DE">Chatroom</label>
                <required>true</required>
                <defaultValue>Hello</defaultValue>
                <helpText>This is the chat room id, you can get the id via telegram api</helpText>
                <helpText lang="de-DE">Dies ist die Chatroom-ID, Sie können die ID über die Telegramm-API abrufen</helpText>
            </input-field>
            <input-field type="text">
                <name>subject</name>
                <label>Subject</label>
                <label lang="de-DE">Thema</label>
                <required>true</required>
            </input-field>
            <input-field type="textarea">
                <name>content</name>
                <label>Content</label>
                <label lang="de-DE">Inhalt</label>
            </input-field>
        </config>
    </flow-action>
</flow-actions>
```

## Variables

| Event | Variables |
| :--- | :--- |
| checkout.order.placed  state\_enter.order.state.cancelled  state\_enter.order.state.completed  state\_enter.order.state.in\_progress state\_enter.order\_transaction.state.reminded  state\_enter.order\_transaction.state.open  state\_enter.order\_transaction.state.refunded state\_enter.order\_transaction.state.paid  state\_enter.order\_transaction.state.cancelled  state\_enter.order\_transaction.state.refunded\_partially  state\_enter.order\_transaction.state.paid\_partially  state\_enter.order\_delivery.state.cancelled   state\_enter.order\_delivery.state.shipped  state\_enter.order\_delivery.state.returned\_partially  state\_enter.order\_delivery.state.shipped\_partially  state\_enter.order\_delivery.state.returned | order |
| customer.group.registration.declined  customer.group.registration.accepted | customer  customerGroup |
| user.recovery.request | userRecovery |
| checkout.customer.double\_opt\_in\_registration  checkout.customer.double\_opt\_in\_guest\_order | customer  confirmUrl |
| customer.recovery.request | customerRecovery  customer  resetUrl  shopName |
| contact\_form.send | contactFormData |
| checkout.customer.register | customer |
| newsletter.register | newsletterRecipient  url |
| newsletter.confirm | newsletterRecipient |

---

---

## Manifest Reference
**Source:** [resources/references/app-reference/manifest-reference.md](https://developer.shopware.com/docs/v6.6/resources/references/app-reference/manifest-reference.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Manifest Reference

## Meta information (required)

Meta-information about your app.

```xml
<meta>
    <!-- This is the element for the technical name of your app and must equal the name of the folder your app is contained in -->
    <name>MyExampleApp</name>
    <!-- In this element, you can set a label for your app. To include translations use the `lang` attribute -->
    <label>Label</label>
    <label lang="de-DE">Name</label>
    <!-- Translatable, a description of your app -->
    <description>A description</description>
    <description lang="de-DE">Eine Beschreibung</description>
    
    <author>Your Company Ltd.</author>
    <copyright>(c) by Your Company Ltd.</copyright>
    <version>1.0.0</version>
    <license>MIT</license>
    <compatibility>~6.5.0</compatibility>
    <!-- Optional, you can set the path to an icon that should be shown for your app, the icon needs to a `png` file -->
    <icon>icon.png</icon>
    <!-- Optional, in this element you can link to your privacy policy -->
    <privacy>https://your-company.com/privacy</privacy>
    <!-- Optional, Translatable, in this element you can describe the changes the shop owner needs to apply to his shops privacy policy, e.g. because you process personal information on an external server -->
    <privacyPolicyExtensions>
        This app processes following personal information on servers based in the U.S.:
        - Address information
        - Order positions
        - Order value
    </privacyPolicyExtensions>
    <privacyPolicyExtensions lang="de-DE">
        Diese App verarbeitet folgende personenbezogene Daten auf Servern in den USA:
        - Adress-Informationen
        - Bestellpositionen
        - Bestellsumme
    </privacyPolicyExtensions>
</meta>

```

:::info
The following configurations are all optional.
:::

## Setup

Can be omitted if no communication between Shopware and your app is needed. For more follow the [app base guide](../../../guides/plugins/apps/app-base-guide#registration-request).

```xml
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        ...
    </meta>
    <setup>
        <!-- The URL which will be used for the registration -->
        <registrationUrl>https://my.example.com/registration</registrationUrl>
        <!-- Dev only, the secret that is used to sign the registration request -->
        <secret>mysecret</secret>
    </setup>
</manifest>

```

## Storefront

Can be omitted if your app template needs higher load priority than other plugins/apps. For more follow the [storefront guide](../../../guides/plugins/apps/storefront/index).

```xml
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"  xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        ....
    </meta>
    <storefront>
        <template-load-priority>100</template-load-priority>
    </storefront>
</manifest>

```

## Permissions

*Optional*, can be omitted if your app does not need permissions. For more follow the [app base guide](../../../guides/plugins/apps/app-base-guide).

```xml
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
  <meta>
    ...
  </meta>
  <permissions>
    <read>product</read> <!-- [!code focus] -->
    <create>product</create> <!-- [!code focus] -->
    <update>product</update> <!-- [!code focus] -->
    <delete>product</delete> <!-- [!code focus] -->

    <!-- Since version 6.4.12.0 your app can request additional non-CRUD privileges-->
    <permission>system:cache:info</permission>
  </permissions>
</manifest>

```

## Allowed hosts

A list of all external endpoints your app communicates with (since `6.4.12.0`)

```xml
<allowed-hosts>
    <host>example.com</host>
</allowed-hosts>

```

## Webhooks

Register webhooks you want to receive, keep in mind that the name needs to be unique. For more follow the [app webhook guide](../../../guides/plugins/apps/webhook).

```xml
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        ...
    </meta>
    <webhooks>
        <webhook name="product-changed" url="https://example.com/event/product-changed" event="product.written"/>
    </webhooks>
</manifest>

```

## Admin extension

Only needed if the Administration should be extended. For more follow the [add custom module guide](../../../guides/plugins/apps/administration/add-custom-modules).

```xml
<admin>
    <!-- Optional, entry point for the Admin Extension API (since 6.4.12.0) -->
    <base-app-url>https://app.example.com</base-app-url>
    <!-- Register a custom module that is used as a parent menu entry for other modules -->
    <module name="myAdminModules"
            parent="sw-marketing"
            position="50"
    >
        <label>My modules</label>
        <label lang="de-DE">Meine Module</label>
    </module>
    <!-- Register a custom module (iframe), that should be loaded from the given source -->
    <module name="exampleModule"
            source="https://example.com/promotion/view/promotion-module"
            parent="app-MyExampleApp-myAdminModules"
    >
        <label>Example Module</label>
        <label lang="de-DE">Beispiel Modul</label>
    </module>
    <!-- Register a module that is opened from the app store and your list of installed apps -->
    <main-module source="https://example.com/main-module"/>
    <!-- Register action buttons that should be displayed in the detail and listing pages of the Administration -->
    <!-- view is one of: "list", "detail" -->
    <action-button action="setPromotion" entity="promotion" view="detail" url="https://example.com/promotion/set-promotion">
        <label>set Promotion</label>
    </action-button>
    <action-button action="deletePromotion" entity="promotion" view="detail" url="https://example.com/promotion/delete-promotion">
        <label>delete Promotion</label>
    </action-button>
    <action-button action="restockProduct" entity="product" view="list" url="https://example.com/restock">
        <label>restock</label>
    </action-button>
</admin>

```

## Custom fields

Add your custom fields easily via the manifest.xml. For more follow the [custom fields app guide](../../../guides/plugins/apps/custom-data/custom-fields).

```xml
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        ...
    </meta>
    <custom-fields>
        <!-- register each custom field set you may want to add -->
        <custom-field-set>
            <!-- the technical name of the custom field set, needs to be unique, therefor use your vendor prefix -->
            <name>swag_example_set</name>
            <!-- Translatable, the label of the field set -->
            <label>Example Set</label>
            <label lang="de-DE">Beispiel-Set</label>
            <!-- define the entities to which your field set should be assigned -->
            <related-entities>
                <order/>
            </related-entities>
            <!-- define the fields in your set -->
            <fields>
                <!-- the element type, defines the type of the field -->
                <!-- the name needs to be unique, therefore use your vendor prefix -->
                <text name="swag_code">
                    <!-- Translatable, the label of the field -->
                    <label>Example field</label>
                    <!-- Optional, Default = 1, order your fields by specifying the position -->
                    <position>1</position>
                    <!-- Optional, Default = false, mark a field as required -->
                    <required>false</required>
                    <!-- Optional, Translatable, the help text for the field -->
                    <help-text>Example field</help-text>
                </text>
                <float name="swag_test_float_field">
                    <label>Test float field</label>
                    <label lang="de-DE">Test-Kommazahlenfeld</label>
                    <help-text>This is an float field.</help-text>
                    <position>2</position>
                    <!-- some elements allow more configuration, like placeholder, main and max values etc. -->
                    <!-- Your IDE should give you pretty good autocompletion support to explore the configuration for a given type -->
                    <placeholder>Enter an float...</placeholder>
                    <min>0.5</min>
                    <max>1.6</max>
                    <steps>0.2</steps>
                </float>
            </fields>
        </custom-field-set>
    </custom-fields>
</manifest>

```

## Cookies

Add a single cookie to the consent manager. For more follow the [cookies with apps guide](../../../guides/plugins/apps/storefront/cookies-with-apps).

```xml
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        <name>ExampleAppWithCookies</name>
        <version>1.0.0</version>
        <!-- other meta data goes here -->
    </meta>
    <cookies>
        <cookie>
            <cookie>my-cookie</cookie>
            <snippet-name>example-app-with-cookies.my-cookie.name</snippet-name>
            <snippet-description>example-app-with-cookies.my-cookie.description</snippet-description>
            <value>a static value for the cookie</value>
            <!-- Expiration in days -->
            <expiration>1</expiration>
        </cookie>
    </cookies>
</manifest>

```

Add a cookie group to the consent manager. For more follow the [cookies with apps guide](../../../guides/plugins/apps/storefront/cookies-with-apps).

```xml
<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/shopware/shopware/trunk/src/Core/Framework/App/Manifest/Schema/manifest-3.0.xsd">
    <meta>
        <name>ExampleAppWithCookies</name>
        <version>1.0.0</version>
        <!-- other meta data goes here -->
    </meta>
    <cookies>
        <group>
            <snippet-name>example-app-with-cookies.cookie-group.name</snippet-name>
            <snippet-description>example-app-with-cookies.cookie-group.description</snippet-description>
            <entries>
                <cookie>
                    <cookie>my-cookie</cookie>
                    <snippet-name>example-app-with-cookies.my-cookie.name</snippet-name>
                    <snippet-description>example-app-with-cookies.my-cookie.description</snippet-description>
                    <value>a static value for the cookie</value>
                    <!-- Expiration in days -->
                    <expiration>1</expiration>
                </cookie>
            </entries>
        </group>
    </cookies>
</manifest>

```

## Payments

Add your payment methods via payments and handle your synchronous and asynchronous via an external app-server. For more follow the [app payment guide](../../../guides/plugins/apps/payment).

```xml
<?xml version="1.0" encoding="UTF-

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/resources/references/app-reference/manifest-reference.md


---

## Payment Reference
**Source:** [resources/references/app-reference/payment-reference.md](https://developer.shopware.com/docs/v6.6/resources/references/app-reference/payment-reference.md)  
# Payment Reference

::: warning
This feature is only available starting with Shopware 6.4.1.0.
:::

These two requests are executed against your API, the up to two endpoints you define per payment method. All bodies are JSON encoded.

## Pay

`POST https://payment.app/pay`

This request gets called, when the users hits *Confirm Order* in Shopware.

### Parameters

| Parameter                | Type                   | Description                                                                                                                                                                                                                          |
|--------------------------|------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Header**               |                        |                                                                                                                                                                                                                                      |
| shopware-shop-signature\* | string                 | The hmac-signature of the JSON encoded body content, signed with the shop secret returned from the registration request                                                                                                              |
| **Body**                 |                        |                                                                                                                                                                                                                                      |
| order\*                   | OrderEntity            | The order entity from Shopware including all necessary associations (like currency, shipping address, billing address, line items). See Shopware for detailed and current structure.                                                 |
| orderTransaction\*        | OrderTransactionEntity | The order transaction entity from Shopware representing the payment you are supposed to process. See Shopware for detailed and current structure.                                                                                    |
| orderTransaction.id\*     | string                 | This should be used to identify the order transaction on a second finalize request.                                                                                                                                                  |
| returnUrl                | string                 | This URL is the URL your app or your payment provider is supposed to redirect back to, once the user has been redirected to the payment provider with the URL you provide in your response. Only supplied on asynchronous payments. |
| source\*                  | object                 | Data to identify the shop that sent this request                                                                                                                                                                                     |
| source.url\*              | string                 | The Shop URL sending this request                                                                                                                                                                                                    |
| source.shopId\*           | string                 | The shop id you can use to identify the sho that has been registered before with your app.                                                                                                                                           |
| source.appVersion\*       | string                 | The version of the app that is installed in the shop.                                                                                                                                                                                |

### Responses

`200`

```json5
/* Successful redirect */
{
  "redirectUrl": "https://payment.app/user/go/here/068b1ec4d7ff431b95d3b7431cc725aa/"
}
```

```json5
/* Failure due to missing credentials */
{
  "status": "fail",
  "message": "The shop has not provided all credentials for the payment provider."
}
```

## Finalize

`POST https://payment.app/finalize`

This request gets called once the user returns to the `returnUrl` Shopware provided in the first request.

### Parameters

| Parameter                | Type                   | Description                                                                                                                                                                                                                          |
|--------------------------|------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Header**               |                        |                                                                                                                                                                                                                                      |
| shopware-shop-signature\* | string                 | The hmac-signature of the JSON encoded body content, signed with the shop secret returned from the registration request                                                                                                              |
| **Body**                 |                        |                                                                                                                                                                                                                                      |
| orderTransaction\*        | OrderTransactionEntity | The order transaction entity from Shopware representing the payment you are supposed to process. See Shopware for detailed and current structure.                                                                                    |
| orderTransaction.id\*     | string                 | This should be used to identify the order transaction on a second finalize request.                                                                                                                                                  |
| source\*                  | object                 | Data to identify the shop that sent this request                                                                                                                                                                                     |
| source.url\*              | string                 | The Shop URL sending this request                                                                                                                                                                                                    |
| source.shopId\*           | string                 | The shop id you can use to identify the sho that has been registered before with your app.                                                                                                                                           |
| source.appVersion\*       | string                 | The version of the app that is installed in the shop.                                                                                                                                                                                |

### Responses

`200`

```json5
/* Successful redirect */
{
  "status": "paid"
}
```

```json5
/* Failure due to missing funds */
{
  "status": "fail",
  "message": "The user did not have adequate funds."
}
```

```json5
/* Failure if the user has not finished the payment process. */
{
  "status": "cancel",
  "message": "The user did not finish payment."
}
```

---

---

## Script Reference
**Source:** [resources/references/app-reference/script-reference.md](https://developer.shopware.com/docs/v6.6/resources/references/app-reference/script-reference.md)  
# Script Reference

Script references include detailed explanations of the available functions, methods, arguments, responses, and samples.

This reference gives you an understanding of the various service capabilities, code structure, and functionalities.

---

---

## Cart Manipulation script services reference
**Source:** [resources/references/app-reference/script-reference/cart-manipulation-script-services-reference.md](https://developer.shopware.com/docs/v6.6/resources/references/app-reference/script-reference/cart-manipulation-script-services-reference.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Cart Manipulation script services reference

## [services.cart (`Shopware\Core\Checkout\Cart\Facade\CartFacade`)](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Facade/CartFacade.php) {#cartfacade}

The `cart` service allows you to manipulate the cart.
You can use the cart service to add line-items, change prices, add discounts, etc. to the cart.

### items()

* The `items()` method returns all line-items of the current cart for further manipulation.

* **Returns** [`Shopware\Core\Checkout\Cart\Facade\ItemsFacade`](./cart-manipulation-script-services-reference#itemsfacade)

  A `ItemsFacade` containing all line-items in the current cart as a collection.

### products()

* The `product()` method returns all products of the current cart for further manipulation. Similar to the `items()` method, but the line-items are filtered, to only contain product line items.

* **Returns** [`Shopware\Core\Checkout\Cart\Facade\ProductsFacade`](./cart-manipulation-script-services-reference#productsfacade)

  A `ProductsFacade` containing all product line-items in the current cart as a collection.

### calculate()

* The `calculate()` method recalculates the whole cart.

  Use this to get the correct prices after you made changes to the cart. Note that after calling the `calculate()` all collections (e.g. items(), products()) get new references,	so if you still hold references to things inside the cart, these are outdated after calling `calculate()`. This method will be called automatically after your cart script executed.

### price()

* The `price()` method returns the current price of the cart.

  Note that this price may be outdated, if you changed something inside the cart in your script.Use the `calculate()` method to recalculate the cart and update the price.

* **Returns** [`Shopware\Core\Checkout\Cart\Facade\CartPriceFacade`](./cart-manipulation-script-services-reference#cartpricefacade)

  The calculated price of the cart.

### errors()

* The `errors()` method returns the current errors of the cart.

  You can use it to add new errors or warning or to remove existing ones.
* **Returns** [`Shopware\Core\Checkout\Cart\Facade\ErrorsFacade`](./cart-manipulation-script-services-reference#errorsfacade)

  A `ErrorsFacade` containing all cart errors as a collection (may be an empty collection if there are no errors).

### states()

* `states()` allows you to access the state functions of the current cart.

* **Returns** [`Shopware\Core\Checkout\Cart\Facade\StatesFacade`](./cart-manipulation-script-services-reference#statesfacade)

  A `StatesFacade` containing all cart states as a collection (maybe an empty collection if there are no states).

### discount()

* The `discount()` methods creates a new discount line-item with the given type and value.

* **Returns** [`Shopware\Core\Checkout\Cart\Facade\DiscountFacade`](./cart-manipulation-script-services-reference#discountfacade).

  Returns the newly created discount line-item.

* **Arguments:**
  * *`string`* **key**: The id for the new discount.
  * *`string`* **type**: The type of the discount, e.g. `percentage`, `absolute`
  * *`float|\PriceCollection`* **value**: The value of the discount, a float for percentage discounts or a `PriceCollection` for absolute discounts.
  * *`string`* **label**: The label of the discount line-item.

* **Examples:**
  * Add an absolute discount to the cart.

    ````
    ```twig
    {# @var services \Shopware\Core\Framework\Script\ServiceStubs #}
    {% do services.cart.products.add(hook.ids.get('p1')) %}

    {% if services.cart.items.count <= 0 %}
        {% return %}
    {% endif %}

    {% if services.cart.items.has('my-discount') %}
        {% return %}
    {% endif %}

    {% set price = services.cart.price.create({
        'default': { 'gross': -19.99, 'net': -19.99}
    }) %}

    {% do services.cart.discount('my-discount', 'absolute', price, 'Fancy discount') %}
    ```
    ````

  * Add a relative discount to the cart.

    ````
    ```twig
    {# @var services \Shopware\Core\Framework\Script\ServiceStubs #}

    {% do services.cart.products.add(hook.ids.get('p1')) %}

    {% if services.cart.has('my-discount') %}
        {% return %}
    {% endif %}

    {% do services.cart.discount('my-discount', 'percentage', -10, 'Fancy discount') %}
    ```
    ````

### surcharge()

* The `surcharge()` methods creates a new surcharge line-item with the given type and value.

* **Returns** [`Shopware\Core\Checkout\Cart\Facade\DiscountFacade`](./cart-manipulation-script-services-reference#discountfacade).

  Returns the newly created surcharge line-item.

* **Arguments:**
  * *`string`* **key**: The id for the new surcharge.
  * *`string`* **type**: The type of the surcharge, e.g. `percentage`, `absolute`
  * *`float|\PriceCollection`* **value**: The value of the surcharge, a float for percentage surcharges or a `PriceCollection` for absolute surcharges.
  * *`string`* **label**: The label of the surcharge line-item.

* **Examples:**

  * Add an absolute surcharge to the cart.#

    ````
    ```twig
    {# @var services \Shopware\Core\Framework\Script\ServiceStubs #}
    {% do services.cart.products.add(hook.ids.get('p1')) %}

    {% set price = services.cart.price.create({
        'default': { 'gross': 19.99, 'net': 19.99}
    }) %}

    {% do services.cart.surcharge('my-surcharge', 'absolute', price, 'Fancy surcharge') %}
    ```
    ````

  * Add a relative surcharge to the cart.

    ````
    ```twig
    {# @var services \Shopware\Core\Framework\Script\ServiceStubs #}

    {% do services.cart.products.add(hook.ids.get('p1')) %}

    {% if services.cart.has('my-surcharge') %}
        {% return %}
    {% endif %}

    {% do services.cart.surcharge('my-surcharge', 'percentage', -10, 'Fancy discount') %}
    ```
    ````

### get()

* `get()` returns the line-item with the given id from this collection.

* **Returns** [`Shopware\Core\Checkout\Cart\Facade\ItemFacade`](./cart-manipulation-script-services-reference#itemfacade) | `null`

  The line-item with the given id, or null if it does not exist.

* **Arguments:**
  * *`string`* **id**: The id of the line-item that should be returned.

### remove()

* `remove()` removes the given line-item or the line-item with the given id from this collection.

* **Arguments:**

  * *`string|\ItemFacade`* **id**: The id of the line-item or the line-item that should be removed.

* **Examples:**

  * Add and then remove a product line-item from the cart.

    ````
    ```twig
    {% do services.cart.products.add(hook.ids.get('p1')) %}

    {% do services.cart.products.remove(hook.ids.get('p1')) %}
    ```
    ````

### has()

* `has()` checks if a line-item with the given id exists in this collection.

* **Returns** `bool`

  Returns true if the given line-item or a line-item with the given id already exists in the collection, false otherwise.

* **Arguments:**

  * *`string|\ItemFacade`* **id**: The id or a line-item that should be checked if it already exists in the collection.

### count()

* `count()` returns the count of line-items in this collection.

  Note that it does only count the line-items directly in this collection and not child line-items of those.

* **Returns** `int`

  The number of line-items in this collection.

***

## [`Shopware\Core\Checkout\Cart\Facade\CartPriceFacade`](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Facade/CartPriceFacade.php) {#cartpricefacade}

The CartPriceFacade is a wrapper around the calculated price of a cart.

### getNet()

* `getNet()` returns the net price of the cart.

* **Returns** `float`

  Returns the net price of the cart as float.

### getTotal()

* `getTotal()` returns the total price of the cart that has to be paid by the customer.

  Depending on the tax settings this may be the gross or net price. Note that this price is already rounded, to get the raw price before rounding use `getRaw()`.

* **Returns** `float`

  The rounded total price of the cart as float.

### getPosition()

* `getPosition()` returns the sum price of all line-items in the cart.

  In the position price the shipping costs are excluded. Depending on the tax settings this may be the gross or net price og the line-items.

* **Returns** `float`

  The position price as float.

### getRounded()

* Alias for `getTotal()`.

* **Returns** `float`

  The rounded total price of the cart as float.

### getRaw()

* \`getRaw() returns the total price of the cart before rounding.

* **Returns** `float`

  The total price before rounding as float.

### create()

* `create()` creates a new `PriceCollection` based on an array of prices.

* **Returns** [`Shopware\Core\Framework\DataAbstractionLayer\Pricing\PriceCollection`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/DataAbstractionLayer/Pricing/PriceCollection.php)

  Returns the newly created `PriceCollection`.

* **Arguments:**

  * *`array`* **price**: The prices for the new collection, indexed by the currency-id or iso-code of the currency.

* **Examples:**

  * Create a new Price in the default currency.

    ````
    ```twig
    {% set price = services.cart.price.create({
        'default': { 'gross': 19.99, 'net': 19.99}
    }) %}
    ```
    ````

***

## [`Shopware\Core\Checkout\Cart\Facade\ContainerFacade`](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Cart/Facade/ContainerFacade.php) {#containerfacade}

The ContainerFacade allows you to wrap multiple line-items inside a container line-item.

### products()

* The `product()` method returns all products inside the current container for further manipulation.

  Similar to the `children()` method, but the line-items are filtered, to only contain product line items.

* **Returns** [`Shopware\Core\Checkout\Cart\Facade\ProductsFacade`](./cart-manipulation-script-services-reference#productsfacade)

  A `ProductsFacade` containing all product line-items inside the current container as a collection.

### add()

* Use the `add()` method to add an item to this container.

* **Returns** [`Shopware\Core\Checkout\Cart\Facade\ItemFacade`](./cart-manipulation-script-services-reference#itemfacade)

  The item that was added to the container.

* **Arguments:**

  * *[`Shopware\Core\Checkout\Cart\Facade\ItemFacade`](./cart-manipulation-script-services-reference#itemfacade)* **item**: The item that should be added.

* **Examples:**

  * Add a product to the container and reduce the quantity of the original line-item.

    ````
    ```twig

    ```
    ````

### getPrice()

* `getPrice()` returns the calculated price of the line-item.

* **Returns** [`Shopware\Core\Checkout\Cart\Facade\PriceFacade`](./cart-manipulation-script-services-reference#pricefacade) | `null`

  Returns the price of the line-item as a `PriceFacade` or null if the line-item has no calculated price.

### take()

* `take()` splits an existing line-item by a given quantity.

  It removes the given quantity from the existing line-item and returns a new line-item with exactly that quantity.

* **Returns** [`Shopware\Core\Checkout\Cart\Facade\ItemFacade`](./cart-manipulation-script-services-reference#itemfacade) | `null`

  Returns the new line-item as an `ItemFacade` or null if taking is not possible because the line-item has no sufficient quantity.

* **Arguments:**

  * *`int`* **quantity**: The quantity that should be taken.
  * *`string` | `null`* **key**: Optional: The id of the new line-item. A random UUID will be used if none is provided.

    ```
    Default: `null`.
    ```

* **Examples:**

  * Take a quantity of 2 from an existing product line-item and add it to the cart again.

    ````
    ```twig
    {# @var services \Shopware\Core\Framework\Script\ServiceStubs #}

    {% do services.cart.products.add(hook.ids.get('p1'), 5) %}

    {% set product = services.cart.products.get(hook.ids.get('p1')) %}

    {% set split = product.take(2, 'new-key') %}

    {% do services.cart.products.add(split)

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/resources/references/app-reference/script-reference/cart-manipulation-script-services-reference.md


---

## Custom Endpoint script services reference
**Source:** [resources/references/app-reference/script-reference/custom-endpoint-script-services-reference.md](https://developer.shopware.com/docs/v6.6/resources/references/app-reference/script-reference/custom-endpoint-script-services-reference.md)  
# Custom Endpoint script services reference

## [services.cache (`Shopware\Core\Framework\Adapter\Cache\Script\Facade\CacheInvalidatorFacade`)](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Adapter/Cache/Script/Facade/CacheInvalidatorFacade.php) {#cacheinvalidatorfacade}

The `cache` service allows you to invalidate the cache if some entity is updated.

### invalidate()

* `invalidate()` allows you to invalidate all cache entries with the given tag.

* **Arguments:**
  * *`array`* **tags**: The tags for which all cache entries should be invalidated as array.

* **Examples:**
  * Invalidate a hard coded tag.

    ```twig
    {% do services.cache.invalidate(['my-tag']) %}
    ```

  * Build tags based on written entities and invalidate those tags.

    ```twig
    {% set ids = hook.event.getIds('product_manufacturer') %}

    {% if ids.empty %}
        {% return %}
    {% endif %}

    {% set tags = [] %}
    {% for id in ids %}
        {% set tags = tags|merge(['my-manufacturer-' ~ id]) %}
    {% endfor %}

    {% do services.cache.invalidate(tags) %}
    ```

  * Build tags if products with a specific property is created and invalidate those tags.

    ```twig
    {% set ids = hook.event.getIds('product') %}

    {% set ids = ids.only('insert').with('description', 'parentId') %}
    {% if ids.empty %}
        {% return %}
    {% endif %}

    {% set tags = [] %}
    {% for id in ids %}
        {% set tags = tags|merge(['my-product-' ~ id]) %}
    {% endfor %}

    {% do services.cache.invalidate(tags) %}
    ```

***

## [services.writer (`Shopware\Core\Framework\DataAbstractionLayer\Facade\RepositoryWriterFacade`)](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/DataAbstractionLayer/Facade/RepositoryWriterFacade.php) {#repositorywriterfacade}

The `writer` service allows you to write data, that is stored inside shopware.
Keep in mind that your app needs to have the correct permissions for the data it writes through this service.

### upsert()

* The `upsert()` method allows you to create or update entities inside the database.

  If you pass an `id` in the payload it will do an update if an entity with that `id` already exists, otherwise it will be a create.
* **Returns** [`Shopware\Core\Framework\DataAbstractionLayer\Event\EntityWrittenContainerEvent`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/DataAbstractionLayer/Event/EntityWrittenContainerEvent.php)

  The WriteEvents that were generated by executing the `upsert()`.
* **Arguments:**
  * *`string`* **entityName**: The name of the entity you want to upsert, e.g. `product` or `media`.
  * *`array`* **payload**: The payload you want to upsert, as a list of associative arrays, where each associative array represents the payload for one entity.
* **Examples:**
  * Create a new entity.

    ```twig
    {% do services.writer.upsert('tax', [
        { 'name': 'new Tax', 'taxRate': 99.9 }
    ]) %}
    ```

  * Update an existing entity.

    ```twig
    {% do services.writer.upsert('product', [
        { 'id':  hook.productId, 'active': true }
    ]) %}
    ```

### delete()

* The `delete()` method allows you to delete entities from the database.

* **Returns** [`Shopware\Core\Framework\DataAbstractionLayer\Event\EntityWrittenContainerEvent`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/DataAbstractionLayer/Event/EntityWrittenContainerEvent.php)

  The WriteEvents that were generated by executing the `delete()`.

* **Arguments:**
  * *`string`* **entityName**: The name of the entity you want to delete, e.g. `product` or `media`.
  * *`array`* **payload**: The primary keys of the entities you want to delete, as a list of associative arrays, associative array represents the primary keys for one entity.

* **Examples:**
  * Delete an entity.

    ```twig
    {% do services.writer.delete('product', [
        { 'id':  hook.productId }
    ]) %}
    ```

### sync()

* The `sync()` method allows you to execute updates and deletes to multiple entities in one method call.

* **Returns** [`Shopware\Core\Framework\Api\Sync\SyncResult`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Api/Sync/SyncResult.php)

  The result of the `sync()`.

* **Arguments:**
  * *`array`* **payload**: All operations that should be executed.

* **Examples:**
  * Update an entity and delete another one with one `sync()` call.

    ```twig
    {% set payload = [
        {
            'entity': 'product',
            'action': 'upsert',
            'payload': [
                { 'id':  hook.updateProductId, 'active': true }
            ]
        },
        {
            'entity': 'product',
            'action': 'delete',
            'payload': [
            { 'id':  hook.deleteProductId }
        ]
        },
    ] %}

    {% do services.writer.sync(payload) %}
    ```

***

## [services.response (`Shopware\Core\Framework\Script\Api\ScriptResponseFactoryFacade`)](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Script/Api/ScriptResponseFactoryFacade.php) {#scriptresponsefactoryfacade}

The `response` service allows you to create HTTP-Responses.

### json()

* The `json()` method allows you to create a JSON-Response.

* **Returns** [`Shopware\Core\Framework\Script\Api\ScriptResponse`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Script/Api/ScriptResponse.php)

  The created response object, remember to assign it to the hook with `hook.setResponse()`.

* **Arguments:**
  * *`array`* **data**: The data that should be sent in the response as array.
  * *`int`* **code**: The HTTP-Status-Code of the response, defaults to 200.

    Default: `200`

* **Examples:**
  * Return hard coded values as JsonResponse.

    ```twig
    {% set response = services.response.json({ 'foo': 'bar' }) %}
    {% do hook.setResponse(response) %}
    ```

  * Search for products and return them in a JsonResponse.

    ```twig
    {# @var services \Shopware\Core\Framework\Script\ServiceStubs #}
    {% set products = services.repository.search('product', hook.request) %}

    {% set response = services.response.json({ 'products': products }) %}
    {% do hook.setResponse(response) %}
    ```

  * Provide a response to a ActionButtons request from the administration.

    ```twig
    {% set ids = hook.request.ids %}

    {% set response = services.response.json({
        "actionType": "notification",
        "payload": {
            "status": "success",
            "message": "You selected " ~ ids|length ~ " products."
        }
    }) %}

    {% do hook.setResponse(response) %}
    ```

### redirect()

* The `redirect()` method allows you to create a RedirectResponse.

* **Returns** [`Shopware\Core\Framework\Script\Api\ScriptResponse`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Script/Api/ScriptResponse.php)

  The created response object, remember to assign it to the hook with `hook.setResponse()`.

* **Arguments:**
  * *`string`* **route**: The name of the route that should be redirected to.
  * *`array`* **parameters**: The parameters needing to generate the URL of the route as an associative array.
  * *`int`* **code**: he HTTP-Status-Code of the response, defaults to 302.

    Default: `302`

* **Examples:**
  * Redirect to an Admin-API route.

    ```twig
    {% set response = services.response.redirect('api.product.detail', { 'path': productId }) %}
    {% do hook.setResponse(response) %}
    ```

  * Redirect to a storefront page.

    ```twig
    {% set response = services.response.redirect('frontend.detail.page', { 'productId': productId }) %}
    {% do hook.setResponse(response) %}
    ```

### render()

* The `render()` method allows you to render a twig view with the parameters you provide and create a StorefrontResponse.

  Note that the `render()` method will throw an exception if it is called from outside a `SalesChannelContext` (e.g. from an `/api` route)
  or if the Storefront-bundle is not installed.
* **Returns** [`Shopware\Core\Framework\Script\Api\ScriptResponse`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Script/Api/ScriptResponse.php)

  The created response object with the rendered template as content, remember to assign it to the hook with `hook.setResponse()`.
* **Arguments:**
  * *`string`* **view**: The name of the twig template you want to render e.g. `@Storefront/storefront/page/content/detail.html.twig`
  * *`array`* **parameters**: The parameters you want to pass to the template, ensure that you pass the `page` parameter from the hook to the templates.

    Default: `array (
    )`
* **Examples:**
  * Fetch a product, add it to the page and return a rendered response.

    ```twig
    {% set product = services.store.search('product', { 'ids': [productId]}).first %}

    {% do hook.page.addExtension('myProduct', product) %}

    {% do hook.setResponse(
        services.response.render('@MyApp/storefront/page/custom-page/index.html.twig', { 'page': hook.page })
    ) %}
    ```

***

---

---

## Data Loading script services reference
**Source:** [resources/references/app-reference/script-reference/data-loading-script-services-reference.md](https://developer.shopware.com/docs/v6.6/resources/references/app-reference/script-reference/data-loading-script-services-reference.md)  
# Data Loading script services reference

## [services.repository (`Shopware\Core\Framework\DataAbstractionLayer\Facade\RepositoryFacade`)](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/DataAbstractionLayer/Facade/RepositoryFacade.php) {#repositoryfacade}

The `repository` service allows you to query data, that is stored inside shopware.
Keep in mind that your app needs to have the correct permissions for the data it queries through this service.

### search()

* The `search()` method allows you to search for Entities that match a given criteria.

* **Returns** [`Shopware\Core\Framework\DataAbstractionLayer\Search\EntitySearchResult`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/DataAbstractionLayer/Search/EntitySearchResult.php)

  A `EntitySearchResult` including all entities that matched your criteria.

* **Arguments:**
  * *`string`* **entityName**: The name of the Entity you want to search for, e.g. `product` or `media`.
  * *`array`* **criteria**: The criteria used for your search.

* **Examples:**
  * Load a single product.

    ```twig
    {% set page = hook.page %}
    {# @var page \Shopware\Storefront\Page\Page #}

    {% set criteria = {
        'ids': [ hook.productId ]
    } %}

    {% set product = services.repository.search('product', criteria).first %}

    {% do page.addExtension('myProduct', product) %}
    ```

  * Filter the search result.

    ```twig
    {% set page = hook.page %}
    {# @var page \Shopware\Storefront\Page\Page #}

    {% set criteria = {
        'filter': [
            { 'field': 'productNumber', 'type': 'equals', 'value': 'p1' }
        ]
    } %}

    {% set product = services.repository.search('product', criteria).first %}

    {% do page.addExtension('myProduct', product) %}
    ```

  * Add associations that should be included in the result.

    ```twig
    {% set page = hook.page %}
    {# @var page \Shopware\Storefront\Page\Page #}

    {% set criteria = {
        'ids': [ hook.productId ],
        'associations': {
            'manufacturer': {}
        }
    } %}

    {% set product = services.repository.search('product', criteria).first %}

    {% do page.addExtension('myProduct', product) %}
    {% do page.addExtension('myManufacturer', product.manufacturer) %}
    ```

### ids()

* The `ids()` method allows you to search for the Ids of Entities that match a given criteria.

* **Returns** [`Shopware\Core\Framework\DataAbstractionLayer\Search\IdSearchResult`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/DataAbstractionLayer/Search/IdSearchResult.php)

  A `IdSearchResult` including all entity-ids that matched your criteria.

* **Arguments:**
  * *`string`* **entityName**: The name of the Entity you want to search for, e.g. `product` or `media`.
  * *`array`* **criteria**: The criteria used for your search.

* **Examples:**
  * Get the Ids of products with the given ProductNumber.

    ```twig
    {% set page = hook.page %}
    {# @var page \Shopware\Storefront\Page\Page #}

    {% set criteria = {
        'filter': [
            { 'field': 'productNumber', 'type': 'equals', 'value': 'p1' }
        ]
    } %}

    {% set productIds = services.repository.ids('product', criteria).ids %}

    {% do page.addArrayExtension('myProductIds', {
        'ids': productIds
    }) %}
    ```

### aggregate()

* The `aggregate()` method allows you to execute aggregations specified in the given criteria.

* **Returns** [`Shopware\Core\Framework\DataAbstractionLayer\Search\AggregationResult\AggregationResultCollection`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/DataAbstractionLayer/Search/AggregationResult/AggregationResultCollection.php)

  A `AggregationResultCollection` including the results of the aggregations you specified in the criteria.

* **Arguments:**
  * *`string`* **entityName**: The name of the Entity you want to aggregate data on, e.g. `product` or `media`.
  * *`array`* **criteria**: The criteria that define your aggregations.

* **Examples:**
  * Aggregate data for multiple entities, e.g. the sum of the gross price of all products.

    ```twig
    {% set page = hook.page %}
    {# @var page \Shopware\Storefront\Page\Page #}

    {% set criteria = {
        'aggregations': [
            { 'name': 'sumOfPrices', 'type': 'sum', 'field': 'price.gross' }
        ]
    } %}

    {% set sumResult = services.repository.aggregate('product', criteria).get('sumOfPrices') %}

    {% do page.addArrayExtension('myProductAggregations', {
        'sum': sumResult.getSum
    }) %}
    ```

***

## [services.store (`Shopware\Core\Framework\DataAbstractionLayer\Facade\SalesChannelRepositoryFacade`)](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/DataAbstractionLayer/Facade/SalesChannelRepositoryFacade.php) {#saleschannelrepositoryfacade}

The `store` service can be used to access publicly available `store-api` data.
As the data is publicly available your app does not need any additional permissions to use this service,
however querying data and also loading associations is restricted to the entities that are also available through the `store-api`.

Notice that the returned entities are already processed for the storefront,
this means that e.g. product prices are already calculated based on the current context.

### search()

* The `search()` method allows you to search for Entities that match a given criteria.

* **Returns** [`Shopware\Core\Framework\DataAbstractionLayer\Search\EntitySearchResult`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/DataAbstractionLayer/Search/EntitySearchResult.php)

  A `EntitySearchResult` including all entities that matched your criteria.

* **Arguments:**
  * *`string`* **entityName**: The name of the Entity you want to search for, e.g. `product` or `media`.
  * *`array`* **criteria**: The criteria used for your search.

* **Examples:**
  * Load a single storefront product.

    ```twig
    {% set page = hook.page %}
    {# @var page \Shopware\Storefront\Page\Page #}

    {% set criteria = {
        'ids': [ hook.productId ]
    } %}

    {% set product = services.store.search('product', criteria).first %}

    {% do page.addExtension('myProduct', product) %}
    ```

  * Filter the search result.

    ```twig
    {% set page = hook.page %}
    {# @var page \Shopware\Storefront\Page\Page #}

    {% set criteria = {
        'filter': [
            { 'field': 'productNumber', 'type': 'equals', 'value': 'p1' }
        ]
    } %}

    {% set product = services.store.search('product', criteria).first %}

    {% do page.addExtension('myProduct', product) %}
    ```

  * Add associations that should be included in the result.

    ```twig
    {% set page = hook.page %}
    {# @var page \Shopware\Storefront\Page\Page #}

    {% set criteria = {
        'ids': [ hook.productId ],
        'associations': {
            'manufacturer': {}
        }
    } %}

    {% set product = services.store.search('product', criteria).first %}

    {% do page.addExtension('myProduct', product) %}
    {% do page.addExtension('myManufacturer', product.manufacturer) %}
    ```

### ids()

* The `ids()` method allows you to search for the Ids of Entities that match a given criteria.

* **Returns** [`Shopware\Core\Framework\DataAbstractionLayer\Search\IdSearchResult`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/DataAbstractionLayer/Search/IdSearchResult.php)

  A `IdSearchResult` including all entity-ids that matched your criteria.

* **Arguments:**
  * *`string`* **entityName**: The name of the Entity you want to search for, e.g. `product` or `media`.
  * *`array`* **criteria**: The criteria used for your search.

* **Examples:**
  * Get the Ids of products with the given ProductNumber.

    ```twig
    {% set page = hook.page %}
    {# @var page \Shopware\Storefront\Page\Page #}

    {% set criteria = {
        'filter': [
            { 'field': 'productNumber', 'type': 'equals', 'value': 'p1' }
        ]
    } %}

    {% set productIds = services.store.ids('product', criteria).ids %}

    {% do page.addArrayExtension('myProductIds', {
        'ids': productIds
    }) %}
    ```

### aggregate()

* The `aggregate()` method allows you to execute aggregations specified in the given criteria.

* **Returns** [`Shopware\Core\Framework\DataAbstractionLayer\Search\AggregationResult\AggregationResultCollection`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/DataAbstractionLayer/Search/AggregationResult/AggregationResultCollection.php)

  A `AggregationResultCollection` including the results of the aggregations you specified in the criteria.

* **Arguments:**
  * *`string`* **entityName**: The name of the Entity you want to aggregate data on, e.g. `product` or `media`.
  * *`array`* **criteria**: The criteria that define your aggregations.

* **Examples:**
  * Aggregate data for multiple entities, e.g. the sum of the children of all products.

    ```twig
    {% set page = hook.page %}
    {# @var page \Shopware\Storefront\Page\Page #}

    {% set criteria = {
        'aggregations': [
            { 'name': 'sumOfChildren', 'type': 'sum', 'field': 'childCount' }
        ]
    } %}

    {% set sumResult = services.store.aggregate('product', criteria).get('sumOfChildren') %}

    {% do page.addArrayExtension('myProductAggregations', {
        'sum': sumResult.getSum
    }) %}
    ```

***

---

---

## Miscellaneous script services reference
**Source:** [resources/references/app-reference/script-reference/miscellaneous-script-services-reference.md](https://developer.shopware.com/docs/v6.6/resources/references/app-reference/script-reference/miscellaneous-script-services-reference.md)  
# Miscellaneous script services reference

## [`Shopware\Core\Framework\Script\Facade\ArrayFacade`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Script/Facade/ArrayFacade.php) {#arrayfacade}

The ArrayFacade acts as a wrapper around an array and allows easier manipulation of arrays inside scripts.
An array facade can also be accessed like a "normal" array inside twig.
Examples:

```twig
{% do array.push('test') %}

{% do array.foo = 'bar' }

{% do array.has('foo') }

{% if array.foo === 'bar' %}

{% foreach array as key => value %}
```

### set()

* `set()` adds a new element to the array using the given key.

* **Arguments:**
  * *`string|int`* **key**: The array key.
  * *`mixed`* **value**: The value that should be added.

* **Examples:**
  * Add a new element with key `test` and value 1.

    ```twig
    {% set product = services.cart.products.get(hook.ids.get('p1')) %}

    {% do product.payload.set('test', 1) %}
    ```

### push()

* `push()` adds a new value to the end of the array.

* **Arguments:**
  * *`mixed`* **value**: The value that should be added.

### removeBy()

* `removeBy()` removes the value at the given index from the array.

* **Arguments:**
  * *`string|int`* **index**: The index that should be removed.

### remove()

* `remove()` removes the given value from the array. It does nothing if the provided value does not exist in the array.

* **Arguments:**
  * *`mixed`* **value**: The value that should be removed.

### reset()

* `reset()` removes all entries from the array.

### merge()

* `merge()` recursively merges the array with the given array.

* **Arguments:**
  * *`array&lt;string|int,mixed&gt;|\ArrayFacade`* **array**: The array that should be merged with this array. Either a plain `array` or another `ArrayFacade`.

* **Examples:**
  * Merge two arrays.

    ```twig
    {% set my_array = array({'bar': 'foo', 'baz': true}) %}

    {% do product.payload.merge(my_array) %}
    ```

### replace()

* `replace()` recursively replaces elements from the given array into this array.

* **Arguments:**
  * *`array&lt;string|int,mixed&gt;|\ArrayFacade`* **array**: The array from which the elements should be replaced into this array. Either a plain `array` or another `ArrayFacade`.

* **Examples:**
  * Replace elements in the product payload array.

    ```twig
    {% set second = array({'bar': 'baz'}) %}

    {% do product.payload.replace(second) %}
    ```

### count()

* `count()` returns the count of elements inside this array.

* **Returns** `int`

  Returns the count of elements.

### all()

* `all()` function returns all elements of this array.

* **Returns** `array`

  Returns all elements of this array.

***

## [services.config (`Shopware\Core\System\SystemConfig\Facade\SystemConfigFacade`)](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SystemConfig/Facade/SystemConfigFacade.php) {#systemconfigfacade}

The `config` service allows you to access the shop's and your app's configuration values.

### get()

* The `get()` method allows you to access all config values of the store.

  Notice that your app needs the `system_config:read` privilege to use this method.

* **Returns** `array|bool|float|int|string|null`

* **Arguments:**
  * *`string`* **key**: The key of the configuration value e.g. `core.listing.defaultSorting`.
  * *`string` | `null`* **salesChannelId**: The SalesChannelId if you need the config value for a specific SalesChannel, if you don't provide a SalesChannelId, the one of the current Context is used as default.

    Default: `null`

* **Examples:**
  * Read an arbitrary system\_config value.

    ```twig
    {% set systemConfig = services.config.get('core.listing.productsPerPage') %}
    ```

### app()

* The `app()` method allows you to access the config values your app's configuration.

  Notice that your app does not need any additional privileges to use this method, as you can only access your own app's configuration.

* **Returns** `array|bool|float|int|string|null`

* **Arguments:**
  * *`string`* **key**: The name of the configuration value specified in the config.xml e.g. `exampleTextField`.
  * *`string` | `null`* **salesChannelId**: The SalesChannelId if you need the config value for a specific SalesChannel, if you don't provide a SalesChannelId, the one of the current Context is used as default.

    Default: `null`

* **Examples:**
  * Read your app's config value.

    ```twig
    {% set appConfig = services.config.app('app_config') %}
    ```

***

---

---

## Product script services reference
**Source:** [resources/references/app-reference/script-reference/product-script-services-reference.md](https://developer.shopware.com/docs/v6.6/resources/references/app-reference/script-reference/product-script-services-reference.md)  
# Product script services reference

## [`Shopware\Core\Content\Product\Hook\Pricing\PriceCollectionFacade`](https://github.com/shopware/shopware/blob/trunk/src/Core/Content/Product/Hook/Pricing/PriceCollectionFacade.php) {#pricecollectionfacade}

The PriceCollectionFacade is a wrapper around the calculated price collection of a product. It allows to manipulate the quantity
prices by resetting or changing the price collection.

### reset()

* The `reset()` functions allows to reset the complete price collection.

### change()

* The `change()` function allows a complete overwrite of the product quantity prices

* **Arguments:**
  * *`array`* **changes**:

* **Examples:**
  * Overwrite the product prices with a new quantity price graduation

    ```twig
    {% do debug.dump(product.calculatedPrice.unit, 'discount') %}

    {% do product.calculatedPrice.surcharge(10) %}

    {% do debug.dump(product.calculatedPrice.unit, 'surcharge') %}
    ```

### count()

* The `count()` function returns the number of prices which are stored inside this collection.

* **Returns** `int`

  Returns the number of prices which are stored inside this collection

***

## [`Shopware\Core\Content\Product\Hook\Pricing\ProductProxy`](https://github.com/shopware/shopware/blob/trunk/src/Core/Content/Product/Hook/Pricing/ProductProxy.php) {#productproxy}

The `ProductProxy` is a wrapper for the `SalesChannelProductEntity`. It provides access to all properties of the product,
but also wraps some data into helper facade classes like `PriceFacade` or `PriceCollectionFacade`.

### \_\_get()

* The `__get()` function allows access to all properties of the [SalesChannelProductEntity](https://github.com/shopware/shopware/blob/trunk/src/Core/Content/Product/SalesChannel/SalesChannelProductEntity.php)

* **Returns** `mixed` | `null`

  Returns the value of the property. The value is `mixed` due to the fact that all properties are accessed via `__get()`

* **Arguments:**
  * *`string`* **name**: Name of the property to access

* **Examples:**
  * Access the product properties

    ```twig
    { to: 30, price: services.price.create({ 'default': { 'gross': 10, 'net': 10} }) },
        { to: null, price: services.price.create({ 'default': { 'gross': 5, 'net': 5} }) },
    ]) %}
    ```

### calculatedCheapestPrice()

* The `calculatedCheapestPrice` property returns the cheapest price of the product. The price object will
  be wrapped into a `PriceFacade` object which allows to manipulate the price.

* **Returns** [`Shopware\Core\Checkout\Cart\Facade\PriceFacade`](./cart-manipulation-script-services-reference#pricefacade) | `null`

  Returns a `PriceFacade` if the product has a calculated cheapest price, otherwise `null`

### calculatedPrice()

* The `calculatedPrice` property returns the price of the product. The price object will
  be wrapped into a `PriceFacade` object which allows to manipulate the price.

* **Returns** [`Shopware\Core\Checkout\Cart\Facade\PriceFacade`](./cart-manipulation-script-services-reference#pricefacade) | `null`

  Returns a `PriceFacade` if the product has a price, otherwise `null`

### calculatedPrices()

* The `calculatedPrices` property returns the price of the product. The price object will
  be wrapped into a `PriceCollectionFacade` object which allows to manipulate the collection.

* **Returns** [`Shopware\Core\Content\Product\Hook\Pricing\PriceCollectionFacade`](./product-script-services-reference#pricecollectionfacade) | `null`

  Returns a `PriceCollectionFacade` if the product has graduated prices, otherwise `null`

***

---

---

## List of all available Hooks for Scripts
**Source:** [resources/references/app-reference/script-reference/script-hooks-reference.md](https://developer.shopware.com/docs/v6.6/resources/references/app-reference/script-reference/script-hooks-reference.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# List of all available Hooks for Scripts

## Data Loading

All available Hooks that can be used to load additional data.

### payment-method-route-request

|                |                                 |
|:-----------------------|:----------------------------------------|
| **Name**               | payment-method-route-request                         |
| **Since**              | 6.5.0.0                        |
| **Class**              | `Shopware\Core\Checkout\Payment\Hook\PaymentMethodRouteHook`                      |
| **Description**        | Triggered when PaymentMethodRoute is requested                  |
| **Available Data**     | collection: [`Shopware\Core\Checkout\Payment\PaymentMethodCollection`](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Payment/PaymentMethodCollection.php)onlyAvailable: `bool`salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php)context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php)        |
| **Available Services** | [repository](./data-loading-script-services-reference#RepositoryFacade)[config](./miscellaneous-script-services-reference#SystemConfigFacade)[store](./data-loading-script-services-reference#SalesChannelRepositoryFacade) |
| **Stoppable**          | `false`                  |

### shipping-method-route-request

|                |                                 |
|:-----------------------|:----------------------------------------|
| **Name**               | shipping-method-route-request                         |
| **Since**              | 6.5.0.0                        |
| **Class**              | `Shopware\Core\Checkout\Shipping\Hook\ShippingMethodRouteHook`                      |
| **Description**        | Triggered when ShippingMethodRoute is requested                  |
| **Available Data**     | collection: [`Shopware\Core\Checkout\Shipping\ShippingMethodCollection`](https://github.com/shopware/shopware/blob/trunk/src/Core/Checkout/Shipping/ShippingMethodCollection.php)onlyAvailable: `bool`salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php)context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php)        |
| **Available Services** | [repository](./data-loading-script-services-reference#RepositoryFacade)[config](./miscellaneous-script-services-reference#SystemConfigFacade)[store](./data-loading-script-services-reference#SalesChannelRepositoryFacade) |
| **Stoppable**          | `false`                  |

### customer-group-registration-page-loaded

|                |                                 |
|:-----------------------|:----------------------------------------|
| **Name**               | customer-group-registration-page-loaded                         |
| **Since**              | 6.4.8.0                        |
| **Class**              | `Shopware\Storefront\Page\Account\CustomerGroupRegistration\CustomerGroupRegistrationPageLoadedHook`                      |
| **Description**        | Triggered when the CustomerGroupRegistrationPage is loaded                  |
| **Available Data**     | page: [`Shopware\Storefront\Page\Account\CustomerGroupRegistration\CustomerGroupRegistrationPage`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Page/Account/CustomerGroupRegistration/CustomerGroupRegistrationPage.php)context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php)salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php)        |
| **Available Services** | [repository](./data-loading-script-services-reference#RepositoryFacade)[config](./miscellaneous-script-services-reference#SystemConfigFacade)[store](./data-loading-script-services-reference#SalesChannelRepositoryFacade) |
| **Stoppable**          | `false`                  |

### account-guest-login-page-loaded

|                |                                 |
|:-----------------------|:----------------------------------------|
| **Name**               | account-guest-login-page-loaded                         |
| **Since**              | 6.4.8.0                        |
| **Class**              | `Shopware\Storefront\Page\Account\Login\AccountGuestLoginPageLoadedHook`                      |
| **Description**        | Triggered when the AccountGuestLoginPage is loaded                  |
| **Available Data**     | page: [`Shopware\Storefront\Page\Account\Login\AccountLoginPage`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Page/Account/Login/AccountLoginPage.php)context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php)salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php)        |
| **Available Services** | [repository](./data-loading-script-services-reference#RepositoryFacade)[config](./miscellaneous-script-services-reference#SystemConfigFacade)[store](./data-loading-script-services-reference#SalesChannelRepositoryFacade) |
| **Stoppable**          | `false`                  |

### account-login-page-loaded

|                |                                 |
|:-----------------------|:----------------------------------------|
| **Name**               | account-login-page-loaded                         |
| **Since**              | 6.4.8.0                        |
| **Class**              | `Shopware\Storefront\Page\Account\Login\AccountLoginPageLoadedHook`                      |
| **Description**        | Triggered when the AccountLoginPage is loaded                  |
| **Available Data**     | page: [`Shopware\Storefront\Page\Account\Login\AccountLoginPage`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Page/Account/Login/AccountLoginPage.php)context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php)salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php)        |
| **Available Services** | [repository](./data-loading-script-services-reference#RepositoryFacade)[config](./miscellaneous-script-services-reference#SystemConfigFacade)[store](./data-loading-script-services-reference#SalesChannelRepositoryFacade) |
| **Stoppable**          | `false`                  |

### account-edit-order-page-loaded

|                |                                 |
|:-----------------------|:----------------------------------------|
| **Name**               | account-edit-order-page-loaded                         |
| **Since**              | 6.4.8.0                        |
| **Class**              | `Shopware\Storefront\Page\Account\Order\AccountEditOrderPageLoadedHook`                      |
| **Description**        | Triggered when the AccountEditOrderPage is loaded                  |
| **Available Data**     | page: [`Shopware\Storefront\Page\Account\Order\AccountEditOrderPage`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Page/Account/Order/AccountEditOrderPage.php)context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php)salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php)        |
| **Available Services** | [repository](./data-loading-script-services-reference#RepositoryFacade)[config](./miscellaneous-script-services-reference#SystemConfigFacade)[store](./data-loading-script-services-reference#SalesChannelRepositoryFacade) |
| **Stoppable**          | `false`                  |

### account-order-detail-page-loaded

|                |                                 |
|:-----------------------|:----------------------------------------|
| **Name**               | account-order-detail-page-loaded                         |
| **Since**              | 6.4.8.0                        |
| **Class**              | `Shopware\Storefront\Page\Account\Order\AccountOrderDetailPageLoadedHook`                      |
| **Description**        | Triggered when the AccountOrderDetailPage is loaded                  |
| **Available Data**     | page: [`Shopware\Storefront\Page\Account\Order\AccountOrderDetailPage`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Page/Account/Order/AccountOrderDetailPage.php)context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php)salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php)        |
| **Available Services** | [repository](./data-loading-script-services-reference#RepositoryFacade)[config](./miscellaneous-script-services-reference#SystemConfigFacade)[store](./data-loading-script-services-reference#SalesChannelRepositoryFacade) |
| **Stoppable**          | `false`                  |

### account-order-page-loaded

|                |                                 |
|:-----------------------|:----------------------------------------|
| **Name**               | account-order-page-loaded                         |
| **Since**              | 6.4.8.0                        |
| **Class**              | `Shopware\Storefront\Page\Account\Order\AccountOrderPageLoadedHook`                      |
| **Description**        | Triggered when the AccountOrderPage is loaded                  |
| **Available Data**     | page: [`Shopware\Storefront\Page\Account\Order\AccountOrderPage`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Page/Account/Order/AccountOrderPage.php)context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php)salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php)        |
| **Available Services** | [repository](./data-loading-script-services-reference#RepositoryFacade)[config](./miscellaneous-script-services-reference#SystemConfigFacade)[store](./data-loading-script-services-reference#SalesChannelRepositoryFacade) |
| **Stoppable**          | `false`                  |

### account-overview-page-loaded

|                |                                 |
|:-----------------------|:----------------------------------------|
| **Name**               | account-overview-page-loaded                         |
| **Since**              | 6.4.8.0                        |
| **Class**              | `Shopware\Storefront\Page\Account\Overview\AccountOverviewPageLoadedHook`                      |
| **Description**        | Triggered when the AccountOverviewPage is loaded                  |
| **Available Data**     | page: [`Shopware\Storefront\Page\Account\Overview\AccountOverviewPage`](https://github.com/shopware/shopware/blob/trunk/src/Storefront/Page/Account/Overview/AccountOverviewPage.php)context: [`Shopware\Core\Framework\Context`](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/Context.php)salesChannelContext: [`Shopware\Core\System\SalesChannel\SalesChannelContext`](https://github.com/shopware/shopware/blob/trunk/src/Core/System/SalesChannel/SalesChannelContext.php)        |
| **Available Services** 

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/resources/references/app-reference/script-reference/script-hooks-reference.md


---

## Webhook Event Reference
**Source:** [resources/references/app-reference/webhook-events-reference.md](https://developer.shopware.com/docs/v6.6/resources/references/app-reference/webhook-events-reference.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Webhook Event Reference

| Event                                                            | Description                                                                 | Permissions needed                       | Payload                                                                                                       |
| :--------------------------------------------------------------- | :-------------------------------------------------------------------------- | :--------------------------------------- | :------------------------------------------------------------------------------------------------------------ |
| `checkout.customer.before.login`                                 | Triggers as soon as a customer logs in                                      | -                                        | `{"email":"string"}`                                                                                          |
| `checkout.customer.changed-payment-method`                       | Triggers when a customer changes his payment method in the checkout process | `customer:read`                          | `{"entity":"customer"}`                                                                                       |
| `checkout.customer.deleted`                                      | Triggers if a customer gets deleted                                         | `customer:read`                          | `{"entity":"customer"}`                                                                                       |
| `checkout.customer.double_opt_in_guest_order`                    | Triggers as soon as double opt-in is accepted in a guest order              | `customer:read`                          | `{"entity":"customer","confirmUrl":"string"}`                                                                 |
| `checkout.customer.double_opt_in_registration`                   | Triggers when a customer commits to his registration via double opt in      | `customer:read`                          | `{"entity":"customer","confirmUrl":"string"}`                                                                 |
| `checkout.customer.guest_register`                               | **EMPTY**                                                                   | `customer:read`                          | `{"entity":"customer"}`                                                                                       |
| `checkout.customer.login`                                        | Triggers as soon as a customer logs in                                      | `customer:read`                          | `{"entity":"customer","contextToken":"string"}`                                                               |
| `checkout.customer.logout`                                       | Triggers when a customer logs out                                           | `customer:read`                          | `{"entity":"customer"}`                                                                                       |
| `checkout.customer.register`                                     | Triggers when a new customer was registered                                 | `customer:read`                          | `{"entity":"customer"}`                                                                                       |
| `checkout.order.payment_method.changed`                          | **EMPTY**                                                                   | `order:read` `order_transaction:read`    | `{"entity":"order_transaction"}`                                                                              |
| `checkout.order.placed`                                          | Triggers when an order is placed                                            | `order:read`                             | `{"entity":"order"}`                                                                                          |
| `contact_form.send`                                              | Triggers when a contact form is send                                        | -                                        | `{"contactFormData":"object"}`                                                                                |
| `customer.group.registration.accepted`                           | **EMPTY**                                                                   | `customer:read` `customer_group:read`    | `{"entity":"customer_group"}`                                                                                 |
| `customer.group.registration.declined`                           | **EMPTY**                                                                   | `customer:read` `customer_group:read`    | `{"entity":"customer_group"}`                                                                                 |
| `customer.recovery.request`                                      | Triggers when a customer recovers his password                              | `customer_recovery:read` `customer:read` | `{"entity":"customer","resetUrl":"string","shopName":"string"}`                                               |
| `mail.after.create.message`                                      | **EMPTY**                                                                   | -                                        | `{"data":"array","message":"object"}`                                                                         |
| `mail.before.send`                                               | Triggers before a mail is send                                              | -                                        | `{"data":"array","templateData":"array"}`                                                                     |
| `mail.sent`                                                      | Triggers when a mail is send from Shopware                                  | -                                        | `{"subject":"string","contents":"string","recipients":"array"}`                                               |
| `newsletter.confirm`                                             | **EMPTY**                                                                   | `newsletter_recipient:read`              | `{"entity":"newsletter_recipient"}`                                                                           |
| `newsletter.register`                                            | **EMPTY**                                                                   | `newsletter_recipient:read`              | `{"entity":"newsletter_recipient","url":"string"}`                                                            |
| `newsletter.unsubscribe`                                         | **EMPTY**                                                                   | `newsletter_recipient:read`              | `{"entity":"newsletter_recipient"}`                                                                           |
| `product_export.log`                                             | **EMPTY**                                                                   | -                                        | `{"name":"string"}`                                                                                           |
| `review_form.send`                                               | Triggers when a product review form is send                                 | `product:read`                           | `{"reviewFormData":"object","entity":"product"}`                                                              |
| `state_enter.order.state.cancelled`                              | **EMPTY**                                                                   | `order:read`                             | `{"entity":"order"}`                                                                                          |
| `state_enter.order.state.completed`                              | **EMPTY**                                                                   | `order:read`                             | `{"entity":"order"}`                                                                                          |
| `state_enter.order.state.in_progress`                            | **EMPTY**                                                                   | `order:read`                             | `{"entity":"order"}`                                                                                          |
| `state_enter.order.state.open`                                   | **EMPTY**                                                                   | `order:read`                             | `{"entity":"order"}`                                                                                          |
| `state_enter.order_delivery.state.cancelled`                     | **EMPTY**                                                                   | `order:read`                             | `{"entity":"order"}`                                                                                          |
| `state_enter.order_delivery.state.open`                          | **EMPTY**                                                                   | `order:read`                             | `{"entity":"order"}`                                                                                          |
| `state_enter.order_delivery.state.returned`                      | **EMPTY**                                                                   | `order:read`                             | `{"entity":"order"}`                                                                                          |
| `state_enter.order_delivery.state.returned_partially`            | **EMPTY**                                                                   | `order:read`                             | `{"entity":"order"}`                                                                                          |
| `state_enter.order_delivery.state.shipped`                       | **EMPTY**                                                                   | `order:read`                             | `{"entity":"order"}`                                                                                          |
| `state_enter.order_delivery.state.shipped_partially`             | **EMPTY**                                                                   | `order:read`                             | `{"entity":"order"}`                                                                                          |
| `state_enter.order_transaction.state.authorized`                 | **EMPTY**                                                                   | `order:read`                             | `{"entity":"order"}`                                                                                          |
| `state_enter.order_transaction.state.cancelled`                  | **EMPTY**                                                                   | `order:read`                             | `{"entity":"order"}`                                                                                          |
| `state_enter.order_transaction.state.chargeback`                 | **EMPTY**                                                                   | `order:read`                             | `{"entity":"order"}`                                                                                          |
| `state_enter.order_transaction.state.failed`                     | **EMPTY**                                                                   | `order:read`                             | `{"entity":"order"}`                                                                                          |
| `state_enter.order_transaction.state.in_progress`                | **EMPTY**                                                                   | `order:read`                             | `{"en

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/resources/references/app-reference/webhook-events-reference.md


---

## Config Reference
**Source:** [resources/references/config-reference.md](https://developer.shopware.com/docs/v6.6/resources/references/config-reference.md)  
# Config Reference

This section gives you a reference on server configuration.

---

---

## Server
**Source:** [resources/references/config-reference/server.md](https://developer.shopware.com/docs/v6.6/resources/references/config-reference/server.md)  
# Server

This section gives you a reference on server configuration.

---

---

## Apache
**Source:** [resources/references/config-reference/server/apache.md](https://developer.shopware.com/docs/v6.6/resources/references/config-reference/server/apache.md)  
# Apache

::: info
The document root must always point to the public folder, to ensure all functionality works.
:::

```text
<VirtualHost *:80>
   ServerName "HOST_NAME"
   DocumentRoot _SHOPWARE_LOCATION_/public

   <Directory _SHOPWARE_LOCATION_>
      Options Indexes FollowSymLinks MultiViews
      AllowOverride All
      Order allow,deny
      allow from all
   </Directory>

   ErrorLog ${APACHE_LOG_DIR}/shopware.error.log
   CustomLog ${APACHE_LOG_DIR}/shopware.access.log combined
</VirtualHost>
```

---

---

## Caddy
**Source:** [resources/references/config-reference/server/caddy.md](https://developer.shopware.com/docs/v6.6/resources/references/config-reference/server/caddy.md)  
# Caddy

```text
mydomain.com {
  header {
    X-Frame-Options DENY
    Referrer-Policy no-referrer-when-downgrade
  }

  @svg {
    file
    path *.svg
  }

  header @svg Content-Security-Policy "script-src 'none'"

  @default {
    not path /theme/* /media/* /thumbnail/* /bundles/* /css/* /fonts/* /js/* /recovery/* /sitemap/*
  }

  root * public
  php_fastcgi 127.0.0.1:9000
  encode zstd gzip
  file_server
}
```

---

---

## Nginx
**Source:** [resources/references/config-reference/server/nginx.md](https://developer.shopware.com/docs/v6.6/resources/references/config-reference/server/nginx.md)  
# Nginx

::: info
The document root must always point to the public folder, to ensure all functionality works.
:::

```text
server {
    listen 80;

    index index.php index.html;
    server_name localhost;

    client_max_body_size 128M;

    root __DOCUMENT_ROOT__/public;

    # Shopware install / update    
    location /shopware-installer.phar.php {
    try_files $uri /shopware-installer.phar.php$is_args$args;
    }
    
    location ~ ^/shopware-installer\.phar\.php/.+\.(?:css|js|png|svg|woff)$ {
     try_files $uri /shopware-installer.phar.php$is_args$args;
    }

    # Deny access to . (dot) files
    location ~ /\. {
        deny all;
    }
    
    # Deny access to .php files in public directories
    location ~ ^/(media|thumbnail|theme|bundles|sitemap).*\.php$ {
        deny all;
    }
    
    location /recovery/install {
        index index.php;
        try_files $uri /recovery/install/index.php$is_args$args;
    }

    location /recovery/update/ {
        location /recovery/update/assets {
        }
        if (!-e $request_filename){
            rewrite . /recovery/update/index.php last;
        }
    }
    
    location ~ ^/(theme|media|thumbnail|bundles|css|fonts|js|recovery|sitemap)/ {
        expires 1y;
        add_header Cache-Control "public, must-revalidate, proxy-revalidate";
        log_not_found off;
        tcp_nodelay off;
        open_file_cache max=3000 inactive=120s;
        open_file_cache_valid 45s;
        open_file_cache_min_uses 2;
        open_file_cache_errors off;
    
        location ~* ^.+\.svg {
            add_header Content-Security-Policy "script-src 'none'";
            add_header Cache-Control "public, must-revalidate, proxy-revalidate";
            log_not_found off;
        }
    }

    location ~* ^.+\.(?:css|cur|js|jpe?g|gif|ico|png|svg|webp|html|woff|woff2|xml)$ {
        expires 1y;
        add_header Cache-Control "public, must-revalidate, proxy-revalidate";

        access_log off;

        # The directive enables or disables messages in error_log about files not found on disk.
        log_not_found off;

        tcp_nodelay off;

        ## Set the OS file cache.
        open_file_cache max=3000 inactive=120s;
        open_file_cache_valid 45s;
        open_file_cache_min_uses 2;
        open_file_cache_errors off;

        try_files $uri /index.php$is_args$args;
    }

    location ~* ^.+\.svg$ {
        add_header Content-Security-Policy "script-src 'none'";
    }

    location / {
        try_files $uri /index.php$is_args$args;
    }

    location ~ \.php$ {
        fastcgi_split_path_info ^(.+\.php)(/.+)$;
        include fastcgi.conf;
        fastcgi_param HTTP_PROXY "";
        fastcgi_buffers 8 16k;
        fastcgi_buffer_size 32k;
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
        send_timeout 300s;
        client_body_buffer_size 128k;
        fastcgi_pass 127.0.0.1:9000;
    }
}
```

---

---

## Core Reference
**Source:** [resources/references/core-reference.md](https://developer.shopware.com/docs/v6.6/resources/references/core-reference.md)  
# Core Reference

The Core reference documents essential components like the DAL, administration panel, flags, filters, Flow Builder, and Rules for efficient platform usage. It details about the classes, methods, commands, events, etc, for your reference. This helps you understand how to use these features to enhance the functionality.

---

---

## Actions Reference
**Source:** [resources/references/core-reference/actions-reference.md](https://developer.shopware.com/docs/v6.6/resources/references/core-reference/actions-reference.md)  
# Actions Reference

## B2B

| Class                                           | Description                                                    | Component           |
|:------------------------------------------------|:---------------------------------------------------------------|:--------------------|
| ChangeEmployeeStatusAction                      | Assigns the configured status to the employee                  | Employee Management |
| ChangeCustomerSpecificFeaturesAction            | Adds or removes the configured b2b components for the customer | Employee Management |

---

---

## Administration Reference
**Source:** [resources/references/core-reference/administration-reference.md](https://developer.shopware.com/docs/v6.4/resources/references/core-reference/administration-reference.md)  
# Administration Reference

---

---

## Directives reference
**Source:** [resources/references/core-reference/administration-reference/directives.md](https://developer.shopware.com/docs/v6.4/resources/references/core-reference/administration-reference/directives.md)  
# Directives reference

This is an overview of all the directives registered globally to Vue.
Directives are the same as normally in Vue, learn how to use them [here](./../../../../guides/plugins/plugins/administration/adding-directives)
Or see all of them in the folder [here](https://github.com/shopware/platform/tree/trunk/src/Administration/Resources/app/administration/src/app/directive)

## Overview of directives

| Name         | Task                                                        |
|--------------|-------------------------------------------------------------|
| `autofocus`  | Focuses an `<input>` in an element on insertion.            |
| `dragdrop`   | Enables the drag and drop functionality of the CMS.         |
| `popover`    | Directive for automatic edge detection of the element place |
| `responsive` | Adds methods to add responsive element classes              |
| `tooltip`    | Provides utility functions to display tooltips.           |

---

---

## Mixins
**Source:** [resources/references/core-reference/administration-reference/mixins.md](https://developer.shopware.com/docs/v6.4/resources/references/core-reference/administration-reference/mixins.md)  
# Mixins

This is an overview of all the mixins provided by the Shopware 6 Administration. Mixins in the Shopware 6 Administration are essentially the same in default Vue. They behave generally the same as they do in Vue normally, differing only in the registration and the way mixins are included in a component. Learn more about them in the official [Vue documentation](https://vuejs.org/v2/guide/mixins.html).

If you want to learn how to use them in your plugin, take a look at this guide [here](../../../../guides/plugins/plugins/administration/using-mixins) or if you want to register your own mixin take a look at this [guide](../../../../guides/plugins/plugins/administration/add-mixins)

## Overview of all the mixins

| Name | Description | Link |
| :--- | :--- | :--- |
| `discard-detail-page-changes` | Mixin which resets entity changes on page leave or if the id of the entity changes. This also affects changes in associations of the entity | [link](https://github.com/shopware/platform/blob/v6.3.4.1/src/Administration/Resources/app/administration/src/app/mixin/discard-detail-page-changes.mixin.js) |
| `listing` | Mixin which is used in almost all listing pages to for example keep track of the current page of the administration | [link](https://github.com/shopware/platform/blob/v6.3.4.1/src/Administration/Resources/app/administration/src/app/mixin/listing.mixin.js) |
| `notification` | This mixin is used to create notifications in the administrations more easily | [link](https://github.com/shopware/platform/blob/v6.3.4.1/src/Administration/Resources/app/administration/src/app/mixin/notification.mixin.js) |
| `placeholder` | Provides a function to localize placeholders | [link](https://github.com/shopware/platform/blob/v6.3.4.1/src/Administration/Resources/app/administration/src/app/mixin/placeholder.mixin.js) |
| `position` | A Mixin which contains helpers to work with position integers | [link](https://github.com/shopware/platform/blob/v6.3.4.1/src/Administration/Resources/app/administration/src/app/mixin/position.mixin.js) |
| `remove-api-error` | This mixin removes API errors e.g. after the user corrected a invalid input i.e. leaving the product name field blank | [link](https://github.com/shopware/platform/blob/v6.3.4.1/src/Administration/Resources/app/administration/src/app/mixin/remove-api-error.mixin.js) |
| `ruleContainer` | Provides common functions between the `sw-condition-or-container` and the `sw-condition-and-container` | [link](https://github.com/shopware/platform/blob/v6.3.4.1/src/Administration/Resources/app/administration/src/app/mixin/rule-container.mixin.js) |
| `salutation` | A common adapter for the `salutation` filter | [link](https://github.com/shopware/platform/blob/v6.3.4.1/src/Administration/Resources/app/administration/src/app/mixin/salutation.mixin.js) |
| `sw-form-field` | This mixin is used to provide common functionality between form fields | [link](https://github.com/shopware/platform/blob/v6.3.4.1/src/Administration/Resources/app/administration/src/app/mixin/form-field.mixin.js) |
| `sw-inline-snippet` | Makes it possible to use snippets inline | [link](https://github.com/shopware/platform/blob/v6.3.4.1/src/Administration/Resources/app/administration/src/app/mixin/sw-inline-snippet.mixin.js) |
| `validation` | Is used to validate inputs in various form fields | [link](https://github.com/shopware/platform/blob/v6.3.4.1/src/Administration/Resources/app/administration/src/app/mixin/validation.mixin.js) |

---

---

## Utils
**Source:** [resources/references/core-reference/administration-reference/utils.md](https://developer.shopware.com/docs/v6.4/resources/references/core-reference/administration-reference/utils.md)  
# Utils

This is an overview of all the utility functions bound to the shopware global object. Utility functions provide many useful shortcuts for common tasks, see how to use them in your plugin [here](../../../../guides/plugins/plugins/administration/using-utils). Or see the code that registers them [here](https://github.com/shopware/platform/blob/v6.3.4.1/src/Administration/Resources/app/administration/src/core/service/util.service.js)

## General functions

| Function | Description | Link |
| :--- | :--- | :--- |
| createId | Returns a uuid string in hex format. Generated with [uuid](https://www.npmjs.com/package/uuid) |  |
| throttle | Creates a `throttled` function that only invokes `func` at most once per every `wait` milliseconds. | [link](https://lodash.com/docs/4.17.15#throttle) |
| debounce | Creates a `debounced` function that delays invoking `func` until after `wait` milliseconds have elapsed since the last time the `debounced` function was invoked. | [link](https://lodash.com/docs/4.17.15#debounce) |
| flow | Creates a function that returns the result of invoking the given functions with the `this` binding of the created function, where each successive invocation is supplied the return value of the previous. | [link](https://lodash.com/docs/4.17.15#flow) |
| get | Gets the value at `path` of `object` | [link](https://lodash.com/docs/4.17.15#get) |

## Object

| Function | Description | Link |
| :--- | :--- | :--- |
| deepCopyObject | Deep copy an object |  |
| hasOwnProperty | Shorthand method for `Object.prototype.hasOwnProperty` |  |
| getObjectDiff | Gets a simple recursive diff of two objects. Does not consider an entity schema or entity related logic. |  |
| getArrayChanges | Check if the compared array has changes. |  |
| cloneDeep | Creates recursively a clone of value. | [link](https://lodash.com/docs/4.17.15#cloneDeep) |
| merge | This method is like \_.assign except that it recursively merges own and inherited enumerable string keyed properties of source objects into the destination object. | [link](https://lodash.com/docs/4.17.15#merge) |
| mergeWith | This method is like \_.merge except that it accepts customizer which is invoked to produce the merged values of the destination and source properties. | [link](https://lodash.com/docs/4.17.15#mergeWith) |
| deepMergeObject | Deep merge two objects |  |
| get | Gets the value at `path` of `object` | [link](https://lodash.com/docs/4.17.15#get) |
| set | Sets the value at `path` of `object` | [link](https://lodash.com/docs/4.17.15#set) |
| pick | Creates an object composed of the picked `object` properties. | [link](https://lodash.com/docs/4.17.15#pick) |

## Debug

| Function | Description |
| :--- | :--- |
| warn | General logging function which provides a unified style of log messages for developers. Please keep the log in mind. Messages will be displayed in the developer console when they're running the application in development mode. |
| debug | The same as `warn` but instead of `console.warn` it uses `console.error`. |

## Format

| Function | Description |
| :--- | :--- |
| currency | Converts a number to a formatted currency. Especially helpful for template filters. |
| date | Formats a Date object to a localized string with the [native `Intl.DateTimeFormat` method](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat) |
| fileSize | Formats a number of bytes to a string with a unit |
| md5 | Generates a md5 hash with [md5-es](https://www.npmjs.com/package/md5-es) of a given value. |

## Dom

| Function | Description |
| :--- | :--- |
| getScrollbarHeight | Returns the scrollbar height of an HTML element. |
| getScrollbarWidth | Returns the scrollbar width of an HTML element. |
| copyToClipboard | Uses the browser's copy function to copy a string |

## String

| Function | Description | Link |
| :--- | :--- | :--- |
| capitalizeString | Converts the first character of `string` to upper case and the remaining to lower case. | [link](https://lodash.com/docs/4.17.15#capitalize) |
| camelCase | Converts `string` to camel case. | [link](https://lodash.com/docs/4.17.15#camelCase) |
| kebabCase | Converts `string` to kebab case. | [link](https://lodash.com/docs/4.17.15#kebabCase) |
| snakeCase | Converts `string` to snake case. | [link](https://lodash.com/docs/4.17.15#snakeCase) |
| md5 | Generates a md5 hash with [md5-es](https://www.npmjs.com/package/md5-es) of a given value. |  |
| isEmptyOrSpaces | Gets if the content of the string is really empty. This does also removes any whitespaces that might exist in the text. |  |
| isUrl | Checks if the provided value is a URL |  |
| isValidIp | Checks if the provided value is an IP with this [Regex](https://regex101.com/r/qHTUIe/1) |  |

## Type

| Function | Description | Link |
| :--- | :--- | :--- |
| isObject | Checks if `value` is the [language type](http://www.ecma-international.org/ecma-262/7.0/#sec-ecmascript-language-types) of `Object`. *(e.g. arrays, functions, objects, regexes, `new Number(0)`, and `new String('')`)* | [link](https://lodash.com/docs/4.17.15#isObject) |
| isPlainObject | Checks if `value` is a plain object, that is, an object created by the `Object` constructor or one with a `[[Prototype]]` of `null`. | [link](https://lodash.com/docs/4.17.15#isPlainObject) |
| isEmpty | Checks if `value` is an empty object, collection, map, or set. | [link](https://lodash.com/docs/4.17.15#isEmpty) |
| isRegExp | Checks if `value` is classified as a `RegExp` object. | [link](https://lodash.com/docs/4.17.15#isRegExp) |
| isArray | Checks if `value` is classified as an `Array` object. | [link](https://lodash.com/docs/4.17.15#isArray) |
| isFunction | Checks if `value` is classified as a `Function` object. | [link](https://lodash.com/docs/4.17.15#isFunction) |
| isDate | Checks if `value` is classified as a `Date` object. | [link](https://lodash.com/docs/4.17.15#isDate) |
| isString | Checks if `value` is classified as a `String` primitive or object. | [link](https://lodash.com/docs/4.17.15#isString) |
| isBoolean | Checks if value is classified as a `boolean` primitive or object. | [link](https://lodash.com/docs/4.17.15#isBoolean) |
| isEqual | Performs a deep comparison between two values to determine if they are equivalent. | [link](https://lodash.com/docs/4.17.15#isEqual) |
| isNumber | Checks if `value` is classified as a Number primitive or object. | [link](https://lodash.com/docs/4.17.15#isNumber) |
| isUndefined | Checks if `value` is `undefined`. |  |

## Filereader

| Function | Description | Link |
| :--- | :--- | :--- |
| readAsArrayBuffer | Reads a `file` as an `ArrayBuffer` | [link](https://developer.mozilla.org/en-US/docs/Web/API/FileReader/readAsArrayBuffer) |
| readAsDataURL | Reads a `file` as a `Data-URL` | [link](https://developer.mozilla.org/en-US/docs/Web/API/FileReader/readAsDataURL) |
| readAsText | Reads a `file` as `text` | [link](https://developer.mozilla.org/en-US/docs/Web/API/FileReader/readAsText) |
| getNameAndExtensionFromFile | Gets the `name` and `extension` from a file |  |
| getNameAndExtensionFromUrl | Gets the `name` and `extension` from a URL |  |

## Sort

| Function | Description |
| :--- | :--- |
| afterSort | Sorts the elements by their after id property chain |

## Array

| Function | Description | Link |
| :--- | :--- | :--- |
| flattenDeep | Recursively flattens `array`. | [link](https://lodash.com/docs/4.17.15#flattenDeep) |
| remove | Removes all elements from `array` that predicate returns truthy for and returns an array of the removed elements | [link](https://lodash.com/docs/4.17.15#remove) |
| slice | Creates a slice of `array` from `start` up to, but not including, `end`. | [link](https://lodash.com/docs/4.17.15#slice) |
| uniqBy | This method is like [`_.uniq`](https://lodash.com/docs/4.17.15#uniq) except that it accepts `iteratee` which is invoked for each element in `array` to generate the criterion by which uniqueness is computed. | [link](https://lodash.com/docs/4.17.15#uniqBy) |

---

---

