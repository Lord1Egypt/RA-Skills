---
number: 14304
title: (newbie question) How can I fix uncaught (in promise) DOMException error
category: Help/Questions
created: 2026-01-11
url: "https://github.com/orgs/vuejs/discussions/14304"
upvotes: 1
comments: 1
answered: true
---

# (newbie question) How can I fix uncaught (in promise) DOMException error

Vue version: 3.5.25
vue-router version: 4.6.3

I'm doing my very first pet-project at all. The error only occurs in Firefox. Everything works fine in Chromium, with no errors, as shown in the second screenshot. I just don't know where to look.

<img width="1377" height="965" alt="image" src="https://github.com/user-attachments/assets/57654464-0aa3-4202-a7b9-2d43e6a39f79" />
<img width="502" height="226" alt="image" src="https://github.com/user-attachments/assets/c431e188-ce3c-4af2-854b-5354fd55517f" />

---

## Accepted Answer

I solved the problem. That warning didn't mean anything. I have a fairly large project with a lot of code (for a beginner's pet project). For some reason, Chromium-like browsers allowed me to accidentally write a semicolon in the component properties, which I didn't notice, while Firefox complained about it but didn't explain anything. Commenting out the components one by one helped. Look below and find it
```
<div class="flex flex-row justify-center gap-4 py-2">
  <AtomRegularButton
    :icon="FolderPlusIcon"
    :customIconSize="5"
    :without-paddings-for-icon="true"
    @click="workspacesStore.addWorkspace('New space')"
    ;
  />
  <AtomRegularButton
    :icon="PencilSquareIcon"
    :custom-icon-size="5"
    @click="
      () => {
        toggleTaskActions();
        showInputForChangeWorkspaceTitle = false;
      }
    "
    :without-paddings-for-icon="true"
  />
</div>
```