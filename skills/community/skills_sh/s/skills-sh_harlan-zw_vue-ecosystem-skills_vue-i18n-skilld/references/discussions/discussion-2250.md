---
number: 2250
title: How to Dynamically Reference Translation Keys in vue-i18n
category: Q&A
created: 2025-08-23
url: "https://github.com/intlify/vue-i18n/discussions/2250"
upvotes: 1
comments: 1
answered: false
---

# How to Dynamically Reference Translation Keys in vue-i18n

# How to Dynamically Reference Translation Keys in vue-i18n

I'm having trouble with `vue-i18n` when using the `@:{key}` syntax for dynamic translation key references. Here's the issue:

### Issue

My translation dictionary is:

```json
{
  "HealthAlarm": "The Health Alarm '@:{reason}' '{name}'",
  "breeding_wound": "Breeding Wound"
}
```

When calling `$t('HealthAlarm', { reason: 'breeding_wound', name:  'Cow#01' })`, I expect:

```
The Health Alarm 'Breeding Wound' 'Cow#01'
```

But the actual output is:

```
The Health Alarm '@:breeding_wound' 'Cow#01'
```

I want to know the best approach for this.

### Current Workaround

I'm using a dictionary structure like:

```json
{
  "HealthAlarm.breeding_wound": "The Health Alarm '@:dict.breeding_wound' '{name}'",
  "HealthAlarm.suspected_mastitis": "The Health Alarm '@:dict.suspected_mastitis' '{name}'",
  "dict.breeding_wound": "Breeding Wound",
  "dict.suspected_mastitis": "Suspected Mastitis"
}
```...

---

## Top Comments

**@vtestah**:

Hey @supemeko! The `@:` syntax can be a bit tricky.

The problem is that `@:{reason}` is for linking to *another key* directly, it doesn't dynamically use the variables you pass in. It's looking for a key literally named "reason".

Here are two better ways to handle this.

### 1. The Easy Way: Nested `$t`

This is the most common and straightforward solution. Just call `$t` inside another `$t`.

**Your JSON:**
```json
{
  "HealthAlarm": "The Health Alarm '{reason}' '{name}'",
  "breeding_wound": "Breeding Wound"
}
```

**Your Template:**
```html
<p>{{ $t('HealthAlarm', { reason: $t('breeding_wound'), name: 'Cow#01' }) }}</p>
```...