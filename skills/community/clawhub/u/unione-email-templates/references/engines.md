# Template engines of UniOne

Pick one per message or template with `template_engine` (`simple` is the default) and write the whole body, subject
and other substituted fields in its syntax. Substitutions work in `body.html`, `body.plaintext`, `body.amp`,
`subject`, `from_name`, `headers` and `options.unsubscribe_url`, from `recipients[].substitutions` and
`global_substitutions` (per-recipient values win). Names: Latin letters, digits and `_`, starting with a letter.

## simple (default)

| Construct | Syntax |
|---|---|
| Value | `{{Name}}` |
| Default when empty | `{{Name|Dear customer}}`, or another field: `{{Name|{{Email}}}}` |
| Text when the field is not empty and not zero | `{{HasOrders?You have 10% discount}}`, `{{HasOrders?{{Discount}}}}` |

`Congratulations{{Name?, }} {{Name}}!` adds the comma only when there is a name. Defaults and conditions do not
work inside links (`href`). Values are flat: no objects, arrays or loops — use `liquid` or `velocity` for those.

## liquid

```liquid
<p>Hello, {{ person.name }} {{ person.secondName }}!</p>

{% if user.is_new %}
  Welcome!
{% else %}
  Glad to have you back!
{% endif %}

<ul>
  {% for product in products %}
    <li>{{ forloop.index }}. {{ product.title }} – {{ product.price }}</li>
  {% endfor %}
</ul>
```

Filters: `capitalize`, `upcase`, `downcase`, `replace: "a", "b"`, `default: "customer"`, `date: "%d.%m.%Y"`.
Substitutions: `{"person": {"name": "John"}, "products": [{"title": "Lamp", "price": "30"}]}`.
Stick to the tags and filters above; anything else of Shopify Liquid may not be supported — test it with a send
to a confirmed address first.

## velocity

```velocity
<h2>Hello, $person.name $person.secondName!</h2>

#if( $shoeSize > 5 )
  too big
#elseif( $shoeSize < 5 )
  too small
#else
  just right
#end

#foreach( $pet in $petList )
  $pet.name for only $pet.price
#end
```

| Need | Syntax |
|---|---|
| Nth element | `$petList.get(0).get("name")` |
| Index in a loop | `$catsArray.indexOf($cat)` |
| Lower case | `$name.toString().toLowerCase()` |
| Escape HTML / URL | `$esc.html($text)`, `$esc.url($value)` |
| Format a date | `$dateFormat.format('yyyy-M-d', $date_Birthdate)` — date substitutions must be named `date_…` |

A literal `$` or `#` followed by a word can be taken as Velocity: prefer `liquid` for prices like `$10`, or escape
the text.

## none

No processing: use it when the content has literal `{{`, `$` or `#` that must stay as is.

## Choosing

| Content | Engine |
|---|---|
| A few flat merge tags (name, link) | `simple` |
| Objects, lists of items, conditions | `liquid` (familiar to most developers) or `velocity` |
| Templates migrated from Handlebars / Mustache / Twig / Jinja | `liquid` (closest syntax) |
| No substitutions, or literal braces | `none` |
