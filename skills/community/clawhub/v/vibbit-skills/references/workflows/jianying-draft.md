# Hand off to the desktop client for a Jianying draft

Use for a Jianying draft, continued editing in Jianying, or opening/installing the desktop client. Cloud editing still follows [production paths](hybrid-video.md). The current OpenAPI path cannot obtain the real editing Job ID required by the client, so do not promise direct draft export for Skill-generated outputs. A separately obtained valid Job ID is required for task-prefilled launch. Installation guidance or opening with a known ID does not require OpenAPI key setup.

## Establish the real Job ID

First establish whether a separately obtained editing Job ID already exists for the adopted output and the client's converter. If the user supplies one, retain its source/version and let the client validate it. Preserve IDs as strings to avoid long-integer precision loss. When a formal API exposes this information in the future, verify its published contract before integrating it; do not assume response fields in advance.

Without a real Job ID, mark draft export as blocked by the current API gap. Preserve the existing output, OpenAPI task_id, adopted assets and production records for later recovery. Do not create a task-prefilled URI, repeatedly poll for an unavailable field or ask customers to find an inaccessible internal ID. A verified official work page containing this exact output and a Save to Jianying entry can provide a manual route; do not assume OpenAPI outputs appear in website work lists.

If a draft is an additional deliverable, deliver the completed video and explain that draft export is unavailable. If an editable draft is the sole goal, disclose the blocked endpoint before paid production. An MP4 can be manually imported into Jianying as an ordinary asset, but it does not restore the original separate tracks, subtitles or editable packaging; use that alternative only if the user accepts it.

OpenAPI task_id, material IDs, video URLs, template IDs and local audiovisual plans are not editing Job IDs. Do not invent IDs, use private website endpoints or resubmit paid jobs to obtain one. Installing the client does not resolve this API gap.

## Client installation and preparation

Use the customer's actual computer and account site, not the cloud Agent's machine. Reuse local app/protocol inspection when available. Otherwise report installation status as unknown and ask only for needed OS or Mac-chip information. One unresponsive launch does not prove absence: browser restrictions or pending permission may prevent opening.

When absent, proactively open `/download` on the current account site: [China download page](https://app.vibbit.cn/download) or [international download page](https://app.vibbit.ai/download). Let that page provide current installers, versions, platform selection and installation instructions. Do not maintain direct installer links, pinned installation versions or alternate download channels in the Skill. If the page is known to be awaiting release, explain that it must go live rather than switching the entry point. When the host cannot open the customer's browser, provide the page link for their own computer.

Follow the page to select Windows, Mac with Apple silicon or Mac with Intel. Extract Windows archives completely and retain companion files; move the Mac client into Applications before launch. Follow the page's current instructions for specific steps.
If the chip is unknown, check About This Mac; an Intel-containing browser UA is not sufficient evidence. On phones, inside WeChat or on remote Agent hosts, provide links for the customer's desktop system browser. If the corresponding site or system has no installer, state that limitation instead of switching to another site’s build or inventing support.

Guide the user to sign in with the work's site/account. For draft conversion, copy the actual draft directory from Jianying settings into the client. Refer first-launch problems to the download page’s installation guidance and let the user perform steps requiring system permissions; installation guidance does not authorize Agent changes to system security settings. Download/install on the user's behalf only when explicitly requested and permitted by the host.

Installation preparation can still be provided when requested without a Job ID, after explaining that installation will not make this task convertible. Once installed and a real ID exists, resume the original job and output. Without an ID, retain the blocked-export state rather than changing it to awaiting user save.

## Open and prefill

The existing China-site Jisi client uses this protocol. Establish that the host can access the customer's computer, that the client is installed with the relevant scheme registered, and that the job site matches the client environment. Do not assume China-client support applies to international accounts, test environments or every platform.

```text
agentcy://open?job_id=<URL-encoded real editing Job ID>
```

Encode the real ID as a URL query parameter using host facilities. Include only `job_id`, with no credentials or extra parameters. Never execute the placeholder. Use the host's supported system-protocol opener within the user's existing request to open the client or prepare a draft, without asking again.

The verified client version 1.1.6 opens the draft-conversion tab, fills the Job ID and validates it. The protocol does not save a draft automatically. At this stage, do not add `auto_save`, automatically click Save, or treat the internal Wails bridge as a public API.

If the client is absent, follow installation guidance first. With a real ID but no access to the customer's desktop or no system-protocol opener, provide the real link and copyable Job ID for local use. If the link is not actionable, the user can paste the ID into the client. Opening an app remotely does not open the customer's client. An explicit app-only request may use `agentcy://open`, but opening without an ID is not a task handoff.

## Stop at the user-save handoff

After observing the correct task in the client, say that the task is ready there and ask the user to click the client's Save to Jianying Draft button. If the draft directory has not been configured, guide the user to obtain the actual directory from Jianying settings and configure it in the client.

If only an open request was sent, report that an open was requested; if only a link was provided, say the user needs to open it. A successful launch, valid ID or website saving toast is not proof of a written draft. After the user clicks Save, the client converts the timeline, downloads media and writes the local draft. This workflow does not guarantee lossless conversion of every cloud effect into editable tracks.

Retain any actual Job ID/source, adopted version and valid protocol link in the private production record. Track export eligibility separately from client installation/handoff. Without an ID, mark draft export blocked; only with an ID can handoff be awaiting installation, entry provided, opening requested or awaiting user save. Do not mark the draft saved early. If later asked to confirm completion, verify the client completion message or actual draft, distinguishing user reports from Agent inspection. Missing confirmation does not justify repeating conversion automatically.
