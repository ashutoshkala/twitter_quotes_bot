import tweepy
import keys


def tweet(txt, path):
    client = tweepy.Client(
        keys.bearer_token,
        keys.api_key,
        keys.api_key_secret,
        keys.access_token,
        keys.access_token_secret,
    )

    auth = tweepy.OAuth1UserHandler(
        keys.api_key,
        keys.api_key_secret,
        keys.access_token,
        keys.access_token_secret,
    )
    api = tweepy.API(auth)
    media_id = api.media_upload(filename=path).media_id_string
    client.create_tweet(text=txt, media_ids=[media_id])
    print("Tweeted!")
