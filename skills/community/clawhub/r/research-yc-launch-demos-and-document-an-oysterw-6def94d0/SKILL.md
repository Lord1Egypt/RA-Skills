---
name: "generated-research-yc-launch-demos-and-document-an-oysterw-6def94d0"
description: "Research comparable YC launch demos and build a structured Google Doc for OysterWorkflow demo-video planning, including candidates, links, analysis dimensions, observations, and script ideas."
---

# Research YC launch demos and document an OysterWorkflow demo-video plan

## Description

This skill supports OysterWorkflow launch/marketing video research. It uses ChatGPT recommendations, public YC Startup Directory and Launch YC pages, embedded launch videos, and Google Docs to identify comparable AI-agent/workflow products, inspect their positioning, watch demos, and document structured notes. The output is a Google Doc containing the video-research plan, demo candidates, YC links, reusable evaluation dimensions, observations, customer angles, and script inspiration for future OysterWorkflow videos.

## Goal

Create a structured Google Doc that captures demo-video candidates, analysis criteria, notes, and script inspiration for producing OysterWorkflow launch/marketing videos.

## When to Use

- Use when planning OysterWorkflow launch, website hero, investor, Twitter/X, LinkedIn, or paid-distribution demo videos.
- Use when researching how YC companies present AI agents, browser automation, computer-use workflows, workflow replay, RPA replacement, or agent infrastructure.
- Use when you want a structured Google Doc that turns video watching into comparable notes and concrete script ideas.

## When Not to Use

- No explicit exclusions in source skill.

## Prerequisites

- Google Chrome is available.
- The user can access ChatGPT or another source of initial comparable-company recommendations.
- The user can access public YC Startup Directory and Launch YC pages.
- The user can edit Google Docs.

## Inputs

- Google account access: User must be signed into a Google account that can create or edit the target Google Doc.
- Target document choice: User should confirm whether to use the existing Google Doc titled “demo 计划 1” or create a new document.
- Number of demos to analyze: Default is 10 demos, but the user can provide a different number.

## Outputs

- Structured demo-research Google Doc: A Google Doc containing the research plan, YC/demo links, evaluation criteria, per-video notes, audience/customer angles, and OysterWorkflow script inspiration.
- Reusable evaluation framework: A repeated table/checklist for comparing launch videos across hook, pain point, magic moment, demo credibility, target user, differentiation, CTA, format, shots to copy, and mistakes to avoid.

## Assets

- Google Doc title: demo 计划 1
- ChatGPT conversation title: Let AI mimic your skill - yc公司demo查找请求
- Primary product being researched: OysterWorkflow / Let AI mimic your skill: observes human computer-use trajectories, generates reusable workflow skills, replays known paths, and falls back to AI/human for unknown paths.
- YC Launch page: https://www.ycombinator.com/launches
- YC Startup Directory: https://www.ycombinator.com/companies
- Kernel Launch YC link: https://www.ycombinator.com/launches/05f-kernel-crazy-fast-browser-infrastructure
- Zenbu Launch YC link: https://www.ycombinator.com/launches/Qey-zenbu-the-extensible-ide-for-managing-coding-agents
- Zenbu embedded video URL: https://www.youtube.com/watch?v=ZUbY8zdv7Rc
- Browser Use YC company page context: Browser Use — Leading open-source web agent project with 50k stars in 3 months; website https://browser-use.com; YC Winter 2025.
- Demo-video evaluation dimensions: 前5秒 hook；痛点是否具体；魔法时刻时间点；demo 可信度；目标用户；差异化；CTA；视频形式；可抄的镜头；不该学的地方。
- Evaluation guiding questions: 它第一句话/第一屏怎么抓人？是泛泛讲 AI automation，还是具体讲某个 workflow？第几秒看到“哇，这东西有用”？是真实录屏，还是概念动画？它到底在跟谁说话：ops、developer、founder、enterprise？它怎么证明自己不是又一个 agent/RPA？最后让用户做什么？真人、旁白、录屏、动画比例各多少？哪 3 个镜头可以借鉴？哪里太慢、太虚、太复杂？
- Initial video-production plan: 1. 10个demo视频，主要是我这个行业的，少数几个不同行业的；2. 分析3类潜在顾客类型；3. 一边做前两者一边记录我的想法；4. 想法整理成脚本，可能有几类；5. 制作视频素材；6. 制作视频；7. 投流。
- OysterWorkflow script inspiration: 主推脚本方向：Watch me once. Run it forever. 强调多数业务流程不在 API 里，而在员工如何使用软件里；人类专家操作一次，OysterWorkflow 学会并生成可复用 skill，下次自动 replay，异常时由 AI/人接管。

