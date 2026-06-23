#!/usr/bin/env python3
"""保存新文章数据到月半里予历史存档"""
import json
from pathlib import Path
from datetime import datetime

ARCHIVE_DIR = Path(__file__).parent.parent / "历史数据存档"
DATA_FILE = ARCHIVE_DIR / "数据汇总.json"
ARTICLES_DIR = ARCHIVE_DIR / "文章历史"

METRIC_FIELDS = [
    "read_count", "avg_read_time", "completion_rate", "new_followers",
    "share_count", "like_count", "fav_count", "comment_count",
    "reward_amount", "recommend_count", "wow_rate"
]

def ensure_directories():
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    ARTICLES_DIR.mkdir(parents=True, exist_ok=True)

def load_data_summary():
    if not DATA_FILE.exists():
        return {
            "articles": [],
            "insights": {"best_performing_pillar": "", "best_title_pattern": "", "optimal_length": "", "optimal_publish_time": ""},
            "created_at": datetime.now().isoformat(), "updated_at": datetime.now().isoformat(), "version": "2.0"
        }
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data_summary(data):
    data["updated_at"] = datetime.now().isoformat()
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return True

def save_article_markdown(article_data):
    date = article_data.get("date", datetime.now().strftime("%Y-%m-%d"))
    title = article_data.get("title", "未命名")[:20]
    safe_title = "".join(c for c in title if c.isalnum() or c in "_- ").strip()
    filename = f"{date}_{safe_title}.md"
    filepath = ARTICLES_DIR / filename
    counter = 1
    while filepath.exists():
        filepath = ARTICLES_DIR / f"{date}_{safe_title}_{counter}.md"
        counter += 1
    d = article_data.get("data", {})
    metrics_table = "\n".join([f"| {k} | {d.get(k, 'N/A')} |" for k in METRIC_FIELDS])
    highlights = "\n".join(['- ' + h for h in article_data.get('highlights', [])]) or '- 待补充'
    content = f"""# {article_data.get('title', '未命名')}

**发布日期**: {date}
**内容支柱**: {article_data.get('pillar', '未分类')}
**文章ID**: {article_data.get('id', 'N/A')}

## 数据表现

| 指标 | 数值 |
|------|------|
{metrics_table}

## 文章亮点
{highlights}

## 读者反馈
{article_data.get('reader_feedback', '待补充')}

## 原文内容
{article_data.get('content', '原文未保存')}

*存档时间: {datetime.now().isoformat()}*
"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return str(filepath)

def add_new_article(article_data):
    ensure_directories()
    data = load_data_summary()
    articles = data.get("articles", [])
    new_id = max([a.get("id", 0) for a in articles], default=0) + 1
    article_data["id"] = new_id
    md_path = save_article_markdown(article_data)
    articles.append({
        "id": new_id, "date": article_data.get("date"),
        "title": article_data.get("title"), "pillar": article_data.get("pillar"),
        "data": article_data.get("data", {}),
        "highlights": article_data.get("highlights", []),
        "reader_feedback": article_data.get("reader_feedback", ""),
        "archive_path": md_path
    })
    data["articles"] = articles
    pillar_counts = {}
    for a in articles:
        p = a.get("pillar", "未分类")
        pillar_counts[p] = pillar_counts.get(p, 0) + 1
    if pillar_counts:
        data["insights"]["best_performing_pillar"] = max(pillar_counts.items(), key=lambda x: x[1])[0]
    return save_data_summary(data)

def save_article_interactive():
    print("=" * 40)
    print("添加新文章到存档")
    print("=" * 40)
    article_data = {}
    article_data["title"] = input("文章标题: ").strip()
    article_data["date"] = input("发布日期 (YYYY-MM-DD): ").strip() or datetime.now().strftime("%Y-%m-%d")
    article_data["pillar"] = input("内容支柱: ").strip()
    print("\n数据表现 (11项):")
    d = {}
    for k in METRIC_FIELDS:
        d[k] = input(f"  {k}: ").strip()
    article_data["data"] = d
    h = input("\n金句/亮点 (用|分隔): ").strip()
    article_data["highlights"] = [x.strip() for x in h.split("|") if x.strip()]
    article_data["reader_feedback"] = input("读者反馈摘要: ").strip()
    print("\n正在保存...")
    print("保存成功！" if add_new_article(article_data) else "保存失败")

if __name__ == "__main__":
    save_article_interactive()
