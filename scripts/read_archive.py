#!/usr/bin/env python3
"""读取月半里予公众号历史数据存档"""
import json
import os
from pathlib import Path
from datetime import datetime

ARCHIVE_DIR = Path(__file__).parent.parent / "历史数据存档"
DATA_FILE = ARCHIVE_DIR / "数据汇总.json"

METRIC_NAMES = {
    "read_count": "阅读量", "avg_read_time": "平均阅读时长",
    "completion_rate": "完读率", "new_followers": "阅读后关注数",
    "share_count": "分享数", "like_count": "点赞数",
    "fav_count": "收藏数", "comment_count": "留言数",
    "reward_amount": "赞赏金额", "recommend_count": "推荐数",
    "wow_rate": "在看率"
}

def load_data_summary():
    if not DATA_FILE.exists():
        return None
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_recent_articles(n=5):
    data = load_data_summary()
    if not data or "articles" not in data:
        return []
    return sorted(data["articles"], key=lambda x: x.get("date", ""), reverse=True)[:n]

def get_best_performing_articles(metric="read_count", n=3):
    data = load_data_summary()
    if not data or "articles" not in data:
        return []
    def val(a):
        v = a.get("data", {}).get(metric, 0)
        if isinstance(v, str) and "%" in v:
            return float(v.replace("%", ""))
        try: return float(v)
        except: return 0
    return sorted(data["articles"], key=val, reverse=True)[:n]

def extract_metric(data_dict, metric_name):
    v = data_dict.get(metric_name, 0)
    if isinstance(v, str) and "%" in v:
        return float(v.replace("%", ""))
    try: return float(v)
    except: return 0

def analyze_trends():
    data = load_data_summary()
    if not data or len(data.get("articles", [])) < 2:
        return None
    articles = sorted(data["articles"], key=lambda x: x.get("date", ""))
    recent = articles[-5:]
    pillar_counts = {}
    for a in recent:
        p = a.get("pillar", "未分类")
        pillar_counts[p] = pillar_counts.get(p, 0) + 1
    best = max(pillar_counts.items(), key=lambda x: x[1])[0] if pillar_counts else "未知"
    return {"best_pillar": best, "pillar_counts": pillar_counts, "total_articles": len(data["articles"])}

def format_data_for_prompt():
    data = load_data_summary()
    trends = analyze_trends()
    recent = get_recent_articles(5)
    if not data or not data.get("articles"):
        return "【暂无历史数据，这是首次启动】"
    output = ["=" * 40, "月半里予历史数据概览", "=" * 40]
    if trends:
        output.append(f"\n整体趋势（最近5篇）")
        output.append(f"  累计文章数: {trends['total_articles']}")
        output.append(f"  最佳表现支柱: {trends['best_pillar']}")
    if recent:
        output.append("\n最近5篇文章表现")
        for a in recent:
            d = a.get("data", {})
            output.append(f"  {a.get('date')} | {a.get('title', '未命名')[:25]}")
            ms = [f"{METRIC_NAMES[k]}:{v}" for k,v in d.items() if v and v != "N/A" and v != 0]
            output.append(f"    {', '.join(ms)}" if ms else "    暂无数据")
    output.append("\n" + "=" * 40)
    return "\n".join(output)

if __name__ == "__main__":
    print(format_data_for_prompt())
