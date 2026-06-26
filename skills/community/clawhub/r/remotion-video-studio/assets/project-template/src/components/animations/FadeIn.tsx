/**
 * FadeIn — fades in children with optional vertical/horizontal offset.
 * All animations driven by useCurrentFrame() per Remotion rules.
 */
import React from "react";
import {
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
} from "remotion";

type FadeInProps = {
  children: React.ReactNode;
  /** Delay in frames before animation starts */
  delay?: number;
  /** Direction to fade in from */
  direction?: "up" | "down" | "left" | "right" | "none";
  /** Offset distance in pixels */
  offset?: number;
  /** Spring damping (higher = less bounce) */
  damping?: number;
  /** Custom style on the wrapper */
  style?: React.CSSProperties;
};

export const FadeIn: React.FC<FadeInProps> = ({
  children,
  delay = 0,
  direction = "up",
  offset = 40,
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

  const opacity = interpolate(progress, [0, 1], [0, 1]);

  let translateX = 0;
  let translateY = 0;

  switch (direction) {
    case "up":
      translateY = interpolate(progress, [0, 1], [offset, 0]);
      break;
    case "down":
      translateY = interpolate(progress, [0, 1], [-offset, 0]);
      break;
    case "left":
      translateX = interpolate(progress, [0, 1], [offset, 0]);
      break;
    case "right":
      translateX = interpolate(progress, [0, 1], [-offset, 0]);
      break;
    case "none":
    default:
      break;
  }

  return (
    <div
      style={{
        opacity,
        transform: `translate(${translateX}px, ${translateY}px)`,
        ...style,
      }}
    >
      {children}
    </div>
  );
};
