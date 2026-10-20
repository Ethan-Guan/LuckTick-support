#!/usr/bin/env python3
"""生成 LuckTick 支持页与隐私政策（每种语言一组页面）。

正文在 content/<page>.<lang>.html，改完运行 `python3 build.py`，再提交推送即可。
输出：<lang>/index.html（支持）、<lang>/privacy.html（隐私政策），
以及根目录的 index.html / privacy.html：按浏览器语言跳到对应版本。
"""
from pathlib import Path

EMAIL = "ethan.guan.work@outlook.com"
ROOT = Path(__file__).parent

LANGS = {
    "zh-Hans": dict(
        name="简体中文", support="支持", privacy="隐私政策",
        support_title="LuckTick 支持", privacy_title="LuckTick 隐私政策",
        effective="生效日期：2026 年 10 月 20 日",
        summary="简而言之：LuckTick 不收集、不上传你的任何数据。你的资料和健康数据只保存在你自己的 Apple Watch 上。",
        faq="常见问题", contact="联系我们",
        contact_text=f'如有问题、建议或隐私方面的疑问，请发送邮件至 <a href="mailto:{EMAIL}">{EMAIL}</a>。',
        disclaimer="运势内容仅供娱乐与自我激励，不构成任何医疗、财务或人生建议。",
        languages="语言",
    ),
    "en": dict(
        name="English", support="Support", privacy="Privacy Policy",
        support_title="LuckTick Support", privacy_title="LuckTick Privacy Policy",
        effective="Effective October 20, 2026",
        summary="In short: LuckTick doesn't collect or upload any of your data. Your profile and Health data stay on your own Apple Watch.",
        faq="Frequently asked questions", contact="Contact us",
        contact_text=f'For questions, feedback or privacy requests, email <a href="mailto:{EMAIL}">{EMAIL}</a>.',
        disclaimer="Readings are for entertainment and self-motivation only; they are not medical, financial or life advice.",
        languages="Language",
    ),
    "ja": dict(
        name="日本語", support="サポート", privacy="プライバシーポリシー",
        support_title="LuckTick サポート", privacy_title="LuckTick プライバシーポリシー",
        effective="施行日：2026年10月20日",
        summary="要点：LuckTick はお客様のデータを一切収集・アップロードしません。プロフィールとヘルスケアのデータはお客様の Apple Watch にのみ保存されます。",
        faq="よくある質問", contact="お問い合わせ",
        contact_text=f'ご質問、ご意見、プライバシーに関するお問い合わせは <a href="mailto:{EMAIL}">{EMAIL}</a> までメールでお送りください。',
        disclaimer="運勢は娯楽と自己応援のためのもので、医療・金融・人生の助言ではありません。",
        languages="言語",
    ),
    "ko": dict(
        name="한국어", support="지원", privacy="개인정보 처리방침",
        support_title="LuckTick 지원", privacy_title="LuckTick 개인정보 처리방침",
        effective="시행일: 2026년 10월 20일",
        summary="요약: LuckTick은 사용자의 데이터를 수집하거나 업로드하지 않습니다. 프로필과 건강 데이터는 사용자의 Apple Watch에만 저장됩니다.",
        faq="자주 묻는 질문", contact="문의",
        contact_text=f'질문, 의견, 개인정보 관련 문의는 <a href="mailto:{EMAIL}">{EMAIL}</a>로 메일을 보내 주세요.',
        disclaimer="운세는 재미와 자기 응원을 위한 것이며 의료, 금융, 인생에 관한 조언이 아닙니다.",
        languages="언어",
    ),
}

PAGES = {"support": "index.html", "privacy": "privacy.html"}
CURRENT_PAGE = ' aria-current="page"'
CURRENT_LANG = ' aria-current="true"'


def layout(lang: str, page: str, title: str, body: str) -> str:
    t = LANGS[lang]
    tabs = "".join(
        f'<a href="{PAGES[p]}"{CURRENT_PAGE if p == page else ""}>{t[p]}</a>'
        for p in ("support", "privacy")
    )
    langs = "".join(
        f'<a href="../{code}/{PAGES[page]}" hreflang="{code}" lang="{code}"'
        f'{CURRENT_LANG if code == lang else ""}>{info["name"]}</a>'
        for code, info in LANGS.items()
    )
    alternates = "\n".join(
        f'<link rel="alternate" hreflang="{code}" href="../{code}/{PAGES[page]}">' for code in LANGS
    )
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
{alternates}
<link rel="stylesheet" href="../style.css">
</head>
<body>
<header class="topbar">
  <div class="wrap">
    <nav class="tabs" aria-label="LuckTick">{tabs}</nav>
    <nav class="langs" aria-label="{t['languages']}">{langs}</nav>
  </div>
</header>
<main class="wrap">
{body}
</main>
<footer><div class="wrap">LuckTick · <a href="index.html">{t['support']}</a> · <a href="privacy.html">{t['privacy']}</a></div></footer>
</body>
</html>
"""


def support_page(lang: str) -> str:
    t = LANGS[lang]
    content = (ROOT / f"content/support.{lang}.html").read_text().strip()
    intro, _, faq = content.partition("<h3>")
    body = f"""<h1>{t['support_title']}</h1>
{intro.strip()}
<h2>{t['faq']}</h2>
<h3>{faq}
<h2>{t['contact']}</h2>
<p>{t['contact_text']}</p>
<p class="note">{t['disclaimer']}</p>"""
    return layout(lang, "support", t["support_title"], body)


def privacy_page(lang: str) -> str:
    t = LANGS[lang]
    content = (ROOT / f"content/privacy.{lang}.html").read_text().strip()
    sections = content.count("<h2>")
    body = f"""<h1>{t['privacy_title']}</h1>
<p class="note">{t['effective']}</p>
<p class="summary">{t['summary']}</p>
{content}
<h2>{sections + 1}. {t['contact']}</h2>
<p>{t['contact_text']}</p>"""
    return layout(lang, "privacy", t["privacy_title"], body)


def redirect_page(page: str) -> str:
    """根目录的入口：按浏览器语言跳到对应版本，不支持脚本时列出各语言的链接。"""
    links = " · ".join(f'<a href="{code}/{PAGES[page]}" lang="{code}">{info["name"]}</a>' for code, info in LANGS.items())
    title = "LuckTick Support" if page == "support" else "LuckTick Privacy Policy"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="style.css">
<script>
(function () {{
  var map = [["zh", "zh-Hans"], ["ja", "ja"], ["ko", "ko"]];
  var prefs = navigator.languages || [navigator.language || "en"];
  var target = "en";
  outer: for (var i = 0; i < prefs.length; i++) {{
    var p = (prefs[i] || "").toLowerCase();
    if (p.indexOf("en") === 0) break;
    for (var j = 0; j < map.length; j++) {{
      if (p.indexOf(map[j][0]) === 0) {{ target = map[j][1]; break outer; }}
    }}
  }}
  location.replace(target + "/{PAGES[page]}" + location.hash);
}})();
</script>
</head>
<body>
<main class="wrap">
<h1>{title}</h1>
<p>{links}</p>
</main>
</body>
</html>
"""


if __name__ == "__main__":
    for lang in LANGS:
        out = ROOT / lang
        out.mkdir(exist_ok=True)
        (out / "index.html").write_text(support_page(lang))
        (out / "privacy.html").write_text(privacy_page(lang))
    for page, filename in PAGES.items():
        (ROOT / filename).write_text(redirect_page(page))
    print("built", ", ".join(LANGS))
