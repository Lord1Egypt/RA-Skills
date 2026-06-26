import type { NextConfig } from "next";
import createNextIntlPlugin from "next-intl/plugin";

const nextConfig: NextConfig = {
  // your app config
};

const withNextIntl = createNextIntlPlugin();
export default withNextIntl(nextConfig);
