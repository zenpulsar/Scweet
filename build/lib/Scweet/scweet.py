import datetime
import argparse
from time import sleep
import random

from Scweet.utils import init_driver, log_search_page, keep_scroling


def scrape(since: datetime, until: datetime = None, words=None, to_account=None, from_account=None,
           mention_account=None, interval=datetime.timedelta(minutes=15), lang=None,
           headless=True, limit=float("inf"), display_type="Top", proxy=None, hashtag=None,
           filter_replies=False, proximity=False,
           geocode=None, minreplies=None, minlikes=None, minretweets=None, remote=False):
    """
    scrape data from twitter using requests, starting from <since> until <until>. The program make a search between each <since> and <until_local>
    until it reaches the <until> date if it's given, else it stops at the actual date.

    - since - datetime, automatic convert to utc unix
    - until - datetime, automatic convert to utc unix

    :return:
    data : dict contains tweets users and more things.

    Example data:

    {
        'tweets': {},
        'users': {},
        'moments': {},
        'cards': {},
        'places': {},
        'media': {},
        'broadcasts': {},
        'topics': {},
        'lists': {}
    }

    Example tweet data:

    {
       "created_at":"Fri Apr 01 22:32:40 +0000 2022",
       "id":1510022360304398348,
       "id_str":"1510022360304398348",
       "full_text":"Kraken's Lightning node has 61 BTC of public capacity. \n\nThey've nearly doubled their capacity in the last 2 days, and are now the 13th largest node on the network.\n\n⚡️ https://t.co/XgCfO4Hn5F",
       "truncated":false,
       "display_text_range":[0, 168],
       "entities":{
          "hashtags":[],
          "symbols":[],
          "user_mentions":[],
          "urls":[],
          "media":[
             {
                "id":1510022106007982082,
                "id_str":"1510022106007982082",
                "indices":[
                   169,
                   192
                ],
                "media_url":"http://pbs.twimg.com/media/FPStGt-X0AIjkFz.jpg",
                "media_url_https":"https://pbs.twimg.com/media/FPStGt-X0AIjkFz.jpg",
                "url":"https://t.co/XgCfO4Hn5F",
                "display_url":"pic.twitter.com/XgCfO4Hn5F",
                "expanded_url":"https://twitter.com/kerooke/status/1510022360304398348/photo/1",
                "type":"photo",
                "original_info":{
                   "width":2024,
                   "height":1012,
                   "focus_rects":[
                      {
                         "x":109,
                         "y":0,
                         "h":1012,
                         "w":1807
                      },
                      {
                         "x":506,
                         "y":0,
                         "h":1012,
                         "w":1012
                      },
                      {
                         "x":568,
                         "y":0,
                         "h":1012,
                         "w":888
                      },
                      {
                         "x":759,
                         "y":0,
                         "h":1012,
                         "w":506
                      },
                      {
                         "x":0,
                         "y":0,
                         "h":1012,
                         "w":2024
                      }
                   ]
                },
                "sizes":{
                   "large":{
                      "w":2024,
                      "h":1012,
                      "resize":"fit"
                   },
                   "thumb":{
                      "w":150,
                      "h":150,
                      "resize":"crop"
                   },
                   "small":{
                      "w":680,
                      "h":340,
                      "resize":"fit"
                   },
                   "medium":{
                      "w":1200,
                      "h":600,
                      "resize":"fit"
                   }
                }
             }
          ]
       },
       "extended_entities":{
          "media":[
             {
                "id":1510022106007982082,
                "id_str":"1510022106007982082",
                "indices":[
                   169,
                   192
                ],
                "media_url":"http://pbs.twimg.com/media/FPStGt-X0AIjkFz.jpg",
                "media_url_https":"https://pbs.twimg.com/media/FPStGt-X0AIjkFz.jpg",
                "url":"https://t.co/XgCfO4Hn5F",
                "display_url":"pic.twitter.com/XgCfO4Hn5F",
                "expanded_url":"https://twitter.com/kerooke/status/1510022360304398348/photo/1",
                "type":"photo",
                "original_info":{
                   "width":2024,
                   "height":1012,
                   "focus_rects":[
                      {
                         "x":109,
                         "y":0,
                         "h":1012,
                         "w":1807
                      },
                      {
                         "x":506,
                         "y":0,
                         "h":1012,
                         "w":1012
                      },
                      {
                         "x":568,
                         "y":0,
                         "h":1012,
                         "w":888
                      },
                      {
                         "x":759,
                         "y":0,
                         "h":1012,
                         "w":506
                      },
                      {
                         "x":0,
                         "y":0,
                         "h":1012,
                         "w":2024
                      }
                   ]
                },
                "sizes":{
                   "large":{
                      "w":2024,
                      "h":1012,
                      "resize":"fit"
                   },
                   "thumb":{
                      "w":150,
                      "h":150,
                      "resize":"crop"
                   },
                   "small":{
                      "w":680,
                      "h":340,
                      "resize":"fit"
                   },
                   "medium":{
                      "w":1200,
                      "h":600,
                      "resize":"fit"
                   }
                },
                "media_key":"3_1510022106007982082",
                "ext_sensitive_media_warning":"None",
                "ext_media_availability":{
                   "status":"available"
                },
                "ext_alt_text":"None",
                "ext_media_color":{
                   "palette":[
                      {
                         "rgb":{
                            "red":255,
                            "green":255,
                            "blue":255
                         },
                         "percentage":97.29
                      },
                      {
                         "rgb":{
                            "red":123,
                            "green":123,
                            "blue":123
                         },
                         "percentage":1.88
                      },
                      {
                         "rgb":{
                            "red":255,
                            "green":229,
                            "blue":190
                         },
                         "percentage":0.54
                      },
                      {
                         "rgb":{
                            "red":243,
                            "green":109,
                            "blue":81
                         },
                         "percentage":0.16
                      }
                   ]
                },
                "ext":{
                   "mediaStats":{
                      "r":"Missing",
                      "ttl":-1
                   }
                }
             }
          ]
       },
       "source":"<a href=\"https://mobile.twitter.com\" rel=\"nofollow\">Twitter Web App</a>",
       "in_reply_to_status_id":"None",
       "in_reply_to_status_id_str":"None",
       "in_reply_to_user_id":"None",
       "in_reply_to_user_id_str":"None",
       "in_reply_to_screen_name":"None",
       "user_id":632528146,
       "user_id_str":"632528146",
       "geo":"None",
       "coordinates":"None",
       "place":"None",
       "contributors":"None",
       "is_quote_status":false,
       "retweet_count":36,
       "favorite_count":272,
       "reply_count":7,
       "quote_count":3,
       "conversation_id":1510022360304398348,
       "conversation_id_str":"1510022360304398348",
       "favorited":false,
       "retweeted":false,
       "possibly_sensitive":false,
       "possibly_sensitive_editable":true,
       "lang":"en",
       "supplemental_language":"None",
       "ext_edit_control":{
          "initial":{
             "edit_tweet_ids":[
                "1510022360304398348"
             ],
             "editable_until_msecs":"1648854160212",
             "edits_remaining":"5",
             "is_edit_eligible":true
          }
       },
       "ext":{
          "unmentionInfo":{
             "r":{
                "ok":{

                }
             },
             "ttl":-1
          },
          "superFollowMetadata":{
             "r":{
                "ok":{

                }
             },
             "ttl":-1
          },
          "editControl":{
             "r":{
                "ok":{
                   "initial":{
                      "editTweetIds":[
                         "1510022360304398348"
                      ],
                      "editableUntilMsecs":"1648854160212",
                      "editsRemaining":"5",
                      "isEditEligible":true
                   }
                }
             },
             "ttl":-1
          }
       }
    }

    Example user data:

    {
       "id":1433832091083546688,
       "id_str":"1433832091083546688",
       "name":"Lucholab",
       "screen_name":"Lucho_ArtArg",
       "location":"Santa Rosa, Argentina",
       "description":"#nfts #nft #digitalart #art #cryptoart  #Bsv #bitcoin #artoftheday #cryptoartist #blockchain #fabriikx \n#Token #KOINU",
       "url":"https://t.co/kkLKHdm0lH",
       "entities":{
          "url":{
             "urls":[
                {
                   "url":"https://t.co/kkLKHdm0lH",
                   "expanded_url":"https://Relayx.com/1lucholab",
                   "display_url":"Relayx.com/1lucholab",
                   "indices":[
                      0,
                      23
                   ]
                }
             ]
          },
          "description":{
             "urls":[

             ]
          }
       },
       "protected":false,
       "followers_count":1618,
       "fast_followers_count":0,
       "normal_followers_count":1618,
       "friends_count":4992,
       "listed_count":17,
       "created_at":"Fri Sep 03 16:40:00 +0000 2021",
       "favourites_count":9366,
       "utc_offset":"None",
       "time_zone":"None",
       "geo_enabled":true,
       "verified":false,
       "statuses_count":4711,
       "media_count":659,
       "lang":"None",
       "contributors_enabled":false,
       "is_translator":false,
       "is_translation_enabled":false,
       "profile_background_color":"F5F8FA",
       "profile_background_image_url":"None",
       "profile_background_image_url_https":"None",
       "profile_background_tile":false,
       "profile_image_url":"http://pbs.twimg.com/profile_images/1562104436436058112/cKZu88ST_normal.jpg",
       "profile_image_url_https":"https://pbs.twimg.com/profile_images/1562104436436058112/cKZu88ST_normal.jpg",
       "profile_banner_url":"https://pbs.twimg.com/profile_banners/1433832091083546688/1657936919",
       "profile_image_extensions_sensitive_media_warning":"None",
       "profile_image_extensions_media_availability":"None",
       "profile_image_extensions_alt_text":"None",
       "profile_image_extensions_media_color":{
          "palette":[
             {
                "rgb":{
                   "red":242,
                   "green":205,
                   "blue":127
                },
                "percentage":64.78
             },
             {
                "rgb":{
                   "red":231,
                   "green":136,
                   "blue":76
                },
                "percentage":7.82
             },
             {
                "rgb":{
                   "red":113,
                   "green":89,
                   "blue":65
                },
                "percentage":6.87
             },
             {
                "rgb":{
                   "red":189,
                   "green":159,
                   "blue":123
                },
                "percentage":3.81
             },
             {
                "rgb":{
                   "red":134,
                   "green":47,
                   "blue":237
                },
                "percentage":2.45
             }
          ]
       },
       "profile_image_extensions":{
          "mediaStats":{
             "r":{
                "missing":"None"
             },
             "ttl":-1
          }
       },
       "profile_banner_extensions_sensitive_media_warning":"None",
       "profile_banner_extensions_media_availability":"None",
       "profile_banner_extensions_alt_text":"None",
       "profile_banner_extensions_media_color":{
          "palette":[
             {
                "rgb":{
                   "red":128,
                   "green":204,
                   "blue":229
                },
                "percentage":16.64
             },
             {
                "rgb":{
                   "red":231,
                   "green":152,
                   "blue":241
                },
                "percentage":15.95
             },
             {
                "rgb":{
                   "red":203,
                   "green":165,
                   "blue":131
                },
                "percentage":11.7
             },
             {
                "rgb":{
                   "red":212,
                   "green":160,
                   "blue":182
                },
                "percentage":6.9
             },
             {
                "rgb":{
                   "red":127,
                   "green":224,
                   "blue":122
                },
                "percentage":4.07
             }
          ]
       },
       "profile_banner_extensions":{
          "mediaStats":{
             "r":{
                "missing":"None"
             },
             "ttl":-1
          }
       },
       "profile_link_color":"1DA1F2",
       "profile_sidebar_border_color":"C0DEED",
       "profile_sidebar_fill_color":"DDEEF6",
       "profile_text_color":"333333",
       "profile_use_background_image":true,
       "has_extended_profile":true,
       "default_profile":true,
       "default_profile_image":false,
       "pinned_tweet_ids":[
          1558597733765844992
       ],
       "pinned_tweet_ids_str":[
          "1558597733765844992"
       ],
       "has_custom_timelines":true,
       "can_dm":"None",
       "following":"None",
       "follow_request_sent":"None",
       "notifications":"None",
       "muting":"None",
       "blocking":"None",
       "blocked_by":"None",
       "want_retweets":"None",
       "advertiser_account_type":"none",
       "advertiser_account_service_levels":[

       ],
       "profile_interstitial_type":"",
       "business_profile_state":"none",
       "translator_type":"none",
       "withheld_in_countries":[

       ],
       "followed_by":"None",
       "ext_has_nft_avatar":false,
       "ext":{
          "superFollowMetadata":{
             "r":{
                "ok":{
                   "superFollowEligible":false,
                   "superFollowing":false,
                   "superFollowedBy":false,
                   "exclusiveTweetFollowing":false,
                   "privateSuperFollowing":false
                }
             },
             "ttl":-1
          },
          "highlightedLabel":{
             "r":{
                "ok":{

                }
             },
             "ttl":-1
          },
          "hasNftAvatar":{
             "r":{
                "ok":false
             },
             "ttl":-1
          }
       },
       "require_some_consent":false
    }

    """

    # ------------------------- Variables : 
    # header of csv
    # header = [
    #     'UserScreenName',  # screen_name
    #     'UserName',  # username
    #     'Timestamp',  #
    #     'Text',
    #     'Embedded_text',
    #     'Emojis',
    #     'Comments',  # nreplies
    #     'Likes',  # nlikes
    #     'Retweets',  # nretweets
    #     'Image link',
    #     'Tweet URL',
    #     'Hashtags',  # hashtags
    #     'Cashtags',  # cashtags
    # ]
    # list that contains all data 
    data = {
        'tweets': {},
        'users': {},
        'moments': {},
        'cards': {},
        'places': {},
        'media': {},
        'broadcasts': {},
        'topics': {},
        'lists': {}
    }
    # start scraping from <since> until <until>
    # add the <interval> to <since> to get <until_local> for the first refresh
    until_local = since + interval
    since_local = since
    # if <until>=None, set it to the actual date
    if until is None:
        until = datetime.datetime.today()
    # set refresh at 0. we refresh the page for each <interval> of time.
    refresh = 0

    # initiate the driver
    driver = init_driver(headless, proxy, remote=remote)

    # log search page for a specific <interval> of time and keep scrolling unltil scrolling stops or reach the <until>
    while until_local <= until:
        # number of scrolls
        scroll = 0
        # log search page between <since> and <until_local>
        path = log_search_page(driver=driver, words=words, since=since_local,
                               until_local=until_local, to_account=to_account,
                               from_account=from_account, mention_account=mention_account, hashtag=hashtag,
                               lang=lang,
                               display_type=display_type, filter_replies=filter_replies, proximity=proximity,
                               geocode=geocode, minreplies=minreplies, minlikes=minlikes, minretweets=minretweets)
        # number of logged pages (refresh each <interval>)
        refresh += 1
        # number of days crossed
        # days_passed = refresh * interval
        # last position of the page : the purpose for this is to know if we reached the end of the page or not so
        # that we refresh for another <since> and <until_local>
        last_position = driver.execute_script("return window.pageYOffset;")
        # should we keep scrolling ?
        scrolling = True
        print("looking for tweets between " + str(since) + " and " + str(until_local) + " ...")
        print(" path : {}".format(path))
        # number of tweets parsed
        tweet_parsed = 0
        # sleep
        sleep(random.uniform(0.5, 1.5))
        # start scrolling and get tweets
        driver, data, scrolling, tweet_parsed, scroll, last_position = \
            keep_scroling(driver, data, scrolling, tweet_parsed, limit, scroll, last_position)

        # keep updating <start date> and <end date> for every search
        since_local = since_local + interval
        until_local = until_local + interval

    # close the web driver
    driver.close()

    # trimming extra tweets
    date_format = '%a %b %d %H:%M:%S +0000 %Y'
    keys = list(data['tweets'].keys())
    for tweet_id in keys:
        tweet = data['tweets'][tweet_id]
        created_at = datetime.datetime.strptime(tweet['created_at'], date_format)
        if since > created_at or until < created_at:
            del data['tweets'][tweet_id]
            continue
        data['tweets'][tweet_id]['created_at'] = created_at

    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape tweets.')

    parser.add_argument('--words', type=str,
                        help='Queries. they should be devided by "//" : Cat//Dog.', default=None)
    parser.add_argument('--from_account', type=str,
                        help='Tweets from this account (example : @Tesla).', default=None)
    parser.add_argument('--to_account', type=str,
                        help='Tweets replyed to this account (example : @Tesla).', default=None)
    parser.add_argument('--mention_account', type=str,
                        help='Tweets mention a account (example : @Tesla).', default=None)
    parser.add_argument('--hashtag', type=str,
                        help='Hashtag', default=None)
    parser.add_argument('--until', type=str,
                        help='Max date for search query. example : %%Y-%%m-%%d.', required=True)
    parser.add_argument('--since', type=str,
                        help='Start date for search query. example : %%Y-%%m-%%d.', required=True)
    parser.add_argument('--interval', type=int,
                        help='Interval days between each start date and end date for search queries. example : 5.',
                        default=1)
    parser.add_argument('--lang', type=str,
                        help='Tweets language. example : "en" for english and "fr" for french.', default=None)
    parser.add_argument('--headless', type=bool,
                        help='Headless webdrives or not. True or False', default=False)
    parser.add_argument('--limit', type=int,
                        help='Limit tweets per <interval>', default=float("inf"))
    parser.add_argument('--display_type', type=str,
                        help='Display type of twitter page : Latest or Top', default="Top")
    parser.add_argument('--resume', type=bool,
                        help='Resume the last scraping. specify the csv file path.', default=False)
    parser.add_argument('--proxy', type=str,
                        help='Proxy server', default=None)
    parser.add_argument('--proximity', type=bool,
                        help='Proximity', default=False)
    parser.add_argument('--geocode', type=str,
                        help='Geographical location coordinates to center the search, radius. No compatible with proximity',
                        default=None)
    parser.add_argument('--minreplies', type=int,
                        help='Min. number of replies to the tweet', default=None)
    parser.add_argument('--minlikes', type=int,
                        help='Min. number of likes to the tweet', default=None)
    parser.add_argument('--minretweets', type=int,
                        help='Min. number of retweets to the tweet', default=None)

    args = parser.parse_args()

    words = args.words
    until = args.until
    since = args.since
    interval = args.interval
    lang = args.lang
    headless = args.headless
    limit = args.limit
    display_type = args.display_type
    from_account = args.from_account
    to_account = args.to_account
    mention_account = args.mention_account
    hashtag = args.hashtag
    resume = args.resume
    proxy = args.proxy
    proximity = args.proximity
    geocode = args.geocode
    minreplies = args.minreplies
    minlikes = args.minlikes
    minretweets = args.minlikes

    data = scrape(since=since, until=until, words=words, to_account=to_account, from_account=from_account,
                  mention_account=mention_account,
                  hashtag=hashtag, interval=interval, lang=lang, headless=headless, limit=limit,
                  display_type=display_type, resume=resume, proxy=proxy, filter_replies=False, proximity=proximity,
                  geocode=geocode, minreplies=minreplies, minlikes=minlikes, minretweets=minretweets)
