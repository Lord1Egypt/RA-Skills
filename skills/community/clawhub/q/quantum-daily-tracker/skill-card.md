## Description: <br>
量子科技论文追踪与速览生成。用于每日追踪量子计算、量子网络、量子纠错等领域最新论文，生成中文笔记和每日速览。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QingquanYao](https://clawhub.ai/user/QingquanYao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Researchers, engineers, and developers use this skill to track quantum computing, quantum networking, quantum error correction, and related papers from public RSS feeds, then generate Chinese Markdown paper notes and daily digests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Daily or catch-up runs may write tracker output or state to an unexpected local path. <br>
Mitigation: Confirm the quantum-tracker output paths and memory/last-run.txt location before enabling scheduled runs. <br>
Risk: An incorrect last-run state can cause the tracker to process the wrong date range. <br>
Mitigation: Reset memory/last-run.txt when the tracker needs to restart from a known date range. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/QingquanYao/quantum-daily-tracker) <br>
- [arXiv Quantum Physics RSS](http://export.arxiv.org/rss/quant-ph) <br>
- [Nature npj Quantum Information RSS](https://www.nature.com/npjqi.rss) <br>
- [Science RSS feed](https://www.science.org/action/showFeed?type=etoc&feed=rss&jc=science) <br>
- [PRX Quantum RSS](http://feeds.aps.org/rss/recent/prxquantum.xml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown paper notes, daily digests, and dashboard summaries in Chinese] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains local tracker state in memory/last-run.txt and writes Markdown under quantum-tracker paths when executed by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
