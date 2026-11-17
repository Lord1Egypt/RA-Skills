# Video Reference Role Map

Turn user-authorized video references into a practical role table. It states whether each item supports identity, location, visual style, or action, flags conflicts, and lists required missing material. It never downloads source material or invents model parameters.

![Promo image](assets/promo-1600x900.png)

## Input and result

Provide a generation goal and a numbered list of authorized references with descriptions, identifiers, and permitted uses where available. The result is a Markdown table with role assignments and conflict notes, followed by only the material needed next. One request supports up to 100 rows; larger sets are split by scene or chapter.

## Install

```bash
npx skills add xxjrq/video-reference-role-map-cn
```

Include viewable material or concrete visible-content descriptions. Type labels such as portrait, street view, or clip still support provisional roles only; they do not establish hairstyle, clothes, location, colors, or lighting. A static frame does not establish a turn sequence: supply start, process, and end descriptions or an authorized continuous clip.

See the [limited-description input and delivery](fixtures/success.md), [missing-material delivery](fixtures/failure.md), and a [separate described-reference input](fixtures/forward-new-input.json) with its [actual role map](fixtures/forward-new-success.md). These are text-material evaluations; they do not claim unseen images were inspected. Run `python3 scripts/self_test.py` to verify package and published-example regression guards.

## Source and license

The public SeaArt Skills page was consulted only to check the business use case; this repository contains original instructions and examples. Source: [seaartpublic/skills](https://github.com/seaartpublic/skills). Licensed under [MIT-0](LICENSE).
