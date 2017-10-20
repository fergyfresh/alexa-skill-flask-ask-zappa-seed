# coding=utf-8

# alexa_skill.py
# By
#
# Alexa skill api

import logging
import os
import time
from datetime import datetime
from random import randint

import requests
from flask import Flask, render_template
from flask_ask import Ask, question, statement

__author__ = os.environ.get('author_name')
__email__ = os.environ.get('author_email')

app = Flask(__name__)
ask = Ask(app, '/')
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


# Session starter
#
# This intent is fired automatically at the point of launch (= when the session starts).
# Use it to register a state machine for things you want to keep track of, such as what the last intent was, so as to be
# able to give contextual help.

@ask.on_session_started
def start_session():
    """
    Fired at the start of the session, this is a great place to initialise state variables and the like.
    """
    logging.debug("Session started at {}".format(datetime.now().isoformat()))


# Launch intent
#
# This intent is fired automatically at the point of launch.
# Use it as a way to introduce your Skill and say hello to the user. If you envisage your Skill to work using the
# one-shot paradigm (i.e. the invocation statement contains all the parameters that are required for returning the
# result

@ask.launch
def handle_launch():
    """
    (QUESTION) Responds to the launch of the Skill with a welcome statement and a card.

    Templates:    
        * Initial statement: 'welcome'    
        * Reprompt statement: 'welcome_re'    
        * Card title: 'My Alexa Skill'    
        * Card body: 'welcome_card'    
    """

    welcome_text = render_template('welcome')
    welcome_re_text = render_template('welcome_re')
    welcome_card_text = render_template('welcome_card')

    return question(welcome_text).reprompt(welcome_re_text).standard_card(title="My Alexa Skill",
                                                                          text=welcome_card_text)


# Custom intents
#
# These intents are custom intents. We need to define utterances for custom intents.

@ask.intent('NewsIntent')
def handle_news():
    """
    (QUESTION) Handles the 'news' custom intention.
    
    This intent will provide user the latest news using RSS feed from Reddit, 
    and asks if user wants ti hear more news
    
    Examples:
        * whats the news
        
    Returns:
        News statements if news found from RSS
        No news statement if news not found from RSS 
        Error statement if can not process the request
    """
    card_title = render_template('card_title')

    try:
        news = get_reddit_headline()
        if news:
            news_text = render_template('news', news=news)
        else:
            news_text = render_template('no_news')
    except Exception as e:
        logging.error('Failed getting news from reddit')
        return error_prompt()

    return question(news_text).simple_card(card_title, news_text)


@ask.intent("YesIntent")
def yes_intent():
    """
    (QUESTION) Handles the 'Yes' answer for more news.
    
    When user asks on more news by saying 'Yes' to news question this intent will
    again call the news intent and fetches a random headline.
            
    Returns:
        News statements if news found from RSS
        No news statement if news not found from RSS 
        Error statement if can not process the request
    """
    headlines = handle_news()
    return headlines


@ask.intent("NoIntent")
def no_intent():
    """
    (STATEMENT) Handles the 'No' answer
                
    Returns:
        Bye statement
    """
    card_title = render_template('card_title')
    bye_text = render_template('bye')
    return statement(bye_text).simple_card(card_title, bye_text)


def get_rss_feed(url, is_verify=True):
    """Gets RSS feed
    
    Get the RSS Feed in json format
    
    Args:
        url: RSS feed url
        is_verify: verify the SSL certificate authority or not
    
    Returns: 
        RSS feed in json format
        
    Raises:
        Exception: An error occurred while getting the RSS feed
    """
    rss_json = None
    try:
        rss = requests.get(url, verify=is_verify)

        if rss is not None:
            rss_json = rss.json()
    except Exception as e:
        logging.error('Failed getting RSS feed')
        raise Exception('Failed getting RSS feed')

    return rss_json


