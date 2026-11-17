# Minimal Input

Generate 8 Xiaohongshu cards for a reviewed content package.

- mode: `project_asset`
- output directory: `docs/series/example-theme/assets/xiaohongshu/`
- retry policy: default
- backend: `auto`
- preferred backend: `chatgpt_computer_use`
- paid fallback: disabled

## Jobs

| job_id | source_id | platform_profile | dimensions | intended_filename |
| --- | --- | --- | --- | --- |
| xhs-01 | card-01 | xiaohongshu | 1080x1440 | 01-cover.png |
| xhs-02 | card-02 | xiaohongshu | 1080x1440 | 02-evidence.png |
| xhs-03 | card-03 | xiaohongshu | 1080x1440 | 03-method.png |
| xhs-04 | card-04 | xiaohongshu | 1080x1440 | 04-chain.png |
| xhs-05 | card-05 | xiaohongshu | 1080x1440 | 05-images.png |
| xhs-06 | card-06 | xiaohongshu | 1080x1440 | 06-public-url.png |
| xhs-07 | card-07 | xiaohongshu | 1080x1440 | 07-human-gate.png |
| xhs-08 | card-08 | xiaohongshu | 1080x1440 | 08-reproduce.png |

Prompt rule: run one job per ImageGen call. If exact Chinese text is required, generate the visual background first and use deterministic typography in the downstream renderer.
