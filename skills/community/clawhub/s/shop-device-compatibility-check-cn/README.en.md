# Device Accessory Compatibility Check

Provide confirmed device models, accessory specifications, and manufacturer inclusion/exclusion data to receive a per-pair result: confirmed compatible, explicitly incompatible, or unknown—with evidence. A rule without a source cannot confirm compatibility; a satisfied, evidenced exclusion takes priority over a generic inclusion. Connector names such as USB-C without a protocol or function standard remain unknown. Incomplete models, missing table entries, or connector appearance alone trigger a request for more information rather than a compatibility guess.

## Input and output

The tool accepts up to ten devices and ten accessories, plus explicit manufacturer rules and relevant customer conditions. It returns a pair-by-pair comparison with status, evidence, and missing-data requests. It does not test products, guarantee electrical performance, or infer full compatibility from matching plugs.

```bash
npx skills add xxjrq/shop-device-compatibility-check-cn
node scripts/self-test.mjs
```

See the [successful delivery](fixtures/success-output.json) and [insufficient-information delivery](fixtures/failure-output.json).
