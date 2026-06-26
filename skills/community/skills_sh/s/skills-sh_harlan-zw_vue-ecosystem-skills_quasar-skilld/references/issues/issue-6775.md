---
number: 6775
title: Resolve Quasar and Tailwind CSS conflicts
type: other
state: closed
created: 2020-04-10
url: "https://github.com/quasarframework/quasar/issues/6775"
reactions: 63
comments: 88
labels: "[discussion :speaking_head:]"
---

# Resolve Quasar and Tailwind CSS conflicts

**Is your feature request related to a problem? Please describe.**

This proposal aims to resolve conflicts between **Quasar** and **TailwindCSS** with minimum changes.
Currently, **Quasar** and **TailwindCSS** offer both useful classes. This post is not to discuss the pros and cons (you can debate here) but to ease the use of **TailwindCSS** with **Quasar** for those who want to.

After investigation (with the help of CSS compare and CSS sort), we can divide **Quasar** class names in 4 categories:
- Classes prefixed with `q-` : not a problem.
- Classes not prefixed but not redundant with **TailwindCSS** (some of these classes are utility classes and could be renamed to match **TailwindCSS**) : not a problem.
- Classes with the same name and behavior in both frameworks : not a problem.
- Classes with the same name but with a different behavior : **it is a problem**.

Hopefully, the last category contain only 12 classes in 5 files with few differences: 

```css
/* Quasar: flex.styl */
.flex{ display: flex; flex-wrap: wrap }
.order-first { order: -10000 }
.order-last { order: 10000 }
/* TailwindCSS */
.flex { display: flex }
.order-first { order: -9999 }
.order-last { order: 9999 }

/* Quasar: mouse.styl */
.cursor-not-allowed { cursor: not-allowed !important }
.cursor-pointer { cursor: pointer !important }
/* TailwindCSS */
.cursor-not-allowed { cursor: not-allowed }
.cursor-pointer { cursor: pointer }

/* Quasar: size.styl */
.block { display: block !important }
.inline-block { display: inline-block !important }
/* TailwindCSS */
.block { display: block }
.inline-block { display: inline-block }

/* Quasar: typography.styl */
.text-justify { text-align: justify; hyphens: auto }
/* TailwindCSS */
.text-justify { text-align: justify }

/* Quasar: visibility.styl */
.hidden { display: none !important }
.invisible { visibility: hidden !important }
.overflow-auto { overflow: auto !important }
.overflow-hidden { overflow: hidden !important }
/* TailwindCSS */
.hidden { display: none }
.invisible { visibility: hidden }
.overflow-auto { overflow: auto }
.overflow-hidden { overflow: hidden }
```...

---

## Top Comments

**@timsayshey** (+27):

We came up with a workaround on our team to get Quasar and Tailwind to work together. Our goal was to build everything in Tailwind on Quasar but we didn't want Quasar styles loading in and taking over or conflicting with our Tailwind styles. The first thing we had to do was prevent the Quasar stylesheet from loading in however there is no option to disable it so we do a find/replace to remove it when webpack builds.

Run `npm i string-replace-loader` then add the following code to the `extendWebpack()` method in your `quasar.conf.js` file:

```
cfg.module.rules.push({
  test: /client-entry\.js$/,
  loader: 'string-replace-loader',
  options: {
    search: "import 'quasar/dist/quasar.sass'",
    replace: '',
  },
})
```...

**@charlie17** (+38):

This is one of those opportunities to open up Quasar to a wide swath of new users. A lot of devs resist Material - we've all seen that, and increasingly so. People want more design choice and control - with some quality building blocks to work with - that's why Tailwind has been so successful.

People also want to build top-quality Vue apps for all platforms using the right building blocks - that's what Quasar is all about. So it's different core competencies, but pointed at the same addressable market.

As another corollary, check the new PrimeVue release:

@gbouteiller I think you have submitted an intelligent and well-thought out request, but I would suggest you consider just using Quasar CSS, rather than asking Quasar team to spend time trying to get two frameworks working with each other, since this is such a marginal edge case that likely, only a tiny number of Quasar community would benefit from.

As a designer for the last 20 years, working with companies like Apple, Canon, Intel and others, I   Quasar CSS and have been creating beautiful UIs with it, I find it very easy to customize and make anything I can imagine, perhaps a more prod...