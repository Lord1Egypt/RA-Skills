import React from 'react';
import { statsData } from '../data/placeholders';

// Top KPI strip with subtle dividers and no card shadows.
export default function StatsBar() {
  return (
    <section className="overflow-hidden rounded-2xl border border-zinc-200 bg-white">
      <div className="grid grid-cols-1 divide-y divide-zinc-200 sm:grid-cols-2 sm:divide-y-0 sm:divide-x xl:grid-cols-4">
        {statsData.map((stat) => (
          <article key={stat.label} className="px-5 py-4">
            <p className="text-sm text-zinc-500">{stat.label}</p>
            <p className="mt-1 text-3xl font-semibold text-zinc-900">{stat.value}</p>
            <p className={`mt-1 text-sm ${stat.subtextClass}`}>{stat.subtext}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
