import { defineRouting } from "next-intl/routing";

export const routing = defineRouting({
  locales: ["en", "ja", "zh-CN", "zh-TW"],
  defaultLocale: "en",
});
