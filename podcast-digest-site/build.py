#!/usr/bin/env python3
"""Merge exported episode JSON files into episodes.json for the static site.

Usage:
  python3 build.py <dir>           full rebuild: episodes.json = exactly the files in <dir>
  python3 build.py <dir> --merge   incremental: keep the rows already in episodes.json and
                                   add or replace only the rows whose <seq>.json is in <dir>
"""
import json, os, sys

merge = "--merge" in sys.argv[1:]
args = [a for a in sys.argv[1:] if not a.startswith("--")]
if len(args) != 1:
    sys.exit(__doc__)
src = args[0]
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "episodes.json")

rows = {}
if merge and os.path.exists(out):
    with open(out, encoding="utf-8") as f:
        for r in json.load(f):
            rows[str(r["id"])] = r
before = len(rows)

updated = 0
for name in os.listdir(src):
    if not name.endswith(".json"):
        continue
    with open(os.path.join(src, name), encoding="utf-8") as f:
        d = json.load(f)
    d.pop("tg", None)
    d["id"] = name[:-5]
    rows[d["id"]] = d
    updated += 1

result = sorted(rows.values(), key=lambda r: r.get("publishTime") or 0, reverse=True)
with open(out, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)
mode = "merge" if merge else "full"
print(f"{mode}: wrote {len(result)} episodes to {out} (before {before}, from {src}: {updated})")
