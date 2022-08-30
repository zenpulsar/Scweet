import json
import time
import zipfile
from io import StringIO, BytesIO
import os
import re
from time import sleep
import random
import chromedriver_autoinstaller
import geckodriver_autoinstaller
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities, Proxy
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import datetime
import pandas as pd
import platform
from selenium.webdriver.common.keys import Keys
# import pathlib

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from . import const
import urllib

from .const import get_username, get_password, get_email


# current_dir = pathlib.Path(__file__).parent.absolute()

def get_data(card, save_images=False, save_dir=None):
    """Extract data from tweet card"""
    image_links = []

    try:
        username = card.find_element(by=By.XPATH, value='.//span').text
    except:
        return

    try:
        handle = card.find_element(by=By.XPATH, value='.//span[contains(text(), "@")]').text
    except:
        return

    try:
        postdate = card.find_element(by=By.XPATH, value='.//time').get_attribute('datetime')
    except:
        return

    try:
        text = card.find_element(by=By.XPATH, value='.//div[2]/div[2]/div[1]').text
    except:
        text = ""

    try:
        embedded = card.find_element(by=By.XPATH, value='.//div[2]/div[2]/div[2]').text
    except:
        embedded = ""

    # text = comment + embedded

    try:
        reply_cnt = card.find_element(by=By.XPATH, value='.//div[@data-testid="reply"]').text
    except:
        reply_cnt = 0

    try:
        retweet_cnt = card.find_element(by=By.XPATH, value='.//div[@data-testid="retweet"]').text
    except:
        retweet_cnt = 0

    try:
        like_cnt = card.find_element(by=By.XPATH, value='.//div[@data-testid="like"]').text
    except:
        like_cnt = 0

    try:
        elements = card.find_elements(by=By.XPATH,
                                      value='.//div[2]/div[2]//img[contains(@src, "https://pbs.twimg.com/")]')
        for element in elements:
            image_links.append(element.get_attribute('src'))
    except:
        image_links = []

    # if save_images == True:
    #	for image_url in image_links:
    #		save_image(image_url, image_url, save_dir)
    # handle promoted tweets

    try:
        promoted = card.find_element(by=By.XPATH, value='.//div[2]/div[2]/[last()]//span').text == "Promoted"
    except:
        promoted = False
    if promoted:
        return

    # get a string of all emojis contained in the tweet
    try:
        emoji_tags = card.find_elements(by=By.XPATH, value='.//img[contains(@src, "emoji")]')
    except:
        return
    emoji_list = []
    for tag in emoji_tags:
        try:
            filename = tag.get_attribute('src')
            emoji = chr(int(re.search(r'svg\/([a-z0-9]+)\.svg', filename).group(1), base=16))
        except AttributeError:
            continue
        if emoji:
            emoji_list.append(emoji)
    emojis = ' '.join(emoji_list)

    # tweet url
    try:
        element = card.find_element(by=By.XPATH, value='.//a[contains(@href, "/status/")]')
        tweet_url = element.get_attribute('href')
    except:
        return

    tweet = (
        username, handle, postdate, text, embedded, emojis, reply_cnt, retweet_cnt, like_cnt, image_links, tweet_url)
    return tweet


