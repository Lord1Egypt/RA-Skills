---
number: 1920
title: How do I test on different languages when the locales are in the SFC?
category: Q&A
created: 2024-08-19
url: "https://github.com/intlify/vue-i18n/discussions/1920"
upvotes: 1
comments: 1
answered: true
---

# How do I test on different languages when the locales are in the SFC?

I am trying to test a component where the localization data is in the `<i18n>` block of an SFC.  But I can't seem to get it working and it always uses the default one

I did it something like this
```typescript
const i18n = createI18n({ locale: 'en', messages, globalInjection: true })

it('should display age correctly in English', () => {
    i18n.global.locale = 'en'
    const wrapper = mount(LjAge, {
      global: {
        plugins: [i18n],
      },
      props: {
        birthDate: '2014-11-11',
        today: '2024-07-29',
      },
    })
    expect(wrapper.text()).toBe('9y 8m')
})

it('should display age correctly in Spanish', () => {
    i18n.global.locale = 'es'
    const wrapper = mount(LjAge, {
      global: {
        plugins: [i18n],
      },
      props: {
        birthDate: '2014-11-11',
        today: '2024-07-29',
      },
    })
    expect(wrapper.text()).toBe('9a 8m')
})
```...

---

## Accepted Answer

I inlined it so this works

```typescript
it('should work with mounted component in Spanish', () => {
  const wrapper = mount(LjAge, {
    global: {
      plugins: [
        createI18n({
          locale: 'es'
        })
      ]
    },
    props: {
      birthDate: '2014-11-11',
      today: '2024-07-29'
    }
  })
  expect(wrapper.text()).toBe('9a 8m')
})
```