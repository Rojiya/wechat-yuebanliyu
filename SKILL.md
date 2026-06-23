---
name: wechat-html-export
description: 微信公众号文章 HTML 导出与排版规范。提供公众号粘贴用 HTML 生成（一键复制、ClipboardItem text/html）、严格标签/CSS 白名单、灰度色号规范、图片规则、布局限制和输出复查清单。触发关键词：导出HTML、生成HTML、公众号粘贴、生成排版。
---

# 微信公众号 HTML 导出与排版规范

---

## 一、触发时机

- 用户要求"导出为 HTML"、"生成 HTML 文件"、"我要粘贴到公众号"
- 用户说"做成浏览器打开就能复制的那种"
- 用户要求检查/修改公众号排版规范

---

## 二、HTML 整体结构

### 核心骨架

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>文章标题</title>
</head>
<body>
  <!-- 顶部 sticky 工具栏 -->
  <div id="toolbar" style="position: fixed; top: 0; left: 0; right: 0; z-index: 9999; background: #fff; border-bottom: 1px solid #eee; padding: 12px 20px; text-align: center;">
    <button id="copy-btn" onclick="copyArticle()" style="background: #7c3aed; color: #fff; border: none; padding: 10px 32px; font-size: 16px; border-radius: 6px; cursor: pointer;">
      📋 一键复制到公众号
    </button>
    <span id="copy-status" style="margin-left: 12px; font-size: 14px; color: #666;"></span>
  </div>

  <!-- 文章内容容器 -->
  <div id="article-content" style="max-width: 677px; margin: 80px auto 40px; padding: 0 16px;">
    <!-- 文章正文（全部内联样式） -->
  </div>

  <script>
    function copyArticle() {
      const content = document.getElementById('article-content').cloneNode(true);
      const btns = content.querySelectorAll('button');
      btns.forEach(b => b.remove());
      const html = new Blob([content.outerHTML], { type: 'text/html' });
      const clipboardItem = new ClipboardItem({ 'text/html': html });
      navigator.clipboard.write([clipboardItem]).then(() => {
        const status = document.getElementById('copy-status');
        status.textContent = '✅ 已复制！去公众号编辑器粘贴吧';
        status.style.color = '#16a34a';
        setTimeout(() => { status.textContent = ''; }, 3000);
      }).catch(err => {
        const status = document.getElementById('copy-status');
        status.textContent = '❌ 复制失败，请重试或手动全选复制';
        status.style.color = '#dc2626';
      });
    }
  </script>
</body>
</html>
```

### 关键设计约束

| 项目 | 规则 | 原因 |
|------|------|------|
| 工具栏 | `position: fixed` + `z-index: 9999` | 不进入公众号内容区 |
| 文章容器 | `max-width: 677px` | 模拟公众号正文宽度 |
| 复制机制 | `ClipboardItem` + `text/html` MIME | 粘贴时保留完整富文本格式 |
| 复制净化 | 移除内容区内的 `button` 元素 | 防止工具栏按钮出现在剪贴板 |

---

## 三、公众号 HTML 严格规范

### 3.1 标签白名单

**允许的标签**：`<div>`, `<section>`, `<header>`, `<footer>`, `<h1>`~`<h6>`, `<p>`, `<span>`, `<br>`, `<pre>`, `<code>`, `<blockquote>`, `<strong>`, `<b>`, `<em>`, `<i>`, `<u>`, `<del>`, `<sub>`, `<sup>`, `<mark>`, `<ul>`, `<ol>`, `<li>`, `<table>`, `<thead>`, `<tbody>`, `<tr>`, `<th>`, `<td>`, `<a>`, `<img>`, `<hr>`

**绝对禁用**：`<script>`（正文内）, `<style>`, `<link>`, `<meta>`, `<iframe>`, `<form>`, `<input>`, `<button>`, `<svg>`, `<canvas>`, `<audio>`, `<video>`

### 3.2 CSS 规则

- 所有样式通过 `style=""` 内联
- 不使用 `position`, `float`, `flex`, `grid`
- 不使用 `background-image`, `box-shadow`, `text-shadow`, `filter`, `animation`, `transform`

**安全 CSS 属性**：`color`, `background-color`, `font-size`, `font-weight`, `font-style`, `font-family`, `text-align`, `text-indent`, `text-decoration`, `line-height`, `letter-spacing`, `margin/padding`, `border`, `width`, `max-width`, `height`, `max-height`, `display` (仅 block/inline/inline-block/none), `vertical-align`, `opacity`, `white-space`, `word-break`

**单位规则**：字号用 `px`，颜色用 `#rrggbb` 或 `rgb(r,g,b)`

### 3.3 灰度文字色号规范

**不使用纯黑 `#000`**。以下色号为强制规范：

| 场景 | 色号 | 说明 |
|------|------|------|
| 正文（最推荐） | `#3f3f3f` | 微信后台默认色，对比度约 10:1 |
| 正文（备选） | `#333333` | 设计系统标准文本色 |
| 次要文字/注释 | `#999999` | 引文、图注、辅助信息 |
| 标题 | `#1a1a1a` | 视觉重心强，比纯黑柔和 |

**应用规则**：
- 正文段落 → `#3f3f3f`
- 引文、图注、日期、署名 → `#999999`
- 标题及开篇引文 → `#1a1a1a`
- `<strong>` 保持与正文同色或稍深

### 3.4 图片规则

- `src` 必须为 `mmbiz.qpic.cn` 域名
- 外链/base64 会被过滤
- 必须设置 `style="max-width: 100%; height: auto; display: block; margin: 10px auto;"`
- 使用占位符并标注 `<!-- 请替换为微信公众号素材库图片地址 -->`

### 3.5 布局限制

仅可用：
1. 正常文档流（块级 + 内联 + margin/padding）
2. `<table>` 布局（多列唯一稳定方案）

---

## 四、输出后复查清单（11项）

1. [ ] 无 `<style>`、`<link>`，所有样式在 `style=""` 中
2. [ ] 无 `class` 或 `id` 依赖样式控制
3. [ ] 无 `position`, `float`, `flex`, `grid`（工具栏除外）
4. [ ] 无 `background-image`, `box-shadow`, `text-shadow`, `animation`, `transform`
5. [ ] 图片 `src` 已标注占位符提示
6. [ ] 无 `<script>`（正文区内）, `<iframe>`, 表单元素
7. [ ] 顶部工具栏不在正文区域内
8. [ ] 一键复制按钮使用 `ClipboardItem` + `text/html` MIME
9. [ ] `#article-content` 容器 `max-width: 677px`
10. [ ] 正文无禁用词、冒号、破折号
11. [ ] 正文 `#3f3f3f`，标题 `#1a1a1a`，次要文字 `#999999`，无纯黑
