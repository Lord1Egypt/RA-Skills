/**
 * SlideIn — slides children in from off-screen with spring physics.
 */
import React from "react";
import {
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
} from "remotion";

type SlideInProps = {
  children: React.ReactNode;
  /** Delay in frames */
  delay?: number;
  /** Direction to slide in from */
  from?: "left" | "right" | "top" | "bottom";
  /** Distance in pixels (defaults to full viewport dimension) */
  distance?: number;
  /** Spring damping */
  damping?: number;
  /** Custom style */
  style?: React.CSSProperties;
};

export const SlideIn: React.FC<SlideInProps> = ({
  children,
  delay = 0,
  from = "left",
  distance = 800,
  damping = 200,
  style,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({
    frame,
    fps,
    delay,
    config: { damping },
  });

  let translateX = 0;
  let translateY = 0;

  switch (from) {
    case "left":
      translateX = interpolate(progress, [0, 1], [-distance, 0]);
      break;
    case "right":
      translateX = interpolate(progress, [0, 1], [distance, 0]);
      break;
    case "top":
      translateY = interpolate(progress, [0, 1], [-distance, 0]);
      break;
    case "bottom":
      translateY = interpolate(progress, [0, 1], [distance, 0]);
      break;
  }

  return (
    <div
      style={{
        transform: `translate(${translateX}px, ${translateY}px)`,
        ...style,
      }}
    >
      {children}
    </div>
  );
};
