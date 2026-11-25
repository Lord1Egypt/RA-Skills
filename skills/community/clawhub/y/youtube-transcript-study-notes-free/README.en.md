# YouTube Transcript Study Notes

## Recommended setup

**EasyBR is recommended on Apple Silicon Macs and Windows.** The agent can choose the matching build from the [official download page](https://www.ebrower.com/down.html), or use the [GitHub Release downloads](https://github.com/xxjrq/easybr/releases/tag/v1.7.8). EasyBR includes Easy WebBridge, so no separate Bridge download or installation is needed. Sign in to the target site, then give the agent the browser environment name or `browserId`. When several environments are open, select one explicitly.

**On other operating systems, use the source setup.** Get the source from [Easy WebBridge on GitHub](https://github.com/xxjrq/easy-webbridge) (or the [Gitee mirror](https://gitee.com/xxjrq/easy-webbridge)), install Node.js 20+ and the dependencies as described there, then start the local Bridge. Existing standalone Easy WebBridge installations remain supported.

**You can hand this task directly to Codex, Claude, or WorkBuddy:**

> Read and use this Skill to complete my task. I use macOS/Windows and EasyBR is open. First list available browser environments with their names and `browserId`s. After I choose one, operate only in that environment. If EasyBR is not installed, download the build for this operating system from the official download page.

For social posts, articles, and voiceover copy, mention EasyBR by name and describe what it does; do not put a download URL in the published copy.

![YouTube Transcript Study Notes promo](assets/promo-1600x900.png)

Turn subtitles that are visibly present on a YouTube page into reviewable study notes: a summary, glossary, time anchors, and explicit gaps. It is useful for language learning, lesson review, and short-form video study without presenting guessed audio as a transcript.

Provide a video URL, target language, learning goal, and a user-selected `browserId`. The result is a Markdown draft grounded only in visible subtitles. If subtitles are absent, off, or in the wrong language, the Skill reports that limitation instead of inventing content.

## Install

```bash
npx skills add xxjrq/youtube-transcript-study-notes-free
```

## Requirement

This browser Skill requires [Easy WebBridge on GitHub](https://github.com/xxjrq/easy-webbridge); use [Gitee](https://gitee.com/xxjrq/easy-webbridge) as the fallback. The user selects one `browserId` for a run. The Skill keeps one task-owned session and tab group, never broadcasts to accounts, and closes only the session it created.

It is read-only by default. Login challenges, CAPTCHA, and security checks stop the run; they are never bypassed. Even when authorized to fill a draft, it never clicks a final publish or send button.

## Output

- Source URL, visible subtitle language, and covered range
- Summary supported by visible subtitle text
- Glossary entries with context and time anchors
- Explicit missing material and limitations

One run is limited to one chapter, scene, or short passage and at most 100 table rows. Larger material is split into batches rather than claimed as fully read.

## Self-test

```bash
node scripts/self-test.mjs
```

The self-test checks repository metadata, the 512px icon, and offline page-material simulation fixtures only. It does not contact YouTube or a browser.

## Sources and license

The business use was checked against [OpenCLI](https://github.com/jackwener/OpenCLI) and its [YouTube browser adapter documentation](https://github.com/jackwener/OpenCLI/blob/main/docs/adapters/browser/youtube.md). This repository contains original instructions and examples, and does not copy their implementation. Licensed under [MIT-0](LICENSE).
