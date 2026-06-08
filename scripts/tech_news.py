import os
import feedparser
import requests
from datetime import datetime, timedelta

# 配置
SCT_KEY = os.getenv("SCT_KEY")
RSS_LIST = [
    "https://www.ithome.com/rss/",
    "https://www.36kr.com/feed",
    "https://techcrunch.com/feed/"
]

# 获取24小时内新闻
def get_news():
    news_list = []
    now = datetime.now()
    limit = now - timedelta(hours=24)

    for url in RSS_LIST:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                try:
                    pub_time = datetime(*entry.published_parsed[:6])
                    if pub_time >= limit:
                        news_list.append({
                            "title": entry.title,
                            "url": entry.link,
                            "time": pub_time.strftime("%m-%d %H:%M")
                        })
                except:
                    continue
        except:
            continue

    news_list = sorted(news_list, key=lambda x: x["time"], reverse=True)
    return news_list[:15]

# 推送到微信
def send_msg(news):
    if not news:
        content = "过去24小时暂无科技资讯更新"
    else:
        content = f"📰 过去24小时科技资讯（共{len(news)}条）\n\n"
        for i, item in enumerate(news, 1):
            content += f"{i}. {item['title']}\n{item['time']}\n{item['url']}\n\n"

    api = f"https://sctapi.ftqq.com/{SCT_KEY}.send"
    data = {"title": "⏰ 每日科技早报", "desp": content}
    try:
        requests.post(api, data=data, timeout=15)
        print("推送成功！")
    except:
        print("推送失败")

# 运行
if __name__ == "__main__":
    news_result = get_news()
    send_msg(news_result)
