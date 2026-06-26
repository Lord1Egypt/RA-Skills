# Sina futures normalized fields

This skill normalizes the commonly useful front part of the Sina quote payload.

## Normalized fields

- `code`: requested contract code
- `name`: contract name returned by Sina
- `date`: trading date string from payload
- `time_hms`: HHMMSS-like time string from payload
- `open`: open price
- `high`: session high
- `low`: session low
- `last`: latest price
- `bid`: best bid-like field from payload
- `ask`: best ask-like field from payload
- `prev_close_or_settle`: previous close or settlement-like field
- `settle_or_avg`: settlement or average-like field
- `bid_vol`: bid volume-like field
- `ask_vol`: ask volume-like field
- `volume`: volume
- `open_interest`: open interest
- `exchange_short`: short exchange marker such as `沪`
- `product_name`: product name such as `白银`
- `raw_fields`: full raw field array for debugging

## Caveats

- Sina does not provide an official field dictionary for this public webpage payload in this skill.
- The first several fields are usually stable enough for quote display.
- Later fields may vary by contract family and should be validated before being treated as authoritative business fields.
- Empty results usually mean the code is unsupported, inactive, unavailable in the current source, or no data is exposed by Sina for that code.
