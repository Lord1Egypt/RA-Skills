import { registerRoot, Composition } from 'remotion';
import React from 'react';
import { Video } from './Video';

const MyComp = () => (
  <Composition
    id='Video'
    component={Video}
    durationInFrames={218}
    fps={30}
    width={1080}
    height={1920}
  />
);

registerRoot(MyComp);
