# TESTING AND QUALITY

Compiled excerpts from the Shopware Developer Documentation snapshot. Prefer live docs at [developer.shopware.com](https://developer.shopware.com/) when in doubt.

---

## Testing
**Source:** [guides/plugins/plugins/testing.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/testing.md)  
# Testing

When it comes to testing, you might immediately think about unit tests. Of course, we have got you covered then:

Even though unit tests are definitely great, you might want to do some end-to-end testing, which is covered here:

Following section also covers unit tests in Storefront and Administration.

---

---

## Cypress End-to-end testing
**Source:** [guides/plugins/plugins/testing/cypress.md](https://developer.shopware.com/docs/guides/plugins/plugins/testing/cypress.md)  
# Cypress End-to-end testing

:::warning
Cypress will be deprecated in the future and is no longer maintained. We recommend using [Playwright](../playwright/index.md) for new projects.
:::

---

---

## Best practices for writing end-to-end tests
**Source:** [guides/plugins/plugins/testing/cypress/cypress-best-practises.md](https://developer.shopware.com/docs/guides/plugins/plugins/testing/cypress/cypress-best-practises.md)  
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

Another useful way for waiting in the Administration is using Cypress possibility to work with [network requests](https://docs.cypress.io/app/guides/network-requests). Here you can let the test wait for a successful API response:

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

## Cypress End-to-End Testing
**Source:** [guides/plugins/plugins/testing/cypress/cypress-end-to-end-testing.md](https://developer.shopware.com/docs/guides/plugins/plugins/testing/cypress/cypress-end-to-end-testing.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Cypress End-to-End Testing

## Overview

In end-to-end testing (E2E testing in short) real user workflows are simulated, whereby as many as possible functional areas and parts of the technology stack used in the application should be included. This way, we are able to put our UI under constant stress and ensure that Shopware's main functionalities are always working correctly.

## Prerequisites

To use Shopware E2E tests, at first you need to have a Shopware 6 installation running. Making sure, that your tests are reliable, you should have a clean installation. Cleanup means no categories, no products, no settings, nothing!

The easiest way to clean up your installation is the initialization. Using the command `composer run init` Shopware 6 gets initialized clean and without demo data. Installation of E2E dependencies can be accomplished separately by running `npm install` in the E2E folder you're using, e.g. for Shopware Administration it's `src/Administration/Resources/app/administration/test/e2e`.

Since our tests should run on an installation that is as close as possible to a release package, we use production mode. If you run the tests on a development environment, the test results may vary.

On top of that, please make sure your shop has a theme assigned. When using `composer run e2e:open` or `run`, this is done automatically.

This guide also won't teach you how to write Cypress tests in general. Please take a look at the official Cypress documentation for further guidance.

### Using our testsuite

The [E2E platform testsuite package](https://github.com/shopwareArchive/e2e-testsuite-platform) contains commands and helpers supporting you while building E2E tests for Shopware 6. On top of that, test data management and custom commands are included as well. More on that here: [Command reference](../../../../resources/references/core-reference/commands-reference/).

This test suite is built on top of [Cypress](https://www.cypress.io/) as well as the following Cypress plugins:

* [cypress-select-tests](https://github.com/bahmutov/cypress-select-tests)
* [cypress-log-to-output](https://github.com/flotwig/cypress-log-to-output)
* [cypress-file-upload](https://github.com/abramenal/cypress-file-upload)

Here you can find the npm package of our testsuite:

Please have a look on our [cypress.json](https://github.com/shopwareArchive/e2e-testsuite-platform/blob/3.x/cypress.json), a few of our commands expect some configuration, e.g. viewportHeight and width, because the admin menu only opens if the viewport is wide enough.

## Setup steps

When you use our [Development template](https://github.com/shopwareArchive/development), we provide you some tooling scripts located in `dev-ops/e2e/actions`, to use E2E tests more comfortably.

The`composer` scripts to run our E2E tests in CLI or in Cypress' test runner are explained in the paragraph [Executing e2e tests](end-to-end-testing/#executing-e2e-tests).

Depending on your environment (administration or storefront) please create the following folder structure:

```text
Resources
  `-- app
    `-- <environment>
      `-- test
        `-- e2e
          `-- cypress
            |-- fixtures
            |-- integration
            |-- plugins
            `-- support
```

We will cover the use of every folder in detail.

Within the folder `Resources/app/<environment>/test/e2e`, please run `npm init -y` to generate a `package.json` file. It is very convenient to place a script inside the newly created `package.json` to run the tests locally. Please add the following section to do so:

```javascript
"scripts": {
   "open": "node_modules/.bin/cypress open"
},
```

Now install this package with the following command:

```text
npm install @shopware-ag/e2e-testsuite-platform
```

As next step, please create a new file `e2e/cypress/plugins/index.js` with the following content:

```javascript
module.exports = require('@shopware-ag/e2e-testsuite-platform/cypress/plugins');
```

Finally, create a new file e2e/cypress/support/index.js with the following line:

```javascript
// Require test suite commands
require('@shopware-ag/e2e-testsuite-platform/cypress/support');
```

However, as we're using this image for running the test runner as well, you may need to do some configuration first. Based on this [guide](https://www.cypress.io/blog/run-cypress-with-a-single-docker-command) you need to forward the XVFB messages from Cypress out of the Docker container into an X11 server running on the host machine. The guide shows an example for Mac; other operating systems might require different commands.

In case you're using Docker on Mac we have summarized the steps from the guide mentioned above, so you can follow these to prepare your environment to get the Test Runner up and running:

**Install and configure XQuartz**

Install XQuartz via [Homebrew](https://docs.brew.sh/Installation) or alternatively [download](https://www.xquartz.org/) it from the official homepage:

```bash
brew install --cask xquartz
```

Run XQuartz via CLI or open it from your Desktop:

```bash
open -a XQuartz
```

Got to `XQuartz > Preferences` (`⌘ + ,`) and enable `Allow connections from network clients`:

![XQuartz Preferences](../../../../../assets/xquartz-allow-connections-from-network-clients.png)

::: warning
Restart your Mac before proceeding with the following steps.
:::

**Configure your environment**

Grab your IP address and save it to the environment variable `IP`:

```bash
IP=$(ipconfig getifaddr en0)
```

Depending on how you're connected you might have to use another interface instead of `en0`.

Now set the `DISPLAY` environment variable:

```bash
DISPLAY=$IP:0
```

Add `$IP` to xhost's ACL:

```bash
xhost + $IP
```

::: danger
It is **crucial** to set these environment variables in the **same terminal session** from where you will later run `psh e2e:open`!

Make sure that the `DISPLAY` environment variable on your Mac is properly set **before** you start the containers as it will be **passed** to the Cypress container when the container is **created**.
Updating the variable on your host won't update it in the container until it is re-created!
:::



## Executing E2E tests

If you want to run E2E tests in your plugin, just switch to the folder `Resources/app/<environment>/test/e2e` and execute the following command:

```bash
CYPRESS_baseUrl=<your-url> npm run open
```

`<your-url>` means the Storefront-URL of your Shopware environment.

It opens up the Cypress test runner which allows you to run and debug your tests, similar to the `e2e:open` command.

::: danger
Don't forget that you might need to adjust test cleanup and other environment-related things according to your plugin's setup.
:::

To prepare your shopware installation, your environment and install dependencies, please run the following command as first step, **outside** of your docker container:

```bash
 composer run e2e:setup
```

In our tests, we assume a clean shopware installation, so we strongly recommend to use `e2e:setup`. However, if your shopware installation is already clean and prepared, you can skip the preparation of your shopware installation by using the following command **inside** your docker container:

```bash
 composer run e2e:prepare
```

Afterwards, just use the following command outside of your container to run the Cypress Test Runner:

```bash
composer run e2e:open
```

If you want to run the tests in CLI, please use the following command outside your container:

```bash
composer e2e:cypress -- run --spec="cypress/e2e/administration/**/*.cy.js"
```

or

```bash
composer e2e:cypress -- run --spec="cypress/e2e/storefront/**/*.cy.js"
```

To see a complete overview on all psh scripts for e2e tests, feel free to refer to our [e2e command reference](../../../../../resources/references/testing-reference/e2e-commands/).



## Writing your first test

### Folder structure

In Shopware platform, you can find the tests in `src/Administration/Resources/app/administration/test/e2e`. There you can find the following folder structure, depending on your environment being Administration or Storefront:

```bash
`-- e2e
  `-- cypress
    |-- fixtures
        `-- example.json
    |-- integration
        `-- testfile.spec.js
    |-- plugins
        `-- index.js
    |-- support
        |-- commands.js
        `-- index.js
    |--cypress.json
    `--cypress.env.json
```

In the `cypress` folder, all test related folders are located. Most things will take place in these four folders:

* `fixtures`: Fixtures are used as external pieces of static data that can be used by your tests. You can use them

  with the `cy.fixture` command.

* `integration`: By default, the test files are located here. A file with the suffix "\*.spec.js" is a test file that

  contains a sequence of tests, performed in the order defined in it.

* `plugins`: Contains extensions or plugins. By default, Cypress will automatically include the plugins file before

  every single spec file it runs.

* `support`: The support folder is a great place to put reusable behavior such as custom commands or global overrides in,

  that you want to be applied and available to all of your spec files.

These two configuration files are important to mention as well:

* `cypress.json`
* `cypress.env.json`

  These are Cypress configuration files. If you need more information about them, take a look at the

  [Cypress configuration docs](https://docs.cypress.io/app/references/configuration).

If you need to use this structure in a plugin, it is just the path to the `e2e` folder, which is slightly different. You can find the folder structure in the paragraph [Setup](cypress-end-to-end-testing#setup-steps).

If you want to contribute to Shopware platform's tests, please ensure to place your test in one of those folders:

```javascript
`-- integration
  |-- catalogue
  |-- content
  |-- customer
  |-- general
  |-- media-marketing
  |-- order
  |-- rule-product-stream
  `-- settings
```

::: warning
This is important because otherwise your test is not considered by our CI.
:::

### Test layout and syntax

Cypress tests are written in Javascript. If you worked with Mocha before, you will be familiar with Cypress' test layout. The test interface borrowed from Mocha provides `describe()`, `context()`, `it()` and `specify()`.

To have a frame surrounding your test and provide a nice way to keep your test organized, use `describe()` (or `context()` as its alias):

```javascript
describe('Test: This is my test file', () => {
    it('test something', () => {
        // This is your first test
    });
    it('tests something else', () => {
        // This is your second test
    });
});
```

The `it()` functions within the `describe()` function are your actual tests. Similar to `describe()` and `context()`, `it()` is identical to `specify()`. However, for writing Shopware tests we focus on `it()` to keep it consistent.

## Commands and assertions

In Cypress, you use commands and assertions to describe the workflow you want to test.

### Commands

Commands are the actions you need to do in order to interact with the elements of your application and reproduce the workflow to test in the end.

```javascript
it('test something', () => {
    ...
    cy.get('.sw-grid__row--0')
        .contains('A Set Name Snippet')
        .dblclick();
    cy.get('.sw-grid__row--0 input')
        .clear()
        .type('Nordfriesisch')
        .click();
    ...
    });
```

You can chain commands by passing its return value to the next one. These commands may contain extra steps to take, e.g. a `click` or `type` operation.

Cypress provides a lot of commands to represent a variety of steps a user could do. On top of that, our E2E testsuite contains a couple of [custom commands](../../../../../resources/references/testing-reference/e2e-custom-commands/) specially for Shopware.

### Assertions

Assertions describe the desired state of your elements, objects and application. Cypre

… **Truncated.** Full document: https://developer.shopware.com/docs/guides/plugins/plugins/testing/cypress/cypress-end-to-end-testing.md


---

## End-to-End Testing
**Source:** [guides/plugins/plugins/testing/end-to-end-testing.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/testing/end-to-end-testing.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# End-to-End Testing

## Overview

In end-to-end testing (E2E testing in short) real user workflows are simulated, whereby as many as possible functional areas and parts of the technology stack used in the application should be included. This way, we are able to put our UI under constant stress and ensure that Shopware's main functionalities are always working correctly.

## Prerequisites

To use Shopware E2E tests, at first you need to have a Shopware 6 installation running. Making sure, that your tests are reliable, you should have a clean installation. Cleanup means no categories, no products, no settings, nothing!

The easiest way to clean up your installation is the initialization. Using the command `composer run init` Shopware 6 gets initialized clean and without demo data. Installation of E2E dependencies can be accomplished separately by running `npm install` in the E2E folder you're using, e.g. for Shopware Administration it's `src/Administration/Resources/app/administration/test/e2e`.

Since our tests should run on an installation that is as close as possible to a release package, we use production mode. If you run the tests on a development environment, the test results may vary.

On top of that, please make sure your shop has a theme assigned. When using `composer run e2e:open` or `run`, this is done automatically.

This guide also won't teach you how to write Cypress tests in general. Please take a look at the official Cypress documentation for further guidance.

### Using our testsuite

The [E2E platform testsuite package](https://github.com/shopware/e2e-testsuite-platform) contains commands and helpers supporting you while building E2E tests for Shopware 6. On top of that, test data management and custom commands are included as well. More on that here: [Command reference](../../../../resources/references/core-reference/commands-reference).

This test suite is built on top of [Cypress](https://www.cypress.io/) as well as the following Cypress plugins:

* [cypress-select-tests](https://github.com/bahmutov/cypress-select-tests)
* [cypress-log-to-output](https://github.com/flotwig/cypress-log-to-output)
* [cypress-file-upload](https://github.com/abramenal/cypress-file-upload)

Here you can find the npm package of our testsuite:

Please have a look on our [cypress.json](https://github.com/shopware/e2e-testsuite-platform/blob/3.x/cypress.json), a few of our commands expect some configuration, e.g. viewportHeight and width, because the admin menu only opens if the viewport is wide enough.

## Setup steps

When you use our [Development template](https://github.com/shopware/development), we provide you some tooling scripts located in `dev-ops/e2e/actions`, to use E2E tests more comfortably.

The`composer` scripts to run our E2E tests in CLI or in Cypress' test runner are explained in the paragraph [Executing e2e tests](end-to-end-testing#executing-e2e-tests).

Depending on your environment (administration or storefront) please create the following folder structure:

```text
Resources
  `-- app
    `-- <environment>
      `-- test
        `-- e2e
          `-- cypress
            |-- fixtures
            |-- integration
            |-- plugins
            `-- support
```

We will cover the use of every folder in detail.

Within the folder `Resources/app/<environment>/test/e2e`, please run `npm init -y` to generate a `package.json` file. It is very convenient to place a script inside the newly created `package.json` to run the tests locally. Please add the following section to do so:

```javascript
"scripts": {
   "open": "node_modules/.bin/cypress open"
},
```

Now install this package with the following command:

```text
npm install @shopware-ag/e2e-testsuite-platform
```

As next step, please create a new file `e2e/cypress/plugins/index.js` with the following content:

```javascript
module.exports = require('@shopware-ag/e2e-testsuite-platform/cypress/plugins');
```

Finally, create a new file e2e/cypress/support/index.js with the following line:

```javascript
// Require test suite commands
require('@shopware-ag/e2e-testsuite-platform/cypress/support');
```

However, as we're using this image for running the test runner as well, you may need to do some configuration first. Based on this [guide](https://www.cypress.io/blog/2019/05/02/run-cypress-with-a-single-docker-command) you need to forward the XVFB messages from Cypress out of the Docker container into an X11 server running on the host machine. The guide shows an example for Mac; other operating systems might require different commands.

In case you're using Docker on Mac we have summarized the steps from the guide mentioned above, so you can follow these to prepare your environment to get the Test Runner up and running:

**Install and configure XQuartz**

Install XQuartz via [Homebrew](https://docs.brew.sh/Installation) or alternatively [download](https://www.xquartz.org/) it from the official homepage:

```bash
brew install --cask xquartz
```

Run XQuartz via CLI or open it from your Desktop:

```bash
open -a XQuartz
```

Got to `XQuartz > Preferences` (`⌘ + ,`) and enable `Allow connections from network clients`:

![XQuartz Preferences](../../../../assets/xquartz-allow-connections-from-network-clients.png)

::: warning
Restart your Mac before proceeding with the following steps.
:::

**Configure your environment**

Grab your IP address and save it to the environment variable `IP`:

```bash
IP=$(ipconfig getifaddr en0)
```

Depending on how you're connected you might have to use another interface instead of `en0`.

Now set the `DISPLAY` environment variable:

```bash
DISPLAY=$IP:0
```

Add `$IP` to xhost's ACL:

```bash
xhost + $IP
```

::: danger
It is **crucial** to set these environment variables in the **same terminal session** from where you will later run `psh e2e:open`!

Make sure that the `DISPLAY` environment variable on your Mac is properly set **before** you start the containers as it will be **passed** to the Cypress container when the container is **created**.
Updating the variable on your host won't update it in the container until it is re-created!
:::



## Executing E2E tests

If you want to run E2E tests in your plugin, just switch to the folder `Resources/app/<environment>/test/e2e` and execute the following command:

```bash
CYPRESS_baseUrl=<your-url> npm run open
```

`<your-url>` means the Storefront-URL of your Shopware environment.

It opens up the Cypress test runner which allows you to run and debug your tests, similar to the `e2e:open` command.

::: danger
Don't forget that you might need to adjust test cleanup and other environment-related things according to your plugin's setup.
:::

To prepare your shopware installation, your environment and install dependencies, please run the following command as first step, **outside** of your docker container:

```bash
 composer run e2e:setup
```

In our tests, we assume a clean shopware installation, so we strongly recommend to use `e2e:setup`. However, if your shopware installation is already clean and prepared, you can skip the preparation of your shopware installation by using the following command **inside** your docker container:

```bash
 composer run e2e:prepare
```

Afterwards, just use the following command outside of your container to run the Cypress Test Runner:

```bash
composer run e2e:open
```

If you want to run the tests in CLI, please use the following command outside your container:

```bash
composer e2e:cypress -- run --spec="cypress/e2e/administration/**/*.cy.js"
```

or

```bash
composer e2e:cypress -- run --spec="cypress/e2e/storefront/**/*.cy.js"
```

To see a complete overview on all psh scripts for e2e tests, feel free to refer to our [e2e command reference](../../../../resources/references/testing-reference/e2e-commands).



## Writing your first test

### Folder structure

In Shopware platform, you can find the tests in `src/Administration/Resources/app/administration/test/e2e`. There you can find the following folder structure, depending on your environment being Administration or Storefront:

```bash
`-- e2e
  `-- cypress
    |-- fixtures
        `-- example.json
    |-- integration
        `-- testfile.spec.js
    |-- plugins
        `-- index.js
    |-- support
        |-- commands.js
        `-- index.js
    |--cypress.json
    `--cypress.env.json
```

In the `cypress` folder, all test related folders are located. Most things will take place in these four folders:

* `fixtures`: Fixtures are used as external pieces of static data that can be used by your tests. You can use them

  with the `cy.fixture` command.

* `integration`: By default, the test files are located here. A file with the suffix "\*.spec.js" is a test file that

  contains a sequence of tests, performed in the order defined in it.

* `plugins`: Contains extensions or plugins. By default, Cypress will automatically include the plugins file before

  every single spec file it runs.

* `support`: The support folder is a great place to put reusable behavior such as custom commands or global overrides in,

  that you want to be applied and available to all of your spec files.

These two configuration files are important to mention as well:

* `cypress.json`
* `cypress.env.json`

  These are Cypress configuration files. If you need more information about them, take a look at the

  [Cypress configuration docs](https://docs.cypress.io/guides/references/configuration.html).

If you need to use this structure in a plugin, it is just the path to the `e2e` folder, which is slightly different. You can find the folder structure in the paragraph [Setup](end-to-end-testing#setup-steps).

If you want to contribute to Shopware platform's tests, please ensure to place your test in one of those folders:

```javascript
`-- integration
  |-- catalogue
  |-- content
  |-- customer
  |-- general
  |-- media-marketing
  |-- order
  |-- rule-product-stream
  `-- settings
```

::: warning
This is important because otherwise your test is not considered by our CI.
:::

### Test layout and syntax

Cypress tests are written in Javascript. If you worked with Mocha before, you will be familiar with Cypress' test layout. The test interface borrowed from Mocha provides `describe()`, `context()`, `it()` and `specify()`.

To have a frame surrounding your test and provide a nice way to keep your test organized, use `describe()` (or `context()` as its alias):

```javascript
describe('Test: This is my test file', () => {
    it('test something', () => {
        // This is your first test
    });
    it('tests something else', () => {
        // This is your second test
    });
});
```

The `it()` functions within the `describe()` function are your actual tests. Similar to `describe()` and `context()`, `it()` is identical to `specify()`. However, for writing Shopware tests we focus on `it()` to keep it consistent.

## Commands and assertions

In Cypress, you use commands and assertions to describe the workflow you want to test.

### Commands

Commands are the actions you need to do in order to interact with the elements of your application and reproduce the workflow to test in the end.

```javascript
it('test something', () => {
    ...
    cy.get('.sw-grid__row--0')
        .contains('A Set Name Snippet')
        .dblclick();
    cy.get('.sw-grid__row--0 input')
        .clear()
        .type('Nordfriesisch')
        .click();
    ...
    });
```

You can chain commands by passing its return value to the next one. These commands may contain extra steps to take, e.g. a `click` or `type` operation.

Cypress provides a lot of commands to represent a variety of steps a user could do. On top of that, our E2E testsuite contains a couple of [custom commands](../../../../resources/references/testing-reference/e2e-custom-commands) specially for Shopware.

### Assertions

Assertions describe the desired state of your elements, objects and application. Cypress bundles the Chai Assertion L

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/testing/end-to-end-testing.md


---

## Jest Unit Tests in Shopware's Administration
**Source:** [guides/plugins/plugins/testing/jest-admin.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/testing/jest-admin.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Jest Unit Tests in Shopware's Administration

## Overview

You should write a unit test for every functional change. It should guarantee that your written code works and that a third developer can't break the functionality with their code.

With a good test coverage we can have the confidence to deploy a stable software without needing to manually test the software in its entirety. This little guide will guide you how to write unit tests for the Administration in Shopware 6.

We are using [Jest](https://jestjs.io) as our testing framework. It's a solid foundation and widely used by many developers. Before you are reading this guide you have to make sure you understand the basics of unit tests and how Jest works.

## Video

Did you know that there's a video available to this topic? Please take a look:

## Prerequisites

This tutorial will have a strong focus on how unit tests should be written when it comes to components in the Administration. So please make sure you already know what a unit test is and why we are doing it. Furthermore, you should know what components tests are and what we want to achieve with them. You can find a good source for best practices in this Github repository:

In addition, you need a running Shopware 6 installation. Your repository used for that should be based on development template, as we need to use some scripts provided by it.

## Test file location

The test files are placed in the same directory as the file which should be tested.
The file name is the same with the suffix `.spec.js` or `spec.ts`.

## Testing services and ES modules

Services and isolated ECMAScript modules are well testable because you can import them directly without mocking or stubbing dependencies. A service can be used isolated and therefore is easy to test.

Let's have a look at an example:

```javascript
// sanitizer.helper.spec.js
import Sanitizer from 'src/core/helper/sanitizer.helper';

describe('core/helper/sanitizer.helper.js', () => {
    it('should sanitize the html', () => {
        expect(Sanitizer.sanitize('<A/hREf="j%0aavas%09cript%0a:%09con%0afirm%0d``">z'))
            .toBe('<a href="j%0aavas%09cript%0a:%09con%0afirm%0d``">z</a>');
    });

    it('should remove script functions from dom elements', () => {
        expect(Sanitizer.sanitize('<details open ontoggle=confirm()>'))
            .toBe('<details open=""></details>');
    });

    it('should remove script functions completely', () => {
        expect(Sanitizer.sanitize(`<script y="><">/*<script* */prompt()</script`))
            .toBe('');
    });

    it('should sanitize js in links', () => {
        expect(Sanitizer.sanitize('<a href=javas&#99;ript:alert(1)>click'))
            .toBe('<a>click</a>');
    });

    // ...more tests 
});
```

You see, you are able to write the test the same way you're used to, writing Jest unit tests in general.

## Write tests for components

After setting up your component test, you need to write your tests. A good way to write them is to test input and output. The most common tests are:

* set Vue Props and check if component looks correctly
* interact with the DOM and check if the desired behaviour is happening

However, when it comes to writing component tests for Shopware's Administration, there are some further steps to go. We will take a look at them in the following paragraphs.

## Setup for testing Vue components

We are using the [Vue Test Utils](https://vue-test-utils.vuejs.org) for easier testing of Vue components. If you don't have experience with testing Vue components it is useful to read some basic guides on this topic. The main part of testing components is similar in Shopware 6.

However, there are some important differences. We can't test components that easily like in other Vue projects because we are supporting template inheritance and extendability for third party developers. This causes overhead which we need to bear in mind.

We are using a global object as an interface for the whole Administration. Every component gets registered to this object, e.g. `Shopware.Component.register()`. Therefore, we have access to Component with the `Shopware.Component.build()` method. This creates a native Vue component with a working template. Every override and extension from another components are resolved in the built component.

## Setup tests with create test command

You can generate a test boilerplate using the create test command.
You encountered an untested component or service? Copy the path in your IDE and go to your terminal.
In the Shopware root directory run `composer run admin:create:test`. Once prompted paste the path you copied and hit enter.

If everything is correct you should now have a `.spec` file with our newest recommended boilerplate code.

### Executing tests

Before you are using the commands make sure that you installed all dependencies for your Administration. If you haven't done this already, then you can do it running the following PSH command: `composer run init:js`

In order to run jest unit tests of the Administration, you can use the psh commands provided by our development template.

::: info
This only applies to the Shopware provided Administration! If you use unit tests in your plugin, you might need to write your own scripts for that.
:::

This command executes all unit tests and shows you the complete code coverage.\
`composer run admin:unit`

This command executes only unit tests of changed files. It automatically restarts if a file gets saved. This should be used during the development of unit tests.\
`composer run admin:unit:watch`

### Example test structure

```typescript
import {shallowMount, createLocalVue, Wrapper} from '@vue/test-utils';
import flushPromises from 'flush-promises';

// add additional parameters to change options for the test
async function createWrapper(/* options = {} */): Wrapper {
    // add localVue only if needed
    const localVue = createLocalVue();

    // prefer shallowMount over normal mount
    return shallowMount(await Shopware.Component.build('sw-your-component-for-test'), {
        // localVue only if needed
        localVue,
        // add stubs for missing component
        stubs: {
            'sw-missing-component-one': Shopware.Component.build('sw-missing-component-one'),
            'sw-missing-component-two': Shopware.Component.build('sw-missing-component-two'),
        },
        mocks: {
            // add mocks if needed
        },
        // needed if you interact with elements
        attachTo: document.body,

        // ...options,
    });
}

describe('the/path/to/the/component', () => {
    let wrapper: Wrapper;

    beforeAll(async () => {
        // generate all needed mocks, etc.
    })

    beforeEach(async () => {
        // reset all mocks and state changes to default
        wrapper = await createWrapper();
        
        // wait for created hook etc.
        await flushPromises();
    })

    afterEach(async () => {
        // cleanup everything

        // destroy the existing wrapper
        if (wrapper) {
            await wrapper.destroy();
        }

        // wait until all promises are finished
        await flushPromises();
    })

    it('should be a Vue.js component', () => {
        expect(wrapper.vm).toBeTruthy();
    });

    // Add more component tests
})
```

## First example: Testing sw-multi-select component

For better understanding how to write component tests for Shopware 6 let's write a test. In our example we are using the component `sw-multi-select`.

When you want to mount your component it needs to be imported first:

```javascript
// test/app/component/form/select/base/sw-multi-select.spec.js
import 'src/app/component/form/select/base/sw-multi-select';
```

You see that we import the `sw-multi-select` without saving the return value. This blackbox import only executes code. However, this is important because this registers the component to the Shopware object:

```javascript
// src/app/component/form/select/base/sw-multi-select/index.js
Shopware.Component.register('sw-multi-select', {
    // The vue component
});
```

### Mounting components

In the next step we can mount our Vue component which we get from the global Shopware object:

```javascript
// test/app/component/form/select/base/sw-multi-select.spec.js
import 'src/app/component/form/select/base/sw-multi-select';

shallowMount(Shopware.Component.build('sw-multi-select'));
```

When we’re testing our vue.js components, we need a way to mount and render the component. Therefore, we use the following methods:

* `mount()`: Creates a Wrapper that contains the mounted and rendered Vue component.
* `shallowMount()`: Like mount, it creates a Wrapper that contains the mounted and rendered Vue component,

  but with stubbed child components.

This way, we create a new `wrapper` before each test. The `build` method resolves the twig template and returns a vue component.

### Test structure

Now you can test the component like any other component. Let's try to write our first test:

```javascript
// test/app/component/form/select/base/sw-multi-select.spec.js
import { shallowMount } from '@vue/test-utils';
import 'src/app/component/form/select/base/sw-multi-select';

describe('components/sw-multi-select', () => {
    let wrapper;

    beforeEach(() => {
        wrapper = shallowMount(Shopware.Component.build('sw-multi-select'));
    });

    afterEach(() => {
        wrapper.destroy();
    });

    it('should be a Vue.js component', () => {
        expect(wrapper.vm).toBeTruthy();
    });
});
```

This contains our component. In our first test we only check if the wrapper is a Vue instance.

### Running the test

Now let's start the watcher to see if the test works. You can do this using our PSH command `composer run admin:unit:watch`. You should see a result like this: `Test Suites: 1 passed, 1 total`. You should also see several warnings like this:

* `[Vue warn]: Missing required prop: "options"`
* `[Vue warn]: Missing required prop: "value"`
* `[Vue warn]: Unknown custom element: <sw-select-base> - did you register the component correctly? ...`

The first two warnings are solved easily by providing the required props to our shallowMount:

```javascript
wrapper = shallowMount(Shopware.Component.build('sw-multi-select'), {
    props: {
        options: [],
        value: ''
    }
});
```

Now you should only see the last warning with an unknown custom element. The reason for this is that most components contain other components. In our case the `sw-multi-select` needs the `sw-select-base` component. Now we have several solutions to solve this. The two most common ways are stubbing or using the component.

```javascript
// test/app/component/form/select/base/sw-multi-select.spec.js
import 'src/app/component/form/select/base/sw-select-base';

wrapper = shallowMount(Shopware.Component.build('sw-multi-select'), {
    props: {
        options: [],
        value: ''
    },
    stubs: {
        'sw-select-base': Shopware.Component.build('sw-select-base'),
    }
});
```

You need to choose which way is needed: Many tests do not need the real component, but in our case we need the real implementation. You will see that if we import another component that they can create also warnings. Let's look at the code that solve all warnings, then we should have a code like this:

```javascript
// test/app/component/form/select/base/sw-multi-select.spec.js
import { shallowMount } from '@vue/test-utils';
import 'src/app/component/form/select/base/sw-multi-select';
import 'src/app/component/form/select/base/sw-select-base';
import 'src/app/component/form/field-base/sw-block-field';
import 'src/app/component/form/field-base/sw-base-field';
import 'src/app/component/form/field-base/sw-field-error';
import 'src/app/component/form/select/base/sw-select-selection-list';
import 'src/app/component/form/select/base/sw-select-result-list';
import 'src/app/component/utils/sw-popover';
import 'src/app/comp

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/testing/jest-admin.md


---

## Jest Unit Tests in Shopware's Storefront
**Source:** [guides/plugins/plugins/testing/jest-storefront.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/testing/jest-storefront.md)  
*(Body truncated in this bundle; follow the link for the rest.)*

# Jest Unit Tests in Shopware's Storefront

## Overview

You should write a unit test for every functional change. Writing tests will ensure that your written code works and that another change can't break your code's functionality with their code.

With a good test coverage you gain confidence to deploy a stable software without the requirement to manually test every change. This little guide will guide you how to write unit tests for the Administration in Shopware 6.

We are using JestJS as our testing framework as it's a solid foundation and widely used by many developers.

## Prerequisites

Before you are reading this guide you have to make sure you understand the basics of unit tests and how Jest works. You can find a good source for best practices in this Github Repo:

In addition, you need a running Shopware 6 installation. Your repository used for that should be based on development template, as we will to use some scripts provided by it.

For one example, we use a Javascript plugin. In oder to follow this example, you need to know how to build a Javascript plugin in the first place. You can learn about it in the corresponding [guide](../storefront/add-custom-javascript).

## Test structure

::: warning
When it comes to the path to the test folder, you are quite free to use your own requirements. You could even build up a separate test suite if you need. There's one limitation though: Please take care you place your tests according your `package.json` file!
:::

The following configuration matches our core configuration in order to give you a starting point. In Shopware's platform repository, you will find the Storefront unit tests in the following directory: `platform/src/Storefront/Resources/app/storefront/test` It may be a good convention to resemble this directory structure, but it's no fixed requirement.

Inside the test directory, you add a test for a file in the same path as the source path. You see: When creating the file, the name should also be the same as the component has with an additional `test`.

The exact test folder structure looks like seen below, starting in `Storefront` bundle:

```bash
Resources
  `-- app
    `-- <environment>
      `-- test
        `-- plugin
          `-- <plugin-name>
            `-- js-plugin-test.spec.js
```

Please note that in this example, `<environment>` is a placeholder for the environment you are working in. In this context, that should be `storefront`.

## Writing a basic test

When writing jest unit tests in the Storefront, you will soon realize that it's not that much different from writing jest unit tests in general. Unlike the [Jest unit tests in the Administration](jest-admin), you basically don't need to go an extra mile to write your unit tests. Services, helper and isolated ECMAScript modules are well testable because you can import them directly without mocking or stubbing dependencies. They can be used isolated and therefore are easy to test.

Let's start from scratch with a simple example: Imagine we want to write a test for a helper class, e.g. the `feature.helper` of our Storefront, handling the feature flag usage. We want to test, if our feature helper can indeed handle active feature flags.

At first, you need to create your test file, e.g. `feature.helper.test.js`. With your new created test file, let's create the test structure for it:

```javascript
// <plugin root>/src/Resources/app/storefront/test/helper/feature.helper.test.js
// describe is meant for grouping and structure
describe('feature.helper.js', () => {

    // This is your actual test
    test('checks the flags', () => {
        // Assertions come here
    });
});
```

Now, let's fill this empty test with life. Our first step is importing the helper under test - the `feature.helper` class. However, there one more step to be done for preparation.

```javascript
// <plugin root>/src/Resources/app/storefront/test/helper/feature.helper.test.js
// Import for the helper to test
import Feature from 'src/helper/feature.helper';

describe('feature.helper.js', () => {
    test('checks the flags', () => {
        // Assertions come here
    });
});
```

In order to be able to test our feature flag integration, we of course need some fixtures to be present - some active and inactive feature flags. So we need to ensure their presence before running the tests, ideally in a setup step. As you might know from other frameworks, it's convenient to use [lifecycle hooks](https://jestjs.io/docs/en/setup-teardown) for that purpose.

To sum it up, we need a feature flag fixture and the implementation of it in the `beforeEach` hook of our test. In our example, that looks like below:

```javascript
// <plugin root>/src/Resources/app/storefront/test/helper/feature.helper.test.js
import Feature from 'src/helper/feature.helper';

// One flag should be active, the other shouldn't.
const default_flags = {
    test1: true,
    test2: false
};

describe('feature.helper.js', () => {

    // This hook is executed before every test
    beforeEach(() => {
        // Applying the flag fixture
        Feature.init(default_flags);
    });

    test('checks the flags', () => {
        // Assertions come here
    });
});
```

Alright, let's get to the point now, writing the actual test. Remember we want to make sure we have active and inactive feature flags. In addition, it may be useful to check the behavior if a third, non-existent feature flag is introduced. Using [Jest's matchers](https://jestjs.io/docs/en/using-matchers) for these assertions, we get the following test:

```javascript
// <plugin root>/src/Resources/app/storefront/test/helper/feature.helper.test.js
import Feature from 'src/helper/feature.helper';

const default_flags = {
    test1: true,
    test2: false
};

describe('feature.helper.js', () => {
    beforeEach(() => {
        Feature.init(default_flags);
    });

    test('checks the flags', () => {
        expect(Feature.isActive('test1')).toBeTruthy();
        expect(Feature.isActive('test2')).toBeFalsy();
        expect(Feature.isActive('test3')).toBeFalsy();
    });
});
```

That's basically it! We wrote our first jest unit test in the Storefront.

## Executing the tests

Before you are using the commands make sure that you installed all dependencies for your Storefront. If you haven't done this already, then you can do it running the following PSH command:

```bash
> composer run build:js:storefront
```

In order to run jest unit tests of the Storefront, you can use the psh commands provided by our development template. This command executes all unit tests and shows you the complete code coverage.

```bash
> composer run storefront:unit
```

::: info
This only applies to the Shopware provided Storefront! If you use unit tests in your Plugin, you might need to write your own scripts for that.
:::

## Mocking JavaScript plugins

Now, let's have a look at a intermediate example: As you're writing JavaScript plugins, you may want to test those. As you need to mock some things in this case, this kind of test might be a bit more complex.

::: info
The folder structure, and the corresponding file locations of the following example will resemble the one used in `platform` repository.
:::

Let's start with the plugin we want to test later. For the sake of simplicity, we will use a plugin which returns "Hello world":

```javascript
// <plugin root>/src/Resources/app/storefront/src/plugin/hello-world/hello-world.plugin.js
import Plugin from 'src/plugin-system/plugin.class'

export default class HelloWorldPlugin extends Plugin {
    static options = {};

    init() {
        console.log('Hello World!', this.el);
    }

    sayHello() {
        return "Hello World!"
    }
}
```

Of course, you need to make sure that your plugin is registered, more details in the guide on [Javascript plugins](../storefront/add-custom-javascript).

In the beginning, writing plugin tests is still similar to other jest unit tests: You import your plugin's class and use the familiar test structure:

```javascript
// <plugin root>/src/Resources/app/storefront/test/plugin/hello-world/hello-world.plugin.test.js
/**
 * @jest-environment jsdom
 */

// import your plugin here
import HelloWorldPlugin from 'src/plugin/hello-world/hello-world.plugin';

describe('HelloWorldPlugin tests', () => {

    beforeEach(() => {
        // Here we need to do all the mocking
    });

    afterEach(() => {
        // Teardown
    });

    test('custom plugin exists', () => {
        // your actual test
    });
});
```

You might notice the lifecycle hook we use in this test. These will be important in the next steps where we begin to mock our plugin and clean it up after our tests.

The `beforeEach` hook will be executed before each test. Thus, it's the perfect location for creating our plugin under test. Therefore, we need to get an element first. We'll use it to create our plugin - resembling the usage of a plugin on an element.

```javascript
// <plugin root>/src/Resources/app/storefront/test/plugin/hello-world/hello-world.plugin.test.js
/**
 * @jest-environment jsdom
 */

import HelloWorldPlugin from 'src/plugin/hello-world/hello-world.plugin';

describe('HelloWorldPlugin tests', () => {

    // Definition of plugin
    let plugin;

    beforeEach(() => {
        // you need to get an element for the plugin
        const mockedElement = document.createElement('div');
        plugin = new HelloWorldPlugin(mockedElement);

    });

    afterEach(() => {
        // Teardown
    });

    test('custom plugin exists', () => {
        // your actual test, temporary filled with a placeholder
        console.log(plugin);
    });
});
```

If you execute your test now, you'll run into an error:

```bash
      HelloWorldPlugin tests
        ✕ custom plugin exists (32ms)

      ● HelloWorldPlugin tests › custom plugin exists

        TypeError: Cannot read property 'getPluginInstancesFromElement' of undefined

          119 |      */
          120 |     _registerInstance() {
        > 121 |         const elementPluginInstances = window.PluginManager.getPluginInstancesFromElement(this.el);
              |                                                             ^
          122 |         elementPluginInstances.set(this._pluginName, this);
          123 |
          124 |         const plugin = window.PluginManager.getPlugin(this._pluginName, false);
```

This was to be expected because you need to mock some more things required for the plugin to run. To solve this issue, you need to mock the `PluginManager` which holds all plugin instances globally in the Storefront. Because our test is just testing the single plugin class, the actual implementation on the real DOM element in the Storefront isn't too important at this moment.

```javascript
// <plugin root>/src/Resources/app/storefront/test/plugin/hello-world/hello-world.plugin.test.js
/**
 * @jest-environment jsdom
 */

import HelloWorldPlugin from 'src/plugin/hello-world/hello-world.plugin';

describe('HelloWorldPlugin tests', () => {
    let plugin;

    beforeEach(() => {

        // Mocking PluginManager to get the plugin working
        window.PluginManager = {
            getPluginInstancesFromElement: () => {
                return new Map();
            },
            getPlugin: () => {
                return {
                    get: () => []
                };
            }
        };

        const mockedElement = document.createElement('div');
        plugin = new HelloWorldPlugin(mockedElement);
    });

    afterEach(() => {
        // Set your plugin to null to clean up afterwards
        plugin = null;
    });

    test('custom plugin exists', () => {
        // your actual test, temporary filled with a placeholder
        console.log(plugin);
    });
});
```

::: warning
Don't forget the cleanup after each test! You need to set your plugin to `null` in your `afterEach` hook to ensure an isolated test.
:::

Finally, we're ready to write our actual

… **Truncated.** Full document: https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/testing/jest-storefront.md


---

## PHP Unit Testing
**Source:** [guides/plugins/plugins/testing/php-unit.md](https://developer.shopware.com/docs/v6.6/guides/plugins/plugins/testing/php-unit.md)  
# PHP Unit Testing

## Overview

This guide will cover the creation of PHPUnit tests in Shopware 6. Refer to the [official PHPUnit documentation](https://phpunit.de/documentation.html) for a deep dive into PHP unit testing.

## Prerequisites

In order to create tests for a plugin, you need a plugin as a base. Refer to the [Plugin Base Guide](../plugin-base-guide) for more information.

Furthermore, have a look at our [Execute database queries/migrations](../plugin-fundamentals/database-migrations) guide since this guide will show you how to create a migration test for these examples.

## PHPUnit configuration

First, to configure PHPUnit, create a file called `phpunit.xml` in the root directory of the plugin. To get more familiar with the configurable options, refer to the [PHPUnit documentation](https://phpunit.readthedocs.io/en/8.5/configuration.html). This example explains configuring PHPUnit to search in the directories `<plugin root>/src/Test` and `<plugin root>/src/Migration/Test` for your tests.

The `phpunit.xml` can be autogenerated for you with the `bin/console plugin:create` command:

```xml
// <plugin root>/phpunit.xml
<?xml version="1.0" encoding="UTF-8"?>
<phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="https://schema.phpunit.de/9.3/phpunit.xsd"
         bootstrap="tests/TestBootstrap.php"
         executionOrder="random">
    <coverage>
        <include>
            <directory>./src/</directory>
        </include>
    </coverage>
    <php>
        <ini name="error_reporting" value="-1"/>
        <server name="KERNEL_CLASS" value="Shopware\Core\Kernel"/>
        <env name="APP_ENV" value="test"/>
        <env name="APP_DEBUG" value="1"/>
        <env name="SYMFONY_DEPRECATIONS_HELPER" value="weak"/>
    </php>
    <testsuites>
        <testsuite name="migration">
            <directory>Migration/Test</directory>
        </testsuite>
    
        <testsuite name="Example Testsuite">
            <directory>Test</directory>
        </testsuite>
    </testsuites>
</phpunit>
```

This command will also generate a `TestBootstrap.php` file:

```php
// <plugin root>/tests/TestBootstrap.php
<?php declare(strict_types=1);

use Shopware\Core\TestBootstrapper;

$loader = (new TestBootstrapper())
    ->addCallingPlugin()
    ->addActivePlugins('BasicExample')
    ->setForceInstallPlugins(true)
    ->bootstrap()
    ->getClassLoader();

$loader->addPsr4('Swag\\BasicExample\\Tests\\', __DIR__);
```

The `setForceInstallPlugins` method ensures that your plugin is installed and active even the test database was already build beforehand.

## Example Tests

### Integration test

After PHPUnit is configured, a first test can be written. In this example, a test simply tries to instantiate every `.php` class to see if any used core classes are missing. In the test, you use the `IntegrationTestBehaviour` trait, which comes with some handy features, such as automatically setting up a database transaction or clearing the cache before starting tests.
This is how your test could look like:

```php
// <plugin root>/src/Test/UsedClassesAvailableTest.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Test;

use PHPUnit\Framework\TestCase;
use Shopware\Core\Framework\Test\TestCaseBase\IntegrationTestBehaviour;
use Symfony\Component\Finder\Finder;

class UsedClassesAvailableTest extends TestCase
{
    use IntegrationTestBehaviour;

    public function testClassesAreInstantiable(): void
    {
        $namespace = str_replace('\Test', '', __NAMESPACE__);

        foreach ($this->getPluginClasses() as $class) {
            $classRelativePath = str_replace(['.php', '/'], ['', '\\'], $class->getRelativePathname());

            $this->getMockBuilder($namespace . '\\' . $classRelativePath)
                ->disableOriginalConstructor()
                ->getMock();
        }

        // Nothing broke so far, classes seem to be instantiable
        $this->assertTrue(true);
    }

    private function getPluginClasses(): Finder
    {
        $finder = new Finder();
        $finder->in(realpath(__DIR__ . '/../'));
        $finder->exclude('Test');
        return $finder->files()->name('*.php');
    }
}
```

### Migration test

In order to test the example migration `Migration1611740369ExampleDescription`, create a new test called `Migration1611740369ExampleDescriptionTest`, which extends from the PHPUnit `TestCase`. Use the `KernelTestBehaviour` trait because a database connection from the container is needed.

This is an example for a migration test:

```php
// <plugin root>/src/Migration/Test/Migration1611740369ExampleDescriptionTest.php
<?php declare(strict_types=1);

namespace Swag\BasicExample\Migration\Test;

use Doctrine\DBAL\Connection;
use PHPUnit\Framework\TestCase;
use Shopware\Core\Framework\Test\TestCaseBase\KernelTestBehaviour;

class Migration1611740369ExampleDescriptionTest extends TestCase
{
    use KernelTestBehaviour;

    public function testNoChanges(): void
    {
        /** @var Connection $conn */
        $conn = $this->getContainer()->get(Connection::class);
        $expectedSchema = $conn->fetchAssoc('SHOW CREATE TABLE `swag_basic_example_general_settings`')['Create Table'];

        $migration = new Migration1611740369ExampleDescription();

        $migration->update($conn);
        $actualSchema = $conn->fetchAssoc('SHOW CREATE TABLE `swag_basic_example_general_settings`')['Create Table'];
        static::assertSame($expectedSchema, $actualSchema, 'Schema changed!. Run init again to have clean state');

        $migration->updateDestructive($conn);
        $actualSchema = $conn->fetchAssoc('SHOW CREATE TABLE `swag_basic_example_general_settings`')['Create Table'];
        static::assertSame($expectedSchema, $actualSchema, 'Schema changed!. Run init again to have clean state');
    }

    public function testNoTable(): void
    {
        /** @var Connection $conn */
        $conn = $this->getContainer()->get(Connection::class);
        $conn->executeStatement('DROP TABLE `swag_basic_example_general_settings`');

        $migration = new Migration1611740369ExampleDescription();
        $migration->update($conn);
        $exists = $conn->fetchColumn('SELECT COUNT(*) FROM `swag_basic_example_general_settings`') !== false;

        static::assertTrue($exists);
    }
}
```

## Mocking services

In some cases a service should behave differently in a test run. Such a case could be where a service deletes a file or makes a critical api call. To avoid this in a test run it is possible to create a `<plugin root>/Resources/config/services_test.{xml|yml}` file which will override your `<plugin root>/Resources/config/services.{xml|yml}`. But only for the test environment.

In this test-only service config you can override arguments, aliases or parameters to change what the service container injects into services during a test run.

## Executing the test

To execute tests, a PHPUnit binary is necessary, which is most likely located in the `vendor/bin` folder. The command below will use the `phpunit.xml` file in the `custom/plugins/SwagBasicExample` folder and execute the testsuite with the name `migration`.

```sh
// <project root>ell
./vendor/bin/phpunit --configuration="custom/plugins/SwagBasicExample" --testsuite "migration"
```

### Executing all tests in the plugin

If no testsuite is passed, it will execute all testsuites.

```shell
./vendor/bin/phpunit --configuration="custom/plugins/SwagBasicExample"
```

### Executing a single class or method

To execute a specific test class or method of a testsuite, pass the argument `--filter` with the name of the class or method.

```shell
./vendor/bin/phpunit --configuration="custom/plugins/SwagBasicExample" --filter testNoChanges
./vendor/bin/phpunit --configuration="custom/plugins/SwagBasicExample" --filter Migration1611740369ExampleDescriptionTest
```

## Flex template

In order to run PHPunit tests install the flex template [dev-tools](../../../../guides/installation/template.md#how-do-i-migrate-from-production-template-to-symfony-flex) package via composer.

```shell
composer require --dev dev-tools
```

## Next steps

Running unit tests with javascript code is explained in the following two articles:

* [Jest unit tests in Shopware's Administration](jest-admin)
* [Jest unit tests in Shopware's Storefront](jest-storefront)

---

---

## Shopware Acceptance Test Suite: Playwright
**Source:** [guides/plugins/plugins/testing/playwright.md](https://developer.shopware.com/docs/guides/plugins/plugins/testing/playwright.md)  
# Shopware Acceptance Test Suite: Playwright

[Playwright](https://playwright.dev/) is a powerful tool for end-to-end testing of web applications. It allows you to automate browser interactions, making it ideal for testing the functionality of your [Shopware](https://github.com/shopware/shopware) plugins and themes.

It provides several useful Playwright [fixtures](https://playwright.dev/docs/test-fixtures) to start testing with Shopware right away, including page contexts and [page objects](https://playwright.dev/docs/pom) for Storefront and Administration, API clients, test data creation, and reusable test logic.

---

---

## Actor pattern
**Source:** [guides/plugins/plugins/testing/playwright/actor-pattern.md](https://developer.shopware.com/docs/guides/plugins/plugins/testing/playwright/actor-pattern.md)  
# Actor pattern

The actor pattern is a basic concept that we added to our test suite. It is something not related to Playwright, but similar concepts exist in other testing frameworks. We implemented it to create reusable test logic that can be used in a human-readable form, without abstracting away Playwright as a framework. So you are free to use it or not. Any standard Playwright functionality will still be usable in your tests.

The concept adds two new entities besides the already mentioned [page objects](./page-object.md)

* **Actor**: A specific user with a given context performing actions (tasks) inside the application.
* **Task**: A specific action performed by an actor.
* **Pages**: A page of the application on which an actor performs a task.

## Actors

The Actor class is a lightweight solution to simplify the execution of reusable test logic or navigate to a specific page.

## Properties

* `name`: The human-readable name of the actor.
* `page`: A Playwright page context that the actor is navigating.

## Primary methods

* `goesTo`: Accepts a URL of a page the actor should navigate to.
* `attemptsTo`: Accepts a "task" function with reusable test logic that the actor should perform.
* `expects`: A one-to-one export of the Playwright `expect` method to use it in the actor pattern.

These methods lead to the following pattern:

* The **actor** *goes to* a **page**.
* The **actor** *attempts to* perform a certain **task**.
* The **actor** *expects* a certain result.

Translated into test code, this pattern can look like this:

```typescript
import { test } from "./../BaseTestFile";

test("Product detail test scenario", async ({
  ShopCustomer,
  StorefrontProductDetail,
  TestDataService,
}) => {
  const product = await TestDataService.createBasicProduct();

  await ShopCustomer.goesTo(StorefrontProductDetail.url(product));
  await ShopCustomer.attemptsTo(AddProductToCart(product));
  await ShopCustomer.expects(
    StorefrontProductDetail.offCanvasSummaryTotalPrice
  ).toHaveText("€99.99*");
});
```

In this example, you can see that this pattern creates very comprehensible tests, even for non-tech people. They also make it easier to abstract simple test logic that might be used in different scenarios into executable tasks, like adding a product to the cart.

The test suite offers two different actors by default:

* `ShopCustomer`: A user that is navigating the Storefront.
* `ShopAdmin`: A user who manages Shopware via the Administration.

## Accessibility methods

* `a11y_checks`: Accepts a locator and verifies if the desired locator is both focused and displays a visible focus indicator. This is automatically called via `presses`, `fillsIn`, and `selectsRadioButton`.
* `presses`: An extension of the Playwright `press` method to include `a11y_checks` as well as automatically apply a keyboard key press per default browser keyboard mappings (which can also be overridden). A keyboard focused alternative to the Playwright `click` method.
* `fillsIn`: An extension of the Playwright `fill` method to include `a11y_checks`.
* `selectsRadioButton`: Selects radio buttons using keyboard navigation in addition to verifying visible focus (via `presses`).

These methods serve as a way to enforce better accessibility practices by using keyboard navigation and checking for visible focus indicators (both of which are WCAG requirements). They can be used both in tests and tasks.

:::info
Be aware that the Playwright `click` method automatically includes a number of [actionability checks](https://playwright.dev/docs/actionability) to combat flakiness. When utilizing the Actor accessibility methods, you may need to adjust your tests to individually assert some of these actionability checks for certain locators yourself.
:::

## Tasks

Tasks are small chunks of reusable test logic that can be passed to the `attemptsTo` method of an actor. They are created via Playwright fixtures and have access to the same dependencies. Every executed task will automatically be wrapped in a test step of Playwright, so you get nicely structured reports of your tests.

**Basic Example**

```typescript
import { test as base } from "@playwright/test";
import type { Task } from "../../../types/Task";
import type { FixtureTypes } from "../../../types/FixtureTypes";
import type { Customer } from "../../../types/ShopwareTypes";

export const Login = base.extend<{ Login: Task }, FixtureTypes>({
  Login: async (
    {
      ShopCustomer,
      DefaultSalesChannel,
      StorefrontAccountLogin,
      StorefrontAccount,
    },
    use
  ) => {
    const task = (customCustomer?: Customer) => {
      return async function Login() {
        const customer = customCustomer
          ? customCustomer
          : DefaultSalesChannel.customer;

        await ShopCustomer.goesTo(StorefrontAccountLogin.url());

        await ShopCustomer.fillsIn(
          StorefrontAccountLogin.emailInput,
          customer.email
        );
        await ShopCustomer.fillsIn(
          StorefrontAccountLogin.passwordInput,
          customer.password
        );
        await ShopCustomer.presses(StorefrontAccountLogin.loginButton);

        await ShopCustomer.expects(
          StorefrontAccount.personalDataCardTitle
        ).toBeVisible();
      };
    };

    await use(task);
  },
});
```

This fixture is the "Login" task and performs a simple Storefront login of the default customer via keyboard navigation (automatically includes `a11y_checks` assertions). Every time we need a logged-in shop customer, we can simply reuse this logic in our test.

```typescript
import { test } from "./../BaseTestFile";

test("Customer login test scenario", async ({ ShopCustomer, Login }) => {
  await ShopCustomer.attemptsTo(Login());
});
```

To keep tests easily readable, use names for your tasks so that in the test itself, the code line resembles the `Actor.attemptsTo(doSomething)` pattern as closely as possible.

```typescript
// Bad example
await ShopCustomer.attemptsTo(ProductCart);

// Better example
await ShopCustomer.attemptsTo(PutProductIntoCart);
```

**Page Object Model Example**

```typescript
import type { Page, Locator } from "playwright-core";
import type { PageObject } from "../../types/PageObject";

export class CheckoutConfirm implements PageObject {
  public readonly paymentMethodRadioGroup: Locator;
  public readonly page: Page;

  constructor(page: Page) {
    this.page = page;
    this.paymentMethodRadioGroup = page.locator(".checkout-card", {
      hasText: "Payment Method",
    });
  }

  url() {
    return "checkout/confirm";
  }
}
```

This page object defines the payment method radio group locator.

```typescript
import { test as base } from "@playwright/test";
import type { Task } from "../../../types/Task";
import type { FixtureTypes } from "../../../types/FixtureTypes";

export const SelectPaymentMethod = base.extend<
  { SelectPaymentMethod: Task },
  FixtureTypes
>({
  SelectPaymentMethod: async (
    { ShopCustomer, StorefrontCheckoutConfirm },
    use
  ) => {
    const task = (paymentOptionName: string) => {
      return async function SelectPaymentMethod() {
        const paymentMethods =
          StorefrontCheckoutConfirm.paymentMethodRadioGroup;
        const paymentOptionRadioButton = paymentMethods.getByRole("radio", {
          name: paymentOptionName,
        });

        await ShopCustomer.selectsRadioButton(
          paymentMethods,
          paymentOptionName
        );
        await ShopCustomer.expects(paymentOptionRadioButton).toBeChecked();
      };
    };

    await use(task);
  },
});
```

This fixture is the "SelectPaymentMethod" task, which selects the desired radio button in the `paymentMethodRadioGroup` defined in the page object using keyboard navigation (automatically includes `a11y_checks` assertions).

To use "SelectPaymentMethod" in a test, you simply pass the name of the desired payment option. Here is a sample scenario for a successful checkout that demonstrates how to combine multiple tasks to build your test scenarios.

```typescript
import { test } from "./../BaseTestFile";

test("Customer successfully orders product", async ({
  ShopCustomer,
  TestDataService,
  Login,
  StorefrontProductDetail,
  AddProductToCart,
  ProceedFromProductToCheckout,
  SelectPaymentMethod,
  ConfirmOrder,
}) => {
  const product = await TestDataService.createBasicProduct();
  await ShopCustomer.attemptsTo(Login());
  await ShopCustomer.goesTo(StorefrontProductDetail.url(product));
  await ShopCustomer.attemptsTo(AddProductToCart(product));
  await ShopCustomer.attemptsTo(ProceedFromProductToCheckout());
  await ShopCustomer.attemptsTo(SelectPaymentMethod("Invoice"));
  await ShopCustomer.attemptsTo(ConfirmOrder());
});
```

You can create your tasks in the same way to make them available for the actor pattern. Every task is just a simple Playwright fixture containing a function call with the corresponding test logic. Make sure to merge your task fixtures with other fixtures you created in your base test file. You can use the `mergeTests` method of Playwright to combine several fixtures into one test extension. Use `/src/tasks/shop-customer-tasks.ts` or `/src/tasks/shop-admin-tasks.ts` for that.

---

---

## Best practices
**Source:** [guides/plugins/plugins/testing/playwright/best-practices.md](https://developer.shopware.com/docs/guides/plugins/plugins/testing/playwright/best-practices.md)  
# Best practices

A good first read about this is the official [playwright best practices page](https://playwright.dev/docs/best-practices). It outlines the essential practices to follow when writing acceptance tests for Shopware.

The most important part is [test isolation](https://playwright.dev/docs/best-practices#make-tests-as-isolated-as-possible), which helps to prevent flaky behavior and enables the test to be run in parallel and on systems with an unknown state.

## Dos

* Use the [`TestDataService`](https://github.com/shopware/acceptance-test-suite/blob/trunk/src/services/TestDataService.ts) for creating test data
* Create all the data that is required for your test case. That includes sales channels, customers, and users (the page fixtures handle most of the common use cases)
* Clean it up if you don't need it anymore. The `TestDataService` will take care of it if you used it to create the test data
* If you need specific settings for your test, set them explicitly for the `user/customer/sales` channel
* Directly jump to the detail pages with the ID of the entities you have created. If that is not possible, use the search with a unique name to filter lists to just that single entity
* If you need to skip tests, comment any relevant github issues as part of the skip method: `test.skip('Blocked by https://[...])`

## Don'ts

* Do not expect lists/tables only to contain one item; leverage unique IDs/names to open or find your entity instead
* Same with helper functions, do not expect only to get one item back from the API. Always use unique criteria for the API call
* Avoid unused fixtures. If you request a fixture but don't use any data from the fixture, the test or fixture should be refactored
* Do not depend on implicit configuration and existing data. Examples:
  * rules
  * flows
  * categories
* Do not expect the shop to have the defaults `en_GB` and `EUR`
* Do not change global settings (sales channel is ok, because we created it). Everything in "Settings" that is not specific to a sales channel (tax, search, etc.)

## Sensitive Data / Credentials

Sometimes you have to provide sensitive data or credentials for your tests to run, for example, credentials for a sandbox environment for a payment provider. Apart from avoiding having those credentials in the actual code, you should also prevent them from appearing in logs or traces. To achieve this, you should outsource steps involving sensitive data to a separate project that runs before the actual test project and disable traces for it.

**Example**

```Typescript
projects: [
    // Init project using sensitive data
 {
      name: 'init', 
      testMatch: /.*\.init\.ts/,
      use : {trace : 'off'}
 },

 {
      // actual test project
      // [...]
      dependencies: ['init'],
 }]
```

## Debugging API calls

Debugging API calls may not be an easy task at first glance, because if the call you made returns an error, it is not directly visible to you. But you can use the `errors[]` array of the response and log that on the console.

**Example**

```Typescript
const response = await this.AdminApiClient.post('some/route', {
    data: {
        limit: 1,
        filter: [
 {
                type: 'equals',
                field: 'someField',
                value: 'someValue',
 },
 ],
 },
});
const responseData = await response.json();
console.log(responseData.errors[0]);
```

## Code contribution

You can contribute to this project via its [official repository](https://github.com/shopware/acceptance-test-suite/) on GitHub.

This project uses [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/). Make sure to form your commits accordingly to the spec.

---

---

## Deployment Process
**Source:** [guides/plugins/plugins/testing/playwright/deployment.md](https://developer.shopware.com/docs/guides/plugins/plugins/testing/playwright/deployment.md)  
# Deployment Process

To deploy a new version of the ATS, follow the steps below:

1. **Create a Pull Request**\
   Open a new pull request with your changes. Ensure that all commits follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification to support automated versioning and changelog generation.

2. **Approval and Merge**\
   Once the pull request has been reviewed and approved, merge it into the main branch.

3. **Automated Deployment PR Creation**\
   After the merge, the [`release-please`](https://github.com/googleapis/release-please) tool will automatically open a new pull request. This deployment PR will include version bumps and a generated changelog.

4. **Review and Approve the Deployment PR**\
   The deployment pull request requires an additional approval before it can be merged.

5. **Merge the Deployment PR**\
   Once the deployment PR is approved and merged, a new release of the ATS will be created in the GitHub repository. This action will also publish a new package version to NPM under [@shopware-ag/acceptance-test-suite](https://www.npmjs.com/package/@shopware-ag/acceptance-test-suite).

6. **Use the New Version**\
   After a short delay, the newly published version will be available on NPM. You can then reference it in your project folders as needed.

## Troubleshooting

If you encounter any issues with the automated deployment process, please check the following [troubleshooting page of release-please](https://github.com/googleapis/release-please?tab=readme-ov-file#release-please-bot-does-not-create-a-release-pr-why).

In most cases, the problem is related to the commit messages not following the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification. Make sure to check your commit messages and rebase your branch if necessary. If your PR is merged with a commit message that does not follow the specification, you can do the following:

* **Create an empty commit to the main branch**

  ```bash
      git commit --allow-empty -m "chore: release 2.0.0" -m "Release-As: 2.0.0"
  ```

  When a commit to the main branch has Release-As: x.x.x (case-insensitive) in the commit body, Release Please will open a new pull request for the specified version.

* **Push the changes**

  ```bash
    git push origin <your-branch>
  ```

* **Adjust the release notes** Remember to adjust the release notes in the deployment PR.

---

---

## General fixtures
**Source:** [guides/plugins/plugins/testing/playwright/fixtures.md](https://developer.shopware.com/docs/guides/plugins/plugins/testing/playwright/fixtures.md)  
# General fixtures

## DefaultSalesChannel

We try to encapsulate test execution within the system under test and make tests as deterministic as possible. The idea is to create a separate sales channel for testing purposes within the standard Storefront. The `DefaultSalesChannel` fixture is worker-scoped and is there to achieve exactly that. Using it will provide you with a new sales channel with default settings, including a default Storefront customer.

### Properties

* `salesChannel`: The Shopware sales channel reference.
* `customer`: A default Storefront customer reference.
* `url`: The url to the sales channel Storefront.

## AdminApiContext

This context provides a ready-to-use client for the Admin-API of Shopware. It is based on the standard Playwright [APIRequestContext](https://playwright.dev/docs/api/class-apirequestcontext), but will handle authentication for you, so you can start making API requests to the Shopware instance under test right away. You can use it, for example, for test data creation or API testing. Learn more about the usage of the Shopware Admin-API in the [API documentation](https://shopware.stoplight.io/docs/admin-api/twpxvnspkg3yu-quick-start-guide).

### Methods

* `get`
* `post`
* `patch`
* `delete`
* `fetch`
* `head`

### Usage

```TypeScript
import { test, expect } from './../BaseTestFile';

test('Property group test scenario', async ({ AdminApiContext }) => {

    const response = await AdminApiContext.post('property-group?_response=1', {
        data: {
            name: 'Size',
            description: 'Size',
            displayType: 'text',
            sortingType: 'name',
            options: [{
                name: 'Small',
 }, {
                name: 'Medium',
 }, {
                name: 'Large',
 }],
 },
 });

    expect(response.ok()).toBeTruthy();
});
```

## StoreApiContext

This context provides a ready-to-use client for the Store-API of Shopware and is based on the standard Playwright [APIRequestContext](https://playwright.dev/docs/api/class-apirequestcontext). You can do API calls on behalf of a Storefront user. Learn more about the usage of the Shopware Store-API in the [documentation](https://shopware.stoplight.io/docs/store-api/38777d33d92dc-quick-start-guide).

Note that, other than the AdminApiContext, the StoreApiContext won't do an automated login of the shop customer. This is because a Storefront user isn't always a registered user by default, and you might want to test this behaviour explicitly. You can use the `login` method to log in as a registered shop customer.

### Methods

* `login(user)`: Does a login of a customer and stores the login state for future requests.
* `get`
* `post`
* `patch`
* `delete`
* `fetch`
* `head`

### Usage

```TypeScript
import { test, expect } from './../BaseTestFile';

test('Store customer test scenario', async ({ StoreApiContext, DefaultSalesChannel }) => {

    // Login as the default customer.
    await StoreApiContext.login(DefaultSalesChannel.customer);

    // Create a new cart for the customer.
    const response = await StoreApiContext.post('checkout/cart', {
        data: { name: 'default-customer-cart' },
 });

    expect(response.ok()).toBeTruthy();
});
```

## AdminPage

This fixture provides a Playwright [page](https://playwright.dev/docs/api/class-page) context for the Shopware Administration. It creates a new admin user with an authenticated session. You can start testing within the Administration using this page right away.

### Usage

```TypeScript
import { test, expect } from './../BaseTestFile';

test('Shopware admin test scenario', async ({ AdminPage }) => {

    await AdminPage.goto('#/sw/product/index');
    await expect(AdminPage.locator('.sw-product-list__add-physical-button')).toBeVisible();
});
```

Note that this is just a very rough example. In most cases, you won't use this page context directly, but maybe a [page-object](#page-objects) using this page.

## StorefrontPage

This fixture provides a Playwright [page](https://playwright.dev/docs/api/class-page) context for the Shopware Storefront of the default sales channel.

## Add new fixtures

To add new general fixtures, create them inside the `src/fixtures` folder. Keep in mind that you need to merge your new fixture inside the `/src/index.ts` file.

---

---

## Overview
**Source:** [guides/plugins/plugins/testing/playwright/install-configure.md](https://developer.shopware.com/docs/guides/plugins/plugins/testing/playwright/install-configure.md)  
# Overview

This is a setup guide for the Shopware Acceptance Test Suite (ATS). This section will walk you through initializing a Playwright project, installing the ATS package, and configuring the environment for local testing. Whether you are writing new tests or running existing ones, following these steps ensures your environment is correctly prepared.

## Installation

Start by creating your own [Playwright](https://playwright.dev/docs/intro) project.

```shell
npm init playwright@latest
```

Add the package for the Shopware ATS to your project.

```shell
npm install @shopware-ag/acceptance-test-suite
```

Make sure to install Playwright and its dependencies.

```shell
npm install
npx playwright install
npx playwright install-deps
```

## Configuration

The test suite is designed to test against any Shopware instance with pure API usage. To grant access to the instance under test, you can use the following environment variables. You can choose between two authentication options: **admin user** or **shopware integration** (recommended).

```dotenv
# .env

APP_URL="<url-to-the-shopware-instance>"

# Authentication via integration
SHOPWARE_ACCESS_KEY_ID="<your-shopware-integration-id>"
SHOPWARE_SECRET_ACCESS_KEY="<your-shopware-integration-secret>"

# Authentication via admin user
SHOPWARE_ADMIN_USERNAME="<administrator-user-name>"
SHOPWARE_ADMIN_PASSWORD="<administrator-user-password>"
```

To ensure Playwright is referencing the correct instance, you can use the same environment variable in your Playwright configuration.

```TypeScript
// playwright.config.ts

import { defineConfig } from '@playwright/test';

export default defineConfig({
    use: {
        baseURL: process.env['APP_URL'],
 }
});
```

For more information about how to configure your Playwright project, have a look at the [official documentation](https://playwright.dev/docs/test-configuration).

## Mailpit configuration

Set up your local Mailpit instance by following the instructions at [Mailpit GitHub repository](https://github.com/axllent/mailpit).\
By default, Mailpit starts a web interface at `http://localhost:8025` and listens for SMTP on port `1025`.\
Set the `MAILPIT_BASE_URL` environment variable in `playwright.config.ts` to `http://localhost:8025`. You can now run email tests, such as `tests/Mailpit.spec.ts`.

## Usage

The test suite uses the [extension system](https://playwright.dev/docs/extensibility) of Playwright and can be used as a complete drop-in for Playwright. However, if you also want to add your extensions, the best approach is to create your base test file and use it as the central reference for your test files. Add it to your project root or a specific fixture directory and name it whatever you like.

Make sure to set `"type": "module",` in your `package.json`.

```TypeScript
// BaseTestFile.ts

import { test as base } from '@shopware-ag/acceptance-test-suite';
import type { FixtureTypes } from '@shopware-ag/acceptance-test-suite';

export * from '@shopware-ag/acceptance-test-suite';

export const test = base.extend<FixtureTypes>({
    
    // Your fixtures 
    
});
```

Within your tests, you can import the necessary dependencies from your base file.

```TypeScript
// tests/MyFirstTest.spec.ts

import { test, expect } from './../BaseTestFile';

test('My first test scenario.', async ({ AdminApiContext, DefaultSalesChannel }) => {
    
    // Your test logic
    
});
```

In the example above, you can see two Shopware-specific fixtures that are used in the test, `AdminApiContext` and `DefaultSalesChannel`. Every fixture can be used as an argument within the test method. Read more about available [fixtures](./fixtures.md) in the following section.

---

---

## Language Agnostic Testing
**Source:** [guides/plugins/plugins/testing/playwright/language-agnostic-testing.md](https://developer.shopware.com/docs/guides/plugins/plugins/testing/playwright/language-agnostic-testing.md)  
# Language Agnostic Testing

Language agnostic testing in @shopware-ag/acceptance-test-suite allows you to write acceptance tests that work across different languages without hard-coding text strings. Tests use translation keys instead of hard-coded strings and automatically adapt to different locales via environment variables.

## translate() Function

Use the `translate()` function in page objects to replace hardcoded strings with translation keys.

### Usage in Page Objects

```typescript
import { translate } from '../../services/LanguageHelper';

export class CategoryListing implements PageObject {
    constructor(page: Page) {
        this.createButton = page.getByRole('button', {
            name: translate('administration:category:actions.createCategory'),
        });
    }
}
```

## Translate Fixture

The `Translate` fixture provides translation functionality in tests.

### Usage in Tests

```typescript
import { test, expect } from '@shopware-ag/acceptance-test-suite';

test('Category creation', async ({ AdminPage, Translate }) => {
    const saveText = Translate('administration:category:general.save');
    await AdminPage.getByRole('button', { name: saveText }).click();
});
```

## Environment Control

Switch test language using environment variables:

```bash
LANG=de-DE npm run test  # German
LANG=en-GB npm run test  # English (default)
```

## Translation Keys

Translation keys follow the pattern: `area:module:section.key`

### Examples

```typescript
'administration:category:general.save';
'administration:category:actions.createCategory';
'storefront:account:fields.firstName';
'storefront:checkout:payment.invoice';
```

### Locale Files

Translations are stored in JSON files organized by language and area:

* `locales/en/administration/category.json`
* `locales/de/administration/category.json`
* `locales/en/storefront/account.json`
* `locales/de/storefront/account.json`

### Example Translation Files

**English (`locales/en/administration/category.json`):**

```json
{
    "general": {
        "save": "Save",
        "cancel": "Cancel"
    },
    "actions": {
        "createCategory": "Create category"
    }
}
```

**German (`locales/de/administration/category.json`):**

```json
{
    "general": {
        "save": "Speichern",
        "cancel": "Abbrechen"
    },
    "actions": {
        "createCategory": "Kategorie erstellen"
    }
}
```

## Supported Locales

**Translation Resources**: `en` (English), `de` (German)\
**Browser UI**: `en`, `de`, `fr`, `es`, `it`, `nl`, `pt`

## Common Issues

**Translation key not found:**

* Verify key exists in both EN/DE locale files
* Check import in `locales/index.ts`
* Ensure proper namespace structure

**Tests fail with LANG changes:**

* Move `translate()` calls inside constructors/functions, not at module level
* Ensure translation resources are properly loaded

**JSON import errors:**

* Always use `with { type: 'json' }` import attribute
* Check file paths and naming conventions

**Browser locale not matching:**

* Verify locale mapping in `playwright.config.ts`
* Check browser args configuration
* Ensure language detection is working correctly

## Using in Your Own Project

If you want to use the `@shopware-ag/acceptance-test-suite` in your own project with custom translations, you can extend the base test suite with your own translation fixture.

### Installation

First, install the required dependencies:

```bash
npm install @shopware-ag/acceptance-test-suite @playwright/test
npm install -D @types/node
```

### Create Custom Translation Fixture

Create a new fixture file (e.g., `fixtures/CustomTranslation.ts`):

```typescript
import {
    test as base,
    LanguageHelper,
    TranslationKey,
    TranslateFn,
    BUNDLED_RESOURCES,
    baseNamespaces,
} from '@shopware-ag/acceptance-test-suite';
import { LOCALE_RESOURCES, enNamespaces } from '../locales';

// Merge base BUNDLED_RESOURCES with your custom LOCALE_RESOURCES
const MERGED_RESOURCES = {
    en: { ...BUNDLED_RESOURCES.en, ...LOCALE_RESOURCES.en },
    de: { ...BUNDLED_RESOURCES.de, ...LOCALE_RESOURCES.de },
} as const;

// Merge base and custom namespaces
const mergedNamespaces = {
    ...baseNamespaces,
    ...enNamespaces,
} as const;

type CustomTranslationKey = TranslationKey<typeof mergedNamespaces>;

interface CustomTranslateFixture {
    Translate: TranslateFn<CustomTranslationKey>;
}

export const test = base.extend<CustomTranslateFixture>({
    Translate: async ({}, use) => {
        let lang = process.env.lang || process.env.LANGUAGE || process.env.LANG || 'en';
        let language = lang.split(/[_.-]/)[0].toLowerCase();

        if (!MERGED_RESOURCES[language as keyof typeof MERGED_RESOURCES]) {
            console.warn(
                `⚠️  Translation resources for '${language}' not available. Supported: ${Object.keys(
                    MERGED_RESOURCES
                ).join(', ')}. Falling back to 'en'.`
            );
            language = 'en';
        }

        const languageHelper = await LanguageHelper.createInstance(
            language,
            MERGED_RESOURCES as unknown as typeof BUNDLED_RESOURCES
        );

        const translate: TranslateFn<CustomTranslationKey> = (key, options) => {
            return languageHelper.translate(key as TranslationKey, options);
        };

        await use(translate);
    },
});

export * from '@shopware-ag/acceptance-test-suite';
export type { CustomTranslationKey };
```

### Create Locale Files Structure

Organize your translation files by language and area:

```text
project-root/
├── locales/
│   ├── en/
│   │   ├── administration/
│   │   │   ├── common.json
│   │   │   └── product.json
│   │   └── storefront/
│   │       ├── account.json
│   │       └── checkout.json
│   ├── de/
│   │   ├── administration/
│   │   │   ├── common.json
│   │   │   └── product.json
│   │   └── storefront/
│   │       ├── account.json
│   │       └── checkout.json
│   └── index.ts
├── fixtures/
│   └── CustomTranslation.ts
├── types/
│   └── TranslationTypes.ts
└── tests/
    └── your-test.spec.ts
```

### Create Locales Index

Create `locales/index.ts` to import and export your translation files:

```typescript
// Import all locale files
import enAdministrationCommon from './en/administration/common.json' with { type: 'json' };
import enStorefrontAccount from './en/storefront/account.json' with { type: 'json' };

import deAdministrationCommon from './de/administration/common.json' with { type: 'json' };
import deStorefrontAccount from './de/storefront/account.json' with { type: 'json' };

// Export the bundled resources for i18next
export const LOCALE_RESOURCES = {
    en: {
        'administration/common': enAdministrationCommon,
        'storefront/account': enStorefrontAccount,
    },
    de: {
        'administration/common': deAdministrationCommon,
        'storefront/account': deStorefrontAccount,
    },
} as const;

export const enNamespaces = {
    administration: {
        common: enAdministrationCommon,
    },
    storefront: {
        account: enStorefrontAccount,
    },
} as const;
```

### Create Translation Types

Create `types/TranslationTypes.ts` to define your custom translation types. This provides:

* **Type Safety**: Ensures translation keys exist in your locale files
* **IntelliSense**: Auto-completion for available translation keys
* **Compile-time Validation**: Catches typos and missing keys before runtime

```typescript
import { TranslationKey, TranslateFn } from '@shopware-ag/acceptance-test-suite';
import { enNamespaces } from '../locales';

export type CustomTranslationKey = TranslationKey<typeof enNamespaces>;

export type CustomTranslateFn = TranslateFn<CustomTranslationKey>;
```

### Merge with Base Test Suite

Create your main test fixture that merges the base test suite with your custom translation:

```typescript
import { test as ShopwareTestSuite, mergeTests } from '@shopware-ag/acceptance-test-suite';
import { test as CustomTranslation } from './fixtures/CustomTranslation';

export * from '@shopware-ag/acceptance-test-suite';

export const test = mergeTests(ShopwareTestSuite, CustomTranslation);
```

**Note**: Save this as `test.ts` or `index.ts` in your project root and import it in your test files.

### Usage in Your Tests

Now you can use the `Translate` fixture in your tests:

```typescript
import { test } from './your-main-test-fixture';

test('My localized test', async ({ Translate, AdminPage }) => {
    const saveText = Translate('administration:common:button.save');
    await AdminPage.getByRole('button', { name: saveText }).click();
});
```

### Environment Configuration

Set up your Playwright configuration to support language switching:

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

const LOCALES = { de: 'de-DE', en: 'en-US', fr: 'fr-FR' };

function getLanguage(): string {
    let lang = process.env.lang || process.env.LANGUAGE || process.env.LANG || 'en';
    return lang.split(/[_.-]/)[0].toLowerCase();
}

function getLocaleConfig() {
    const lang = getLanguage();
    const browserLocale = LOCALES[lang as keyof typeof LOCALES] || 'en-US';
    const browserArgs =
        lang !== 'en' && LOCALES[lang as keyof typeof LOCALES]
            ? [`--lang=${browserLocale}`, `--accept-lang=${browserLocale},${lang};q=0.9,en;q=0.8`]
            : [];

    return { lang, browserLocale, browserArgs };
}

export default defineConfig({
    use: {
        locale: getLocaleConfig().browserLocale,
    },
    projects: [
        {
            name: 'Platform',
            use: {
                ...devices['Desktop Chrome'],
                launchOptions: {
                    args: [...getLocaleConfig().browserArgs],
                },
            },
        },
    ],
});
```

### Running Tests with Different Languages

```bash
# German
LANG=de-DE npx playwright test

# English (default)
npx playwright test
```

---

---

## Local development with ATS
**Source:** [guides/plugins/plugins/testing/playwright/local-development.md](https://developer.shopware.com/docs/guides/plugins/plugins/testing/playwright/local-development.md)  
# Local development with ATS

To work locally with ATS and your development setup, follow these steps:

## Create your Page Objects and TestDataService methods

In the ATS repository ([shopware/acceptance-test-suite](https://github.com/shopware/acceptance-test-suite)), create or modify your custom page objects, `TestDataService` methods, or any related files.

After making your changes, build the project by running the following command in the ATS repository:

```bash
npm run build
```

This will generate the necessary artifacts in the `dist` folder.

Copy the generated artifacts (e.g., all files in the `dist` folder) from the ATS repository to your local Shopware instance's `node_modules` folder, specifically under the ATS package path:

```bash
cp -R dist/* <path-to-your-shopware-instance>/tests/acceptance/node_modules/@shopware-ag/acceptance-test-suite/dist
```

### Adjust tests, Page Objects, and methods

In your Shopware instance, adjust any tests, page objects, `TestDataService` methods, or other related files to align them with the changes made in the ATS repository.

### Run the tests

Execute the tests to verify your changes. Use the following command from your Shopware project's acceptance test directory:

```bash
cd tests/acceptance
npx playwright test --ui
```

This will launch the Playwright Test Runner UI, where you can select and run specific tests.
By following these steps, you can work locally with the ATS and test your changes in your Shopware instance.

:::info
When running your tests, the Acceptance Test Suite operates under the assumption that any themes are compiled beforehand and the "Shopware default theme" is being used for Storefront. Custom themes may require some adjustments for certain locators to work properly.
:::

---

---

## Page Objects
**Source:** [guides/plugins/plugins/testing/playwright/page-object.md](https://developer.shopware.com/docs/guides/plugins/plugins/testing/playwright/page-object.md)  
# Page Objects

Page objects can be helpful to simplify the usage of element selectors and make them available in a reusable way. They help you to organize page-specific locators and provide helpers for interacting with a given page. Within our test suite, we try to keep the page objects very simple and not add too much logic to them. So most of the page objects resemble just a collection of element locators and maybe some little helper methods.

There are several page objects to navigate the different pages of the Administration and Storefront. You can use them as any other fixture within your test. There is also a guide on page objects in the [official Playwright documentation](https://playwright.dev/docs/pom).

## Usage

```TypeScript
import { test, expect } from './../BaseTestFile';

test('Storefront cart test scenario', async ({ StorefrontPage, StorefrontCheckoutCart }) => {

    await StorefrontPage.goto(StorefrontCheckoutCart.url());
    await expect(StorefrontCheckoutCart.grandTotalPrice).toHaveText('€100.00*');
});
```

You can get an overview of all available page objects in the [repository](https://github.com/shopware/acceptance-test-suite/tree/trunk/src/page-objects) of this test suite.

## Page Object module

The `modules` folder is designed to house reusable utility functions that operate on a `Page` object (from Playwright). These functions dynamically interact with different browser pages or contexts using the `page` parameter.
For example, utility functions like `getCustomFieldCardLocators` or `getSelectFieldListitem` are used across multiple page objects to handle specific functionality (e.g., managing custom fields or select field list items). Centralizing these utilities in the `modules` folder improves code organization, readability, and reduces duplication.
Create a new class inside a module when it helps to streamline the codebase and avoid repetitive logic across page objects.

You can find how `getCustomFieldCardLocators` is defined in the [modules folder](https://github.com/shopware/acceptance-test-suite/blob/trunk/src/page-objects/administration/modules/CustomFieldCard.ts) and used in other [page object classes](https://github.com/shopware/acceptance-test-suite/blob/trunk/src/page-objects/administration/ProductDetail.ts).

## Add new Page Objects

Page objects are organized mainly by their usage in the Administration or Storefront. To add a new page object, simply add it to the respective subfolder and reference it in `AdministrationPages.ts` or `StorefrontPages.ts`.

### Usage

```TypeScript
import { test as base } from '@playwright/test';
import type { FixtureTypes } from '../types/FixtureTypes';

import { ProductDetail } from './administration/ProductDetail';
import { OrderDetail } from './administration/OrderDetail';
import { CustomerListing } from './administration/CustomerListing';
// [...]
import { MyNewPage } from './administration/MyNewPage';

export interface AdministrationPageTypes {
    AdminProductDetail: ProductDetail;
    AdminOrderDetail: OrderDetail;
    AdminCustomerListing: CustomerListing;
    // [...]
    AdminMyNewPage: MyNewPage;
}

export const AdminPageObjects = {
    ProductDetail,
    OrderDetail,
    CustomerListing,
    // [...]
    MyNewPage,
}
```

---

---

## Services
**Source:** [guides/plugins/plugins/testing/playwright/test-data-service.md](https://developer.shopware.com/docs/guides/plugins/plugins/testing/playwright/test-data-service.md)  
# Services

The test suite provides several services that can be used to simplify your test code. These services are designed to be reusable and can be easily extended to fit your specific needs.

## Test Data Service

The `TestDataService` is a powerful utility designed to simplify test data creation, management, and cleanup when writing acceptance and API tests for Shopware. It provides ready-to-use functions for common data needs and ensures reliable, isolated test environments.
For detailed documentation of the methods, you can have a look at the [service class](https://github.com/shopware/acceptance-test-suite/blob/trunk/src/services/TestDataService.ts) or use the auto-completion of your IDE.

## When to use the TestDataService in tests

You should use the `TestDataService` whenever you need **test data** that matches common Shopware structures, such as:

* Creating a **basic product**, **customer**, **order**, **category**, etc
* Setting up **media** resources like product images or digital downloads
* Creating **promotions**, **rules**, or **payment/shipping methods**
* Fetching existing entities via helper methods (`getCurrency()`, `getShippingMethod()`, etc)
* **Assigning relations** between entities (e.g., linking a product to a category)

### Typical examples

```typescript
const product = await TestDataService.createBasicProduct();
const customer = await TestDataService.createCustomer();
const shipping = await TestDataService.createBasicShippingMethod();
```

## When and why to extend the `TestDataService`

You should add new functions to the `TestDataService` (or extend it) when:

* Your project or plugin introduces **new entity types** (e.g., `CommercialCustomerGroup`, `CustomProductType`)
* You need a **specialized creation logic** (e.g., a shipping method with multiple rules, a pre-configured product bundle)
* Existing methods require **modifications** that should not affect the core service
* You want to **reuse the same setup across multiple tests** without duplicating logic
* You require **special cleanup handling** for newly created entities

Using and extending the `TestDataService` properly ensures your acceptance tests stay **readable**, **maintainable**, and **scalable** even as your Shopware project grows.

## Available `create*` methods in `TestDataService`

These methods are designed to streamline the setup of test data, ensuring consistency and efficiency in your testing processes. They are much more available than listed below, but these are the most common ones. Use your IDE auto-completion to find all available methods.

* `createBasicProduct(): Promise<Product>`
* `createVariantProducts(parentProduct: Product, propertyGroups: PropertyGroup[]): Promise<Product[]>`
* `createCustomer(): Promise<Customer>`
* `createCustomerGroup(): Promise<CustomerGroup>`
* `createOrder(lineItems: SimpleLineItem[], customer: Customer): Promise<Order>`
* `createCategory(): Promise<Category>`
* `createColorPropertyGroup(): Promise<PropertyGroup>`
* `createBasicPaymentMethod(): Promise<PaymentMethod>`
* `createBasicShippingMethod(): Promise<ShippingMethod>`
* \[...]

## Available `assign*` methods in `TestDataService`

These methods are designed to establish associations between entities, such as linking products to categories or assigning media to manufacturers, ensuring that your test data reflects realistic scenarios. They are much more available than listed below, but these are the most common ones. Use your IDE auto-completion to find all available methods.

* `assignProductCategory(productId: string, categoryIds: string[]): Promise<void>`
* `assignProductManufacturer(productId: string, manufacturerId: string): Promise<void>`
* `assignProductMedia(productId: string, mediaId: string): Promise<void>`
* \[...]

## Available `get*` methods in `TestDataService`

They are much more available than listed below, but these are the most common ones. Use your IDE auto-completion to find all available methods.

* `getCountry(iso2: string): Promise<Country>`
* `getCurrency(isoCode: string): Promise<Currency>`
* `getCustomerGroups(): Promise<CustomerGroup[]>`
* `getPaymentMethod(name = 'Invoice'): Promise<PaymentMethod>`
* \[...]

## Writing new methods in `TestDataService`

If you want to add new functionality to this service such as a new type of entity creation, you can follow this approach:

### 1. Define the purpose

Decide whether you're creating, assigning, or retrieving data. Most methods fall into one of the following patterns:

* `create*`: Creates a new entity (e.g., product, customer, category)
* `assign*`: Links existing entities (e.g., assign media to product)
* `get*`: Retrieves specific or filtered data from the system

### 2. Implement the method

Use the `AdminApiContext` to interact with the Shopware Admin API. Here is a simplified example of adding a method to [create a new shipping method](https://github.com/shopware/acceptance-test-suite/blob/e8d2a5e8cee2194b914aa35aa87fe7cf04060834/src/services/TestDataService.ts#L679)

### 3. Follow naming conventions

Be consistent in naming:

* Use `createBasic*` for standardized, default setups with predefined values (e.g., `createBasicProduct`)
* Use `create*With*` for variations (e.g. `createProductWithImage`)
* Use `assign*` for methods that associate two entities (e.g., `assignProductMedia`)
* Use `get*` to retrieve specific entities or lists (e.g. `getCurrency`)

### 4. Add a return type

Always define a return type (typically a `Promise<...>`) to improve autocompletion and documentation support.

### 5. Add cleanup logic

Make sure to clean up the entity via code after the test run by putting the entity in a record. See the example below:

```typescript
async createBasicRule(): Promise<Rule> {
        [...]
                
 this.addCreatedRecord('rule', rule.id);

 [...]
 }
```

Explore further info on this in [Automatic Cleanup](#automatic-cleanup-of-test-data-and-system-configurations).

### 6. Test the method

Once added, use your new method inside a test to verify it works as expected (`/tests/TestDataService.spec.ts`):

```typescript
test('Verify new shipping method creation', async ({ TestDataService }) => {
    const shippingMethod = await TestDataService.createShippingMethod({
        name: 'Express Delivery'
 });

    expect(shippingMethod.name).toEqual('Express Delivery');
});
```

## Automatic cleanup of test data and system configurations

The `TestDataService` includes a built-in mechanism to ensure that any test data & system configuration entries created during a test run are automatically deleted afterward. This ensures that the Shopware instance remains clean and consistent between tests, helping to maintain **test isolation** and prevent **state leakage**.

### How cleanup works

When you create an entity using a `create*` method (e.g., `createBasicProduct`, `createCustomer`), the service automatically registers that entity for deletion by calling the `addCreatedRecord()` method:

```typescript
this.addCreatedRecord('product', product.id);
```

These records are stored in a cleanup queue processed at the end of each test using the Playwright lifecycle.

### Cleanup execution

The `cleanup()` method handles the deletion of all registered entities and system config changes. All created records are grouped into two categories:

* Priority Deletions (`priorityDeleteOperations`) – for entities with dependencies that must be deleted first (e.g., orders, customers)
* Standard Deletions (`deleteOperations`) – for all other entities

This prioritization prevents errors when deleting interdependent data. Any modified system configurations are reset to their previous state after deleting priority records.
The priority entities can be found in the `TestDataService` class. If you want to add a new entity to the priority deletion list, you can do so by adding it to the `priorityDeleteOperations` array.

### Skipping cleanup

In rare scenarios, such as performance testing or debugging, you may want to prevent cleanup for specific entities. You can simply skip the cleanup by calling `TestDataService.setCleanUp(false)` within your test.

## Extending the TestDataService in external projects

The `TestDataService` is designed to be **easily extendable**. This allows you to add project-specific data generation methods while still benefiting from the existing, standardized base functionality.

### 1. Create a new subclass

You can create a new TypeScript class that **extends** the base `TestDataService`.

```typescript
import { TestDataService } from '@shopware-ag/acceptance-test-suite';

export class CustomTestDataService extends TestDataService {

    constructor(AdminApiContext, DefaultSalesChannel) {
        super(...);
 }
    
    async createCustomCustomerGroup(data: Partial<CustomerGroup>) {
        const response = await this.adminApi.post('customer-group?_response=true', {
            data: {
 ...
 },
 });

        const { data: createdGroup } = await response.json();
        this.addCreatedRecord('customer-group', createdGroup.id);

        return createdGroup;
 }
}
```

### 2. Provide the extended service as a fixture

Following the Playwright [fixture system](https://playwright.dev/docs/test-fixtures) described, you create a new fixture that initializes your extended service.

Example from `AcceptanceTest.ts`:

```typescript
import { test as base } from '@shopware-ag/acceptance-test-suite';
import type { FixtureTypes } from './BaseTestFile';
import { CustomTestDataService } from './CustomTestDataService';

export interface CustomTestDataServiceType {
    TestDataService: CustomTestDataService;
}

export const test = base.extend<FixtureTypes & CustomTestDataServiceType>({
    TestDataService: async ({ AdminApiContext, DefaultSalesChannel }, use) => {
        const service = new CustomTestDataService(AdminApiContext, DefaultSalesChannel.salesChannel);
        await use(service);
        await service.cleanUp();
 },
});
```

In this setup:

* The `TestDataService` fixture is **overridden** with your custom `CustomTestDataService`.
* Now, all tests that use `TestDataService` will have access to both the original and your extended methods.
* The automated cleanup is still in place, ensuring that any test data created during the test run is removed afterward.

---

---

## Types in the Test Suite
**Source:** [guides/plugins/plugins/testing/playwright/test-suite-types.md](https://developer.shopware.com/docs/guides/plugins/plugins/testing/playwright/test-suite-types.md)  
# Types in the Test Suite

The Shopware Acceptance Test Suite leverages TypeScript’s static typing to ensure that test data structures, API interactions, and test logic are consistent and error-resistant.

## Shopware Types

The centralized type definition file, [ShopwareTypes.ts](https://github.com/shopware/acceptance-test-suite/blob/trunk/src/types/ShopwareTypes.ts) is tightly coupled with the TestDataService, which defines the shape and default data of all supported Shopware entities. Each supported entity such as Product, Customer, Media, etc is defined with its properties and default values. These types are then referenced throughout the [`TestDataService`](./test-data-service.md) to provide IntelliSense, validation, and consistent data structures.

```typescript
export type ProductReview = components['schemas']['ProductReview'] & {
 id: string,
 productId: string,
 salesChannelId: string,
 title: string,
 content: string,
 points: number,
}
```

Within that example above, you are importing the auto-generated type for `ProductReview` from the Shopware Admin API OpenAPI schema and extending it with additional or overridden fields using `& { ... }`.

Sometimes, you might want to remove fields from a type. TypeScript provides the `Omit<T, K>` utility to exclude fields from a type:

```typescript
export type Country = Omit<components['schemas']['Country'], 'states'> & {
 id: string,
 states: [{
 name: string,
 shortCode: string,
 }],
}
```

For custom use cases, simply define a custom type:

```typescript
export type CustomShippingMethod = {
 name: string;
 active: boolean;
 deliveryTimeId: string;
}
```

---

---

## Testing within the Test Suite
**Source:** [guides/plugins/plugins/testing/playwright/test.md](https://developer.shopware.com/docs/guides/plugins/plugins/testing/playwright/test.md)  
# Testing within the Test Suite

The `tests` folder ensures the reliability of the testing framework by validating the functionality of tools and data used in tests. Add tests to verify any new features or changes you introduce:

* **Page Objects**: Ensure they are correctly implemented and interact with the application as expected, including navigation, element visibility, and user interactions.
* **TestDataService Methods**: Verify that methods for creating, getting, and cleaning up test data (e.g., products, customers, orders) work correctly and produce consistent results.

```TypeScript
//Example for page objects

await ShopAdmin.goesTo(AdminManufacturerCreate.url());
await ShopAdmin.expects(AdminManufacturerCreate.nameInput).toBeVisible();
await ShopAdmin.expects(AdminManufacturerCreate.saveButton).toBeVisible();
```

```TypeScript
//Example for TestDataService

const product = await TestDataService.createProductWithImage({ description: 'Test Description' });
expect(product.description).toEqual('Test Description');
expect(product.coverId).toBeDefined();
```

## Running tests in the Test Suite

To work on the test suite and execute tests from within this repository, you must run a corresponding Docker image for the specific Shopware version.

We publish pre-built images at the [GitHub container registry](https://github.com/shopware/acceptance-test-suite/pkgs/container/acceptance-test-suite%2Ftest-image). The images are built daily; check to see which versions are available.

To select an image, export the corresponding tag as `SHOPWARE_VERSION` and start the containers:

```bash
SHOPWARE_VERSION=trunk docker compose up --wait shopware
```

If you want to test with an image that's not available already, you can build it yourself by exporting a few more variables:

```bash
export PHP_VERSION="8.3" # PHP version of the base image
export SHOPWARE_VERSION="v6.5.8.0" # Shopware version to check out. This may be either a branch or a tag, depending on the value of SHOPWARE_BUILD_SOURCE
export SHOPWARE_BUILD_SOURCE="tag" # Either "branch" or "tag"

docker compose up --attach-dependencies shopware # This will build the image if it's not available
```

Afterwards, you can execute the normal playwright commands:

```bash
npx playwright test --ui
```

---

---

## Storefront Accessibility
**Source:** [resources/accessibility/accessibility-checklist.md](https://developer.shopware.com/docs/resources/accessibility/accessibility-checklist.md)  
# Storefront Accessibility

Creating an accessible storefront ensures that all users can navigate, interact with, and benefit from your site. Accessibility is not only a best practice but a legal and ethical responsibility that contributes to a more inclusive web.

This checklist outlines the key principles and technical requirements for building accessible web interfaces, with a focus on semantic structure, keyboard usability, screen reader compatibility, and inclusive design practices.

## Storefront Accessibility Checklist: Best Practices for Inclusive Web Design

### Use Semantic HTML

Leverage native HTML elements that communicate their purpose effectively:

* Use appropriate tags for actions: `<button>`, `<a>`, `<select>` instead of `<div>` or `<span>`.
* Structure your layout with semantic elements: `<nav>`, `<main>`, `<header>`, `<footer>`.
* Always pair `<label>` elements with form controls using `for` and `id`. Avoid relying solely on `placeholder` text for labeling.

### Set the Correct Document Language

Proper language settings help screen readers use accurate pronunciation and intonation:

* Add `lang="en"` (or the appropriate language code) to the `<html>` tag.

### Ensure Accessible Forms

All form fields must be clearly labeled and error states must be identifiable:

* Use `<label for="input-id">`, `aria-label`, or `aria-labelledby`.
* Provide error messages that are clear and easy to locate.
* Don’t rely solely on color (e.g., red) to indicate errors. You can use icons or text additionally.
* Use `aria-describedby` to connect input fields to help or error messages.

### Manage Focus

Ensure users know where they are and can move through the interface logically:

* Use `tabindex="0"` for custom interactive elements. Try to not mess around with the tabindex if possible and keep the "natural" tab flow.
* Do not remove focus outlines unless replaced with a clear visible alternative.
* Use `focus()` to direct user attention (e.g. after form errors or modal open).
* Each interactive element that can be clicked or navigated by keyboard (`<a>`, `<button>` etc.) must have a clearly visible focus indication.

### Keyboard Accessibility

Users should be able to navigate and interact with all features using only the keyboard:

* Ensure `Enter` and `Space` activate interactive elements.
* Avoid using `onclick` on non-focusable elements without keyboard support.
* Custom widgets must respond to arrow keys and expected keyboard patterns.

### Use ARIA Carefully

Use ARIA roles and attributes only when native HTML doesn’t work.

* Use `role="alert"` for live error messaging.
* Apply `aria-expanded`, `aria-controls`, and `aria-hidden` for toggleable UI elements.
* Prefer native HTML elements over ARIA whenever possible to reduce complexity.

### Provide Live Region Updates

Ensure real-time changes are accessible:

* Use `aria-live="polite"` or `aria-live="assertive"` for real-time updates (e.g. validation messages, chat widgets).

### Manage Page Titles and Headings

Headings and titles provide structure and orientation. It helps users understand page structure:

* Always update the `<title>`  tag on page load or route change.
* Use one `<h1>` per page, followed by correct heading hierarchy (`<h2>`, `<h3>`, etc.).

### Support Skip Links

Help keyboard users skip repetitive content:

* Include a skip link at the top of the page:

  ```html
  <a href="#main-content" class="skip-link">Skip to main content</a>
  ```

### Control Focus When Using Modals or Popovers

Focus should remain within the modal and return to the trigger element after closing:

* Trap focus while the modal is open.
* Return focus to the initiating element once it is closed.

### Avoid Auto-Playing Audio or Video

If unavoidable, make sure users can easily pause or stop it:

* Provide controls on `<video>` or `<audio>` elements.
* Avoid autoplay unless muted and non-disruptive.

### Ensure Unique IDs and ARIA Attributes

Avoid duplicated IDs to maintain screen reader reliability:

* Validate that `id` attributes are unique.
* Ensure any referenced IDs in `aria-labelledby` or `aria-describedby` exist and are not duplicated.

### Test with Assistive Technologies

Test your site with real-world tools and scenarios:

* Use screen readers like NVDA (Windows), VoiceOver (macOS).
* Navigate with only the keyboard (Tab, Shift+Tab, Enter, Space).
* Leverage browser dev tools (Chrome DevTools > Accessibility, Axe Core).

## Conclusion

Following this checklist will help ensure your storefront is usable by everyone, regardless of ability. It also improves SEO, performance, and user satisfaction for all visitors.

Regularly audit your code, test with assistive technologies, and stay updated with evolving accessibility standards. Inclusive design is good design.

---

---

