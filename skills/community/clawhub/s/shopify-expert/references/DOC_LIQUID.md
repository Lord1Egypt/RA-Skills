# Shopify docs: Liquid

> Generated from Shopify official LLM documentation snapshot (maintainer export). Prefer live docs at [shopify.dev](https://shopify.dev/) for API versions and current behaviour.

---
## Liquid

### Liquid

Shopify themes are a package of template files, building blocks, and supporting assets. Themes shape the online store experience for merchants and their customers. You can build fast, flexible themes at scale using Liquid, Shopify's theme templating language, along with HTML, CSS, JavaScript, and JSON.

#### Liquid basics

[Liquid](https://shopify.dev/docs/api/liquid) is used to dynamically output **objects** and their properties. You can further modify that output by creating logic with **tags**, or directly altering it with a **filter**. Objects and object properties are output using one of six basic data types. Liquid also includes basic logical and **comparison operators** for use with tags.

#### Objects

Liquid [objects](https://shopify.dev/docs/api/liquid) represent variables that you can use to build your theme. Object types include, but aren't limited to:

- Store resources, such as a collection or product and its properties
- Standard content that is used to power Shopify themes, such as `content_for_header`
- Functional elements that can be used to build interactivity, such as `paginate` and `search`

Objects might represent a single data point, or contain multiple properties. Some products might represent a related object, such as a product in a collection. Some objects can be accessed globally, and some are available only in certain contexts. Refer to the specific object reference to find its access scope.

Objects, along with their properties, are wrapped in curly brace delimiters `{{ }}`.

You can find a [list of all objects](https://shopify.dev/docs/api/liquid/objects) in the Liquid reference docs.

##### Example object

The `product` object contains a property called `title` that can be used to output the title of a product:

Code:

```
{{ product.title }}
```

Data:

```
{
  "product": {
    "title": "Health potion"
  }
}
```

Output:

```
Health potion
```

#### Tags

Liquid [tags](https://shopify.dev/docs/api/liquid/tags) are used to define logic that tells templates what to do. There are four types of tags:

* [**Conditional tags**](https://shopify.dev/docs/api/liquid/tags/conditional-tags): Define conditions that determine whether blocks of Liquid code get executed.
* [**Iteration tags**](https://shopify.dev/docs/api/liquid/tags/iteration-tags): Repeatedly run blocks of code.
* [**Theme tags**](https://shopify.dev/docs/api/liquid/tags/theme-tags): Assign or render content that’s part of your theme.
* [**Variable tags**](https://shopify.dev/docs/api/liquid/tags/variable-tags): Enable you to create new liquid variables.

Tags are wrapped with curly brace percentage delimiters `{% %}`. The text within the delimiters doesn't produce visible output when rendered.

You can find a [list of all tags](https://shopify.dev/docs/api/liquid/tags) in the Liquid reference docs.

##### Tag operators

Liquid supports basic logical and comparison operators for use with conditional tags.

| Operator | Function |
| :---- | :---- |
| \== | equals |
| \!= | does not equal |
| \> | greater than |
| \< | less than |
| \<= | less than or equal to |
| or | Condition A or Condition B |
| and | Condition A and Condition B |
| contains | Checks for strings in strings or arrays |

##### Example tag logic

In the example below, the `if` tag defines the condition to be met. If `product.available` returns `true`, then the number of available units is displayed. Otherwise, the “sold-out” message is shown.

Code:

```
{% if product.available %}
  Available units: 42
{% else %}
  Sorry, this product is sold out.
{% endif %}
```

Data:

```
{
  "product": {
    "available": true
  }
}
```

Output:

```
Available units: 42
```

#### [Filters](https://shopify.dev/docs/api/liquid/filters)

Liquid filters are used to modify the output of variables and objects. To apply filters to an output, add the filter and any filter parameters within the output's curly brace delimiters `{{ }}`, preceded by a pipe character `|`. So the syntax is: `{{ input | filter }}`. Multiple filters can be used on one output. They're parsed from left to right.

You can find a [list of all filters](https://shopify.dev/docs/api/liquid/filters) in the Liquid reference docs.

##### Example filter

In the example below, product is the object, title is its property, and upcase is the filter being applied.

Code:

```
{% # product.title -> Health potion %}

{{ product.title | upcase }}
```

Data:

```
{
  "product": {
    "title": "Health potion"
  }
}
```

Output:

```
HEALTH POTION
```

