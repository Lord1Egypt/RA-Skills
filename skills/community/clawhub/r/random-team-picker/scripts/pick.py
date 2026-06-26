#!/usr/bin/env python3
"""Random Team Picker - Pick random members or split into teams"""
import random, sys, argparse

def pick_members(members, count=1, weights=None, exclude=None):
    excluded = set(exclude.split(',')) if exclude else set()
    pool = [m for m in members if m not in excluded]
    if not pool:
        return []
    if weights:
        weight_list = []
        weight_map = dict(w.split(':') for w in weights.split(','))
        for m in pool:
            w = int(weight_map.get(m, 1))
            weight_list.extend([m] * w)
        return random.sample(weight_list, min(count, len(pool)))
    return random.sample(pool, min(count, len(pool)))

def split_teams(members, num_teams):
    shuffled = list(members)
    random.shuffle(shuffled)
    teams = [[] for _ in range(num_teams)]
    for i, m in enumerate(shuffled):
        teams[i % num_teams].append(m)
    return teams

def main():
    parser = argparse.ArgumentParser(description='Random Team Picker')
    parser.add_argument('--from', dest='members', required=True)
    parser.add_argument('--count', type=int, default=1)
    parser.add_argument('--num-teams', type=int, default=0)
    parser.add_argument('--weighted', default='')
    parser.add_argument('--exclude', default='')
    
    args = parser.parse_args()
    members = [m.strip() for m in args.members.split(',')]
    
    if args.num_teams > 0:
        teams = split_teams(members, args.num_teams)
        for i, team in enumerate(teams):
            print(f"Team {i+1}: {', '.join(team)}")
    else:
        picked = pick_members(members, args.count, args.weighted, args.exclude)
        if args.count == 1:
            print(picked[0] if picked else "No members available")
        else:
            print(', '.join(picked))

if __name__ == "__main__":
    main()
