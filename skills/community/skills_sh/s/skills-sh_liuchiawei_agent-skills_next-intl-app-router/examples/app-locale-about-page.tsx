// Place at: app/[locale]/about/page.tsx
import { use } from "react";
import { setRequestLocale } from "next-intl/server";
import AboutContainer from "./components/AboutContainer";

export default function AboutPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = use(params);
  setRequestLocale(locale);
  return <AboutContainer />;
}
