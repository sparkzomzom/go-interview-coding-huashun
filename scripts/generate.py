#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成比赛提交文件 答案.json（FOFA 自然语言转查询语句，参赛包 pkg-08e82c8d）。

用法：
    python3 scripts/generate.py            # 写出 答案.json
    python3 scripts/generate.py --check    # 只校验，不写文件
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from queries import QUERIES  # noqa: E402

PLAYER = "林星宇"
PKG_ID = "pkg-08e82c8d"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_IDS = None  # 由题目模板提供时填入；本仓库直接使用题号顺序


def build():
    return {
        "选手名称": PLAYER,
        "参赛包编号": PKG_ID,
        "答案": [{"题号": qid, "查询语句": q} for qid, q in QUERIES],
    }


def check(payload):
    ids = [a["题号"] for a in payload["答案"]]
    assert payload["参赛包编号"] == PKG_ID
    assert len(ids) == 100, f"题数错误: {len(ids)}"
    assert len(set(ids)) == len(ids), "存在重复题号"
    assert all(a["查询语句"].strip() for a in payload["答案"]), "存在空答案"
    assert ids[0] == "M001-S009" and ids[-1] == "M100-S001"
    return True


def main():
    payload = build()
    check(payload)
    out = os.path.join(ROOT, "答案.json")
    if "--check" in sys.argv:
        print("OK: 100 题，题号连续无重复，UTF-8 JSON")
        return
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"已生成 {out}（{len(payload['答案'])} 题）")


if __name__ == "__main__":
    main()
