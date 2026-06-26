/**
 * StaggeredList — renders a list of items with staggered entrance animations.
 * Each item fades/slides in with a configurable delay between them.
 */
import React from "react";
import {
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
} from "remotion";

type StaggeredListProps = {
  /** Items to render */
  items: React.ReactNode[];
  /** Delay between each item in frames */
  staggerDelay?: number;
  /** Initial delay before first item */
  delay?: number;
  /** Direction items enter from */
  direction?: "up" | "down" | "left" | "right";
  /** Offset distance in pixels */
  offset?: number;
  /** Spring damping */
  damping?: number;
  /** Gap between items in pixels */
  gap?: number;
  /** Layout direction */
  layout?: "vertical" | "horizontal";
  /** Custom style on the container */
  style?: React.CSSProperties;
  /** Custom style on each item wrapper */
  itemStyle?: React.CSSProperties;
};

export const StaggeredList: React.FC<StaggeredListProps> = ({
  items,
  staggerDelay = 8,
  delay = 0,
  direction = "up",
  offset = 30,
  damping = 200,
  gap = 16,
  layout = "vertical",
  style,
  itemStyle,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div
      style={{
        display: "flex",
        flexDirection: layout === "vertical" ? "column" : "row",
        gap,
        ...style,
      }}
    >
      {items.map((item, i) => {
        const progress = spring({
          frame,
          fps,
          delay: delay + i * staggerDelay,
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
        }

        return (
          <div
            key={i}
            style={{
              opacity,
              transform: `translate(${translateX}px, ${translateY}px)`,
              ...itemStyle,
            }}
          >
            {item}
          </div>
        );
      })}
    </div>
  );
};
