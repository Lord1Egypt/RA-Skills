---
number: 2207
title: Use of local messages in composable
type: bug
state: open
created: 2025-06-21
url: "https://github.com/intlify/vue-i18n/issues/2207"
reactions: 1
comments: 6
labels: "[ p3-minor-bug]"
---

# Use of local messages in composable

### Clear and concise description of the problem

In my current project, I use component specific message files in local i18n scopes which works amazing!:

```typescript
// component.vue
<script setup lang="ts">
  // Imports
  import { useI18n } from "vue-i18n";
  import i18nMessages from "./component.i18n";

  // I18n
  const { t } = useI18n({ messages: i18nMessages });
  
  const projectStatus = getProjectStatus(project);

  </script>

{{ t("component.message") }} 

{{ projectStatus }}

```

But if I want to do the same for a composable: 

```typescript
// composable.ts
  // Imports
  import { useI18n } from "vue-i18n";
  import i18nMessages from "./component.i18n";

...