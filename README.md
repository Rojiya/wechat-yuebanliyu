# 月半里予 · 公众号 HTML 导出技能

微信公众号「月半里予」的 HTML 导出与排版规范子技能。

> 主技能（内容创作/选题规划/数据复盘）仅保存在本地，不公开发布。

**作者**：里予

---

## 仓库结构

```
wechat-yuebanliyu/
├── SKILL.md                          # 占位说明（主技能已移至本地）
├── README.md                         # 本说明文件
├── wechat-html-export/
│   └── SKILL.md                      # 子技能（HTML导出、排版规范、色号标准）
└── scripts/
    ├── read_archive.py               # 读取历史数据脚本
    └── save_article.py               # 保存文章数据脚本（交互式）
```

---

## 功能

### wechat-html-export（子技能）

1. **HTML 生成** — 一键复制到公众号编辑器的完整 HTML 文件
2. **排版规范** — 标签白名单、CSS 安全属性列表
3. **色号标准** — 正文 `#3f3f3f` / 标题 `#1a1a1a` / 次要文字 `#999999`
4. **布局限制** — 微信编辑器兼容（无 flex/grid/float/position）
5. **复查清单** — 11 项输出后自动检查

---

## 使用方法

在对话中提及以下关键词触发：

- "导出HTML" / "生成HTML" / "公众号粘贴"
- "做成浏览器打开就能复制的那种"

---

## 脚本使用

```bash
# 读取历史数据
python scripts/read_archive.py

# 交互式保存文章数据
python scripts/save_article.py
```

---

## 技能依赖

设计用于 OpenClaw / LobsterAI 运行环境：

| 技能 | 用途 | 频率 |
|------|------|------|
| `web-search` | 内容事实核查 | 每次写作 |
| `humanizer` | 去 AI 化润色 | 每次写作 |
| `copy-editing` | 7 遍精校 | 定稿前 |
