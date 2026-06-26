---
number: 18103
title: "Feature Request: Add icon-size prop to QBtn"
category: Ideas / Proposals
created: 2025-08-25
url: "https://github.com/quasarframework/quasar/discussions/18103"
upvotes: 8
comments: 2
answered: false
---

# Feature Request: Add icon-size prop to QBtn

I’d like to propose adding an `icon-size` prop to `<q-btn>` that allows customizing the size of the icon independently of the button size.

Currently, the icon inside `QBtn` changes with respect to the button size, while this works in most cases, there are situations where developers want a larger or smaller icon without altering the button size.

### Problem: Just to change the icon size, we have to use slots
```
<q-btn>
      <q-icon left size="3em" name="map" />
      <div>Label</div>
</q-btn>
```
### Proposal: Inline prop `icon-size`
```
<q-btn label="Label" icon="map" icon-size="3em" />
```
Looking forward to feedback! 
<img width="1002" height="124" alt="Screenshot 2025-08-25 at 5 56 02 PM" src="https://github.com/user-attachments/assets/abfb9f4e-f6d5-4122-acb0-fb91e96488be" />



---

## Top Comments

**@stefanvanherwijnen**:

You can use custom content and modify the icon any way you like.

**@shailabsinghha**:

Useful feature!