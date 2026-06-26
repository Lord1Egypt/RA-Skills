# SKILL: getAddressBalance

## Description
A skill for querying the balance of a specified blockchain address using the Tokenview API.  
The default supported coin is **BTC**, and the API Key must be provided through the environment variable `TOKENVIEW_API_KEY`.

## Triggers
- "What is the balance of BTC address `<address>`?" or "How much BTC does `<address>` have?"
- Any conversation where an address is detected and interpreted as a balance query

## API Endpoint and Secret Handling
- Tokenview API：`https://services.tokenview.io/vipapi/addr/b/{lowercase-coin-abbr}/{address}?apikey={apikey}`
- Using environment variable `TOKENVIEW_API_KEY` to config API Key。
- Parameters：`lowercase-coin-abbr` is coin abbreviation in lowercase (default: `btc`)，`address` blockchain address extracted from the conversation
- Output format：The script returns JSON

## Parameters
- address:The Blockchain address
- coin:Coin abbreviation, default is btc

## Output Format
- Success:The script returns JSON , and the user sees："Balance is {balance} {COIN}"
- Failure:Example raw Tokenview API JSON:
  ```json
  {
    "code": 1,
    "msg": "404",
    "data": "NONE"
  }
  ```
  will be like: "Balance query failed：Code=1, Msg=404, Data=NONE"

## Implementation (execution plan)
- The skill executes the tokenview_api.py script to perform the API call:
  - Example command (BTC):
    ```bash
    python $OPENCLAW_STATE_DIR/workspace/skills/tokenview_balance_checker/tokenview_api.py <address> --coin btc
    ```
- Script information:
  - Path: `$OPENCLAW_STATE_DIR/workspace/skills/tokenview_balance_checker/tokenview_api.py`
  - Inputs: address (required)，coin (optional, default is btc)
  - Dependencies: requests
  - API Key: Provided via environment variable TOKENVIEW_API_KEY
  - Output: JSON printed to stdout, e.g.:`{"code":1,"msg":"success","data":"0.123 BTC"}`

## Parameters (payload-driven)
- address: blockchain address to query
- coin: currency abbreviation (default: btc)

## Output Mapping (to user-facing text)
- Success: "Balance is {balance} {COIN}"
- Failure: "Code={code}, Msg={msg}, Data={data}"

## Example
- Input: "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa 余额多少？"
- Script output: {"code":1, "msg":"成功", "data":"0.12345678 BTC"}
- User visible: 余额为 0.12345678 BTC