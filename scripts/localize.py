#!/usr/bin/env python3
"""
Tự động áp dụng từ điển i18n vào file console.html trước khi build.
Không làm thay đổi git source trừ khi được gọi trong build pipeline.
"""
import sys
import json
import os
import re

def localize(html_path, json_path, out_path=None):
    if not os.path.exists(html_path):
        print(f"Error: {html_path} does not exist", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(json_path):
        print(f"Error: {json_path} does not exist", file=sys.stderr)
        sys.exit(1)
        
    with open(json_path, "r", encoding="utf-8") as f:
        mapping = json.load(f)
        
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Sort keys by length descending (longest phrases replaced first)
    sorted_keys = sorted(mapping.keys(), key=lambda k: -len(k))
    
    replace_count = 0
    for k in sorted_keys:
        if k in content:
            v = mapping[k]
            # protect raw === "免费"
            if k == "免费":
                continue
            count = content.count(k)
            content = content.replace(k, v)
            replace_count += count

    # Also update lang attribute
    content = content.replace('<html lang="zh-CN">', '<html lang="vi">')

    out_file = out_path if out_path else html_path
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Localized {html_path} with {len(sorted_keys)} dictionary terms ({replace_count} replacements applied).")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 scripts/localize.py <path/to/console.html> <path/to/vi.json> [output_path]")
        sys.exit(1)
    html_f = sys.argv[1]
    json_f = sys.argv[2]
    out_f = sys.argv[3] if len(sys.argv) > 3 else None
    localize(html_f, json_f, out_f)
