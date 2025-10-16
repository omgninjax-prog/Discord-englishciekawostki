# -*- coding: utf-8 -*-
"""
english_facts.py
Put in your repo and run with DISCORD_WEBHOOK_URL environment variable set
(GitHub Actions: export DISCORD_WEBHOOK_URL="${{ secrets.ENGLISH_WEBHOOK }}")
Script chooses a yearly permutation (seed = year) and sends the fact corresponding to the day of year.
Requires: requests
"""

import os
import datetime
import json
import requests
import random
import sys

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")

# Small pools to programmatically build 365 readable English facts about the language.
starters = [
    "Did you know", "Fun fact", "Language note", "Quick fact", "Word trivia",
    "Pronunciation tip", "Grammar note", "Etymology insight", "Vocabulary fact",
    "Historical note"
]

english_topics = [
    "word origins", "spelling quirks", "idioms", "phrasal verbs", "pronunciation",
    "grammar", "slang", "loanwords", "false friends", "word families",
    "register", "punctuation", "collocations", "etymology", "rhymes"
]

short_facts_base = [
    "The word 'set' has one of the highest number of different meanings in English.",
    "'OK' probably comes from a humorous misspelling 'oll korrect' from the 19th century.",
    "English has borrowed many words from Latin, French, German, and other languages.",
    "'Pneumonoultramicroscopicsilicovolcanoconiosis' is often cited as a very long English word.",
    "The letter 'J' was added to the Latin alphabet later than many other letters.",
    "Many English words used to have very different meanings centuries ago (e.g., 'nice').",
    "The Great Vowel Shift greatly changed English pronunciation in history.",
    "Many English irregular verbs date back to Old English patterns.",
    "English is considered stress-timed; unstressed syllables are often reduced.",
    "Homophones (e.g., 'there', 'their', 'they're') are a common spelling challenge."
]

# small extras to vary phrasing
extras = [
    "This often surprises learners.",
    "You can see it in modern vocabulary.",
    "Writers and speakers use it frequently.",
    "It appears in many idioms.",
    "It reflects the language's long history.",
    "It often causes spelling mistakes.",
    "It is a fun thing to notice in texts.",
    "Teachers often highlight this in lessons.",
    "It helps explain seemingly irregular spelling.",
    "It's useful for exam vocabulary."
]

def generate_365_english_facts():
    facts = []
    for s in short_facts_base:
        # ensure the base facts already are full messages
        facts.append(f"{s}.")
    i = 0
    # generate until 365 unique items
    while len(facts) < 365:
        starter = starters[i % len(starters)]
        topic = english_topics[i % len(english_topics)]
        base = short_facts_base[i % len(short_facts_base)]
        extra = extras[i % len(extras)]
        if i % 4 == 0:
            fact = f"{starter}: In {topic}, {base.lower()} {extra}"
        elif i % 4 == 1:
            fact = f"{starter}! {base} It relates to {topic}."
        elif i % 4 == 2:
            fact = f"{starter} — {base} This is a classic {topic} example."
        else:
            fact = f"{starter}: {base} {extra}"
        # clean
        fact = fact.strip()
        if not fact.endswith("."):
            fact += "."
        if fact not in facts:
            facts.append(fact)
        i += 1
        if i > 2000:
            break
    while len(facts) < 365:
        facts.append("Fun fact: keep exploring English every day!")
    return facts

FACTS = generate_365_english_facts()

def get_index_for_day(year, day_of_year):
    rng = random.Random(year)
    perm = list(range(len(FACTS)))
    rng.shuffle(perm)
    idx = perm[(day_of_year - 1) % len(FACTS)]
    return idx

def send_fact(fact):
    if not DISCORD_WEBHOOK_URL:
        print("Set environment variable DISCORD_WEBHOOK_URL (e.g. in GitHub Actions set secret ENGLISH_WEBHOOK).")
        return
    payload = {"content": f"💡 {fact}"}
    headers = {"Content-Type": "application/json"}
    r = requests.post(DISCORD_WEBHOOK_URL, data=json.dumps(payload), headers=headers)
    if r.status_code // 100 == 2:
        print("Sent successfully.")
    else:
        print("Send error:", r.status_code, r.text)

def main():
    arg_day = None
    if len(sys.argv) > 1:
        try:
            arg_day = int(sys.argv[1])
            if not (1 <= arg_day <= 366):
                arg_day = None
        except:
            arg_day = None

    now = datetime.datetime.now()
    year = now.year
    day_of_year = arg_day if arg_day is not None else now.timetuple().tm_yday
    idx = get_index_for_day(year, day_of_year)
    fact = FACTS[idx]
    print(f"Year={year}, day_of_year={day_of_year}, idx={idx}")
    send_fact(fact)

if __name__ == "__main__":
    main()
