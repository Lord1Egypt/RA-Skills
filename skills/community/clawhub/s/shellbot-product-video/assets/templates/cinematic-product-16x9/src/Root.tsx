import {Composition} from "remotion";
import {CinematicProductVideo} from "./template";

export const RemotionRoot = () => {
  return (
    <Composition
      id="CinematicProduct16x9"
      component={CinematicProductVideo}
      width={1920}
      height={1080}
      fps={30}
      durationInFrames={900}
    />
  );
};
