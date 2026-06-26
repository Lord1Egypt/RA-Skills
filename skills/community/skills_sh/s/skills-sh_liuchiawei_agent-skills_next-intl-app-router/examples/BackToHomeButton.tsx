"use client";
import { useTranslations } from "next-intl";
import { Link } from "@/i18n/navigation";

export default function BackToHomeButton() {
  const t = useTranslations("BackToHomeButton");
  return (
    <Link href="/">
      <span>{t("buttonText")}</span>
    </Link>
  );
}
