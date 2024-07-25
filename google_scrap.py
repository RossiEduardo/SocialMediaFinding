from langchain_openai import OpenAI
from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_community.callbacks import get_openai_callback
import os
import csv
import re

os.environ["SERPER_API_KEY"] = "YOUR_API_KEY"
llm = OpenAI(openai_api_key='YOUR_API_KEY', temperature=0, top_p=1)


def extract_urls(text, social_medias):
    #Instagram : 0
    #Facebook: 1
    #Twitter: 2
    social_medias_urls = ["", "", ""]
    
    regex = re.compile(r'https?://\S+')

    urls = regex.findall(text)
    # if the url ends with . remove it
    urls = [url.rstrip('.,') for url in urls]

    for url in urls:
        for i, social_media in enumerate(social_medias):
            if social_media.lower() in url:
                social_medias_urls[i] = url

    return social_medias_urls


def get_social_medias(artist_name):
    search = GoogleSerperAPIWrapper(gl="ar", hl="en", autocorrect=True, engine="google")
    possible_social_medias = ["Instagram", "Facebook", "Twitter"]

    social_medias = {"artist_name": artist_name}
    links = {}
    for social_media in possible_social_medias:
        # results = search.results(f"{social_media} do artista {artist_name}")

        # Para artistas gringos:
        results = search.results(f"Artist {artist_name}'s {social_media} ")
        
        media_links_str = ""

        if 'answerBox' in results:
            try:
                answer_box = results['answerBox']
                media_links_str += f'{answer_box["link"]} '
            except Exception as e:
                pass

        for result in results['organic']:
            media_links_str += f'{result["link"]} '
       
        links[social_media] = media_links_str
    
    template = f'You are a helpful assistant that retrieves the correct Instagram, Facebook and Twitter accounts URL of an artist from a given lists of URLs. The corrects social medias accounts must contain a reference that they are a musician and usually appears first on each respect list. You never create a URL. Justify your choices'
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)

    human_template = '{text}'
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    chain = LLMChain(llm=llm, prompt=chat_prompt)

    response = chain.invoke({'text': f'The artist is named {artist_name} and this is the Instagram list: {links["Instagram"]}, this is the Facebook list: {links["Facebook"]} and this is the Twitter list: {links["Twitter"]}.'})
    # print(response['text'])
    urls = extract_urls(response['text'], possible_social_medias)
    social_medias["Instagram"] = urls[0]
    social_medias["Facebook"] = urls[1]
    social_medias["Twitter"] = urls[2]

    return social_medias



with open('artists.txt', 'r') as file:
    artists = [line.strip() for line in file.readlines()]

data = []
with get_openai_callback() as cb:
    for artist in artists:
        social_medias = get_social_medias(artist)
        data.append(social_medias)

    print(cb)

with open ('social_medias.csv', 'w') as csvfile:
    writer = csv.DictWriter (csvfile, fieldnames = data[0].keys())
    writer.writeheader()
    writer.writerows (data)
