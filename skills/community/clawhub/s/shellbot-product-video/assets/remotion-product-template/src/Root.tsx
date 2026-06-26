import {Composition} from "remotion";
import {ProductAidaVideo} from "./ProductAidaVideo";
import {samplePlan} from "./sample-plan";

const durationInFrames = samplePlan.scenes.reduce((sum, scene) => sum + scene.durationInFrames, 0);

export const RemotionRoot = () => {
  return (
    <Composition
      id="ProductAida"
      component={ProductAidaVideo}
      width={1920}
      height={1080}
      fps={30}
      durationInFrames={durationInFrames}
      defaultProps={{plan: samplePlan}}
    />
  );
};
