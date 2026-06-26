---
description: Send Live-Activities & Ongoing-Notifications to your iOS / Android phones using
  Signalgrid.
homepage: "https://web.signalgrid.co"
metadata:
  clawdbot:
    emoji: 📲
    primaryEnv: SIGNALGRID_CLIENT_KEY
    requires:
      bins:
      - node
      env:
      - SIGNALGRID_CLIENT_KEY
      - SIGNALGRID_CHANNEL
name: signalgrid-activity
---

# Signalgrid Live Activities

Send Live Activities & Ongoing Notifications to your phone through the Signalgrid API.

## When to use

Use this skill whenever the user asks to:  
&nbsp;  
&nbsp;&nbsp;o   &nbsp;start an ongoing notification  
&nbsp;&nbsp;o   &nbsp;update progress of an ongoing notification  
&nbsp;&nbsp;o   &nbsp;show a live activity / live progress  
&nbsp;&nbsp;o   &nbsp;keep a notification updated while something runs (deploy, backup, import, CI job, etc.)  
&nbsp;&nbsp;o   &nbsp;end/finish an ongoing notification  

## Start Live Activity:

```bash
node {baseDir}/skills/signalgrid-activity/signalgrid-activity.js \
  --type start \
  --title "OpenClaw" \
  --body "Starting…" \
  --severity info \
  --steps 1 \
  --progress 10 \
  --progress_legend "true" \
  --start_text "Activity Start" \
  --end_text "Activity End" \
```

## Update Live Activity:

```bash
node {baseDir}/skills/signalgrid-activity/signalgrid-activity.js \
  --type update \
  --token "MX2L2K" \
  --title "OpenClaw" \
  --body "Step 3/6" \
  --severity warning \
  --steps 1 \
  --progress 50 \
  --progress_legend "true" \
  --start_text "Activity Start" \
  --end_text "Activity End" \
```

## End Live Activity:

```bash
node {baseDir}/skills/signalgrid-activity/signalgrid-activity.js \
  --type end \
  --token "MX2L2K" \
  --title "OpenClaw" \
  --body "Done" \
  --severity success \
  --steps 1 \
  --progress 100 \
  --progress_legend "true" \
  --start_text "Activity Start" \
  --end_text "Activity End" \
  --dismissal_delay 60
```

### Parameters

| Name            | Type    | Description |
| :-------------- | :------ | :---------- |
| title           | string  | Activity title. Defaults to `No Title`. |
| body            | string  | Activity body text. Defaults to `No Body`. |
| type            | enum    | Activity phase. Common values: `start`, `update`, `end`. Defaults to `start`. |
| severity        | string  | Mapped to `crit`, `warn`, `success`, `info` (see Notes). |
| start_text      | string  | Optional. Label for the start state. Defaults to `Activity Start`. |
| end_text        | string  | Optional. Label for the end state. Defaults to `Activity End`. |
| steps           | number  | Optional. For the progressbar-prensentation if set to 5, the progressbar has 5 steps. Defaults to `5`. |
| progress        | number  | Current progress value. Defaults to `10`. |
| progress_legend | boolean | Optional. Show progress legend. Defaults to `true` (passed as a string). |
| token           | string  | Optional. only used with update & end messages. is for matching the activity. |
| dismissal_delay | string  | Optional. The delay a activity is shown after end message is sent. Only on end messages |

## Usage

In update & end messages the following parameters need to be taken from start message and retransmitted if not defined otherwise:  

&nbsp;&nbsp;o   &nbsp;title  
&nbsp;&nbsp;o   &nbsp;body  
&nbsp;&nbsp;o   &nbsp;severity  
&nbsp;&nbsp;o   &nbsp;steps  
&nbsp;&nbsp;o   &nbsp;progress_legend  
&nbsp;&nbsp;o   &nbsp;start_text  
&nbsp;&nbsp;o   &nbsp;end_text  
&nbsp;  
Otherwise the activity will change its appearance. 
It is allowed for flexibility, but not needed most of the time.

## Notes

-   Requires a Signalgrid account: https://web.signalgrid.co/
&nbsp;  
&nbsp;  
-   Install the skill:

``` bash
clawdhub --workdir ~/.openclaw install signalgrid-activity
```

-   And ensure your OpenClaw **Tool Profile** is set to `full`  ( Config -> Tools -> Tool Profile )  
&nbsp;  
-   Configure environment variables ( Config -> Environment -> Environment Variables Overrides + Add Entry):

```
SIGNALGRID_CLIENT_KEY=your_client_key_here
SIGNALGRID_CHANNEL=your_channel_name_here
````

&nbsp;  
-   Signalgrid notifications do **not** require a phone number or
    message target.
