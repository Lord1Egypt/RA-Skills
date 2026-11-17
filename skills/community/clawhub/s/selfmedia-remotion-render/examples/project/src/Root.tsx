import React from 'react';
import {Composition} from 'remotion';

const SampleVertical: React.FC = () => (
  <div style={{width: '100%', height: '100%', background: '#172033', color: 'white', display: 'grid', placeItems: 'center', fontSize: 72}}>
    Sample render
  </div>
);

export const Root: React.FC = () => (
  <Composition id="SampleVertical" component={SampleVertical} durationInFrames={90} width={1080} height={1920} fps={30} />
);