## Steps

1. Open Google Chrome and start from the existing ChatGPT conversation about YC demo research for OysterWorkflow / “Let AI mimic your skill.” Review the recommendations for comparable YC companies and launch pages.
   Intent: Use ChatGPT as the research brief and candidate source before browsing YC pages.
   Operation App: Google Chrome
   Hints: Prioritize companies whose demos relate to AI agents, computer use, workflow automation, observing human operations, replaying learned workflows, RPA, browser agents, or agent infrastructure.; The trace emphasized that public YC Demo Day pitches are usually private, so focus on public YC Startup Directory and Launch YC pages, especially pages with embedded YouTube/Loom/demo videos.

2. Extract the most relevant YC demo candidates and the positioning angles from ChatGPT’s answer. Keep Sola, Skyvern, Cyberdesk, AutoComputer, CopyCat, RamAI, Browser Use, BrowserOS, Intuned, Zenbu, and Kernel as candidate references when relevant.
   Intent: Build a shortlist of comparable companies and clarify what to learn from each demo.
   Operation App: Google Chrome
   Hints: For Sola, note the “screen recording to bot” / “watch me do it once” angle.; For Skyvern, note the Explore → Replay architecture: observe/explore a workflow, compile to deterministic Playwright replay, and fallback to AI when needed.; For Cyberdesk, note memorized steps plus unexpected popup fallback.; For AutoComputer, note human-in-the-loop prediction of next keyboard/mouse actions.

3. Open the YC Startup Directory and Launch YC pages in Chrome. Use the YC navigation and filters/search to find AI/B2B/devtools/automation-related companies and launch posts.
   Intent: Move from ChatGPT’s recommendations into primary source pages on YC.
   Operation App: Google Chrome
   Hints: The user navigated through YC Companies, Startup Directory, and Launch YC.; On Launch YC, use filters such as AI, B2B, Devtools, SaaS, and relevant batches such as Spring 2026 or Winter 2025 when needed.

4. Open a relevant YC company or Launch YC page, inspect its headline, one-line description, batch, category tags, website link, and whether the page contains an embedded launch video.
   Intent: Collect stable references and determine which pages are worth deeper demo analysis.
   Operation App: Google Chrome
   Hints: Example inspected page: Browser Use — “Leading open-source web agent project with 50k stars in 3 months.”; Example inspected Launch YC page: Zenbu — “The extensible IDE for managing coding agents.”

5. When a Launch YC page has an embedded video, play the video directly on the page and watch for structure, narration, product positioning, demo credibility, and the first visible “magic moment.”
   Intent: Analyze launch video execution rather than only reading the written launch copy.
   Operation App: Google Chrome
   Hints: For Zenbu, watch the embedded YouTube launch video and note that it opens by saying Zenbu is a coding agent orchestrator for the Pi coding agent.; The Zenbu video demonstrates that every feature in the app is implemented as a plugin, so the agent can create plugins and add features into the app in real time.; The Zenbu demo example asks the agent to make a slash command /context or a tree slash command to visualize context/session history, then shows files being created and UI updates appearing.; Look for whether the video is mostly real screen recording, product UI, narration, subtitles, or concept animation.

6. Open or switch to the Google Doc used for the research plan, titled “demo 计划 1,” and maintain it as the central working document.
   Intent: Record the video-research plan, candidate links, evaluation framework, observations, and script ideas in one structured document.
   Operation App: Google Chrome
   Hints: Use Google Docs editing mode.; Let the document autosave after major edits.

7. At the top of the Google Doc, write the overall plan as a numbered workflow: watch 10 demo videos, mostly from the same industry and a few from other industries; analyze three potential customer types; record thoughts while doing the first two phases; turn ideas into several scripts; create video assets; produce videos; and run distribution/ads.
   Intent: Define the research-to-production pipeline before collecting individual notes.
   Operation App: Google Chrome
   Hints: No explicit hints.

