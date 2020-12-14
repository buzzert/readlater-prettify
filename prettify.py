#!/usr/bin/python3.7

import email, email.policy
import re
import urllib
import uuid
import os, sys

import pdb

from bs4 import BeautifulSoup
from typing import TextIO

class EmailParseException(Exception):
    pass

class LinkNotFoundException(Exception):
    pass

def filter_email(eml: email.message.EmailMessage) -> str: 
    # Get plaintext part
    body = eml.get_body("plain")
    if body == None:
        raise EmailParseException()

    # Find a link in the body
    link_re = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))" 

    urls = re.findall(link_re, body.get_content())
    if len(urls) == 0:
        raise LinkNotFoundException()

    url: str = urls[0][0]

    # Download the contents at that URL with urllib
    with urllib.request.urlopen(url) as req:
        webpage = req.read()

        # Parse with BeautifulSoup
        bs = BeautifulSoup(webpage, features='lxml')
        content = bs.prettify()

        return content

    return url



# Parse email
eml = email.message_from_file(sys.stdin, policy=email.policy.default)

# Get content 
filtered_content = filter_email(eml)
eml.set_payload(filtered_content)
eml.set_type("text/html")

# For iPhone: Delete the originating message-id, because we don't want iOS Mail (or any other
# client) to correlate the sent message with this one, since the contents will be entirely different. 
del eml["Message-Id"]
eml["Message-Id"] = "<" + str(uuid.uuid1()) + ">"

sys.stdout.write(eml.as_string())

