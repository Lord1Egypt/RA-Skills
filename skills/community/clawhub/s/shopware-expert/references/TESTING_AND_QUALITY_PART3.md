# TESTING AND QUALITY

Compiled excerpts from the Shopware Developer Documentation snapshot. Prefer live docs at [developer.shopware.com](https://developer.shopware.com/) when in doubt.

---

## Language and Grammar
**Source:** [resources/guidelines/documentation-guidelines/03-language-and-grammar.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/documentation-guidelines/03-language-and-grammar.md)  
# Language and Grammar

Basic guidelines for the apt use of language and grammar in the documentation are discussed in this section. In order to create a consistent product solution, Shopware maintains consistent documentation not just in terms of content but also style. A distinctive editorial voice helps create high-quality, readable, and consistent documentation.

Use American English to cater to a global audience. You may refer to the [Cambridge dictionary](https://dictionary.cambridge.org/dictionary/essential-american-english/) for American vocabulary, spell check, and alternate words.

## Voice and tone

Shopware voices a friendly and conversational tone. We are direct, clear, and more human at conveying information.

### Our voice principles

* **Friendly** — Be less formal and more down-to-earth. Developer documentation is technical, but you can vocalize your writing to sound more human than a robot. Occasionally be funny when it is appropriate.

* **Direct and clear** — Be to the point. Write in such a way that just a skim through provides a clear idea to the reader. Make it simple above all.

* **Customer focussed** — Assume that the reader is knowledgeable but has varying proficiency levels. So, understand their real needs and offer help in the right way.

## Active voice and passive voice

In general, use the active voice (the subject is the person or thing performing the action) instead of the passive voice (the subject is the person or thing being acted upon). For example,

::: tip
**Active Voice** - The user passes the access-key.
:::

::: danger
**Passive Voice** - The access-key is passed by the user.
:::

It is okay to use passive voice in the following cases:

* To emphasize an object over an action — for example, *The file is modified*.

* To de-emphasize a subject — for example, *Over 20 bugs were found in the code*.

* The action doer is not necessarily to be known — for example, *The database was updated in the last week*.

## Second-person over first-person

* In general, use the second-person instead of the first-person, such as *you* instead of *we* or *I*. However, first-person usage is an exception for FAQs.

* If you are guiding the reader to perform something, use an imperative form with an implicit *you*. For example:

::: tip
**Recommended** - Create a PDF file.
:::

::: danger
**Not recommended** - You need to create a PDF file.
:::

* Avoid the usage of *our* in sentences.

## Gender-neutral reference

* Use gender-neutral pronouns, such as *they* rather than *he, she, his, him, her*.

* Use gender-neutral words such as, humankind instead of mankind.

## Abbreviations

Abbreviations include initialisms, acronyms, shortened words, and contractions. They are intended to save the writer's and the reader's time.

### Initialisms and acronyms

* An initialism is formed from the first letters of words in a phrase — for example, *API, SQL, DDL*; whereas an acronym is formed from the initial letters of words in a phrase and pronounced as a word — for example, *ASCII, NASA*. Collectively, let's term it as abbreviation itself.

* When an abbreviation is not familiar to the audience, spell out the term followed by the abbreviation in parentheses, for example, *JSON Web Token (JWT)*. For all subsequent mentions, use the abbreviation only.

* Some abbreviations rarely need to be spelled out — for example, *API, HTTPS, SSA,* File formats such as *PDF, XML, PNG, or HTML*.

* Do not create abbreviations for product or feature names. Always spell out Shopware product and feature names.

* Abbreviations in plural form end with “s” — for example, *APIs, SKEs, and IDEs*. However, if the acronym itself ends in s, sh, ch, or x, then add es — for example, *OSes, and SSHes*.

* Don't define your own abbreviations. Use only the recognized industry-standard.

### Shortened words

* A shortened word is just part of a word or phrase — for example, *etc* for et cetera, *app* for application, *sync* for synchronization.

* Be consistent. Use either the shortened or the full word throughout the document.

### Contractions

* Contractions are unique words that are formed as a combination of two or more words with an apostrophe — for example, *it’s, you’re, you’ll, let’s, or we’re*. Such contractions add a more informal and friendly tone. So limit the usage of it.

* On the other hand, negation contractions (such as *isn't, don't, and can't*) are recommended to use as it is easy for a reader to miss the word *not*, whereas it is harder to misread *don't* as *do*.

## Tense

* In general, use the simple present tense.

* Avoid future or past tense. When you are talking about the future, the reader will be writing or running code in the future. This makes the description look ridiculous. The same holds true for past references.

## Articles

* Indefinite articles, *A* and *An* represent a singular noun.

* While *The* is a definite article used before singular and plural nouns in particular.

* Use an article with the acronym (an ISP, or a URL), nouns (the product database), etc.

## Capitalization

* Capitalize the first letter of the word immediately following a colon.

* Follow capitalization for the names of companies, software, products, services, features, and terms defined by companies and open-source communities.

* When a hyphenated word is the first word in a sentence, capitalize only the first element in the word unless a subsequent element is a proper noun or proper adjective.

## Spellings

* Spellings are based on [Cambridge dictionary](https://dictionary.cambridge.org/dictionary/essential-american-english/).

* It is ideal to use filenames, URLs, and data parameters in words that are not spelled differently by different English dictionaries — for example, color and colour.

## Conjugations

* Don't use */ (slash)* as conjugation. Use *or* instead.

* Don't use *& (ampersands)* as conjunctions. Use *and* instead.

## Punctuations

### Comma

* In a series of three or more items, use a comma before the sentence's final conjugation (and, or) — for example, *Bundles and plugins can provide their own resources like assets, controllers, services, or tests*.

* Place a comma after an introductory word or phrase — for example, *Also, each plugin is represented as a Composer package*.

* Use a semicolon, a period, or a dash before a conjunctive adverb, such as *otherwise, however*. Place a comma after the conjunctive adverb.

* Conjunction (and, but, or, nor, for, so, or yet) separate two independent clauses. Insert a comma after the first clause (before the conjunction) unless both clauses are very short — for example, *The more time you put into indexing data, the faster it is possible to read it*.

### Dashes and hyphens

To indicate a break in the flow of a sentence,  use an em dash (long dash) — for example, *Some programming languages — Pascal, COBOL, Ada are long gone*.

However, use a hyphen (small dash) in the following cases :

* Word prefixes — for example, *self-aware*

* Range of numbers — for example, *25-30 GB*

* Compound nouns — for example, *Mac-specific users*

* To remove ambiguity and clarify the meaning — for example, *logged-in, re-mark*.

* When the prefix ends in a vowel and the word it precedes starts with the same vowel — for example, *co-op, de-energize*.

### Period

* End every sentence with a period.

* Don't end headings with period.

* Don't end a URL with a period. Instead, place the URL in between the description.

* When a sentence ends with quotation marks, place the period inside the quotation marks.

* End every complete sentence with a period in a list. The exception is for phrases. For example,

```markdown
New cart features:

1. Store-level sales tax
2. Shipping modifier
3. Minimum and maximum order quantities
```

### Slashes

* Don't use date formats that rely on slashes.

* Don't use slashes with fractions because they can be ambiguous.

* Don't use slashes to separate alternatives — for example, *blue/red*.

### Parenthesis

Don't add important information in parentheses to describe it in detail.

## Dos and don'ts

* Don't use informal internet slang.

* Avoid usage of buzzwords and jargons.

* Avoid the usage of idioms and phrases.

* Don't start all sentences with the same phrase such as, *In order to, To do, You can*.

* It is good to use polite words such as *may,* and *might* — for example, *That might require you to pass the parameter*.

* Avoid the usage of requesting words such as, please, request — for example, *please use this method, please take a look at the below table*.

* Don't write the way you speak; speaking may be more colloquial and verbose. Instead, add a pinch of formal style with it to convey only enough information to our audience that is sufficient to perform their tasks. This avoids cluttering the page.

Apart from language style, proper fonts and formats must be chosen to promote readers' legibility. The following section covers what fonts and formats need to be used.

---

---

## Fonts and Formats
**Source:** [resources/guidelines/documentation-guidelines/04-fonts-and-formats.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/documentation-guidelines/04-fonts-and-formats.md)  
# Fonts and Formats

This section explains how to format text and code in sentences.

---

---

## Fonts and Format for Text
**Source:** [resources/guidelines/documentation-guidelines/04-fonts-and-formats/01-text.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/documentation-guidelines/04-fonts-and-formats/01-text.md)  
# Fonts and Format for Text

Follow the below textual formats for good content visualization.

::: info
Don't override global styles.
:::

* **Bold**

Use bold to signify UI elements, notices (warning, notice, important declaration), API response - status codes, and titles in descriptions lists.

Use double asterisk in Markdown to signify bold format - for example, `**bold**`.

* **Italic**

Use italics to draw attention to a specific word, phrase, parameter values, classes, methods, product versions, and key terms like SQL Database.

Use a single asterisk in Markdown to signify italic format - for example, `*italic*`.

* **Underline**

Don't underline any content.

## List

Use sentence cases for items in all types of lists as below:

* **Numbered list** - Use when you have a fixed number of entities — for example, three varieties, four categories, two types, etc, or sequential steps as shown below:

```markdown
Follow the below steps to start your project:

1. Create a docker-compose.yml file
2. Start the Docker
3. Prepare Development
4. ...
```

* **Regular bulleted list** - Use this for general enlisting with an asterisk `*` in Markdown to signify bulleted lists.

```text
You can install Shopware on Mac with the help of tools like:

* Docker
```

However, regular bulleted lists within tables use HTML tags.

```text
| Who is the audience? | What are their roles? |
| :--- | :--- |
| Fullstack Developer | <ul><li>Plugin Development</li><li>Templates</li><li>Routes/ Controllers</li></ul>|
```

* **Description list** - Use when you need to describe them along with their titles. In such a case, title tags are bolded, followed by a hyphen or new line and a detailed description. For example,

```text
The Administrations components implement a number of cross-cutting concerns. The most important are:

* **Providing inheritance** - As Shopware 6 offers a flexible extension system to develop your own Apps, Plugins, or Themes.
* **Data management** - The Administration displays entities of the Core component.
* **State management** - Proper state management is key here.
```

The description list can again be a numbered list or a bulleted list based on its sequence or fixed number of entities.

## Date and time

In general, use the following guidelines to format expressions of date and time:

* Use the 12-hour clock, except if required to use a 24-hour time, such as when documenting features that use 24-hour time.

* Capitalize AM and PM, and leave one space between them and the time.

* Avoid using time zones unless absolutely necessary. If using a specific time zone, spell out the region and include the *UTC or GMT* label.

* Spell out the names of the months. For example, `January 19, 2017`.

* You can also use the numerical date format, `MM-DD-YYYY`, and separate the elements by hyphens.

## Numbers

Spell out all ordinal numbers in the text, such as first, fourth, twelfth, and twenty-third for 1st, 4th, 12th, and 23rd, respectively. However, there are exceptions like prices, weight, and quantity which can only be represented as numbers.

## Tables

* Don't embed a table in the middle of a sentence.

* Use table headings for the first column and the first row only.

* Use tables only when you have more than one row and column to represent.

* Don't end sentences with punctuation, including a period, an ellipsis, or a colon.

* Use sentence case for all the elements in a table - contents, headings, labels, and captions.

* Introduce a table using a complete sentence and try to refer to the table's position, using a phrase such as *the following table or the preceding table*.

## Hyperlinks

* Provide meaningful URL text links. Don't use *click here or read this document* phrases.

* Write a complete sentence that refers the reader to another topic. Introduce the link with a phrase such as *For more information, see or For more information about..., see*.

* Keep the link text as short as possible. Do not write lengthy link text such as a sentence or short paragraph.

* Place important words at the beginning of the link text.

* Don't use the exact link text in the same document for different target pages.

* If the hyperlink text includes an abbreviation in parentheses, include the long form and the abbreviation in the link text.

## Heading

* Use `#` to set the levels of heading.

* Don't skip levels of the heading hierarchy. For example, an `<H3>` heading must fall under `<H2>`.

* Follow camel case for all the `<H1>` headings — for example, *Flow Sequence Evaluation* and sentence case for the rest of the sub-headings that follow - for example, *Flow sequence evaluation*.

Refer to [Vitepress syntax](https://vitepress.dev/guide/markdown) for more.

This section covers fonts and formats for text, while the following section covers fonts and formats for code.

---

---

## Fonts and Format for Code
**Source:** [resources/guidelines/documentation-guidelines/04-fonts-and-formats/02-code.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/documentation-guidelines/04-fonts-and-formats/02-code.md)  
# Fonts and Format for Code

Fonts and formats for inline code, code blocks, non-code items, API reference, classes and methods are detailed below:

## Inline code

* Inline code is a short snippet of code. Use ``backticks (`)`` for single-line code/ inline code.

* The following are examples of inline code:

  * Attribute names and values

  * Command Line (CLI) utility names

  * Class, methods, and function names

  * Enum names

  * Command output

  * Data types

  * Environment variable names

  * File names and paths

  * Folders and directories

  * HTTP methods and status codes

  * HTTP status codes

  * Alias names

  * Parameter values

Below are a few more instances:

### HTTP status codes

* In general, put the number and the name of the status code in code font:

  HTTP `400 Bad Request` status code

* To refer to a range of codes, use the following form:

  `HTTP 2xx` or `200` status code

* If you prefer to specify an exact range, use the following form:

  HTTP status code in the `400-499` range

### Command prompt

* If your CLI instructions show single-line or multi-line input, start each line of input with the `$` prompt symbol.

* Don't show the current directory path before the prompt, even if part of the instruction includes changing directories.

### Placeholders

* In a code output, explain any placeholder that appears in the sample output the first time.

* Mention the placeholders in complete capital and italicized code font.

* In markdown, wrap inline placeholders in ``backticks (`)`` and `asterisk (*)`.

```markdown
(*`PLACEHOLDER_NAME`*)
```

* Don't use *X* as a placeholder; instead, use an informative placeholder name.

## Code blocks

* Code blocks are used for code snippets longer than a single line or terminal commands containing sample output when executed.

* In markdown, code blocks are represented using a `code fence (```)`.

* Mention language identifier to enable syntax highlighting in your fenced code block.

````markdown

 ```markdown
 Language identifier is markdown here.  
 ```

````

* When using code blocks within lists, use correct indention to avoid breaking the list. For example,

::: tip

* Payment

  ```jsx
  const pay_type = <Payment type=COD />;
  ```

* Transaction

:::

::: danger

* Payment

```jsx
const pay_type = <Payment type=COD />;
```

* Transaction

:::

* Don't use tabs to indent text within a code block; use two spaces.

* Use three dots (...) on a separate line to indicate that more lines of output are omitted from the sample output.

## Blockquote

* Blockquotes are represented by `>`

```text
> Added A Name preset according to new naming scheme.
```

* To add blockquotes within a blockquote, use `>>`

## Items to put in ordinary (non-code) font

The following list includes items that should not be in code font:

* Email addresses

* Domain names

* URLs

* Names of products, services, and organizations

## API reference

* The API reference code must describe every class, interface, struct, constant, field, enum, and method, with a description for each parameter and the status codes.

* Capitalize the API method names such as `GET`, `PUT`, `PATCH,` etc.

* Provide meaningful information about the request parameters. Link them to other sections of the documentation for more explanations.

* Include any valid and default value at the end of the parameter description. For example, *Valid values are `true` and `false`. The default is `false`.*

* In detailed documentation, elaborate on how to use the API, including invoking or instantiating it, the key features, and best practices or pitfalls.

## Classes and methods

* Describe the class briefly and state the intended function with information that can't be deduced from the class name and signature.

* Describe the method briefly and what action the method performs. In subsequent sentences, state any pre-requisites that must be met before calling it, explain why and how to use the method, give details about exceptions that may occur, and specify any related APIs.

* Method names should be followed by a pair of parentheses `()`.

* You may also cross-link parameters, classes, and methods.

## Deprecations

When something is deprecated, tell the user what to use as a replacement or what to do to make their code work. For example,

::: warning

**Deprecated** - Access it using this getProd() method instead.

:::

The following section deals with asset (files, images, and videos) management.

---

---

## Methodize Assets
**Source:** [resources/guidelines/documentation-guidelines/05-methodize-assets.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/documentation-guidelines/05-methodize-assets.md)  
# Methodize Assets

Maintaining a well-organized repository for all documentation assets, including images, videos, and files, is crucial. This section provides an overview of how assets are represented, managed, and the naming conventions that are adhered to.

::: info
For the creation of a visual representation, either contact the Shopware design team directly or submit a request through the [Issues](https://github.com/shopware/docs/issues) section.
:::

## Visual diagram guidelines

Our documentation categorizes visuals into different types, including screenshots, diagrams (such as UML and flowcharts), and GIFs. Each of these visual elements shares common quality standards. This section outlines the specific requirements that must be met by all visuals used in technical documentation.

### Diagram specifications

| Image attributes | Specification | Notes|
|------------------|---------------|---------|
| File type| Only .png, .svg and .gif| Use a lossless image format for screenshots (i.e., PNG) and vector format (i.e., SVG) for drawings (diagram, chart, logos, ...).|
|File size | max. 5 MB | It is best to upload high-quality images. |
|File name | Only use letters and hyphens `<topicName>-<subtopicName>-<meaningfulImageName>.md.` | Use the naming convention documented below in naming conventions for images.|
|Image size | Width: max 768px, Height: max 576px | This is automatically taken care by the inbuilt functions in our docs.|
|Aspect ratio | 4:3 | This is automatically taken care by the inbuilt functions in our docs. |
|Copyright| - |Determine if an image or diagram is protected by copyright. If it is, you must obtain permission and acknowledge credit.|
|Personal identifiable information (PII) | - | Make sure to mask, modify, or remove any PII such as passwords, logins, account details, or other information that could compromise security.|
|Alt tags| `![Alt](/path/to/img.jpg “image title”)` | Make sure to include alt text for every image. The text is used in situations where the image isn’t visible and image SEOs.|
|Borders|-|No borders are added to the images|

### Considerations for Visual Diagrams

* If you add images to illustrate items in a list (typically, steps in a procedure), align these images accordingly:
  * If there is only one image that illustrates the entire procedure, place the image at the end of the procedure or align it with the lead-in paragraph.
  * If you need to provide an image for each step in the procedure, place each image at the end of each step it follows.

* Use the below naming convention for the images:

  * *`<topicName>-<meaningfulImageName>.svg`*. For example,

```markdown
storefront-pages.svg
```

* If sub-topic exists, *`<topicName>-<subtopicName>-<meaningfulImageName>.svg`*. For example,

```markdown
storefront-dataHandling-pages.svg 
```

* The image names can be serialized if multiple images are under the same topic. For example,

```markdown
storefront-dataHandling-pages_01.svg
```

* An introductory sentence should precede most images.

* Store all the media in the [assets directory](https://github.com/shopware/docs/tree/main/assets). Once it is loaded, copy the reference to the Markdown file. Test images in a local build.

## Diagrams

### Considerations for Diagrams

Consider creating diagrams to :

* Show architecture
* Show complex relationships
* Define a complex workflow

### Diagram creation tools

* [Mermaid](https://mermaid.live/) - Use Mermaid for generating Flowcharts, Sequence Diagrams, State Machine Diagrams, Class Diagrams, etc. Embed the diagram code within a codeblock named `mermaid`.

* [Meteor Diagram Kit](https://www.figma.com/community/file/1339141765099471739) - Apart from UML diagrams, utilize *Meteor Diagram Kit* to create other diagrams. This follows Shopware design and quality standards.

## Screenshots

### Considerations for Diagrams

Consider creating screenshots to :

* Provide an example of a visualization
* Show panels populated with query and settings
* Show configurations and settings
* Emphasize a new feature
* Limit the contents of an image to the relevant portion. Do not include distracting or unnecessary content and whitespace.

### Aspects for Capturing Screenshots

* If the screenshot shows a desktop application interface, you must use the latest OS version supported by the solution to take the screenshot.
* The screenshot must be in focus and show an active window, wizard or dialog box.
* Avoid both horizontal and vertical scroll bars whenever possible.
* The screenshot must show real-world data or at least data that is close to realistic use cases.
* All screenshots you take must be consistent with each other.
* Screenshots can be taken using GIMP, Snipping tools, or any tool you have already worked on.
* Do not use screenshots for Code samples (show code samples in codeblocks).
* Do not take screenshots for a page that is likely to change frequently.

## GIFs

### Considerations for GIFs

Consider using GIFs when you want to:

* Demonstrate flow of procedures.
* Highlight functionalities visually.
* Aid setup and initial tasks with visual guides.

## File

Every file added to a folder can have a naming convention as:

*`<two_digit_number>-<meaningful_image_name>.md`.* For example,

```markdown
01-doc-process.md
```

## Video

* Provide captions and transcripts for video content.

* A similar naming pattern to that of images is also followed for videos.

All the previous sections detail how to articulate and format the document. The next section describes the entire process of writing, reviewing, and publishing the documentation.

---

---

## Documentation Process
**Source:** [resources/guidelines/documentation-guidelines/06-doc-process.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/documentation-guidelines/06-doc-process.md)  
# Documentation Process

You have gone a long way in understanding audience types, language rules, grammar treatment on textual content, and Shopware documentation structure to managing assets.

Now, are you thinking of how to kick-start?

Refer to our [GitHub repository](https://github.com/shopware/docs) for the complete process, from cloning the repository to publishing the content.

Well-defined writing leads to a more consistent, efficient learning experience for readers. We want to establish a common process for writing, reviewing, iterating, and maintaining documentation.

This section guides you on how to ink down your knowledge and publish the article.

## Ideate

When you prefer to contribute to an existing article or create a new one, consider yourself the "knowledge lead" for that particular topic while documenting.

Do some research and prepare a rough outline addressing the following points and prompt other maintainers for feedback:

* Who is the audience?
* What article are you going to write?
* What are the prerequisites for readers?
* Which questions are you going to answer?
* Which other topics might be relevant/interesting?

## Write

After you have discussed the abstract and set the objectives, start writing.

It is good to follow a "30/90" rule. This rule suggests creating the first draft when 30% done and taking the first feedback at a high level. When 90% done, schedule a steady review for in-depth validation.

In your first draft:

* Prepare the document structure (flow of topics).
* Jot down the topics of the documentation to be included and describe them.
* Mention all the points briefly that would be part of this article.
* Have a common thread throughout your article.
* Add placeholders for images or code blocks to be added later.
* Work with cross-references (knowledge is a network, not a one-way street ).
* Try to use non-Shopware-specific language when possible or provide a link to its description (e.g., "DAL").

### Guidelines to writing concepts

* **Introduction** - Introduce the concept (for example, cart) by its purpose in such a way that it answers the following general questions:
  * *What is a cart?*
  * *What can it contain?*
  * *How does it relate to users and orders?*
  * *What can the readers expect in the further connected articles?*

Use cross-references to help users fully understand the text — for example, provide a link to *configurable products* or *checkout* articles. Don't use terms like *"custom products"* as these are Shopware-specific, and newcomers may find it difficult to understand.

* **Comprehensive explanation** - Explain the concept in detail with examples, illustrations, tables, graphs, or pseudo-code.

  Don't use any Shopware-specific source code. Using source code within a conceptual article has the following drawbacks:

  * It introduces another dependency that has to be maintained.
  * It builds on the presumption that readers know the given language and context.
  * People tend to copy & paste without context.

* **Conclusions** - If possible add a connective statement to the next article that follows.

## Review

After writing the first 30%, consult a reviewer to give some initial feedback. Discuss the current progress and re-arrange some parts if needed.

If you are the reviewer, check the text's general approach, tone, and wording as per the standard guidelines. Provide the curator with some early direction and feedback. Having multiple reviewers can be beneficial.

This process can be repetitive until the final version is ready.

## Publish

Before the final version is published, cross-check if the article fulfills all the questions and objectives outlined at the beginning. This must be reviewed, and feedback must be incorporated.

After reviewing the final draft, it will be published on notifying the administrators.

## Maintain Versions

All contents are based on Shopware Major versions, such as 6.3, 6.4, 6.5, etc. The current version is reflected by our GitHub repositories' `master` branch, whereas each older version has its respective separate branch.

If a documented feature or functionality is introduced within major versions (and also in cases where you think it is applicable), please include a hint showing the version constraints as below:

::: info
This functionality is available starting with Shopware 6.4.3.0.
:::

**Your contribution is our pride!**

---

---

## Embedding external repositories
**Source:** [resources/guidelines/documentation-guidelines/07-embedding-external-repositories.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/documentation-guidelines/07-embedding-external-repositories.md)  
# Embedding external repositories

This guide will explain how to embed project documentation from your repository into the [Developer documentation](https://developer.shopware.com/).

[Developer Portal](https://github.com/shopware/developer-portal) is built using the [`shopware/developer-documentation-vitepress`](https://github.com/shopware/developer-documentation-vitepress) repository (`vitepress-shopware-docs` package). This setup heavily utilizes [Vitepress](https://vitepress.dev/) and incorporates custom Shopware features such as unique design, breadcrumbs, Algolia search, Copilot AI chat and recommendations, auto-built sidebar and more.

This portal serves as a central hub for all developer resources and documentation. However, the actual content is distributed across various repositories but integrated into the developer portal using the [Docs CLI](https://github.com/shopware/developer-documentation-vitepress/blob/main/CLI.md). This approach allows for decentralized content management, enabling the maintainers of each repository to manage their content independently.

## Configure Developer Portal

To set up your local instance of the developer portal, clone Developer Portal repository and install the dependencies:

```bash
cd /www/shopware/
git clone https://github.com/shopware/developer-portal.git
cd developer-portal
pnpm i
```

We also want to create a new branch so we can test the integration first in the pull request, then merge it to the `main` branch and do production deployment.

```bash
git checkout -b feature/embed-meteor-icon-kit
```

### Docs CLI

Now access `./docs-cli` in the root of the `shopware/developer-portal` repository.

To start embedding a new repository, update `.vitepress/portal.json` and create a new entry in the `repositories` array. Then run the CLI and see if your repository is visible in the list - select it and continue by confirming the default settings.

```bash
./docs-cli manage
```

You should be able to preview your new content by running the Vitepress dev server and opening your defined URL in the browser using the below command.

```bash
pnpm dev
```

### Sidebar and main navigation

The content is already there and published, but in most cases you will also want to have a sidebar dedicated for your section.

Open `.vitepress/navigation.ts` and update `sublinks` and `ignore` parameters to auto-build the sidebar based on your directory structure and frontmatter config.

If you also want to add it to the top-bar main menu, update the `navigation` accordingly.

### Algolia search

By default, contents are grouped under `General` section in the Algolia search using Algolia *facets*. You can configure that and group your articles together into a new section, or even create multiple new sections.

Update `sections: SwagSectionsConfig[]` with all the regex matches for your sections and define the title of new section displayed in the Algolia search modal.

```javascript
const sections: SwagSectionsConfig[] = [
    // ...
    {
        title: 'Meteor Icon Kit',
        matches: [
            '/resources/meteor-icon-kit/',
        ],
    },
];
```

### Edit links

Every article has a `Edit this page on GitHub` link in the bottom left corner. Because we are embedding content from external repositories, we need to make sure that the link points to the correct repository and branch.

You can do that by updating `const embeds: SwagEmbedsConfig[]`.

```javascript
const embeds: SwagEmbedsConfig[] = [
    // ...
    {
        repository: 'meteor',
        points: {
            '/resources/meteor-icon-kit/': 'main',
        },
        folder: 'packages/icon-kit/docs',
    },
]
```

### Optional

#### Copilot AI

Update `themeConfig.swag.similarArticles.filter` with your settings for recommended articles in Copilot AI. This is only needed for repositories that are embedding multiple branches (versions) so that Copilot only uses articles from one version at the time.

#### Version switcher

Update `themeConfig.swag.versionSwitcher` with additional settings for your paths when you are embedding multiple branches (versions) from the same repository. This allows users to switch between different versions of the same article.

#### Color coding

Update `themeConfig.swag.colorCoding` with your settings for color coding in the breadcrumbs. This is currently only used for Plugins and Apps in the `docs` repository.

#### Static assets

When you also want to share static assets from your repository such as `.pdf` or `.zip` files (excluding statically linked images in articles), make sure to copy them in the `buildEnd` hook.

```javascript
export default {
    // ...
    async buildEnd() {
        // ...
        await copyAdditionalAssets([
            // meteor-icon-kit
            {
                src: './resources/meteor-icon-kit/public/icons/regular',
                dst: 'icons/regular',
            }
        ])
    }
}
```

### Production deployment

While we already added the repository to the Docs CLI, it is not included in the production build by default.

The new repository must be activated in `.github/scripts/mount.sh`. This script is needed to apply correct build config in production build and during PR workflows where custom `branch` or even `org` is used and switched to by overwriting environment variables.

```sh
# ...
BRANCH_METEOR_ICON_KIT=main
ORG_METEOR_ICON_KIT=shopware

# ...
./docs-cli.cjs clone \
 --ci \
 --repository shopware/meteor \
 --branch ${BRANCH_METEOR_ICON_KIT:-main} \
 --src packages/icon-kit/docs \
 --dst resources/meteor-icon-kit \
 --org ${ORG_METEOR_ICON_KIT:-shopware} \
 --root ../..
```

## Configure your repository

The Last step includes configuring your repository for better developer experience and integration with the Developer Portal. Let's switch to your repository.

```bash
cd ../docs
# or
cd /www/shopware/docs
```

### Shortcuts

You will want to create at least 3 scripts in `package.json` of your repository

* `docs:env` - Run this in the context of your repository and the script will either clone the `developer-portal` inside `../developer-portal` or pull changes from the remote, and install latest dependencies.
* `docs:link` - Mount documentation from your repository into your local `developer-portal` instance.
* `docs:preview` - Run Vitepress dev server from your local `developer-portal` instance.

Examples are available in [meteor](https://github.com/shopware/meteor/blob/main/package.json) (monorepo setup), [frontends](https://github.com/shopware/frontends/blob/main/package.json), [release](https://github.com/shopware/release-notes/blob/main/package.json) and [docs](https://github.com/shopware/docs/blob/main/package.json) repositories (all standard repos).

```json
{
  "scripts": {
    "docs:env": "[ -d \"../developer-portal\" ] && ../developer-portal/docs-cli.cjs pull || (git clone git@github.com:shopware/developer-portal.git ../developer-portal && pnpm i -C ../developer-portal)",
    "docs:link": "../developer-portal/docs-cli.cjs link --src . --dst docs --symlink",
    "docs:preview": "../developer-portal/docs-cli.cjs preview"
  }
}
```

### CI pipelines

Custom GitHub workflows are not needed anymore, but new repos need to be added to the `Shopware Dev Docs connector` app in `shopware` organization on GitHub, so the app can listen for GitHub events. Shopware Dev Docs connector GitHub app takes care of:

* Creating a commit status check in PRs.
* Triggering full integration check in `developer-portal`.
* Updating the status check based on the integration check outcome, with a dedicated preview URL.
* Triggering production deployment when `main` branch is updated.

## Commit changes and create a PR

Once you have everything set up, commit your changes and create PRs for the `shopware/developer-portal` and your repository.

Usually, you will want to first preview the docs from the feature branch of your repository inside the Developer portal. You can do that by changing the environment variable of the default branch for your repository in the `.github/scripts/mount.sh` inside the `developer-portal`, review changes, and then switch back to `main` branch before merging.

For example, follow the instructions in the article above, and use the feature branch of your repository in production build.

```bash
BRANCH_METEOR_ICON_KIT=feature/embed-meteor-repo-to-developer-portal
```

```shell
cd /www/shopware/developer-portal/
git checkout -b feature/embeds-meteor-icon-kit
# apply changes
git commit -m "feat: embedded meteor repo"
```

Make changes in your feature branch of your repository.

```shell
cd /www/shopware/meteor/
git checkout -b feature/embed-meteor-repo-to-developer-portal
# apply changes
git commit -m "chore: updated shortcuts, set up pipeline for developer portal"
```

Then create a PR and once the Vercel preview inside `developer-portal` is ready and correct, merge feature branch in your repository.

```shell
cd /www/shopware/meteor/
git checkout main
git merge feature/embed-meteor-repo-to-developer-portal
```

Now switch back production branch for your repository to `main` in the `developer-portal`.

```shell
cd /www/shopware/developer-portal/
git checkout feature/embeds-meteor-icon-kit
# change BRANCH_METEOR_ICON_KIT=main inside .github/scripts/mount.sh
git commit -m "chore: switched back to main branch for meteor repo"
```

Once the PR is merged, the production build will be triggered and the changes will be live on the Developer Portal.

---

---

## Testing
**Source:** [resources/guidelines/testing.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/testing.md)  
# Testing

Testing ensures software reliability, quality, and optimum performance. Detailed E2E testing and quality guidelines are described in the following sections.

---

---

## Differentiator cluster for Shopware plugins or apps
**Source:** [resources/guidelines/testing/Differentiator-Clusters.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/testing/Differentiator-Clusters.md)  
# Differentiator cluster for Shopware plugins or apps

This section will show you the new differentiator groups which needs to be fulfilled to be to released to the store .

## Cluster variations

* Cluster 1: Your plugin or app offers meaningful use case that cannot be replicated with other comparable plugins or apps. Additionally, it provides a meaningful integration that is not implemented in the comparison plugin or app.

* Cluster 2: Your plugin or app offers meaningful use case that cannot be replicated with other comparable plugins or apps. Moreover, it works sensibly with Shopware standards, instead of using its own technical approaches.

* Cluster 3: Your app is based on the app system and offers a meaningful integration that is not implemented in the comparison plugins.

* Cluster 4: Your app is based on the app system and offers meaningful use case that cannot be replicated with other comparable plugins.

## Examples of meaningful use of the Shopware standard

* Uses custom fields instead of own tables. This facilitates data management and querying and avoids inconsistencies or conflicts with the Shopware data model.

* Uses Admin SDK instead of own modules. This allows for seamless integration of the plugins or apps into the Shopware admin interface.

* Offers a headless solution. This enables Shopware to be used as a backend for any frontend applications that can communicate with Shopware via the API.

* Offers a reasonable API connection. This means that the plugin or app uses the Shopware API in a compliant and efficient manner to exchange, update, or manipulate data.

* Precisely adapts to Shopware externally. This means that the plugin or app complements or extends the appearance of the Shopware admin interface without disturbing or altering it, by using the same styles and elements.

## Examples of meaningful use cases that cannot be represented with other plugins or apps

* Offers the possibility to send automatic emails to customers or partners to inform them about important information or offers.

* Offers the possibility to combine the function of the plugin or app with variants.

* Offers the possibility to link the function of your plugin or app with advanced pricing to enable flexible pricing or discounts.

* Offers different configurations for different sales channels.

## Examples of Shopware integrations

* The plugin or app has meaningfully integrated the Rule Builder into the plugin or app.

* The plugin or app has meaningfully integrated the Dynamic Product Stream into the plugin or app.

* The plugin or app has meaningfully integrated the Shopware webhook integration into the plugin or app.

* The plugin or app has meaningfully integrated the Flow Builder into the plugin or app.

---

---

## Best practices for writing end-to-end tests
**Source:** [resources/guidelines/testing/e2e-best-practises.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/testing/e2e-best-practises.md)  
# Best practices for writing end-to-end tests

## Overview

A typical E2E test can be complex, with many steps that take a lot of time to complete manually. Because of this complexity, E2E tests can be difficult to automate and slow to execute. The following tips can help reduce the cost and pain of E2E testing and still reap the benefits.

Cypress got you covered with their best practices as well: So please also look at their best practices to get to know their patterns:

::: warning
We strongly recommend following Cypress own best practices as well.
:::

## Amount and prioritization of end-to-end tests

### Video

When it comes to dividing test types, selecting and prioritizing test cases, and thus designing tests, things get a bit more complicated. We have generally aligned our test strategy with the test pyramid, although not 100%. The pyramid states that end-to-end tests should be written in a few but well chosen test cases because end-to-end tests are slow and expensive.

At [Shopware Community Day](https://scd.shopware.com/en-US/) 2020, we gave a talk on how we approach automated testing in Shopware, how far we have come on this journey, and what we have gained so far:

To sum it up briefly, the end-to-end tests are slow and thus expensive to maintain. That is why we need a way to prioritize our test cases.

### When should I write an end-to-end test

::: danger
Cover every possible workflow with E2E tests.
:::

::: tip
Use proper prioritization to choose test cases covered by E2E tests.
:::

Due to running times, it is not advisable to cover every single workflow available. The following criteria may help you with that:

* **Cover the most general, most used workflows of a feature**, e.g., CRUD operations. The term "[happy path](https://en.wikipedia.org/wiki/Happy_path)" describes those workflows quite well.
* **Beware the critical path**: Cover those workflows with E2E tests, which are the most vulnerable and would cause the most damage if broken.
* **Avoid duplicate coverage**: E2E tests should only cover what they can, usually big-picture user stories (workflows) that contain many components and views.
  * Sometimes, unit tests are better suited. For example, use an E2E test to test your application's reaction to a failed validation, not the validation itself.

## Workflow-based end-to-end tests

::: danger
Write the E2E test as you would write unit tests.
:::

::: tip
Writing E2E tests in a "workflow-based" manner means writing the test describing a real user's workflow just like a real user would use your application.
:::

A test should be written "workflow-based" - We like to use this word very much because it is simply apt for this purpose. You should always keep your persona and goal of an E2E test in mind. The test is then written from the user's point of view, not from the developer's point of view.

## Structure and scope

### Test scope

::: danger
Write long E2E tests covering lots of workflows and use cases.
:::

::: tip
Keep tests as simple as possible. Only test the workflow you explicitly want to test. Ideally, use **one test for one workflow**.
:::

The second most important thing is to test the workflow you explicitly want to test. Any other steps or workflows to get your test running should be done using API operations in the `beforeEach` hook, as we don't want to test them more than once. For example, if you want to test the checkout process, you shouldn't do all the steps, like creating the sales channel, products, and categories, although you need them to process the checkout. Use the API to create these things and let the test just do the checkout.

You need to focus on the workflow to be tested to ensure minimum test runtimes and to get a valid result of your test case if it fails. For this workflow, you have to think like the end-user would do - Focus on the usage of your feature, not technical implementation.

Other examples of steps or workflow to cut off the actual tests are:

* The routines which should only provide the data we need: Just use test fixtures to create this data to have everything available before the test starts.
* Logging in to the Administration: You need it in almost every Administration test, but writing it in all tests is pure redundancy and way more error sensitive.

::: info
This [scope practice](https://docs.cypress.io/guides/references/best-practices.html#Organizing-Tests-Logging-In-Controlling-State) is also mentioned in Cypress best practices as well.
:::

### Focus on stability first

::: danger
Design your tests dependent on each other, doing lots of write operations without removing corresponding data.
:::

::: tip
Keep tests isolated, enable them to run independently, and restore a clean installation between tests
:::

It is important to focus on stability as the most important asset of a test suite. A flaky test like this can block the continuous deployment pipeline, making feature delivery slower than it needs to be. Moreover, imagine the following case: Tests that fail to deliver deterministic results: Those flaky test is problematic because they won't show valid results anymore, making them useless. After all, you wouldn't trust one any more than you would trust a liar. If you want to find out more on that topic, including solutions, please take a look at this article:

This was one of the reasons you need stable tests to create value. To achieve that, you have several possibilities. We will introduce you to some of them in the following paragraphs.

Let's start with some easy strategy. Keep tests as simple as possible, and avoid a lot of logic in each one. Think about it this way, the more you do in a test, the more you can go wrong. In addition, by avoiding big tests, you avoid causing load on your application and resource leaks in your environment.

When planning your test cases and structure, always keep your tests isolated from other tests so that they are able to be run in an independent or random order. Don't ever rely on previous tests. You need to test specs in isolation to take control of your application’s state. Every test is supposed to be able to run on its own and independent from any other tests. This is crucial to ensure valid test results. You can realize these using test fixtures to create all data you need beforehand and take care of the cleanup of your application using an appropriate reset method.

## Choosing selectors

::: danger
Choose fuzzy selectors which are prone to change, e.g. xpath.
:::

::: tip
Use selectors which won't change often.
:::

XPath selectors are quite fuzzy and rely a lot on the texts, which can change quickly. Please avoid using them as much as possible. If you work in Shopware platform and notice that one selector is missing or not unique enough, just add another one in the form of an additional class.

### Avoid framework specific selectors

::: danger
Choose framework specific syntax as a selector prone to change, e.g. `.btn-primary`.
:::

::: tip
Use individual selectors which won't often change, e.g., `.btn-buy`.
:::

Using selectors which rely on a framework specific syntax can be unstable because the framework selectors are prone to change. Instead, you should use individual selectors, which are less likely to change.

```html
<button class="btn btn-primary btn-buy">Add to cart</button>
```

```javascript
// ✗ Avoid using framework specific syntax from Bootstrap as a selector.
cy.get('.btn.btn-primary').click();

// ✓ Instead, you should use a shopware specific class like `.btn-buy`.
// (This also remains stable when the button variant is changed to, e.g., `.btn-secondary`.)
cy.get('.btn-buy').click();
```

```html
<button
    data-toggle="modal"
    data-target="#exampleModal"
    class="btn btn-primary btn-open-settings">
    Open settings modal
</button>
```

```javascript
// ✗ Avoid using framework specific syntax from Bootstrap as a selector.
cy.get('[data-toggle="modal"]').click();

// ✓ Instead, you should use a shopware specific class like `.btn-open-settings`.
cy.get('.btn-open-settings').click();
```

```html
<div class="custom-control custom-checkbox">
  <label 
      for="tos" 
      class="checkout-confirm-tos-label custom-control-label">
      I have read and accepted the general terms and conditions.
  </label>
</div>
```

```javascript
// ✗ Avoid using framework specific syntax from Bootstrap as a selector.
cy.get('.custom-checkbox label').click();

// ✓ Instead, you should use a shopware specific class like `.checkout-confirm-tos-label`.
cy.get('.checkout-confirm-tos-label').click();
```

If there are no suitable selectors available, please add descriptive classes or IDs for your desired elements.

## Waiting in E2E tests

::: danger
Waiting for arbitrary time periods, e.g., using `cy.wait(500)`
:::

::: tip
Use route aliases or assertions to guard Cypress from proceeding until an explicit condition is met.
:::

Never use fixed waiting times in the form of `.wait(500)` or similar. Using Cypress, you never need to do this. Cypress has a built-in retry-ability in almost every command, so you don't need to wait, e.g., if an element already exists. If you need more than that, we got you covered. Wait for changes in the UI instead, notifications, API requests, etc., via the appropriate assertions. For example, if you need to wait for an element to be visible:

```javascript
cy.get('.sw-category-tree').should('be.visible');
```

Another useful way for waiting in the Administration is using Cypress possibility to work with [network requests](https://docs.cypress.io/guides/guides/network-requests.html). Here you can let the test wait for a successful API response:

```javascript
cy.server();

// Route POST requests with matching URL and assign an alias to it
cy.route({
    url: '/api/search/category',
    method: 'post'
}).as('getData');

// Later, you can use the alias to wait for the API response
cy.wait('@getData').then((xhr) => {
    expect(xhr).to.have.property('status', 200);
});
```

::: info
This [best practice](https://docs.cypress.io/guides/references/best-practices#Unnecessary-Waiting) is also mentioned in Cypress best practices as well. Actually, it can be considered a general best practice to avoid flakiness.
:::

## Cypress commands and their queue

::: danger
Using vanilla JavaScript logic alongside cypress commands without further caution
:::

::: tip
If you need vanilla Javascript in your test, wrap it in a Cypress `then` or build a custom command to get it queued.
:::

Cypress commands are asynchronous and get queued for execution at a later time. During execution, subjects are yielded from one command to the next, and a lot of helpful Cypress code runs between each command to ensure everything is in order.

This won't happen with Vanilla JS, though. It will be executed immediately. In the worst case, this difference can cause timing issues. So always wrap your vanilla JavaScript code into Cypress commands or `then` in order to make use of Cypress command queue.

::: warning
Concerning Cypress `then`: Even though Cypress commands look like promises, they aren't completely the same. Head over to the [Cypress docs](https://docs.cypress.io/guides/core-concepts/introduction-to-cypress#Commands-Are-Not-Promises) for more information.
:::

---

---

## Testing Guidelines for Shopware Extensions
**Source:** [resources/guidelines/testing/store.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/testing/store.md)  
# Testing Guidelines for Shopware Extensions

This section guides you with the criteria used to test your extension. Detailed information is available on [quality guidelines for apps](../store/quality-guidelines-apps/),[quality guidelines for plugins](../store/quality-guidelines-plugins/) and [differentiator cluster](../Differentiator-Clusters.html).

Check out the points that affect your extension and go through them before submitting it for testing.

We assign three statuses when testing your extension:

::: tip
OK: This point was tested and passed
:::

::: danger
Failed: This point was tested, and errors were found
:::

::: warning
Not necessary: This point does not need to be tested
:::

## Test criteria

Here is what the test criteria include:

* **[Function availability](../store/quality-guidelines-apps/#every-app-based-on-the-app-system)** - Here, we proceed like a user and check the complete functionality of the app, as well as the logical structure and usability. For instance,

  * Is a general function as described in your extension available?
  * Do the buttons, export, rules, etc., work?
  * Are errors displayed in the console?

* **[Lighthouse audit home/listing/detail](../store/quality-guidelines-apps/#frontend-apps)** - We check:

  * If your extension affects the Storefront or not?  (so that the search engines have no problems with it).
  * If all buttons, labels, etc., are named correctly?

We pay attention to all five audits. The app must not limit these. Like most search engines, we also pay attention to mobile-first.

* **[Rich snippet home/listing/detail](../store/quality-guidelines-apps/#template-tests)** - We check:

  * If the page can be indexed?
  * Is there any incorrect price information being displayed?

Rich snippets have no influence on the ranking of a website. Thus, they do not count among the ranking factors. Nevertheless, search hits enriched with additional information have various SEO advantages: higher attention, higher click-through rate, and greater relevance.

* **[No errors in the Storefront and 503/404 errors](../store/quality-guidelines-apps/#error-messages-must-be-entered-in-the-event-log)** - We check:

  * If the app is active in the Storefront?
  * If it involves display errors and errors of any kind?

The end customer should not receive any misleading error messages. It does not matter whether a function causes the error or the customer does not use the function correctly. For example, the customer can upload a picture using a function, but if the customer tries to upload a video, a clear message should be displayed here.

* **[Cookie check storefront/checkout](../store/quality-guidelines-apps/#register-a-cookie-to-the-cookie-consent-manager)** - Since the GDPR/DSGVO, the classification of cookies is particularly important. We distinguish between three types of cookies.

  * **Technically required**: Only cookies that are really important for the store without which no purchase would be possible.

  * **Comfort functions**: Cookies to display personalized ads as banners, newsletter pop-ups, and content from video and social media platforms.

  * **Statistics and Tracking**: Statistics and everything that has to do with data collection and tracking.

* **[Store description German/English](../store/quality-guidelines-apps/#app-descriptions-in-your-shopware-account)** - The app store description includes several points if the app can be used only in a specific country, so leave this clearly in the description. The German description is only mandatory if the app is to be offered in the German market. Furthermore, there must always be at least two images of the app in English, e.g., of the Storefront and the Admin. [Here](https://docs.shopware.com/en/account-en/adding-pictures-and-icons/how-to) you can find a guide detailing how to add images and icons to the extensions.

* **[Translations managed admin](../store/quality-guidelines-apps/#fallback-language)** - We check if the app is available in all languages specified in your account. However, it is important that English is fallback if the app does not support any other language.

* **[API validation](../store/quality-guidelines-apps/#api-or-payment-apps)** - If access data is required for the app - for example, an API key; a button must be implemented with which the customer can check the data if this is technically possible.

![api access](../../../../assets/guidelines-test-store-apiValidation.png)

* **[Uninstallation process](../store/quality-guidelines-apps/#extension-manager)** - During the uninstallation process, the app should be able to uninstall and install without any problems. It is also important to check whether the app depends on other apps and whether they must be uninstalled first.

* **Data will be removed from the database after uninstallation** - If the customer selects the option "delete all data" during uninstallation, then all the data has to be removed from the database that was created with the app.

* **Manual code review by a Shopware developer to ensure code quality** - This is the last step. A developer looks at the app's code to ensure it is clean and has no security gaps.

---

---

## Quality Guidelines for apps and themes based on the app system in the Shopware Store
**Source:** [resources/guidelines/testing/store/quality-guidelines-apps.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/testing/store/quality-guidelines-apps.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Quality Guidelines for apps and themes based on the app system in the Shopware Store

> **Changelog**
>
> > 09/11/24: Quality guidelines for apps and themes based on app system.
>
> > 23/11/23: [Added - New rules for Checklist for app testing](#every-app-based-on-the-app-system)
>
> > 27/09/23: [Added - Identical name rule](#every-app-based-on-the-app-system)
>
> > 26/07/23: [Added - Name preset according to new naming scheme](#every-app-based-on-the-app-system)

## The way we test apps and themes based on the app system

It is always a good idea to review our test process before submitting your app for review.
This ensures the quickest way for your app to be published.

We perform the *first test*, and if successful, we do the *follow-up test* again with the most current Shopware version.

The Shopware installation is located in a subfolder.
It has a language sub-shop/sales channel with a virtual URL as well as an independent sub-shop/sales channel with its own URL, also located in a subfolder.
E.g. `myshop.com/public/admin`.
The app must neither produce any error messages in the administration nor in the frontend.

The app is tested with the latest official Shopware 6 CE Version.

::: info
We always test with the [actual SW6 version](https://www.shopware.com/de/download/#shopware-6).
So set it to the actual SW6 version e.g., shopware/testenv:6.6.6.
Always test with the app\`s highest supported Shopware version.
:::

[Test your app for the Shopware Store (DE):](https://www.youtube.com/watch?v=gLb5CmOdi4g) and EN version is coming soon.

**Progressive Web App:** If your app is PWA compatible and you would like the PWA flag, please contact us at <alliances@shopware.com>.

## Checklist for app testing

Could you be sure to use the most recent testing checklist from Shopware and not any other provider?
Please pay attention to every point in this guide. We'll review it before you release your app.

### Every app and theme based on the app system

* We pay attention to the automatic code review and look for security issues and shopware coding standards in the manual code review.

* We check the complete functionality of the app (separately sales channel configurations in the config.xml, the uninstallation and reinstallation procedure) and check for styling errors on every viewport.

* We want to improve the quality of the Shopware Community Store and offer as many different apps as possible.
  Hence, we check for a functional comparison with other apps already in the Shopware Community store, in the Rise edition or above.
  If an extension with the same function exists and it does not fit into one of our differentiator clusters, it can be rejected as it doesn't provide any added value.
  If you would like more information, please write an email to <qa@shopware.com>.

[Differentiator cluster for Shopware extensions](../../../../../resources/guidelines/testing/Differentiator-Clusters.md)

[Documentation for Extension Partner](https://docs.shopware.com/en/account-en/extension-partner/extensions?category=account-en/extension-partner#how-can-i-request-a-preview)

::: info
**Safe your app idea and get a preview in the store**
If you already have an idea and don't want it to be snatched away, ensure you get it by creating a preview in your account.
You can apply for this if you have maintained placeholder images for the store, meaningful use cases, highlight features, a description, and a release month without uploading any binary.
:::

## App / Theme store description

The release to the English store is standard.
As an app / theme will be released in both stores (German and International), the content must accurately translate 1:1 from English to German.

* The mandatory number of characters is set in short and long descriptions. No blank spaces as fillers are allowed (EN/DE).
* Check if the description makes sense and describe the use cases of your app.
* Check if your configuration manual includes step-by-step instructions on how to configure and use your app.
* Check if you have included enough screenshots showing the app in action in the Storefront and administration.
* Check if the display name does not contain the terms "plugin" or "shopware".
* Check if all images for the English store description contain the English language. \[Please do not mix English with other languages in your screenshots. Screenshots in German for the German store description are optional.]
* Check if you explained the setup of the app / theme and added a configuration manual.

### Display Name

According to the new naming scheme, extensions may no longer display the words "plugin" and "shopware" in their names.
An extension with a name that directly reflects its functional purpose is permissible, even if it shares the same name as another extension.

Also, the store-display name had to be used for `theme.json` or `manifest.xml`.

### Short description

(Min. 150 — max. 185 characters)—The app's short description must be unique and at least 150 characters long.
Use the short description wisely, as the text will tease your app in the overview along with the "Customers also bought" and "Customers also viewed" recommendations.
The short description is also published as a meta-description.

### Description

(Min. 200 characters)—The app / theme description must be at least 200 characters long and describe the app's/theme's functions in detail.

* Inline styles will be stripped. The following HTML tags are allowed:

```markdown
<a> <p> <br> <b> <strong> <i> <ul> <ol> <li> <h2> <h3> <h4> <h5>
```

* **Tips:**

  * When it comes to increasing your app / theme sales, it is important that potential customers feel completely informed about your products and services.
    To this end, you should provide description, highlights, and features that are meaningful, detailed, and easy to understand, even for people with very minimal technical knowledge.
    Explain step-by-step how your app works and how to use it to achieve the desired result.
    Of course, your app description should be accompanied by clean HTML source code.

  * Video content increases awareness and trust and has proven to convert potential customers better than other content types.
    You can help your customers better understand your app or service with explainer videos, product demos, tutorials, etc.
    You can embed a maximum of 2 YouTube videos in your app description.

::: info
You can no longer advertise your Shopware certificates within the app description, in your app images, or in your manufacturer profile. The manufacturer/partner certificates are dynamically loaded at the end of each app description and published by us.
:::

### Images

::: info
Screenshots and preview images in English are standard. Only full English screenshots are accepted. Please do not mix English with other languages in your screenshots. Screenshots in German for the German store description are optional.
:::

Include several screenshots and descriptive images from the Storefront and backend that represent the app functionality.
They must show the app "in action", its configuration options, and how to use it.
We recommend uploading screenshots showing the mobile and desktop-view.

[How To - Add images and icons to extensions](https://docs.shopware.com/en/account-en/adding-pictures-and-icons/how-to)

### Link to demoshop

If you provide a demo shop, the link must be valid (the URL cannot contain `http:` or `https:`).
Do not link to your test environments, as we will delete them automatically two weeks after they are created.

### Personal data protection information

If necessary, personal data protection information has to be set.
If personal data of the customers (store operator and/or his customers) are processed with this extension according to Art. 28 DSGVO, the following information of the data processing company must be stored in the field "Subprocessor".

If other companies are involved in the data processing of personal data, the same information must be stored accordingly for them in the field "Further subprocessors".

### Configuration manual

Explain how your app is installed and configured, how it works on a technical base, and how it can be used to achieve the desired result.
Of course, your app manual should contain a setup guide and be accompanied by clean HTML source code.

### Manufacturer Profile

Your manufacturer profile must mandatorily contain accurate English and German descriptions and a manufacturer logo.
You can find the manufacturer profile in your account under Shopware Account > Extension Partner > [Extension Partner profile](https://account.shopware.com/producer/profile).

::: info
The source code's descriptions, profiles, and instructions do not allow iframes, external scripts, or tracking pixels.
Custom styles may not overwrite the original Shopware styles. External sources must be included via https.
:::

## Basic Guidelines

### Testing functionality

Due to our quality assurance, we check the app's / theme's complete functionality and test it wherever it impacts the administration or storefront.

Also, every app / theme will be code-reviewed by one of our core-developer ensuring coding and security standards.

### Extension master data/license

Please enter the valid license you set in your Shopware account.
You have to identify this license in the `manifest.xml` as well.

::: info
The chosen license can't be changed after adding your app / theme to your account.
If you want to change the license later, add a new app based on the app system with a new technical name and upload the extension again.
:::

### Fallback language / Translations

The installation is not always in English or German.
Could you make sure that your app works in other languages as well?
For example, if the customer has his installation in Spanish and your app is not yet available in this language, you should use the English translation as a fallback. Our test environment includes Dutch as the standard language.

If your app is available in more than one language (e.g., English, Spanish, French and German), these can be defined using the option "Translations into the following languages are available" (located in the “Description & images” section of your *Extension Manager*).

We check for text snippets, `config.xml`, `manifest.xml`, or `theme.json`.

### Valid preview images for the Shopware administration

Preview images: There must be a preview image available in the *Extension Manager*.
You must upload a valid favicon named plugin.png (png / 40 x 40 px) for the app.
This favicon will help you identify your app in the Extension Manager module in the administration.
The favicon has to be stored under `src/Resources/config/`.

Also, provide a preview image for Themes in the *Theme Manager* and CMS elements in the *Shopping Experiences*.

### Configuration per sales channel

Apps that appear in the Storefront and use a `config.xml` must be able to be configured separately for each sales channel.

### External links with rel="noopener"

Every external link in the administration or Storefront must be marked as *rel="noopener" AND target="\_blank"*.

### Error messages and logging

Error or informational messages can only be recorded in the event log of Shopware's log folder (/var/log/).
You have to develop your own log service.
Never write app exceptions into the Shopware default log or outside the Shopware system log folder.
This ensures that the log file can never be accessed via the URL.

### Avoid 400/500 Error

*Avoid 500 errors at any time.* Avoid 400 errors unless they are related to an API call.

### Not allowed to extend the Extension Manager

The *Extension Manager* must not be extended or overwritten.

### Extension manager

The Debug Console controls the app's installation, uninstallation, reinstallation, and deletion.
No 400 errors or exceptions are allowed to appear. If the app requires special PHP options, it must be queried during insta

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/resources/guidelines/testing/store/quality-guidelines-apps.md


---

## Quality Guidelines for the Plugin System in the Shopware Store
**Source:** [resources/guidelines/testing/store/quality-guidelines-plugins.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/testing/store/quality-guidelines-plugins.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Quality Guidelines for the Plugin System in the Shopware Store

> **Changelog**
>
> > 09/10/24: Quality guidelines for apps in the plugin system.
>
> > 01/08/24: [Added - Message queue](..//quality-guidelines-plugins/#message-queue)
>
> > 06/09/23: [Added - Rules for own composer dependencies](../quality-guidelines-plugins/#own-composer-dependencies)
>
> > 26/07/23: [Added - Identical name rule](../quality-guidelines-plugins/#every-app-based-on-the-plugin-system)

## The way we test apps based on the plugin system

It is always a good idea to review our test process before submitting your app for review.
This ensures the quickest way for your app to be published.

We perform the *first test*, and if successful, we do the *follow-up test* again with the most current Shopware version.

The Shopware installation is located in a subfolder.
It has a language sub-shop/sales channel with a virtual URL as well as an independent sub-shop/sales channel with its own URL, also located in a subfolder.
E.g. `myshop.com/public/admin`.
The app must neither produce any error messages in the administration nor in the frontend.

The app is tested with the latest official Shopware 6 CE Version.

::: info
We always test with the [actual SW6 version](https://www.shopware.com/de/download/#shopware-6).
So set it to the actual SW6 version e.g., shopware/testenv:6.6.6.
Always test with the app\`s highest supported Shopware version.
:::

Link: [Test your app for the Shopware Store (DE):](https://www.youtube.com/watch?v=gLb5CmOdi4g) and EN version is coming soon.

**Progressive Web App:** If your app is PWA compatible and you would like the PWA flag, please contact us at <alliances@shopware.com>.

## Checklist for app testing

Could you be sure to use the most recent testing checklist from Shopware and not any other provider?
Please pay attention to every point in this guide. We'll review it before you release your app.

### Every app based on the plugin system

* We pay attention to the automatic code review and look for security issues and shopware coding standards in the manual code review.

* We check the complete functionality of the app (separately sales channel configurations in the config.xml, the uninstallation and reinstallation procedure) and check for styling errors on every viewport.

* We want to improve the quality of the Shopware Community Store and offer as many different apps as possible.
  Hence, we check for a functional comparison with other apps already in the Shopware Community store, in the Rise edition or above.
  If an extension with the same function exists and it does not fit into one of our differentiator clusters, it can be rejected as it doesn't provide any added value.
  If you would like more information, please write an email to <qa@shopware.com>.

Link: [Differentiator cluster for Shopware extensions](../../../../../resources/guidelines/testing/Differentiator-Clusters.md)

Link: [Documentation for Extension Partner](https://docs.shopware.com/en/account-en/extension-partner/extensions?category=account-en/extension-partner#how-can-i-request-a-preview)

::: info
**Safe your app idea and get a preview in the store**
If you already have an idea and don't want it to be snatched away, ensure you get it by creating a preview in your account.
You can apply for this if you have maintained placeholder images for the store, meaningful use cases, highlight features, a description, and a release month without uploading any binary.
:::

## App store description

The release to the English store is standard.
As an app will be released in both stores (German and International), the content must accurately translate 1:1 from English to German.

* The mandatory number of characters is set in short and long descriptions. No blank spaces as fillers are allowed (EN/DE).
* Check if the description makes sense and describe the use cases of your app.
* Check if your configuration manual includes step-by-step instructions on how to configure and use your app.
* Check if you have included enough screenshots showing the app in action in the Storefront and administration.
* Check if the display name does not contain the terms "plugin" or "shopware".
* Check if all images for the English store description contain the English language. \[Please do not mix English with other languages in your screenshots. Screenshots in German for the German store description are optional.]
* Check if you explained the setup of the app and added a configuration manual.

### Display Name

According to the new naming scheme, extensions may no longer display the words "plugin" and "shopware" in their names.
An extension with a name that directly reflects its functional purpose is permissible, even if it shares the same name as another extension.

Also, the store-display name had to be used for `composer.json` and `config.xml`.

### Short description

(Min. 150 — max. 185 characters)—The app's short description must be unique and at least 150 characters long.
Use the short description wisely, as the text will tease your app in the overview along with the "Customers also bought" and "Customers also viewed" recommendations.
The short description is also published as a meta-description.

### Description

(Min. 200 characters)—The app description must be at least 200 characters long and describe the app's functions in detail.

* Inline styles will be stripped. The following HTML tags are allowed:

```markdown
<a> <p> <br> <b> <strong> <i> <ul> <ol> <li> <h2> <h3> <h4> <h5>
```

* **Tips:**

  * When it comes to increasing your app sales, it is important that potential customers feel completely informed about your products and services.
    To this end, you should provide description, highlights, and features that are meaningful, detailed, and easy to understand, even for people with very minimal technical knowledge.
    Explain step-by-step how your app works and how to use it to achieve the desired result.
    Of course, your app description should be accompanied by clean HTML source code.

  * Video content increases awareness and trust and has proven to convert potential customers better than other content types.
    You can help your customers better understand your app or service with explainer videos, product demos, tutorials, etc.
    You can embed a maximum of 2 YouTube videos in your app description.

::: info
You can no longer advertise your Shopware certificates within the app description, in your app images, or in your manufacturer profile.
The manufacturer/partner certificates are dynamically loaded at the end of each app description and published by us.
:::

### Images

::: info
Screenshots and preview images in English are standard. Only full English screenshots are accepted. Please do not mix English with other languages in your screenshots. Screenshots in German for the German store description are optional.
:::

Include several screenshots and descriptive images from the Storefront and backend that represent the app functionality.
They must show the app "in action", its configuration options, and how to use it.
We recommend uploading screenshots showing the mobile and desktop-view.

Link: [How To - Add images and icons to extensions](https://docs.shopware.com/en/account-en/adding-pictures-and-icons/how-to)

### Link to demoshop

If you provide a demo shop, the link must be valid (the URL cannot contain `http:` or `https:`).
Do not link to your test environments, as we will delete them automatically two weeks after they are created.

### Personal data protection information

If necessary, personal data protection information has to be set.
If personal data of the customers (store operator and/or his customers) are processed with this extension according to Art. 28 DSGVO, the following information of the data processing company must be stored in the field "Subprocessor".

If other companies are involved in the data processing of personal data, the same information must be stored accordingly for them in the field "Further subprocessors".

### Configuration manual

Explain how your app is installed and configured, how it works on a technical base, and how it can be used to achieve the desired result.
Of course, your app manual should contain a setup guide and be accompanied by clean HTML source code.

### Manufacturer Profile

Your manufacturer profile must mandatorily contain accurate English and German descriptions and a manufacturer logo.
You can find the manufacturer profile in your account under Shopware Account > Extension Partner > [Extension Partner profile](https://account.shopware.com/producer/profile).

::: info
The source code's descriptions, profiles, and instructions do not allow iframes, external scripts, or tracking pixels.
Custom styles may not overwrite the original Shopware styles. External sources must be included via https.
:::

## Basic Guidelines

### Testing functionality

Due to our quality assurance, we check the app's complete functionality and test it wherever it impacts the administration or storefront.

Also, every app will be code-reviewed by one of our core-developer ensuring coding and security standards.

### Extension master data/license

Please enter the valid license you set in your Shopware account.
You have to identify this license in the `composer.json` as well.

::: info
The chosen license can't be changed after adding your app to your account.
If you want to change the license later, add a new app based on the app system with a new technical name and upload the extension again.
:::

### Fallback language / Translations

The installation is not always in English or German.
Could you make sure that your app works in other languages as well?
For example, if the customer has his installation in Spanish and your app is not yet available in this language, you should use the English translation as a fallback. Our test environment includes Dutch as the standard language.

If your app is available in more than one language (e.g., English, Spanish, French and German), these can be defined using the option "Translations into the following languages are available" (located in the “Description & images” section of your *Extension Manager*).

We check for text snippets, `config.xml`, and `composer.json`.

### Valid preview images for the Shopware administration

Preview images: There must be a preview image available in the *Extension Manager*.
You must upload a valid favicon named plugin.png (png / 40 x 40 px) for the app.
This favicon will help you identify your app in the Extension Manager module in the administration.
The favicon has to be stored under `src/Resources/config/`.

Also, provide a preview image for Themes in the *Theme Manager* and CMS elements in the *Shopping Experiences*.

### Configuration per sales channel

Apps that appear in the Storefront and use a `config.xml` must be able to be configured separately for each sales channel.

### External links with rel="noopener"

Every external link in the administration or Storefront must be marked as *rel="noopener" AND target="\_blank"*.

### Error messages and logging

Error or informational messages can only be recorded in the event log of Shopware's log folder (/var/log/).
You have to develop your own log service.
Never write app exceptions into the Shopware default log or outside the Shopware system log folder.
This ensures that the log file can never be accessed via the URL.

For payment apps, we check if the "plugin logger" service is used for the debug/error.log and that logs are written in the directory /var/log/. Log files must be used in every circumstance.

The log file had to be named like this: "MyExtension-Year-Month-Day.log"

Another solution is to store them in the database.
Try to avoid using your own log tables. Otherwise, you have to implement a scheduled task that regularly empties your log table within the given time of max. 6 months.

### Avoid 400/500 Error

*Avoid 500 errors at any time.* 

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/resources/guidelines/testing/store/quality-guidelines-plugins.md


---

## Troubleshooting
**Source:** [resources/guidelines/trouble-shoting.md](https://developer.shopware.com/docs/v6.6/resources/guidelines/trouble-shoting.md)  
# Troubleshooting

## Performance

### Dynamic product groups are slow to load

When you use a `contains` filter in dynamic product groups (especially when you use that on a custom field), the loading of that dynamic product group might get slow.
The reason is that the underlying SQL query is not and cannot be optimized for this kind of filter. When you use OpenSearch instead of relying on the DB for searching, this issue should be resolved.
Alternatively, for using `contains` on custom fields, it should be preferred to create individual bool custom fields for the different values and check those instead.
When contains on usual fields is used and slow, it should help to add a [custom field](../../guides/plugins/plugins/framework/custom-field/) and manually manage that.
Alternatively, [tags](https://docs.shopware.com/en/shopware-6-en/settings/tags) can be used for this purpose.

### Cache is invalided too often

It might be that your caching is not effective because the cache is invalidated too often. You should look for the reason why the cache is invalidated that frequently.
In general, it means that probably there is a background process running that leads to the cache invalidation.
This could be more obvious cases like cron jobs manually clearing the cache or more subtle cases like your ERP system syncing products frequently, which will lead to cache invalidations of all pages where those products are referenced.
For cases like the latter, there is the option to only clear the cache delayed and not immediately ([this will be the new default starting with shopware 6.7.0.0](https://github.com/shopware/shopware/blob/trunk/UPGRADE-6.7.md#delayed-cache-invalidation)). You might consider [activating this feature](../../guides/hosting/performance/performance-tweaks.md#delayed-invalidation) in older versions.

---

---

## Troubleshooting
**Source:** [resources/guidelines/troubleshooting.md](https://developer.shopware.com/docs/resources/guidelines/troubleshooting.md)  
# Troubleshooting

Use this section to diagnose and resolve common issues you might encounter while working with Shopware projects.

---

---

## Elasticsearch
**Source:** [resources/guidelines/troubleshooting/elasticsearch.md](https://developer.shopware.com/docs/resources/guidelines/troubleshooting/elasticsearch.md)  
# Elasticsearch

## Common Error Handling

### Enabling `SHOPWARE_ES_THROW_EXCEPTION`

It is recommended to set the environment variable `SHOPWARE_ES_THROW_EXCEPTION=0` in **production environments** and enable it (`=1`) in **development environments**.
This setting helps prevent unexpected interruptions to other processes caused by Elasticsearch or OpenSearch issues.

Some common scenarios include:

* **Search server is not reachable**:
  If the OpenSearch or Elasticsearch server is temporarily unavailable, keeping this option disabled (`=0`) allows Shopware to automatically fall back to the default MySQL-based search. This ensures that search functionality remains available.
  A similar fallback also applies when updating products in the Administration, where data synchronization with the search server might fail intermittently.

* **System updates causing expected errors**:
  During updates—whether through the web UI or via the CLI (`bin/console system:update:finish`)—index mappings may change, requiring a reindex. These expected errors should not block system updates in production, which is why exceptions should remain disabled in such environments.

***

## Adjusting N-gram Settings for Search Precision

When a search field is marked as *searchable* and the **“Split search term”** option is enabled, Shopware uses an **n-gram tokenizer** to index and search that field.
By default, Shopware uses the following configuration:

```bash
SHOPWARE_ES_NGRAM_MIN_GRAM=4
SHOPWARE_ES_NGRAM_MAX_GRAM=5
```

With this configuration, a term like `"shopware"` is tokenized into the following n-grams:

```bash
["shop", "hopw", "opwa", "pwar", "ware", "shopw", "hopwa", "opwar", "pware"]
```

This allows search results to match even if only part of the search term is entered—for example, searching for `"ware"` will still find `"shopware"`.

If you want to make the search more flexible (fuzzier) or more precise (stricter), you can adjust the environment variables:

```bash
SHOPWARE_ES_NGRAM_MIN_GRAM=<value>
SHOPWARE_ES_NGRAM_MAX_GRAM=<value>
```

After modifying these values, a full Elasticsearch reindex is required to apply the new configuration:

```bash
bin/console es:index
```

---

---

## Performance
**Source:** [resources/guidelines/troubleshooting/performance.md](https://developer.shopware.com/docs/resources/guidelines/troubleshooting/performance.md)  
# Performance

## Common Performance Considerations

### Dynamic product groups are slow to load

When you use a `contains` filter in dynamic product groups (especially when you use that on a custom field), the loading of that dynamic product group might get slow.
The reason is that the underlying SQL query is not and cannot be optimized for this kind of filter.
When you use OpenSearch instead of relying on the DB for searching, this issue should be resolved.
Alternatively, for using `contains` on custom fields, it should be preferred to create individual bool custom fields for the different values and check those instead.
When contains on usual fields is used and slow, it should help to add a [custom field](../../../guides/plugins/plugins/framework/custom-field/index) and manually manage that.
Alternatively, [tags](https://docs.shopware.com/en/shopware-6-en/settings/tags) can be used for this purpose.

### Cache is invalided too often

It might be that your caching is not effective because the cache is invalidated too often.
You should look for the reason why the cache is invalidated that frequently.
In general, it means that probably there is a background process running that leads to the cache invalidation.
This could be more obvious cases like cron jobs manually clearing the cache or more subtle cases like your ERP system syncing products frequently,
which will lead to cache invalidations of all pages where those products are referenced.
For cases like the latter, there is the option to only clear the cache delayed and not immediately ([this will be the new default starting with shopware 6.7.0.0](https://github.com/shopware/shopware/blob/trunk/UPGRADE-6.7.md#delayed-cache-invalidation)).
You might consider [activating this feature](../../../guides/hosting/performance/performance-tweaks#redis-for-delayed-cache-invalidation) in older versions.

### High Memory Usage

While using certain APIs or e.g. the `EntityRepository` it might happen that the memory usage is increasing constantly.
First, you should make sure that you have set the `APP_ENV` variable to `prod` in your `.env` file.
If the `APP_ENV` is set to `dev` Shopware keeps many objects for debugging purposes, which will lead to high memory usage.
If the memory usage issue persists after setting `APP_ENV` to `prod`, check if you are using the [sync API](https://shopware.stoplight.io/docs/admin-api/faf8f8e4e13a0-bulk-payloads).
Also consider changing the `indexing-behavior` to your needs if you need to sync many entities.
Another reason for high memory usage might be the logging within the application.
See the logging section in the [performance guide](../../../guides/hosting/performance/performance-tweaks#logging) for more information.
After all, you still can make use of tools like blackfire.io to find the root cause of the memory usage.

### Session Deadlocks with file-based sessions

If you experience request timeouts or hanging requests in environments using file-based sessions (common in shared hosting), you might be encountering a session deadlock. This occurs when two concurrent processes create a circular lock dependency: one process holds the session file lock while trying to acquire the cache lock, another holds the cache lock while trying to acquire the session lock.

Symptoms include:

* Requests randomly timing out under load
* PHP processes stuck in "waiting" state
* Issues appearing only under concurrent requests

The recommended solution is to [use Redis for sessions](../../../guides/hosting/performance/session), which eliminates the file-based locking conflict.
If Redis is not available in your environment, you can work around the issue by disabling cache stampede protection (option available since Shopware 6.7.7.0).

```yaml
shopware:
  cache:
    disable_stampede_protection: true
```

This option only takes effect when file-based sessions are detected. Be aware that disabling stampede protection may increase backend load when multiple requests simultaneously try to regenerate the same expired cache entry. For most shops, this trade-off is acceptable compared to deadlock issues.

---

---

## PHPStan
**Source:** [resources/guidelines/troubleshooting/phpstan.md](https://developer.shopware.com/docs/resources/guidelines/troubleshooting/phpstan.md)  
# PHPStan

## Common PHPStan Issues in Shopware Code

### EntityRepository Should Define a Generic Type

**Problem**: Repository returns EntityCollection without type information.

```php
$products = $this->productRepository->search($criteria, $context)->getEntities();
foreach ($products as $product) {
    // PHPStan doesn't know $product is ProductEntity
    $name = $product->getName(); // Call to an undefined method Shopware\Core\Framework\DataAbstractionLayer\Entity::getName()
}
```

**Solution**: Add a PHP doc with a generic type to EntityRepository:

```php
class Foo
{
    /**
     * @param EntityRepository<ProductCollection> $productRepository
     */
    public function __construct(
        private readonly EntityRepository $productRepository,
    ) {
    }

    public function doSomething(): void
    {
        // ...
        $products = $this->productRepository->search($criteria, $context)->getEntities();
        foreach ($products as $product) {
            $name = $product->getName(); // PHPStan correctly identifies this as ProductEntity
        }
    }
}
```

Be aware that the `EntityRepository` class is a generic class, which gets an EntityCollection as type.
This might sound counter-intuitive and different to other well-known repository classes, which take the Entity class as the generic type.
But it was the easiest technical solution to get PHPStan to understand the type of the collection returned by the search method.

### Null Safety with First method and Associations

**Problem**: Calling `first` could return `null`, also entity associations can be `null` if not loaded.

```php
$product = $this->productRepository->search($criteria, $context)->first();
$manufacturer = $product->getManufacturer(); // Cannot call method getManufacturer() on Shopware\Core\Content\Product\ProductEntity|null.
$manufacturerName = $manufacturer->getName(); // Cannot call method getName() on Shopware\Core\Content\Product\Aggregate\ProductManufacturer\ProductManufacturerEntity|null.
```

**Solution**: Ensure associations are added before in the criteria and always check for possible `null` returns:

```php
$criteria = new Criteria();
$criteria->addAssociation('manufacturer');

$product = $this->productRepository->search($criteria, $context)->first();
if ($product === null) {
    throw new ProductNotFoundException();
}

$manufacturer = $product->getManufacturer();
if ($manufacturer === null) {
    throw new ManufacturerNotLoadedException();
}

$manufacturerName = $manufacturer->getName(); // No error
```

Or use the null-safe operators:

```php
$manufacturerName = $product?->getManufacturer()?->getName() ?? 'Unknown';
```

### Missing Generic Type for EntityCollection

**Problem**: Custom EntityCollection does not have a generic type.

```php
class FooCollection extends EntityCollection
{
    protected function getExpectedClass(): string
    {
        return FooEntity::class;
    }
}

$foo = $fooCollection->first();
if ($foo === null) {
    throw new FooNotFoundException();
}
$foo->bar(); // Cannot call method bar() on Shopware\Core\Framework\DataAbstractionLayer\Entity.
```

**Solution**: Add a generic type to EntityCollection:

```php
/**
 * @extends EntityCollection<FooEntity>
 */
class FooCollection extends EntityCollection
{
    protected function getExpectedClass(): string
    {
        return FooEntity::class;
    }
}

$foo = $fooCollection->first();
if ($foo === null) {
    throw new FooNotFoundException();
}
$foo->bar(); // No error
```

---

---

## Tooling
**Source:** [resources/tooling.md](https://developer.shopware.com/docs/v6.6/resources/tooling.md)  
# Tooling

---

---

## CLI
**Source:** [resources/tooling/cli.md](https://developer.shopware.com/docs/v6.6/resources/tooling/cli.md)  
# CLI

---

---

## Hot Module Replacement
**Source:** [resources/tooling/cli/using-watchers.md](https://developer.shopware.com/docs/v6.6/resources/tooling/cli/using-watchers.md)  
# Hot Module Replacement

## Building JS and CSS

When developing with Shopware, you will probably notice that changes in JavaScript require commands to build the Administration or
Storefront, depending on your change using the following commands:

```bash
composer run build:js:admin
```

```bash
./bin/build-administration.sh
```

```bash
composer run build:js:storefront
```

```bash
./bin/build-storefront.sh
```

## Watchers

This building process is always time-consuming. Alternatively, to speed up the process.
Shopware's [Production template](https://github.com/shopware/production) and [Source code](https://github.com/shopware/shopware) offers
commands to enable Hot Module Replacement (HMR) to automatically reload and preview your changes.

::: info
This procedure doesn't replace the final build process when you finish developing your feature.
:::

To enable Hot Module Replacement, use the following composer commands in the Shopware source code:

```bash
composer run watch:admin
```

```bash
composer run watch:storefront
```

To enable Hot Module Reloading, use the following shell scripts in the Shopware Production template:

```bash
./bin/watch-administration.sh
```

```bash
./bin/watch-storefront.sh
```

### Environment variables

Using environment variables can also affect Shopware and, therefore, its watchers. Like in Unix, prefixing command calls with a variable set
will run the command with the respective change. The following example will run the storefront watcher in production mode:

```bash
APP_ENV=prod composer run watch:storefront
```

#### APP\_ENV

When using `APP_ENV=dev`, Shopware runs in development mode and provides features for debugging - for example, the Symfony toolbar in the
Storefront, while its counterpart `APP_ENV=prod` enables production mode and therefore disables any such tools.

#### IPV4FIRST

Starting with NodeJS v17.0.0, it prefers IPv6 over IPv4. However, in some setups, IPv6 may cause problems when using watchers. In such
cases, setting `IPV4FIRST=1` reverts this behavior.

---

---

## Fixture Bundle
**Source:** [resources/tooling/fixture-bundle.md](https://developer.shopware.com/docs/resources/tooling/fixture-bundle.md)  
# Fixture Bundle

The Fixture Bundle provides a flexible and organized way to load test and demo data into your Shopware 6 application. It's designed to be extensible and easy to use, supporting dependency management, priority-based execution, and group filtering. This guide will walk you through the process of creating and managing data fixtures for your Shopware project.

## Installation

To get started, add the Fixture Bundle to your project using Composer:

```bash
composer require shopware/fixture-bundle:*
```

## Creating a basic fixture

To create a fixture, you need to create a new class that implements the `Shopware\Core\Framework\Test\TestCaseBase\FixtureInterface` and has the `#[Fixture]` attribute.

Here is an example of a simple fixture that creates two product categories:

```php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Test\Fixture;

use Shopware\Core\Framework\DataAbstractionLayer\EntityRepository;
use Shopware\Core\Framework\Test\TestCaseBase\Fixture;
use Shopware\Core\Framework\Test\TestCaseBase\FixtureInterface;
use Shopware\Core\Framework\Uuid\Uuid;
use Symfony\Component\DependencyInjection\Attribute\Autowire;

#[Fixture(name: 'category')]
class CategoryFixture implements FixtureInterface
{
    public function __construct(
        #[Autowire(service: 'category.repository')]
        private readonly EntityRepository $categoryRepository,
    ) {
    }

    public function load(): void
    {
        $categories = [
            [
                'id' => Uuid::randomHex(),
                'name' => 'Electronics',
                'active' => true,
            ],
            [
                'id' => Uuid::randomHex(),
                'name' => 'Clothing',
                'active' => true,
            ],
        ];

        $this->categoryRepository->create($categories, Context::createDefaultContext());
    }
}
```

### The `Fixture` attribute

The `#[Fixture]` attribute configures the behavior of your fixture and accepts the following parameters:

* **`priority`** (`int`, default: `0`): A higher integer means the fixture will be executed earlier.
* **`dependsOn`** (`array`, default: `[]`): An array of fixture class names that must be executed before this fixture.
* **`groups`** (`array`, default: `['default']`): An array of group names this fixture belongs to. This allows for selective loading of fixtures.

## Commands

The Fixture Bundle comes with two `bin/console` commands to help you manage your fixtures.

### Loading fixtures

To execute your fixtures and load data into the database, use the `fixture:load` command.

* **Load all fixtures:**

  ```bash
  bin/console fixture:load
  ```

* **Load fixtures from a specific group:**
  You can also load a subset of fixtures by specifying a group. This is useful for separating test data from demo data, for example.

  ```bash
  bin/console fixture:load --group=test-data
  ```

### Listing fixtures

To see a list of all available fixtures, their execution order, and their configuration, use the `fixture:list` command.

```bash
bin/console fixture:list
```

This command provides a clear overview of how your fixtures are prioritized and what their dependencies are.

**Example output:**

```text
 Available Fixtures
 ==================

+-------+---------------------+----------+-----------------+---------------------+
| Order | Class               | Priority | Groups          | Depends On          |
+-------+---------------------+----------+-----------------+---------------------+
| 1     | CategoryFixture     | 100      | catalog, test-  | -                   |
|       |                     |          | data            |                     |
| 2     | ManufacturerFixture | 90       | catalog         | -                   |
| 3     | ProductFixture      | 50       | catalog, test-  | CategoryFixture,    |
|       |                     |          | data            | ManufacturerFixture |
| 4     | CustomerFixture     | 0        | customers       | -                   |
+-------+---------------------+----------+-----------------+---------------------+

 [OK] Found 4 fixture(s).
```

## Execution order

The execution order of fixtures is determined by the following rules:

1. **Dependencies**: If a fixture declares dependencies using `dependsOn`, it will always run after its dependencies have been executed.
2. **Priority**: Among fixtures without dependency relationships, those with a higher `priority` value are executed first.
3. **Circular dependency detection**: The system will throw an exception if circular dependencies are detected, preventing infinite loops.

## Specialized fixtures

The Fixture Bundle includes several specialized loaders to simplify common data creation tasks.

### Theme fixtures

The `ThemeFixtureLoader` provides a convenient, fluent interface for configuring theme settings. It automatically handles theme discovery, recompilation, and only applies changes when necessary.

```php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Test\Fixture;

use Shopware\Core\Framework\Test\TestCaseBase\Fixture;
use Shopware\Core\Framework\Test\TestCaseBase\FixtureInterface;
use Shopware\Storefront\Theme\ThemeDefinition;

#[Fixture(name: 'theme', groups: ['theme-config', 'branding'])]
class ThemeFixture implements FixtureInterface
{
    public function __construct(
        private readonly ThemeFixtureLoader $themeFixtureLoader
    ) {
    }

    public function load(): void
    {
        // Will be uploaded just once and reused based on file content
        $logo = $this->mediaHelper->upload(__DIR__ . '/shop.png', $this->mediaHelper->getDefaultFolder(ThemeDefinition::ENTITY_NAME)->getId());

        $this->themeFixtureLoader->apply(
            (new ThemeFixtureDefinition('Shopware default theme'))
                ->config('sw-color-brand-primary', '#ff6900')
                ->config('sw-border-radius-default', '8px')
                ->config('sw-font-family-base', '"Inter", sans-serif')
                ->config('sw-logo-desktop', $logo)
        );
    }
}
```

### Custom field fixtures

The `CustomFieldSetFixtureLoader` helps you create and manage custom field sets and their associated custom fields for different entities.

```php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Test\Fixture;

use Shopware\Core\Framework\Test\TestCaseBase\Fixture;
use Shopware\Core\Framework\Test\TestCaseBase\FixtureInterface;
use Shopware\Core\System\CustomField\CustomFieldTypes;

#[Fixture(name: 'custom-field')]
class CustomFieldFixture implements FixtureInterface
{
    public function __construct(
        private readonly CustomFieldSetFixtureLoader $customFieldSetFixtureLoader
    ) {
    }

    public function load(): void
    {
        $this->customFieldSetFixtureLoader->apply(
            (new CustomFieldSetFixtureDefinition('Product Specifications', 'product_specs'))
                ->relation('product')
                ->field(
                    (new CustomFieldFixtureDefinition('weight', CustomFieldTypes::FLOAT))
                        ->label('en-GB', 'Weight (kg)')
                        ->label('de-DE', 'Gewicht (kg)')
                )
                ->field(
                    (new CustomFieldFixtureDefinition('warranty_period', CustomFieldTypes::INT))
                        ->label('en-GB', 'Warranty Period (months)')
                )
        );
    }
}
```

### Customer fixtures

The `CustomerFixtureLoader` offers a comprehensive way to create customers with addresses, custom fields, and other properties. The loader uses the email address as a unique identifier, updating existing customers if a match is found.

```php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Test\Fixture;

use Shopware\Core\Framework\Test\TestCaseBase\Fixture;
use Shopware\Core\Framework\Test\TestCaseBase\FixtureInterface;

#[Fixture(name: 'customer', groups: ['customers', 'addresses'])]
class CustomerFixture implements FixtureInterface
{
    public function __construct(
        private readonly CustomerFixtureLoader $customerFixtureLoader
    ) {
    }

    public function load(): void
    {
        $this->customerFixtureLoader->apply(
            (new CustomerFixtureDefinition('max.mustermann@example.com'))
                ->firstName('Max')
                ->lastName('Mustermann')
                ->salutation('mr')
                ->password('password')
                ->defaultBillingAddress([
                    'firstName' => 'Max',
                    'lastName' => 'Mustermann',
                    'street' => 'Musterstraße 123',
                    'zipcode' => '12345',
                    'city' => 'Musterstadt',
                    'country' => 'DEU',
                ])
                ->addAddress('work', [
                    'firstName' => 'Max',
                    'lastName' => 'Mustermann',
                    'street' => 'Office Street 789',
                    'zipcode' => '11111',
                    'city' => 'Business City',
                    'country' => 'DEU',
                ])
        );
    }
}
```

## Best practices

* **Meaningful Names**: Give your fixture classes clear, descriptive names.
* **Organize with Groups**: Use groups like `test-data`, `demo-data`, or `performance-test` to categorize fixtures.
* **Declare Dependencies**: Explicitly declare dependencies to ensure a predictable and correct execution order.
* **Focused Fixtures**: Each fixture should have a single, clear responsibility.
* **Idempotent Design**: Fixtures should be possible to run multiple times without causing errors or creating duplicate data.
* **Use Dependency Injection**: Inject services into your fixture's constructor instead of fetching them from the container.

By following these guidelines, you can build a robust and maintainable set of data fixtures for your Shopware project.

---

---

## IDE
**Source:** [resources/tooling/ide.md](https://developer.shopware.com/docs/v6.6/resources/tooling/ide.md)  
# IDE

---

---

## Shopware 6 Toolbox
**Source:** [resources/tooling/ide/shopware-toolbox.md](https://developer.shopware.com/docs/v6.6/resources/tooling/ide/shopware-toolbox.md)  
# Shopware 6 Toolbox

Shopware 6 Toolbox is a helper plugin and productivity tool for common tasks for Shopware 6 development. It adds some live templates and scaffolding of common Shopware files.

![Shopware Toolbox Screenshot 1](../../../assets/shopware-toolbox-1.png)

![Shopware Toolbox Screenshot 2](../../../assets/shopware-toolbox-2.png)

## Current features

### Live templates

Multiple live templates for development. Use Cmd/Ctrl + J to see all live templates available.

### Generators

* Vue.js Admin component
* config.xml
* Extend Storefront blocks with automatic file creation
* Vue module
* Scheduled task
* Changelog

### Static code check

Inspection to show an error when abstract class is used incorrectly in the constructor (guideline check).

### Auto-completion

* Admin components
* Snippets in Administration and Storefront
* Storefront functions `theme_config`, `config`, `seoUrl`, `sw_include` and `sw_extends`
* Repositories at this.repositoryFactory.create
* Module.register labels
* Show only admin component auto-completion when the twig file is next to an index.js
* Feature flags

## Installation

Either search for `Shopware 6 Toolbox` in the JetBrains Marketplace or get it on the marketplace website.

---

---

