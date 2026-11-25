# AI Video Prompt Optimizer (Chinese)

![Chinese AI video prompt optimization](assets/promo-1600x900.png)

Turn a Chinese AI-video brief into a copy-ready final prompt, ordered shot actions, and continuity constraints. Use the result as a clear brief for your video-generation tool. Run the workflow with a skill-capable assistant; no browser or additional API key is required.

It is designed for Chinese social-media creators and small-shop operators. Give the skill an intended visual, an optional draft prompt, optional duration or shot count, and any constraints. If duration and shot count are absent, it assumes one 5–8 second shot and labels that assumption. It returns four concise Markdown sections: final prompt, shot sequence, continuity constraints, and comparison/open questions.

See [fixtures/success-input.md](fixtures/success-input.md) and [fixtures/success-expected.md](fixtures/success-expected.md) for an immediately usable example. The failure fixture demonstrates that a missing subject and visual intent must be requested rather than invented; duration or shot count remains optional.

The writing model (including a user-selected Opus 5.5) is kept separate from the video model. This skill does not silently change the writing model and never invents video-model parameters, seeds, or proprietary syntax. It does not generate video.

Run `node scripts/self-test.mjs` to verify the repository.

Original prompt-writing instructions and examples, licensed under [MIT-0](LICENSE).

## Install

```bash
npx skills add xxjrq/video-prompt-optimizer-cn
```

Alternatively, copy this repository folder into your Agent’s skill directory, then invoke `$video-prompt-optimizer-cn` with your input.
