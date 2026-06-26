---
number: 18166
title: "`QUploader`: Support async filter or trigger addFiles instead of  addFilesToQueue in drag-and-drop flow"
category: Ideas / Proposals
created: 2025-11-03
url: "https://github.com/quasarframework/quasar/discussions/18166"
upvotes: 2
comments: 0
answered: false
---

# `QUploader`: Support async filter or trigger addFiles instead of  addFilesToQueue in drag-and-drop flow

In my custom uploader, I need to process files **before** sending them to the uploader.

To achieve this, I had to create my own addFiles method using a native input and then call Quasar’s addFiles internally.

However, when using drag and drop, I can’t intercept the files — and I can’t use the filter prop either, since it doesn’t support async functions.

I also can’t override the addFiles method because Quasar doesn’t call it for drag-and-drop; instead, it uses addFilesToQueue.

It would be great if the filter prop could support returning a Promise for async processing before uploading, or alternatively, if `addFiles` could be called inside the onDrop handler instead of `addFilesToQueue`.