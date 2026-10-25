#!/usr/bin/env python3
"""Merge exported episode JSON files into episodes.json for the static site.

Usage: python3 build.py <dir-with-<seq>.json-files>
"""
import json, os, sys

src = sys.argv[1]
rows = []
for name in os.listdir(src):
    if not name.endswith(".json"):
        continue
    with open(os.path.join(src, name), encoding="utf-8") as f:
        d = json.load(f)
    d.pop("tg", None)
    d["id"] = name[:-5]
    rows.append(d)
rows.sort(key=lambda r: r.get("publishTime") or 0, reverse=True)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "episodes.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=1)
print(f"wrote {len(rows)} episodes to {out}")