8. Create a reusable evaluation table for every demo video. Copy the dimensions exactly enough to reuse them for each candidate: 前5秒 hook, 痛点是否具体, 魔法时刻时间点, demo 可信度, 目标用户, 差异化, CTA, 视频形式, 可抄的镜头, 不该学的地方.
   Intent: Standardize how each launch/demo video is analyzed.
   Operation App: Google Chrome
   Hints: The spoken guidance was: “Just copy these dimensions.”; For each dimension, preserve the guiding questions: how the first line/screen grabs attention; whether the pain point is generic AI automation or a concrete workflow; when the viewer feels the product is useful; whether the demo is real screen recording or concept animation; who the video speaks to; how it proves it is not just another agent/RPA; what CTA it uses; the ratio of human, voiceover, screen recording, and animation; which three shots can be copied; and what is too slow, vague, or complex.

9. For each watched demo, add a numbered subsection under the evaluation framework, paste the YC Launch URL, and fill in observations against the dimensions.
   Intent: Turn each video into comparable research notes instead of loose impressions.
   Operation App: Google Chrome
   Hints: The document used sections such as 1.1, 1.2, and 1.3.; For the first analyzed demo, the notes included: real-person intro; first 5 seconds explain what the product is; about 10 seconds of more detailed explanation; then a real example and outcome; the workflow felt somewhat generic; the product experience could be shown more precisely; the magic moment was around 36 seconds using a quantitative result; demo credibility was real screen recording; the target was sales but mixed in too much technical content; CTA asked users to imagine what they could do with the product; the format mixed human presentation, screen recording, work animation, and likely staged software recording.

10. Add Kernel as a numbered candidate in the Google Doc by pasting its Launch YC link and writing script inspiration for a technical automation/workflow audience.
   Intent: Capture an infrastructure-oriented reference and convert it into OysterWorkflow script angles.
   Operation App: Google Chrome
   Hints: Kernel link used: https://www.ycombinator.com/launches/05f-kernel-crazy-fast-browser-infrastructure; Script angle recorded: for people who understand automation/workflows, emphasize no code and no prompt writing; 24-hour recording in a real environment; converting operations into a harness; for example, automatically checking whether a website runs smoothly by opening pages and filling forms, now with one-click recording.; Additional audience angles recorded: for sales, emphasize embedded operating experience; for bosses, frame it as turning the best employee into an AI employee and doubling the best employee.

11. Add Zenbu as another numbered candidate in the Google Doc by pasting its Launch YC link and copying the same evaluation dimensions beneath it for later analysis.
   Intent: Set up the next demo-analysis slot after watching the Zenbu video.
   Operation App: Google Chrome
   Hints: Zenbu link used: https://www.ycombinator.com/launches/Qey-zenbu-the-extensible-ide-for-managing-coding-agents; After pasting the link, add the same dimensions table/questions underneath so the Zenbu video can be analyzed consistently.

12. While watching and documenting, synthesize possible OysterWorkflow positioning and script ideas in the Google Doc rather than waiting until all videos are finished.
   Intent: Convert research into usable launch-video directions as insights appear.
   Operation App: Google Chrome
   Hints: Strong positioning from ChatGPT to preserve: “OysterWorkflow turns successful human computer-use trajectories into reliable, reusable AI skills.”; Main script concept: “Watch me once. Run it forever.”; Product contrast: do not present it as just another AI agent that clicks around; emphasize that a human expert demonstrates once, OysterWorkflow learns, generates a reusable skill, replays deterministically for known paths, and falls back to AI/human for unknown paths.; Suggested CTA: “Send us a workflow your team still does by hand. We’ll turn it into an AI skill.”

13. Verify that the Google Doc has saved and contains the plan, reusable evaluation dimensions, at least the Kernel and Zenbu YC links, and current script inspiration before leaving the session.
   Intent: Close the research pass with a durable, reusable planning document.
   Operation App: Google Chrome
   Hints: Google Docs showed “Saved to Drive” / saving status during the trace.; If the page is still saving, wait until the save status confirms before switching away.

## Success Criteria

- The Google Doc contains the numbered research-to-production plan.
- The document includes the reusable demo-video evaluation dimensions and guiding questions.
- At least one or more YC demo candidates are recorded with stable links.
- Watched videos have notes about positioning, target user, demo credibility, and script inspiration.
- The document is saved in Google Docs before the session ends.

## Failure Modes

- No explicit failure modes in source skill.

## Fallback

- LLM did not generate this field successfully
- Warning: LLM output missing fallback; used placeholder.
- Warning: Generalization skipped: component disabled by configuration.
- Warning: Planner optimization skipped: component disabled by configuration.

## Examples

- No explicit examples in source skill.

