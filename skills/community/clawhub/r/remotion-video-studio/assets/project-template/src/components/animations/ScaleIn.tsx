/**
 * ScaleIn — scales children from a starting scale to 1 with spring physics.
 */
import React from "react";
import {
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
} from "remotion";

type ScaleInProps = {
  children: React.ReactNode;
  /** Delay in frames */
  delay?: number;
  /** Starting scale (0 = invisible, 0.5 = half size) */
  initialScale?: number;
  /** Spring damping */
  damping?: number;
  /** Spring stiffness */
  stiffness?: number;
  /** Custom style */
  style?: React.CSSProperties;
};

export const ScaleIn: React.FC<ScaleInProps> = ({
  children,
  delay = 0,
  initialScale = 0,
  damping = 12,
  stiffness = 100,
  style,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({
    frame,
    fps,
    delay,
    config: { damping, stiffness },
  });

  const scale = interpolate(progress, [0, 1], [initialScale, 1]);
  const opacity = interpolate(progress, [0, 1], [0, 1]);

  return (
    <div
      style={{
        opacity,
        transform: `scale(${scale})`,
        ...style,
      }}
    >
      {children}
    </div>
  );
};
