import React from 'react';
import { recentConnections } from '../data/placeholders';

function badgeClass(platform) {
  if (platform === 'LI') {
    return 'bg-blue-50 text-[#0077b5]';
  }
  return 'bg-pink-50 text-rose-600';
}

// Recent connection rows with avatars, details, and platform pills.
export default function ConnectionList() {
  return (
    <section className="rounded-2xl border border-zinc-200 bg-white p-5">
      <h2 className="text-lg font-semibold text-zinc-900">Recent connections</h2>

      <ul className="mt-4 space-y-3">
        {recentConnections.map((person) => (
          <li key={person.id} className="flex items-center justify-between rounded-xl border border-zinc-100 px-3 py-3">
            <div className="flex items-center gap-3">
              <div
                className={`flex h-10 w-10 items-center justify-center rounded-full text-xs font-semibold ${person.avatarClass}`}
              >
                {person.initials}
              </div>

              <div>
                <p className="font-semibold text-zinc-900">{person.name}</p>
                <p className="text-sm text-zinc-500">
                  {person.roleCompany}
                  {person.location ? ` · ${person.location}` : ''}
                </p>
              </div>
            </div>

            <div className="flex gap-2">
              {person.platforms.map((platform) => (
                <span
                  key={`${person.id}-${platform}`}
                  className={`rounded-full px-2.5 py-1 text-xs font-semibold ${badgeClass(platform)}`}
                >
                  {platform}
                </span>
              ))}
            </div>
          </li>
        ))}
      </ul>
    </section>
  );
}
