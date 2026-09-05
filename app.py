import feedparser
import requests
import os

RSS_URL = "https://rss.app/feeds/cmq7Qyuh2nJArfkp.xml"

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

LAST_POST_FILE = "last_post.txt"


def get_last_post():
    if os.path.exists(LAST_POST_FILE):
        with open(LAST_POST_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None


def save_last_post(post_id):
    with open(LAST_POST_FILE, "w", encoding="utf-8") as f:
        f.write(post_id)


def check_feed():

    print("Xの投稿をチェックしています...")

    feed = feedparser.parse(RSS_URL)

    if not feed.entries:
        print("投稿を取得できませんでした。")
        return

    latest = feed.entries[0]

    post_id = latest.get("id", latest.get("link"))
    title = latest.get("title", "新しい投稿")
    url = latest.get("link", "")

    print("最新の投稿：")
    print(title)
    print(url)

    last_post = get_last_post()

    # 初回起動
    if last_post is None:

        print("初回起動です。現在の最新投稿を記録します。")
        save_last_post(post_id)

    # 新しい投稿がある
    elif post_id != last_post:

        message = {
            "content": (
                "📢 **SAG徳島の新しいポスト**\n\n"
                f"{title}\n\n"
                f"🔗 {url}"
            )
        }

        response = requests.post(
            WEBHOOK_URL,
            json=message
        )

        if response.status_code == 204:

            print("Discordに投稿しました！")
            save_last_post(post_id)

        else:

            print("Discordへの投稿に失敗しました。")
            print(response.status_code)
            print(response.text)

    # 新しい投稿がない
    else:

        print("新しい投稿はありません。")


check_feed()
