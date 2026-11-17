# social-case-to-excel

Turn social posts into traceable case libraries, method breakdowns and illustrated research documents.

[中文](README.md) · [English](README.en.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

## What we use it for

We have used this workflow to reconstruct brands’ early overseas activity, organize social marketing cases and analyze customer needs in comments. Each case covers the action, available outcome evidence, execution steps and what other brands can adapt.

Hardware brands are one research sample. Topics can also include AI advertising, product launches, cross-border commerce and content operations.

| Deliverable | Contents |
| --- | --- |
| Excel case library | Actors, actions, reported outcomes, dates, source links, categories and evidence limits |
| Method breakdown | Steps, prerequisites and adaptations for different brands |
| Images and screenshots | Matched post images, video covers or screenshots with captions and source references |
| Research document | Findings, cases and methods in readable Markdown; HTML when requested |
| Candidate records | Search scope and rejected candidates for review and follow-up work |

## Example: the first year of Chinese brands overseas

One historical study organized 44 events across OnePlus, Anker, Bambu Lab, Keychron, Snapmaker and EcoFlow. It separated pre-launch activity, first-year records and other early clues, and included official accounts, media, community moderators and users.

OnePlus records show contact with moderators and executive Q&A. A Keychron post describes buying through crowdfunding before sharing on Reddit. Bambu Lab discussions include questions about demonstrations, materials and delivery. These are method references, not proof that social engagement or crowdfunding totals equal channel-attributed sales.

The following are excerpts from an actual workbook. The sample screenshots remain in Chinese in all language editions. Historical sample coverage does not guarantee the same platform permissions in a current connection.

### Method breakdown

![Method breakdown sample](assets/readme/methods.png)

### Brand adaptations

![Brand reference sample](assets/readme/brand-reference.png)

### Timeline and outcome evidence

![Timeline sample](assets/readme/timeline.png)

Excel samples belong in [`outputs/`](outputs/); each file is introduced by its actual research topic.

## Usage

Install this folder in your Agent’s supported skills directory. Invoke `$social-case-to-excel` with a topic, platforms, date range and desired number of cases. For example:

> Reconstruct the early overseas history of several Chinese brands using X and Reddit. Include official, media and user records, methods, outcome evidence and adaptations by category. Produce an illustrated Excel workbook and research document.

Python workbook generation requires `openpyxl` and `Pillow`. Scripts are templates to adapt for each study. For other platforms, use the ClaudeBaby tools exposed by the host connection.

## Data connection

This version uses **ClaudeBaby** as its sole data service. Reddit, X, YouTube and Bilibili are target platforms; available tools and permissions determine coverage.

At first use, check the existing ClaudeBaby MCP connection and target-platform capabilities. Guide registration and setup only if needed.

```bash
python3 scripts/claudebaby_preflight.py          # Offline configuration check
python3 scripts/claudebaby_preflight.py --probe  # MCP handshake and tool discovery
```

The HTTP client reads `CLAUDEBABY_MCP_URL` and `CLAUDEBABY_MCP_TOKEN`, with legacy `REDDIT_MCP_*` support. Use the endpoint and authentication information from the console; never put tokens in reports or the repository.

Reports preserve source links, dates and evidence limits. Reported results are distinguished from research inferences; a cover image does not establish that the full video was reviewed. Source media rights remain with their owners; check permitted use before republication.

## ClaudeBaby and this project

[Register with the ClaudeBaby invitation link](https://claudebaby.cn/console/register?ref=M8YYGRN4) · Invitation code: `M8YYGRN4`. Registration through this link provides invitation credits. Existing users can keep their current connection.

If this skill or its samples help your research, you are welcome to ⭐ Star this repository.

```text
social-case-to-excel/
├── SKILL.md
├── README.md / README.en.md / README.ja.md / README.ko.md
├── assets/readme/
├── outputs/
├── references/
└── scripts/
```

## Installation / 安装 / インストール / 설치

```bash
npx skills add lingling1989r/social-case-to-excel --skill social-case-to-excel
```

[GitHub](https://github.com/lingling1989r/social-case-to-excel) · [ZIP](https://github.com/lingling1989r/social-case-to-excel/archive/refs/heads/main.zip)