def set_proxy_options(options, proxy: str):
    proxy = proxy.strip('https://').strip('http://').strip('/')
    proxy_data, proxy_url = proxy.split('@')
    proxy_host, proxy_port = proxy_url.split(':')
    proxy_user, proxy_pass = proxy_data.split(':')

    manifest_json = """
    {
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
            username: "%s",
            password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
    );
    """ % (proxy_host, proxy_port, proxy_user, proxy_pass)
    pluginfile = 'proxy_auth_plugin.zip'
    with zipfile.ZipFile(pluginfile, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
    options.add_extension(pluginfile)
    return options


def init_driver(headless=True, proxy=None, option=None, firefox=False, remote=None):
    """ initiate a chromedriver or firefoxdriver instance
        --option : other option to add (str)
    """

    options = ChromeOptions()

    if firefox:
        options = FirefoxOptions()

    if headless is True:
        print("Scraping on headless mode.")
        options.add_argument('--disable-gpu')
        options.headless = True
    else:
        options.headless = False
    options.add_argument('log-level=3')
    if proxy is not None:
        options = set_proxy_options(options, proxy)
        print("using proxy : ", proxy)
    if option is not None:
        options.add_argument(option)

    # disable show images
    # prefs = {"profile.managed_default_content_settings.images": 2}
    prefs = {'profile.default_content_setting_values': {
        'cookies': 2, 'images': 2,
        'plugins': 2, 'popups': 2, 'geolocation': 2,
        'notifications': 2, 'auto_select_certificate': 2,
        'fullscreen': 2,
        'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
        'media_stream_mic': 2, 'media_stream_camera': 2,
        'protocol_handlers': 2,
        'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2,
        'push_messaging': 2, 'ssl_cert_decisions': 2,
        'metro_switch_to_desktop': 2,
        'protected_media_identifier': 2, 'app_banner': 2,
        'site_engagement': 2,
        'durable_storage': 2
    }}
    options.add_experimental_option("prefs", prefs)

    options.add_argument('--no-sandbox')
    options.add_argument("disable-infobars")
    options.add_argument('--autoplay-policy=no-user-gesture-required')
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    capabilities = {
        "browserName": "chrome",
        'goog:loggingPrefs': {'performance': 'ALL'},
    }

    if remote:
        driver = webdriver.Remote(remote, desired_capabilities=capabilities, options=options)
    elif firefox:
        driver_path = geckodriver_autoinstaller.install()
        driver = webdriver.Firefox(options=options, executable_path=driver_path)
    else:
        driver_path = chromedriver_autoinstaller.install()
        driver = webdriver.Chrome(options=options, desired_capabilities=capabilities, executable_path=driver_path)

    driver.set_page_load_timeout(100)
    return driver


def log_search_page(driver, since, until_local, lang, display_type, words, to_account, from_account, mention_account,
                    hashtag, filter_replies, proximity,
                    geocode, minreplies, minlikes, minretweets):
    """ Search for this query between since and until_local"""
    # format the <from_account>, <to_account> and <hash_tags>
    from_account = "(from%3A" + from_account + ")%20" if from_account is not None else ""
    to_account = "(to%3A" + to_account + ")%20" if to_account is not None else ""
    mention_account = "(%40" + mention_account + ")%20" if mention_account is not None else ""
    hash_tags = "(%23" + hashtag + ")%20" if hashtag is not None else ""

    if words is not None:
        if len(words) == 1:
            words = "(" + str(''.join(words)) + ")%20"
        else:
            words = "(" + str('%20OR%20'.join(words)) + ")%20"
    else:
        words = ""

    if lang is not None:
        lang = 'lang%3A' + lang
    else:
        lang = ""

    until_local_unix = int(until_local.replace(tzinfo=datetime.timezone.utc).timestamp())
    since_unix = int(since.replace(tzinfo=datetime.timezone.utc).timestamp())

    until_local = "until%3A" + str(until_local_unix) + "%20"
    since = "since%3A" + str(since_unix) + "%20"

    if display_type == "Latest" or display_type == "latest":
        display_type = "&f=live"
    elif display_type == "Image" or display_type == "image":
        display_type = "&f=image"
    else:
        display_type = ""

    # filter replies
    if filter_replies == True:
        filter_replies = "%20-filter%3Areplies"
    else:
        filter_replies = ""
    # geo
    if geocode is not None:
        geocode = "%20geocode%3A" + geocode
    else:
        geocode = ""
    # min number of replies
    if minreplies is not None:
        minreplies = "%20min_replies%3A" + str(minreplies)
    else:
        minreplies = ""
    # min number of likes
    if minlikes is not None:
        minlikes = "%20min_faves%3A" + str(minlikes)
    else:
        minlikes = ""
    # min number of retweets
    if minretweets is not None:
        minretweets = "%20min_retweets%3A" + str(minretweets)
    else:
        minretweets = ""

    # proximity
    if proximity == True:
        proximity = "&lf=on"  # at the end
    else:
        proximity = ""

    path = 'https://twitter.com/search?q=' + words + from_account + to_account + mention_account + hash_tags + until_local + since + lang + filter_replies + geocode + minreplies + minlikes + minretweets + '&src=typed_query' + display_type + proximity
    driver.get(path)
    return path


def get_last_date_from_csv(path):
    df = pd.read_csv(path)
    return datetime.datetime.strftime(max(pd.to_datetime(df["Timestamp"])), '%Y-%m-%dT%H:%M:%S.000Z')


def log_in(driver, env, timeout=20, wait=4):
    email = get_email(env)  # const.EMAIL
    password = get_password(env)  # const.PASSWORD
    username = get_username(env)  # const.USERNAME

    driver.get('https://twitter.com/i/flow/login')

    email_xpath = '//input[@autocomplete="username"]'
    password_xpath = '//input[@autocomplete="current-password"]'
    username_xpath = '//input[@data-testid="ocfEnterTextTextInput"]'

    sleep(random.uniform(wait, wait + 1))

    # enter email
    email_el = driver.find_element(by=By.XPATH, value=email_xpath)
    sleep(random.uniform(wait, wait + 1))
    email_el.send_keys(email)
    sleep(random.uniform(wait, wait + 1))
    email_el.send_keys(Keys.RETURN)
    sleep(random.uniform(wait, wait + 1))
    # in case twitter spotted unusual login activity : enter your username
    if check_exists_by_xpath(username_xpath, driver):
        username_el = driver.find_element(by=By.XPATH, value=username_xpath)
        sleep(random.uniform(wait, wait + 1))
        username_el.send_keys(username)
        sleep(random.uniform(wait, wait + 1))
        username_el.send_keys(Keys.RETURN)
        sleep(random.uniform(wait, wait + 1))
    # enter password
    password_el = driver.find_element(by=By.XPATH, value=password_xpath)
    password_el.send_keys(password)
    sleep(random.uniform(wait, wait + 1))
    password_el.send_keys(Keys.RETURN)
    sleep(random.uniform(wait, wait + 1))


def keep_scroling(driver, data, scrolling, tweet_parsed, limit, scroll, last_position):
    """ scrolling function for tweets crawling"""

    while scrolling and tweet_parsed < limit:
        sleep(random.uniform(0.2, 0.6))
        # get the card of tweets
        # page_cards = driver.find_elements(by=By.XPATH,
        #                                   value='//article[@data-testid="tweet"]')  # changed div by article
        # for card in page_cards:
        #     tweet = get_data(card, save_images, save_images_dir)
        #     if tweet:
        #         # check if the tweet is unique
        #         tweet_id = ''.join(tweet[:-2])
        #         if tweet_id not in tweet_ids:
        #             tweet_ids.add(tweet_id)
        #             data.append(tweet)
        #             last_date = str(tweet[2])
        #             print("Tweet made at: " + str(last_date) + " is found.")
        #             writer.writerow(tweet)
        #             tweet_parsed += 1
        #             if tweet_parsed >= limit:
        #                 break

        logs_raw = driver.get_log("performance")
        logs = [json.loads(lr["message"])["message"] for lr in logs_raw]

        for log in logs:
            if log['method'] != 'Network.responseReceived':
                continue
            if 'adaptive.json' not in log['params']['response']['url']:
                continue
            request_id = log['params']['requestId']
            response = execute_remote_cdp_cmd(driver, "Network.getResponseBody", {"requestId": request_id})
            body = json.loads(response.get('body')).get('globalObjects')
            for key in data:
                data[key].update(body[key])

        scroll_attempt = 0
        while tweet_parsed < limit:
            # check scroll position
            scroll += 1
            print("scroll ", scroll)
            sleep(random.uniform(0.2, 0.6))
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            curr_position = driver.execute_script("return window.pageYOffset;")
            if last_position == curr_position:
                scroll_attempt += 1
                # end of scroll region
                if scroll_attempt >= 2:
                    scrolling = False
                    break
                else:
                    sleep(random.uniform(0.2, 0.6))  # attempt another scroll
            else:
                last_position = curr_position
                break
    return driver, data, scrolling, tweet_parsed, scroll, last_position


def get_users_follow(users, headless, env, follow=None, verbose=1, wait=2, limit=float('inf')):
    """ get the following or followers of a list of users """

    # initiate the driver
    driver = init_driver(headless=headless, env=env, firefox=True)
    sleep(wait)
    # log in (the .env file should contain the username and password)
    # driver.get('https://www.twitter.com/login')
    log_in(driver, env, wait=wait)
    sleep(wait)
    # followers and following dict of each user
    follows_users = {}

    for user in users:
        # if the login fails, find the new log in button and log in again.
        if check_exists_by_link_text("Log in", driver):
            print("Login failed. Retry...")
            login = driver.find_element_by_link_text("Log in")
            sleep(random.uniform(wait - 0.5, wait + 0.5))
            driver.execute_script("arguments[0].click();", login)
            sleep(random.uniform(wait - 0.5, wait + 0.5))
            sleep(wait)
            log_in(driver, env)
            sleep(wait)
        # case 2
        if check_exists_by_xpath('//input[@name="session[username_or_email]"]', driver):
            print("Login failed. Retry...")
            sleep(wait)
            log_in(driver, env)
            sleep(wait)
        print("Crawling " + user + " " + follow)
        driver.get('https://twitter.com/' + user + '/' + follow)
        sleep(random.uniform(wait - 0.5, wait + 0.5))
        # check if we must keep scrolling
        scrolling = True
        last_position = driver.execute_script("return window.pageYOffset;")
        follows_elem = []
        follow_ids = set()
        is_limit = False
        while scrolling and not is_limit:
            # get the card of following or followers
            # this is the primaryColumn attribute that contains both followings and followers
            primaryColumn = driver.find_element(by=By.XPATH, value='//div[contains(@data-testid,"primaryColumn")]')
            # extract only the Usercell
            page_cards = primaryColumn.find_elements(by=By.XPATH, value='//div[contains(@data-testid,"UserCell")]')
            for card in page_cards:
                # get the following or followers element
                element = card.find_element(by=By.XPATH, value='.//div[1]/div[1]/div[1]//a[1]')
                follow_elem = element.get_attribute('href')
                # append to the list
                follow_id = str(follow_elem)
                follow_elem = '@' + str(follow_elem).split('/')[-1]
                if follow_id not in follow_ids:
                    follow_ids.add(follow_id)
                    follows_elem.append(follow_elem)
                if len(follows_elem) >= limit:
                    is_limit = True
                    break
                if verbose:
                    print(follow_elem)
            print("Found " + str(len(follows_elem)) + " " + follow)
            scroll_attempt = 0
            while not is_limit:
                sleep(random.uniform(wait - 0.5, wait + 0.5))
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                sleep(random.uniform(wait - 0.5, wait + 0.5))
                curr_position = driver.execute_script("return window.pageYOffset;")
                if last_position == curr_position:
                    scroll_attempt += 1
                    # end of scroll region
                    if scroll_attempt >= 2:
                        scrolling = False
                        break
                    else:
                        sleep(random.uniform(wait - 0.5, wait + 0.5))  # attempt another scroll
                else:
                    last_position = curr_position
                    break

        follows_users[user] = follows_elem

    return follows_users


def check_exists_by_link_text(text, driver):
    try:
        driver.find_element_by_link_text(text)
    except NoSuchElementException:
        return False
    return True


def check_exists_by_xpath(xpath, driver):
    timeout = 3
    try:
        driver.find_element(by=By.XPATH, value=xpath)
    except NoSuchElementException:
        return False
    return True


def dowload_images(urls, save_dir):
    for i, url_v in enumerate(urls):
        for j, url in enumerate(url_v):
            urllib.request.urlretrieve(url, save_dir + '/' + str(i + 1) + '_' + str(j + 1) + ".jpg")


def execute_remote_cdp_cmd(driver, cmd, params):
    if params is None:
        params = {}
    resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
    url = driver.command_executor._url + resource
    body = json.dumps({'cmd': cmd, 'params': params})
    response = driver.command_executor._request('POST', url, body)
    return response.get('value')