def get_reddit_headline():
    """
    Gets the news headline from Reddit.
    It fetches 10 news headlines and picks one randomly
    
    Returns:
         headline from Reddit
    """
    reddit_username = os.environ.get('reddit_username')
    reddit_password = os.environ.get('reddit_password')

    user_pass_dict = {'user': reddit_username,
                      'passwd': reddit_password,
                      'api_type': 'json'}
    sess = requests.Session()
    sess.headers.update({'User-Agent': 'My Alexa Skill'})
    sess.post('https://www.reddit.com/api/login', data=user_pass_dict, verify=False)

    # Sometime login may fail, try increasing the sleep time
    time.sleep(1)

    url = os.environ.get('reddit_url')
    rss_json = get_rss_feed(url, False)
    titles = [str(i['data']['title']) for i in rss_json['data']['children']]

    # Read random number in range 1 to 10 and get the title from random number index
    num_facts = 10
    rand_index = randint(0, num_facts - 1)
    title = titles[rand_index]

    return title


def error_prompt():
    """
    (Question) handles if there is any error 
    
    Returns: 
        response error
    """
    card_title = render_template('card_title')
    question_text = render_template('error_prompt')
    return question(question_text).reprompt(question_text).simple_card(card_title, question_text)


# Built-in intents
#
# These intents are built-in intents. Conveniently, built-in intents do not need you to define utterances, so you can
# use them straight out of the box. Depending on whether you wish to implement these in your application, you may keep
#  or delete them/comment them out.
#
# More about built-in intents: http://d.pr/KKyx

@ask.intent('AMAZON.StopIntent')
def handle_stop():
    """
    (STATEMENT) Handles the 'stop' built-in intention.
    """
    farewell_text = render_template('stop_bye')
    return statement(farewell_text)


@ask.intent('AMAZON.CancelIntent')
def handle_cancel():
    """
    (STATEMENT) Handles the 'cancel' built-in intention.
    """
    farewell_text = render_template('cancel_bye')
    return statement(farewell_text)


@ask.intent('AMAZON.HelpIntent')
def handle_help():
    """
    (QUESTION) Handles the 'help' built-in intention.

    You can provide context-specific help here by rendering templates conditional on the help referrer.
    """

    help_text = render_template('help_text')
    return question(help_text)


@ask.intent('AMAZON.NoIntent')
def handle_no():
    """
    (?) Handles the 'no' built-in intention.
    """
    pass


@ask.intent('AMAZON.YesIntent')
def handle_yes():
    """
    (?) Handles the 'yes'  built-in intention.
    """
    pass


@ask.intent('AMAZON.PreviousIntent')
def handle_back():
    """
    (?) Handles the 'go back!'  built-in intention.
    """
    pass


@ask.intent('AMAZON.StartOverIntent')
def start_over():
    """
    (?) Handles the 'start over!'  built-in intention.
    """
    pass


@ask.intent('AMAZON.NavigateSettingsIntent')
def start_over():
    """
    (?) Handles the 'Navigate Settings'  built-in intention.
    """
    pass


@ask.intent('AMAZON.MoreIntent')
def start_over():
    """
    (?) Handles the 'More'  built-in intention.
    """
    pass


@ask.intent('AMAZON.PageDownIntent')
def start_over():
    """
    (?) Handles the 'page down'  built-in intention.
    """
    pass


@ask.intent('AMAZON.PageUpIntent')
def start_over():
    """
    (?) Handles the 'page up'  built-in intention.
    """
    pass


@ask.intent('AMAZON.ScrollRightIntent')
def start_over():
    """
    (?) Handles the 'scroll right'  built-in intention.
    """
    pass


@ask.intent('AMAZON.ScrollDownIntent')
def start_over():
    """
    (QUESTION) Handles the 'scroll down'  built-in intention.
    """
    pass


@ask.intent('AMAZON.ScrollLeftIntent')
def start_over():
    """
    (?) Handles the 'scroll left'  built-in intention.
    """
    pass


@ask.intent('AMAZON.ScrollUpIntent')
def start_over():
    """
    (?) Handles the 'scroll up'  built-in intention.
    """
    pass


@ask.intent('AMAZON.NextIntent')
def start_over():
    """
    (?) Handles the 'next'  built-in intention.
    """
    pass


# Ending session
#
# This intention ends the session.

@ask.session_ended
def session_ended():
    """
    Returns an empty for `session_ended`.

    .. warning::

    The status of this is somewhat controversial. The `official documentation`_ states that you cannot return a response
    to ``SessionEndedRequest``. However, if it only returns a ``200/OK``, the quit utterance (which is a default test
    utterance!) will return an error and the skill will not validate.

    """
    return statement("")


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)
