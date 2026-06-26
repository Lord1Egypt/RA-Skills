## Description: <br>
Searches Twitter/X with keyword or advanced queries, retrieves tweet data through twitterapi.io, and helps agents produce data-driven social media analysis reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flyfoxCI](https://clawhub.ai/user/flyfoxCI) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to search Twitter/X with advanced query syntax and generate social listening, trend, influencer, and engagement reports from retrieved tweets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The wrapper evaluates shell-profile content while loading TWITTER_API_KEY. <br>
Mitigation: Provide TWITTER_API_KEY directly through the process environment and avoid the wrapper unless the eval-based shell-profile parsing is removed. <br>
Risk: The wrapper may install the Python requests package without an approval step. <br>
Mitigation: Preinstall dependencies in a controlled environment before running the skill. <br>


## Reference(s): <br>
- [Twitter API Reference](artifact/references/twitter_api.md) <br>
- [twitterapi.io Advanced Search API](https://docs.twitterapi.io/api-reference/endpoint/tweet_advanced_search) <br>
- [Twitter Advanced Search Syntax](https://github.com/igorbrigadir/twitter-advanced-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON search results and Markdown analysis reports with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a TWITTER_API_KEY credential and may fetch up to 1000 tweets per query.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
