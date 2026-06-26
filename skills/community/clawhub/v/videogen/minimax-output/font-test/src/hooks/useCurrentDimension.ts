/**
 * useCurrentDimension — 获取当前视频渲染尺寸
 * 用于字体/元素自动缩放
 */
import { useVideoConfig } from "remotion";

export function useCurrentDimension(): {
  width: number;
  height: number;
  scale: number;       // 相对于基准 1920 的缩放比
  scaleX: number;      // 相对于基准宽度 1080 的缩放比
  scaleY: number;      // 相对于基准高度 1920 的缩放比
} {
  const { width, height } = useVideoConfig();

  return {
    width,
    height,
    scale: height / 1920,
    scaleX: width / 1080,
    scaleY: height / 1920,
  };
}

/**
 * useFontSize — 根据当前视频尺寸返回缩放后的字号
 * 推荐在组件中使用此 hook
 */
import { useMemo } from "react";
import { BASE_FONT_SIZES } from "../theme";

export function useFontSize(
  key: keyof typeof BASE_FONT_SIZES
): number {
  const { scaleY } = useCurrentDimension();
  return useMemo(
    () => Math.round(BASE_FONT_SIZES[key] * scaleY),
    [key, scaleY]
  );
}
