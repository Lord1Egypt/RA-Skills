import React, {useMemo} from "react";
import {
  AbsoluteFill,
  Sequence,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import type {AidaPlan, AidaScene, AidaStage} from "./scene-types";

type Props = {
  plan: AidaPlan;
};

const stageGradients: Record<AidaStage, string> = {
  attention: "linear-gradient(135deg, #1f2937 0%, #7f1d1d 100%)",
  interest: "linear-gradient(135deg, #0f172a 0%, #164e63 100%)",
  desire: "linear-gradient(135deg, #172554 0%, #1e3a8a 100%)",
  action: "linear-gradient(135deg, #052e16 0%, #14532d 100%)",
};

const stageLabel: Record<AidaStage, string> = {
  attention: "Attention",
  interest: "Interest",
  desire: "Desire",
  action: "Action",
};

const SceneCard: React.FC<{scene: AidaScene; cta: string; incentive: string}> = ({
  scene,
  cta,
  incentive,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const enter = spring({
    frame,
    fps,
    config: {damping: 200, stiffness: 140},
    durationInFrames: 18,
  });

  const opacity = interpolate(
    frame,
    [0, 8, Math.max(scene.durationInFrames - 10, 9), scene.durationInFrames],
    [0, 1, 1, 0],
    {extrapolateLeft: "clamp", extrapolateRight: "clamp"}
  );

  const translateY = interpolate(enter, [0, 1], [40, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        background: stageGradients[scene.stage],
        color: "#f8fafc",
        opacity,
        fontFamily:
          "Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial",
        justifyContent: "space-between",
        padding: 96,
      }}
    >
      <div style={{fontSize: 28, opacity: 0.9, letterSpacing: 1.6}}>
        {stageLabel[scene.stage].toUpperCase()}
      </div>

      <div style={{transform: `translateY(${translateY}px)`}}>
        <h1 style={{fontSize: 86, lineHeight: 1.05, margin: 0, maxWidth: 1400}}>{scene.headline}</h1>
        {scene.subheadline ? (
          <p style={{fontSize: 42, lineHeight: 1.2, marginTop: 26, maxWidth: 1400, opacity: 0.92}}>
            {scene.subheadline}
          </p>
        ) : null}
      </div>

      <div style={{display: "flex", justifyContent: "space-between", fontSize: 28, opacity: 0.9}}>
        <div>Asset hint: {scene.assetHint ?? "none"}</div>
        {scene.stage === "action" ? (
          <div>
            {cta} | {incentive}
          </div>
        ) : (
          <div>Voiceover cue: {scene.voiceover}</div>
        )}
      </div>
    </AbsoluteFill>
  );
};

export const ProductAidaVideo: React.FC<Props> = ({plan}) => {
  const timeline = useMemo(() => {
    let from = 0;
    return plan.scenes.map((scene) => {
      const result = {scene, from};
      from += scene.durationInFrames;
      return result;
    });
  }, [plan.scenes]);

  return (
    <AbsoluteFill style={{backgroundColor: "#020617"}}>
      {timeline.map(({scene, from}) => (
        <Sequence key={scene.id} from={from} durationInFrames={scene.durationInFrames}>
          <SceneCard scene={scene} cta={plan.cta} incentive={plan.incentive} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
