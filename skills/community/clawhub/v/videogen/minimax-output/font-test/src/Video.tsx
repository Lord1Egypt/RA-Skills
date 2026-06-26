import React from "react";
import { AbsoluteFill } from "remotion";
import { FontShowcase } from "./scenes/FontShowcase";

export const Video: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0e17" }}>
      <FontShowcase />
    </AbsoluteFill>
  );
};
