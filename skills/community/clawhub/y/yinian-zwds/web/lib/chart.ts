/**
 * 一念紫微斗数 Web App
 * Yinian ZWDS - Next.js frontend with react-iztro
 * 
 * 使用iztro JS在前端排盘，零后端依赖
 */

import { bySolar, byLunar } from "iztro/lib/astro/astro";
import type { IFunctionalAstrolabe } from "iztro/lib/astro/FunctionalAstrolabe";

// 时辰映射（0-23 → iztro index 0-12）
const SOLAR_TERMS = [
  "子初", "子正", "丑初", "丑正", "寅初", "寅正",
  "卯初", "卯正", "辰初", "辰正", "巳初", "巳正",
  "午初", "午正", "未初", "未正", "申初", "申正",
  "酉初", "酉正", "戌初", "戌正", "亥初", "亥正",
];

export function hourToTimeIndex(hour: number): number {
  // iztro timeIndex: 0=子初, 1=子正, ... 23=亥正 → 实际索引0~12
  // iztro 使用时辰序号：子时=0, 丑时=2, 寅时=4 ...
  return Math.floor(hour / 2) * 2; // 子时0~1→0, 丑时2~3→2, ...
}

export function calculateChart(
  dateStr: string,
  hour: number,
  gender: string,
  isLunar = false
): { success: boolean; astrolabe?: IFunctionalAstrolabe; error?: string } {
  try {
    const timeIndex = hourToTimeIndex(hour);
    const g = gender === "男" ? "male" : "female";

    if (isLunar) {
      const astrolabe = byLunar(dateStr, timeIndex, g);
      return { success: true, astrolabe };
    }
    const astrolabe = bySolar(dateStr, timeIndex, g);
    return { success: true, astrolabe };
  } catch (e: any) {
    return { success: false, error: e.message || "排盘失败" };
  }
}

export function getHourLabel(hour: number): string {
  return SOLAR_TERMS[hour] || `${hour}时`;
}
