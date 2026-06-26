// Place at: app/[locale]/page.tsx
import { use } from "react";
import { setRequestLocale } from "next-intl/server";

export default function IndexPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = use(params);
  setRequestLocale(locale);
  return <YourHomeComponent />;
}
