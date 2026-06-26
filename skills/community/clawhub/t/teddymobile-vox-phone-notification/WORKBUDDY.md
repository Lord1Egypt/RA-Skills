# WorkBuddy Compatibility Notes

This file records the WorkBuddy-specific assumptions used to shape this skill package.

## What could be confirmed

From the public WorkBuddy website bundle, the following signals were observable:

- WorkBuddy has a Claw documentation route: `/docs/workbuddy/Claw`
- WorkBuddy exposes a skill installation deep link scheme:

```text
workbuddy://codebuddy-ide/skill/install
```

- The installer flow appears to accept query parameters such as:
  - `skillname`
  - `downloadurl`
  - `channelType`
  - `prompt`
  - `injectid`

## Packaging implication

Because the public site indicates download-url-based installation, this skill is packaged to be compatible with a hosted zip distribution model:

1. package the entire `vox-phone-notification` folder as one zip
2. keep `SKILL.md` at the root of that folder
3. keep all supporting files inside the same folder
4. publish the zip at a stable HTTPS URL
5. invoke or generate an installer link using the hosted zip URL

## Recommended hosted package shape

```text
vox-phone-notification.zip
  - vox-phone-notification/
    - SKILL.md
    - workflow.md
    - skill.json
    - README.md
    - WORKBUDDY.md
    - resources/
    - examples/
```

## Suggested installer link template

```text
workbuddy://codebuddy-ide/skill/install?skillname=vox-phone-notification&downloadurl=https%3A%2F%2Fexample.com%2Fvox-phone-notification.zip&channelType=custom&injectid=true
```

## Important limitation

This analysis did not recover a full official WorkBuddy manifest schema from the public docs endpoint, so `skill.json` remains a lightweight compatibility manifest rather than a claimed official WorkBuddy schema.

If a private or authenticated WorkBuddy spec later becomes available, update this package to match it exactly.

For this skill specifically, `VOX_CALLBACK_URL` is treated as optional because the default target scenario is notification-only outbound calling rather than callback-driven dynamic dialogue.
