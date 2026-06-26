# Session note: mobile detail QA must use the real mobile domain

Date: 2026-05-18

## Trigger

During a live xz01 detail-page repair for `https://www.900az.com/zoszx04/7270.html`, PC bottom modules were adjusted successfully:

- `更多精选攻略`: 4 items, 2 columns × 2 rows on PC.
- `手游推荐`: 8 items, compact 4 columns × 2 rows on PC.
- `猜你喜欢`: 8 items, compact 4 columns × 2 rows on PC.

An independent test initially reported mobile 390px FAIL because the test script emulated a mobile viewport but still navigated to the PC URL `https://www.900az.com/...`. The reported overflow came from PC-only containers such as `.xz-wrap` / `.xz-header-main` at 1200px.

## Correction

For xz01 mobile validation, viewport emulation is not enough. The URL/domain must also be the mobile site:

```text
PC validation:     https://www.900az.com/... with desktop UA
Mobile validation: https://m.900az.com/...   with mobile UA + mobile viewport/CDP metrics
```

A 390px failure on `www.900az.com` is not automatically a mobile-site failure unless the requirement is explicitly to make the PC domain responsive at phone widths.

## Reusable validation pattern

When writing browser/CDP validation scripts, parameterize the URL per case instead of using one global `URL` for PC and mobile cases.

Bad pattern:

```js
const URL = 'https://www.900az.com/path.html';
await Page.navigate({ url: URL }); // reused for both PC and mobile cases
```

Good pattern:

```js
const cases = [
  { name: 'pc', url: 'https://www.900az.com/path.html', mobile: false, width: 1440 },
  { name: 'mobile', url: 'https://m.900az.com/path.html', mobile: true, width: 390 },
];
for (const c of cases) {
  await Emulation.setDeviceMetricsOverride({ width: c.width, height: 844, mobile: c.mobile, deviceScaleFactor: 1 });
  await Network.setUserAgentOverride({ userAgent: c.mobile ? MOBILE_UA : DESKTOP_UA });
  await Page.navigate({ url: c.url });
}
```

## Acceptance evidence to capture

For mobile detail QA, report all of these from the real `m.` URL:

- `location.href` begins with `https://m.900az.com/`.
- `document.documentElement.clientWidth` equals intended viewport width, e.g. `390`.
- `document.body.scrollWidth` and `document.documentElement.scrollWidth` do not exceed client width except for intentional internal scrollers.
- Module rects stay within the viewport.
- Full-page mobile screenshot is captured from the `m.` URL.

## Related pitfall

If a dev/test delegate times out, inspect recent modified files before continuing. In this session, a timed-out follow-up had signs of unrelated recent template edits. Future xz01 follow-ups should verify the changed-file list against the assigned target before accepting or continuing the work.
