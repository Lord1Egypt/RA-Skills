"use client";
import { useTranslations } from "next-intl";
import { Link } from "@/i18n/navigation";

export default function Nav() {
  const t = useTranslations("Navigation");
  return <Link href="/about">{t("links.about")}</Link>;
}
