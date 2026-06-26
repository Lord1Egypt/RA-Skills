# Create Order Analysis

Use this reference when you need the previously collected notes about the mini-program `createOrder` API and its signing assumptions.

- API: `/miniprogram/areaOrder/createOrder`
- Related precheck API: `/miniprogram/areaOrder/createOrderCheck`
- Embedded private key appears in `config/signKey.js`
- `utils/http.js` injects `x-gym-client-id` and `token-user`
- `createOrderReq(data, header)` passes the caller-provided custom header through unchanged

The exact runtime construction of `X-Ca-Signature` was not recovered from the available extracted bundles, so replay and public-key verification remain the safest local debugging tools.
