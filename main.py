import discord
from discord.ext import commands
from discord.ext.commands.core import command
import os
from dotenv import load_dotenv

load_dotenv('.env')
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as req

import webscraper
rfd_web = webscraper.RedFlagDeals()

no_result_message = "No results found."

# Client
client = commands.Bot(command_prefix='--')
description = "Michael's RFD Bot"

# stores rfd posts
rfd_posts = []
# stores time of rfd post
post_time = []
# check if post is the first post
counter = 0


# add lines to string
def join_strings(current_string):
    return "\n".join(current_string)


# checks if message exceeds char limit of discord
def char_limit_exceeded(current_string):
    if len(current_string) >= 500:
        return True
    else:
        return False


# changes URL based on user's inputted category
def category_link(link):
    if link == "all":
        return "https://forums.redflagdeals.com/hot-deals-f9/"
    elif link == "apparel":
        return "https://forums.redflagdeals.com/hot-deals-f9/?c=12"
    elif link == "automotive":
        return "https://forums.redflagdeals.com/hot-deals-f9/?c=11"
    elif link == "beauty":
        return "https://forums.redflagdeals.com/hot-deals-f9/?c=10"
    elif link == "cellphones":
        return "https://forums.redflagdeals.com/hot-deals-f9/?c=5121"
    elif link == "computers":
        return "https://forums.redflagdeals.com/hot-deals-f9/?c=9"
    elif link == "entertainment":
        return "https://forums.redflagdeals.com/hot-deals-f9/?c=8"
    elif link == "finance":
        return "https://forums.redflagdeals.com/hot-deals-f9/?c=7"
    elif link == "groceries":
        return "https://forums.redflagdeals.com/hot-deals-f9/?c=53"
    elif link == "home":
        return "https://forums.redflagdeals.com/hot-deals-f9/?c=5"
    elif link == "kids":
        return "https://forums.redflagdeals.com/hot-deals-f9/?c=196"
    elif link == "restaurants":
        return "https://forums.redflagdeals.com/hot-deals-f9/?c=6"
    elif link == "smallbusiness":
        return "https://forums.redflagdeals.com/hot-deals-f9/?c=4"
    elif link == "sports":
        return "https://forums.redflagdeals.com/hot-deals-f9/?c=3"
    elif link == "travel":
        return "https://forums.redflagdeals.com/hot-deals-f9/?c=2"
    elif link == "videogames":
        return "https://forums.redflagdeals.com/hot-deals-f9/?c=5127"
    else:
        return "invalid"

def add_header(current_string, counter):
    if counter == 0:
        return "__**Red Flag Deals Forum Hot Deals:**__\n\n" + current_string + "** **" + "\n"
    else:
        return current_string


def get_score(post, index):
    return post[index].findAll("span", {"class": "total_count"})[0].text


def get_store(post, index):
    return post[index].findAll("a", {"class": "topictitle_retailer"})


def get_time(post, index):
    return post[index].findAll("ul", {"class": "thread-meta-small"})[0].li.text.replace('\n', '')


def get_title(post, index):
    return post[index].findAll("a", {"class": "topic_title_link"})[0].text.replace('\n', '')


def create_post(post, index, rfd_posts):
    score = get_score(post, index)
    store = get_store(post, index)
    time = get_time(post, index)
    title = get_title(post, index)

    if score == '':
        score = "0 SCORE"

    if not store:
        store = post[index].findAll("h3", {"class": "topictitle"})
        store = store[0].text.replace('\n', '')
        if store == title and score == '':
            score = "**" + "+0 SCORE" + "**"
            rfd_posts.append(score + " " + time + " " + "**" + store + "**" + "\n")
        elif score == '':
            score = "**" + "+0 SCORE" + "**"
            rfd_posts.append(score + " " + time + " " + "**" + store + "**" + "\n")
        else:
            rfd_posts.append("**" + score + "**" + " " + " " + time + " " + "**" + store + "**" + "\n")
    elif score == '':
        store = store[0].text.replace('\n', '')
        rfd_posts.append(time + " " + "**" + store + "**" + " " + "**" + title + "**" + "\n")
    else:
        store = store[0].text.replace('\n', '')
        rfd_posts.append(
            "**" + score + "**" + " " + time + " " + "**" + store + "**" + " " + "**" + title + "**" + "\n")
    print(rfd_posts)

    for i in rfd_posts:
        if 'Sponsored' in rfd_posts:
            return rfd_posts

    return rfd_posts

