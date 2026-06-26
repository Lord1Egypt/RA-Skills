import React from 'react';
import {Composition} from 'remotion';
import {ProductMarketingTemplate} from './ProductMarketingTemplate';
import manifest from './creative-manifest.json';

export const RemotionRoot: React.FC = () => {
  const comp = manifest.composition;

  return (
    <Composition
      id={comp.id}
      component={ProductMarketingTemplate}
      durationInFrames={comp.durationInFrames}
      fps={comp.fps}
      width={comp.width}
      height={comp.height}
      defaultProps={comp.defaultProps}
    />
  );
};
