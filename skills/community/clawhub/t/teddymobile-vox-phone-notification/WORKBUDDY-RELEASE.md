# WorkBuddy Release Guide

Use this guide when you want to publish `vox-phone-notification` as a downloadable WorkBuddy Claw skill package.

## Release goal

Prepare one hosted zip file and one installer link.

## Package contents

The published zip should contain this root structure:

```text
vox-phone-notification/
  SKILL.md
  workflow.md
  skill.json
  README.md
  SKILLHUB.md
  WORKBUDDY.md
  WORKBUDDY-RELEASE.md
  examples/
  resources/
```

## Build the zip

From the repository root, package the skill folder as a zip file named:

```text
vox-phone-notification.zip
```

Recommended archive rule:

- keep the top-level folder name `vox-phone-notification`
- do not zip only the inner files
- do not exclude `SKILL.md` or `workflow.md`

## Host the zip

Upload the zip to a stable HTTPS URL, for example:

```text
https://your-domain.example/skills/vox-phone-notification.zip
```

Requirements:

- public HTTPS access
- direct download without login
- stable filename and URL

## Build the WorkBuddy installer link

Use this template:

```text
workbuddy://codebuddy-ide/skill/install?skillname=vox-phone-notification&downloadurl=<URL_ENCODED_ZIP_URL>&channelType=custom&injectid=true
```

Example:

```text
workbuddy://codebuddy-ide/skill/install?skillname=vox-phone-notification&downloadurl=https%3A%2F%2Fyour-domain.example%2Fskills%2Fvox-phone-notification.zip&channelType=custom&injectid=true
```

## Optional landing page link

If you want to distribute an HTTP link before jumping into WorkBuddy, keep a simple page that shows:

- skill name
- what it does
- one "Install in WorkBuddy" button
- one backup manual download link for the zip

## Pre-release checklist

- `SKILL.md` present at skill root
- `workflow.md` present at skill root
- `skill.json` present at skill root
- zip contains top-level `vox-phone-notification/` folder
- hosted URL can be downloaded in browser
- installer link contains correct URL-encoded `downloadurl`
- required env list reflects notification-only mode by default
- TeddyMobile platform registration and bot configuration have been completed for the target production environment
- at least one real outbound call has been verified with audible notification playback

## Post-release verification

1. open the hosted zip URL directly in browser
2. confirm download succeeds
3. open the WorkBuddy installer link on a machine with WorkBuddy installed
4. confirm WorkBuddy recognizes the skill package
5. confirm the skill content loads and references the expected workflow files