def create_post_search(post, index, rfd_posts):
    base_url = 'https://forums.redflagdeals.com/search.php?keywords='
    url_end = '&sf=titleonly'


# Commands
@client.command(name='command1')
async def command1(context):
    embed1 = discord.Embed(title="Title of Embed", description="Description of Embed", color=0xEB0801)
    embed1.add_field(name="Embed Name:", value="Michael's First Embed", inline=False)
    embed1.add_field(name="Date Released:", value="Jul 8 2021")
    embed1.set_author(name="Michael")
    embed1.set_footer(text="Footer for embed")

    await context.message.channel.send(embed=embed1)

@client.command(name='categories')
async def categories(context):
    embed1 = discord.Embed(title="Hot Deals Categories",
                           description="To use, do --hot_deals *CATEGORY*",
                           color=0xEB0801)
    embed1.add_field(name="Categories",
                     value="all, apparel, automotive, beauty, cellphones, computers, entertainment,"
                           "groceries, home, kids, restaurants, smallbusiness, sports, travel, videogames")
    # embed1.set_thumbnail(url="")
    embed1.set_footer(text="Footer for embed")

    await context.message.channel.send(embed=embed1)

@client.command(name='hot_deals')
async def hot_deals(context, category):

    rfd_posts = []
    link = category_link(category)

    if category=='':
        await context.message.channel.send("Invalid Category")
    elif link == "invalid":
        await context.message.channel.send("Invalid Category")
    else:
        # Sends message while fetching data
        await context.message.channel.send("Fetching")

        # Opening up connection, grabbing the page
        page = req(link)
        # Stores the content into a variable
        page_html = page.read()
        # Close the content
        page.close()
        # Html parser
        page_soup = soup(page_html, "html.parser")
        # Searching html with all divs with class "thread_info_title"
        posts = page_soup.findAll("div", {"class": "thread_info_title"})

        for index, value in enumerate(posts):
            global counter
            user_string = add_header(join_strings(rfd_posts), counter)

            if char_limit_exceeded(user_string):
                embedded = discord.Embed(title="Hot Deals",
                                         description="Most recent discounts", color=discord.Colour.red())
                embedded.set_thumbnail(url="https://pbs.twimg.com/profile_images/1185292632353857539/It_3dBVK_400x400.jpg")
                embedded.add_field(name="\u200b", value=user_string)
                await context.send(embed=embedded)
                rfd_posts = ["\n"]
                # adds 1 to the counter
                counter += 1

            if counter == 15:
                break

            else:
                orig_len = len(rfd_posts)
                rfd_posts = create_post(posts, index, rfd_posts)

                if len(rfd_posts) == orig_len:
                    counter += 0
                else:
                    counter += 1
        counter = 0
        return

@client.event
async def on_ready():
    # Functionality
    general_channel = client.get_channel(633832748800540677)

    await general_channel.send("Sup bro")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    message_content = message.content.lower()

    if message.content.startswith(f'--search'):

        key_words, search_words = rfd_web.key_words_search_words(message_content)
        result_links = rfd_web.search(key_words)
        links = rfd_web.send_link(result_links, search_words)

        links = links[:5]

        if len(links) > 0:
            for link in links:
                await message.channel.send("https://forums.redflagdeals.com/"+link)
        else:
            await message.channel.send(no_result_message)


    await client.process_commands(message)


# Run client on server
client.run(os.getenv('BOT_TOKEN'))
