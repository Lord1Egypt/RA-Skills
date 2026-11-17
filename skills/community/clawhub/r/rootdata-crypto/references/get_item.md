# Project details

`POST https://api.rootdata.com/open/skill/get_item`

Send `Authorization: Bearer {ROOTDATA_SKILL_KEY}`, `Content-Type: application/json`, and optionally `language: cn` (default: `en`).
Success envelope: `{"result":200,"data":...}`. Fields without source data can be null or absent.

Pro-level project fields are available. Set `include_team` and `include_investors` as needed (both default to false). `project_id` takes precedence over `contract_address`. RD growth fields are `rd_score` and `rd_rank`; RD heat is `rd_hot_index`. Do not confuse these with X `heat`/`influence`. `similar_project` is currently not populated by the query implementation; do not promise it.

## Request body

| Field | Type | Required | Meaning |
|---|---|---|---|
| `project_id` | int | false | One of project_id or contract_address is required. |
| `contract_address` | string | false | One of project_id or contract_address is required. |
| `include_team` | boolean | false | Whether to include team member information, default is false. |
| `include_investors` | boolean | false | Whether to include investor information, default is false. |

## Response fields

| Field | Type | Meaning |
|---|---|---|
| `project_id` | int | Project ID |
| `project_name` | string | Project Name |
| `logo` | string | The URL of the project logo. |
| `token_symbol` | string | Token Ticker |
| `establishment_date` | string | Establishment date |
| `one_liner` | string | A brief introduction. |
| `description` | string | Detailed introduction |
| `active` | boolean | true: Active; false: Inactive |
| `total_funding` | decimal | Total fundraising amount |
| `countries` | array | Where the company operates (Country/Region) |
| `rd_score` | decimal | RD Growth Index score |
| `rd_rank` | int | RD Growth Index ranking |
| `rd_hot_index` | decimal | RD Hot Index |
| `tags` | array | Project tags (array of tag names) |
| `rootdataurl` | string | The RootData link corresponding to the project. |
| `transparency` | string | Transparency score |
| `project_type` | string | Crypto or Non-Crypto |
| `investors` | array | Investor Information |
| `investors.type` | int | Type: 1 Project 2 VC 3 People |
| `investors.invest_id` | int | Investor ID |
| `investors.name` | string | Name of the investor |
| `investors.logo` | string | Investor Logo |
| `investors.lead_investor` | int | Is it a lead investor? 1: Yes, 0: No |
| `social_media` | array | Social media link |
| `social_media.website` | string | Official website |
| `social_media.X` | string | X link |
| `social_media.discord` | string | Discord link |
| `social_media.linkedin` | string | LinkedIn link PRO |
| `social_media.gitbook` | string | Gitbook link |
| `social_media.cmc` | string | CMC ID PRO |
| `social_media.coingecko` | string | COINGECKO ID PRO |
| `social_media.medium` | string | Medium link |
| `social_media.defillama` | string | Defillama link PRO |
| `social_media.github` | string | GitHub link PRO |
| `similar_project` | array | Similar projects |
| `similar_project.project_id` | int | Project ID |
| `similar_project.logo` | string | Project Logo URI |
| `similar_project.project_name` | string | Project Name |
| `similar_project.brief_description` | string | Project Overview |
| `ecosystem` | array | Project's associated ecosystem (array, ecosystem name, not distinguishing between testnet and mainnet) PRO |
| `on_main_net` | array | Mainnet launched (array, ecosystem name) PRO |
| `plan_to_launch` | array | Planned ecosystem (array, ecosystem name) PRO |
| `on_test_net` | array | Testnet launched (array, ecosystem name) PRO |
| `fully_diluted_market_cap` | string | Fully diluted market capitalizationPRO |
| `market_cap` | string | Market capitalization PRO |
| `price` | string | Price PRO |
| `event` | array | Major Project Events PRO |
| `event.hap_date` | string | Time of the event |
| `event.event` | string | Event content |
| `reports` | array | News dynamic data PRO |
| `reports.title` | string | News headline |
| `reports.url` | string | News link |
| `reports.site` | string | News sources |
| `reports.time_east` | string | Publication time of the news (UTC+8) |
| `team_members` | array | Team Member Information PRO |
| `team_members.head_img` | string | Logo |
| `team_members.name` | string | Name |
| `team_members.position` | string | Position |
| `team_members.X` | string | X Link |
| `team_members.linkedin` | string | LinkedIn Link |
| `team_members.people_id` | long | People ID |
| `team_members.start_employ` | string | Employment Start Date |
| `team_members.end_employ` | string | Employment End Date |
| `former_team_members` | array | Former Team Member Information PRO |
| `former_team_members.head_img` | string | Logo |
| `former_team_members.name` | string | Name |
| `former_team_members.position` | string | Position |
| `former_team_members.X` | string | X Link |
| `former_team_members.linkedin` | string | LinkedIn Link |
| `former_team_members.people_id` | long | People ID |
| `former_team_members.start_employ` | string | Employment Start Date |
| `former_team_members.end_employ` | string | Employment End Date |
| `token_launch_time` | string | Token issuance time yyyy-MMPRO |
| `contracts` | array | Smart Contract AddressPRO |
| `contracts.contract_platform` | string | Platform |
| `contracts.contract_address` | string | Address |
| `support_exchanges` | array | Supported exchanges include (exchange name, exchange logo) PRO |
| `heat` | string | X Hot Index PRO |
| `heat_rank` | int | X Hot Ranking PRO |
| `influence` | string | X Influence IndexPRO |
| `influence_rank` | int | X Influence Ranking PRO |
| `followers` | int | Number of followersPRO |
