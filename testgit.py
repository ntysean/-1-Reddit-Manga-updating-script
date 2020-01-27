import praw


#Check for new posts
def check_new_posts(sub):
    for post in r.subreddit(sub).new(limit=10):
        if first is True:
            seen_posts.append(post.id)
        if config['keywords']['enabled'] and not any(x.lower() in post.title.lower() for x in config['keywords']['list']):
            seen_posts.append(post.id)
        if post.id not in seen_posts:
            notify(sub, post.title, post.shortlink)
        seen_posts.append(post.id)


def notify(subreddit, title, url):
    if config['reddit_pm']['enabled']:
        notify_reddit(subreddit, title, url)


def notify_reddit(subreddit, title, url):
    subject = 'New post on /r/' + subreddit + '!'

    message = '[' + title + '](' + url + ')'

    for user in config['reddit_pm']['users']:
        r.redditor(user).message(subject, message)


with open(CONFIG_FILE) as config_file:
    config = json.load(config_file)

r = praw.Reddit(
    user_agent = config['reddit']['user_agent'],
    client_id = config['reddit']['client_id'],
    client_secret = config['reddit']['client_secret'],
    username = config['reddit']['username'],
    password = config['reddit']['password']
)

seen_posts = []
first = True

while True:
    try:
        for sub in config['subreddits']:
            if config['new_posts']:
                check_new_posts(sub)

