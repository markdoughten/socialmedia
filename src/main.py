# custom libraries
from lib import topics
from lib import linkedin
import os
import time
import random
import pandas as pd
from openai import OpenAI
import requests
import base64

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_prompt(articles):

    prompt = "Create a professional LinkedIn post summarizing the following data and analytics news.\n\n"

    for article in articles:
        prompt += (
            f"Source: {article['source']}\n"
            f"Title: {article['title']}\n"
            f"Link: {article['link']}\n"
            f"Summary: {article['summary']}\n\n"
        )

    prompt += (
        "Write a concise LinkedIn post highlighting key insights. "
        "Use a professional tone and include 3 relevant hashtags."
    )

    return prompt

def generate_text(model, prompt):

    response = client.responses.create(
        model=model,
        input=prompt
    )

    text = response.output_text

    return text

def save_image(image, filename="../data/post_image.png"):
    with open(filename, "wb") as f:
        f.write(image)
    return filename

def generate_image(model, text):

    prompt = f"""
    LinkedIn professional illustration.

    Topic:
    {text}

    Style:
    - modern tech illustration
    - minimal corporate design
    - blue/white analytics dashboard theme
    - abstract data visualization elements
    - suitable for a LinkedIn business post
    """

    response = client.images.generate(
        model=model,
        prompt=prompt,
        size="1024x1024"
    )

    image = response.data[0].b64_json

    return base64.b64decode(image)

if __name__ == '__main__':
    
    os.makedirs("../data", exist_ok=True)
    random_select = True
    write = True
    text_model = 'gpt-5-2025-08-07'
    image_model = 'gpt-image-1'
    articles = topics.fetch_articles(limit_per_feed=1)
    upload = True
    save = True
    linkedin_api_key = os.getenv("LINKEDIN_ACCESS_TOKEN")
    
    prompt = generate_prompt(articles)
    text = generate_text(text_model, prompt)
    image = generate_image(image_model, text)

    if save:
        save_image(image)

    if upload:
        confirmation = linkedin.send_to_linkedin(linkedin_api_key, text, image)
        print(confirmation)
